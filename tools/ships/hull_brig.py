"""The *Diligence* class's hull as drawn: one hull in two roles, the brig and the merchant brig
(package 75's hull step, SW-2 with SW-2b.2; docs/design/Build-Ships.md §5.0 principle 10, §5.7,
§5.9). Rung S throughout: her class's own lines, Henslow's design of 1795, measured at full size
on RMG ZAZ4491 (the sheer draught, body plan and half-breadth) and ZAZ4492 (the inboard profile
and the decks), both stamped *Harpy*, read and cited and never copied
(docs/design/ships-design/pages-zaz4491.md, the note below; §6 its points, as here).

Every table is the note's §6.2, to the centimetre:
- x forward of the mid-perpendiculars, 47 ft 6 in forward of AP;
- z above WL1, the top green waterline, at each station, as the load line: the lead's ruling of
  2026-10-31 on the note's judgement, no line being labelled, and the faint ruled grey line just
  above it on ZAZ4491 alone recorded and not taken (the note's §4.1, §4.2);
- half-breadths with 3 in of plank, the difference of the table's breadths moulded and extreme.

Drawn only (§5.0 principle 8, §5.6). Nothing the physics or the gunnery reads is taken from here:
the brig's hull figures, spars, sails and guns' x are her file's, and a difference between the
sheet and the file is recorded, not moved. A gun's `height_m` is its port's sill and its `deck`
its deck (§5.3): nothing reads either until SW-5 L2.

`profile_into` is the one call for the hull, from `gen_ships.brig`; `sill_m` the one for a gun's
height, from `brig_armament` and `merchant_brig_armament`. Imported by `gen_ships.brig` with
`gen_ships` the running script, as a ship's module is (tools/ships/__init__.py). It is no ship's
module and writes no file: the two files are the generator's.
"""

from __future__ import annotations

import sys

import gen_ships as g

from freesail.ship.profile import interp

