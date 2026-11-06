"""What a person below is told, and who commands when the captain cannot (package 65,
step 3; the design's §7; decision 63).

**The rules' officer of the watch reports to the captain below.** By the Regulations of
1806 (the Lieutenant, art. IV: "He is to inform the Captain of all strange sails that are
seen ... all shifts of wind, and, in general, of all circumstances which may ... prevent the
Ship's continuing on the course directed") and Luce 1884 ch. XXIII (the officer of the deck
sends for the captain when a sail is sighted at night, the wind shifts or the ship is in
danger). When the captain is in the hull, awake and not on the open deck or aloft, and no
model or player holds a station of the officer of the watch's kind (they have the duty
themselves: the brief says it), each line of a **reportable kind** makes a report a minute
later, the messenger's minute (`people.PASS_THE_WORD_S`): `report.made`, notable, "Mr
Pearce sent down to the captain, in the cabin: a sail sighted, two points on the larboard
bow.", its reach the captain's (`knowledge.REACH`: `person`). A line of `readings.
DANGER_LINES`, an urgent line of the deck's business, and by night every reportable line,
makes a **call** instead, at once: `report.called`, notable, "Mr Pearce sends for the
captain: land close ahead.", which reaches him wherever he is aboard and wakes him asleep
(`wakes`). The captain on deck gets no report (he sees it); ashore or in the boat none.

**The boat's report ashore.** When a ship's boat manned as a hull (82) comes to the quay of
a port where a person of her company is ashore, the coxswain reports her state: `report.boat`,
notable, in the ship's log, reaching the quay of that port (`port`).

**The command devolves (decision 63).** `you have the deck` with the captain aboard and able
is the watch, as built. When the captain is unavailable, by choice (ashore, in the boat,
aboard another ship) or by force (wounded below, sick below, a captive), the command devolves
on the senior officer, preferring a held station (a model's or the player's) over the rules'
persons: `ship.command_devolved`, notable, "The command devolves on Mr Pearce, the captain
ashore." He holds the captain's authority whole (`tools.judge` reads `in_command`), his
standing orders his guide, and gives it back when the captain is available again and has
given an order again (`ship.command_resumed`). The state is read from the log (the last of
the two lines), cached by the log's length, so that a checkpoint and a replay read the same.

**A told order is the captain's word** (decision 63): an order the captain tells a station
to carry out is the captain's word for that thing; `told_covers` says whether a station's
order is one it was told, and `tools.judge` lets it through as `TOLD`, logged as given by
the station at the captain's word.

The reports and the calls are written from the log and the places, deterministic, so a
replay gives the same lines; the rules' officer writes nothing while a model or the player
holds his station (two reports of one sail would be a doubled line). Ticked by `World.tick`
after the lookout and the routine and before the stations, so that a report is in the tick
the stations sample.
"""

from __future__ import annotations

import weakref
from typing import Any

from freesail.core.events import Severity

__all__ = [
    "COMMAND_DEVOLVED",
    "COMMAND_RESUMED",
    "MESSENGER_S",
    "REPORTABLE",
    "REPORT_BOAT",
    "REPORT_CALLED",
    "REPORT_MADE",
    "call_the_captain",
    "captain_below",
    "command_state",
    "in_command",
    "officer_words",
    "tick",
    "told_covers",
]

REPORT_MADE = "report.made"
REPORT_CALLED = "report.called"
REPORT_BOAT = "report.boat"
COMMAND_DEVOLVED = "ship.command_devolved"
COMMAND_RESUMED = "ship.command_resumed"

# the messenger's minute: the word passed below reaches the captain a minute later, as a
# letter does (`people.PASS_THE_WORD_S`)
MESSENGER_S = 60

# the places aboard from which the captain sees the deck for himself: no report there
_SEES_THE_DECK = frozenset({"quarterdeck", "deck", "galley", "tops", "masthead"})

# the seniority the command devolves by, among the rules' persons (the health module's
# order for a captain killed, package 73)
_SENIORITY = (
    "first lieutenant",
    "lieutenant",
    "second lieutenant",
    "third lieutenant",
    "mate",
    "master",
    "boatswain",
)


