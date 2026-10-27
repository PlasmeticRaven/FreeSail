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
from freesail.crew.model import number_words

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


# -- the health's rows (spec M7 §16; package 73) ---------------------------------------------


def _crew(world: Any) -> Any:
    ship = getattr(world, "ship", None)
    return (getattr(ship, "extra", None) or {}).get("crew") if ship is not None else None


def _no_muster_words(world: Any) -> str | None:
    return "no ship's company is mustered" if _crew(world) is None else None


def _sick_list(world: Any, _: str | None) -> dict[str, Any] | None:
    crew = _crew(world)
    if crew is None:
        return None
    from freesail.crew.health import hurt_words

    listed = [s for s in crew.sailors if s.hurt in ("wounded", "sick")]
    light = [s for s in crew.sailors if s.hurt == "hurt"]
    dead = [s for s in crew.sailors if s.hurt == "killed"]
    if not listed and not light and not dead:
        return {"words": "none", "count": 0, "names": [], "light_duty": 0}
    names = [f"{s.name}, {hurt_words(s)}" for s in listed]
    words = f"{len(listed)} on the list: " + "; ".join(names) if listed else "nobody on the list"
    if light:
        words += f"; at light duty: {', '.join(s.name for s in light)}"
    if dead:
        words += f"; dead, to be buried: {', '.join(s.name for s in dead)}"
    return {
        "words": words,
        "count": len(listed),
        "names": [(s.name, s.hurt, getattr(s, "wound", "")) for s in listed],
        "light_duty": len(light),
        "dead": len(dead),
    }


def _wounded(world: Any, _: str | None) -> dict[str, Any] | None:
    crew = _crew(world)
    if crew is None:
        return None
    from freesail.crew.health import hurt_words

    wounded = [s for s in crew.sailors if s.hurt == "wounded"]
    if not wounded:
        return {"words": "none", "count": 0, "names": []}
    waiting = [s for s in wounded if not getattr(s, "dressed", False)]
    words = f"{len(wounded)}: " + "; ".join(f"{s.name}, {hurt_words(s)}" for s in wounded)
    if waiting:
        words += f"; {len(waiting)} not yet dressed"
    return {
        "words": words,
        "count": len(wounded),
        "waiting": len(waiting),
        "names": [(s.name, getattr(s, "wound", "")) for s in wounded],
    }


def _surgeon(world: Any, _: str | None) -> dict[str, Any] | None:
    crew = _crew(world)
    health = getattr(world, "health", None)
    if crew is None or health is None:
        return None
    surgeon = health.surgeon()
    mates = health.mates()
    if surgeon is None and not mates:
        return {
            "words": "no surgeon borne: the wounded are dressed by their messmates",
            "borne": False,
            "at_work": 0,
            "waiting": len(health.waiting()),
        }
    st = health.state
    at_work = len(st.at_work) if st is not None else 0
    waiting = len(health.waiting())
    where = "the cockpit" if (crew.all_hands_called_by == "quarters") else "the sick berth"
    name = f"the surgeon, {surgeon.name}" if surgeon is not None else "the surgeon's mate"
    if at_work:
        words = f"{name}, in {where}, at work on the wounded"
        words += f", {number_words(waiting)} waiting" if waiting else ""
    else:
        words = f"{name}, in {where}" + (", nobody under his hands" if not waiting else "")
    if mates:
        words += f"; {number_words(len(mates))} mate{'s' if len(mates) != 1 else ''}"
    return {
        "words": words,
        "borne": surgeon is not None,
        "name": surgeon.name if surgeon is not None else "",
        "mates": len(mates),
        "at_work": at_work,
        "waiting": waiting,
        "where": where,
    }


# -- the fight's rows (spec M7 §11, §11a; package 73) ------------------------------------------