# The top of the side (§5.2, §5.6), taffrail to the rail's moulded end at the stem head, ±0.05 ft.
RAIL = [
    (-16.47, 3.68), (-15.90, 3.51), (-15.54, 3.45), (-14.93, 3.38), (-14.48, 3.33),
    (-12.84, 3.16), (-12.19, 3.10), (-10.89, 2.98), (-9.61, 2.88), (-8.34, 2.80),
    (-7.04, 2.72), (-5.76, 2.66), (-4.49, 2.61), (-3.19, 2.57), (-1.92, 2.55), (-0.64, 2.54),
    (0.65, 2.55), (1.82, 2.57), (2.98, 2.59), (4.26, 2.64), (5.54, 2.70), (6.81, 2.77),
    (8.09, 2.86), (9.38, 2.96), (10.65, 3.09), (11.93, 3.23), (13.21, 3.39), (13.68, 3.46),
    (14.14, 3.52), (14.59, 3.58), (14.97, 3.64),
]  # fmt: skip
# By station: the half-breadth at WL1 and at the rail, the plan's top-timber line (§5.10), ±0.03 ft
# between 16 and K, ±0.1 ft at the ends; the two end points where the waterline meets the rabbets.
BREADTH = [
    (-13.99, 0.31, 2.84), (-12.84, 1.37, 3.07), (-12.19, 1.93, 3.19), (-10.89, 2.78, 3.39),
    (-9.61, 3.24, 3.56), (-8.34, 3.52, 3.70), (-7.04, 3.72, 3.82), (-5.76, 3.85, 3.92),
    (-4.49, 3.95, 4.00), (-3.19, 4.02, 4.07), (-1.92, 4.07, 4.11), (-0.64, 4.10, 4.13),
    (0.65, 4.12, 4.15), (1.82, 4.12, 4.16), (2.98, 4.11, 4.15), (4.26, 4.07, 4.13),
    (5.54, 3.98, 4.09), (6.81, 3.82, 4.02), (8.09, 3.57, 3.90), (9.38, 3.21, 3.72),
    (10.65, 2.68, 3.40), (11.93, 1.92, 2.95), (13.21, 0.93, 2.22), (14.01, 0.22, 1.48),
]  # fmt: skip
# K, the false keel's lower edge, the heel at the post to the knee's foot (§5.4). That the strip's
# heavy upper border is K is judgement: no other line is drawn there, and the post and the knee end
# on it. It draws 3.11 ft of drag against WL1 (§4.3).
KEEL = [
    (-13.08, -3.86), (12.21, -3.03),
]  # fmt: skip
# The stem's fore edge, its foot boxed into the keel to the stem head (§5.5), ±0.05 ft.
STEM = [
    (11.19, -2.72), (11.55, -2.60), (12.13, -2.34), (12.65, -2.02), (13.05, -1.70),
    (13.37, -1.39), (13.64, -1.07), (13.86, -0.76), (14.05, -0.45), (14.20, -0.14),
    (14.26, -0.01), (14.33, 0.17), (14.44, 0.47), (14.54, 0.78), (14.63, 1.09), (14.71, 1.40),
    (14.78, 1.70), (14.84, 2.01), (14.87, 2.16), (14.90, 2.32), (14.95, 2.56), (14.98, 2.74),
    (15.01, 2.93), (15.04, 3.08), (15.06, 3.23), (15.08, 3.36), (15.10, 3.44),
]  # fmt: skip
# The post's after edge, the counter and the transom's face to the taffrail at the middle line
# (§5.6), ±0.1 ft.
STERN = [
    (-13.08, -3.86), (-13.60, -2.24), (-13.80, -1.63), (-13.99, -1.03), (-14.19, -0.43),
    (-14.34, 0.02), (-14.48, 0.48), (-14.68, 1.08), (-14.77, 1.38), (-14.83, 1.59),
    (-14.90, 1.65), (-15.40, 1.90), (-15.89, 2.10), (-15.96, 2.20), (-15.95, 2.41),
    (-16.01, 2.56), (-16.06, 2.71), (-16.12, 2.86), (-16.17, 3.01), (-16.23, 3.16),
    (-16.28, 3.31), (-16.33, 3.46), (-16.40, 3.58), (-16.47, 3.68),
]  # fmt: skip
# The wale's edges, from where it runs out at the counter to the stem (§5.2), ±0.05 ft.
WALES = [
    (-14.21, 1.10, 1.75), (-12.84, 0.96, 1.60), (-12.19, 0.90, 1.54), (-10.89, 0.78, 1.42),
    (-9.61, 0.68, 1.32), (-8.34, 0.59, 1.23), (-7.04, 0.51, 1.15), (-5.76, 0.45, 1.09),
    (-4.49, 0.40, 1.04), (-3.19, 0.36, 1.00), (-1.92, 0.34, 0.98), (-0.64, 0.33, 0.97),
    (0.65, 0.34, 0.98), (1.82, 0.35, 0.99), (2.98, 0.38, 1.01), (4.26, 0.42, 1.05),
    (5.54, 0.47, 1.11), (6.81, 0.54, 1.18), (8.09, 0.62, 1.26), (9.38, 0.73, 1.37),
    (10.65, 0.85, 1.49), (11.93, 0.99, 1.63), (13.21, 1.15, 1.78), (13.98, 1.25, 1.90),
    (14.29, 1.29, 1.94),
]  # fmt: skip
# The dead flat's section, ⊗ on the body plan (§5.11), its keel's half-siding at the rabbet.
SECTION = [
    (-2.89, 0.18), (-2.73, 0.39), (-2.58, 0.67), (-2.28, 1.36), (-1.97, 2.12), (-1.67, 2.75),
    (-1.36, 3.20), (-1.06, 3.53), (-0.75, 3.77), (-0.45, 3.96), (-0.14, 4.09), (0.16, 4.19),
    (0.47, 4.25), (0.77, 4.27), (0.86, 4.26), (1.08, 4.27), (1.38, 4.27), (1.69, 4.25),
    (1.99, 4.22), (2.29, 4.19), (2.57, 4.16),
]  # fmt: skip
# The deck at side, the third red line and 3 in of plank (§5.1, §5.3): the sheets name no line, so
# the identification is judgement, on the Raven's plank and round (Steel 1805 pp. lix-lx) and the
# 16-in sill. Flush from the counter to the stem: no quarterdeck or forecastle.
DECK = [
    (-14.69, 1.67), (-14.48, 1.67), (-12.84, 1.55), (-12.19, 1.51), (-10.89, 1.44),
    (-9.61, 1.37), (-8.34, 1.31), (-7.04, 1.27), (-5.76, 1.23), (-4.49, 1.19), (-3.19, 1.17),
    (-1.92, 1.16), (-0.64, 1.15), (0.65, 1.16), (1.82, 1.18), (2.98, 1.19), (4.26, 1.22),
    (5.54, 1.26), (6.81, 1.31), (8.09, 1.37), (9.38, 1.44), (10.65, 1.52), (11.93, 1.61),
    (13.21, 1.71), (14.48, 1.87),
]  # fmt: skip
# The ten ports a side as the sheet draws them, aft to forward (§5.7): centre ±0.03 ft, sill above
# WL1 ±0.05 ft, half-breadth at the sill between the stations either side on the body plan with 3
# in of plank, ±0.1 ft.
SHEET_PORTS = [
    (-11.55, 1.89, 3.40), (-8.98, 1.76, 3.73), (-6.41, 1.66, 3.97), (-3.84, 1.60, 4.13),
    (-1.28, 1.57, 4.21), (1.29, 1.58, 4.25), (3.90, 1.62, 4.21), (6.46, 1.70, 4.14),
    (9.00, 1.83, 3.83), (11.57, 1.99, 3.05),
]  # fmt: skip
# Their size, the mean of the ten (§5.7): 2 ft 9 in by 2 ft 4 in.
PORT_SIZE = (0.84, 0.70)
# The guns stand where the file has them and never move (§5.3), and a port gun stands on a triple
# of its deck (§5.1; truth 7-185), so a port with a gun in it is written at that gun's x, its sill
# and half-breadth read along the sheet's own ports there. These are `brig_armament`'s x_m, by port
# (the eight within 0.12 m of the sheet's; which gun stands in which port is judgement, the nearest,
# the note's §5.7), and `merchant_brig_armament`'s by the brig's (within 0.16 m). Port 1 holds no
# gun in either file and stays at the sheet's x. `sill_m` raises for a gun on no triple.
GUNS_BY_PORT = {2: -9.1, 3: -6.5, 4: -3.9, 5: -1.3, 6: 1.3, 7: 3.9, 8: 6.5, 9: 9.1}
MERCHANT_GUNS_BY_PORT = {4: -4.0, 7: 4.0}
# The chase port: the file's gun at +12.0, the sheet's port 10 at +11.57, the gun on its fore edge
# (a chaser's port is a triple at the chaser's x: §5.1). Beyond the sheet's last port, so read off
# the lines (judgement): the sill the deck's rise above port 10's, every sill standing 1 ft 4 in
# above the deck at side (§5.7); the half-breadth on the body plan at that height, between Q and S
# (§5.11), with the plank.
CHASE_PORT = (12.0, 2.02, 2.87)
# The knee of the head's fore edge, leaving K to the top of the scroll (§5.5), ±0.05 ft.
HEAD = [
    (12.21, -3.03), (12.50, -2.94), (12.81, -2.77), (13.01, -2.62), (13.30, -2.30),
    (13.52, -1.99), (13.72, -1.68), (13.90, -1.37), (14.07, -1.06), (14.24, -0.75),
    (14.42, -0.44), (14.68, 0.01), (15.00, 0.49), (15.37, 0.96), (15.87, 1.43), (16.31, 1.75),
    (16.70, 2.07), (16.95, 2.38), (17.08, 3.06), (17.18, 3.58), (16.95, 3.77),
]  # fmt: skip
# The main breadth: the height of breadth by station, the plan's main half-breadth (§5.2, §5.10),
# from section 23 to the hawse holes. Its two points abaft the post at the water (the note's §6.3)
# are left out: a station there would be drawn down to the water (`form.py`'s `_station_xs`, every
# x of this line a station), a box abaft the post where the sheet has the counter over the rudder.
BREADTH_LINE = [
    (-12.84, 1.48, 3.20), (-12.19, 1.42, 3.31),
    (-10.89, 1.24, 3.51), (-9.61, 1.11, 3.67), (-8.34, 1.00, 3.81), (-7.04, 0.92, 3.93),
    (-5.76, 0.85, 4.03), (-4.49, 0.81, 4.11), (-3.19, 0.79, 4.17), (-1.92, 0.78, 4.22),
    (-0.64, 0.79, 4.24), (0.65, 0.82, 4.25), (1.82, 0.86, 4.26), (2.98, 0.90, 4.25),
    (4.26, 0.96, 4.23), (5.54, 1.06, 4.18), (6.81, 1.21, 4.08), (8.09, 1.35, 3.94),
    (9.38, 1.55, 3.72), (10.65, 1.79, 3.39), (11.93, 2.09, 2.90), (13.21, 2.45, 2.14),
    (13.98, 2.71, 1.40),
]  # fmt: skip
# The rabbet line and the stem's (§5.4, §5.5): kept and not drawn. Half-sidings read at two places,
# 0.34 ft at ⊗ and 0.48 ft on the stem, and taken so along each (judgement).
RABBET = [
    (-12.78, -3.36, 0.10), (-10.89, -3.31, 0.10), (-5.76, -3.14, 0.10), (-0.64, -2.97, 0.10),
    (1.82, -2.89, 0.10), (4.26, -2.81, 0.10), (6.81, -2.72, 0.10), (9.38, -2.64, 0.10),
    (10.73, -2.59, 0.10), (11.56, -2.36, 0.15), (12.21, -2.03, 0.15), (12.68, -1.71, 0.15),
    (13.04, -1.40, 0.15), (13.33, -1.08, 0.15), (13.58, -0.77, 0.15), (13.78, -0.46, 0.15),
    (13.95, -0.15, 0.15), (14.01, -0.01, 0.15), (14.21, 0.47, 0.15), (14.39, 1.08, 0.15),
    (14.55, 1.70, 0.15), (14.71, 2.39, 0.15), (14.79, 2.94, 0.15), (14.86, 3.39, 0.15),
]  # fmt: skip
# By station, aft to forward: 0.5 to 3 ft above the rabbet off the body plan where they stand below
# WL4 (§5.11), then WL4, WL3, WL2 and WL1 off the half-breadth plan at the sheer's heights (§5.10),
# at 23 and 22 with the body plan's two whole-foot levels between WL2 and WL1, the run's hollow
# (§6.1: without them the drawn side missed it by up to 0.11 m); then at 23 to 18 and H to S, where
# the height of breadth stands over 3 ft 6 in above WL1, the body plan's whole-foot levels up to it
# (§6.1: without them the drawn side missed it by up to 0.56 m); then the main breadth and the rail.
# Stations 2 and B come off the plan alone: the body plan draws neither. S, with no WL3 or WL4,
# starts from its lowest cell of §5.11, 5 ft: just under it her line ends on the stem's rabbet.
SECTIONS = [
    # 23
    (-12.84, [(-3.22, 0.15), (-3.07, 0.15), (-2.76, 0.15), (-2.18, 0.16), (-1.45, 0.25),
        (-0.73, 0.46), (-0.63, 0.53), (-0.32, 0.86), (0.00, 1.37), (0.29, 2.09), (0.59, 2.71),
        (0.90, 3.02), (1.20, 3.16), (1.48, 3.20), (3.16, 3.07)]),
    # 22
    (-12.19, [(-3.20, 0.17), (-3.04, 0.18), (-2.74, 0.20), (-2.18, 0.22), (-1.45, 0.39),
        (-0.73, 0.76), (-0.61, 0.91), (-0.30, 1.37), (0.00, 1.93), (0.31, 2.62), (0.61, 3.01),
        (0.92, 3.20), (1.22, 3.29), (1.42, 3.31), (3.10, 3.19)]),
    # 20
    (-10.89, [(-3.15, 0.18), (-3.00, 0.20), (-2.70, 0.24), (-2.39, 0.31), (-2.18, 0.37),
        (-1.45, 0.73), (-0.73, 1.48), (0.00, 2.78), (0.35, 3.21), (0.66, 3.39), (0.96, 3.48),
        (1.24, 3.51), (2.98, 3.39)]),
    # 18
    (-9.61, [(-2.18, 0.55), (-1.45, 1.15), (-0.73, 2.17), (0.00, 3.24), (0.39, 3.50),
        (0.70, 3.62), (1.00, 3.67), (1.11, 3.67), (2.88, 3.56)]),
    # 16
    (-8.34, [(-3.07, 0.21), (-2.92, 0.26), (-2.61, 0.42), (-2.31, 0.64), (-2.18, 0.76),
        (-1.45, 1.63), (-0.73, 2.71), (0.00, 3.52), (1.00, 3.81), (2.80, 3.70)]),
    # 14
    (-7.04, [(-2.18, 0.98), (-1.45, 2.07), (-0.73, 3.09), (0.00, 3.72), (0.92, 3.93),
        (2.72, 3.82)]),
    # 12
    (-5.76, [(-2.83, 0.37), (-2.53, 0.71), (-2.18, 1.20), (-1.45, 2.43), (-0.73, 3.35),
        (0.00, 3.85), (0.85, 4.03), (2.66, 3.92)]),
    # 10
    (-4.49, [(-2.79, 0.43), (-2.49, 0.89), (-2.18, 1.40), (-1.45, 2.69), (-0.73, 3.53),
        (0.00, 3.95), (0.81, 4.11), (2.61, 4.00)]),
    # 8
    (-3.19, [(-2.75, 0.51), (-2.44, 1.03), (-2.17, 1.55), (-1.45, 2.87), (-0.73, 3.64),
        (0.00, 4.02), (0.79, 4.17), (2.57, 4.07)]),
    # 6
    (-1.92, [(-2.71, 0.58), (-2.40, 1.17), (-2.17, 1.62), (-1.45, 2.98), (-0.73, 3.71),
        (0.00, 4.07), (0.78, 4.22), (2.55, 4.11)]),
    # 4
    (-0.64, [(-2.66, 0.63), (-2.36, 1.27), (-2.17, 1.65), (-1.45, 3.04), (-0.73, 3.75),
        (0.00, 4.10), (0.79, 4.24), (2.54, 4.13)]),
    # 2
    (0.65, [(-2.17, 1.66), (-1.45, 3.07), (-0.73, 3.76), (0.00, 4.12), (0.82, 4.25),
        (2.55, 4.15)]),
    # ⊗
    (1.82, [(-2.73, 0.39), (-2.58, 0.67), (-2.17, 1.63), (-1.45, 3.05), (-0.73, 3.75),
        (0.00, 4.12), (0.86, 4.26), (2.57, 4.16)]),
    # B
    (2.98, [(-2.17, 1.56), (-1.45, 2.98), (-0.73, 3.73), (0.00, 4.11), (0.90, 4.25),
        (2.59, 4.15)]),
    # D
    (4.26, [(-2.17, 1.41), (-1.45, 2.85), (-0.73, 3.66), (0.00, 4.07), (0.96, 4.23),
        (2.64, 4.13)]),
    # F
    (5.54, [(-2.46, 0.61), (-2.17, 1.21), (-1.45, 2.65), (-0.73, 3.52), (0.00, 3.98),
        (1.06, 4.18), (2.70, 4.09)]),
    # H
    (6.81, [(-2.57, 0.33), (-2.42, 0.56), (-2.17, 0.97), (-1.45, 2.36), (-0.73, 3.29),
        (0.00, 3.82), (0.33, 3.98), (0.63, 4.07), (0.94, 4.11), (1.21, 4.08), (2.77, 4.02)]),
    # K
    (8.09, [(-2.38, 0.49), (-2.17, 0.74), (-1.45, 2.00), (-0.73, 2.97), (0.00, 3.57),
        (0.37, 3.80), (0.67, 3.89), (0.98, 3.95), (1.35, 3.94), (2.86, 3.90)]),
    # M
    (9.38, [(-2.49, 0.25), (-2.33, 0.40), (-2.16, 0.53), (-1.45, 1.57), (-0.72, 2.52),
        (0.00, 3.21), (0.11, 3.32), (0.41, 3.49), (0.72, 3.61), (1.02, 3.69), (1.33, 3.74),
        (1.55, 3.72), (2.96, 3.72)]),
    # O
    (10.65, [(-2.29, 0.29), (-2.17, 0.34), (-1.45, 1.10), (-0.73, 1.94), (0.00, 2.68),
        (0.15, 2.83), (0.45, 3.03), (0.76, 3.19), (1.06, 3.30), (1.37, 3.37), (1.67, 3.41),
        (1.79, 3.39), (3.09, 3.40)]),
    # Q
    (11.93, [(-2.16, 0.18), (-1.45, 0.60), (-0.73, 1.24), (0.00, 1.92), (0.19, 2.10),
        (0.49, 2.34), (0.80, 2.54), (1.10, 2.69), (1.41, 2.80), (1.71, 2.87), (2.09, 2.90),
        (3.23, 2.95)]),
    # S
    (13.21, [(-0.99, 0.28), (-0.72, 0.45), (0.00, 0.93), (0.23, 1.12), (0.54, 1.33),
        (0.84, 1.53), (1.15, 1.72), (1.45, 1.88), (1.76, 2.00), (2.06, 2.07), (2.45, 2.14),
        (3.39, 2.22)]),
]  # fmt: skip

