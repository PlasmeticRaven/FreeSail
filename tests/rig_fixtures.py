"""Three rigs for package 75's engine extensions, built in memory from the committed files
(docs/design/Design-ShipsEngineExtensions.md §8 item 7, §17.8): the ships the engine's steps
and the viewer work on before any ship file carries the new keys. None is a ship of the
package; each is a committed file with its new parts cut to the design's contracts, so that
what is built against them is built against the contracts the ship builders write to.

- `frigate_with_mizen_yard()`: `frigate-36.yaml` with her spanker, its gaff and boom (and the
  ringtail on the boom) replaced by a lateen mizen course cut at the mast on a `lateen_yard`
  (Ext §3.4), and a spritsail yard under the bowsprit and a sprit-topsail yard under the
  jib-boom, each with its square sail (Ext §4.1).
- `brig_with_settee()`: `brig.yaml` with her main course, spanker, gaff, boom and storm
  trysail replaced by a settee on a lug yard, cut to D5(a)'s proportions
  (docs/design/Decisions-ShipsRound2-2026-10.md), the dry main yard and the main topsail above
  it kept, and the main mast laid aback to heave to (Ext §5.1, §5.7). It is the scratch
  bilander of Eng §4.4 (docs/design/Research-ShipsEngine-2026-10.md) with that variant's two
  faults corrected: its centre of effort is the corners' centroid above the water, not above
  the deck, and its peak is inside the stern, not abaft it.
- `frigate_with_driver()` (Ext §17.8, the driver's stage 0): the first with the frigate's
  `mizzen.boom` put back, lengthened to the 64's and hung where the 64's driver puts its jaws,
  and the 64's driver boomsail (Steel's, Ext §17.1-§17.2) on its four corners, a lateen cut at
  the mast on the mizen yard and the boom, filed after the course in its place and in the sail
  room, the boom rigged in (Ext §17.11); `bent=True` gives it bent in the course's place, the
  boom rigged out and the course's canvas in the sail room, for the drawing and for the shift
  back. The storm mizzen stays in the course's place, so that the one-place rule has its case;
  the ringtail and its boom stay out, as the 64 carries none (Indf §4.7).

Each `..._doc()` gives the document, fresh at every call, for a test that changes it or
writes it out (`write_ship`, for `make_world`, which reads a path); the three functions above
give the `Ship`. The new parts' figures are the design's where it gives them (the mizen
course is the 64's, by Steel's table) and marked judgement where it does not; the lines'
ratings are those of the lines they stand for in the same file. Nothing here is read by the
game: the tests import it as a helper module beside them.
"""

from __future__ import annotations

import copy
import math
from collections.abc import Callable
from functools import cache
from pathlib import Path
from typing import Any

import yaml

from freesail.ship.graph import Ship
from freesail.ship.loader import ship_from_dict

ROOT = Path(__file__).resolve().parents[1]
SHIPS = ROOT / "data" / "ships"

FT = 0.3048
YD = 0.9144

# -- the mizen course cut at the mast (Ext §2, §3.4) ---------------------------------------

# The 64's mizen course by Steel's sail table, as Ext §2 measures it (22 1/2 in to a cloth):
# the luff 9 1/4 yd and the after leech 17 1/4 yd, the head rising 24 ft over a run of
# 27.2 ft (41 degrees), the foot 8.86 m, about 104 square metres; her yard 77 ft 0 in, about
# 0.53 of it before the mast (Ind §3.1), the head laced along the rest. Hung on the frigate's
# mizzen as it is: the fixture's course is the 64's, not one cut for the frigate.
MIZEN_LUFF_M = 9.25 * YD
MIZEN_LEECH_M = 17.25 * YD
MIZEN_HEAD_RUN_M = 27.2 * FT
MIZEN_HEAD_RISE_M = 24.0 * FT
MIZEN_FOOT_M = 8.86
MIZEN_YARD_M = 77.0 * FT
# The truss (the throat) above the deck: judgement, the foot about 3 m above the deck, clear
# over the quarterdeck, and the yard under the cross-jack yard (15.0 m).
MIZEN_TRUSS_M = 11.5

# -- the yards under the bowsprit (Ext §4.1) ------------------------------------------------

