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

import re
from dataclasses import dataclass
from typing import Any

from freesail.world.hulls import is_observer
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
    "WORDS_BETWEEN_PEOPLE",
    "WORD_KINDS",
    "all_known",
    "as_heard",
    "elsewhere_words",
    "as_the_owner_sees",
    "hears",
    "his_own",
    "owners_world_order",
    "is_asleep",
    "player_hull",
    "players_person",
    "players_senses",
    "players_station",
    "players_visitor",
    "reach_of",
    "reaches",
    "reading_here",
    "rows_elsewhere",
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
        # the script's boat on her errand and the pilot's cutter alongside (a person off the
        # ship, in no hull of his own: 82's manned boat is a hull and reads as a deck): within
        # a boat's pull of her he sees what her deck does and hears her bell across the water
        # (judgement); nothing of what every man in the hull feels (the heel, the motion)
        return frozenset({DECK, p})
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
    return Senses(senses_of_place(spot[0] if spot else "boat"), spot, "", person)


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
#   reader   the person the line names (`to`) and nobody else, asleep or awake, with no
#            fallback to a place (package 100: a letter's words shown its reader, a
#            writer's own words shown him)
REACH: dict[str, str] = {
    "free.read": "reader",
    "free.written": "reader",
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
    "ship.taken_up": "aboard",  # package 60: a captain takes command of her, or leaves her
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
    "message.received": "reader",  # the words read at the door, the captain's (package 100)
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
    "thing.handed": "port",  # a letter given from the boat to its addressee ashore (100)
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
    # package 74 (step 6): an appointment and an exchange are the port's news, said ashore
    # where the man stands (each line's data names the shore and the port): he and the
    # persons ashore at that port have them, and no ship's deck is woken by them (the
    # `prize` family wakes a ship; these two are not her business)
    "command.new": "said",
    "prize.exchanged": "said",
    "log.read": "record",
    # the report, the call and the boat's report (step 3 writes them; placed first)
    "report.made": "person",
    "report.called": "wakes",
    "report.boat": "port",
    # the command devolved and resumed (decision 63; package 65, step 3): every man aboard
    "ship.command_devolved": "aboard",
    "ship.command_resumed": "aboard",
}

