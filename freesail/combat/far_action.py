"""The far fight on the sleeping hulls (spec M7 §18; package 74, step 4; the design in
`docs/design/Design-Prizes.md` §4): the rounds of `combat/far.py` run by the world.

Once a minute in the sea's minute (`Vessels.tick`, after the brains have judged and the sets
have ticked, before the bodies move), **every pair of far bodies of which at least one is in
`engaging` with the other as her mark** resolves one round every `FAR_ROUND_S` (three
minutes, 70's step) while the two lie within the reach of her guns (the longest random shot
of her fit's guns; beyond it nothing fires and the state's chase leg closes her). Each side is
a `FarShip` built from her `Vessel` (`far.far_ship`: her file, her fit, her nation; the aim
and the morale figures from her brain's doctrine under the nation's habit), her record's
killed, wounded, dismounted, holes, sail cut, spars gone and morale carried in, so that a
ship that fought yesterday fights hurt today; the draws from the World's stream `far`, opened
at the first round and not before (70's rule for the gunnery's stream, so that no sailing
passage's list of streams moves); the sums written back into `Vessel.damage` with a line in
each side's story and, where a hull sleeps under her, in her log (`action.far_round`).

**The strike by morale** is `far._judge` on the carried sums: the colours come down by the
doctrine's line as 70 measured; then she is struck as `far_captures` writes it (her state,
her brain, her plan, her colours), and her captor's brain takes `taking possession` (§2.4).

**One side awake** (a hull under the cap, the other far): the awake hull's battery fires at
the far mark by 70's road already (`hits._far_hit` sums into the far record); the far ship's
reply is the round's half **only as a fallback where the cap has no room to wake her** (the
lead's ruling 4): her broadside at the awake hull by the tables, each shot that strikes
resolved into the awake hull's parts by `hits.resolve_shot` with a synthetic gun of her
fit's kind. How often it fires is counted (`FALLBACK_COUNT`) for the tuning notes.

**Guns heard off the horizon** (§4.5; the lead's ruling 5, under this module's toggle): a
line of the player's log once a round while any far round fires within `GUNS_HEARD_NM` of
her (the period's logs have the guns of an action heard ten and fifteen miles off: judgement,
twelve), by night the flashes seen to the horizon's range of the light.

`ENABLED` is the toggle for the bisection (§4.6): with it False nothing of this module fires,
the far brain never engages and the world is 70's.
"""

from __future__ import annotations

import functools
import math
from typing import Any

from freesail import units
from freesail.combat import far as F
from freesail.core.events import Severity

__all__ = [
    "ACTION_STATES",
    "ENABLED",
    "FALLBACK_COUNT",
    "FAR_ROUND_S",
    "GUNS_HEARD_NM",
    "STREAM",
    "engage_range_m",
    "far_damage_into_parts",
    "far_ship_of",
    "has_guns",
    "minute",
    "reach_m",
    "struck_within_hour",
]

ENABLED = True
FAR_ROUND_S = 180.0
STREAM = "far"
GUNS_HEARD_NM = 12.0  # judgement: the guns of an action heard ten to fifteen miles off
FLASHES_SEEN_NM = 15.0  # by night, the flashes at the horizon's range: judgement
ACTION_STATES: frozenset[str] = frozenset({"engaging", "taking possession"})
STRUCK_HOUR_S = 3600
FALLBACK_COUNT: dict[str, int] = {"rounds": 0}  # the awake-hull fallback's firings, for the notes

_CARRIED = ("killed", "wounded", "dismounted", "holes", "holes_below", "sail_cut", "spars_gone")


# -- the far side from her record ------------------------------------------------------------------


def has_guns(vessel: Any) -> bool:
    """Whether her fit has guns to fire (a merchantman's 'unarmed' has none)."""
    return _fit_has_guns(str(vessel.ship_file), str(getattr(vessel, "fit", "") or ""))


