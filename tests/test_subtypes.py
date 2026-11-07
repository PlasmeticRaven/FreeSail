"""Package 75, SW-4: the sub-types as fits and roles, and every file's armament and bill
(docs/design/Build-Ships.md §8, §9; §14.1's line for this file). The files' side (the first
pass): each file's `ship.descriptions` carries the table's `fit` and `roles` (§8.2), every
description's fit a fit of its file or `unarmed`; the three small files sail unarmed by default
with fits for the editor and their bills (§9.1); the privateer schooner's pivot reckons its arc
from her own rig (§9.2). The world side (the second pass): the index's four new rows, their
words and their class (§8.2); the merchant brig sailing her own file (§8.4, the lead's ruling of
2026-10-29); a scenario's `role:` refused at the load outside her description's roles and the
captains' (§8.1); the two new books, the Indiaman's and the revenue cutter's (§8.3), each against
the book it is made from and at sea; quarters beaten in the three unarmed files meeting their
bills, measured and pinned (§9.1); and truth 7-191, drafted here for Phase 5 to move into
`tests/test_known_truths.py` (§15). The reviews' mends: a crewed ship kept evading by a man of war
of her own class (a row's `unless` naming several stimuli), a crewed sub-type keeping her first
role when her intent is changed, the sub-types found after "the", and one role refused in the
singular."""

from __future__ import annotations

import importlib.util
import math
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail import units
from freesail.api.session import make_world
from freesail.combat import guns as G
from freesail.core.world import Scenario
from freesail.ship.graph import Ship
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.schema import UNARMED
from freesail.world import brains as B
from freesail.world import captains as C
from freesail.world import service as SV
from freesail.world import ships as S
from freesail.world.captains import ROLES
from freesail.world.geo import Position, destination

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
FRIGATE = "data/ships/frigate-36.yaml"
BRIG = "data/ships/brig.yaml"
MERCHANT = "data/ships/merchant-brig.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"
CUTTER = "data/ships/cutter.yaml"
LUGGER = "data/ships/lugger.yaml"
SMACK = "data/ships/smack.yaml"

# Build-Ships.md §8.2, every row whose file exists, as (file, description): (fit, whether it is
# her file's default, roles). The merchant brig sails merchant-brig.yaml by the lead's ruling of
# §8.4; brig.yaml keeps its pair of words with no fit or role (the shared design's §4.4).
TABLE = {
    (FRIGATE, "frigate"): ("amazon class 1795", True, ["kings-ship", "commodore"]),
    (BRIG, "brig-sloop"): ("diligence class 1796", True, ["cruiser", "kings-ship", "commodore"]),
    (MERCHANT, "merchant brig"): ("merchant", True, ["merchant", "packet", "indiaman"]),
    (SCHOONER, "schooner"): (UNARMED, True, ["merchant"]),
    (PRIVATEER, "privateer schooner"): ("long tom", True, ["privateer"]),
    (CUTTER, "cutter"): ("carronades", True, ["cruiser", "kings-ship"]),
    (CUTTER, "revenue cutter"): ("long guns", False, ["revenue"]),
    (CUTTER, "hired armed cutter"): ("long guns", False, ["cruiser"]),
    (CUTTER, "coasting cutter"): (UNARMED, False, ["merchant"]),
    (LUGGER, "lugger"): (UNARMED, True, ["fisherman", "merchant"]),
    (LUGGER, "privateer lugger"): ("gun lugger 1795", False, ["privateer"]),
    (SMACK, "smack"): (UNARMED, True, ["fisherman"]),
}
# §8.3's two new roles, in `captains.ROLES` with their books since the world side (the first
# pass let a description name them ahead of `ROLES`; that allowance is gone)
NEW_ROLES = ("indiaman", "revenue")
# The four rows the world side adds to the index (§8.2), each a sub-type of a file already sailed
NEW_ROWS = ("revenue cutter", "hired armed cutter", "coasting cutter", "privateer lugger")


def _doc(path):
    return yaml.safe_load((ROOT / path).read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# The descriptions' fits and roles (§8.1, §8.2)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", SHIP_FILES, ids=lambda p: p.name)
def test_every_descriptions_fit_is_a_fit_of_its_file_or_unarmed(path):
    """§8.1: 'a test proves every description's fit is a fit of its file' (and `unarmed`), and
    its roles are captains' roles (`captains.ROLES`), each with its book."""
    spec = load_spec(path)
    fits = set(spec.armament.fits) if spec.armament is not None else set()
    for key, words in S.file_descriptions(str(path)).items():
        if "fit" in words:
            assert words["fit"] in fits | {UNARMED}, (path.name, key, words["fit"])
        for role in words.get("roles", []):
            assert role in ROLES and C.load_doctrine(role).role == role, (path.name, key, role)


def test_every_index_rows_fit_is_a_fit_of_her_file_and_her_roles_captains_roles():
    """The index's side of the same (§8.1): every row of `DESCRIPTIONS` names a file there is,
    whose description of her gives a fit of that file (or `unarmed`) and roles all in
    `captains.ROLES`, but the razee's and the 64's, which §8.2 does not list and whose designs
    give neither; the two new roles are in `ROLES` (no allowance beside it now)."""
    assert set(NEW_ROLES) <= set(ROLES)
    for key in S.DESCRIPTIONS:
        d = S.description(key)
        assert (ROOT / d["file"]).is_file(), key
        if key in ("razee", "sixty-four"):
            assert "fit" not in d and "roles" not in d, key
            continue
        spec = load_spec(d["file"])
        fits = set(spec.armament.fits) if spec.armament is not None else set()
        assert d["fit"] in fits | {UNARMED}, (key, d["fit"])
        assert d["roles"] and set(d["roles"]) <= set(ROLES), (key, d["roles"])


@pytest.mark.parametrize(("path", "key"), list(TABLE), ids=lambda v: str(v).split("/")[-1])
def test_each_rows_fit_and_roles_are_the_tables(path, key):
    """§8.2's rows in their files: the fit, the roles, and the fit her file's default exactly where
    the table puts it in the default's column."""
    fit, is_default, roles = TABLE[(path, key)]
    words = S.file_descriptions(path)[key]
    assert (words["fit"], words["roles"]) == (fit, roles)
    assert (S._default_fit(path) == fit) is is_default


def test_the_brig_keeps_her_two_descriptions_and_the_merchant_brigs_has_no_fit_there():
    """§8.4 as the lead ruled it: the merchant brig's fit and roles are in merchant-brig.yaml, whose
    fit `merchant` brig.yaml has not; the brig's own pair of words stays (the shared design's
    §4.4), the merchant brig's with no fit or role, and the brig-sloop's ports ten a side (RMG
    ZAZ4491, read; docs/design/ships-design/pages-zaz4491.md §0)."""
    own = S.file_descriptions(BRIG)
    assert set(own) == {"brig-sloop", "merchant brig"}
    assert "fit" not in own["merchant brig"] and "roles" not in own["merchant brig"]
    assert own["brig-sloop"]["what"] == "a brig-sloop of war, ten ports a side"
    assert S.file_descriptions(MERCHANT)["merchant brig"]["what"] == own["merchant brig"]["what"]


def test_the_new_rows_glass_words_are_the_index_rows():
    """The four new rows (§8.2) give their rig in their files and no `what`: what the glass makes
    her out is the index's row. The revenue cutter's names her service, a man of war's word to a
    privateer (§8.2: '"revenue" is already a man-of-war word', `captains.MAN_OF_WAR_WORDS`); the
    hired and the coasting cutters are made out as a cutter, as the King's cutter is, and the
    privateer lugger as the chasse-marée, since no design words them otherwise (for the lead)."""
    for path, key in ((CUTTER, "revenue cutter"), (CUTTER, "hired armed cutter")):
        words = S.file_descriptions(path)[key]
        assert words["rig"] == "a cutter" and "what" not in words
    assert "what" not in S.file_descriptions(CUTTER)["coasting cutter"]
    words = S.file_descriptions(LUGGER)["privateer lugger"]
    assert words["rig"] == "a lugger" and "what" not in words
    whats = {key: S.description(key)["what"] for key in NEW_ROWS}
    assert whats == {
        "revenue cutter": "a revenue cutter",
        "hired armed cutter": S.description("cutter")["what"],
        "coasting cutter": S.description("cutter")["what"],
        "privateer lugger": S.description("lugger")["what"],
    }
    from freesail.world.signalling import _man_of_war_words

    assert [key for key, what in whats.items() if _man_of_war_words(what)] == ["revenue cutter"]


def _world():
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
        position=Position(49.60, -5.40).to_dict(),
        region="channel-west",
    )
    return make_world(7, FRIGATE, sc)


