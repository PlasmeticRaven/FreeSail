"""The Ship: a graph of parts with role queries.

Everything the engine asks about a ship it asks here, by role: the yard of
this sail, the braces of this yard, everything that stands on this mast.
The Ship also carries the motion state (`dyn`), the hull, a queue of notes
for the log, and two pluggable hooks: `stepper` (physics and evolutions,
called once per tick) and `order_handler` (the Orders parser). The World
calls `step` and `handle_order` and needs nothing else.
"""

from __future__ import annotations

import weakref
from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.ship.parts import Dynamics, Gun, Hull, Line, Part, Sail, Spar
from freesail.ship.schema import BY_DECK, FitSpec, ShipSpec
from freesail.ship.stub import OrderError

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

Note = tuple[str, str, str, str | None, dict[str, Any]]  # severity, kind, text, subject, data
Stepper = Callable[["Ship", float, "Wind"], None]
OrderHandler = Callable[["Ship", str], tuple[str, str, dict[str, Any]]]

# The yards on a schooner's mast, each ship's (`Ship.on_schooner_mast`; package 75, B3.4), found
# once a ship from her parts as filed and held here, beside her and not in her: the checkpoint
# pickles the Ship's own `__dict__` (`core/replay._Pickler`), and `pickle` her `__dict__` too,
# so a memo kept in her (as `_chain_memo` is) would put a key in every save that had read the
# rule, and one kept here puts none. A ship read back from a checkpoint finds them again from the
# same parts, the same yards.
_SCHOONER_YARDS: weakref.WeakKeyDictionary[Ship, frozenset[str]] = weakref.WeakKeyDictionary()

# A braced yard's level, each ship's (`Ship.yard_level`; package 90, A5), found once a ship from
# her parts as filed and held here for the same reason as the schooner's yards.
_YARD_LEVELS: weakref.WeakKeyDictionary[Ship, dict[str, int]] = weakref.WeakKeyDictionary()

# The spars a yard hangs on, by its level: the course on the lower mast, the topsail on the
# topmast, the topgallant and the royal on theirs.
YARD_LEVEL_SPARS = ("mast", "topmast", "topgallant_mast", "royal_mast")


def _square_foot_m(yard: Spar, sail: Sail, deck_height_m: float) -> float:
    """A square sail's foot above the deck as her file cuts it: its head on its yard and its
    centre (`centre_height_m`, the centre of its cut) midway between head and foot, so the foot
    is the centre's height less its depth below the yard (package 90, nudge 39). One datum, the
    deck: the yards' (`Spar.height_m`, above the deck), and so the lateen yard's it is set
    against (`Ship._find_yard_levels`). The centre is filed above the water
    (TechnicalSpec-M0-M2.md §6.2) and is brought to the deck by her `deck_height_m` (the lead's
    nudge 88, item 3: the centre above the water was set against the yard above the deck, the
    foot too high by twice her deck's height, on the tartane 1.08 m)."""
    return 2.0 * (sail.centre_height_m - deck_height_m) - yard.height_m


