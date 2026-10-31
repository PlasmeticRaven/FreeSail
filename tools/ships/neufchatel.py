"""The *Prince de Neufchatel*, the American privateer built at New York in 1812-13 (package 75,
the second ship; her builder B2): a stub writing nothing, laid by stage 0
(docs/design/Build-Ships.md §3.1 item 2).

Her design is not yet written: it is designed before her build, as
`docs/design/Design-Ship-<name>.md` (Build-Ships.md §13), from her research note,
docs/design/Research-PrinceDeNeufchatel-2026-10.md. What stage 0 lays for her and what her
design must settle are Build-Ships.md §3.3 and §13.1. Built, the module begins
`import gen_ships as g` and writes `data/ships/hermaphrodite-brig.yaml` (the name the lead
accepted on 2026-10-28).
"""


def build(out_dir: str) -> None:
    """Write her file to `out_dir`: none yet."""
