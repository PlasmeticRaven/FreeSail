"""Read-only state queries for views and agents: the snapshot and the ship graph.

`snapshot(world)` is the state a view redraws from (spec §9.4): the clock,
the hull's motion, the wind, every sail, spar and line, the evolutions in
progress, and the watch (`crew`, spec M3 §5.2; None for a ship without a
crew). The crew's lines for the console's `state` and its `muster` are here
too (`watch_lines`, `sail_set_line`, `muster_lines`).

`ship_graph(ship)` is what a view *builds* from once: every
spar with its class, position and dimensions, every sail with its roles
and area, the hull's dimensions, groups and aliases. Both are plain
dictionaries of SI numbers; the client converts for display.

Neither function changes anything. Both work on a World whose ship is the
milestone 0 point ship (no parts): the part lists are then empty.
"""

from __future__ import annotations

from typing import Any

from freesail.api import readings
from freesail.core.world import World
from freesail.crew import bill
from freesail.crew.model import Crew, Station, Watch
from freesail.physics.sails import SAIL_CLASSES
from freesail.ship.form import stations as drawn_stations
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, Sail, SailState, Spar, booms, sail_room
from freesail.ship.schema import PROFILE_KEYS, STERN_KEYS, HullForm, HullProfile


def weather_block(world: World) -> dict[str, Any]:
    """The instruments' weather: the glass in inches, its tendency's words, the sky with
    its signs, the weather and the visibility, each None where not to be had, with the
    words the registry gives for that (`readings.reading_words`)."""
    r = world.readings
    tendency = r["tendency"]
    sky = r["sky"]
    visibility = r["visibility"]
    sea = r["sea"]
    motion = r["motion"]
    return {
        "glass_in": r["glass"],
        "tendency": tendency["words"] if tendency else None,
        "tendency_words": r.words("tendency"),
        "glass_words": r.words("glass"),
        "sky": sky["words"] if sky else None,
        "signs": sky["signs"] if sky else None,
        "weather": r["weather"],
        "visibility": visibility["words"] if visibility else None,
        "visibility_miles": visibility["miles"] if visibility else None,
        "sky_words": r.words("sky"),
        # the sea and the motion (spec M5 §4): the words, and the numbers behind them
        "sea": sea["words"] if sea else None,
        "sea_from": sea["from"] if sea else None,
        "sea_height_m": sea["height_m"] if sea else None,
        "sea_words": r.words("sea"),
        "motion": motion["words"] if motion else None,
        "roll_deg": motion["roll_deg"] if motion else None,
        "pitch_deg": motion["pitch_deg"] if motion else None,
    }


def weather_lines(world: World) -> list[str]:
    """The console's `state` line for the weather, when the scenario keeps one: 'The
    glass 29.72, falling; overcast, drizzle; a few miles.'"""
    out = []
    r = world.readings
    if getattr(world, "conditions", None) is not None:
        parts = []
        if r["glass"] is not None:
            tendency = r["tendency"]
            words = f", {tendency['words']}" if tendency else ""
            parts.append(f"The glass {r['glass']:.2f}{words}")
        else:
            parts.append("No glass aboard")
        parts.append(r.words("sky") + ", " + r.words("weather"))
        parts.append(r.words("visibility"))
        out.append("; ".join(parts) + ".")
    if getattr(world, "sea", None) is not None:
        # the sea and the motion (spec M5 §4): 'A heavy sea from the north-westward;
        # rolling heavily.'
        from freesail.world.sea import quarter_words

        sea = r["sea"]
        words = sea["words"]
        if "from" not in words:
            words += f" from {quarter_words(sea['from'])}"
        out.append(f"{words[:1].upper()}{words[1:]}; {r.words('motion')}.")
    return out


def lookout_lines(world: World) -> list[str]:
    """The console's `state` line for the lookout (spec M5 §12), when the scenario has a
    chart: 'In sight: the Lizard bearing N by E, distant four leagues.' or 'Nothing in
    sight.'; nothing without a chart."""
    r = world.readings
    if getattr(world, "lookout", None) is None:
        return []
    sight = r["in_sight"]
    if not sight or not sight["count"]:
        return ["Nothing in sight."]
    return [f"In sight: {sight['words']}."]


