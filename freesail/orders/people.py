"""The people's orders (spec M5 §22; package 35): what the captain says about the
named few aboard.

    send for the master             the messenger goes for him; he comes to where the
    pass the word for the carpenter captain is a minute later (`people.PASS_THE_WORD_S`)
    go below                        the captain to his cabin; a message reaches him there
    come on deck                    the captain to the quarterdeck
    ask the pilot <question>        the pilot answers from his knowledge of his port: the
                                    tide, the channel, the marks, the anchorage, the news

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

__all__ = ["NO_PEOPLE_WORDS", "check", "execute"]

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
    if verb == "go below":
        if rest:
            raise OrderError(f"'go below' takes nothing after it; '{rest}' was not understood.")
        text, data = people.captain_moves(below=True)
        return "captain.below", text, {"verb": verb, "level": 1} | data
    if verb == "come on deck":
        if rest:
            raise OrderError(f"'come on deck' takes nothing after it; '{rest}' was not understood.")
        text, data = people.captain_moves(below=False)
        return "captain.on_deck", text, {"verb": verb, "level": 1} | data
    if verb == "ask the pilot":
        ports = getattr(world, "ports", None)
        if ports is None or ports.pilot is None:
            raise OrderError("There is no pilot aboard to ask.")
        question = rest or order.verb_phrase.removeprefix("ask the pilot").strip()
        answer = ports.answer(question or "the channel")
        return "pilot.answered", answer, {"verb": verb, "level": 1, "question": question}
    raise OrderError(f"'{verb}' is not an order about the people this ship knows.")


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
        if world.people.find(who) is None:
            names = ", ".join(x.name for x in world.people.all)
            raise OrderError(f"Nobody aboard answers to '{who}'; the people are {names}.")
    elif verb in ("go below", "come on deck") and rest:
        raise OrderError(f"'{verb}' takes nothing after it; '{rest}' was not understood.")