# Each yard's station a fraction of its spar's length out from its heel, "near the cap" of
# the bowsprit and near the jib-boom's end (Steel 1794 vol. I pp. 196-197; Lavery I30), and
# hung so far below the spar's line: the spritsail yard in its slings, the sprit-topsail
# yard on its traveller (judgement, both).
SPRITSAIL_STATION = 0.85
SPRITSAIL_HANG_M = 0.8
SPRIT_TOPSAIL_STATION = 0.85
SPRIT_TOPSAIL_HANG_M = 0.5
# Their lengths: the frigate's fore topsail and fore topgallant yards', 16.4 and 10.5 m, near
# the 64's proportion between the two (57 ft 6 in and 34 ft 6 in, Ext §4.1) (judgement).
# Braced within 30 degrees: their braces lead forward to the fore stay and up to the fore top
# (Lavery I30) (judgement).
SPRIT_BRACE_LIMIT_DEG = 30
# The spritsail hangs to a metre above the water at no heel (Ext §6.2: its foot above the
# water), its area over nine-tenths of its yard as the drawing hangs a sail with no yard
# below it (`client/projection.js`, `squareCut`); the sprit topsail is the trapezoid between
# its yard and the spritsail yard's arms, nine-tenths of each, where its clews are sheeted
# (Falconer 1780, SPRITSAIL-TOPSAIL) (judgement, both).
SPRITSAIL_FOOT_ABOVE_WATER_M = 1.0
SPREAD = 0.9

# -- the settee (D5(a); Ext §5.1) -----------------------------------------------------------

# D5(a), Gwyn's cut (RMG PAG3828, measured: Bil §2.3): the luff 0.16 of the leech, the leech
# and the foot each 0.72 of the head, the yard at 44 degrees, slung a third of the head from
# the throat; the sling on the main mast's raked line at its height (Ext §5.1).
SETTEE_LUFF_OF_LEECH = 0.16
SETTEE_LEECH_OF_HEAD = 0.72
SETTEE_FOOT_OF_HEAD = 0.72
SETTEE_YARD_DEG = 44.0
# The head: judgement, the longest that keeps the peak and the clew about a metre inside the
# brig's stern (her waterline's after end, -13.4 m), as Gwyn's peak is inside the taffrail
# (D5(a)). The tack at the rail under the throat, as the lugger's main lug's is under its
# throat (judgement: Gwyn's yard has its fore end a few feet above the rail; slung so, the
# yard hangs well under the brig's main top, her mast being taller than Gwyn's: D6). The
# yard is as long as the head, as the lugger's are.
SETTEE_HEAD_M = 17.0
SETTEE_TACK_M = 1.0

# -- the driver (Ext §17.2, §17.8) ----------------------------------------------------------

# The 64's driver boomsail as Ext §17.2 cuts it on her geometry (`mend17/driver_four.py`): the
# fore leech 6.98 m down the mast from the course's throat to the boom's jaws, 1.71 m short of
# Steel's 9 1/2 yd (her jaws 2.4 m above her quarterdeck, judgement); the head 17.15 m along the
# mizen yard's line from the throat, 6.09 m beyond the yard's peak; the foot 16.57 m along the
# boom from the jaws; about 197 square metres against 198.5 by Steel's rule (vol. I, OCR l.
# 10891-10897: mean cloths by mean depth, 22 1/2 in to a cloth). Canvas No. 5 (Steel: "No. 5 or
# 6", l. 13819).
DRIVER_FORE_LEECH_M = 6.98
DRIVER_HEAD_M = 17.15
DRIVER_FOOT_M = 16.57
DRIVER_STEEL_AREA_M2 = 198.5
DRIVER_CANVAS_NO = 5
# Her boom by Steel's p. 40 rule, the main topsail yard's length: 65 ft 4 in (Indf §4.5); laid
# level, its jaws where the fore leech from the fixture's truss puts them, about 4.5 m above the
# frigate's deck (Ext §17.8, judgement).
DRIVER_BOOM_M = 19.91
# Her driver yard by the same rule, 34 ft 6 in (Ext §17.2), not filed as a spar: it went aloft
# with the sail. The peak stands no more than two-thirds of it beyond the mizen yard's peak.
DRIVER_YARD_M = 10.52


# ---------------------------------------------------------------------------
# The fixtures
# ---------------------------------------------------------------------------


