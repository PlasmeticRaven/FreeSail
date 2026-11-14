"""The company moved between two hulls (package 60, step 2; `docs/design/Design-ShipBought.md`
§6): one order, `transfer ... to the "Fly"`, of persons by name and hands by count and rating,
between the ship the player commands and a ship that is his to man (the one he left, or one
given him), within a boat's pull or alongside.

This module is the order alone (the lead's reading of ab0ade58: one road, not two): its words,
the men drawn (`musters.draw`, the prize crew's draw), the refusals that are a company's (the
King's books, either ship left unable to be worked, the receiver past her berths, a ship not
his, the officer a ship is left to, his own ship laid up under him), and the lay-up tail. The
boat that carries them is the dealings' road to another hull (`Dealings.send_boat_to`): her pace,
her refusals (no boat, lost, away, beyond the pull), a load at a time of `LOAD_MEN`, every man
told off out of the giving muster from the order, each load into the other ship's watches as
they stand and said in her log, and checked again as the boat comes to where she lay. Alongside
(within `ALONGSIDE_M`) the men cross by the gangway at the order, said in both logs.
"""

from __future__ import annotations

import math
import re
from typing import Any

from freesail import units
from freesail.core.events import Severity

__all__ = [
    "ALONGSIDE_M",
    "LOAD_MEN",
    "TransferError",
    "berths",
    "coming",
    "on_passage",
    "passage_words",
    "say_came_aboard",
    "transfer",
    "worked_by",
]

# JUDGEMENT (the design's §6.2): a ship's largest boat carries twelve men and their bags a
# load; no boat file carries a capacity.
LOAD_MEN = 12
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
    """Her hands: the muster's men off the quarterdeck (its rows are her officers, persons of
    her company counted as such, not twice)."""
    from freesail.crew.model import Station

    crew = getattr(getattr(hull, "ship", None), "extra", {}).get("crew")
    if crew is None:
        return []
    return [s for s in crew.sailors if s.station is not Station.QUARTERDECK]


def on_passage(hull: Any) -> tuple[int, int, str]:
    """Her men in neither muster while her boat carries them (the lead's ruling on the one
    road: counted where a reader finds them): (in her boat now, told off for her next loads,
    the ship they go to); all nought where her boat carries none."""
    boat = getattr(getattr(hull, "dealings", None), "boat", None)
    if boat is None or not getattr(boat, "load_of", 0):
        return 0, 0, ""
    waiting = sum(len(h) for h, _ in boat.loads)
    return len(boat.hands), waiting, str(boat.to_name or "")


def coming(root: Any, hull: Any) -> int:
    """The men in another ship's boat, or told off for her loads, bound for this one: hers to
    berth from the order."""
    hid = str(getattr(hull, "id", ""))
    n = 0
    for other in (getattr(root, "hulls", None) or {}).values():
        boat = getattr(getattr(other, "dealings", None), "boat", None)
        if boat is not None and getattr(boat, "load_of", 0) and str(boat.to_hull) == hid:
            n += len(boat.hands) + sum(len(h) for h, _ in boat.loads)
    return n


def passage_words(hull: Any) -> str:
    """The muster's line for her men on passage: 'Of her company out of the muster: twelve
    hands in the boat for the Fly, three told off for her next load.'; "" where none are."""
    in_boat, waiting, to = on_passage(hull)
    if not in_boat and not waiting:
        return ""
    parts = []
    if in_boat:
        parts.append(f"{_count_words(in_boat)} in the boat for the {to}")
    if waiting:
        parts.append(f"{_count_words(waiting)} told off for her next load")
    return "Of her company out of the muster: " + ", ".join(parts) + "."


