"""A ship's muster made again when men leave it or join it: 74's functions (the prize crew put
aboard, the prisoners' muster), shared with package 60's transfer of a company between two
hulls (`docs/design/Design-ShipBought.md` §6.2; `freesail/world/prizes.py` keeps its callers
under their old names)."""

from __future__ import annotations

from typing import Any

from freesail.crew.model import Crew, Sailor, Station, Watch

__all__ = ["deal_watches", "remuster", "take_out"]


def remuster(hull: Any, crew: Crew) -> int:
    """The hull's working company is `crew` from here: `ship.extra["crew"]`, the routine
    re-pointed (its all-hands call dropped), the quarter bill reckoned afresh at the next
    beat. Returns how many keepers were re-pointed (the audit's figure)."""
    ship = hull.ship
    extra = ship.extra
    moved = 0
    crew.reindex()
    extra["crew"] = crew
    moved += 1
    routine = extra.get("routine")
    if routine is not None:
        routine.crew = crew
        routine._coming = []
        routine._called_at = None
        routine._aloft_ids = frozenset()
        routine._aloft_instances = set()
        moved += 1
    if extra.pop("quarters", None) is not None:
        moved += 1
    battery = extra.get("battery")
    if battery is not None and hasattr(battery, "mode"):
        from freesail.combat.guns import FireMode

        battery.mode = FireMode.HOLD
        battery.word = None
    # the hull's people read the registry (84's one registry); nothing of theirs is cached
    return moved


def deal_watches(sailors: list[Sailor]) -> None:
    """The watches dealt again, by id (the posts and the idlers in none), every man off his
    work and his quarters."""
    for i, s in enumerate(sorted(sailors, key=lambda x: x.id)):
        if s.station in (Station.QUARTERDECK, Station.IDLERS):
            s.watch = Watch.NONE
        else:
            s.watch = (Watch.STARBOARD, Watch.LARBOARD)[i % 2]
        s.at = None
        s.quarters = ""
        s.turned_up = False


def take_out(hull: Any, men: list[Sailor]) -> None:
    """The men out of the hull's muster and off her quarter bill."""
    crew = hull.ship.extra.get("crew")
    if crew is None:
        return
    ids = {s.id for s in men}
    crew.sailors = [s for s in crew.sailors if s.id not in ids]
    crew.reindex()
    quarters = hull.ship.extra.get("quarters")
    if quarters is not None:
        for gc in quarters.crews.values():
            gc.members = [s for s in gc.members if s.id not in ids]
        for name, division in list(quarters.divisions.items()):
            quarters.divisions[name] = [s for s in division if s.id not in ids]
