"""The place's knowledge (package 65; spec M7b §14 "as built"; the owner's ruling of
2026-10-19: a place carries at least what can reasonably be perceived from it, by action
and by what is there; decision 59: the player reads by his place as a model does, with the
scenario key `knowledge: all` for testing; `docs/design/Design-PlaceKnowledge.md`).

**A sample carries what the person's place allows.** The harness keeps the rule, not the
model. Three ideas, each a function here, read the world and change nothing:

- **A person's senses** (`senses_of`, `station_senses`): where he is (66's spot,
  `hearing.spot_of`: aboard a hull at a place, ashore at a port's place, in a boat) and
  whether he is asleep, read as the set of **senses** he has there: the open deck's
  (`DECK`: the quarterdeck, the waist and the galley open to it), the masthead's (`ALOFT`),
  the cabin's, the gunroom's, a room's below (the hold, the magazine, the sail room, the sick
  berth, the cockpit), the shore's (`ASHORE`), and `ABOARD` for whatever every man in the
  hull has (the bell, the heel, the motion). A sleeper has `ASLEEP` alone: he perceives
  nothing but what wakes him. The director, and everyone under `knowledge: all`, has `ALL`.
- **Where a line is heard** (`reaches`, `reach_of`): every kind of log line carries a
  reach, one of a few classes (`REACH`), keyed by the kind or by its family with **the deck
  as the default** for a kind nobody placed, so that a new kind is the ship's business, heard
  on deck and nowhere else, and never leaks below or ashore by accident; a line's data is
  read first where it names its place (`place`), its hearers (`heard_by`) or the person it
  is for (`to`). The words (66's kinds) keep 66's rule, which the harness applies
  (`Harness._reaches`). The cabin, under the quarterdeck, hears the sail work overhead as a
  sound and not a figure (`as_heard`: the lead's ruling of 2026-10-31).
- **Where a reading is to be had** (`reading_here`, `elsewhere_words`): every row of the
  readings registry carries its places (`Reading.where`, the deck by default) and the words
  for where it is ("the lead is cast on deck"); a row is his when any of its places is among
  his senses, and the rest are said in one line.

Nothing here writes a line or moves a person. The tables are data; `tests/test_knowledge.py`
walks every kind the code writes against `REACH` and `FAMILIES`, so that a kind an author
forgot to place fails the suite instead of leaking.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from freesail.world.places import PLACES, earshot, place_words

__all__ = [
    "ABOARD",
    "ALL",
    "ALOFT",
    "ASHORE",
    "ASLEEP",
    "CABIN",
    "DECK",
    "DEFAULT_REACH",
    "FAMILIES",
    "GUNROOM",
    "NOT_KINDS",
    "REACH",
    "ROOMS",
    "Senses",
    "WAKES",
    "all_known",
    "as_heard",
    "elsewhere_words",
    "is_asleep",
    "reach_of",
    "reaches",
    "reading_here",
    "senses_of",
    "senses_of_place",
    "station_senses",
    "where_words",
]

# -- the senses -------------------------------------------------------------------------

DECK = "deck"  # the open deck: the quarterdeck, the waist and the forecastle, the galley
ALOFT = "aloft"  # the tops and the masthead
CABIN = "cabin"
GUNROOM = "gunroom"
ABOARD = "aboard"  # what every man awake in the hull has
ASHORE = "ashore"
ASLEEP = "asleep"
ALL = "all"  # the director's, and everyone's under `knowledge: all`
# the rooms below with their own knowledge (each its own sense, by the place's id)
ROOMS: frozenset[str] = frozenset({"hold", "magazine", "sail_room", "sick_berth", "cockpit"})

# The places open to one another on the upper deck, which share the deck's senses (52's
# earshot: the galley is under the forecastle, open to the waist).
_OPEN_DECK = frozenset({"quarterdeck", "deck", "galley"})
_ALOFT = frozenset({"tops", "masthead"})


def senses_of_place(place_id: str) -> frozenset[str]:
    """The senses a man awake has at a place aboard, by the place's id (`places.PLACES`,
    and 'masthead' for the lookout's station): the open deck's, the masthead's, the
    cabin's, the gunroom's, a room's below; 'shore' the shore's; a place not known, the
    deck's (judgement: a place nobody placed is on deck, where everything is seen)."""
    p = str(place_id or "")
    if p in _OPEN_DECK or p == "":
        return frozenset({ABOARD, DECK})
    if p in _ALOFT:
        return frozenset({ABOARD, ALOFT})
    if p == "cabin":
        return frozenset({ABOARD, CABIN})
    if p == "gunroom":
        return frozenset({ABOARD, GUNROOM})
    if p in ROOMS:
        return frozenset({ABOARD, p})
    if p == "shore":
        return frozenset({ASHORE})
    if p in ("boat", "cutter"):
        # the script's boat and the pilot's cutter (a person off the ship, in no hull of
        # his own: 82's boat is a hull and reads as a deck)
        return frozenset({"boat"})
    return frozenset({ABOARD, DECK})


