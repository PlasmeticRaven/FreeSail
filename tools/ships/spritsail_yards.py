"""The spritsail yard under the bowsprit and the sprit-topsail yard under the jib-boom, with
their square sails (package 75; docs/design/Design-ShipsEngineExtensions.md, cited here as Ext,
§4.1). Written by the 64's builder (B1) and imported by the 74's and the bilander's.

Pure: numbers in, dicts out, importing nothing from the generator (Ext §9.3). Every height is
metres above the ship's own water and every x metres forward of the middle of her load line, in
the ship module's frame; the ship module writes the heights above its datum, rates the yards and
the lines through `gen_ships` (`square_sail_lines`, the guys) and files them. Each cut raises
`ValueError` with a sentence where what it writes would break the contract (Ext §9.3): each
yard below its spar's line at its station, the sprit-topsail yard above the spritsail yard, and
every foot above the water at no heel.

The cut, on the line the file's bowsprit and jib-boom have (the bowsprit from its root at the
stem head along its steeve, the jib-boom on along it from the bowsprit's end):
- **The spritsail yard** slung under the bowsprit near the cap (Steel 1794 vol. I pp. 196-197:
  its slings over the bowsprit, its halyards from the cap; Lavery 1985 I30), at `station` of
  the bowsprit's outboard part from the root and `hang` below the spar's line (judgement, both).
- **The spritsail** hangs from it, square, its foot clear of the water.
- **The sprit-topsail yard** hangs under the jib-boom (Steel p. 197: its parral over the
  jib-boom, its halyard from a block under the boom's outer part) where the sail's depth from
  the spritsail yard, on whose arms its foot is spread (Steel, SPRITSAIL TOPSAIL), is Steel's
  depth: so the spars hold the sail as the table cuts it, the yard falling near the jib-boom's
  end, `hang` below its line.
"""

from __future__ import annotations

import math

FOOT_M = 0.3048
YARD_M = 3.0 * FOOT_M
CLOTH_M = 22.5 / 12.0 * FOOT_M  # Steel's cloth in the sail, as `mizen_yard.CLOTH_M`
# The viewer's spread of the clews on the yard below (`client/projection.js`, CLEW_SPREAD), for
# the figures of the drawn sail reported beside the cut (Ext §6.2 as built).
CLEW_SPREAD = 0.9


def square_area(head_cloths, foot_cloths, depth_yd, cloth_m=CLOTH_M):
    """Steel's rule for a square sail's canvas: the mean of the cloths at the head and the foot
    by the depth (Steel 1794 vol. I, SPRITSAIL TOPSAIL's rule), square metres."""
    return 0.5 * (head_cloths + foot_cloths) * cloth_m * depth_yd * YARD_M


