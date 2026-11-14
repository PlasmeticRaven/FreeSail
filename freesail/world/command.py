"""The change of the player's ship (package 60, step 1; the design in
`docs/design/Design-ShipBought.md` §2 to §4, its gate in §13).

**The game's first hull and the player's ship are two things.** The first hull (`World.
first_hull`, the hull the scenario built, id `PLAYER_ID`) keeps the sea, the game's seed and
scenario, the save's first block and the director's station for the whole game; the player's
ship (`World.players`) is the hull `World._players` names once he has taken command of
another, the first hull until then and in every save and checkpoint from before.

**One act, `take_up`**, called by one order of his person's, `take command of the "Fly"`
(`orders.command`), and so journaled by that order and given again by the replay at its tick:
his person rehomed to her (`Registry.rehome`) and her command passed to him
(`command_passed_to`), her captain's station bound to him, her rules captain standing aside at
his hand and her far brain dropped, his seat (where he holds one) carried to her captain's
station with no home kept, `World._players` set, the old ship settled (laid up at the port's
anchorage, or left to her senior officer, under an intent where one is given), and a line
`ship.taken_up` in both ships' logs. Refused in words, nothing changed, where she is not his
to take, he is not aboard her, a model holds her captain's station, either ship is in a set
or has ships under her orders, or the old ship cannot be settled; a prisoner's order is
refused before it reaches here (`movement.check`).

**What makes her his to take, in this step**: the director's word, the `command:` form given
in play where the ship it names lies at the named port (`court.new_command`, recorded here by
`give`); a ship bought (step 3) and a prize of an owner's (later) come by the same act.
"""

from __future__ import annotations

from typing import Any

from freesail.core.events import Severity

__all__ = [
    "LAID_UP",
    "LEFT",
    "TAKEN_UP",
    "CommandError",
    "give",
    "given_to",
    "ship_at_port",
    "take_up",
]

TAKEN_UP = "ship.taken_up"  # the line in both ships' logs
# The world's list of the ids of the hulls he has left (the hull and her body), for the switch.
HULLS_LEFT = "_hulls_left"
LAID_UP = "laid up"
LEFT = "left"


class CommandError(ValueError):
    """A change of ship refused, in words."""


def _root(world: Any) -> Any:
    from freesail.world.hulls import world_of

    return world_of(world)


def _name(hull: Any) -> str:
    """Her name as it follows 'the' in a line ('Fly', "Amazon's launch")."""
    name = str(getattr(getattr(hull, "ship", None), "name", "") or getattr(hull, "id", ""))
    return name[4:] if name.lower().startswith("the ") else name


# -- given by the director's word -----------------------------------------------------------


def ship_at_port(world: Any, ship_name: str, port: Any) -> Any:
    """The vessel of that name lying at the port (in its waters by `Ports.in_port_at`), or
    None: the ship a `command:` form names when she is in this world (the design's §5.5)."""
    root = _root(world)
    key = " ".join(str(ship_name).lower().split()).strip('"').removeprefix("the ")
    ports = getattr(root, "ports", None)
    for v in list(getattr(root.sea_vessels, "vessels", []) or []):
        if v.done or v.position is None:
            continue
        name = " ".join(str(v.name).lower().split()).removeprefix("the ")
        if name != key:
            continue
        here = ports.in_port_at(v.position) if ports is not None else None
        if here is not None and str(here.id) == str(getattr(port, "id", "")):
            return v
    return None


def give(world: Any, vessel: Any, person: Any, by: str) -> None:
    """The ship given to the person (the director's word in play): she is his to take up by
    `take command of her` once he is aboard her. Kept on the World by her id."""
    root = _root(world)
    given = root.__dict__.get("ships_given")
    if given is None:
        given = root.__dict__["ships_given"] = {}
    given[str(vessel.id)] = {
        "person": str(person.name),
        "tick": int(root.clock.tick),
        "by": str(by),
    }


def given_to(world: Any, hull_id: str) -> str:
    """The name of the person a ship was given to, or ""."""
    given = _root(world).__dict__.get("ships_given") or {}
    return str((given.get(str(hull_id)) or {}).get("person") or "")


