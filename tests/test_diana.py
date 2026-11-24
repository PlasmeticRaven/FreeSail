"""Package 90, the fourth hull: the corvette Diana, the Danish light frigate of 1804 in the Spanish
navy (her builder).

Her design is docs/design/Design-Ship-Diana.md (Dia-D), revised 2026-11-20 on her measuring and the
lead's rulings of that day (nudge 24), from her research note docs/design/Research-Diana-2026-11.md
(Dia) and the note of her measuring, docs/design/ships-design/pages-diana.md (Pages);
`tools/ships/diana.py` writes her file, `data/ships/corvette-20.yaml`. These are her tests (Dia-D
§14; Plan-Package90.md §8.0 steps 2 to 4, §10.1), each entering through the door the behaviour is
met at: her file loaded as the game loads it, an order given as a player gives it, her row as the
harbour reads it. Her six truths are drafted here under their reserved numbers, 7-660 to 7-665
(Dia-D §14's A to F), for the integrator to move into tests/test_known_truths.py at the close.

Measured on the cloud's container at her build (seed 7, the wind from the north, no gusts, the
truths' own helpers); the bands are her sources' or judgement where they say so.
"""

from __future__ import annotations

import json
import math
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest
import yaml

from freesail.core.rng import Rng
from freesail.crew import hands
from freesail.crew.model import Watch
from freesail.crew.muster import muster
from freesail.evolutions.registry import load_directory
from freesail.ship.loader import load_ship, load_spec
from freesail.ship.parts import SailState
from freesail.world import captains
from freesail.world import ships as S
from freesail.world.nations import load_nations

ROOT = Path(__file__).resolve().parents[1]
HER = "data/ships/corvette-20.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
LIBRA_KG = 0.4608  # the libra castellana, the book's own
FITS = ("danish 1807", "as captured 1809", "carronadas de a 30 1810", "1817")
DEFAULT_FIT = "carronadas de a 30 1810"
# Pages §5.7: her eleven ports a side, aft to forward, [x, sill, half-breadth at the sill]; the
# bow port's half-breadth her drawn side's at its sill (the lead's nudge 59; 2.1 before, by
# JUDGEMENT, 0.24 m outside her drawn side)
PORTS = [
    [-13.49, 2.11, 3.19], [-10.69, 1.93, 3.77], [-7.81, 1.82, 4.14], [-4.93, 1.75, 4.34],
    [-2.06, 1.72, 4.42], [0.80, 1.72, 4.46], [3.65, 1.75, 4.42], [6.42, 1.82, 4.33],
    [9.37, 1.91, 4.14], [12.27, 2.06, 3.74], [15.96, 2.38, 1.86],
]  # fmt: skip