@dataclass(frozen=True)
class Senses:
    """What a person perceives where he is: the set of his senses (`tokens`), his spot as
    66 has it (`spot`: ("aboard", hull, place), ("ashore", port, place), ("boat", hull)),
    his place's id aboard (`place`, "" elsewhere), the person himself (None for a station
    bound to nobody) and whether he is asleep."""

    tokens: frozenset[str]
    spot: tuple[str, ...] = ()
    place: str = ""
    person: Any = None
    asleep: bool = False

    @property
    def everything(self) -> bool:
        return ALL in self.tokens

    def has(self, token: str) -> bool:
        return self.everything or token in self.tokens

    def words(self) -> str:
        """Where he is, for a sentence: 'in the cabin', 'ashore', 'asleep'."""
        if self.asleep:
            return "asleep"
        if self.spot and self.spot[0] == "ashore":
            return "ashore"
        if self.place:
            return place_words(self.place)
        return "aboard"


EVERYTHING = Senses(frozenset({ALL}))


def all_known(world: Any) -> bool:
    """Whether the scenario turns the rule off (`knowledge: all`, decision 59: for testing):
    read from the root World's scenario, so that every hull of the game reads alike; a
    checkpoint from before the key has the rule on."""
    root = getattr(world, "parent", None) or world
    sc = getattr(root, "scenario", None)
    return str(getattr(sc, "knowledge", "place") or "place") == "all"


def is_asleep(world: Any, person: Any) -> bool:
    """Whether a person is asleep: by his needs (`needs.asleep`: turned in below, or
    fallen asleep where he stood) or by the bill (a watch-keeper in his watch below at
    night, `People._asleep`)."""
    if person is None:
        return False
    needs = getattr(person, "needs", None)
    if needs is not None and getattr(needs, "asleep", ""):
        return True
    people = getattr(world, "people", None)
    try:
        return bool(people is not None and people._asleep(person))
    except Exception:  # noqa: BLE001  (a world whose people cannot be read)
        return False


def senses_of(world: Any, person: Any) -> Senses:
    """A person's senses where he is now; `EVERYTHING` for nobody, and under
    `knowledge: all`."""
    if person is None or all_known(world):
        return EVERYTHING
    from freesail.world.hearing import spot_of

    spot = spot_of(world, person)
    if is_asleep(world, person):
        place = spot[2] if spot and spot[0] == "aboard" and len(spot) == 3 else ""
        return Senses(frozenset({ASLEEP}), spot, place, person, asleep=True)
    if spot and spot[0] == "aboard" and len(spot) == 3:
        place = str(spot[2])
        return Senses(senses_of_place(place), spot, place, person)
    if spot and spot[0] == "ashore":
        return Senses(frozenset({ASHORE}), spot, "", person)
    return Senses(frozenset({"boat"}), spot, "", person)


def station_senses(world: Any, station: str, person: Any = None) -> Senses:
    """A station's senses: its person's, else its own place aboard (the lookout's masthead,
    `agent.place_of`); the director's everything."""
    from freesail.agents.agent import DIRECTOR, place_of

    if station == DIRECTOR or all_known(world):
        return EVERYTHING
    if person is not None:
        return senses_of(world, person)
    place = place_of(world, station)
    if place == "shore":
        return Senses(frozenset({ASHORE}), ("ashore", "", ""), "")
    place = "quarterdeck" if place == "deck" else place
    from freesail.world.hearing import own_hull

    return Senses(senses_of_place(place), ("aboard", own_hull(world), place), place)


