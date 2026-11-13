"""The company moved between two hulls (package 60, step 2; `docs/design/Design-ShipBought.md`
§6): one order, `transfer ... to the "Fly"`, of persons by name and hands by count and rating,
between the ship the player commands and a ship that is his to man (the one he left, or one
given him), within a boat's pull or alongside.

The persons move by `movement.put_aboard` and are rehomed (`Registry.rehome`, as the act rehomes
him), so that they belong to the receiving ship's company. The hands are drawn from the giving
muster as `prizes._draw_prize_crew` draws a prize crew (fit, at no work, by id; the order's
ratings first), taken out of it and its quarter bill (`musters.take_out`), and each muster
made again (`musters.remuster`, `musters.deal_watches`): 74's functions, made shared.

The boat's loads take their time (§6.2, JUDGEMENT): twelve men and their bags a load; a load
pulled across, cleared and pulled back in a quarter of an hour within two cables and half an
hour at a mile; alongside, the whole across by the gangway in a quarter of an hour. The men in
the boat are in neither muster while she is away (kept on the giving ship's `extra`, by load),
and each load is said in the receiving ship's log as it comes aboard.

Refused in words (§6.3): either ship left unable to be worked (one watch at her sail-handling
stations, never fewer than four; a ship laid up keeps none), the receiver past a complement and
a half, a company not his to move (a King's ship's to another's), beyond a boat's pull, the
boat away, either ship under way, a prisoner giving it, an observed world.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.core.events import Severity

__all__ = [
    "ALONGSIDE_M",
    "ALONGSIDE_S",
    "LOAD_MEN",
    "LOAD_MILE_S",
    "LOAD_NEAR_S",
    "TransferError",
    "apply_load",
    "berths",
    "transfer",
    "worked_by",
]

# JUDGEMENT (the design's §6.2): a ship's largest boat carries twelve men and their bags a
# load; no boat file carries a capacity.
LOAD_MEN = 12
# JUDGEMENT (§6.2): a load pulled across, cleared and pulled back in a quarter of an hour within
# two cables, half an hour at a mile, and in between by the distance.
LOAD_NEAR_S = 15 * 60
LOAD_MILE_S = 30 * 60
NEAR_NM = 0.2
# JUDGEMENT (§6.2): alongside, the whole across by the gangway in a quarter of an hour.
ALONGSIDE_S = 15 * 60
# Within this of each other the two lie alongside (JUDGEMENT: two hulls' beams and a fender).
ALONGSIDE_M = 30.0
# JUDGEMENT (§6.3): she can be worked by one watch at her sail-handling stations, and never by
# fewer than four.
WORKED_LEAST = 4
# JUDGEMENT (§6.3): never more than her file's complement and a half.
BERTH_SHARE = 1.5
# The stations at which a ship's sail is handled (the forecastle, the tops, the afterguard and
# the waisters: `ship.schema.SEAMAN_STATIONS`).
_SAIL_STATIONS = ("forecastle", "fore_top", "main_top", "mizzen_top", "afterguard", "waisters")
# The ratings an order may name, as the muster's tables say them, with the words for each.
_RATINGS = {
    "able seamen": "able",
    "able seaman": "able",
    "able": "able",
    "ordinary seamen": "ordinary",
    "ordinary seaman": "ordinary",
    "ordinary": "ordinary",
    "landsmen": "landsman",
    "landsman": "landsman",
    "petty officers": "petty officer",
    "petty officer": "petty officer",
    "marines": "marine",
    "marine": "marine",
}
# JUDGEMENT (the design's §4.1, after Falconer 1780, ORDINARY): a King's ship laid in ordinary
# keeps her warrant officers aboard (the gunner, the boatswain, the carpenter, the purser and
# the cook); a merchantman laid up keeps her mate and a ship-keeper, one hand.
KINGS_KEEPERS = ("gunner", "boatswain", "carpenter", "purser", "cook")
MERCHANT_KEEPERS = ("mate", "first mate", "chief mate", "master's mate")
MERCHANT_SHIP_KEEPER_HANDS = 1
# The giving ship's `extra` key for the men in the boat, by load.
IN_THE_BOAT = "transfer_in_the_boat"


class TransferError(ValueError):
    """A transfer refused, in words."""


# -- what a ship needs, and what she berths ------------------------------------------------


def worked_by(hull: Any) -> int:
    """The fewest hands she can be worked by: one watch at her sail-handling stations (half the
    hands her file puts there), never fewer than four (§6.3, JUDGEMENT); a ship laid up her
    keepers alone (§4.1): none for a King's ship, whose keepers are her warrant officers, and
    the ship-keeper for a merchantman."""
    if _laid_up(hull):
        return 0 if _service(hull) == "kings" else MERCHANT_SHIP_KEEPER_HANDS
    crew_spec = getattr(getattr(getattr(hull, "ship", None), "spec", None), "crew", None)
    stations = dict(getattr(crew_spec, "stations", None) or {})
    at_sail = sum(int(stations.get(s, 0) or 0) for s in _SAIL_STATIONS)
    return max(WORKED_LEAST, math.ceil(at_sail / 2))


def berths(hull: Any) -> int:
    """The most she berths: her file's complement and a half (§6.3, JUDGEMENT)."""
    crew_spec = getattr(getattr(getattr(hull, "ship", None), "spec", None), "crew", None)
    complement = int(getattr(crew_spec, "complement", 0) or 0)
    return int(math.floor(complement * BERTH_SHARE))