def _souls(hull: Any) -> int:
    """Her hands and her persons aboard, and the men in a boat bound for her: what she
    berths."""
    people = getattr(hull, "people", None)
    persons = 0
    if people is not None:
        hid = str(getattr(hull, "id", ""))
        persons = sum(
            1
            for p in people.people
            if not getattr(p, "dead", False) and str(getattr(p, "hull", "") or "") == hid
        )
    from freesail.world.hulls import world_of

    root = world_of(hull) if getattr(hull, "clock", None) is not None else None
    return len(_hands(hull)) + persons + (coming(root, hull) if root is not None else 0)


# -- the order's words -----------------------------------------------------------------------


def read_counts(words: str) -> tuple[bool, dict[str, int], int, list[str]]:
    """(all the hands, by rating, a count of hands, the names) from the order's words before
    `to the "X"`, by the list's grammar (package 60, the lead's fourth round: what a list of
    names IS, everything outside it refused by saying what was not understood):

        list       := part { ("," | "and" | ", and") part }
        part       := collective | count | name
        collective := "the people" | "all the people" | "her people"
                    | "the hands" | "all the hands" | "all hands"
        count      := number ("hands" | "hand" | "men" | "seamen" | a rating)
        name       := [title] word {word}       (a person's address, whole or without its
                                                title, a surname, a title and a surname;
                                                at most four words after the title)
                    | ["the"] word {word}        (a role: "the boatswain", "master-at-arms",
                                                "the lieutenant of marines", "the 2nd mate")
        word       := letters and digits, with a hyphen or an apostrophe within

    No word excludes (there is no "but" or "except"), and none joins but the comma and "and";
    a part that is none of these is refused, saying it was not understood. Whether a name is
    answered by anybody aboard is the persons' reading's (`_persons`, `_answers_to`). A count
    is read by the one reader for numbers (`orders.numbers`); a number said with its own 'and'
    ('a hundred and twenty hands') is one part."""
    from freesail.orders import numbers

    text = " ".join(str(words).replace(";", ",").replace(",", " , ").split())
    parts = [p.strip() for p in _split_and(text) if p.strip()]
    every, by_rating, count, rest = False, {}, 0, []
    for part in parts:
        low = part.lower()
        if low in _HANDS:
            every = True
            continue
        if low in _PEOPLE:
            rest.append("the people")
            continue
        ws = low.split()
        got = numbers.read(ws, 0)
        if got is not None and got[1] > 0:
            n, used = int(got[0]), got[1]
            what = " ".join(ws[used:])
            if what in ("hands", "hand", "men", "seamen"):
                count += n
                continue
            if what in _RATINGS:
                by_rating[_RATINGS[what]] = by_rating.get(_RATINGS[what], 0) + n
                continue
            raise TransferError(_not_understood(part))
        if not name_shaped(low):
            raise TransferError(_not_understood(part))
        rest.append(part)
    return every, by_rating, count, rest


_HANDS = frozenset({"the hands", "all the hands", "all hands"})
_PEOPLE = frozenset({"the people", "all the people", "her people"})


def name_shaped(part: str) -> bool:
    """Whether a part of the list has the shape of a name (the grammar's `name`): one to four
    words after an optional title or 'the', each of letters and digits with a hyphen or an
    apostrophe within (the stop of a contraction read away)."""
    words = part.replace(".", " ").lower().split()
    if not words or any(not _WORD.match(w) for w in words):
        return False
    body = words[1:] if words[0] in _TITLES or words[0] == "the" else words
    return 1 <= len(body) <= 4


_WORD = re.compile(r"^[a-z0-9](?:[a-z0-9'\-]*[a-z0-9])?$")


def _not_understood(part: str) -> str:
    """The refusal of a part that is no name, count or collective, his words given back as he
    said them, in the ship's voice (the lead's fourth reading, item 6)."""
    return (
        f"Who is meant by '{part}'? Name each who goes, as 'Mr Pascoe' or 'the boatswain', or "
        "say how many hands, or 'the people', or 'the hands'."
    )


# The titles a surname may be said with.
_TITLES = frozenset(
    {"mr", "mister", "mrs", "miss", "captain", "lieutenant", "sergeant", "doctor", "dr"}
)


