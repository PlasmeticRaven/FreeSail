"""Scripted manoeuvres: tack, wear, heave to and fill away (spec §8.5).

Without a crew model these are timelines. Each script sets the helm targets
in ``ship.dyn`` (``helm_mode``, ``target_heading``, ``target_rudder``) and
moves the yards' ``brace_angle`` over time, then watches what the physics
does with the ship (her heading relative to the true wind, and her speed)
to decide how the manoeuvre ended. The physics is not touched: a script
gives orders and reads the compass, like an officer on deck.

Conventions used here (spec §4 and the package 3 Dynamics):

- ``rel`` is the true wind's bearing relative to the bow, positive when the
  wind is on the starboard side. ``sign`` is +1 on the starboard tack and
  -1 on the larboard tack.
- A yard's ``brace_angle`` is positive when it is braced up for the
  starboard tack (wind from starboard: the starboard yardarm forward, the
  lee yardarm aft) and negative for the larboard tack. So a yard braced
  sharp up on tack ``sign`` sits at ``sign * brace_limit``; braced aback for
  that tack it sits at ``-sign * brace_limit``; square is 0. The limit is
  always read from the spar, never assumed.
- "Close-hauled" for the true wind is six points (67.5 degrees) unless the
  ship carries ``ship.extra["close_hauled_angle"]`` in radians.

The timings each script uses come from the ``timing:`` block of its
evolution file, so they can be tuned without touching this code:

- ``brace_s``: seconds to swing a set of yards round (45 s in the spec).
- ``brace_rate_deg_s``: how fast yards follow the wind when wearing.
- ``stays_timeout_s``: how long a tacking ship may hang before she has
  missed stays.
- ``steady_deg``, ``steady_timeout_s``: when a manoeuvre counts as steady on
  its new course, and how long to wait for that before giving up waiting.
- ``wear_timeout_s``: how long a wear may take before it is abandoned.
- ``helm_deg``: the rudder angle for "helm a-lee" when heaving to.
- ``min_speed_kn``: below this, before her head is through the wind, a
  tacking ship has missed stays (0.8 kn in the spec).

Every script keeps its own ``status`` ("running", "done" or "failed") and,
when failed, a ``reason`` in words that the evolution's ``on_fail`` line
shows.
"""

from __future__ import annotations

import math
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.evolutions import trim as yard_trim
from freesail.ship import parts
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode, LineState, Sail, SailState, Spar, sync_catharpins
from freesail.ship.schema import YARD_LIKE_CLASSES

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

POINT = units.POINT


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


def sharp_up_targets(ship: Ship, head: list[Spar], after: list[Spar]) -> dict[str, float]:
    """Each yard's unsigned angle braced sharp up on a wind, the after yards
    `trim.AFTER_YARDS_SHARPER_DEG` sharper than the head yards where the limits
    allow (spec 3b §2.2, Fincham art. 94; `trim.stagger`): the tack's final trim."""
    sync_catharpins(ship)
    targets, _ = yard_trim.stagger(ship, {y.id: y.brace_limit for y in head + after})
    return targets


def bowlines_hauled(ship: Ship) -> list[str]:
    """The sails whose bowline is hauled out now, in the ship's order (spec 3b §4)."""
    out: list[str] = []
    for line in ship.lines.values():
        if line.bowline_hauled and line.of not in out:
            out.append(line.of)
    return out


def let_go_bowlines(ship: Ship) -> bool:
    """Let go every bowline hauled out, as the yards are swung (Luce 1884, ch. XXIV,
    'Tacking': "The lee braces and the bowlines are let go"). True if any was."""
    any_hauled = False
    for line in ship.lines.values():
        if line.bowline_hauled:
            line.state = LineState.FREE
            line.hauled = 0.0
            any_hauled = True
    return any_hauled


def steady_out_bowlines(ship: Ship, sail_ids: list[str], sign: float) -> bool:
    """Haul out the weather bowline, for the tack `sign` gives (+1 starboard), of each
    sail named that is drawing: "Haul taut the lifts and weather braces! Steady out the
    bo'lines!" (Luce 1884, ch. XXIV, 'Tacking', 'Wearing'). True if any was hauled."""
    side = "starboard" if sign > 0 else "larboard"
    any_hauled = False
    for sid in sail_ids:
        sail = ship.sails.get(sid)
        if (
            sail is None
            or sail.wrecked
            or sail.state not in (SailState.SET, SailState.GOOSE_WINGED)
        ):
            continue
        line = ship.line_of(sail, "bowline", side)
        if line is None or line.state is LineState.PARTED:
            continue
        line.state = LineState.BELAYED
        line.hauled = 1.0
        any_hauled = True
    return any_hauled


# The studding sails in before going about (milestone 3b, spec 3b §7). Luce's tacking and
# wearing begin with them in (RigGeometryNotes §5), and his words for taking them in with
# all hands are "Stand by to take in the stun'sails ...! Haul taut! IN STUN'SAILS ... Rig in
# and get alongside the booms ... make up and stow away the studding-sails" (Luce 1884,
# ch. XXVII, 'Going large under all sail, to round to under single reefs'; ch. XXXIV,
# 'Having a leading wind, to run in and anchor': "Haul taut! IN STUDDING-SAILS"). The time:
# the watch's own evolutions', all at once with all hands: lowered away and hauled down (90
# s, data/evolutions/take_in_studding.yaml) and the booms rigged in (40 s,
# rig_in_studdingsail_boom.yaml); the sails are made up while she goes about.
STUDDING_IN_S = 90.0 + 40.0
BOOMS_IN_S = 40.0  # the booms alone, their sails already in (rig_in_studdingsail_boom.yaml)
_STUDDING_ALOFT = (
    SailState.SET,
    SailState.GOOSE_WINGED,
    SailState.SHEETED,
    SailState.LOOSED,
    SailState.IN_THE_GEAR,
)


def studding_work(ship: Ship) -> tuple[list[Sail], list[Spar]]:
    """The studding sails aloft (set, or on their way up or down) and the booms rigged
    out: what a tack or a wear takes in first. Both empty: nothing to do."""
    sails = [
        s
        for s in ship.sails.values()
        if s.cls == "studding" and not s.wrecked and s.state in _STUDDING_ALOFT
    ]
    booms = [
        b
        for b in ship.spars.values()
        if b.cls in parts.RIGGED_IN_CLASSES and b.rigged_out and not b.wrecked
    ]
    return sails, booms


class StuddingSailsIn:
    """The first all-hands work of a tack or a wear when studding sails are set or their
    booms out: in studding-sails and rig in the booms, then the manoeuvre proper."""

    def __init__(self, ship: Ship):
        self.ship = ship
        self.sails, self.booms = studding_work(ship)
        self.duration_s = STUDDING_IN_S if self.sails else BOOMS_IN_S
        self.progress = 0.0

    @property
    def needed(self) -> bool:
        return bool(self.sails or self.booms)

    def begin_words(self) -> str:
        if self.sails:
            return "Stand by to take in the studding-sails. Haul taut! In studding-sails!"
        return "Rig in and get alongside the studding-sail booms."

    def advance(self, dt: float, factor: float) -> bool:
        """Work on; True when the sails are in and made up and the booms rigged in."""
        self.progress = min(1.0, self.progress + dt / (self.duration_s * factor))
        if self.progress < 1.0 - 1e-9:
            return False
        for sail in self.sails:
            if not sail.wrecked and sail.state in _STUDDING_ALOFT:
                sail.state = SailState.FURLED  # made up and stowed as she goes about
        for boom in self.booms:
            if not boom.wrecked:
                boom.rigged_out = False
        return True

    def end_words(self) -> str:
        if self.sails:
            return "In studding-sails; rigged in and got alongside the booms."
        return "Rigged in the studding-sail booms."

    def remaining_s(self) -> float:
        return (1.0 - self.progress) * self.duration_s


def close_hauled_true_angle(ship: Ship) -> float:
    """The angle off the true wind at which this ship sails close-hauled."""
    return float(ship.extra.get("close_hauled_angle", 6 * POINT))


def working_yards(ship: Ship) -> list[Spar]:
    """Every yard that can be braced: yard-like, not wrecked, not sent down."""
    return [
        s
        for s in ship.spars.values()
        if s.cls in YARD_LIKE_CLASSES and not s.wrecked and not s.sent_down
    ]


def _masts_with_yards(ship: Ship) -> list[Spar]:
    masts: list[Spar] = []
    for y in working_yards(ship):
        m = ship.mast_of(y)
        if m is not None and m not in masts:
            masts.append(m)
    return masts


def head_and_after_yards(ship: Ship) -> tuple[list[Spar], list[Spar]]:
    """Split the yards into the head yards (on the foremost mast that carries
    yards) and the after yards (all the rest). A ship whose yards are all on
    one mast, like a topsail schooner, has head yards only."""
    masts = _masts_with_yards(ship)
    if not masts:
        return [], []
    foremost = max(masts, key=lambda m: m.x_m)
    head = [y for y in working_yards(ship) if ship.mast_of(y) is foremost]
    after = [y for y in working_yards(ship) if ship.mast_of(y) is not foremost]
    return head, after


def after_square_yards(ship: Ship) -> list[Spar]:
    """The yards on the aftermost mast that carries yards (the mizzen on a
    frigate, the fore on a topsail schooner)."""
    masts = _masts_with_yards(ship)
    if not masts:
        return []
    aftermost = min(masts, key=lambda m: m.x_m)
    return [y for y in working_yards(ship) if ship.mast_of(y) is aftermost]


def yards_to_back(ship: Ship) -> list[Spar]:
    """The yards laid aback to heave to: those on the mast carrying the most
    square sail (Luce 1866 ch. XXVI: "the main topsail to the mast"). On a
    ship-rigged vessel that is the main; on a topsail schooner the fore, being
    the only mast with yards."""
    masts = _masts_with_yards(ship)
    if not masts:
        return []

    def square_area(mast: Spar) -> float:
        return sum(
            sl.area_m2
            for y in working_yards(ship)
            if ship.mast_of(y) is mast
            for sl in [ship.sail_of(y)]
            if sl is not None and sl.cls == "square"
        )

    chosen = max(masts, key=square_area)
    return [y for y in working_yards(ship) if ship.mast_of(y) is chosen]


def after_gaff_sails(ship: Ship) -> list:
    """The driver: gaff sails set on the aftermost lower mast (the spanker of a
    ship; a schooner's mainsail). Hove to with the main topsail aback it is
    brailed up, else it brings her head to wind and she gathers sternway
    (Luce 1866 ch. XXVI: 'regulate by easing off, or hauling aft, the spanker
    and jib sheets'; package 10 found the frigate with the spanker set lies 40
    degrees off with two knots of sternway, brailed up 55 to 60 degrees off
    with almost none). A schooner keeps her mainsail: it is her driving sail,
    not a driver, and without it she pays off broad and forereaches under her
    foresail and jibs (the period way for a fore-and-after is a jib sheet to
    windward, which the sail model cannot yet do)."""
    masts = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    if len(masts) < 3:
        return []
    aftermost = min(masts, key=lambda m: m.x_m)
    return [
        sl
        for sl in ship.sails.values()
        if sl.cls == "gaff" and sl.is_set and ship.mast_of(sl) is aftermost
    ]


