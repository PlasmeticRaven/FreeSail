"""The court martial and a new command (spec M7 §20; package 74, step 6; the design in
`docs/design/Design-Prizes.md` §7): **the court as the director's proceeding**, sat by a
form at a place of a port on a person who lost a ship, its questions through the channel
(`say as the president of the court: "..."` heard at the place, the accused's `say to the
court: ...` his own words, the log of the action read by the judge advocate so that the
proceeding has the facts without the director inventing them), its verdict a form and a
world order journaled, the play log carrying the sentence read and never the order; **the
person's record** (`Person.record`, a list of dated entries: the loss, the trial, the
verdict, the appointment) the thing the career of M8 remembers, kept in the save and read
as `the record` and as the paper "the captain's record"; and **a new command as a
scenario's start**: `command: a new command for <person>: the <description> "<name>" at
<port>` writes a scenario file under the saves' folder (never `data/scenarios/`) carrying
his name as her captain, his people who followed him (the persons ashore at the same port
whose record has the same loss) and the record as a paper, to be given to either driver
with `--scenario`; the career that remembers (half-pay, the reputation, the next ship chosen
by the record) is M8's, the hooks named here (`record_of`, the paper, the scenario's
`papers.record` and `people[].record`, `VERDICTS`).

The verdicts are the period's for the loss of a ship (the Articles of War's sentences as
the courts of 1805 gave them, FROM MEMORY: honourably acquitted, acquitted, reprimanded,
dismissed the ship, dismissed the service); the director decides the sentence as it decides
every cause (the brief: "the director sits as the court"). A world order is never shown as
sent: the court's lines are the court's."""

from __future__ import annotations

import re
from datetime import timedelta
from pathlib import Path
from typing import Any

from freesail.core.events import Severity

__all__ = [
    "COURT_KEY",
    "COURT_PLACE",
    "JUDGE_ADVOCATE",
    "PRESIDENT",
    "VERDICTS",
    "accused_speaks",
    "command_doubt",
    "court_doubt",
    "new_command",
    "note",
    "read_log",
    "record_lines",
    "record_loss",
    "record_of",
    "sit",
    "sitting",
    "verdict",
]

VERDICTS: tuple[str, ...] = (
    "acquitted with honour",
    "acquitted",
    "reprimanded",
    "dismissed the ship",
    "dismissed the service",
)
# the sentence read, by verdict: "{name} is honourably acquitted of the loss of the {ship}"
_SENTENCE_WORDS: dict[str, str] = {
    "acquitted with honour": "is honourably acquitted of the loss of the {ship}, which was "
    "defended with every exertion against a superior force",
    "acquitted": "is acquitted of the loss of the {ship}",
    "reprimanded": "is reprimanded for the loss of the {ship}, and admonished to be more careful "
    "in future",
    "dismissed the ship": "is dismissed his ship for the loss of the {ship}",
    "dismissed the service": "is dismissed His Majesty's service for the loss of the {ship}",
}
COURT_KEY = "court_martial"  # the root World's record of the court sitting
COURT_PLACE = "court_martial"  # the place of the port while the court sits
PRESIDENT = "the president of the court"
JUDGE_ADVOCATE = "the judge advocate"
LOG_KINDS_READ = ("action.", "prize.taken", "prize.possessed", "prize.captive", "colours.struck")
READ_MAX = 40  # lines of the log read to the court at most: the action's, not the passage's
WITHIN_THE_YEAR_S = 365 * 86400