def chart_block(world: World) -> dict[str, Any] | None:
    """The captain's chart for the browser (spec M5 §17, the first half; package 32):
    the region, its bounds, the coast as polylines of [lon, lat], the features with
    their kind, name and position (a light with its dates), and the attribution the
    game shows. Built once and fetched once (`/api/chart`); None without a chart. The
    truth's depth tiles are never in it."""
    chart = getattr(world, "chart", None)
    if chart is None:
        return None
    south, north, west, east = chart.bounds
    return {
        "region": chart.region,
        "title": chart.spec.get("title", chart.region),
        "bounds": {"south": south, "north": north, "west": west, "east": east},
        "coast": chart.coast_lines(),
        "features": [
            {
                "id": f.id,
                "kind": f.kind,
                "name": f.name,
                "lat_deg": f.lat_deg,
                "lon_deg": f.lon_deg,
                **({"lit": dict(f.lit)} if f.lit else {}),
                **({"marks": list(f.marks), "bearing_deg": f.bearing_deg} if f.marks else {}),
            }
            for f in chart.features.values()
        ],
        "attribution": chart.attribution(),
    }


def reckoning_block(world: World) -> dict[str, Any] | None:
    """The reckoning for the captain's chart (spec M5 §17; package 33a): what
    `world.reckoning.Navigation.to_dict` gives, through the registry's own reading of the
    position by account so that the chart and a rule read one account; None on the plane."""
    nav = getattr(world, "navigation", None)
    if nav is None:
        return None
    block = nav.to_dict()
    reading = world.readings["reckoning"]
    if reading is not None:
        block["lat_deg"] = round(reading["lat_deg"], 5)
        block["lon_deg"] = round(reading["lon_deg"], 5)
        block["words"] = reading["words"]
    return block


def reckoning_lines(world: World) -> list[str]:
    """The console's `state` lines for the reckoning (spec M5 §15): the position by
    account with the master's doubt, and the last cast; nothing on the plane."""
    r = world.readings
    if getattr(world, "navigation", None) is None:
        return []
    where = r.words("reckoning")
    out = [f"{where[:1].upper()}{where[1:]}. {r['reckoning_uncertainty']['words']}"]
    if r["depth"] is not None:
        out.append(f"The last cast: {r.words('depth')}; {r.words('ground')}.")
    return out


def _spar_state(s: Spar) -> str:
    if s.wrecked and s.sent_down:
        return "cleared"  # carried away, its wreck cleared: on deck or over the side (30b)
    if s.wrecked:
        return "wrecked"
    if s.sent_down:
        return "sent_down"
    return "sound"


def _sail_state(s: Sail) -> str:
    return "wrecked" if s.wrecked else s.state.value