# ---------------------------------------------------------------------------
# The reportable kinds, each in the officer's words
# ---------------------------------------------------------------------------


def _lower_first(text: str) -> str:
    text = " ".join(str(text or "").split()).rstrip(".")
    return text[:1].lower() + text[1:] if text else text


def _sighting(e: Any) -> str | None:
    d = e.data or {}
    seen_as = str(d.get("seen_as") or "")
    where = str(d.get("relative") or "").strip()
    tail = f", {where}" if where else ""
    name = str(d.get("name") or "")
    if seen_as == "sail":
        return f"a sail sighted{tail}"
    if seen_as == "danger":
        named = f" ({name})" if name else ""
        return f"a danger sighted{named}{tail}"
    if d.get("landfall"):
        named = f": {name}" if name else ""
        return f"the landfall made{named}{tail}"
    if seen_as in ("land", "light", "mark"):
        what = "a light" if seen_as == "light" else "the land"
        named = f" ({name})" if name and seen_as != "land" else ""
        return f"{what} sighted{named}{tail}"
    return None


def _wind_shift(e: Any) -> str | None:
    return f"a shift of wind: {_lower_first(e.text)}"


def _made_out(e: Any) -> str | None:
    return f"the sail made out: {_lower_first(e.text)}"


def _sail_lost(e: Any) -> str | None:
    words = str((e.data or {}).get("words") or "the sail")
    return f"{_lower_first(words)} lost sight of"


def _land_ahead(e: Any) -> str | None:
    urgent = bool((e.data or {}).get("urgent"))
    return ("land close ahead: " if urgent else "land ahead: ") + _lower_first(e.text)


def _closing(e: Any) -> str | None:
    return f"a bearing steady and closing: {_lower_first(e.text)}"


def _signal(e: Any) -> str | None:
    read = e.kind == "signal.read"
    return f"a signal {'read' if read else 'seen'}: {_lower_first(e.text)}"


def _hail_heard(e: Any) -> str | None:
    return f"a hail: {_lower_first(e.text)}"


def _hail_answered(e: Any) -> str | None:
    if (e.data or {}).get("own"):
        return None  # our own answer to a hail: the hail itself was reported
    return f"the hail answered: {_lower_first(e.text)}"


def _pilot_hail(e: Any) -> str | None:
    return f"the pilot's hail: {_lower_first(e.text)}"


def _boat(e: Any) -> str | None:
    return f"the boat: {_lower_first(e.text)}"


# kind -> the words of the report ("" or None: not reported)
REPORTABLE: dict[str, Any] = {
    "lookout.sighting": _sighting,
    "lookout.made_out": _made_out,
    "lookout.sail_lost": _sail_lost,
    "lookout.land_ahead": _land_ahead,
    "lookout.closing": _closing,
    "wind.shift": _wind_shift,
    "signal.seen": _signal,
    "signal.read": _signal,
    "hail.heard": _hail_heard,
    "hail.answered": _hail_answered,
    "port.pilot_hail": _pilot_hail,
    "boat.alongside": _boat,
    "boat.away": _boat,
}

# the kinds no report is made of though urgent: the stations' and the records' own
_NOT_THE_DECKS = ("agent.", "director.", "query.", "driver.", "world.", "report.", "message.")


def _what(e: Any) -> str | None:
    fn = REPORTABLE.get(e.kind)
    if fn is None:
        return None
    try:
        return fn(e) or None
    except Exception:  # noqa: BLE001  (a line whose data is not the kind's usual)
        return _lower_first(e.text) or None