def _put(world, description, **kw):
    pos = destination(world.position, 90.0, 6.0 * units.NAUTICAL_MILE)
    spec = {
        "description": description,
        "name": description.title(),
        "position": pos,
        "goal": "bound for Falmouth",
        **kw,
    }
    world.vessels.serial += 1
    return world.vessels.add(S.vessel_from_spec(world, spec, world.vessels.serial))


def test_a_far_ship_of_her_files_default_carries_no_fit_in_her_form():
    """§8.1's last sentence: every index row today is her file's default, so no far ship's pinned
    form moves (`Vessel.to_dict` writes a fit only where she has one)."""
    w = _world()
    for key in ("frigate", "brig-sloop", "schooner", "privateer schooner", "cutter", "lugger",
                "smack", "merchant brig"):  # fmt: skip
        v = _put(w, key)
        assert v.fit == "" and "fit" not in v.to_dict(), key


def test_a_far_ship_of_a_row_not_her_files_default_carries_its_fit():
    """The other half of §8.1: a row whose fit is not her file's default carries it, read from
    her file, and writes it in her form. The files' side set the hired armed cutter's row for
    its test alone; the index has the four now, each carrying her own."""
    w = _world()
    for key, fit in (
        ("revenue cutter", "long guns"),
        ("hired armed cutter", "long guns"),
        ("coasting cutter", UNARMED),
        ("privateer lugger", "gun lugger 1795"),
    ):
        v = _put(w, key)
        assert v.fit == fit and v.to_dict()["fit"] == fit, key
        assert S.description(key)["file"] == v.ship_file
    assert _put(w, "hired armed cutter", role="cruiser").role == "cruiser"
    with pytest.raises(ValueError, match="no role a hired armed cutter takes"):
        _put(w, "hired armed cutter", role="merchant")


# ---------------------------------------------------------------------------
# The index's four new rows, their words and their class (§8.2)
# ---------------------------------------------------------------------------


def test_the_four_new_rows_are_in_the_index_with_their_words_and_class():
    """§8.2: the rows and their lookout's words ("a revenue cutter", "a hired cutter", "a hired
    armed cutter", "a coasting cutter", "a privateer lugger") in `world/ships.py`, rank 1 each in
    `SIZE_RANK`, each on her file's hull (the cutter's three, the lugger's one); qualified words
    take the row's tail as before ("a French privateer lugger"), and the plain rows are the first
    of their files, so that a ship of the file is still the cutter or the lugger by it. After
    "the", which the `ship:` world order takes, the whole of the words is tried first (the
    reviews: "the revenue cutter" had taken the cutter's row by its last word, her default guns
    and the merchant's book with it, and "the frigate" none)."""
    files = {key: S.description(key)["file"] for key in NEW_ROWS}
    assert files == {
        "revenue cutter": CUTTER,
        "hired armed cutter": CUTTER,
        "coasting cutter": CUTTER,
        "privateer lugger": LUGGER,
    }
    for words, key in (
        ("a revenue cutter", "revenue cutter"),
        ("a hired cutter", "hired armed cutter"),
        ("a hired armed cutter", "hired armed cutter"),
        ("a coasting cutter", "coasting cutter"),
        ("a privateer lugger", "privateer lugger"),
        ("a French privateer lugger", "privateer lugger"),
        ("a King's cutter", "cutter"),
        ("a French lugger", "lugger"),
        # OLD BESIDE NEW (SW-4's reviews): old, the cutter's row, the cutter's, the cutter's, the
        # lugger's and none; new, each her own
        ("the revenue cutter", "revenue cutter"),
        ("the hired armed cutter", "hired armed cutter"),
        ("the coasting cutter", "coasting cutter"),
        ("the privateer lugger", "privateer lugger"),
        ("the frigate", "frigate"),
    ):
        assert S.description_key(words) == key, words
    assert {key: C.SIZE_RANK[key] for key in NEW_ROWS} == dict.fromkeys(NEW_ROWS, 1)
    assert C.size_of_file(CUTTER) == C.SIZE_RANK["cutter"] and C.size_of_file(LUGGER) == 1
    keys = list(S.DESCRIPTIONS)
    assert keys.index("cutter") < min(keys.index(k) for k in NEW_ROWS[:3])
    assert keys.index("lugger") < keys.index("privateer lugger")