def light_sails_forward_of(ship: Ship, backed: list[Spar]) -> list:
    """The topgallants and royals set on the masts forward of the backed
    yards' mast: the light head sails. Hove to they are clewed up (Luce 1866
    ch. XXVI: 'settle down the top-gallant sails and royals, or clew them
    up'); left set, the fore topgallant drives her ahead at a knot and a half
    and lies her a point too broad (package 10, truth 12)."""
    masts = [ship.mast_of(y) for y in backed]
    if not masts or any(m is None for m in masts):
        return []
    x_backed = max(m.x_m for m in masts)
    out = []
    for sl in ship.sails.values():
        if not (sl.is_set and sl.cls == "square"):
            continue
        yard = ship.yard_of(sl)
        above = ship.parent_of(yard) if yard is not None else None
        mast = ship.mast_of(sl)
        if (
            above is not None
            and above.cls in ("topgallant_mast", "royal_mast")
            and mast is not None
            and mast.x_m > x_backed
        ):
            out.append(sl)
    return out


def names_of_sails(ship: Ship, sails: list) -> str:
    """'the spanker', or 'the foresail and the mainsail', for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    return " and ".join(f"the {part_name(ship, sl.id)}" for sl in sails) if sails else "the sail"


def lowest_square_sails(ship: Ship) -> list:
    """The courses: square sails on yards that hang directly on a lower mast."""
    out = []
    for y in working_yards(ship):
        parent = ship.parent_of(y)
        sl = ship.sail_of(y)
        if parent is not None and parent.cls == "mast" and sl is not None and sl.cls == "square":
            out.append(sl)
    return out


def wind_rel(ship: Ship, wind: Wind) -> float:
    """The true wind's bearing from the bow, positive on the starboard side."""
    return units.relative_bearing(ship.dyn.heading, wind.direction_from)


def estimated_wind_from(ship: Ship) -> float:
    """Where the wind comes from, as the deck reads it before any tick has told
    the script the true wind: heading plus the apparent wind angle."""
    return units.wrap_2pi(ship.dyn.heading + ship.dyn.apparent_wind_angle)


def trim_angle(rel: float, limit: float, close_hauled: float) -> float:
    """The brace angle a yard wants for a given true wind bearing: sharp up
    (the limit) when by the wind, easing to square as the wind comes aft."""
    a = abs(rel)
    if a <= close_hauled:
        fraction = 1.0
    else:
        fraction = (math.pi - a) / (math.pi - close_hauled)
    return math.copysign(limit * fraction, rel) if rel != 0 else 0.0


def sail_name_on(ship: Ship, yards: list[Spar]) -> str:
    """The name of the principal sail on a group of yards, for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    for y in yards:
        sail = ship.sail_of(y)
        if sail is not None and sail.is_set:
            return part_name(ship, sail.id)
    for y in yards:
        sail = ship.sail_of(y)
        if sail is not None:
            return part_name(ship, sail.id)
    return part_name(ship, yards[0].id) if yards else "the yards"


class YardSwing:
    """Moves a set of yards from where they are to their targets over a fixed
    time, scaled by the weather factor each tick."""

    def __init__(self, yards: list[Spar], targets: list[float], duration_s: float):
        self.yards = yards
        self.starts = [y.brace_angle for y in yards]
        self.targets = targets
        self.duration_s = max(duration_s, 0.0)
        self.progress = 1.0 if not yards or self.duration_s <= 0 else 0.0
        if self.progress >= 1.0:
            self._apply()

    def advance(self, dt: float, factor: float) -> bool:
        if self.progress < 1.0:
            self.progress = min(1.0, self.progress + dt / (self.duration_s * factor))
            if self.progress >= 1.0 - 1e-9:
                self.progress = 1.0
            self._apply()
        return self.progress >= 1.0

    def _apply(self) -> None:
        for y, s, t in zip(self.yards, self.starts, self.targets, strict=True):
            y.brace_angle = s + (t - s) * self.progress

    @property
    def done(self) -> bool:
        return self.progress >= 1.0

    def remaining_s(self) -> float:
        return (1.0 - self.progress) * self.duration_s


def move_toward(yards: list[Spar], targets: list[float], max_step: float) -> bool:
    """Brace each yard toward its target, moving at most ``max_step`` radians
    this tick. Returns True when every yard is at its target."""
    settled = True
    for y, target in zip(yards, targets, strict=True):
        delta = target - y.brace_angle
        if abs(delta) <= max_step:
            y.brace_angle = target
        else:
            y.brace_angle += math.copysign(max_step, delta)
            settled = False
    return settled


def follow_wind(yards: list[Spar], rel: float, close_hauled: float, max_step: float) -> bool:
    """Brace each yard toward its trim for the wind (see ``trim_angle``)."""
    targets = [trim_angle(rel, y.brace_limit, close_hauled) for y in yards]
    return move_toward(yards, targets, max_step)


# ---------------------------------------------------------------------------
# The base class
# ---------------------------------------------------------------------------


class Script:
    """One scripted manoeuvre in progress. The runner calls ``check`` before
    starting, ``begin`` when the manoeuvre starts, and ``tick`` every tick."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        self.ship = ship
        self.params = params
        self.timing = timing
        self.status = "running"
        self.reason: str | None = None
        self.phase = "ready"
        self.t = 0.0

    def timing_value(self, key: str, default: float) -> float:
        return float(self.timing.get(key, default))

    def holds(self) -> set[str]:
        return {self.ship.name}

    def clears(self) -> set[str]:
        """The parts whose work in hand this script belays when it begins, rather than
        waiting for it or leaving it to run on (a send-down's sails: see `_Rig.held`)."""
        return set()

    def check(self, words: dict[str, Any]) -> str | None:
        """An extra precondition in code. Returns the reason it fails, or None."""
        return None

    def begin(self, words: dict[str, Any]) -> None:
        raise NotImplementedError

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        raise NotImplementedError

    def remaining_s(self) -> float:
        return 0.0

    def words(self) -> dict[str, Any]:
        return {}

    def data(self) -> dict[str, Any]:
        return {"phase": self.phase, "elapsed_s": round(self.t, 1)}

    def note(self, text: str, kind: str = "evolution.step") -> None:
        self.ship.note("routine", kind, text, self.ship.name)

    def fail(self, reason: str) -> None:
        self.status = "failed"
        self.reason = reason

    def finish(self) -> None:
        self.status = "done"


# ---------------------------------------------------------------------------
# Tack
# ---------------------------------------------------------------------------


class TackScript(Script):
    """Tack ship, after Luce 1866 ch. XXIV 'Tacking' and Lever 'Tacking expeditiously'.

    Helm's a-lee: the helm is ordered to a heading twelve points round,
    through the wind. When her head is within a point of the wind, "mainsail
    haul": the after yards swing to the new tack. When her head has passed
    through the wind, "let go and haul": the head yards follow, and the helm
    is ordered to the new close-hauled course. She is tacked when steady on
    it. If she loses her way (below ``min_speed_kn``) or hangs longer than
    ``stays_timeout_s`` before her head comes through, she has missed stays:
    the yards are squared, ready for a wear, and the helm put up to fall
    back on the old tack.
    """

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.through = False
        self.swing: YardSwing | None = None
        self.old_heading = ship.dyn.heading
        self.new_course = ship.dyn.heading
        self.t_steady = 0.0
        self.bowlined: list[str] = []  # sails whose bowlines were hauled out before going about
        self.studding: StuddingSailsIn | None = None

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.head + self.after}

    def begin(self, words: dict[str, Any]) -> None:
        # the studding sails first, if any are set or their booms out (spec 3b §7)
        studding = StuddingSailsIn(self.ship)
        if studding.needed:
            self.studding = studding
            self.phase = "in_studding_sails"
            self.note(studding.begin_words())
            return
        self._ready_about()

    def _ready_about(self) -> None:
        self.t = 0.0  # the stays are timed from "ready about"
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.bowlined = bowlines_hauled(self.ship)
        self.old_heading = dyn.heading
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(dyn.heading + self.sign * 12 * POINT)
        dyn.steady = False
        self.phase = "helm_down"
        self.note("Ready about. Helm's a-lee; eased off the head sheets.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        if self.phase == "in_studding_sails":
            assert self.studding is not None
            if self.studding.advance(dt, factor):
                self.note(self.studding.end_words())
                self._ready_about()
            return
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        if not self.through and self.sign * rel < 0 and abs(rel) < math.pi / 2:
            self.through = True
        if not self.through:
            if dyn.speed < units.knots_to_ms(self.timing_value("min_speed_kn", 0.8)):
                self._miss_stays("she lost her way before her head came through the wind")
                return
            if self.t > self.timing_value("stays_timeout_s", 180.0):
                self._miss_stays("she hung in stays and would not come round")
                return
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "helm_down":
            if abs(rel) <= POINT or self.through:
                self.phase = "mainsail_haul"
                # "The lee braces and the bowlines are let go, and the yards swung
                # around briskly by the weather braces" (Luce 1884, ch. XXIV, 'Tacking')
                if let_go_bowlines(self.ship):
                    self.note("Rise tacks and sheets. Mainsail haul; let go the bowlines.")
                else:
                    self.note("Rise tacks and sheets. Mainsail haul.")
                self.swing = YardSwing(
                    self.after, [-self.sign * y.brace_limit for y in self.after], brace_s
                )
        if self.phase == "mainsail_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor) and self.through:
                self.phase = "let_go_and_haul"
                self.note("Let go and haul.")
                # the head yards to the final trim: the after yards stand sharper
                # (spec 3b §2.2, Fincham art. 94)
                sharp = sharp_up_targets(self.ship, self.head, self.after)
                self.swing = YardSwing(
                    self.head, [-self.sign * sharp[y.id] for y in self.head], brace_s
                )
                self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
                dyn.target_heading = self.new_course
                dyn.steady = False
        elif self.phase == "let_go_and_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor):
                self.phase = "steady"
                self.t_steady = 0.0
                if steady_out_bowlines(self.ship, self.bowlined, -self.sign):
                    self.note("Haul taut the lifts and weather braces. Steady out the bowlines.")
        elif self.phase == "steady":
            self.t_steady += dt
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.target_heading = self.new_course
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            if error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0)) or (
                self.t_steady >= self.timing_value("steady_timeout_s", 120.0)
            ):
                self.finish()

    def _miss_stays(self, why: str) -> None:
        dyn = self.ship.dyn
        for y in self.head + self.after:
            y.brace_angle = 0.0
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = self.old_heading
        dyn.steady = False
        self.fail(why)

    def remaining_s(self) -> float:
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "in_studding_sails" and self.studding is not None:
            return self.studding.remaining_s() + 60.0 + 2 * brace_s + 30.0
        if self.phase == "helm_down":
            return 60.0 + 2 * brace_s + 30.0
        if self.phase == "mainsail_haul" and self.swing is not None:
            return self.swing.remaining_s() + brace_s + 30.0
        if self.phase == "let_go_and_haul" and self.swing is not None:
            return self.swing.remaining_s() + 30.0
        return 30.0

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d.update({"through_the_wind": self.through, "new_course": self.new_course})
        return d