def snapshot(world: World) -> dict[str, Any]:
    """The state a view redraws from. SI units; see spec §9.4.

    The instrument values (the wind, the apparent wind, the heading, the speed, the
    leeway, the heel, the helm, the bell, each sail's state and every part's strain)
    come through the readings registry (`World.readings`, spec M4 §2), the same view a
    standing order tests and an agent asks for. The shape the client sees is unchanged.
    """
    ship = world.ship
    wind = world.wind
    r = world.readings
    out: dict[str, Any] = {
        "tick": world.clock.tick,
        "ship_time": world.clock.ship_time.isoformat(),
        "stamp": world.clock.stamp(),
        "bell": dict(r["time"]),
        "wind": {
            "true_from": r["true_wind_from"],
            "true_speed": r["true_wind_speed"],
            "mean_speed": wind.speed,
            "gust_factor": wind.gust_factor,
            "squall": bool(getattr(wind, "in_squall", False)),
        },
        # the weather's readings (spec M5 §5), through the registry: None where the ship
        # has no glass or the scenario keeps no sky
        "weather": weather_block(world),
        # the lookout's reading (spec M5 §12), None without a chart
        "lookout": r["in_sight"],
        # the other sail in sight (spec M5 §25, package 36): each by her bearing and her
        # distance by estimation with what has been made out, for the captain's chart to
        # draw at that bearing and distance from the account; never her position
        "strangers": r["strangers"],
        # the captain's chart (spec M5 §17, package 33a): the reckoned position brought up
        # to now and its ellipse, the track by account, the noons, the bearings taken, the
        # soundings with their ground, the master; None on the plane. The truth's position
        # is not in the snapshot: it is in the save and the tests only
        # (`world.reckoning.Navigation.to_dict`).
        "reckoning": reckoning_block(world),
    }
    # On the sphere the ship's plane metres from the start are the truth's track, and the
    # chart is drawn about the reckoning; they leave the snapshot with the position.
    on_the_sphere = getattr(world, "position", None) is not None
    if not isinstance(ship, Ship):
        st = ship.state()
        out["ship"] = {
            "name": st.get("name", "point"),
            "x": None if on_the_sphere else st.get("x", 0.0),
            "y": None if on_the_sphere else st.get("y", 0.0),
            "heading": r["heading"],
            "speed_through_water": r["speed"],
            "leeway": r["leeway"],
            "heel": r["heel"],
            "rudder": r["helm"],
            "weather_helm": 0.0,
            "tack": "starboard",
            "helm_mode": "heading",
            "target_heading": r["course"],
        }
        out["wind"]["apparent_angle"] = r["apparent_wind_angle"]
        out["wind"]["apparent_speed"] = r["apparent_wind_speed"]
        out["sails"] = []
        out["spars"] = []
        out["lines"] = []
        out["evolutions_in_progress"] = []
        out["crew"] = None
        out["agents"] = agents_state(world)
        return out

    d = ship.dyn
    out["ship"] = {
        "name": ship.name,
        "x": None if on_the_sphere else d.x,
        "y": None if on_the_sphere else d.y,
        "heading": r["heading"],
        "speed_through_water": r["speed"],
        "leeway": r["leeway"],
        "heel": r["heel"],
        "rudder": r["helm"],
        "weather_helm": d.weather_helm,
        "tack": d.tack,
        "helm_mode": d.helm_mode.value,
        "target_heading": d.target_heading,
    }
    out["wind"]["apparent_angle"] = r["apparent_wind_angle"]
    out["wind"]["apparent_speed"] = r["apparent_wind_speed"]
    out["sails"] = [
        {
            "id": s.id,
            "class": s.cls,
            "state": r.value("sail", s.id)["state"],
            "reefs": s.reefs,
            "area_effective": s.area_effective_m2,
            "thrust": s.thrust_kn,
            "side": s.side_force_kn,
            "strain_ratio": r.value("strain", s.id),
            "backed": s.backed,
            "shivering": s.shivering,  # a studding sail too near the wind (spec 3b §7)
            "sheet_angle": s.sheet_angle,
            "lug_side": _lug_side(ship, s),  # package 57: a lug drawn on its side of the mast
            # package 75: a settee's yard lowered on deck to be dipped, only while it is
            **_only_when_true(s, "yard_lowered"),
        }
        for s in ship.sails.values()
    ]
    out["spars"] = [
        {
            "id": s.id,
            "class": s.cls,
            "state": _spar_state(s),
            "condition": s.condition,
            "strain_ratio": r.value("strain", s.id),
            "brace_angle": s.brace_angle,
            "rigged_out": s.rigged_out,  # studding sail booms, a driver's boom; true for the rest
        }
        for s in ship.spars.values()
    ]
    out["lines"] = [
        {
            "id": ln.id,
            "class": ln.cls,
            "state": ln.state.value,
            "strain_ratio": r.value("strain", ln.id),
            "hauled": ln.hauled,
        }
        for ln in ship.lines.values()
    ]
    runner = ship.extra.get("evolutions")
    out["evolutions_in_progress"] = list(runner.in_progress()) if runner is not None else []
    out["crew"] = crew_state(world)
    out["agents"] = agents_state(world)
    return out


def agents_state(world: World) -> list[dict[str, Any]]:
    """The agents at their stations (spec M4 §11): station, state, last sampled, and the
    question a pause puts to the human. Empty when none is stationed."""
    return [agent.snapshot() for agent in world.agents.values()]


def _spar_entry(s: Spar) -> dict[str, Any]:
    return {
        "id": s.id,
        "class": s.cls,
        "x_m": s.x_m,
        "height_m": s.height_m,
        "length_m": s.length_m,
        "parent": s.parent,
        "side": s.side,
        "brace_angle": s.brace_angle,
        "brace_limit": s.brace_limit,
        "rake": s.rake,
        "rating_kn": s.rating_kn,
        "rigged_out": s.rigged_out,  # studding sail booms, a driver's boom; true for the rest
    }