# -- where a line is heard ----------------------------------------------------------------

# The reach classes (the design's §4):
#   aboard   every person awake in the hull (the bell, the pipes, the drum, a gun, the ship
#            striking, a spar gone, the pumps: felt or heard through a wooden ship)
#   wakes    the subset of `aboard` that wakes a sleeper too
#   deck     the open deck and aloft (THE DEFAULT: the ship's business, seen on her deck)
#   aft      the deck, aloft and the cabin under the quarterdeck (the sounds of sail work)
#   said     a word: 66's hearing, which the harness applies
#   person   the person the line is for (`to`), wherever he is aboard, else the captain
#   place    within earshot of the place the line's data names, and the deck
#   port     the persons ashore at the port the line names, and the deck of a hull there
#   record   the record's and the driver's lines, which reach whoever the record reaches
REACH: dict[str, str] = {
    "clock.bell": "aboard",
    "watch.relieved": "aboard",
    "watch.deck_passed": "deck",
    "crew.all_hands": "wakes",
    "crew.all_hands_up": "aboard",
    "crew.piped_down": "aboard",
    "crew.idlers_up": "aboard",
    "crew.idlers_down": "aboard",
    "crew.watch_turned_up": "aboard",
    "crew.quarters": "wakes",
    "crew.buried": "deck",
    "quarters.beat": "wakes",
    "quarters.robbed": "aboard",
    "ship.aground": "wakes",
    "ship.afloat": "aboard",
    "ship.aback": "aboard",
    "ship.beam_ends": "wakes",
    "ship.foundered": "wakes",
    "ship.settling": "aboard",
    "ship.leak": "aboard",
    "ship.anchored": "aboard",
    "ship.brought_up": "aboard",
    "ship.grappled": "wakes",
    "ship.grapnels_short": "deck",
    "ship.missed_stays": "aboard",
    "ship.tacked": "aboard",
    "ship.wore": "aboard",
    "ship.hove_to": "aboard",
    "ship.filled_away": "aboard",
    "ship.command_passes": "aboard",
    "ground.kedge_home": "deck",
    "ground.master": "deck",
    "spar.carried_away": "wakes",
    "spar.fished": "aboard",
    "mast.jury": "aboard",
    "sail.blown_out": "aboard",
    "line.parted": "aboard",
    "cable.parted": "wakes",
    "gun.dismounted": "aboard",
    "pumps.gaining": "aboard",
    "pumps.losing": "aboard",
    "pumps.manned": "aboard",
    "pumps.secured": "aboard",
    "pumps.spelled": "aboard",
    "pumps.sucked": "aboard",
    "well.rising": "aboard",
    "well.sounded": "aboard",
    "leak.stopped": "aboard",
    "leak.fothered": "aboard",
    "leak.fother_gone": "aboard",
    "hole.plugged": "aboard",
    "hatches.battened": "aboard",
    "motion.change": "aboard",
    "sea.change": "aboard",
    "health.died": "aboard",
    "health.morning_report": "person",
    "health.sick": "place",
    "health.returned": "place",
    "health.invalided": "deck",
    "message.aboard": "deck",
    "message.door": "person",
    "message.received": "person",
    "message.by": "person",
    "message.at": "port",
    "person.sent_for": "person",
    "person.moved": "place",
    "person.came": "place",
    "person.free": "place",
    "person.collapsed": "place",
    "person.hurt": "place",
    "person.killed": "aboard",
    "person.ashore": "port",
    "person.aboard": "place",
    "person.waterman": "port",
    "captain.below": "place",
    "captain.on_deck": "place",
    "aboard.found": "place",
    "aboard.thing": "place",
    "aboard.freight": "place",
    "aboard.debt": "person",
    "aboard.paid_in": "person",
    "aboard.paid_out": "person",
    "paper.written": "place",
    "stores.allowance": "aboard",
    "stores.out": "aboard",
    "hold.freighted": "place",
    "thing.landed": "port",
    "boat.at_quay": "port",
    "market.bargain": "port",
    "market.bought": "port",
    "market.prices": "port",
    "port.news": "port",
    "port.rumour": "port",
    "query.slate": "person",
    "query.journal": "record",
    "query.director_brief": "record",
    "query.director_log": "record",
    "query.director_word": "record",
    "query.two_stories": "record",
    "query.seat_refused": "record",
    "director.answer": "record",
    "director.answered": "record",
    "director.player": "record",
    "needs.answer": "person",
    "needs.felt": "person",
    "log.rollup": "record",
    "log.read": "record",
    # the report, the call and the boat's report (step 3 writes them; placed first)
    "report.made": "person",
    "report.called": "wakes",
    "report.boat": "port",
}