# §5.0 principles 3 and 4: the rung of each line, its word its weakest point's; S throughout, the
# class's own lines, and `judged` where a line's weak point is reasoning on those lines.
MARKS = {
    "rail_m": "sourced",
    "breadth_m": "sourced",
    "keel_m": "judged",  # that the strip's border is K
    "stem_m": "sourced",
    "stern_m": "sourced",
    "wales_m": "sourced",
    "section_m": "sourced",
    "decks_m": "judged",  # which red line is the deck at side, the plank added
    "ports_m": "judged",  # the half-breadths at the sills; a gun's port at the gun's x
    "port_size_m": "sourced",
    "head_m": "sourced",
    "breadth_line_m": "sourced",
    "sections_m": "sourced",
    "rabbet_m": "judged",  # the half-sidings between their two places
    "form.stern": "sourced",
    "form.stern.knuckle_z_m": "sourced",
    "form.stern.transom_hb_m": "sourced",
    "form.stern.round_up_m": "sourced",
    "form.head": "sourced",
}
# Her form (the note's §5.6). The knuckle is the wing transom's ends, its crown rounded up 5 in
# above them; the transom's half-breadths the moulded taffrail's and the knuckle's, each with the
# plank. No fullness: the ends are drawn through her waterlines. No galleries (read). No
# `lights_m`: the sheet's two stern ports are ports, package 81's, and the only openings on the
# stern board (Build-Ships.md §5.7's "no galleries or lights" stands as read).
FORM = {
    "stern": {
        "type": "square",
        "knuckle_z_m": 0.99,
        "transom_hb_m": [2.33, 2.93],
        "round_up_m": 0.13,
    },
    "head": "scroll",
}
# The hull's keys the sheets disagree with, recorded, not moved (§5.0 principle 8; the note's
# §7), each said after the note the generator gives the key.
RECORDED = {
    "beam_m": (
        "Recorded, not moved: her class's draught gives 28 ft 0 in extreme, 27 ft 6 in moulded "
        "(ZAZ4491)."
    ),
    "length_waterline_m": "Recorded, not moved: her class's WL1 (ZAZ4491; the note's §7).",
    "draught_m": (
        "Recorded, not moved: her class's drag and depth to K (ZAZ4491; the note's §4.3, §7; 3 ft "
        "2 in of drag on the sisters' ZAZ4320 and ZAZ4262). Harpy's as-built 7 ft 3 in forward and "
        "10 ft 10 in aft, 3 ft 7 in of drag (Winfield p. 256), fall near WL2, 2 ft 2 in lighter, "
        "in a state not said."
    ),
    "deck_height_m": "Recorded, not moved: her class's deck (ZAZ4491; the note's §5.3, §7).",
}


