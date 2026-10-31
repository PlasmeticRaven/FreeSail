"""The boat as a hull of the one world (package 82, item 4; the design's §5.3).

A ship's boat with a file of her own (`BoatSpec.file`, the five patterns `data/ships/boat-
*.yaml`) becomes a vessel of the sea with a hull of her own **when she is commanded**: `go
to the boat` (the player or a stationed person goes down into her to take her), `tow her
with the boat` (item 5) or `pull for ...` after `go to the boat`. She is put on the sea by
`Vessels.add` (her id `<her ship's id>:<boat id>`, her name "the Raven's boat", `boat=True`
so that she is seen within `BOAT_SEEN_NM` and no farther, her nation her ship's, her file
the pattern's, no brain: she is commanded or she is alongside), her hull made by
`crews.make_hull` from her file at her ship's truth a boat's length off the ship's lee
quarter, awake, her company mustered from her file (the coxswain and the oarsmen), the person
who commands her put aboard her by `movement.put_aboard` with his station following (his
harness or his seat, the design's §2; the drivers follow the player). Her errands as before
when nobody commands her: the prices, a letter, a passenger landed or fetched, the kedge laid
out, the pilot's cutter, the lighter's and the hoy's jobs run as they do by the script or the
port's jobs, with no hull made and no line moved. The one new road into the boat is to
command her.

Her tick is a hull's: the World's tick with her current, her physics by the oars
(`physics/oars.py`) and the lug, her lookout a man standing in her, her log her own while she
is away; `tick_boat` once a minute steers her for the coxswain's mark (`pull for`), brings
her alongside and hoists her in (`come alongside`: her people aboard the ship, the one who
commanded her back at his station, her log's notable lines folded into the ship's as
`boat.log` entries, her vessel gone from the sea and her hull released), and swamps her in a
sea above her weather. **The boat lost** is a state the ship's `BoatState` knows (`lost`,
with the word: swamped, stove, cut adrift); a boat lost is sent on no errand and manned by
nobody until the yard's job at a port replaces her (`demand a boat of the yard`, two days).
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.orders.errors import OrderError
from freesail.world.geo import distance_words

__all__ = [
    "ALONGSIDE_M",
    "BOAT_DECK",
    "BOAT_WORDS",
    "SWAMP_STATES_LARGE",
    "SWAMP_STATES_SMALL",
    "come_alongside",
    "cut_adrift",
    "go_to_boat",
    "hoist_in",
    "is_boat",
    "lose_boat",
    "man_boat",
    "manned_hull",
    "ship_of",
    "tick_boat",
]

# Where a person stands in a boat (the hull's one deck place): "on the deck" in the places'
# words, "in the boat" in `where am I`'s.
BOAT_DECK = "deck"
# The words that name a boat in `go to the boat` and her kin (the file's kinds and the
# hands' words); a boat of the ship's by her own name beside them.
BOAT_WORDS = frozenset(
    {"boat", "launch", "cutter", "yawl", "jolly boat", "gig", "barge", "pinnace", "long boat"}
)
# Within this of her ship (metres), the boat is alongside and may be hoisted in: a boat's
# length and a little (judgement).
ALONGSIDE_M = 25.0
# A boat is hoisted out with the ship hove to or at anchor, not under way (the period's
# practice; the bound a hove-to ship's forereach and drift, judgement): knots in m/s.
HOIST_OUT_WAY_MS = 2.0 * 0.514444
# Hoisted out, she lies this far off the ship's lee quarter (metres; judgement: a boat's
# length clear of the side).
HOIST_OUT_OFF_M = 15.0
# Within this of a port's shore (metres), the boat is at the quay (a cable: the shore's spot
# is a point of the chart, and the boat takes the ground or lies off the steps; judgement).
QUAY_M = 200.0
# The sea's states a boat is swamped in when she is away under oars or sail (the design's
# §5.3; judgement): beyond "moderate" for a boat under twenty feet, beyond "short" for a
# launch or a cutter (`world.sea.SEA_STATE_WORDS`: smooth, moderate, short, heavy, very heavy).
SWAMP_STATES_SMALL = frozenset({"short", "heavy", "very heavy"})
SWAMP_STATES_LARGE = frozenset({"heavy", "very heavy"})
SMALL_BOAT_FT = 20.0
# The yard's time to find a ship a new boat (hours; judgement: two days), and the chandlers'
# price for one (pounds; judgement).
NEW_BOAT_HOURS = 48.0
NEW_BOAT_POUNDS = 25.0


# ---------------------------------------------------------------------------
# reading a hull
# ---------------------------------------------------------------------------


def is_boat(hull: Any) -> bool:
    """Whether a hull (or a World read at its current hull) is a boat's: her file has oars."""
    ship = getattr(hull, "ship", None)
    return getattr(getattr(ship, "spec", None), "oars", None) is not None


