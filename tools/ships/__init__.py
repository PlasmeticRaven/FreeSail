"""The new ships of package 75, one module each (docs/design/Build-Ships.md §3.1 items 1 to 3;
docs/design/Plan-ShipsWorkflow.md, Phase 3).

`tools/gen_ships.py` writes the eight ship files of the packages before 75 from its own
functions and then, in its `__main__` block, calls `build(out_dir)` of each module its
`SHIP_MODULES` names, in the order the ships are built. Before the first it makes the name
`gen_ships` the running script (`sys.modules.setdefault("gen_ships", ...)`), and `ships` is this
directory because the script's own, `tools/`, is on the path when it runs. So a ship's module
begins `import gen_ships as g`, takes every helper as `g.<name>` (the one copy of `Builder`,
`DesignLoad` and the rest that the script is running: Design-Ship-Indefatigable.md §1.2), and is
imported by that hook alone. Each is a stub writing nothing until its builder fills it.

The `hull_*.py` modules (package 75's hull step, SW-2 with SW-2b.2) are no ships' modules. Each
gives one or two of the eight files their drawn hull and writes no file: the script's own function
for that ship imports it plainly, at the one place it calls it, once `gen_ships` is the running
script, and a test may import it the same way. `SHIP_MODULES` does not name them, and they have no
`build`.

`period.py` holds the period's tables the new ships share: constants with their sources,
importing nothing, which the builder of each ship's window may append to.
"""
