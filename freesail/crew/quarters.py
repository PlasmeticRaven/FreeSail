"""The quarter bill at run time (spec M7 §8a; package 70; the design in
`docs/design/Design-WorkInAction.md`).

The watch bill (`crew/bill.py`) says who is on deck; at quarters every fit hand is, and
this module says **where each man stands**: the gun crews by the fit (one crew to the pair
of one number, who fight whichever gun bears and are divided when both do), the sail
trimmers by station (the men who leave the guns for a brace or a sail), the hands at the
helm, the powder, the marines, the carpenter's crew at the wings and the surgeon's mates in
the cockpit. The bill is data in the ship file (`crew.quarter_bill`, the gun crews in the
fit's `crew` figures; `tools/gen_ships.py` writes both with their sources); the runtime
here assigns each man once at the beat to quarters, deterministically from the muster in
id order within each station's preference, and keeps `Sailor.quarters` for him.

**One assignment of the same men.** Nothing here is a second crew: a man at a gun is the
muster's sailor with his `at` set to his gun crew's key (`"gun:3"`), so that the watch
bill, the needs, the routine's fatigue and every reader of the muster see him where he
is, and a sail evolution asking the runner for hands finds the trimmers idle and the gun
crews busy, as the period had it.

**Robbing (the fighting book's priority).** When sail work wants more hands than the
trimmers give, `lend` frees them by the bill's priority: under `sail before guns` from the
gun crews, the swivels and the chasers first, then the broadside crews from the end that
bears least on the enemy (the after guns when she engages on the bow, the forward when on
the quarter; the whole of a crew before the next, so that one gun falls silent rather
than two go short), then the marines, the powder last, never the helm, the carpenter's
crew or the surgeon's; under `guns before sail` nothing, and the sail work waits
short-handed. The line that begins the work says from where. Hands come back of
themselves: each tick a man at quarters whose `at` is None is put back at his quarters
station (`tick`), so the guns refill as the tack ends, the forward guns first.

Nothing here draws randomness.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from freesail.crew.model import Crew, Rating, Sailor, Station, number_words
from freesail.ship.parts import Gun

__all__ = [
    "CARPENTER",
    "GUN_PREFIX",
    "HELM",
    "MARINES",
    "POWDER",
    "SURGEON",
    "TRIMMERS",
    "GunCrew",
    "Quarters",
    "quarters_of",
]

GUN_PREFIX = "gun:"
TRIMMERS = "trimmers"
HELM = "helm"
POWDER = "powder"
MARINES = "marines"
CARPENTER = "carpenter"
SURGEON = "surgeon"

# The trades quartered by their trade (Luce 1884 ch. XX: the carpenter's crew to the wings
# and the pumps, the surgeon's mates to the cockpit); the rest of the idlers pass powder.
_TRADE_STATIONS = {"carpenter's crew": CARPENTER, "surgeon's mate": SURGEON}

# The share of a gun crew told off for the sails at quarters (Luce 1884 ch. XX, the station
# bill: the boarders and sail trimmers "told off from the guns' crews"; half, judgement):
# an all-hands manoeuvre under `sail before guns` takes this much of each crew.
TOLD_OFF_SHARE = 0.5

# A gun forward of this share of the hull's length is a forward gun, abaft its negative an
# after gun, for the stations that man it (the forecastlemen forward, the afterguard aft,
# the waisters amidships: Luce 1884 ch. XX, the quarter bill by divisions; judgement).
FORWARD_SHARE = 1.0 / 6.0


@dataclass
class GunCrew:
    """The crew of one gun pair (or one chaser or swivel): its key, the guns it serves,
    the men wanted and the men assigned (sailor ids, in id order)."""

    key: str
    guns: list[str]
    wanted: int
    members: list[Sailor] = field(default_factory=list)
    x_m: float = 0.0
    kind: str = "long"

    @property
    def hands(self) -> list[Sailor]:
        """The men at the gun now: assigned, fit, and not lent to other work."""
        return [s for s in self.members if s.fit and s.at == self.key]

    @property
    def short(self) -> int:
        return max(0, self.wanted - len(self.hands))


class Quarters:
    """The company at quarters, kept in `ship.extra["quarters"]` (`quarters_of`)."""

    def __init__(self, ship: Any, crew: Crew) -> None:
        self.ship = ship
        self.crew = crew
        self.at_quarters = False
        self.since: int | None = None
        self.crews: dict[str, GunCrew] = {}
        self.divisions: dict[str, list[Sailor]] = {}
        spec = getattr(getattr(ship, "spec", None), "crew", None)
        bill = getattr(spec, "quarter_bill", None)
        self.priority = str(getattr(bill, "priority", "sail before guns") or "sail before guns")
        self._robbed_lines: list[str] = []

    # -- the marines between the carronades and their muskets (package 73, spec M7 §11) ----

    def marines_to_arms(self) -> int:
        """The marines leave the guns for their muskets (the quarterdeck carronades they
        serve at the beat, Luce 1884 ch. XX, go short by them): every fit marine at a gun
        into the marines' division. Returns how many moved."""
        from freesail.crew.model import Station

        moved = 0
        division = self.divisions.setdefault(MARINES, [])
        for gc in self.crews.values():
            keep = []
            for s in gc.members:
                if s.station is Station.MARINES and s.fit:
                    s.quarters = MARINES
                    division.append(s)
                    moved += 1
                else:
                    keep.append(s)
            gc.members = keep
        return moved

    def marines_to_guns(self) -> int:
        """The marines back to the carronades from their muskets: each short crew made up
        from the division, the carronades first. Returns how many moved."""
        division = self.divisions.get(MARINES, [])
        if not division:
            return 0
        moved = 0
        crews = sorted(self.crews.values(), key=lambda gc: (gc.kind != "carronade", gc.key))
        for gc in crews:
            while len(gc.members) < gc.wanted and division:
                s = division.pop(0)
                s.quarters = gc.key
                gc.members.append(s)
                moved += 1
        return moved

    # -- the beat to quarters and the pipe down ------------------------------------------

    def beat(self, tick: int) -> list[str]:
        """Assign every fit hand his station by the bill. Returns the lines for the log:
        the bill in brief, and the guns left unmanned where the company is short."""
        ship, crew = self.ship, self.crew
        spec = getattr(getattr(ship, "spec", None), "crew", None)
        bill = getattr(spec, "quarter_bill", None)
        guns: list[Gun] = sorted(getattr(ship, "guns", {}).values(), key=lambda g: _gun_order(g))
        pool = [s for s in crew.sailors if s.fit and s.station is not Station.QUARTERDECK]
        for s in pool:
            s.quarters = ""
        taken: set[str] = set()

        def take(candidates: list[Sailor], n: int, where: str) -> list[Sailor]:
            out = []
            for s in candidates:
                if len(out) >= n:
                    break
                if s.id in taken:
                    continue
                taken.add(s.id)
                s.quarters = where
                out.append(s)
            return out

        divisions: dict[str, list[Sailor]] = {
            TRIMMERS: [],
            HELM: [],
            POWDER: [],
            MARINES: [],
            CARPENTER: [],
            SURGEON: [],
        }
        by_station = {st: [s for s in pool if s.station is st] for st in Station}
        # the trades by their trade, first
        for s in by_station[Station.IDLERS]:
            where = _TRADE_STATIONS.get(str(s.trade or ""))
            if where:
                divisions[where] += take([s], 1, where)
        # the trimmers by the bill's stations
        trimmers = dict(getattr(bill, "trimmers", {}) or {})
        for station_word, n in trimmers.items():
            st = Station(station_word)
            divisions[TRIMMERS] += take(by_station[st], int(n), TRIMMERS)
        # the helm: able men of the afterguard, else the best there are
        helm_n = int(getattr(bill, "helm", 2) or 0)
        able_ag = [s for s in by_station[Station.AFTERGUARD] if s.rating is Rating.ABLE]
        divisions[HELM] += take(able_ag, helm_n, HELM)
        if len(divisions[HELM]) < helm_n:
            rest = [s for s in pool if s.station is not Station.MARINES]
            divisions[HELM] += take(rest, helm_n - len(divisions[HELM]), HELM)
        # the gun crews, forward first, chasers next, the swivels last
        length = float(getattr(getattr(ship, "hull", None), "length", 40.0) or 40.0)
        crews: dict[str, GunCrew] = {}
        has_marines = bool(by_station[Station.MARINES])
        for g in guns:
            key = g.pair_key
            gc = crews.get(key)
            if gc is None:
                gc = crews[key] = GunCrew(key, [], int(g.crew_n), x_m=g.x_m, kind=g.kind)
            gc.guns.append(g.id)
        for key, gc in crews.items():
            prefs = _preferred_stations(gc, length, has_marines)
            candidates = [s for st in prefs for s in by_station[st]]
            gc.members = take(candidates, gc.wanted, key)
        # the powder: the bill's hands beyond the idlers, landsmen first, and every idler
        # left; the marines left to the marines' division; the rest to the trimmers
        powder_n = int(getattr(bill, "powder", 0) or 0)
        landsmen = [
            s for s in pool if s.rating is Rating.LANDSMAN and s.station is not Station.MARINES
        ]
        divisions[POWDER] += take(landsmen, powder_n, POWDER)
        if len(divisions[POWDER]) < powder_n:
            rest = [s for s in pool if s.station not in (Station.MARINES, Station.IDLERS)]
            divisions[POWDER] += take(rest, powder_n - len(divisions[POWDER]), POWDER)
        divisions[POWDER] += take(by_station[Station.IDLERS], len(pool), POWDER)
        divisions[MARINES] += take(by_station[Station.MARINES], len(pool), MARINES)
        divisions[TRIMMERS] += take(pool, len(pool), TRIMMERS)
        self.crews = crews
        self.divisions = divisions
        self.at_quarters = True
        self.since = tick
        crew.all_hands_called = True
        crew.all_hands_called_by_order = True
        crew.all_hands_called_by = "quarters"
        for s in pool:
            s.turned_up = True
        self._to_stations()
        return self._beat_lines()

    def stand_down(self) -> None:
        """The guns secured or the hands piped down: every man back under the watch bill."""
        for gc in self.crews.values():
            for s in gc.members:
                if s.at == gc.key:
                    s.at = None
        for s in self.crew.sailors:
            s.quarters = ""
        self.crews = {}
        self.divisions = {}
        self.at_quarters = False
        self.since = None
        crew = self.crew
        crew.all_hands_called_by_order = False
        crew.all_hands_called_by = ""

    # -- each tick --------------------------------------------------------------------

    def tick(self) -> None:
        """A man at quarters whose work is done goes back to his quarters station."""
        if self.at_quarters:
            self._to_stations()

    def _to_stations(self) -> None:
        for gc in self.crews.values():
            for s in gc.members:
                if s.fit and s.at is None:
                    s.at = gc.key

    # -- what is at each gun ----------------------------------------------------------

    def crew_of(self, gun: Gun) -> GunCrew | None:
        return self.crews.get(gun.pair_key)

    def hands_at(self, gun: Gun) -> list[Sailor]:
        gc = self.crews.get(gun.pair_key)
        return gc.hands if gc is not None else []

    def wanted_at(self, gun: Gun) -> int:
        gc = self.crews.get(gun.pair_key)
        return gc.wanted if gc is not None else int(gun.crew_n)

    def casualties(self) -> tuple[int, int]:
        """(killed, wounded) of the whole company, by the muster's hurt."""
        killed = sum(1 for s in self.crew.sailors if s.hurt == "killed")
        killed += len(getattr(self.crew, "dead", []) or [])  # buried (package 73)
        wounded = sum(1 for s in self.crew.sailors if s.hurt in ("wounded", "hurt"))
        return killed, wounded

    # -- robbing by the fighting book's priority ----------------------------------------

    def lend(
        self, want: int, aloft: bool, bearing_fwd: bool | None, share: float | None = None
    ) -> tuple[list[Sailor], str]:
        """Free `want` hands for sail work by the priority: the swivels' and the chasers'
        crews first, then the broadside crews from the end that bears least (`bearing_fwd`
        true when the enemy is forward of the beam, so the after guns go first; None, the
        after guns), whole crews before the next; then the marines; the powder last. With
        `share` (an all-hands manoeuvre) each crew gives that share of its hands instead,
        the guns going on short-handed. Returns the men freed (their `at` cleared) and the
        words for the log ('from the larboard guns, Nos. 3 to 6' or ''); nothing under
        `guns before sail`."""
        if not self.at_quarters or want <= 0 or self.priority != "sail before guns":
            return [], ""
        from freesail.crew import hands as H

        freed: list[Sailor] = []
        from_guns: list[str] = []
        if share is not None:
            for gc in self.crews.values():
                at = [s for s in gc.hands if H.can_work(s, aloft)]
                n = int(len(at) * share)
                for s in at[:n]:
                    s.at = None
                    freed.append(s)
                if n:
                    from_guns.append(gc.key)
            words = f"from the guns, {_share_words(share)} of each crew" if freed else ""
            return freed, words
        order = sorted(self.crews.values(), key=lambda gc: _rob_order(gc, bearing_fwd))
        for gc in order:
            if len(freed) >= want:
                break
            at = [s for s in gc.hands if H.can_work(s, aloft)]
            if not at:
                continue
            for s in at:
                s.at = None
                freed.append(s)
            from_guns.append(gc.key)
        words = f"from {self._guns_words(from_guns)}" if from_guns else ""
        if len(freed) < want:
            marines = [
                s
                for s in self.divisions.get(MARINES, [])
                if s.fit and s.at is None and H.can_work(s, aloft)
            ]
            # the marines are idle by the bill (their fire is 73's): they are lent as they
            # stand, counted here so that the line says it
            if marines:
                words += (", and " if words else "") + "the marines"
        return freed, words

    def _guns_words(self, keys: list[str]) -> str:
        """'the swivels', 'the bow chasers', 'the guns, Nos. 7 to 9' for the crews robbed."""
        numbers = sorted(int(k[len(GUN_PREFIX) :]) for k in keys if k[len(GUN_PREFIX) :].isdigit())
        others = [k for k in keys if not k[len(GUN_PREFIX) :].isdigit()]
        parts: list[str] = []
        kinds: set[str] = set()
        for k in others:
            gid = k[len(GUN_PREFIX) :]
            g = self.ship.guns.get(gid)
            if g is not None:
                kinds.add("the swivels" if g.place == "rail" else f"the {g.place} chasers")
        parts += sorted(kinds)
        if numbers:
            if len(numbers) == 1:
                parts.append(f"No. {numbers[0]} gun")
            else:
                runs = _runs(numbers)
                parts.append("the guns, Nos. " + " and ".join(runs))
        return " and ".join(parts)

    # -- words ----------------------------------------------------------------------

    def _beat_lines(self) -> list[str]:
        manned = sum(1 for gc in self.crews.values() if len(gc.members) * 2 >= gc.wanted)
        short = [gc for gc in self.crews.values() if gc.wanted and len(gc.members) * 2 < gc.wanted]
        marines = self.divisions.get(MARINES, [])
        at_work = sum(
            1 for gc in self.crews.values() for m in gc.members if m.at and m.at != gc.key
        )
        lines = [
            f"Quarters: {number_words(manned)} gun crew{'s' if manned != 1 else ''} manned, "
            f"the trimmers {len(self.divisions.get(TRIMMERS, []))}, the helm "
            f"{len(self.divisions.get(HELM, []))}, the powder "
            f"{len(self.divisions.get(POWDER, []))}"
            + (f", the marines {len(marines)}" if marines else "")
            + "."
        ]
        if short:
            names = self._guns_words([gc.key for gc in short])
            lines.append(f"Not hands enough for every gun: {names} stand unmanned.")
        if at_work:
            lines.append(
                f"{number_words(at_work).capitalize()} of the guns' hands at the work in hand, "
                "to go to their guns as it is done."
            )
        return lines

    def describe(self) -> list[str]:
        """The quarter bill for the muster and the reading: each crew and its state."""
        if not self.at_quarters:
            return ["Not at quarters: the company is under the watch bill."]
        lines = list(self._beat_lines())
        for gc in self.crews.values():
            guns = [self.ship.guns[g] for g in gc.guns if g in self.ship.guns]
            name = guns[0].name if len(guns) == 1 else f"Nos. {guns[0].number} guns"
            at = len(gc.hands)
            state = "manned" if at >= gc.wanted else f"{at} of {gc.wanted}" if at else "unmanned"
            lines.append(f"{_cap(name)}: {state}.")
        return lines


