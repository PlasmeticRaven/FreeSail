"""The prize's readings and events (spec M7 §18; package 74; the design in
`docs/design/Design-Prizes.md` §8), registered in the readings registry from this module,
which `readings` imports at its end as it imports the action's.

    the prize         every prize of this ship's: her name, how she was taken, her prize
    the prizes        master, the prize crew's and the prisoners' counts, her goal, in
                      company or parted and where she lies by the lookout; 'no prize'
    the prisoners     the prisoners this hull holds: how many, where confined, in irons,
                      the named with their parole; 'no prisoners'
    the prize crew    on a prize: the men who work her, their fatigue, the hours since the
                      taking, the prize master; on any other ship 'she is no prize'

The events, for `at` and a stand-by: `she is taken` (`prize.taken`), `possession taken`
(`prize.possessed`, on the prize), `the prisoners rising` (`prize.rising`), `the prize
retaken` (`prize.retaken`), `a prize lost` (`prize.lost`), `a prize burnt` (`prize.burnt`),
`the prisoners aboard` (`prize.prisoners_aboard`).
"""

from __future__ import annotations

from typing import Any

from freesail.api import readings as R
from freesail.crew.model import number_words

__all__ = ["register"]


def _own_id(world: Any) -> str:
    from freesail.world.signals import own_id

    return own_id(world)


def _no_muster_words(world: Any) -> str | None:
    return "no ship's company is mustered"


def _prizes(world: Any, _: str | None) -> dict[str, Any] | None:
    from freesail.world import prizes as P

    sea_world = getattr(world, "parent", None) or world
    sea = getattr(sea_world, "vessels", None)
    if sea is None:
        return None
    mine = P.prizes_of(world, _own_id(world))
    if not mine:
        return {"words": "no prize", "count": 0, "items": []}
    items = []
    words = []
    for v in mine:
        rec = P.record_of(v) or {}
        where = _where_words(world, v)
        company = "in company" if rec.get("company") else "parted"
        ports = getattr(world, "ports", None)
        goal = rec.get("goal", "")
        port = getattr(ports, "ports", {}).get(goal) if ports is not None else None
        goal_words = f"for {port.name}" if port is not None else "with no port named"
        w = (
            f"the {v.name}, {rec.get('how', 'taken')}, under "
            f"{rec.get('master') or 'a prize master'} "
            f"with a prize crew of {number_words(int(rec.get('crew', 0)))} and "
            f"{number_words(int(rec.get('prisoners', 0)))} prisoners, {goal_words}, {company}"
            + (f", {where}" if where else "")
        )
        words.append(w)
        items.append(
            {
                "id": v.id,
                "name": v.name,
                "how": rec.get("how"),
                "master": rec.get("master"),
                "crew": rec.get("crew"),
                "prisoners": rec.get("prisoners"),
                "goal": goal,
                "company": bool(rec.get("company")),
            }
        )
    return {"words": "; ".join(words), "count": len(mine), "items": items}


def _where_words(world: Any, v: Any) -> str:
    from freesail import units
    from freesail.world.geo import bearing_and_distance

    here = getattr(world, "position", None)
    if here is None or getattr(v, "position", None) is None:
        return ""
    bearing, distance = bearing_and_distance(here, v.position)
    nm = distance / units.NAUTICAL_MILE
    if nm > 20.0:
        return "out of sight"
    return f"bearing {units.point_name(units.deg_to_rad(bearing))}, {nm:.1f} miles"