def _laid_up(hull: Any) -> bool:
    vessel = getattr(hull, "vessel", None)
    return str(getattr(vessel, "regime", "") or "") == "in ordinary"


def _hands(hull: Any) -> list[Any]:
    crew = getattr(getattr(hull, "ship", None), "extra", {}).get("crew")
    return list(crew.sailors) if crew is not None else []


def _souls(hull: Any) -> int:
    """Her hands and her persons aboard: what she berths."""
    people = getattr(hull, "people", None)
    persons = 0
    if people is not None:
        hid = str(getattr(hull, "id", ""))
        persons = sum(
            1
            for p in people.people
            if not getattr(p, "dead", False) and str(getattr(p, "hull", "") or "") == hid
        )
    return len(_hands(hull)) + persons


# -- the order's words -----------------------------------------------------------------------


def read_counts(words: str) -> tuple[bool, dict[str, int], int, list[str]]:
    """(all the hands, by rating, a count of hands, the other words) from the order's words
    before `to the "X"`: 'the people and the hands', 'twenty hands', 'six able seamen and four
    ordinary', 'Mr Ryan and twelve hands'. A rating's count is read by the one reader for
    numbers (`orders.numbers`)."""
    from freesail.orders import numbers

    text = " ".join(str(words).replace(",", " , ").split())
    parts = [p.strip() for p in _split_and(text) if p.strip()]
    every, by_rating, count, rest = False, {}, 0, []
    for part in parts:
        low = part.lower()
        if low in ("the hands", "all the hands", "all hands", "the people and the hands"):
            every = True
            if "people" in low:
                rest.append("the people")
            continue
        if low in ("the people", "all the people", "her people"):
            rest.append("the people")
            continue
        ws = low.split()
        got = numbers.read(ws, 0)
        if got is not None:
            n, used = int(got[0]), got[1]
            what = " ".join(ws[used:])
            if what in ("hands", "hand", "men", "seamen"):
                count += n
                continue
            if what in _RATINGS:
                by_rating[_RATINGS[what]] = by_rating.get(_RATINGS[what], 0) + n
                continue
            raise TransferError(
                f"'{part}' is no number of hands I can read; say 'twenty hands' or 'six able "
                "seamen and four ordinary'."
            )
        rest.append(part)
    return every, by_rating, count, rest