def _sail_entry(s: Sail) -> dict[str, Any]:
    # the reef factor by `Sail.curve_class` (package 75: the gaff's for a lateen cut at the
    # mast, as the physics will take it from the engine's lateen step; else its own class)
    cls = SAIL_CLASSES.get(s.curve_class)
    return {
        "id": s.id,
        "class": s.cls,
        "roles": dict(s.roles),
        "area_m2": s.area_m2,
        "x_m": s.x_m,
        "centre_height_m": s.centre_height_m,
        "reef_bands": s.reef_bands,
        "reef_factor": cls.reef_factor if cls is not None else 0.0,
        "side": s.side,
        "state": _sail_state(s),
        "reefs": s.reefs,
        "sheet_angle": s.sheet_angle,
        # package 57: the drawing's lug on its side, the flying sail sent down, the cut
        "dipping": s.dipping,
        "flying": s.flying,
        "sheeted_to": s.sheeted_to,
        "corners_m": _corners_of(s),
        # package 75: a settee and a lateen cut at the mast, each only where the file says
        **_only_when_true(s, "settee", "cut_at_mast"),
    }


def _only_when_true(s: Sail, *keys: str) -> dict[str, bool]:
    """Package 75's keys on a sail (docs/design/Design-ShipsEngineExtensions.md §6.4), each
    served as true where it holds and left out where it does not, so that the graph and the
    snapshot of a ship without them are as before them."""
    return {key: True for key in keys if getattr(s, key, False)}


def _corners_of(s: Sail) -> list[list[float]] | None:
    spec = getattr(s, "corners_m", None)
    return [[float(x), float(z)] for x, z in spec] if spec else None


def _lug_side(ship: Ship, s: Sail) -> str | None:
    """The side of its mast a lug lies on (package 43b), a lug topsail its lower lug's
    (package 57: its clew is sheeted to that lug's yard)."""
    host = ship.sails.get(s.sheeted_to) if s.sheeted_to else None
    return host.lug_side if host is not None else s.lug_side


def _line_entry(ln: Line) -> dict[str, Any]:
    # `hauled`: a bowline's hauled out or not (spec 3b §4), drawn faintly when it is (§8)
    return {
        "id": ln.id,
        "class": ln.cls,
        "of": ln.of,
        "side": ln.side,
        "state": ln.state.value,
        "hauled": ln.hauled,
    }


def _profile_entry(p: HullProfile) -> dict[str, Any]:
    """The hull's profile as her file gives it (package 75; docs/design/Build-Ships.md §5.1,
    §6), in plain lists in `PROFILE_KEYS`' order: each line a list of points, `decks_m`,
    `ports_m` and `port_size_m` mappings by deck word; from stage 0H the shape keys, the
    `form` and the `marks` as mappings in the file's form (§5.1). A line the file does not
    give is left out, as it is out of the file."""
    out: dict[str, Any] = {}
    for key in PROFILE_KEYS:
        value = getattr(p, key)
        if not value:
            continue
        if key in ("decks_m", "ports_m"):
            out[key] = {word: [list(pt) for pt in pts] for word, pts in value}
        elif key == "port_size_m":
            out[key] = {word: list(size) for word, size in value}
        elif key == "form":
            out[key] = _form_entry(value)
        elif key == "marks":
            out[key] = dict(value)
        else:
            out[key] = [list(pt) for pt in value]
    return out


def _form_entry(form: HullForm) -> dict[str, Any]:
    """The profile's `form` as her file gives it (stage 0H; Build-Ships.md §5.1): the fullness,
    the stern by its keys in the file's order and the head's word, each only where given."""
    out: dict[str, Any] = {}
    if form.fullness is not None:
        out["fullness"] = list(form.fullness)
    if form.stern is not None:
        stern: dict[str, Any] = {}
        for key in STERN_KEYS:
            value = getattr(form.stern, key)
            if value is None or value == ():
                continue
            if key in ("galleries_m", "lights_m"):
                stern[key] = [list(pt) for pt in value]
            elif key == "transom_hb_m":
                stern[key] = list(value)
            else:
                stern[key] = value
        out["stern"] = stern
    if form.head is not None:
        out["head"] = form.head
    return out


def _station_entry(station: tuple[tuple[float, float, float], ...]) -> list[list[float]]:
    """A drawn station (`freesail.ship.form`) as plain lists of [x, z, hb], to the millimetre."""
    return [[round(c, 3) + 0.0 for c in pt] for pt in station]  # + 0.0: never a "-0.0"


