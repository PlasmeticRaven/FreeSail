"""The marines and the small arms (spec M7 §11; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): the musketry within musket shot of a near deck.

The detachment is the muster's `marines` station, at quarters the `marines` division
(`crew/quarters.py`: the poop and the gangways); its kit is the nation's
(`data/marines.yaml` through `Nations.marines_kit_of`: the musket, the seconds between
volleys, the chance a shot tells at fifty yards, the share the book sends aloft and the
marksman's edge there). The ship's company's small arms are the quarter bill's
`small_arms` men with the stand of arms' muskets, once `serve out the small arms` has been
given (an evolution of five minutes).

Each tick of the action (`combat/action.py`) within `MUSKET_SHOT_M` of the battery's mark
when she is a near deck (a crewed vessel's or the player's ship; a far vessel gets nothing:
74's), under the standing intention `marines, fire by volley` (one volley every `volley_s`
by the whole detachment, the hits drawn at once) or `marines, fire at will` (the same fire
spread over the seconds), else `marines, hold your fire`; the small-arms men at will when
the arms are served out. The hits are a Poisson draw on the gunnery stream about the
muskets times the chance at the range times the roll's scatter; each falls on a man exposed
on the mark: the quarterdeck's people with `QUARTERDECK_SHARE` (history's lesson, spec M7
§11), the deck's divisions else (the marines and the gun crews of the side that bears
first). Killed three in ten, the wound light or grave as the shot's (`crew/health.py`). The
mark's people fire back by their own book. The hits are counted into her `Damage.minute`
so that her minute line says "musketry from her deck: two wounded", and the firer's log
says what his marines did.

Every figure is judgement with its source in `data/marines.yaml`; the musket shot of a
hundred yards is the spec's.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail.core.events import Severity
from freesail.crew.model import Sailor, Station, number_words

__all__ = [
    "KILLED_SHARE",
    "MUSKET_SHOT_M",
    "QUARTERDECK_SHARE",
    "Musketry",
    "boarders_count",
    "hit_chance",
    "kit_of",
    "marines_of",
    "musketry_of",
    "small_arms_count",
    "small_arms_of",
    "strike_a_man",
    "tick",
]

# Musket shot: a hundred yards (spec M7 §11; the period's commonplace, Falconer 1780 MUSKET).
MUSKET_SHOT_M = 91.44
# The range the kit's chance is given at (fifty yards).
AIMED_AT_M = 45.72
# The share of the hits that fall on the quarterdeck's people when the mark's after deck
# bears (history's lesson, spec M7 §11: the officers on the quarterdeck the marksmen's
# mark; judgement at two in five).
QUARTERDECK_SHARE = 0.4
# Killed three in ten of the men hit by musketry, the rest wounded (the returns of the
# single-ship actions, James; judgement, as the shot's `hits.KILLED_SHARE`).
KILLED_SHARE = 0.3
# The scatter of the roll: a musket aimed from a rolling deck tells the less, by the roll's
# degrees over this figure (judgement).
ROLL_SCATTER_DEG = 10.0
# The seconds between a small-arms man's shots: a seaman is no drilled soldier (judgement).
SMALL_ARMS_SHOT_S = 30.0
# Where the ball struck, for the wound's words.
BALL_WORDS = (
    "a musket ball in the arm",
    "a musket ball in the thigh",
    "a musket ball in the shoulder",
    "a musket ball in the breast",
    "a musket ball through the hand",
    "a musket ball in the side",
)
MODES = ("hold", "volley", "at will")


@dataclass
class Musketry:
    """The marines' and the small arms' standing intentions, kept in
    `ship.extra["musketry"]` (`musketry_of`)."""

    mode: str = "hold"  # the marines: hold, volley, at will
    in_tops: bool = False  # the book's share sent aloft
    served: bool = False  # the small arms served out to the company
    small_arms_mode: str = "hold"  # the small-arms men: hold, at will
    repelling: bool = False  # `repel boarders`: the gun crews up, the guns silent
    last_volley_tick: int | None = None
    # the minute's tally for the firer's own line: the volleys and the men seen to fall
    minute_volleys: int = 0
    minute_hits: int = 0
    minute_target: str = ""
    # the tick the mark's keeper was told of this minute's musketry (one line a minute)
    told_minute: dict[str, int] = field(default_factory=dict)


def musketry_of(ship: Any) -> Musketry:
    extra = ship.extra
    m = extra.get("musketry")
    if not isinstance(m, Musketry):
        m = Musketry()
        extra["musketry"] = m
    return m


def kit_of(world: Any) -> dict[str, Any]:
    """The ship's nation's kit (`data/marines.yaml`), the basic kit where the world has no
    nations or the ship no nation."""
    from freesail.world.nations import load_marines

    nations = getattr(world, "nations", None)
    ports = getattr(world, "dealings", None)
    nation = str(getattr(ports, "ship_nation", "") or "")
    if nations is not None and hasattr(nations, "marines_kit_of"):
        return nations.marines_kit_of(nation)
    kits = load_marines().get("kits") or {}
    kit = dict(kits.get("basic") or {})
    kit["id"] = "basic"
    return kit


def small_arms_of(world: Any) -> dict[str, Any]:
    from freesail.world.nations import load_marines

    return dict(load_marines().get("small_arms") or {})


def marines_of(ship: Any) -> list[Sailor]:
    """The detachment fit for the deck: at quarters the marines' division, else the
    station's fit men."""
    from freesail.crew.quarters import MARINES

    crew = ship.extra.get("crew")
    if crew is None:
        return []
    quarters = ship.extra.get("quarters")
    if quarters is not None and getattr(quarters, "at_quarters", False):
        return [s for s in quarters.divisions.get(MARINES, []) if s.fit]
    return [s for s in crew.by_station.get(Station.MARINES, []) if s.fit]