def _split_and(text: str) -> list[str]:
    """The list's parts at its commas and its 'and's; 'the people and the hands' is one part,
    and so is a number said with its 'and' ('a hundred and twenty hands')."""
    from freesail.orders import numbers

    out: list[str] = []
    for chunk in text.split(" , "):
        words = chunk.split()
        cur: list[str] = []
        for w in words:
            if w.lower() == "and" and cur:
                said = " ".join(cur).lower()
                if said != "the people" and numbers.read_all(cur) is None:
                    out.append(" ".join(cur))
                    cur = []
                    continue
            cur.append(w)
        out.append(" ".join(cur))
    return [x.removeprefix("and ").strip() for x in out]


# -- the order -------------------------------------------------------------------------------


def transfer(
    root: Any,
    person: Any,
    receiver: Any,
    words: str,
    *,
    giver: Any = None,
    lay_up: bool = False,
) -> tuple[str, dict[str, Any]]:
    """`transfer <who> [from the "Y"] to the "X"`, given by the player's person aboard either
    ship, of the other: the giver is the ship he is aboard, or, aboard the receiver, the ship
    the words name or the one other ship of his within a boat's pull. Returns the line and its
    data; raises `TransferError` in words, nothing changed."""
    from freesail.world.movement import BOAT_BETWEEN_NM, hull_of

    if getattr(root, "observed", False):
        raise TransferError("There is no ship of the player's in this world to man.")
    if getattr(person, "confined_to", ""):
        raise TransferError(f"{person.name} is a prisoner; he gives no order to her company.")
    here = hull_of(root, getattr(person, "hull", None))
    if here is None:
        raise TransferError("You are aboard no ship; go aboard the ship you move her people from.")
    if giver is None:
        giver = here if receiver is not here else _the_other(root, here)
    if giver is receiver:
        raise TransferError(f"They are aboard the {_name(giver)}; name another ship.")
    if here is not giver and here is not receiver:
        raise TransferError(
            f"You are aboard the {_name(here)}; the order is given aboard the {_name(giver)} or "
            f"the {_name(receiver)}."
        )
    if not _his_to_man(root, giver) or not _his_to_man(root, receiver):
        raise TransferError(
            f"The {_name(giver if not _his_to_man(root, giver) else receiver)} is not yours to "
            "man; her company is moved by the one who commands her."
        )
    _company_his(giver, receiver)
    metres = _between_m(giver, receiver)
    if metres is None or metres / units.NAUTICAL_MILE > BOAT_BETWEEN_NM:
        raise TransferError(
            f"The {_name(receiver)} is beyond a boat's pull ({BOAT_BETWEEN_NM:g} mile); close her "
            "first."
        )
    alongside = metres <= ALONGSIDE_M
    for h in (giver, receiver):
        if _under_way(h) and not alongside:
            raise TransferError(
                f"The {_name(h)} has way on her; heave to or come to an anchor before the boat "
                "is hoisted out."
            )
    dealings = getattr(giver, "dealings", None)
    if not alongside:
        boat = getattr(dealings, "boat", None) if dealings is not None else None
        if boat is not None and getattr(boat, "away", False):
            raise TransferError("The boat is away; the people go across when she is back.")
        if dealings is None or dealings.boat_spec() is None:
            raise TransferError(
                f"The {_name(giver)} carries no boat to put them across; lay her alongside."
            )
    every, by_rating, count, rest = read_counts(words)
    port = _lay_up_port(root, giver) if lay_up else None
    laid = lay_up or _laid_up(giver)
    if lay_up:
        wants = 0 if _service(giver) == "kings" else MERCHANT_SHIP_KEEPER_HANDS
    else:
        wants = worked_by(giver)
    persons = _persons(root, giver, rest, laid)
    men = _draw(giver, every, by_rating, count, keep=wants)
    if not men and not persons:
        raise TransferError(
            "Transfer whom? Say 'transfer the people and the hands to the \"Fly\"', 'transfer "
            "twenty hands to ...' or 'transfer Mr Ryan and twelve hands to ...'."
        )
    keeps = len(_hands(giver)) - len(men)
    if keeps < wants:
        raise TransferError(
            f"The {_name(giver)} would keep {_count_words(keeps)}; she wants "
            f"{_count_words(wants)} to be worked. Transfer fewer, or lay her up first."
        )
    room = berths(receiver)
    would = _souls(receiver) + len(men) + len(persons)
    if room and would > room:
        raise TransferError(
            f"The {_name(receiver)} berths {_number(room)}; she has "
            f"{_number(_souls(receiver))}, and would have {_number(would)}."
        )
    if port is not None:
        from freesail.world.regimes import put_in_ordinary

        vessel = getattr(giver, "vessel", None)
        if vessel is not None:
            put_in_ordinary(root, vessel, port)
    return _put_across(root, giver, receiver, persons, men, metres, alongside)