def port_triples(merchant=False):
    """The file's ports, [x, sill, half-breadth] from aft forward: the sheet's ten, each with a
    gun in it at that gun's x (`GUNS_BY_PORT`), the chase gun's by `CHASE_PORT`."""
    guns = {**GUNS_BY_PORT, **(MERCHANT_GUNS_BY_PORT if merchant else {})}
    sills = [(x, sill) for x, sill, _hb in SHEET_PORTS]
    half_breadths = [(x, hb) for x, _sill, hb in SHEET_PORTS]
    out = []
    for number, (x, sill, hb) in enumerate(SHEET_PORTS, start=1):
        if number in guns:
            x = guns[number]
            sill, hb = round(interp(sills, x), 2), round(interp(half_breadths, x), 2)
        out.append([x, sill, hb])
    out[-1] = list(CHASE_PORT)
    return out


def sill_m(x, merchant=False):
    """A port gun's `height_m`: the sill of the triple it stands on (Build-Ships.md §5.3, the
    generator's assertion of truth 7-185), raising for a gun on none."""
    for port_x, sill, _hb in port_triples(merchant):
        if abs(port_x - x) < 0.005:
            return sill
    raise ValueError(f"hull_brig: no port stands at a gun's x {x:g}; a gun's x never moves (§5.3).")


