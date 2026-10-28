"""HMS *Indefatigable*, the 64 of 1784 and the razee of 1795 (package 75, the first ship; her
builder B1): a stub writing nothing, laid by stage 0 (docs/design/Build-Ships.md §3.1 item 2).

Her design is docs/design/Design-Ship-Indefatigable.md: §1 the module, §12.1 what stage 0 lays
for her. Built, the module begins `import gen_ships as g` and writes
`data/ships/sixty-four.yaml` and `data/ships/razee-44.yaml` (the names the lead accepted on
2026-10-28), the 64 first and the razee derived from her as data.
"""


def build(out_dir: str) -> None:
    """Write her files to `out_dir`: none yet."""