def _put_across(
    root: Any,
    giver: Any,
    receiver: Any,
    persons: list[Any],
    men: list[Any],
    metres: float,
    alongside: bool,
) -> tuple[str, dict[str, Any]]:
    """The men taken out of the giving muster as their load leaves, the loads made jobs of the
    giving ship's dealings at the boat's pace, each said as it comes aboard."""
    from freesail.world.musters import take_out as _take_out
    from freesail.world.ports import Job

    now = int(root.clock.tick)
    loads = _loads(men, persons, alongside)
    each = ALONGSIDE_S if alongside else _load_s(metres)
    kept = giver.ship.extra.setdefault(IN_THE_BOAT, {})
    serial = int(giver.ship.extra.get(IN_THE_BOAT + "_serial", 0) or 0)
    dealings = giver.dealings
    for i, (load_men, load_persons) in enumerate(loads):
        serial += 1
        key = f"{now}:{serial}"
        # the first load leaves now; each after it as the boat is back
        if i == 0:
            _take_out(giver, load_men)
            for p in load_persons:
                p.where = "boat" if not alongside else p.where
        kept[key] = {"men": list(load_men), "persons": list(load_persons), "left": i == 0}
        due = now + each * (i + 1)
        dealings.jobs.append(
            Job(
                due,
                "transfer",
                "",
                {"key": key, "to": str(receiver.id), "load": i + 1, "of": len(loads)},
                hull=str(giver.id),
            )
        )
    giver.ship.extra[IN_THE_BOAT + "_serial"] = serial
    if not alongside:
        from freesail.world.ports import BoatState

        spec = dealings.boat_spec()
        dealings.boat = BoatState(
            away=True,
            boat_id=spec.id,
            boat_name=spec.name,
            errand="transfer",
            phase=f"putting her people across, {_count_words(len(loads), 'load')}",
            since_tick=now,
            to_hull=str(receiver.id),
            to_name=_name(receiver),
        )
    from freesail.world.musters import remuster

    remuster(giver, giver.ship.extra["crew"])
    who = _who_words(men, persons)
    minutes = _count_words(max(1, round(each * len(loads) / 60)), "minute")
    if alongside:
        how = f"over the gangway to the {_name(receiver)} lying alongside, in some {minutes}"
    else:
        boat = dealings.boat_spec()
        loads_words = "in one load" if len(loads) == 1 else f"in {_count_words(len(loads), 'load')}"
        how = (
            f"across to the {_name(receiver)} by {getattr(boat, 'name', 'the boat')} "
            f"{loads_words}, the last aboard her in some {minutes}"
        )
    text = f"{who[:1].upper()}{who[1:]} to go {how}."
    data = {
        "to": str(receiver.id),
        "from": str(giver.id),
        "hands": len(men),
        "persons": [p.name for p in persons],
        "loads": len(loads),
        "alongside": alongside,
    }
    return text, data