def frigate_with_mizen_yard_doc() -> dict[str, Any]:
    """`frigate-36.yaml` with the mizen course cut at the mast on its lateen yard and the two
    yards under the bowsprit, each with its square sail (Ext §8 item 7)."""
    doc = _file("frigate-36")
    deck = doc["hull"]["deck_height_m"]
    spars = _by_id(doc["spars"])
    _mizen_course(doc, deck, spars["mizzen.mast"])
    _sprit_yards(doc, deck)
    return doc


def frigate_with_mizen_yard() -> Ship:
    return ship_from_dict(frigate_with_mizen_yard_doc(), "tests/rig_fixtures.py:frigate")


def brig_with_settee_doc() -> dict[str, Any]:
    """`brig.yaml` with a settee on the main in place of her main course and spanker, the dry
    main yard and the main topsail kept, the main mast laid aback to heave to (Ext §8 item 7;
    Eng §4.4's variant with its two faults corrected)."""
    doc = _file("brig")
    deck = doc["hull"]["deck_height_m"]
    spars = _by_id(doc["spars"])
    _settee(doc, deck, spars["main.mast"])
    spars["main.mast"]["heave_to_aback"] = True  # D4(a): her main topsail to the mast
    return doc


def brig_with_settee() -> Ship:
    return ship_from_dict(brig_with_settee_doc(), "tests/rig_fixtures.py:brig")


def frigate_with_driver_doc(bent: bool = False) -> dict[str, Any]:
    """`frigate_with_mizen_yard_doc()` with the 64's driver (Ext §17.8): the frigate's boom put
    back, lengthened and hung at the driver's jaws, and the driver filed after the course in its
    place, in the sail room, the boom rigged in; `bent`, bent in the course's place with the boom
    rigged out and the course in the sail room (Ext §17.6, §17.11), as a shift leaves her."""
    doc = frigate_with_mizen_yard_doc()
    _driver(doc, doc["hull"]["deck_height_m"], bent)
    return doc


def frigate_with_driver(bent: bool = False) -> Ship:
    return ship_from_dict(frigate_with_driver_doc(bent), "tests/rig_fixtures.py:frigate-driver")


def write_ship(doc: dict[str, Any], folder: str | Path, name: str = "fixture") -> Path:
    """The document written as a ship file `<name>.yaml` in `folder`, for what reads a path
    (`api.session.make_world`, `ship.loader.load_ship`)."""
    path = Path(folder) / f"{name}.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False, allow_unicode=True), encoding="utf-8")
    return path


def area_centroid(pts: list) -> tuple[float, float, float]:
    """A sail's area and the centroid of its corners, (x, height) (the generator's
    `_quad_area_centroid`): the fixtures' sails take their area, `x_m` and centre from it, and
    the tests check them by it."""
    pts = list(pts)
    a = cx = cz = 0.0
    for (x1, z1), (x2, z2) in zip(pts, pts[1:] + pts[:1], strict=True):
        cross = x1 * z2 - x2 * z1
        a += cross
        cx += (x1 + x2) * cross
        cz += (z1 + z2) * cross
    a *= 0.5
    return abs(a), cx / (6.0 * a), cz / (6.0 * a)


# ---------------------------------------------------------------------------
# The mizen course and its yard (Ext §3.4)
# ---------------------------------------------------------------------------