_SITS = re.compile(
    r"^court:\s*sits\s+on\s+(?:the\s+captain\s+of\s+the\s+(?P<ship>[\w' -]+?)"
    r"|\"?(?P<name>[^\":]+?)\"?(?:\s+for\s+the\s+loss\s+of\s+the\s+(?P<ship2>[\w' -]+?))?)"
    r"(?:\s+at\s+(?P<port>[\w' -]+?))?\s*\.?\s*$",
    re.I,
)
_READ = re.compile(r"^court:\s*reads?\s+the\s+log(?:\s+of\s+the\s+action)?\s*\.?\s*$", re.I)
_VERDICT = re.compile(
    r"^court:\s*the\s+verdict\s+on\s+\"?(?P<name>[^\":]+?)\"?\s*:\s*(?P<verdict>.+?)\s*\.?\s*$",
    re.I,
)
_COMMAND = re.compile(
    r"^command:\s*a\s+new\s+command\s+for\s+\"?(?P<name>[^\":]+?)\"?\s*:\s*"
    r"(?:the\s+|a\s+|an\s+)?(?P<desc>[\w' -]+?)\s+\"(?P<ship>[^\"]+)\"\s+at\s+(?P<port>[\w' -]+?)"
    r"\s*\.?\s*$",
    re.I,
)


class CourtError(ValueError):
    """Refused in words (the channel's `WorldOrderError` wraps it)."""


def _root(world: Any) -> Any:
    from freesail.world.hulls import world_of

    return world_of(world)


def _stamp(root: Any) -> str:
    from freesail import units

    clock = root.clock
    return f"{clock.ship_time:%d %B %Y}, {units.time_stamp(clock.ship_time)}"


# -- the person's record --------------------------------------------------------------------------
def record_of(person: Any) -> list[dict[str, Any]]:
    """The person's record: dated entries (the loss of a ship, the court, the verdict, an
    appointment), kept on him in the save; a person of a checkpoint from before has none
    until something is entered."""
    d = getattr(person, "__dict__", None)
    if d is None:
        return []
    rec = d.get("record")
    if not isinstance(rec, list):
        rec = []
        d["record"] = rec
    return rec


def note(world: Any, person: Any, kind: str, words: str, **data: Any) -> dict[str, Any]:
    """An entry in his record, dated now."""
    root = _root(world)
    entry: dict[str, Any] = {
        "tick": int(root.clock.tick),
        "when": _stamp(root),
        "kind": kind,
        "words": words,
        **data,
    }
    record_of(person).append(entry)
    return entry


def record_lines(person: Any) -> list[str]:
    return [f"{e.get('when', '')}: {e.get('words', '')}." for e in record_of(person)]


def record_loss(world: Any, hull: Any, record: dict[str, Any]) -> Any:
    """The loss entered in the records of the ship's officers at her taking (hooked at the
    possession): her captain's as the man who commanded her, and her officers' as the men
    who lost her with him (the followers a new command gathers, §7.2). Returns the captain,
    or None for a hull with no named captain."""
    from freesail.world.prizes import OFFICER_ROLES

    people = getattr(hull, "people", None)
    if people is None:
        return None
    try:
        captain = people.captain
    except Exception:  # noqa: BLE001  (a hull with no muster)
        return None
    ship_name = str(getattr(getattr(hull, "ship", None), "name", "") or hull.id)
    captor = str(record.get("captor_name") or "the enemy")
    how = str(record.get("how") or "taken")
    hid = str(getattr(hull, "id", ""))
    for p in list(getattr(people, "everyone", None) or people.people):
        # her company's officers wherever each is now (her captain is aboard the captor
        # already where he is the player's person, `captive.player_taken`)
        if getattr(p, "dead", False) or str(getattr(p, "home", "") or "") != hid:
            continue
        if p is not captain and str(getattr(p, "role", "")) not in OFFICER_ROLES:
            continue
        mine = p is captain
        note(
            world,
            p,
            "loss",
            f"the loss of the {ship_name}, {how} by the {captor}"
            + ("" if mine else f", {p.role} in her"),
            ship=hid,
            ship_name=ship_name,
            captor=str(record.get("captor") or ""),
            command=mine,
            nation=str(record.get("nation_was") or ""),
        )
    if captain is None or getattr(captain, "dead", False):
        return None
    return captain


def _losses(person: Any) -> list[dict[str, Any]]:
    return [e for e in record_of(person) if e.get("kind") == "loss"]


def _last_verdict(person: Any) -> dict[str, Any] | None:
    found = [e for e in record_of(person) if e.get("kind") == "verdict"]
    return found[-1] if found else None