def apply_load(dealings: Any, job: Any) -> None:
    """A load come aboard the receiving ship (the job of `_put_across`): the hands into her
    muster, each muster made again, the persons put aboard her and rehomed, said in her log; the
    next load taken out of the giving muster as the boat goes back for it."""
    from freesail.world.movement import hull_of, put_aboard
    from freesail.world.musters import deal_watches as _watches
    from freesail.world.musters import remuster
    from freesail.world.musters import take_out as _take_out

    root = dealings.world
    giver = hull_of(root, str(job.hull or dealings.hull_id))
    receiver = hull_of(root, str(job.payload.get("to") or ""))
    if giver is None:
        return
    kept = giver.ship.extra.get(IN_THE_BOAT) or {}
    key = str(job.payload.get("key") or "")
    load = kept.pop(key, None)
    if load is None:
        return
    men = list(load.get("men") or [])
    if not load.get("left"):
        _take_out(giver, men)
        remuster(giver, giver.ship.extra["crew"])
    registry = getattr(root, "registry", None)
    persons = list(load.get("persons") or [])
    if receiver is None or getattr(getattr(receiver, "vessel", None), "done", False):
        # she is gone: the men back into their own muster (nothing is lost on the way)
        crew = giver.ship.extra.get("crew")
        if crew is not None:
            crew.sailors.extend(men)
            crew.sailors.sort(key=lambda s: s.id)
            remuster(giver, crew)
        for p in persons:
            p.where = "quarterdeck"
        _boat_home(dealings)
        return
    crew = receiver.ship.extra.get("crew")
    from freesail.crew.model import Crew

    if crew is None:
        crew = Crew(ship_name=_name(receiver), sailors=[])
    taken = {s.id for s in crew.sailors}
    for s in men:
        if s.id in taken:
            s.id = f"{s.id}:{giver.id}"  # told apart by the ship he came from, as a person is
        taken.add(s.id)
        s.post = None
        crew.sailors.append(s)
    crew.sailors.sort(key=lambda s: s.id)
    _watches(crew.sailors)
    remuster(receiver, crew)
    for p in persons:
        put_aboard(root, p, receiver, "quarterdeck", by="the boat", said=False)
        if registry is not None:
            registry.rehome(p, str(receiver.id))
    whence = f"the {_name(giver)}"
    who = _who_words(men, persons)
    n, of = int(job.payload.get("load") or 1), int(job.payload.get("of") or 1)
    part = f" (the {_ordinal(n)} load of {_number(of)})" if of > 1 else ""
    articles = ""
    if men and _service(receiver) != "kings":
        articles = f"; {_count_words(len(men), 'hand')} sign the {_name(receiver)}'s articles"
    receiver.record(
        Severity.NOTABLE,
        "company.came_aboard",
        f"{who[:1].upper()}{who[1:]} came aboard from {whence}{part}{articles}.",
        data={"from": str(giver.id), "hands": len(men), "persons": [p.name for p in persons]},
    )
    if n >= of:
        _boat_home(dealings)
    if n < of:
        # the boat back for the next: its men out of the giving muster now
        for other in kept.values():
            if not other.get("left"):
                _take_out(giver, list(other.get("men") or []))
                other["left"] = True
                remuster(giver, giver.ship.extra["crew"])
                break


def _boat_home(dealings: Any) -> None:
    """The last load aboard her (or she gone): the boat back at the booms."""
    from freesail.world.ports import BoatState

    if getattr(getattr(dealings, "boat", None), "errand", "") != "transfer":
        return
    spec = dealings.boat_spec()
    dealings.boat = BoatState(
        boat_name=getattr(spec, "name", "the boat"), boat_id=getattr(spec, "id", "")
    )


# -- the readings the order needs -------------------------------------------------------------


def _the_other(root: Any, here: Any) -> Any:
    """Aboard the receiving ship with no ship named: the one other ship of his within a boat's
    pull; refused in words where there is none, or more than one."""
    from freesail.world.movement import BOAT_BETWEEN_NM

    near = []
    for hull in (getattr(root, "hulls", None) or {}).values():
        if hull is here or not _his_to_man(root, hull) or _is_boat(hull):
            continue
        metres = _between_m(here, hull)
        if metres is not None and metres / units.NAUTICAL_MILE <= BOAT_BETWEEN_NM:
            near.append(hull)
    if not near:
        raise TransferError(
            f"No other ship of yours lies within a boat's pull of the {_name(here)}; say "
            "'transfer ... from the \"Amazon\" to ...'."
        )
    if len(near) > 1:
        names = " or ".join(f"the {_name(h)}" for h in near)
        raise TransferError(f"From which ship: {names}? Say 'transfer ... from the ... to ...'.")
    return near[0]


