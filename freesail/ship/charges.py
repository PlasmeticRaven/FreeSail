"""The service charges of the great guns (package 75; docs/design/Build-Ships.md §3.1 item 15,
§10): the Regulations and Instructions of 1806 (the 1808 printing), Table No. 29, "A Table
shewing the quantities of Gunpowder to be used with different natures of Ordnance", its
service column with one shot: cylinder powder for one shot by the gun's kind and calibre.
Its title is in the OCR
(`docs/references/admiralty/regulations-and-instructions-1808-ocr.txt:27498-27502`) and its
figures are not; they were read on the page image (the Internet Archive's b22017033_0001,
leaf n533: Research-Indefatigable-2026-10.md §6.4, Build-Ships.md §10) and entered here by
package 75's shared work SW-1.

The table confirms the shares `freesail.ship.parts.CHARGE_SHARE` gave from memory: its
column heads the guns' one shot "being 1/3 the weight of one shot", and each of its figures
is a third of the shot for a gun and a twelfth for a carronade, rounded down to the ounce.
Where the share rounds to the nearest ounce it gives an ounce more: the long 32-pounder
10 lb 11 oz (the table's 10 lb 10 oz), the long 2-pounder 11 oz (10 oz), the 68-pounder
carronade 5 lb 11 oz (5 lb 10 oz), the 32-pounder carronade 2 lb 11 oz (2 lb 10 oz) and
the long half-pounder 3 oz (2 oz). The table's half-pounder, the last of its guns, is the
game's swivel: 2 oz, where the swivel's half (a judgement) gives 4. The guns' row names no
mount, so its two least, the 1-pounder and the half-pounder, are entered for the long gun
and the swivel both (the swivel of a pound 5 oz, where its half gives 8).

`freesail.ship.parts.charge_lb` gives the table's figure where it has one, and its kind's
share of the shot to the nearest ounce where the table names no such gun (a French 36 or
8, a swivel above a pound). The eight ship files of the packages before 75 keep the
charges they were filed with, the shares, by the lead's rule (the stage 0 read of
2026-10-28, item 1, docs/dev/M7-WorkPackages.md: where a figure of the eight would move, the
table serves the new ships alone, "read only where a file asks", and the eight's charges
stay as filed until a package of their own re-measures them); `tools/gen_ships.py`'s
`fit_magazine(..., as_filed=True)` writes them so. The magazine and the viewer's plume read a
gun's charge from its fit (`parts.filed_charge_lb`), and a fit without charges, an old
save's from before practice and resupply and so one of the eight, takes the shares as filed:
the table reaches a fit only through its file.

Left out (Build-Ships.md §10): the table's charges with two shots (a double-shotted round
draws one service cartridge, `parts.py`), for salutes and scaling, and its advice to
restrain two shots in guns after twenty rounds. Each changes the gunnery's cycle, package
77's.
"""

from __future__ import annotations

# A cartridge's powder in pounds by (the gun's kind, its calibre in pounds), as
# `schema.GUN_KINDS` names the kind. The table as printed, pounds and ounces:
#   guns, one shot: 42-pdr 14 0, 32 10 10, 24 8 0, 18 6 0, 12 4 0, 9 3 0, 6 2 0, 4 1 5,
#     3 1 0, 2 0 10, 1 0 5, 1/2 0 2;
#   carronades: 68-pdr 5 10, 42 3 8, 32 2 10, 24 2 0, 18 1 8, 12 1 0.
CHARGE_TABLE_LB: dict[tuple[str, float], float] = {
    ("long", 42.0): 14.0,
    ("long", 32.0): 10.0 + 10 / 16,
    ("long", 24.0): 8.0,
    ("long", 18.0): 6.0,
    ("long", 12.0): 4.0,
    ("long", 9.0): 3.0,
    ("long", 6.0): 2.0,
    ("long", 4.0): 1.0 + 5 / 16,
    ("long", 3.0): 1.0,
    ("long", 2.0): 10 / 16,
    ("long", 1.0): 5 / 16,
    # the table's half-pounder, the last of its guns: the game's half-pounder is a swivel
    ("swivel", 0.5): 2 / 16,
    # the guns' row names no mount, so its two least calibres serve the swivel and the long
    # gun both, a swivel of a pound and a long half-pounder, though no file carries either
    # (judgement); a swivel above a pound, which the game has none of, keeps its half
    ("swivel", 1.0): 5 / 16,
    ("long", 0.5): 2 / 16,
    ("carronade", 68.0): 5.0 + 10 / 16,
    ("carronade", 42.0): 3.0 + 8 / 16,
    ("carronade", 32.0): 2.0 + 10 / 16,
    ("carronade", 24.0): 2.0,
    ("carronade", 18.0): 1.0 + 8 / 16,
    ("carronade", 12.0): 1.0,
}