def sections():
    """`SECTIONS` as the profile's points, [x, z, half-breadth], aft to forward."""
    return [[x, z, hb] for x, points in SECTIONS for z, hb in points]


def profile_into(hull, notes, merchant=False):
    """Add her profile, form and marks to the hull mapping as its last key, and her sources,
    departures and judgements to its notes; print the drawn hull's report."""
    hull["profile"] = g.hull_profile(
        RAIL,
        BREADTH,
        keel=KEEL,
        stem=STEM,
        stern=STERN,
        wales=WALES,
        section=SECTION,
        decks={"upper": DECK},
        ports={"upper": port_triples(merchant)},
        port_size={"upper": PORT_SIZE},
        head=HEAD,
        breadth_line=BREADTH_LINE,
        sections=sections(),
        rabbet=RABBET,
    )
    notes.update(profile_notes(merchant))
    for key, words in RECORDED.items():
        notes[key] = f"{notes[key]} {words}"
    # no triple's half-breadth was measured at its port (the note's §5.7: each is read between two
    # stations), so every gap is reported and none raises, as the 64's. The lead's ruling: a figure
    # a rule computes from the file's keys goes in this report and the tests, not in a note.
    report: list[str] = []
    g.hull_form(hull, form=FORM, marks=MARKS, measured=(), report=report)
    name = "merchant brig" if merchant else "brig"
    for line in report:
        print(f"{name}: {line}", file=sys.stderr)


