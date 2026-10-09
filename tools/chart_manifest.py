"""Print the chart data's manifest: every source with its licence, its attribution and what
it was used for, the regions and levels present, the checks of the study's unverified list,
and the attribution block the game shows (spec M5 §20: "a tool that prints the chart data's
manifest and attribution").

Run from the repository root:  python tools/chart_manifest.py [data/charts/manifest.yaml]
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).resolve().parents[1]


def lines_of(manifest: dict) -> list[str]:
    out = [
        f"Chart data built {manifest.get('built')} by {manifest.get('tool')} "
        f"(build {manifest.get('build_hash')})."
    ]
    out.append("")
    out.append("Sources:")
    for key, s in (manifest.get("sources") or {}).items():
        out.append(
            f"  {s.get('name', key)}: {s.get('licence_name', s.get('licence'))} "
            f"({s.get('licence_text', 'no licence text')}); {s.get('status', 'unknown')}."
        )
        if s.get("attribution"):
            out.append(f"    {s['attribution']}")
        used = s.get("used_for")
        if used:
            out.append(f"    used for: {', '.join(used) if isinstance(used, list) else used}")
    out.append("")
    out.append("Regions and levels:")
    for name, r in (manifest.get("regions") or {}).items():
        b = r.get("bounds") or {}
        out.append(
            f"  {name}: {r.get('title', '')} ({b.get('south')} to {b.get('north')} N, "
            f"{b.get('west')} to {b.get('east')} E)"
        )
    for name, c in (manifest.get("corridors") or {}).items():
        b = c.get("bounds") or {}
        out.append(
            f"  corridor {name}: level {c.get('level')}, {b.get('south')} to {b.get('north')} N, "
            f"{b.get('west')} to {b.get('east')} E, {len(c.get('tiles') or [])} tiles, "
            f"{'committed' if c.get('committed') else 'not committed'}; built by "
            f"`{c.get('built_by', '?')}`"
        )
    for level in ("world", "atlantic"):
        lv = manifest.get(level) or {}
        if lv:
            state = "present" if lv.get("tiles") else "not committed"
            out.append(f"  {level}: {state}; built by `{lv.get('built_by', '?')}`")
    charts = manifest.get("charts") or {}
    if charts:
        out.append("")
        out.append("Charts (package 38: the regions each holds and the corridor under them):")
        for name, c in charts.items():
            held = ", ".join(c.get("regions") or []) or "none"
            corridor = c.get("corridor")
            out.append(
                f"  {name}: {c.get('title', '')}; regions {held}"
                + (f"; corridor {corridor}" if corridor else "")
                + (
                    f"; not yet built: {', '.join(c['regions_not_built'])}"
                    if c.get("regions_not_built")
                    else ""
                )
            )
    notes = manifest.get("notes") or {}
    items = notes.get("items") if isinstance(notes, dict) else None
    if items:
        out.append("")
        out.append("The study's unverified list, as checked:")
        for it in items:
            if isinstance(it, dict):
                found = it.get("found", it.get("status", ""))
                out.append(f"  {it.get('item', it.get('name', '?'))}: {found}")
            else:
                out.append(f"  {it}")
    out.append("")
    out.append("Attribution, as the game shows it:")
    out.append(f"  {manifest.get('attribution', '')}")
    return out


def main(argv: list[str] | None = None) -> int:
    args = list(sys.argv[1:] if argv is None else argv)
    path = Path(args[0]) if args else REPO_ROOT / "data" / "charts" / "manifest.yaml"
    manifest = yaml.safe_load(path.read_text(encoding="utf-8"))
    print("\n".join(lines_of(manifest)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
