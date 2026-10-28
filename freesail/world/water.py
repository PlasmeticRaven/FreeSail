"""Water in the ship, the well, the pumps and foundering (spec M7 §13; package 73; the
design in `docs/design/Design-WaterAndHealth.md`).

**One quantity.** The water in the ship is so many tons, kept by this keeper on every
World (`world.water`, the player's and each crewed one), ticked once a tick after the
ship's step. Its sources are each a state the game already has (rule 1):

- **a shot hole** below the water (`combat.hits.Damage.holes`, 70's dict with its side, its
  place along the hull, its height against the upright waterline and its diameter), which
  flows by the orifice law `Q = C_d A sqrt(2 g h)` from its depth under the heeled waterline
  less the water inside above it, until the carpenter plugs it (`plugged`);
- **the ground** (`world.ground`'s `extra["leak_m_per_h"]`, the hotfix's figures kept to
  the number and converted by the bilge's floor to tons), running while she lies on it,
  and afloat again at its rate on rock (her planks stove) and at a third on a soft bottom
  (the seams she strained close as she stops working on the bank: judgement), until the
  carpenter caulks it (`stop the leak`) or the director's cause;
- **the seams working in a seaway**: a small rate by her size and her roll, nought under a
  gentle roll, so that a sound ship in ordinary weather makes no water worth a line; the
  watch pumps her dry at the change of the watch unasked and silently (the period's "sucked
  the pumps dry at eight bells" is a routine, not an event) while no leak but the seams runs;
- **the sea shipped** over open hatches in a heavy sea, until they are battened down;
- **a seam started** by the director's cause (`aboard: a seam found working`), caulked by
  the carpenter in his hours.

The well's depth is the volume over the bilge's floor (`WELL_FLOOR_COEFF · L · B`), written
to `Hull.water_in_well_m` each tick, so `sound the well` and `the well` read as the hotfix
left them; the free surface takes from the metacentric height by the naval architect's
formula (`Hull.free_surface_m`, read by the heel's balance and the roll in place of the
file's figure, nought with a dry well). **The pumps** are a standing work like the guns'
cycle (`Pumps`): the ship file's pumps through the generator with Falconer's figures (the
chain pump of Cole and Bentinck "wrought by four men, discharged a ton of water in 43
seconds and a half": Falconer 1780, PUMP; the common brake pump a fraction of it), manned by
`man the pumps` from the hands' pool through `hands.request` (so the braces and the pumps
compete for the same men, and the routine's fatigue has them at work), spelled every glass
by the keeper or by the word, gaining or losing by the rates, sucking when the well is dry.
**She founders** when the water reaches `FOUNDER_SHARE` of her displacement (her reserve of
buoyancy gone), the log saying when the pumps lost her; the integrator holds her as the
ground does; a crewed ship goes down and is seen to.

Every figure is judgement with its source named here and in the tuning notes (rule 6).
Nothing here draws randomness.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.crew import bill
from freesail.crew import hands as H
from freesail.crew.model import Rating, number_words

__all__ = [
    "FOUNDER_SHARE",
    "PUMPS_ID",
    "SPELL_S",
    "WELL_FLOOR_COEFF",
    "Leak",
    "Pumps",
    "Water",
    "WaterState",
    "orifice_t_per_h",
    "water_of",
]

PUMPS_ID = "pumps"  # the instance id the hands at the pumps carry (`Sailor.at`)

# -- the well -------------------------------------------------------------------------------
# The bilge's floor: the depth the carpenter's rod finds is the volume over this share of
# the length by the beam (judgement: a hull of block coefficient about a half, narrower at
# the bilge; the frigate's metre of water in the well is 220 tons, the cutter's 40).
WELL_FLOOR_COEFF = 0.45
FOOT_M = 0.3048
INCH_M = 0.0254
SEAWATER_T_PER_M3 = 1.025

# -- the shot hole --------------------------------------------------------------------------
# The orifice's coefficient of discharge (the sharp-edged orifice of any hydraulics text).
ORIFICE_CD = 0.6
G = 9.81

# -- the seams ------------------------------------------------------------------------------
# Tons an hour for a hundred tons of displacement at a roll a scale over the free roll:
# judgement, calibrated so that the frigate in a moderate sea (a roll of nine degrees)
# makes a tenth of a ton an hour, a few inches a day, and in a gale's twenty degrees some
# three tons an hour, two inches a watch: the "sucked the pumps dry at eight bells" of the
# period's logs, never a line.
SEAMS_T_PER_H_PER_100T = 0.02
SEAMS_ROLL_FREE_DEG = 6.0
SEAMS_ROLL_SCALE_DEG = 4.0
SEAMS_ROLL_CAP_DEG = 25.0
# A ship that has taken the ground works her seams this much more for a day after
# (judgement: her fastenings started).
SEAMS_STRAINED_FACTOR = 3.0
SEAMS_STRAINED_S = 24 * 3600
# The ground's leak afloat again: on rock as it was (her planks stove), on a soft bottom
# this share (judgement).
GROUND_AFLOAT_SOFT_SHARE = 1.0 / 3.0

# -- the sea shipped ------------------------------------------------------------------------
# Over this combined height the sea comes over the hatches of a ship not battened down
# (the sea's "heavy" words begin near it), at so many tons an hour a metre of excess for a
# cutter's length, scaled by her length (judgement).
SEA_SHIPS_OVER_M = 3.0
SEA_T_PER_H_PER_M = 2.0
SEA_LENGTH_REFERENCE_M = 20.0

# -- the routine's pumping ------------------------------------------------------------------
# At the change of the watch the watch pumps her dry unasked while the well shows under
# this and nothing but the seams runs (half a foot; judgement).
ROUTINE_PUMP_UNDER_M = 0.15

# -- the pumps ------------------------------------------------------------------------------
SPELL_S = 1800  # the men relieved every glass (Falconer 1780, PUMP: "at short intervals")
SUCK_M = 0.05  # under two inches the pumps suck and are stood down
# The pumps lose at a short crew more than in proportion, as the guns do (the brake wants
# its numbers; judgement, the square).
PUMP_NUMBERS_POWER = 1.5

# -- foundering -----------------------------------------------------------------------------
# She founders at this share of her displacement in water (judgement: half her own weight
# of water in her and her reserve of buoyancy is gone); the settling line at three fifths
# of it.
FOUNDER_SHARE = 0.5
SETTLING_SHARE = 0.6

# -- the free surface -----------------------------------------------------------------------
# The free surface's second moment `l b^3 / 12` over the volume of displacement (Rawson and
# Tupper, Basic Ship Theory, the free surface effect): the flooded length three fifths of
# the waterline, the surface's breadth growing from a trough to the beam as the water rises
# over the bilge (judgement), the metacentric height floored at the motion's own floor.
FREE_SURFACE_LENGTH_SHARE = 0.6
FREE_SURFACE_BREADTH_FLOOR = 0.15
FREE_SURFACE_DEPTH_OF_DRAUGHT = 0.5
GM_FLOOR_M = 0.05
# Under this depth in the well the water lies in the limbers and the trough of the bilge
# and the free surface is nothing (four inches; judgement): the seams' water in a seaway,
# pumped at the change of the watch, never reaches the heel of a recorded passage.
FREE_SURFACE_FROM_M = 0.1


def orifice_t_per_h(diameter_m: float, head_m: float) -> float:
    """The orifice law: tons an hour through a round hole under so much head."""
    if head_m <= 0.0 or diameter_m <= 0.0:
        return 0.0
    area = math.pi * (diameter_m / 2.0) ** 2
    q = ORIFICE_CD * area * math.sqrt(2.0 * G * head_m)  # cubic metres a second
    return q * 3600.0 * SEAWATER_T_PER_M3


@dataclass
class Leak:
    """One source of water this tick: its kind ('shot hole', 'the ground', 'the seams',
    'the sea', 'a seam'), its words, its rate now in tons an hour, and where it is."""

    kind: str
    words: str
    t_per_h: float
    where: str = ""
    hole: Any = None  # the shot hole's dict, for the carpenter's plug


@dataclass
class WaterState:
    """The water's state, kept in `ship.extra["well"]` (`water_of`; the tide's stream has
    `extra["water"]`, which is why the key is the well's)."""

    tons: float = 0.0
    hatches_battened: bool = False
    fothered: bool = False
    # seams started by the director's cause or the strain, each {words, t_per_h, since}
    seams: list[dict[str, Any]] = field(default_factory=list)
    # the ground's leak afloat: the rate in metres of the well an hour and the bottom
    ground_rate_m_per_h: float = 0.0
    ground_rock: bool = False
    strained_until: int | None = None
    # the lines' memory
    feet_said: int = 0
    gaining: bool | None = None  # the sign of the balance under manned pumps, last said
    settling_said: bool = False
    foundered: int | None = None
    pumps_lost_tick: int | None = None
    last_gain_t_per_h: float = 0.0
    last_pumped_t_per_h: float = 0.0
    routine_watch: str | None = None
    routine_pumped_tick: int | None = None
    # the pumps
    pumps_manned: bool = False
    pumps_since: int | None = None
    pumps_spelled: int | None = None
    pumps_hands: list[str] = field(default_factory=list)
    pumps_said_sucked: bool | str = False  # False, 'kept' (a leak still runs) or True


