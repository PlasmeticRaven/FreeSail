"""The prize (spec M7 §18; package 74, step 2; the design in `docs/design/Design-Prizes.md`
§2): a ship struck is possessed as a hull of the one world with a new nation and goal.

**Possession is one function** (`possess`), whatever brought her colours down (the strike
by morale, the captain's own word, the boarders' hand, the far rounds, 72's cut-out) and
whatever shape the two are in. It writes, on the far records: her nation the captor's, her
colours the captor's hoisted over her own (`Colours.over`), her role the prize master's
(`PRIZE_MASTER_ROLE`, `data/captains/prize-master.yaml`), her intent `carry the prize to
<port>` or her captor's company by 72's set, and `Vessel.prize`, the record the truth and the
court read. Where both have hulls it moves men: **the muster is whoever works her, the
prisoners are whoever is confined**. The prize's working `Crew` becomes the prize crew's
sailors moved out of the captor's muster (`remuster`: the routine and the quarters re-pointed,
the quarter bill reckoned afresh), and her former company becomes `ship.extra["prisoners"]`,
a `Prisoners` record (her old `Crew` with its hurt, where they are confined, their parole, the
irons); her named few are confined by their place (`Person.confined_to`, 65's hook: the
officers to the cabin, the people to the hold), their stations unbound (a model holding one
stood down by the handover's rule, "taken in the prize") and her `captain`'s station bound
to **the prize master**, the first of one **ladder of standing** (`standing`: the first
lieutenant, a lieutenant, the mate, the senior midshipman, then the senior petty officer of
the muster drawn as a person), which also answers who leads on when the boarders' officer
falls (`party_leader`, `combat/boarding.py`, package 97's paragraph). The prize master is
rehomed to her (`Registry.rehome`: he commands her, she is his ship while he has her) and
his harness or the player's seat follows him into her `captain`'s station. Where a hull is
wanting the counts go on the record alone (`far` possession), and a far prize made a hull
later has her muster cut to the counts (`fill_far_prize`).

**The rising** (`minute`): while her prisoners outnumber her prize crew's fit men by
`RISING_ODDS`, the prize crew is tired (`RISING_FATIGUE`, or `RISING_HOURS` since the taking),
no ship of her captor's nation is within `COVER_NM` and the prisoners are not in irons, a draw
once an hour from her own stream `prize` rises with chance `RISING_CHANCE`; the fight is 73's
tables on one deck (`boarding._strength`, `ROUND_LOSS`, `CARRIED_RATIO`), and ends with her
retaken (the swap back: `retake`) or the rising put down and the prisoners in irons for
`IRONS_HOURS`. **Retaken by a cruiser coming up** is 72's `squadrons.far_captures` read from
the prize's side (her doctrine yields when caught): the cruiser's possession of a prize of her
own nation is the swap back. **Burning and scuttling** (`burn`): her people into the captor as
prisoners, the vessel gone from the sea with the word.

Every figure here is judgement named in `docs/dev/TuningNotes.md` ("Package 74"); the
sources are Falconer 1780 (ENGAGEMENT: "invests his principal officer with the command of the
prize"), the Regulations of 1806 Sect. XII ch. III (prisoners victualled at two thirds, their
lists) and the actions' narratives (James).
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.crew.model import Crew, Rating, Sailor, Station, Watch, number_words
from freesail.world.ships import PLAYER_ID

__all__ = [
    "COVER_NM",
    "IRONS_HOURS",
    "LADDER",
    "PRISONER_PLACES",
    "PRIZE_CREW_LEAST",
    "PRIZE_MASTER_ROLE",
    "PRIZE_STREAM",
    "RISING_CHANCE",
    "RISING_FATIGUE",
    "RISING_HOURS",
    "RISING_ODDS",
    "Prisoners",
    "burn",
    "far_minute",
    "fill_far_prize",
    "is_prize",
    "minute",
    "party_leader",
    "possess",
    "prisoners_of",
    "prize_crew_size",
    "prize_master",
    "prizes_of",
    "record_of",
    "remuster",
    "retake",
    "standing",
    "take_prisoners_aboard",
]

PRIZE_MASTER_ROLE = "prize-master"
PRIZE_STREAM = "prize"
# The ladder of standing (the design's §2.3): Falconer's "principal officer", the first of
# these present and whole; the senior petty officer of the muster after them.
LADDER: tuple[str, ...] = ("first lieutenant", "lieutenant", "mate", "master's mate", "midshipman")
PETTY_OFFICER_ROLE = "boatswain's mate"
# A prize crew's least (judgement: six men work a brig's plain sail and keep a watch of three).
PRIZE_CREW_LEAST = 6
# The rising (the design's §2.8), every figure judgement named in the tuning notes.
RISING_ODDS = 2.0
RISING_FATIGUE = 0.6
RISING_HOURS = 18
RISING_CHANCE = 0.25
IRONS_HOURS = 24
# The cover a captor gives his prize: 72's two miles (`squadrons.COVER_NM`), read there.
COVER_NM = 2.0
# The captor's colours over hers are seen for a day (judgement: the period's sign of a prize).
OVER_COLOURS_S = 24 * 3600
# The roles of a prize's company confined to the cabin on their parole; the rest the hold.
OFFICER_ROLES: frozenset[str] = frozenset(
    {
        "captain",
        "commander",
        "master",
        "first lieutenant",
        "lieutenant",
        "mate",
        "master's mate",
        "surgeon",
        "purser",
        "supercargo",
        "passenger",
    }
)
PRISONER_PLACES: dict[str, str] = {"officer": "cabin", "people": "hold"}
# The rounds of a rising: 73's figures read from `combat.boarding`.
RISING_ROUNDS_MOST = 15


@dataclass
class Prisoners:
    """The prisoners a hull holds: a company's `Crew` as it stood when she was taken (or the
    men taken out of a prize into the captor), where they are confined, their parole by name,
    the irons after a rising put down, and the count taken out of her."""

    crew: Crew
    nation: str
    since: int
    confined: str = "below"
    irons_until: int | None = None
    parole: dict[str, str] = field(default_factory=dict)
    divided_out: int = 0
    rose_at: list[int] = field(default_factory=list)

    @property
    def alive(self) -> list[Sailor]:
        return [s for s in self.crew.sailors if s.hurt != "killed"]

    @property
    def count(self) -> int:
        return len(self.alive)

    @property
    def fit(self) -> int:
        return sum(1 for s in self.crew.sailors if s.fit)

    def in_irons(self, tick: int) -> bool:
        return self.irons_until is not None and tick < self.irons_until

    def words(self, tick: int) -> str:
        if self.count == 0:
            return "no prisoners"
        irons = ", in irons" if self.in_irons(tick) else ""
        where = "confined below" if self.confined == "below" else self.confined
        hurt = sum(1 for s in self.alive if s.hurt)
        hurt_words = f", {number_words(hurt)} of them hurt" if hurt else ""
        out = f"{number_words(self.count)} prisoners{hurt_words}, {where}{irons}"
        if self.divided_out:
            out += f" ({number_words(self.divided_out)} more taken out of her)"
        return out


# -- the records ----------------------------------------------------------------------------


def prisoners_of(ship: Any) -> Prisoners | None:
    extra = getattr(ship, "extra", None)
    if not isinstance(extra, dict):
        return None
    p = extra.get("prisoners")
    return p if isinstance(p, Prisoners) else None


def record_of(vessel: Any) -> dict[str, Any] | None:
    """The prize record of a vessel (`Vessel.prize`), None for a ship that is no prize and
    for one given back or retaken (the record then keeps its history under `retaken`)."""
    rec = getattr(vessel, "prize", None)
    return rec if isinstance(rec, dict) else None


def is_prize(vessel: Any) -> bool:
    rec = record_of(vessel)
    if not rec or rec.get("retaken") or rec.get("restored"):
        return False
    return bool(rec.get("manned", True))


def prizes_of(world: Any, captor_id: str) -> list[Any]:
    """Every prize a captor holds now, by her id (the player's `PLAYER_ID`): each still her prize
    by the one answer (`relations.still`, `PRIZE`)."""
    from freesail.world import relations as R

    sea = getattr(world, "vessels", None)
    return [
        v
        for v in list(getattr(sea, "vessels", []) or [])
        if R.still(world, str(captor_id), v, R.PRIZE)
    ]


def _story(vessel: Any, tick: int, words: str) -> None:
    story = list(getattr(vessel, "story", ()) or ())
    story.append((tick, words))
    vessel.story = tuple(story[-30:])


def _hull(vessel: Any) -> Any:
    crew = getattr(vessel, "crew", None)
    return crew if crew is not None and hasattr(crew, "ship") else None


def _doctrine(vessel: Any) -> Any:
    """The doctrine a vessel's captain sails by: her hull's captain's, else her brain's;
    for a hull whose captain sails by no doctrine (the player's, given no role) the one her
    service answers (a King's ship's, a privateer's, a merchant's), so that the prize rules
    are her service's and not a default's."""
    hull = _hull(vessel)
    cap = getattr(hull, "captain", None) if hull is not None else None
    d = getattr(cap, "doctrine", None) if cap is not None else None
    if d is None:
        d = getattr(getattr(vessel, "brain", None), "doctrine", None)
    if d is None and hull is not None:
        from freesail.world.captains import load_doctrine
        from freesail.world.service import KINGS, PRIVATEER, service_of

        try:
            service = service_of(hull)
        except Exception:  # noqa: BLE001
            service = KINGS
        role = {KINGS: "kings-ship", PRIVATEER: "privateer"}.get(service, "merchant")
        d = load_doctrine(role)
    return d


def _th(doctrine: Any, key: str, default: Any) -> Any:
    if doctrine is None:
        return default
    value = doctrine.threshold(key, default)
    return default if value is None else value


def _root(world: Any) -> Any:
    from freesail.world.hulls import world_of

    return world_of(world)


def _nation_of(world: Any, nation_id: str) -> Any:
    nations = getattr(world, "nations", None)
    try:
        return nations.get(nation_id) if nations is not None else None
    except KeyError:
        return None


# -- the ladder of standing -----------------------------------------------------------------


def _rating_rank(s: Sailor) -> tuple[int, float]:
    order = {
        Rating.OFFICER: 6,
        Rating.PETTY_OFFICER: 5,
        Rating.ABLE: 4,
        Rating.MARINE: 3,
        Rating.ORDINARY: 2,
        Rating.IDLER: 1,
        Rating.LANDSMAN: 0,
    }
    return (order.get(s.rating, 0), float(s.skill_deck))


def standing(
    hull: Any,
    among: list[Sailor] | None = None,
    exclude: tuple[Any, ...] = (),
    petty: bool = True,
) -> Any:
    """The first of the ladder present, whole and aboard her (the captain never), among the
    hull's persons; `among` restricts the men to those sailors (a boarding party) and the
    senior petty officer is drawn from them when no officer stands; None for nobody."""
    people = getattr(hull, "people", None)
    if people is None:
        return None
    try:
        captain = people.captain
    except Exception:  # noqa: BLE001  (a muster that cannot run)
        captain = None
    ids = {s.id for s in among} if among is not None else None
    excluded = {id(x) for x in exclude}
    for role in LADDER:
        for p in people.by_role(role):
            if p is captain or id(p) in excluded:
                continue
            if getattr(p, "dead", False) or not getattr(p, "aboard", True):
                continue
            if getattr(p, "sick", False) or getattr(p, "confined_to", ""):
                continue
            if str(getattr(p, "hull", "") or "") != str(getattr(hull, "id", "")):
                continue
            if ids is not None and p.sailor_id not in ids:
                continue
            return p
    if not petty:
        return None
    crew = (getattr(getattr(hull, "ship", None), "extra", None) or {}).get("crew")
    if crew is None:
        return None
    pool = [
        s
        for s in (among if among is not None else crew.sailors)
        if s.fit
        and s.station not in (Station.QUARTERDECK, Station.MARINES, Station.IDLERS)
        and s.at is None
    ]
    taken = {p.sailor_id for p in people.all if p.sailor_id}
    pool = [s for s in pool if s.id not in taken] or pool
    if not pool:
        return None
    best = max(pool, key=lambda s: (_rating_rank(s), s.id))
    return people.draw_sailor(best, PETTY_OFFICER_ROLE)


def party_leader(hull: Any, boarders: list[Sailor]) -> Any:
    """Who leads the boarders on when their officer falls (package 97's paragraph): the
    ladder among the party on her deck, the senior petty officer of the party last."""
    return standing(hull, among=boarders)


def prize_master(captor_hull: Any, doctrine: Any = None, party: list[Sailor] | None = None) -> Any:
    """The prize master by the captor's doctrine (`prize_master_from`: the roles he sends,
    in order; the first lieutenant kept with his ship unless the file names him), the ladder
    otherwise; from the party on her deck first where there is one."""
    people = getattr(captor_hull, "people", None)
    if people is None:
        return None
    froms = _th(doctrine, "prize_master_from", None)
    if isinstance(froms, str) and froms.strip():
        # the file's words: the roles in order, comma-separated
        roles: tuple[str, ...] = tuple(x.strip() for x in froms.split(",") if x.strip())
    elif isinstance(froms, (list, tuple)):
        roles = tuple(str(x) for x in froms)
    else:
        roles = ("lieutenant", "mate", "master's mate", "midshipman", "petty officer")
    try:
        captain = people.captain
    except Exception:  # noqa: BLE001
        captain = None
    ids = {s.id for s in party} if party else None
    for role in roles:
        if role == "petty officer":
            found = standing(captor_hull, among=party if party else None)
            if found is not None and found.role == PETTY_OFFICER_ROLE:
                return found
            continue
        for p in people.by_role(role):
            if p is captain or getattr(p, "dead", False) or not getattr(p, "aboard", True):
                continue
            if getattr(p, "sick", False) or getattr(p, "confined_to", ""):
                continue
            if ids is not None and p.sailor_id not in ids and party:
                continue
            return p
    return standing(captor_hull, among=party if party else None)


# -- the prize crew's size ------------------------------------------------------------------


def prize_crew_size(captor_fit: int, prize_complement: int, doctrine: Any) -> int:
    """So many of the captor's fit men (the doctrine's `prize_crew_share`, at least
    `PRIZE_CREW_LEAST`), never more than half of her complement nor more than he can spare
    (a third of his fit men)."""
    share = float(_th(doctrine, "prize_crew_share", 0.1) or 0.1)
    least = int(_th(doctrine, "prize_crew_least", PRIZE_CREW_LEAST) or PRIZE_CREW_LEAST)
    n = max(least, int(round(share * max(captor_fit, 0))))
    n = min(n, max(1, prize_complement // 2) if prize_complement else n)
    n = min(n, max(1, captor_fit // 3)) if captor_fit else n
    return max(1, n)


# -- the muster swapped ---------------------------------------------------------------------


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


def _watches(sailors: list[Sailor]) -> None:
    for i, s in enumerate(sorted(sailors, key=lambda x: x.id)):
        if s.station in (Station.QUARTERDECK, Station.IDLERS):
            s.watch = Watch.NONE
        else:
            s.watch = (Watch.STARBOARD, Watch.LARBOARD)[i % 2]
        s.at = None
        s.quarters = ""
        s.turned_up = False


def _draw_prize_crew(captor_hull: Any, n: int, party: list[Sailor] | None) -> list[Sailor]:
    """The men put aboard her: the party on her deck first (the boarders, whole and at no
    work), then the captor's fit seamen at no work by id, never a post, a marine or an idler."""
    crew = captor_hull.ship.extra.get("crew")
    if crew is None:
        return []
    chosen: list[Sailor] = []
    if party:
        for s in party:
            if s.fit and s.at is None and s.station not in (Station.QUARTERDECK, Station.IDLERS):
                chosen.append(s)
            if len(chosen) >= n:
                break
    if len(chosen) < n:
        taken = {s.id for s in chosen}
        for s in crew.sailors:
            if len(chosen) >= n:
                break
            if s.id in taken or not s.fit or s.at is not None or s.post:
                continue
            if s.station in (Station.QUARTERDECK, Station.MARINES, Station.IDLERS):
                continue
            chosen.append(s)
    return chosen


def _take_out(captor_hull: Any, men: list[Sailor]) -> None:
    """The men out of the captor's muster and off her quarter bill."""
    crew = captor_hull.ship.extra.get("crew")
    if crew is None:
        return
    ids = {s.id for s in men}
    crew.sailors = [s for s in crew.sailors if s.id not in ids]
    crew.reindex()
    quarters = captor_hull.ship.extra.get("quarters")
    if quarters is not None:
        for gc in quarters.crews.values():
            gc.members = [s for s in gc.members if s.id not in ids]
        for name, division in list(quarters.divisions.items()):
            quarters.divisions[name] = [s for s in division if s.id not in ids]


def _confine_people(hull: Any, tick: int) -> dict[str, str]:
    """Her named few confined by the custom: the officers to the cabin (their parole not yet
    asked), the people to the hold; their stations unbound by the handover's rule. Returns
    the parole record's start."""
    people = getattr(hull, "people", None)
    parole: dict[str, str] = {}
    if people is None:
        return parole
    hid = str(getattr(hull, "id", ""))
    for p in list(people.people):
        if getattr(p, "dead", False) or str(getattr(p, "hull", "") or "") != hid:
            continue
        place = PRISONER_PLACES["officer"] if p.role in OFFICER_ROLES else PRISONER_PLACES["people"]
        p.confined_to = place
        p.where = place
        p.occupied_until = None
        p.occupied_with = ""
        p.pending = None
        if p.role in OFFICER_ROLES:
            parole[p.name] = "not asked"
    stations = getattr(hull, "stations", None)
    if stations is not None:
        for name in list(stations.names()):
            try:
                holder = stations.holder(name)
            except Exception:  # noqa: BLE001
                holder = None
            if holder is None or not getattr(holder, "confined_to", ""):
                continue
            if name == "captain":
                continue  # bound to the prize master below
            try:
                stations.unbind(name, why="taken in the prize", quiet=True)
            except ValueError:
                pass
    return parole


def _station_follows(world: Any, person: Any, hull: Any, station_name: str) -> None:
    """The person's harness or the player's seat carried into the hull's station of the
    name (his own command there: the boat's rule of 82's §2 extended to a prize master), his
    station at home standing bound to him; nothing when no model or seat holds him."""
    from freesail.agents.agent import captain as captain_station
    from freesail.world.movement import harness_of, seat_of_person

    held = harness_of(world, person)
    if held is not None:
        from_hull, h = held
        # from his own ship, or from a visitor's voice on her deck already (the boarders'
        # officer standing on the deck won)
        if from_hull is not hull or h.station.name != station_name:
            station = captain_station(h.policy, world=hull)
            home = h._home or (str(getattr(from_hull, "id", "") or ""), h.station)
            h.move_to(hull, station, home)
    seated = seat_of_person(world, person)
    if seated is not None:
        from_hull, s = seated
        if from_hull is not hull or getattr(s.station, "name", "") != station_name:
            home = s._home or (str(getattr(from_hull, "id", "") or ""), s.station)
            s.move_to(hull, captain_station(world=hull), home)


def _bind_captain(hull: Any, person: Any) -> None:
    stations = getattr(hull, "stations", None)
    if stations is None:
        return
    try:
        stations.bind("captain", person, quiet=True)
    except ValueError:
        pass


# -- possession --------------------------------------------------------------------------------


def _port_for(world: Any, captor: Any, doctrine: Any) -> Any:
    """The prize's port by the captor's doctrine (`prize_goal`): "home", his intent's
    origin where it is a port of the world; else the nearest port open to his nation."""
    ports = getattr(world, "ports", None)
    table = getattr(ports, "ports", None) or {}
    nations = ports
    goal = str(_th(doctrine, "prize_goal", "the nearest friendly port") or "")
    brain = getattr(captor, "brain", None)
    intent = getattr(brain, "intent", None)
    if goal == "home" and intent is not None:
        for key in (getattr(intent, "origin", ""), getattr(intent, "destination", "")):
            if key and key in table and _open(nations, table[key], captor.nation):
                return table[key]
    if intent is not None and getattr(intent, "kind", "") in ("passage", "home", "letter"):
        dest = getattr(intent, "destination", "")
        if dest in table and _open(nations, table[dest], captor.nation):
            return table[dest]
    best = None
    for port in table.values():
        if not _open(nations, port, captor.nation):
            continue
        _, d = _bearing_distance(captor.position, port.outer_road.position)
        if best is None or d < best[1]:
            best = (port, d)
    return best[0] if best is not None else None


def _open(ports: Any, port: Any, nation_id: str) -> bool:
    """The port open to the nation by the ports' stance (the nations' table over the port's
    closures and its blockade)."""
    if ports is None or not hasattr(ports, "stance"):
        return True
    try:
        return ports.stance(port, nation_id) == "open"
    except Exception:  # noqa: BLE001
        return False


def _bearing_distance(a: Any, b: Any) -> tuple[float, float]:
    from freesail.world.geo import bearing_and_distance

    return bearing_and_distance(a, b)


def _nation_words(world: Any, vessel: Any, nation_id: str) -> None:
    """Her nation and its words: the one road by which a ship changes hands (taken, retaken,
    restored), and so where she becomes a new party to every judge on the sea and her own judges
    to every ship (`relations.changed_hands`; the whole-change review of 80e703c7, gundeck-1)."""
    from freesail.world import relations as R

    n = _nation_of(world, nation_id)
    vessel.nation = str(nation_id)
    R.changed_hands(world, vessel)
    if n is not None:
        vessel.colours = n.colours
        vessel.flag = getattr(n, "flag", "")
        vessel.nation_adjective = n.adjective


def _set_colours(world: Any, vessel: Any, nation_id: str, over: str, tick: int) -> None:
    from freesail.world import signals as S

    locker = S.vessel_locker(vessel)
    S.set_colours(locker.colours, getattr(world, "nations", None), "shown", nation_id, tick)
    locker.colours.over = over
    locker.colours.over_since = tick if over else 0
    hull = _hull(vessel)
    if hull is not None:
        hull.ship.extra["signals"] = locker  # one object (71)
        hull.ship.extra.pop("struck", None)
    vessel.struck = False
    # the strike's record ends with the strike (the whole-change review of 80e703c7, engine-2):
    # her colours given back, she is struck to nobody, and a later strike by a road that names no
    # taker is to no one known (`relations.STRUCK`), its hour counted from then
    damage = getattr(vessel, "damage", None)
    if isinstance(damage, dict):
        damage.pop("struck_to", None)
        damage.pop("struck_tick", None)


def _give_intent(world: Any, vessel: Any, words: str, role: str) -> None:
    """Her brain's intent and role set anew (a brain made where she had none), and her
    hull's captain's with them."""
    from freesail.world.brains import FarCaptain

    vessel.role = role
    brain = getattr(vessel, "brain", None)
    if brain is None and str(getattr(vessel, "id", "")) == PLAYER_ID:
        brain = None  # the player's own hull is awake always: no far brain for her
    elif brain is None:
        brain = FarCaptain(_root(world), vessel, words, role=role)
        vessel.brain = brain
        vessel.intent_words = brain.intent_words
    elif brain is not None:
        try:
            brain.set_intent(words)
        except ValueError:
            brain.set_intent(words, free=True)
        vessel.intent_words = brain.intent_words
        brain.role = role
        from freesail.world.captains import load_doctrine

        brain.doctrine = load_doctrine(role)
        brain._stranger = None
        brain.state = None
        brain.planned = False
        brain.vessel.saved_plan = None
    vessel.state = "on passage"
    vessel.plan = [("lie_to", math.inf)]
    hull = _hull(vessel)
    cap = getattr(hull, "captain", None) if hull is not None else None
    if cap is not None:
        cap.scenario_role = role
        cap.aside = False
        try:
            cap.set_intent(words)
        except ValueError:
            cap.set_intent(words, free=True)
        cap._stranger = None


def possess(
    world: Any,
    captor: Any,
    prize: Any,
    *,
    by: str,
    master: Any = None,
    party: list[Sailor] | None = None,
    said: bool = True,
) -> dict[str, Any]:
    """Possession taken of `prize` (a `Vessel` struck) by `captor` (a `Vessel`), by any road
    (the module's head). A prize of the captor's own nation retaken from the enemy is given
    back to her people (`retake`). Returns the record written."""
    world = _root(world)
    tick = int(world.clock.tick)
    rec = record_of(prize)
    if rec and is_prize(prize) and str(rec.get("nation_was")) == str(captor.nation):
        return retake(world, prize, by=f"{captor.name} coming up", how="retaken", captor=captor)
    captor_hull, prize_hull = _hull(captor), _hull(prize)
    if str(prize.id) == PLAYER_ID and captor_hull is None:
        # the player's ship taken by a far body (the design's §3.1): her captor is made a
        # hull and woken, a dealing of the first rank under the cap, so that the captive is
        # aboard a real hull with places, a company and a log
        from freesail.world.crews import promote

        promote(world, captor)
        captor.dealing_tick = tick
        captor_hull = _hull(captor)
    doctrine = _doctrine(captor)
    nation_was = str(prize.nation)
    role_was = str(getattr(prize, "role", "") or "")
    intent_was = str(getattr(prize, "intent_words", "") or "")
    # the record
    complement = _complement(prize)
    record: dict[str, Any] = {
        "captor": str(captor.id),
        "captor_name": str(captor.name),
        "captor_nation": str(captor.nation),
        "taken_at": tick,
        "how": by,
        "nation_was": nation_was,
        "role_was": role_was,
        "intent_was": intent_was,
        "men_at_start": complement,
        # the sharers of the prize money (the design's §5.3; Lavery, p. 116): the ships at war
        # with her in sight from her masthead at the strike, written there (`prize_court.
        # note_in_sight`), and the captor's complement for the division
        "in_sight": list(getattr(prize, "in_sight_at_strike", None) or []),
        "captor_complement": _complement(captor),
        "manned": True,
        "crew": 0,
        "prisoners": complement,
        "master": "",
        "goal": "",
        "service": _service_of(captor),
    }
    # the goal: his port, or his company
    port = _port_for(world, captor, doctrine)
    company_rule = str(_th(doctrine, "prize_company", "in company") or "in company")
    if port is not None:
        intent_words = f"carry the prize to {port.name}"
        record["goal"] = port.id
    else:
        # no port open to him on this sea: she keeps his company (a free intent, the words
        # the prize master's)
        intent_words = f"keep company with the {captor.name}"
    # her nation, her colours over her own, her role and her intent
    _nation_words(world, prize, str(captor.nation))
    _set_colours(world, prize, str(captor.nation), nation_was, tick)
    _give_intent(world, prize, intent_words, PRIZE_MASTER_ROLE)
    # her set: out of her own, into her captor's company by his doctrine
    sets = getattr(world, "squadrons", None)
    if sets is not None:
        old = sets.of(prize.id)
        if old is not None:
            old.leave(world, prize.id, f"taken by {captor.name}")
        if company_rule.startswith("in company"):
            from freesail.world.squadrons import Squadron

            company = sets.commanded_by(captor.id)
            if company is None:
                company = Squadron(
                    id=f"{captor.id}-company",
                    name=f"{captor.name}'s company",
                    kind="squadron",
                    nation=str(captor.nation),
                    commander=str(captor.id),
                    members=[str(captor.id)],
                    goal=str(getattr(captor, "intent_words", "") or ""),
                    formation="line ahead",
                )
                sets.add(company, world)
            company.join(world, prize.id, as_prize=True)
            record["company"] = company.id
    # the men
    n = prize_crew_size(_fit(captor), complement, doctrine)
    if captor_hull is not None and prize_hull is not None:
        men = _draw_prize_crew(captor_hull, n, party)
        _take_out(captor_hull, men)
        old_crew = prize_hull.ship.extra.get("crew")
        new_crew = Crew(ship_name=str(prize.name), sailors=list(men))
        _watches(new_crew.sailors)
        for s in old_crew.sailors if old_crew is not None else []:
            s.at = None
            s.quarters = ""
        remuster(prize_hull, new_crew)
        if str(prize.id) == PLAYER_ID:
            # the player's person taken aboard the captor (the captive's channel, §3.1)
            from freesail.world.captive import player_taken

            player_taken(world, captor, captor_hull, prize_hull, record)
        if old_crew is not None:
            prize_hull.ship.extra["prisoners"] = Prisoners(
                crew=old_crew, nation=nation_was, since=tick, parole={}
            )
            prize_hull.ship.extra["prisoners"].parole = _confine_people(prize_hull, tick)
        from freesail.world.court import record_loss

        record_loss(world, prize_hull, record)  # the loss in her captain's record (§7)
        record["crew"] = len(men)
        record["prisoners"] = (
            prisoners_of(prize_hull.ship).count if prisoners_of(prize_hull.ship) else 0
        )
        if master is None:
            master = prize_master(captor_hull, doctrine, party)
        if master is not None:
            _put_master(world, master, captor_hull, prize_hull, record)
    elif captor_hull is not None:
        # the prize a far record: his men go over on the record, kept on his hull for her
        # hull when the cap makes it (`fill_far_prize`)
        men = _draw_prize_crew(captor_hull, n, party)
        _take_out(captor_hull, men)
        kept = captor_hull.ship.extra.setdefault("prize_crews", {})
        kept[str(prize.id)] = list(men)
        record["crew"] = len(men)
        if master is None:
            master = prize_master(captor_hull, doctrine, party)
        if master is not None:
            record["master"] = master.name
            record["master_id"] = master.id
    else:
        record["crew"] = n
        if prize_hull is not None:
            # her hull without a captor's: the muster cut to the counts, a prize master made
            # from words (the design's §2.6)
            fill_far_prize(prize_hull, record, nation_was, tick)
    prize.prize = record
    # what her captor knew her an enemy by (her shot at him, a pirate's act, the signal or the
    # hail) went with her change of hands (`_nation_words`, `relations.changed_hands`); she is
    # his prize from now and judged so (`Judgement._prize_of_ours`)
    _lines(world, captor, prize, record, said)
    return record


def _service_of(captor: Any) -> str:
    hull = _hull(captor)
    if hull is not None:
        from freesail.world.service import service_of

        try:
            return service_of(hull)
        except Exception:  # noqa: BLE001
            pass
    from freesail.world.service import ROLE_SERVICE

    role = str(getattr(getattr(captor, "brain", None), "role", "") or getattr(captor, "role", ""))
    return ROLE_SERVICE.get(role, "merchant")


def _complement(vessel: Any) -> int:
    hull = _hull(vessel)
    crew = hull.ship.extra.get("crew") if hull is not None else None
    if crew is not None:
        return len([s for s in crew.sailors if s.hurt != "killed"])
    try:
        from freesail.ship.loader import load_spec

        spec = load_spec(vessel.ship_file)
        return int(getattr(spec.crew, "complement", 0) or 0)
    except Exception:  # noqa: BLE001
        return 0


def _fit(vessel: Any) -> int:
    hull = _hull(vessel)
    crew = hull.ship.extra.get("crew") if hull is not None else None
    if crew is not None:
        return sum(1 for s in crew.sailors if s.fit)
    d = getattr(vessel, "damage", {}) or {}
    return max(0, _complement(vessel) - int(d.get("killed", 0)) - int(d.get("wounded", 0)))


def _put_master(world: Any, master: Any, captor_hull: Any, prize_hull: Any, record: dict) -> None:
    """The prize master into her: rehomed to her (he commands her), put aboard her
    quarterdeck, her `captain`'s station bound to him, his harness or seat following."""
    from freesail.world.movement import put_aboard

    registry = getattr(world, "registry", None)
    record["master"] = master.name
    record["master_home"] = str(getattr(master, "home", "") or captor_hull.id)
    if registry is not None:
        registry.rehome(master, str(prize_hull.id))
    record["master_id"] = master.id  # as it stands after the move (`Registry.rehome`)
    master.confined_to = ""
    put_aboard(world, master, prize_hull, "quarterdeck", by="the prize crew", said=False)
    people = getattr(prize_hull, "people", None)
    if people is not None:
        people.command_passed_to = master.id
    _bind_captain(prize_hull, master)
    _station_follows(world, master, prize_hull, "captain")
    prize_hull.record(
        Severity.NOTABLE,
        "person.aboard",
        f"{master.name} of the {captor_hull.name} takes the command of her as prize master.",
        data={"person": master.name, "ship": str(prize_hull.id), "by": "the prize crew"},
    )


def _lines(world: Any, captor: Any, prize: Any, record: dict[str, Any], said: bool) -> None:
    tick = int(world.clock.tick)
    captor_hull, prize_hull = _hull(captor), _hull(prize)
    n = int(record.get("crew", 0))
    k = int(record.get("prisoners", 0))
    master = record.get("master") or "a prize master"
    port = record.get("goal", "")
    ports = getattr(world, "ports", None)
    port_name = ""
    if port and getattr(ports, "ports", None) and port in ports.ports:
        port_name = ports.ports[port].name
    company = "in company" if record.get("company") else "parting company"
    goal = f"for {port_name}, {company}" if port_name else company
    text = (
        f"Possession is taken of the {prize.name} ({record['how']}): {master} and "
        f"{number_words(n)} hands put aboard her as her prize crew, her people, "
        f"{number_words(k)}, prisoners confined below. The colours hoisted over hers. "
        f"She is {goal}."
    )
    data = {"prize": str(prize.id), "captor": str(captor.id)} | {
        k2: v for k2, v in record.items() if k2 in ("crew", "prisoners", "master", "goal", "how")
    }
    _story(captor, tick, f"possession taken of the {prize.name}: a prize, {goal}")
    _story(prize, tick, f"taken by the {captor.name}: a prize under {master}, {goal}")
    # `said` is the captor's own line: an order's road records its reply itself
    if said and captor_hull is not None:
        captor_hull.record(Severity.URGENT, "prize.taken", text, data=data)
    if prize_hull is not None:
        prize_hull.record(
            Severity.URGENT,
            "prize.possessed",
            f"Taken possession of by the {captor.name}'s people: {master} has the command, "
            f"{number_words(n)} of theirs work her; the company, {number_words(k)}, prisoners "
            f"confined below. Her colours over ours. She is {goal}.",
            data=data,
        )


def fill_far_prize(hull: Any, record: dict[str, Any], nation_was: str, tick: int) -> None:
    """A far prize made a hull (or taken with no captor's hull): her file's muster cut to
    the prize crew's count by the bill's order (the trimmers and the helm first), the rest
    her prisoners confined below, her named few confined, a prize master of the captor's
    made from words at her captain's station (the design's §2.6)."""
    crew = hull.ship.extra.get("crew")
    if crew is None or hull.ship.extra.get("prisoners") is not None:
        return
    n = max(1, int(record.get("crew", 0) or PRIZE_CREW_LEAST))
    hands = [
        s
        for s in crew.sailors
        if s.fit and s.station not in (Station.QUARTERDECK, Station.MARINES, Station.IDLERS)
    ]
    hands.sort(key=lambda s: (-_rating_rank(s)[0], s.id))
    keep = hands[:n]
    keep_ids = {s.id for s in keep}
    rest = [s for s in crew.sailors if s.id not in keep_ids]
    new_crew = Crew(ship_name=str(crew.ship_name), sailors=list(keep))
    _watches(new_crew.sailors)
    old_crew = Crew(ship_name=str(crew.ship_name), sailors=list(rest), dead=list(crew.dead))
    if getattr(crew, "post_watches", None):
        # a merchantman's master and mate keep the watches they head, so that retaken they haul
        # with them again (the lead's ruling 11 of 2026-11-13; `hands.post_watch`), as the near
        # prize's company, kept whole, keeps them
        old_crew.post_watches = dict(crew.post_watches)
    for s in old_crew.sailors:
        s.at = None
        s.quarters = ""
    remuster(hull, new_crew)
    hull.ship.extra["prisoners"] = Prisoners(crew=old_crew, nation=nation_was, since=tick)
    hull.ship.extra["prisoners"].parole = _confine_people(hull, tick)
    from freesail.world.court import record_loss

    record_loss(
        _root(hull.world), hull, record
    )  # the loss in her captain's record (the design's §7)
    record["prisoners"] = old_crew_count = len(old_crew.sailors)
    people = getattr(hull, "people", None)
    master_name = str(record.get("master") or "")
    if people is not None:
        from freesail.world.people import Person

        name = master_name or f"the prize master, Mr {_surname(hull, record)}"
        master = Person(
            "prize_master",
            name,
            PRIZE_MASTER_ROLE,
            0.7,
            place="quarterdeck",
            home=str(record.get("master_home") or record.get("captor") or hull.id),
        )
        master.hull = str(hull.id)
        people.add(master)
        people.command_passed_to = master.id
        _bind_captain(hull, master)
        record["master"] = master.name
        record["master_id"] = master.id
    hull.record(
        Severity.NOTABLE,
        "prize.manned",
        f"Her prize crew of {number_words(n)} work her under "
        f"{record.get('master') or 'the prize master'}; "
        f"{number_words(old_crew_count)} of her people prisoners below.",
        data={"crew": n, "prisoners": old_crew_count},
    )


def _surname(hull: Any, record: dict[str, Any]) -> str:
    """A prize master's surname drawn from the captor's names where no person was, by the
    hull's own stream (deterministic), else the record's captor's."""
    try:
        from freesail.crew.muster import name_lists

        lists = name_lists()
        given, surnames = lists.get("english", next(iter(lists.values())))
        rng = hull.rng.stream(PRIZE_STREAM)
        return str(surnames[int(rng.random() * len(surnames)) % len(surnames)])
    except Exception:  # noqa: BLE001
        return str(record.get("captor_name") or "Smith").split()[-1]


# -- given back: retaken or restored ----------------------------------------------------------


def retake(world: Any, prize: Any, *, by: str, how: str, captor: Any = None) -> dict[str, Any]:
    """The prize given back to her people (retaken by them rising, by a cruiser of her
    nation coming up, or restored by a court): the swap back, her nation, colours, role and
    intent her own again, the prize crew her prisoners, the prize master a captive in her
    cabin and his station stood down by the handover's rule; the record kept under `retaken`."""
    world = _root(world)
    tick = int(world.clock.tick)
    rec = dict(record_of(prize) or {})
    hull = _hull(prize)
    nation_was = str(rec.get("nation_was") or prize.nation)
    _nation_words(world, prize, nation_was)
    _set_colours(world, prize, nation_was, "", tick)
    intent = str(rec.get("intent_was") or "")
    role = str(rec.get("role_was") or "")
    prize.role = role
    brain = getattr(prize, "brain", None)
    given = False
    if intent or (brain is not None and getattr(prize, "goal", "")):
        # her own intent again, or her goal's words where she had a brain made for the
        # prize crew alone (a far merchantman with a goal and no brain of her own)
        try:
            _give_intent(world, prize, intent or str(prize.goal), role or _role_of(prize, intent))
            given = True
        except Exception:  # noqa: BLE001  (words the chart no longer reads)
            given = False
    if not given:
        if brain is not None:
            brain.role = _role_of(prize, None)
            from freesail.world.captains import load_doctrine

            brain.doctrine = load_doctrine(brain.role)
            brain.state = None
            brain.planned = False
            brain._stranger = None
        prize.struck = False
        prize.state = "on passage"
        prize.plan = [("lie_to", math.inf)]
    sets = getattr(world, "squadrons", None)
    if sets is not None:
        old = sets.of(prize.id)
        if old is not None:
            old.leave(world, prize.id, how)
    if hull is not None:
        pris = prisoners_of(hull.ship)
        crew = hull.ship.extra.get("crew")
        if pris is not None:
            for s in pris.crew.sailors:
                s.at = None
                s.quarters = ""
            _watches(pris.crew.sailors)
            remuster(hull, pris.crew)
            if crew is not None and crew.sailors:
                for s in crew.sailors:
                    s.at = None
                    s.quarters = ""
                hull.ship.extra["prisoners"] = Prisoners(
                    crew=crew, nation=str(rec.get("captor_nation") or ""), since=tick
                )
            else:
                hull.ship.extra.pop("prisoners", None)
        _free_people(world, hull, rec, tick)
    rec["retaken"] = (how, by, tick)
    if captor is not None:
        rec["recaptor"] = str(captor.id)  # the salvors (the design's §5.2)
        captor_hull = _hull(captor)
        for cb in (
            getattr(captor, "brain", None),
            getattr(captor_hull, "captain", None) if captor_hull is not None else None,
        ):
            if cb is None:
                continue
            # the recaptor's captain has his mark no more (package 74, step 4: wired, the
            # far cruiser came up `engaging` and stayed so over a ship of his own nation):
            # spoken, she is a stranger no more, and he resumes his passage; his hull's captain
            # the same where she is crewed (the whole-change review of 80e703c7, gundeck-2)
            spoken = getattr(cb, "spoken_ids", None)
            if isinstance(spoken, set):
                spoken.add(str(prize.id))
            if str(getattr(cb, "_stranger", "") or "") == str(prize.id) and cb.state in (
                "engaging",
                "chasing",
                "investigating a stranger",
                "taking possession",
            ):
                cb._enter("on passage")
    prize.prize = rec
    _story(prize, tick, f"{how} ({by}): her own people have her again")
    if hull is not None:
        hull.record(
            Severity.URGENT,
            "prize.retaken",
            f"The {prize.name} is {how} ({by}): her own people have her again, the prize crew "
            "prisoners in their turn.",
            data={"prize": str(prize.id), "how": how, "by": by},
        )
    captor_v = _captor_vessel(world, rec)
    if captor_v is not None:
        _story(captor_v, tick, f"the {prize.name} {how} ({by})")
        ch = _hull(captor_v)
        if ch is not None:
            ch.record(
                Severity.URGENT if how != "restored" else Severity.NOTABLE,
                "prize.lost",
                f"The {prize.name}, our prize, is {how} ({by}).",
                data={"prize": str(prize.id), "how": how, "by": by},
            )
    # the player's person his own ship's captain again: the mark of who he is is past
    from freesail.world.captive import settle_person

    settle_person(world)
    return rec


def adversarial_seat_why(world: Any, vessel: Any, station: str) -> str | None:
    """Why a model may not be seated at `station` of `vessel` (the design's §6): the
    captain's station of a hull adversarial to a human, read from the world at the seating:
    her nation at war with the nation of a hull a human holds (the player's own, or the hull
    the player's person is on), or her holding a human's person as a prisoner (a prize
    master's over a prize whose prisoners include him, the captor over a captive); None when
    the seat is no such thing, or the flag `seats.ADVERSARIAL_SEATS_CONSENTED` is turned. A
    passenger's voice aboard an enemy, a prisoner's, a lookout's fire into nobody."""
    from freesail.agents.agent import CAPTAIN
    from freesail.world import knowledge, seats
    from freesail.world.captive import is_captive

    if getattr(seats, "ADVERSARIAL_SEATS_CONSENTED", False) or vessel is None:
        return None
    if str(station or "").lower() not in (CAPTAIN, "the captain", "prize master"):
        return None
    root = _root(world)
    nations = getattr(root, "nations", None)
    hulls = getattr(root, "hulls", None) or {}
    human_hulls: list[Any] = []
    players = knowledge.player_hull(root)
    if players is not None:
        human_hulls.append(players)
    person = None
    try:
        person = knowledge.players_person(root)
    except Exception:  # noqa: BLE001
        person = None
    if person is not None:
        on = hulls.get(str(getattr(person, "hull", "") or ""))
        if on is not None and all(on is not h for h in human_hulls):
            human_hulls.append(on)
    her_hull = _hull(vessel)
    human_names: list[str] = []
    for h in human_hulls:
        hv = getattr(h, "vessel", None)
        if her_hull is not None and h is her_hull:
            continue
        his_nation = str(getattr(hv, "nation", "") or getattr(root.scenario, "nation", "") or "")
        his_name = str(getattr(getattr(h, "ship", None), "name", "") or "the player's ship")
        if nations is not None and his_nation and nations.at_war(str(vessel.nation), his_nation):
            human_names.append(f"an enemy of the {his_name}'s")
    if (
        person is not None
        and her_hull is not None
        and str(getattr(person, "hull", "") or "") == str(her_hull.id)
        and is_captive(person)
    ):
        human_names.append(f"who holds {person.name} her prisoner")
    if not human_names:
        return None
    why = " and ".join(dict.fromkeys(human_names))
    return (
        "The consent brief names no role in which a model fires into a human's ship or takes "
        "him prisoner; until it is revised and the question put again, the game seats no model "
        f"as the captain of the {vessel.name}, {why}. Her rules-based captain and the "
        "director's voice serve meanwhile (rule 4)."
    )


def _role_of(vessel: Any, intent_words: str | None) -> str:
    from freesail.world.brains import role_of_vessel
    from freesail.world.captains import read_intent

    intent = None
    if intent_words:
        try:
            intent = read_intent(_root(getattr(vessel.brain, "world", None)), intent_words)
        except Exception:  # noqa: BLE001
            intent = None
    return role_of_vessel(vessel, intent)


def _captor_vessel(world: Any, rec: dict[str, Any]) -> Any:
    sea = getattr(world, "vessels", None)
    return sea.get(str(rec.get("captor") or "")) if sea is not None else None


def _free_people(world: Any, hull: Any, rec: dict[str, Any], tick: int) -> None:
    """Her named few unconfined and her stations hers again; the prize master a prisoner in
    her cabin, his station stood down by the handover's rule, rehomed to his ship."""
    from freesail.world.movement import harness_of, seat_of_person

    people = getattr(hull, "people", None)
    if people is None:
        return
    hid = str(hull.id)
    master_id = str(rec.get("master_id") or "")
    registry = getattr(world, "registry", None)
    master = None
    for p in list(people.people):
        if p.id == master_id and p.name == rec.get("master"):
            master = p
            continue
        if str(getattr(p, "hull", "") or "") == hid:
            p.confined_to = ""
    people.command_passed_to = None
    stations = getattr(hull, "stations", None)
    if master is not None:
        held = harness_of(world, master)
        if held is not None:
            held[1].stand_down("taken in the prize", by="the handover")
        seated = seat_of_person(world, master)
        if seated is not None:
            seated[1].stand_down_quietly("taken in the prize")
        master.confined_to = PRISONER_PLACES["officer"]
        master.where = PRISONER_PLACES["officer"]
        home = str(rec.get("master_home") or rec.get("captor") or "")
        if registry is not None and home and home != hid:
            registry.rehome(master, home)
    if stations is not None:
        try:
            captain = people.captain
            if captain is not None and not getattr(captain, "confined_to", ""):
                stations.bind("captain", captain, quiet=True)
        except Exception:  # noqa: BLE001
            pass


# -- burning and scuttling -------------------------------------------------------------------


def burn(world: Any, captor: Any, prize: Any, *, how: str = "burnt", said: bool = True) -> str:
    """A prize not worth manning (the captor's doctrine, `burns_when`) or burnt by the
    order: her people into the captor as prisoners (the prize crew home again), the vessel
    gone from the sea with the word; nothing paid for her at any court but the head money.
    Returns the line."""
    world = _root(world)
    tick = int(world.clock.tick)
    rec = dict(record_of(prize) or {})
    captor_hull, prize_hull = _hull(captor), _hull(prize)
    taken = 0
    if prize_hull is not None and captor_hull is not None:
        taken = take_prisoners_aboard(world, captor, prize, None, said=False)
        crew = prize_hull.ship.extra.get("crew")
        if crew is not None and rec.get("manned", True):
            back = captor_hull.ship.extra.get("crew")
            if back is not None:
                for s in crew.sailors:
                    s.at = None
                    s.quarters = ""
                back.sailors.extend(crew.sailors)
                back.reindex()
            crew.sailors = []
            crew.reindex()
        people = getattr(prize_hull, "people", None)
        if people is not None:
            from freesail.world.movement import put_aboard

            for p in list(people.people) + list(getattr(prize_hull, "aboard", [])):
                if str(getattr(p, "hull", "") or "") == str(prize_hull.id) and not getattr(
                    p, "dead", False
                ):
                    put_aboard(
                        world,
                        p,
                        captor_hull,
                        "hold",
                        seat="stands down",
                        why="her prize burnt",
                        by="the captor",
                        said=False,
                    )
                    if p.id == rec.get("master_id"):
                        p.confined_to = ""
                        p.where = "quarterdeck"
                        registry = getattr(world, "registry", None)
                        if registry is not None:
                            registry.rehome(p, str(captor_hull.id))
    elif captor_hull is not None:
        kept = captor_hull.ship.extra.get("prize_crews", {}) or {}
        men = kept.pop(str(prize.id), [])
        back = captor_hull.ship.extra.get("crew")
        if back is not None and men:
            for s in men:
                s.at = None
            back.sailors.extend(men)
            back.reindex()
        taken = int(rec.get("prisoners", 0))
    rec["manned"] = False
    rec["fate"] = (how, tick)
    prize.prize = rec
    prize.done = True
    prize.struck = True
    text = (
        f"The {prize.name} is {how}: her people, {number_words(taken)}, taken aboard as "
        "prisoners, the prize crew home again; nothing is to be had for her at any court but "
        "the head money, if she was a ship of war."
    )
    _story(captor, tick, f"the {prize.name} {how}")
    _story(prize, tick, how)
    if said and captor_hull is not None:
        captor_hull.record(
            Severity.URGENT,
            "prize.burnt",
            text,
            data={"prize": str(prize.id), "how": how, "prisoners": taken},
        )
    return text


def take_prisoners_aboard(
    world: Any, captor: Any, prize: Any, n: int | None, *, said: bool = True
) -> int:
    """So many of the prize's prisoners (all when `n` is None) taken into the captor's hold
    by the boat, where they are prisoners of his (`ship.extra["prisoners"]` on the captor).
    Returns how many came."""
    world = _root(world)
    tick = int(world.clock.tick)
    captor_hull, prize_hull = _hull(captor), _hull(prize)
    if captor_hull is None or prize_hull is None:
        return 0
    pris = prisoners_of(prize_hull.ship)
    if pris is None or pris.count == 0:
        return 0
    moving = pris.alive if n is None else pris.alive[: max(0, int(n))]
    ids = {s.id for s in moving}
    pris.crew.sailors = [s for s in pris.crew.sailors if s.id not in ids]
    pris.crew.reindex()
    pris.divided_out += len(moving)
    held = prisoners_of(captor_hull.ship)
    if held is None:
        held = Prisoners(
            crew=Crew(ship_name=str(prize.name), sailors=[]), nation=pris.nation, since=tick
        )
        captor_hull.ship.extra["prisoners"] = held
    for s in moving:
        s.at = None
        s.quarters = ""
    # a prisoner's id is his old company's; two companies' men in one hold are told apart by
    # the ship they came from, prefixed once
    for s in moving:
        if not s.id.startswith(f"{prize.id}:"):
            s.id = f"{prize.id}:{s.id}"
    held.crew.sailors.extend(moving)
    held.crew.reindex()
    if said:
        captor_hull.record(
            Severity.NOTABLE,
            "prize.prisoners_aboard",
            f"{number_words(len(moving))} of the {prize.name}'s people taken aboard by the boat "
            f"and confined in the hold; {number_words(pris.count)} left in her.",
            data={"prize": str(prize.id), "taken": len(moving), "left": pris.count},
        )
    return len(moving)


# -- the rising ---------------------------------------------------------------------------------


def _captor_near(world: Any, prize: Any, rec: dict[str, Any]) -> bool:
    """A ship of the captor's nation within the cover distance (awake or far) who could support
    her prize crew: the one answer (`relations.still`, `SUPPORT` within `COVER_NM`: on the sea,
    not struck, nobody's prize; the lead's readings of cda12ec9, the far fight's family), so that
    another prize of hers, or a ship of hers struck, holds no prisoners down."""
    from freesail.world import relations as R

    sea = getattr(world, "vessels", None)
    if sea is None:
        return False
    nation = str(prize.nation)
    for o in list(sea.vessels):
        if o is prize or o.done or str(o.nation) != nation:
            continue
        if str(o.id) == str(rec.get("captor")) or getattr(o, "brain", None) is not None:
            if R.still(world, prize, o, R.SUPPORT, within_nm=COVER_NM):
                return True
    return False


def _tired(hull: Any, rec: dict[str, Any], tick: int) -> bool:
    crew = hull.ship.extra.get("crew")
    if crew is None or not crew.sailors:
        return True
    fatigue = sum(float(s.fatigue) for s in crew.sailors) / len(crew.sailors)
    hours = (tick - int(rec.get("taken_at", tick))) / 3600.0
    return fatigue >= RISING_FATIGUE or hours >= RISING_HOURS


def minute(hull: Any) -> None:
    """The prize's minute (awake or asleep): the prisoners rising by the rule of the
    module's head, once an hour while the conditions hold."""
    ship = getattr(hull, "ship", None)
    pris = prisoners_of(ship) if ship is not None else None
    vessel = getattr(hull, "vessel", None)
    rec = record_of(vessel) if vessel is not None else None
    world = _root(hull.world)
    tick = int(world.clock.tick)
    if vessel is not None:
        _over_down(vessel, tick)
    if pris is not None and getattr(hull, "awake", True):
        # the captor's side (the captive's channel): the parole by doctrine, the prisoners
        # landed in port
        from freesail.world.captive import minute as captive_minute

        captive_minute(hull)
    if vessel is not None and rec:
        _court_minute(hull, vessel, rec, tick)
    if pris is None or vessel is None or not rec or not is_prize(vessel):
        return
    if pris.in_irons(tick) or pris.count == 0:
        return
    last = int(rec.get("rising_judged", rec.get("taken_at", tick)))
    if tick - last < 3600:
        return
    rec["rising_judged"] = tick
    crew = ship.extra.get("crew")
    fit = sum(1 for s in crew.sailors if s.fit) if crew is not None else 0
    if pris.fit < RISING_ODDS * max(fit, 1):
        return
    if not _tired(hull, rec, tick):
        return
    if _captor_near(world, vessel, rec):
        return
    rng = hull.rng.stream(PRIZE_STREAM)
    if rng.random() >= RISING_CHANCE:
        return
    _rise(world, hull, vessel, pris, rng, tick)


def _none(n: int) -> str:
    return "none" if n == 0 else number_words(n)


def _rise(world: Any, hull: Any, vessel: Any, pris: Prisoners, rng: Any, tick: int) -> None:
    """The fight on one deck by 73's tables: the prize crew the defenders (their arms
    served, the captor's temper), the prisoners the attackers (unarmed, their old doctrine's
    temper, the boarders' cover in the first round)."""
    from freesail.combat import boarding as B
    from freesail.combat.hits import hit_man
    from freesail.combat.small_arms import small_arms_of

    pris.rose_at.append(tick)
    crew = hull.ship.extra["crew"]
    arms = small_arms_of(hull)
    served = float(arms.get("served_factor", 1.0))
    unarmed = float(arms.get("unserved_factor", 0.5))
    rec = record_of(vessel) or {}
    temper_crew = float(rec.get("morale", 0.7) or 0.7)
    temper_pris = 0.5
    lost_crew = lost_pris = 0
    hull.record(
        Severity.URGENT,
        "prize.rising",
        f"The prisoners are rising! {number_words(pris.fit)} of them up the hatchways against "
        f"{number_words(sum(1 for s in crew.sailors if s.fit))} of the prize crew.",
        data={"prisoners": pris.fit, "crew": sum(1 for s in crew.sailors if s.fit)},
    )
    outcome = "contested"
    for rnd in range(1, RISING_ROUNDS_MOST + 1):
        defenders = [(s, served) for s in crew.sailors if s.fit]
        attackers = [(s, unarmed) for s in pris.crew.sailors if s.fit]
        first = rnd == 1
        sd = B._strength(defenders, temper_crew, 1.0)
        sa = B._strength(attackers, temper_pris, B.FIRST_ROUND_ATTACK if first else 1.0)
        lose_d = min(len(defenders), B._poisson(B.ROUND_LOSS * sa / 10.0, rng))
        lose_a = min(len(attackers), B._poisson(B.ROUND_LOSS * sd / 10.0, rng))
        for _i in range(lose_d):
            s = defenders[int(rng.random() * len(defenders)) % len(defenders)][0]
            if s.fit:
                killed = rng.random() < B.KILLED_SHARE
                hit_man(hull.ship, s, killed, rng, tick, how="a blow in the rising")
        for _i in range(lose_a):
            s = attackers[int(rng.random() * len(attackers)) % len(attackers)][0]
            if s.fit:
                s.fit = False
                s.hurt = "killed" if rng.random() < B.KILLED_SHARE else "wounded"
                s.hurt_tick = tick
                s.hurt_how = "a blow in the rising"
        lost_crew += lose_d
        lost_pris += lose_a
        defenders = [s for s in crew.sailors if s.fit]
        attackers = [s for s in pris.crew.sailors if s.fit]
        sd = B._strength([(s, served) for s in defenders], temper_crew, 1.0)
        sa = B._strength([(s, unarmed) for s in attackers], temper_pris, 1.0)
        if not defenders or sd < B.CARRIED_RATIO * sa:
            outcome = "retaken"
            break
        if not attackers or sa < B.CARRIED_RATIO * sd:
            outcome = "put down"
            break
    if outcome == "retaken":
        hull.record(
            Severity.URGENT,
            "prize.rising_won",
            f"The prisoners have the deck: {number_words(lost_crew)} of the prize crew down, "
            f"{_none(lost_pris)} of theirs.",
            data={"lost_crew": lost_crew, "lost_prisoners": lost_pris},
        )
        retake(world, vessel, by="the prisoners rising", how="retaken")
    else:
        pris.irons_until = tick + IRONS_HOURS * 3600
        hull.record(
            Severity.URGENT,
            "prize.rising_down",
            f"The rising is put down: {_none(lost_pris)} of the prisoners down and the "
            f"rest in irons, {_none(lost_crew)} of the prize crew hurt.",
            data={"lost_crew": lost_crew, "lost_prisoners": lost_pris, "irons_h": IRONS_HOURS},
        )


def _court_minute(hull: Any, vessel: Any, rec: dict[str, Any], tick: int) -> None:
    """The prize court's road for a prize hull (the design's §5.2): lying in a port open to
    her captor's nation she queues the port's job `prize_court`, due in the court's days by
    the port's nation; a ship retaken by her own nation's cruiser queues the salvage sentence
    the same; the reserved fourth is paid when its day comes."""
    from freesail.world import prize_court as PC
    from freesail.world.ports import Job

    world = _root(hull.world)
    if rec.get("court"):
        due = rec.get("reserved_due")
        if due is not None and tick >= int(due):
            PC.pay_reserved(world, vessel)
        return
    if rec.get("court_due") is not None:
        return
    salvage = bool(rec.get("recaptor")) and not is_prize(vessel)
    if not is_prize(vessel) and not salvage:
        return
    dealings = getattr(hull, "dealings", None)
    port = dealings.in_port() if dealings is not None else None
    if port is None:
        return
    nation = str(rec.get("captor_nation") or "")
    if salvage:
        recaptor = world.vessels.get(str(rec.get("recaptor") or ""))
        nation = str(getattr(recaptor, "nation", "") or vessel.nation)
    ports = getattr(world, "ports", None)
    try:
        stance = ports.stance(port, nation) if ports is not None else "open"
    except Exception:  # noqa: BLE001
        stance = "open"
    if stance != "open":
        if not rec.get("no_court_said"):
            rec["no_court_said"] = tick
            hull.record(
                Severity.NOTABLE,
                "prize.no_court",
                f"{port.name} is {stance} to the captors: no court sits for the {vessel.name} "
                "here; she lies in the road.",
                data={"port": port.id, "stance": stance},
            )
        return
    days = PC.court_days(port)
    due = tick + days * 86400
    rec["court_due"] = due
    rec["court_port"] = port.id
    dealings.jobs.append(
        Job(
            due,
            "prize_court",
            port.id,
            {"prize": str(vessel.id), "salvage": salvage},
            words=f"the court on the {vessel.name}",
            hull=str(hull.id),
        )
    )
    hull.record(
        Severity.NOTABLE,
        "prize.court_sits",
        f"The {vessel.name} is brought in at {port.name}: {PC.court_name(port, False)} will sit "
        f"on her in {days} days.",
        data={"port": port.id, "due": due, "salvage": salvage},
    )


def _far_court(world: Any, v: Any, rec: dict[str, Any], tick: int) -> None:
    """A far prize with no hull in her goal's road (the design's §5.2): the court sits on her
    record in the court's days, the sentence as a hull's."""
    from freesail.world import prize_court as PC

    if rec.get("court"):
        due = rec.get("reserved_due")
        if due is not None and tick >= int(due):
            PC.pay_reserved(world, v)
        return
    ports = getattr(world, "ports", None)
    table = getattr(ports, "ports", {}) or {}
    port = table.get(str(rec.get("goal") or ""))
    if port is None or v.position is None:
        return
    due = rec.get("court_due")
    if due is None:
        _, d = _bearing_distance(v.position, port.outer_road.position)
        if d > float(getattr(port, "reach_nm", 2.0)) * units.NAUTICAL_MILE:
            return
        rec["court_due"] = tick + PC.court_days(port) * 86400
        rec["court_port"] = port.id
        _story(v, tick, f"brought in at {port.name}: the court sits in {PC.court_days(port)} days")
    # she lies in the road until the court has sat (a far body whose plan runs out is done
    # and gone from the sea at the minute's end; the court's days keep her)
    v.done = False
    v.plan = [("lie_to", math.inf)]
    if tick >= int(rec["court_due"]):
        PC.sentence(world, v, port)
        v.done = True  # her business on the sea is over: in port, sentenced


def _over_down(vessel: Any, tick: int) -> None:
    """The captor's colours over hers hauled down after a day (the sign of a prize new taken)."""
    locker = getattr(vessel, "signals", None)
    colours = getattr(locker, "colours", None)
    if colours is None or not getattr(colours, "over", ""):
        return
    if tick - int(getattr(colours, "over_since", 0) or 0) >= OVER_COLOURS_S:
        colours.over = ""
        colours.over_since = 0


def far_minute(world: Any) -> list[tuple[Any, ...]]:
    """The far records' minute (`Vessels.tick`): a captor in `taking possession` at hailing
    distance of his struck mark takes her (the far possession); a far prize with no hull
    and prisoners on her record rises by the counts alone (the design's §2.8)."""
    from freesail.world.brains import HAIL_REACH_M

    lines: list[tuple[Any, ...]] = []
    sea = getattr(world, "vessels", None)
    if sea is None:
        return lines
    tick = int(world.clock.tick)
    from freesail.world.captive import cartel_minute

    lines.extend(cartel_minute(world))
    for v in list(sea.vessels):
        if getattr(v, "prize", None) and _hull(v) is None:
            _over_down(v, tick)
        brain = getattr(v, "brain", None)
        if v.done or brain is None or brain.state != "taking possession":
            continue
        hull = _hull(v)
        if hull is not None and hull.awake:
            continue  # the near captain's own work (`Captain._take_possession`)
        from freesail.world import relations as R

        prey = sea.get(str(brain._stranger or ""))
        if prey is None or not R.still(world, v, prey, R.STRUCK):
            # (the lead's readings of cda12ec9, (F2)): no longer hers to take, by the one answer;
            # her judgement gives her up at its next minute (`Judgement._prize_taken`)
            continue
        _, d = _bearing_distance(v.position, prey.position)
        if d > HAIL_REACH_M:
            continue
        possess(world, v, prey, by="struck at far detail")
        lines.append(
            (
                Severity.NOTABLE,
                "prize.taken",
                f"{v.name} takes possession of the {prey.name}, struck to her.",
                {"captor": v.id, "prize": prey.id},
            )
        )
    for v in list(sea.vessels):
        rec = record_of(v)
        if not rec or not is_prize(v) or _hull(v) is not None:
            continue
        if v.done and not (rec.get("court_due") and not rec.get("court")):
            continue
        _far_court(world, v, rec, tick)
        if v.done or not is_prize(v):
            continue
        # the counts' rising: the same odds on the record, the losses as counts
        last = int(rec.get("rising_judged", rec.get("taken_at", tick)))
        if tick - last < 3600:
            continue
        rec["rising_judged"] = tick
        crew, pris = int(rec.get("crew", 0)), int(rec.get("prisoners", 0))
        hours = (tick - int(rec.get("taken_at", tick))) / 3600.0
        if pris < RISING_ODDS * max(crew, 1) or hours < RISING_HOURS or _captor_near(world, v, rec):
            continue
        rng = world.rng.stream(PRIZE_STREAM)
        if rng.random() >= RISING_CHANCE:
            continue
        lost = min(crew, 1 + int(rng.random() * 3))
        rec["crew"] = crew - lost
        rec["prisoners"] = max(0, pris - int(rng.random() * 3))
        retake(world, v, by="the prisoners rising", how="retaken")
        lines.append(
            (
                Severity.NOTABLE,
                "prize.retaken",
                f"The {v.name}, prize to {rec.get('captor_name', 'her captor')}, is retaken by "
                "her prisoners rising.",
                {"prize": v.id},
            )
        )
    return lines