@functools.lru_cache(maxsize=64)
def _fit_has_guns(ship_file: str, fit: str) -> bool:
    try:
        return bool(_fit_guns(ship_file, fit))
    except Exception:  # noqa: BLE001  (a file without armament)
        return False


def _fit_guns(ship_file: str, fit: str) -> tuple[tuple[str, float, float], ...]:
    """The engaged broadside of a file's fit (one side's guns and the chasers), read once a
    file and fit (`far.file_figures`): the far brain asks it of every stranger at every
    minute of hers, and the file's reading from disk each time cost the convoy's pace two
    thirds of its tick (docs/dev/TuningNotes.md, package 74, step 4)."""
    return F.file_figures(ship_file, fit)[1]


def _guns_of(vessel: Any) -> list[tuple[str, float, float]]:
    return list(_fit_guns(str(vessel.ship_file), str(getattr(vessel, "fit", "") or "")))


def reach_m(vessel: Any) -> float:
    """The longest random shot of her fit's guns, in metres; nought with no guns."""
    return _fit_reach_m(str(vessel.ship_file), str(getattr(vessel, "fit", "") or ""))


@functools.lru_cache(maxsize=64)
def _fit_reach_m(ship_file: str, fit: str) -> float:
    from freesail.combat import shot as S

    best = 0.0
    for kind, pounder, _w in _fit_guns(ship_file, fit):
        b = S.ballistics_of(kind, pounder)
        best = max(best, float(b.random_m))
    return best


def _doctrine_figures(world: Any, vessel: Any) -> dict[str, Any]:
    """The aim and the morale figures she fights by: her brain's doctrine, the nation's
    habit over the file where it leaves the aim empty (`Captain._habit`'s rule)."""
    from freesail.world.nations import DEFAULT_HABITS

    brain = getattr(vessel, "brain", None)
    d = getattr(brain, "doctrine", None)
    th = d.threshold if d is not None else (lambda k, v=None: v)
    nations = getattr(world, "nations", None)
    habit = nations.habits_of(str(vessel.nation)) if nations is not None else dict(DEFAULT_HABITS)
    aim = str(th("aim", "") or habit.get("aim", "hull"))
    out: dict[str, Any] = {"aim": aim}
    ms = th("morale_start", None)
    sb = th("strike_below", None)
    if ms is not None:
        out["morale_start"] = float(ms)
    if sb is not None:
        out["strike_below"] = float(sb)
    out["range_factor"] = float(habit.get("range_factor", 1.0))
    out["engage_range_cables"] = float(th("engage_range_cables", 2.0))
    return out


def engage_range_m(brain: Any) -> float:
    """The doctrine's engaging range in metres under the nation's habit (§4.2)."""
    world = getattr(brain, "world", None)
    vessel = getattr(brain, "vessel", None)
    if world is None or vessel is None:
        return 2.0 * units.CABLE
    fig = _doctrine_figures(world, vessel)
    return max(0.5 * units.CABLE, fig["engage_range_cables"] * fig["range_factor"] * units.CABLE)


def far_ship_of(world: Any, vessel: Any) -> F.FarShip:
    """Her far side with her record carried in."""
    fig = _doctrine_figures(world, vessel)
    kw = {k: v for k, v in fig.items() if k in ("aim", "morale_start", "strike_below")}
    fs = F.far_ship(vessel.ship_file, str(vessel.nation), getattr(vessel, "fit", "") or None, **kw)
    fs.name = str(vessel.name)
    d = dict(getattr(vessel, "damage", None) or {})
    fs.killed = int(d.get("killed", 0) or 0)
    fs.wounded = int(d.get("wounded", 0) or 0)
    fs.dismounted = int(d.get("dismounted", 0) or 0)
    fs.holes = int(d.get("holes", 0) or 0)
    fs.holes_below = int(d.get("holes_below", 0) or 0)
    fs.sail_cut = float(d.get("sail_cut", 0.0) or 0.0)
    fs.spars_gone = int(d.get("spars_gone", 0) or 0)
    fs.rounds_fired = int(d.get("rounds_fired", 0) or 0)
    if d.get("morale") is not None:
        fs.morale = float(d["morale"])
    return fs