# -- the act ----------------------------------------------------------------------------------


def _service(hull: Any) -> str:
    from freesail.world.service import service_of

    try:
        return service_of(hull)
    except Exception:  # noqa: BLE001  (a ship with no wardroom: a merchantman's)
        return "merchant"


def _his_to_take(root: Any, person: Any, hull: Any) -> str | None:
    """None when she is his to take; else the refusal's words."""
    if given_to(root, str(hull.id)) == str(person.name):
        return None
    from freesail.world.service import KINGS

    if _service(hull) == KINGS:
        return f"The {_name(hull)} is the King's; she is given by an order, not taken."
    return (
        f"The {_name(hull)} is not yours: she is her owners'; she must be bought, or given you "
        "by her owners' word."
    )


def _in_a_set(root: Any, hull: Any) -> str | None:
    """The refusal's words where the ship is in a set or has ships under her orders (the
    design's §2.5: a set's command is not carried to another hull in step 1)."""
    vessel = getattr(hull, "vessel", None)
    hid = str(hull.id)
    if vessel is not None and str(getattr(vessel, "squadron", "") or ""):
        return f"The {_name(hull)} is in a squadron or a convoy; shift the broad pendant first."
    for v in list(getattr(root.sea_vessels, "vessels", []) or []):
        if v.done or v is vessel:
            continue
        if str(getattr(v, "under_orders_of", "") or "") == hid:
            return (
                f"The {v.name} is under the {_name(hull)}'s orders; put her under nobody's first."
            )
    return None


def _officer(old: Any, named: str = "") -> Any:
    """The person the old ship is left to: the one named, else her senior officer by the
    ladder (`prizes.standing`), the player's person never."""
    people = getattr(old, "people", None)
    if people is None:
        return None
    if named:
        p = people.find(named)
        if p is None or getattr(p, "dead", False):
            raise CommandError(f"Nobody of the {_name(old)} answers to '{named}'.")
        if str(getattr(p, "hull", "") or "") != str(old.id):
            raise CommandError(f"{p.name} is not aboard the {_name(old)}.")
        return p
    from freesail.world.prizes import standing

    return standing(old, petty=False)


def _settlement(root: Any, old: Any, how: str, officer_words: str) -> tuple[str, Any, Any]:
    """(how, the officer, the port) for the old ship, or a refusal: laid up where she lies at
    an anchor in a port; left to an officer where one is aboard her (the design's §4)."""
    ports = getattr(root, "ports", None)
    port = ports.in_port_at(old.position) if ports is not None and old.position else None
    at_anchor = bool(getattr(old, "at_anchor", False))
    if not how:
        from freesail.world.service import KINGS

        # the defaults (§4.1): a King's ship left to her senior officer, an owner's laid up
        # where she lies at an anchor in a port, left to her officer otherwise
        how = LEFT if _service(old) == KINGS or not (at_anchor and port is not None) else LAID_UP
    if how == LAID_UP:
        if port is None or not at_anchor:
            raise CommandError(
                f"The {_name(old)} lies at no anchor in a port; bring her to an anchor in a road "
                "before she is laid up."
            )
        return how, _officer(old, officer_words) if officer_words else None, port
    officer = _officer(old, officer_words)
    if officer is None:
        raise CommandError(
            f"The {_name(old)} has nobody to leave her to; bring her to an anchor in a road and "
            "lay her up."
        )
    return how, officer, port