def _split_and(text: str) -> list[str]:
    """The list's parts at its commas and its 'and's ('Mr Pascoe, Richd. Oliver and two hands':
    three parts; 'the people and two hands': two), a number said with its 'and' ('a hundred and
    twenty hands') one part."""
    from freesail.orders import numbers

    out: list[str] = []
    for chunk in text.split(" , "):
        words = chunk.split()
        cur: list[str] = []
        for w in words:
            if w.lower() == "and" and cur and numbers.read_all(cur) is None:
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

    if getattr(root, "observed", False) or person is None:
        raise TransferError("You command no ship here, and move no ship's people.")
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
    for h in (giver, receiver):
        if not _his_to_man(root, h):
            raise TransferError(
                f"The {_name(h)} is not yours to man; her company is moved by the one who "
                "commands her."
            )
    if lay_up and giver is getattr(root, "players", None):
        raise TransferError(
            f"You command her: the {_name(giver)} is laid up when you have left her ('take "
            f"command of ..., and lay the {_name(giver)} up')."
        )
    _company_his(giver, receiver)
    metres = _between_m(giver, receiver)
    if metres is None or metres / units.NAUTICAL_MILE > BOAT_BETWEEN_NM:
        raise TransferError(
            f"The {_name(receiver)} is beyond a boat's pull ({_number(int(BOAT_BETWEEN_NM))} "
            "mile); close her first."
        )
    alongside = metres <= ALONGSIDE_M
    if not alongside:
        from freesail.world.boats import way_on_her

        for h in (giver, receiver):
            refused = way_on_her(h)
            if refused:
                raise TransferError(f"The {_name(h)}{refused.removeprefix('She')}")
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
            f"Transfer whom? Say 'transfer the people and the hands to the {_name(receiver)}', "
            f"'transfer twenty hands to the {_name(receiver)}', or name them."
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
    if alongside:
        said, data = _by_the_gangway(root, giver, receiver, persons, men)
    else:
        said, data = _by_the_boat(giver, receiver, persons, men)
    if port is not None:
        from freesail.world.regimes import put_in_ordinary

        vessel = getattr(giver, "vessel", None)
        if vessel is not None:
            put_in_ordinary(root, vessel, port)
    return said, data


def _by_the_boat(
    giver: Any, receiver: Any, persons: list[Any], men: list[Any]
) -> tuple[str, dict[str, Any]]:
    """The loads by the giving ship's boat, by the dealings' road to another hull
    (`Dealings.send_boat_to`): the first away now, each after it as she is back; every man
    told off out of her muster from the order (her watches as they stand)."""
    from freesail.orders.errors import OrderError
    from freesail.world.musters import take_out

    loads = _loads(men, persons)
    (first_men, first_persons), rest = loads[0], loads[1:]
    boat = giver.dealings.boat
    if boat.lost:
        # in the dealings' own words (`Dealings._send_boat`); the road to another hull has no
        # check of its own of a boat lost, and the lead's ruling keeps that road as it is
        raise TransferError(
            f"{boat.boat_name[:1].upper()}{boat.boat_name[1:]} was "
            f"{boat.lost_words or boat.lost}; a new one is the yard's."
        )
    try:
        sent, _ = giver.dealings.send_boat_to(
            receiver,
            list(first_persons),
            [],
            hands=tuple(first_men),
            join=True,
            loads=tuple((tuple(m), tuple(p)) for m, p in rest),
        )
    except OrderError as e:
        raise TransferError(str(e)) from None
    take_out(giver, men)
    who = _who_words(men, persons)
    how = "in one load" if len(loads) == 1 else f"in {_count_words(len(loads), 'load')}"
    text = f"{who[:1].upper()}{who[1:]} told off for the {_name(receiver)}, {how}. {sent}"
    return text, {
        "to": str(receiver.id),
        "from": str(giver.id),
        "hands": len(men),
        "persons": [p.name for p in persons],
        "loads": len(loads),
        "alongside": False,
    }