def _why_called(world: Any, e: Any, what: str | None) -> str | None:
    """Why a line is a call and not a report: a danger line, an urgent line of the deck's
    business, or any reportable line by night; None for a plain report."""
    from freesail.api import readings as R

    if e.kind.startswith(_NOT_THE_DECKS):
        return None  # the stations' own lines (the masthead's hail is the sighting's report)
    danger = R.speaks_of_danger(e.kind, e.data)
    if danger is not None:
        text = _lower_first(e.text)
        head = danger.split()[-1]  # 'dragging', 'aback', 'lifting': the line says it already
        return text if head in text else f"{danger}: {text}"
    if e.severity is Severity.URGENT and not e.kind.startswith(_NOT_THE_DECKS):
        return _lower_first(e.text)
    if what is not None and str(getattr(world, "daylight", "") or "") == "night":
        return what
    return None


# ---------------------------------------------------------------------------
# The captain's whereabouts, the officer's name
# ---------------------------------------------------------------------------


def _people(world: Any) -> Any:
    from freesail.world.movement import _mustered

    people = getattr(world, "people", None)
    if people is None or not _mustered(world):
        return None
    return people


def _hull_id(world: Any) -> str:
    from freesail.world.hearing import own_hull

    return own_hull(world)


def _aboard_here(world: Any, person: Any) -> bool:
    """Whether a person is in this hull (his home's sentinel counts as his own)."""
    from freesail.world.people import ABOARD_HOME

    if not getattr(person, "aboard", True):
        return False
    hull = getattr(person, "hull", None)
    if hull in (None, "", ABOARD_HOME):
        return True
    mine = _hull_id(world)
    return not mine or str(hull) == mine


def captain_below(world: Any) -> Any:
    """The captain, when he is in this hull, awake and not where he sees the deck (the
    cabin, the gunroom, a room below); None otherwise."""
    people = _people(world)
    if people is None:
        return None
    try:
        cap = people.captain
    except Exception:  # noqa: BLE001  (a world with no muster)
        return None
    if cap is None or getattr(cap, "dead", False) or not _aboard_here(world, cap):
        return None
    from freesail.world import knowledge

    if knowledge.is_asleep(world, cap):
        return None
    place = str(people.effective_place(cap) or "")
    return None if place in _SEES_THE_DECK or not place else cap


def _captain_asleep_or_below(world: Any) -> Any:
    """The captain for a call: in this hull and asleep, or below; None on deck awake."""
    people = _people(world)
    if people is None:
        return None
    try:
        cap = people.captain
    except Exception:  # noqa: BLE001
        return None
    if cap is None or getattr(cap, "dead", False) or not _aboard_here(world, cap):
        return None
    from freesail.world import knowledge

    if knowledge.is_asleep(world, cap):
        return cap
    place = str(people.effective_place(cap) or "")
    return None if place in _SEES_THE_DECK or not place else cap


def officer_words(world: Any) -> str:
    """The rules' officer of the watch as the log names him: the person bound to the
    station ("Mr Pearce"; on a merchantman the mate), else 'the officer of the watch'."""
    from freesail.agents.agent import OFFICER, station_holder

    return station_holder(world, OFFICER, ("the officer of the watch", "officer"))[0]


def _officer_held(world: Any) -> bool:
    """Whether a model or the player holds a station of the officer of the watch's kind:
    then the rules' officer makes no report (the duty is the holder's)."""
    try:
        from freesail.agents.watches import held_officers

        return bool(held_officers(world))
    except Exception:  # noqa: BLE001  (a world whose stations cannot be read)
        return False


def _place_words(place: str) -> str:
    from freesail.world.places import place_words

    return place_words(place)


# ---------------------------------------------------------------------------
# The tick
# ---------------------------------------------------------------------------


def _lines_at(log: Any, tick: int) -> list[Any]:
    """The log's lines of one tick, read from the tail (the lines of the last minute)."""
    out: list[Any] = []
    i = len(log) - 1
    while i >= 0:
        e = log[i]
        if e.tick < tick:
            break
        if e.tick == tick:
            out.append(e)
        i -= 1
    out.reverse()
    return out


