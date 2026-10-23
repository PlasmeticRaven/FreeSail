"""The people's orders (spec M5 §22; package 35): what the captain says about the
named few aboard.

    send for the master             the messenger goes for him; he comes to where the
    pass the word for the carpenter captain is a minute later (`people.PASS_THE_WORD_S`)
    go below                        the captain to his cabin; a message reaches him there
    come on deck                    the captain to the quarterdeck
    ask the pilot <question>        the pilot answers from his knowledge of his port: the
                                    tide, the channel, the marks, the anchorage, the news

People in places (spec M7b §14; package 53; `freesail.world.movement`): the giver of the
order goes, the captain at the prompt or a station's person at his station.

    go below                        the captain to his cabin; anyone else to his berth
    come on deck                    to the quarterdeck (the deck for the idlers' chiefs)
    go to the gunroom               any place aboard his duty allows (not the captain's
                                    cabin); ashore, the port's places: `go to the market`
    go aloft                        into the tops
    go ashore                       by the boat, at a port's reach, landed at the quay
    come aboard                     the boat sent for him from the ship at his port
    hire a waterman                 a shore boat between the ship and the quay, her own
                                    boat away or not, a shilling a head (package 68)

Each is a verb of `data/vocabulary.yaml` with the object `person`: the grammar takes the
words after the verb as they are, and this module reads a role or a name from them. The
people themselves are `freesail.world.people.People`, reached through the World the ship
sails in; a ship alone (no World) refuses in words. `where is <person>` and `the people`
are readings (`freesail.api.readings`), answered at the prompt by `orders.prompt`.
"""

from __future__ import annotations

from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["MOVE_VERBS", "NO_PEOPLE_WORDS", "REACH_VERBS", "check", "execute"]

# The people's verbs that move the giver (package 53; `freesail.world.movement`).
MOVE_VERBS: tuple[str, ...] = (
    "go below",
    "come on deck",
    "go to",
    "go aloft",
    "go ashore",
    "come aboard",
    "hire a waterman",
)
# The verbs of the equal reach (spec M7b §17): every station's, whatever its domain, with
# the deck or without: its own moves, and the port's places asked.
REACH_VERBS: tuple[str, ...] = (*MOVE_VERBS, "the places ashore")

NO_PEOPLE_WORDS = "There is nobody to send for: the ship is not in a world."

Result = tuple[str, str, dict[str, Any]]


def _people(ship: Any) -> tuple[Any, Any]:
    world = world_of(ship)
    if world is None:
        raise OrderError(NO_PEOPLE_WORDS)
    return world, world.people


def execute(ship: Any, order: Order) -> Result:
    """Carry out a people's order. The verb is the vocabulary's key."""
    verb = order.verb
    rest = (order.object or "").strip()
    world, people = _people(ship)
    if verb == "send for":
        who = rest
        phrase = order.verb_phrase
        if phrase.startswith("call the "):
            who = phrase.removeprefix("call the ") + (f" {rest}" if rest else "")
        if not who.strip():
            raise OrderError(
                "Send for whom? Say 'send for the master', 'pass the word for the carpenter'."
            )
        text, data = people.send_for(who)
        return "person.sent_for", text, {"verb": verb, "level": 1} | data
    if verb in MOVE_VERBS:
        return _move(ship, world, people, order, verb, rest)
    if verb == "the places ashore":
        # the port's places (package 53): a question, answered and never journaled
        from freesail.world import movement

        actor = (getattr(ship, "extra", None) or {}).get("order_actor") or "captain"
        text, data = movement.places_ashore(world, movement.person_of_actor(world, actor))
        return "query.places", text, {"verb": verb} | data
    if verb == "ask the pilot":
        ports = getattr(world, "ports", None)
        if ports is None or ports.pilot is None:
            raise OrderError("There is no pilot aboard to ask.")
        question = rest or order.verb_phrase.removeprefix("ask the pilot").strip()
        answer = ports.answer(question or "the channel")
        return "pilot.answered", answer, {"verb": verb, "level": 1, "question": question}
    raise OrderError(f"'{verb}' is not an order about the people this ship knows.")