# ---------------------------------------------------------------------------
# Wear
# ---------------------------------------------------------------------------


class WearScript(Script):
    """Wear ship, after Luce 1866 ch. XXIV 'Wearing'.

    Up helm: the helm is ordered dead before the wind and the after yards
    are braced in as she falls off, the head yards following once the wind
    is abaft the beam. When the wind is aft, the helm is ordered to the new
    close-hauled course and all yards are braced up as she comes to. She has
    worn when steady on it. Six to twelve minutes for a frigate is the truth
    to hit; the time is set by how fast the physics turns her, not by this
    script, which only sets the targets.
    """

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.new_course = ship.dyn.heading
        self.bowlined: list[str] = []  # sails whose bowlines were hauled out before wearing
        self.studding: StuddingSailsIn | None = None

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.head + self.after}

    def begin(self, words: dict[str, Any]) -> None:
        # the studding sails first, if any are set or their booms out (spec 3b §7)
        studding = StuddingSailsIn(self.ship)
        if studding.needed:
            self.studding = studding
            self.phase = "in_studding_sails"
            self.note(studding.begin_words())
            return
        self._up_helm()

    def _up_helm(self) -> None:
        self.t = 0.0  # the wear is timed from "up helm"
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(estimated_wind_from(self.ship) + math.pi)
        dyn.steady = False
        self.phase = "bear_away"
        # "Put the helm up! Clear away the bo'lines! and as she falls off, BRACE IN THE
        # AFTER YARDS!" (Luce 1884, ch. XXIV, 'Wearing')
        self.bowlined = bowlines_hauled(self.ship)
        if let_go_bowlines(self.ship):
            self.note(
                "Stand by to wear ship. Up helm; clear away the bowlines; brace in the after "
                "yards.",
                "helm.order",
            )
        else:
            self.note("Stand by to wear ship. Up helm; brace in the after yards.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        if self.phase == "in_studding_sails":
            assert self.studding is not None
            if self.studding.advance(dt, factor):
                self.note(self.studding.end_words())
                self._up_helm()
            return
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 1.0)) * dt / factor
        if self.t > self.timing_value("wear_timeout_s", 900.0):
            self.fail("she would not come round")
            return
        if self.phase == "bear_away":
            dyn.target_heading = units.wrap_2pi(wind.direction_from + math.pi)
            follow_wind(self.after, rel, ch, max_step)
            if abs(rel) > math.pi / 2:
                follow_wind(self.head, rel, ch, max_step)
            wind_aft = abs(rel) >= units.deg_to_rad(165.0)
            crossed = self.sign * rel < 0 and abs(rel) > math.pi / 2
            if wind_aft or crossed:
                self.phase = "come_to"
                self.note("Wind aft. Squared the head yards; hauled out and braced up.")
        if self.phase == "come_to":
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.target_heading = self.new_course
            dyn.steady = False
            sharp_up = -self.sign  # braced sharp up for the new tack
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
            # The after yards go sharp up at once to bring her to; the head yards
            # follow the wind, keeping their sails full, until she is by the wind.
            # (All yards end at their limits, as at milestone 2: spec 3b §2.2 asks
            # the after yards' trim of the tack's final trim and the orders only.)
            after_done = move_toward(
                self.after, [sharp_up * y.brace_limit for y in self.after], max_step
            )
            if steady:
                head_done = move_toward(
                    self.head, [sharp_up * y.brace_limit for y in self.head], max_step
                )
            else:
                follow_wind(self.head, rel, ch, max_step)
                head_done = False
            if steady and after_done and head_done:
                # "When by the wind, right the helm, trim the yards, Haul taut the lifts
                # and weather braces! Steady out the bowlines!" (Luce 1884, 'Wearing')
                if steady_out_bowlines(self.ship, self.bowlined, sharp_up):
                    self.note("Haul taut the lifts and weather braces. Steady out the bowlines.")
                self.finish()

    def remaining_s(self) -> float:
        first = self.studding.remaining_s() if self.studding is not None else 0.0
        return first + max(0.0, self.timing_value("wear_estimate_s", 480.0) - self.t)

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }


# ---------------------------------------------------------------------------
# Heave to and fill away
# ---------------------------------------------------------------------------


class HeaveToScript(Script):
    """Heave to (M2 simplified, after Luce 1866 ch. XXVI 'To heave to'): haul up
    the courses, lay the yards of the mast carrying the most square sail aback
    (the main topsail to the mast), the rest full, and put the helm a-lee. The
    physics does the rest. The backed yards are remembered in
    ``ship.extra["hove_to"]`` so that fill away can undo it. Hauling up the
    courses is done directly here rather than through their own evolutions,
    which is the M2 simplification; the crew system will replace it."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.swing: YardSwing | None = None

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards}

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.yards:
            return "She has no square yards to lay aback."
        if not any(s.is_set for y in self.yards for s in [self.ship.sail_of(y)] if s):
            return f"No sail is set on the {sail_name_on(self.ship, self.yards)} to lay aback."
        wanted = self.params.get("tack")
        if wanted in ("port",):
            wanted = "larboard"
        if wanted and wanted != self.ship.dyn.tack:
            return (
                f"She is on the {self.ship.dyn.tack} tack; "
                f"tack or wear first to heave to on the {wanted}."
            )
        if "hove_to" in self.ship.extra:
            return "She is hove to already."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.swing = YardSwing(
            self.yards,
            [-self.sign * y.brace_limit for y in self.yards],
            self.timing_value("brace_s", 45.0),
        )
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 15.0))
        dyn.steady = False
        self.phase = "back_after_yards"
        courses = [sl for sl in lowest_square_sails(self.ship) if sl.is_set]
        for sl in courses:
            sl.state = SailState.IN_THE_GEAR
        drivers = after_gaff_sails(self.ship)
        for sl in drivers:
            sl.state = SailState.IN_THE_GEAR
        if courses and drivers:
            self.note(f"Hauled up the courses; brailed up {names_of_sails(self.ship, drivers)}.")
        elif courses:
            self.note("Hauled up the courses.")
        elif drivers:
            self.note(f"Brailed up {names_of_sails(self.ship, drivers)}.")
        light = light_sails_forward_of(self.ship, self.yards)
        for sl in light:
            sl.state = SailState.IN_THE_GEAR
        if light:
            self.note(f"Clewed up {names_of_sails(self.ship, light)}.")
        self.note(f"Braced the {sail_name_on(self.ship, self.yards)} aback; helm a-lee.")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            self.ship.extra["hove_to"] = {"yards": [y.id for y in self.yards], "sign": self.sign}
            self.finish()

    def remaining_s(self) -> float:
        return self.swing.remaining_s() if self.swing else self.timing_value("brace_s", 45.0)

    def words(self) -> dict[str, Any]:
        return {"backed": sail_name_on(self.ship, self.yards)}


class FillAwayScript(Script):
    """Fill away after lying to (Luce 1866 ch. XXVI 'To fill away, after lying
    to with the main topsail to the mast': 'Right the helm, haul aft the head
    sheets ... As she falls off, brace up the after yards ... and trim to the
    course'). Hove to she lies close to the wind with little way or some
    sternway; braced full from there she is only taken aback. So first she is
    let fall off: the helm is kept a-lee while she has sternway (the rudder
    then throws her head off) and put up once she gathers headway, until her
    head is ``fill_off_deg`` off the true wind (far enough for the backed
    sails to fill when braced) or ``fall_off_timeout_s`` has passed. Lying
    hove to as heave_to leaves her, five points off, she needs no falling
    off and is braced at once. Then the backed yards are braced round
    full over ``brace_s`` and the helm ordered to the close-hauled course on the
    present tack. The courses and driver that heaving to hauled up stay as they
    are: setting them again is the captain's order."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        info = ship.extra.get("hove_to") or {}
        self.yards = [ship.spars[i] for i in info.get("yards", []) if i in ship.spars]
        self.sign = float(info.get("sign", 1.0 if ship.dyn.tack == "starboard" else -1.0))
        self.swing: YardSwing | None = None
        self.new_course = ship.dyn.heading

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards}

    def check(self, words: dict[str, Any]) -> str | None:
        if "hove_to" not in self.ship.extra:
            return "She is not hove to."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        ch = close_hauled_true_angle(self.ship)
        self.new_course = units.wrap_2pi(estimated_wind_from(self.ship) - self.sign * ch)
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 20.0))
        dyn.steady = False
        self.phase = "fall_off"
        self.note(
            "Hauled aft the head sheets; kept the helm a-lee to let her fall off.", "helm.order"
        )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        ch = close_hauled_true_angle(self.ship)
        self.new_course = units.wrap_2pi(wind.direction_from - self.sign * ch)
        if self.phase == "fall_off":
            helm = units.deg_to_rad(self.timing_value("helm_deg", 20.0))
            # with sternway the rudder works the other way: the helm a-lee throws
            # her head off; with headway it is the helm up that does it
            dyn.target_rudder = self.sign * helm if dyn.u < 0.0 else -self.sign * helm
            wanted = units.deg_to_rad(self.timing_value("fill_off_deg", 55.0))
            fallen_off = abs(wind_rel(self.ship, wind)) >= wanted
            if fallen_off or self.t >= self.timing_value("fall_off_timeout_s", 180.0):
                self.phase = "brace_full"
                what = sail_name_on(self.ship, self.yards)
                if self.t > 1.0:
                    self.note(f"Fallen off; braced the {what} full.")
                else:
                    self.note(f"Braced the {what} full.")
                self.swing = YardSwing(
                    self.yards,
                    [self.sign * y.brace_limit for y in self.yards],
                    self.timing_value("brace_s", 45.0),
                )
                dyn.helm_mode = HelmMode.HEADING
                dyn.target_heading = self.new_course
                dyn.target_rudder = 0.0
                dyn.steady = False
            return
        dyn.target_heading = self.new_course
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            self.ship.extra.pop("hove_to", None)
            self.finish()

    def remaining_s(self) -> float:
        brace_s = self.timing_value("brace_s", 45.0)
        if self.phase == "fall_off":
            return max(0.0, self.timing_value("fall_off_timeout_s", 180.0) - self.t) + brace_s
        return self.swing.remaining_s() if self.swing else brace_s

    def words(self) -> dict[str, Any]:
        return {"new_course": units.format_heading(self.new_course)}


# ---------------------------------------------------------------------------
# Milestone 3, package 19: the catalogue to forty
# ---------------------------------------------------------------------------
#
# The scripts below do crew work that one step list cannot express, because it
# changes several parts at once (every topgallant mast and the yards on it),
# keeps a count (the spare sails in the sail room) or steers the ship. Each
# follows the contract above: its timings come from the file's `timing:`
# block (`<phase>_s`), it keeps `status` and `reason`, it says which parts it
# `holds()`, and it reports its `data()`. It gives orders (helm targets, brace
# angles, sail states) and reads the compass; it never touches the physics.
#
# Work aloft: a phase named in the file's `params.aloft` list is work on the
# yards or in the tops, and `script.aloft` is true while it runs, so that the
# crew factor (spec M3 §3.3) can use the hands' skill aloft for it.

