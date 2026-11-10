"""The captive's channel (spec M7 §19; package 74, step 3; the design in
`docs/design/Design-Prizes.md` §3): what follows for a person whose ship is taken.

**The player struck** (§3.1). When the captor takes possession of the player's ship (the
rules captain by `taking possession`, a model's own `take possession of her`, the far body at
hail) the player's person is put aboard the captor by `movement.put_aboard` with his station
standing down ("taken in the prize": a captive does not command his ship, and her `captain`
is the prize master's); the captor is made a hull and woken if she has none. **His prompt
follows his body** (decision 62: `put_aboard` moves the drivers' `followed` with him), and
at her prompt he is a visitor of 82's kind with a prisoner's reach: `where am I`, the readings
his place allows, `say to the captain: ...`, `ask`, `tell`, his journal, a free line, a stand-
by; every order of her deck refused in words naming his state (`movement.check`), and every
order of his own ship's from her prompt refused as a prize's (`CAPTIVE_WORDS`). The one
world keeps who he is (`captivity`: the root's record, read by `knowledge.players_person`,
since his ship's `captain` answers for the prize master from the taking).

**The parole** (§3.2): a state of the captive on the captor's `Prisoners` record and of his
person (`confined_to`, `liberty`). Asked by the captor's rules captain by doctrine
(`parole_accepted`) a minute after the taking in the period's words from `data/captains/
hail.yaml`'s `parole:` table by his nation (France's in French and English as the hail's
lies are; Spain's row, decision 64), a line of the hull's log the captive's place hears
(`prize.parole_asked`); answered by the captive in his own words (`say to the captain: I
give you my parole`), read by a small table of the period's forms only while a parole is
asked and unanswered (`PAROLE_GIVEN_WORDS`, `PAROLE_REFUSED_WORDS`); asked once more after
a glass when nothing readable came; given by rule when nobody speaks for a watch (an
officer's word was taken by the custom; the people were confined). Given: the cabin and the
gunroom his and the quarterdeck by day, his sword returned (a thing of 53b's made at the
taking in the captor's captain's keeping); refused: the gunroom alone, a sentry at the door
(said, nothing modelled of the sentry). The director sets it for a captive nobody asks
(`aboard the <captor>: the parole of Captain Bowen given`).

**The prisoners landed** (§3.3): the captor's course for his doctrine's port (`prisoners_
landed`), and in port the prisoners landed to the port's **agent for prisoners** (`places.
PORT_PLACES`: "the agent for prisoners", "le commissaire des prisonniers", "el comisario de
prisioneros" by the port's nation), the captive's person ashore at that place ("a prisoner
of war ashore at Brest"), from where the continuation is the director's.

**The cartel** (§3.4): `cartel: a cartel from <port> for <persons>` puts a vessel of the
`cartel` description on the sea at the port's road under a flag of truce (her colours'
state `truce`, which no captain fires on and the far captures pass by), who steers for the
hull that holds the persons named, takes them off by the boat within hail and sails for her
port, where they are landed free. Her words and places filled out are package 80's.

**Parity** (§3.5): a prisoner of the player's prize is a person of her company in her cabin
by the same record, his voice a seat the director may hold (not an adversarial one: §6).
"""

from __future__ import annotations

import re
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.crew.model import number_words

__all__ = [
    "CAPTIVE_KEY",
    "CARTEL_ROLE",
    "PAROLE_ASK_AGAIN_S",
    "PAROLE_BY_RULE_S",
    "PAROLE_GIVEN_WORDS",
    "PAROLE_REFUSED_WORDS",
    "PLACES_ON_PAROLE",
    "PLACES_ON_PAROLE_NIGHT",
    "PLACES_REFUSED",
    "answer_parole",
    "ask_parole",
    "captive_of",
    "captive_person",
    "captive_words",
    "cartel_minute",
    "hear_parole",
    "is_captive",
    "land_prisoners",
    "minute",
    "player_taken",
    "put_cartel",
    "release",
]