def _prisoners(world: Any, _: str | None) -> dict[str, Any] | None:
    from freesail.world import prizes as P
    from freesail.world.captive import _captives_aboard

    ship = getattr(world, "ship", None)
    pris = P.prisoners_of(ship)
    captives = _captives_aboard(world) if pris is not None else []
    if pris is None or (pris.count == 0 and not captives):
        return {"words": "no prisoners", "count": 0}
    tick = int(world.clock.tick)
    named = []
    for p in captives:
        parole = pris.parole.get(p.name, "")
        at = R_place(p.confined_to) if p.confined_to else R_place(p.where)
        named.append(f"{p.name} in {at}" + (f" (parole {parole})" if parole else ""))
    words = pris.words(tick) if pris.count else ""
    if named:
        who = (
            f"{number_words(len(named))} prisoner{'s' if len(named) != 1 else ''} of rank"
            if not words
            else ""
        )
        words = (words + "; " if words else who + ": ") + ", ".join(named)
    return {
        "words": words,
        "count": pris.count,
        "fit": pris.fit,
        "confined": pris.confined,
        "irons": pris.in_irons(tick),
        "named": named,
        "parole": dict(pris.parole),
    }


def R_place(place: str) -> str:
    from freesail.world.places import PLACES

    p = PLACES.get(place)
    return p.name if p is not None else place


def _prize_crew(world: Any, _: str | None) -> dict[str, Any] | None:
    from freesail.crew.model import fatigue_words
    from freesail.world import prizes as P

    vessel = getattr(world, "vessel", None)
    rec = P.record_of(vessel) if vessel is not None else None
    if not rec or not P.is_prize(vessel):
        return {"words": "she is no prize", "prize": False}
    crew = (getattr(getattr(world, "ship", None), "extra", None) or {}).get("crew")
    sailors = list(getattr(crew, "sailors", []) or [])
    fit = sum(1 for s in sailors if s.fit)
    fatigue = sum(float(s.fatigue) for s in sailors) / len(sailors) if sailors else 0.0
    hours = (int(world.clock.tick) - int(rec.get("taken_at", 0))) / 3600.0
    words = (
        f"a prize crew of {number_words(len(sailors))} of the "
        f"{rec.get('captor_name', 'captor')}'s, "
        f"{number_words(fit)} fit, {fatigue_words(fatigue)}, {hours:.0f} hours since the taking, "
        f"under {rec.get('master') or 'a prize master'}"
    )
    return {
        "words": words,
        "prize": True,
        "crew": len(sailors),
        "fit": fit,
        "fatigue": round(fatigue, 2),
        "hours": round(hours, 1),
        "master": rec.get("master"),
    }


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "prize",
            ("the prize", "the prizes", "our prize", "our prizes"),
            "state",
            "",
            _prizes,
            description="every prize of this ship's: how she was taken, her prize master, the "
            "prize crew's and the prisoners' counts, her goal, in company or parted and where "
            "she lies; 'no prize'",
            none_words=_no_muster_words,
            where=("deck", "cabin"),
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "prisoners",
            ("the prisoners", "the prisoners aboard"),
            "state",
            "",
            _prisoners,
            description="the prisoners this ship holds: how many, where confined, in irons, the "
            "named with their parole; 'no prisoners'",
            none_words=_no_muster_words,
            where=("deck", "cabin", "gunroom", "hold"),
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "prize_crew",
            ("the prize crew",),
            "state",
            "",
            _prize_crew,
            description="on a prize: the men who work her, how many fit and how tired, the hours "
            "since the taking, the prize master; 'she is no prize' else",
            none_words=_no_muster_words,
            where=("deck", "cabin"),
        )
    )
    R._event(R.EventSpec("she is taken", "prize.taken"))
    R._event(R.EventSpec("possession taken", "prize.possessed"))
    R._event(R.EventSpec("the prisoners rising", "prize.rising"))
    R._event(R.EventSpec("the prize retaken", "prize.retaken"))
    R._event(R.EventSpec("a prize lost", "prize.lost"))
    R._event(R.EventSpec("a prize burnt", "prize.burnt"))
    R._event(R.EventSpec("the prisoners aboard", "prize.prisoners_aboard"))
    # the captive's channel (the design's §3)
    R._event(R.EventSpec("a captive aboard", "prize.captive"))
    R._event(R.EventSpec("the parole asked", "prize.parole_asked"))
    R._event(R.EventSpec("the parole given", "prize.parole"))
    R._event(R.EventSpec("the prisoners landed", "prize.prisoners_landed"))
    R._event(R.EventSpec("the cartel", "prize.cartel"))