# ...and by family, for every kind of a family not named above.
FAMILIES: dict[str, str] = {
    "clock": "aboard",
    "guns": "wakes",
    "action": "wakes",
    "small_arms": "wakes",
    "prize": "wakes",  # package 74: she is taken, the prisoners rising, the prize retaken
    # package 74 (step 6): the court martial's lines are words said before the court, heard
    # by the persons ashore at its port (each line's data names the shore and the port) and
    # on no ship's deck
    "court": "said",
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
    "flags": "deck",  # package 76 (item 8): a flag of command hoisted, seen as the colours are
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
    {"guns", "action", "small_arms", "prize"}
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
    if cls == "reader":
        # a letter's words (package 100): the reader's, whoever and wherever he is, by his
        # name whole (a surname shared is no reader)
        person = senses.person
        name = str(getattr(person, "name", "") or "")
        to = _names(data, "to")
        if not to:
            # a letter come aboard read at the door (`message.received`): the captain's,
            # whose it is; nobody's beside him, wherever he reads it (step 2)
            return person is not None and _is_captain(world, person)
        return bool(name) and to.lower() == name.lower()
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


# -- the player at the prompt (decision 59 and decision 62; the design's §11) ------------

# The lines of words said between people (package 52; spec M7b §15): a word told, a
# question put, an answer, a person's words, a free line; and a word said in a place
# (`agent.spoke`, package 66). Their hearing is 66's, which the harness applies to a
# station (`Harness._reaches`) and `hears` below to the player's person.
WORDS_BETWEEN_PEOPLE = ("agent.told", "agent.asked", "agent.said", "person.spoke", "free.line")
WORD_KINDS = (*WORDS_BETWEEN_PEOPLE, "agent.spoke")

# The driver's line that says the player is aboard another ship than his own (`--ship`,
# package 82, item 2; `ui.console.aboard_ship`): read from his own ship's log, so that a
# save and a replay read the same.
PLAYER_LEFT = "driver.left"


def _root(world: Any) -> Any:
    """The one World behind a hull's façade (`hulls.Hull.world`; `World.parent` is the
    followed hull's façade, not the World)."""
    from freesail.world.hulls import Hull

    while isinstance(world, Hull):
        world = world.world
    return world


def player_hull(world: Any) -> Any:
    """The hull of the ship the player is aboard as her captain: his own, or the one
    `--ship` named (the last `driver.left` line of his own ship's log, which the replay
    writes again); None in an observed world, which has no ship of the player's."""
    root = _root(world)
    players = getattr(root, "players", None)
    if players is None or is_observer(players):
        return None
    if (getattr(root, "__dict__", None) or {}).get("_players"):
        return players  # he has taken command of her (package 60): `--ship` stood at the start
    hulls = getattr(root, "hulls", None) or {}
    log = getattr(players, "log", None)
    if log is None or not hulls:
        return players
    # the scan is from where it left off (the line is written at the start, if at all)
    held = root.__dict__.get("_player_hull_read") or (0, None)
    n = len(log)
    if held[0] != n:
        found = held[1]
        for i in range(held[0], n):
            e = log[i]
            if e.kind == PLAYER_LEFT:
                found = str((e.data or {}).get("ship") or "")
        held = (n, found)
        root.__dict__["_player_hull_read"] = held
    name = held[1]
    if not name:
        return players
    key = name.strip().strip('"').lower()
    for hull in hulls.values():
        ship_name = str(getattr(getattr(hull, "ship", None), "name", "") or "")
        if str(hull.id).lower() == key or ship_name.lower() == key:
            return hull
    return players


def _seat_person(root: Any, seat: Any) -> Any:
    """The seat's person, read in the seat's hull's block (a façade read from inside another
    hull's block answers for that hull)."""
    hull = getattr(seat, "world", root)
    as_hull = getattr(root, "as_hull", None)
    try:
        if callable(as_hull) and hull is not root:
            with as_hull(hull):
                return hull.stations.holder(seat.station.name)
        return root.stations.holder(seat.station.name)
    except Exception:  # noqa: BLE001  (a people's build that cannot run binds nobody)
        return None


def _seat(world: Any) -> Any:
    """The player's seat, held (not released), on the world given or its root; None."""
    for w in (world, _root(world)):
        seat = getattr(w, "player_seat", None)
        agent = getattr(seat, "agent", None)
        if seat is not None and agent is not None and not agent.released:
            return seat
    return None


def players_station(world: Any) -> str:
    """The station the player's words are said as: his seat's, else the captain's."""
    seat = _seat(world)
    return str(seat.station.name) if seat is not None else "captain"


def players_person(world: Any) -> Any:
    """The player's one person (decision 62): the seat's person when he is seated, else the
    captain of the ship he is aboard as her captain (`player_hull`), wherever his body is
    (in the boat, aboard another ship, ashore). None where there is none: an observed world,
    a seat bound to nobody (the director's), or a model at that captain's station."""
    root = _root(world)
    from freesail.world.captive import captive_person

    captive = captive_person(root)
    if captive is not None:
        # the player's person a captive (package 74, the design's §3.1): his ship's captain
        # answers for the prize master from the taking, so the one world keeps who he is
        return captive
    seat = _seat(world)
    if seat is not None:
        return _seat_person(root, seat)
    from freesail.world.captive import remembered_person

    remembered = remembered_person(root)
    if remembered is not None:
        # freed (exchanged, landed by a cartel), he is the player's person still while his
        # own ship has a prize master for her captain (package 74, step 6): after the seat,
        # which is the player's own choice of person, and only while the mark stands (it is
        # past once he is her captain again, and the checks below read as they did)
        return remembered
    hull = player_hull(root)
    if hull is None:
        return None
    from freesail.agents.agent import CAPTAIN

    held = (getattr(hull, "agents", None) or {}).get(CAPTAIN)
    if held is not None and not held.agent.released:
        return None  # a model holds her captain's station: the owner looks on
    as_hull = getattr(root, "as_hull", None)
    try:
        if callable(as_hull) and hull is not root:
            with as_hull(hull):
                return hull.people.captain
        return root.people.captain
    except Exception:  # noqa: BLE001  (a world with no muster: the point ship)
        return None


def players_visitor(world: Any) -> Any:
    """The player's person when he is aboard the current hull as a visitor (decision 62; the
    road from his own boat aboard another ship): his orders at the prompt are his and not
    her captain's. None when he is at home, elsewhere, seated, or there is none."""
    if _seat(world) is not None:
        return None  # the seat goes with its person already (package 82, item 2)
    person = players_person(world)
    if person is None or not getattr(person, "aboard", True):
        return None
    from freesail.world.hearing import own_hull
    from freesail.world.movement import hull_of, is_boat_hull

    here = own_hull(world)
    hid = str(getattr(person, "hull", "") or "")
    home = str(getattr(person, "home", "") or "")
    if not hid or hid != here or not home or home == here:
        return None
    hull = hull_of(_root(world), hid)
    return None if hull is None or is_boat_hull(hull) else person  # his own boat is his


def _hull_of_person(root: Any, person: Any) -> str:
    """The hull the person belongs to now: the one he is in, else (in the boat, ashore) his
    home's."""
    hid = getattr(person, "hull", None) if getattr(person, "aboard", True) else None
    return str(hid or getattr(person, "home", "") or "")


def players_senses(world: Any) -> Senses:
    """What the player perceives at the prompt (decision 59: as a model does, so that there
    are not two views of one world): his person's senses where he is, read in his hull's
    block; `EVERYTHING` under `knowledge: all`, with no person of his (an observed world,
    the director's seat), and under `follow` of a hull he holds no person in, which is the
    owner's eye (the design's §11)."""
    root = _root(world)
    if all_known(root):
        return EVERYTHING
    seat = _seat(world)
    person = players_person(root)
    hulls = getattr(root, "hulls", None) or {}
    followed = hulls.get(getattr(root, "followed", None)) or getattr(root, "players", None)
    followed_id = str(getattr(followed, "id", "") or "")
    as_hull = getattr(root, "as_hull", None)
    if seat is not None:
        from freesail.agents.agent import DIRECTOR

        if person is None and str(seat.station.name) == DIRECTOR:
            return EVERYTHING
        hull = getattr(seat, "world", root)  # the seat's hull, or the World as it was given
        if hull is root:
            hull = getattr(root, "players", None) or root
        his = _hull_of_person(root, person) if person is not None else str(hull.id)
        if hulls and his != followed_id:
            return EVERYTHING  # the owner's eye on a hull he holds no person in
        if callable(as_hull) and hull is not root:
            with as_hull(hull):
                return station_senses(hull, seat.station.name, person)
        return station_senses(root, seat.station.name, person)
    if person is None:
        return EVERYTHING
    if hulls and _hull_of_person(root, person) != followed_id:
        return EVERYTHING  # `follow` of a hull he holds no person in: the owner's eye
    if callable(as_hull) and followed is not None and followed is not root:
        with as_hull(followed):
            return senses_of(followed, person)
    return senses_of(root, person)


# The player's own lines (package 98, step 2; the owner's ruling of 2026-11-09): what is not
# in the world, made by the man at the prompt, is always shown him wherever he stands, asleep
# or awake: his readings (`query.*`, the information calls), his orders' acknowledgements
# and refusals (`order.*`), his own word (the words' kinds said by him: `say`, `tell` and
# `ask`, a word said below directly to another station among them) and the seat's lines of
# his own (a refusal by the station's authority, an answer he gave). What is done in the
# world out of his sight is not shown him by this, and is not reported of itself.
OWN_FAMILIES: tuple[str, ...] = ("query.", "order.")
SEAT_ACTOR_SUFFIX = " (the player)"  # `agents.seat.seat_actor`'s: "the master (the player)"


# The owner's world order typed at his prompt (package 98, the lead's addition (d) of
# 2026-11-10): `world.order` with this source (`ui.console.LIVE_WORLD_ORDER_SOURCE`), his own
# line, shown him as given with its outcome; for the record to every other reader (decision
# 46), and a director's orders, of another source, never shown the player.
OWNER_SOURCE = "the owner"
WORLD_ORDER_KIND = "world.order"


def owners_world_order(e: Any) -> bool:
    """Whether a line is the owner's own world order, typed at his prompt."""
    data = getattr(e, "data", None) or {}
    return getattr(e, "kind", "") == WORLD_ORDER_KIND and data.get("source") == OWNER_SOURCE


def as_the_owner_sees(e: Any) -> Any:
    """The owner's world order as his play log shows it: the order as he gave it, then its
    outcome ('Your world order 'ship "X": ...': not carried out: ...'); any other line as it
    is. A copy: the log's own line is unchanged."""
    if not owners_world_order(e):
        return e
    import dataclasses

    order = str((e.data or {}).get("order") or "")
    outcome = str(e.text).split(": ", 1)[1] if ": " in str(e.text) else str(e.text)
    return dataclasses.replace(e, text=f"Your world order '{order}': {outcome}")


def his_own(e: Any, station: str = "captain") -> bool:
    """Whether a line is the player's own at the prompt (`OWN_FAMILIES`, the words he said,
    his seat's lines), by its actor: the captain's at the captain's prompt, the seat's
    actor at a station's, the driver's for the seat's own refusals and answers. A rule
    captain, a standing order and a station held by a model each have their own actor."""
    if owners_world_order(e):
        return True
    kind = str(getattr(e, "kind", "") or "")
    actor = str(getattr(e, "actor", "") or "")
    data = getattr(e, "data", None) or {}
    mine = actor == station or actor == f"the {station}{SEAT_ACTOR_SUFFIX}"
    if mine and (kind.startswith(OWN_FAMILIES) or kind in WORD_KINDS):
        return True
    return bool(data.get("seat")) and actor == "driver" and str(data.get("station")) == station


def hears(world: Any, senses: Senses, e: Any, station: str = "captain") -> bool:
    """Whether a line reaches a person at the prompt with these senses (the console's and
    the browser's play log, decision 59): his own lines wherever he stands (`his_own`, the
    owner's ruling of 2026-11-09); `reaches` for every other kind but the words, and for
    the words 66's hearing as the harness applies it to a station (`Harness._reaches`): his
    own, a word to him, one whose hearers name his station, else one said within his
    hearing; a sleeper hears a word to him and nothing else."""
    if senses.everything:
        return True
    if his_own(e, station):
        return True
    kind = str(getattr(e, "kind", "") or "")
    if kind not in WORD_KINDS:
        return reaches(world, senses, e)
    data = getattr(e, "data", None) or {}
    speaker = str(data.get("speaker") or data.get("station") or "")
    addressee = str((data.get("to") if kind == "agent.said" else data.get("station")) or "")
    if kind == "agent.spoke" and speaker == station:
        return True  # his own word
    if kind in WORDS_BETWEEN_PEOPLE and addressee == station:
        return True
    if senses.asleep:
        return False
    if station in (data.get("heard_by") or ()):
        return True
    if "heard_by" in data:
        return False  # its hearers are named, and he is not among them
    from freesail.world.hearing import own_hull, within_hearing

    hull = str(data.get("said_from") or own_hull(world))
    place = str(data.get("place") or data.get("where") or "quarterdeck")
    if data.get("hail"):
        said: tuple[str, ...] = ("aboard", hull, "quarterdeck")
    elif place in PLACES and PLACES[place].aboard:
        said = ("aboard", hull, place)
    else:
        return bool(senses.spot) and senses.spot[0] == "ashore"  # a word said ashore
    return within_hearing(said, senses.spot)


def rows_elsewhere(senses: Senses) -> list[Any]:
    """The rows of the readings registry not to be had by these senses (the sample's and
    the snapshot's "not to be had here"): the rows a person is asked, the driver's, the
    parametric and the absent left out."""
    from freesail.api import readings as R

    if senses.everything:
        return []
    return [
        r
        for r in R.REGISTRY
        if not r.is_absent
        and r.parametric is None
        and r.kind not in R.DRIVER_KINDS
        and not r.per_asker
        and not reading_here(r, senses)
    ]


# -- books, papers and pictures in their places (the design's §8; step 5) -----------------

# Where the ship's own things are kept, by the senses that read them there: the log (the
# log board on the quarterdeck, the log books in the cabin and the gunroom), the chart (the
# chart table in the cabin and the gunroom, the binnacle's chart on deck), the book of
# standing orders (the quarterdeck, where the night orders hang at the binnacle, and the
# cabin), the books drafted (with the book of standing orders: a sheet of night orders is
# the officer's to read at the binnacle, a manifest the boat's; the owner's ruling of
# 2026-10-16 that a book is read from anywhere aboard is kept to the deck and the cabin,
# and not to the cabin alone as §8's table has it) and the ship seen (`ship_view`: the open
# deck, aloft and the boat). The player's reference (the primer, the catalogue, the grammar,
# the tools, the world) is nowhere and everywhere: his own, read from anywhere.
KEPT: dict[str, tuple[str, ...]] = {
    "log": (DECK, CABIN, GUNROOM),
    "chart": (DECK, CABIN, GUNROOM),
    "standing orders": (DECK, CABIN),
    "books": (DECK, CABIN),
    "ship_view": (DECK, ALOFT, "boat", "cutter"),
}
KEPT_WORDS: dict[str, str] = {
    "log": "The log book is in the cabin and the gunroom, the log board on the quarterdeck",
    "chart": "The chart is in the cabin and the gunroom, and at the binnacle on deck",
    "standing orders": "The book of standing orders is on the quarterdeck and in the cabin",
    "books": "on the quarterdeck and in the cabin, with the book of standing orders",
    "ship_view": "She is seen from the deck or the boat",
}
# what a man does with each where it is
KEPT_DO: dict[str, str] = {
    "log": "read it",
    "chart": "read it",
    "standing orders": "read it",
    "books": "read it",
    "ship_view": "see her",
}
ASLEEP_WORDS = "You are asleep; nothing is read until you are woken."
# ashore, where the sentence is not the kept words' subject
ASHORE_WORDS: dict[str, str] = {"log": "The ship's log is aboard her."}


def _below(senses: Senses) -> bool:
    """Whether he is below decks (the cabin, the gunroom, a room)."""
    return bool(senses.tokens & ({CABIN, GUNROOM} | ROOMS))


def walk_words(senses: Senses, places: tuple[str, ...], do: str = "read it") -> str:
    """The walk that would bring him to a thing kept in `places`, for the end of a
    sentence: ': come on deck to read it', ': come down to read it' (aloft), ': go below to
    read it'; '' where no walk of his own would (ashore, asleep, in a boat)."""
    if senses.asleep or ASHORE in senses.tokens or (senses.spot and senses.spot[0] != "aboard"):
        return ""
    if DECK in places:
        if ALOFT in senses.tokens:
            return f": come down to {do}"
        if _below(senses):
            return f": come on deck to {do}"
        return ""
    if CABIN in places or GUNROOM in places:
        return f": go below to {do}"
    return ""


def thing_here(key: str, senses: Senses) -> bool:
    """Whether a thing of the ship's (`KEPT`) is to be had where he is: everything for the
    director and under `knowledge: all`; nothing by a sleeper or ashore."""
    if senses.everything:
        return True
    if senses.asleep or ASHORE in senses.tokens:
        return False
    return any(w in senses.tokens for w in KEPT[key])


def thing_elsewhere(key: str, senses: Senses, title: str = "") -> str | None:
    """The sentence for a thing not to be had where he is, with where it is and the walk
    ("The log book is in the cabin and the gunroom, the log board on the quarterdeck; you
    are in the hold: come on deck to read it."); ashore, "The ship's log is aboard her.";
    None where it is to be had."""
    if thing_here(key, senses):
        return None
    if senses.asleep:
        return ASLEEP_WORDS
    if key == "books":
        what = f"The book '{title}' is" if title else "The books drafted are"
        where = f"{what} {KEPT_WORDS[key]}"
    else:
        where = KEPT_WORDS[key]
    if ASHORE in senses.tokens:
        if key in ASHORE_WORDS:
            return ASHORE_WORDS[key]
        if key == "ship_view":
            return f"{where}; you are ashore."
        thing = where.split(" is ", 1)[0].split(" are ", 1)[0]
        return f"{thing} {'are' if ' are ' in where else 'is'} aboard her."
    return f"{where}; you are {senses.words()}{walk_words(senses, KEPT[key], KEPT_DO[key])}."


# -- the papers -------------------------------------------------------------------------


def _shares_stem(task: str, handle: str) -> bool:
    """Whether the words of a man's task name the paper (a stem of four letters shared:
    'writing up the manifest' and 'the manifest'; 'the purser's books' and 'books')."""
    small = {"the", "and", "with", "for", "of", "his", "book", "books", "list", "account"}
    stems = {w[:4] for w in re.findall(r"[a-z]+", str(handle or "").lower()) if w not in small}
    if not stems:
        stems = {w[:4] for w in re.findall(r"[a-z]+", str(handle or "").lower())}
    words = {w[:4] for w in re.findall(r"[a-z]+", str(task or "").lower())}
    return bool(stems & words)


def paper_place(world: Any, page: Any) -> tuple[str, str]:
    """Where a paper is now and in whose hands: (the place's id, 'with the purser'). The
    keeper's rule: the keeper carries his paper with him while he is occupied with it (the
    words of his task name it), else it lies in its place."""
    keeper_role = str(getattr(page, "keeper", "") or "")
    people = getattr(world, "people", None)
    keeper = None
    if people is not None and keeper_role:
        try:
            keeper = people.find(f"the {keeper_role}")
        except Exception:  # noqa: BLE001  (a company that cannot be read)
            keeper = None
    with_whom = f"with the {keeper_role}" if keeper_role else ""
    if (
        keeper is not None
        and getattr(keeper, "aboard", True)
        and getattr(keeper, "occupied", False)
        and _shares_stem(str(getattr(keeper, "task", "") or ""), str(page.handle))
    ):
        where = str(getattr(keeper, "where", "") or page.place)
        return ("quarterdeck" if where == "deck" else where), f"{with_whom} at his {keeper.task}"
    return str(page.place), with_whom


def place_here(place_id: str, senses: Senses) -> bool:
    """Whether a place aboard is where he is: the open deck's three one place, the rooms
    each their own; nothing for a sleeper, ashore or in a boat."""
    if senses.everything:
        return True
    if senses.asleep or ASHORE in senses.tokens:
        return False
    if senses.spot and senses.spot[0] != "aboard":
        return False
    needed = senses_of_place(place_id) - {ABOARD}
    return bool(needed) and needed <= senses.tokens


def paper_here(world: Any, page: Any, senses: Senses) -> bool:
    return place_here(paper_place(world, page)[0], senses)


def paper_where_words(world: Any, page: Any) -> str:
    """Where a paper is, for a listing: 'in the hold, with the purser'."""
    place, with_whom = paper_place(world, page)
    return f"{place_words(place)}, {with_whom}" if with_whom else place_words(place)


def paper_elsewhere(world: Any, page: Any, senses: Senses) -> str | None:
    """The sentence for a paper not where he is: "The manifest is kept in the hold, with
    the purser; go to the hold to read it (or ask the purser)."; None where he reads it."""
    if paper_here(world, page, senses):
        return None
    if senses.asleep:
        return ASLEEP_WORDS
    head = str(page.handle)
    head = head[:1].upper() + head[1:]
    place, with_whom = paper_place(world, page)
    keeper = str(getattr(page, "keeper", "") or "")
    if ASHORE in senses.tokens:
        return f"{head} is aboard her, {place_words(place)}."
    kept = f"{head} is kept {place_words(place)}" + (f", {with_whom}" if with_whom else "")
    ask = f" (or ask the {keeper})" if keeper else ""
    # the walk, in the same words whoever reads them (the pane and a station agree): the
    # cabin is the captain's, and a man who may not walk in asks him for it
    senses_there = senses_of_place(place) - {ABOARD}
    if DECK in senses_there:
        walk = "come down" if ALOFT in senses.tokens else "come on deck"
    else:
        walk = f"go to {PLACES[place].name}" if place in PLACES else f"go to {place}"
    return f"{kept}; {walk} to read it{ask}."