def ship_of(world: Any, boat_hull: Any) -> Any:
    """The hull of the ship a boat belongs to; None for a hull that is no ship's boat."""
    sid = boat_hull.__dict__.get("boat_of") if hasattr(boat_hull, "__dict__") else None
    return (getattr(world, "hulls", None) or {}).get(str(sid)) if sid else None


def manned_hull(world: Any, ship_hull: Any) -> Any:
    """The hull of the ship's boat manned and away, None when she is at the booms, on an
    errand of the script's, or lost."""
    dealings = getattr(ship_hull, "dealings", None)
    hid = str(getattr(getattr(dealings, "boat", None), "hull", "") or "")
    return (getattr(world, "hulls", None) or {}).get(hid) if hid else None


def boat_named(ship_hull: Any, words: str = "") -> Any:
    """The boat of the ship's file the words name ('the launch', 'the cutter', 'the boat'):
    with no words, the first that has a file of her own; by her name, her kind or her id.
    None for no boat; a boat without a file is returned too, for the refusal's words."""
    spec = getattr(getattr(ship_hull, "ship", None), "spec", None)
    boats = list(getattr(spec, "boats", None) or [])
    if not boats:
        return None
    key = " ".join(str(words or "").lower().split()).removeprefix("the ").strip()
    if not key or key == "boat":
        with_file = [b for b in boats if getattr(b, "file", None)]
        if with_file and (not key or len(boats) == 1 or key == "boat"):
            named = [b for b in with_file if b.name.lower().removeprefix("the ") == "boat"]
            return named[0] if named else with_file[0]
        return boats[0]
    for b in boats:
        if key in (b.id.lower().replace("_", " "), b.name.lower().removeprefix("the "), b.kind):
            return b
    return None


# ---------------------------------------------------------------------------
# manning her
# ---------------------------------------------------------------------------