@pytest.mark.parametrize(
    ("key", "intent", "role"),
    [
        ("revenue cutter", "bound for Falmouth", "revenue"),
        ("revenue cutter", "keep the station off the Lizard within 10 miles", "revenue"),
        ("hired armed cutter", "bound for Falmouth", "cruiser"),
        ("coasting cutter", "trade 30 tons of tin from Falmouth to Plymouth", "merchant"),
        ("privateer lugger", "bound for Falmouth", "privateer"),
        ("privateer lugger", "cruise for prizes off the Lizard within 10 miles", "privateer"),
        ("coasting cutter", "carry this letter to Brest", "packet"),
        ("revenue cutter", "carry this letter to Brest", "packet"),
        ("revenue cutter", "cruise for prizes off the Lizard within 10 miles", "privateer"),
        ("cutter", "bound for Falmouth", "merchant"),  # the rows before keep their rules
        ("cutter", "keep the station off the Lizard within 10 miles", "cruiser"),
    ],
)
def test_the_new_rows_sail_by_their_first_role_where_the_intent_names_none(key, intent, role):
    """§8.1: a description's roles, 'the first the one the intent rules give': the four new rows
    sail by their first role (`brains.SUB_TYPE_ROWS`) unless the intent's kind names one (a
    letter the packet's, prizes the privateer's), and no row before them moves. Her crewed
    captain takes the same by the same rule (`captains.role_for` with her `sub_type_role`, the
    reviews' mend: a crewed revenue cutter given a new intent had fallen to the merchant's)."""
    w = _world()
    v = SimpleNamespace(description=key, role="")
    read = C.read_intent(w, intent)
    assert B.role_of_vessel(v, read) == role
    assert set(B.SUB_TYPE_ROWS) == set(NEW_ROWS)
    if key in NEW_ROWS:
        assert B.sub_type_role(v) == S.description(key)["roles"][0]
        assert C.role_for(w, read, "", B.sub_type_role(v)) == role
        assert C.role_for(w, read, "indiaman", B.sub_type_role(v)) == "indiaman"  # `role:` first
    else:
        assert B.sub_type_role(v) == ""


# ---------------------------------------------------------------------------
# The merchant brig's own file (§8.4, the lead's ruling of 2026-10-29)
# ---------------------------------------------------------------------------


def test_the_merchant_brig_sails_her_own_file_and_its_guns_and_company():
    """§8.4 as ruled: `DESCRIPTIONS["merchant brig"]` sails merchant-brig.yaml, the brig's hull and
    rig with the same polar and masthead, her own company of 16 and her four 6-pounders, where it
    sailed brig.yaml's sixteen 32-pounder carronades and two 6s and her 121 (old beside new, the
    far fight's side of her, `combat.far.far_ship`); a far merchant brig of the index carries no
    fit in her form (her file's default); `SHADOW_FILES` is gone."""
    from freesail.combat.far import far_ship

    d = S.description("merchant brig")
    assert (d["file"], d["fit"]) == (MERCHANT, "merchant")
    assert d["roles"] == ["merchant", "packet", "indiaman"]
    assert S.polar_of(MERCHANT) == S.polar_of(BRIG)
    assert S.rig_height_m(MERCHANT) == S.rig_height_m(BRIG)
    new = far_ship(d["file"], "britain")
    old = far_ship(BRIG, "britain")
    assert (sorted(g[:2] for g in new.guns), new.complement) == ([("long", 6.0)] * 2, 16)
    assert old.complement == 121
    # one side's eight carronades and both bow chasers
    assert sorted(g[:2] for g in old.guns) == [("carronade", 32.0)] * 8 + [("long", 6.0)] * 2
    assert not hasattr(S, "SHADOW_FILES")


def test_the_players_merchant_brig_is_made_out_by_her_own_files_row():
    """The player's shadow (the followed hull's vessel, `Vessels.player_shadow`) takes her words
    by her file's first row: the merchant brig's own file the merchant brig's row now, where
    `SHADOW_FILES` named it (package 70) and her shadow's file was the brig's; the brig's file a
    brig-sloop under her commander, as before."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position=Position(49.60, -5.40).to_dict(),
        region="channel-west",
    )
    for path, key, what in (
        (MERCHANT, "merchant brig", "a merchant brig, deep laden"),
        (BRIG, "brig-sloop", "a brig-sloop of war, ten ports a side"),
    ):
        w = make_world(7, path, sc)
        own = w.vessels.player_shadow(w)
        assert (own.description, own.what, own.kind) == (key, what, "a brig"), path
        assert own.ship_file == path


# ---------------------------------------------------------------------------
# A scenario's `role:` (§8.1), refused at the load in words
# ---------------------------------------------------------------------------


def _scenario_with(tmp_path, entry: str):
    from freesail.world.scenarios import load_scenario

    body = (
        "name: a role\n"
        "seed: 7\n"
        "start: 1805-06-12T10:00\n"
        "position: {lat_deg: 49.80, lon_deg: -5.30}\n"
        "region: channel-west\n"
        "nation: britain\n"
        "ship: {file: data/ships/frigate-36.yaml, heading_deg: 180, speed_kn: 4}\n"
        "wind: {from_deg: 270, knots: 12, gustiness: 0.0, variability: 0.0}\n"
        "ports: [falmouth, plymouth, brest]\n"
        "ships:\n"
        "  - {id: hope, name: Hope, nation: britain, position: 49 50 N 5 10 W,\n"
        '     goal: "bound for Falmouth", intent: "bound for Falmouth", ' + entry + "}\n"
    )
    path = tmp_path / "role.yaml"
    path.write_text(body, encoding="utf-8", newline="\n")
    return load_scenario(path)


@pytest.mark.parametrize(
    ("entry", "words"),
    [
        ("description: merchant brig, role: pirate", "'pirate' is no captain's role; the roles: "),
        (
            "description: merchant brig, role: kings-ship",
            "'kings-ship' is no role a merchant brig takes; her file gives a merchant brig the "
            "roles merchant, packet, indiaman.",
        ),
        # OLD BESIDE NEW (SW-4's reviews): old "the roles revenue.", one role in the plural
        (
            "description: revenue cutter, role: cruiser",
            "'cruiser' is no role a revenue cutter takes; her file gives a revenue cutter the "
            "role revenue.",
        ),
        (
            "description: smack, role: privateer",
            "'privateer' is no role a smack takes; her file gives a smack the role fisherman.",
        ),
        ("description: razee, role: kings-ship", "her file gives a razee no role."),
    ],
)
def test_a_scenarios_role_outside_her_descriptions_is_refused_at_the_load(tmp_path, entry, words):
    """§8.1: 'it must be one of her description's roles and of `ROLES`, or the load refuses it',
    in words, at the scenario's load (`scenarios.load_scenario`), where stage 0 refused it only
    when she was made (`ships.vessel_from_spec`, the same words)."""
    from freesail.world.scenarios import ScenarioError

    with pytest.raises(ScenarioError) as refused:
        _scenario_with(tmp_path, entry)
    said = str(refused.value)
    assert said.startswith(f"{tmp_path / 'role.yaml'}, ships 1: ") and words in said, said


@pytest.mark.parametrize(
    ("entry", "role"),
    [
        ("description: merchant brig, role: indiaman", "indiaman"),
        ("description: merchant brig, role: Packet", "packet"),
        ("description: revenue cutter, role: revenue", "revenue"),
        ("description: merchant brig", ""),
    ],
)
def test_a_scenarios_role_among_her_descriptions_loads_and_her_captain_sails_by_it(
    tmp_path, entry, role
):
    """A role among her description's loads, and the World made from it gives her captain that
    role's book (her far brain's, `brains.role_of_vessel`); with none, the intent's rules."""
    from freesail.world.scenarios import make_scenario_world

    sf = _scenario_with(tmp_path, entry)
    w = make_scenario_world(sf)
    v = w.vessels.find("Hope")
    assert v.role == role
    assert v.brain.role == (role or "merchant") and v.brain.doctrine.role == v.brain.role