def profile_notes(merchant):
    """Her lines' notes, keyed as `Builder.dump` reads them (`gen_ships.py`, the hull's profile):
    sources, departures and judgements only."""
    notes = {
        "profile": (
            "Her side, decks and ports, her class's own lines (Build-Ships.md §5.7, §5.9): the "
            "Diligence class, Henslow's design of 1795, measured at full size on RMG ZAZ4491 and "
            "ZAZ4492, both stamped Harpy, with Diligence's ZAZ4320 and Hound's ZAZ4262 as checks "
            "(docs/design/ships-design/pages-zaz4491.md). x forward of the mid-perpendiculars, z "
            "above WL1 at each station, half-breadths with 3 in of plank. WL1, the top green "
            "waterline, is taken as her load line by judgement, as the lead ruled: no line is "
            "labelled, and a faint ruled grey line just above it on ZAZ4491 alone is recorded and "
            "not taken (the note's §4.1, §4.2). Her masts stay where the file has them, against "
            "the sheet's -3.96 and +9.62 m; the change made on board Harpy in January 1799 at "
            "Captain Bazely's request, in green on ZAZ4492 (-4.07 and +9.37 m), is noted and not "
            "moved."
        ),
        "profile.rail_m": (
            "The top of the side, from the taffrail at the middle line to the rail's moulded end "
            "at the stem head, measured on ZAZ4491 (±0.05 ft; the note's §5.2, §5.6)."
        ),
        "profile.breadth_m": (
            "By station: the half-breadth at WL1 and at the rail, the plan's top-timber line, "
            "measured on ZAZ4491 (±0.03 ft between 16 and K, ±0.1 ft at the ends; the note's "
            "§5.10), with the plank."
        ),
        "profile.keel_m": (
            "K, the false keel's lower edge, from the post's heel to the knee's foot (the note's "
            "§5.4): the scale strip's heavy upper border, by judgement. Its drag against WL1 is "
            "the sheet's, not the file's 2 ft."
        ),
        "profile.stem_m": (
            "The stem's fore edge from its foot boxed into the keel to the stem head (ZAZ4491, "
            "measured; the note's §5.5)."
        ),
        "profile.stern_m": (
            "The post's after edge, the counter and the transom's face to the taffrail at the "
            "middle line (ZAZ4491, measured, ±0.1 ft; the note's §5.6)."
        ),
        "profile.wales_m": (
            "The wale's two edges, 2 ft 1 in apart at the lowest (ZAZ4491, measured; the note's "
            "§5.1, §5.2)."
        ),
        "profile.section_m": (
            "The dead flat's section, off the body plan (ZAZ4491; the note's §5.11)."
        ),
        "profile.decks_m": (
            "The flush upper deck at side, the third red line and 3 in of plank: the sheets name "
            "no line, so the identification is judgement on measured lines (the note's §5.1)."
        ),
        "profile.ports_m.upper": (
            "Ten a side (read on both sheets). Every sill measured on ZAZ4491, 1 ft 4 in above the "
            "deck at side at every port, as Steel's Raven's 16 in (1805 p. lx), the lowest a few "
            "inches above Steel's four to five feet (p. 124): the sheet, the higher rung, decides. "
            "The half-breadth at the sill is read between the stations on the body plan, with the "
            "plank (judgement on measured lines). A port with a gun in it stands at the gun's x, "
            "which never moves (Build-Ships.md §5.3), the chase port's sill and half-breadth read "
            "off the lines beyond the sheet's last port (judgement); the sheet's own centres are "
            "in the note's §5.7, the differences in its §6.3."
        ),
        "profile.port_size_m": (
            "The mean of the ten, 2 ft 9 in by 2 ft 4 in (ZAZ4491, measured; Steel's Raven's 2 ft "
            "9 in by 2 ft 6 in)."
        ),
        "profile.head_m": (
            "The knee of the head's fore edge from K to the top of the scroll (ZAZ4491, measured; "
            "the note's §5.5)."
        ),
        "profile.breadth_line_m": (
            "The main breadth by station: the sheet's height of breadth at the plan's main "
            "half-breadth (ZAZ4491, measured; the note's §5.2, §5.10), with the plank."
        ),
        "profile.sections_m": (
            "Off the body plan low down, then WL4 to WL1 off the half-breadth plan at the sheer's "
            "heights, at the ends the body plan's whole-foot levels up to the main breadth, and at "
            "23 and 22 between WL2 and WL1, then the main breadth and the rail (ZAZ4491; the "
            "note's §5.10, §5.11, §6.1). Sections 2 and B are not on the body plan, so theirs come "
            "off the plan alone."
        ),
        "profile.rabbet_m": (
            "The rabbet line and the stem's, kept and not drawn (ZAZ4491). The half-sidings are "
            "read at two places and held along each, by judgement."
        ),
        "profile.form": (
            "Her form (Build-Ships.md §5.1): no fullness, the ends drawn through her waterlines; "
            "no floor line, the sheet drawing no rising line."
        ),
        "profile.form.stern": (
            "Square, with a tuck, a counter and a raked transom, plain (ZAZ4491, read and "
            "measured; the note's §5.6): the knuckle the wing transom's ends, rounded up 5 in at "
            "its crown; the half-breadths the moulded taffrail's and the knuckle's, with the "
            "plank. No galleries or lights: the sheet's two stern ports are ports, package 81's."
        ),
        "profile.form.head": "A scroll head (ZAZ4491, read; Steel's Raven, 1805 p. lxv, the same).",
        "profile.marks": (
            "Each line's rung (Build-Ships.md §5.0 principles 3 and 4): S throughout, her class's "
            "own lines; sourced where the line stands as measured, judged where its weakest point "
            "is reasoning on those lines, each said in its note."
        ),
    }
    notes["profile.ports_m.upper"] += (
        " Her hull is the brig's, one class in two roles (Build-Ships.md §5.0 principle 10), so "
        "the ports with no gun of hers stand as the brig's; her own two guns' ports stand at her "
        "guns' x, ±4.0, against the sheet's -3.84 and +3.90."
        if merchant
        else " The fit stays as the file has it, so the aftmost stands empty."
    )
    return notes