CAPTIVE_KEY = "captive"  # the root World's record of the player's person taken
CARTEL_ROLE = "cartel"
# the cartel sails as a merchant brig of her own file (75's sub-type rows: every row of the
# index is a file's own description with its fit and roles, so she has no row of her own;
# what she is when made out is said on her, below)
CARTEL_DESCRIPTION = "merchant brig"
PAROLE_ASK_AGAIN_S = 1800  # a glass: the question put once more when nothing readable came
PAROLE_BY_RULE_S = 4 * 3600  # a watch: an officer's parole given by rule when nobody spoke
PAROLE_FIRST_ASK_S = 60  # the rules captain asks a minute after the taking
# the places a parole gives (the liberty of the quarterdeck by day), and refused
PLACES_ON_PAROLE: tuple[str, ...] = ("cabin", "gunroom", "quarterdeck")
PLACES_ON_PAROLE_NIGHT: tuple[str, ...] = ("cabin", "gunroom")
PLACES_REFUSED: tuple[str, ...] = ("gunroom",)
# the period's forms, read only while a parole is asked and unanswered
PAROLE_GIVEN_WORDS: tuple[str, ...] = (
    "give my parole",
    "give you my parole",
    "my parole",
    "you have my word",
    "i give it",
    "give my word",
    "ma parole",
    "doy mi palabra",
)
PAROLE_REFUSED_WORDS: tuple[str, ...] = (
    "refuse",
    "will not give",
    "shall not give",
    "no parole",
    "i decline",
    "do not give",
    "cannot give",
)
# a bare answer to the open question (the owner's play of 2026-11-09: "Yes." was not read),
# read as whole words and only while the question is open; both sides in one answer read
# as neither, and the question stays open
PAROLE_YES_WORDS: tuple[str, ...] = ("yes", "oui", "sí", "si", "aye", "i do", "you have it")
PAROLE_NO_WORDS: tuple[str, ...] = ("no", "non", "never", "i will not")
# the cartel's errand
CARTEL_HAIL_M = 4.0 * units.CABLE  # within hail of the holder: the persons taken off
CARTEL_DAY_NM = 100.0  # a day's sail from her port, beyond which the form is doubted
CARTEL_SPEED_KN = 6.0

_PAROLE_FORM = re.compile(
    r"^the\s+parole\s+of\s+(?P<name>.+?)\s+(?:is\s+)?(?P<what>given|taken|refused)\s*\.?$", re.I
)


# -- the record ------------------------------------------------------------------------------------


def _root(world: Any) -> Any:
    from freesail.world.hulls import world_of

    return world_of(world)


def captive_of(world: Any) -> dict[str, Any] | None:
    """The root's record of the player's person taken: his name and id, his home hull, the
    captor's hull, the tick, where he was landed; None when he is free."""
    root = _root(world)
    rec = root.__dict__.get(CAPTIVE_KEY)
    return rec if isinstance(rec, dict) and rec else None


def captive_person(world: Any) -> Any:
    """The player's person while he is a captive, found in the one registry by his id and
    his home; None when he is free or cannot be found."""
    rec = captive_of(world)
    if rec is None:
        return None
    root = _root(world)
    registry = getattr(root, "registry", None)
    if registry is None:
        return None
    pid, home = str(rec.get("id") or ""), str(rec.get("home") or "")
    for hid in (home, *[h for h in getattr(registry, "hulls", []) if h != home]):
        for p in registry.company(hid):
            if p.id == pid and p.name == rec.get("person") and not getattr(p, "dead", False):
                return p
    return None


def is_captive(person: Any) -> bool:
    return bool(getattr(person, "confined_to", "") or getattr(person, "liberty", ()))


def release(world: Any, person: Any, why: str) -> None:
    """The captive free: his confinement and his liberty gone, the root's record cleared
    when it is his."""
    person.confined_to = ""
    person.liberty = ()
    rec = captive_of(world)
    if rec is not None and rec.get("person") == person.name:
        root = _root(world)
        root.__dict__.pop(CAPTIVE_KEY, None)
        hull = _hull_of(root, rec.get("captor"))
        if hull is not None:
            hull.record(
                Severity.NOTABLE,
                "prize.captive_freed",
                f"{person.name} is free: {why}.",
                data={"person": person.name, "why": why},
            )


def _hull_id(hull: Any) -> str:
    """A hull's id, the World's own hull's when the World itself is given (a world order's
    target for the followed hull)."""
    hid = getattr(hull, "id", None)
    if hid is None:
        own = getattr(hull, "own", None)
        hid = getattr(own, "id", "")
    return str(hid or "")


def _hull_of(root: Any, hid: Any) -> Any:
    from freesail.world.movement import hull_of

    return hull_of(root, str(hid or ""))


def _captain_of(hull: Any) -> Any:
    people = getattr(hull, "people", None)
    try:
        return people.captain if people is not None else None
    except Exception:  # noqa: BLE001
        return None


def _nation_adjective(world: Any, nation_id: str) -> str:
    nations = getattr(_root(world), "nations", None)
    try:
        n = nations.get(nation_id) if nations is not None else None
    except KeyError:
        n = None
    return str(getattr(n, "adjective", "") or nation_id)