# ---------------------------------------------------------------------------
# The two new books (§8.3), against the books they are made from
# ---------------------------------------------------------------------------

# §8.3's figures for the Indiaman, against the merchant's (all judgement)
INDIAMAN_FIGURES = {
    "yields_when_caught": (True, False),
    "engage_nm": (0.3, 1.0),
    "engage_range_cables": (2, 4),
    "morale_start": (0.5, 0.65),
    "strike_below": (0.4, 0.25),
    "engage_side": ("lee", "weather"),
    "board_odds": (0.0, 0.0),
}


def test_the_indiamans_book_is_the_merchants_with_the_figures_of_a_ship_that_fights():
    """§8.3: `indiaman.yaml` is the merchant's book with seven figures (`board_odds` the
    merchant's nought already): every other threshold, every state's book and every transition
    the merchant's, so that she keeps the merchant's seamanship and hauls off from a stranger as
    he does; each figure carries its source, the accounts by page where the tree holds James.
    Her service and the revenue cutter's are the merchant's (`service.ROLE_SERVICE`)."""
    merchant, ship = C.load_doctrine("merchant"), C.load_doctrine("indiaman")
    for key, (was, now) in INDIAMAN_FIGURES.items():
        assert (merchant.thresholds[key], ship.thresholds[key]) == (was, now), key
    others = set(merchant.thresholds) - set(INDIAMAN_FIGURES)
    assert set(ship.thresholds) == set(merchant.thresholds)
    assert {k: ship.thresholds[k] for k in others} == {k: merchant.thresholds[k] for k in others}
    assert ship.books == merchant.books and ship.transitions == merchant.transitions
    said = " ".join(ship.sources[k] for k in INDIAMAN_FIGURES)
    assert "James vol. 3 p. 252" in said and "James vol. 5 p. 135" in said
    assert (SV.ROLE_SERVICE["indiaman"], SV.ROLE_SERVICE["revenue"]) == (SV.MERCHANT,) * 2


def _rows(d, frm=None):
    return [(t.frm, t.on, t.to, t.unless) for t in d.transitions if frm is None or t.frm == frm]


def test_the_revenue_cutters_book_is_the_cruisers_but_whom_she_speaks_and_runs_from():
    """§8.3: `revenue.yaml` is the cruiser's book with every sail she investigates spoken (no
    `friend made out` row from `investigating a stranger`), a man of war of the enemy's hauled
    off from as the privateer's (`man of war near`, within `man_of_war_nm`), and no blockade
    station (no `stations:` table for the world's business); every other threshold, every book
    and every other transition the cruiser's, but that out of `evading` she engages an enemy in
    range unless overmatched or a man of war is near, as the privateer's (the reviews' mend: an
    enemy's revenue cutter had her evading and engaging by turns). The smuggler and the search
    are not modelled."""
    cruiser, revenue = C.load_doctrine("cruiser"), C.load_doctrine("revenue")
    assert set(revenue.thresholds) - set(cruiser.thresholds) == {"man_of_war_nm"}
    same = set(cruiser.thresholds)
    assert {k: revenue.thresholds[k] for k in same} == {k: cruiser.thresholds[k] for k in same}
    assert revenue.thresholds["man_of_war_nm"] == revenue.thresholds["stranger_hostile_nm"] == 6
    assert revenue.books == cruiser.books
    gone = ("investigating a stranger", "friend made out", "on passage", "")
    added = {r for r in _rows(revenue) if r[1] == "man of war near"}
    plain = ("evading", "enemy in range", "engaging", "overmatched")
    guarded = ("evading", "enemy in range", "engaging", ("overmatched", "man of war near"))
    assert gone in _rows(cruiser) and gone not in _rows(revenue)
    assert plain in _rows(cruiser) and plain not in _rows(revenue)
    assert set(_rows(revenue)) == (set(_rows(cruiser)) - {gone, plain}) | added | {guarded}
    assert guarded in _rows(C.load_doctrine("privateer"))
    assert {r[0] for r in added} == {
        "on passage", "beating", "keeping station", "investigating a stranger", "chasing",
        "engaging", "in company",
    }  # fmt: skip
    assert all(r[2] == "evading" for r in added)
    # each `man of war near` row comes before the state's `enemy in range`, as the privateer's
    for frm in {r[0] for r in added} - {"engaging"}:
        ons = [r[1] for r in _rows(revenue, frm)]
        assert ons.index("man of war near") < ons.index("enemy in range"), frm
    docs = {role: _doc(f"data/captains/{role}.yaml") for role in ("cruiser", "revenue")}
    assert docs["cruiser"].get("stations") and "stations" not in docs["revenue"]


FAR_OFF = Position(49.30, -6.40)


