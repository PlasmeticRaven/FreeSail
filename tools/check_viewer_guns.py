"""Check that every gun of a ship file is drawn by the viewer's one rule (package 81).

    python tools/check_viewer_guns.py [data/ships/<file>.yaml ...]

With no files, every file under data/ships/. For each file: what she gives and lacks of the
contract (docs/design/Design-ViewerAction.md §1); for each fit, each gun's place by the rule
(§2: in a port, over the rail, on the rail, a pivot) or why not; the ports empty in that fit;
the notes for the ships session (a triple put over the rail by the side's test and not at the
generator's 2 in; a port cut to the rail); each gun whose weight stands more than a tenth off
its pattern's (§3.2); and each port's sill on her drawn side, below her rail, between her
stem and her stern. The ship builder's checklist is in docs/design/Build-Ships.md §6's
postscript.

Exit status 1 if any gun is refused or any port lies off her drawn side, else 0. The rule and
the table are `freesail/api/viewer_guns.py`'s, the functions the server serves the viewer from,
so what is checked is what is drawn. Reads the files; writes nothing.
"""

from __future__ import annotations

import argparse
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from freesail.api import viewer_guns as V  # noqa: E402
from freesail.ship import form  # noqa: E402
from freesail.ship.loader import load_spec  # noqa: E402
from freesail.ship.profile import rail_at  # noqa: E402

# a port's sill on her drawn side: the side's half-breadth there at least this much
ON_THE_SIDE_M = 0.05


@dataclass
class Report:
    """One file's check: its lines to print and whether it passes."""

    path: str
    lines: list[str] = field(default_factory=list)
    refused: list[str] = field(default_factory=list)
    off_side: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.refused and not self.off_side


def check(path: str | Path) -> Report:
    """The check of one ship file."""
    spec = load_spec(path)
    rep = Report(str(path))
    say = rep.lines.append
    profile = spec.hull.profile
    arm = spec.armament
    if arm is None or not arm.fits:
        n = len(V.ports(profile, [], {}))
        say(f"{Path(path).name}: no armament; {n} empty port{'s' if n != 1 else ''} a side")
        return rep
    every = [g for fit in arm.fits.values() for g in fit.guns]
    lacks = V.contract(profile, every)
    given = "the contract given" if not lacks else "lacks " + "; ".join(lacks)
    say(f"{Path(path).name}: {given}")
    for name, fit in arm.fits.items():
        placings = [V.place(profile, g) for g in fit.guns]
        hows = Counter(p.how or "refused" for p in placings)
        counts = ", ".join(f"{n} {h}" for h, n in hows.items())
        say(f"  fit '{name}': {len(fit.guns)} guns: {counts}")
        for g, p in zip(fit.guns, placings, strict=True):
            if p.how is None:
                rep.refused.append(f"{name}: {g.id}: {p.refused}")
                say(f"    REFUSED {g.id}: {p.refused}")
            for note in p.notes:
                say(f"    note {g.id}: {note}")
            f = V.figure(g.kind, g.pounder, g.weight_cwt)
            if f.weight_off > V.WEIGHT_LISTED_SHARE:
                say(
                    f"    weight {g.id}: {g.weight_cwt:g} cwt, {f.weight_off:.0%} off its "
                    f"pattern ({f.pattern})"
                )
        ports = V.ports(profile, placings, {g.id: g.side for g in fit.guns})
        empty = Counter(p.deck for p in ports if not p.guns)
        if empty:
            say("    empty ports a side: " + ", ".join(f"{d} {n}" for d, n in empty.items()))
    if profile is not None:
        for p in V.ports(profile, [], {}):
            for x in (p.x_m - p.width_m / 2, p.x_m + p.width_m / 2):
                hb = form.half_breadth_at(spec.hull, x, p.sill_m)
                if hb < ON_THE_SIDE_M or p.sill_m >= rail_at(profile, x):
                    rep.off_side.append(f"the {p.deck} port at {p.x_m:g} m: its sill off her side")
                    say(f"  OFF HER SIDE: the {p.deck} port at {p.x_m:g} m, at {x:.2f} m")
                    break
    return rep


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="ship files (default: every file under data/ships/)")
    args = ap.parse_args(argv)
    files = args.files or sorted(str(p) for p in (ROOT / "data" / "ships").glob("*.yaml"))
    ok = True
    for f in files:
        rep = check(f)
        print("\n".join(rep.lines))
        ok = ok and rep.ok
    print("clean" if ok else "NOT clean")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