# -- the court sitting ----------------------------------------------------------------------------
def sitting(world: Any) -> dict[str, Any] | None:
    rec = _root(world).__dict__.get(COURT_KEY)
    return rec if isinstance(rec, dict) and rec else None


def _person(root: Any, name: str) -> Any:
    from freesail.world.orders import _person_anywhere

    found = _person_anywhere(root, name)
    if found is None:
        raise CourtError(f"No person of the world is named {name!r}.")
    return found


def _by_ship(root: Any, ship: str) -> Any:
    key = " ".join(ship.lower().split())
    registry = getattr(root, "registry", None)
    for p in registry.persons() if registry is not None else []:
        if any(str(e.get("ship_name", "")).lower() == key for e in _losses(p)):
            return p
    raise CourtError(f"Nobody of the world lost a ship named {ship!r}.")


def _port(root: Any, words: str) -> Any:
    from freesail.world.orders import _port_named

    return _port_named(root, words)


def _port_of_person(root: Any, person: Any) -> Any:
    ports = getattr(getattr(root, "ports", None), "ports", {}) or {}
    pid = str(getattr(person, "port", "") or "")
    return ports.get(pid) if (pid and not getattr(person, "aboard", True)) else None


def _parts_sit(root: Any, body: str) -> tuple[Any, dict[str, Any], Any]:
    m = _SITS.match(" ".join(str(body).split()))
    if m is None:
        raise CourtError(
            "A court order is 'court: sits on <person> for the loss of the <ship> at <port>' "
            "(or 'court: sits on the captain of the <ship> at <port>'), 'court: read the log "
            "of the action' or 'court: the verdict on <person>: <verdict>'."
        )
    if m.group("ship"):
        person = _by_ship(root, m.group("ship"))
    else:
        person = _person(root, m.group("name").strip())
    losses = _losses(person)
    if not losses:
        raise CourtError(
            f"{person.name} lost no ship under his command: his record has no loss, and the "
            "court sits on nobody for nothing."
        )
    loss = losses[-1]
    if m.group("ship2"):
        key = " ".join(m.group("ship2").lower().split())
        named = [e for e in losses if str(e.get("ship_name", "")).lower() == key]
        if not named:
            raise CourtError(
                f"{person.name} lost no ship named {m.group('ship2')!r}; his record has the "
                f"loss of the {loss.get('ship_name')}."
            )
        loss = named[-1]
    port = _port(root, m.group("port")) if m.group("port") else _port_of_person(root, person)
    if port is None:
        raise CourtError(
            f"Say at which port the court sits: {person.name} is not ashore at a port of the chart."
        )
    return person, loss, port


def _nation_of_person(root: Any, person: Any) -> str:
    """His nation: the one his lost ship sailed under (her record's `nation_was`, kept in his
    loss entry: a prize flies her captor's colours now), else his home hull's, else the
    scenario's."""
    losses = _losses(person)
    if losses and losses[-1].get("nation"):
        return str(losses[-1]["nation"])
    hulls = getattr(root, "hulls", None) or {}
    home = hulls.get(str(getattr(person, "home", "") or ""))
    v = getattr(home, "vessel", None) if home is not None else None
    if v is not None:
        from freesail.world.prizes import is_prize
        from freesail.world.prizes import record_of as prize_record

        if is_prize(v) and (prize_record(v) or {}).get("nation_was"):
            return str(prize_record(v)["nation_was"])
        if getattr(v, "nation", ""):
            return str(v.nation)
    return str(getattr(getattr(root, "scenario", None), "nation", "") or "")