# -- the player struck -----------------------------------------------------------------------------


def player_taken(
    world: Any, captor: Any, captor_hull: Any, prize_hull: Any, record: dict[str, Any]
) -> Any:
    """The player's person taken aboard the captor at the possession of his ship (§3.1):
    his station stood down, his prompt following him, his sword in the captor's captain's
    keeping, his parole not yet asked; the captor's captain's course for his doctrine's port
    (`prisoners_landed`). Returns the person, or None where the ship has no player's person
    (a model holds her captain's station; an observed world): her people are confined as
    any prize's."""
    from freesail.world import knowledge
    from freesail.world.movement import put_aboard
    from freesail.world.prizes import Prisoners, prisoners_of

    root = _root(world)
    tick = int(root.clock.tick)
    try:
        with root.as_hull(prize_hull):
            person = knowledge.players_person(root)
    except Exception:  # noqa: BLE001
        person = None
    if person is None or str(getattr(person, "hull", "") or "") != str(prize_hull.id):
        return None
    captain = _captain_of(captor_hull)
    # his sword, in the captor's captain's keeping (the period's gesture; a thing of 53b's)
    sword = _make_sword(root, person, captain, captor_hull)
    put_aboard(
        root,
        person,
        captor_hull,
        "cabin",
        seat="stands down",
        why="taken in the prize",
        by="the captor",
    )
    person.confined_to = "cabin"
    person.liberty = ()
    person.occupied_until = None
    person.occupied_with = ""
    person.pending = None
    held = prisoners_of(captor_hull.ship)
    if held is None:
        from freesail.crew.model import Crew

        held = Prisoners(
            crew=Crew(ship_name=str(prize_hull.ship.name), sailors=[]),
            nation=str(record.get("nation_was") or ""),
            since=tick,
        )
        captor_hull.ship.extra["prisoners"] = held
    held.parole[person.name] = "not asked"
    root.__dict__[CAPTIVE_KEY] = {
        "person": person.name,
        "id": person.id,
        "role": str(getattr(person, "role", "") or ""),
        "home": str(prize_hull.id),
        "captor": str(captor_hull.id),
        "since": tick,
        "sword": sword.id if sword is not None else "",
    }
    record["captive"] = person.name
    who = f"{person.name}, {_role_words(person)} the {prize_hull.ship.name},"
    keeping = f"; his sword is in {captain.name}'s keeping" if (sword and captain) else ""
    captor_hull.record(
        Severity.URGENT,
        "prize.captive",
        f"{who} is brought aboard a prisoner and put in the cabin, his parole not yet "
        f"asked{keeping}.",
        data={"person": person.name, "from": str(prize_hull.id), "sword": bool(sword)},
    )
    _course_for_port(root, captor, captor_hull, record)
    return person


def _role_words(person: Any) -> str:
    role = str(getattr(person, "role", "") or "")
    if role in ("captain", "commander", ""):
        return "lately commanding"
    return f"the {role} of"


def _make_sword(root: Any, person: Any, captain: Any, captor_hull: Any) -> Any:
    from freesail.world.things import Thing, _new_id, things_of

    things = things_of(root) if captain is not None else None
    if things is None:
        return None
    name = f"{person.name}'s sword"
    thing = Thing(_new_id(root, name), name, description="given up at the taking of his ship")
    thing.keeper = captain.id
    thing.keeper_home = str(getattr(captain, "home", "") or captor_hull.id)
    things.append(thing)
    return thing


def _course_for_port(root: Any, captor: Any, captor_hull: Any, record: dict[str, Any]) -> None:
    """The captor's captain's course for his doctrine's port with the prisoners
    (`prisoners_landed`: the first friendly port by the stance for a King's ship, home for
    a privateer), his intent set and said; nothing where a model holds his station."""
    from freesail.world.prizes import _doctrine, _port_for, _th

    agents = getattr(captor_hull, "agents", None) or {}
    held = agents.get("captain")
    if held is not None and not getattr(held.agent, "released", False):
        return  # a model at her captain's station does this by its own orders, or not
    doctrine = _doctrine(captor)
    rule = str(_th(doctrine, "prisoners_landed", "the first friendly port") or "")
    if rule.startswith("never") or rule.startswith("none"):
        return
    port = _port_for(root, captor, doctrine)
    if port is None:
        return
    record["captive_port"] = port.id
    cap = getattr(captor_hull, "captain", None)
    words = f"bound for {port.name}"
    if cap is not None:
        try:
            cap.set_intent(words)
        except ValueError:
            # the chart gives no way (a leg across the land from where she lies): he keeps
            # his intent and the port is the record's for the director's hand
            record["captive_port_unreached"] = port.id
            return
        cap.aside = False
        cap._business["prisoners_port"] = port.id
    brain = getattr(captor, "brain", None)
    if brain is not None:
        try:
            brain.set_intent(words)
        except ValueError:
            record["captive_port_unreached"] = port.id
            return
        brain.state = None
        brain.planned = False
    captor.intent_words = words
    captor_hull.record(
        Severity.NOTABLE,
        "captain.intent",
        f"The captain shapes his course for {port.name} with the prisoners: {words}.",
        data={"intent": words, "port": port.id, "why": "the prisoners landed"},
    )


