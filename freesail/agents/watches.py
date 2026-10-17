"""The deck passing among the officers of the watch by the watch bill (spec M7b §17;
package 53).

A ship may have several stations of the officer of the watch's kind (45c's groundwork:
the frigate's `second officer` and, since this package, `third officer`, each a
lieutenant with a watch of his own by the bill). The captain gives the deck to any of them
(`you have the deck`, `Mr Russell, you have the deck`); once an officer who keeps a watch
has it, it passes at the change of the watch to the officer whose watch comes on deck,
where a model or the player holds his station: the one going below gives it up as at the
captain's `I have the deck`, the one coming up takes it as at `you have the deck` (the
night orders, what the captain's word allows him and the last handover note said to him),
he is on the quarterdeck, and one line of the log says so. The first lieutenant keeps no
watch and keeps the deck until the captain takes it; an officer whose relief is held by
nobody keeps it, as a lieutenant of the period kept the deck until he was relieved.

Nothing here runs where fewer than two officers' stations are held, so that a ship with
one officer, or none seated, is as it was, line for line.
"""

from __future__ import annotations

from typing import Any

from freesail.core.events import Severity

__all__ = ["DECK_PASSED", "held_officers", "tick"]

DECK_PASSED = "watch.deck_passed"


def held_officers(world: Any) -> list[Any]:
    """The officers' stations held now (a model's harness or the player's seat, seated,
    not released and not paused), the officer of the watch's own first."""
    from freesail.agents.agent import officer_stations

    out = []
    agents = getattr(world, "agents", None) or {}
    seat = getattr(world, "player_seat", None)
    for name in officer_stations(world):
        held = agents.get(name)
        if held is None and seat is not None and seat.station.name == name:
            held = seat
        if held is None or held.agent.released or held.agent.paused:
            continue
        if not getattr(held, "started", True):
            continue
        out.append(held)
    return out


def tick(world: Any) -> None:
    """On the hour (the watches and the dog watches change on it): where the bill's watch
    on deck has changed and two officers' stations are held, the deck passes to the
    officer of the watch coming on deck (`_pass`)."""
    from datetime import timedelta

    from freesail.crew import bill
    from freesail.world.movement import _mustered

    seats = len(getattr(world, "agents", None) or {}) + (
        1 if getattr(world, "player_seat", None) is not None else 0
    )
    if seats < 2 or not _mustered(world):
        # fewer than two stations held, or nobody mustered: nothing to pass, and nothing
        # read that would muster the people for nothing
        return
    when = world.clock.ship_time
    now = bill.watch_on_duty(when).value
    if bill.watch_on_duty(when - timedelta(minutes=1)).value == now:
        return
    held = held_officers(world)
    if len(held) < 2:
        return
    _pass(world, now, held)


def _pass(world: Any, watch: str, held: list[Any]) -> None:
    going = next((h for h in held if getattr(h.agent, "deck", False)), None)
    if going is None:
        return
    stations = world.stations
    person = stations.holder(going.station.name)
    if person is None or person.watch is None or person.watch == watch:
        return
    coming = None
    for h in held:
        if h is going:
            continue
        relief = stations.holder(h.station.name)
        if relief is not None and relief.watch == watch and relief.aboard:
            coming = h
            break
    if coming is None:
        return
    relief = stations.holder(coming.station.name)
    going.take_deck(
        by=f"the {coming.station.name} ({relief.name}), relieving him at the change of the watch"
    )
    if relief.where not in ("quarterdeck", "deck"):
        relief.where = "quarterdeck"
    relief.up = True
    coming.give_deck(by=f"the {going.station.name} ({person.name}), at the change of the watch")
    world.record(
        Severity.NOTABLE,
        DECK_PASSED,
        f"At the change of the watch the deck passed from the {going.station.name} "
        f"({person.name}) to the {coming.station.name} ({relief.name}), by the watch bill.",
        data={
            "from": going.station.name,
            "to": coming.station.name,
            "watch": watch,
        },
    )