def _marines(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None or _crew(world) is None:
        return None
    from freesail.combat.small_arms import describe

    return describe(world, ship)


def _small_arms(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None or _crew(world) is None:
        return None
    from freesail.combat.small_arms import musketry_of, small_arms_count, small_arms_of

    m = musketry_of(ship)
    arms = small_arms_of(world)
    n = small_arms_count(ship)
    what = str(arms.get("words") or "cutlasses, pikes, pistols and tomahawks")
    if m.served:
        fire = {"at will": "firing at will", "hold": "the muskets held"}[m.small_arms_mode]
        words = (
            f"served out ({what}); {number_words(n)} small-arms men with the stand of arms' "
            f"muskets, {fire}"
        )
    else:
        words = (
            f"in the arms chests ({what}; 'serve out the small arms'); {number_words(n)} "
            "small-arms men by the bill"
        )
    return {"words": words, "served": m.served, "mode": m.small_arms_mode, "men": n}


def _boarders(world: Any, _: str | None) -> dict[str, Any] | None:
    ship = getattr(world, "ship", None)
    if ship is None or _crew(world) is None:
        return None
    from freesail.combat.boarding import describe

    return describe(world, ship)


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "marines",
            ("the marines", "the detachment", "the marines' station"),
            "state",
            "",
            _marines,
            description="the marines: the detachment fit of its number, its officer and its "
            "kit, where it stands (the sentries and the drill; at quarters the poop and the "
            "gangways, the tops) and its fire (held, by volley, at will)",
            none_words=_no_muster_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "small_arms",
            ("the small arms", "the stand of arms", "the arms"),
            "state",
            "",
            _small_arms,
            description="the small arms: in the chests or served out, the small-arms men by "
            "the bill and their fire",
            none_words=_no_muster_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "boarders",
            ("the boarders", "the fight on deck", "the boarding", "the grapnels"),
            "state",
            "",
            _boarders,
            description="the boarders by the bill with their arms, whom she is grappled to, "
            "the fight on deck by rounds and losses, the gun crews up to repel boarders",
            none_words=_no_muster_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "sick_list",
            ("the sick list", "the sick", "the list"),
            "state",
            "",
            _sick_list,
            description="the sick list by name: the wounded and the sick with each man's "
            "hurt, the men at light duty, the dead to be buried; 'none'",
            none_words=_no_muster_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "wounded",
            ("the wounded", "the hurt"),
            "state",
            "",
            _wounded,
            description="the wounded by name with each wound, light or dangerous, and how "
            "many wait for the surgeon; 'none'",
            none_words=_no_muster_words,
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "surgeon",
            ("the surgeon", "the doctor", "the surgeon's work"),
            "state",
            "",
            _surgeon,
            description="the surgeon: borne or not, where he is, at work on the wounded or "
            "idle, how many wait, his mates",
            none_words=_no_muster_words,
        )
    )
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
        # the health's (package 73)
        ev("a man taken ill", "health.sick"),
        ev("a man dead", "health.died"),
        ev("a death", "health.died"),
        ev("the burial", "crew.buried"),
        ev("the morning report", "health.morning_report"),
        ev("the butcher's bill", "action.bill"),
        ev("the surgeon's report", "health.sick"),
        ev("a man collapsed", "person.collapsed"),
        ev("an officer killed", "person.killed"),
        ev("the command passes", "ship.command_passes"),
        # the fight's (package 73)
        ev("musketry", "action.musketry"),
        ev("the marines' fire", "action.musketry"),
        ev("grappled", "ship.grappled"),
        ev("the grapnels cast off", "ship.cast_off"),
        ev("the boarders away", "action.boarders"),
        ev("boarded", "action.boarded"),
        ev("the fight on deck", "action.boarding"),
        ev("a round of the fight", "action.boarding"),
        ev("the deck carried", "action.carried"),
        ev("the boarders repulsed", "action.repulsed"),
        ev("repel boarders", "action.repel"),
    ):
        R.EVENTS[spec.words] = spec