def _by_the_gangway(
    root: Any, giver: Any, receiver: Any, persons: list[Any], men: list[Any]
) -> tuple[str, dict[str, Any]]:
    """Alongside her: no boat, the men across by the gangway at the order, into her watches
    as they stand, the persons of her company and put aboard her, said in both logs."""
    from freesail.world.movement import put_aboard
    from freesail.world.musters import join, take_out

    take_out(giver, men)
    join(receiver, men, came_from=str(giver.id))
    registry = getattr(root, "registry", None)
    for p in persons:
        if registry is not None:
            registry.rehome(p, str(receiver.id))
        put_aboard(root, p, receiver, "quarterdeck", by="the gangway", said=False)
    say_came_aboard(receiver, giver, men, persons, 1, 1, by="over the gangway")
    who = _who_words(men, persons)
    text = (
        f"{who[:1].upper()}{who[1:]} across to the {_name(receiver)} lying alongside, over "
        "the gangway."
    )
    giver.record(Severity.NOTABLE, "company.went_across", text, data={"to": str(receiver.id)})
    return text, {
        "to": str(receiver.id),
        "from": str(giver.id),
        "hands": len(men),
        "persons": [p.name for p in persons],
        "loads": 1,
        "alongside": True,
    }


def boat_lost(root: Any, giver: Any, state: Any) -> str:
    """The giving ship's boat lost with a transfer's load in her or told off for her (the
    lead's ruling on the second reading of 4dda3dfe), or with a person she carries on any
    errand (the third reading, item 6: the same rule; ashore or at another ship, the other
    ship where she was sent to one, her own otherwise): the men told off and not yet embarked
    back in their watches; the men and the persons in her picked up by the nearer of the two
    ships (JUDGEMENT: `boats.lose_boat` gives the script's boat's own crew no fate, being no
    persons, and no drowning is invented here), the hands into her watches and the persons
    aboard her, a person bound for the receiver of her company when she is the one; each said
    in that ship's log. Returns the words for the giver's line of the loss."""
    from freesail.world.movement import hull_of, put_aboard
    from freesail.world.musters import join

    receiver = hull_of(root, str(getattr(state, "to_hull", "") or ""))
    if receiver is not None and getattr(getattr(receiver, "vessel", None), "done", False):
        receiver = None
    waiting = [s for hands, _ in state.loads for s in hands]
    if waiting:
        join(giver, waiting, came_from=str(getattr(state, "to_hull", "") or ""))
    nearer = _nearer(giver, receiver, state, int(root.clock.tick))
    men = list(state.hands)
    registry = getattr(root, "registry", None)
    everyone = list(registry.persons()) if registry is not None else []
    persons = [
        p
        for p in everyone
        if p.id in state.people
        and p.hull is None
        and p.where == "boat"
        and str(getattr(p, "home", "") or "") in (str(giver.id), str(getattr(receiver, "id", "")))
    ]
    if men:
        bound = str(getattr(state, "to_hull", "") or "")
        join(nearer, men, came_from=str(giver.id) if nearer is not giver else bound)
    for p in persons:
        if nearer is receiver and p.id in state.joining and registry is not None:
            registry.rehome(p, str(receiver.id))
        put_aboard(root, p, nearer, "deck", by="picked up", said=False)
    parts: list[str] = []
    picked = _who_words(men, persons)
    if men or persons:
        where = "her own side" if nearer is giver else f"the {_name(nearer)}"
        line = f"{picked[:1].upper()}{picked[1:]} picked up out of the water by {where}"
        nearer.record(
            Severity.URGENT,
            "company.picked_up",
            f"{line}." if nearer is giver else f"{line}, from the {_name(giver)}'s boat.",
            data={"from": str(giver.id), "hands": len(men), "persons": [p.name for p in persons]},
        )
        parts.append(f"{picked} picked up by {where}")
    if waiting:
        parts.append(f"{_count_words(len(waiting))} told off for her stand down")
    return ("; " + "; ".join(parts)) if parts else ""


