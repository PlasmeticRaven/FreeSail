"""The water's and the damage control's readings and events (spec M7 §13, §14; package
73), registered in the readings registry from this module, which `readings` imports at its
end as it imports the action's.

    the pumps         the ship's pumps: their kinds, manned by so many of so many hands and
                      lifting so many tons an hour, or not manned ('is manned', 'is not manned')
    the leaks         every source of water running now with its rate: the shot holes
                      unplugged, the ground's leak, a started seam, the seams working, the
                      sea over the hatches; 'none'
    the hatches       'open' or 'battened down'
    the water         the water in the ship in tons, the gain an hour and the pumps' lift

The well itself (`the well`) is the carpenter's last sounding as the hotfix left it, with
the keeper's gain and the pumps' state added to its words.

The events, for `at` and a stand-by: `the well rising` (`well.rising`), `the pumps gaining`
(`pumps.gaining`), `the pumps losing` (`pumps.losing`), `the pumps suck` (`pumps.sucked`),
`the leak stopped` (`leak.stopped`), `she is settling` (`ship.settling`), `she founders`
(`ship.foundered`), `the hatches battened` (`hatches.battened`), `a shot hole plugged`
(`hole.plugged`).
"""

from __future__ import annotations

from typing import Any

from freesail.api import readings as R

__all__ = ["register"]


def _water(world: Any) -> Any:
    return getattr(world, "water", None)


def _no_hull_words(world: Any) -> str | None:
    ship = getattr(world, "ship", None)
    if ship is None or getattr(ship, "hull", None) is None:
        return "she has no hull to make water through"
    return None


def _pumps(world: Any, _: str | None) -> dict[str, Any] | None:
    water = _water(world)
    if water is None or getattr(getattr(world, "ship", None), "hull", None) is None:
        return None
    d = water.pumps.describe()
    if not d["kinds"]:
        return {"words": "no pumps", "manned": False, "state": "none"} | d
    d["state"] = "manned" if d["manned"] else "not manned"
    return d


def _leaks(world: Any, _: str | None) -> dict[str, Any] | None:
    water = _water(world)
    if water is None or getattr(getattr(world, "ship", None), "hull", None) is None:
        return None
    leaks = water.leaks()
    if not leaks:
        return {"words": "none", "count": 0, "gain_t_per_h": 0.0, "items": []}
    parts = [f"{lk.words} ({lk.t_per_h:.1f} tons an hour)" for lk in leaks]
    gain = sum(lk.t_per_h for lk in leaks)
    return {
        "words": "; ".join(parts) + f"; {gain:.1f} tons an hour in all",
        "count": len(leaks),
        "gain_t_per_h": round(gain, 1),
        "items": [
            {"kind": lk.kind, "words": lk.words, "t_per_h": round(lk.t_per_h, 1)} for lk in leaks
        ],
    }


def _hatches(world: Any, _: str | None) -> dict[str, Any] | None:
    water = _water(world)
    if water is None or water.state is None:
        return None
    battened = bool(water.state.hatches_battened)
    return {"words": "battened down" if battened else "open", "battened": battened}


def _water_row(world: Any, _: str | None) -> dict[str, Any] | None:
    water = _water(world)
    if water is None or getattr(getattr(world, "ship", None), "hull", None) is None:
        return None
    d = water.describe()
    tons = d["tons"]
    words = f"{tons:.0f} tons in her" if tons >= 1.0 else "dry"
    if d["gain_t_per_h"] > 0.0:
        words += f", {d['gain_t_per_h']:.1f} tons an hour coming in"
    if d["pumped_t_per_h"] > 0.0:
        words += f", the pumps lifting {d['pumped_t_per_h']:.0f}"
    if d["foundered"] is not None:
        words = "foundered"
    d["words"] = words
    return d


def well_tail(world: Any) -> str:
    """The keeper's words after the sounding, for `the well`: ', gaining 12 tons an hour;
    the pumps lifting 30' or ', sucked dry at eight bells'."""
    water = _water(world)
    if water is None or water.state is None:
        return ""
    d = water.describe()
    bits = []
    if d["gain_t_per_h"] > 0.0:
        bits.append(f"gaining {d['gain_t_per_h']:.1f} tons an hour")
    if d["pumps"]["manned"]:
        bits.append(f"the pumps lifting {d['pumped_t_per_h']:.0f}")
    elif d["gain_t_per_h"] > 0.0:
        bits.append("the pumps not manned")
    if not bits and d["routine_pumped_tick"] is not None and d["tons"] < 0.5:
        clock = getattr(world, "clock", None)
        if clock is not None and clock.tick - int(d["routine_pumped_tick"]) < 4 * 3600:
            bits.append("sucked dry at the change of the watch")
    return ", " + "; ".join(bits) if bits else ""


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "pumps",
            ("the pumps", "the chain pumps", "the hand pumps"),
            "state",
            "",
            _pumps,
            description="the pumps: their kinds, manned by so many hands and lifting so many "
            "tons an hour, or not manned ('is manned', 'is not manned')",
            none_words=_no_hull_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "leaks",
            ("the leaks", "the leak", "where she makes water"),
            "state",
            "",
            _leaks,
            description="every source of water running now with its tons an hour: the shot "
            "holes unplugged, the ground's leak, a seam started, the seams working in the "
            "sea, the sea over open hatches; 'none'",
            none_words=_no_hull_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "hatches",
            ("the hatches", "the hatchways"),
            "state",
            "",
            _hatches,
            description="the hatches: open, or battened down",
            none_words=_no_hull_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "water",
            ("the water in the ship", "the water in her", "the water aboard"),
            "state",
            "",
            _water_row,
            description="the water in the ship in tons, the gain an hour and the pumps' lift; "
            "'dry'; 'foundered'",
            none_words=_no_hull_words,
        )
    )
    ev = R.EventSpec
    for spec in (
        ev("the well rising", "well.rising"),
        ev("the pumps gaining", "pumps.gaining"),
        ev("the pumps losing", "pumps.losing"),
        ev("the pumps suck", "pumps.sucked"),
        ev("the leak stopped", "leak.stopped"),
        ev("a shot hole plugged", "hole.plugged"),
        ev("she is settling", "ship.settling"),
        ev("she founders", "ship.foundered"),
        ev("the ship founders", "ship.foundered"),
        ev("the hatches battened", "hatches.battened"),
    ):
        R.EVENTS[spec.words] = spec