def _called_lately(log: Any, kind: str, now: int) -> bool:
    """Whether the captain was called for a line of this kind within the hour and has not
    come on deck since: the officer sends for him once for a thing (the recurring lines,
    her sails lifting every look while nobody trims, are one call until he comes up)."""
    i = len(log) - 1
    while i >= 0:
        e = log[i]
        if e.tick < now - 3600:
            return False
        if e.kind == "captain.on_deck":
            return False
        if e.kind == REPORT_CALLED and str((e.data or {}).get("of") or "") == kind:
            return True
        i -= 1
    return False


def tick(world: Any) -> None:
    """Each tick of a hull: the calls for the lines of the tick before (the officer sends
    at once), the reports for the lines of the minute before (the messenger's minute), the
    boat's report at the quay, and the command devolved or resumed."""
    now = int(world.clock.tick)
    from freesail.world.movement import is_boat_hull

    own = getattr(world, "own", None)
    if own is not None and is_boat_hull(own):
        _boats_report(world, own, now)  # her own people are the oars' and unmustered
        return
    people = _people(world)
    if people is None:
        return
    log = world.log
    _devolution(world, people, now)
    if _officer_held(world):
        return  # the holder has the duty himself (the brief says it)
    cap = _captain_asleep_or_below(world)
    if cap is None:
        return
    who = officer_words(world)
    place = str(people.effective_place(cap) or "")
    # the calls: the lines of the tick before, whole
    for e in _lines_at(log, now - 1):
        if e.kind in (REPORT_MADE, REPORT_CALLED):
            continue
        what = _what(e)
        why = _why_called(world, e, what)
        if why is None or _called_lately(log, e.kind, now):
            continue
        world.record(
            Severity.NOTABLE,
            REPORT_CALLED,
            f"{who} sends for the captain: {why}.",
            data={"to": cap.name, "place": place, "why": why, "of": e.kind, "by": who},
        )
    # the reports: the lines of the minute before, for a captain below and awake
    from freesail.world import knowledge

    if knowledge.is_asleep(world, cap):
        return  # the messenger lets him sleep; by night the line was a call
    for e in _lines_at(log, now - MESSENGER_S):
        what = _what(e)
        if what is None or _why_called(world, e, what) is not None:
            continue  # nothing to report, or it was a call already
        world.record(
            Severity.NOTABLE,
            REPORT_MADE,
            f"{who} sent down to the captain, {_place_words(place)}: {what}.",
            data={"to": cap.name, "place": place, "of": e.kind, "text": what, "by": who},
        )


# ---------------------------------------------------------------------------
# The boat's report at the quay
# ---------------------------------------------------------------------------


def _boats_report(world: Any, boat: Any, now: int) -> None:
    """The coxswain's report when the boat comes to the quay of a port where a person of
    her ship's company is ashore (`boat.at_quay`, the tick before); `boat` her hull."""
    from freesail.world import boats as B

    for e in _lines_at(world.log, now - 1):
        if e.kind != "boat.at_quay":
            continue
        port = str((e.data or {}).get("port") or "")
        root = getattr(boat, "world", None) or world
        ship = B.ship_of(root, boat)
        if ship is None or not port:
            continue
        people = getattr(ship, "people", None)
        if people is None:
            continue
        try:
            ashore = [
                p
                for p in people.people
                if not getattr(p, "aboard", True)
                and str(getattr(p, "where", "") or "") == "shore"
                and str(getattr(p, "port", "") or "") == port
            ]
        except Exception:  # noqa: BLE001
            ashore = []
        if not ashore:
            continue
        ship.record(
            Severity.NOTABLE,
            REPORT_BOAT,
            f"The boat came in to the quay at {_port_name(root, port)}; the coxswain "
            f"reports: {_ships_state(ship)}.",
            data={
                "port": port,
                "boat": str(getattr(boat, "id", "") or ""),
                "to": [p.name for p in ashore],
            },
        )


def _port_name(world: Any, port: str) -> str:
    dealings = getattr(world, "dealings", None)
    ports = getattr(dealings, "ports", None) or {}
    found = ports.get(port) if hasattr(ports, "get") else None
    name = getattr(found, "name", None)
    return str(name or port[:1].upper() + port[1:])


