"""The damage control's evolutions (spec M7 §13, §14; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): the hatches battened, the shot holes plugged and
the leaks caulked, a sail fothered over the leak, a sprung spar fished, the preventers and
the chain slings before an action, the standing rigging set up again, a mast cut away, a
jury mast from the booms. Each is an evolution of M3's kind (a file in `data/evolutions/`
with its crew line, its timing and its source; the script where a step list cannot decide
what the work finds), competing for hands with the guns and the sails by the fighting
book's priority as every evolution does, and consuming a counted store (the carpenter's
shot plugs, the boatswain's cordage, the sail room, the booms). The effects are states the
game has (rule 1): a hole `plugged`, the ground's leak nought, a line's `preventer`, a
spar's condition, a lower mast standing again as a jury mast.

The times are judgement with their sources in the files; nothing here draws randomness.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions.scripts import PhasedScript
from freesail.ship import parts
from freesail.ship.graph import Ship
from freesail.ship.parts import Line, LineState, Spar

__all__ = [
    "REPAIR_SCRIPTS",
    "BattenDownScript",
    "CutAwayMastScript",
    "FishSparScript",
    "FotherSailScript",
    "JuryMastScript",
    "PlugShotHoleScript",
    "RigPreventersScript",
    "SetUpRiggingScript",
    "parted_running_lines",
    "parted_standing_lines",
    "shot_plugs",
    "sprung_spars",
]

# A spar is sprung under this condition (the carpenter's survey; judgement), and fished it
# stands at this at most (Luce 1884 ch. XXXI: a fished mast is eased of a press of sail).
SPRUNG_UNDER = 60.0
FISHED_CONDITION = 70.0
# A jury mast's rating against the mast's own, and its condition (judgement: Luce's jury
# rig carries the courses in a moderate breeze and no more).
JURY_RATING_SHARE = 0.4
JURY_CONDITION = 40.0
# A fothered sail goes when she makes more than this through the water (judgement).
FOTHER_HOLDS_UNDER_KN = 6.0
# The hole's place for its time: at or within this under the waterline it is reached from
# between decks with the water about the men; deeper from the hold.
NEAR_UNDER_M = 0.5
# The chain slings go on these yards' hoisting gear (Luce 1884 ch. XX: the lower yards
# slung with chains, the topsail yards' ties), and the preventer braces on the yards of
# the lower masts and the topmasts (the courses' and the topsails' yards; the light yards
# aloft went without: Luce 1884 ch. XX; judgement), each a single rope lighter than the
# brace with its pendants and blocks, this share of its fathoms (judgement).
SLING_SPAR_CLASSES = frozenset({"yard", "gaff"})
PREVENTER_MAST_CLASSES = frozenset({"mast", "topmast"})
PREVENTER_FATHOMS_SHARE = 0.5


def _world(ship: Ship) -> Any:
    from freesail.orders.prompt import world_of

    return world_of(ship)


def _tick(ship: Ship) -> int:
    world = _world(ship)
    return int(world.clock.tick) if world is not None else 0


def _water_state(ship: Ship) -> Any:
    from freesail.world.water import water_of

    return water_of(ship)


def _name(ship: Ship, part_id: str) -> str:
    from freesail.evolutions.runner import part_name

    return part_name(ship, part_id)


class ShotPlugs:
    """The carpenter's shot plugs, counted (`crew.stores.shot_plugs`); kept in
    `ship.extra["shot_plugs"]` as the cordage is, a function of the ship file and the
    orders given."""

    def __init__(self, count: int) -> None:
        self.count = int(count)

    def take(self) -> None:
        if self.count <= 0:
            raise ValueError("there is no shot plug left in the carpenter's store")
        self.count -= 1

    def describe(self) -> str:
        n = self.count
        return f"{n} shot plug{'s' if n != 1 else ''}" if n > 0 else "no shot plugs"


def shot_plugs(ship: Ship) -> ShotPlugs:
    store = ship.extra.get("shot_plugs")
    if not isinstance(store, ShotPlugs):
        stores = getattr(getattr(getattr(ship, "spec", None), "crew", None), "stores", None)
        n = int(getattr(stores, "shot_plugs", 0) or 0) if stores is not None else 0
        store = ShotPlugs(n)
        ship.extra["shot_plugs"] = store
    return store


# -- the hatches ------------------------------------------------------------------------


class BattenDownScript(PhasedScript):
    """Batten down the hatches, or take the battens off (`params.open`): one phase,
    `battens`; at its end the water's state has the hatches battened or open."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"battens": 600.0}

    def holds(self) -> set[str]:
        return {"hatches"}

    @property
    def opening(self) -> bool:
        return bool(self.params.get("open"))

    def check(self, words: dict[str, Any]) -> str | None:
        st = _water_state(self.ship)
        if st is None:
            return "she has no hatches to speak of"
        if self.opening and not st.hatches_battened:
            return "the hatches are open already"
        if not self.opening and st.hatches_battened:
            return "the hatches are battened down already"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["battens"])

    def end_phase(self, name: str) -> None:
        st = _water_state(self.ship)
        if st is not None:
            st.hatches_battened = not self.opening

    def words(self) -> dict[str, Any]:
        if self.opening:
            return {
                "begin": "Take the battens off the hatches!",
                "done": "The hatches are open again, the tarpaulins off and stowed.",
                "verb_word": "open",
            }
        return {
            "begin": "Batten down the hatches! The tarpaulins on and the battens nailed down.",
            "done": "The hatches are battened down: the tarpaulins on and the battens wedged; "
            "the sea she ships comes no further than the deck.",
            "verb_word": "batten down",
        }