def ship_graph(ship: Ship) -> dict[str, Any]:
    """Everything a drawing needs to build the ship once: parts, dimensions, roles.

    Spars carry their class, `x_m` (root spars only; a child spar stands at its
    parent's x), `height_m`, `length_m`, parent, side and brace angle. Sails
    carry class, roles, area, state, reefs, sheet angle and centre height.
    The hull carries its principal dimensions, and its profile where the file gives one
    (package 75: the side, the decks and the ports; absent otherwise), with the hull as drawn
    from it (stage 0H: `stations`, `freesail.ship.form`'s, the ends' closures first and last,
    each station's [x, z, hb] from its lowest point up to the rail). SI throughout.
    """
    h = ship.hull.spec
    hull: dict[str, Any] = {
        "length_waterline_m": h.length_waterline_m,
        "beam_m": h.beam_m,
        "draught_m": h.draught_m,
        "deck_height_m": h.deck_height_m,
        "displacement_kg": h.displacement_kg,
        "gm_m": h.gm_m,
        "clr_x_m": h.clr_x_m,
    }
    profile = getattr(h, "profile", None)
    if profile is not None:
        hull["profile"] = _profile_entry(profile)
        hull["stations"] = [_station_entry(s) for s in drawn_stations(h)]
    return {
        "name": ship.name,
        "rig": ship.spec.rig,
        "hull": hull,
        "spars": [_spar_entry(s) for s in ship.spars.values()],
        "sails": [_sail_entry(s) for s in ship.sails.values()],
        "lines": [_line_entry(ln) for ln in ship.lines.values()],
        "groups": {g: list(m) for g, m in ship.groups.items()},
        "aliases": dict(ship.aliases),
    }


# ---------------------------------------------------------------------------
# The ship's company (spec M3 §5.2)
# ---------------------------------------------------------------------------

# Fatigue means are given to three places: finer than the eye can use, coarse enough that a
# snapshot does not change every tick for a hand standing idle. The constant lives with the
# readings (spec M4 §2), which the `hands on deck` reading and this snapshot share.
FATIGUE_DECIMALS = readings.FATIGUE_DECIMALS


def _crew(world: World) -> Crew | None:
    extra = getattr(world.ship, "extra", None) or {}
    crew = extra.get("crew")
    return crew if isinstance(crew, Crew) else None


def _at_work(world: World) -> list[dict[str, Any]]:
    """The work that holds hands now, in the order it was given: evolution, subject, hands,
    and the work in words for a view ('at the fore topsail', 'tacking ship')."""
    runner = (getattr(world.ship, "extra", None) or {}).get("evolutions")
    if runner is None:
        return []
    out = []
    for e in runner.in_progress():
        if e.get("hands"):
            entry = {"evolution": e["id"], "subject": e["subject"], "hands": e["hands"]}
            entry["words"] = _work_words(world, entry)
            out.append(entry)
    return out


def crew_state(world: World) -> dict[str, Any] | None:
    """The watch for the snapshot: who has the deck, how many are there and at what, and
    how tired the deck and the watch below are. None when the ship has no crew."""
    crew = _crew(world)
    if crew is None:
        return None
    when = world.clock
    deck = bill.on_deck(crew, when)
    turned = sorted(
        {s.watch.value for s in crew.sailors if s.turned_up and s.watch is not Watch.NONE}
    )
    r = world.readings  # the hands' count and fatigue are readings (spec M4 §2)
    return {
        "watch_on_deck": bill.watch_on_deck(crew, when).value,
        "on_deck": r["hands_on_deck"]["count"],
        "idle": sum(1 for s in deck if s.at is None),
        "at_work": _at_work(world),
        "all_hands": crew.all_hands_called,
        "fatigue_mean_on_deck": r["hands_on_deck"]["fatigue"],
        "fatigue_mean_below": r["watch_below"]["fatigue"],
        "idlers_up": bill.idlers_up(when),
        "turned_up": turned,
    }


