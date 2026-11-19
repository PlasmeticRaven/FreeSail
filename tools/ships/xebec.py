"""The xebec, the Spanish navy's and the regency's cruiser under three lateens, and the merchant
xebec of the same hull (package 90, the third hull; her builder): a stub writing nothing, laid by
stage 0 (docs/design/Plan-Package90.md §5.1 item 1).

Her design is docs/design/Design-Ship-Xebec.md, from her research note,
docs/design/Research-Xebec-2026-11.md, and the engine's note for her lateens and her sweeps,
docs/design/Design-Package90-Engine.md. Built, the module begins `import gen_ships as g`, cuts her
lateens with `ships.lateen`, and writes `data/ships/xebec.yaml` and `data/ships/merchant-xebec.yaml`
(her design's decision 2).
"""


def build(out_dir: str) -> None:
    """Write her files to `out_dir`: none yet."""