def _bill(ship: Any) -> Any:
    return getattr(getattr(getattr(ship, "spec", None), "crew", None), "quarter_bill", None)


def small_arms_count(ship: Any) -> int:
    """The quarter bill's small-arms men, so many as the company has fit seamen for; a
    ship whose bill is reckoned has a tenth of her fit seamen (judgement)."""
    crew = ship.extra.get("crew")
    if crew is None:
        return 0
    fit = [
        s for s in crew.sailors if s.fit and s.station not in (Station.MARINES, Station.QUARTERDECK)
    ]
    bill = _bill(ship)
    n = int(getattr(bill, "small_arms", 0) or 0) if bill is not None else len(fit) // 10
    return max(0, min(n, len(fit)))


def boarders_count(ship: Any) -> int:
    """The quarter bill's boarders (the men told off from the guns' crews, Luce 1884 ch.
    XX), beside the marines; a bill reckoned gives half the fit seamen (judgement)."""
    crew = ship.extra.get("crew")
    if crew is None:
        return 0
    fit = [
        s for s in crew.sailors if s.fit and s.station not in (Station.MARINES, Station.QUARTERDECK)
    ]
    bill = _bill(ship)
    n = int(getattr(bill, "boarders", 0) or 0) if bill is not None else len(fit) // 2
    return max(0, min(n, len(fit)))


def hit_chance(kit: dict[str, Any], range_m: float) -> float:
    """The chance a shot tells on a man on a near deck: the kit's figure at fifty yards,
    falling with the square of the range to nought at musket shot (spec M7 §11), and
    rising nearer (point-blank some five times the fifty-yard figure)."""
    if range_m >= MUSKET_SHOT_M:
        return 0.0
    base = float(kit.get("hit_at_50_yd", 0.04) or 0.04)
    scale = (1.0 - AIMED_AT_M / MUSKET_SHOT_M) ** 2
    return min(1.0, base * ((1.0 - range_m / MUSKET_SHOT_M) ** 2) / scale)


def _poisson(mean: float, rng: Any) -> int:
    if mean <= 0.0:
        return 0
    limit = math.exp(-mean)
    k, p = 0, 1.0
    while True:
        p *= rng.random()
        if p <= limit:
            return k
        k += 1
        if k > 50:
            return k


def _bearing_side(body: Any, from_bearing_rad: float) -> str:
    """The side of the mark the firer bears on."""
    heading = float(getattr(getattr(body, "dyn", None), "heading", 0.0) or 0.0)
    rel = (from_bearing_rad - heading + math.pi) % (2.0 * math.pi) - math.pi
    return "starboard" if rel >= 0.0 else "larboard"