def _mizen_course(doc: dict[str, Any], deck: float, mast: dict[str, Any]) -> None:
    like = _like(doc)
    spanker = _by_id(doc["sails"])["mizzen.spanker"]
    gaff = _by_id(doc["spars"])["mizzen.gaff"]
    # the tack and the throat on the mast's raked line, the luff laced to it; the head along
    # the yard's slope; the clew loose, the foot and the after leech from it
    rake = math.radians(mast.get("rake_deg", 0.0))
    throat = (_mast_x(mast, MIZEN_TRUSS_M), MIZEN_TRUSS_M)
    tack_z = MIZEN_TRUSS_M - MIZEN_LUFF_M * math.cos(rake)
    tack = (_mast_x(mast, tack_z), tack_z)
    peak = (throat[0] - MIZEN_HEAD_RUN_M, throat[1] + MIZEN_HEAD_RISE_M)
    clew = min(_meet(tack, MIZEN_FOOT_M, peak, MIZEN_LEECH_M), key=lambda p: p[0])  # abaft
    corners = _rounded([tack, throat, peak, clew])
    area, cx, cz = area_centroid(corners)
    yard = {
        "id": "mizzen.yard",
        "class": "lateen_yard",
        "on": "mizzen.mast",
        "length_m": round(MIZEN_YARD_M, 2),
        "height_m": MIZEN_TRUSS_M,  # the truss
        "rating_kn": gaff["rating_kn"],  # as the gaff it replaces (judgement)
    }
    course = {
        "id": "mizzen.course",
        "class": "lateen",
        "yard": "mizzen.yard",
        "mast": "mizzen.mast",
        "cut_at_mast": True,
        "corners_m": corners,
        "area_m2": round(area),
        "reef_bands": 1,  # Steel: one band a fifth of the mast leech from the foot (Bel §5.6)
        "x_m": round(cx, 1),
        "centre_height_m": round(deck + cz, 1),  # above the water
        "canvas_no": spanker["canvas_no"],
    }
    # Steel 1794 II p. 37; Lavery I32: the jeers, the lifts and the derrick, the vangs, the
    # bowlines at the heel (guys: a bowline is a sail's line in the engine), one sheet to the
    # taffrail and one tack forward of the mast; no brace and no brails
    lines = [
        _line("mizzen.yard.jeers", "halyard", "mizzen.yard", like("mizzen.gaff.throat_halyard")),
        _line("mizzen.yard.derrick", "lift", "mizzen.yard", like("mizzen.gaff.peak_halyard")),
        *_pair("mizzen.yard.lift", "lift", "mizzen.yard", like("mizzen.gaff.vang.starboard")),
        *_pair("mizzen.yard.vang", "vang", "mizzen.yard", like("mizzen.gaff.vang.starboard")),
        *_pair("mizzen.yard.bowline", "guy", "mizzen.yard", like("mizzen.gaff.vang.starboard")),
        _line("mizzen.course.sheet", "sheet", "mizzen.course", like("mizzen.spanker.sheet")),
        _line("mizzen.course.tack", "tack", "mizzen.course", like("mizzen.spanker.outhaul")),
    ]
    # in the groups the frigate files her spanker in, never "courses" (Ext §3.4); the storm
    # mizen bent in its place, as it was in the spanker's
    _take_the_place(doc, "mizzen.course", "mizzen.spanker")
    for sail in doc["sails"]:
        if sail.get("in_place_of") == "mizzen.spanker":
            sail["in_place_of"] = "mizzen.course"
    _add_after(doc["spars"], "mizzen.crossjack.yard", [yard])
    _add_after(doc["sails"], "mizzen.spanker", [course])
    doc["lines"].extend(lines)
    # its names: the frigate's "mizzen" (the spanker's until now) and the period's; the
    # spanker's own names go with it
    doc["aliases"]["mizzen"] = "mizzen.course"
    _remove(doc, {"mizzen.spanker", "mizzen.gaff", "mizzen.boom", "ringtail_boom", "ringtail"})
    for name in ("mizen", "mizzen course", "mizen course"):
        doc["aliases"][name] = "mizzen.course"


# ---------------------------------------------------------------------------
# The driver (Ext §17.2, §17.8)
# ---------------------------------------------------------------------------