def _write_back(vessel: Any, fs: F.FarShip, tick: int) -> None:
    d = vessel.damage
    for key in _CARRIED:
        d[key] = getattr(fs, key)
    d["rounds_fired"] = fs.rounds_fired
    d["morale"] = round(float(fs.morale), 3)
    d["rounds"] = int(d.get("rounds", 0) or 0) + 1
    d["last_round_tick"] = tick


def struck_within_hour(world: Any, vessel: Any) -> bool:
    if not getattr(vessel, "struck", False):
        return False
    since = int((getattr(vessel, "damage", None) or {}).get("struck_tick", -1))
    return since >= 0 and int(world.clock.tick) - since <= STRUCK_HOUR_S


# -- the minute ------------------------------------------------------------------------------------


def _hull(vessel: Any) -> Any:
    crew = getattr(vessel, "crew", None)
    return crew if crew is not None and hasattr(crew, "ship") else None


def _awake(vessel: Any) -> bool:
    hull = _hull(vessel)
    return (
        hull is not None
        and getattr(hull, "shape", "full") == "full"
        and getattr(hull, "awake", True)
    )


def _pairs(world: Any) -> list[tuple[Any, Any]]:
    """(the engaging ship, her mark) for every far body in `engaging` whose mark is on the
    sea and not struck; one pair for two ships engaging each other."""
    sea = getattr(world, "vessels", None)
    out: list[tuple[Any, Any]] = []
    seen: set[tuple[str, str]] = set()
    if sea is None:
        return out
    for v in list(sea.vessels):
        brain = getattr(v, "brain", None)
        if v.done or brain is None or brain.state != "engaging" or _awake(v):
            continue
        mark = sea.get(str(brain._stranger or ""))
        if (
            mark is None
            or mark.done
            or getattr(mark, "struck", False)
            or getattr(v, "struck", False)
        ):
            continue
        key = tuple(sorted((str(v.id), str(mark.id))))
        if key in seen:
            continue
        seen.add(key)
        out.append((v, mark))
    return out


def minute(world: Any) -> list[tuple[Any, ...]]:
    """The far rounds of the minute (the module's head). Returns the lines for the player's
    log: the guns heard."""
    lines: list[tuple[Any, ...]] = []
    if not ENABLED:
        return lines
    from freesail.world.hulls import world_of

    root = world_of(world)
    tick = int(root.clock.tick)
    pairs = _pairs(root)
    if not pairs:
        return lines
    book = root.__dict__.setdefault("_far_rounds", {})
    fired_somewhere: list[tuple[Any, Any, float]] = []
    for a, b in pairs:
        key = "|".join(sorted((str(a.id), str(b.id))))
        rec = book.setdefault(key, {"last": -(10**9), "fired_on": {}, "since": tick})
        if tick - rec["last"] < FAR_ROUND_S:
            continue
        if _awake(b):
            _fallback_reply(root, a, b, rec, tick, lines)
            continue
        from freesail.world.geo import bearing_and_distance

        _, range_m = bearing_and_distance(a.position, b.position)
        if range_m > max(reach_m(a), reach_m(b)):
            continue  # beyond the guns' reach nothing fires; the chase leg closes her
        rec["last"] = tick
        rng = root.rng.stream(STREAM)
        fa, fb = far_ship_of(root, a), far_ship_of(root, b)
        t_s = float(tick - rec["since"])
        fired_on = rec["fired_on"]
        fired_on.setdefault(fa.name, False)
        fired_on.setdefault(fb.name, False)
        r = F.round_once(fa, fb, range_m, rng, t_s, fired_on, FAR_ROUND_S)
        _write_back(a, fa, tick)
        _write_back(b, fb, tick)
        _say_round(root, a, b, fa, fb, r, range_m, tick)
        if fa.struck_at_s is not None:
            _strike(root, a, b, tick)
        elif fb.struck_at_s is not None:
            _strike(root, b, a, tick)
        fired_somewhere.append((a, b, range_m))
    if fired_somewhere:
        lines.extend(_guns_heard(root, fired_somewhere, tick))
    return lines