def _ships_state(ship: Any) -> str:
    """Her state in the coxswain's words: the ship's state in the truth's words (R-35),
    whose the deck is, and 'all well' or the last urgent line of her log this hour."""
    from freesail.api.readings import _own_state_truth

    try:
        state = _own_state_truth(ship)
    except Exception:  # noqa: BLE001
        state = "as she was"
    deck = _deck_words(ship)
    now = int(ship.clock.tick)
    urgent = None
    log = ship.log
    i = len(log) - 1
    while i >= 0 and log[i].tick >= now - 3600:
        e = log[i]
        if e.severity is Severity.URGENT and not e.kind.startswith(_NOT_THE_DECKS):
            urgent = e
            break
        i -= 1
    tail = "all well" if urgent is None else _lower_first(urgent.text)
    return f"the ship {state}, the deck {deck}, {tail}"


def _deck_words(ship: Any) -> str:
    from freesail.agents.agent import OFFICER, station_holder
    from freesail.agents.harness import holder_of

    try:
        from freesail.agents.watches import held_officers

        for held in held_officers(ship):
            if getattr(held.agent, "has_deck", False):
                person = (
                    getattr(held.station, "person", "")
                    or station_holder(
                        ship, held.station.name, ("the officer of the watch", "officer")
                    )[0]
                )
                return f"{person}'s"
    except Exception:  # noqa: BLE001
        pass
    cap = holder_of(ship, "captain")
    if cap is not None and getattr(cap.agent, "has_deck", False):
        return "the captain's"
    people = _people(ship)
    try:
        aboard = people is not None and _aboard_here(ship, people.captain)
        if aboard and captain_below(ship) is None:
            return "the captain's"
    except Exception:  # noqa: BLE001
        pass
    return f"{station_holder(ship, OFFICER, ('the officer of the watch', 'officer'))[0]}'s"


# ---------------------------------------------------------------------------
# The command devolved (decision 63)
# ---------------------------------------------------------------------------


def _unavailable(world: Any, people: Any, cap: Any) -> str:
    """Why the captain cannot command, in the log's words; "" when he can."""
    if getattr(cap, "dead", False):
        return ""  # the command passed by the bill already (package 73)
    if getattr(cap, "confined_to", ""):
        return "the captain a captive"
    if not getattr(cap, "aboard", True):
        where = str(getattr(cap, "where", "") or "")
        if where == "shore":
            return "the captain ashore"
        return "the captain in the boat"
    if not _aboard_here(world, cap):
        from freesail.world.movement import hull_name, hull_of

        other = hull_of(getattr(world, "world", None) or world, getattr(cap, "hull", None))
        name = hull_name(other) if other is not None else "another ship"
        return f"the captain aboard the {name}"
    where = str(getattr(cap, "where", "") or "")
    if where in ("cockpit", "sick_berth"):
        return "the captain below wounded"
    if getattr(cap, "sick", False):
        return "the captain sick below"
    return ""


# the command's state as last read from each hull's log, by the hull (a weak key, so a
# World dropped takes its cache with it); nothing of it is saved, the log is the record
_STATE_CACHE: Any = weakref.WeakKeyDictionary()
_STATE_CACHE_BY_ID: dict[int, dict[str, Any]] = {}


def _state_cache(world: Any) -> dict[str, Any]:
    key = getattr(world, "own", None) or world
    try:
        cache = _STATE_CACHE.get(key)
        if cache is None:
            cache = _STATE_CACHE[key] = {"seen": 0, "state": None}
        return cache
    except TypeError:  # a key that takes no weak reference
        return _STATE_CACHE_BY_ID.setdefault(id(key), {"seen": 0, "state": None})