def _at_sea(player=FAR_OFF):
    """Open water south of the Lizard, the player's cutter lying some forty miles to the west so
    that the ships put on the sea below stay at far detail (judgement); or where `player` puts
    her, near enough that a ship promoted to crewed detail stays crewed."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position=player.to_dict(),
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
    )
    return make_world(7, CUTTER, sc)


def _sail(w, description, name, nation, where, intent, goal=None):
    w.vessels.serial += 1
    spec = {
        "description": description,
        "name": name,
        "nation": nation,
        "position": where.to_dict(),
        "goal": goal or intent,
        "intent": intent,
    }
    return w.vessels.add(S.vessel_from_spec(w, spec, w.vessels.serial))


def _states(w, v, minutes):
    seen = []
    for _ in range(minutes):
        w.run(60)
        if not seen or seen[-1][1] != v.brain.state:
            seen.append((w.clock.tick, v.brain.state))
    return seen


def test_a_revenue_cutter_speaks_the_neutral_coaster_a_cruiser_lets_go():
    """Whom she speaks (§8.3), at far detail: a Danish merchant brig three miles to the east of a
    British cutter standing east. The hired armed cutter, a cruiser, closes and makes her out,
    and lets her go by her neutral colours at two minutes, never spoken; the revenue cutter on
    the same water closes her and speaks her, at 32 minutes (seed 7, measured on the owner's
    machine 2026-11-06). Both sail by their rows' first role, given no `role:`."""
    here = Position(49.90, -5.20)
    there = destination(here, 90.0, 3.0 * units.NAUTICAL_MILE)
    out = {}
    for key in ("hired armed cutter", "revenue cutter"):
        w = _at_sea()
        cutter = _sail(w, key, "Rose", "britain", here, "bound for 49 50 N 4 30 W")
        dane = _sail(w, "merchant brig", "Anna Maria", "denmark", there, "bound for 49 50 N 6 00 W")
        assert dane.brain.role == "merchant"
        brain = cutter.brain
        out[key] = (brain.role, _states(w, cutter, 35), set(brain.spoken_ids), set(brain.given_up))
    role, states, spoken, given_up = out["hired armed cutter"]
    assert role == "cruiser" and states == [(60, "investigating a stranger"), (120, "on passage")]
    assert not spoken and given_up == {"ship-2"}
    role, states, spoken, given_up = out["revenue cutter"]
    assert role == "revenue" and states == [(60, "investigating a stranger"), (1920, "on passage")]
    assert spoken == {"ship-2"} and not given_up


def test_a_privateer_keeps_away_from_a_revenue_cutter_made_out_and_not_from_a_cutter():
    """§8.2: '"revenue" is already a man-of-war word, so a privateer keeps away from a revenue
    cutter made out'. A French privateer lugger cruising for prizes three miles east of a British
    cutter closes her and chases her; the revenue cutter made out by her service's words, she
    runs at nine minutes (`man of war near`); the hired armed cutter, made out a cutter, she
    chases on (seed 7, measured on the owner's machine 2026-11-06)."""
    here = Position(49.90, -5.20)
    there = destination(here, 90.0, 3.0 * units.NAUTICAL_MILE)
    out = {}
    for key in ("revenue cutter", "hired armed cutter"):
        w = _at_sea()
        _sail(w, key, "Rose", "britain", here, "bound for 49 50 N 4 30 W")
        lugger = _sail(
            w,
            "privateer lugger",
            "Hirondelle",
            "france",
            there,
            "cruise for prizes off the Lizard within 10 miles",
            goal="cruising off the Lizard within 10 miles",
        )
        assert lugger.brain.role == "privateer" and lugger.fit == "gun lugger 1795"
        out[key] = _states(w, lugger, 12)
    assert out["revenue cutter"][-1] == (540, "evading"), out
    assert "evading" not in [s for _t, s in out["hired armed cutter"]], out


def test_a_row_is_held_back_by_any_of_its_unless_and_only_two_rows_name_several():
    """The doctrine's grammar (the reviews' mend): a row's `unless` a list holds it back on any of
    its stimuli, kept as a tuple; one stimulus stays the word it was, so that every older row reads
    as before; none holds nothing back. Only the privateer's and the revenue cutter's way out of
    `evading` name two: an enemy in range engaged unless she is overmatched or a man of war is
    near (the privateer's `engage_nm`: 'unless she is overmatched or a man of war is near')."""
    one = C.Transition("on passage", "gale", "hove to for weather", "no sea room")
    assert one.unless == "no sea room" and one.unless_any == ("no sea room",)
    assert C.Transition("in port", "under way", "on passage").unless_any == ()
    two = C.Transition("evading", "enemy in range", "engaging", ("overmatched", "man of war near"))
    assert two.unless_any == ("overmatched", "man of war near")
    several = {
        (role, t.frm, t.on, t.unless)
        for role in ROLES
        for t in C.load_doctrine(role).transitions
        if not isinstance(t.unless, str)
    }
    assert several == {
        (role, "evading", "enemy in range", ("overmatched", "man of war near"))
        for role in ("privateer", "revenue")
    }
    assert "man of war is near" in C.load_doctrine("privateer").sources["engage_nm"]


def _crewed_beside(key, nation, intent, goal=None):
    """A British revenue cutter, the Rose, and a ship of `key` 0.6 miles to the east of her, both
    near the player's cutter (some four miles off, so that a ship promoted stays crewed); a
    minute run. Returns (world, the Rose, the second, `crews.promote` to promote either)."""
    from freesail.world import crews

    w = _at_sea(Position(49.90, -5.30))
    here = Position(49.90, -5.20)
    there = destination(here, 90.0, 0.6 * units.NAUTICAL_MILE)
    rose = _sail(w, "revenue cutter", "Rose", "britain", here, "bound for 49 50 N 4 30 W")
    other = _sail(w, key, "Other", nation, there, intent, goal=goal)
    w.run(60)
    return w, rose, other, crews.promote