def _say_round(
    root: Any, a: Any, b: Any, fa: F.FarShip, fb: F.FarShip, r: F.Round, range_m: float, tick: int
) -> None:
    from freesail.crew.model import number_words
    from freesail.world.prizes import _story

    cables = range_m / units.CABLE
    for us, them, fired, struck_us, struck_them, hurt in (
        (a, b, r.fired[0], r.struck[1], r.struck[0], r.hurt[0]),
        (b, a, r.fired[1], r.struck[0], r.struck[1], r.hurt[1]),
    ):
        text = (
            f"A round of the action with the {them.name} at {cables:.0f} cables: "
            f"{number_words(struck_us)} shot struck us"
            + (f", {number_words(hurt)} men hurt in all" if hurt else "")
            + f"; our fire told {number_words(struck_them)} times of {number_words(fired)}."
        )
        _story(us, tick, f"a round with the {them.name} at {cables:.0f} cables")
        hull = _hull(us)
        if hull is not None:
            hull.record(
                Severity.ROUTINE,
                "action.far_round",
                text,
                data={
                    "with": str(them.id),
                    "range_m": round(range_m),
                    "fired": fired,
                    "struck_us": struck_us,
                    "struck_them": struck_them,
                    "hurt": hurt,
                },
            )


def _strike(root: Any, loser: Any, winner: Any, tick: int) -> None:
    """The colours struck by morale in the rounds, as `far_captures` writes it."""
    from freesail.world import signals as S
    from freesail.world.prizes import _story

    loser.struck = True
    loser.damage["struck_tick"] = tick
    from freesail.world.prize_court import note_in_sight

    note_in_sight(root, loser)
    S.set_colours(
        S.vessel_locker(loser).colours, getattr(root, "nations", None), "struck", "", tick
    )
    loser.state = "struck"
    loser.plan = [("lie_to", math.inf)]
    loser.saved_plan = None
    brain = getattr(loser, "brain", None)
    if brain is not None:
        brain.state = "struck"
        brain.history.append((tick, "struck"))
    _story(loser, tick, f"struck to the {winner.name}: the hands would not stand to the guns")
    _story(winner, tick, f"the {loser.name} struck to us")
    hull = _hull(loser)
    if hull is not None:
        hull.record(
            Severity.URGENT,
            "action.struck",
            f"The colours are struck to the {winner.name}: the hands will not stand to the "
            "guns; she lies to for her captor.",
            data={"to": str(winner.id), "by_rule": True},
        )
    wh = _hull(winner)
    if wh is not None:
        wh.record(
            Severity.URGENT,
            "action.enemy_struck",
            f"The {loser.name} strikes her colours to us.",
            data={"struck": str(loser.id)},
        )