def man_boat(world: Any, ship_hull: Any, words: str = "", by: str = "") -> tuple[Any, str]:
    """The ship's boat manned as a hull of the world: (her hull, the words). Refused in
    words for a ship with no boat, a boat with no file of her own, a boat away on an
    errand, one manned already, or one lost."""
    from freesail.world.crews import make_hull
    from freesail.world.ports import BoatState
    from freesail.world.ships import BOAT_SEEN_NM, Vessel

    dealings = getattr(ship_hull, "dealings", None)
    if dealings is None:
        raise OrderError("She has no boat to man: no dealings are kept for her.")
    spec = boat_named(ship_hull, words)
    if spec is None:
        boats = getattr(getattr(ship_hull.ship, "spec", None), "boats", None) or []
        if not boats:
            raise OrderError("She carries no boat: the ship's file lists none.")
        names = ", ".join(b.name for b in boats)
        raise OrderError(f"No boat of hers answers to {words!r}; her boats: {names}.")
    state = dealings.boat
    if state.lost:
        raise OrderError(f"{_cap(spec.name)} is lost: {state.lost_words}; nobody mans her.")
    if state.hull:
        held = (getattr(world, "hulls", None) or {}).get(state.hull)
        who = state.commander or "her crew"
        if held is not None:
            raise OrderError(f"{_cap(spec.name)} is manned and away already, {who} in her.")
    if state.away:
        raise OrderError(f"{_cap(spec.name)} is away already ({state.words()}).")
    if not getattr(spec, "file", None):
        raise OrderError(
            f"{_cap(spec.name)} has no file of her own to be a vessel by: her errands are the "
            "script's ('send the boat ashore', 'send the boat to the <ship>')."
        )
    way = abs(float(getattr(ship_hull.ship.dyn, "u", 0.0) or 0.0))
    if way > HOIST_OUT_WAY_MS:
        raise OrderError(
            f"She has {units.ms_to_knots(way):.1f} knots of way on her; heave to or come to an "
            "anchor before the boat is hoisted out."
        )
    pos = getattr(ship_hull, "position", None)
    if pos is None:
        raise OrderError("The boat is hoisted out on the sphere alone; this world has no chart.")
    # hoisted out and lying off the lee quarter
    wind = getattr(ship_hull, "wind", None)
    lee = (float(getattr(wind, "direction_from", 0.0)) + math.pi) if wind is not None else 0.0
    heading = float(getattr(ship_hull.ship, "heading", 0.0) or 0.0)
    aft = heading + math.pi
    dx = HOIST_OUT_OFF_M * (0.7 * math.sin(lee) + 0.7 * math.sin(aft))
    dy = HOIST_OUT_OFF_M * (0.7 * math.cos(lee) + 0.7 * math.cos(aft))
    where = pos.advanced(dx, dy)
    ship_name = str(getattr(ship_hull.ship, "name", "") or "the ship")
    name = f"the {ship_name}'s {spec.name.removeprefix('the ')}"
    vessel = Vessel.boat_of(
        str(ship_hull.id),
        {"kind": "a boat", "name": name, "pace_kn": 0.0, "seen_nm": BOAT_SEEN_NM},
        id=f"{ship_hull.id}:{spec.id}",
        ship_file=str(spec.file),
        nation=str(getattr(dealings, "ship_nation", "") or "britain"),
        position=where,
        heading_deg=units.rad_to_deg(heading) % 360.0,
        speed_kn=0.0,
        plan=[("lie_to", math.inf)],
        sail_state="under oars",
        what="a boat",
    )
    world.vessels.add(vessel)
    hull = make_hull(world, vessel)
    hull.__dict__["boat_of"] = str(ship_hull.id)
    hull.__dict__["boat_id"] = str(spec.id)
    hull.ship.name = name
    # hoisted out with her mast unstepped and laid along the thwarts: the oars first, the
    # lug when 'step the mast' and 'set the lug' are given (the period's practice)
    for spar in hull.ship.spars.values():
        if getattr(spar, "cls", "") == "mast":
            spar.sent_down = True
    dealings.boat = BoatState(
        away=True,
        boat_id=spec.id,
        boat_name=spec.name,
        errand="manned",
        phase="manned",
        since_tick=int(world.clock.tick),
        hull=str(hull.id),
    )
    oars = _oars(hull)
    n = int(oars.number) if oars is not None else int(spec.oars)
    text = (
        f"{_cap(spec.name)} hoisted out and manned: her coxswain and {n} oarsmen in her, "
        f"lying off the lee quarter{' by ' + by if by else ''}."
    )
    ship_hull.record(
        Severity.NOTABLE,
        "boat.manned",
        text,
        data={"boat": spec.id, "hull": str(hull.id), "oars": n},
    )
    hull.record(
        Severity.NOTABLE,
        "boat.manned",
        f"{_cap(name)} manned from the {ship_name}: the coxswain at the yoke lines, {n} oars; "
        "the oars in until 'give way'.",
        data={"ship": str(ship_hull.id), "oars": n},
    )
    return hull, text


def go_to_boat(world: Any, person: Any, words: str = "") -> tuple[str, str, dict[str, Any]]:
    """`go to the boat` (`go to the launch`, a boat of the file's by her name): the boat
    manned and made a hull if she is not, his person put aboard her with his station
    following, and the drivers following him when he is the player's."""
    from freesail.world.movement import hull_of, put_aboard

    here = hull_of(world, getattr(person, "hull", None))
    if here is None or not getattr(person, "aboard", True):
        raise OrderError("You are not aboard any ship; the boat is hers to go down into.")
    if is_boat(here):
        raise OrderError(f"You are in {hull_name_of(here)} already.")
    if getattr(person, "occupied", False):
        raise OrderError(f"You are at the {person.task}; the boat waits on it.")
    hull = manned_hull(world, here)
    made = ""
    if hull is None:
        hull, made = man_boat(world, here, words, by=person.name)
    else:
        bearing, distance = _bearing_distance(here, hull)
        if distance is not None and distance > ALONGSIDE_M:
            raise OrderError(
                f"{_cap(hull_name_of(hull))} is away, {distance_words(distance)} off; she "
                "comes alongside first ('come alongside' from her, or wait for her)."
            )
    players = _players_person(world, person)
    kind, text, data = put_aboard(world, person, hull, BOAT_DECK, by="the boat", said=True)
    if players:
        follow_boat(world, hull, person)
    oars = _oars(hull)
    tail = f" {oars.words()[:1].upper()}{oars.words()[1:]}." if oars is not None else ""
    text = f"{made + ' ' if made else ''}{person.name} went down into {hull_name_of(hull)}.{tail}"
    hull.record(Severity.NOTABLE, "boat.commanded", f"{person.name} takes her.", data={})
    return "person.aboard", text, data | {"boat": str(hull.id)}


