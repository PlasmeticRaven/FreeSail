"""The Ship: a graph of parts with role queries.

Everything the engine asks about a ship it asks here, by role: the yard of
this sail, the braces of this yard, everything that stands on this mast.
The Ship also carries the motion state (`dyn`), the hull, a queue of notes
for the log, and two pluggable hooks: `stepper` (physics and evolutions,
called once per tick) and `order_handler` (the Orders parser). The World
calls `step` and `handle_order` and needs nothing else.
"""

from __future__ import annotations

from collections.abc import Callable, Iterable
from typing import TYPE_CHECKING, Any

from freesail import units
from freesail.ship.parts import Dynamics, Hull, Line, Part, Sail, Spar
from freesail.ship.schema import ShipSpec
from freesail.ship.stub import OrderError

if TYPE_CHECKING:
    from freesail.physics.wind import Wind

Note = tuple[str, str, str, str | None, dict[str, Any]]  # severity, kind, text, subject, data
Stepper = Callable[["Ship", float, "Wind"], None]
OrderHandler = Callable[["Ship", str], tuple[str, str, dict[str, Any]]]


class Ship:
    def __init__(self, spec: ShipSpec):
        self.spec = spec
        self.name = spec.name
        self.hull = Hull(spec.hull)
        self.spars: dict[str, Spar] = {s.id: Spar.from_spec(s) for s in spec.spars}
        self.sails: dict[str, Sail] = {s.id: Sail.from_spec(s) for s in spec.sails}
        self.lines: dict[str, Line] = {ln.id: Line.from_spec(ln) for ln in spec.lines}
        self.parts: dict[str, Part] = {**self.spars, **self.sails, **self.lines}
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
