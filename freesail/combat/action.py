"""The action's tick (spec M7 §8a, §9, §10; package 70): each World's battery served and
fired, the shot resolved against the mark's body, the lines each ship's people can see,
and the strike by morale; called from `World.tick` for the player's World and for each
crewed World alike (one brain, two bodies: a crewed ship fights the player's as the
player's fights hers).

**The mark.** The battery's target is a sail as the lookout names her (the far vessel's
id, or the player's ship under `PLAYER_ID` to a crewed enemy). Her body is her crewed
World's ship when she is crewed (the shot lands in her part graph and her muster), the
player's ship when she is the player's, or the far vessel herself when she is far (the
damage summed on her for 74 to build the far fight from). The truth of where she is, her
head and her heel comes from her body; what the firer's people **see** of the fall of shot
is the battery's minute line (struck, short, over; a spar coming down); what the mark's
people see is her own minute line (the hits as they land, the men hurt), in her own log,
by what they can see. The truth sees both (the director's `truth`).

**Recognition before fire (rule 3, the least of it).** The first shot at a mark not made
out as an enemy (her colours not read, or her nation not at war with the firer's) is not
refused: the firer's log says so and the consequence (every port and ship that hears of
it treats her as a pirate: `ship.extra["outlaw"]`, which the ports' stance reads), and the
mark's captain treats the firer as an enemy from then on (`fired_on`), whatever her
colours.

**The strike.** Once a minute each ship under fire judges her morale (`morale.py`); under
the doctrine's line the colours are struck: the battery holds, the state is written for
the captain's machine and the lookout, and both logs say it.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.combat import hits as HITS
from freesail.combat.guns import Battery, FireMode, Firer, Target, battery_of
from freesail.combat.morale import UNDER_FIRE_S, morale_of
from freesail.combat.shot import range_words
from freesail.core.events import Severity
from freesail.crew.model import number_words
from freesail.crew.quarters import quarters_of
from freesail.world.geo import bearing_and_distance

__all__ = ["GUNNERY_STREAM", "strike", "target_of", "tick_action"]

GUNNERY_STREAM = "gunnery"
PLAYER_ID = "the ship"


def tick_action(world: Any) -> None:
    """One tick of the action for this World's ship."""
    ship = world.ship
    battery = battery_of(ship)
    if battery is None:
        return
    quarters = quarters_of(ship)
    tick = world.clock.tick
    minute = world.clock.ship_time.second == 0
    target = target_of(world, battery.target) if battery.target else None
    if target is not None:
        battery.target_words = target.words
    firer = _firer(world, ship)
    # the mark's relative bearing, kept for the runner's robbing of the guns (the crews
    # from the end that bears least; `Runner._rob_the_guns`)
    battery.target_relative_rad = (
        units.wrap_pi(target.bearing_rad - firer.heading_rad) if target is not None else None
    )
    rng = world.rng.stream(GUNNERY_STREAM)
    fired_before = battery.rounds_fired
    opened_before = dict(battery.opened_fire_at)
    battery.tick(1.0, quarters, firer, target, rng, tick, HITS.resolve_shot)
    if target is not None and battery.rounds_fired > fired_before:
        _fired_on(world, battery, target, tick, opened_before)
    if minute:
        line = battery.minute_line(tick)
        if line is not None:
            text, data = line
            world.record(Severity.NOTABLE, "action.fired", text, data=data)
        _damage_minute(world, ship, tick)
        _judge_morale(world, ship, battery, tick)
        _watch_struck(world, battery, tick)


# -- the mark ---------------------------------------------------------------------------


def target_of(world: Any, target_id: str) -> Target | None:
    """The mark's body and truth for this World's battery: a far vessel (her crewed World's
    ship when crewed), or the player's ship for a crewed World."""
    here = getattr(world, "position", None)
    if here is None:
        return None
    parent = getattr(world, "parent", None)
    if target_id == PLAYER_ID and parent is not None:
        body, tw = parent.ship, parent
        pos = parent.position
        heading = float(body.heading)
        heel = math.degrees(float(getattr(body.dyn, "heel", 0.0)))
        words = _words_for(world, PLAYER_ID, getattr(body, "name", "the ship"))
        nation = _nation_made_out(world, PLAYER_ID)
    else:
        sea = parent.vessels if parent is not None else world.vessels
        vessel = sea.get(target_id)
        if vessel is None or getattr(vessel, "done", False):
            return None
        crew = getattr(vessel, "crew", None)
        if crew is not None and getattr(crew, "shape", "full") == "full":
            body, tw = crew.ship, crew
            heel = math.degrees(float(getattr(body.dyn, "heel", 0.0)))
        else:
            body, tw = vessel, None
            heel = 0.0
        pos = vessel.position
        heading = math.radians(float(vessel.heading_deg))
        words = _words_for(world, target_id, vessel.name)
        nation = _nation_made_out(world, target_id)
    if pos is None:
        return None
    bearing, distance = bearing_and_distance(here, pos)
    length = float(getattr(getattr(body, "hull", None), "length", 0.0) or 0.0)
    if length <= 0.0:
        from freesail.world.ships import rig_height_m

        length = max(10.0, rig_height_m(getattr(body, "ship_file", "")) * 1.2)
    return Target(
        id=target_id,
        words=words,
        bearing_rad=math.radians(bearing),
        range_m=float(distance),
        heading_rad=heading,
        length_m=length,
        heel_deg=heel,
        nation=nation,
        body=body,
        world=tw,
    )