# -- the shot holes and the leaks ---------------------------------------------------------


def _holes(ship: Ship) -> list[dict[str, Any]]:
    keeper = ship.extra.get("damage")
    return [h for h in (getattr(keeper, "holes", []) or []) if h.get("plugged") is None]


def _hole_rate(ship: Ship, hole: dict[str, Any]) -> float:
    water = getattr(_world(ship), "water", None)
    if water is None:
        return 0.0
    for lk in water.leaks():
        if lk.kind == "shot hole" and lk.hole is hole:
            return lk.t_per_h
    return 0.0


class PlugShotHoleScript(PhasedScript):
    """Plug the shot holes, the worst leak first, a phase a hole (`hole_<i>`), each its
    time by its place against the waterline and a plug from the carpenter's store; or,
    with no hole to plug, the ground's leak and the started seams caulked (`caulk`)."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"above": 600.0, "near": 1200.0, "deep": 2400.0, "caulk": 10800.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.queue: list[dict[str, Any]] = []
        self.plugged: list[dict[str, Any]] = []
        self.caulking = False
        self.stopped: list[str] = []

    def holds(self) -> set[str]:
        return {"the carpenter"}

    def _leaks_to_caulk(self) -> bool:
        water = getattr(_world(self.ship), "water", None)
        if water is None:
            return False
        return any(lk.kind in ("the ground", "a seam") for lk in water.leaks())

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        holes = _holes(ship)
        verb = str(self.params.get("verb") or "plug the shot holes")
        if holes:
            if shot_plugs(ship).count <= 0:
                return (
                    "the carpenter has no shot plug left; a hole wants a plug, oakum and a "
                    "piece of sheet lead, and his store is empty"
                )
            return None
        if self._leaks_to_caulk():
            return None
        if verb == "stop the leak":
            return (
                "she is making no water worth the carpenter's finding: no hole, no seam, no "
                "leak from the ground"
            )
        return "there is no shot hole in her side to plug"

    def begin(self, words: dict[str, Any]) -> None:
        ship = self.ship
        holes = _holes(ship)
        if holes:
            # the worst leak first: the holes under water by their rate, then the dry ones
            holes.sort(key=lambda h: (-_hole_rate(ship, h), float(h.get("z_m", 0.0))))
            self.queue = holes
            self.start_phases([f"hole_{i}" for i in range(len(holes))])
            return
        self.caulking = True
        self.start_phases(["caulk"])

    def _hole_of(self, name: str) -> dict[str, Any] | None:
        if not name.startswith("hole_"):
            return None
        i = int(name.rsplit("_", 1)[-1])
        return self.queue[i] if 0 <= i < len(self.queue) else None

    def phase_s(self, name: str) -> float:
        hole = self._hole_of(name)
        if hole is None:
            return super().phase_s(name)
        z = float(hole.get("z_m", 0.0))
        if z > 0.0:
            return super().phase_s("above")
        if z >= -NEAR_UNDER_M:
            return super().phase_s("near")
        return super().phase_s("deep")

    def start_phase(self, name: str) -> None:
        hole = self._hole_of(name)
        if hole is None:
            self.note("The carpenter and his crew go down to find the leak and caulk it.")
            return
        from freesail.world.water import _hole_words

        self.note(f"The carpenter's crew to {_hole_words(self.ship, hole)}.")

    def end_phase(self, name: str) -> None:
        ship = self.ship
        hole = self._hole_of(name)
        tick = _tick(ship)
        if hole is None:
            water = getattr(_world(ship), "water", None)
            if water is not None:
                self.stopped = water.stop_leaks(tick)
                world = _world(ship)
                if world is not None:
                    from freesail.core.events import Severity

                    world.record(
                        Severity.NOTABLE,
                        "leak.stopped",
                        "The carpenter reports the leak found and stopped: "
                        + (", ".join(self.stopped) if self.stopped else "the seams")
                        + " payed and caulked.",
                        data={"stopped": list(self.stopped)},
                    )
            return
        if hole.get("plugged") is not None:
            return  # plugged meanwhile
        store = shot_plugs(ship)
        if store.count <= 0:
            self.fail("the carpenter's shot plugs are all used")
            return
        store.take()
        hole["plugged"] = tick
        self.plugged.append(hole)
        from freesail.world.water import _hole_words

        self.note(
            f"Plugged {_hole_words(ship, hole)}: a plug driven in, oakum and a piece of sheet "
            f"lead over it ({store.describe()} left).",
            kind="hole.plugged",
        )

    def words(self) -> dict[str, Any]:
        verb = str(self.params.get("verb") or "plug the shot holes")
        if self.caulking:
            return {
                "begin": "Stop the leak! The carpenter and his crew below with oakum and tallow.",
                "done": "The leak stopped: "
                + (", ".join(self.stopped) if self.stopped else "the seams")
                + " caulked by the carpenter's crew.",
                "verb_word": verb,
            }
        n = len(self.plugged)
        done = (
            f"The carpenter reports the shot hole{'s' if n != 1 else ''} plugged, {n} of "
            f"{'them' if n != 1 else 'it'}; {shot_plugs(self.ship).describe()} left in his store."
        )
        return {
            "begin": "Plug the shot holes! The carpenter and his crew to the side with the plugs.",
            "done": done,
            "verb_word": verb,
        }


class FotherSailScript(PhasedScript):
    """A sail from the sail room thrummed and hauled under the bottom over the leak:
    phases `thrum` and `haul_under`; the sail used up; every leak below the water at
    `water.FOTHER_SHARE` while the sail holds."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"thrum": 3600.0, "haul_under": 1800.0}

    def holds(self) -> set[str]:
        return {"the sail room"}

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        st = _water_state(ship)
        if st is None:
            return "she has no bottom to fother"
        if st.fothered:
            return "a sail is fothered over the leak already"
        room = parts.sail_room(ship)
        if len(room) == 0:
            return "there is no spare sail in the sail room to fother with"
        water = getattr(_world(ship), "water", None)
        if water is None or not any(
            lk.kind in ("shot hole", "the ground", "a seam") for lk in water.leaks()
        ):
            return "she is making no water below to fother"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        self.start_phases(["thrum", "haul_under"])

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if name == "thrum":
            room = parts.sail_room(ship)
            spare = max(room.sails, key=lambda s: -s.condition) if room.sails else None
            if spare is None:
                self.fail("the sail room is empty")
                return
            what = room.names.get(spare.kind or "", "spare sail") if spare.kind else "made-up sail"
            room.take(spare)
            ship.extra["spare_sails"] = len(room)
            self.taken = what
            self.note(
                f"The spare {what} thrummed with oakum and rope-yarns, and the ropes bent to it."
            )
        elif name == "haul_under":
            st = _water_state(ship)
            if st is not None:
                st.fothered = True
            self.note(
                "The sail hauled under her bottom over the leak; the sea presses it into the "
                "place and the water comes in the slower.",
                kind="leak.fothered",
            )

    def words(self) -> dict[str, Any]:
        return {
            "done": f"The leak fothered with the spare {getattr(self, 'taken', 'sail')}: the "
            "water comes in at a third of what it did while the sail holds."
        }


