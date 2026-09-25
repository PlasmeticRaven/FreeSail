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
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode, Spar
from freesail.ship.schema import YARD_LIKE_CLASSES

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

POINT = units.POINT


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------


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
    """The yards on the aftermost mast that carries yards: the ones laid aback
    to heave to (the mizzen topsail yard on a frigate, the fore topsail yard
    on a topsail schooner)."""
    masts = _masts_with_yards(ship)
    if not masts:
        return []
    aftermost = min(masts, key=lambda m: m.x_m)
    return [y for y in working_yards(ship) if ship.mast_of(y) is aftermost]


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

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.head + self.after}

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        self.old_heading = dyn.heading
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(dyn.heading + self.sign * 12 * POINT)
        dyn.steady = False
        self.phase = "helm_down"
        self.note("Ready about. Helm's a-lee; eased off the head sheets.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
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
                self.note("Rise tacks and sheets. Mainsail haul.")
                self.swing = YardSwing(
                    self.after, [-self.sign * y.brace_limit for y in self.after], brace_s
                )
        if self.phase == "mainsail_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor) and self.through:
                self.phase = "let_go_and_haul"
                self.note("Let go and haul.")
                self.swing = YardSwing(
                    self.head, [-self.sign * y.brace_limit for y in self.head], brace_s
                )
                self.new_course = units.wrap_2pi(wind.direction_from + self.sign * ch)
                dyn.target_heading = self.new_course
                dyn.steady = False
        elif self.phase == "let_go_and_haul":
            assert self.swing is not None
            if self.swing.advance(dt, factor):
                self.phase = "steady"
                self.t_steady = 0.0
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

    def holds(self) -> set[str]:
        return {self.ship.name} | {y.id for y in self.head + self.after}

    def begin(self, words: dict[str, Any]) -> None:
        dyn = self.ship.dyn
        self.sign = 1.0 if dyn.tack == "starboard" else -1.0
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(estimated_wind_from(self.ship) + math.pi)
        dyn.steady = False
        self.phase = "bear_away"
        self.note("Stand by to wear ship. Up helm; brace in the after yards.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
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

    def remaining_s(self) -> float:
        return max(0.0, self.timing_value("wear_estimate_s", 480.0) - self.t)

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
    """Heave to (M2 simplified, after Luce 1866 ch. XXVI 'To heave to'): lay the
    aftermost square yards aback, the rest full, and put the helm a-lee. The
    physics does the rest. The backed yards are remembered in
    ``ship.extra["hove_to"]`` so that fill away can undo it."""

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.yards = after_square_yards(ship)
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
    """Fill away after lying to (Luce 1866 ch. XXVI 'To fill away'): right the
    helm, order the close-hauled course on the present tack, and brace the
    backed yards round full."""

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
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = self.new_course
        dyn.target_rudder = 0.0
        dyn.steady = False
        self.swing = YardSwing(
            self.yards,
            [self.sign * y.brace_limit for y in self.yards],
            self.timing_value("brace_s", 45.0),
        )
        self.phase = "brace_full"
        self.note("Righted the helm; hauled aft the head sheets.", "helm.order")

    def tick(self, dt: float, wind: Wind, factor: float) -> None:
        self.t += dt
        ch = close_hauled_true_angle(self.ship)
        self.new_course = units.wrap_2pi(wind.direction_from - self.sign * ch)
        self.ship.dyn.target_heading = self.new_course
        assert self.swing is not None
        if self.swing.advance(dt, factor):
            self.ship.extra.pop("hove_to", None)
            self.finish()

    def remaining_s(self) -> float:
        return self.swing.remaining_s() if self.swing else self.timing_value("brace_s", 45.0)

    def words(self) -> dict[str, Any]:
        return {"new_course": units.format_heading(self.new_course)}


SCRIPTS: dict[str, type[Script]] = {
    "tack": TackScript,
    "wear": WearScript,
    "heave_to": HeaveToScript,
    "fill_away": FillAwayScript,
}
