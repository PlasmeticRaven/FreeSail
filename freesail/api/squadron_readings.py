"""The squadron's, the station's and the convoy's readings and events (spec M7 §21 to §23;
package 72; docs/design/Design-Squadrons.md), registered in the readings registry from this
module, which `readings` imports at its end after the signals'.

    the squadron          the set the ship commands or is a member of: its name and kind, the
                          commander, the formation and its interval, every member in her
                          order of sailing with whether she is in her station, the
                          stragglers, the divisions detached; "the ship is in no squadron"
    the station           her own station: the flag by name, the station wanted, in or out
                          of it as last kept by the lookout's bearing and distance
    the convoy            the squadron reading for a convoy (the same row, the convoy's words)
    the order of sailing  the formation's words and the order

A squadron is shown to the player by his own ship's membership (the set he commands, or the
one his ship is a member of) and never as the world's object: the other sets on the sea
are ships and signals to him. The rows ride a sample only while the ship is in a set or
has a station ordered (`idle_rows`). The events, for `at` and a stand-by: `a ship out of
her station` (`squadron.straggler`), `a straggler` (the same), `a ship regains her
station` (`squadron.in_station`), `out of station` and `in station` (the ship's own,
`sail.out_of_station`, `sail.in_station`), `the commodore makes a signal` (a signal read
from the ship she is under the orders of), `a division detached`, `the division recalled`,
`a ship lost to the convoy` (`squadron.lost`), `a ship cut out` (`squadron.cut_out`).
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.api import readings as R

__all__ = ["SQUADRON_ROWS", "idle_squadron_rows", "register"]

SQUADRON_ROWS: tuple[str, ...] = ("squadron", "station", "convoy", "order_of_sailing")


def _root(world: Any) -> Any:
    return getattr(world, "parent", None) or world


def _own_id(world: Any) -> str:
    vessel = getattr(world, "vessel", None)
    return str(vessel.id) if vessel is not None else "the ship"


def _set_of(world: Any) -> Any:
    sets = getattr(_root(world), "squadrons", None)
    if sets is None:
        return None
    own = _own_id(world)
    return sets.commanded_by(own) or sets.of(own)


def _name_of(root: Any, vid: str) -> str:
    if vid == "the ship":
        return str(getattr(getattr(root, "ship", None), "name", "the ship") or "the ship")
    v = root.vessels.get(vid)
    return str(getattr(v, "name", vid) or vid)


def _squadron(world: Any, _: str | None) -> dict[str, Any] | None:
    sq = _set_of(world)
    if sq is None:
        return None
    root = _root(world)
    own = _own_id(world)
    commander = _name_of(root, sq.commander)
    members = []
    for m in sq.members:
        row: dict[str, Any] = {"name": _name_of(root, m)}
        if m == sq.commander:
            row["commander"] = True
        elif m in sq.stragglers:
            row["station"] = "a straggler"
        else:
            off = sq.off_station_m.get(m)
            if off is None:
                row["station"] = "her station"
            else:
                row["station"] = (
                    "in station"
                    if off <= 2.0 * units.CABLE * 0.5
                    else f"{_cables(off)} out of her station"
                )
        d = sq.division_of(m)
        if d is not None and d.detached:
            row["division"] = d.name + (" (leader)" if d.leader == m else "")
        if m in sq.prizes:
            row["prize"] = True
        if m == own:
            row["this_ship"] = True
        members.append(row)
    kind_words = "convoy" if sq.kind == "convoy" else "squadron"
    bits = [
        f"{sq.name}, {commander} commanding" + (" (this ship)" if sq.commander == own else ""),
        f"{sq.formation}, {_cables(sq.interval_m)} apart",
    ]
    names = []
    for row in members:
        said = row["name"]
        if row.get("commander"):
            said += " (the commodore)"
        elif row.get("station") == "a straggler":
            said += " (a straggler)"
        elif row.get("station") and row["station"] != "in station":
            said += f" ({row['station']})"
        if row.get("division"):
            said += f", {row['division']} division"
        if row.get("prize"):
            said += " (a prize)"
        names.append(said)
    bits.append("the order of sailing: " + ", ".join(names))
    if sq.divisions:
        bits.append(
            "detached: "
            + "; ".join(
                f"the {d.name} division under {_name_of(root, d.leader)}"
                for d in sq.divisions.values()
                if d.detached
            )
        )
    if sq.rendezvous:
        bits.append(f"the rendezvous {sq.rendezvous}")
    return {
        "id": sq.id,
        "name": sq.name,
        "kind": kind_words,
        "commander": commander,
        "commanding": sq.commander == own,
        "formation": sq.formation,
        "interval_m": round(sq.interval_m),
        "members": members,
        "stragglers": [_name_of(root, m) for m in sq.stragglers],
        "divisions": [d.name for d in sq.divisions.values() if d.detached],
        "goal": sq.goal,
        "words": "; ".join(bits),
    }


def _convoy(world: Any, _: str | None) -> dict[str, Any] | None:
    sq = _set_of(world)
    if sq is None or sq.kind != "convoy":
        return None
    return _squadron(world, None)


def _order_of_sailing(world: Any, _: str | None) -> dict[str, Any] | None:
    sq = _set_of(world)
    if sq is None:
        return None
    root = _root(world)
    order = [_name_of(root, m) for m in sq.members]
    return {
        "formation": sq.formation,
        "interval_m": round(sq.interval_m),
        "columns": sq.columns if sq.formation == "order of sailing" else None,
        "order": order,
        "words": f"{sq.formation}, {_cables(sq.interval_m)} apart: " + ", ".join(order),
    }


def _station(world: Any, _: str | None) -> dict[str, Any] | None:
    from freesail.orders.station import station_reading

    return station_reading(world)


def _cables(m: float) -> str:
    from freesail.world.geo import distance_words

    return distance_words(m)


def _no_set_words(world: Any) -> str:
    return "the ship is in no squadron"


def idle_squadron_rows(world: Any) -> set[str]:
    """The squadron's rows to leave out of a sample now: all of them while the ship is in
    no set and has no station ordered, so that a ship alone carries nothing of them."""
    if _set_of(world) is not None:
        return set()
    extra = getattr(getattr(world, "ship", None), "extra", None) or {}
    if extra.get("station"):
        return set(SQUADRON_ROWS) - {"station"}
    return set(SQUADRON_ROWS)


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "squadron",
            ("the squadron", "our squadron", "the set"),
            "state",
            "",
            _squadron,
            description="the squadron the ship commands or is a member of: the commander, the "
            "formation, every member in her order of sailing and whether she is in her "
            "station, the stragglers, the divisions detached; 'the ship is in no squadron'",
            none_words=_no_set_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "convoy",
            ("the convoy", "our convoy"),
            "state",
            "",
            _convoy,
            description="the convoy the ship is commodore of or sails in: the merchantmen in "
            "their order with the stragglers; 'the ship is in no squadron'",
            none_words=_no_set_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "order_of_sailing",
            ("the order of sailing", "the formation", "the line"),
            "state",
            "",
            _order_of_sailing,
            description="the set's formation and its interval, and the order of sailing",
            none_words=_no_set_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "station",
            ("the station", "our station", "my station"),
            "state",
            "",
            _station,
            description="her own station in the set or on a ship named: the flag, the station "
            "wanted, and whether she is in it as last kept",
            none_words=lambda world: (
                "no station is kept: the ship is in no squadron and none has been ordered"
            ),
        )
    )
    ev = R.EventSpec
    for spec in (
        ev("a ship out of her station", "squadron.straggler"),
        ev("a straggler", "squadron.straggler"),
        ev("a ship regains her station", "squadron.in_station"),
        ev("out of station", "sail.out_of_station"),
        ev("in station", "sail.in_station"),
        ev("a ship lost to the convoy", "squadron.lost"),
        ev("a ship cut out", "squadron.cut_out"),
        ev("a ship parts company", "squadron.parted"),
        ev(
            "the commodore makes a signal",
            "signal.read",
            lambda d: bool(d.get("commander")),
        ),
        ev("a division detached", "squadron.detached"),
        ev("the division recalled", "squadron.recalled"),
    ):
        R.EVENTS[spec.words] = spec