def take_up(
    world: Any,
    person: Any,
    hull: Any,
    *,
    how: str = "",
    officer: str = "",
    intent: str = "",
    by: str = "the captain",
    said: bool = True,
) -> tuple[str, dict[str, Any]]:
    """The player's person takes command of `hull` (the design's §2.3): returns her line and
    its data; raises `CommandError` in words, nothing changed. `said` False leaves her line to
    the order that called it (its reply is the line)."""
    root = _root(world)
    if getattr(root, "observed", False):
        raise CommandError("You command no ship here, and leave none.")
    old = root.players
    if hull is old:
        raise CommandError(f"You command the {_name(hull)} already.")
    if hull is root.first_hull and given_to(root, str(hull.id)) != str(person.name):
        raise CommandError(f"The {_name(hull)} is not yours to take up again by your own word.")
    from freesail.world.movement import is_boat_hull

    if is_boat_hull(hull):
        raise CommandError(f"The {_name(hull)} is a boat; go aboard the ship you take command of.")
    refused = _his_to_take(root, person, hull)
    if refused:
        raise CommandError(refused)
    if str(getattr(person, "hull", "") or "") != str(hull.id) or not getattr(
        person, "aboard", True
    ):
        raise CommandError(f"You are not aboard the {_name(hull)}; go aboard her first.")
    from freesail.agents.agent import CAPTAIN

    held = (getattr(hull, "agents", None) or {}).get(CAPTAIN)
    if held is not None and not held.agent.released:
        raise CommandError(
            f"Her captain's station is held; the {_name(hull)} has a captain who is not yours "
            "to displace."
        )
    for h in (old, hull):
        in_a_set = _in_a_set(root, h)
        if in_a_set:
            raise CommandError(in_a_set)
    how, left_to, port = _settlement(root, old, how, officer)
    if intent and how == LAID_UP:
        raise CommandError("A ship laid up sails for nothing; leave her to an officer to sail her.")
    if intent:
        from freesail.world.captains import read_intent

        try:
            read_intent(root, intent)
        except ValueError as e:
            raise CommandError(f"No intent a captain knows: {str(e).rstrip('.')}.") from None

    # -- the act, in order (§2.3) --
    registry = getattr(root, "registry", None)
    if registry is not None:
        registry.rehome(person, str(hull.id))
    person.confined_to = ""
    captain = getattr(hull, "captain", None)
    if captain is not None and getattr(captain, "commands", False):
        # before the command passes, so that the man who gives her up is her own late
        # captain, never the player
        captain.give_up(person.name, _late_captain(hull, person))
    hull.people.command_passed_to = person.id
    stations = getattr(hull, "stations", None)
    if stations is not None:
        try:
            stations.bind(CAPTAIN, person, quiet=True)
        except ValueError:
            pass
    vessel = getattr(hull, "vessel", None)
    if vessel is not None:
        vessel.brain = None  # the player's ship is awake always (crews.crewed)
        if getattr(vessel, "regime", "") == "in ordinary":
            # out of ordinary in his hands (package 60, step 2: a ship the director laid up
            # and gave him read as laid up still, her keepers alone wanted to work her)
            vessel.regime = ""
            vessel.sortie = ""
            vessel.commission_tick = -1
            vessel.goal = ""
        _woken_at_her_anchor(root, hull, vessel)
    _seat_follows(root, person, hull)
    root.__dict__["_players"] = str(hull.id)
    # the hull he left, kept with no far brain, is woken within the range again
    # (`crews.switch`; the lead's review of 1eb18434: that hull alone, not any hull without one)
    left = list(root.__dict__.get(HULLS_LEFT) or [])
    old_vessel = getattr(old, "vessel", None)
    for hid in (str(old.id), str(getattr(old_vessel, "id", "") or "")):
        if hid and hid not in left:
            left.append(hid)
    root.__dict__[HULLS_LEFT] = left
    root.__dict__.pop("_player_hull_read", None)
    given = root.__dict__.get("ships_given") or {}
    given.pop(str(hull.id), None)

    # the old ship settled (§4)
    old_line = _settle(root, old, how, left_to, port, intent, person, hull)
    _boats_home(root, hull, person)
    text = f"{person.name} takes command of the {_name(hull)}; the {_name(old)} {old_line}."
    data = {
        "person": person.name,
        "ship": str(hull.id),
        "from": str(old.id),
        "settle": how,
        "officer": getattr(left_to, "name", "") if left_to is not None else "",
        "by": by,
    }
    old.record(
        Severity.NOTABLE,
        TAKEN_UP,
        f"{person.name} leaves the {_name(old)} for the {_name(hull)}; she {old_line}.",
        data=dict(data),
    )
    if said:
        # the order's own reply is her line where an order gave it (`orders.command`)
        hull.record(Severity.NOTABLE, TAKEN_UP, text, data=dict(data))
    return text, data