def water_of(ship: Any) -> WaterState | None:
    extra = getattr(ship, "extra", None)
    if extra is None:
        return None
    st = extra.get("well")
    if not isinstance(st, WaterState):
        st = WaterState()
        extra["well"] = st
    return st


class Water:
    """The World's water keeper: the sources summed, the pumps' work taken off, the well
    written, the lines said, the foundering."""

    def __init__(self, world: Any) -> None:
        self.world = world
        self.pumps = Pumps(self)

    # -- the ship's figures -------------------------------------------------------------

    @property
    def ship(self) -> Any:
        return self.world.ship

    @property
    def state(self) -> WaterState | None:
        return water_of(self.ship)

    def _hull(self) -> Any:
        return getattr(self.ship, "hull", None)

    def floor_m2(self) -> float:
        hull = self._hull()
        if hull is None:
            return 1.0
        return max(
            1.0, WELL_FLOOR_COEFF * float(hull.spec.length_waterline_m) * float(hull.spec.beam_m)
        )

    def displacement_t(self) -> float:
        hull = self._hull()
        return float(hull.spec.displacement_kg) / 1000.0 if hull is not None else 100.0

    def depth_m(self) -> float:
        st = self.state
        return float(st.tons) / self.floor_m2() if st is not None else 0.0

    def founder_t(self) -> float:
        return FOUNDER_SHARE * self.displacement_t()

    # -- the sources ----------------------------------------------------------------------

    def leaks(self) -> list[Leak]:
        """Every source running this tick with its rate in tons an hour."""
        ship = self.ship
        st = self.state
        hull = self._hull()
        if st is None or hull is None:
            return []
        out: list[Leak] = []
        extra = ship.extra
        depth = self.depth_m()
        beam = float(hull.spec.beam_m)
        draught = float(hull.spec.draught_m)
        heel = float(getattr(getattr(ship, "dyn", None), "heel", 0.0) or 0.0)
        # the shot holes (package 70's state), by the orifice law
        keeper = extra.get("damage")
        for hole in getattr(keeper, "holes", []) or []:
            if hole.get("plugged") is not None:
                continue
            z = float(hole.get("z_m", 1.0))
            sign = 1.0 if hole.get("side") == "starboard" else -1.0
            under = -z + sign * (beam / 2.0) * math.sin(heel)
            if under <= 0.0:
                continue
            inside = max(0.0, depth - (draught + z))
            head = max(0.0, under - inside)
            rate = orifice_t_per_h(float(hole.get("diameter_m", 0.1)), head)
            if rate <= 0.0:
                continue
            if st.fothered:
                rate *= FOTHER_SHARE
            out.append(Leak("shot hole", _hole_words(ship, hole), rate, hole.get("side", ""), hole))
        # the ground's leak: aground at the hotfix's rate, afloat at the bottom's share
        rate_m = float(extra.get("leak_m_per_h", 0.0) or 0.0)
        if rate_m > 0.0:
            if extra.get("aground"):
                st.ground_rate_m_per_h = rate_m
                st.ground_rock = (
                    bool(extra["aground"].get("rock"))
                    if isinstance(extra["aground"], dict)
                    else st.ground_rock
                )
                share = 1.0
                words = (
                    "her planks stove on the rock"
                    if st.ground_rock
                    else "her seams strained on the ground"
                )
            else:
                share = 1.0 if st.ground_rock else GROUND_AFLOAT_SOFT_SHARE
                words = (
                    "the planks she stove on the rock"
                    if st.ground_rock
                    else "the seams she strained on the ground"
                )
            rate = rate_m * share * self.floor_m2() * SEAWATER_T_PER_M3
            if st.fothered:
                rate *= FOTHER_SHARE
            if rate > 0.0:
                out.append(Leak("the ground", words, rate))
        # the seams started by a cause
        for seam in st.seams:
            if seam.get("stopped") is None and float(seam.get("t_per_h", 0.0)) > 0.0:
                rate = float(seam["t_per_h"]) * (FOTHER_SHARE if st.fothered else 1.0)
                out.append(Leak("a seam", str(seam.get("words") or "a seam working"), rate))
        # the seams working in a seaway
        roll = self._roll_deg()
        if roll > SEAMS_ROLL_FREE_DEG:
            r = min(roll, SEAMS_ROLL_CAP_DEG)
            f = ((r - SEAMS_ROLL_FREE_DEG) / SEAMS_ROLL_SCALE_DEG) ** 2
            rate = SEAMS_T_PER_H_PER_100T * (self.displacement_t() / 100.0) * f
            tick = int(self.world.clock.tick)
            if st.strained_until is not None and tick < st.strained_until:
                rate *= SEAMS_STRAINED_FACTOR
            if rate > 0.0:
                out.append(Leak("the seams", "her seams working in the sea", rate))
        # the sea shipped over the hatches
        if not st.hatches_battened:
            height = self._sea_height_m()
            if height > SEA_SHIPS_OVER_M:
                scale = float(hull.spec.length_waterline_m) / SEA_LENGTH_REFERENCE_M
                rate = SEA_T_PER_H_PER_M * (height - SEA_SHIPS_OVER_M) * scale
                out.append(Leak("the sea", "the seas she ships over the open hatches", rate))
        return out

    def _roll_deg(self) -> float:
        motion = getattr(self.world, "motion", None)
        return float(getattr(motion, "roll_deg", 0.0) or 0.0) if motion is not None else 0.0

    def _sea_height_m(self) -> float:
        """The sea's height, read once a minute (the reading is the sea model's work, and
        the sea she ships does not change by the second; the far convoy's pace, truth 7-159,
        felt the reading every tick)."""
        sea = getattr(self.world, "sea", None)
        if sea is None:
            return 0.0
        minute = int(self.world.clock.tick) // 60
        cached = getattr(self, "_sea_cache", None)
        if cached is not None and cached[0] == minute:
            return cached[1]
        try:
            height = float(sea.reading().height_m)
        except Exception:  # noqa: BLE001  (a sea that cannot be read ships nothing)
            height = 0.0
        self._sea_cache = (minute, height)
        return height

    def gain_t_per_h(self) -> float:
        return sum(lk.t_per_h for lk in self.leaks())

    # -- the tick -------------------------------------------------------------------------

    def tick(self) -> None:
        world = self.world
        ship = self.ship
        st = self.state
        hull = self._hull()
        if st is None or hull is None:
            return
        tick = int(world.clock.tick)
        if ship.extra.get("aground") and st.strained_until is None:
            st.strained_until = tick + SEAMS_STRAINED_S
        elif (
            not ship.extra.get("aground")
            and st.strained_until is not None
            and tick >= st.strained_until
        ):
            st.strained_until = None
        if st.foundered is not None:
            self._hold_foundered()
            return
        if st.fothered and (knots_of(ship) > FOTHER_HOLDS_UNDER_KN or ship.extra.get("aground")):
            # the fothered sail goes: torn off by her way through the water, or by the ground
            st.fothered = False
            world.record(
                Severity.NOTABLE,
                "leak.fother_gone",
                "The fothered sail has gone from under her, and the leak runs as it did.",
                data={"tick": tick},
            )
        if self._quiet(st, ship):
            # a dry ship with no source running: nothing to sum, nothing to say (the far
            # convoy's pace, truth 7-159, felt the keeper's full tick at every second)
            st.last_gain_t_per_h = 0.0
            st.last_pumped_t_per_h = 0.0
            hull.water_in_well_m = 0.0
            self._free_surface(hull, 0.0)  # the well just pumped out gives her stiffness back
            return
        gain = self.gain_t_per_h()
        st.last_gain_t_per_h = gain
        pumped = self.pumps.tick(tick)
        st.last_pumped_t_per_h = pumped
        before = st.tons
        st.tons = max(0.0, st.tons + (gain - pumped) / 3600.0)
        self._routine_pumping(st, gain)
        depth = self.depth_m()
        hull.water_in_well_m = depth
        self._free_surface(hull, depth)
        self._lines(st, gain, pumped, before, depth, tick)

    def _quiet(self, st: WaterState, ship: Any) -> bool:
        """Dry, nothing manned, and no source that could run: no holes unplugged, no
        ground's leak, no started seam, the roll under the seams' free angle, and the sea
        under the hatches' height (or the hatches battened)."""
        if st.tons > 0.0 or st.pumps_manned or st.fothered:
            return False
        extra = ship.extra
        if float(extra.get("leak_m_per_h", 0.0) or 0.0) > 0.0:
            return False
        keeper = extra.get("damage")
        if any(h.get("plugged") is None for h in (getattr(keeper, "holes", []) or [])):
            return False
        if any(seam.get("stopped") is None for seam in st.seams):
            return False
        if self._roll_deg() > SEAMS_ROLL_FREE_DEG:
            return False
        if not st.hatches_battened and self._sea_height_m() > SEA_SHIPS_OVER_M:
            return False
        return True

    def _routine_pumping(self, st: WaterState, gain: float) -> None:
        """Every glass the watch pumps her dry unasked while the well is shallow and nothing
        but the weather's water runs (her seams working, the sea she ships): no line and no
        hands (the routine's minutes at the brakes, "the pumps going every half hour" of a
        ship in a blow). A leak of the hull's, the ground's or a started seam's is the
        carpenter's and the order's."""
        clock = self.world.clock
        tick = int(clock.tick)
        if tick % SPELL_S:
            return
        if st.tons <= 0.0 or st.pumps_manned:
            return
        if self.depth_m() >= ROUTINE_PUMP_UNDER_M:
            return
        if any(lk.kind not in ("the seams", "the sea") for lk in self.leaks()):
            return
        if not _pump_specs(self.ship):
            return
        st.tons = 0.0
        st.routine_pumped_tick = int(clock.tick)

    def _free_surface(self, hull: Any, depth: float) -> None:
        if depth < FREE_SURFACE_FROM_M:
            fs = 0.0
        else:
            spec = hull.spec
            length = FREE_SURFACE_LENGTH_SHARE * float(spec.length_waterline_m)
            share = min(
                1.0,
                FREE_SURFACE_BREADTH_FLOOR
                + depth / max(FREE_SURFACE_DEPTH_OF_DRAUGHT * float(spec.draught_m), 0.1),
            )
            b = share * float(spec.beam_m)
            volume = float(spec.displacement_kg) / 1025.0
            fs = length * b**3 / 12.0 / max(volume, 1.0)
            fs = min(fs, float(spec.gm_m) - GM_FLOOR_M)
            fs = max(0.0, fs)
        was = float(getattr(hull, "free_surface_m", 0.0) or 0.0)
        if abs(fs - was) < 0.005 and (fs > 0.0 or was == 0.0):
            return
        hull.free_surface_m = fs
        motion = getattr(self.world, "motion", None)
        if motion is not None:
            from freesail.physics.motion import Particulars

            p = motion.particulars
            motion.particulars = Particulars(beam_m=p.beam_m, gm_m=hull.gm_m, length_m=p.length_m)
            motion.roll_period_s = motion.particulars.roll_period_s

    def _lines(
        self, st: WaterState, gain: float, pumped: float, before: float, depth: float, tick: int
    ) -> None:
        world = self.world
        feet = int(depth / FOOT_M)
        if feet > st.feet_said:
            st.feet_said = feet
            n = "a foot" if feet == 1 else f"{feet} feet"
            trend = "and gaining" if gain > pumped else "and holding"
            world.record(
                Severity.NOTABLE if feet < 3 else Severity.URGENT,
                "well.rising",
                f"The carpenter reports {n} of water in the well, {trend}.",
                data={"well_m": round(depth, 2), "feet": feet, "tons": round(st.tons, 1)},
            )
        elif feet < st.feet_said and st.tons < before:
            st.feet_said = feet
        if st.pumps_manned and gain > 0.0:
            gaining = pumped > gain
            if st.gaining is None or gaining != st.gaining:
                st.gaining = gaining
                if gaining:
                    world.record(
                        Severity.NOTABLE,
                        "pumps.gaining",
                        f"The pumps are gaining on the leak: {pumped:.0f} tons an hour "
                        f"against {gain:.0f} coming in.",
                        data={"pumped_t_per_h": round(pumped, 1), "gain_t_per_h": round(gain, 1)},
                    )
                else:
                    st.pumps_lost_tick = tick
                    world.record(
                        Severity.URGENT,
                        "pumps.losing",
                        f"The pumps are losing: {gain:.0f} tons an hour coming in against "
                        f"{pumped:.0f} pumped; the water gains on them.",
                        data={"pumped_t_per_h": round(pumped, 1), "gain_t_per_h": round(gain, 1)},
                    )
        elif (
            not st.pumps_manned
            and gain > 0.0
            and st.gaining is not False
            and st.pumps_lost_tick is None
        ):
            if depth >= FOOT_M:
                st.pumps_lost_tick = tick  # the water gains with nobody at the pumps
        founder = self.founder_t()
        if st.tons >= SETTLING_SHARE * founder and not st.settling_said:
            st.settling_said = True
            world.record(
                Severity.URGENT,
                "ship.settling",
                "She is settling: the water is over the orlop and she answers her helm "
                "like a log; the pumps cannot hold her unless the leak is stopped.",
                data={"tons": round(st.tons, 1), "founder_t": round(founder, 1)},
            )
        if st.tons >= founder:
            self._founder(st, tick)

    # -- foundering -----------------------------------------------------------------------

    def _founder(self, st: WaterState, tick: int) -> None:
        world = self.world
        ship = self.ship
        st.foundered = tick
        ship.extra["foundered"] = tick
        lost = st.pumps_lost_tick
        when = ""
        if lost is not None:
            from datetime import timedelta

            at = world.clock.start + timedelta(seconds=int(lost))
            when = f"; the pumps lost her at {at:%H:%M}"
        aground = bool(ship.extra.get("aground"))
        if aground:
            text = (
                "She has bilged on the ground and filled: the water is up to the lower deck "
                f"and she is lost where she lies{when}. The hands take to the boats."
            )
        else:
            text = (
                f"She is going down: the water has beaten the pumps{when}. The hands take to "
                "the boats; the ship is lost."
            )
        world.record(
            Severity.URGENT,
            "ship.foundered",
            text,
            data={"tons": round(st.tons, 1), "pumps_lost_tick": lost, "aground": aground},
        )
        self.pumps.stand_down(tick, say=False)
        from freesail.ship.parts import SailState

        for sail in getattr(ship, "sails", {}).values():
            if not sail.wrecked and sail.state not in (SailState.UNBENT, SailState.BLOWN_OUT):
                sail.state = SailState.FURLED
        battery = ship.extra.get("battery")
        if battery is not None:
            from freesail.combat.guns import FireMode

            battery.mode = FireMode.HOLD
            battery.word = None
        quarters = ship.extra.get("quarters")
        if quarters is not None and getattr(quarters, "at_quarters", False):
            quarters.stand_down()
        world.ship_lost = True
        vessel = getattr(world, "vessel", None)
        parent = getattr(world, "parent", None)
        if vessel is not None and parent is not None:
            vessel.sunk = tick
            vessel.struck = False
            vessel.done = True
            words = ""
            lookout = getattr(parent, "lookout", None)
            if lookout is not None:
                try:
                    words = lookout.sail_name(f"sail:{vessel.id}", "")
                except Exception:  # noqa: BLE001
                    words = ""
            words = words or vessel.name
            parent.record(
                Severity.URGENT,
                "action.enemy_sunk",
                f"{words[:1].upper()}{words[1:]} has gone down; her people are in the water "
                "and her boats.",
                data={"id": vessel.id},
            )

    def _hold_foundered(self) -> None:
        ship = self.ship
        dyn = getattr(ship, "dyn", None)
        if dyn is not None:
            dyn.u = dyn.v = dyn.r = 0.0
            dyn.speed = 0.0

    # -- the director's causes and the carpenter's work --------------------------------

    def pump_out(self) -> float:
        """The well emptied by a cause (`aboard: the well pumped out`): the tons taken."""
        st = self.state
        if st is None:
            return 0.0
        was = st.tons
        st.tons = 0.0
        st.feet_said = 0
        st.settling_said = False
        hull = self._hull()
        if hull is not None:
            hull.water_in_well_m = 0.0
        return was

    def start_seam(self, t_per_h: float, words: str) -> dict[str, Any]:
        st = self.state
        seam = {
            "words": words,
            "t_per_h": float(t_per_h),
            "since": int(self.world.clock.tick),
            "stopped": None,
        }
        if st is not None:
            st.seams.append(seam)
        return seam

    def stop_leaks(self, tick: int) -> list[str]:
        """The ground's leak and every started seam stopped (the carpenter's caulking or the
        director's cause). Returns the words of what was stopped."""
        st = self.state
        stopped: list[str] = []
        extra = self.ship.extra
        if float(extra.get("leak_m_per_h", 0.0) or 0.0) > 0.0:
            extra["leak_m_per_h"] = 0.0
            stopped.append(
                "the seams she strained on the ground"
                if st is None or not st.ground_rock
                else "the planks stove on the rock"
            )
        if st is not None:
            for seam in st.seams:
                if seam.get("stopped") is None:
                    seam["stopped"] = tick
                    stopped.append(str(seam.get("words") or "the seam"))
            st.gaining = None
        return stopped

    def describe(self) -> dict[str, Any]:
        """The well, the leaks and the pumps for the readings."""
        st = self.state
        leaks = self.leaks()
        gain = sum(lk.t_per_h for lk in leaks)
        pumped = st.last_pumped_t_per_h if st is not None else 0.0
        return {
            "tons": round(st.tons, 1) if st is not None else 0.0,
            "well_m": round(self.depth_m(), 3),
            "gain_t_per_h": round(gain, 1),
            "pumped_t_per_h": round(pumped, 1),
            "leaks": [
                {"kind": lk.kind, "words": lk.words, "t_per_h": round(lk.t_per_h, 1)}
                for lk in leaks
            ],
            "pumps": self.pumps.describe(),
            "hatches": "battened down" if st is not None and st.hatches_battened else "open",
            "fothered": bool(st is not None and st.fothered),
            "foundered": st.foundered if st is not None else None,
            "routine_pumped_tick": st.routine_pumped_tick if st is not None else None,
        }