def _driver(doc: dict[str, Any], deck: float, bent: bool) -> None:
    frigate = _file("frigate-36")
    like = _like(frigate)  # the frigate's own spanker's and gaff's lines, gone from the doc
    mast = _by_id(doc["spars"])["mizzen.mast"]
    # the throat the course's, under the same truss; the tack down the mast's raked line at the
    # boom's jaws, the fore leech below the throat; the head along the mizen yard's line (the
    # course's head, the throat to its peak) and on past the yard's peak on the driver yard;
    # the clew along the level boom
    rake = math.radians(mast.get("rake_deg", 0.0))
    throat = (_mast_x(mast, MIZEN_TRUSS_M), MIZEN_TRUSS_M)
    jaws_z = MIZEN_TRUSS_M - DRIVER_FORE_LEECH_M * math.cos(rake)
    tack = (_mast_x(mast, jaws_z), jaws_z)
    along = DRIVER_HEAD_M / math.hypot(MIZEN_HEAD_RUN_M, MIZEN_HEAD_RISE_M)
    peak = (throat[0] - along * MIZEN_HEAD_RUN_M, throat[1] + along * MIZEN_HEAD_RISE_M)
    clew = (tack[0] - DRIVER_FOOT_M, jaws_z)
    corners = _rounded([tack, throat, peak, clew])
    area, cx, cz = area_centroid(corners)
    # the frigate's spanker boom put back, lengthened to the 64's and hung at the jaws; its
    # horse and its rating kept (the rating pass loads nothing on a boom whose sail starts in
    # the sail room: Ext §17.2); out only while the driver is bent (Ext §17.11)
    boom = dict(_by_id(frigate["spars"])["mizzen.boom"])
    boom.update(length_m=DRIVER_BOOM_M, height_m=round(jaws_z, 2), rigged_out=bent)
    driver = {
        "id": "mizzen.driver",
        "class": "lateen",
        "yard": "mizzen.yard",
        "mast": "mizzen.mast",
        "boom": "mizzen.boom",
        "cut_at_mast": True,
        "corners_m": corners,
        "area_m2": round(area),
        "reef_bands": 0,  # Steel names no reef band in the driver (Ext §17.2)
        "x_m": round(cx, 1),
        "centre_height_m": round(deck + cz, 1),  # above the water
        "canvas_no": DRIVER_CANVAS_NO,
    }
    course = _by_id(doc["sails"])["mizzen.course"]
    if bent:
        course["bent"] = False  # in the sail room
    else:
        driver["bent"] = False
    driver["in_place_of"] = "mizzen.course"
    # Steel's lines (vol. I, "THE DRIVER or SPANKER SAIL", OCR l. 24523-24545; Ext §17.2), each
    # rated as the frigate's line it stands for: one halyard for Steel's pairs of halyards (the
    # gaff's peak halyard's), the tack to the boom's throat (the course's tack, the spanker's
    # outhaul's), one unsided sheet rove through the boom's end, two parts (the spanker's
    # sheet's), and the downhaul (the storm mizzen's)
    d = "mizzen.driver"
    lines = [
        _line(f"{d}.halyard", "halyard", d, like("mizzen.gaff.peak_halyard")),
        _line(f"{d}.tack", "tack", d, like("mizzen.spanker.outhaul")),
        _line(f"{d}.sheet", "sheet", d, like("mizzen.spanker.sheet")),
        _line(f"{d}.downhaul", "downhaul", d, like("storm_mizzen.downhaul")),
    ]
    # the course filed first, so that the yard's sail (`sail_of`, the first naming it) stays it
    _add_after(doc["spars"], "mizzen.yard", [boom])
    _add_after(doc["sails"], "mizzen.course", [driver])
    doc["lines"].extend(lines)
    # "occasional sails" alone, never "plain sail", "courses" or "all sail" (Ext §17.2)
    doc["groups"]["occasional sails"].insert(0, d)
    for name in ("driver", "spanker", "driver boomsail"):
        doc["aliases"][name] = d
    for name in ("driver boom", "spanker boom"):
        doc["aliases"][name] = "mizzen.boom"
    # its spare in the sail room, with the occasional sails' (Ext §17.2); bent, the course's
    # canvas in the driver's stead, as a shift leaves it (Ext §17.10 item 9), so that the count
    # of spares stands and "shift the driver for the mizen" has a sail to bend
    spare = (
        {"kind": course["id"], "canvas_no": course["canvas_no"], "condition": 100}
        if bent
        else {"kind": d, "canvas_no": DRIVER_CANVAS_NO, "condition": 100}
    )
    doc["crew"]["stores"]["sails"].append(spare)


# ---------------------------------------------------------------------------
# The yards under the bowsprit (Ext §4.1)
# ---------------------------------------------------------------------------