def _words_for(world: Any, target_id: str, fallback: str) -> str:
    lookout = getattr(world, "lookout", None)
    if lookout is not None:
        try:
            return lookout.sail_name(f"sail:{target_id}", "").removeprefix("the ") or fallback
        except Exception:  # noqa: BLE001 - the lookout's names are words, never a failure
            return fallback
    return fallback


def _nation_made_out(world: Any, target_id: str) -> str | None:
    """Her nation as the firer's people have made it out (the lookout's strangers), None
    while she is a stranger."""
    lookout = getattr(world, "lookout", None)
    if lookout is None:
        return None
    try:
        items = lookout.strangers(world, float(world.ship.heading)).get("items") or []
    except Exception:  # noqa: BLE001
        return None
    for i in items:
        if i.get("id") == target_id:
            return i.get("nation")
    return None


def _firer(world: Any, ship: Any) -> Firer:
    motion = getattr(world, "motion", None)
    sea = getattr(world, "sea", None)
    runner = ship.extra.get("evolutions")
    return Firer(
        heel_deg=math.degrees(float(ship.dyn.heel)),
        roll_deg=float(getattr(motion, "roll_deg", 0.0) or 0.0) if motion is not None else 0.0,
        sea_height_m=float(sea.reading().height_m) if sea is not None else 0.0,
        weather_factor=float(getattr(runner, "_last_factor", 1.0) or 1.0),
        half_beam_m=float(ship.hull.spec.beam_m) / 2.0,
        heading_rad=float(ship.heading),
        position=world.position,
    )


# -- being fired on -------------------------------------------------------------------------


def _fired_on(world: Any, battery: Battery, target: Target, tick: int, opened_before) -> None:
    """A shot went at the mark: her people see the flash (the first time, a line of her
    own: 'she opens fire'), her captain knows his enemy, and the recognition's consequence
    is told the firer the first time he fires on a sail not made out as an enemy."""
    firer_id = _own_id(world)
    first = target.id not in opened_before
    # the last shot this tick a signal (across her bows, or a blank): no fire opened
    last = battery.volleys[-1] if battery.volleys else None
    signal = last is not None and last.outcome in ("across her bows", "blank")
    if target.world is not None:
        keeper = HITS.damage_of(target.world.ship)
        if keeper is not None:
            words = _words_in(target.world, firer_id, world.ship.name)
            if signal:
                if last.outcome == "across her bows" and firer_id not in keeper.warned_by:
                    keeper.warned_by.add(firer_id)
                    target.world.record(
                        Severity.URGENT,
                        "action.warning_shot",
                        f"{_cap(words)} fires a shot across our bows.",
                        data={"firer": firer_id, "range_m": round(target.range_m)},
                    )
                return
            keeper.struck_by[firer_id] = tick  # under fire from her, from now
            if firer_id not in keeper.opened_by:
                keeper.opened_by.add(firer_id)
                target.world.record(
                    Severity.URGENT,
                    "action.fired_at",
                    f"{_cap(words)} opens fire on us at {range_words(target.range_m)}.",
                    data={"firer": firer_id, "range_m": round(target.range_m)},
                )
        captain = getattr(target.world, "captain", None)
        if captain is not None:
            captain.fired_on.add(firer_id)
    else:
        if signal:
            return
        brain = getattr(target.body, "brain", None)
        if brain is not None:
            brain.fired_on.add(firer_id)
    if first:
        _recognition(world, target)