# -- the words at the prompt -----------------------------------------------------------------------


def captive_words(world: Any, person: Any, here: Any, leaving: bool = False) -> str | None:
    """The refusal a captive's order of a deck meets (§3.1), or None when he is no captive:
    aboard the captor, her deck is not his; at the prompt of his own ship (a prize under a
    prize master), nothing of her deck is his from there; ashore, a prisoner of war. With
    `leaving`, the words for his going ashore or aboard another ship by his own order."""
    from freesail.world.movement import hull_name

    rec = captive_of(world)
    if rec is None or rec.get("person") != getattr(person, "name", None):
        if not is_captive(person):
            return None
    if not getattr(person, "aboard", True):
        port = _port_of(world, person)
        at = f" at {port.name}" if port is not None else ""
        return (
            f"You are a prisoner of war ashore{at}; no deck is yours from here. You may speak "
            "and read where you are."
        )
    his = _hull_of(_root(world), getattr(person, "hull", None))
    if here is not None and his is not None and str(here.id) != str(his.id):
        home = _hull_of(_root(world), getattr(person, "home", None))
        if home is not None and str(here.id) == str(home.id):
            return (
                f"The {hull_name(home)} is a prize under a prize master; nothing of her deck "
                f"is yours from the {hull_name(his)}, where you are held."
            )
        return (
            f"You are a prisoner aboard the {hull_name(his)}; no deck is yours from there, "
            "and least of all this one."
        )
    name = hull_name(his) if his is not None else "her"
    if leaving:
        return (
            f"You are a prisoner aboard the {name}; you leave her where her captain lands "
            "you, or by a cartel, and not at your own word. You may speak: 'say to the "
            "captain: ...', 'ask the ...', 'tell the ...'; and read what your place allows."
        )
    return (
        f"You are a prisoner aboard the {name}; her deck is not yours. You may speak: 'say "
        "to the captain: ...', 'ask the ...', 'tell the ...'; and read what your place "
        "allows."
    )


def _port_of(world: Any, person: Any) -> Any:
    ports = getattr(_root(world), "ports", None)
    table = getattr(ports, "ports", {}) or {}
    return table.get(str(getattr(person, "port", "") or ""))


def state_words(world: Any, person: Any) -> str:
    """'a prisoner on parole', 'a prisoner, his parole refused', 'a prisoner, his parole not
    asked', 'a prisoner of war' (ashore), for `where am I` and the station line."""
    if not getattr(person, "aboard", True):
        return "a prisoner of war"
    hull = _hull_of(_root(world), getattr(person, "hull", None))
    pris = _prisoners(hull)
    state = pris.parole.get(person.name, "") if pris is not None else ""
    if state == "given":
        return "a prisoner on parole"
    if state == "refused":
        return "a prisoner, his parole refused"
    if state in ("asked", "not asked"):
        return f"a prisoner, his parole {state}"
    return "a prisoner"


def _prisoners(hull: Any) -> Any:
    from freesail.world.prizes import prisoners_of

    ship = getattr(hull, "ship", None)
    return prisoners_of(ship) if ship is not None else None


# -- the parole ------------------------------------------------------------------------------------


def _parole_table(nation_id: str) -> dict[str, str]:
    from freesail.world.hail import _table

    table = _table().get("parole") or {}
    rows = table.get(nation_id) or table.get("default") or {}
    return {str(k): str(v) for k, v in rows.items()}