def _sprit_yards(doc: dict[str, Any], deck: float) -> None:
    like = _like(doc)
    spars = _by_id(doc["spars"])
    sails = _by_id(doc["sails"])
    bowsprit = _head_spar_line(spars, "bowsprit")
    jib_boom = _head_spar_line(spars, "jib_boom")
    ss_x, ss_z = _along(bowsprit, SPRITSAIL_STATION)
    st_x, st_z = _along(jib_boom, SPRIT_TOPSAIL_STATION)
    ss_z -= SPRITSAIL_HANG_M
    st_z -= SPRIT_TOPSAIL_HANG_M
    ss_len = spars["fore.topsail.yard"]["length_m"]
    st_len = spars["fore.topgallant.yard"]["length_m"]
    # the spritsail: its area over nine-tenths of its yard, down to a metre above the water
    ss_depth = deck + ss_z - SPRITSAIL_FOOT_ABOVE_WATER_M
    ss_area = SPREAD * ss_len * ss_depth
    # the sprit topsail: the trapezoid from its yard to the spritsail yard's arms, its centre
    # the trapezoid's (from the foot: depth (2 head + foot) / 3 (head + foot))
    head, foot, gap = SPREAD * st_len, SPREAD * ss_len, st_z - ss_z
    st_area = 0.5 * (head + foot) * gap
    up = (2.0 * head + foot) / (3.0 * (head + foot))
    new_spars = [
        {
            "id": "spritsail.yard",
            "class": "yard",
            "on": "bowsprit",
            "x_m": round(ss_x, 1),
            "length_m": ss_len,
            "height_m": round(ss_z, 1),
            "brace_limit_deg": SPRIT_BRACE_LIMIT_DEG,
            "rating_kn": spars["fore.topsail.yard"]["rating_kn"],  # as the yard of its length
        },
        {
            "id": "sprit_topsail.yard",
            "class": "yard",
            "on": "jib_boom",
            "x_m": round(st_x, 1),
            "length_m": st_len,
            "height_m": round(st_z, 1),
            "brace_limit_deg": SPRIT_BRACE_LIMIT_DEG,
            "rating_kn": spars["fore.topgallant.yard"]["rating_kn"],
        },
    ]
    new_sails = [
        {
            "id": "spritsail",
            "class": "square",
            "yard": "spritsail.yard",
            "area_m2": round(ss_area),
            "reef_bands": 2,  # Steel's two diagonal bands, reefed as any square sail's (Ext §4.1)
            "x_m": round(ss_x, 1),
            "centre_height_m": round(deck + ss_z - 0.5 * ss_depth, 1),
            "canvas_no": sails["fore.topsail"]["canvas_no"],
        },
        {
            "id": "sprit_topsail",
            "class": "square",
            "yard": "sprit_topsail.yard",
            "area_m2": round(st_area),
            "reef_bands": 0,  # none (Lever l. 7354-7356; Ext §4.1)
            "x_m": round(ss_x + up * (st_x - ss_x), 1),
            "centre_height_m": round(deck + ss_z + up * gap, 1),
            "canvas_no": sails["fore.topgallant"]["canvas_no"],
        },
    ]
    # the square sail's lines (`gen_ships.square_sail_lines`: sided braces, lifts and sheets,
    # clewlines, a buntline) and the guys (Lavery I28); no halyard to the spritsail yard,
    # which hangs in slings, and the sprit-topsail yard's halyard for its traveller's
    # outhauler (Falconer 1780, SPRITSAIL-TOPSAIL), each rated as the fore topsail's and the
    # fore topgallant's lines
    lines = []
    for yard, sail, by in (
        ("spritsail.yard", "spritsail", "fore.topsail"),
        ("sprit_topsail.yard", "sprit_topsail", "fore.topgallant"),
    ):
        if sail == "sprit_topsail":
            lines.append(_line(f"{yard}.halyard", "halyard", yard, like(f"{by}.yard.halyard")))
        lines += [
            *_pair(f"{yard}.brace", "brace", yard, like(f"{by}.yard.brace.starboard")),
            *_pair(f"{yard}.lift", "lift", yard, like(f"{by}.yard.lift.starboard")),
            *_pair(f"{yard}.guy", "guy", yard, like(f"{by}.yard.brace.starboard")),
            *_pair(f"{sail}.sheet", "sheet", sail, like(f"{by}.sheet.starboard")),
            *_pair(f"{sail}.clewline", "clewline", sail, like(f"{by}.clewline.starboard")),
            _line(f"{sail}.buntline", "buntline", sail, like(f"{by}.buntline")),
        ]
    _add_after(doc["spars"], "flying_jib_boom", new_spars)
    doc["sails"].extend(new_sails)
    doc["lines"].extend(lines)
    # their own group, which the engine does not read, and "all sail"; never "plain sail",
    # "courses", "topsails", "headsails" or "jibs", which it reads by name (Ext §4.1)
    doc["groups"]["spritsails"] = ["spritsail", "sprit_topsail"]
    doc["groups"]["all sail"] += ["spritsail", "sprit_topsail"]


Point = tuple[float, float]


