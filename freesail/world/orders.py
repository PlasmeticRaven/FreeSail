"""The world-order channel (spec M5 §26; the proposal's §7.6; package 36).

Orders to the world, not to the ship: append a weather system or a waypoint to one; put
a ship on the sea with a goal, or change her goal; leave a message at a place or send one
by a vessel; change a port's stance or a price; name a person aboard or ashore. They are
given only by a scenario file at a time (`data/scenarios/*.yaml`, `world_orders:`) or by
the lead's test harness (`World.world_order`); never by the captain's grammar, which
refuses one in words (`REFUSAL`; truth 71). Every world order is journaled at its tick
with its source, visible after the fact in the log at the driver's mark (`world.order`,
actor "driver"), saved and replayed (truth 72): the scenario's own are a function of the
scenario and are applied again by a replay from the saved scenario, as the standing
orders' firings are; the harness's go into the save's `inputs` and are given again at
their ticks. This is the seam the director of milestone 7b fills, and the principle's
carrier rule (`docs/design/InwardAndOutward.md`): a world order can send the cutter with
a letter, it cannot put the letter on the cabin table; it can put a brig on the sea, it
cannot put a line in the captain's log. Everything a world order causes reaches the ship
through what she models: the lookout, the boat, the pilot, the messenger and the door.

The words, one order a line, the channel first:

    weather: low "the low" radius 450 km at 1805-06-13T04:00 -300 500 990
    weather: high "the old high" radius 900 km at 1805-06-13T04:00 300 -500 1024
    weather: waypoint for "the low" at 1805-06-13T16:00 -100 400 988
    ship: a merchant brig "Two Brothers" of Britain at 49 50 N 5 30 W, trading Falmouth
        to the Lizard
    ship: a brig-sloop "Harpy" of France at the Iroise, running home to Brest, no colours
    ship: a cutter "Nimble" of Britain at 49 40 N 5 10 W, carrying a letter from the port
        admiral to the ship: "Proceed with all dispatch."
    ship "Two Brothers": running home to Falmouth
    message: at Brest from the Prefect maritime: "The captain is begged to dine."
    message: by a cutter from Plymouth from the port admiral: "Rejoin without delay."
    port brest: closed to the United States
    port brest: open to the United States
    port falmouth: price of tin 130
    person: supercargo "Mr Pentreath" aboard in the cabin
    person: agent "Mr Fox" ashore at Brest
    mark: a wreck, her masts showing above the water at 49 58 N 5 16 W

A ship's goal is one of `freesail.world.ships._goal_plan`: trading A to B, bound from A
for B, patrolling off <place> within <n> miles, running home to <place>, carrying the
mail to <place>, carrying a letter to the ship. A place is a port by name, a feature of
the chart by name, or a position. The descriptions are `ships.DESCRIPTIONS`.

A point of interest (`mark:`, package 45c, the owner's note 23 of gate m6a-2): a thing of
the world with a description at a place, seen by the lookout as a mark is seen (by day and
twilight, at a mark's height), its bearing, distance and description in the log when it
comes in sight; it is the world's (`World.marks_of_interest`), not the chart's, and is
saved and replayed as every world order is.

**The director's additions (spec M7b §3; package 50).** `aboard: <a thing found aboard>`
(`data/director/aboard.yaml`: a spar found sprung, a cask stove, a seam working, the water
foul), each a report of the ship's own people in the play log with what it does in the part
graph or the stores; and **the feasibility check, which doubts and does not refuse**
(decision 50): `doubt(world, order)` says why an order is one the simulation could not have
produced on its own from where it is (a sail put inside the player's horizon in clear
weather, a low out of a steady glass or deeper than the season's floor, a cutter sent from a
port she is far from, a thing found aboard with no cause), and the director's channel
(`freesail/agents/director.py`) answers with the reason and the owner's words: entered again
with a `[reason: ...]` at its end (`parse` peels it into `WorldOrder.reason`), the order is
performed and the director's log keeps the act, the doubt and the reason together. The
scenario's and the owner's orders are never doubted: the doubt is the director's channel's.

**The director's voice (spec M7b §8, §9; package 52).** `person:` makes a person from words
and moves him (`person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Brest, who knew
the captain's father`; `person: "Mr Fox" comes aboard as master`; `person: "Mr Fox" goes
ashore`; `person: "Mr Fox" leaves the ship at Falmouth`), and `say as <person>: <his
words>` (a channel of its own, `say`) puts words in the mouth of a person nobody holds: a
line of the play log in his name where he is, heard by the stations within earshot and
journaled as his, never the order. **The rule of reach**: nobody speaks as, moves or binds
a station to a person a model or the player holds (`reach`), whoever gives the order; the
refusal says which stations are held. The movements are doubted where no boat could carry
him (a port beyond `BOAT_REACH_NM`); a person made and a word said are not.

**The director's hand (spec M7b §3; package 62).** `ship "<name>": order <an order of her
own grammar>` passes the order to her captain's station as his own (`crews.hand`): crewed,
through her World as his order under his rules' actor (her grammar is his domain), at far
detail through the far shape's orders (`crews.far_order`, `submit_far`); her log says it as
his ("By the captain: heaving to"), never a line of the player's log; he holds by it a glass
or until the next order to her, then sails by his intent again (`ship "X": order carry on`
sooner). What the far shape cannot carry is answered in words naming what it can, and
within the promotion's range `ship "X": crewed` asks for her at full detail first, the cap
and its order unchanged. The rule of reach refuses it where a model or the player holds her
captain, and for the player's own ship (`reach`); the doubt bites only where her captain's
order is implausible for her (`_doubt_hand`).
"""

from __future__ import annotations

import functools
import math
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from freesail import units
from freesail.core.events import Severity

__all__ = [
    "CHANNELS",
    "REFUSAL",
    "WorldOrder",
    "WorldOrderError",
    "aboard_table",
    "apply",
    "doubt",
    "parse",
    "held_stations",
    "held_words",
    "reach",
    "recognises",
    "is_hand",
    "say_as_person",
    "split_reason",
]

# The channels a world order speaks on, in the spec's order (§26), and `captain` (spec M6
# §4; package 40): the rules-based captain's intent given or changed, the director's seam;
# `mark` (package 45c): a point of interest; `seat` and `unseat` (spec M6 §23; package 43):
# the director's seat hook, a model seated as the captain of another ship for a budget,
# refused without a consent record, an owner's grant or budget, and the stand-down with
# the director's note.
CHANNELS = (
    "weather",
    "ship",
    "message",
    "port",
    "person",
    "captain",
    "mark",
    "seat",
    "unseat",
    "aboard",
    "say",
)

# The captain's grammar refuses a world order in these words (truth 71).
REFUSAL = (
    "That is an order to the world, not to the ship: the weather, the other sail, a "
    "message, a port and the people ashore are the scenario's and the director's to "
    "order, journaled at the driver's mark; the captain orders his ship, sends the boat "
    "and reads what the lookout sees."
)

# `say as <person>: <words>` (package 52) is the `say` channel's; a bare `say <words>` is the
# deck's conversation and no world order.
_HEAD = re.compile(
    r"^\s*(?:(weather|ship|message|port|person|captain|mark|seat|unseat|aboard)\b"
    r"\s*(\"[^\"]*\"|[\w-]+)?\s*:|(say)\s+as\s+[^:]+:)",
    re.I,
)
# The director's reason at the end of an order entered again after a doubt (decision 50):
# `[reason: the story wants her there]`, peeled off and kept apart.
_REASON = re.compile(r"\s*\[\s*reason\s*:\s*(?P<reason>[^\]]*)\]\s*$", re.I)


class WorldOrderError(ValueError):
    """A world order that cannot be read or carried out, in words."""


@dataclass(frozen=True)
class WorldOrder:
    channel: str
    text: str  # the order as given, which is what the journal keeps (the reason peeled off)
    reason: str = ""  # the director's `[reason: ...]`, when the order was entered again


def recognises(text: str) -> bool:
    """Whether a line is a world order's: a channel's word and a colon, or the words
    'world order' (the captain's grammar refuses either; `orders.handle`)."""
    low = " ".join(str(text).lower().split())
    if low.startswith("world order"):
        return True
    return _HEAD.match(low) is not None


def split_reason(text: str) -> tuple[str, str]:
    """(the order, the director's reason): the `[reason: ...]` at the end peeled off,
    "" when there is none (package 50; decision 50)."""
    text = " ".join(str(text).split())
    rm = _REASON.search(text)
    if rm is None:
        return text, ""
    return text[: rm.start()].rstrip(), " ".join(rm.group("reason").split())


def parse(text: str) -> WorldOrder:
    text, reason = split_reason(text)
    m = _HEAD.match(text)
    if m is None:
        raise WorldOrderError(
            f"'{text}' is no world order: say weather:, ship:, message:, port <id>:, person:, "
            "captain:, mark:, aboard:, seat:, unseat: or say as <person>:."
        )
    return WorldOrder((m.group(1) or m.group(3)).lower(), text, reason)


def apply(world: Any, order: WorldOrder) -> tuple[str, dict[str, Any]]:
    """Carry a world order out on the world: (the words for the journal's line, data).
    Raises `WorldOrderError` in words."""
    body = order.text
    if order.channel == "weather":
        return _weather(world, body)
    if order.channel == "ship":
        return _ship(world, body)
    if order.channel == "message":
        return _message(world, body)
    if order.channel == "port":
        return _port(world, body)
    if order.channel == "captain":
        return _captain(world, body)
    if order.channel == "mark":
        return _mark(world, body)
    if order.channel == "seat":
        return _seat(world, body)
    if order.channel == "unseat":
        return _unseat(world, body)
    if order.channel == "aboard":
        held = reach(world, order)
        if held:
            # the rule of reach for a thing and a held person's money (package 53b)
            raise WorldOrderError(f"{held}; the stations held now: {held_words(world)}")
        return _aboard(world, body)
    held = reach(world, order)
    if held:
        # the rule of reach (package 52): whoever gives the order
        raise WorldOrderError(f"{held}; the stations held now: {held_words(world)}")
    if order.channel == "say":
        return _say_as(world, body)
    return _person(world, body)


# ---------------------------------------------------------------------------
# captain (package 40): the rules-based captain's intent, the director's seam
# ---------------------------------------------------------------------------

_CAPTAIN = re.compile(r"^captain\s*:\s*(?:intent\s+)?(?P<words>.+?)\s*$", re.I)


def _captain(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`captain: intent trade tin from Falmouth to Brest` (or `captain: trade ...`): the
    player's ship's rules-based captain given an intent, or his intent changed; he sails
    by it when no model holds the captain's station. Refused in words when the intent
    cannot be read."""
    m = _CAPTAIN.match(body)
    captain = getattr(world, "captain", None)
    if m is None or captain is None:
        raise WorldOrderError(
            "A captain order is 'captain: intent <the intent in words>' or 'captain: carry on'."
        )
    try:
        if m.group("words").strip().lower() == "carry on":
            # decision 41 (package 40c): the ship given back to him after the player's hand
            words = captain.carry_on()
        else:
            words = captain.set_intent(m.group("words"))
    except ValueError as e:
        raise WorldOrderError(str(e)) from None
    return words, {"intent": captain.intent.words if captain.intent else ""}


# ---------------------------------------------------------------------------
# seat and unseat (spec M6 §23; package 43): the director's seat hook
# ---------------------------------------------------------------------------

_SEAT = re.compile(
    r"^seat:\s*(?P<model>.+?)\s+as\s+captain\s+of\s+(?P<ship>.+?)\s+for\s+"
    r"(?P<n>[\w-]+)\s+(?P<unit>samples?|hours?)\s*$",
    re.I,
)
_UNSEAT = re.compile(r"^unseat:\s*(?P<ship>[^,:]+?)\s*(?:[,:]\s*(?P<note>.+?))?\s*$", re.I)
_SEAT_FORM = (
    "A seat order is 'seat: <the model's exact name> as captain of <ship> for <n> samples' (or "
    "'<n> hours'); 'unseat: <ship>' stands the seat down, a note after a comma."
)


def director_grant(world: Any) -> dict[str, Any]:
    """The owner's grant to the director (spec M6 §23: how many model seats the director
    may hold at once and in a voyage, and which models), the scenario's `director:` block:
    {models: [names], seats: n, seats_in_voyage: m}; empty where the owner gave none."""
    sc = getattr(world, "scenario", None)
    grant = getattr(sc, "director", None) or {}
    return dict(grant) if isinstance(grant, dict) else {}


def director_seats(world: Any) -> dict[str, dict[str, Any]]:
    """The seats the director holds now, by the ship's id (kept on the World; a class
    default for a checkpoint from before)."""
    seats = getattr(world, "director_seats", None)
    if seats is None:
        seats = {}
        try:
            world.director_seats = seats
        except AttributeError:
            pass
    return seats


def _seat(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`seat: <model> as captain of <ship> for <budget>`: refused when no consent record
    holds a yes for that model (the game's own records), when the owner's grant does not
    name it or there is none, when the seats at once or in the voyage are spent, when the
    ship is not on the sea or has no captain of her own; else the seat is held for the
    director's door (M7b writes the agent): a door that comes for that model and that
    ship is admitted under the budget, which the game counts and stands down when spent."""
    from freesail.agents import consent
    from freesail.orders.numbers import read_all

    m = _SEAT.match(body)
    if m is None:
        raise WorldOrderError(_SEAT_FORM)
    model = m.group("model").strip().strip('"')
    n = read_all(m.group("n"))
    if n is None or n <= 0:
        raise WorldOrderError(f"'{m.group('n')}' is no budget; say a number of samples or hours.")
    unit = "hours" if m.group("unit").lower().startswith("hour") else "samples"
    records_dir = getattr(world, "consent_records_dir", None) or consent.RECORDS_DIR
    record = consent.check(model, records_dir)
    if record is None:
        raise WorldOrderError(
            f"No consent is on record for {model}; the consent step comes first, at a door."
        )
    if not record.proceeds:
        raise WorldOrderError(
            f"The consent record for {model} ({record.date}) is no yes with the drill passed "
            f"('{record.verdict}'); the director seats no model whose yes does not stand."
        )
    grant = director_grant(world)
    if not grant:
        raise WorldOrderError(
            "The owner has granted the director no seats (the scenario's 'director:' block: "
            "models, seats, seats_in_voyage)."
        )
    models = [str(x) for x in (grant.get("models") or [])]
    if model not in models:
        raise WorldOrderError(
            f"The owner's grant does not name {model}; it names "
            f"{', '.join(models) if models else 'no model'}."
        )
    seats = director_seats(world)
    at_once = int(grant.get("seats", 1) or 0)
    in_voyage = int(grant.get("seats_in_voyage", at_once) or 0)
    made = int(getattr(world, "director_seats_made", 0) or 0)
    if len(seats) >= at_once:
        raise WorldOrderError(
            f"The director's seats at once are spent ({at_once}): unseat one first."
        )
    if made >= in_voyage:
        raise WorldOrderError(f"The director's seats in this voyage are spent ({in_voyage}).")
    from freesail.world.crews import station_world

    try:
        vessel, _crew = station_world(world, m.group("ship").strip())
    except ValueError as e:
        raise WorldOrderError(str(e)) from None
    if vessel.id in seats:
        raise WorldOrderError(
            f"{vessel.name} has a director's seat already ({seats[vessel.id]['model']})."
        )
    seats[vessel.id] = {
        "model": model,
        "budget": int(n),
        "unit": unit,
        "tick": world.clock.tick,
    }
    world.director_seats_made = made + 1
    return (
        f"the director's seat held for {model} as captain of {vessel.name} for {int(n):g} "
        f"{unit}; a door that comes for her under that name is admitted, and the game stands "
        "the seat down when the budget is spent (the director's own door is milestone 7b's)",
        {"ship": vessel.id, "model": model, "budget": int(n), "unit": unit},
    )