# ...and by family, for every kind of a family not named above.
FAMILIES: dict[str, str] = {
    "clock": "aboard",
    "guns": "wakes",
    "action": "wakes",
    "small_arms": "wakes",
    "marines": "aboard",
    "evolution": "aft",
    "sail": "aft",
    "sails": "aft",
    "yard": "aft",
    "agent": "said",
    "person": "said",
    "free": "said",
    "query": "said",
    "driver": "record",
    "world": "record",
    "director": "record",
    "hull": "record",
    "seat": "record",
    "station": "record",
    "report": "person",
    "message": "person",
    "needs": "person",
    "aboard": "place",
    "market": "port",
    "thing": "place",
    # the deck's, named so that the test knows each family was placed on purpose
    "anchor": "deck",
    "bearing": "deck",
    "boat": "deck",
    "book": "deck",
    "cable": "deck",
    "captain": "deck",
    "chronometer": "deck",
    "colours": "deck",
    "crew": "deck",
    "fishing": "deck",
    "fog": "deck",
    "ground": "deck",
    "gun": "deck",
    "hail": "deck",
    "hatches": "deck",
    "health": "deck",
    "helm": "deck",
    "hold": "deck",
    "hole": "deck",
    "lead": "deck",
    "leak": "deck",
    "lights": "deck",
    "line": "deck",
    "log": "deck",
    "lookout": "deck",
    "lunar": "deck",
    "lying_to": "deck",
    "mast": "deck",
    "master": "deck",
    "motion": "deck",
    "navigation": "deck",
    "order": "deck",
    "ordnance": "deck",
    "paper": "deck",
    "pilot": "deck",
    "plan": "deck",
    "port": "deck",
    "practice": "deck",
    "pumps": "deck",
    "purse": "deck",
    "quarters": "deck",
    "ration": "deck",
    "reckoning": "deck",
    "regime": "deck",
    "rigging": "deck",
    "sea": "deck",
    "ship": "deck",
    "signal": "deck",
    "spar": "deck",
    "speed": "deck",
    "squadron": "deck",
    "standing": "deck",
    "stores": "deck",
    "strain": "deck",
    "sun": "deck",
    "watch": "deck",
    "weather": "deck",
    "well": "deck",
    "wind": "deck",
    "work": "deck",
}
DEFAULT_REACH = "deck"

# The dotted string families in the code that are no log kind (the test's exclusions: a
# file's name, a sail's or a part's id, a ship file's section, a settings key).
NOT_KINDS: frozenset[str] = frozenset(
    {
        "fore",
        "main",
        "mizzen",
        "form",
        "trim",
        "orders",
        "sails",
        "names",
        "nations",
        "constituents",
        "streams",
        "establishments",
        "climatology",
        "regimes",
        "ration",
        "manifest",
        "papers",
        "scenario",
        "settings",
        "starter",
        "numerary",
        "night_fog",
        "convoy",
        "cruiser",
        "fish",
        "harbour",
        "index",
        "claude_desktop_config",
        "sail_classes",
        "vocabulary",
        "business",
        "freesail",  # a module's dotted name
    }
)

# The kinds that wake a sleeper (the `wakes` class: the design's §3.1), beside a word or a
# question to him, which the harness reads.
WAKES: frozenset[str] = frozenset(k for k, c in REACH.items() if c == "wakes") | frozenset(
    {"guns", "action", "small_arms"}
)


def reach_of(kind: str) -> str:
    """The reach class of a kind: by the kind, by its family, else the default (the deck)."""
    k = str(kind or "")
    found = REACH.get(k)
    if found is not None:
        return found
    return FAMILIES.get(k.split(".", 1)[0], DEFAULT_REACH)


