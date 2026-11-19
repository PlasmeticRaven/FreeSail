"""The tartane, a Provençal coaster under a great lateen and a square topsail, and the coastguard
tartane of the same hull (package 90, the first hull; her builder): a stub writing nothing, laid by
stage 0 (docs/design/Plan-Package90.md §5.1 item 1).

Her design is docs/design/Design-Ship-Tartane.md, from her research note,
docs/design/Research-Tartane-2026-11.md, and the engine's note for her lateens,
docs/design/Design-Package90-Engine.md. Built, the module begins `import gen_ships as g`, cuts her
lateens with `ships.lateen` (the shared cut, which her builder fills and merges alone first), and
writes `data/ships/tartane.yaml` (the trader) and `data/ships/coastguard-tartane.yaml` (her design's
decision 1).
"""


def build(out_dir: str) -> None:
    """Write her files to `out_dir`: none yet."""