def _move(ship: Any, world: Any, people: Any, order: Order, verb: str, rest: str) -> Result:
    """The giver of the order goes (package 53; `freesail.world.movement`): the captain's
    own `go below` and `come on deck` as they always were, every other move by the
    movement's verbs, for whoever gives it."""
    from freesail.world import movement

    actor = (getattr(ship, "extra", None) or {}).get("order_actor") or "captain"
    person = movement.person_of_actor(world, actor)
    if person is None:
        # a station bound to nobody named (a passenger's, the watcher's), a standing order's
        # firing or a rule: nobody to go anywhere, and never the captain in his place
        who = actor.split(" (", 1)[0].removeprefix("the ")
        raise OrderError(
            f"Nobody is named at the {who}'s station: there is no person to go anywhere."
            if actor.startswith("the ")
            else "A rule moves nobody; a person goes where he is ordered by his own word."
        )
    captain = person is people.captain and person.aboard
    if verb in ("go below", "come on deck") and rest:
        raise OrderError(f"'{verb}' takes nothing after it; '{rest}' was not understood.")
    if captain and verb == "go below" and person.where != "cabin":
        text, data = people.captain_moves(below=True)
        return "captain.below", text, {"verb": verb, "level": 1} | data
    if captain and verb == "come on deck" and person.where not in movement.DECK_PLACES:
        text, data = people.captain_moves(below=False)
        return "captain.on_deck", text, {"verb": verb, "level": 1} | data
    if captain and verb in ("go below", "come on deck"):
        raise OrderError(f"You are {movement.where_words(world, person)} already.")
    if verb == "go to" and not rest:
        raise OrderError("Go where? Say 'go to the gunroom', 'go below', 'come on deck'.")
    if verb in ("go ashore", "come aboard", "hire a waterman") and rest:
        raise OrderError(f"'{verb}' takes nothing after it; '{rest}' was not understood.")
    if verb == "hire a waterman":
        kind, text, data = movement.by_waterman(world, person)
    elif verb == "go ashore":
        kind, text, data = movement.go_ashore(world, person)
    elif verb == "come aboard":
        kind, text, data = movement.come_aboard(world, person)
    else:
        words = rest or order.verb_phrase
        kind, text, data = movement.go(world, person, verb, words)
    return kind, text, {"verb": verb, "level": 1} | data


def check(ship: Any, order: Order) -> None:
    """Read a people's order whole without carrying it out (package 37l): the person sent
    for is one aboard by his role or his name; the captain's own moves take nothing after
    them. Where he is and what he is at are the order's own business when it fires."""
    verb = order.verb
    rest = (order.object or "").strip()
    world = world_of(ship)
    if world is None:
        return
    if verb == "send for":
        who = rest
        if order.verb_phrase.startswith("call the "):
            who = order.verb_phrase.removeprefix("call the ") + (f" {rest}" if rest else "")
        if not who.strip():
            raise OrderError(
                "Send for whom? Say 'send for the master', 'pass the word for the carpenter'."
            )
        from freesail.world.people import ROLE_WORDS, _words

        # a role the game knows ('the pilot', who comes aboard later) is the moment's
        # business; a name nobody answers to, or no role at all, is the words'
        if world.people.find(who) is None and _words(who) not in ROLE_WORDS:
            names = ", ".join(x.name for x in world.people.all)
            raise OrderError(f"Nobody aboard answers to '{who}'; the people are {names}.")
    elif (
        verb in ("go below", "come on deck", "go ashore", "come aboard", "hire a waterman") and rest
    ):
        raise OrderError(f"'{verb}' takes nothing after it; '{rest}' was not understood.")
    elif verb == "go to" and not rest:
        raise OrderError("Go where? Say 'go to the gunroom', 'go below', 'come on deck'.")