def _fallback_reply(root: Any, far: Any, awake: Any, rec: dict, tick: int, lines: list) -> None:
    """The far ship's broadside at an awake hull by the tables, only where the cap has no
    room to wake her (the lead's ruling 4); each shot that strikes resolved into the awake
    hull's parts with a synthetic gun of her fit's kind."""
    from freesail.world.crews import crewed, settings

    cap, _within, _demote = settings(root)
    if cap <= 0 or len(crewed(root)) < cap:
        return  # room under the cap: the switch wakes her and the near action takes over
    from freesail.world.geo import bearing_and_distance

    bearing, range_m = bearing_and_distance(far.position, awake.position)
    if range_m > reach_m(far):
        return
    rec["last"] = tick
    FALLBACK_COUNT["rounds"] += 1
    hull = _hull(awake)
    rng = root.rng.stream(STREAM)
    fa = far_ship_of(root, far)
    target_len = float(getattr(getattr(hull.ship, "hull", None), "length", 40.0) or 40.0)
    fb = F.FarShip(
        name=str(awake.name),
        nation=str(awake.nation),
        guns=[],
        complement=len(getattr(hull.ship.extra.get("crew"), "sailors", []) or []),
        length_m=target_len,
    )
    fired, struck = F._fire(fa, fb, range_m, rng, FAR_ROUND_S)
    fa.rounds_fired += 0  # counted in _fire
    _write_back(far, fa, tick)
    if struck:
        _into_parts(root, hull, awake, far, fa, struck, bearing, range_m, rng, tick)
    from freesail.crew.model import number_words

    # the line in the ship's words, the counts as the round's line has them; that it was the
    # reply by the tables with the cap full is the data's `fallback`, for the record (85's
    # rule: the engine's words are not served)
    told = "none" if not struck else number_words(struck)
    hull.record(
        Severity.NOTABLE,
        "action.far_reply",
        f"The {far.name} fires her broadside at us from {range_m / units.CABLE:.0f} cables: "
        f"{told} of her {number_words(fired)} shot {'strikes' if struck == 1 else 'strike'} us.",
        data={"from": str(far.id), "fired": fired, "struck": struck, "fallback": True},
    )


def _into_parts(
    root: Any,
    hull: Any,
    awake: Any,
    far: Any,
    fa: F.FarShip,
    struck: int,
    bearing: float,
    range_m: float,
    rng: Any,
    tick: int,
) -> None:
    import types

    from freesail.combat import hits as H
    from freesail.combat.guns import Target
    from freesail.ship.parts import Charge, Gun

    guns = fa.guns or [("long", 12.0, 30.0)]
    kind, pounder, weight = max(guns, key=lambda g: g[1])
    gun = Gun(
        id=f"far-{far.id}", cls="gun", rating_kn=0.0, kind=kind, pounder=pounder, weight_cwt=weight
    )
    battery = types.SimpleNamespace(aim=H.Aim.HULL if fa.aim == "hull" else H.Aim.RIGGING)
    target = Target(
        id=str(awake.id),
        words=str(awake.name),
        bearing_rad=math.radians(bearing),
        range_m=float(range_m),
        heading_rad=math.radians(float(awake.heading_deg)),
        length_m=float(getattr(getattr(hull.ship, "hull", None), "length", 40.0) or 40.0),
        heel_deg=0.0,
        nation=str(awake.nation),
        body=hull.ship,
        world=hull,
    )
    for _ in range(struck):
        H.resolve_shot(battery, gun, Charge.ROUND, target, high=False, rng=rng, tick=tick)


def _guns_heard(root: Any, fired: list[tuple[Any, Any, float]], tick: int) -> list[tuple[Any, ...]]:
    """The guns of a far round heard (or the flashes seen by night) at the player's ship,
    once a round, as a line of her log (the lookout's rule: judgement)."""
    from freesail.world.geo import bearing_and_distance

    players = getattr(root, "players", None)
    here = getattr(players, "position", None)
    if here is None:
        return []
    light = str(getattr(root, "daylight", "day") or "day")
    reach = FLASHES_SEEN_NM if light == "night" else GUNS_HEARD_NM
    out: list[tuple[Any, ...]] = []
    for a, b, _r in fired:
        mid = a.position
        bearing, d = bearing_and_distance(here, mid)
        nm = d / units.NAUTICAL_MILE
        if nm > reach:
            continue
        from freesail.world.hulls import players_id

        mine = players_id(root)  # the player's ship (package 60: his now)
        if any(str(getattr(v, "id", "")) == mine for v in (a, b)):
            return out  # our own action is our own log's
        point = units.point_name(units.deg_to_rad(bearing))
        what = "The flashes of guns" if light == "night" else "The sound of guns"
        text = f"{what} to the {point}, distant about {nm:.0f} miles: an action off the horizon."
        out.append(
            (
                Severity.NOTABLE,
                "action.guns_heard",
                text,
                {"bearing": point, "distance_nm": round(nm, 1), "ships": [str(a.id), str(b.id)]},
            )
        )
        break  # one line a round, whatever the pairs
    return out