def _woken_at_her_anchor(root: Any, hull: Any, vessel: Any) -> None:
    """The ship he takes up woken at once, if she sleeps in the far shape (the player's own
    ship is awake always, and `crews.switch` wakes no hull that is his: the lead's reading of
    ab0ade58, item 1). An awake hull is taken up as she lies."""
    woken_at_her_anchor(root, vessel)


def woken_at_her_anchor(root: Any, vessel: Any) -> None:
    """A sleeping hull woken for him, at his take-up or as he steps aboard her
    (`movement`'s boarding): by the trunk's wake, and where her far body rode at an anchor
    (her plan's leg, kept while she slept), laid at it whole (`laid_at_her_anchor`)."""
    from freesail.world import crews

    crew = getattr(vessel, "crew", None)
    if crew is None or getattr(crew, "awake", True):
        return
    plan = getattr(vessel, "plan", None) or []
    rode = bool(plan) and plan[0][0] == "anchor"
    crews.promote(root, vessel)
    if rode:
        laid_at_her_anchor(vessel.crew)


def laid_at_her_anchor(hull: Any) -> str | None:
    """A ship taken up asleep whose far body rode at an anchor, laid at it in one state (the
    lead's cut of package 60, ruling 3): one anchor, the first `scripts.cannot_anchor` passes,
    down on the ground under her at the scope the chart's depth where she lies wants, brought
    up; nothing set; no way. An anchor marked down on other ground (where she fell asleep,
    before her far body moved) is laid again under her, never left to hold her a mile off.
    Where no anchor can hold her, nothing is done beyond the trunk's wake and her log says why
    in one line. A state, set at once: no evolution is started, and nothing here can refuse
    or raise. Returns why none holds, or None where she is laid."""
    from freesail.evolutions.scripts import _let_go, _scope_plan, cannot_anchor
    from freesail.ship.parts import AnchorState, SailState, ground_tackle

    ship = hull.ship
    tackle = ground_tackle(ship)
    anchors = list(tackle.anchors) if tackle is not None else []
    depth = None
    chart = getattr(hull, "chart", None)
    if chart is not None and hull.position is not None:
        charted = chart.depth_at(hull.position)
        if charted is not None:
            depth = float(charted) + float(getattr(hull, "tide_height_m", 0.0) or 0.0)
    chosen, whys = None, []
    for a in anchors:
        # one marked down is asked as if at her bows: it is to be laid again under her
        was = a.state
        if was is AnchorState.DOWN:
            a.state = AnchorState.READY
        why = cannot_anchor(ship, a, depth)
        a.state = was
        if why is None:
            chosen = a
            break
        whys.append(why)
    if chosen is None:
        why = whys[0] if whys else cannot_anchor(ship, None, depth)
        hull.record(
            Severity.NOTABLE,
            "ship.not_anchored",
            f"No anchor of hers will hold her where she lies ({why}).",
            data={"id": str(hull.id), "why": why},
        )
        return why
    for a in anchors:
        if a.state is AnchorState.DOWN:
            # weighed with the far body's move, in the state the far body left her in
            a.state = AnchorState.STOWED
            a.ground_x = a.ground_y = None
            a.scope_m = 0.0
            a.brought_up = a.taut = a.dragging = False
    for sail in ship.sails.values():
        if sail.is_set:
            sail.state = SailState.FURLED
    dyn = ship.dyn
    dyn.u = dyn.v = 0.0
    if hasattr(dyn, "speed"):
        dyn.speed = 0.0
    if hasattr(dyn, "r"):
        dyn.r = 0.0
    ship.extra["water_depth_m"] = depth
    _let_go(ship, chosen, depth)
    chosen.scope_m = _scope_plan(chosen, depth, None)[0]
    chosen.brought_up = True
    hull._far_anchored = True
    return None