def follow_boat(world: Any, hull: Any, person: Any) -> None:
    """The drivers follow the player into the boat (and back): a consequence of his order,
    recorded as a routine line `hull.followed` of the ship's log and never as a driver's
    input, so that a replay of the order moves it the same; the console's and the browser's
    `follow` stand for the owner's own choice."""
    if getattr(world, "followed", None) == hull.id:
        return
    world.followed = str(hull.id)
    with world.as_hull(hull):
        world.record(
            Severity.ROUTINE,
            "hull.followed",
            f"The drivers follow {person.name} into {hull_name_of(hull)}: her readings are his.",
            data={"ship": str(hull.id), "person": person.name},
        )


# ---------------------------------------------------------------------------
# her tick: the coxswain's mark, alongside, swamped
# ---------------------------------------------------------------------------


def tick_boat(world: Any) -> None:
    """Every tick, with a boat's hull current (`World.tick`): the coxswain steers for the
    mark `pull for` set and keeps steering as it bears; within reach of her ship when she
    was told to come alongside she is hoisted in; at the quay she lies on her oars and
    says so; once a minute, in a sea above her weather she is swamped."""
    hull = world.own
    oars = _oars(hull)
    if oars is None:
        return
    ship_hull = ship_of(world, hull)
    sea = getattr(world, "sea", None)
    minute = world.clock.ship_time.second == 0
    if minute and sea is not None and ship_hull is not None:
        try:
            state = str(sea.reading().state)
        except Exception:  # noqa: BLE001  (a sea that cannot be read swamps nobody)
            state = ""
        length_ft = float(getattr(hull.ship.hull.spec, "length_waterline_m", 5.0)) / 0.3048
        states = SWAMP_STATES_SMALL if length_ft < SMALL_BOAT_FT else SWAMP_STATES_LARGE
        if state in states:
            lose_boat(world, ship_hull, "swamped", f"swamped in {sea.reading().words}")
            return
    _tend_sheet(hull)
    mark = dict(oars.pulling_for or {})
    if not mark:
        return
    target, name = _mark_position(world, hull, mark)
    if target is None:
        oars.pulling_for = {}
        hull.record(
            Severity.ROUTINE, "boat.mark", f"The mark ({name}) is lost sight of; lying on the oars."
        )
        oars.stroke = 0.0
        return
    bearing, distance = _bearing_to(hull, target)
    if mark.get("alongside") and ship_hull is not None and distance <= ALONGSIDE_M:
        hoist_in(world, hull)
        return
    if mark.get("quay") and distance <= QUAY_M:
        oars.pulling_for = {}
        oars.stroke = 0.0
        hull.record(
            Severity.NOTABLE,
            "boat.at_quay",
            f"Alongside the quay at {name}; the oars tossed and laid in.",
            data={"port": mark.get("quay")},
        )
        return
    _steer(hull, bearing)


def _tend_sheet(hull: Any) -> None:
    """The lug's sheet in the bowman's hand, tended to the apparent wind every tick as the
    ship's `trim sails` trims a fore-and-aft sail (`world.ships._trim_for`, the engine's
    own trimmer): a boat's sheet is never belayed (the period's practice, a lugger's
    sheet held in hand against a capsize), so she never sails with the sheet where
    `set the lug` left it, which on a run left her lug flat amidships and aback."""
    from freesail.ship.parts import SailState

    ship = hull.ship
    if not any(
        getattr(s, "cls", "") == "lug" and s.state == SailState.SET for s in ship.sails.values()
    ):
        return
    awa = float(getattr(ship.dyn, "apparent_wind_angle", 0.0) or 0.0)
    if awa == 0.0:
        return
    from freesail.world.ships import _trim_for

    _trim_for(ship, awa)