MAST_CLASSES = frozenset({"mast", "topmast", "topgallant_mast", "royal_mast"})
DRAWING = frozenset({SailState.SET, SailState.SHEETED, SailState.GOOSE_WINGED})
HANGING = frozenset({SailState.LOOSED, SailState.IN_THE_GEAR})
DEFAULT_SPARE_SAILS = parts.DEFAULT_SPARE_SAILS  # made-up sails when the file gives no stores


def _names(ship: Ship, parts: list) -> str:
    """'the fore royal', 'the fore royal and the main royal', for the log."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    names = [f"the {part_name(ship, p.id)}" for p in parts]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def _in_ship_order(ship: Ship, parts: list) -> list:
    order = {pid: i for i, pid in enumerate(ship.parts)}
    seen: dict[str, Any] = {}
    for p in parts:
        seen.setdefault(p.id, p)
    return sorted(seen.values(), key=lambda p: order.get(p.id, 0))


def _nearest_mast(ship: Ship, part: Any) -> Spar | None:
    """The mast, topmast, topgallant mast or royal mast a part is carried on."""
    for sp in ship.spar_chain(part):
        if sp.cls in MAST_CLASSES:
            return sp
    return None


def _chain_standing(ship: Ship, part: Any) -> bool:
    """True when nothing the part stands on is wrecked or sent down."""
    return not any(sp.wrecked or sp.sent_down for sp in ship.spar_chain(part))


def _spar_words(ship: Ship, spars: list[Spar], mast_cls: str) -> str:
    """The spars for the log, without the poles and booms that go with them:
    'the fore topgallant yard and the fore royal yard, with their studding sail
    booms', 'the fore topgallant mast and the main topgallant mast'."""
    heads = [s for s in spars if s.cls == mast_cls]
    if heads:
        return _names(ship, heads)
    yards = [s for s in spars if s.is_yard]
    booms = [s for s in spars if s.cls == "studdingsail_boom"]
    text = _names(ship, yards or spars)
    if yards and booms:
        text += ", with their studding sail booms"
    return text


def mast_inventory(ship: Ship) -> str:
    """What masts she has, for a refusal: 'the fore mast and fore topmast, and the
    main mast and main topmast'."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    groups: list[str] = []
    for lower in ship.spars.values():
        if lower.cls != "mast":
            continue
        chain = [lower] + [
            d for d in ship.dependents(lower) if isinstance(d, Spar) and d.cls in MAST_CLASSES
        ]
        names = [part_name(ship, m.id) for m in _in_ship_order(ship, chain)]
        groups.append(
            "the " + (names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1])
        )
    if not groups:
        return "she has no masts"
    return "her masts are " + (
        groups[0] if len(groups) == 1 else ", ".join(groups[:-1]) + ", and " + groups[-1]
    )


def spare_sails(ship: Ship) -> int:
    """The sails in the sail room, counted (spec M3 §6; spec 3b §6.3 keeps the count).

    The room itself is `parts.sail_room(ship)`: the ship file's list of sails
    (`crew.stores.sails`), or for a file that gives only `spare_sails` that many
    made-up sails that fit any yard, else DEFAULT_SPARE_SAILS of them. The count
    is also kept in ``ship.extra["spare_sails"]`` for anything that reads it."""
    return len(parts.sail_room(ship))


def _subject_sail(ship: Ship, params: dict[str, Any], words: dict[str, Any] | None):
    """The sail a sail script works on: `params["sail"]` (the verbs pass it), or
    the subject the runner names in its words."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    sid = params.get("sail")
    if isinstance(sid, str) and sid in ship.sails:
        return ship.sails[sid]
    name = (words or {}).get("subject")
    for sail in ship.sails.values():
        if part_name(ship, sail.id) == name:
            params["sail"] = sail.id
            return sail
    return None


class PhasedScript(Script):
    """Work done in named phases, one after another. Each phase takes
    ``timing[<phase>_s]`` seconds (else the class default) stretched by the
    factor the runner passes. A subclass lists its phases in ``begin`` with
    ``start_phases`` and says in ``end_phase`` what each one changes; a phase
    that has nothing to do is simply left out of the list."""

    DEFAULTS: dict[str, float] = {}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.plan: list[str] = []
        self.index = -1
        self.progress = 0.0
        self.aloft_phases = frozenset(str(p) for p in (params.get("aloft") or ()))

    @property
    def aloft(self) -> bool:
        """True while the phase under way is work aloft (the file's `params.aloft`)."""
        return self.phase in self.aloft_phases

    def phase_s(self, name: str) -> float:
        return self.timing_value(f"{name}_s", self.DEFAULTS.get(name, 60.0))

    def start_phases(self, phases: list[str]) -> None:
        self.plan = list(phases)
        self.index = -1
        self._next_phase()

    def _next_phase(self) -> None:
        self.index += 1
        self.progress = 0.0
        if self.index >= len(self.plan):
            self.phase = "done"
            self.finish()
            return
        self.phase = self.plan[self.index]
        self.start_phase(self.phase)

    def start_phase(self, name: str) -> None:
        """Called as a phase begins; nothing by default."""

    def end_phase(self, name: str) -> None:
        """Called as a phase ends: apply what it did."""

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        if self.status != "running" or not (0 <= self.index < len(self.plan)):
            return
        duration = self.phase_s(self.phase)
        if duration <= 0:
            self.progress = 1.0
        else:
            self.progress = min(1.0, self.progress + dt / (duration * factor))
        if self.progress >= 1.0 - 1e-9:
            self.end_phase(self.phase)
            if self.status == "running":
                self._next_phase()

    def remaining_s(self) -> float:
        if not (0 <= self.index < len(self.plan)):
            return 0.0
        this = (1.0 - self.progress) * self.phase_s(self.phase)
        return this + sum(self.phase_s(p) for p in self.plan[self.index + 1 :])

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["aloft"] = self.aloft
        return d


# ---------------------------------------------------------------------------
# Sending spars down and up: topgallant masts, their yards, topmasts
# ---------------------------------------------------------------------------


class _Rig:
    """The upper spars of one class across the ship: for each mast of the class
    (the *head*), the masts that go with it (a royal pole on a topgallant mast),
    the yards and booms they carry, and the sails bent or hanked to them."""

    def __init__(self, ship: Ship, mast_cls: str, poles: tuple[str, ...]):
        self.heads: list[Spar] = [
            s for s in ship.spars.values() if s.cls == mast_cls and not s.wrecked
        ]
        self.group: dict[str, list[Spar]] = {}
        self.yards: dict[str, list[Spar]] = {}
        self.sails: dict[str, list] = {}
        self.above: dict[str, list[Spar]] = {}
        for head in self.heads:
            deps = ship.dependents(head)
            group = [head] + [
                d for d in deps if isinstance(d, Spar) and d.cls in poles and not d.wrecked
            ]
            ids = {m.id for m in group}
            carried = [d for d in deps if isinstance(d, Sail) and not d.wrecked]
            yards = [
                d
                for d in deps
                if isinstance(d, Spar)
                and d.cls not in MAST_CLASSES
                and not d.wrecked
                and (_nearest_mast(ship, d) or head).id in ids
            ]
            sails = [
                s for s in carried if (m := _nearest_mast(ship, s)) is not None and m.id in ids
            ]
            self.group[head.id] = _in_ship_order(ship, group)
            self.yards[head.id] = _in_ship_order(ship, yards)
            self.sails[head.id] = _in_ship_order(ship, sails)
            self.above[head.id] = _in_ship_order(
                ship,
                [
                    d
                    for d in deps
                    if isinstance(d, Spar)
                    and d.cls in MAST_CLASSES
                    and d.id not in ids
                    and not d.wrecked
                ],
            )

    def held(self, sails: bool = True) -> set[str]:
        """What a send-down or sway-up holds against other evolutions: the masts,
        and the sails on them unless ``sails`` is false. Held, a sail being set
        is finished first and one ordered meanwhile waits. Sending down the
        topgallant masts holds the masts alone and belays the sail work in hand on
        those masts' sails instead of waiting for it (`Script.clears`): the masts
        come down, and a royal cannot be set on a mast being struck; what was
        belayed is refused when it takes up again on a spar sent down. The rest of
        the sail work in hand runs on: all hands is a pool action (the owner's
        ruling of 2026-09-29 at gate 4c, spec M3 §3.4). Not the yards: a brace on
        one is harmless, and one ordered after it is down is refused."""
        out: set[str] = set()
        for head in self.heads:
            out |= {p.id for p in self.group[head.id]}
            if sails:
                out |= {p.id for p in self.sails[head.id]}
        return out


