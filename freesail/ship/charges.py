"""The service charges of the great guns (package 75; docs/design/Build-Ships.md §3.1 item 15,
§10): the Regulations and Instructions of 1806 (the 1808 printing), Table No. 29, the
service charges of cylinder powder for one shot by the gun's kind and calibre. Its title is
in the OCR (`docs/references/admiralty/regulations-and-instructions-1808-ocr.txt:27498-27502`)
and its figures are not; they are read from the page image and entered here by package 75's
shared work SW-1, with the page cited beside them.

`freesail.ship.parts.charge_lb` gives the table's figure where it has one and its kind's
share of the shot (`parts.CHARGE_SHARE`) where it has none. Empty, as it stands, it changes
nothing.
"""

from __future__ import annotations

# A cartridge's powder in pounds by (the gun's kind, its calibre in pounds), as
# `schema.GUN_KINDS` names the kind: ("long", 32.0), ("carronade", 12.0).
CHARGE_TABLE_LB: dict[tuple[str, float], float] = {}