def exposed_men(body: Any, side: str) -> tuple[list[Sailor], list[Sailor]]:
    """(the quarterdeck's fit people, the deck's fit men with the marines and the side's
    gun crews first) on the mark."""
    from freesail.crew.quarters import HELM, MARINES, TRIMMERS

    crew = body.extra.get("crew")
    if crew is None:
        return [], []
    quarterdeck = [s for s in crew.by_station.get(Station.QUARTERDECK, []) if s.fit]
    deck: list[Sailor] = []
    quarters = body.extra.get("quarters")
    if quarters is not None and getattr(quarters, "at_quarters", False):
        deck += [s for s in quarters.divisions.get(MARINES, []) if s.fit]
        guns = getattr(body, "guns", {}) or {}
        crews = list(quarters.crews.values())
        near = [
            gc for gc in crews if any(getattr(guns.get(g), "side", "") == side for g in gc.guns)
        ]
        far = [gc for gc in crews if gc not in near]
        for gc in near + far:
            deck += [s for s in gc.hands if s.fit]
        for name in (HELM, TRIMMERS):
            deck += [s for s in quarters.divisions.get(name, []) if s.fit]
    else:
        clock = None
        try:
            from freesail.combat.hits import _clock_of

            clock = _clock_of(body)
        except Exception:  # noqa: BLE001
            clock = None
        deck = [s for s in (crew.on_deck(clock) if clock is not None else crew.sailors) if s.fit]
    seen: set[str] = set()
    deck = [s for s in deck if not (s.id in seen or seen.add(s.id))]
    return quarterdeck, deck


def strike_a_man(
    body: Any,
    side: str,
    rng: Any,
    tick: int,
    how: str,
    firer_id: str,
    quarterdeck_share: float = QUARTERDECK_SHARE,
) -> Sailor | None:
    """One ball or blow on the mark: the man chosen among the exposed, struck through the
    hit model (the health keeper's states), counted in her damage keeper."""
    from freesail.combat.hits import damage_of, hit_man

    quarterdeck, deck = exposed_men(body, side)
    pool = quarterdeck if (quarterdeck and rng.random() < quarterdeck_share) else deck
    if not pool:
        pool = deck or quarterdeck
    if not pool:
        return None
    s = pool[int(rng.random() * len(pool)) % len(pool)]
    killed = rng.random() < KILLED_SHARE
    hit_man(body, s, killed, rng, tick, how=how)
    keeper = damage_of(body)
    if keeper is not None:
        if killed:
            keeper.killed += 1
        else:
            keeper.wounded += 1
        keeper.minute_men.append(s)
        keeper.struck_by[firer_id] = tick
    return s


def _own_id(world: Any) -> str:
    from freesail.world.brains import PLAYER_ID

    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else PLAYER_ID


def tick(world: Any, ship: Any, target: Any, firer: Any, tick_n: int, rng: Any) -> None:
    """The musketry this tick, and the firer's minute line."""
    m = ship.extra.get("musketry")
    minute = world.clock.ship_time.second == 0
    if m is None:
        return
    if target is None or target.range_m > MUSKET_SHOT_M:
        if minute and m.minute_volleys:
            _minute_line(world, m)
        return
    body = target.body
    if getattr(body, "extra", None) is None or body.extra.get("crew") is None:
        return  # a far vessel: her people are not modelled to be hit (74's)
    if m.mode == "hold" and not (m.served and m.small_arms_mode == "at will"):
        return
    quarters = ship.extra.get("quarters")
    if quarters is None or not getattr(quarters, "at_quarters", False):
        return
    kit = kit_of(world)
    p = hit_chance(kit, float(target.range_m))
    roll = abs(float(getattr(firer, "roll_deg", 0.0) or 0.0))
    scatter = 1.0 / (1.0 + roll / ROLL_SCATTER_DEG)
    marines = marines_of(ship)
    aloft = int(round(len(marines) * float(kit.get("tops_share", 0.2) or 0.0))) if m.in_tops else 0
    on_deck = len(marines) - aloft
    muskets = on_deck + aloft * float(kit.get("tops_factor", 1.0) or 1.0)
    volley_s = max(5.0, float(kit.get("volley_s", 25) or 25))
    mean = 0.0
    volleyed = False
    if m.mode == "volley" and marines:
        last = m.last_volley_tick
        if last is None or tick_n - last >= volley_s:
            m.last_volley_tick = tick_n
            mean += muskets * p * scatter
            volleyed = True
            m.minute_volleys += 1
    elif m.mode == "at will" and marines:
        mean += muskets * p * scatter / volley_s
        if m.last_volley_tick is None or tick_n - m.last_volley_tick >= 60:
            m.last_volley_tick = tick_n
            m.minute_volleys += 1
    if m.served and m.small_arms_mode == "at will":
        mean += small_arms_count(ship) * p * scatter / SMALL_ARMS_SHOT_S
    hits = _poisson(mean, rng)
    if hits:
        side = _bearing_side(body, float(target.bearing_rad) + math.pi)
        own = _own_id(world)
        where = "her tops" if m.in_tops else "her deck"
        from freesail.combat.hits import damage_of

        keeper = damage_of(body)
        minute_key = tick_n // 60
        if keeper is not None and m.told_minute.get(target.id) != minute_key:
            m.told_minute[target.id] = minute_key
            keeper.minute.append(("musketry", f"musketry from {where}"))
        for _ in range(hits):
            how = BALL_WORDS[int(rng.random() * len(BALL_WORDS)) % len(BALL_WORDS)]
            if strike_a_man(body, side, rng, tick_n, how, own) is not None:
                m.minute_hits += 1
    m.minute_target = target.words
    if minute and (m.minute_volleys or m.minute_hits or volleyed):
        _minute_line(world, m)