def _wakes(kind: str) -> bool:
    return reach_of(kind) == "wakes"


def _names(data: dict[str, Any], key: str) -> str:
    v = data.get(key)
    if isinstance(v, dict):
        v = v.get("name")
    return str(v or "")


def _is_captain(world: Any, person: Any) -> bool:
    people = getattr(world, "people", None)
    try:
        return people is not None and people.captain is person
    except Exception:  # noqa: BLE001
        return False


def reaches(world: Any, senses: Senses, e: Any) -> bool:
    """Whether a line of the log reaches a person with these senses (the design's §4),
    for every kind but the words (66's kinds, whose hearing the harness applies). A line
    whose data names a place is read by it first; the deck's lines reach the open deck and
    aloft; `aboard` every man awake in the hull; `wakes` a sleeper too; `person` the person
    it is for, else the captain; `port` the persons ashore at that port and the deck;
    `record` everyone."""
    if senses.everything:
        return True
    kind = str(getattr(e, "kind", "") or "")
    cls = reach_of(kind)
    data = getattr(e, "data", None) or {}
    if senses.asleep:
        # a sleeper perceives nothing but what wakes him (the brief's list: the call, all
        # hands, a gun, the ship striking, and nothing else; 54 and 66 let a word or a
        # question to him wake him, which the harness reads)
        if cls == "wakes":
            return True
        if cls == "person":
            return _for_me(world, senses, data, default_captain=False)
        return False
    if cls == "record":
        return True
    tokens = senses.tokens
    aboard = ABOARD in tokens
    on_deck = DECK in tokens or ALOFT in tokens
    if cls in ("aboard", "wakes"):
        return aboard
    if cls == "aft":
        return on_deck or CABIN in tokens
    if cls == "person":
        if _for_me(world, senses, data, default_captain=True):
            return True
        # else where it was delivered: the messenger at the cabin door is seen by whoever is
        # in the cabin, a letter brought to the captain on deck by the deck
        where = str(data.get("place") or "")
        if where in PLACES and PLACES[where].aboard:
            return aboard and senses.place in earshot(where)
        return on_deck
    if cls == "place":
        where = str(data.get("place") or "")
        if where in PLACES and PLACES[where].aboard:
            if aboard and senses.place in earshot(where):
                return True
            return on_deck  # a man seen going below, or coming up, from the deck
        if where in ("shore", "quay") or data.get("port"):
            return _at_the_port(senses, data) or on_deck
        return on_deck
    if cls == "port":
        return _at_the_port(senses, data) or on_deck
    if cls == "said":
        # a word not of 66's kinds (`agent.*` about a station, a query at the prompt): heard
        # where it was said, by its data's place, else on deck
        where = str(data.get("place") or "")
        if where in ("shore",):
            return _at_the_port(senses, data)
        if where and where in PLACES:
            return aboard and senses.place in earshot(where)
        if where == "masthead":
            return on_deck
        return on_deck
    return on_deck  # the deck, the default


def _for_me(world: Any, senses: Senses, data: dict[str, Any], default_captain: bool) -> bool:
    """A line for a person: his when it names him (`to`, `person`), or, naming nobody, the
    captain's when `default_captain` (a report is made to the captain)."""
    person = senses.person
    if person is None:
        return False
    name = str(getattr(person, "name", "") or "")
    to = _names(data, "to") or _names(data, "person")
    if to:
        key = to.lower()
        if name and (key == name.lower() or key.endswith(name.split()[-1].lower())):
            return True
        if key in ("captain", "the captain") and _is_captain(world, person):
            return True
        return False
    return bool(default_captain and _is_captain(world, person))


def _at_the_port(senses: Senses, data: dict[str, Any]) -> bool:
    """Whether a person ashore is at the port a line names (any place of it for the quay's
    lines: the boat coming in is the quay's talk within the hour; judgement)."""
    spot = senses.spot
    if not spot or spot[0] != "ashore":
        return False
    port = str(data.get("port") or "")
    return not port or port == str(spot[1])


