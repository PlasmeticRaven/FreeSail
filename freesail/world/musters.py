"""A ship's muster made again when men leave it or join it: 74's functions (the prize crew put
aboard, the prisoners' muster), shared with package 60's transfer of a company between two
hulls (`docs/design/Design-ShipBought.md` §6.2; `freesail/world/prizes.py` keeps its callers
under their old names)."""

from __future__ import annotations

from typing import Any

from freesail.crew.model import Crew, Sailor, Station, Watch

__all__ = ["deal_watches", "draw", "join", "remuster", "take_out"]


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


def draw(
    hull: Any,
    n: int,
    party: list[Sailor] | None = None,
    *,
    rating: str = "",
    taken: frozenset[str] | set[str] = frozenset(),
) -> list[Sailor]:
    """Up to `n` men drawn from the hull's muster, as a prize crew is drawn (74): the party
    given first (whole and at no work, never the quarterdeck or an idler), then her fit men at
    no work in the muster's order, never a post, the quarterdeck, a marine or an idler; a
    `rating` named ('able', 'marine') draws that rating alone, a marine then from the marines.
    Men whose ids are `taken` are passed over. Shared by `prizes._draw_prize_crew` and package
    60's transfer (the lead's reading of ab0ade58: one draw, not two)."""
    crew = hull.ship.extra.get("crew")
    if crew is None:
        return []
    chosen: list[Sailor] = []
    if party:
        for s in party:
            if s.fit and s.at is None and s.station not in (Station.QUARTERDECK, Station.IDLERS):
                chosen.append(s)
            if len(chosen) >= n:
                break
    barred = {Station.QUARTERDECK, Station.MARINES, Station.IDLERS}
    if rating == "marine":
        barred.discard(Station.MARINES)
    if len(chosen) < n:
        passed = {s.id for s in chosen} | set(taken)
        for s in crew.sailors:
            if len(chosen) >= n:
                break
            if s.id in passed or not s.fit or s.at is not None or s.post:
                continue
            if s.station in barred:
                continue
            if rating and s.rating.value != rating:
                continue
            chosen.append(s)
    return chosen


def join(hull: Any, men: list[Sailor], came_from: str = "") -> None:
    """The men into the hull's muster as her watches stand (the lead's reading of ab0ade58,
    item 3): each into the smaller watch (the starboard on a tie), nobody already aboard moved,
    her routine, her quarter bill and her guns as they are; a man whose id is taken already is
    told apart by the ship he came from, as a person is. A muster made where she has none."""
    extra = hull.ship.extra
    crew = extra.get("crew")
    if crew is None:
        crew = Crew(ship_name=str(getattr(hull, "name", "") or ""), sailors=[])
        remuster(hull, crew)
    taken = {s.id for s in crew.sailors}
    for s in men:
        if s.id in taken and came_from:
            s.id = f"{s.id}:{came_from}"
        taken.add(s.id)
        s.post = None
        s.at = None
        s.quarters = ""
        s.turned_up = False
        if s.station in (Station.QUARTERDECK, Station.IDLERS):
            s.watch = Watch.NONE
        else:
            star = sum(1 for x in crew.sailors if x.watch is Watch.STARBOARD)
            lar = sum(1 for x in crew.sailors if x.watch is Watch.LARBOARD)
            s.watch = Watch.STARBOARD if star <= lar else Watch.LARBOARD
        crew.sailors.append(s)
    crew.reindex()