def _captives_aboard(hull: Any) -> list[Any]:
    """The prisoners of the hull who are persons (the officers taken into her), by the
    record: confined, aboard her, of another home."""
    people = getattr(hull, "people", None)
    if people is None:
        return []
    hid = _hull_id(hull)
    out = []
    for p in list(getattr(people, "everyone", None) or people.people):
        if getattr(p, "dead", False) or not getattr(p, "aboard", True):
            continue
        if str(getattr(p, "hull", "") or "") != hid:
            continue
        if getattr(p, "confined_to", "") or getattr(p, "liberty", ()):
            out.append(p)
    return out


def _hearers(hull: Any, place: str) -> list[Any]:
    from freesail.agents.agent import DIRECTOR, place_of
    from freesail.agents.harness import _stations_held
    from freesail.world.places import earshot

    near = earshot(place)
    return [
        h
        for h in _stations_held(hull)
        if h.station.name != DIRECTOR and place_of(hull, h.station.name) in near
    ]


def _said_by_captain(hull: Any, kind: str, speaker: Any, place: str, words: str, data: dict) -> str:
    """A line of the hull's log in the captain's name at the captive's place, heard by the
    stations within earshot in their next samples (as `say as` has it), in no sample's
    operator voice: the log's data."""
    from freesail.world.places import place_words

    who = speaker.name if speaker is not None else "The captain"
    line = f"{who}, {place_words(place)}: {words}"
    for h in _hearers(hull, place):
        h.hear(line)
    hull.record(
        Severity.NOTABLE,
        kind,
        line,
        data={"person": who, "place": place, "words": words} | data,
    )
    return line


def ask_parole(world: Any, hull: Any, person: Any, *, again: bool = False, by: str = "") -> str:
    """The captor's captain asks the captive his parole (§3.2), the period's words by his
    nation; the record `asked` with the tick."""
    root = _root(world)
    tick = int(root.clock.tick)
    pris = _prisoners(hull)
    if pris is None:
        return ""
    captain = _captain_of(hull)
    table = _parole_table(str(getattr(getattr(hull, "ship", None), "nation", "") or _nation(hull)))
    key = "ask_again" if again else "ask"
    words = (table.get(key) or table.get("ask") or "Will you give me your parole, sir?").format(
        name=person.name, captain=captain.name if captain else "the captain"
    )
    place = str(getattr(person, "where", "") or "cabin")
    line = _said_by_captain(
        hull,
        "prize.parole_asked",
        captain,
        place,
        words,
        {"asked": person.name, "again": again, "by": by or "the captain"},
    )
    pris.parole[person.name] = "asked"
    asked = hull.ship.extra.setdefault("parole_asked", {})
    times = list(asked.get(person.name) or [])
    times.append(tick)
    asked[person.name] = times
    return line


def _nation(hull: Any) -> str:
    vessel = getattr(hull, "vessel", None)
    return str(getattr(vessel, "nation", "") or "")


def answer_parole(world: Any, hull: Any, person: Any, given: bool, by: str) -> str:
    """The parole given or refused (§3.2): the record, his places, his sword returned when
    given; the line of the hull's log and the captor's captain's acknowledgement in the
    table's words."""
    root = _root(world)
    pris = _prisoners(hull)
    if pris is None:
        return ""
    captain = _captain_of(hull)
    table = _parole_table(_nation(hull))
    if given:
        pris.parole[person.name] = "given"
        person.liberty = PLACES_ON_PAROLE
        person.confined_to = "cabin"
        if str(getattr(person, "where", "")) not in PLACES_ON_PAROLE:
            person.where = "cabin"
        sword = _sword_of(root, person)
        returned = ""
        if sword is not None:
            sword.keeper = person.id
            sword.keeper_home = str(getattr(person, "home", "") or "")
            returned = "; his sword is returned him"
        text = (
            f"{person.name} gives his parole ({by}): the cabin and the gunroom are his, and "
            f"the quarterdeck by day{returned}."
        )
        ack = table.get("taken") or "Your word is enough, sir; the cabin is yours."
    else:
        pris.parole[person.name] = "refused"
        person.liberty = PLACES_REFUSED
        person.confined_to = "gunroom"
        person.where = "gunroom"
        text = (
            f"{person.name} refuses his parole ({by}): the gunroom alone is his, a sentry at "
            "the door."
        )
        ack = table.get("refused") or "As you please, sir; the sentry has his orders."
    hull.record(
        Severity.URGENT,
        "prize.parole",
        text,
        data={"person": person.name, "given": given, "by": by},
    )
    if captain is not None and by != "the captain's word":
        _said_by_captain(
            hull,
            "prize.parole_answered",
            captain,
            str(getattr(person, "where", "") or "cabin"),
            ack.format(name=person.name, captain=captain.name),
            {"answered": person.name, "given": given},
        )
    return text