# -- the far state into the near body --------------------------------------------------------------


def far_damage_into_parts(hull: Any, damage: dict[str, Any] | None) -> dict[str, int]:
    """The far record's counts applied to her parts beyond what the parts already show (the
    design's §4.4), once (`damage["carried_in"]` keeps what was applied): the men killed and
    wounded on her muster, the guns dismounted from the end of her engaged side, the shot
    holes into her damage keeper (above and below the water, along her length), the sail cut
    as her set sails' condition, the spars gone as her topgallant masts and yards wrecked
    first. Returns what was applied."""
    from freesail.combat import hits as H
    from freesail.ship.parts import SailState

    applied: dict[str, int] = {}
    if not damage:
        return applied
    carried = dict(damage.get("carried_in") or {})
    ship = hull.ship
    tick = int(hull.world.clock.tick) if getattr(hull, "world", None) is not None else 0
    rng = hull.rng.stream("muster") if hasattr(hull, "rng") else None
    muster = ship.extra.get("crew")
    sailors = list(getattr(muster, "sailors", []) or [])

    def want(key: str) -> int:
        return max(0, int(damage.get(key, 0) or 0) - int(carried.get(key, 0) or 0))

    # the men
    for key, killed in (("killed", True), ("wounded", False)):
        n = want(key)
        fit = [s for s in sailors if s.fit]
        for _ in range(min(n, len(fit))):
            s = fit.pop(int(rng.random() * len(fit)) % len(fit)) if rng is not None else fit.pop()
            H.hit_man(ship, s, killed, rng, tick, how="a round shot")
        applied[key] = n
    # the guns dismounted, from the end of the engaged side
    n = want("dismounted")
    guns = [g for g in getattr(ship, "guns", {}).values() if not getattr(g, "dismounted", False)]
    for g in list(reversed(guns))[:n]:
        g.dismounted = True
    applied["dismounted"] = n
    # the shot holes
    keeper = H.damage_of(ship)
    n_holes, n_below = want("holes"), want("holes_below")
    length = float(getattr(getattr(ship, "hull", None), "length", 40.0) or 40.0)
    if keeper is not None:
        for i in range(n_holes):
            below = i < n_below
            x = (rng.random() - 0.5) * length if rng is not None else 0.0
            keeper.holes.append(
                {
                    "tick": tick,
                    "side": "starboard" if (rng is None or rng.random() < 0.5) else "larboard",
                    "x_m": round(x, 1),
                    "z_m": -0.5 if below else 0.8,
                    "diameter_m": 0.12,
                    "pounder": 12.0,
                    "below": below,
                }
            )
    applied["holes"], applied["holes_below"] = n_holes, n_below
    # the sail cut: the set sails' condition
    cut = float(damage.get("sail_cut", 0.0) or 0.0) - float(carried.get("sail_cut", 0.0) or 0.0)
    if cut > 0:
        for sl in getattr(ship, "sails", {}).values():
            if getattr(sl, "state", None) == SailState.SET:
                sl.condition = max(0.0, float(sl.condition) - cut * 100.0)
    # the spars gone: the topgallant masts and yards first
    n = want("spars_gone")
    spars = [sp for sp in getattr(ship, "spars", {}).values() if not getattr(sp, "wrecked", False)]
    spars.sort(key=lambda sp: (0 if "topgallant" in sp.id else 1, sp.id))
    for sp in spars[:n]:
        sp.wrecked = True
    applied["spars_gone"] = n
    damage["carried_in"] = {
        k: int(damage.get(k, 0) or 0)
        for k in ("killed", "wounded", "dismounted", "holes", "holes_below", "spars_gone")
    } | {"sail_cut": float(damage.get("sail_cut", 0.0) or 0.0)}
    return applied