def command_state(world: Any) -> dict[str, Any] | None:
    """Whom the command has devolved on, read from the log (the last `ship.command_devolved`
    not followed by `ship.command_resumed`): {station, person, why, tick, journal_at}; None
    while the captain commands. Cached by the log's length."""
    log = getattr(world, "log", None)
    if log is None:
        return None
    cache = _state_cache(world)
    n = len(log)
    if cache["seen"] > n:
        cache["seen"], cache["state"] = 0, None  # a log cut back: read again
    for i in range(cache["seen"], n):
        e = log[i]
        if e.kind == COMMAND_DEVOLVED:
            d = dict(e.data or {})
            d["tick"] = e.tick
            cache["state"] = d
        elif e.kind == COMMAND_RESUMED:
            cache["state"] = None
    cache["seen"] = n
    return cache["state"]


def in_command(world: Any, station: str) -> bool:
    """Whether a station holds the captain's authority by devolution now (decision 63): the
    command devolved on it and it is held still."""
    state = command_state(world)
    if not state or str(state.get("station") or "") != str(station):
        return False
    from freesail.agents.harness import holder_of

    return holder_of(world, station) is not None


def _senior(world: Any, people: Any) -> tuple[str, str]:
    """(the station, the person) the command devolves on: a held station of the officer's
    kind first (the officer of the watch's own first), else the senior of the rules' persons
    aboard; ("", "") when nobody is."""
    try:
        from freesail.agents.watches import held_officers

        for held in held_officers(world):
            name = str(held.station.name)
            person = str(getattr(held.station, "person", "") or "")
            if not person:
                stations = getattr(world, "stations", None)
                bound = stations.holder(name) if stations is not None else None
                person = bound.name if bound is not None else f"the {name}"
            return name, person
    except Exception:  # noqa: BLE001
        pass
    for role in _SENIORITY:
        for p in people.people:
            if (
                p.role == role
                and not getattr(p, "dead", False)
                and _aboard_here(world, p)
                and not getattr(p, "sick", False)
                and str(getattr(p, "where", "") or "") not in ("cockpit", "sick_berth")
            ):
                return "", p.name
    return "", ""


def _captains_order_since(world: Any, journal_at: int) -> bool:
    """Whether the captain has given an order since the devolution (the orders' journal,
    whose actor for the prompt's and the captain's station's orders is 'captain')."""
    journal = getattr(world, "journal", None) or []
    for entry in list(journal)[journal_at:]:
        actor = entry[1] if isinstance(entry, (tuple, list)) and len(entry) > 1 else ""
        if str(actor) in ("captain", "the captain"):
            return True
    return False


def _devolution(world: Any, people: Any, now: int) -> None:
    try:
        cap = people.captain
    except Exception:  # noqa: BLE001
        return
    if cap is None:
        return
    state = command_state(world)
    why = _unavailable(world, people, cap)
    if state is None:
        if not why:
            return
        station, person = _senior(world, people)
        if not person:
            return
        world.record(
            Severity.NOTABLE,
            COMMAND_DEVOLVED,
            f"The command devolves on {person}, {why}.",
            data={
                "station": station,
                "person": person,
                "why": why,
                "journal_at": len(getattr(world, "journal", None) or []),
            },
        )
        command_state(world)  # the cache reads the line
        if station:
            _tell_the_station(world, station, person, why)
        return
    if why:
        return  # the captain unavailable still
    if not _captains_order_since(world, int(state.get("journal_at") or 0)):
        return
    person = str(state.get("person") or "the officer")
    world.record(
        Severity.NOTABLE,
        COMMAND_RESUMED,
        f"The captain has the command again; {person} gives it back.",
        data={"station": str(state.get("station") or ""), "person": person},
    )
    command_state(world)
    station = str(state.get("station") or "")
    if station:
        from freesail.agents.harness import holder_of

        held = holder_of(world, station)
        if held is not None:
            held.agent.notices.append(
                "The captain has the command again: your authority is the station's own, "
                "the deck as you hold it under his standing orders."
            )
            if hasattr(held, "note"):
                held.note("The captain has the command again.", kind="agent.command")