def _head_spar_line(spars: dict[str, dict], sid: str) -> tuple[Point, Point]:
    """A bowsprit's or a jib-boom's heel and end, (x, height above the deck), as the drawing
    places them (`client/projection.js`, `placeSpars`): the bowsprit from its `x_m` at the
    deck, rising its `height_m` over its length; a boom on it from its end, to its own
    `height_m` above the deck."""
    s = spars[sid]
    length, height = s["length_m"], s["height_m"]
    if s["class"] == "bowsprit":
        heel = (s["x_m"], 0.0)
        rise = min(height, 0.95 * length)
    else:
        heel = _head_spar_line(spars, s["on"])[1]
        rise = max(min(height - heel[1], 0.7 * length), 0.0)
    return heel, (heel[0] + math.sqrt(max(length * length - rise * rise, 0.0)), heel[1] + rise)


def _along(line: tuple[Point, Point], fraction: float) -> Point:
    (x0, z0), (x1, z1) = line
    return x0 + fraction * (x1 - x0), z0 + fraction * (z1 - z0)


# ---------------------------------------------------------------------------
# The settee (D5(a); Ext §5.1)
# ---------------------------------------------------------------------------


def _settee(doc: dict[str, Any], deck: float, mast: dict[str, Any]) -> None:
    like = _like(doc)
    spars = _by_id(doc["spars"])
    course = _by_id(doc["sails"])["main.course"]
    # the head on the yard at 44 degrees, slung a third along it from the throat on the
    # mast's raked line; the luff down from the throat to the tack at the rail; the clew
    # where the foot from the tack meets the leech from the peak, below them
    head = SETTEE_HEAD_M
    leech = SETTEE_LEECH_OF_HEAD * head
    foot = SETTEE_FOOT_OF_HEAD * head
    luff = SETTEE_LUFF_OF_LEECH * leech
    run = math.cos(math.radians(SETTEE_YARD_DEG)) * head / 3.0  # a third of the head
    rise = math.sin(math.radians(SETTEE_YARD_DEG)) * head / 3.0
    sling_z = SETTEE_TACK_M + luff + rise
    sling_x = _mast_x(mast, sling_z)
    throat = (sling_x + run, sling_z - rise)
    peak = (sling_x - 2.0 * run, sling_z + 2.0 * rise)
    tack = (throat[0], SETTEE_TACK_M)
    clew = min(_meet(tack, foot, peak, leech), key=lambda p: p[1])  # the lower
    corners = _rounded([tack, throat, peak, clew])
    area, cx, cz = area_centroid(corners)
    lug_yard = {
        "id": "main.lug_yard",
        "class": "lug_yard",
        "on": "main.mast",
        "length_m": head,
        "height_m": round(sling_z, 2),  # the sling, as the lugger's lug yards'
        "rating_kn": spars["main.gaff"]["rating_kn"],  # as the gaff it replaces (judgement)
    }
    settee = {
        "id": "main.settee",
        "class": "lug",
        "yard": "main.lug_yard",
        "mast": "main.mast",
        "dipping": True,
        "settee": True,
        "corners_m": corners,
        "area_m2": round(area),
        "reef_bands": 1,  # D42(a): one band parallel to the foot, a fifth of the leech up
        "x_m": round(cx, 1),
        "centre_height_m": round(deck + cz, 1),  # above the water (Eng §4.4's first fault)
        "canvas_no": course["canvas_no"],
    }
    # Lescallier p. 390 (Bil §1.2; Ext §5.1): the jeers, the derrick (a lift), the peak brace
    # (the English vangs), the ourses (the bowlines at the heel: guys), the tacks, one sheet
    # to the taffrail, and the clewlines and buntline "comme pour les voiles quarrées"
    y, s = "main.lug_yard", "main.settee"
    lines = [
        _line(f"{y}.jeers", "halyard", y, like("main.gaff.throat_halyard")),
        _line(f"{y}.derrick", "lift", y, like("main.gaff.peak_halyard")),
        *_pair(f"{y}.vang", "vang", y, like("main.gaff.vang.starboard")),
        *_pair(f"{y}.ourse", "guy", y, like("main.course.bowline.starboard")),
        *_pair(f"{s}.tack", "tack", s, like("main.course.tack.starboard")),
        _line(f"{s}.sheet", "sheet", s, like("main.spanker.sheet")),
        *_pair(f"{s}.clewline", "clewline", s, like("main.course.clewline.starboard")),
        _line(f"{s}.buntline", "buntline", s, like("main.course.buntline")),
    ]
    # "courses" with the fore course, "plain sail" and "all sail" (Ext §5.1); "mainsail" its
    # name, as it was the course's
    _take_the_place(doc, s, "main.course", only=("courses", "plain sail", "all sail"))
    doc["aliases"]["mainsail"] = s
    _add_after(doc["spars"], "main.boom", [lug_yard])
    _add_after(doc["sails"], "main.course", [settee])
    doc["lines"].extend(lines)
    _remove(doc, {"main.course", "main.spanker", "main.gaff", "main.boom", "storm_trysail"})


