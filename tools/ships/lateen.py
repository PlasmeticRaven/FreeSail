"""The whole lateen's cut, shared by package 90's three lateen hulls (the tartane, the polacre and
the xebec): a stub, laid by stage 0 (docs/design/Plan-Package90.md §5.1 item 1), holding nothing
yet.

Filled, it is pure: from a lateen yard's length and the mast's raked line it gives the yard, the
sail's corners, its area and centre, and the slinging at a third on the mast's raked line, reading
nothing and writing nothing (its contract: docs/design/Design-Ship-Polacre.md §1.1 and
docs/design/Design-Ship-Xebec.md §4.2). The tartane's builder fills it and merges it alone, first,
before the polacre's and the xebec's rigs are written; after that it passes to the integrator, and
an extension of it is a small commit of its own (the plan's §7.2). `SHIP_MODULES` does not name
it, and it has no `build`: the hulls' modules import it.
"""