def _recognition(world: Any, target: Target) -> None:
    """Rule 3, the least of it: the first shot at a mark not made out as an enemy is said
    with its consequence (`ship.extra["outlaw"]`), not refused."""
    nations = getattr(world, "nations", None)
    ports = getattr(world, "ports", None)
    own = getattr(ports, "ship_nation", None) if ports is not None else None
    enemy = bool(
        target.nation and own and nations is not None and nations.at_war(str(target.nation), own)
    )
    if enemy:
        return
    if target.nation is None:
        why = "her colours not made out"
    else:
        whose = nations.get(target.nation).adjective if nations else target.nation
        why = f"a {whose} vessel, no enemy of ours"
    world.ship.extra["outlaw"] = f"fired into {target.words}, {why}"
    world.record(
        Severity.URGENT,
        "action.unrecognised",
        f"Fired into {target.words}, {why}: every port and ship that hears of it will "
        "hold us pirates (the colours, the private signal and the hail are not yet to be "
        "had; the stance of the ports is turned).",
        data={"target": target.id, "nation": target.nation},
    )


def _damage_minute(world: Any, ship: Any, tick: int) -> None:
    """The mark's own line for the minute's hits, by what her people can see."""
    keeper = HITS.damage_of(ship)
    if keeper is None or not keeper.minute and not keeper.minute_men:
        return
    parts = _counted([words for _kind, words in keeper.minute])
    men = keeper.minute_men
    killed = sum(1 for s in men if s.hurt == "killed")
    wounded = len(men) - killed
    if men:
        said = []
        if killed:
            said.append(f"{number_words(killed)} killed")
        if wounded:
            said.append(f"{number_words(wounded)} wounded")
        named = [s.name for s in men if _is_named(world, s)]
        parts.append(" and ".join(said) + (f" ({', '.join(named)} among them)" if named else ""))
    firers = [fid for fid, t in keeper.struck_by.items() if tick - t <= 120]
    who = _words_in(world, firers[0], "the enemy") if firers else "the enemy"
    text = f"Shot from {who}: {'; '.join(parts)}."
    grave = killed or any(k in ("spar", "helm") for k, _ in keeper.minute)
    severity = Severity.URGENT if grave else Severity.NOTABLE
    world.record(
        severity,
        "action.hit",
        text,
        data={
            "hits": len(keeper.minute),
            "killed": killed,
            "wounded": wounded,
            "kinds": [k for k, _ in keeper.minute],
            "from": firers,
        },
    )
    for s in men:
        if _is_named(world, s):
            world.record(
                Severity.URGENT,
                "person.hurt",
                f"{s.name} is {s.hurt}.",
                data={"sailor": s.id, "hurt": s.hurt},
            )
    keeper.minute = []
    keeper.minute_men = []


def _is_named(world: Any, sailor: Any) -> bool:
    people = getattr(world, "people", None)
    if people is None or not getattr(people, "_built", False):
        return False
    return any(p.sailor_id == sailor.id for p in people.all)


# -- the strike ---------------------------------------------------------------------------


def _judge_morale(world: Any, ship: Any, battery: Battery, tick: int) -> None:
    keeper = HITS.damage_of(ship)
    if keeper is None or ship.extra.get("struck"):
        return
    recent = [t for t in keeper.struck_by.values() if tick - t <= UNDER_FIRE_S]
    engaged = battery.last_fired_tick is not None and tick - battery.last_fired_tick <= UNDER_FIRE_S
    if not recent and not engaged and not keeper.hits:
        return
    captain = getattr(world, "captain", None)
    doctrine = getattr(captain, "doctrine", None) if captain is not None else None
    m = morale_of(ship, doctrine)
    enemy_lb = _enemy_weight(world, keeper, tick)
    complement = int(getattr(getattr(ship.spec, "crew", None), "complement", 0) or 0)
    m.judge(ship, complement, enemy_lb, under_fire=bool(recent))
    if recent and m.value < m.strike_below:
        strike(world, by_rule=True)


def _enemy_weight(world: Any, keeper: Any, tick: int) -> float:
    """The weight of broadside of the ship whose shot struck last, in pounds."""
    recent = sorted(keeper.struck_by.items(), key=lambda kv: -kv[1])
    for fid, _t in recent:
        body = _body_of(world, fid)
        guns = list(getattr(body, "guns", {}).values()) if body is not None else []
        if guns:
            return sum(g.pounder for g in guns if g.side == "starboard" or g.place != "broadside")
        if body is not None and getattr(body, "ship_file", None):
            return _far_weight(body)
    return 0.0