def cut(
    *,
    root,
    steeve_deg,
    bowsprit_out_m,
    jib_out_m,
    spritsail,
    sprit_topsail=None,
    station=0.85,
    hang=0.8,
    topsail_hang=0.5,
    cloth_m=CLOTH_M,
):
    """The yards under the bowsprit and their sails. `root` is the bowsprit's root (x, z), at
    the stem head; `bowsprit_out_m` and `jib_out_m` the outboard lengths along `steeve_deg`.
    `spritsail` and `sprit_topsail` are each {"yard_m", "head_cloths", "foot_cloths",
    "depth_yd"} (Steel's table IV and p. 49); `sprit_topsail` None for a ship that crosses no
    sprit-topsail yard. Returns, for each yard, its slings (x, z) and length, and for each sail
    its area by Steel's rule, its centre (x, z) and its foot's height; for the sprit topsail the
    slant between the yards (its depth) and the gap between their heights."""
    c, s = math.cos(math.radians(steeve_deg)), math.sin(math.radians(steeve_deg))

    def on_bowsprit(d):
        return root[0] + d * c, root[1] + d * s

    end = on_bowsprit(bowsprit_out_m)

    def on_jib_boom(d):
        return end[0] + d * c, end[1] + d * s

    sx, sz_line = on_bowsprit(station * bowsprit_out_m)
    sz = sz_line - hang
    depth = spritsail["depth_yd"] * YARD_M
    ss_area = square_area(
        spritsail["head_cloths"], spritsail["foot_cloths"], spritsail["depth_yd"], cloth_m
    )
    if spritsail["head_cloths"] * cloth_m > spritsail["yard_m"]:
        raise ValueError("the spritsail's head is wider than its yard.")
    if sz >= sz_line:
        raise ValueError("the spritsail yard is not below the bowsprit's line at its station.")
    if sz - depth <= 0.0:
        raise ValueError(
            f"the spritsail's foot stands {sz - depth:.2f} m above the water at no heel: its "
            "yard must stand higher under the bowsprit."
        )
    out = {
        "end": end,
        "jib_end": on_jib_boom(jib_out_m),
        "spritsail.yard": {"x": sx, "z": sz, "length_m": spritsail["yard_m"], "line_z": sz_line},
        "spritsail": {
            "area": ss_area,
            "x": sx,
            "centre": sz - 0.5 * depth,
            "foot_z": sz - depth,
            "depth": depth,
        },
    }
    if sprit_topsail is None:
        return out
    # the sprit-topsail yard where its sail's depth from the spritsail yard is Steel's: the
    # distance from the slings below to a point `topsail_hang` under the jib-boom's line grows
    # along the boom, so it is found by halving
    want = sprit_topsail["depth_yd"] * YARD_M

    def at(d):
        x, z = on_jib_boom(d)
        return x, z - topsail_hang

    def slant(d):
        x, z = at(d)
        return math.hypot(x - sx, z - sz)

    if slant(jib_out_m) < want:
        raise ValueError(
            f"the jib-boom's end stands {slant(jib_out_m):.2f} m from the spritsail yard, short "
            f"of the sprit topsail's depth ({want:.2f} m)."
        )
    lo, hi = 0.0, jib_out_m
    if slant(lo) > want:
        raise ValueError("the sprit topsail's depth falls inside the bowsprit's cap.")
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        if slant(mid) < want:
            lo = mid
        else:
            hi = mid
    tx, tz = at(hi)
    if tz <= sz:
        raise ValueError("the sprit-topsail yard is not above the spritsail yard.")
    if sprit_topsail["head_cloths"] * cloth_m > sprit_topsail["yard_m"]:
        raise ValueError("the sprit topsail's head is wider than its yard.")
    head_m = sprit_topsail["head_cloths"] * cloth_m
    foot_m = sprit_topsail["foot_cloths"] * cloth_m
    st_area = square_area(
        sprit_topsail["head_cloths"],
        sprit_topsail["foot_cloths"],
        sprit_topsail["depth_yd"],
        cloth_m,
    )
    # the trapezoid's centroid from its foot on the spritsail yard toward its head
    up = (2.0 * head_m + foot_m) / (3.0 * (head_m + foot_m))
    out["sprit_topsail.yard"] = {
        "x": tx,
        "z": tz,
        "length_m": sprit_topsail["yard_m"],
        "station": hi / jib_out_m,
    }
    out["sprit_topsail"] = {
        "area": st_area,
        "x": sx + up * (tx - sx),
        "centre": sz + up * (tz - sz),
        "foot_z": sz,
        "slant": math.hypot(tx - sx, tz - sz),
        "gap": tz - sz,
    }
    return out


def drawn_by_slant(area, top_yard_m, foot_yard_m, slant):
    """The viewer's sprit topsail (`client/projection.js`, `squareCut`, Ext §6.2 as built): its
    foot at the clew spread of the yard below, its head what the file's area leaves along the
    slant between the two yards, within half its yard and the whole. Fed the file's rounded
    figures, it gives what is drawn. Returns (head, foot), metres."""
    foot = CLEW_SPREAD * foot_yard_m
    head = min(max(2.0 * area / slant - foot, 0.5 * top_yard_m), top_yard_m)
    return head, foot