@pytest.mark.parametrize(
    ("key", "promoted"),
    [("privateer lugger", "other"), ("revenue cutter", "rose")],
    ids=["a privateer lugger", "a revenue cutter"],
)
def test_a_man_of_war_of_her_own_class_keeps_a_crewed_ship_evading(key, promoted):
    """The reviews' blocker, mended: within her engaging distance of an enemy's revenue cutter,
    of her own class and so not overmatching her, a crewed privateer lugger (or a revenue cutter
    beside a French revenue cutter) went from `evading` to `engaging` and back every minute,
    beating to quarters, casting loose and securing the guns by turns, the `evading` row's guard
    `overmatched` alone. OLD BESIDE NEW (seed 7, measured on the owner's machine 2026-11-06,
    thirty minutes crewed): old, 27 changes of state for the lugger and 13 for the revenue cutter,
    evading and engaging by turns from seven minutes; new, three, investigating, chasing and then
    evading from seven minutes to the end, no gun cast loose."""
    if key == "privateer lugger":
        w, rose, other, promote = _crewed_beside(
            key,
            "france",
            "cruise for prizes off the Lizard within 10 miles",
            goal="cruising off the Lizard within 10 miles",
        )
    else:
        w, rose, other, promote = _crewed_beside(key, "france", "bound for 49 50 N 6 30 W")
    her = promote(w, other if promoted == "other" else rose)
    cap = her.captain
    seen = []
    for _ in range(30):
        w.run(60)
        if not seen or seen[-1][1] != cap.state:
            seen.append((w.clock.tick, cap.state))
    assert seen == [
        (120, "investigating a stranger"),
        (360, "chasing"),
        (420, "evading"),
    ], seen
    assert not [e for e in her.log if e.kind == "crew.quarters"]


@pytest.mark.parametrize(
    ("key", "nation", "role"),
    [
        ("revenue cutter", "britain", "revenue"),
        ("hired armed cutter", "britain", "cruiser"),
        ("privateer lugger", "france", "privateer"),
    ],
)
def test_a_crewed_sub_type_keeps_her_first_role_when_her_intent_is_changed(key, nation, role):
    """The reviews' mend: her far brain and her crewed captain both sail by her description's
    first role, and a world order changing her intent (`ship "X": intent ...`) left her far brain's
    but dropped her crewed captain's to the merchant's, `captains.role_for` knowing nothing of the
    sub-types. Her first role is carried in at the promotion (`Captain.sub_type_role`). OLD BESIDE
    NEW: old, after the order, her far brain's role hers and her crewed captain's and book the
    merchant's; new, all three hers."""
    from freesail.world import crews
    from freesail.world import orders as O

    w = _at_sea(Position(49.90, -5.30))
    there = destination(w.position, 90.0, 1.0 * units.NAUTICAL_MILE)
    v = _sail(w, key, "Rose", nation, there, "bound for 49 50 N 6 30 W")
    w.run(60)
    crew = crews.promote(w, v)
    assert (v.brain.role, crew.captain.role, crew.captain.sub_type_role) == (role,) * 3
    said = O.apply(w, O.parse('ship "Rose": intent bound for 49 50 N 4 30 W'))
    assert said[0] == "the intent of Rose's captain changed: bound for 49 50 N 4 30 W"
    assert (v.brain.role, crew.captain.role, crew.captain.doctrine.role) == (role,) * 3
    assert C.Captain.sub_type_role == ""  # the class's own: every other ship and old checkpoints


# ---------------------------------------------------------------------------
# The three small files: unarmed by default, their fits and bills (§9.1)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", [SCHOONER, LUGGER, SMACK])
def test_an_unarmed_default_makes_no_gun_and_no_battery(path):
    """`armament.default: unarmed`: no gun is made and no battery (`battery_of`), so a ship with
    no guns never engages (70); each named fit makes its guns."""
    spec = load_spec(path)
    assert spec.armament.default == UNARMED and spec.armament.fit() is None
    ship = load_ship(path)
    assert not ship.guns and G.battery_of(ship) is None
    for name, fit in spec.armament.fits.items():
        armed = Ship(spec, fit=name)
        assert len(armed.guns) == len(fit.guns) and G.battery_of(armed) is not None, name


def _kinds(fit):
    return sorted((g.kind, g.pounder, g.place) for g in fit.guns)


def test_the_topsail_schooners_two_fits_and_her_bill():
    """Lynx's six guns and forty men as a letter of marque (Chapelle 1930 p. 82: 'the Lynx, 6
    guns and 40 men'; the long 6s judgement), the privateer's same fit; and H.M. schooner
    Musquidobit's eight 18-pounder carronades and two 6-pounders (Winfield 1793-1817 p. 335),
    fought by the file's forty. The bill: the privateer's trimmers, helm 1, powder 1, the
    filling reckoned, the small arms and boarders the privateer's; every fit's gun crews and the
    bill's other stations within her forty."""
    spec = load_spec(SCHOONER)
    marque = spec.armament.fit("letter of marque")
    assert _kinds(marque) == [("long", 6, "broadside")] * 6 + [("swivel", 0.5, "rail")] * 4
    same = load_spec(PRIVATEER).armament.fit("letter of marque")
    assert [(g.id, g.x_m, g.height_m) for g in marque.guns] == [
        (g.id, g.x_m, g.height_m) for g in same.guns
    ]
    navy = spec.armament.fit("musquidobit 1813")
    assert _kinds(navy) == [("carronade", 18, "broadside")] * 8 + [("long", 6, "broadside")] * 2
    assert {g.x_m for g in navy.guns if g.kind == "long"} == {10.5}
    assert navy.exercise_charges == 2  # a King's fit: a fourth of her ten upper deck guns
    bill = spec.crew.quarter_bill
    assert bill.trimmers == {"forecastle": 4, "fore_top": 3, "afterguard": 4}
    assert (bill.helm, bill.powder, bill.filling) == (1, 1, None)
    assert (bill.small_arms, bill.boarders) == (8, 26)
    others = sum(bill.trimmers.values()) + bill.helm + bill.powder
    for fit in (marque, navy):
        at_guns = sum(g.crew for g in fit.guns if g.kind != "swivel" and g.side == "starboard")
        assert at_guns + others <= spec.crew.complement == 40, fit.name


def test_the_luggers_fit_is_eclairs_three_18s_over_the_rail_and_her_bill():
    """'Carrying No. 3 - 18 Pounder Guns' (RMG ZAZ6306's caption, the 8 probable: pages-zaz6306.md
    §2.1); no port on her sheet, so three rail guns (§6.4's pick), each at the waist rail's height
    (1.49 to 1.66 m, the note's §5.4). Ten men a gun by the gun's rule against her thirty, said in
    the fit's note. The bill judgement."""
    spec = load_spec(LUGGER)
    (name,) = spec.armament.fits
    fit = spec.armament.fit(name)
    assert name == "gun lugger 1795" and _kinds(fit) == [("long", 18, "rail")] * 3
    assert sorted(g.side for g in fit.guns) == ["larboard", "starboard", "starboard"]
    assert all(1.49 <= g.height_m <= 1.66 and g.deck is None for g in fit.guns)
    assert sum(g.crew for g in fit.guns) == 30 == spec.crew.complement
    bill = spec.crew.quarter_bill
    assert bill.trimmers == {"forecastle": 2, "afterguard": 2}
    assert (bill.helm, bill.powder, bill.filling, bill.small_arms, bill.boarders) == (
        1, 1, None, 6, 20,
    )  # fmt: skip