# -- the spars ------------------------------------------------------------------------


def sprung_spars(ship: Ship) -> list[Spar]:
    return [
        s
        for s in ship.spars.values()
        if not s.wrecked and not s.sent_down and s.condition < SPRUNG_UNDER
    ]


class FishSparScript(PhasedScript):
    """A sprung spar fished and woolded: `fishes` on deck, `woold` aloft; the spar's
    condition raised to `FISHED_CONDITION` at most."""

    DEFAULTS = {"fishes": 900.0, "woold": 1800.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.spar: Spar | None = None

    def _subject(self, words: dict[str, Any] | None) -> Spar | None:
        sid = self.params.get("spar") or (words or {}).get("subject_id")
        if sid in self.ship.spars:
            return self.ship.spars[sid]
        return None

    def holds(self) -> set[str]:
        return {self.spar.id} if self.spar is not None else set()

    def check(self, words: dict[str, Any]) -> str | None:
        self.spar = self._subject(words)
        spar = self.spar
        if spar is None:
            return "name the spar to fish"
        name = _name(self.ship, spar.id)
        if spar.wrecked:
            return (
                f"the {name} is carried away, not sprung; clear the wreck and shift it for a spare"
            )
        if spar.sent_down:
            return f"the {name} is sent down on deck; it is fished when it stands"
        if spar.condition >= FISHED_CONDITION:
            return f"the {name} is sound enough; a fish would add nothing to it"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        if self.spar is None:
            self.spar = self._subject(words)
        self.start_phases(["fishes", "woold"])

    def end_phase(self, name: str) -> None:
        spar = self.spar
        if spar is None:
            return
        if name == "fishes":
            self.note(f"The fishes made and got up to the {_name(self.ship, spar.id)}.")
        elif name == "woold":
            spar.condition = max(spar.condition, FISHED_CONDITION)
            self.note(
                f"The {_name(self.ship, spar.id)} fished and woolded: it will serve, eased of a "
                "press of sail.",
                kind="spar.fished",
            )

    def words(self) -> dict[str, Any]:
        spar = self.spar
        name = _name(self.ship, spar.id) if spar is not None else "spar"
        return {
            "spar": name,
            "done": f"Fished the {name}: it stands at {FISHED_CONDITION:.0f} of a hundred, "
            "and will not bear a press of sail.",
        }


class CutAwayMastScript(PhasedScript):
    """A standing lower mast cut away: `axes`, then `clear`; the strain model's own
    wrecking (`how="cut away"`) and the wreck cleared over the side."""

    DEFAULTS = {"axes": 600.0, "clear": 300.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.spar: Spar | None = None

    def _subject(self, words: dict[str, Any] | None) -> Spar | None:
        sid = self.params.get("spar") or (words or {}).get("subject_id")
        if sid in self.ship.spars:
            return self.ship.spars[sid]
        return None

    def holds(self) -> set[str]:
        if self.spar is None:
            return set()
        return {self.spar.id} | {d.id for d in self.ship.dependents(self.spar)}

    def check(self, words: dict[str, Any]) -> str | None:
        self.spar = self._subject(words)
        spar = self.spar
        if spar is None:
            return "name the mast to cut away"
        name = _name(self.ship, spar.id)
        if spar.cls != "mast":
            return f"the {name} is no lower mast; a topmast is sent down, not cut away"
        if spar.wrecked:
            return f"the {name} is carried away already; clear the wreck"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        if self.spar is None:
            self.spar = self._subject(words)
        self.start_phases(["axes", "clear"])

    def end_phase(self, name: str) -> None:
        ship, spar = self.ship, self.spar
        if spar is None:
            return
        if name == "axes":
            from freesail.physics import strain as ST

            st = ST.strain_state(ship)
            ST._wreck_spar(ship, st, spar, 0.0, how="cut away")
        elif name == "clear":
            # the wreck over the side cut adrift, as clear_wreck's cut_adrift phase leaves it
            spar.sent_down = True
            for d in ship.dependents(spar):
                if isinstance(d, Spar):
                    d.sent_down = True
            self.note(f"The wreck of the {_name(ship, spar.id)} cut adrift from the chains.")

    def words(self) -> dict[str, Any]:
        spar = self.spar
        name = _name(self.ship, spar.id) if spar is not None else "mast"
        return {
            "spar": name,
            "done": f"The {name} is cut away and gone over the side with all it carried; the "
            "wreck cut adrift.",
        }


def _jury_candidates(ship: Ship) -> list[Spar]:
    """The lower masts carried away whose wreck is cleared, in the ship file's order."""
    return [
        s
        for s in ship.spars.values()
        if s.cls == "mast" and s.wrecked and s.sent_down and not getattr(s, "jury", False)
    ]


class JuryMastScript(PhasedScript):
    """A jury mast: a spare topmast from the booms stepped in the stump of a lower mast
    carried away and cleared; phases `get_up`, `step`, `stay`; the mast stands again at
    `JURY_RATING_SHARE` of its rating and `JURY_CONDITION`, the topmast and what stood on
    it still down, its own gear rove again."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"get_up": 3600.0, "step": 5400.0, "stay": 5400.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.spar: Spar | None = None

    def _find(self) -> Spar | None:
        words = " ".join(str(self.params.get("mast_words") or "").lower().split())
        candidates = _jury_candidates(self.ship)
        if not words:
            return candidates[0] if candidates else None
        from freesail.orders.resolve import resolve as resolve_noun_

        try:
            ids = resolve_noun_(self.ship, words, None, "rig a jury mast").ids
        except Exception:  # noqa: BLE001  (no such mast: refused below)
            return None
        for s in candidates:
            if s.id in ids:
                return s
        return None

    def holds(self) -> set[str]:
        return {self.spar.id} if self.spar is not None else {"the booms"}

    def check(self, words: dict[str, Any]) -> str | None:
        ship = self.ship
        self.spar = self._find()
        if self.spar is None:
            wrecked = [s for s in ship.spars.values() if s.cls == "mast" and s.wrecked]
            if not wrecked:
                return "no lower mast is carried away; there is nothing to rig a jury mast for"
            if any(not s.sent_down for s in wrecked):
                return "the wreck of the mast is not cleared yet; cut it away first"
            return "no lower mast carried away answers to that name"
        if parts.booms(ship).have("topmast") == 0:
            return "there is no spare topmast on the booms to step as a jury mast"
        return None

    def begin(self, words: dict[str, Any]) -> None:
        if self.spar is None:
            self.spar = self._find()
        self.start_phases(["get_up", "step", "stay"])

    def end_phase(self, name: str) -> None:
        ship, spar = self.ship, self.spar
        if spar is None:
            return
        if name == "get_up":
            store = parts.booms(ship)
            if store.have("topmast") == 0:
                self.fail("the spare topmast was taken for another spar meanwhile")
                return
            store.take("topmast")
            ship.extra["spare_spars"] = len(store)
            self.note("The spare topmast got out of the booms and its heel shaped for the stump.")
        elif name == "step":
            spar.wrecked = False
            spar.sent_down = False
            spar.jury = True
            spar.condition = JURY_CONDITION
            if not getattr(spar, "rating_whole_kn", 0.0):
                spar.rating_whole_kn = float(spar.rating_kn)
            spar.rating_kn = float(spar.rating_whole_kn) * JURY_RATING_SHARE
            spar.load_kn = 0.0
            self.note(f"The jury {_name(ship, spar.id)} swayed up and stepped in the stump.")
        elif name == "stay":
            from freesail.evolutions.scripts import regear

            # the mast's own standing rigging and the course's gear stand again; what hung
            # on the topmast stays down
            for ln in ship.lines.values():
                if ln.of == spar.id and ln.wrecked:
                    ln.wrecked = False
                    ln.state = LineState.BELAYED
                    ln.load_kn = 0.0
            regear(ship)
            self.note(
                f"The jury {_name(ship, spar.id)} stayed and its rigging set up; the course may "
                "be bent to it.",
                kind="mast.jury",
            )

    def words(self) -> dict[str, Any]:
        spar = self.spar
        name = _name(self.ship, spar.id) if spar is not None else "mast"
        return {
            "mast": name,
            "done": f"A jury {name} stands: a spare topmast stepped in the stump, stayed and "
            "rigged, at two fifths of the mast's strength; the topmast and what stood on it "
            "are still down, and the course may be bent to it.",
        }


# -- the rigging ------------------------------------------------------------------------


def parted_running_lines(ship: Ship) -> list[Line]:
    """Every parted running line that may be rove afresh (not standing, not gone with its
    spar), in the ship file's order."""
    return [
        ln
        for ln in ship.lines.values()
        if ln.state is LineState.PARTED and not ln.is_standing and not ln.wrecked
    ]


def parted_standing_lines(ship: Ship) -> list[Line]:
    return [
        ln
        for ln in ship.lines.values()
        if ln.state is LineState.PARTED and ln.is_standing and not ln.wrecked
    ]


class RigPreventersScript(PhasedScript):
    """The preventer braces, the preventer backstays or the chain slings rove
    (`params.what`): one phase, `reeve`; each line gains its `preventer`, the preventers'
    fathoms taken from the boatswain's store."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"reeve": 1200.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.lines: list[Line] = []

    @property
    def what(self) -> str:
        return str(self.params.get("what") or "braces")

    def _lines(self) -> list[Line]:
        ship = self.ship
        what = self.what
        out = []
        for ln in ship.lines.values():
            if ln.wrecked or ln.state is LineState.PARTED or getattr(ln, "preventer", False):
                continue
            if what == "braces" and ln.cls == "brace":
                yard = ship.parts.get(ln.of)
                mast = ship.parent_of(yard) if isinstance(yard, Spar) else None
                if mast is not None and mast.cls in PREVENTER_MAST_CLASSES:
                    out.append(ln)
            elif what == "backstays" and ln.cls == "backstay":
                out.append(ln)
            elif what == "slings":
                target = ship.parts.get(ln.of)
                if (
                    ln.cls in ("halyard", "throat_halyard", "peak_halyard", "tye", "lift")
                    and isinstance(target, Spar)
                    and target.cls in SLING_SPAR_CLASSES
                ):
                    out.append(ln)
        return out

    def holds(self) -> set[str]:
        return {f"preventers:{self.what}"}

    def check(self, words: dict[str, Any]) -> str | None:
        self.lines = self._lines()
        if not self.lines:
            return f"every {self.what_words()} has its preventer already, or there is none to rig"
        if self.what != "slings":
            wants = self._fathoms()
            store = parts.cordage(self.ship)
            if store.fathoms + 1e-9 < wants:
                return (
                    f"the boatswain's store has {store.describe()}, and the preventers want "
                    f"{wants:.0f} fathoms"
                )
        return None

    def _fathoms(self) -> float:
        from freesail.evolutions.scripts import line_fathoms

        return PREVENTER_FATHOMS_SHARE * sum(line_fathoms(self.ship, ln) for ln in self.lines)

    def what_words(self) -> str:
        return {
            "braces": "preventer braces",
            "backstays": "preventer backstays",
            "slings": "chain slings on the yards",
        }.get(self.what, self.what)

    def begin(self, words: dict[str, Any]) -> None:
        if not self.lines:
            self.lines = self._lines()
        self.start_phases(["reeve"])

    def end_phase(self, name: str) -> None:
        ship = self.ship
        if self.what != "slings":
            store = parts.cordage(ship)
            wants = self._fathoms()
            if store.fathoms + 1e-9 < wants:
                self.fail("the spare cordage was used meanwhile")
                return
            store.take(wants)
            ship.extra["spare_cordage_fathoms"] = store.fathoms
        for ln in self.lines:
            ln.preventer = True

    def words(self) -> dict[str, Any]:
        n = len(self.lines)
        what = self.what_words()
        return {
            "what_words": what,
            "begin": f"Rig the {what}! Hands aloft with the "
            f"{'chains' if self.what == 'slings' else 'preventers'}.",
            "done": f"The {what} rigged on {n} line{'s' if n != 1 else ''}: each keeps its "
            "office if it is shot away or parts.",
        }


class SetUpRiggingScript(PhasedScript):
    """The parted standing rigging set up again, a phase a line (`line_<i>`), the one
    named (`params.line_words`) or every one; each a new rope from the boatswain's store
    at the file's rating."""

    # the work holds its own key and not the ship herself (the runner's
    # `holds_subject`): a manoeuvre in hand does not wait for it, nor it for one
    holds_subject = False

    DEFAULTS = {"shroud": 2700.0, "backstay": 2700.0, "stay": 3600.0}

    def __init__(self, ship: Ship, params: dict[str, Any], timing: dict[str, float]):
        super().__init__(ship, params, timing)
        self.lines: list[Line] = []
        self.done_lines: list[Line] = []

    def _lines(self) -> list[Line] | str:
        ship = self.ship
        words = " ".join(str(self.params.get("line_words") or "").lower().split())
        parted = parted_standing_lines(ship)
        if not words:
            return parted
        from freesail.orders.resolve import resolve as resolve_noun_

        try:
            ids = set(resolve_noun_(ship, words, None, "set up").ids)
        except Exception as e:  # noqa: BLE001
            return str(e).rstrip(".")
        named = [ln for ln in ship.lines.values() if ln.id in ids]
        if not named:
            return f"'{words}' is no line of this ship"
        if not all(ln.is_standing for ln in named):
            return (
                "only the standing rigging (the shrouds, the backstays and the stays) is set "
                "up; a running line is rove ('reeve new lines')"
            )
        chosen = [ln for ln in named if ln.state is LineState.PARTED and not ln.wrecked]
        if not chosen:
            return (
                f"the {_name(ship, named[0].id)} stands sound; only a parted line is set up again"
            )
        return chosen

    def holds(self) -> set[str]:
        return {ln.id for ln in self.lines} | {"the boatswain"}

    def check(self, words: dict[str, Any]) -> str | None:
        found = self._lines()
        if isinstance(found, str):
            return found
        if not found:
            return "no shroud, backstay or stay is parted; there is nothing to set up"
        self.lines = found
        from freesail.evolutions.scripts import line_fathoms

        wants = sum(line_fathoms(self.ship, ln) for ln in self.lines)
        store = parts.cordage(self.ship)
        if store.fathoms + 1e-9 < wants:
            return (
                f"the boatswain's store has {store.describe()}, and the rigging wants "
                f"{wants:.0f} fathoms; knot what can be knotted and wait for the dockyard"
            )
        return None

    def begin(self, words: dict[str, Any]) -> None:
        if not self.lines:
            found = self._lines()
            self.lines = found if isinstance(found, list) else []
        self.start_phases([f"line_{i}" for i in range(len(self.lines))])

    def phase_s(self, name: str) -> float:
        i = int(name.rsplit("_", 1)[-1])
        ln = self.lines[i]
        return super().phase_s(ln.cls if ln.cls in self.DEFAULTS else "shroud")

    def start_phase(self, name: str) -> None:
        i = int(name.rsplit("_", 1)[-1])
        self.note(f"Hands aloft to set up the {_name(self.ship, self.lines[i].id)}.")

    def end_phase(self, name: str) -> None:
        ship = self.ship
        i = int(name.rsplit("_", 1)[-1])
        ln = self.lines[i]
        from freesail.evolutions.scripts import line_fathoms

        store = parts.cordage(ship)
        wants = line_fathoms(ship, ln)
        if store.fathoms + 1e-9 < wants:
            self.fail(f"the spare cordage ran out before the {_name(ship, ln.id)}")
            return
        store.take(wants)
        ship.extra["spare_cordage_fathoms"] = store.fathoms
        ln.state = LineState.BELAYED
        ln.condition = 100.0
        ln.load_kn = 0.0
        self.done_lines.append(ln)
        self.note(
            f"The {_name(ship, ln.id)} set up again with deadeyes and lanyards.",
            kind="rigging.set_up",
        )

    def words(self) -> dict[str, Any]:
        names = [_name(self.ship, ln.id) for ln in self.done_lines]
        said = ", ".join(names[:-1]) + " and " + names[-1] if len(names) > 1 else "".join(names)
        n = len(self.lines)
        return {
            "begin": f"Set up the rigging! {n} line{'s' if n != 1 else ''} to set up.",
            "done": f"The standing rigging set up again: the {said}."
            if said
            else "nothing set up.",
        }


REPAIR_SCRIPTS: dict[str, type[PhasedScript]] = {
    "batten_down": BattenDownScript,
    "plug_shot_hole": PlugShotHoleScript,
    "fother_sail": FotherSailScript,
    "fish_spar": FishSparScript,
    "cut_away_mast": CutAwayMastScript,
    "jury_mast": JuryMastScript,
    "rig_preventers": RigPreventersScript,
    "set_up_rigging": SetUpRiggingScript,
}
