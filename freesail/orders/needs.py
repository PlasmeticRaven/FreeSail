"""The needs' orders (spec M7b §19, §20; package 54).

    eat                       the person eats: at a table where there is one (the cabin,
                              the gunroom, the galley, ashore), else a biscuit and a piece
                              of cheese brought up from the stores
    drink                     at the scuttle-butt on deck, or where he is; his beer when
                              the water is foul or expended
    drink the foul water      the water found foul, drunk all the same: it gripes him
    sleep                     the player turns in below until his next order, an urgent
                              line, or he wakes rested (a model's station turns in with
                              `stand by, asleep below until called`)
    how am I                  his needs in words, and when he last ate, drank and slept
    short allowance           the captain's: the people at half the whole, every man
    whole allowance           alike (the Regulations' Art. III), and back

The first five are a person's own (object `needs`, which every station's domain allows):
the person is the one whose station gives the order (`world.needs.NeedsKeeper.person_of`),
and the answer is his alone, never a line of the log (`core.world.UNLOGGED_KINDS`). The
allowance is the ship's, the captain's to give, and its line says it with the people's
temper (`crew.victuals.set_allowance`).
"""

from __future__ import annotations

from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["execute"]

Result = tuple[str, str, dict[str, Any]]

# The model's own way to turn in, said when a model's station orders `sleep`.
MODEL_SLEEP_WORDS = (
    "A station turns in with its own stand-by: stand_by('asleep below until called'). You "
    "sleep below until you are called, an urgent line wakes you, and you wake of yourself "
    "when you are rested."
)


def execute(ship: Any, order: Order) -> Result:
    world = world_of(ship)
    verb = order.verb
    if world is None or getattr(world, "needs", None) is None:
        if verb in ("short allowance", "whole allowance"):
            raise OrderError("She keeps no stores to put the people to an allowance of.")
        raise OrderError("Nobody here eats, drinks or sleeps: the ship is not in a world.")
    data: dict[str, Any] = {"verb": verb, "level": 1}
    if verb in ("short allowance", "whole allowance"):
        from freesail.crew import victuals

        text, more = victuals.set_allowance(world, short=verb == "short allowance")
        return "stores.allowance", text, data | more
    actor = str((getattr(ship, "extra", None) or {}).get("order_actor") or "captain")
    keeper = world.needs
    person, holder = keeper.person_of(actor)
    data["person"] = person.name
    if verb == "eat":
        text = keeper.eat(person, holder)
    elif verb == "drink":
        text = keeper.drink(person, holder)
    elif verb == "drink the foul water":
        text = keeper.drink(person, holder, foul_water=True)
    elif verb == "sleep":
        if holder is not None and getattr(holder, "model_name", "") != "the player":
            text = MODEL_SLEEP_WORDS
        else:
            text = keeper.turn_in(person, holder)
    elif verb == "how am i":
        text = keeper.how(person, holder)
    else:
        raise OrderError(f"'{verb}' is not an order of the needs this ship knows.")
    return "needs.answer", text, data