def _sword_of(root: Any, person: Any) -> Any:
    rec = captive_of(root)
    from freesail.world.things import things_of

    sid = str(rec.get("sword") or "") if rec is not None else ""
    things = things_of(root) or []
    for t in things:
        if sid and t.id == sid:
            return t
    for t in things:
        if t.name == f"{person.name}'s sword":
            return t
    return None


def hear_parole(world: Any, hull: Any, person: Any, words: str) -> bool:
    """The captive's words read for his parole, only while one is asked of him and not yet
    answered (§3.2); True when they were read (given or refused), False when they were not
    (the question stays open)."""
    pris = _prisoners(hull)
    if pris is None or pris.parole.get(person.name) != "asked":
        return False
    low = " ".join(str(words).lower().replace("'", "").split())
    if any(w in low for w in PAROLE_REFUSED_WORDS):
        answer_parole(world, hull, person, False, "in his own words")
        return True
    if any(w in low for w in PAROLE_GIVEN_WORDS):
        answer_parole(world, hull, person, True, "in his own words")
        return True
    yes, no = _whole_words(low, PAROLE_YES_WORDS), _whole_words(low, PAROLE_NO_WORDS)
    if yes != no:
        answer_parole(world, hull, person, yes, "in his own words")
        return True
    return False


def _whole_words(low: str, forms: tuple[str, ...]) -> bool:
    """Whether any of the forms stands in the words as whole words ('no', not 'not')."""
    return any(re.search(rf"(?<!\w){re.escape(f)}(?!\w)", low) for f in forms)


def set_parole(world: Any, hull: Any, name: str, given: bool, by: str) -> str:
    """The director's `aboard the <captor>: the parole of <name> given | refused` (§3.2):
    for a captive aboard her; refused in words for a person who is no prisoner of hers."""
    from freesail.world.orders import WorldOrderError

    for p in _captives_aboard(hull):
        if p.name.lower() == name.lower() or p.name.lower().endswith(" " + name.lower()):
            return answer_parole(world, hull, p, given, by)
    raise WorldOrderError(
        f"{name} is no prisoner aboard the {hull.ship.name}; a parole is a captive's to give "
        "or refuse."
    )


def read_parole_form(body: str) -> tuple[str, bool] | None:
    """(the name, given) from `the parole of Captain Bowen given | refused`, or None."""
    m = _PAROLE_FORM.match(" ".join(str(body).split()))
    if m is None:
        return None
    return m.group("name").strip().strip('"'), m.group("what").lower() != "refused"


def _parole_minute(hull: Any, tick: int) -> None:
    """The captor's rules captain by doctrine: the parole asked a minute after the taking,
    asked again after a glass, given by rule after a watch (an officer's); nothing where a
    model holds her captain's station (it asks in its own words, or not at all)."""
    from freesail.world.prizes import _doctrine, _th

    pris = _prisoners(hull)
    if pris is None or not pris.parole:
        return
    agents = getattr(hull, "agents", None) or {}
    held = agents.get("captain")
    model_holds = held is not None and not getattr(held.agent, "released", False)
    vessel = getattr(hull, "vessel", None)
    accepted = bool(_th(_doctrine(vessel), "parole_accepted", True)) if vessel is not None else True
    asked = hull.ship.extra.setdefault("parole_asked", {})
    for p in _captives_aboard(hull):
        state = pris.parole.get(p.name)
        if state is None:
            continue
        if state == "not asked":
            since = int(pris.since)
            if model_holds or not accepted:
                continue
            if tick - since >= PAROLE_FIRST_ASK_S:
                ask_parole(hull.world, hull, p, by="the captain, by his doctrine")
            continue
        if state == "asked":
            times = list(asked.get(p.name) or [since_default(pris)])
            first, last = times[0], times[-1]
            if tick - first >= PAROLE_BY_RULE_S:
                answer_parole(
                    hull.world,
                    hull,
                    p,
                    True,
                    "the captain's word: an officer's parole by the custom",
                )
            elif len(times) == 1 and tick - last >= PAROLE_ASK_AGAIN_S and not model_holds:
                ask_parole(hull.world, hull, p, again=True, by="the captain, once more")


def since_default(pris: Any) -> int:
    return int(getattr(pris, "since", 0) or 0)


# -- the prisoners landed --------------------------------------------------------------------------