def test_the_smacks_fit_is_cullodens_two_guns_and_her_bill():
    """Culloden, '2 guns', 8 men (Charnock 1802 vol. III p. 274), their calibre not given: two long
    3-pounders, one a side over the rail (judgement); the bill for eight men judgement."""
    spec = load_spec(SMACK)
    fit = spec.armament.fit("culloden 1746")
    assert _kinds(fit) == [("long", 3, "rail")] * 2
    assert {g.side for g in fit.guns} == {"starboard", "larboard"}
    bill = spec.crew.quarter_bill
    assert bill.trimmers == {}
    assert (bill.helm, bill.powder, bill.filling, bill.small_arms, bill.boarders) == (
        1, 0, None, 0, 0,
    )  # fmt: skip
    assert sum(g.crew for g in fit.guns) + bill.helm <= spec.crew.complement == 8


def test_no_port_gun_of_the_small_files_wants_a_port_they_have_not():
    """Truth 7-185's form (`tests/test_profiles.py`): the lugger and the smack have no port, and
    their guns stand on none; the schooner's stand on the file's existing triples (Musquidobit's
    carronades at +4.81 on the plate's own port 5, where no gun of the privateer's fits stands)."""
    from freesail.combat.ports import PORT_PLACES
    from freesail.ship.profile import ports_of

    for path in (LUGGER, SMACK):
        spec = load_spec(path)
        assert not spec.hull.profile.ports_m
        for fit in spec.armament.fits.values():
            assert not [g for g in fit.guns if g.place in PORT_PLACES], path
    spec = load_spec(SCHOONER)
    for fit in spec.armament.fits.values():
        for g in fit.guns:
            if g.place in PORT_PLACES:
                on = [
                    t
                    for t in ports_of(spec.hull.profile, g.deck)
                    if abs(t[0] - g.x_m) <= 0.01 and abs(t[1] - g.height_m) <= 0.01
                ]
                assert on, (fit.name, g.id)