def _tell_the_station(world: Any, station: str, person: str, why: str) -> None:
    """The held station the command devolved on: the deck his if it is not, a notice in
    his next sample and a line in his journal."""
    from freesail.agents.harness import holder_of
    from freesail.orders.errors import OrderError

    held = holder_of(world, station)
    if held is None:
        return
    a = held.agent
    if not getattr(a, "has_deck", False) and getattr(held, "_wants_deck", False):
        try:
            held.give_deck(by="the command devolving on him")
        except OrderError:
            pass
        except Exception:  # noqa: BLE001  (a seat or a station with no deck to give)
            pass
    a.notices.append(
        f"The command has devolved on you, {why}: you hold the captain's authority whole, "
        "his standing orders your guide, until he gives an order again. The log says so."
    )
    if hasattr(held, "note"):
        held.note(f"The command devolved on me, {why}.", kind="agent.command")


# ---------------------------------------------------------------------------
# `call the captain [: <why>]`
# ---------------------------------------------------------------------------


def call_the_captain(world: Any, actor: str, why: str) -> tuple[str, str, dict[str, Any]]:
    """The officer of the watch's order (`orders/people.py`): the call's line, which reaches
    the captain wherever he is aboard and wakes him asleep. Refused in words from the
    captain himself, and when he is on deck already (he sees it: say it to him)."""
    from freesail.orders.errors import OrderError

    people = getattr(world, "people", None)
    if people is None:
        raise OrderError("There is nobody to call: the ship is not in a world.")
    cap = people.captain
    station = str(actor or "captain").split(" (", 1)[0].removeprefix("the ").strip()
    if station in ("captain", ""):
        raise OrderError("You are the captain; there is no sending for yourself.")
    if getattr(cap, "dead", False):
        raise OrderError(f"{cap.name} is dead; the command has passed.")
    if not _aboard_here(world, cap):
        from freesail.world.movement import where_words

        raise OrderError(f"The captain is {where_words(world, cap)}; he cannot be called.")
    from freesail.world import knowledge

    place = str(people.effective_place(cap) or "")
    if place in _SEES_THE_DECK and not knowledge.is_asleep(world, cap):
        raise OrderError(
            f"The captain is {_place_words(place)}: he sees it; say it to him ('say to the "
            "captain ...')."
        )
    why = " ".join(str(why or "").strip(" :,;").split())
    from freesail.agents.agent import station_holder

    who = station_holder(world, station, (f"the {station}", station))[0]
    text = f"{who} sends for the captain" + (f": {why}" if why else "") + "."
    return (
        REPORT_CALLED,
        text,
        {
            "to": cap.name,
            "place": place,
            "why": why,
            "of": "the officer's call",
            "by": who,
            "station": station,
        },
    )


# ---------------------------------------------------------------------------
# A told order is the captain's word (decision 63)
# ---------------------------------------------------------------------------


def _norm(text: str) -> str:
    import re

    text = " ".join(str(text or "").lower().split())
    text = re.sub(r"[.,;:!?'\"]+", " ", text)
    return " ".join(text.split())


def told_covers(ship: Any, told: Any, text: str, order: Any = None, vocab: Any = None) -> bool:
    """Whether an order of a station's is one the captain told it to carry out: the told
    words hold the order's words (after a leading 'to'), or a clause of them parses to the
    same verb and object by the grammar."""
    mine = _norm(text)
    if not mine:
        return False
    clauses: list[str] = []
    for t in list(told or ()):
        t = _norm(t)
        if t.startswith("to "):
            t = t[3:]
        t = t.replace(" and then ", ";").replace(" then ", ";").replace(" and ", ";")
        for part in t.split(";"):
            part = part.strip()
            if part.startswith("to "):
                part = part[3:]
            if part:
                clauses.append(part)
    for c in clauses:
        if c == mine or mine in c or (len(c) > 3 and c in mine):
            return True
    if order is None or vocab is None or not hasattr(ship, "parts"):
        return False
    from freesail.orders import grammar as imperative

    for c in clauses:
        try:
            parsed = imperative.parse(ship, c, vocab)
        except Exception:  # noqa: BLE001  (words the grammar does not read)
            continue
        if parsed.verb == order.verb and (parsed.object or "") == (order.object or ""):
            return True
    return False
