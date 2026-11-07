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
from freesail.ship.schema import FitSpec, ShipSpec
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
        ruling 1 of 2026-11-06 on place 2's timing), and nowhere else: her main's yards are
        still braced and trimmed, and swung as after yards while her fore keeps a working yard
        (with every fore yard shot away no mast carries yards at place 1, and
        `evolutions.scripts.head_and_after_yards`, place 2, left, puts them in neither list:
        reported to the lead at B3.4).
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