def _steer(hull: Any, bearing_rad: float) -> None:
    """The coxswain's hand on the yoke lines: the engine's helmsman's law (`hp.steer`,
    the helm in proportion to how far she is off), the heading the mark's bearing. With
    her sheet tended it brings her round at a boat's speeds; sailed with the sheet left
    where `set the lug` put it she lay aback on a run and no helm would move her, which
    `_tend_sheet` is for."""
    from freesail.ship.parts import HelmMode

    dyn = hull.ship.dyn
    dyn.target_heading = units.wrap_2pi(bearing_rad)
    if hasattr(dyn, "helm_mode"):
        dyn.helm_mode = HelmMode.HEADING


def _mark_position(world: Any, hull: Any, mark: dict[str, Any]) -> tuple[Any, str]:
    """(the position of the coxswain's mark, its name): her ship, another hull, a port's
    quay, a far vessel by her id, or a position pricked."""
    from freesail.world.geo import Position

    hid = mark.get("hull")
    if hid:
        other = (getattr(world, "hulls", None) or {}).get(str(hid))
        if other is not None and getattr(other, "position", None) is not None:
            return other.position, hull_name_of(other)
        return None, str(hid)
    port_id = mark.get("quay")
    if port_id:
        port = world.ports.ports.get(str(port_id)) if getattr(world, "ports", None) else None
        if port is not None:
            return port.shore.position, port.name
        return None, str(port_id)
    vid = mark.get("vessel")
    if vid:
        v = world.vessels.get(str(vid)) if hasattr(world.vessels, "get") else None
        if v is not None and not v.done:
            return v.position, v.name
        return None, str(vid)
    if "lat_deg" in mark:
        pos = Position(float(mark["lat_deg"]), float(mark["lon_deg"]))
        return pos, mark.get("name") or "the position"
    return None, "nothing"


def _bearing_to(hull: Any, target: Any) -> tuple[float, float]:
    from freesail.world.geo import bearing_and_distance

    bearing_deg, distance = bearing_and_distance(hull.position, target)
    return units.deg_to_rad(bearing_deg), float(distance)


def _bearing_distance(a: Any, b: Any) -> tuple[float | None, float | None]:
    pa, pb = getattr(a, "position", None), getattr(b, "position", None)
    if pa is None or pb is None:
        return None, None
    bearing, distance = _bearing_to(a, pb)
    return bearing, distance


# ---------------------------------------------------------------------------
# alongside and hoisted in
# ---------------------------------------------------------------------------


def come_alongside(world: Any, hull: Any) -> str:
    """`come alongside` from the boat: she pulls for her ship (the coxswain's mark her,
    the oars out and giving way) and, within a boat's length, is hoisted in; alongside
    already, hoisted in at once."""
    ship_hull = ship_of(world, hull)
    if ship_hull is None:
        raise OrderError("She is no ship's boat: there is nothing to come alongside of.")
    _bearing, distance = _bearing_distance(hull, ship_hull)
    if distance is not None and distance <= ALONGSIDE_M:
        return hoist_in(world, hull)
    oars = _oars(hull)
    if oars is None:
        raise OrderError("She has no oars to pull with.")
    oars.pulling_for = {"hull": str(ship_hull.id), "alongside": True}
    if _lug_set(hull):
        # under the lug: the coxswain steers for her, the lug taken in as she is hoisted
        _steer(hull, _bearing_distance(hull, ship_hull)[0] or 0.0)
        return (
            f"Making for the {hull_name_of(ship_hull)} under the lug, "
            f"{distance_words(distance or 0.0)} off; alongside, she is hoisted in."
        )
    oars.out = True
    oars.manned = oars.number
    oars.stroke = 1.0
    return (
        f"Pulling for the {hull_name_of(ship_hull)}, {distance_words(distance or 0.0)} "
        "off; alongside, she is hoisted in."
    )