def _unseat(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`unseat: <ship>[, <note>]`: the director's seat on her stood down, with his note,
    the station released and the seat given back to the budget."""
    m = _UNSEAT.match(body)
    if m is None:
        raise WorldOrderError(_SEAT_FORM)
    vessel = world.vessels.find(m.group("ship").strip())
    if vessel is None:
        raise WorldOrderError(f"No ship named {m.group('ship').strip()!r} is on the sea.")
    seats = director_seats(world)
    note = " ".join(str(m.group("note") or "").split()) or "the director's word"
    held = seats.pop(vessel.id, None)
    crew = getattr(vessel, "crew", None)
    stood = ""
    if crew is not None:
        for h in list(crew.agents.values()):
            if not h.agent.released:
                h.stand_down(note, by="the director")
                stood = f"; {h.model_name or 'the station'} stood down"
    if held is None and not stood:
        raise WorldOrderError(f"The director holds no seat on {vessel.name}.")
    return f"the director's seat on {vessel.name} given up ({note}){stood}", {
        "ship": vessel.id,
        "note": note,
    }


# ---------------------------------------------------------------------------
# mark (package 45c): a point of interest
# ---------------------------------------------------------------------------

# the description greedy, so that the last ' at ' is the place's
_MARK = re.compile(r"^mark:\s*(?P<desc>.+)\s+at\s+(?P<where>.+?)\s*$", re.I)
# a mark's height above the sea for the horizon (judgement: a hull and her masts, a
# boat, a cask, a raft: a mark's ten metres, `chart.DEFAULT_HEIGHT_M["mark"]`)
MARK_HEIGHT_M = 10.0


def _mark(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`mark: <description> at <place>`: a point of interest put in the world, which the
    lookout sees as a mark when it is in sight (`Lookout.look`)."""
    from freesail.world.chart import Feature
    from freesail.world.ships import place_position

    m = _MARK.match(body)
    if m is None:
        raise WorldOrderError("A mark order is 'mark: <description> at <place or position>'.")
    desc = m.group("desc").strip().strip('"').strip()
    if not desc:
        raise WorldOrderError("A mark wants a description: 'mark: <description> at <place>'.")
    found = place_position(world, m.group("where"))
    if found is None:
        raise WorldOrderError(f"'{m.group('where')}' is no position and no place of the chart.")
    marks = world.marks_of_interest
    fid = f"interest-{len(marks) + 1}"
    pos = found[0]
    marks.append(
        Feature(
            id=fid,
            kind="mark",
            name=desc,
            lat_deg=pos.lat_deg,
            lon_deg=pos.lon_deg,
            height_m=MARK_HEIGHT_M,
            source="a world order",
            says=desc,
        )
    )
    return f"a mark put in the world, {desc}, at {found[1]}", {
        "id": fid,
        "description": desc,
        "lat_deg": round(pos.lat_deg, 5),
        "lon_deg": round(pos.lon_deg, 5),
    }


# ---------------------------------------------------------------------------
# weather
# ---------------------------------------------------------------------------

_WAYPOINT = re.compile(
    r"^weather:\s*waypoint\s+for\s+\"(?P<name>[^\"]+)\"\s+at\s+(?P<at>\S+)\s+"
    r"(?P<x>-?[\d.]+)\s+(?P<y>-?[\d.]+)\s+(?P<hpa>[\d.]+)\s*$",
    re.I,
)
_SYSTEM = re.compile(
    r"^weather:\s*(?P<kind>low|high)\s+\"(?P<name>[^\"]+)\"(?:\s+radius\s+(?P<r>[\d.]+)\s*km)?"
    r"(?:\s+fronts\s+(?P<warm>[\d.]+)\s+(?P<cold>[\d.]+))?"
    r"\s+at\s+(?P<at>\S+)\s+(?P<x>-?[\d.]+)\s+(?P<y>-?[\d.]+)\s+(?P<hpa>[\d.]+)\s*$",
    re.I,
)


def _time(text: str) -> datetime:
    try:
        return datetime.fromisoformat(text)
    except ValueError:
        raise WorldOrderError(f"'{text}' is not a time like 1805-06-13T04:00.") from None


def _weather(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    systems = getattr(world, "systems", None)
    if systems is None:
        raise WorldOrderError(
            "The world keeps no weather systems (the scenario pins its wind alone); there is "
            "nothing to append to."
        )
    m = _WAYPOINT.match(body)
    if m:
        at = _time(m.group("at"))
        name = m.group("name")
        try:
            systems.append_waypoint(
                name, at, float(m.group("x")), float(m.group("y")), float(m.group("hpa"))
            )
        except ValueError as e:
            raise WorldOrderError(str(e)) from None
        return f"a waypoint appended to {name}", {"system": name, "at": at.isoformat()}
    m = _SYSTEM.match(body)
    if m:
        at = _time(m.group("at"))
        name = m.group("name")
        d: dict[str, Any] = {
            "name": name,
            "kind": m.group("kind").lower(),
            "radius_km": float(m.group("r") or 500.0),
            "track": [
                {
                    "at": at.isoformat(),
                    "x_km": float(m.group("x")),
                    "y_km": float(m.group("y")),
                    "hpa": float(m.group("hpa")),
                }
            ],
        }
        if m.group("warm"):
            d["fronts"] = {"warm_deg": float(m.group("warm")), "cold_deg": float(m.group("cold"))}
        try:
            systems.append_system(d)
        except ValueError as e:
            raise WorldOrderError(str(e)) from None
        return f"{d['kind']} {name!r} appended to the weather", {"system": name}
    raise WorldOrderError(
        'A weather order is \'weather: low "<name>" radius <km> km at <time> <x_km> <y_km> '
        "<hPa>' or 'weather: waypoint for \"<name>\" at <time> <x_km> <y_km> <hPa>'."
    )


# ---------------------------------------------------------------------------
# ship
# ---------------------------------------------------------------------------

_SHIP_NEW = re.compile(
    r"^ship:\s*(?P<desc>(?:a|an|the)\s+[\w' -]+?)\s+\"(?P<name>[^\"]+)\"\s+of\s+"
    r"(?P<nation>[\w' -]+?)\s+at\s+(?P<where>.+?)\s*,\s*(?P<goal>.+?)\s*$",
    re.I,
)
_SHIP_GOAL = re.compile(r"^ship\s+\"(?P<name>[^\"]+)\"\s*:\s*(?P<goal>.+?)\s*$", re.I)
# The tails after a new ship's goal (package 43): `, no colours` and `, intent: <the
# intent in words>` (a brain on her far body, `captains.FarCaptain`), in either order; and
# `ship "X": intent <words>`, a brain given to a ship on the sea or her intent changed.
_SHIP_TAIL = re.compile(r",\s*(?P<tail>no\s+colours|intent:?\s+[^,]+?)\s*$", re.I)
_INTENT_TAIL = re.compile(r"^intent:?\s+(?P<words>.+?)\s*$", re.I)
# The director's hand (spec M7b §3; package 62): `ship "X": order <an order of her own
# grammar>`, given to her captain's station as his own; and `ship "X": crewed`, a far ship
# within the promotion's range asked for at full detail first.
_HAND_TAIL = re.compile(r"^order:?\s+(?P<words>.+?)\s*$", re.I)
_CREWED_TAIL = re.compile(r"^(?:crewed|at\s+full\s+detail)\.?$", re.I)


def _peel_tails(goal: str) -> tuple[str, bool, str]:
    """(the goal, no colours, the intent's words) from a new ship's words after her
    place, the tails peeled from the end in either order."""
    no_colours, intent = False, ""
    while True:
        m = _SHIP_TAIL.search(goal)
        if m is None:
            return goal.strip(), no_colours, intent
        tail = m.group("tail")
        im = _INTENT_TAIL.match(tail)
        if im:
            intent = im.group("words").strip()
        else:
            no_colours = True
        goal = goal[: m.start()]


_LETTER = re.compile(
    r"^(?P<goal>carrying\s+a\s+(?:letter|message|dispatch|despatch)(?:\s+from\s+"
    r"(?P<origin>.+?))?\s+to\s+the\s+ship)\s*:\s*\"(?P<text>[^\"]*)\"\s*$",
    re.I,
)


def _ship(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    from freesail.world.ships import vessel_from_spec

    m = _SHIP_GOAL.match(body)
    if m:
        hm = _HAND_TAIL.match(m.group("goal"))
        if hm or _CREWED_TAIL.match(m.group("goal")):
            return _hand(world, m.group("name"), hm.group("words") if hm else None)
        vessel = world.vessels.find(m.group("name"))
        if vessel is None:
            raise WorldOrderError(f"No ship named {m.group('name')!r} is on the sea.")
        im = _INTENT_TAIL.match(m.group("goal"))
        if im:
            # a brain given to a ship on the sea, or her intent changed (package 43)
            from freesail.world.brains import FarCaptain

            try:
                vessel.warning = ""  # the guard's word on her goal's legs: her captain plans anew
                if vessel.brain is None:
                    vessel.brain = FarCaptain(world, vessel, im.group("words"))
                    vessel.intent_words = vessel.brain.intent_words
                    vessel.brain._plan()
                    words = f"the captain of {vessel.name} given an intent"
                else:
                    if vessel.crew is not None and getattr(vessel.crew, "captain", None):
                        vessel.crew.captain.set_intent(im.group("words"))
                    vessel.brain.set_intent(im.group("words"))
                    vessel.intent_words = vessel.brain.intent_words
                    words = f"the intent of {vessel.name}'s captain changed"
            except ValueError as e:
                raise WorldOrderError(str(e)) from None
            if vessel.warning:
                raise WorldOrderError(f"{vessel.name} {vessel.warning}")
            vessel.done = False
            return f"{words}: {vessel.brain.intent.words}", {
                "id": vessel.id,
                "intent": vessel.brain.intent.words,
            }
        from freesail.world.ships import _goal_plan

        try:
            plan, cycle, goal = _goal_plan(world, m.group("goal"), vessel.position)
        except ValueError as e:
            raise WorldOrderError(str(e)) from None
        vessel.plan, vessel.cycle, vessel.goal, vessel.tack = plan, cycle, goal, 0.0
        vessel.done = False
        return f"the goal of {vessel.name} changed: {goal}", {"id": vessel.id, "goal": goal}
    m = _SHIP_NEW.match(body)
    if m is None:
        raise WorldOrderError(
            "A ship order is 'ship: a <description> \"<name>\" of <nation> at <place>, <goal>' "
            "(then ', no colours' and ', intent: <the intent>' as wanted) or 'ship \"<name>\": "
            "<goal>' or 'ship \"<name>\": intent <the intent>'."
        )
    nation = world.nations.find(m.group("nation"))
    if nation is None:
        raise WorldOrderError(f"'{m.group('nation')}' is no nation of the table.")
    goal, no_colours, intent = _peel_tails(m.group("goal"))
    letter: dict[str, Any] | None = None
    lm = _LETTER.match(goal)
    if lm:
        goal = lm.group("goal")
        letter = {"text": lm.group("text"), "origin": (lm.group("origin") or "").strip()}
    spec: dict[str, Any] = {
        "description": m.group("desc"),
        "name": m.group("name"),
        "nation": nation.id,
        "position": m.group("where"),
        "goal": goal,
        "colours": "none" if no_colours else "shown",
    }
    if intent:
        spec["intent"] = intent
    if letter is not None:
        spec["letter"] = {
            "text": letter["text"],
            "origin": letter["origin"] or m.group("name"),
        }
    world.vessels.serial += 1
    try:
        vessel = vessel_from_spec(world, spec, world.vessels.serial)
    except (ValueError, KeyError) as e:
        raise WorldOrderError(str(e)) from None
    world.vessels.add(vessel)
    brain = f", her captain's intent {vessel.intent_words}" if vessel.brain is not None else ""
    guard = f" ({vessel.warning})" if vessel.warning else ""
    words = f"{vessel.what} {vessel.name!r} of {nation.name} put on the sea, {vessel.goal}"
    data = {"id": vessel.id, "goal": vessel.goal, "nation": nation.id}
    if vessel.intent_words:
        data["intent"] = vessel.intent_words  # on a ship with a brain only: the old pins stand
    return words + brain + guard, data


def is_hand(order: WorldOrder) -> bool:
    """Whether the order is the director's hand (`ship "X": order ...`; package 62)."""
    if order.channel != "ship":
        return False
    m = _SHIP_GOAL.match(order.text)
    return m is not None and _HAND_TAIL.match(m.group("goal")) is not None


def _players_ship(world: Any, name: str) -> bool:
    """Whether a ship's name in an order is the player's own ship's."""
    key = " ".join(str(name).lower().split()).removeprefix("the ")
    ship = getattr(world, "ship", None)
    own = " ".join(str(getattr(ship, "name", "") or "").lower().split()).removeprefix("the ")
    return bool(key) and key in ("ship", own)


def _hand_reach(world: Any, name: str) -> str | None:
    """The rule of reach for the hand (spec M7b §3; package 62): why no order may be given
    through her captain, in words, or None. The player's own ship is never the hand's (her
    captain is the player's at the prompt, or a model's); a ship whose captain's station a
    model or the player holds is his holder's to order."""
    if _players_ship(world, name):
        from freesail.agents.agent import CAPTAIN

        who = next((w for st, _p, w in held_stations(world) if st == CAPTAIN), "the player")
        return (
            f"{name} is the player's own ship, and her captain is held by {who}: the director "
            "moves no sail of hers and gives no order of hers"
        )
    vessel = world.vessels.find(name)
    if vessel is None or vessel.done:
        return None
    from freesail.world.crews import captain_held_by

    held = captain_held_by(vessel)
    if held is None:
        return None
    person, who = held
    return (
        f"{vessel.name}'s captain ({person}) is held by {who}: his orders are his holder's own, "
        "and nobody gives one through him; write to him instead ('message: ...')"
    )


def _hand(world: Any, name: str, words: str | None) -> tuple[str, dict[str, Any]]:
    """`ship "X": order <words>` (the hand) or `ship "X": crewed` (words None): see
    `crews.hand` and `crews.ask_crewed`; the rule of reach whoever gives it."""
    from freesail.world import crews

    held = _hand_reach(world, name)
    if held:
        raise WorldOrderError(held)
    vessel = world.vessels.find(name)
    if vessel is None or vessel.done:
        raise WorldOrderError(f"No ship named {name!r} is on the sea.")
    try:
        if words is None:
            said = crews.ask_crewed(world, vessel)
        else:
            said = crews.hand(world, vessel, words)
    except ValueError as e:
        raise WorldOrderError(str(e).rstrip(".")) from None
    data: dict[str, Any] = {"id": vessel.id}
    if words is None:
        data["crewed"] = True
    else:
        data["hand"] = " ".join(words.split())
    return said, data


# ---------------------------------------------------------------------------
# message
# ---------------------------------------------------------------------------

_MESSAGE_AT = re.compile(
    r"^message:\s*at\s+(?P<port>[\w' -]+?)\s+from\s+(?P<origin>.+?)\s*:\s*\"(?P<text>[^\"]*)\"\s*$",
    re.I,
)
_MESSAGE_BY = re.compile(
    r"^message:\s*by\s+(?:a|the)\s+cutter\s+from\s+(?P<port>[\w' -]+?)\s+from\s+"
    r"(?P<origin>.+?)\s*:\s*\"(?P<text>[^\"]*)\"\s*$",
    re.I,
)


def _message(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    from freesail.world.people import Message

    ports = getattr(world, "ports", None)
    m = _MESSAGE_AT.match(body)
    if m:
        port = ports.find(m.group("port")) if ports is not None else None
        if port is None:
            raise WorldOrderError(f"'{m.group('port')}' is no port of the world.")
        port.letters.append(Message(m.group("text"), m.group("origin").strip()))
        return f"a letter from {m.group('origin').strip()} left at {port.name}", {
            "port": port.id,
            "origin": m.group("origin").strip(),
        }
    m = _MESSAGE_BY.match(body)
    if m:
        port = ports.find(m.group("port")) if ports is not None else None
        if port is None:
            raise WorldOrderError(f"'{m.group('port')}' is no port of the world.")
        origin = m.group("origin").strip()
        spec = {
            "description": "cutter",
            "name": f"the {port.name} cutter",
            "nation": port.nation,
            "position": port.shore.position,
            "goal": "carrying a letter to the ship",
            "letter": {"text": m.group("text"), "origin": origin},
        }
        from freesail.world.ships import vessel_from_spec

        world.vessels.serial += 1
        vessel = vessel_from_spec(world, spec, world.vessels.serial)
        vessel.letter.carried_by = f"the {port.name} cutter"
        world.vessels.add(vessel)
        return f"a cutter sent from {port.name} with a letter from {origin}", {
            "port": port.id,
            "origin": origin,
            "id": vessel.id,
        }
    raise WorldOrderError(
        "A message order is 'message: at <port> from <origin>: \"<text>\"' or 'message: by a "
        'cutter from <port> from <origin>: "<text>"\'.'
    )


# ---------------------------------------------------------------------------
# port
# ---------------------------------------------------------------------------

_PORT = re.compile(
    r"^port\s+(?P<port>\"[^\"]+\"|[\w-]+)\s*:\s*(?P<what>closed to|open to|price of)\s+"
    r"(?P<rest>.+?)\s*$",
    re.I,
)


def _port(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    ports = getattr(world, "ports", None)
    m = _PORT.match(body)
    if m is None:
        raise WorldOrderError(
            "A port order is 'port <id>: closed to <nation>', 'port <id>: open to <nation>' or "
            "'port <id>: price of <good> <pounds>'."
        )
    port = ports.find(m.group("port").strip('"')) if ports is not None else None
    if port is None:
        raise WorldOrderError(f"'{m.group('port')}' is no port of the world.")
    what, rest = m.group("what").lower(), m.group("rest").strip()
    if what in ("closed to", "open to"):
        nation = world.nations.find(rest)
        if nation is None:
            raise WorldOrderError(f"'{rest}' is no nation of the table.")
        if what == "closed to":
            if nation.id not in port.closed_to:
                port.closed_to.append(nation.id)
            words = f"{port.name} closed to {nation.people}"
        else:
            port.closed_to = [n for n in port.closed_to if n != nation.id]
            words = f"{port.name} open to {nation.people}"
        return words, {"port": port.id, "nation": nation.id, "closed_to": list(port.closed_to)}
    pm = re.match(r"^(?P<good>.+?)\s+(?P<pounds>[\d.]+)$", rest)
    if pm is None:
        raise WorldOrderError("Say 'port <id>: price of <good> <pounds a ton>'.")
    good = port.market.find(pm.group("good"))
    if good is None:
        raise WorldOrderError(f"{port.name} deals in no '{pm.group('good')}'.")
    good.price = float(pm.group("pounds"))
    return f"the price of {good.good} at {port.name} set at £{good.price:g} a ton", {
        "port": port.id,
        "good": good.good,
        "pounds": good.price,
    }


# ---------------------------------------------------------------------------
# person
# ---------------------------------------------------------------------------

_PERSON = re.compile(
    r"^person:\s*(?P<role>[\w' -]+?)\s+\"(?P<name>[^\"]+)\"\s+"
    r"(?:(?P<aboard>aboard)(?:\s+in\s+the\s+(?P<place>[\w' -]+))?|ashore\s+at\s+(?P<port>[\w' -]+))"
    r"(?:,\s*skill\s+(?P<skill>[\d.]+))?\s*$",
    re.I,
)


# A person made from words (spec M7b §8; package 52): `person: make "<name>"` and, after
# commas, what the words say of him in any order: a role ('a Guernsey pilot', with an age
# at its end, 'of sixty'), an age ('aged sixty', 'sixty years old'), a place aboard ('aboard
# in the cabin', 'in the gunroom') or ashore ('ashore at Brest', 'at Brest'), and any other
# words as his line of history.
_MAKE = re.compile(r'^person:\s*make\s+"(?P<name>[^"]+)"\s*(?:,\s*(?P<rest>.*?))?\s*$', re.I)
# A person moved: `person: "Mr Fox" comes aboard [as <station>]`, `... goes ashore`,
# `... leaves the ship at <port>` (the name quoted, or bare before the verb).
_MOVE = re.compile(
    r'^person:\s*(?:"(?P<name>[^"]+)"|(?P<bare>.+?))\s+(?P<move>comes\s+aboard'
    r"(?:\s+as\s+(?:the\s+|a\s+|an\s+)?(?P<station>.+?))?|goes\s+ashore"
    r"|leaves\s+the\s+ship\s+at\s+(?P<port>.+?))\s*$",
    re.I,
)
_AGE = re.compile(
    r"^(?:aged\s+(?P<a>[\w -]+?)(?:\s+years?)?|(?P<b>[\w -]+?)\s+years?(?:\s+old|\s+of\s+age)?"
    r"|of\s+(?P<c>[\w -]+?)(?:\s+years?(?:\s+of\s+age)?)?)$",
    re.I,
)
_ROLE_AGE = re.compile(
    r"^(?P<head>.+?)\s+of\s+(?P<n>[\w -]+?)(?:\s+years?(?:\s+of\s+age)?)?$", re.I
)
_ABOARD_AT = re.compile(r"^(?:aboard|on\s+board)(?:\s+(?:in|on)\s+(?P<place>.+))?$", re.I)
_IN_PLACE = re.compile(r"^(?:in|on)\s+(?P<place>.+)$", re.I)
_ASHORE_AT = re.compile(r"^ashore(?:\s+(?:at|in)\s+(?P<port>.+))?$", re.I)
_AT_PORT = re.compile(r"^(?:at|of)\s+(?P<port>.+)$", re.I)
# A person put ashore or taken aboard by a boat within this many miles of the port's roads
# (judgement: a shore boat or the pilot's comes off to a ship lying off the port, and the
# pilots board at their stations some miles out; spec M7b §8's movements are doubted beyond).
BOAT_REACH_NM = 6.0
# A person made from words with no skill said has the old form's (`person: ... skill`).
MADE_SKILL = 0.7


def _age_of(words: str) -> int:
    """An age in years from the words ('sixty', '60', 'sixty two'), or 0."""
    from freesail.orders.numbers import read_all

    n = read_all(" ".join(str(words).replace("-", " ").split()))
    return int(n) if n is not None and 0 < n < 120 else 0


def _role_of(words: str) -> tuple[str, list[str]]:
    """(the role, the words that qualify it) from 'Guernsey pilot', 'merchant of Brest',
    'retired master's mate': the role the people's table knows at its end, else its last
    word; the rest kept as said."""
    from freesail.world.people import ROLE_WORDS

    quals: list[str] = []
    om = re.match(r"^(?P<head>.+?)\s+(?P<of>of\s+.+)$", words, re.I)
    if om is not None:
        words, quals = om.group("head"), [om.group("of")]
    parts = words.split()
    low = [w.lower() for w in parts]
    for n in range(min(3, len(parts)), 0, -1):
        tail = " ".join(low[-n:])
        if tail in ROLE_WORDS:
            head = " ".join(parts[:-n])
            return ROLE_WORDS[tail], [x for x in [head, *quals] if x]
    head = " ".join(parts[:-1])
    return (low[-1] if low else ""), [x for x in [head, *quals] if x]


def _port_miles(world: Any, port: Any) -> float | None:
    """The miles from the ship to the port's nearest roads or mooring, or None."""
    pos = getattr(world, "position", None)
    if pos is None or port is None:
        return None
    return float(port.nearest_spot(pos)[1])


def _make_person(world: Any, name: str, rest: str) -> tuple[str, dict[str, Any]]:
    """`person: make "<name>", <the words>`: a person with an outline from the words, among
    the world's people from now on (spec M7b §8; package 52)."""
    from freesail.world.people import TRADE_PLACES, Outline, Person
    from freesail.world.places import PLACES, Places, place_words

    name = " ".join(str(name).split())
    if not name:
        raise WorldOrderError(
            "A person made from words wants a name: 'person: make \"Mr Fox\", ...'."
        )
    if world.people.find(name) is not None:
        raise WorldOrderError(f"{name} is among the people already.")
    ports = getattr(world, "ports", None)
    places = Places()
    role, quals, age, history, rank = "", [], 0, [], ""
    aboard: bool | None = None
    place, port_words = "", ""
    ashore_said: list[tuple[str, str]] = []
    for phrase in [" ".join(x.split()) for x in str(rest).split(",") if x.strip()]:
        low = phrase.lower()
        am = _AGE.match(low)
        if am is not None and _age_of(am.group("a") or am.group("b") or am.group("c") or ""):
            age = _age_of(am.group("a") or am.group("b") or am.group("c") or "")
            continue
        m = _ABOARD_AT.match(phrase)
        if m is not None:
            aboard = True
            found = places.find(m.group("place")) if m.group("place") else None
            if m.group("place") and (found is None or not found.aboard):
                raise WorldOrderError(
                    f"'{m.group('place')}' is no place aboard; the places are "
                    f"{', '.join(p.name for p in PLACES.values() if p.aboard)}."
                )
            place = found.id if found is not None else ""
            continue
        m = _ASHORE_AT.match(phrase)
        if m is not None:
            aboard, port_words = False, (m.group("port") or "").strip()
            continue
        if not role and low.startswith(("a ", "an ", "the ")):
            words = phrase.split(None, 1)[1] if " " in phrase else ""
            rm = _ROLE_AGE.match(words)
            if rm is not None and _age_of(rm.group("n")):
                age, words = _age_of(rm.group("n")), rm.group("head")
            role, quals = _role_of(words)
            rank = " ".join(words.split())  # who he is, as said: 'Guernsey pilot'
            continue
        m = _IN_PLACE.match(phrase)
        found = places.find(m.group("place")) if m is not None else None
        if found is not None and found.aboard:
            aboard, place = True, found.id
            continue
        m = _AT_PORT.match(phrase)
        if m is not None and ports is not None and ports.find(m.group("port")) is not None:
            aboard, port_words = False, m.group("port").strip()
            continue
        # a place ashore ('in the tavern', 'at the counting house'; package 53), read once
        # the port is known, and his history's words else
        m = _IN_PLACE.match(phrase) or _AT_PORT.match(phrase)
        if m is not None:
            ashore_said.append((phrase, m.groupdict().get("place") or m.group("port") or ""))
        history.append(phrase)
    port = None
    if aboard is False:
        if port_words:
            port = ports.find(port_words) if ports is not None else None
            if port is None:
                raise WorldOrderError(f"'{port_words}' is no port of the world.")
        else:
            near = ports.nearest() if ports is not None else None
            if near is None:
                raise WorldOrderError("Ashore where? Say 'ashore at <port>'.")
            port = near[0]
    else:
        aboard = True
        place = place or TRADE_PLACES.get(role, "cabin")
    ashore_at = ""
    if not aboard and port is not None:
        from freesail.world.places import find_port_place

        for phrase, words in ashore_said:
            found = find_port_place(port, words)
            if found is not None:
                ashore_at = found.id
                history.remove(phrase)
                break
    outline = Outline(
        role=role,
        rank=rank or role,
        place=place if aboard else "",
        history="; ".join(history),
        age=age,
        said=" ".join(str(rest).split()),
    )
    pid = re.sub(r"[^a-z0-9]+", "_", f"{role} {name}".lower()).strip("_")
    person = Person(
        pid,
        name,
        role,
        MADE_SKILL,
        place=place if aboard else "shore",
        aboard=bool(aboard),
        port=port.id if port is not None else None,
        outline=outline,
        ashore_at=ashore_at,
    )
    world.people.add(person)
    where = place_words(place) if aboard else f"ashore at {port.name}"
    if ashore_at:
        from freesail.world.movement import ashore_place_words

        where += f", {ashore_place_words(ashore_at, port)}"
    data: dict[str, Any] = {"id": pid, "name": name, "role": role, "aboard": bool(aboard)}
    if age:
        data["age"] = age
    if aboard:
        data["place"] = place
    else:
        data["port"] = port.id
        if ashore_at:
            data["ashore_at"] = ashore_at
    return f"{person.outline_words().rstrip('.')}; made from words, {where}", data


def _station_key(words: str) -> str:
    from freesail.agents.agent import station_name

    return station_name(" ".join(str(words).lower().split()).removesuffix("'s station"))


def _move_person(world: Any, m: re.Match[str]) -> tuple[str, dict[str, Any]]:
    """`person: "Mr Fox" comes aboard [as <station>]`, `... goes ashore`, `... leaves the
    ship at <port>` (spec M7b §8; package 52): the person moved, his coming or going a
    line of the play log, a station bound to him or unbound from him with its own line."""
    from freesail.world.places import place_words

    name = " ".join(str(m.group("name") or m.group("bare") or "").split()).strip('"')
    person = world.people.find(name)
    if person is None:
        raise WorldOrderError(
            f"Nobody named {name} is among the people; make him first: 'person: make "
            f'"{name}", ...\'.'
        )
    move = " ".join(m.group("move").lower().split())
    stations = world.stations
    ports = getattr(world, "ports", None)
    data: dict[str, Any] = {"person": person.name}
    if move.startswith("comes aboard"):
        said = []
        if not person.aboard:
            came = ports.ports.get(person.port) if (ports is not None and person.port) else None
            person.aboard = True
            person.where = "quarterdeck"
            whence = f" from {came.name}" if came is not None else ""
            world.record(
                Severity.NOTABLE,
                "person.aboard",
                f"{person.name} came aboard{whence}.",
                data={"person": person.name, "from": came.id if came is not None else ""},
            )
            said.append(f"{person.name} came aboard{whence}")
            data["came_aboard"] = True
        station = m.group("station")
        if station:
            key = _station_key(station)
            if stations.aboard(key) or key in stations.kinds():
                stations.bind(key, person, quiet=True)
                person.station = key
                said.append(f"the {key}'s station bound to him")
                data["station"] = key
            else:
                role = " ".join(station.lower().split())
                person.role = role
                said.append(f"borne as {role} (no station of that name aboard)")
                data["role"] = role
        if not said:
            raise WorldOrderError(
                f"{person.name} is aboard already ({world.people.state_words(person)})."
            )
        return "; ".join(said), data
    # ashore: by the boat, at the nearest port or the one named
    if not person.aboard:
        raise WorldOrderError(f"{person.name} is {place_words(person.where)} already.")
    if person is world.people.captain or person.mirror is not None:
        does = "commands" if person is world.people.captain else "keeps the reckoning"
        raise WorldOrderError(
            f"{person.name} {does} and cannot be put ashore by the game yet (the player "
            "ashore, and a ship left to her officers, are spec M7b §14's)"
        )
    if move.startswith("goes ashore"):
        near = ports.nearest() if ports is not None else None
        if near is None:
            raise WorldOrderError(
                "No port is near to put him ashore at; say 'leaves the ship at <port>'."
            )
        port = near[0]
    else:
        port = ports.find(m.group("port")) if ports is not None else None
        if port is None:
            raise WorldOrderError(f"'{m.group('port')}' is no port of the world.")
    for st in stations.names():
        try:
            holder = stations.holder(st)
        except Exception:  # a people's build that cannot run binds nobody
            holder = None
        if holder is not person:
            continue
        # the station goes back to the person the wardroom file binds it to, where he is
        # aboard and another (Mr Fox, brought aboard as master, leaves: the master's is Mr
        # Harvey's again); else it is unbound, with nobody left to hold it
        try:
            kept = stations._file_holder(st)
        except Exception:  # a people's build that cannot run binds nobody
            kept = None
        if kept is not None and kept is not person and kept.aboard:
            stations.bind(st, kept, quiet=True)
        else:
            stations.unbind(st, why=f"{person.name} went ashore at {port.name}", quiet=True)
    person.station = ""
    person.aboard = False
    person.place = "shore"
    person.port = port.id
    verb = "went ashore at" if move.startswith("goes") else "left the ship at"
    world.record(
        Severity.NOTABLE,
        "person.ashore",
        f"{person.name} {verb} {port.name}.",
        data={"person": person.name, "port": port.id},
    )
    data["port"] = port.id
    return f"{person.name} {verb} {port.name}", data


def _person(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    from freesail.world.people import Person
    from freesail.world.places import PLACES

    mm = _MAKE.match(body)
    if mm is not None:
        return _make_person(world, mm.group("name"), mm.group("rest") or "")
    mv = _MOVE.match(body)
    if mv is not None:
        return _move_person(world, mv)
    m = _PERSON.match(body)
    if m is None:
        raise WorldOrderError(
            'A person order is \'person: make "<name>", <who he is, his age, where he is, his '
            "history>', 'person: \"<name>\" comes aboard [as <station>]', 'person: \"<name>\" "
            "goes ashore', 'person: \"<name>\" leaves the ship at <port>', 'person: <role> "
            '"<name>" aboard in the <place>\' or \'person: <role> "<name>" ashore at <port>\'.'
        )
    role = m.group("role").strip().lower()
    name = m.group("name").strip()
    skill = float(m.group("skill") or 0.7)
    pid = re.sub(r"[^a-z0-9]+", "_", f"{role} {name}".lower()).strip("_")
    if world.people.find(name) is not None:
        raise WorldOrderError(f"{name} is among the people already.")
    if m.group("aboard"):
        place = (m.group("place") or "cabin").strip().lower().replace(" ", "_")
        if place not in PLACES:
            raise WorldOrderError(
                f"'{place}' is no place aboard; the places are {', '.join(PLACES)}."
            )
        world.people.add(Person(pid, name, role, skill, place=place))
        return f"{name}, {role}, aboard {PLACES[place].name}", {
            "id": pid,
            "role": role,
            "place": place,
        }
    ports = getattr(world, "ports", None)
    port = ports.find(m.group("port")) if ports is not None else None
    if port is None:
        raise WorldOrderError(f"'{m.group('port')}' is no port of the world.")
    world.people.add(Person(pid, name, role, skill, place="shore", aboard=False, port=port.id))
    return f"{name}, {role}, ashore at {port.name}", {"id": pid, "role": role, "port": port.id}


# ---------------------------------------------------------------------------
# say as (spec M7b §9; package 52): words in the mouth of a person nobody holds
# ---------------------------------------------------------------------------

_SAY_AS = re.compile(r"^say\s+as\s+(?P<who>[^:]+?)\s*:\s*(?P<words>.*?)\s*$", re.I)
# The log's kind for a person's words said by the director's voice: a word on deck.
PERSON_SPOKE_KIND = "person.spoke"
_QUOTES = "\"'\u201c\u201d\u2018\u2019"


def _say_as_parts(world: Any, body: str, draw: bool) -> tuple[Any, str]:
    """(the person, his words) of a `say as` order; the man of the muster by his trade
    drawn into the people only when `draw` (`People.of_the_company`)."""
    m = _SAY_AS.match(body)
    if m is None:
        raise WorldOrderError("A word put in a mouth is 'say as <person>: <his words>'.")
    words = m.group("words").strip()
    if len(words) >= 2 and words[0] in _QUOTES and words[-1] in _QUOTES:
        words = words[1:-1].strip()
    if not words:
        raise WorldOrderError("Say what as him? Put his words after the colon.")
    who = " ".join(m.group("who").split()).strip(_QUOTES)
    people = getattr(world, "people", None)
    # one of the people by role or name first, as before; then a station's person or one
    # of the ship's own voices (package 66); then a man of the muster by his trade
    person = people.find(who) if people is not None else None
    if person is None:
        person = _by_station_or_voice(world, who)
    if person is None:
        person = people.of_the_company(who, draw=draw) if people is not None else None
    if person is None:
        raise WorldOrderError(
            f"nobody answering to '{who}' is among the people or the ship's company; a person "
            'ashore or a stranger is made first (\'person: make "<name>", <who he is>, '
            "<where>')"
        )
    return person, words


@dataclass
class Voice:
    """A speaker of the ship's who is no person of the people (package 66; the dispatches
    test's finding 2): the lookout at the masthead, whose hail reaches the deck, and the
    hands on deck. He speaks where he is, is journaled by his name, and is never drawn
    into the people."""

    name: str  # "the lookout", "the hands"
    role: str
    place: str  # "masthead", "deck"
    station: str = ""  # the station whose holder's words would be his ('lookout')
    aboard: bool = True
    port: str | None = None

    @property
    def where(self) -> str:
        return self.place


# The words that name the ship's own voices, by their key (`_words`-like, lower case).
VOICE_WORDS: dict[str, tuple[str, str, str, str]] = {
    "lookout": ("the lookout", "lookout", "masthead", "lookout"),
    "the lookout": ("the lookout", "lookout", "masthead", "lookout"),
    "the lookout at the masthead": ("the lookout", "lookout", "masthead", "lookout"),
    "the masthead": ("the lookout", "lookout", "masthead", "lookout"),
    "the masthead lookout": ("the lookout", "lookout", "masthead", "lookout"),
    "the hands": ("the hands", "hands", "deck", ""),
    "hands": ("the hands", "hands", "deck", ""),
    "the people": ("the hands", "hands", "deck", ""),
    "the men": ("the hands", "hands", "deck", ""),
    "the watch": ("the hands", "hands", "deck", ""),
    "the watch on deck": ("the hands", "hands", "deck", ""),
}


def _by_station_or_voice(world: Any, who: str) -> Any:
    """`say as` by station or trade (package 66): the person a station of the ship is
    bound to ('the officer of the watch', 'the second officer', 'the lookout' where the
    wardroom file binds one), or one of the ship's own voices (`VOICE_WORDS`: the lookout
    at the masthead, the hands on deck); None for anything else, which is found among the
    people and the muster as before."""
    key = " ".join(str(who).lower().replace("’", "'").split()).strip(".")
    stations = getattr(world, "stations", None)
    name = key.removeprefix("the ")
    if stations is not None:
        try:
            names = list(stations.names())
        except Exception:  # noqa: BLE001  (a world whose stations cannot be read)
            names = []
        if name in names:
            try:
                bound = stations.holder(name)
            except Exception:  # noqa: BLE001
                bound = None
            if bound is not None:
                return bound
    voice = VOICE_WORDS.get(key)
    if voice is None:
        return None
    return Voice(*voice)


def say_as_person(world: Any, body: str) -> Any:
    """The person a `say as` order names, drawn into nothing (for the director's door and
    the rule of reach); None when it names nobody."""
    try:
        return _say_as_parts(world, body, draw=False)[0]
    except WorldOrderError:
        return None


def _hearers(world: Any, place: str) -> list[Any]:
    """The stations held (not the director's, which has no place aboard) within earshot of
    a word said in `place` (`places.earshot`), each with its place."""
    from freesail.agents.agent import DIRECTOR, place_of
    from freesail.agents.harness import _stations_held
    from freesail.world.places import earshot

    near = earshot("quarterdeck" if place == "deck" else place) | earshot(place)
    return [
        h
        for h in _stations_held(world)
        if h.station.name != DIRECTOR and place_of(world, h.station.name) in near
    ]


def _say_as(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`say as <person>: <his words>`: a line of the play log in his name where he is
    (`person.spoke`, notable: a word on deck for the stand-bys), heard by the stations
    within earshot in their next samples, journaled as his (`journal.person_journal`); an
    answer to a question put to him while nobody held him goes back to the asker
    (`director.answer_questions`). A person ashore is heard aboard only while the ship
    lies within a boat's reach of his port."""
    from freesail.agents.journal import SAID_KIND, person_journal
    from freesail.world.places import place_words

    person, words = _say_as_parts(world, body, draw=True)
    people = world.people
    voice = isinstance(person, Voice)
    if voice and person.place == "masthead":
        # the lookout's hail from the masthead reaches the deck (package 66)
        place, where = "masthead", "from the masthead"
        heard = _hearers(world, "quarterdeck")
        heard += [h for h in _hearers(world, "masthead") if h not in heard]
    elif voice:
        place = person.place
        where = place_words(place)
        heard = _hearers(world, place)
    elif person.aboard:
        place = people.effective_place(person)
        where = place_words(place)
        heard = _hearers(world, place)
    else:
        ports = getattr(world, "ports", None)
        port = ports.ports.get(person.port) if (ports is not None and person.port) else None
        miles = _port_miles(world, port)
        if port is None or miles is None or miles > BOAT_REACH_NM:
            at = f" at {port.name}, {miles:.0f} miles off" if (port and miles is not None) else ""
            raise WorldOrderError(
                f"nobody aboard can hear {person.name}: he is {place_words(person.where)}{at}; "
                f"a letter carries his words ('message: at <port> from {person.name}: "
                '"..."\'), or he comes aboard'
            )
        place, where = "shore", f"ashore at {port.name}"
        # package 66: heard by the stations held at the same place of the same port (the
        # captain at the counting house hears the clerk there; at the market he does not)
        heard = _hearers_ashore(world, person)
    role = person.role
    tail = f", the {role}" if role and role not in ("captain", "commander") else ""
    if role and role.lower() in person.name.lower():
        tail = ""
    line = f"{person.name}{tail}, {where}: {words}"
    if voice:
        line = line[:1].upper() + line[1:]  # 'The lookout, from the masthead: ...'
    for h in heard:
        h.hear(line)
    names = [h.station.name for h in heard]
    world.record(
        Severity.NOTABLE,
        PERSON_SPOKE_KIND,
        line,
        data={
            "person": person.name,
            "role": role,
            "place": place,
            "where": where,
            "words": words,
            "heard_by": names,
        },
    )
    person_journal(world, person).append(world, f"Said, {where}: {words}", kind=SAID_KIND)
    from freesail.agents.director import answer_questions

    answered = answer_questions(world, person, words, where)
    # who heard it (package 66): the people within hearing by name, the stations held
    # among them, or nobody and where the stations held are
    from freesail.world.hearing import heard_words, spot_of

    spot = ("aboard", "quarterdeck") if place == "masthead" else spot_of(world, person)
    said = heard_words(world, spot, person, names, absent=_wanted(world))
    data: dict[str, Any] = {"person": person.name, "heard_by": names}
    if answered:
        data["answered"] = answered
    return f"{person.name} spoke {where}, {said}", data


def _hearers_ashore(world: Any, person: Any) -> list[Any]:
    """The stations held whose person is at the same place ashore as `person` (package
    66; the director's has no place)."""
    from freesail.agents.agent import DIRECTOR
    from freesail.agents.harness import _stations_held
    from freesail.world.hearing import spot_of, station_spot, within_hearing

    here = spot_of(world, person)
    return [
        h
        for h in _stations_held(world)
        if h.station.name != DIRECTOR and within_hearing(here, station_spot(world, h.station.name))
    ]


def _wanted(world: Any) -> Any:
    """The person a word put in a mouth is most likely for, named where nobody heard it:
    the captain's (the station held by a model or the player at the prompt)."""
    people = getattr(world, "people", None)
    try:
        return people.captain if people is not None else None
    except Exception:  # noqa: BLE001  (a world with no muster)
        return None


def held_stations(world: Any) -> list[tuple[str, str, str]]:
    """The stations of the ship held now, as (the station, its person's name or "", who
    holds it): a model's, the player's seat, and the captain's by the player at the prompt
    while no model holds it and the player is seated nowhere else (package 52; the rule of
    reach)."""
    from freesail.agents.agent import CAPTAIN, DIRECTOR
    from freesail.agents.harness import _stations_held

    out: list[tuple[str, str, str]] = []
    stations = getattr(world, "stations", None)
    seat = getattr(world, "player_seat", None)
    held: set[str] = set()
    for h in _stations_held(world):
        name = h.station.name
        if name == DIRECTOR:
            continue
        try:
            holder = stations.holder(name) if stations is not None else None
        except Exception:  # a people's build that cannot run binds nobody
            holder = None
        who = "the player at his seat" if h is seat else "a model"
        out.append((name, holder.name if holder is not None else "", who))
        held.add(name)
    if CAPTAIN not in held and (seat is None or seat.agent.released):
        people = getattr(world, "people", None)
        try:
            cap = people.captain if people is not None else None
        except Exception:  # a world with no muster
            cap = None
        out.append((CAPTAIN, cap.name if cap is not None else "", "the player at the prompt"))
    return out


def held_words(world: Any) -> str:
    """The stations held now in words, for the rule of reach's refusal and the truth."""
    parts = []
    for station, person, who in held_stations(world):
        parts.append(f"the {station} ({person + ', ' if person else ''}{who})")
    return "; ".join(parts) if parts else "none"


def reach(world: Any, order: WorldOrder) -> str | None:
    """**The rule of reach** (spec M7b §9; package 52): why the order would speak as, move,
    or bind a station to a person a model or the player holds, in words, or None. The
    director speaks as anyone nobody holds and never as a held station, whose words are
    its holder's own; and so moves nobody held and binds nobody to a held station."""
    if order.channel == "ship":
        # the director's hand (package 62): no order through a captain a model or the
        # player holds, and none of the player's own ship
        m = _SHIP_GOAL.match(order.text)
        if m is None or _HAND_TAIL.match(m.group("goal")) is None:
            return None
        return _hand_reach(world, m.group("name"))
    if order.channel == "aboard":
        # package 53b: a thing into or out of a held person's keeping, and his money
        return _aboard_reach(world, order.text)
    if order.channel not in ("say", "person"):
        return None
    held = {person: (station, who) for station, person, who in held_stations(world) if person}
    stations_held = {station: who for station, _person, who in held_stations(world)}
    if order.channel == "say":
        person = say_as_person(world, order.text)
        if isinstance(person, Voice) and person.station in stations_held:
            # the lookout's station held (package 66): his hail is his holder's own
            return (
                f"the {person.station}'s station is held by {stations_held[person.station]}: "
                "his words are his holder's own, and nobody speaks as a held station"
            )
        if person is not None and person.name in held:
            station, who = held[person.name]
            return (
                f"{person.name} is the {station}'s, held by {who}: his words are his holder's "
                "own, and nobody speaks as a held station"
            )
        return None
    m = _MOVE.match(order.text)
    if m is None:
        return None
    name = " ".join(str(m.group("name") or m.group("bare") or "").split()).strip('"')
    person = world.people.find(name)
    if person is not None and person.name in held:
        station, who = held[person.name]
        return (
            f"{person.name} is the {station}'s, held by {who}: nobody moves or binds a person "
            "a model or the player holds"
        )
    if m.group("station"):
        key = _station_key(m.group("station"))
        if key in stations_held:
            return (
                f"the {key}'s station is held by {stations_held[key]}: nobody binds another "
                "person to a station a model or the player holds"
            )
    return None


# ---------------------------------------------------------------------------
# aboard (spec M7b §3; package 50): a thing found aboard, from the table
# ---------------------------------------------------------------------------

ABOARD_PATH = Path(__file__).resolve().parents[2] / "data" / "director" / "aboard.yaml"
# A spar found sprung keeps this much of its condition when the table gives no figure.
SPRUNG_CONDITION = 30.0
# The watch the strain is looked back over for a spar found sprung (`strained`).
STRAINED_LOOKBACK_S = 4 * 3600
# The mean wind, in knots, above which a spar may spring without a strain line of its own.
STRAINED_WIND_KN = 20.0


@functools.lru_cache(maxsize=1)
def aboard_table(path: str = str(ABOARD_PATH)) -> list[dict[str, Any]]:
    """The things that may be found aboard (`data/director/aboard.yaml`), as the file has
    them."""
    import yaml

    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    out = []
    for d in raw.get("things") or []:
        if not isinstance(d, dict) or not d.get("id") or not d.get("words"):
            raise ValueError(f"{path}: each thing wants an id and its words.")
        # a key the game does not know is the table's mistake, said at the load rather than
        # passed over in play
        for field_name, known in (
            ("effect", ABOARD_EFFECT_KEYS),
            ("plausible_when", ABOARD_PLAUSIBLE_KEYS),
        ):
            unknown = sorted(set(d.get(field_name) or {}) - known)
            if unknown:
                raise ValueError(
                    f"{path}: {d['id']}: {field_name} has no key {', '.join(unknown)}; "
                    f"the keys are {', '.join(sorted(known))}."
                )
        slots = {m.group(1) for form in d["words"] for m in _SLOT.finditer(str(form))}
        if len(slots) > 1 or any(len(_SLOT.findall(str(form))) > 1 for form in d["words"]):
            raise ValueError(f"{path}: {d['id']}: a thing names one slot in its words, once.")
        for key in d.get("effect") or {}:
            want = ABOARD_EFFECT_SLOTS.get(key)
            if want is not None and (
                slots != {want} or not all(f"{{{want}}}" in str(form) for form in d["words"])
            ):
                raise ValueError(
                    f"{path}: {d['id']}: the effect {key} wants every form to name the "
                    f"{{{want}}} it falls on."
                )
        out.append(dict(d))
    return out


def _key(words: str) -> str:
    return " ".join(str(words).lower().split()).removeprefix("the ").strip()


def _part_by_name(ship: Any, words: str, of: str) -> str | None:
    """A part of the ship by her own name for it, among her `of` (`spars`, `sails`,
    `lines`): 'the fore topmast', 'the fore topsail', 'the starboard main brace'; a line
    or a sail by its name without the side ('the main brace') where the full name finds
    none, the first of the pair. None when nothing of hers is called so."""
    from freesail.orders.resolve import display_name, family_name

    key = _key(words)
    ids = list(getattr(ship, of, None) or ())
    for pid in ids:
        if _key(display_name(ship, pid)) == key:
            return pid
    for pid in ids:
        if _key(family_name(ship, pid)) == key:
            return pid
    return None


def _spar_by_name(ship: Any, words: str) -> str | None:
    """A spar of the ship by her own name for it ('the fore topmast'), or None."""
    return _part_by_name(ship, words, "spars")


def _anchor_by_name(ship: Any, words: str) -> str | None:
    """An anchor of the ship by its name ('the best bower', 'the small bower'), or None."""
    from freesail.ship.parts import ground_tackle

    tackle = ground_tackle(ship) if ship is not None else None
    key = _key(words)
    for a in getattr(tackle, "anchors", None) or ():
        if _key(a.name) in (key, f"{key} anchor") or _key(a.name).removesuffix(" anchor") == key:
            return a.id
    return None


def _good_by_name(world: Any, words: str) -> str | None:
    """A good in the hold by its name ('tin', 'the brandy'), or None."""
    hold = getattr(world, "hold", None)
    key = _key(words)
    for good, tons in (getattr(hold, "goods", None) or {}).items():
        if tons > 1e-9 and _key(good) == key:
            return good
    return None


# The table's slots for a part of the ship or a thing of hers, each named by her own name
# for it in the words ('the {spar} is found sprung': 'the fore topmast is found sprung'),
# and how it is found from the words.
SLOTS: dict[str, Any] = {
    "spar": lambda world, words: _part_by_name(getattr(world, "ship", None), words, "spars"),
    "sail": lambda world, words: _part_by_name(getattr(world, "ship", None), words, "sails"),
    "line": lambda world, words: _part_by_name(getattr(world, "ship", None), words, "lines"),
    "anchor": lambda world, words: _anchor_by_name(getattr(world, "ship", None), words),
    "good": _good_by_name,
}
_SLOT = re.compile(r"\{(" + "|".join(SLOTS) + r")\}")


def _slot_of(thing: dict[str, Any]) -> str | None:
    """The slot the table's thing names in its words (`spar`, `sail`, ...), or None."""
    for form in thing.get("words") or ():
        m = _SLOT.search(str(form))
        if m is not None:
            return m.group(1)
    return None


def _target_words(world: Any, thing: dict[str, Any], target: str | None) -> str:
    """The target in the report's words: 'the fore topmast', 'the best bower', 'tin'."""
    from freesail.orders.resolve import display_name

    if target is None:
        return ""
    slot = _slot_of(thing)
    ship = getattr(world, "ship", None)
    if slot in ("spar", "sail", "line"):
        return f"the {display_name(ship, target)}"
    if slot == "anchor":
        from freesail.ship.parts import ground_tackle

        tackle = ground_tackle(ship)
        a = next((a for a in tackle.anchors if a.id == target), None) if tackle else None
        return a.name if a is not None else target
    return str(target)


def _fill(words: str, thing: dict[str, Any], name: str) -> str:
    """The table's words with its slot filled by the target's name."""
    return _SLOT.sub(name, str(words))


def _form_words(thing: dict[str, Any]) -> str:
    """The thing's first form for the channel's answer, its slot as '<spar>' and so on."""
    return _SLOT.sub(lambda m: f"the <{m.group(1)}>", str(thing["words"][0]))


def _aboard_match(world: Any, body: str) -> tuple[dict[str, Any], str | None] | None:
    """The table's thing the words name and, for one with a slot, the target the slot
    names (a spar's, a sail's or a line's id, an anchor's id, a good's name): None when no
    thing's words fit."""
    said = " ".join(re.sub(r"^aboard\s*:", "", body, flags=re.I).split()).lower().rstrip(".")
    for thing in aboard_table():
        for form in thing["words"]:
            form = " ".join(str(form).lower().split())
            m = _SLOT.search(form)
            if m is None:
                if said == form:
                    return thing, None
                continue
            head, tail = form[: m.start()].strip(), form[m.end() :].strip()
            if not (said.startswith(head) and said.endswith(tail)):
                continue
            inner = said[len(head) : len(said) - len(tail)].strip()
            if not inner:
                continue
            target = SLOTS[m.group(1)](world, inner)
            if target is not None:
                return thing, target
    return None


# ---------------------------------------------------------------------------
# aboard (spec M7b §17a; package 53b): a thing made or moved, and the transactions
# ---------------------------------------------------------------------------

# A sum paid into the purse by someone, or from it to someone; a cargo freighted; a debt
# owed to someone or by someone. Each changes the purse or the hold by a transaction with
# its cause in the ledger, never a figure set (the owner's question and the lead's answer
# of 2026-10-19).
_PAID_IN = re.compile(
    r"^(?P<sum>.+?)\s+paid\s+(?:into|in\s+to|to)\s+the\s+purse(?:\s+by\s+(?P<who>.+?))?"
    r"(?:\s+for\s+(?P<for>.+))?$",
    re.I,
)
_PAID_OUT = re.compile(
    r"^(?P<sum>.+?)\s+paid\s+(?:from|out\s+of)\s+the\s+purse(?:\s+to\s+(?P<who>.+?))?"
    r"(?:\s+for\s+(?P<for>.+))?$",
    re.I,
)
_FREIGHT = re.compile(
    r"^(?P<tons>.+?)\s+tons?\s+of\s+(?P<good>.+?)\s+freighted(?:\s+by\s+(?P<who>.+?))?"
    r"(?:\s+at\s+(?P<at>.+?))?(?:\s+for\s+(?P<dest>.+))?$",
    re.I,
)
_DEBT = re.compile(
    r"^a\s+debt\s+of\s+(?P<sum>.+?)\s+owed\s+(?P<dir>to|by)\s+(?P<who>.+?)"
    r"(?:\s+for\s+(?P<for>.+))?$",
    re.I,
)
# The money's units in pounds (a guinea twenty-one shillings; a crown five shillings).
MONEY_UNITS: dict[str, float] = {
    "pound": 1.0,
    "pounds": 1.0,
    "guinea": 1.05,
    "guineas": 1.05,
    "crown": 0.25,
    "crowns": 0.25,
    "shilling": 0.05,
    "shillings": 0.05,
    "penny": 1.0 / 240.0,
    "pence": 1.0 / 240.0,
}
# A sum in the clerk's figures: '£30', '£6 10s', '£6 10s 6d'.
_STERLING = re.compile(
    r"^£\s*(?P<l>\d+(?:\.\d+)?)(?:\s+(?P<s>\d+)\s*s\.?)?(?:\s+(?P<d>\d+)\s*d\.?)?"
)
# The forms the channel's thing and transaction orders take, for its answer in words.
ABOARD_FORMS = (
    "a thing made or moved ('aboard: a sealed packet, on the cabin table'; 'aboard: a cask "
    "of brandy, in the hold'; 'aboard: the packet, in the keeping of Mr Veale'), a sum "
    "('aboard: twenty guineas paid into the purse by Mr Veale'; 'aboard: £6 paid from the "
    "purse to the pilot'), a freight ('aboard: ten tons of wool freighted by Mr Veale at the "
    "quay for Falmouth') or a debt ('aboard: a debt of £30 owed to the chandler at Plymouth')"
)


def read_sum(words: str) -> float | None:
    """A sum of money in pounds from the words ('twenty guineas', '£30', '£6 10s', 'thirty
    pounds ten shillings', 'a guinea'), or None when the words are no sum."""
    from freesail.orders.numbers import read

    text = " ".join(str(words).lower().replace(",", " ").split())
    total = 0.0
    said = False
    m = _STERLING.match(text)
    if m is not None:
        shillings, pence = int(m.group("s") or 0), int(m.group("d") or 0)
        total += float(m.group("l")) + shillings / 20.0 + pence / 240.0
        text, said = text[m.end() :].strip(), True
    tokens = [t for t in text.replace("-", " ").split() if t not in ("and", "sterling")]
    i = 0
    while i < len(tokens):
        got = read(tokens, i)
        if got is None or i + got[1] >= len(tokens):
            return None
        unit = MONEY_UNITS.get(tokens[i + got[1]])
        if unit is None:
            return None
        total += got[0] * unit
        i += got[1] + 1
        said = True
    return round(total, 4) if said and total > 0 else None


def _party(world: Any, words: str) -> tuple[Any, str]:
    """(the person the words name, or None; the party in words: his name, else the words
    as said)."""
    words = " ".join(str(words or "").split()).strip(" .")
    people = getattr(world, "people", None)
    p = people.find(words) if (people is not None and words) else None
    return p, (p.name if p is not None else words)


def _transaction(body: str) -> tuple[str, re.Match[str]] | None:
    """(the kind, the match) of a transaction's words, or None."""
    said = " ".join(re.sub(r"^aboard\s*:", "", body, flags=re.I).split()).rstrip(".")
    for kind, rx in (
        ("received", _PAID_IN),
        ("paid", _PAID_OUT),
        ("freight", _FREIGHT),
        ("debt", _DEBT),
    ):
        m = rx.match(said)
        if m is not None:
            return kind, m
    return None


def _thing_words(body: str) -> str:
    return " ".join(re.sub(r"^aboard\s*:", "", body, flags=re.I).split()).rstrip(".")


def _aboard_thing(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`aboard: <a thing>, <where>[, <more of it>]`: a thing made, or a thing known moved
    (spec M7b §17a): never a line of the play log, which carries the thing where it is met
    (the people's reading, the places', the truth)."""
    from freesail.world import things as TH

    try:
        thing, where, moved = TH.make(world, _thing_words(body))
    except TH.ThingWordsError as e:
        raise WorldOrderError(str(e)) from None
    was = TH.where_words(world, thing, keeper_where=False) if moved else ""
    TH.put(thing, where)
    if not moved:
        TH.things_of(world).append(thing)
    now = TH.where_words(world, thing, keeper_where=False)
    data: dict[str, Any] = {"thing": thing.id, "name": thing.name, **thing.to_dict()}
    if moved:
        data["moved"] = True
        return f"{thing.the} moved: it was {was}, and is {now}", data
    desc = f" ({thing.description})" if thing.description else ""
    return f"{thing.name}{desc} made, {now}", data


def _aboard_transaction(world: Any, kind: str, m: re.Match[str]) -> tuple[str, dict[str, Any]]:
    """A transaction of the purse or the hold (spec M7b §17a): written in its own ledger
    with its cause, a notable line of the play log saying it as the purser's books do (the
    effect, never the order), the director's log keeping the act."""
    from freesail.world.places import pounds_words

    purse = getattr(world, "purse", None)
    now = world.clock.tick
    if kind == "freight":
        return _freight(world, m)
    pounds = read_sum(m.group("sum"))
    said = " ".join(m.group("sum").split())
    if pounds is None:
        raise WorldOrderError(
            f"'{said}' is no sum the purse reads: say '£30', '£6 10s', 'twenty guineas', "
            "'thirty pounds'"
        )
    if purse is None:
        raise WorldOrderError("she keeps no purse")
    who, party = _party(world, m.group("who") or "")
    why = f" for {m.group('for').strip()}" if m.groupdict().get("for") else ""
    sum_words = said if said.startswith("£") else f"{said} ({pounds_words(pounds)})"
    data: dict[str, Any] = {"kind": kind, "pounds": round(pounds, 2), "party": party}
    if kind == "received":
        if not party:
            raise WorldOrderError(
                "say who paid it: 'aboard: twenty guineas paid into the purse by Mr Veale'"
            )
        line = purse.receive(pounds, party, f"{sum_words}{why}", now)
        text = f"Paid into the purse by {party}, {sum_words}{why}; the purse {purse.words()}."
        world.record(Severity.NOTABLE, "purse.received", text, data=data | {"ledger": line})
        return f"{sum_words} paid into the purse by {party}; the purse {purse.words()}", data
    if kind == "paid":
        if not party:
            raise WorldOrderError(
                "say to whom it is paid: 'aboard: £6 paid from the purse to the pilot'"
            )
        if pounds > purse.pounds + 1e-9:
            raise WorldOrderError(
                f"the purse holds {purse.words()}, not {pounds_words(pounds)}: nothing is paid "
                "below nothing"
            )
        line = purse.pay_to(pounds, party, f"{sum_words}{why}", now)
        text = f"Paid from the purse to {party}, {sum_words}{why}; the purse {purse.words()}."
        world.record(Severity.NOTABLE, "purse.paid", text, data=data | {"ledger": line})
        return f"{sum_words} paid from the purse to {party}; the purse {purse.words()}", data
    to_us = m.group("dir").lower() == "by"
    line = purse.owe(pounds, party, f"{sum_words}{why}", now, to_us=to_us)
    text = f"{line[:1].upper()}{line[1:]}, entered in the purser's books."
    world.record(Severity.NOTABLE, "purse.owed", text, data=data | {"to_us": to_us})
    return line, data | {"to_us": to_us}


def _freight(world: Any, m: re.Match[str]) -> tuple[str, dict[str, Any]]:
    """`aboard: ten tons of wool freighted by Mr Veale at the quay for Falmouth`: the
    market's own form at no price (spec M7b §17a): the freight entered in the hold's ledger
    and the manifest with its cause, the goods off by the port's lighter where she lies in
    port, struck down at once where the freighter is aboard; refused in words where the hold
    has no room (the hold's tons are the game's, and no reason stows more)."""
    from freesail.orders.numbers import read_all
    from freesail.world.ports import BOAT_ASHORE_S, BOAT_PACE_KN, LIGHTER_S_PER_TON, Job

    tons = read_all(" ".join(m.group("tons").lower().replace("-", " ").split()))
    if tons is None or tons <= 0:
        raise WorldOrderError(f"'{m.group('tons')}' is no number of tons")
    good = " ".join(m.group("good").lower().split())
    hold = getattr(world, "hold", None)
    if hold is None or hold.capacity_tons <= 0:
        raise WorldOrderError("she has no hold for a cargo")
    ports = getattr(world, "ports", None)
    coming = _tons_coming(ports)
    room = max(0.0, hold.room_tons - coming)
    if tons > room + 1e-9:
        bought = f" ({coming:g} tons bought are coming off)" if coming > 0 else ""
        raise WorldOrderError(
            f"there is room in the hold for {room:g} tons and no more{bought}; {tons:g} tons "
            f"of {good} will not stow"
        )
    who, party = _party(world, m.group("who") or "")
    port = ports.in_port() if (ports is not None and ports.ports) else None
    at = " ".join((m.group("at") or "").split())
    dest = " ".join((m.group("dest") or "").split())
    words = f"{tons:g} tons of {good} freighted" + (f" by {party}" if party else "")
    if port is not None:
        words += f" at {port.name}"
    elif at:
        words += f" at {at}"
    if dest:
        words += f" for {dest}"
    now = world.clock.tick
    hold.freight(tons, good, words, now)
    papers = getattr(world, "papers", None)
    if papers is not None:
        world.record(
            Severity.ROUTINE,
            "paper.written",
            papers.write("the manifest", words),
            data={"paper": "the manifest"},
        )
    data: dict[str, Any] = {"kind": "freight", "tons": tons, "good": good, "party": party}
    if port is not None and (who is None or not who.aboard):
        pull_s = ports.to_shore_m(port) / (BOAT_PACE_KN * units.KNOT)
        due = now + int(BOAT_ASHORE_S["purchase"] + tons * LIGHTER_S_PER_TON + pull_s)
        ports.jobs.append(
            Job(due, "lighter", port.id, {"items": [{"good": good, "tons": tons, "freight": 1}]})
        )
        text = f"{words[:1].upper()}{words[1:]}; the lighter brings it off."
        data |= {"port": port.id, "due_tick": due}
        said = f"{words}; off by the lighter"
    else:
        hold.stow(good, tons)
        text = (
            f"{words[:1].upper()}{words[1:]}, struck down into the hold; the manifest "
            f"{hold.words()}."
        )
        said = f"{words}; struck down into the hold"
    world.record(Severity.NOTABLE, "hold.freighted", text, data=data)
    return said, data


def _tons_coming(ports: Any) -> float:
    """The tons bought or freighted and not yet in the hold: in the boat on her errand of a
    purchase, or in the port's lighter (the hold's room is the room left after them)."""
    if ports is None:
        return 0.0
    tons = 0.0
    boat = getattr(ports, "boat", None)
    if boat is not None and getattr(boat, "away", False):
        for item in getattr(boat, "carrying", None) or []:
            if item.get("kind") == "purchase":
                tons += float(item.get("tons") or 0.0)
    for job in getattr(ports, "jobs", None) or []:
        if job.kind == "lighter":
            tons += sum(float(i.get("tons") or 0.0) for i in job.payload.get("items") or [])
    return tons


def _aboard_reach(world: Any, body: str) -> str | None:
    """The rule of reach for the `aboard:` channel (package 53b): no thing put into or
    taken out of the keeping of a person a model or the player holds but by his own act,
    and no sum paid, freight sent or debt owed by him but by his own word."""
    from freesail.world import things as TH

    tx = _transaction(body)
    if tx is not None:
        kind, m = tx
        if kind in ("received", "freight") or (kind == "debt" and m.group("dir").lower() == "by"):
            who, _party_words = _party(world, m.group("who") or "")
            held = TH.held_by(world, who)
            if who is not None and held:
                return (
                    f"{who.name} is held by {held}: a sum, a freight or a debt of his is his "
                    "holder's own word, and nobody gives it for him"
                )
        return None
    try:
        thing, where, moved = TH.make(world, _thing_words(body))
    except TH.ThingWordsError:
        return None
    if moved and thing.keeper:
        owner = TH.keeper_of(world, thing)
        held = TH.held_by(world, owner)
        if owner is not None and held:
            return (
                f"{thing.the} is in {owner.name}'s keeping, and he is held by {held}: nothing "
                "is taken out of a held person's keeping but by his own act"
            )
    if where.get("keeper"):
        people = getattr(world, "people", None)
        to = next((p for p in people.all if p.id == where["keeper"]), None) if people else None
        held = TH.held_by(world, to)
        if to is not None and held:
            return (
                f"{to.name} is held by {held}: nothing is put into a held person's keeping but "
                "by his own act; leave it where he can take it ('on the cabin table') and say so"
            )
    return None


def _doubt_aboard_new(world: Any, body: str) -> str | None:
    """The doubt of a transaction (package 53b): a sum from nobody, or from a person the
    world does not know; a payer, a payee or a freighter neither aboard nor at a port she
    lies within a boat's reach of; a sum beyond a port's means by the business's figures; a
    freight with no lighter to bring it (she lies in no port and the freighter is not
    aboard). A thing moved from one port to another, or between the ship and a port beyond
    a boat's reach, by no hand that could carry it. A thing made is never doubted."""
    from freesail.world import things as TH
    from freesail.world.places import pounds_words

    tx = _transaction(body)
    if tx is None:
        try:
            thing, where, moved = TH.make(world, _thing_words(body))
        except TH.ThingWordsError:
            return None
        if not moved:
            return None
        return _doubt_thing_moved(world, thing, where)
    kind, m = tx
    if kind == "debt":
        return None
    who, party = _party(world, m.group("who") or "")
    if kind in ("received", "freight") and not party:
        return "money or goods from nobody: no payer is named, and nothing comes aboard of itself"
    if who is None and party:
        return (
            f"nobody answering to '{party}' is among the people: money or goods from nobody "
            "the world knows ('person: make ...' first, or give a reason)"
        )
    ports = getattr(world, "ports", None)
    port = None
    if who is not None and not who.aboard and who.where != "boat":
        port = ports.ports.get(who.port) if (ports is not None and who.port) else None
        miles = _port_miles(world, port)
        if port is None or miles is None or miles > BOAT_REACH_NM:
            off = f" at {port.name}, {miles:.0f} miles off" if (port and miles is not None) else ""
            return (
                f"{who.name} is {world.people.state_words(who)}{off}: neither aboard nor at a "
                f"port she lies within a boat's reach of ({BOAT_REACH_NM:g} miles), so no hand "
                "carries it"
            )
    if kind == "freight":
        in_port = ports.in_port() if (ports is not None and ports.ports) else None
        if in_port is None and (who is None or not who.aboard):
            return "she lies in no port: no lighter brings a freight off to her at sea"
        return None
    pounds = read_sum(m.group("sum"))
    if pounds is None:
        return None
    if port is None and ports is not None and ports.ports:
        port = ports.in_port()
        if port is None:
            near = ports.nearest()
            port = near[0] if near is not None else None
    from freesail.world.business import port_means_pounds

    means = port_means_pounds(world, port) if port is not None else None
    if means is not None and pounds > means:
        return (
            f"{pounds_words(pounds)} in one sum is beyond {port.name}'s means by the business's "
            f"figures (a full lading of its dearest good, {pounds_words(means)})"
        )
    return None


def _doubt_thing_moved(world: Any, thing: Any, where: dict[str, Any]) -> str | None:
    from freesail.world import things as TH

    here_place, here_port, _ = TH.place_of(world, thing)
    if where.get("keeper"):
        people = getattr(world, "people", None)
        to = next((p for p in people.all if p.id == where["keeper"]), None)
        if to is None:
            return None
        if to.aboard or to.where in ("boat", "cutter"):
            there_place, there_port = "aboard", None
        else:
            there_place, there_port = "shore", to.port
    else:
        there_place, there_port = str(where.get("place") or ""), where.get("port")
    here_ashore = here_place == "shore"
    there_ashore = there_place == "shore"
    if here_ashore and there_ashore and here_port != there_port:
        return (
            f"{thing.the} would go from one port to another in a word, by no hand that carries it"
        )
    if here_ashore != there_ashore:
        ports = getattr(world, "ports", None)
        pid = here_port if here_ashore else there_port
        port = ports.ports.get(pid) if (ports is not None and pid) else None
        miles = _port_miles(world, port)
        if port is not None and miles is not None and miles > BOAT_REACH_NM:
            return (
                f"{thing.the} would cross between the ship and {port.name}, {miles:.0f} miles "
                f"off: no boat carries it so far ({BOAT_REACH_NM:g} miles at the most)"
            )
    return None


def _aboard(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`aboard: <a thing found aboard>`, the table's (package 50); else a transaction of
    the purse or the hold, or a thing made or moved (package 53b); else refused in words
    naming the forms."""
    if _aboard_match(world, body) is None:
        tx = _transaction(body)
        if tx is not None:
            return _aboard_transaction(world, *tx)
        if "," in _thing_words(body):
            return _aboard_thing(world, body)
        forms = "; ".join(_form_words(t) for t in aboard_table())
        raise WorldOrderError(
            f"An aboard order is one of the table's things ({forms}), or {ABOARD_FORMS}."
        )
    return _aboard_found(world, body)


def _aboard_found(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`aboard: <a thing found aboard>`: the thing's effect in the part graph or the
    stores, and its people's report as a notable line of the play log (the order itself
    is for the record only, decision 46). A thing's effect that wants what she lacks (a
    chronometer, a glass, spare canvas) changes nothing and is refused in words."""
    found = _aboard_match(world, body)
    if found is None:
        forms = "; ".join(_form_words(t) for t in aboard_table())
        raise WorldOrderError(f"An aboard order is one of the table's things: {forms}.")
    thing, target = found
    effect = dict(thing.get("effect") or {})
    name = _target_words(world, thing, target)
    for key in effect:
        lacking = _ABOARD_LACKS.get(key)
        why = lacking(world) if lacking is not None else None
        if why:
            # the game has no way to do it as said: nothing changed, and the words say why
            raise WorldOrderError(why)
    data: dict[str, Any] = {"thing": thing["id"]}
    whats = [
        _ABOARD_EFFECTS[key](world, thing, target, name, value, data)
        for key, value in effect.items()
        if key in _ABOARD_EFFECTS
    ]
    if not whats:
        unmodelled = str(thing.get("unmodelled") or "nothing of it is modelled yet")
        whats = [f"{thing['id'].replace('_', ' ')} reported ({unmodelled})"]
        data["report_only"] = True
    report = _fill(str(thing.get("report") or ""), thing, name)
    report = report[:1].upper() + report[1:]
    world.record(Severity.NOTABLE, "aboard.found", report, data=data)
    return f"found aboard: {'; '.join(whats)}", data


# The effects a thing found aboard may have (`data/director/aboard.yaml`, `effect:`), each
# a change to what the ship models, by the table's key: `(world, thing, target, the
# target's name, the table's value, the line's data) -> the change in words`. Several keys
# in one thing are each done, in the table's order. `report_only` (or no key) changes
# nothing and says so.


def _cut_condition(world: Any, target: str, value: Any, data: dict[str, Any], key: str) -> float:
    part = world.ship.parts[target]
    was = float(getattr(part, "condition", 100.0))
    part.condition = min(was, float(value if value is not None else SPRUNG_CONDITION))
    data.update({key: target, "condition": part.condition, "was": was})
    return part.condition


def _fx_spar(world, thing, target, name, value, data) -> str:
    c = _cut_condition(world, target, value or SPRUNG_CONDITION, data, "spar")
    return f"{name} {thing.get('state') or 'sprung'} (its condition {c:g})"


def _fx_part(world, thing, target, name, value, data) -> str:
    c = _cut_condition(world, target, value, data, "part")
    return f"{name} {thing.get('state') or 'worn'} (its condition {c:g})"


def _fx_cable(world, thing, target, name, value, data) -> str:
    from freesail.ship.parts import ground_tackle

    anchor = next(a for a in ground_tackle(world.ship).anchors if a.id == target)
    was = float(anchor.cable_condition)
    anchor.cable_condition = min(was, float(value))
    data.update({"anchor": target, "cable_condition": anchor.cable_condition, "was": was})
    return f"{name}'s cable chafed (its condition {anchor.cable_condition:g})"


def _fx_water_tons(world, thing, target, name, value, data) -> str:
    stores = getattr(world, "stores", None)
    lost = float(value)
    if stores is not None:
        taken = min(lost, max(0.0, float(stores.water_tons)))
        stores.water_tons = max(0.0, float(stores.water_tons) - lost)
        data.update({"water_tons_lost": taken, "water_tons": stores.water_tons})
    return f"{lost:g} ton{'' if lost == 1 else 's'} of water lost"


def _fx_water_share(world, thing, target, name, value, data) -> str:
    stores = world.stores
    lost = max(0.0, float(stores.water_tons)) * min(max(float(value), 0.0), 1.0)
    stores.water_tons = max(0.0, float(stores.water_tons) - lost)
    data.update({"water_tons_lost": round(lost, 3), "water_tons": stores.water_tons})
    return f"{lost:.1f} tons of water lost, {float(value):.0%} of what was in the tier"


def _fx_water_foul(world, thing, target, name, value, data) -> str:
    stores = getattr(world, "stores", None)
    if stores is not None:
        stores.foul = True
    data["water_foul"] = True
    return "the water found foul"


def _fx_provisions_share(world, thing, target, name, value, data) -> str:
    stores = world.stores
    lost = max(0.0, float(stores.provisions_days)) * min(max(float(value), 0.0), 1.0)
    stores.provisions_days = max(0.0, float(stores.provisions_days) - lost)
    data.update({"provisions_days_lost": round(lost, 3), "provisions_days": stores.provisions_days})
    return f"{lost:.1f} days of provisions lost, {float(value):.0%} of what was in store"


def _fx_provisions_days(world, thing, target, name, value, data) -> str:
    stores = world.stores
    lost = min(float(value), max(0.0, float(stores.provisions_days)))
    stores.provisions_days = max(0.0, float(stores.provisions_days) - lost)
    data.update({"provisions_days_lost": round(lost, 3), "provisions_days": stores.provisions_days})
    return f"{lost:.1f} days of provisions lost"


def _fx_cargo(world, thing, target, name, value, data, share: bool = False) -> str:
    from freesail.world.places import _tons

    hold = world.hold
    have = hold.goods.get(target, 0.0)
    tons = have * min(max(float(value), 0.0), 1.0) if share else float(value)
    cause = str(thing.get("cause") or "found spoiled")
    tons = min(tons, have)
    words = f"{_tons(tons)} of {target} struck off the manifest, {cause}"
    lost = hold.lose(target, tons, words, world.clock.tick)
    data.update({"good": target, "tons_lost": round(lost, 3), "tons": hold.goods.get(target, 0.0)})
    return f"{_tons(lost)} of {target} struck off, {cause}"


def _fx_cargo_share(world, thing, target, name, value, data) -> str:
    return _fx_cargo(world, thing, target, name, value, data, share=True)


def _fx_spare_sails(world, thing, target, name, value, data) -> str:
    from freesail.ship.parts import sail_room

    room = sail_room(world.ship)
    bar = float(value)
    hit = 0
    for spare in room.sails:
        if spare.condition > bar:
            spare.condition = bar
            hit += 1
    data.update({"spare_sails_worn": hit, "spare_sails_condition": bar})
    return f"{hit} spare sail{'' if hit == 1 else 's'} in the sail room worn to {bar:g}"


def _fx_cordage_share(world, thing, target, name, value, data) -> str:
    from freesail.ship.parts import cordage

    store = cordage(world.ship)
    lost = max(0.0, float(store.fathoms)) * min(max(float(value), 0.0), 1.0)
    store.take(lost)
    data.update({"cordage_fathoms_lost": round(lost, 1), "cordage_fathoms": store.fathoms})
    return f"{lost:.0f} fathoms of spare cordage lost"


def _fx_chronometer(world, thing, target, name, value, data) -> str:
    c = world.navigation.chronometer
    c.going = False
    c.stopped = str(value) if isinstance(value, str) else "stopped of itself in its box"
    data.update({"chronometer_stopped": True})
    return f"{c.name} stopped"


def _fx_glass(world, thing, target, name, value, data) -> str:
    world.glass = None
    world.ship.extra["glass_broken"] = True
    data["glass_broken"] = True
    return "the glass broken"


def _fx_leak_stopped(world, thing, target, name, value, data) -> str:
    # the grounding's leak (`world.ground`) stopped: the well gains no more, aground or not
    extra = world.ship.extra
    was = float(extra.get("leak_m_per_h", 0.0) or 0.0)
    extra["leak_m_per_h"] = 0.0
    data.update({"leak_stopped": True, "leak_m_per_h_was": round(was, 3)})
    return "the leak stopped"


def _fx_well_pumped(world, thing, target, name, value, data) -> str:
    hull = world.ship.hull
    was = float(hull.water_in_well_m)
    hull.water_in_well_m = 0.0
    ground = getattr(world, "ground", None)
    if ground is not None:
        # the carpenter's reports count the feet afresh from a dry well
        ground._feet_said = 0
        ground._waterlogged_said = False
    data.update({"well_pumped": True, "well_m_was": round(was, 2)})
    return f"the well pumped dry ({was:.2f} m of water pumped out)"


_ABOARD_EFFECTS: dict[str, Any] = {
    "spar_condition": _fx_spar,
    "sail_condition": _fx_part,
    "line_condition": _fx_part,
    "cable_condition": _fx_cable,
    "water_tons": _fx_water_tons,
    "water_share": _fx_water_share,
    "water_foul": _fx_water_foul,
    "provisions_share": _fx_provisions_share,
    "provisions_days": _fx_provisions_days,
    "cargo_tons": _fx_cargo,
    "cargo_share": _fx_cargo_share,
    "spare_sails_condition": _fx_spare_sails,
    "cordage_share": _fx_cordage_share,
    "chronometer_stopped": _fx_chronometer,
    "glass_broken": _fx_glass,
    "leak_stopped": _fx_leak_stopped,
    "well_pumped": _fx_well_pumped,
}


def _lacks_stores(world: Any) -> str | None:
    return None if getattr(world, "stores", None) is not None else "she keeps no stores"


def _lacks_chronometer(world: Any) -> str | None:
    nav = getattr(world, "navigation", None)
    c = getattr(nav, "chronometer", None)
    if c is None:
        return "she carries no chronometer"
    if not c.going:
        return f"{c.name} is stopped already"
    return None


def _lacks_glass(world: Any) -> str | None:
    if getattr(world, "glass", None) is not None:
        return None
    extra = getattr(getattr(world, "ship", None), "extra", None) or {}
    return "the glass is broken already" if extra.get("glass_broken") else "she carries no glass"


def _lacks_sail_room(world: Any) -> str | None:
    from freesail.ship.parts import sail_room

    return None if len(sail_room(world.ship)) else "there is no spare canvas in the sail room"


def _lacks_cordage(world: Any) -> str | None:
    from freesail.ship.parts import cordage

    return None if cordage(world.ship).fathoms > 0 else "there is no spare cordage in the store"


def _lacks_hull(world: Any) -> str | None:
    return None if getattr(world.ship, "hull", None) is not None else "she has no hull modelled"


# What a thing's effect wants of the ship before it is done (else the game has no way to
# do it as said, and nothing changes): by the effect's key, the reason she lacks it or None.
_ABOARD_LACKS: dict[str, Any] = {
    "water_share": _lacks_stores,
    "provisions_share": _lacks_stores,
    "provisions_days": _lacks_stores,
    "spare_sails_condition": _lacks_sail_room,
    "cordage_share": _lacks_cordage,
    "chronometer_stopped": _lacks_chronometer,
    "glass_broken": _lacks_glass,
    "well_pumped": _lacks_hull,
}
# The keys the table's things may use: the effects and `report_only`.
ABOARD_EFFECT_KEYS = frozenset(_ABOARD_EFFECTS) | {"report_only"}
# The effects that fall on the target a slot names, by the slot every form must name.
ABOARD_EFFECT_SLOTS: dict[str, str] = {
    "spar_condition": "spar",
    "sail_condition": "sail",
    "line_condition": "line",
    "cable_condition": "anchor",
    "cargo_tons": "good",
    "cargo_share": "good",
}
# The keys the table's `plausible_when` may use (`_doubt_aboard`).
ABOARD_PLAUSIBLE_KEYS = frozenset(
    {
        "strained",
        "sea_above",
        "days_out",
        "days_since_watered",
        "wind_above",
        "at_anchor",
        "leaking",
        "well_above",
    }
)


# ---------------------------------------------------------------------------
# The feasibility check (spec M7b §3; decision 50): doubted, not refused
# ---------------------------------------------------------------------------

# The sentence the director is answered with after the doubt's reason (the owner's words,
# decision 50).
REENTER_WORDS = (
    "If you think the action you requested is still reasonable, you may enter it again "
    "along with a [reason: ...], and it will be logged and performed."
)
# A cutter with a letter is sent from a port within this of the ship; sent from farther, a
# port could not know where to find her (judgement: a day's sail for a cutter).
LETTER_REACH_NM = 60.0
# A price changed by more than this share of its standing is a market out of its ordinary.
PRICE_SWING = 0.3
# A low appended with its centre within this of the ship, deep, is a gale out of a steady
# glass: the glass would have been falling for a day before such a centre came so near.
LOW_NEAR_KM = 300.0
# ...and "deep" is an anomaly below this many hPa under the month's background.
LOW_DEEP_HPA = 12.0
# The visibility, in miles, at or above which the weather is clear for the horizon's doubt.
CLEAR_NM = 10.0
# A sail's height for the horizon a new ship is doubted inside (a brig's trucks, metres).
SAIL_HEIGHT_M = 30.0


def doubt(world: Any, order: WorldOrder) -> str | None:
    """Why the order is one the simulation could not have produced on its own from where
    it is, in words, or None when it is a plausible cause. Never a refusal: the channel
    says the reason and the director decides (decision 50). The checks, by channel:
    `ship:` a new sail inside the player's horizon in clear weather by day, or on the
    land; `mark:` a mark inside the horizon by day; `weather:` a low deeper than the
    season's floor, a near deep low out of a steady glass, a waypoint faster than the
    season's lows move or deeper than its floor; `message: by a cutter from <port>` beyond
    the letter's reach; `port: price of` beyond the market's ordinary swing; `aboard:` a
    thing with no cause (the table's `plausible_when`); `person:` a person moved where no
    boat could carry him (package 52); `ship "X": order ...` (the hand, package 62) an
    anchor let go too deep for her cables, plain sail in a gale, a chase by a merchantman,
    a fisherman or a packet. The rest (`ship "X": intent`, a person made or named,
    `say as`, `captain:`, `seat:`, `unseat:`, a letter left at a port, a port closed or
    opened) are never doubted: a mind changed, a person's errand, a man's words and the
    owner's grant want no cause of the sea's."""
    body = order.text
    try:
        if order.channel == "ship":
            return _doubt_ship(world, body)
        if order.channel == "mark":
            return _doubt_mark(world, body)
        if order.channel == "weather":
            return _doubt_weather(world, body)
        if order.channel == "message":
            return _doubt_message(world, body)
        if order.channel == "port":
            return _doubt_port(world, body)
        if order.channel == "aboard":
            if _aboard_match(world, body) is None:
                return _doubt_aboard_new(world, body)  # a thing or a transaction (53b)
            return _doubt_aboard(world, body)
        if order.channel == "person":
            return _doubt_person(world, body)
    except WorldOrderError:
        return None  # a malformed order is the channel's own refusal, not a doubt
    return None


def _horizon(world: Any) -> tuple[float | None, bool]:
    """(the lookout's reach in miles now, whether it is clear daylight): the horizon the
    masthead gives a sail, cut to the visibility; None without a chart or a position."""
    lookout = getattr(world, "lookout", None)
    pos = getattr(world, "position", None)
    if lookout is None or pos is None:
        return None, False
    from freesail.world.chart import NIGHT_LAND_NM
    from freesail.world.geo import horizon_nm

    day = str(getattr(world, "daylight", "")) == "day"
    conditions = getattr(world, "conditions", None)
    vis = conditions.visibility_nm if conditions is not None else math.inf
    reach = min(vis, horizon_nm(lookout.height_of_eye_m, SAIL_HEIGHT_M))
    if not day:
        reach = min(reach, NIGHT_LAND_NM)
    return reach, day and vis >= CLEAR_NM


def _doubt_ship(world: Any, body: str) -> str | None:
    from freesail.world.geo import bearing_and_distance
    from freesail.world.ships import place_position

    g = _SHIP_GOAL.match(body)
    hm = _HAND_TAIL.match(g.group("goal")) if g is not None else None
    if g is not None and hm is not None:
        return _doubt_hand(world, g.group("name"), hm.group("words"))
    m = _SHIP_NEW.match(body)
    if m is None:
        return None  # a goal or an intent changed: a mind changed wants no cause
    found = place_position(world, m.group("where"))
    if found is None:
        return None
    pos = found[0]
    chart = getattr(world, "chart", None)
    if chart is not None and chart.contains(pos):
        depth = chart.depth_at(pos)
        if depth is not None and depth <= 0.0:
            return (
                f"the place {found[1]} is on the land by the chart: a ship put there would be "
                "aground, and no ship sails from dry land"
            )
    reach, clear = _horizon(world)
    here = getattr(world, "position", None)
    if reach is None or here is None or not clear:
        return None
    nm = bearing_and_distance(here, pos)[1] / units.NAUTICAL_MILE
    if nm <= reach:
        return (
            f"a sail put on the sea {nm:.1f} miles off is inside the lookout's horizon "
            f"({reach:.0f} miles in this visibility, by day): she would have been seen coming "
            "up over it, and appears from nothing"
        )
    return None


# The hand's doubt (package 62; the lead's reading: a captain's order is always a plausible
# cause, so the doubt bites only where the order itself is implausible for her). An anchor
# let go deeper than this many fathoms by the chart (judgement: a bower's cable of a hundred
# to a hundred and twenty fathoms wants a scope of three or four, and the period's roads lie
# in five to twenty; beyond thirty no master lets go); plain sail made in a wind at her over
# this many knots (force 8, a gale, the top of force 7 being 33); a chase given by a master
# whose doctrine is these roles', who runs from a stranger or keeps his course.
HAND_ANCHOR_FATHOMS = 30.0
HAND_GALE_KN = 34.0
HAND_PEACEFUL_ROLES = ("merchant", "fisherman", "packet")
_HAND_ANCHOR = re.compile(
    r"^(?:come to (?:an |the )?anchor|let go the (?:best |small |sheet )?(?:bower|anchor)|anchor)"
    r"\b",
    re.I,
)
_HAND_SAIL = re.compile(
    r"^(?:make (?:all )?sail|set (?:all )?(?:plain )?sail|set all plain sail|set the "
    r"(?:royals|topgallants|topgallant sails|studdingsails))\b",
    re.I,
)
_HAND_CHASE = re.compile(r"^(?:give chase|chase\b|stand after)", re.I)


def _doubt_hand(world: Any, name: str, words: str) -> str | None:
    """Why the order given through her captain is implausible for her, or None (package
    62): an anchor let go too deep for her cables, plain sail in a gale, a chase by a
    merchantman, a fisherman or a packet. A captain's order is a plausible cause, so the
    rest are never doubted."""
    vessel = world.vessels.find(name)
    if vessel is None or vessel.done:
        return None
    low = " ".join(str(words).lower().split()).rstrip(".")
    if _HAND_ANCHOR.match(low):
        chart = getattr(world, "chart", None)
        depth = None
        if chart is not None and chart.contains(vessel.position):
            depth = chart.depth_at(vessel.position)
        fathoms = None if depth is None else float(depth) / units.FATHOM
        if fathoms is not None and fathoms > HAND_ANCHOR_FATHOMS:
            return (
                f"{vessel.name} lies in {fathoms:.0f} fathoms by the chart, deeper than any "
                f"scope of her cables would hold in (no master lets go beyond "
                f"{HAND_ANCHOR_FATHOMS:.0f})"
            )
        return None
    if _HAND_SAIL.match(low):
        kn = units.ms_to_knots(float(vessel._wind_at(world)[1]))
        if kn > HAND_GALE_KN:
            return (
                f"the wind at {vessel.name} is {kn:.0f} knots, a gale: no master makes plain "
                "sail in it"
            )
        return None
    if _HAND_CHASE.match(low):
        crew = getattr(vessel, "crew", None)
        if crew is not None and crew.shape == "full":
            role = str(getattr(crew.captain, "role", "") or "")
        else:
            role = str(getattr(vessel.brain, "role", "") or "")
        if role in HAND_PEACEFUL_ROLES:
            return (
                f"{vessel.name}'s master sails by the {role}'s doctrine: he runs from a "
                "stranger or keeps his course, and gives chase to nobody"
            )
    return None


def _doubt_mark(world: Any, body: str) -> str | None:
    from freesail.world.geo import bearing_and_distance
    from freesail.world.ships import place_position

    m = _MARK.match(body)
    if m is None:
        return None
    found = place_position(world, m.group("where"))
    reach, clear = _horizon(world)
    here = getattr(world, "position", None)
    if found is None or reach is None or here is None or not clear:
        return None
    nm = bearing_and_distance(here, found[0])[1] / units.NAUTICAL_MILE
    if nm <= reach:
        return (
            f"a mark put {nm:.1f} miles off is inside the lookout's horizon ({reach:.0f} "
            "miles in this visibility, by day): it would have been in sight already"
        )
    return None


def _month_table(world: Any) -> Any:
    """The climatology's table for the month and the box she is in (the Channel's where
    the world keeps none), for the season's bounds."""
    from freesail.world.weather import load_climatology

    systems = getattr(world, "systems", None)
    try:
        if systems is not None and getattr(systems, "climatology", None) is not None:
            return systems._table(world.clock.ship_time)
        clim = load_climatology()
        origin = getattr(world, "origin", None)
        box = (
            clim.box_at(origin.lat_deg, origin.lon_deg) if origin is not None else clim.default_box
        )
        return box.month(world.clock.ship_time.month)
    except Exception:  # noqa: BLE001  (no table: no bound to doubt by)
        return None


def _glass_steady(world: Any) -> bool:
    """Whether the glass has not been falling: no glass, no tendency yet, or its words
    steady or rising."""
    glass = getattr(world, "glass", None)
    tendency = glass.tendency() if glass is not None else None
    if not tendency:
        return True
    words = str(tendency.get("words", "")).lower()
    return not words.startswith("falling")


def _doubt_weather(world: Any, body: str) -> str | None:
    systems = getattr(world, "systems", None)
    table = _month_table(world)
    m = _SYSTEM.match(body)
    if m is not None and m.group("kind").lower() == "low":
        hpa = float(m.group("hpa"))
        if table is not None and hpa < table.central_hpa[2]:
            return (
                f"a low of {hpa:g} hPa is deeper than the season's floor for these waters "
                f"({table.central_hpa[2]:g} hPa in {table.name})"
            )
        if systems is not None:
            x, y = float(m.group("x")), float(m.group("y"))
            near = math.hypot(x - world.ship_x_km, y - world.ship_y_km)
            background = float(systems.background_hpa)
            if near <= LOW_NEAR_KM and background - hpa >= LOW_DEEP_HPA and _glass_steady(world):
                return (
                    f"a low {background - hpa:.0f} hPa deep put {near:.0f} km from the ship "
                    "out of a steady glass: the glass would have been falling for a day before "
                    "such a centre came so near"
                )
        return None
    m = _WAYPOINT.match(body)
    if m is not None and systems is not None:
        system = systems.find(m.group("name"))
        if system is None or not system.track or table is None:
            return None
        last = system.track[-1]
        at = _time(m.group("at"))
        hours = (at - last.at).total_seconds() / 3600.0
        if hours <= 0:
            return None
        km = math.hypot(float(m.group("x")) - last.x_km, float(m.group("y")) - last.y_km)
        fastest = table.speed_kn[1] * 1.852 * 1.5  # the season's fastest low, with a half over
        if km / hours > fastest:
            return (
                f"the waypoint moves {system.name} at {km / hours:.0f} km an hour, faster than "
                f"the season's lows move ({table.speed_kn[1]:g} knots at the most in {table.name})"
            )
        if system.kind == "low" and float(m.group("hpa")) < table.central_hpa[2]:
            return (
                f"the waypoint deepens {system.name} to {float(m.group('hpa')):g} hPa, below "
                f"the season's floor ({table.central_hpa[2]:g} hPa in {table.name})"
            )
    return None


def _doubt_message(world: Any, body: str) -> str | None:
    from freesail.world.geo import bearing_and_distance

    m = _MESSAGE_BY.match(body)
    ports = getattr(world, "ports", None)
    here = getattr(world, "position", None)
    if m is None or ports is None or here is None:
        return None
    port = ports.find(m.group("port"))
    if port is None:
        return None
    nm = bearing_and_distance(here, port.shore.position)[1] / units.NAUTICAL_MILE
    if nm > LETTER_REACH_NM:
        return (
            f"a cutter sent from {port.name} with a letter for a ship {nm:.0f} miles off: the "
            f"port could not know where to find her beyond {LETTER_REACH_NM:g} miles"
        )
    return None


def _doubt_port(world: Any, body: str) -> str | None:
    m = _PORT.match(body)
    ports = getattr(world, "ports", None)
    if m is None or ports is None or m.group("what").lower() != "price of":
        return None
    port = ports.find(m.group("port").strip('"'))
    pm = re.match(r"^(?P<good>.+?)\s+(?P<pounds>[\d.]+)$", m.group("rest").strip())
    if port is None or pm is None:
        return None
    good = port.market.find(pm.group("good"))
    if good is None or not good.price:
        return None
    swing = abs(float(pm.group("pounds")) - float(good.price)) / float(good.price)
    if swing > PRICE_SWING:
        return (
            f"the price of {good.good} at {port.name} moved by {swing:.0%} in a word, where a "
            f"market moves by a few parts in ten; it stood at £{good.price:g} a ton"
        )
    return None


def _doubt_person(world: Any, body: str) -> str | None:
    """A person moved where no boat could carry him (package 52): coming aboard from a port
    she is beyond a boat's reach of, going ashore with no port within it, leaving the ship
    at a port beyond it. A person made from words, and a word said, are never doubted: a
    supernumerary the story names, and a man's words, want no cause of the sea's."""
    from freesail.world.places import place_words

    m = _MOVE.match(body)
    if m is None:
        return None
    name = " ".join(str(m.group("name") or m.group("bare") or "").split()).strip('"')
    person = world.people.find(name)
    ports = getattr(world, "ports", None)
    if person is None or ports is None or getattr(world, "position", None) is None:
        return None
    move = " ".join(m.group("move").lower().split())
    if move.startswith("comes aboard"):
        if person.aboard:
            return None
        port = ports.ports.get(person.port) if person.port else None
        miles = _port_miles(world, port)
        if port is not None and miles is not None and miles > BOAT_REACH_NM:
            return (
                f"{person.name} is {place_words(person.where)} at {port.name}, and she is "
                f"{miles:.0f} miles from it: no boat brings a man off so far "
                f"({BOAT_REACH_NM:g} miles at the most)"
            )
        return None
    if move.startswith("goes ashore"):
        near = ports.nearest()
        if near is not None and near[1] > BOAT_REACH_NM:
            return (
                f"the nearest port, {near[0].name}, is {near[1]:.0f} miles off: no boat puts a "
                f"man ashore so far ({BOAT_REACH_NM:g} miles at the most)"
            )
        return None
    port = ports.find(m.group("port") or "")
    miles = _port_miles(world, port)
    if port is not None and miles is not None and miles > BOAT_REACH_NM:
        return (
            f"she is {miles:.0f} miles from {port.name}: no boat puts a man ashore there from "
            f"so far ({BOAT_REACH_NM:g} miles at the most)"
        )
    return None


def _doubt_aboard(world: Any, body: str) -> str | None:
    """The doubt of a thing found aboard (the table's `plausible_when`): every condition it
    names must hold, else the thing's own `doubt` words."""
    found = _aboard_match(world, body)
    if found is None:
        return None
    thing, target = found
    when = dict(thing.get("plausible_when") or {})
    why = _fill(
        str(thing.get("doubt") or "the thing has no cause in the ship's state"),
        thing,
        _target_words(world, thing, target),
    )
    for key, value in when.items():
        if not _PLAUSIBLE[key](world, target, value):
            return why
    return None


def _mean_wind_kn(world: Any) -> float | None:
    record = getattr(world, "wind_record", None)
    mean = record.mean_speed() if record is not None else None
    return units.ms_to_knots(mean) if mean is not None else None


def _plausible_strained(world: Any, target: str | None, value: Any) -> bool:
    """A strain line of the part's (or any above the figure) in the last watch, a fresh
    mean wind, or the part above the figure now."""
    bar = float(value)
    since = world.clock.tick - STRAINED_LOOKBACK_S
    for e in reversed(world.log.all()):
        if e.tick < since:
            break
        if e.kind.startswith("strain.") and (
            e.data.get("part") == target or float(e.data.get("ratio", 0.0) or 0.0) >= bar
        ):
            return True
    mean = _mean_wind_kn(world)
    if mean is not None and mean >= STRAINED_WIND_KN:
        return True
    parts = getattr(getattr(world, "ship", None), "parts", None) or {}
    part = parts.get(target) if target is not None else None
    return part is not None and float(getattr(part, "strain_ratio", 0.0)) >= bar


def _plausible_sea_above(world: Any, target: str | None, value: Any) -> bool:
    """The sea beyond the words named: she has been working."""
    sea = getattr(world, "sea", None)
    words = str(getattr(sea, "words", "") or "").lower() if sea is not None else ""
    calm = [str(w).lower() for w in (value or [])]
    return sea is not None and not any(words == c or words.startswith(c) for c in calm)


def _plausible_days_out(world: Any, target: str | None, value: Any) -> bool:
    """So many days of the ship's time since the voyage began."""
    return world.clock.tick / 86400.0 >= float(value)


def _plausible_days_since_watered(world: Any, target: str | None, value: Any) -> bool:
    """So many days since she last took in water (the voyage's start, if she has not)."""
    watered = int(getattr(getattr(world, "stores", None), "watered_tick", 0) or 0)
    return (world.clock.tick - watered) / 86400.0 >= float(value)


def _plausible_wind_above(world: Any, target: str | None, value: Any) -> bool:
    """The mean wind at or above so many knots."""
    mean = _mean_wind_kn(world)
    return mean is not None and mean >= float(value)


def _plausible_at_anchor(world: Any, target: str | None, value: Any) -> bool:
    """She lies at anchor (an anchor down), or with `false` she does not."""
    from freesail.ship.parts import ground_tackle

    tackle = ground_tackle(getattr(world, "ship", None))
    down = any(a.down for a in getattr(tackle, "anchors", None) or ())
    return down == bool(value)


def _plausible_leaking(world: Any, target: str | None, value: Any) -> bool:
    """She is making water from a grounding (`world.ground`'s leak), or with `false` she
    is not."""
    extra = getattr(getattr(world, "ship", None), "extra", None) or {}
    leaking = float(extra.get("leak_m_per_h", 0.0) or 0.0) > 0.0
    return leaking == bool(value)


def _plausible_well_above(world: Any, target: str | None, value: Any) -> bool:
    """More than so many metres of water in the well."""
    hull = getattr(getattr(world, "ship", None), "hull", None)
    return hull is not None and float(hull.water_in_well_m) > float(value)


_PLAUSIBLE: dict[str, Any] = {
    "strained": _plausible_strained,
    "sea_above": _plausible_sea_above,
    "days_out": _plausible_days_out,
    "days_since_watered": _plausible_days_since_watered,
    "wind_above": _plausible_wind_above,
    "at_anchor": _plausible_at_anchor,
    "leaking": _plausible_leaking,
    "well_above": _plausible_well_above,
}