# A fothered sail over the leak lets through this share (Falconer 1780, FOTHERING; judgement),
# and goes when she makes more than this through the water (judgement).
FOTHER_SHARE = 0.3
FOTHER_HOLDS_UNDER_KN = 6.0


def _hole_words(ship: Any, hole: dict[str, Any]) -> str:
    z = float(hole.get("z_m", 0.0))
    where = "between wind and water" if z <= 0.0 else "through the side"
    length = float(getattr(getattr(ship, "hull", None), "length", 40.0) or 40.0)
    x = float(hole.get("x_m", 0.0))
    along = "forward" if x > length / 6.0 else "aft" if x < -length / 6.0 else "amidships"
    return f"a shot hole {where} to {hole.get('side', 'starboard')}, {along}"


# -- the pumps -------------------------------------------------------------------------------


def _pump_specs(ship: Any) -> list[Any]:
    spec = getattr(ship, "spec", None)
    return list(getattr(spec, "pumps", []) or [])


class Pumps:
    """The ship's pumps as a standing work: manned from the hands' pool, each pump lifting
    its rated tons an hour by the men at it, spelled every glass."""

    def __init__(self, water: Water) -> None:
        self.water = water

    @property
    def ship(self) -> Any:
        return self.water.ship

    @property
    def state(self) -> WaterState | None:
        return self.water.state

    def specs(self) -> list[Any]:
        return _pump_specs(self.ship)

    def wanted(self) -> int:
        return sum(int(p.hands) for p in self.specs())

    def hands(self) -> list[Any]:
        crew = self.ship.extra.get("crew")
        if crew is None:
            return []
        return [s for s in crew.sailors if s.at == PUMPS_ID and s.fit]

    @property
    def manned(self) -> bool:
        st = self.state
        return bool(st is not None and st.pumps_manned)

    # -- the orders ---------------------------------------------------------------------

    def man(self, tick: int) -> str:
        """`man the pumps`: the hands taken, the words for the log; refused in words when
        the ship has no pumps or no company, or nobody can be had."""
        from freesail.orders.errors import OrderError

        st = self.state
        specs = self.specs()
        if not specs:
            raise OrderError("She has no pumps in her file: nothing to man.")
        crew = self.ship.extra.get("crew")
        if crew is None:
            raise OrderError("There is no ship's company mustered in this ship to man the pumps.")
        if st is not None and st.foundered is not None:
            raise OrderError("She has foundered; the pumps are under water with the rest.")
        if self.manned:
            got = len(self.hands())
            return f"The pumps are manned already, {number_words(got)} hands at them."
        taken = self._take(crew, tick, avoid=())
        if not taken:
            raise OrderError(
                "Not a hand to be had for the pumps: every man on deck is at other work. "
                "'Belay' some of it, or wait for it to end."
            )
        st.pumps_manned = True
        st.pumps_since = tick
        st.pumps_spelled = tick
        st.pumps_hands = [s.id for s in taken]
        st.pumps_said_sucked = False
        st.gaining = None
        return (
            f"Man the pumps! {number_words(len(taken)).capitalize()} hands to the {self._names()}."
        )

    def spell(self, tick: int, by_order: bool = True) -> str:
        from freesail.orders.errors import OrderError

        st = self.state
        if not self.manned:
            if by_order:
                raise OrderError("The pumps are not manned; 'man the pumps' mans them.")
            return ""
        crew = self.ship.extra.get("crew")
        tired = self.hands()
        tired_ids = {s.id for s in tired}
        H.release(crew, PUMPS_ID)
        fresh = self._take(crew, tick, avoid=tired_ids)
        if not fresh:
            # nobody fresh: the same men go on
            fresh = self._take(crew, tick, avoid=())
        st.pumps_spelled = tick
        st.pumps_hands = [s.id for s in fresh]
        if not fresh:
            st.pumps_manned = False
            return (
                "The pumps' crews are spelled, and nobody can be had to relieve them: the "
                "pumps stand."
            )
        new = sum(1 for s in fresh if s.id not in tired_ids)
        if new == 0:
            return "Spell the pumps: no fresh hands to be had; the same men go on at the brakes."
        return f"Spell the pumps: {number_words(new)} fresh hands relieve the men at the brakes."

    def stand_down(self, tick: int, say: bool = True) -> str:
        st = self.state
        crew = self.ship.extra.get("crew")
        if crew is not None:
            H.release(crew, PUMPS_ID)
        if st is not None:
            st.pumps_manned = False
            st.pumps_hands = []
            st.gaining = None
        return "The pumps' crews stand down." if say else ""

    def _take(self, crew: Any, tick: int, avoid: set[str] | tuple) -> list[Any]:
        want = self.wanted()
        if want <= 0:
            return []
        clock = self.water.world.clock
        deck = bill.on_deck(crew, clock.ship_time)
        pool = [s for s in deck if s.id not in avoid]
        request = H.CrewRequest(
            hands=want,
            rating=Rating.ORDINARY,
            stations=("waisters", "afterguard", "forecastle", "idlers", "marines"),
        )
        got = H.request(crew, pool, PUMPS_ID, request, None, aloft=False)
        if got.outcome == H.TOO_FEW and avoid:
            got = H.request(crew, deck, PUMPS_ID, request, None, aloft=False)
        if got.outcome == H.TOO_FEW:
            # the pumps are worked by whoever can be had, down to one man at a brake
            idle = [s for s in pool if s.at is None and H.can_work(s, False)]
            for s in idle[:want]:
                s.at = PUMPS_ID
            return idle[:want]
        return list(got.hands)

    # -- the work -------------------------------------------------------------------------

    def tick(self, tick: int) -> float:
        """The tons an hour the pumps lift now; the men spelled every glass; stood down
        when the well sucks."""
        st = self.state
        if st is None or not st.pumps_manned:
            return 0.0
        water = self.water
        if st.pumps_spelled is not None and tick - st.pumps_spelled >= SPELL_S:
            words = self.spell(tick, by_order=False)
            if words:
                water.world.record(Severity.ROUTINE, "pumps.spelled", words, data={"tick": tick})
            if not st.pumps_manned:
                return 0.0
        men = self.hands()
        if not men:
            return 0.0
        rate = self.rate_t_per_h(men)
        if water.depth_m() < SUCK_M:
            # the pumps suck: the crews stand down unless a leak runs (then they are kept
            # at it by spells, pumping each glass, as the period kept a known leak); the
            # weather's water (her seams working, the sea she ships) keeps nobody at the
            # brakes: the well is pumped again when it shows (the doctrine's foot)
            leaks = [lk for lk in water.leaks() if lk.kind not in ("the seams", "the sea")]
            if not leaks:
                if st.pumps_said_sucked is not True:
                    st.pumps_said_sucked = True
                    water.world.record(
                        Severity.NOTABLE,
                        "pumps.sucked",
                        "The pumps suck: the well is dry, and the pumps' crews stand down.",
                        data={"tick": tick},
                    )
                water.state.tons = 0.0
                self.stand_down(tick, say=False)
                return 0.0
            if not st.pumps_said_sucked:
                st.pumps_said_sucked = "kept"  # said once; the stand-down line comes when it can
                water.world.record(
                    Severity.NOTABLE,
                    "pumps.sucked",
                    "The pumps suck; the crews are kept at them by spells while the leak runs.",
                    data={"tick": tick},
                )
        return rate

    def rate_t_per_h(self, men: list[Any]) -> float:
        """The pumps' lift with these men: each pump in the file's order given its hands
        from the men at the brakes, lifting its rated tons by the numbers (a short crew
        the less, more than in proportion), their rating, their fatigue and the roll."""
        total = 0.0
        pool = list(men)
        roll = self.water._roll_deg()
        seaway = H.seaway_factor(roll, False)
        for p in self.specs():
            n = int(p.hands)
            at = pool[:n]
            pool = pool[n:]
            if not at:
                break
            numbers = min(1.0, len(at) / max(n, 1)) ** PUMP_NUMBERS_POWER
            reference = H.rating_skill(H.DEFAULT_RATING, False)
            skill = sum(
                min(1.0, max(H.rating_skill(s.rating, False), H.SKILL_FLOOR) / reference)
                for s in at
            ) / len(at)
            mean_fatigue = sum(s.fatigue for s in at) / len(at)
            fatigue = 1.0 + H.FATIGUE_WEIGHT * max(0.0, mean_fatigue - H.FATIGUE_FRESH)
            total += float(p.tons_per_hour) * numbers * skill / (fatigue * seaway)
        return total

    def _names(self) -> str:
        specs = self.specs()
        kinds: dict[str, int] = {}
        for p in specs:
            kinds[p.kind] = kinds.get(p.kind, 0) + 1
        parts = [f"{number_words(n)} {k} pump{'s' if n != 1 else ''}" for k, n in kinds.items()]
        return " and ".join(parts) if parts else "pumps"

    def describe(self) -> dict[str, Any]:
        st = self.state
        specs = self.specs()
        men = self.hands()
        rate = self.rate_t_per_h(men) if men else 0.0
        if not specs:
            words = "no pumps"
        elif st is None or not st.pumps_manned:
            words = f"{self._names()}, not manned"
        else:
            words = (
                f"{self._names()} manned by {len(men)} of {self.wanted()} hands, "
                f"lifting {rate:.0f} tons an hour"
            )
        return {
            "words": words,
            "manned": bool(st is not None and st.pumps_manned),
            "hands": len(men),
            "wanted": self.wanted(),
            "rate_t_per_h": round(rate, 1),
            "kinds": [p.kind for p in specs],
            "rated_t_per_h": round(sum(float(p.tons_per_hour) for p in specs), 1),
        }


def well_feet_words(depth_m: float) -> str:
    from freesail.world.ground import well_words

    return well_words(depth_m)


def knots_of(ship: Any) -> float:
    dyn = getattr(ship, "dyn", None)
    return units.ms_to_knots(float(dyn.speed)) if dyn is not None else 0.0