class Ship:
    def __init__(self, spec: ShipSpec, fit: str | None = None):
        self.spec = spec
        self.name = spec.name
        self.hull = Hull(spec.hull)
        self.spars: dict[str, Spar] = {s.id: Spar.from_spec(s) for s in spec.spars}
        self.sails: dict[str, Sail] = {s.id: Sail.from_spec(s) for s in spec.sails}
        self.lines: dict[str, Line] = {ln.id: Line.from_spec(ln) for ln in spec.lines}
        # the guns (spec M7 §7; package 70): the fit the scenario chose, or the file's
        # default; a ship whose file lists no armament carries none
        self.fit_spec: FitSpec | None = (
            spec.armament.fit(fit) if spec.armament is not None else None
        )
        self.fit: str = self.fit_spec.name if self.fit_spec is not None else ""
        self.guns: dict[str, Gun] = (
            {g.id: Gun.from_spec(g) for g in self.fit_spec.guns} if self.fit_spec else {}
        )
        # numbered by deck where her armament says so (package 75, B7.d:
        # docs/design/Design-Ship-Bellerophon.md §5.2), read by each gun's name and crew's key
        if spec.armament is not None and spec.armament.numbering == BY_DECK:
            for gun in self.guns.values():
                gun.by_deck = True
        self.parts: dict[str, Part] = {**self.spars, **self.sails, **self.lines, **self.guns}
        self.groups: dict[str, list[str]] = {g: list(m) for g, m in spec.groups.items()}
        self.aliases: dict[str, str] = dict(spec.aliases)
        self.dyn = Dynamics()
        self.notes: list[Note] = []
        self.stepper: Stepper | None = None
        self.order_handler: OrderHandler | None = None
        self.extra: dict[str, Any] = {}  # scratch space for systems (evolution runner etc.)
        self._index_roles()

    # -- role index ------------------------------------------------------------

    def _index_roles(self) -> None:
        self._children: dict[str, list[str]] = {sid: [] for sid in self.spars}
        for s in self.spars.values():
            if s.parent:
                self._children[s.parent].append(s.id)
        self._sail_by_role: dict[tuple[str, str], list[str]] = {}
        for sl in self.sails.values():
            for role, target in sl.roles.items():
                self._sail_by_role.setdefault((role, target), []).append(sl.id)
        self._lines_of: dict[str, list[str]] = {}
        for ln in self.lines.values():
            self._lines_of.setdefault(ln.of, []).append(ln.id)
        # Memos of the role queries the physics asks every substep (package 29's profile:
        # `spar_chain`, `lines_of` and `mast_of` were a third of a tick). The graph's shape
        # (parents, roles, what a line is of) is fixed once the ship is loaded: states
        # change, parts never move in the graph. Each memo holds the answer as built by the
        # query itself; callers get a fresh list, so nothing they do reaches the memo.
        self._chain_memo: dict[str, tuple[Spar, ...]] = {}
        self._lines_memo: dict[tuple[str, str | None], tuple[Line, ...]] = {}

    # -- queries: sails and spars -------------------------------------------

    def yard_of(self, sail: str | Sail) -> Spar | None:
        sl = self._sail(sail)
        yid = sl.roles.get("yard")
        return self.spars[yid] if yid else None

    def sail_of(self, spar: str | Spar) -> Sail | None:
        """The sail whose yard (or gaff, lug yard, lateen yard) this spar is."""
        sp = self._spar(spar)
        for role in ("yard", "gaff", "sprit", "boom"):
            ids = self._sail_by_role.get((role, sp.id))
            if ids:
                return self.sails[ids[0]]
        return None

    def sails_using(self, spar: str | Spar) -> list[Sail]:
        """Every sail with a role link to this spar, or hanked to a stay that is of it."""
        sp = self._spar(spar)
        out: list[Sail] = []
        for (_, target), ids in self._sail_by_role.items():
            if target == sp.id:
                out.extend(self.sails[i] for i in ids if self.sails[i] not in out)
        for ln in self.lines_of(sp):
            for i in self._sail_by_role.get(("stay", ln.id), []):
                if self.sails[i] not in out:
                    out.append(self.sails[i])
        return out

    def spar_of_role(self, sail: str | Sail, role: str) -> Spar | None:
        sl = self._sail(sail)
        sid = sl.roles.get(role)
        return self.spars[sid] if sid and sid in self.spars else None

    def parent_of(self, spar: str | Spar) -> Spar | None:
        sp = spar if isinstance(spar, Spar) else self._spar(spar)
        return self.spars[sp.parent] if sp.parent else None

    def spar_chain(self, part: str | Part) -> list[Spar]:
        """The spars this part depends on, nearest first, down to the one on the hull.

        For a sail: its principal spar, then that spar's parents. For a spar:
        itself, then its parents. For a line: the chain of what it is of.
        """
        key = part if isinstance(part, str) else part.id
        chain = self._chain_memo.get(key)
        if chain is None:
            chain = tuple(self._build_spar_chain(part))
            self._chain_memo[key] = chain
        return list(chain)

    def _build_spar_chain(self, part: str | Part) -> list[Spar]:
        p = self._part(part)
        if isinstance(p, Sail):
            start = self._principal_spar(p)
        elif isinstance(p, Line):
            target = self.parts[p.of]
            return self.spar_chain(target)
        else:
            start = p
        chain: list[Spar] = []
        cur: Spar | None = start
        while cur is not None:
            chain.append(cur)
            cur = self.parent_of(cur)
        return chain

    def dependents(self, spar: str | Spar) -> list[Part]:
        """Every part that stands on, hangs from, or is of this spar, recursively."""
        sp = self._spar(spar)
        out: list[Part] = []
        stack = [sp.id]
        seen: set[str] = set()
        while stack:
            sid = stack.pop()
            if sid in seen:
                continue
            seen.add(sid)
            for child in self._children.get(sid, []):
                out.append(self.spars[child])
                stack.append(child)
            for sl in self.sails_using(sid):
                if sl not in out:
                    out.append(sl)
                    for ln in self.lines_of(sl):
                        if ln not in out:
                            out.append(ln)
            for ln in self.lines_of(sid):
                if ln not in out:
                    out.append(ln)
        return out

    def sails_on(self, spar: str | Spar) -> list[Sail]:
        """Sails carried by this spar or anything standing on it."""
        return [p for p in self.dependents(spar) if isinstance(p, Sail)]

    def mast_of(self, part: str | Part) -> Spar | None:
        """The lower mast (or bowsprit) at the root of this part's spar chain."""
        key = part if isinstance(part, str) else part.id
        chain = self._chain_memo.get(key)
        if chain is None:
            self.spar_chain(part)
            chain = self._chain_memo[key]
        return chain[-1] if chain else None

    def under_bowsprit(self, part: str | Part) -> bool:
        """A yard crossed under the bowsprit or the jib-boom (the spritsail yard, the
        sprit-topsail yard: Steel 1794 vol. I pp. 196-197; Lavery I27-I30), or the square
        sail bent to one (package 75; docs/design/Design-ShipsEngineExtensions.md §4.2): a
        spar of class `yard` whose chain roots at a bowsprit. Not a jib, whose chain roots
        there too: the rule names the yards and their square sails alone. Read through
        `mast_of`'s memo, at the nine places of §4.2 (the engine's bowsprit step, B3.2)."""
        p: Part | None = self._part(part)
        if isinstance(p, Sail):
            p = self.yard_of(p) if p.cls == "square" else None
        if not isinstance(p, Spar) or p.cls != "yard":
            return False
        root = self.mast_of(p)
        return root is not None and root.cls == "bowsprit"

    def on_schooner_mast(self, part: str | Part) -> bool:
        """A braced yard on a schooner's mast, or the square sail bent to one (package 75, B3.4;
        the lead's ruling of 2026-11-06 on docs/design/Design-Ship-PrinceDeNeufchatel.md §12.2a):
        "An after mast with yards and no yard on its lower mast handles as a fore-and-after's
        mast". The *Neufchatel*'s main was "rigged as a schooner" though her foremast was
        "rigged as a brig" (Cobb 1841 vol. I p. 38, as her decision 13 cites it), and the two light
        yards of her main topgallant, or a topsail schooner's main topsail, do not make her a
        brig to the manoeuvres.

        True for a spar of class `yard` whose lower mast (`mast_of`) is not the foremost lower
        mast carrying a braced yard and carries no braced yard on the lower mast itself (a yard
        whose parent is that mast), and for a square sail whose yard is one. The yards under the
        bowsprit (`under_bowsprit`) count for nothing: never such a yard, nor making the
        bowsprit a mast with yards. Judgement: a lug's yard and a lateen yard have classes of
        their own and are no braced yard (`Spar.is_yard`), so neither makes a mast one with
        yards nor stands as its lower yard: a tartane's main, a lateen under a square topsail,
        is her one mast with yards, as the cutter's is, and a polacre's square main with its
        lower yard is hers between her two lateens.

        Read from every spar as filed, wrecked or sent down or not, once a ship, and held
        (`_SCHOONER_YARDS`): a brig whose main yard is shot away and sent down in the middle of a
        fight stays a brig. Read where the manoeuvres count the masts with yards
        (`evolutions.scripts._masts_with_yards`, Ext §4.2's place 1) and where the helm and the
        gale's reduction ask whether she is square-rigged (`physics.sails._square_rigged`, place
        3), and for the time of the tack's swing at "mainsail haul", the short after swing for a
        schooner's light main yards (`evolutions.scripts.TackScript._after_swing_s`, the lead's
        ruling 1 of 2026-11-06 on place 2's timing), and where no mast carries yards at place 1,
        every fore yard shot away, for her after yards (`evolutions.scripts.head_and_after_yards`,
        place 2, the lead's ruling 3 of 2026-11-06: "nothing changes in their handling but that
        they are no longer left standing"; before it they were in neither list), and nowhere
        else: her main's yards are still braced and trimmed, and swung as after yards, her fore
        yards whole or shot away.
        The limits, recorded: a schooner with a lower square-sail yard on her main (Fincham p. 78,
        as her design cites it; the *Neufchatel*'s D10(d), not taken) still classes as a brig;
        and so does one whose main is a pole mast with a square topsail yard filed on the lower
        mast itself, as the smack's topsail yard is (`data/ships/smack.yaml`, no topmast), that
        yard standing as its lower yard."""
        p = self._part(part)
        if isinstance(p, Sail):
            yard = p.roles.get("yard") if p.cls == "square" else None
            return yard is not None and yard in self._schooner_yards()
        return isinstance(p, Spar) and p.id in self._schooner_yards()

    def yard_level(self, yard: str | Spar) -> int:
        """A braced yard's level on its lower mast (package 90, A5; docs/design/Design-Ship-
        Polacre.md §5.1, decision 6): 0 the course, 1 the topsail, 2 the topgallant, 3 the
        royal; -1 a yard under the bowsprit, which stands on no mast. Read from its order on its
        lower mast as filed, not from the class of the spar it hangs on alone: the level of that
        spar (`YARD_LEVEL_SPARS`) and one more for each braced yard on the same spar below it,
        so that on a pole mast, the mast and topmast in one stick, the topsail yard crossing the
        mast's own head over the lower yard is a topsail and not a course (the smack's, the
        polacre's main). A square yard on a lower mast with no braced yard below it and a whole
        lateen's yard below it there counts that yard as its level below where its sail is set
        over the lateen, the sail's foot clear above the lateen's yard (JUDGEMENT, the lead's lean
        ruled, Plan §13.1 item 2, and narrowed so, nudge 39: the tartane's topsail over her great
        lateen, the polacre's mizen topsail over her lateen mizen); a square sail whose foot comes
        down below the lateen's yard is the course, wherever its yard crosses (the tartane's
        tréou). On every file with one yard to a spar
        it is the spar's level, as it always was. Found once a ship and held (`_YARD_LEVELS`);
        any other spar's level is its parent's, or 0."""
        sp = yard if isinstance(yard, Spar) else self._spar(yard)
        levels = _YARD_LEVELS.get(self)
        if levels is None:
            levels = self._find_yard_levels()
            _YARD_LEVELS[self] = levels
        found = levels.get(sp.id)
        if found is not None:
            return found
        parent = self.spars.get(sp.parent) if sp.parent else None
        cls = parent.cls if parent is not None else ""
        return YARD_LEVEL_SPARS.index(cls) if cls in YARD_LEVEL_SPARS else 0

    def is_pole_mast(self, mast: str | Spar) -> bool:
        """A lower mast that is a pole, the mast and topmast in one stick (package 90, A6;
        docs/design/Design-Ship-Polacre.md §5.1, decision 7): a braced yard above its lowest
        hangs on the mast itself and no topmast stands on it (the smack's main, the polacre's, a
        tartane's). Read from the parts as filed, with no key, as the schooner's mast is."""
        sp = mast if isinstance(mast, Spar) else self._spar(mast)
        if sp.cls != "mast":
            return False
        on_it = [y for y in self.spars.values() if y.cls == "yard" and y.parent == sp.id]
        if not any(self.yard_level(y) > 0 for y in on_it):
            return False
        return not any(s.parent == sp.id and s.cls == "topmast" for s in self.spars.values())

    def on_pole(self, part: str | Part) -> bool:
        """A braced yard above the lowest on a pole mast (`is_pole_mast`), or the square sail
        bent to one (package 90, A6): taken in by letting its halyards go and lowering it onto
        the yard below, and furled from the yard below."""
        p = self._part(part)
        if isinstance(p, Sail):
            yid = p.roles.get("yard") if p.cls == "square" else None
            if yid is None or yid not in self.spars:
                return False
            p = self.spars[yid]
        if not isinstance(p, Spar) or p.cls != "yard" or not p.parent:
            return False
        mast = self.spars.get(p.parent)
        return mast is not None and self.yard_level(p) > 0 and self.is_pole_mast(mast)

    def _find_yard_levels(self) -> dict[str, int]:
        """Every braced yard's level (`yard_level`), from the parts as filed, wrecked or sent
        down or not, each yard's lower mast found by its parents (as `_schooner_yards` finds
        them), so that the ship's own memos, and so every pickle, are as they were."""
        yards = [sp for sp in self.spars.values() if sp.cls == "yard"]

        def root_of(sp: Spar) -> Spar:
            while sp.parent:
                sp = self.spars[sp.parent]
            return sp

        out: dict[str, int] = {}
        for order, sp in enumerate(yards):
            root = root_of(sp)
            if root.cls == "bowsprit":
                out[sp.id] = -1  # under the bowsprit: no mast's
                continue
            parent = self.spars.get(sp.parent) if sp.parent else None
            cls = parent.cls if parent is not None else ""
            level = YARD_LEVEL_SPARS.index(cls) if cls in YARD_LEVEL_SPARS else 0
            below = sum(
                1
                for i, other in enumerate(yards)
                if other.parent == sp.parent and (other.height_m, i) < (sp.height_m, order)
            )
            level += below
            if level == 0:
                # a square sail set over a whole lateen, its foot clear above the lateen's yard,
                # and no braced yard below it on its mast; not one whose foot comes down below
                # that yard to the deck (the tartane's tréou, her course: nudge 39, ruling 1)
                square = self.sail_of(sp)
                deck = self.hull.spec.deck_height_m
                foot = _square_foot_m(sp, square, deck) if square is not None else None
                for lat in self.spars.values():
                    sail = self.sail_of(lat) if lat.cls == "lateen_yard" else None
                    if (
                        foot is not None
                        and sail is not None
                        and sail.cls == "lateen"
                        and not sail.cut_at_mast
                        and root_of(lat) is root
                        and lat.height_m < sp.height_m
                        and foot > lat.height_m
                    ):
                        level = 1
                        break
            out[sp.id] = level
        return out

    def _schooner_yards(self) -> frozenset[str]:
        """The ids of the braced yards on a schooner's mast (`on_schooner_mast`), found once a
        ship from the parts as filed. Each yard's lower mast is found by its parents, not
        through `mast_of`, whose memo is pickled with her, so that reading the rule leaves the
        ship's own state, and so every pickle and checkpoint, as it was."""
        found = _SCHOONER_YARDS.get(self)
        if found is not None:
            return found
        on: list[tuple[str, Spar]] = []  # each braced yard and its lower mast, in file order
        masts: dict[str, Spar] = {}  # the lower masts carrying braced yards, first seen first
        lower: set[str] = set()  # the spars that carry a braced yard on themselves
        for sp in self.spars.values():
            if sp.cls != "yard":
                continue
            root = sp
            while root.parent:
                root = self.spars[root.parent]
            if root.cls == "bowsprit":
                continue  # under the bowsprit: counted for nothing
            on.append((sp.id, root))
            masts.setdefault(root.id, root)
            if sp.parent:
                lower.add(sp.parent)
        schooner: set[str] = set()
        if masts:
            foremost = max(masts.values(), key=lambda m: m.x_m)
            schooner = {mid for mid in masts if mid != foremost.id and mid not in lower}
        found = frozenset(yid for yid, root in on if root.id in schooner)
        _SCHOONER_YARDS[self] = found
        return found

    # -- queries: lines -------------------------------------------------------

    def lines_of(self, part: str | Part, cls: str | None = None) -> list[Line]:
        key = (part if isinstance(part, str) else part.id, cls)
        found = self._lines_memo.get(key)
        if found is None:
            p = self._part(part)
            out = [self.lines[i] for i in self._lines_of.get(p.id, [])]
            if cls:
                out = [ln for ln in out if ln.cls == cls]
            found = tuple(out)
            self._lines_memo[key] = found
        return list(found)

    def line_of(self, part: str | Part, cls: str, side: str | None = None) -> Line | None:
        for ln in self.lines_of(part, cls):
            if side is None or ln.side == side:
                return ln
        return None

    def halyard_of(self, part: str | Part) -> Line | None:
        p = self._part(part)
        ln = self.line_of(p, "halyard")
        if ln is None and isinstance(p, Sail):
            yard = self.yard_of(p) or self.spar_of_role(p, "gaff")
            if yard is not None:
                ln = self.line_of(yard, "halyard") or self.line_of(yard, "peak_halyard")
        return ln

    def braces_of(self, yard: str | Spar) -> list[Line]:
        return self.lines_of(yard, "brace")

    def sheets_of(self, sail: str | Sail) -> list[Line]:
        return self.lines_of(sail, "sheet")

    # -- notes for the log ----------------------------------------------------

    def note(
        self,
        severity: str,
        kind: str,
        text: str,
        subject: str | None = None,
        data: dict[str, Any] | None = None,
    ) -> None:
        self.notes.append((severity, kind, text, subject, data or {}))

    def drain_notes(self) -> list[Note]:
        out, self.notes = self.notes, []
        return out

    # -- the World's interface ---------------------------------------------

    def step(self, dt: float, wind: Wind) -> list[Note]:
        if self.stepper is not None:
            self.stepper(self, dt, wind)
        return self.drain_notes()

    def handle_order(self, text: str) -> tuple[str, str, dict[str, Any]]:
        if self.order_handler is None:
            raise OrderError("This ship has no one to take orders yet.")
        return self.order_handler(self, text)

    @property
    def heading(self) -> float:
        return self.dyn.heading

    def state(self) -> dict[str, Any]:
        return {
            "name": self.name,
            **self.dyn.state(),
            "sails": [
                {
                    "id": s.id,
                    "class": s.cls,
                    "state": s.state.value,
                    "reefs": s.reefs,
                    "wrecked": s.wrecked,
                    "area_effective": s.area_effective_m2,
                    "thrust_kn": s.thrust_kn,
                    "side_kn": s.side_force_kn,
                    "strain_ratio": s.strain_ratio,
                    "backed": s.backed,
                }
                for s in self.sails.values()
            ],
            "spars": [
                {
                    "id": s.id,
                    "class": s.cls,
                    "condition": s.condition,
                    "wrecked": s.wrecked,
                    "brace_angle": s.brace_angle,
                    "strain_ratio": s.strain_ratio,
                }
                for s in self.spars.values()
            ],
            "lines": [
                {
                    "id": ln.id,
                    "class": ln.cls,
                    "state": ln.state.value,
                    "hauled": getattr(ln, "bowline_hauled", False),  # milestone 3b, for the view
                    "strain_ratio": ln.strain_ratio,
                }
                for ln in self.lines.values()
            ],
            # the guns (package 70): their load state, for the view and the tests
            "guns": [
                {
                    "id": g.id,
                    "kind": g.kind,
                    "pounder": g.pounder,
                    "place": g.place,
                    "number": g.number,
                    "side": g.side,
                    # a pivot gun's training, for the view (PROVISIONAL, 2026-10-25)
                    **({"train_deg": round(g.train_deg, 1)} if g.place == "pivot" else {}),
                    "state": g.state_words,
                    "dismounted": g.dismounted,
                    "fired": g.fired,
                }
                for g in self.guns.values()
            ],
        }

    def summary_lines(self) -> list[str]:
        d = self.dyn
        set_sails = [s.id for s in self.sails.values() if s.is_set]
        return [
            f"{self.name}: heading {units.format_heading(d.heading)}, "
            f"speed {units.format_speed(d.speed)}, leeway {units.rad_to_deg(d.leeway):.0f}°, "
            f"heel {units.rad_to_deg(d.heel):.0f}°",
            f"Apparent wind {units.rad_to_deg(abs(d.apparent_wind_angle)):.0f}° "
            f"{units.wind_bearing_words(d.apparent_wind_angle)}, "
            f"{units.format_speed(d.apparent_wind_speed)}; "
            f"helm {units.rad_to_deg(d.rudder):+.0f}°",
            "Sail set: " + (", ".join(set_sails) if set_sails else "none"),
        ]

    def save_ref(self) -> dict[str, Any]:
        return {"type": "file", "path": self.spec.source}

    # -- helpers --------------------------------------------------------------

    def _part(self, p: str | Part) -> Part:
        if isinstance(p, Part):
            return p
        try:
            return self.parts[p]
        except KeyError:
            raise KeyError(f"no part '{p}' in {self.name}") from None

    def _spar(self, p: str | Spar) -> Spar:
        part = self._part(p)
        if not isinstance(part, Spar):
            raise TypeError(f"'{part.id}' is a {part.cls}, not a spar")
        return part

    def _sail(self, p: str | Sail) -> Sail:
        part = self._part(p)
        if not isinstance(part, Sail):
            raise TypeError(f"'{part.id}' is a {part.cls}, not a sail")
        return part

    def _principal_spar(self, sl: Sail) -> Spar | None:
        for role in ("yard", "gaff", "boom", "sprit", "mast", "halyard_spar"):
            sid = sl.roles.get(role)
            if sid and sid in self.spars:
                return self.spars[sid]
        stay = sl.roles.get("stay")
        if stay and stay in self.lines:
            target = self.lines[stay].of
            if target in self.spars:
                return self.spars[target]
        return None

    def iter_parts(self) -> Iterable[Part]:
        return self.parts.values()