def _far_weight(vessel: Any) -> float:
    from freesail.ship.loader import load_spec

    try:
        spec = load_spec(vessel.ship_file)
    except Exception:  # noqa: BLE001
        return 0.0
    if spec.armament is None:
        return 0.0
    fit = spec.armament.fit(getattr(vessel, "fit", "") or None)
    return sum(g.pounder for g in fit.guns if g.side == "starboard" or g.place != "broadside")


def _body_of(world: Any, ship_id: str) -> Any:
    parent = getattr(world, "parent", None)
    if ship_id == PLAYER_ID and parent is not None:
        return parent.ship
    sea = parent.vessels if parent is not None else world.vessels
    v = sea.get(ship_id)
    if v is None:
        return None
    crew = getattr(v, "crew", None)
    return crew.ship if crew is not None and crew.shape == "full" else v


def strike(world: Any, by_rule: bool, words: str = "") -> str:
    """The colours struck: the battery holds, the state written for the captain's machine
    and the lookout, the log saying why. Returns the line."""
    ship = world.ship
    tick = world.clock.tick
    ship.extra["struck"] = tick
    ship.extra["colours"] = "struck"
    battery = battery_of(ship)
    if battery is not None:
        battery.mode = FireMode.HOLD
        battery.word = None
        battery.single = []
    vessel = getattr(world, "vessel", None)
    if vessel is not None:
        vessel.struck = True
    m = ship.extra.get("morale")
    if by_rule:
        why = m.reasons if m is not None else "the hands will not stand to the guns"
        text = (
            f"The colours are struck: {why}; the hands will not stand to the guns. The guns "
            "fall silent and she lies to for her captor."
        )
    else:
        text = (
            "The colours are struck"
            + (f" ({words})" if words else "")
            + ": the guns fall silent and she lies to for her captor; what follows (the "
            "prize crew, the prisoners) is not yet in the game."
        )
    world.record(
        Severity.URGENT,
        "action.struck",
        text,
        data={"by_rule": by_rule, "morale": round(m.value, 2) if m is not None else None},
    )
    captain = getattr(world, "captain", None)
    if captain is not None and hasattr(captain, "strike_state"):
        captain.strike_state()
    return text


def _watch_struck(world: Any, battery: Battery, tick: int) -> None:
    """A mark whose colours have come down, seen from this ship: said once, and the
    battery's book ceases on her (`cease firing` is the captain's book's by `at the enemy
    strikes`; here the mark is dropped as a target so nothing fires at a struck ship)."""
    seen = world.ship.extra.setdefault("struck_seen", set())
    parent = getattr(world, "parent", None)
    sea = parent.vessels if parent is not None else getattr(world, "vessels", None)
    if sea is None:
        return
    candidates = list(getattr(sea, "vessels", []) or [])
    if parent is not None:
        shadow = parent.vessels.player_shadow(parent)
        if shadow is not None:
            candidates.append(shadow)
    here = world.position
    own = _own_id(world)
    for v in candidates:
        if not getattr(v, "struck", False) or v.id in seen or v.id == own:
            continue  # her own body in the parent's list is not a sail she watches
        if here is None or bearing_and_distance(here, v.position)[1] > 4.0 * units.NAUTICAL_MILE:
            continue
        seen.add(v.id)
        words = _words_in(world, v.id, v.name)
        world.record(
            Severity.URGENT,
            "action.enemy_struck",
            f"{_cap(words)} has struck her colours!",
            data={"id": v.id},
        )
        if battery.target == v.id:
            battery.mode = FireMode.HOLD
            battery.word = None


# -- names ---------------------------------------------------------------------------------


def _own_id(world: Any) -> str:
    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else PLAYER_ID


def _counted(words: list[str]) -> list[str]:
    """The same words said once with their number: 'a shot through the side to starboard'
    twice is 'two shot through the side to starboard'."""
    out: list[str] = []
    counts: dict[str, int] = {}
    for w in words:
        if w not in counts:
            out.append(w)
        counts[w] = counts.get(w, 0) + 1
    said = []
    for w in out:
        n = counts[w]
        if n > 1 and w.startswith("a shot "):
            said.append(f"{number_words(n)} shot {w[len('a shot ') :]}")
        elif n > 1:
            said.append(f"{w} ({number_words(n)} times)")
        else:
            said.append(w)
    return said


def _words_in(world: Any, ship_id: str, fallback: str) -> str:
    """A ship's words in this World's log: the lookout's name for her where he has one."""
    lookout = getattr(world, "lookout", None)
    if lookout is not None:
        try:
            name = lookout.sail_name(f"sail:{ship_id}", "")
            if name:
                return name
        except Exception:  # noqa: BLE001
            pass
    return fallback


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]