def _work_words(world: World, entry: dict[str, Any]) -> str:
    """'at the fore topsail', 'tacking ship', 'sending down topgallant masts'."""
    from freesail.evolutions.runner import gerund, part_name

    ship = world.ship
    if entry["subject"] in ship.parts:
        return f"at the {part_name(ship, entry['subject'])}"
    verb = entry["evolution"].replace("_", " ")
    first, _, rest = verb.partition(" ")
    rest = rest or ("ship" if first in ("tack", "wear") else "")
    return f"{gerund(first)} {rest}".rstrip()


def watch_lines(world: World) -> list[str]:
    """The console's `state` lines for the crew (spec M3 §5.2): the watch on deck, and
    'All hands called' when they are. Empty for a ship without a crew."""
    crew = _crew(world)
    if crew is None:
        return []
    state = crew_state(world)
    assert state is not None
    work = state["at_work"]
    busy = sum(w["hands"] for w in work)
    line = f"Watch on deck: {state['watch_on_deck']}, {state['on_deck']} hands, "
    if work:
        parts = [f"{w['hands']} {w['words']}" for w in work]
        line += f"{busy} at work ({', '.join(parts)})"
    else:
        line += "none at work"
    extras: list[str] = []
    others = [w for w in state["turned_up"] if w != state["watch_on_deck"]]
    if others and not crew.all_hands_called:
        extras.append(f"the {' and '.join(others)} watch turned up")
    if crew.by_station[Station.IDLERS]:
        extras.append("idlers up" if state["idlers_up"] else "idlers below")
    line += "".join(f"; {e}" for e in extras) + "."
    lines = [line]
    routine = (getattr(world.ship, "extra", None) or {}).get("routine")
    if crew.all_hands_called:
        whose = getattr(crew, "all_hands_called_by", "") or "the captain's"
        by = f" by {whose} order" if crew.all_hands_called_by_order else ""
        lines.append(f"All hands called{by}.")
    elif getattr(routine, "calling", False):
        lines.append("All hands called; the watch below coming up.")
    return lines


def sail_set_line(ship: Any) -> str:
    """'Sail set: ...' with the states milestone 3 added: a goose-winged sail is listed
    with the set ones and says so; unbent sails and the spars sent down follow."""
    drawing = [
        s.id + (" (goose-winged)" if s.state is SailState.GOOSE_WINGED else "")
        for s in ship.sails.values()
        if s.is_set or (s.state is SailState.GOOSE_WINGED and not s.wrecked)
    ]
    line = "Sail set: " + (", ".join(drawing) if drawing else "none")
    unbent = [s.id for s in ship.sails.values() if s.state is SailState.UNBENT]
    if unbent:
        line += "; unbent: " + ", ".join(unbent)
    down = [
        s.id
        for s in ship.spars.values()
        if s.sent_down and not (s.parent and ship.spars[s.parent].sent_down)
    ]
    if down:
        line += "; sent down: " + ", ".join(down)
    return line


def muster_lines(world: World) -> list[str]:
    """The muster (spec M3 §5.1): the watch bill station by station, and the posts."""
    crew = _crew(world)
    if crew is None:
        return ["There is no ship's company mustered in this ship."]
    sail_room(world.ship)  # gives the crew its sail room for the muster's line (spec 3b §6.3)
    lines = crew.describe(world.clock)
    people = getattr(world, "people", None)
    if people is not None and getattr(people, "_built", False):
        # the named few in their places (spec M7b §14; package 53, truth 100): where each
        # is, by his state, as `the people` says it; once they are mustered, so that the
        # muster (a driver's query, never replayed) musters nobody
        lines.append(
            "The people's places: "
            + "; ".join(f"{p.name}, {people.state_words(p)}" for p in people.all)
            + "."
        )
    return lines


def sail_room_lines(world: World) -> list[str]:
    """The `the sail room` query (spec 3b §6.3): every sail in it, by kind of canvas."""
    return sail_room(world.ship).inventory_lines()


# The words of the `the booms` query (package 30b), as the console takes them; the ship
# takes the same words through the vocabulary (`the booms`, object `query`).
BOOMS_QUERIES = (
    "the booms",
    "booms",
    "the spare spars",
    "spare spars",
    "show the booms",
    "show the spare spars",
)


def booms_lines(world: World) -> list[str]:
    """The `the booms` query (package 30b): the spare spars aboard, by class, in the form
    of `the sail room`. A ship with no parts has none."""
    ship = world.ship
    if not hasattr(ship, "spars"):
        return ["There are no booms in this ship."]
    return booms(ship).inventory_lines()