def _is_boat(hull: Any) -> bool:
    from freesail.world.boats import is_boat

    return bool(is_boat(hull))


def _his_to_man(root: Any, hull: Any) -> bool:
    """The ship he commands, a ship he has left (`command.HULLS_LEFT`) or one given him."""
    from freesail.world.command import HULLS_LEFT

    hid = str(getattr(hull, "id", ""))
    if hull is getattr(root, "players", None):
        return True
    left = set(root.__dict__.get(HULLS_LEFT) or ())
    given = root.__dict__.get("ships_given") or {}
    return hid in left or hid in given


def _company_his(giver: Any, receiver: Any) -> None:
    """A King's ship's company goes only to another King's ship, and by an order the
    director's form gives (FROM MEMORY: borne on her books, turned over by the Admiralty's
    order); merchant hands sign the new ship's articles."""
    if _service(giver) == "kings" and _service(receiver) != "kings":
        raise TransferError(
            f"The {_name(giver)}'s people are borne on the King's books; they are turned over to "
            "a King's ship alone, by the Admiralty's order."
        )
    if _service(giver) == "kings" or _service(receiver) == "kings":
        # §6.3: a King's ship's company is turned over by an order alone (the director's
        # form, not built in this step); a merchantman's hands do not enter a King's ship by
        # signing her articles
        raise TransferError(
            f"The {_name(giver)}'s people are turned over to the {_name(receiver)} by the "
            "Admiralty's order, not by her captain's."
        )


def _service(hull: Any) -> str:
    from freesail.world.command import _service as service

    return service(hull)


def _persons(root: Any, giver: Any, rest: list[str], laid: bool = False) -> list[Any]:
    """The persons the order names, of the giving ship's company and aboard her; 'the people'
    every one of them but the player, and but her keepers where she is laid up (§4.1)."""
    from freesail.world import knowledge

    me = knowledge.players_person(root)
    people = getattr(giver, "people", None)
    if people is None:
        return []
    gid = str(giver.id)
    hers = [
        p
        for p in people.people
        if not getattr(p, "dead", False)
        and str(getattr(p, "hull", "") or "") == gid
        and str(getattr(p, "home", "") or "") == gid
        and p is not me
        and not getattr(p, "confined_to", "")
    ]
    keepers = KINGS_KEEPERS if _service(giver) == "kings" else MERCHANT_KEEPERS
    out: list[Any] = []
    for words in rest:
        if words == "the people":
            out += [
                p
                for p in hers
                if p not in out and not (laid and str(getattr(p, "role", "")).lower() in keepers)
            ]
            continue
        key = " ".join(words.replace('"', " ").split()).lower()
        found = [p for p in hers if _answers_to(p, key)]
        if not found:
            raise TransferError(
                f"Nobody of the {_name(giver)}'s answers to '{_as_a_name(words)}' aboard her."
            )
        if found[0] not in out:
            out.append(found[0])
    return out


def _answers_to(person: Any, key: str) -> bool:
    name = str(getattr(person, "name", "")).lower()
    role = str(getattr(person, "role", "")).lower()
    bare = key.removeprefix("the ")
    return key == name or bare == role or (len(key) > 3 and name.endswith(key.split()[-1]))