@pytest.fixture(scope="module")
def doc():
    return yaml.safe_load((ROOT / HER).read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def spec():
    return load_spec(HER)


REPORT_PROBE = """
import sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import diana as her
her.build(sys.argv[1])
"""

MODULE_PROBE = """
import json, sys
sys.path.insert(0, "tools")
import gen_ships
sys.modules["gen_ships"] = gen_ships
from ships import diana as her
out = {}
for name, call in (
    ("table", her.check_table), ("winfield", her.check_winfield), ("masts", her.check_masts),
    ("ports", her.check_ports),
):
    call()
    out[name] = "held"
her.TABLE["fore"] = (281, 1463)
try:
    her.check_table()
except ValueError as e:
    out["table wrong"] = str(e)
her.TABLE["fore"] = (281, 1462)
her.WINFIELD["beam_m"] = 9.10
try:
    her.check_winfield()
except ValueError as e:
    out["winfield wrong"] = str(e)
her.WINFIELD["beam_m"] = 9.06
her.MASTS["main"]["heel"] = 1.40
try:
    her.check_masts()
except ValueError as e:
    out["masts wrong"] = str(e)
her.MASTS["main"]["heel"] = -2.18
her.PORTS[5][1] = 2.70
try:
    her.check_ports()
except ValueError as e:
    out["ports wrong"] = str(e)
her.PORTS[5][1] = 1.72
out["notes"] = {k: her.HULL_NOTES[k] for k in ("gm_m", "clr_x_m")}
p = her.particulars()
out["displacement"] = p.displacement_kg
out["table_kg"] = p.table_kg
out["length"] = round(p.length_m, 3)
out["beam"] = round(p.beam_m, 3)
out["depth"] = round(p.depth_m, 3)
out["scale"] = round(p.scale, 4)
out["main_len_ft"] = round(p.main_len_ft, 2)
geom = her.mast_geometry(p)
out["masts_ft"] = {n: round(g["length"], 1) for n, g in geom.items()}
out["main_yard_m"] = round(geom["main"]["yard"] * her.FT, 2)
fits = her.her_fits()
out["fits"] = [(n, len(g), her.broadside_lb(g)) for n, _s, g, _t in fits]
print(json.dumps(out, ensure_ascii=True))
"""


def _probe(code, *args):
    done = subprocess.run(
        [sys.executable, "-c", code, *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    assert done.returncode == 0, done.stderr
    return done


# ---------------------------------------------------------------------------
# Her module and her file (Dia-D §1)
# ---------------------------------------------------------------------------


def test_the_generator_writes_her_file_as_committed_and_reports_its_checks(tmp_path):
    """`build()` raises the checks of Dia-D §1.3 before her file is written and prints the
    generator's report (the lead's notes of 2026-10-29, item 2): her hull as drawn, 448 t against
    the filed 470 t (-5%, recorded and not moved: the filed figure her measuring's body outside 3.5
    pulgadas of plank, the lead's ruling of nudge 30; 498 t, the table's, before it), drawn 3.26 m
    deep at the greatest section to the rabbet against
    her draught of 3.78 m to K; her eleven ports within 0.05 m of the drawn side at their sills
    (ports 1 to 10 her body plan's readings at the sills, among her sections; the bow port's
    half-breadth read off the drawn side, the lead's nudge 59: old, JUDGEMENT, 0.24 m outside it,
    reported and not held); her plain sail and her rope's scale; Luce's chain on her
    particulars; each fit's pieces, broadside, men at the guns of a side and weight of guns; the
    quarter bill's trimmers; and her idlers by trade. Her file comes out as it stands."""
    said = _probe(REPORT_PROBE, str(tmp_path)).stderr
    assert (ROOT / HER).read_bytes() == (tmp_path / Path(HER).name).read_bytes()
    drawn = "corvette-20: the hull as drawn (freesail/ship/form.py):"
    assert f"{drawn} drawn displacement 448 t against the filed 470 t (-5%)." in said
    assert f"{drawn} drawn 3.26 m deep at the greatest section (x 1.26)" in said
    assert (
        "off the half-breadth by +0.00, -0.02, +0.00, +0.00, +0.00, +0.00, +0.00, +0.00, +0.00, "
        "+0.00, +0.00, +0.00 m; the 11 measured each within 0.05 m." in said
    )
    # her spanker as her spars carry it (the owner's decision D-s2): old 1054 m2 and 0.816
    assert (
        "corvette-20: plain sail 1038 m2 against the frigate-36's 1584; her rope's scale 0.810."
        in said
    )
    assert "corvette-20: the main mast 71.4 ft heel to head (21.77 m)" in said
    for fit, pieces, lb, men, tonnes in (
        ("danish 1807", 20, 256, 44, 18.6),
        ("as captured 1809", 20, 240, 40, 13.2),
        ("carronadas de a 30 1810", 20, 300, 40, 17.4),
        ("1817", 24, 198, 62, 28.3),
    ):
        assert (
            f"corvette-20: the fit '{fit}', {pieces} pieces, a broadside of {lb} lb, {men} at the "
            f"guns of a side, {tonnes} t of guns." in said
        )
    assert (
        "corvette-20: the quarter bill's trimmers 29 (forecastle 5, fore_top 7, main_top 8, "
        "mizzen_top 4, afterguard 5), 13 small-arms men and 38 boarders." in said
    )
    assert (
        "corvette-20: her idlers by trade, carpenter's crew 3, sailmaker's crew 2, cooper 1, "
        "armourer 0, cook 1, steward 2, servant 4, surgeon's mate 1, clerk 0, master-at-arms's "
        "party 2." in said
    )


def test_her_table_holds_its_arithmetic_and_her_checks_raise_in_words():
    """Dia-D §1.3: the table's two bodies sum to its total and differ by its difference; Winfield's
    metres within 0.01 m of the table's pies at the book's pie; every mast's heel between K and the
    deck over it; her midship lee port at 21.1 deg and every sill on her side. Each raised in words
    when a figure of it is put wrong (never an `assert`, which `python -O` strips): a body's libras,
    Winfield's breadth, the main mast's heel above her deck, the midship port's sill."""
    got = json.loads(_probe(MODULE_PROBE).stdout)
    assert [got[k] for k in ("table", "winfield", "masts", "ports")] == ["held"] * 4
    assert "do not sum to its total" in got["table wrong"]
    assert "not within 0.01 m of Winfield's 9.1" in got["winfield wrong"]
    assert "her main mast's heel stands at z 1.4 m, not between K under it" in got["masts wrong"]
    assert "her midship lee port dips at" in got["ports wrong"]
    # Luce's chain on her measured waterline and Winfield's breadth (Dia-D §4.1, 2026-11-20): the
    # main (113.1 + 29.7) / 2 = 71.4 ft, every spar the frigate-36's times 0.8145; the masts beside
    # Steel's 20-gun column, 72, 64 and 61 ft (Pages §7), the main yard 19.79 m beside Steel's
    # 19.20
    assert got["main_len_ft"] == pytest.approx(71.41, abs=0.01)
    assert got["scale"] == pytest.approx(0.8145, abs=0.0001)
    assert got["masts_ft"] == {"fore": 64.3, "main": 71.4, "mizzen": 62.8}
    assert got["main_yard_m"] == 19.79


def test_her_notes_carry_no_figure_a_rule_computes():
    """The lead's notes of 2026-10-29, item 2: no rating's figure and no bowline's size in her
    notes, what each rule read staying; and her two tuned figures' notes give their reasons and
    point to their record without the measured heels and helms, which would go stale there."""
    said = [
        line.strip()
        for line in (ROOT / HER).read_text(encoding="utf-8").splitlines()
        if line.strip().startswith("#")
    ]
    assert not [line for line in said if re.search(r" -> [0-9.]+ kN", line)]
    assert not [line for line in said if re.search(r"than the sheet, [0-9.]+ in", line)]
    assert [line for line in said if "Rating: fore.course" in line]
    for key, note in json.loads(_probe(MODULE_PROBE).stdout)["notes"].items():
        assert "docs/dev/TuningNotes.md" in note and " deg" not in note, key


def test_her_file_loads_and_rates_and_her_masts_are_classed_square(spec):
    """Her file loads as the game loads it, with no warning, every spar and line rated; her three
    masts classed square, B3.4's rule naming no part of hers on a schooner's mast (her mizen
    crosses its dry crossjack, Dia-D §4.3), and no mizen course."""
    ship = load_ship(HER)
    assert not [pid for pid in ship.parts if ship.on_schooner_mast(pid)]
    assert spec.warnings == []
    assert all(sp.rating_kn > 0.0 for sp in spec.spars)
    assert all(ln.rating_kn > 0.0 for ln in ship.lines.values())
    assert spec.name == "Diana" and spec.rig == "ship"
    assert {s.id for s in spec.sails} >= {"mizzen.topsail", "mizzen.spanker", "fore.course"}
    assert "mizzen.course" not in {s.id for s in spec.sails}


# ---------------------------------------------------------------------------
# Her shape (Dia-D §3; Build-Ships.md §5.0-§5.3)
# ---------------------------------------------------------------------------


def test_every_line_of_her_shape_carries_its_rung(doc):
    """Her own plan for every line (Dia-D §3.4), the judgements in each named in its note; her
    sections judged where the water at a port's station is carried between two stations (the
    line's weakest point, Build-Ships.md §5.0 principle 4), and the ends' fullness the default
    rule's. No stern lights filed (the lead's ruling of nudge 32; old: a judged band)."""
    marks = doc["hull"]["profile"]["marks"]
    judged = {k for k, v in marks.items() if v == "judged"}
    assert judged == {"sections_m", "form.fullness"}
    assert "form.stern.lights_m" not in marks
    assert set(marks.values()) == {"sourced", "judged"}


def test_her_profile_is_her_plans_points_and_her_form_a_square_stern_and_a_scroll(doc):
    """Pages §6.2 as filed: K from the post's heel to the knee's foot, the draught's line (D29 (b));
    the deck at side the upper red line, 1.33 m at the middle (ruling 5); eleven ports a side of
    0.83 by 0.66 m and a place over the rail for the 1817 fit's obuses; the stern square, its
    knuckle 3.20 m; the head a scroll (ruling 6)."""
    p = doc["hull"]["profile"]
    assert p["keel_m"] == [[-16.54, -3.91], [14.65, -3.66]]
    assert [17.23, 0.0] in p["stem_m"] and p["stem_m"][-1] == [17.31, 5.09]
    assert p["head_m"][-1] == [20.52, 3.64]
    assert [0.0, 1.33] in p["decks_m"]["upper"]
    triples = p["ports_m"]["upper"]
    assert [t for t in triples if t[0] != -12.09] == PORTS
    assert [t for t in triples if t[0] == -12.09] == [[-12.09, 2.87, 3.45]]
    assert p["port_size_m"]["upper"] == [0.83, 0.66]
    assert p["form"]["stern"] == {
        "type": "square",
        "knuckle_z_m": 3.2,
        "transom_hb_m": [1.95, 1.99],
    }
    assert p["form"]["head"] == "scroll"
    assert doc["hull"]["deck_height_m"] == 1.33


def test_her_hull_is_not_drawn_alike_with_the_frigates_or_the_brigs():
    """Build-Ships.md §5.0 principle 10: no two files draw alike unless they are one class in two
    roles. Her outline abeam differs from the frigate-36's and the brig-sloop's (Dia-D §3.5: she is
    told at a glance from the frigate, taller and stepped, and from the brig-sloop)."""
    from freesail.ship import form

    hers = form.outline(load_spec(HER).hull, "abeam")
    for other in (FRIGATE, "data/ships/brig.yaml"):
        assert form.outline(load_spec(other).hull, "abeam") != hers, other


# ---------------------------------------------------------------------------
# Her guns (Dia-D §5; package 81's checklist)
# ---------------------------------------------------------------------------


def test_her_four_fits_by_their_dates_each_on_her_ports(doc):
    """Dia-D §5.1: the Danish fit of 1807 (sixteen 30-pounder carronades and four long 8s), as
    captured in 1809 (twenty 24-pounder carronades), the plan's own of 1810 and her default
    (twenty 30-pounder carronades), and 1817's (twelve long 12s, eight 30-pounder carronades and
    four 3-pounder obuses as carronades); every gun on a triple of her deck to the centimetre, its
    pounds as her navy named them (the owner's decision 9), numbered from forward."""
    arm = doc["armament"]
    assert arm["default"] == DEFAULT_FIT
    assert tuple(arm["fits"]) == FITS
    triples = {(x, s) for x, s, _ in doc["hull"]["profile"]["ports_m"]["upper"]}
    counts = {}
    for name, fit in arm["fits"].items():
        guns = fit["guns"]
        assert all((g["x_m"], g["height_m"]) in triples for g in guns), name
        assert all(g["deck"] == "upper" and g["place"] == "broadside" for g in guns), name
        counts[name] = Counter((g["kind"], g["pounder"]) for g in guns)
        numbers = [g["number"] for g in guns if g["side"] == "starboard"]
        xs = [g["x_m"] for g in guns if g["side"] == "starboard"]
        assert numbers == list(range(1, len(numbers) + 1)) and xs == sorted(xs, reverse=True)
    assert counts == {
        "danish 1807": Counter({("carronade", 30): 16, ("long", 8): 4}),
        "as captured 1809": Counter({("carronade", 24): 20}),
        "carronadas de a 30 1810": Counter({("carronade", 30): 20}),
        "1817": Counter({("long", 12): 12, ("carronade", 30): 8, ("carronade", 3): 4}),
    }


def test_the_builders_checklist_draws_every_gun_of_hers():
    """Package 81's checklist (Build-Ships.md §6's postscript): `tools/check_viewer_guns.py` on her
    file is clean, every fit's port guns on their ports and the 1817 fit's after obuses over the
    rail; the bow port empty in her first three fits."""
    done = subprocess.run(
        [sys.executable, "tools/check_viewer_guns.py", HER],
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert done.stdout.rstrip().endswith("clean")
    assert "fit '1817': 24 guns: 22 port, 2 over the rail" in done.stdout
    assert done.stdout.count("empty ports a side: upper 1") == 3


@pytest.mark.parametrize("fit", FITS)
def test_each_fit_loads_and_fills_its_magazine(doc, fit):
    """Each fit loads as a scenario names it and its magazine is filled for its guns: every
    calibre's cartridges and shot (Table No. 29's charge where it names the gun, its kind's share
    where it does not: a 30-pounder carronade, an 8 and a 3)."""
    ship = load_ship(HER, fit=fit)
    mag = doc["armament"]["fits"][fit]
    calibres = {(g["kind"], g["pounder"]) for g in mag["guns"]}
    for kind, pounder in calibres:
        assert mag["cartridges"][kind][pounder] > 0, (fit, kind, pounder)
        assert mag["charges"][kind][pounder] > 0.0, (fit, kind, pounder)
    assert len(ship.guns) == len(mag["guns"])


# ---------------------------------------------------------------------------
# Her company and her people (Dia-D §6)
# ---------------------------------------------------------------------------


def test_her_company_is_167_with_fifty_soldiers_and_spanish_names(doc):
    """Dia-D §6.1: 167 (Winfield et al. 2023, p. 930), ten posts, her soldiers the regulation of
    1788's fifty for her rate, the other stations the frigate-36's shares of the rest; her names
    the spanish list (N1), which reads as Spain's where a scenario names no nation (truth 7-680)."""
    crew = doc["crew"]
    assert crew["complement"] == 167 and crew["names"] == "spanish"
    assert crew["stations"] == {
        "forecastle": 14,
        "fore_top": 12,
        "main_top": 15,
        "mizzen_top": 7,
        "afterguard": 25,
        "waisters": 18,
        "marines": 50,
        "idlers": 16,
    }
    assert len(crew["posts"]) == 10
    assert sum(crew["idlers_by_trade"].values()) == 16
    assert sum(crew["stations"].values()) + len(crew["posts"]) == 167


def test_her_soldiers_are_spains_kit(doc):
    """Her names list reads as Spain's where a scenario names no nation (`NAMES_TO_NATION`, truth
    7-680), and Spain's kit is the soldiers of the navy's infantry and artillery (data/marines.yaml
    `spanish`, N3; Spain's row naming it since the lead's follow-up): her fifty are Spain's."""
    from freesail.world.nations import NAMES_TO_NATION

    nation = NAMES_TO_NATION[doc["crew"]["names"]]
    kit = load_nations().marines_kit_of(nation)
    assert nation == "spain" and doc["crew"]["stations"]["marines"] == 50
    assert (kit["id"], kit["name"]) == ("spanish", "the Spanish navy's infantry and artillery")


def test_her_ship_files_posts_and_people_agree_with_her_wardroom_file(doc):
    """Her people file (data/people/corvette-20.yaml) names her ship file, binds the captain, the
    officer of the watch, the master and the second officer by role, and its posts and drawn
    people are her ship file's, in order: the muster and the people agree."""
    people = yaml.safe_load((ROOT / "data/people/corvette-20.yaml").read_text(encoding="utf-8"))
    assert people["ship"] == HER
    assert set(people["stations"]) == {
        "captain",
        "officer of the watch",
        "master",
        "second officer",
    }
    posts = [e["role"] for e in people["wardroom"] if e.get("post")]
    assert [p["post"] for p in doc["crew"]["posts"]] == posts
    drawn = [(e["role"], e["drawn"]["station"]) for e in people["wardroom"] if e.get("drawn")]
    assert [(p["role"], p["station"]) for p in doc["crew"]["people"]] == drawn
    assert sum(1 for e in people["wardroom"] if e.get("messenger")) == 1


QUARTERS = {
    "danish 1807": (10, 44, 18),
    "as captured 1809": (10, 40, 10),
    "carronadas de a 30 1810": (10, 40, 10),
    "1817": (12, 62, 30),
}


@pytest.mark.parametrize("fit", FITS)
def test_at_quarters_every_crew_of_every_fit_is_manned(fit):
    """Dia-D §6.1: her builder measures whether every crew is manned, the 1817 fit's twelve long
    12-pounders among them. `Quarters.beat` at seed 7 off Cartagena (crew/quarters.py): every
    numbered crew of every fit manned whole, her soldiers at the carronades (the engine's rule:
    marines serve carronades and no long gun) and the rest of them kept in their division; the
    1817 fit's twelve crews want 62, 20 of them soldiers at its carronades and obuses (21 before
    its long guns went forward, nudge 32)."""
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(37.5, -0.9, HER, fit=fit)
    w.run(10)
    w.submit("beat to quarters")
    w.run(30)
    q = quarters_of(w.ship)
    crews, wanted, kept = QUARTERS[fit]
    assert len(q.crews) == crews
    assert sum(gc.wanted for gc in q.crews.values()) == wanted
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())
    said = [e.text for e in w.log if e.kind == "crew.quarters"]
    assert len(said) == 1 and f"the marines {kept}." in said[0]
    assert "Not hands enough" not in said[0]
    assert not [e for e in w.log if e.kind == "order.rejected"]


def test_every_evolutions_want_against_her_watches_is_listed():
    """Dia-D §6.2: every evolution of data/evolutions/ (the registry's 113), its crew line asked
    of her watch on deck alone by night, through the muster's own request (`crew.hands`): her
    watches are 71 and 70 (46 and 45 seamen with 25 soldiers each, package 119's rule for the odd
    hands), and the request takes any idle hand on deck, its stations ranked first; so every one
    of the 85 numbered evolutions is manned whole by either watch, none calls all hands for too
    few and none waits; the other 28 are all hands' work by their files. Old: 110, 83 and 27,
    before the package's A5 and A6 (`take_in_pole` and `furl_pole`, numbered) and A1a (the
    whole lateen's `change_lateen`, all hands); no other evolution's answer moved. Her design's
    "the anchor's twelve forecastle hands against her watch's seven" reads by station: the
    request makes up the twelve from the watch's other hands."""
    spec = load_spec(HER)
    evos = load_directory()
    assert len(evos) == 113  # 110 before the package's A1a and A5-A6
    by = {}
    for watch in (Watch.STARBOARD, Watch.LARBOARD):
        crew = muster(spec.crew, Rng(7).stream("muster"))
        counts = Counter(s.station.value for s in crew.sailors if s.watch is watch)
        by[watch.value] = sum(counts.values())
        for name, evo in evos.items():
            crew = muster(spec.crew, Rng(7).stream("muster"))
            deck = [s for s in crew.sailors if s.watch is watch or s.station.value == "quarterdeck"]
            want = hands.CrewRequest.from_mapping(evo.crew)
            aloft = any(st.aloft for st in evo.steps)
            if want.all_hands:
                said = "all hands"
            elif hands.too_few_on_deck(crew, deck, want, aloft, posts=True):
                said = "too few"
            else:
                said = hands.request(crew, deck, "x", want, None, aloft=aloft, posts=True).outcome
            by.setdefault(said, set()).add(name)
    assert by["starboard"] == 71 and by["larboard"] == 70
    assert set(by) == {"starboard", "larboard", "all hands", hands.ENOUGH}
    assert len(by["all hands"]) == 28 and len(by[hands.ENOUGH]) == 85  # 27 and 83 before
    assert {"tack", "wear", "weigh_anchor", "clear_for_action"} <= by["all hands"]
    assert {"let_go_anchor", "heave_to", "fill_away", "back_anchor"} <= by[hands.ENOUGH]


# ---------------------------------------------------------------------------
# Her rows: her description, rank and words (Dia-D §8, §12)
# ---------------------------------------------------------------------------


def test_her_description_in_her_file_and_through_the_index(doc):
    """Dia-D §8.1: the tops make her out "a ship", the glass "a corvette, flush-decked, eleven ports
    a side"; her default fit; her roles a King's ship's and a cruiser's. The index's row is her
    file's, and the scenario's words name her."""
    d = doc["ship"]["descriptions"]["corvette"]
    assert (d["rig"], d["what"], d["fit"], d["roles"]) == (
        "a ship",
        "a corvette, flush-decked, eleven ports a side",
        DEFAULT_FIT,
        ["kings-ship", "cruiser"],
    )
    row = S.description("corvette")
    assert row["file"] == HER and row["what"] == d["what"] and row["rig"] == "a ship"
    for words in ("a corvette", "corvette", "a ship-sloop", "ship-sloop", "a ship sloop"):
        assert S.description_key(words) == "corvette", words
    # qualified by a nation (the lead's nudge 78: "a Spanish ship sloop" named none, where "a
    # ship-sloop" and "a French corvette" did, her rows wanting the bare "ship sloop")
    qualified = ("ship sloop", "a Spanish ship sloop", "a Spanish ship-sloop", "a French corvette")
    for words in qualified:
        assert S.description_key(words) == "corvette", words
    assert S.description_key("a sloop of war") == "brig-sloop"


def _her_reading_world(nation: str):
    from datetime import datetime

    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    sc = Scenario(
        start_time=datetime(1810, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth"],
        nation=nation,
    )
    return make_world(7, HER, sc)


def test_her_reading_names_her_once_and_her_class_with_one_article():
    """The ship reading's first line, to the player and in every station's brief (the lead's
    nudge 78): her era note's first clause, her name taken out, her rig after it. Old, her note
    opening "The Diana, a light frigate", it read "Diana, a a light frigate of the Danish navy"."""
    from freesail.api import readings as R

    w = _her_reading_world("spain")
    first = R.ship_words(w).split(" Her guns: ")[0]
    assert first == (
        "The ship: Diana, a light frigate of the Danish navy built at Copenhagen in 1804, taken "
        "by Spain at Cartagena in September 1809 and kept as a corvette to 1832, ship-rigged; a "
        "ship of the Spanish navy."
    )
    assert w.submit("the ship").text.startswith(first)


def test_no_committed_ships_reading_holds_a_doubled_article():
    """Every committed file's class words, as the ship reading serves them (the lead's nudge 78)."""
    from freesail.api.readings import ship_class_words

    doubled = re.compile(r"\b(a|an|the)\s+(a|an|the)\b", re.IGNORECASE)
    files = sorted((ROOT / "data" / "ships").glob("*.yaml"))
    assert len(files) == 19
    for path in files:
        spec = load_spec(path)
        words = ship_class_words(spec, spec.name)
        assert words and not doubled.search(words), (path.name, words)


def test_her_rank_is_a_frigates_at_the_rigs_distance_and_the_brig_sloops_made_out():
    """Dia-D §8.2: "a ship" at the rig's distance ranks her 3, a frigate's class (held as designed
    by the lead's nudge 32, Dia-D §17.2 item 1); made out, "a corvette", 2, the brig-sloop's; her
    file's size 2."""
    assert captains.size_of_words("a ship") == 3
    assert captains.size_of_words("a corvette, flush-decked, eleven ports a side") == 2
    assert captains.SIZE_RANK["corvette"] == 2
    assert captains.size_of_file(HER) == 2


# ---------------------------------------------------------------------------
# Her six truths (Dia-D §14), 7-660 to 7-665, drafted here
# ---------------------------------------------------------------------------


def test_truth_7_660_her_particulars_hold_her_sources(doc):
    """Package 90, her builder (Dia-D §14, truth A), drafted in `tests/test_diana.py`. Her plan's
    table, 124 by 32 1/2 by 16 pies, is 34.55 by 9.06 by 4.46 m at the book's pie, and its 540
    toneladas 691 libras 498.0 t at its libra, recorded beside her mass; she floats at 3.78 m, the
    mean to K on the arrowed line as drawn, 3.91 m aft and 3.65 m forward (the lead's ruling 1),
    her mass the body drawn to that line outside the plank, 465.6 to 473.6 t at 3 to 4 pulgadas,
    the middle filed, 470 t (the lead's ruling of nudge 30; Pages §4.3); her lateral area the
    measured 122.2 m2 (ruling 4); her waterline 34.47 m; eleven ports a side at the plan's sills
    (Pages §5.7); her four fits by date. Her module's particulars give the metres and the table's
    mass from the table's own units, and her file the rulings' figures."""
    got = json.loads(_probe(MODULE_PROBE).stdout)
    assert [round(got[k], 2) for k in ("length", "beam", "depth")] == [34.55, 9.06, 4.46]
    assert got["table_kg"] == round((540 * 2000 + 691) * LIBRA_KG, -3) == 498000.0
    assert got["displacement"] == round((465.6 + 473.6) / 2.0, 0) * 1000.0 == 470000.0
    hull = doc["hull"]
    assert hull["displacement_kg"] == 470000.0
    assert hull["draught_m"] == 3.78 and hull["length_waterline_m"] == 34.47
    assert hull["beam_m"] == 9.06 and hull["lateral_area_m2"] == 122.2
    (x0, z0), (x1, z1) = hull["profile"]["keel_m"]
    assert round(z0 + (z1 - z0) * (0.0 - x0) / (x1 - x0), 2) == -3.78  # K at the middle
    assert [t for t in hull["profile"]["ports_m"]["upper"] if t[0] != -12.09] == PORTS
    assert tuple(doc["armament"]["fits"]) == FITS


@pytest.mark.parametrize(("wind_kn", "off"), [(24.0, 124.0), (25.0, 118.0), (27.0, 112.0)])
def test_truth_7_661_meyers_speed_with_the_wind_abaft_the_beam_in_a_fresh_breeze(wind_kn, off):
    """Package 90, her builder (Dia-D §14, truth B), drafted in `tests/test_diana.py`. Her captain
    of 1807, Meyer: 10 to 11 knots with the wind two or three points abaft the beam in a fresh
    breeze (Roos 1957 p. 94: Dia §6). With the wind 112 to 124 degrees off in 24 to 27 knots, under
    the sail her book carries in that wind (a King's ship's: plain sail below `shorten_sail_kn`,
    30), she makes 9.5 to 11.5 knots: measured 10.30 to 11.26 (10.28 to 11.29 with the frigate's
    spanker scaled, before the owner's decision D-s2). A case a wind (the five-second line: the
    lead's nudges 34 and 69; old: the three in one test)."""
    from tests.test_known_truths import knots, under_plain_sail

    world = under_plain_sail(HER, 360.0 - off, wind_kn)
    assert 9.5 <= knots(world) <= 11.5, (wind_kn, off, knots(world))


@pytest.mark.parametrize("off", [66.0, 90.0])
def test_truth_7_662_she_is_stiff_as_her_captain_said(off):
    """Package 90, her builder (Dia-D §14, truth C), drafted in `tests/test_diana.py`. Close-hauled
    and abeam under plain sail in 22 knots she heels no more than 1.15 times the frigate-36 does
    (measured at her GM of 1.75: 8.17 against 7.34 degrees close-hauled, 1.11; 12.63 against
    11.30 abeam, 1.12; 8.10 and 12.61 with the frigate's spanker scaled, before the owner's
    decision D-s2), and her midship lee port stays open (it shuts at 18.5 degrees: truth
    7-665). A case a heading off the wind (old: the two in one test)."""
    from tests.test_known_truths import reading, under_plain_sail

    hers = reading(under_plain_sail(HER, 360.0 - off, 22.0))["heel"]
    frigates = reading(under_plain_sail(FRIGATE, 360.0 - off, 22.0))["heel"]
    assert hers <= 1.15 * frigates, (off, hers, frigates)
    assert hers < 18.5, off


@pytest.mark.parametrize("off", [66.0, 90.0])
def test_truth_7_663_she_steers_well(off):
    """Package 90, her builder (Dia-D §14, truth D), drafted in `tests/test_diana.py`, restated as
    measured (the owner's decision D-s2; the lead's nudges 61 and 62). In 15 knots her helm
    close-hauled is within half a degree of amidships, and with the wind abeam she carries 1 to 3
    degrees of weather helm (measured at her `clr_x_m` of 2.65: -0.33 and 1.54; the frigate-36's
    1.31 and 1.99). Old: Meyer's "steers splendidly" read as 0.5 to 3 degrees of weather helm
    close-hauled, met at 0.82 and 2.02 with the frigate's spanker scaled (111 m2, `clr_x_m` 2.8).
    Why: the spanker her spars carry by her note's rule is 95 m2, and with it no `clr_x_m` gives
    her that weather helm close-hauled and her tacks too (her report's §10.1); the owner chose the
    sail and her tacks. **Owed with package 125** (the moment of the haul, the lead's nudge 67):
    her `clr_x_m` and her helm measured again, and truth D back to its first band if she then
    holds it. A case a heading off the wind (old: the two in one test)."""
    from tests.test_known_truths import reading, under_plain_sail

    helm = reading(under_plain_sail(HER, 360.0 - off, 15.0))["weather_helm"]
    if off == 66.0:
        assert abs(helm) <= 0.5, helm  # old: 0.5 <= helm <= 3.0
    else:
        assert 1.0 <= helm <= 3.0, helm


# Truth E, her going about, as a count across the winds (the owner's word "Join now", Decisions
# Part F, rows D-j and D-j3; the lead's nudges 67 and 70), measured at seed 7 by the truths' helpers
# with the spanker her spars carry and her `clr_x_m` of 2.65: each case her tack's outcome from
# 290, 292.5 and 295 degrees, and for a tack made its band in seconds. Under all plain sail: she
# stays from every heading in 12 and 15 knots; in 8 she stays from 290 alone, slowly; in 20 and 25
# she is slack in stays and misses from every heading (the tack script's haul a point on the bow,
# the engine's and every ship's: package 125). Measured so on 36b4a3e (her report's §12, §13).
TACK_PLAIN = {
    (8.0, 290.0): ("ship.tacked", 300, 420),  # measured 351 s: slow in light airs
    (8.0, 292.5): ("ship.missed_stays", 0, 900),
    (8.0, 295.0): ("ship.missed_stays", 0, 900),
    (12.0, 290.0): ("ship.tacked", 180, 330),  # 184 to 187 s
    (12.0, 292.5): ("ship.tacked", 180, 330),
    (12.0, 295.0): ("ship.tacked", 180, 330),
    (15.0, 290.0): ("ship.tacked", 180, 330),  # 232 to 238 s
    (15.0, 292.5): ("ship.tacked", 180, 330),
    (15.0, 295.0): ("ship.tacked", 180, 330),
    (20.0, 290.0): ("ship.missed_stays", 0, 900),
    (20.0, 292.5): ("ship.missed_stays", 0, 900),
    (20.0, 295.0): ("ship.missed_stays", 0, 900),
    (25.0, 290.0): ("ship.missed_stays", 0, 900),
    (25.0, 292.5): ("ship.missed_stays", 0, 900),
    (25.0, 295.0): ("ship.missed_stays", 0, 900),
}
TACK_KINDS = ("ship.tacked", "ship.missed_stays", "evolution.failed")


def _idle(world, limit: int) -> None:
    """Run her until no evolution of hers is under way (the runner holds none), trimmed every
    two minutes, at most `limit` seconds."""
    for i in range(limit):
        runner = world.ship.extra.get("evolutions")
        if not getattr(runner, "instances", None):
            return
        world.tick()
        if i % 120 == 60:
            world.submit("trim sails")


def _shortened(wind_kn: float, heading: float):
    """Plain sail set and braced up as the truths settle her, every evolution of it finished;
    then the game's own `shorten sail`, run to its end before the helm is put down."""
    from tests.test_known_truths import close_hauled_on_starboard

    world = close_hauled_on_starboard(HER, knots_=wind_kn, heading=heading)
    _idle(world, 900)
    world.submit("shorten sail")
    world.tick()
    _idle(world, 1500)
    return world


@pytest.mark.parametrize(("wind_kn", "heading"), sorted(TACK_PLAIN))
def test_truth_7_664_she_goes_about_as_a_light_ship_does(wind_kn, heading):
    """Package 90, her builder (Dia-D §14, truth E), drafted in `tests/test_diana.py`, as a count
    across the winds (the lead's nudge 67). **She goes about as a light ship does: under all plain
    sail she stays in a working breeze, and in a fresh breeze she is slack in stays.** From 290,
    292.5 and 295 degrees: in 12 and 15 knots she stays every time, in three to four minutes; in 8
    knots she stays from 290 alone, in about six; in 20 and 25 knots she misses stays from every
    heading, falling off on the old tack. Stayed 7 of 15 (the frigate-36 15 of 15).

    Put about before her sail is set and her way is on her (600 s after `set plain sail`, in the
    game's default gusts, 2 to 3.5 knots of way) she stayed in none of nine in 12 and 15 knots,
    where settled she stays in 11 of 12: the lead's reader's measure (nudge 78), said, not pinned.

    Her tack's band is her own, 180 to 330 s (the lead's ruling of nudge 32): the floor JUDGEMENT,
    a small ship quick in stays; the ceiling about half again her slowest tack as measured then
    (216 s), JUDGEMENT. Truth 10's 285 to 600 s is Luce's five to ten minutes for a frigate of
    42 m. The ground each tack loses is recorded, not asserted. Old: three tacks in 15 knots alone,
    232, 235 and 238 s (206, 215 and 216 with the frigate's spanker scaled), and her wear, now its
    own case below."""
    from tests.test_known_truths import close_hauled_on_starboard, until

    kind, low, high = TACK_PLAIN[(wind_kn, heading)]
    world = close_hauled_on_starboard(HER, knots_=wind_kn, heading=heading)
    world.submit("tack ship")
    done, seconds = until(world, TACK_KINDS, 900)
    assert [e.kind for e in done] == [kind], (wind_kn, heading, [e.text for e in done])
    if kind == "ship.tacked":
        assert low <= seconds <= high, (wind_kn, heading, seconds)
        assert world.ship.dyn.tack == "larboard"


def test_truth_7_664_she_wears_in_truth_11s_band():
    """Truth E's wear, its own case (old: in the one test with her tacks): from close-hauled in 15
    knots she wears in 360 to 720 s, truth 11's band (measured 492 s)."""
    from tests.test_known_truths import close_hauled_on_starboard, wear

    world = close_hauled_on_starboard(HER)
    seconds, _ = wear(world)
    assert 360 <= seconds <= 720, seconds
    assert world.ship.dyn.tack == "larboard"


@pytest.mark.parametrize("heading", [290.0, 292.5, 295.0])
def test_truth_7_664_shortened_in_20_knots_she_stays(heading):
    """Truth E's shortened row, 20 knots (the lead's nudge 70): **shortened, she stays.** The
    game's own `shorten sail` run to its end (her topgallants in and her topsails single-reefed;
    in 20 knots her jib stays on her), then the helm put down: she stays from every heading, 3 of
    3, within her band (measured 186 to 193 s)."""
    from tests.test_known_truths import run, until

    world = _shortened(20.0, heading)
    assert world.ship.sails["jib"].state == SailState.SET
    run(world, 60, trim_every=120)
    world.submit("tack ship")
    done, seconds = until(world, TACK_KINDS, 900)
    assert [e.kind for e in done] == ["ship.tacked"], [e.text for e in done]
    assert 180 <= seconds <= 330, seconds


# 25 knots shortened and no more, as measured (the lead's nudge 70): from 290 she keeps her way and
# stays; from 292.5 and 295 the game's shortening takes in her jib and she gripes past what her
# rudder holds, comes up into the wind and lies there with a knot or two, and the tack is refused
# for want of way (or missed). Her angle off the wind, her way and her weather helm in their bands.
NOT_ABOUT = ("evolution.failed", "ship.missed_stays")  # refused for want of way, or missed
SHORTENED_25 = {
    290.0: {"off": (65.0, 75.0), "kn": (6.0, 9.0), "tack": ("ship.tacked",)},  # 235 s
    292.5: {"off": (30.0, 62.0), "kn": (0.0, 2.5), "tack": NOT_ABOUT},
    295.0: {"off": (30.0, 62.0), "kn": (0.0, 2.5), "tack": NOT_ABOUT},
}


@pytest.mark.parametrize("heading", sorted(SHORTENED_25))
def test_truth_7_664_shortened_in_25_knots_she_gripes_without_her_jib(heading):
    """Truth E's shortened row, 25 knots and no more (the lead's nudge 70): **in a fresh breeze,
    shortened by the game's own order, she wants her jib.** `shorten sail` takes it in there (it
    is loaded to three quarters of its rating, `orders/storm.py`), and with it in she gripes: her
    weather helm past what her small rudder holds, she comes up into the wind and lies there with
    a knot or two of way, and will not go about. Stayed 1 of 3, from 290, where her way held.
    Measured with the shortening finished (her report's §14): from 292.5 and 295, 35 to 59
    degrees off at 1.2 kn, the tack refused ("she has not way enough on her to stay"); her rudder,
    traced from her plan and the least of any ship's, is the cause (with the frigate-36's ratio
    she holds her course)."""
    from tests.test_known_truths import knots, off_wind, run, until

    band = SHORTENED_25[heading]
    world = _shortened(25.0, heading)
    assert world.ship.sails["jib"].state != SailState.SET  # taken in by the game's own order
    run(world, 60, trim_every=120)
    off, way = off_wind(world), knots(world)
    assert band["off"][0] <= off <= band["off"][1], (heading, off)
    assert band["kn"][0] <= way <= band["kn"][1], (heading, way)
    world.submit("tack ship")
    done, seconds = until(world, TACK_KINDS, 900)
    assert [e.kind for e in done][:1] and done[0].kind in band["tack"], [e.text for e in done]
    if done[0].kind == "ship.tacked":
        assert 180 <= seconds <= 330, seconds


@pytest.mark.parametrize("heading", [290.0, 292.5, 295.0])
def test_truth_7_664_shortened_in_25_knots_with_her_jib_set_again_she_stays(heading):
    """Truth E's shortened row, 25 knots with her jib (the lead's nudges 69 and 70): **set the jib
    again and she bears away, gathers way and stays.** After the game's own shortening has taken it
    in, `set the jib` is taken, the jib holds under its rating, she comes back to her course with
    way (6.9 to 8.7 kn measured) and stays from every heading, 3 of 3, within her band (184 to 189
    s); the jib loaded through the tack to under its rating (0.68 to 0.78 measured) and not blown
    out."""
    from tests.test_known_truths import knots, off_wind

    world = _shortened(25.0, heading)
    world.submit("set the jib")
    world.tick()
    _idle(world, 900)
    jib = world.ship.sails["jib"]
    assert jib.state == SailState.SET
    held = 0
    for _ in range(600):
        world.tick()
        held = held + 1 if knots(world) >= 4.0 and off_wind(world) >= 60.0 else 0
        if held >= 60:
            break
    assert held >= 60, (off_wind(world), knots(world))
    start = world.clock.tick
    world.submit("tack ship")
    peak = 0.0
    done: list = []
    for _ in range(900):
        world.tick()
        rating = jib.effective_cloth_rating_kn
        if rating > 0.0:
            peak = max(peak, jib.load_kn / rating)
        done = [e for e in world.log if e.kind in TACK_KINDS and e.tick > start]
        if done:
            break
    seconds = world.clock.tick - start
    assert [e.kind for e in done] == ["ship.tacked"], [e.text for e in done]
    assert 180 <= seconds <= 330, seconds
    assert peak < 1.0 and jib.state == SailState.SET, (peak, jib.state)


def test_truth_7_665_her_midship_lee_port():
    """Package 90, her builder (Dia-D §14, truth F), drafted in `tests/test_diana.py`. Her midship
    port's sill, 1.72 m over a half-breadth of 4.46 m (Pages §5.7), comes to the water at 21.1
    degrees of heel (atan, the lead's ruling 6), and by §7.1's rule (L2: a foot short of the water)
    her lowest lee port, that one, shuts at 18.50 degrees: open half a degree below and, a degree
    above, shut with ports 5, 7 and 4 (18.67, 19.08 and 19.45 by the rule's arithmetic). Her
    design's truth F put the shut at 21.1 deg by L2's rule; the two are not one measure, and both
    are held here (docs/dev/TuningNotes.md, 'Package 90, the Diana')."""
    from tests import test_lee_ports as L

    triples = {round(t[0], 2): t for t in load_spec(HER).hull.profile.ports_m[0][1]}
    _x, sill, half = triples[0.80]
    assert math.degrees(math.atan2(sill, half)) == pytest.approx(21.1, abs=0.05)
    w = L._in_a_sea(HER)
    gid, heel = L._lowest_lee(w, "upper")
    assert heel == pytest.approx(18.50, abs=0.05)
    assert w.ship.guns[gid].x_m == 0.80
    assert L._open_then_shut(w, "upper", 18.50, 0.0, 0) == (0, 4)
    for x, figure in ((-2.06, 18.67), (3.65, 19.08), (-4.93, 19.45)):
        assert L.shut_heel(*triples[x][1:]) == pytest.approx(figure, abs=0.01), x