class SendDownScript(PhasedScript):
    """Send down upper spars: the topgallant and royal yards, the topgallant
    masts with them, or the topmasts (Luce 1884, ch. XX 'To send down topgallant
    and royal yards and topgallant masts'; ch. XXIX 'Preparations for a Gale':
    "send down top-gallant masts ... as it eases her considerably").

    The file's params say which: ``mast`` (the class of mast, e.g.
    ``topgallant_mast``), ``poles`` (classes that go down with it, e.g. the
    royal mast), ``with_masts`` (false to send down only the yards on them),
    ``clear_away`` (true to clew up anything still set first; false to refuse
    instead) and the words for the log (``what``, ``doing``, ``first``).

    Phases: ``clear_away`` (clew up what is drawing on those spars),
    ``yards`` (the yards and booms sent down, their sails furled on them),
    ``mast`` (unfid and lower the masts). Everything sent down is marked
    ``sent_down``; the strain model then puts no load on it, the physics no
    windage, and nothing on it can be set until it is swayed up again."""

    DEFAULTS = {"clear_away": 60.0, "yards": 300.0, "mast": 420.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.mast_cls = str(params.get("mast") or "topgallant_mast")
        self.poles = tuple(str(p) for p in (params.get("poles") or ()))
        self.with_masts = bool(params.get("with_masts", True))
        self.clear_away = bool(params.get("clear_away", True))
        self.rig = _Rig(ship, self.mast_cls, self.poles)
        self.masts: list[Spar] = []
        self.yards: list[Spar] = []
        self.sails: list = []
        self.clew: list = []
        self.sent: list[Spar] = []

    def holds(self) -> set[str]:
        return {self.ship.name} | self.rig.held(bool(self.params.get("hold_sails", True)))

    def clears(self) -> set[str]:
        if bool(self.params.get("hold_sails", True)):
            return set()
        return self.rig.held(sails=True) - self.rig.held(sails=False)

    def _what(self) -> str:
        return str(self.params.get("what") or self.mast_cls.replace("_", " ") + "s")

    def _survey(self) -> None:
        """What is still aloft to be sent down, now."""
        self.rig = _Rig(self.ship, self.mast_cls, self.poles)
        heads = [h for h in self.rig.heads if not h.sent_down]
        self.masts, self.yards, self.sails = [], [], []
        for h in heads:
            if self.with_masts:
                self.masts += [m for m in self.rig.group[h.id] if not m.sent_down]
                self.sails += self.rig.sails[h.id]
                self.yards += [y for y in self.rig.yards[h.id] if not y.sent_down]
            else:
                self.yards += [y for y in self.rig.yards[h.id] if not y.sent_down]
                yard_ids = {y.id for y in self.yards}
                self.sails += [
                    s
                    for s in self.rig.sails[h.id]
                    if (chain := self.ship.spar_chain(s)) and chain[0].id in yard_ids
                ]
        self.clew = [s for s in self.sails if s.state in DRAWING]

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        what = self._what()
        verb = str(self.params.get("verb_words") or "send down")
        if not self.rig.heads:
            return f"She has no {what} to {verb}; {mast_inventory(ship)}."
        self._survey()
        if self.with_masts and not self.masts:
            return f"The {what} are sent down already."
        if not self.with_masts:
            if all(h.sent_down for h in self.rig.heads):
                masts = self.mast_cls.replace("_", " ") + "s"
                return f"The {masts} are on deck; there are no yards aloft on them to {verb}."
            if not self.yards:
                return f"The {what} are on deck already."
        standing = [
            m
            for h in self.rig.heads
            if not h.sent_down
            for m in self.rig.above[h.id]
            if not m.sent_down and m.parent == h.id  # the mast stepped on it, not its pole
        ]
        if standing:
            first = str(self.params.get("first") or "send down the masts above")
            return (
                f"{first[:1].upper()}{first[1:]} first: {_names(ship, standing)} "
                f"{'is' if len(standing) == 1 else 'are'} still aloft."
            )
        if not self.clear_away and self.clew:
            doing = str(self.params.get("doing") or f"{verb}ing the {what}")
            return (
                f"{_names(ship, self.clew)[:1].upper()}{_names(ship, self.clew)[1:]} "
                f"{'is' if len(self.clew) == 1 else 'are'} set; take "
                f"{'it' if len(self.clew) == 1 else 'them'} in before {doing}."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self._survey()
        phases = []
        if self.clew:
            phases.append("clear_away")
            self.note(f"Clew up {_names(self.ship, self.clew)}; stand by to send down.")
        if self.yards:
            phases.append("yards")
        if self.masts:
            phases.append("mast")
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "clear_away":
            for s in self.clew:
                if s.state in DRAWING:
                    s.state = SailState.IN_THE_GEAR
            self.note(f"Clewed up {_names(ship, self.clew)}; hands aloft to send down.")
        elif name == "yards":
            for y in self.yards:
                y.sent_down = True
                y.brace_angle = 0.0
            yard_ids = {y.id for y in self.yards}
            for s in self.sails:
                chain = ship.spar_chain(s)
                if chain and chain[0].id in yard_ids:
                    self._stow(s)
            self.sent += self.yards
            self.note(f"Sent down on deck {_spar_words(ship, self.yards, self.mast_cls)}.")
        elif name == "mast":
            for s in self.sails:
                self._stow(s)
            for m in self.masts:
                m.sent_down = True
            self.sent += self.masts
            self.note(f"Unfidded and lowered away {_spar_words(ship, self.masts, self.mast_cls)}.")

    @staticmethod
    def _stow(sail) -> None:
        if sail.state not in (SailState.UNBENT, SailState.BLOWN_OUT):
            sail.state = SailState.FURLED

    def words(self) -> dict[str, Any]:
        return {"sent": _spar_words(self.ship, self.sent, self.mast_cls)}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["sent_down"] = [p.id for p in self.sent]
        return d


class SwayUpScript(PhasedScript):
    """Sway up and fid what SendDownScript sent down: the topgallant masts and
    their yards, the yards alone, or the topmasts (Luce 1884, ch. XX 'To send up
    topgallant masts and topgallant and royal yards': "Sway aloft and fid ...
    Sway across! Bend the gear!"). Params as for SendDownScript; ``below``
    names the order that must come first when the mast below is struck.

    Phases: ``mast`` (sway aloft and fid) and ``yards`` (cross the yards,
    square). The sails come up furled on their yards, to be set by order."""

    DEFAULTS = {"mast": 480.0, "yards": 360.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.mast_cls = str(params.get("mast") or "topgallant_mast")
        self.poles = tuple(str(p) for p in (params.get("poles") or ()))
        self.with_masts = bool(params.get("with_masts", True))
        self.rig = _Rig(ship, self.mast_cls, self.poles)
        self.masts: list[Spar] = []
        self.yards: list[Spar] = []
        self.crossed: list[Spar] = []

    def holds(self) -> set[str]:
        return {self.ship.name} | self.rig.held(bool(self.params.get("hold_sails", True)))

    def clears(self) -> set[str]:
        if bool(self.params.get("hold_sails", True)):
            return set()
        return self.rig.held(sails=True) - self.rig.held(sails=False)

    def _what(self) -> str:
        return str(self.params.get("what") or self.mast_cls.replace("_", " ") + "s")

    def _survey(self) -> None:
        self.rig = _Rig(self.ship, self.mast_cls, self.poles)
        self.masts, self.yards = [], []
        for h in self.rig.heads:
            if self.with_masts:
                if not h.sent_down:
                    continue
                self.masts += [m for m in self.rig.group[h.id] if m.sent_down]
                self.yards += [y for y in self.rig.yards[h.id] if y.sent_down]
            elif not h.sent_down:
                self.yards += [y for y in self.rig.yards[h.id] if y.sent_down]

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        what = self._what()
        verb = str(self.params.get("verb_words") or "sway up")
        if not self.rig.heads:
            return f"She has no {what} to {verb}; {mast_inventory(ship)}."
        self._survey()
        if not self.with_masts and all(h.sent_down for h in self.rig.heads):
            masts = self.mast_cls.replace("_", " ") + "s"
            return f"The {masts} are on deck; sway them up before crossing the yards."
        if not self.masts and not self.yards:
            return f"The {what} are aloft already."
        struck = []
        for m in self.masts:
            below = ship.parent_of(m)
            if below is not None and below.id not in {x.id for x in self.masts}:
                if below.sent_down or below.wrecked:
                    struck.append(below)
        if struck:
            first = str(self.params.get("below") or "sway up the masts below")
            return (
                f"{first[:1].upper()}{first[1:]} first: {_names(ship, struck)} "
                f"{'is' if len(struck) == 1 else 'are'} struck."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self._survey()
        phases = []
        if self.masts:
            phases.append("mast")
            what = _spar_words(self.ship, self.masts, self.mast_cls)
            self.note(f"Man the mast-ropes; sway aloft {what}.")
        if self.yards:
            phases.append("yards")
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "mast":
            for m in self.masts:
                m.sent_down = False
            self.crossed += self.masts
            what = _spar_words(ship, self.masts, self.mast_cls)
            self.note(f"Swayed aloft and fidded {what}; set up the rigging.")
        elif name == "yards":
            for y in self.yards:
                y.sent_down = False
                y.brace_angle = 0.0
            self.crossed += self.yards
            self.note(f"Crossed {_spar_words(ship, self.yards, self.mast_cls)}; bent the gear.")

    def words(self) -> dict[str, Any]:
        return {"swayed": _spar_words(self.ship, self.crossed, self.mast_cls)}

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["swayed_up"] = [p.id for p in self.crossed]
        return d


# ---------------------------------------------------------------------------
# Bending, unbending and shifting a sail
# ---------------------------------------------------------------------------
#
# Milestone 3b (package 22, spec 3b §6.3): the sail room holds sails, not a count. A sail
# unbent goes down to it with its canvas number and condition; bending draws the best
# spare of the kind (`parts.SailRoom.choose`), or the one the order names:
#   params["canvas_no"]  a number: "bend the No. 1 fore topsail"
#   params["heavy"]      true: "shift the fore topsail for the heavy one"
#   params["for"]        another sail's id (or name) bent in the subject's place:
#                        "shift the spanker for the storm mizzen"
# A sail bent in place of another (`Sail.in_place_of`: the storm mizzen for the spanker, a
# schooner's storm trysail for her mainsail, her storm jib for the jib) is bent only when
# the other is unbent: the one refusal spec 3b §6.4 names.


def _sail_named(ship: Ship, value: Any) -> Sail | None:
    """A sail by id, alias or a sailor's name for it."""
    from freesail.evolutions.runner import part_name  # local import to avoid a cycle

    if not isinstance(value, str) or not value:
        return None
    if value in ship.sails:
        return ship.sails[value]
    target = ship.aliases.get(value)
    if target in ship.sails:
        return ship.sails[target]
    for sail in ship.sails.values():
        if part_name(ship, sail.id) == value:
            return sail
    return None


def _in_each_others_place(a: Sail, b: Sail) -> bool:
    return a.in_place_of == b.id or b.in_place_of == a.id


class _SailWork(PhasedScript):
    """A script on one sail, the evolution's subject. The verbs pass the sail's
    id as `params["sail"]`; without it the sail is found from the runner's
    words. Holds nothing beyond the sail, which the runner holds for it.

    `target` is the sail that is bent (the subject, or the one a shift names
    with `params["for"]`) and `spare` the sail chosen for it from the sail
    room, chosen at the check so that a refusal comes at once."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sail = _subject_sail(ship, params, None)
        self.target: Sail | None = None
        self.spare: parts.SpareSail | None = None

    def holds(self) -> set[str]:
        return set()

    def _find(self, words: dict[str, Any]) -> str | None:
        if self.sail is None:
            self.sail = _subject_sail(self.ship, self.params, words)
        if self.sail is None:
            return "Name the sail to work on."
        if not _chain_standing(self.ship, self.sail):
            return f"The {self._name()}'s yard or mast is wrecked or sent down."
        return None

    def _name(self, sail: Sail | None = None) -> str:
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        sail = sail if sail is not None else self.sail
        return part_name(self.ship, sail.id) if sail is not None else "sail"

    def room(self) -> parts.SailRoom:
        return parts.sail_room(self.ship)

    def _rival(self, sail: Sail, but: Sail | None = None) -> Sail | None:
        """A bent sail that holds this one's place (spec 3b §6.4), other than `but`."""
        for other in self.ship.sails.values():
            if other is sail or other is but or other.state is SailState.UNBENT:
                continue
            if _in_each_others_place(sail, other):
                return other
        return None

    def _choose(self, target: Sail) -> str | None:
        """Choose the sail to bend to `target` from the room, or say why there is none."""
        room = self.room()
        name = self._name(target)
        raw_no = self.params.get("canvas_no")
        canvas_no = int(raw_no) if isinstance(raw_no, int | float) and raw_no else None
        heavy = bool(self.params.get("heavy"))
        self.spare = room.choose(target.id, canvas_no=canvas_no, heavy=heavy)
        if self.spare is not None:
            return None
        fits = room.fitting(target.id)
        if not fits:
            return (
                f"There is no spare sail left in the sail room to bend in place of the "
                f"{name}; the sailmaker must make one first."
            )
        there = "; ".join(room.describe(s, target.id)[4:] for s in fits)
        if canvas_no is not None:
            return (
                f"There is no {name} of No. {canvas_no} canvas in the sail room; it holds {there}."
            )
        return f"There is no heavy-weather {name} in the sail room; it holds {there}."

    def _draw(self) -> bool:
        """Take the chosen sail out of the room (choosing again if another evolution has
        taken it meanwhile). False, with the evolution failed, when there is none left."""
        room = self.room()
        if self.spare is None or not any(s is self.spare for s in room.sails):
            reason = self._choose(self.target)
            if reason:
                self.fail(reason)
                return False
        room.take(self.spare)
        self.ship.extra["spare_sails"] = len(room)
        return True

    def _stow(self, sail: Sail) -> None:
        """The unbent sail goes down to the sail room with its canvas and condition."""
        room = self.room()
        room.stow(parts.SpareSail(kind=sail.id, canvas_no=sail.canvas_no, condition=sail.condition))
        self.ship.extra["spare_sails"] = len(room)

    def _bend_spare(self) -> None:
        target = self.target
        target.state = SailState.FURLED
        target.reefs = 0
        spare = self.spare
        target.bend_canvas(
            spare.canvas_no if spare is not None else None,
            spare.condition if spare is not None else 100.0,
        )

    def _spare_words(self) -> str:
        """'No. 1 canvas, new' for the sail chosen."""
        if self.spare is None or self.target is None:
            return "new"
        room = self.room()
        no = room.number_of(self.spare, self.target.id)
        cond = parts.condition_words(self.spare.condition)
        return f"No. {no} canvas, {cond}" if no is not None else cond

    def words(self) -> dict[str, Any]:
        n = spare_sails(self.ship)
        return {
            "spare_sails": f"{n} spare sail{'s' if n != 1 else ''}",
            "bent": self._name(self.target or self.sail),
            "canvas": self._spare_words(),
            # how a shift leaves the new sail: set in a drawing sail's place, else furled
            "left": "set" if getattr(self, "was_drawing", False) else "furled",
        }

    def data(self) -> dict[str, Any]:
        d = super().data()
        d["spare_sails"] = spare_sails(self.ship)
        if self.target is not None:
            d["bent"] = self.target.id
        if self.spare is not None:
            d["canvas_no"] = self.spare.canvas_no
            d["condition"] = self.spare.condition
        return d


class UnbendScript(_SailWork):
    """Unbend a sail from its yard, gaff or stay and send it down (Luce 1884, ch. XX 'To
    unbend sail': "Trice up! Lay out and unbend! ... Ease away! Lower
    together!"). Phases ``unbend`` (aloft: cast off the robands and head
    earings) and ``lower`` (on deck: lower it down by the buntlines and stow
    it). A sound sail goes back to the sail room with its canvas number and
    condition; a blown-out one is condemned and does not."""

    DEFAULTS = {"unbend": 180.0, "lower": 90.0}

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        sail = self.sail
        if sail.state is SailState.UNBENT:
            return f"The {self._name()} is unbent already; there is no sail on the yard."
        if sail.state in DRAWING:
            return f"The {self._name()} is set; take it in before unbending it."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["unbend", "lower"])

    def end_phase(self, name: str) -> None:
        if name == "lower":
            sound = self.sail.state is not SailState.BLOWN_OUT
            self.sail.state = SailState.UNBENT
            self.sail.reefs = 0
            if sound:
                self._stow(self.sail)
                self.note(f"Lowered the {self._name()} on deck and stowed it in the sail room.")
            else:
                self.note(f"Lowered the {self._name()} down on deck; the rags are condemned.")


class BendScript(_SailWork):
    """Bend a sail from the sail room to a bare yard, gaff or stay (Luce 1884, ch.
    XX 'Bending sail': "Sway aloft! ... Haul out! Lay out! And bring to!").
    Phases ``send_up`` (on deck: rouse the sail up from the sail room and sway
    it aloft) and ``bend`` (aloft: haul out the head, pass the robands and head
    earings, bend the gear). The sail bent is the best of its kind in the room
    or the one the order names, and brings its canvas number and condition to
    the part. It is left furled, to be set by order."""

    DEFAULTS = {"send_up": 120.0, "bend": 240.0}

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        if self.sail.state is not SailState.UNBENT:
            return (
                f"The {self._name()} is bent already ({self.sail.describe_state()}); "
                f"to change it for another, shift it."
            )
        rival = self._rival(self.sail)
        if rival is not None:
            return (
                f"The {self._name(rival)} is bent in the {self._name()}'s place; unbend it first, "
                f"or shift the {self._name(rival)} for the {self._name()}."
            )
        self.target = self.sail
        return self._choose(self.sail)

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["send_up", "bend"])

    def end_phase(self, name: str) -> None:
        if name == "send_up":
            if self._draw():
                self.note(
                    f"Roused up the {self._name()} from the sail room ({self._spare_words()}) "
                    f"and swayed it aloft."
                )
        elif name == "bend":
            self._bend_spare()


class ShiftScript(_SailWork):
    """Shift a sail: take it in if it is drawing, unbend it and bend another in
    its place, and set the new one if the old was drawing. Luce's shift begins
    with the sail set: 'To shift a topsail (by the wind, under all plain sail)'
    opens "Clew up! ... Settle away the topsail halliards ... Lay out! Furl
    and unbend! ... Lower the sail down to leeward by the buntlines. Send up
    the new sail ... Bring to and bend the sail ... Let fall! Sheet home!"
    (Luce 1866, ch. XXXII Shifting Sails and Spars), and 'To shift a jib'
    opens "Haul the sail down". So the phases are ``take_in`` (on deck, only
    for a drawing sail), ``unbend`` (aloft), ``send_up`` (on deck: the old sail
    down to the sail room, unless it is in rags, and the new one up), ``bend``
    (aloft) and ``set`` (only when the old sail was drawing; a furled or
    hauled-up sail is shifted where it hangs and the new one left furled, as
    the port drill has it). The new sail is the best of the kind in the room,
    or the one the order names: a number, the heavy one, or another sail bent
    in this one's place ("shift the spanker for the storm mizzen", Luce 1884
    ch. XXVII: "the storm mizzen is a substitute for the spanker"). Gate 4a's
    ruling (2026-09-27): shifting a sail is the whole of taking in and
    replacing it, so a set sail is not refused."""

    # take_in: the take-in evolutions' steps run 45 s (a head sail's downhaul) to
    # 105 s (a course clewed up and hauled up); 90 s is the gaff sail's, taken as the
    # middle. set: the set evolutions' hoist or sheet-home-and-hoist steps, 75 s to
    # 150 s; 120 s. Both judgement from data/evolutions/take_in_*.yaml, set_*.yaml.
    DEFAULTS = {"take_in": 90.0, "unbend": 180.0, "send_up": 150.0, "bend": 240.0, "set": 120.0}

    def check(self, words: dict[str, Any]) -> str | None:
        reason = self._find(words)
        if reason:
            return reason
        sail = self.sail
        if sail.state is SailState.UNBENT:
            return f"The {self._name()} is unbent; there is nothing to shift. Bend a new one."
        self.was_drawing = sail.state in DRAWING
        target = sail
        wanted = self.params.get("for")
        if wanted:
            target = _sail_named(self.ship, wanted)
            if target is None:
                return f"There is no sail called the {wanted} to shift the {self._name()} for."
            if not _in_each_others_place(sail, target):
                return (
                    f"The {self._name(target)} is not bent in the {self._name()}'s place; "
                    f"shift the {self._name()} for another of its kind."
                )
            if target.state is not SailState.UNBENT:
                return f"The {self._name(target)} is bent already."
            rival = self._rival(target, but=sail)
            if rival is not None:
                return (
                    f"The {self._name(rival)} is bent in the {self._name(target)}'s place; "
                    f"unbend it first."
                )
        self.target = target
        return self._choose(target)

    def begin(self, words: dict[str, Any]) -> None:
        drawing = getattr(self, "was_drawing", False)
        phases = ["unbend", "send_up", "bend"]
        if drawing:
            phases = ["take_in", *phases, "set"]
        self.start_phases(phases)

    def end_phase(self, name: str) -> None:
        if name == "take_in":
            # the sail hauled up in its gear or hauled down its stay, the hands standing
            # by to unbend it; the same state the take-in evolutions leave
            self.old_state = self.sail.state
            self.sail.state = SailState.IN_THE_GEAR
            verb = "Hauled down" if self.sail.cls == "jibheaded" else "Clewed up"
            self.note(f"{verb} the {self._name()} to shift it.")
        elif name == "unbend":
            if getattr(self, "old_state", None) is None:
                self.old_state = self.sail.state
            self.sail.state = SailState.UNBENT
            self.sail.reefs = 0
            self.note(f"Unbent the {self._name()} and lowered it down on deck.")
        elif name == "set":
            # the new sail let fall and set in the old one's place (Luce: "Let fall!
            # Sheet home!"); its sheet and yard stand as the old sail's did
            self.target.state = SailState.SET
            self.ship.note(
                "notable",
                "sail.set",
                f"Set the {self._name(self.target)} in the {self._name()}'s place.",
                self.target.id,
            )
        elif name == "send_up":
            # draw the new sail first, so the old one going down is not sent straight back up
            if not self._draw():
                return
            if getattr(self, "old_state", None) is not SailState.BLOWN_OUT:
                # the old sail is sound: it goes down to the sail room for the sailmaker
                self._stow(self.sail)
            self.note(f"Swayed aloft the {self._name(self.target)} ({self._spare_words()}).")
        elif name == "bend":
            self._bend_spare()


# ---------------------------------------------------------------------------
# Routine sail work for the whole ship: loosing to dry, furling everything
# ---------------------------------------------------------------------------


class LooseToDryScript(PhasedScript):
    """Loose sails to dry (Luce 1884, ch. XX 'To loose sail to the buntlines'
    (port routine): "Loose sail! ... Let fall! ... Topgallant-sails and royals
    hang down, their clews hauled up snug. The head sails are spread on the
    booms, heads of fore and aft sails hauled about half-way out"). Every
    furled sail on a standing spar, except the studding sails, which are
    stowed below, is loosed to hang in its gear. One phase, ``loose``
    (aloft). Refused when it blows more than ``max_wind_kn`` across the deck."""

    DEFAULTS = {"loose": 180.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sails = self._furled()

    def _furled(self) -> list:
        return [
            s
            for s in self.ship.sails.values()
            if s.state is SailState.FURLED
            and s.cls != "studding"
            and not s.wrecked
            and _chain_standing(self.ship, s)
        ]

    def holds(self) -> set[str]:
        return {self.ship.name} | {s.id for s in self.sails}

    def check(self, words: dict[str, Any]) -> str | None:
        limit = self.timing_value("max_wind_kn", 20.0)
        across = units.ms_to_knots(self.ship.dyn.apparent_wind_speed)
        if across > limit:
            return (
                f"It blows too hard to loose sails to dry: {across:.0f} knots across the deck; "
                f"wait for it to fall below {limit:.0f}."
            )
        self.sails = self._furled()
        if not self.sails:
            return "There is no furled sail to loose; they are all set, in the gear or below."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sails = self._furled()
        self.start_phases(["loose"])

    def end_phase(self, name: str) -> None:
        for s in self.sails:
            if s.state is SailState.FURLED:
                s.state = SailState.LOOSED
        self.note("Let fall; the sails hang in their gear to dry.")

    def words(self) -> dict[str, Any]:
        return {"count": len(self.sails)}


class FurlAllScript(PhasedScript):
    """Furl every sail (Luce 1884, ch. XX 'To furl sail': "Furl sail! ... Lay
    out! ... Furl away! ... Lay in! Down booms! Lay down from aloft!"). What is
    drawing is clewed up, hauled down or brailed first (phase ``clew_up``, on
    deck), then everything that hangs loose is furled or stowed (phase
    ``furl``, aloft). Studding sails are made up and sent below."""

    DEFAULTS = {"clew_up": 90.0, "furl": 240.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sails = self._loose()

    def _loose(self) -> list:
        return [
            s
            for s in self.ship.sails.values()
            if (s.state in DRAWING or s.state in HANGING)
            and not s.wrecked
            and _chain_standing(self.ship, s)
        ]

    def holds(self) -> set[str]:
        return {self.ship.name} | {s.id for s in self.sails}

    def check(self, words: dict[str, Any]) -> str | None:
        self.sails = self._loose()
        if not self.sails:
            return "Every sail is furled already."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sails = self._loose()
        drawing = [s for s in self.sails if s.state in DRAWING]
        self.start_phases((["clew_up"] if drawing else []) + ["furl"])

    def end_phase(self, name: str) -> None:
        if name == "clew_up":
            drawing = [s for s in self.sails if s.state in DRAWING]
            for s in drawing:
                s.state = SailState.IN_THE_GEAR
            self.note(f"Clewed up, hauled down and brailed up {_names(self.ship, drawing)}.")
        elif name == "furl":
            for s in self.sails:
                if s.state in DRAWING or s.state in HANGING:
                    s.state = SailState.FURLED

    def words(self) -> dict[str, Any]:
        return {"count": len(self.sails)}


# ---------------------------------------------------------------------------
# Ship handling: box-hauling, lying a-try, scudding, backing and filling
# ---------------------------------------------------------------------------


def _after_courses(ship: Ship) -> list:
    """The courses abaft the foremost mast that carries yards: the mainsail of a
    ship (Luce: "Up mainsail and spanker!")."""
    head, _after = head_and_after_yards(ship)
    head_ids = {y.id for y in head}
    return [
        sl
        for sl in lowest_square_sails(ship)
        if sl.is_set and ship.yard_of(sl) is not None and ship.yard_of(sl).id not in head_ids
    ]


def _after_sail(ship: Ship) -> list:
    """What is hauled up to box-haul: the courses abaft the head yards and the
    gaff sails set on the aftermost mast (Luce: "Up mainsail and spanker!"; on a
    schooner, whose after sail is her main gaff sail, that is lowered)."""
    masts = [sp for sp in ship.spars.values() if sp.cls == "mast" and not sp.wrecked]
    drivers: list = []
    if masts:
        aftermost = min(masts, key=lambda m: m.x_m)
        drivers = [
            sl
            for sl in ship.sails.values()
            if sl.cls == "gaff" and sl.is_set and ship.mast_of(sl) is aftermost
        ]
    return _after_courses(ship) + drivers


class BoxHaulScript(Script):
    """Box-haul her: wear short round by bracing the head yards abox (Luce 1884,
    ch. XXIV 'Box-hauling'; Luce 1866 ch. XXIV 'Box Hauling').

    ``luff``: "Put the helm down! ... Up mainsail and spanker!" The helm is put
    a-lee and the mainsail and spanker hauled up; she flies up toward the wind
    and loses her way. (``luff_first`` 0 skips this for wearing short round:
    the helm is put hard up at once.)
    ``box``: "Square away the after yards! Brace abox the head yards!" The
    after yards are squared and the head yards laid aback over ``brace_s``;
    the helm is left a-lee, which is right for the sternboard.
    ``fall_off``: she gathers sternway and her head falls off; "as the after
    sails lift, brace them in to keep them lifting", and the head yards are
    squared once the wind is abaft the beam. "As soon as the sails on the
    foremast give her headway, shift the helm."
    ``come_to``: with the wind across the stern, the mainsail and spanker are
    set again and she comes to on the new tack, the after yards sharp up and
    the head yards braced up as she comes, as at the end of a wear.

    She has box-hauled when steady on the new close-hauled course; she fails
    if it takes longer than ``box_timeout_s``."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.head, self.after = head_and_after_yards(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.hauled_up: list = []
        self.swing: YardSwing | None = None
        self.new_course = ship.dyn.heading
        self.sternway = False
        self.helm_shifted = False

    def holds(self) -> set[str]:
        held = {self.ship.name} | {y.id for y in self.head + self.after}
        held |= {s.id for s in _after_sail(self.ship)}
        return held

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.head:
            return "She has no head yards to brace abox."
        if "hove_to" in self.ship.extra:
            return "She is hove to; fill away first, or wear."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        helm = units.deg_to_rad(self.timing_value("helm_deg", 25.0))
        dyn.helm_mode = HelmMode.RUDDER
        dyn.steady = False
        if self.timing_value("luff_first", 1.0) > 0:
            dyn.target_rudder = self.sign * helm
            self.phase = "luff"
            self.note("Ready about. Helm's a-lee; checked the lee head braces.", "helm.order")
        else:
            dyn.target_rudder = -self.sign * helm
            self._box()

    def _box(self) -> None:
        """Up mainsail and spanker (as the sails lift, in box-hauling; at once, in
        wearing short round), square the after yards and brace the head yards abox."""
        self.phase = "box"
        self.hauled_up = _after_sail(self.ship)
        for sl in self.hauled_up:
            sl.state = SailState.IN_THE_GEAR
        up = ""
        if self.hauled_up:
            from freesail.evolutions.runner import part_name  # local import to avoid a cycle

            up = "Up " + " and ".join(part_name(self.ship, sl.id) for sl in self.hauled_up) + "! "
        targets = [-self.sign * y.brace_limit for y in self.head] + [0.0 for _ in self.after]
        self.swing = YardSwing(self.head + self.after, targets, self.timing_value("brace_s", 45.0))
        if self.after:
            text = "Square away the after yards! Brace abox the head yards!"
        else:
            text = "Brace abox the head yards!"
        self.note(up + text)

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        helm = units.deg_to_rad(self.timing_value("helm_deg", 25.0))
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 1.0)) * dt / factor
        if self.t > self.timing_value("box_timeout_s", 900.0):
            self._restore()
            self.fail("she would not come round")
            return
        if self.phase == "luff":
            stopped = dyn.u <= units.knots_to_ms(self.timing_value("stop_kn", 1.0))
            head_to_wind = abs(rel) <= POINT or self.sign * rel < 0
            if stopped or head_to_wind or self.t >= self.timing_value("luff_timeout_s", 120.0):
                self._box()
        if self.phase in ("box", "fall_off"):
            # sternway throws her head off with the helm a-lee; headway needs it up
            dyn.target_rudder = self.sign * helm if dyn.u < 0.0 else -self.sign * helm
            if dyn.u < 0.0:
                self.sternway = True
            elif self.sternway and not self.helm_shifted:
                self.helm_shifted = True
                self.note("She gathers headway. Shift the helm!", "helm.order")
        if self.phase == "box":
            assert self.swing is not None
            if self.swing.advance(dt, factor):
                self.phase = "fall_off"
                self.note("Her head falls off.")
        elif self.phase == "fall_off":
            follow_wind(self.after, rel, ch, max_step)
            if abs(rel) > math.pi / 2:
                follow_wind(self.head, rel, ch, max_step)
            crossed = self.sign * rel < 0 and abs(rel) > math.pi / 2
            if crossed or abs(rel) >= units.deg_to_rad(165.0):
                self.phase = "come_to"
                words = self._restore()
                self.note(f"Wind aft; braced up the after yards.{words}")
        if self.phase == "come_to":
            self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
            dyn.helm_mode = HelmMode.HEADING
            dyn.target_heading = self.new_course
            dyn.steady = False
            sharp_up = -self.sign
            error = abs(units.wrap_pi(dyn.heading - self.new_course))
            steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
            after_done = move_toward(
                self.after, [sharp_up * y.brace_limit for y in self.after], max_step
            )
            if steady:
                head_done = move_toward(
                    self.head, [sharp_up * y.brace_limit for y in self.head], max_step
                )
            else:
                follow_wind(self.head, rel, ch, max_step)
                head_done = False
            if steady and after_done and head_done:
                self.finish()

    def _restore(self) -> str:
        """Set again the mainsail and spanker that were hauled up for the evolution;
        the words for the log ("Main tack and sheet! Haul out the spanker!")."""
        from freesail.evolutions.runner import part_name  # local import to avoid a cycle

        words = []
        for sl in self.hauled_up:
            if sl.state is SailState.IN_THE_GEAR and _chain_standing(self.ship, sl):
                sl.state = SailState.SET
                name = part_name(self.ship, sl.id)
                if sl.cls == "square":
                    tack = name.replace("sail", "").replace("course", "").strip()
                    words.append(f"Board the {tack} tack and haul aft the sheet!")
                else:
                    words.append(f"Haul out the {name}!")
        self.hauled_up = []
        return (" " + " ".join(words)) if words else ""

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("box_estimate_s", 360.0) - self.t)

    def words(self) -> dict[str, Any]:
        old = "starboard" if self.sign > 0 else "larboard"
        new = "larboard" if self.sign > 0 else "starboard"
        return {
            "old_tack": old,
            "new_tack": new,
            "new_course": units.format_heading(self.new_course),
        }


def _topsails_on(ship: Ship, yards: list[Spar]) -> list:
    """The topsails among a mast's yards: square sails on yards that hang on a topmast."""
    out = []
    for y in yards:
        sl = ship.sail_of(y)
        parent = ship.parent_of(y)
        if sl is not None and sl.cls == "square" and parent is not None and parent.cls == "topmast":
            out.append(sl)
    return out


class LieATryScript(Script):
    """Lie a-try (lie to in a gale) under the close-reefed topsail of the mast
    that carries the most square sail and the staysails (Luce 1884, ch. XXIX
    'In a Gale': "The ship is now 'lying to' under close-reefed main topsail,
    fore storm staysail, and probably single reefed trysail").

    Phase ``hand_sails`` (``hand_s``): every other square sail is clewed up
    or hauled up, the studding sails taken in, the jibs hauled down (the ship
    file's ``jibs`` group) and the driver brailed up (``after_gaff_sails``: the
    spanker of a ship, which is far bigger than Luce's trysail and brings her
    head to the wind with sternway, as package 10 found for heaving to; a
    schooner keeps her gaff sails). The staysails stand. Phase ``brace``: the
    topsail yards braced sharp up for the tack she is on and the helm put a
    little a-lee (``helm_deg``); she comes up to about five points off and
    lies there, drifting to leeward. How much reef is in the topsail is the
    captain's order before this one. She is left lying to as ``heave_to``
    leaves her (``ship.extra["hove_to"]``, the topsail yards already full),
    so ``fill away`` ends it."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.topsails = _topsails_on(ship, self.yards)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.handed: list = []
        self.swing: YardSwing | None = None
        self.progress = 0.0

    def _to_hand(self) -> list:
        ship = self.ship
        keep = {s.id for s in self.topsails}
        jibs = set(ship.groups.get("jibs", []))
        out = []
        for sl in ship.sails.values():
            if sl.id in keep or not (sl.state in DRAWING or sl.state is SailState.LOOSED):
                continue
            if sl.cls in ("square", "studding") or sl.id in jibs:
                out.append(sl)
        drivers = {sl.id for sl in after_gaff_sails(ship)}
        out += [sl for sl in ship.sails.values() if sl.id in drivers and sl not in out]
        return out

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards} | {s.id for s in self._to_hand()}

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.topsails:
            return "She has no topsail to lie a-try under."
        if "hove_to" in self.ship.extra:
            return "She is lying to already."
        if not any(s.is_set for s in self.topsails):
            return (
                f"The {names_of_sails(self.ship, self.topsails)[4:]} is not set; set it, "
                f"close-reefed, to lie a-try under it."
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.sign = 1.0 if self.ship.dyn.tack == "starboard" else -1.0
        self.handed = self._to_hand()
        if self.handed:
            self.phase = "hand_sails"
            self.note(f"Hands to shorten sail: {_names(self.ship, self.handed)}.")
        else:
            self._brace()

    def _brace(self) -> None:
        self.phase = "brace"
        self.swing = YardSwing(
            self.yards,
            [self.sign * y.brace_limit for y in self.yards],
            self.timing_value("brace_s", 45.0),
        )
        dyn = self.ship.dyn
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = self.sign * units.deg_to_rad(self.timing_value("helm_deg", 5.0))
        dyn.steady = False
        self.note(
            f"Braced the {sail_name_on(self.ship, self.yards)} sharp up; helm a-lee.", "helm.order"
        )

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        if self.phase == "hand_sails":
            self.progress = min(
                1.0, self.progress + dt / (self.timing_value("hand_s", 120.0) * factor)
            )
            if self.progress >= 1.0 - 1e-9:
                for sl in self.handed:
                    if sl.state in DRAWING or sl.state is SailState.LOOSED:
                        sl.state = (
                            SailState.FURLED if sl.cls == "studding" else SailState.IN_THE_GEAR
                        )
                self.note(f"Took in {_names(self.ship, self.handed)}.")
                self._brace()
            return
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            # the topsail yard is already full: fill away braces it where it is
            yards = [y.id for y in self.yards]
            self.ship.extra["hove_to"] = {"yards": yards, "sign": self.sign, "how": "a-try"}
            self.finish()

    def remaining_s(self) -> float:
        brace = self.timing_value("brace_s", 45.0)
        if self.phase == "hand_sails":
            return (1.0 - self.progress) * self.timing_value("hand_s", 120.0) + brace
        return self.swing.remaining_s() if self.swing else brace

    def words(self) -> dict[str, Any]:
        return {"topsail": names_of_sails(self.ship, self.topsails)[4:]}


class ScudScript(Script):
    """Scud before a gale (Luce 1884, ch. XXIX 'To scud': "a vessel may scud
    before it, under such sail as the force of the wind will allow ... The best
    sails for scudding are a close-reefed main topsail and single or
    double-reefed foresail ... The fore topmast staysail should always be
    set"). The helm is put up and she is steered with the wind ``quarter_deg``
    on the weather quarter (not dead aft, where she would be brought by the
    lee); the driver is brailed up so that she will bear up; every yard is
    braced in to the wind as she goes off (``brace_rate_deg_s``). She is
    scudding when steady on that course with the yards trimmed, or after
    ``scud_timeout_s``. What sail she carries is the captain's order before
    this one; the helmsman keeps the course afterwards."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.course = ship.dyn.heading
        self.drivers: list = []

    def holds(self) -> set[str]:
        return (
            {self.ship.name}
            | {y.id for y in working_yards(self.ship)}
            | {s.id for s in after_gaff_sails(self.ship)}
        )

    def check(self, words: dict[str, Any]) -> str | None:
        if "hove_to" in self.ship.extra:
            return "She is lying to; fill away first, then bear up to scud."
        return None

    def _course_for(self, wind_from: float) -> float:
        q = units.deg_to_rad(self.timing_value("quarter_deg", 15.0))
        return units.wrap_2pi(wind_from - self.sign * (math.pi - q))

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.course = self._course_for(estimated_wind_from(self.ship))
        self.drivers = after_gaff_sails(self.ship)
        for sl in self.drivers:
            sl.state = SailState.IN_THE_GEAR
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = self.course
        dyn.steady = False
        self.phase = "bear_up"
        brailed = f"; brailed up {names_of_sails(self.ship, self.drivers)}" if self.drivers else ""
        self.note(f"Up helm{brailed}; brace in the yards as she goes off.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        dyn = self.ship.dyn
        rel = wind_rel(self.ship, wind)
        ch = close_hauled_true_angle(self.ship)
        max_step = units.deg_to_rad(self.timing_value("brace_rate_deg_s", 0.5)) * dt / factor
        self.course = self._course_for(wind.direction_from)
        dyn.target_heading = self.course
        yards = working_yards(self.ship)
        settled = follow_wind(yards, rel, ch, max_step)
        error = abs(units.wrap_pi(dyn.heading - self.course))
        steady = error <= units.deg_to_rad(self.timing_value("steady_deg", 5.0))
        if (steady and settled) or self.t >= self.timing_value("scud_timeout_s", 600.0):
            self.finish()

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("scud_estimate_s", 180.0) - self.t)

    def words(self) -> dict[str, Any]:
        side = "starboard" if self.sign > 0 else "larboard"
        return {"course": units.format_heading(self.course), "quarter": side}


class BackAndFillScript(Script):
    """Back and fill (Luce 1884, Appendix I 'In a Tideway', 'Backing and
    Filling': "by backing, filling, or shivering the main yard, either to keep
    in the best of the tide, or to make way for other vessels"; Luce 1866 ch.
    XXII). The yards of the mast that carries the most square sail are laid
    aback and she drops astern, then braced full and she forereaches, ``cycles``
    times, each board held for ``hold_s`` after a brace of ``brace_s``. As in
    heaving to, the courses are hauled up, the driver brailed up and the light
    sails forward clewed up first; the helm is a-lee (``helm_deg``) while she
    is aback and amidships while she forereaches. She ends with the yards
    aback, lying to as ``heave_to`` leaves her, so ``fill away`` stands her on.
    There are no tides yet (milestone 5), so what she keeps is her place, not a
    channel."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = yards_to_back(ship)
        self.sign = 1.0 if ship.dyn.tack == "starboard" else -1.0
        self.boards: list[str] = []
        self.board = -1
        self.swing: YardSwing | None = None
        self.hold = 0.0

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.yards}

    def check(self, words: dict[str, Any]) -> str | None:
        if not self.yards:
            return "She has no square yards to back and fill."
        if not any(s.is_set for y in self.yards for s in [self.ship.sail_of(y)] if s):
            return f"No sail is set on the {sail_name_on(self.ship, self.yards)} to back and fill."
        return None

    def begin(self, words: dict[str, Any]) -> None:
        info = self.ship.extra.get("hove_to")
        if info:
            self.sign = float(info.get("sign", self.sign))
        else:
            self.sign = 1.0 if self.ship.dyn.tack == "starboard" else -1.0
        cycles = max(1, int(round(self.timing_value("cycles", 2.0))))
        boards = ["back", "fill"] * cycles + ["back"]
        if info and info.get("yards"):
            boards = boards[1:]  # already aback: begin by filling
        self.boards = boards
        dyn = self.ship.dyn
        dyn.helm_mode = HelmMode.RUDDER
        dyn.target_rudder = 0.0
        dyn.steady = False
        self.ship.extra.pop("hove_to", None)
        # as for heaving to: the courses hauled up, the driver brailed up and the
        # light sails forward clewed up, or she flies up into the wind when backed
        handed = [sl for sl in lowest_square_sails(self.ship) if sl.is_set]
        handed += after_gaff_sails(self.ship) + light_sails_forward_of(self.ship, self.yards)
        for sl in handed:
            sl.state = SailState.IN_THE_GEAR
        if handed:
            self.note(f"Hauled up {_names(self.ship, handed)}.")
        self._next_board()

    def _next_board(self) -> None:
        self.board += 1
        if self.board >= len(self.boards):
            self.ship.extra["hove_to"] = {"yards": [y.id for y in self.yards], "sign": self.sign}
            self.finish()
            return
        self.phase = self.boards[self.board]
        aback = self.phase == "back"
        target = [(-self.sign if aback else self.sign) * y.brace_limit for y in self.yards]
        self.swing = YardSwing(self.yards, target, self.timing_value("brace_s", 45.0))
        self.hold = 0.0
        # the helm a-lee while she drops astern keeps her head from falling off
        # (sternway reverses the rudder); amidships while she forereaches
        helm = units.deg_to_rad(self.timing_value("helm_deg", 15.0))
        self.ship.dyn.target_rudder = self.sign * helm if aback else 0.0
        what = sail_name_on(self.ship, self.yards)
        if aback:
            self.note(f"Backed the {what}; her way checked.")
        else:
            self.note(f"Filled the {what}; she forereaches.")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        assert self.swing is not None
        if not self.swing.advance(dt, factor):
            return
        self.hold += dt
        last = self.board == len(self.boards) - 1
        if last or self.hold >= self.timing_value("hold_s", 90.0):
            self._next_board()

    def remaining_s(self) -> float:
        left = len(self.boards) - self.board - 1
        each = self.timing_value("brace_s", 45.0) + self.timing_value("hold_s", 90.0)
        now = self.swing.remaining_s() if self.swing else 0.0
        return now + max(0, left) * each

    def words(self) -> dict[str, Any]:
        return {"backed": sail_name_on(self.ship, self.yards)}


SCRIPTS: dict[str, type[Script]] = {
    "tack": TackScript,
    "wear": WearScript,
    "heave_to": HeaveToScript,
    "fill_away": FillAwayScript,
    "send_down": SendDownScript,
    "sway_up": SwayUpScript,
    "unbend": UnbendScript,
    "bend": BendScript,
    "shift": ShiftScript,
    "loose_to_dry": LooseToDryScript,
    "furl_all": FurlAllScript,
    "boxhaul": BoxHaulScript,
    "lie_a_try": LieATryScript,
    "scud": ScudScript,
    "back_and_fill": BackAndFillScript,
}