def land_prisoners(world: Any, hull: Any, port: Any) -> str:
    """In port (§3.3): the prisoners of the hull landed to the port's agent for prisoners,
    the captive persons ashore at that place, the record cleared; the line."""
    from freesail.world.places import agent_for_prisoners_words
    from freesail.world.prizes import prisoners_of

    root = _root(world)
    tick = int(root.clock.tick)
    pris = prisoners_of(hull.ship)
    n = pris.count if pris is not None else 0
    names = []
    for p in _captives_aboard(hull):
        p.aboard = False
        p.where = "shore"
        p.port = port.id
        p.ashore_at = "agent_for_prisoners"
        p.confined_to = ""
        p.liberty = ()
        p.occupied_until = None
        p.occupied_with = ""
        names.append(p.name)
        rec = captive_of(root)
        if rec is not None and rec.get("person") == p.name:
            rec["ashore"] = port.id
            rec["landed_at"] = tick
    if pris is not None:
        pris.landed = int(getattr(pris, "landed", 0) or 0) + n
        pris.crew.sailors = []
        pris.crew.reindex()
        pris.parole = {}
    hull.ship.extra.pop("parole_asked", None)
    agent = agent_for_prisoners_words(port)
    who = ""
    if names:
        who = f"; {', '.join(names)} ashore there, prisoners of war"
    text = (
        f"The prisoners, {number_words(n)}, are landed at {port.name} to {agent} with the "
        f"list of their names and the day they were first victualled{who}."
    )
    hull.record(
        Severity.URGENT,
        "prize.prisoners_landed",
        text,
        data={"port": port.id, "count": n, "persons": names},
    )
    return text


# -- the minute ------------------------------------------------------------------------------------


def minute(hull: Any) -> None:
    """The captor's minute (awake): the parole by the rules captain's doctrine, and the
    prisoners landed when she lies in port."""
    ship = getattr(hull, "ship", None)
    pris = _prisoners(hull) if ship is not None else None
    if pris is None:
        return
    root = _root(hull.world)
    tick = int(root.clock.tick)
    if pris.parole:
        _parole_minute(hull, tick)
    if pris.count == 0 and not _captives_aboard(hull):
        return
    dealings = getattr(hull, "dealings", None)
    port = dealings.in_port() if dealings is not None else None
    if port is not None:
        land_prisoners(root, hull, port)


# -- the cartel ------------------------------------------------------------------------------------


def put_cartel(world: Any, port: Any, who: list[Any], holder: Any, said_for: str) -> Any:
    """A cartel put on the sea at the port's road under a flag of truce (§3.4), bound for the
    hull that holds the persons; her record on the vessel (`cartel`: the persons' names,
    the holder's id, her port)."""
    from freesail.world.ships import vessel_from_spec
    from freesail.world.signals import set_colours, vessel_locker

    root = _root(world)
    sea = root.vessels
    sea.serial += 1
    spot = port.outer_road.position
    spec = {
        "description": CARTEL_DESCRIPTION,
        "name": f"the cartel from {port.name}",
        "nation": str(getattr(port, "nation", "") or ""),
        "position": {"lat_deg": spot.lat_deg, "lon_deg": spot.lon_deg},
        "goal": f"bound for {port.name}",
        "colours": "shown",
    }
    v = vessel_from_spec(root, spec, sea.serial)
    v.role = CARTEL_ROLE
    v.what = "a cartel"  # what the glass makes out of her, under her flag of truce
    v.cartel = {
        "port": port.id,
        "holder": str(holder.id),
        "persons": [p.name for p in who],
        "for": said_for,
        "taken_off": False,
    }
    sea.add(v)
    tick = int(root.clock.tick)
    set_colours(vessel_locker(v).colours, getattr(root, "nations", None), "truce", v.nation, tick)
    return v


def cartel_minute(world: Any) -> list[tuple[Any, ...]]:
    """Every cartel's minute: she steers for the hull that holds her persons; within hail she
    takes them off by the boat (82's road) and shapes her course for her port; at her port's
    road they are landed free and she is done."""
    root = _root(world)
    sea = getattr(root, "vessels", None)
    lines: list[tuple[Any, ...]] = []
    if sea is None:
        return lines
    for v in list(sea.vessels):
        rec = getattr(v, "cartel", None)
        if not rec or rec.get("landed_at"):
            continue
        v.done = False  # her errand goes on whatever her own plan's end said of her
        if not rec.get("taken_off"):
            holder = _hull_of(root, rec["holder"])
            target = getattr(holder, "vessel", None) if holder is not None else None
            if holder is None or target is None or target.position is None:
                continue
            from freesail.world.geo import bearing_and_distance

            _, d = bearing_and_distance(v.position, target.position)
            if d <= CARTEL_HAIL_M:
                _cartel_takes_off(root, v, holder, rec, lines)
            else:
                v.plan = [("to", target.position, f"the {holder.ship.name}")]
            continue
        port = (getattr(root.ports, "ports", {}) or {}).get(rec["port"])
        if port is None:
            continue
        from freesail.world.geo import bearing_and_distance

        _, d = bearing_and_distance(v.position, port.outer_road.position)
        if d <= 2.0 * units.NAUTICAL_MILE:
            _cartel_lands(root, v, port, rec, lines)
    return lines


