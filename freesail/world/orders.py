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
    "recognises",
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
)

# The captain's grammar refuses a world order in these words (truth 71).
REFUSAL = (
    "That is an order to the world, not to the ship: the weather, the other sail, a "
    "message, a port and the people ashore are the scenario's and the director's to "
    "order, journaled at the driver's mark; the captain orders his ship, sends the boat "
    "and reads what the lookout sees."
)

_HEAD = re.compile(
    r"^\s*(weather|ship|message|port|person|captain|mark|seat|unseat|aboard)\b"
    r"\s*(\"[^\"]*\"|[\w-]+)?\s*:",
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
            "captain:, mark:, aboard:, seat: or unseat:."
        )
    return WorldOrder(m.group(1).lower(), text, reason)


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
        return _aboard(world, body)
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


def _person(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    from freesail.world.people import Person
    from freesail.world.places import PLACES

    m = _PERSON.match(body)
    if m is None:
        raise WorldOrderError(
            "A person order is 'person: <role> \"<name>\" aboard in the <place>' or 'person: "
            '<role> "<name>" ashore at <port>\'.'
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
        out.append(dict(d))
    return out


def _spar_by_name(ship: Any, words: str) -> str | None:
    """A spar of the ship by her own name for it ('the fore topmast'), or None."""
    from freesail.orders.resolve import display_name

    key = " ".join(str(words).lower().split()).removeprefix("the ").strip()
    for sid in getattr(ship, "spars", None) or ():
        if display_name(ship, sid).lower().removeprefix("the ").strip() == key:
            return sid
    return None


def _aboard_match(world: Any, body: str) -> tuple[dict[str, Any], str | None] | None:
    """The table's thing the words name and, for a spar's, the spar's id: None when no
    thing's words fit."""
    said = " ".join(re.sub(r"^aboard\s*:", "", body, flags=re.I).split()).lower().rstrip(".")
    ship = getattr(world, "ship", None)
    for thing in aboard_table():
        for form in thing["words"]:
            form = " ".join(str(form).lower().split())
            if "{spar}" not in form:
                if said == form:
                    return thing, None
                continue
            head, _, tail = form.partition("{spar}")
            head, tail = head.strip(), tail.strip()
            if not (said.startswith(head) and said.endswith(tail)):
                continue
            inner = said[len(head) : len(said) - len(tail)].strip()
            if not inner:
                continue
            sid = _spar_by_name(ship, inner)
            if sid is not None:
                return thing, sid
    return None


def _aboard(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`aboard: <a thing found aboard>`: the thing's effect in the part graph or the
    stores, and its people's report as a notable line of the play log (the order itself
    is for the record only, decision 46)."""
    from freesail.orders.resolve import display_name

    found = _aboard_match(world, body)
    if found is None:
        forms = "; ".join(
            str(t["words"][0]).replace("{spar}", "the <spar>") for t in aboard_table()
        )
        raise WorldOrderError(f"An aboard order is one of the table's things: {forms}.")
    thing, sid = found
    ship = world.ship
    effect = dict(thing.get("effect") or {})
    name = f"the {display_name(ship, sid)}" if sid is not None else ""
    data: dict[str, Any] = {"thing": thing["id"]}
    if "spar_condition" in effect:
        spar = ship.parts[sid]
        was = float(getattr(spar, "condition", 100.0))
        spar.condition = min(was, float(effect.get("spar_condition") or SPRUNG_CONDITION))
        data.update({"spar": sid, "condition": spar.condition, "was": was})
        what = f"{name} sprung (its condition {spar.condition:g})"
    elif "water_tons" in effect:
        stores = getattr(world, "stores", None)
        lost = float(effect["water_tons"])
        if stores is not None:
            taken = min(lost, max(0.0, float(stores.water_tons)))
            stores.water_tons = max(0.0, float(stores.water_tons) - lost)
            data.update({"water_tons_lost": taken, "water_tons": stores.water_tons})
        what = f"a cask stove, {lost:g} ton of water lost"
    elif effect.get("water_foul"):
        stores = getattr(world, "stores", None)
        if stores is not None:
            stores.foul = True
        data["water_foul"] = True
        what = "the water found foul"
    else:
        what = f"{thing['id'].replace('_', ' ')} reported (nothing of the hull is modelled yet)"
        data["report_only"] = True
    report = str(thing.get("report") or "").replace("{spar}", name)
    report = report[:1].upper() + report[1:]
    world.record(Severity.NOTABLE, "aboard.found", report, data=data)
    return f"found aboard: {what}", data


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
    thing with no cause (the table's `plausible_when`). The rest (`ship "X": intent`,
    `person:`, `captain:`, `seat:`, `unseat:`, a letter left at a port, a port closed or
    opened) are never doubted: a mind changed, a person's errand and the owner's grant want
    no cause of the sea's."""
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
            return _doubt_aboard(world, body)
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


def _doubt_aboard(world: Any, body: str) -> str | None:
    from freesail.orders.resolve import display_name

    found = _aboard_match(world, body)
    if found is None:
        return None
    thing, sid = found
    when = dict(thing.get("plausible_when") or {})
    ship = world.ship
    name = f"the {display_name(ship, sid)}" if sid is not None else ""
    why = str(thing.get("doubt") or "the thing has no cause in the ship's state").replace(
        "{spar}", name
    )
    if "strained" in when:
        bar = float(when["strained"])
        # a strain line of the spar's in the last watch, or a fresh mean wind
        since = world.clock.tick - STRAINED_LOOKBACK_S
        for e in reversed(world.log.all()):
            if e.tick < since:
                break
            if e.kind.startswith("strain.") and (
                e.data.get("part") == sid or float(e.data.get("ratio", 0.0) or 0.0) >= bar
            ):
                return None
        record = getattr(world, "wind_record", None)
        mean = record.mean_speed() if record is not None else None
        if mean is not None and units.ms_to_knots(mean) >= STRAINED_WIND_KN:
            return None
        spar = ship.parts.get(sid) if sid is not None else None
        if spar is not None and float(getattr(spar, "strain_ratio", 0.0)) >= bar:
            return None
        return why
    if "sea_above" in when:
        sea = getattr(world, "sea", None)
        words = str(getattr(sea, "words", "") or "").lower() if sea is not None else ""
        calm = [str(w).lower() for w in (when["sea_above"] or [])]
        if sea is None or any(words == c or words.startswith(c) for c in calm):
            return why
        return None
    if "days_out" in when:
        days = world.clock.tick / 86400.0
        if days < float(when["days_out"]):
            return why
        return None
    return None