def _minute_line(world: Any, m: Musketry) -> None:
    if m.mode == "volley":
        how = (
            f"by volley ({number_words(m.minute_volleys)} this minute)"
            if m.minute_volleys
            else "by volley"
        )
    elif m.mode == "at will":
        how = "at will"
    else:
        how = "the small arms at will"
    where = "from the tops and the gangways" if m.in_tops else "from the poop and the gangways"
    fell = (
        f"{number_words(m.minute_hits)} of her people seen to fall"
        if m.minute_hits
        else "nobody seen to fall"
    )
    world.record(
        Severity.NOTABLE,
        "action.musketry",
        f"The marines fire {how} {where} at {m.minute_target or 'the enemy'}: {fell}.",
        data={"volleys": m.minute_volleys, "hits": m.minute_hits, "mode": m.mode},
    )
    m.minute_volleys = 0
    m.minute_hits = 0


def describe(world: Any, ship: Any) -> dict[str, Any]:
    """The marines for the reading: the detachment, its officer, its kit, where it is and
    what it does."""
    crew = ship.extra.get("crew")
    if crew is None:
        return {"words": "no ship's company is mustered", "count": 0}
    all_marines = list(crew.by_station.get(Station.MARINES, []))
    fit = [s for s in all_marines if s.fit]
    if not all_marines:
        return {"words": "none borne: she carries no marines", "count": 0, "fit": 0}
    kit = kit_of(world)
    m = musketry_of(ship)
    quarters = ship.extra.get("quarters")
    at_quarters = bool(quarters is not None and getattr(quarters, "at_quarters", False))
    people = getattr(world, "people", None)
    officer = None
    if people is not None:
        try:
            for p in people.people:
                if p.role in ("lieutenant of marines", "sergeant of marines") and not getattr(
                    p, "dead", False
                ):
                    officer = p
                    if p.role == "lieutenant of marines":
                        break
        except Exception:  # noqa: BLE001
            officer = None
    if officer is not None:
        from freesail.world.people import _address

        under = f" under {_address(officer.role, officer.name)}"
    else:
        under = ""
    head = (
        f"{number_words(len(fit))} fit of {len(all_marines)} ({kit.get('name', 'the marines')}; "
        f"{kit.get('musket', 'the musket')}){under}"
    )
    if at_quarters:
        where = "the poop and the gangways" + (
            ", the book's share in the tops" if m.in_tops else ""
        )
        fire = {"hold": "the fire held", "volley": "firing by volley", "at will": "firing at will"}[
            m.mode
        ]
        words = f"{head}: at quarters on {where}, {fire}"
    else:
        words = (
            f"{head}: the sentries at the cabin door, the spirit room and the gangway, the "
            "rest at the drill or below"
        )
    return {
        "words": words,
        "count": len(all_marines),
        "fit": len(fit),
        "kit": kit.get("id", "basic"),
        "mode": m.mode,
        "in_tops": m.in_tops,
        "at_quarters": at_quarters,
        "officer": officer.name if officer is not None else "",
    }