def court_doubt(world: Any, body: str) -> str | None:
    """Why the court could not sit: the accused is not ashore at a port of his own nation (a
    captive is tried when he comes home: by cartel, by exchange, by the port's agent landing
    him at a friendly port); the doubt's words say where he is."""
    root = _root(world)
    if _READ.match(" ".join(str(body).split())) or _VERDICT.match(" ".join(str(body).split())):
        return None
    try:
        person, _loss, port = _parts_sit(root, body)
    except CourtError:
        return None
    from freesail.world.movement import where_words

    nation = _nation_of_person(root, person)
    if nation and str(getattr(port, "nation", "")) != nation:
        return (
            f"{port.name} is {_people(root, str(port.nation))}: a court martial sits at a port "
            f"of his own nation, and {person.name} is {_people(root, nation)}"
        )
    at = _port_of_person(root, person)
    if at is None or at is not port:
        return (
            f"{person.name} is {where_words(root, person)}: a court martial sits when he is "
            f"ashore at {port.name} (by cartel, by exchange, or landed there by the port's agent)"
        )
    return None


def _people(root: Any, nation_id: str) -> str:
    nations = getattr(root, "nations", None)
    try:
        n = nations.get(nation_id)
        return str(getattr(n, "people", None) or getattr(n, "name", None) or nation_id)
    except Exception:  # noqa: BLE001
        return nation_id or "of no nation"


def _place_entry(port: Any, person: Any) -> dict[str, Any]:
    return {
        "id": COURT_PLACE,
        "name": "the court martial",
        "done": "the great cabin of the flagship in the harbour, where the court martial sits "
        f"on {person.name}; the president and the members, the judge advocate, the witnesses "
        "waiting",
        "found": "the president and the members of the court, the judge advocate, the accused "
        "and the witnesses",
        "roles": ["president of the court", "judge advocate", "member of the court"],
    }


def _make_officer(root: Any, name: str, role: str, port: Any) -> Any:
    from freesail.world.people import Person

    pid = re.sub(r"[^a-z0-9]+", "_", f"{role}".lower()).strip("_")
    found = root.people.find_anywhere(name)
    if found is not None:
        return found
    p = Person(pid, name, role, 0.8, place="shore", aboard=False, port=port.id)
    p.ashore_at = COURT_PLACE
    root.people.add(p)
    return p


def _hearers_at(root: Any, person: Any) -> list[Any]:
    from freesail.world.orders import _hearers_ashore

    try:
        return _hearers_ashore(root, person)
    except Exception:  # noqa: BLE001  (a world whose stations cannot be read)
        return []