def _nearer(giver: Any, receiver: Any, state: Any, now: int) -> Any:
    """The ship nearer the boat when she is lost (JUDGEMENT, by her stage of the trip): pulling
    for the other ship, the other once she is more than half way there; alongside her, the
    other; pulling back, her own once more than half way home."""
    if receiver is None:
        return giver
    phase = str(getattr(state, "phase", "") or "")
    if phase.startswith("alongside"):
        return receiver
    jobs = [j for j in giver.dealings.jobs if j.kind == "boat_to"]
    due = {j.payload.get("stage"): int(j.due_tick) for j in jobs}
    since = int(getattr(state, "since_tick", 0) or 0)
    if phase.startswith("pulling for") and "alongside" in due:
        span = max(1, due["alongside"] - since)
        return receiver if (now - since) * 2 > span else giver
    if phase.startswith("pulling back") and "back" in due:
        start = due.get("alongside", since)
        span = max(1, due["back"] - start)
        return giver if (now - start) * 2 > span else receiver
    return giver


def say_came_aboard(
    receiver: Any,
    giver: Any,
    men: list[Any],
    persons: list[Any],
    n: int,
    of: int,
    *,
    by: str = "",
) -> None:
    """The receiving ship's log line for a load come aboard (the boat's road and the gangway
    alike): who, from whom, which load of how many, and a merchantman's articles signed."""
    if not men and not persons:
        return
    who = _who_words(men, persons)
    part = f" (the {_ordinal(n)} load of {_number(of)})" if of > 1 else ""
    how = f" {by}" if by else ""
    articles = ""
    if men and _service(receiver) != "kings":
        articles = f"; {_count_words(len(men), 'hand')} sign the {_name(receiver)}'s articles"
    receiver.record(
        Severity.NOTABLE,
        "company.came_aboard",
        f"{who[:1].upper()}{who[1:]} came aboard from the {_name(giver)}{how}{part}{articles}.",
        data={"from": str(giver.id), "hands": len(men), "persons": [p.name for p in persons]},
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
            f"No other ship of yours lies within a boat's pull of the {_name(here)}; close her, "
            f"or give the order aboard the ship her people leave."
        )
    if len(near) > 1:
        names = " or ".join(f"the {_name(h)}" for h in near)
        raise TransferError(
            f"From which ship: {names}? Say 'transfer ... from the {_name(near[0])} to the "
            f"{_name(here)}'."
        )
    return near[0]


def _is_boat(hull: Any) -> bool:
    from freesail.world.boats import is_boat

    return bool(is_boat(hull))


def _his_to_man(root: Any, hull: Any) -> bool:
    """The ship he commands, a ship he has left (`command.HULLS_LEFT`) or one given him."""
    from freesail.world.command import HULLS_LEFT, given_to

    hid = str(getattr(hull, "id", ""))
    if hull is getattr(root, "players", None):
        return True
    left = set(root.__dict__.get(HULLS_LEFT) or ())
    return hid in left or bool(given_to(root, hid))


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
    # the officer she was left to (`People.command_passed_to`; §4): never moved out of her by
    # a transfer while she is in his charge, nor among 'the people'
    left_to = ""
    if giver is not getattr(root, "players", None):
        left_to = str(getattr(people, "command_passed_to", "") or "")
    out: list[Any] = []
    for words in rest:
        if words == "the people":
            out += [
                p
                for p in hers
                if p not in out
                and p.id != left_to
                and not (laid and str(getattr(p, "role", "")).lower() in keepers)
            ]
            continue
        key = " ".join(words.replace('"', " ").split()).lower()
        found = [p for p in hers if _answers_to(p, key)]
        if not found:
            raise TransferError(f"Nobody of the {_name(giver)}'s answers to '{words}' aboard her.")
        if len(found) > 1:
            names = ", ".join(p.name for p in found[:-1]) + f" and {found[-1].name}"
            raise TransferError(f"{names} each answer to '{words}'; name the one who goes.")
        if left_to and found[0].id == left_to:
            raise TransferError(
                f"{found[0].name} has the {_name(giver)} left in his charge; he stays in her "
                "while she is his."
            )
        if found[0] not in out:
            out.append(found[0])
    return out