# ---------------------------------------------------------------------------
# The pivot's arc from its own rig (§9.2)
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def gen():
    """The generator as a module, not run."""
    spec = importlib.util.spec_from_file_location(
        "gen_ships_under_test_subtypes", ROOT / "tools" / "gen_ships.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


# Lynx's channels on her plate, typed from docs/design/ships-design/pages-chapelle-fig17.md §5.10
# (measured): each mast's axis at the sill line and its channel's after and fore ends, metres in
# her own frame; the file's length over her load line (26.84 m, the note's §6.2) gives k_L.
PLATE = {"fore.mast": (8.26, 5.26, 8.45), "main.mast": (-2.60, -5.18, -2.54)}
LYNX_LOAD_LINE_M = 26.84


def _privateers_rig(channels=None):
    doc = _doc(PRIVATEER)
    k_l = doc["hull"]["length_waterline_m"] / LYNX_LOAD_LINE_M
    if channels is None:
        channels = {
            m: (round((fore - axis) * k_l, 2), round((aft - axis) * k_l, 2))
            for m, (axis, aft, fore) in PLATE.items()
        }
    return SimpleNamespace(doc=doc, channels=channels)


def test_the_pivots_arc_is_reckoned_from_her_rig(gen):
    """From the pivot at +2.6 m: the fore topmast backstays in the after end of the fore channel
    (Steel 1794 vol. I pp. 199-200), x 4.91 m, bear 57.0 degrees off the bow at the rail's
    half-breadth there; the foremost main shroud in the fore end of the main channel, x -2.54 m,
    146.2; five degrees each way: 62 to 141 (measured on this machine, 2026-11-06). The owner's
    ruling by eye of 2026-10-25 was 60 to 140 (Proposal-PivotGun.md §3)."""
    arc, working = gen.pivot_arc_from_rig(_privateers_rig(), 2.6)
    assert arc == (62.0, 141.0)
    assert any("x 4.91 m: 57.0" in line for line in working)
    assert any("x -2.54 m: 146.2" in line for line in working)
    assert gen.pivot_arc_from_rig(_privateers_rig(), 2.6, margin_deg=0.0)[0] == (57.0, 146.0)
    # a pivot further aft opens forward and shuts sooner aft
    lo, hi = gen.pivot_arc_from_rig(_privateers_rig(), 1.0)[0]
    assert lo < 62.0 and hi < 141.0


def test_the_arc_wants_every_masts_channel_and_a_pivot_clear_of_them(gen):
    rig = _privateers_rig()
    with pytest.raises(ValueError, match="no channel is given for main.mast"):
        gen.pivot_arc_from_rig(_privateers_rig({"fore.mast": rig.channels["fore.mast"]}), 2.6)
    with pytest.raises(ValueError, match="within the run of fore.mast's channel"):
        gen.pivot_arc_from_rig(rig, 6.0)


def test_the_privateers_pivot_stands_on_the_arc_from_her_rig(gen):
    """Her file's pivot carries the reckoned arc, and bears at its ends and not past them."""
    arc = gen.pivot_arc_from_rig(_privateers_rig(), 2.6)[0]
    ship = load_ship(PRIVATEER)
    (pivot,) = [g for g in ship.guns.values() if g.place == "pivot"]
    assert pivot.x_m == 2.6 and pivot.arc_deg == arc
    battery = G.Battery(ship)
    for deg, bears in (
        (arc[0], True),
        (arc[0] - 1.0, False),
        (arc[1], True),
        (arc[1] + 1.0, False),
    ):
        pivot.train_deg = deg
        assert battery.bears(pivot, math.radians(deg)) is bears, deg


# ---------------------------------------------------------------------------
# Quarters beaten in the three unarmed files (§9.1), measured and pinned
# ---------------------------------------------------------------------------

# Measured on the owner's machine, 2026-11-06, seed 7: the quarters' divisions and their line
# when each file is the player's ship and beats to quarters at once, no gun manned. Before SW-4
# no file of the three had a bill, and `crew/quarters.py` reckoned the defaults (the helm two,
# no trimmers by station, the powder the idlers alone): the Speedwell's trimmers 31, helm 2,
# powder 3; the lugger's 23, 2, 1; the smack's 3, 2, 1 (the tuning notes, SW-4, old beside new).
UNARMED_QUARTERS = {
    SCHOONER: {"trimmers": 31, "helm": 1, "powder": 4},
    LUGGER: {"trimmers": 23, "helm": 1, "powder": 2},
    SMACK: {"trimmers": 4, "helm": 1, "powder": 1},
}


@pytest.mark.parametrize("path", list(UNARMED_QUARTERS), ids=lambda p: p.split("/")[-1])
def test_quarters_beaten_unarmed_meet_her_files_bill(path):
    """§9.1: 'a scenario that beats to quarters in an unarmed schooner meets the file's bill in
    place of the reckoned defaults' (`crew/quarters.py`), and the lugger and the smack the same:
    no gun crew is manned (no gun), the helm the bill's one where the defaults put two, the
    trimmers by her bill's stations and every hand left to them after, the powder the bill's and
    the second helmsman's place where it falls (measured, `UNARMED_QUARTERS`)."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=315.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=180.0,
        ship_speed_kn=4.0,
        position=Position(49.60, -5.40).to_dict(),
        region="channel-west",
    )
    w = make_world(7, path, sc)
    assert not w.ship.guns
    n0 = len(w.log)
    w.submit("beat to quarters")
    w.run(5)
    q = w.ship.extra["quarters"]
    bill = load_spec(path).crew.quarter_bill
    wanted = UNARMED_QUARTERS[path]
    words = ", ".join(f"the {k} {n}" for k, n in wanted.items())
    assert {k: len(q.divisions.get(k, [])) for k in wanted} == wanted
    assert len(q.divisions["helm"]) == bill.helm == 1 and not q.crews
    line = [e for e in list(w.log)[n0:] if e.kind == "crew.quarters"][0]
    assert line.text == f"Beat to quarters! Quarters: no gun crews manned, {words}."


# ---------------------------------------------------------------------------
# Truth 7-191 (§15), drafted here for Phase 5 to move into tests/test_known_truths.py
# ---------------------------------------------------------------------------


def _one_broadside_into_the_brig(role: str):
    """The French cutter (the player's ship, her carronades at the word) and the British merchant
    brig Hope, crewed, lying to a cable off her starboard beam with her scenario's `role:`; one
    broadside fired at the word and the fire held as soon as it has gone (no second), then ten
    minutes. Returns the brig's vessel and World, the cutter's World, and the least of the brig's
    morale over the ten minutes."""
    from freesail.world import crews

    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="france",
        ship_heading_deg=180.0,
        ship_speed_kn=0.0,
    )
    w = make_world(7, CUTTER, sc)
    w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    heading = float(w.ship.heading)
    there = destination(w.position, math.degrees(heading) + 90.0, 185.0)
    w.vessels.serial += 1
    v = S.vessel_from_spec(
        w,
        {
            "description": "merchant brig",
            "name": "Hope",
            "nation": "britain",
            "position": there,
            "goal": "bound for 48 30 N 5 18 W",
            "intent": "bound for 48 30 N 5 18 W",
            "role": role,
        },
        w.vessels.serial,
    )
    v.plan = [("lie_to", math.inf)]
    v.sail_state = "lying to"
    w.vessels.add(v)
    brig = crews.promote(w, v)
    brig.ship.dyn.heading = heading
    w.submit("hold your fire")
    w.run(65)
    w.submit("engage her to starboard")
    w.run(1)
    t0 = w.clock.tick
    assert w.submit("fire").kind == "guns.fire"
    for _ in range(120):
        w.run(1)
        if any(e.kind == "action.fired" and e.tick >= t0 for e in w.log):
            break
    w.submit("hold your fire")
    least = math.inf
    while w.clock.tick < t0 + 600:
        w.run(60)
        m = brig.ship.extra.get("morale")
        if m is not None:
            least = min(least, m.value)
    return v, brig, w, least


def test_truth_7_191_an_indiaman_holds_her_colours_through_a_merchantmans_striking_broadside():
    """**A draft, for Phase 5 to move into `tests/test_known_truths.py` and measure again on the
    merged tree** (Build-Ships.md §15, row 7-191; the brief's item 4: "an Indiaman is not a
    merchantman who strikes at the first telling broadside"). The merchant brig, her own file's
    sixteen men and four 6-pounders, given `role: indiaman` and `role: merchant` by her scenario
    entry, crewed a cable off the French cutter's starboard beam; one broadside at the word, three
    12-pounder carronades (36 pounds to her 12), the fire held after it. At seed 7 (measured on the
    owner's machine, 2026-11-06) the one broadside is the same in both: three fired, one struck
    her, one killed and one wounded. As a merchantman she strikes at it, her figure 0.12 under the
    merchant's 0.4 (two of sixteen hurt and the odds); as an Indiaman she holds her colours through
    the ten minutes, her figure at its least 0.27 over the Indiaman's 0.25. Each half can fail: the
    Indiaman's strikes if her role is not carried to her crewed captain or her book's figures are
    the merchant's, and the merchantman's holds if no shot tells or his line is the Indiaman's."""
    out = {role: _one_broadside_into_the_brig(role) for role in ("indiaman", "merchant")}
    broadsides = {}
    for role, (v, brig, w, _least) in out.items():
        assert brig.captain.role == role and v.brain.role == role
        assert brig.ship.spec.crew.complement == 16 and len(brig.ship.guns) == 4
        fired = [(e.data["fired"], e.data["struck"]) for e in w.log if e.kind == "action.fired"]
        hit = [
            (e.data["hits"], e.data["killed"], e.data["wounded"])
            for e in brig.log
            if e.kind == "action.hit"
        ]
        broadsides[role] = (fired, hit)
    # one broadside, the same broadside into both
    assert broadsides["indiaman"] == broadsides["merchant"] == ([(3, 1)], [(1, 1, 1)])
    v, brig, _w, _least = out["merchant"]
    line = [e for e in brig.log if e.kind == "action.struck"]
    assert v.struck and brig.captain.state == "struck" and line
    assert line[0].data["by_rule"] and line[0].data["strike_below"] == 0.4
    assert line[0].data["morale"] == 0.12 and brig.ship.extra["morale"].value == pytest.approx(
        0.123, abs=0.001
    )
    assert "two of 16 hurt, against a broadside of 36 pounds to our 12" in line[0].text
    v, brig, _w, least = out["indiaman"]
    assert not v.struck and not brig.ship.extra.get("struck")
    assert not [e for e in brig.log if e.kind == "action.struck"]
    m = brig.ship.extra["morale"]
    assert m.strike_below == 0.25 and least == pytest.approx(0.273, abs=0.001)
    assert least >= m.strike_below