def _seat_follows(root: Any, person: Any, hull: Any) -> None:
    """His seat (where he holds a station through one) carried to her captain's station, no
    home kept: she is his home (the design's §2.3, item 5)."""
    from freesail.agents.agent import captain as captain_station
    from freesail.world.movement import seat_of_person

    seated = seat_of_person(root, person)
    if seated is None:
        return
    from_hull, s = seated
    if from_hull is hull and getattr(s.station, "name", "") == "captain" and not s.visiting:
        return
    s.move_to(hull, captain_station(world=hull), None)


def _settle(
    root: Any,
    old: Any,
    how: str,
    officer: Any,
    port: Any,
    intent: str,
    person: Any,
    hull: Any,
) -> str:
    """The old ship settled; returns the words of how ('is laid up at Falmouth', 'is left to
    Mr Ryan')."""
    from freesail.world.service import KINGS

    vessel = getattr(old, "vessel", None)
    people = getattr(old, "people", None)
    if officer is not None and people is not None:
        people.command_passed_to = officer.id
    elif people is not None and getattr(people, "command_passed_to", None) == person.id:
        people.command_passed_to = None
    if how == LAID_UP:
        from freesail.world.regimes import put_in_ordinary

        if vessel is not None:
            put_in_ordinary(root, vessel, port)
        laid = "is laid in ordinary" if _service(old) == KINGS else "is laid up"
        keeper = f", in the charge of {officer.name}" if officer is not None else ""
        return f"{laid} at {port.name}{keeper}"
    words = f"is left to {officer.name}"
    if intent and vessel is not None:
        from freesail.world.prizes import _give_intent

        role = "kings-ship" if _service(old) == KINGS else "merchant"
        _give_intent(root, vessel, intent, role)
        words += f" to {intent}"
    return words


def _brought_him(boat: Any, hull: Any, person: Any) -> bool:
    """Whether the boat's last coming alongside her put him aboard her
    (`boats.board_from_boat`'s `boat.alongside` line names who went aboard)."""
    for x in reversed(list(getattr(boat, "log", None) or [])):
        if x.kind != "boat.alongside":
            continue
        data = dict(getattr(x, "data", None) or {})
        return str(data.get("ship") or "") == str(hull.id) and person.name in (
            data.get("people") or []
        )
    return False


def _boats_home(root: Any, hull: Any, person: Any) -> None:
    """The boat that brought him across (`boats.board_from_boat`), lying fast alongside her
    for his coming back, pulls home to her own ship and is hoisted in there
    (`boats.come_alongside`): he will not come back, she is his home now. Another boat
    alongside her, waiting for its own visitor, waits on (the lead's review of 1eb18434)."""
    from freesail.world import boats

    for boat in list((getattr(root, "hulls", None) or {}).values()):
        if boat is hull or not boats.is_boat(boat):
            continue
        oars = boats._oars(boat)
        mark = dict(getattr(oars, "pulling_for", None) or {})
        if not (mark.get("fast") and str(mark.get("hull") or "") == str(hull.id)):
            continue
        ship_hull = boats.ship_of(root, boat)
        if ship_hull is None or ship_hull is hull or not _brought_him(boat, hull, person):
            continue
        text = boats.come_alongside(root, boat, "")
        boat.record(
            Severity.NOTABLE,
            "boat.mark",
            f"Cast off from the {_name(hull)}, nobody to wait for; {text[0].lower()}{text[1:]}",
            data={"hull": str(ship_hull.id), "home": True},
        )


def _late_captain(hull: Any, person: Any) -> str:
    """The name of the man who commanded her before him: her captain or commander, else her
    master; never the player's person (who is among her people as he comes aboard)."""
    people = list(getattr(getattr(hull, "people", None), "people", None) or [])
    for roles in (("captain", "commander"), ("master",)):
        for p in people:
            if p is person or getattr(p, "dead", False) or p.role not in roles:
                continue
            if str(getattr(p, "home", "") or hull.id) == str(hull.id):
                return str(p.name)
    return "Her master"