def _answers_to(person: Any, key: str) -> bool:
    """Whether a name-shaped part names this person (the grammar's `name`): his address whole
    ('Mr Pascoe', 'Richd. Oliver') or without its title ('pascoe', 'john smith' for Mr John
    Smith), his role with 'the' or without ('the boatswain', 'master-at-arms'), or his surname
    after any title ('Mr Oliver', 'Captain Bowen'); the stops of a contraction read away on
    both sides. Never a part's last word alone where the part is more than a surname."""
    name = " ".join(str(getattr(person, "name", "")).lower().replace(".", " ").split())
    role = " ".join(str(getattr(person, "role", "")).lower().split())
    key = " ".join(key.lower().replace(".", " ").split())
    if not key or not name:
        return False
    words = key.split()
    bare = name.split()[1:] if name.split()[0] in _TITLES else name.split()
    if key == name or words == bare or key.removeprefix("the ") == role:
        return True
    surname = name.split()[-1]
    return words == [surname] or (len(words) == 2 and words[0] in _TITLES and words[1] == surname)


def _draw(
    giver: Any, every: bool, by_rating: dict[str, int], count: int, keep: int = 0
) -> list[Any]:
    """The hands drawn by the prize crew's draw (`musters.draw`): fit, at no work, no post,
    in the muster's order; the order's ratings first. 'The hands' are every one of them she can
    spare, `keep` left her to be worked by. Refused in words where she has too few."""
    from freesail.world.musters import draw

    if every:
        spare = max(0, len(_hands(giver)) - keep)
        return draw(giver, spare)
    chosen: list[Any] = []
    for rating, n in by_rating.items():
        got = draw(giver, n, rating=rating, taken={s.id for s in chosen})
        if len(got) < n:
            raise TransferError(
                f"The {_name(giver)} has {_count_words(len(got))} {rating} fit and free; "
                f"{_count_words(n)} were asked."
            )
        chosen += got
    if count:
        got = draw(giver, count, taken={s.id for s in chosen})
        if len(got) < count:
            raise TransferError(
                f"The {_name(giver)} has {_count_words(len(got))} fit and free; "
                f"{_count_words(count)} were asked."
            )
        chosen += got
    return chosen


def _loads(men: list[Any], persons: list[Any]) -> list[tuple[list, list]]:
    """The men and the persons in boat loads of `LOAD_MEN`, the persons in the first."""
    out: list[tuple[list, list]] = []
    queue = list(persons) + list(men)
    while queue:
        take, queue = queue[:LOAD_MEN], queue[LOAD_MEN:]
        out.append(([x for x in take if x in men], [x for x in take if x in persons]))
    return out or [([], [])]


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


def _name(hull: Any) -> str:
    from freesail.world.movement import hull_name

    return hull_name(hull).removeprefix("the ")


def _who_words(men: list[Any], persons: list[Any]) -> str:
    """'Mr Pearce and two hands', by the dealings' own joining of names (`ports._and`)."""
    from freesail.world.ports import _and

    names = [p.name for p in persons]
    if men:
        names.append(_count_words(len(men), "hand"))
    return _and(names) if names else "nobody"


def _count_words(n: int, what: str = "hand") -> str:
    from freesail.combat.guns import count_words

    return f"{count_words(n)} {what}" + ("" if n == 1 else "s")


def _number(n: int) -> str:
    from freesail.combat.guns import count_words

    return count_words(n)


def _ordinal(n: int) -> str:
    from freesail.agents.agent import ordinal_words

    return ordinal_words(n)