def _draw(
    giver: Any, every: bool, by_rating: dict[str, int], count: int, keep: int = 0
) -> list[Any]:
    """The hands drawn as 74 draws a prize crew: fit, at no work, by id, no post; the order's
    ratings first. 'The hands' are every one of them she can spare, `keep` left her to be
    worked by. Refused in words where she has too few of a rating."""
    from freesail.crew.model import Station

    pool = [
        s
        for s in _hands(giver)
        if s.fit and s.at is None and not s.post and s.station is not Station.QUARTERDECK
    ]
    pool.sort(key=lambda s: s.id)
    if every:
        spare = max(0, len(_hands(giver)) - keep)
        return pool[:spare]
    chosen: list[Any] = []
    for rating, n in by_rating.items():
        of = [s for s in pool if s.rating.value == rating and s not in chosen]
        if len(of) < n:
            raise TransferError(
                f"The {_name(giver)} has {_count_words(len(of))} {rating} fit and free; "
                f"{_count_words(n)} were asked."
            )
        chosen += of[:n]
    if count:
        seamen = [
            s
            for s in pool
            if s not in chosen and s.station not in (Station.MARINES, Station.IDLERS)
        ]
        if len(seamen) < count:
            raise TransferError(
                f"The {_name(giver)} has {_count_words(len(seamen))} fit and free; "
                f"{_count_words(count)} were asked."
            )
        chosen += seamen[:count]
    return chosen


def _loads(men: list[Any], persons: list[Any], alongside: bool) -> list[tuple[list, list]]:
    """The men and the persons in boat loads of `LOAD_MEN`, the persons in the first; one load
    by the gangway alongside."""
    if alongside:
        return [(list(men), list(persons))]
    out: list[tuple[list, list]] = []
    queue = list(persons) + list(men)
    while queue:
        take, queue = queue[:LOAD_MEN], queue[LOAD_MEN:]
        out.append(([x for x in take if x in men], [x for x in take if x in persons]))
    return out or [([], [])]


def _load_s(metres: float) -> int:
    nm = metres / units.NAUTICAL_MILE
    if nm <= NEAR_NM:
        return LOAD_NEAR_S
    share = min(1.0, (nm - NEAR_NM) / (1.0 - NEAR_NM))
    return int(round(LOAD_NEAR_S + share * (LOAD_MILE_S - LOAD_NEAR_S)))


def _lay_up_port(root: Any, giver: Any) -> Any:
    """`..., and lay the Amazon up` in the same order: the port where she lies at an anchor, to
    lay her up at once the order is carried out (`regimes.put_in_ordinary`), so that she needs
    only her keepers; refused in words where she lies at none."""
    ports = getattr(root, "ports", None)
    port = ports.in_port_at(giver.position) if ports is not None and giver.position else None
    if port is None or not getattr(giver, "at_anchor", False):
        raise TransferError(
            f"The {_name(giver)} lies at no anchor in a port; bring her to an anchor in a road "
            "before she is laid up."
        )
    return port


def _between_m(a: Any, b: Any) -> float | None:
    from freesail.world.geo import bearing_and_distance

    pa, pb = getattr(a, "position", None), getattr(b, "position", None)
    if pa is None or pb is None:
        return None
    return float(bearing_and_distance(pa, pb)[1])


def _under_way(hull: Any) -> bool:
    from freesail.world.boats import HOIST_OUT_WAY_MS

    if getattr(hull, "at_anchor", False):
        return False
    dyn = getattr(getattr(hull, "ship", None), "dyn", None)
    return abs(float(getattr(dyn, "u", 0.0) or 0.0)) > HOIST_OUT_WAY_MS


def _name(hull: Any) -> str:
    from freesail.world.movement import hull_name

    return hull_name(hull).removeprefix("the ")


def _who_words(men: list[Any], persons: list[Any]) -> str:
    names = [p.name for p in persons]
    if men:
        names.append(_count_words(len(men), "hand"))
    if not names:
        return "nobody"
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def _count_words(n: int, what: str = "hand") -> str:
    from freesail.combat.guns import count_words

    return f"{count_words(n)} {what}" + ("" if n == 1 else "s")


def _as_a_name(words: str) -> str:
    """The order's words (normalised to the lower case) said as a name: 'Mr Nobody'."""
    small = {"the", "of", "and", "a", "an"}
    return " ".join(w if w in small else w[:1].upper() + w[1:] for w in words.split())


def _number(n: int) -> str:
    from freesail.combat.guns import count_words

    return count_words(n)


def _ordinal(n: int) -> str:
    from freesail.agents.agent import ordinal_words

    return ordinal_words(n)