def hoist_in(world: Any, hull: Any) -> str:
    """The boat hoisted in: her people aboard the ship by `put_aboard` (the one who
    commanded her back at his station, his harness or his seat home), the drivers back
    to the ship where they followed him into her, her log's notable lines folded into the
    ship's log under her name (`boat.log`), her vessel gone from the sea and her hull
    released, the ship's `BoatState` at the booms again."""
    from freesail.world.crews import release_done
    from freesail.world.movement import put_aboard
    from freesail.world.ports import BoatState

    ship_hull = ship_of(world, hull)
    if ship_hull is None:
        raise OrderError("She is no ship's boat.")
    dealings = ship_hull.dealings
    name = hull_name_of(hull)
    boat_id = str(hull.__dict__.get("boat_id") or dealings.boat.boat_id)
    spec = next(
        (b for b in (getattr(ship_hull.ship.spec, "boats", None) or []) if b.id == boat_id), None
    )
    # the lug taken in and the oars laid in as she comes alongside
    from freesail.ship.parts import SailState

    for sail in hull.ship.sails.values():
        if sail.state == SailState.SET:
            sail.state = SailState.FURLED
    oars = _oars(hull)
    if oars is not None:
        oars.out, oars.manned, oars.stroke, oars.pulling_for = False, 0, 0.0, {}
    registry = getattr(world, "registry", None)
    people = list(registry.aboard(str(hull.id))) if registry is not None else []
    home_ids = {str(getattr(p, "home", "") or "") for p in people}
    commander = next((p for p in people if str(getattr(p, "home", "")) != str(hull.id)), None)
    # the drivers back to the ship before anyone moves, so that the lines land where they did
    was_followed = getattr(world, "followed", None) == hull.id
    if was_followed:
        world.followed = str(ship_hull.id)
    for p in people:
        if str(getattr(p, "home", "") or "") == str(hull.id):
            continue  # her own crew go back into the ship's muster with her
        put_aboard(world, p, ship_hull, "deck", by="the boat hoisted in", said=False)
    # her log folded into the ship's: the notable lines and her orders, under her name
    folded = 0
    for e in list(hull.log):
        # her orders, her own lines and every notable line; not the helm's and the wind's
        # routine chatter, which is the voyage's noise and not its record
        if e.kind == "boat.manned" or (
            e.severity == Severity.ROUTINE
            and not e.kind.startswith(("order.accepted", "boat.", "person."))
        ):
            continue
        ship_hull.record(
            Severity.ROUTINE,
            "boat.log",
            f"{_cap(name)}, {e.ship_time.strftime('%H:%M')}: {e.text}",
            data={"boat": boat_id, "kind": e.kind, "tick": e.tick},
        )
        folded += 1
    who = f", {commander.name} aboard again" if commander is not None else ""
    ship_hull.record(
        Severity.NOTABLE,
        "boat.hoisted_in",
        f"{_cap(name)} alongside and hoisted in{who}; her people aboard, {folded} lines of her "
        "log entered.",
        data={"boat": boat_id, "folded": folded, "homes": sorted(home_ids)},
    )
    if was_followed:
        ship_hull.record(
            Severity.ROUTINE,
            "hull.followed",
            f"The drivers follow {commander.name if commander else 'the player'} back aboard the "
            f"{hull_name_of(ship_hull)}: her readings are his again.",
            data={"ship": str(ship_hull.id)},
        )
    vessel = getattr(hull, "vessel", None)
    if vessel is not None:
        vessel.done = True
    release_done(world)
    dealings.boat = BoatState(boat_name=spec.name if spec is not None else dealings.boat.boat_name)
    return f"{_cap(name)} hoisted in; her people aboard."


# ---------------------------------------------------------------------------
# the boat lost
# ---------------------------------------------------------------------------