def _cartel_takes_off(root: Any, v: Any, holder: Any, rec: dict[str, Any], lines: list) -> None:

    tick = int(root.clock.tick)
    taken = []
    for name in rec["persons"]:
        p = holder.people.find_aboard(name) if hasattr(holder.people, "find_aboard") else None
        if p is None:
            p = next((q for q in _captives_aboard(holder) if q.name == name), None)
        if p is None:
            continue
        p.confined_to = ""
        p.liberty = ()
        # the cartel is a hull of the sea only when she is made one; her persons are kept
        # on her record and ashore at her port when she arrives (80's words fill her out)
        p.aboard = False
        p.where = "cartel"
        p.cartel = v.id
        taken.append(p.name)
        c = captive_of(root)
        if c is not None and c.get("person") == name:
            c["cartel"] = v.id
    pris = _prisoners(holder)
    if pris is not None:
        for name in taken:
            pris.parole.pop(name, None)
    rec["taken_off"] = True
    rec["taken_at"] = tick
    port = (getattr(root.ports, "ports", {}) or {}).get(rec["port"])
    v.plan = [("to", port.outer_road.position, port.name)] if port is not None else []
    v.done = False  # her errand goes on whatever her own goal's arrival said
    text = (
        f"{v.name[:1].upper()}{v.name[1:]}, under a flag of truce, takes off "
        f"{', '.join(taken) or 'nobody'} by the boat and shapes her course for "
        f"{port.name if port else 'her port'}."
    )
    holder.record(
        Severity.URGENT,
        "prize.cartel",
        text,
        data={"cartel": v.id, "persons": taken, "port": rec["port"]},
    )
    if port is not None:
        from freesail.world.geo import bearing_and_distance

        _, d = bearing_and_distance(v.position, port.outer_road.position)
        if d <= 2.0 * units.NAUTICAL_MILE:
            # she lies in her port's road already: landed at once (a vessel done is gone
            # from the sea at the minute's end)
            _cartel_lands(root, v, port, rec, lines)


def _cartel_lands(root: Any, v: Any, port: Any, rec: dict[str, Any], lines: list) -> None:
    tick = int(root.clock.tick)
    registry = getattr(root, "registry", None)
    names = []
    for hid in list(getattr(registry, "hulls", []) or []):
        for p in registry.company(hid):
            if getattr(p, "cartel", "") == v.id:
                p.cartel = ""
                p.where = "shore"
                p.port = port.id
                p.ashore_at = "quay"
                p.aboard = False
                names.append(p.name)
                c = captive_of(root)
                if c is not None and c.get("person") == p.name:
                    root.__dict__.pop(CAPTIVE_KEY, None)
    rec["landed_at"] = tick
    v.done = True
    text = (
        f"{v.name[:1].upper()}{v.name[1:]} comes into {port.name} and lands "
        f"{', '.join(names) or 'her people'} free; the exchange is her business ashore."
    )
    holder = _hull_of(root, rec.get("holder"))
    if holder is not None:
        holder.record(
            Severity.URGENT,
            "prize.cartel_landed",
            text,
            data={"cartel": v.id, "persons": names, "port": port.id},
        )
    else:
        lines.append(
            (Severity.URGENT, "prize.cartel_landed", text, {"cartel": v.id, "persons": names})
        )


def cartel_doubt(world: Any, port: Any) -> str | None:
    """The form doubted beyond a day's sail of the port (§3.4)."""
    root = _root(world)
    here = getattr(root.players, "position", None) if hasattr(root, "players") else None
    if here is None or port is None:
        return None
    from freesail.world.geo import bearing_and_distance

    _, d = bearing_and_distance(here, port.outer_road.position)
    nm = d / units.NAUTICAL_MILE
    if nm > CARTEL_DAY_NM:
        return (
            f"{port.name} lies {nm:.0f} miles off, beyond a day's sail: a cartel from there "
            f"is a day or more away"
        )
    return None