def quarters_of(ship: Any) -> Quarters | None:
    """The ship's quarters, made at the first call from her crew; None without one."""
    extra = getattr(ship, "extra", None)
    if extra is None:
        return None
    q = extra.get("quarters")
    if isinstance(q, Quarters):
        return q
    crew = extra.get("crew")
    if not isinstance(crew, Crew):
        return None
    q = Quarters(ship, crew)
    extra["quarters"] = q
    return q


# -- helpers --------------------------------------------------------------------------


def _gun_order(g: Gun) -> tuple[int, float, str]:
    place = {"broadside": 0, "bow": 1, "stern": 1, "rail": 2}.get(g.place, 3)
    return (place, -g.x_m, g.id)


def _preferred_stations(gc: GunCrew, length_m: float, has_marines: bool) -> list[Station]:
    """The stations a gun crew is drawn from, in order (Luce 1884 ch. XX: the forecastlemen
    forward, the waisters amidships, the afterguard aft; the marines at the quarterdeck
    carronades with the afterguard; a chaser's crew the forecastlemen's; a swivel's whoever
    is spare)."""
    key = gc.key[len(GUN_PREFIX) :]
    # the topmen are quartered at the guns too, told off from them for the sails (Luce 1884
    # ch. XX): after the deck stations, in the order of the masts
    tops = [Station.FORE_TOP, Station.MAIN_TOP, Station.MIZZEN_TOP]
    fc, w, ag, m = Station.FORECASTLE, Station.WAISTERS, Station.AFTERGUARD, Station.MARINES
    if not key.isdigit():
        if "swivel" in key:
            return [w, ag, fc, m, *tops]
        if "stern" in key:
            return [ag, w, m, fc, *tops]
        return [fc, w, ag, m, *tops]
    forward, aft = length_m * FORWARD_SHARE, -length_m * FORWARD_SHARE
    if gc.kind == "carronade" and has_marines:
        return [m, ag, w, fc, *tops]
    if gc.x_m >= forward:
        return [fc, w, ag, m, *tops]
    if gc.x_m <= aft:
        return [ag, w, m, fc, *tops]
    return [w, fc, ag, m, *tops]


def _rob_order(gc: GunCrew, bearing_fwd: bool | None) -> tuple[int, float, str]:
    key = gc.key[len(GUN_PREFIX) :]
    if "swivel" in key:
        return (0, 0.0, key)
    if not key.isdigit():
        return (1, 0.0, key)
    # the end that bears least first: the after guns when the enemy is forward, else the
    # forward guns
    x = gc.x_m if bearing_fwd in (True, None) else -gc.x_m
    return (2, x, key)


def _share_words(share: float) -> str:
    if abs(share - 0.5) < 1e-9:
        return "half"
    if abs(share - 1.0 / 3.0) < 1e-6:
        return "a third"
    return f"{share:.0%}"


def _runs(numbers: list[int]) -> list[str]:
    out: list[str] = []
    start = prev = numbers[0]
    for n in numbers[1:] + [None]:
        if n is not None and n == prev + 1:
            prev = n
            continue
        out.append(f"{start}" if start == prev else f"{start} to {prev}")
        if n is not None:
            start = prev = n
    return out


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]