def sit(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`court: sits on <person> for the loss of the <ship> at <port>`: the court's place
    made at the port, its president and judge advocate found there, the accused moved
    there, the sitting entered in his record and said (`court.sits`, urgent)."""
    root = _root(world)
    tick = int(root.clock.tick)
    if sitting(root) is not None:
        rec = sitting(root)
        raise CourtError(
            f"A court martial sits already, on {rec.get('person')} at {rec.get('port_name')}: "
            "its verdict first."
        )
    person, loss, port = _parts_sit(root, body)
    ship_name = str(loss.get("ship_name") or "her")
    port.places = (*tuple(getattr(port, "places", ()) or ()), _place_entry(port, person))
    president = _make_officer(root, PRESIDENT, "president of the court", port)
    judge = _make_officer(root, JUDGE_ADVOCATE, "judge advocate", port)
    # the accused before the court: ashore at the place, whatever held him before
    from freesail.world.captive import release

    was_aboard = bool(getattr(person, "aboard", True))
    if was_aboard:
        person.aboard = False
    person.where = "shore"
    person.port = port.id
    person.ashore_at = COURT_PLACE
    person.occupied_until = None
    person.occupied_with = ""
    person.pending = None
    release(root, person, "brought before the court")
    person.cartel = ""
    root.__dict__[COURT_KEY] = {
        "person": person.name,
        "id": person.id,
        "port": port.id,
        "port_name": port.name,
        "ship": str(loss.get("ship") or ""),
        "ship_name": ship_name,
        "since": tick,
        "read": 0,
        "president": president.id,
        "judge_advocate": judge.id,
    }
    note(
        root,
        person,
        "court",
        f"tried by court martial at {port.name} for the loss of the {ship_name}",
        port=port.id,
        ship=str(loss.get("ship") or ""),
    )
    text = (
        f"The court martial sits at {port.name} on {person.name} for the loss of the "
        f"{ship_name}: the great cabin of the flagship in the harbour; the president and the "
        "members, the judge advocate, the witnesses waiting."
    )
    root.record(
        Severity.URGENT,
        "court.sits",
        text,
        data={
            "person": person.name,
            "port": port.id,
            "place": "shore",
            "ship": str(loss.get("ship") or ""),
        },
    )
    for h in _hearers_at(root, person):
        h.hear(text)
    return (
        f"the court martial sits at {port.name} on {person.name} for the loss of the "
        f"{ship_name}; {person.name} is before it",
        {
            "person": person.name,
            "port": port.id,
            "ship": str(loss.get("ship") or ""),
            "place": COURT_PLACE,
        },
    )


def _log_lines(root: Any, rec: dict[str, Any]) -> list[tuple[str, str]]:
    """(the stamp, the text) of the action's lines of the lost ship's log: the hull's where
    she is a hull still, else her story's lines."""
    from freesail import units

    hulls = getattr(root, "hulls", None) or {}
    hull = hulls.get(str(rec.get("ship") or ""))
    out: list[tuple[str, str]] = []
    if hull is not None and getattr(hull, "log", None) is not None:
        for e in hull.log:
            kind = str(getattr(e, "kind", ""))
            if any(kind.startswith(k) if k.endswith(".") else kind == k for k in LOG_KINDS_READ):
                out.append((units.time_stamp(e.ship_time), str(e.text)))
    if not out:
        v = getattr(root, "vessels", None)
        vessel = v.get(str(rec.get("ship") or "")) if v is not None else None
        for tick, words in getattr(vessel, "story", ()) or ():
            when = root.clock.ship_time - timedelta(seconds=int(root.clock.tick) - int(tick))
            out.append((units.time_stamp(when), str(words)))
    return out[-READ_MAX:]


def read_log(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`court: read the log of the action`: the judge advocate reads the action's lines of
    the lost ship's log to the court (`court.reading`, heard at the place), so that the
    proceeding has the facts without the director inventing them."""
    root = _root(world)
    rec = sitting(root)
    if rec is None:
        raise CourtError("No court martial sits: 'court: sits on <person> ...' first.")
    lines = _log_lines(root, rec)
    ship_name = rec.get("ship_name", "her")
    if not lines:
        raise CourtError(
            f"The log of the {ship_name} is not before the court: no line of an action is "
            "in it, and her story has none."
        )
    judge = None
    registry = getattr(root, "registry", None)
    for p in registry.persons() if registry is not None else []:
        if p.id == rec.get("judge_advocate"):
            judge = p
            break
    hearers = _hearers_at(root, judge) if judge is not None else []
    for stamp, text in lines:
        line = f"The judge advocate reads from the log of the {ship_name}: {stamp}, {text}"
        root.record(
            Severity.NOTABLE,
            "court.reading",
            line,
            data={
                "ship": rec.get("ship"),
                "stamp": stamp,
                "port": rec.get("port"),
                "place": "shore",
            },
        )
        for h in hearers:
            h.hear(line)
    rec["read"] = int(rec.get("read", 0) or 0) + len(lines)
    return (
        f"the log of the {ship_name} read to the court by the judge advocate: "
        f"{len(lines)} lines of the action",
        {"ship": rec.get("ship"), "lines": len(lines)},
    )


def accused_speaks(world: Any, person: Any, words: str) -> tuple[str, str, dict[str, Any]]:
    """`say to the court: <words>` (the player's or a model's, the accused's own): heard at
    the place, in the play log as his (`court.said`), once, by the order's own line."""
    root = _root(world)
    rec = sitting(root)
    words = " ".join(str(words or "").split()).strip(" ,:")
    if rec is None:
        raise CourtError("No court martial sits; there is no court to speak to.")
    if person is None or person.name != rec.get("person"):
        who = getattr(person, "name", None) or "you"
        raise CourtError(
            f"The court sits on {rec.get('person')}, not on {who}: a witness speaks when he "
            "is called (the director's 'say as <him>: ...')."
        )
    if str(getattr(person, "ashore_at", "")) != COURT_PLACE or getattr(person, "aboard", True):
        raise CourtError(f"You are not before the court; it sits at {rec.get('port_name')}.")
    if not words:
        raise CourtError("Say what to the court? Put your words after the colon.")
    line = f"{person.name}, before the court at {rec.get('port_name')}: {words}"
    for h in _hearers_at(root, person):
        h.hear(line)
    # one line in the log, the order's own (the world writes what an order returns): his
    # words as he said them, the shore and the port named for who hears them
    data = {"person": person.name, "words": words, "port": rec.get("port"), "place": "shore"}
    return "court.said", line, data | {"level": 2}


def verdict(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`court: the verdict on <person>: <verdict>`: one of `VERDICTS`, entered in his record
    and read as the court's sentence (`court.verdict`, urgent; the order is never shown as
    sent); the court rises: its place and its officers gone from the port, the accused on
    the quay."""
    root = _root(world)
    m = _VERDICT.match(" ".join(str(body).split()))
    if m is None:
        raise CourtError(
            "The verdict is 'court: the verdict on <person>: acquitted with honour | acquitted "
            "| reprimanded | dismissed the ship | dismissed the service'."
        )
    rec = sitting(root)
    if rec is None:
        raise CourtError("No court martial sits: 'court: sits on <person> ...' first.")
    name = m.group("name").strip()
    if name.lower() != str(rec.get("person", "")).lower():
        raise CourtError(f"The court sits on {rec.get('person')}, not on {name}.")
    said = " ".join(m.group("verdict").lower().split()).rstrip(".")
    said = said.removeprefix("he is ").removeprefix("is ")
    if said in ("honourably acquitted", "acquitted with honour", "acquitted honourably"):
        said = "acquitted with honour"
    if said in ("dismissed his ship", "dismissed from the ship", "dismissed the ship"):
        said = "dismissed the ship"
    if said in ("dismissed from the service", "dismissed the service", "broke", "broken"):
        said = "dismissed the service"
    if said not in VERDICTS:
        raise CourtError(
            f"The court knows no sentence {m.group('verdict').strip()!r}; its sentences for "
            f"the loss of a ship are {', '.join(VERDICTS)}."
        )
    person = _person(root, name)
    port_id = str(rec.get("port") or "")
    ports = getattr(getattr(root, "ports", None), "ports", {}) or {}
    port = ports.get(port_id)
    ship_name = str(rec.get("ship_name") or "her")
    sentence = f"{person.name} {_SENTENCE_WORDS[said].format(ship=ship_name)}"
    note(
        root,
        person,
        "verdict",
        f"{said} by the court martial at {rec.get('port_name')} for the loss of the {ship_name}",
        verdict=said,
        port=port_id,
        ship=str(rec.get("ship") or ""),
    )
    text = f"The sentence of the court martial is read: {sentence}."
    root.record(
        Severity.URGENT,
        "court.verdict",
        text,
        data={
            "person": person.name,
            "verdict": said,
            "port": port_id,
            "place": "shore",
            "ship": rec.get("ship"),
        },
    )
    for h in _hearers_at(root, person):
        h.hear(text)
    # the court rises
    if port is not None:
        port.places = tuple(
            e for e in (getattr(port, "places", ()) or ()) if e.get("id") != COURT_PLACE
        )
    registry = getattr(root, "registry", None)
    for p in list(registry.persons()) if registry is not None else []:
        if p.id in (rec.get("president"), rec.get("judge_advocate")):
            root.people.remove(p)
    if str(getattr(person, "ashore_at", "")) == COURT_PLACE:
        person.ashore_at = "quay"
    root.__dict__.pop(COURT_KEY, None)
    root.__dict__["last_court_martial"] = {**rec, "verdict": said, "tick": int(root.clock.tick)}
    return (
        f"the sentence of the court martial on {person.name}: {said}; the court rises",
        {"person": person.name, "verdict": said, "port": port_id},
    )


# -- a new command --------------------------------------------------------------------------------
def _parts_command(root: Any, body: str) -> tuple[Any, str, dict[str, Any], str, Any]:
    from freesail.world.ships import DESCRIPTIONS, description_key

    m = _COMMAND.match(" ".join(str(body).split()))
    if m is None:
        raise CourtError(
            "A command order is 'command: a new command for <person>: the <description> "
            "\"<name>\" at <port>' ('command: a new command for Captain Bowen: the sloop "
            '"Alert" at Plymouth\').'
        )
    person = _person(root, m.group("name").strip())
    key = description_key(m.group("desc"))
    if key is None:
        names = ", ".join(sorted(k for k in DESCRIPTIONS if k != "cartel"))
        raise CourtError(
            f"'{m.group('desc')}' names no ship the game has a file for; the descriptions: {names}."
        )
    port = _port(root, m.group("port"))
    return person, key, dict(DESCRIPTIONS[key]), m.group("ship").strip(), port


def command_doubt(world: Any, body: str) -> str | None:
    """A new command for a man dismissed his ship within the year wants a cause."""
    root = _root(world)
    try:
        person, _key, _desc, _ship, _port = _parts_command(root, body)
    except CourtError:
        return None
    last = _last_verdict(person)
    if last is not None and last.get("verdict") == "dismissed the ship":
        ago = int(root.clock.tick) - int(last.get("tick", 0))
        if ago < WITHIN_THE_YEAR_S:
            return (
                f"{person.name} was dismissed his ship {ago // 86400} days ago: a new command "
                "within the year wants a cause (interest, a friend at the Admiralty)"
            )
    return None


def _followers(root: Any, person: Any, port: Any) -> list[Any]:
    """His people who followed him: the persons ashore at the same port whose record has the
    same loss (the period's followers: a captain's coxswain and his lieutenants going with
    him)."""
    ships = {str(e.get("ship") or "") for e in _losses(person)}
    registry = getattr(root, "registry", None)
    out = []
    for p in registry.persons() if registry is not None else []:
        if p is person or getattr(p, "dead", False) or getattr(p, "aboard", True):
            continue
        if str(getattr(p, "port", "") or "") != str(port.id):
            continue
        if any(str(e.get("ship") or "") in ships for e in _losses(p)):
            out.append(p)
    return out


def _saves_dir(root: Any) -> Path:
    said = root.__dict__.get("saves_dir")
    if said:
        return Path(str(said))
    from freesail.agents.remote import SAVES_DIR

    return Path(SAVES_DIR)


def new_command(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`command: a new command for <person>: the <description> "<name>" at <port>`: a
    scenario file written under the saves' folder (96's writer) carrying what the records
    keep, named in the answer; refused for a man dismissed the service."""
    from freesail.world.scenarios import write_scenario

    root = _root(world)
    person, key, desc, ship_name, port = _parts_command(root, body)
    last = _last_verdict(person)
    if last is not None and last.get("verdict") == "dismissed the service":
        raise CourtError(
            f"{person.name} was dismissed the service by the court martial at "
            f"{_port_words(root, last.get('port'))}; the service gives him no command."
        )
    if sitting(root) is not None and sitting(root).get("person") == person.name:
        raise CourtError(f"The court martial sits on {person.name} still: its verdict first.")
    followers = _followers(root, person, port)
    when = root.clock.ship_time + timedelta(days=1)
    start = when.replace(hour=8, minute=0, second=0, microsecond=0)
    position = port.anchorage.position
    nation = _nation_of_person(root, person) or str(getattr(port, "nation", "") or "")
    region = str(getattr(getattr(root, "scenario", None), "region", "") or "")
    slug = re.sub(r"[^a-z0-9]+", "-", ship_name.lower()).strip("-") or "ship"
    path = _saves_dir(root) / f"new-command-{slug}-{start:%Y-%m-%d}.yaml"
    if root.__dict__.get("dry_run"):
        # the director's dry run performs on a copy of the world and writes no file
        names = ", ".join(f.name for f in followers) or "nobody of his old company"
        return (
            f"a new command for {person.name}: the {key} {ship_name} at {port.name}; her "
            f"scenario would be written to {path.as_posix()}; following him, {names}",
            {"person": person.name, "ship": ship_name, "port": port.id, "dry_run": True},
        )
    # the appointment in his record first, so that the record the scenario carries has it
    appointed = note(
        root,
        person,
        "command",
        f"appointed to the {key} {ship_name} at {port.name}",
        ship_name=ship_name,
        port=port.id,
        scenario=path.as_posix(),
    )
    people: list[dict[str, Any]] = [
        {"role": "captain", "name": person.name, "record": [dict(e) for e in record_of(person)]}
    ]
    for f in followers:
        people.append(
            {"role": str(f.role), "name": str(f.name), "record": [dict(e) for e in record_of(f)]}
        )
    raw: dict[str, Any] = {
        "name": f"A new command: the {key} {ship_name} at {port.name}",
        "seed": int(getattr(root, "seed", 7)),
        "start": start.strftime("%Y-%m-%dT%H:%M"),
        "position": {
            "lat_deg": round(float(position.lat_deg), 5),
            "lon_deg": round(float(position.lon_deg), 5),
        },
        "ship": {"file": str(desc["file"]), "name": ship_name, "heading_deg": 0},
        "people": people,
        "papers": {"record": record_lines(person)},
        "ports": [str(port.id)],
    }
    if region:
        raw["region"] = region
    if nation:
        raw["nation"] = nation
    try:
        written = write_scenario(raw, path)
    except Exception as e:  # noqa: BLE001  (the writer's own words)
        record_of(person).remove(appointed)
        raise CourtError(f"the scenario could not be written: {str(e).rstrip('.')}") from None
    names = ", ".join(f.name for f in followers)
    follow = f"; {names} follow him" if followers else "; nobody of his old company follows him"
    text = (
        f"A new command: the {key} {ship_name} at {port.name} for {person.name}; her scenario "
        f"is {written.as_posix()}, to be given to either driver with --scenario{follow}."
    )
    root.record(
        Severity.NOTABLE,
        "command.new",
        text,
        data={
            "person": person.name,
            "ship": ship_name,
            "file": str(desc["file"]),
            "port": port.id,
            "scenario": written.as_posix(),
            "followers": [f.name for f in followers],
        },
    )
    return text.rstrip("."), {
        "person": person.name,
        "ship": ship_name,
        "port": port.id,
        "scenario": written.as_posix(),
        "followers": [f.name for f in followers],
    }


def _port_words(root: Any, port_id: Any) -> str:
    ports = getattr(getattr(root, "ports", None), "ports", {}) or {}
    p = ports.get(str(port_id or ""))
    return str(getattr(p, "name", None) or port_id or "a port")


# -- the record read ------------------------------------------------------------------------------
def record_words(world: Any, person: Any) -> str:
    """`the record`: his record's entries in words, or 'no record'."""
    if person is None:
        return "no record: nobody is named at your station"
    entries = record_of(person)
    if not entries:
        return f"no record: nothing is entered against {person.name}"
    return f"{person.name}'s record: " + "; ".join(
        f"{e.get('when', '')}, {e.get('words', '')}" for e in entries
    )


def paper_lines(world: Any) -> list[str]:
    """The paper "the captain's record": the scenario's `papers.record` lines (a record
    carried from the last game) and the captain's own entries."""
    out: list[str] = []
    sc = getattr(world, "scenario", None)
    carried = (getattr(sc, "papers", None) or {}).get("record") if sc is not None else None
    for line in carried or []:
        out.append(str(line))
    people = getattr(world, "people", None)
    try:
        captain = people.captain if people is not None else None
    except Exception:  # noqa: BLE001
        captain = None
    if captain is not None:
        out += [ln for ln in record_lines(captain) if ln not in out]
    if not out:
        return ["Nothing is entered in the captain's record."]
    return out