# ---------------------------------------------------------------------------
# The document's work
# ---------------------------------------------------------------------------


@cache
def _read(name: str) -> dict[str, Any]:
    return yaml.safe_load((SHIPS / f"{name}.yaml").read_text(encoding="utf-8"))


def _file(name: str) -> dict[str, Any]:
    """The committed file's document, a fresh copy."""
    return copy.deepcopy(_read(name))


def _by_id(items: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["id"]: item for item in items}


def _like(doc: dict[str, Any]) -> Callable[[str], dict[str, Any]]:
    """The rating (and purchase) of a line of the file, by its id, for a new line that stands
    for it; read before the old parts go."""
    lines = _by_id(doc["lines"])

    def like(line_id: str) -> dict[str, Any]:
        old = lines[line_id]
        return {k: old[k] for k in ("rating_kn", "parts") if k in old}

    return like


def _line(lid: str, cls: str, of: str, like: dict[str, Any], side: str | None = None) -> dict:
    line: dict[str, Any] = {"id": lid if side is None else f"{lid}.{side}", "class": cls, "of": of}
    if side is not None:
        line["side"] = side
    line.update(like)
    return line


def _pair(lid: str, cls: str, of: str, like: dict[str, Any]) -> list[dict[str, Any]]:
    return [_line(lid, cls, of, like, side) for side in ("starboard", "larboard")]


def _mast_x(mast: dict[str, Any], z: float) -> float:
    """x of the point on a lower mast's raked line `z` above the deck: the rake carries it aft
    as it rises (`gen_ships.py`'s lugger, `client/projection.js`'s `xAt`)."""
    return mast["x_m"] - math.tan(math.radians(mast.get("rake_deg", 0.0))) * z


def _meet(p0, r0, p1, r1) -> list[tuple[float, float]]:
    """The two points `r0` from `p0` and `r1` from `p1`."""
    (x0, z0), (x1, z1) = p0, p1
    dx, dz = x1 - x0, z1 - z0
    d = math.hypot(dx, dz)
    a = (r0 * r0 - r1 * r1 + d * d) / (2.0 * d)
    h = math.sqrt(max(r0 * r0 - a * a, 0.0))
    mx, mz = x0 + a * dx / d, z0 + a * dz / d
    return [(mx + h * dz / d, mz - h * dx / d), (mx - h * dz / d, mz + h * dx / d)]


def _rounded(points) -> list[list[float]]:
    return [[round(x, 2), round(z, 2)] for x, z in points]


def _add_after(items: list[dict[str, Any]], after: str, new: list[dict[str, Any]]) -> None:
    at = next(i for i, item in enumerate(items) if item["id"] == after) + 1
    items[at:at] = new


def _take_the_place(doc: dict[str, Any], new: str, old: str, only: tuple[str, ...] = ()) -> None:
    """`new` listed where `old` is, in every group that lists it (or in `only` those)."""
    for name, members in doc["groups"].items():
        if old in members and (not only or name in only):
            members.insert(members.index(old), new)


def _remove(doc: dict[str, Any], ids: set[str]) -> None:
    """The parts `ids` taken out with everything that names them: their lines, their places
    in the groups (a group left empty goes, and an alias of it), the aliases of them, and the
    spares made for them in the sail room."""
    doc["spars"] = [s for s in doc["spars"] if s["id"] not in ids]
    doc["sails"] = [s for s in doc["sails"] if s["id"] not in ids]
    gone = ids | {ln["id"] for ln in doc["lines"] if ln["of"] in ids}
    doc["lines"] = [ln for ln in doc["lines"] if ln["id"] not in gone]
    groups = {}
    for name, members in doc["groups"].items():
        kept = [m for m in members if m not in gone]
        if kept:
            groups[name] = kept
        else:
            gone.add(name)
    doc["groups"] = groups
    doc["aliases"] = {a: t for a, t in doc["aliases"].items() if t not in gone}
    room = (doc.get("crew") or {}).get("stores", {}).get("sails")
    if room is not None:
        doc["crew"]["stores"]["sails"] = [s for s in room if s["kind"] not in gone]