# What the cabin hears of the sail work overhead (the lead's ruling of 2026-10-31): the
# sound and not the figure, the kind kept so that the roll-up and the stand-by count the
# line. Which sail, and whether set or taken in, is not his until told or until he comes up.
_HEARD_SAIL: dict[str, str] = {
    "sail.filled": "Sail filled again.",
    "sail.fills": "Sail filled again.",
    "sail.drawing": "Sail drawing again.",
    "sail.backed": "Sail aback overhead.",
    "sail.shivering": "Sail shaking overhead.",
    "sail.shivers": "Sail shaking overhead.",
}


def as_heard(e: Any, senses: Senses) -> str | None:
    """The text a person below hears of a deck line, or None where the line passes as
    written: in the cabin the sail and yard lines are sounds ("Sail handled overhead.",
    "The hands at the braces."), an evolution's lines as written (any seaman below knows a
    tack from a wear by the feel); a line whose data names no sail or yard passes as
    written. Everywhere else, None."""
    if senses.everything or CABIN not in senses.tokens or DECK in senses.tokens:
        return None
    kind = str(getattr(e, "kind", "") or "")
    family = kind.split(".", 1)[0]
    if family not in ("sail", "sails", "yard"):
        return None
    data = getattr(e, "data", None) or {}
    named = bool(getattr(e, "subject", None)) or any(
        k in data for k in ("sail", "sails", "sail_id", "id", "yard", "yards", "part", "subject")
    )
    if not named and family != "yard":
        return None
    if family == "yard":
        return "The hands at the braces."
    return _HEARD_SAIL.get(kind, "Sail handled overhead.")


# -- where a reading is to be had ----------------------------------------------------------

_PLACE_NAMES: dict[str, str] = {
    DECK: "on deck",
    ALOFT: "aloft",
    CABIN: "in the cabin",
    GUNROOM: "in the gunroom",
    "hold": "in the hold",
    "magazine": "in the magazine",
    "sail_room": "in the sail room",
    "sick_berth": "in the sick berth",
    "cockpit": "in the cockpit",
    ASHORE: "ashore",
    ABOARD: "anywhere aboard",
    "boat": "in the boat",
}


def reading_here(row: Any, senses: Senses) -> bool:
    """Whether a row is to be had by these senses: any of its places among them; a row the
    whole hull has (`aboard`) by anyone awake aboard; nothing by a sleeper but his own."""
    if senses.everything:
        return True
    where = tuple(getattr(row, "where", None) or (DECK,))
    if senses.asleep:
        return ASLEEP in where
    tokens = senses.tokens
    if ABOARD in where and ABOARD in tokens:
        return True
    return any(w in tokens for w in where)


def where_words(row: Any) -> str:
    """Where a row is to be had, in words: the row's own ("the lead is cast on deck"), else
    from its places ("to be had on deck or in the cabin")."""
    own = str(getattr(row, "where_words", "") or "")
    if own:
        return own
    where = [w for w in (getattr(row, "where", None) or (DECK,)) if w != ASLEEP]
    names = [_PLACE_NAMES.get(w, w) for w in where]
    if not names:
        return "not to be had"
    if len(names) == 1:
        return f"to be had {names[0]}"
    return f"to be had {', '.join(names[:-1])} or {names[-1]}"


def _row_name(row: Any) -> str:
    words = getattr(row, "words", None) or ()
    return str(words[0]) if words else str(getattr(row, "id", "") or "")


def elsewhere_words(rows: list[Any], senses: Senses, named_max: int = 6) -> str | None:
    """One sentence for the rows not to be had where he is, grouped by where they are:
    'Not to be had in the cabin: the true wind, the apparent wind, the speed and 14 more (to
    be had on deck); the depth (the lead is cast on deck).' None with nothing left out."""
    if not rows:
        return None
    groups: dict[str, list[str]] = {}
    for r in rows:
        groups.setdefault(where_words(r), []).append(_row_name(r))
    parts: list[str] = []
    for where, names in groups.items():
        seen: list[str] = []
        for n in names:
            if n not in seen:
                seen.append(n)
        shown = seen[:named_max]
        more = len(seen) - len(shown)
        listed = ", ".join(shown)
        if more:
            listed += f" and {more} more"
        parts.append(f"{listed} ({where})")
    return f"Not to be had {senses.words()}: {'; '.join(parts)}."