def lose_boat(world: Any, ship_hull: Any, how: str, words: str = "") -> str:
    """The ship's boat lost (`how`: swamped, stove, cut adrift): her people lost into the
    water where she was manned and away (as a man overboard is lost), the drivers back to
    the ship, her vessel gone and her hull released; the ship's `BoatState.lost` carries
    the word and the tick, and the boat is sent on no errand and manned by nobody until the
    yard replaces her. Said urgently in both logs."""
    from freesail.world.crews import release_done
    from freesail.world.ports import BoatState

    dealings = ship_hull.dealings
    state = dealings.boat
    hull = manned_hull(world, ship_hull)
    name = state.boat_name or "the boat"
    lost: list[str] = []
    if hull is not None:
        registry = getattr(world, "registry", None)
        for p in list(registry.aboard(str(hull.id))) if registry is not None else []:
            if str(getattr(p, "home", "") or "") == str(hull.id):
                continue  # her own crew are her file's: gone with her
            p.dead = True
            p.hull = None
            p.where = "lost"
            lost.append(p.name)
        if getattr(world, "followed", None) == hull.id:
            world.followed = str(ship_hull.id)
        hull.record(
            Severity.URGENT,
            "boat.lost",
            f"{_cap(hull_name_of(hull))} {words or how}; her people lost into the water.",
            data={"how": how, "lost": lost},
        )
        vessel = getattr(hull, "vessel", None)
        if vessel is not None:
            vessel.done = True
        release_done(world)
    when = world.clock.ship_time
    dealings.boat = BoatState(
        boat_name=name,
        boat_id=state.boat_id,
        lost=how,
        lost_tick=int(world.clock.tick),
        lost_words=f"{how} on the {when.day}{_th(when.day)}",
    )
    people_words = f"; {', '.join(lost)} lost with her" if lost else ""
    text = f"{_cap(name)} {words or how}{people_words}. A new one is the yard's."
    ship_hull.record(
        Severity.URGENT, "boat.lost", text, data={"how": how, "lost": lost, "boat": state.boat_id}
    )
    return text


def cut_adrift(world: Any, ship_hull: Any) -> str:
    """`cut the boat adrift`: the boat let go in a sea the ship cannot hoist her in; refused
    with her people in her (bring her alongside first) and with no boat to cut."""
    dealings = getattr(ship_hull, "dealings", None)
    if dealings is None or boat_named(ship_hull) is None:
        raise OrderError("She carries no boat: the ship's file lists none.")
    state = dealings.boat
    if state.lost:
        raise OrderError(f"{_cap(state.boat_name)} is lost already: {state.lost_words}.")
    hull = manned_hull(world, ship_hull)
    if hull is not None:
        registry = getattr(world, "registry", None)
        aboard = [
            p
            for p in (registry.aboard(str(hull.id)) if registry is not None else [])
            if str(getattr(p, "home", "") or "") != str(hull.id)
        ]
        if aboard:
            names = ", ".join(p.name for p in aboard)
            raise OrderError(
                f"{_cap(state.boat_name)} has {names} in her; bring her alongside before she "
                "is cut adrift."
            )
    elif state.away:
        raise OrderError(f"{_cap(state.boat_name)} is away on her errand ({state.words()}).")
    return lose_boat(world, ship_hull, "cut adrift", "cut adrift by order")


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def hull_name_of(hull: Any) -> str:
    return str(getattr(getattr(hull, "ship", None), "name", "") or getattr(hull, "id", "") or "")


def _oars(hull: Any) -> Any:
    from freesail.physics.oars import oars_of

    return oars_of(getattr(hull, "ship", None))


def _lug_set(hull: Any) -> bool:
    from freesail.ship.parts import SailState

    ship = hull.ship
    return any(
        getattr(s, "cls", "") == "lug" and s.state == SailState.SET for s in ship.sails.values()
    )


def _players_person(world: Any, person: Any) -> bool:
    """Whether the person is the player's: the followed hull's captain at the prompt (no
    seat), or the seat's person."""
    from freesail.agents.agent import CAPTAIN

    held = (getattr(world, "agents", None) or {}).get(CAPTAIN)
    if held is not None and not held.agent.released:
        return False  # a model holds her captain's station: his boat, not the player's
    seat = getattr(world, "player_seat", None)
    if seat is not None and not seat.agent.released:
        try:
            holder = world.stations.holder(seat.station.name)
        except Exception:  # noqa: BLE001
            holder = None
        return holder is person or str(getattr(seat.station, "person", "")) == person.name
    people = getattr(world, "people", None)
    try:
        return people is not None and people.captain is person
    except Exception:  # noqa: BLE001  (a muster that cannot run)
        return False


def _cap(words: str) -> str:
    return f"{words[:1].upper()}{words[1:]}" if words else words


def _th(day: int) -> str:
    if 10 <= day % 100 <= 20:
        return "th"
    return {1: "st", 2: "nd", 3: "rd"}.get(day % 10, "th")
