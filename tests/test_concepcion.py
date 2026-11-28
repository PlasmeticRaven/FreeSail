"""Package 90, the fifth hull: the *Purísima Concepción* class three-decker of the Spanish navy, as
rebuilt at Cádiz (1786 to 1793), in her fits of 1797 and 1809.

Her design is docs/design/Design-Ship-PurisimaConcepcion.md (Con-D), her measuring note
docs/design/ships-design/pages-concepcion.md (Pages, its head the owner's choice of PB-039 and the
lead's rulings of 2026-11-20), and `tools/ships/concepcion.py` writes her one file,
`data/ships/three-decker.yaml`. These are her tests (Con-D §14; Build-Ships.md §14.1), each through
the door the behaviour is met at (Plan-Package90.md §10.1): her file loaded as the game loads it,
an order given as a player gives it, her description and words as a scenario's are read. Her
hull at her line as traced; her three tiers of ports and their places; her drawn side on every
measured port; her guns by deck in both fits; her company by the regulation of 1788 and her bill;
her rows, her words and her rank; her ground tackle, boats, pumps and hold; her rig; her polar
and her handling; and her truths, 7-735 to 7-739, drafted here as Plan-Package90.md §10.1 has
them, for the integrator to move into tests/test_known_truths.py at the close.

The figures quoted as measured were measured at seed 7 on the cloud's build machine (2026-11-28);
the bands are the sources' or judgement where they say so.
"""

from __future__ import annotations

import math
import subprocess
import sys
from pathlib import Path

import pytest

from freesail.ship.loader import load_ship, load_spec
from freesail.ship.profile import interp, ports_of

ROOT = Path(__file__).resolve().parents[1]
HER = "data/ships/three-decker.yaml"
SEVENTY_FOUR = "data/ships/seventy-four.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
FIT_1797 = "concepcion 1797"
FIT_1809 = "concepcion 1809"
FT = 0.3048
GUN_DECKS = ("lower", "middle", "upper")


@pytest.fixture(scope="module")
def her():
    return load_ship(HER)


@pytest.fixture(scope="module")
def spec():
    return load_spec(HER)


def _fit(spec, name):
    return spec.armament.fits[name]


def _broadside(fit):
    """A fit's broadside by 70's rule, one side's broadside guns, in her guns' own pounds."""
    return sum(g.pounder for g in fit.guns if g.place != "broadside" or g.side == "starboard")


# ---------------------------------------------------------------------------
# Her hull at her line as traced (Con-D §2; the lead's rulings 1 to 5 and nudge 33)
# ---------------------------------------------------------------------------


def test_her_hull_is_her_own_plan_at_her_line_as_traced(her):
    """Her length PB-039's 61.26 m post to stem on her line (ruling 3; Winfield's 61.30 within
    0.1%); her beam James's extreme breadth of the San Josef, 54 ft 3 in, 16.54 m; her draught 7.94
    m to K at the middle of her line as traced (ruling 1); her mass her drawn body outside the
    plank at her line, about 4,440 t, inside the ruled 4,421 to 4,473 t (ruling 2); her datum, her
    upper deck at the middle by the 74's method, 5.99 m (nudge 33); PB-039's rudder, 13.3 m2 and a
    span of 8.29 m, and her lateral plane to her line as traced, about 473.5 m2 (ruling 5)."""
    h = her.hull.spec
    assert h.length_waterline_m == 61.26
    assert abs(h.length_waterline_m / 61.30 - 1.0) <= 0.001
    assert h.beam_m == pytest.approx((54.0 + 3.0 / 12.0) * FT, abs=0.01)
    assert h.draught_m == 7.94
    assert h.displacement_kg == 4_440_000
    assert 4_421_000 <= h.displacement_kg <= 4_473_000
    assert h.deck_height_m == 5.99
    assert (h.rudder.area_m2, h.rudder.span_m) == (13.3, 8.29)
    assert h.lateral_area_m2 == 473.5
    assert h.hull_speed_kn == 13.1


def test_her_heights_stand_above_her_line_as_traced_at_their_own_station(her):
    """Ruling 1 and Pages §12.1: K lies 7.94 m under her water at the middle and 8.02 m at the
    post's after face (8.17 on the straight fit), her line as traced being her water; her upper deck
    at the middle stands at her datum within a centimetre (the 74's method: the mean of PB-039's
    pair, 0.055 m under the upper line); her midship lower sill 1.89 m over her water (1.91 over
    L0, the line as traced standing 0.02 m over L0 there), her aftmost lower sill higher by the
    gap aft (2.30 over L0 at x -24.66, about 2.42 over her water)."""
    p = her.hull.spec.profile
    keel = list(p.keel_m)
    assert interp(keel, 0.0) == pytest.approx(-7.94, abs=0.01)
    assert keel[0] == (-30.63, -8.02)
    upper = list(dict(p.decks_m)["upper"])
    assert interp(upper, 0.0) == pytest.approx(5.99, abs=0.01)
    lower = {round(x, 2): (z, hb) for x, z, hb in ports_of(p, "lower")}
    assert lower[0.18] == (1.89, 8.07)
    assert 2.40 <= lower[-24.66][0] <= 2.44


def test_her_three_tiers_of_sixteen_ports_and_her_upper_works_places(her):
    """Con-D §3.3 (ruling 5): fifteen lower ports a side on PB-039 and the sixteenth pair aftmost,
    under the upper tier's aftmost port (ZAZ0100), sixteen middle and sixteen upper; the
    quarterdeck's six a side and the poop's three at ZAZ0100's places, the forecastle's three
    (JUDGEMENT); the ports' sizes PB-039's, the upper works' the 74's quarterdeck's."""
    p = her.hull.spec.profile
    counts = {deck: len(ports_of(p, deck)) for deck in dict(p.ports_m)}
    assert counts == {
        "lower": 16,
        "middle": 16,
        "upper": 16,
        "quarterdeck": 6,
        "forecastle": 3,
        "roundhouse": 3,
    }
    aftmost_lower = min(x for x, _z, _hb in ports_of(p, "lower"))
    aftmost_upper = min(x for x, _z, _hb in ports_of(p, "upper"))
    assert aftmost_lower == aftmost_upper == -28.27
    sizes = {deck: tuple(round(v, 2) for v in wd) for deck, wd in p.port_size_m}
    assert sizes["lower"] == (1.01, 0.93)
    assert sizes["middle"] == (0.91, 0.76)
    assert sizes["upper"] == (0.80, 0.67)
    assert sizes["quarterdeck"] == (0.79, 0.71)


def test_her_drawn_side_stands_on_every_port_of_her_three_tiers(her):
    """Build-Ships.md §5.0 principle 8: her sourced section points are her ports' own triples, so
    the side as drawn (freesail/ship/form.py) stands on every port of her three gun decks within a
    centimetre, and no port was moved to the drawing."""
    from freesail.ship import form

    h = her.hull.spec
    for deck in GUN_DECKS:
        for x, z, hb in ports_of(h.profile, deck):
            assert abs(form.half_breadth_at(h, x, z) - hb) <= 0.01, (deck, x)


# ---------------------------------------------------------------------------
# Her guns by deck (Con-D §5; package 81's checklist)
# ---------------------------------------------------------------------------

BY_DECK = {
    FIT_1797: {
        ("lower", "long", 36): 30,
        ("middle", "long", 24): 32,
        ("upper", "long", 12): 32,
        ("quarterdeck", "long", 8): 12,
        ("forecastle", "long", 8): 6,
    },
    FIT_1809: {
        ("lower", "long", 36): 30,
        ("middle", "long", 24): 32,
        ("upper", "long", 18): 32,
        ("quarterdeck", "long", 8): 4,
        ("quarterdeck", "carronade", 48): 6,
        ("forecastle", "long", 8): 4,
        ("forecastle", "carronade", 48): 2,
        ("roundhouse", "carronade", 24): 6,
    },
}


@pytest.mark.parametrize("name", [FIT_1797, FIT_1809])
def test_her_guns_by_deck_are_her_own_records_in_both_fits(spec, name):
    """Winfield p. 407 (VR-Sp §4, §16): 112 pieces in 1797 and 116 in 1809, by deck as her own
    record gives them; each half summing to the book's broadside in libras, 1,188 and 1,508, her
    pounds as her navy named them (the owner's Dec 9); the obús carried as a carronade of its
    calibre, its note saying obús (Plan §4 row 10); the lower deck's No. 16 empty in both."""
    fit = _fit(spec, name)
    got = {}
    for g in fit.guns:
        key = (g.deck, g.kind, g.pounder)
        got[key] = got.get(key, 0) + 1
    assert got == BY_DECK[name]
    assert len(fit.guns) == {FIT_1797: 112, FIT_1809: 116}[name]
    assert _broadside(fit) == {FIT_1797: 1188, FIT_1809: 1508}[name]
    assert not [g for g in fit.guns if g.deck == "lower" and g.number == 16]
    assert {g.number for g in fit.guns if g.deck == "lower"} == set(range(1, 16))
    assert spec.armament.numbering == "by deck"
    assert all(g.id == f"gun.{g.deck}.{g.number}.{g.side}" for g in fit.guns)


def test_her_guns_weights_and_crews_and_the_obus_said_so(spec):
    """Con-D §5.3, interim, JUDGEMENT: no Spanish weight by calibre being read, an English pattern
    of nearest weight each (Adye 1804 pp. 72, 155), the 36 the English 32's 55 cwt by the shot,
    62.9 cwt; the crews Falconer's and Douglas's (the 36's fourteen judgement). Her 1809 obuses'
    notes say obús, and her file's notes the book's broadside pairs."""
    weights, crews = {}, {}
    for fit in spec.armament.fits.values():
        for g in fit.guns:
            weights[(g.kind, g.pounder)] = g.weight_cwt
            crews[(g.kind, g.pounder)] = g.crew
    assert weights == {
        ("long", 36): 62.9,
        ("long", 24): 49.5,
        ("long", 12): 34.0,
        ("long", 18): 42.0,
        ("long", 8): 24.5,
        ("carronade", 48): 22.25,
        ("carronade", 24): 13.0,
    }
    assert crews == {
        ("long", 36): 14,
        ("long", 24): 11,
        ("long", 12): 7,
        ("long", 18): 9,
        ("long", 8): 6,
        ("carronade", 48): 4,
        ("carronade", 24): 4,
    }
    text = (ROOT / HER).read_text(encoding="utf-8")
    assert "48-pounder obús" in text and "24-pounder obuses" in text
    assert "1,188 libras (1,282 lb)" in text and "1,508 libras (1,627 lb)" in text
    assert "118 pieces" in text  # the ordinance of 1803's, noted beside her 116


def test_check_viewer_guns_is_clean_on_her_file():
    """Package 81's checklist, item 5: every gun on its triple, her empty sixteenth lower pair and
    the 1809 fit's empty quarterdeck port said, the poop's obuses over the rail."""
    run = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "check_viewer_guns.py"), HER],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    out = run.stdout + run.stderr
    assert run.returncode == 0, out
    assert out.strip().endswith("clean"), out
    assert "fit 'concepcion 1797': 112 guns: 112 port" in out
    assert "fit 'concepcion 1809': 116 guns: 110 port, 6 over the rail" in out
    assert "empty ports a side: lower 1, quarterdeck 1" in out


# ---------------------------------------------------------------------------
# Her company, her soldiers and her bill (Con-D §6)
# ---------------------------------------------------------------------------


def test_her_company_is_the_regulation_of_1788s(spec):
    """VR-Sp §15: a 112's 877 by the regulation of 1788, of whom 225 soldiers (168 infantry and 57
    infantry-artillery) in the marines' station; her posts twenty-one (JUDGEMENT on the split, the
    regulation's kinds the check); her idlers sixty by trade; the spanish names list (N1); her own
    839 and the 1809 fit's 1,015 of whom 275 in her notes, the latter a departure."""
    crew = spec.crew
    st = dict(crew.stations)
    assert crew.complement == 877
    assert len(crew.posts) + sum(st.values()) == 877
    assert st["marines"] == 225
    assert st["idlers"] == 60 == sum(dict(crew.idlers_by_trade).values())
    assert len(crew.posts) == 21
    posts = [p.post for p in crew.posts]
    assert posts[:3] == ["captain", "second captain", "first lieutenant"]
    assert sum(1 for p in posts if p.endswith("lieutenant")) == 9
    assert crew.names == "spanish"
    seamen = sum(v for k, v in st.items() if k not in ("marines", "idlers"))
    assert seamen == 571
    text = (ROOT / HER).read_text(encoding="utf-8")
    assert "Her own 839" in text
    assert "1,015, of whom 275 soldiers" in text


def _beaten(fit=None):
    """Her quarters at muster, seed 7, tests/test_brains.py's world (the 74's `_beaten`)."""
    from freesail.crew.quarters import quarters_of
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, HER, **({"fit": fit} if fit else {}))
    w.run(10)
    said = w.submit("beat to quarters")
    w.run(30)
    return w, said, quarters_of(w.ship)


@pytest.mark.parametrize(
    "fit, crews, wanted, trimmers, at_obuses, division",
    [(FIT_1797, 56, 552, 15, 0, 225), (FIT_1809, 58, 582, 13, 28, 197)],
)
def test_every_crew_of_both_fits_is_manned_and_her_soldiers_serve_no_long_gun(
    fit, crews, wanted, trimmers, at_obuses, division
):
    """Con-D §6.1 and §6.3, measured on her file (the lead's ask, her brief): the engine's rule that
    marines serve no long gun leaves no crew of hers empty, but it takes her trimmers: her 571
    seamen, less the 552 at one side's guns of 1797 and four at the wheel, leave 15 (the 74's share
    of her seamen would be 75), and in 1809, the obuses taking 28 of her soldiers first, 13. In
    1797 all 225 soldiers stand in their division, in 1809 197 (the fit's own bill)."""
    from freesail.crew.model import Station
    from freesail.crew.quarters import MARINES, TRIMMERS

    _w, _said, q = _beaten(fit)
    assert len(q.crews) == crews and sum(gc.wanted for gc in q.crews.values()) == wanted
    assert all(len(gc.members) == gc.wanted for gc in q.crews.values())
    soldiers = [
        gc.kind for gc in q.crews.values() for s in gc.members if s.station is Station.MARINES
    ]
    assert soldiers.count("long") == 0
    assert soldiers.count("carronade") == at_obuses
    assert len(q.divisions[MARINES]) == division
    assert len(q.divisions[TRIMMERS]) == trimmers


def test_her_people_file_gives_her_posts_and_her_drawn_people(spec):
    """Con-D §6.6: her people file names her posts in the file's order and draws her pilot's
    mates, a guardiamarina as the captain's messenger, and her soldiers' captain, lieutenant and
    sergeant from her stations."""
    import yaml

    doc = yaml.safe_load((ROOT / "data" / "people" / "three-decker.yaml").read_text("utf-8"))
    posts = tuple(e["role"] for e in doc["wardroom"] if e.get("post"))
    assert posts == tuple(p.post for p in spec.crew.posts)
    drawn = [(e["role"], e["drawn"]["station"]) for e in doc["wardroom"] if e.get("drawn")]
    assert drawn == [
        ("master's mate", "forecastle"),
        ("master's mate", "forecastle"),
        ("midshipman", "afterguard"),
        ("captain of marines", "marines"),
        ("lieutenant of marines", "marines"),
        ("sergeant of marines", "marines"),
    ]
    assert doc["ship"] == HER


# ---------------------------------------------------------------------------
# Her rows, her words and her rank (Con-D §8)
# ---------------------------------------------------------------------------


def test_her_rows_her_words_and_her_rank():
    """Con-D §8.1-§8.3 (package 75's made-out rule): the tops make out "a three-decker" at her
    rig's distance, rigged as a ship, rank 5, a class above the line; the glass her three tiers
    of sixteen; her words and a first rate's name her row, and "a ship of the line" stays the
    74's."""
    from freesail.world import captains as C
    from freesail.world import ships as S

    row = S.DESCRIPTIONS["three-decker"]
    assert row == {
        "file": HER,
        "rig": "a three-decker",
        "what": "a three-decker, sixteen ports a tier",
    }
    assert S.rigged("a three-decker") == "a ship"
    for words in (
        "a three-decker",
        "three-decker",
        "a first rate",
        "a first-rate",
        "a 112",
        "a ship of the line of three decks",
    ):
        assert S.description_key(words) == "three-decker", words
    assert S.description_key("a ship of the line") == "seventy-four"
    assert C.size_of_words("a three-decker") == 5
    assert C.size_of_words("a three-decker, sixteen ports a tier") == 5
    assert C.SIZE_RANK["three-decker"] == 5 > C.LINE_OF_BATTLE_RANK
    d = S.description("three-decker")
    assert d["file"] == HER and d["fit"] == FIT_1797
    assert d["roles"] == ["kings-ship", "commodore"]
    own = S.file_descriptions(HER)["three-decker"]
    assert own["what"] == d["what"] and S._default_fit(HER) == own["fit"]
    assert C.size_of_file(HER) == 5


def test_her_reading_names_her_class_with_one_article():
    """The ship reading's class words, her era note's first clause, her name taken out (the lead's
    nudge 78, the Diana's mend): one article."""
    from freesail.api.readings import ship_class_words

    spec = load_spec(HER)
    assert ship_class_words(spec, spec.name) == (
        "a three-decker of 112 guns of the Spanish navy, the first rate of her class as rebuilt, "
        "ship-rigged"
    )


# ---------------------------------------------------------------------------
# Her ground tackle, boats, pumps and hold (Con-D §7)
# ---------------------------------------------------------------------------


def test_her_ground_tackle_boats_pumps_and_hold(spec):
    """Con-D §7, JUDGEMENT on the 74's: four bowers of 89 cwt (the 74's 67 by her rig's area,
    x 1.32) on seven cables of 24 in, a stream of 21 cwt and a kedge of 10.6; the 74's six boats
    and a second launch; four chain pumps and two hand pumps."""
    anchors = {a.id: a for a in spec.ground_tackle.anchors}
    assert sorted(anchors) == [
        "best_bower",
        "kedge",
        "sheet",
        "small_bower",
        "spare_anchor",
        "stream",
    ]
    assert anchors["best_bower"].weight_kg == pytest.approx(89 * 50.80234544, abs=1.0)
    assert anchors["best_bower"].cable_in == 24.0
    assert len(spec.boats) == 7
    assert sum(1 for b in spec.boats if b.kind == "launch") == 2
    assert len(spec.pumps) == 6


# ---------------------------------------------------------------------------
# Her rig (Con-D §4)
# ---------------------------------------------------------------------------


def test_her_rig_is_the_74s_scaled_on_her_own_masts_places(her):
    """Con-D §4.1-§4.2: her masts at PB-039's places, upright (ruling 5); her main lower mast 108
    ft x 1.15, 124 ft 2 in; her mizen course a lateen cut at the mast on its yard; no driver; her
    yards under the bowsprit; plain sail the 74's eleven."""
    sp = her.spars
    assert [round(sp[f"{m}.mast"].x_m, 2) for m in ("fore", "main", "mizzen")] == [
        23.37,
        -3.47,
        -18.94,
    ]
    assert all(sp[f"{m}.mast"].rake == 0.0 for m in ("fore", "main", "mizzen"))
    text = (ROOT / HER).read_text(encoding="utf-8")
    assert "main lower mast 124 ft 2 in" in text
    course = her.sails["mizzen.course"]
    assert course.cls == "lateen" and course.cut_at_mast
    assert "mizzen.driver" not in her.sails and "mizzen.boom" not in sp
    assert {"spritsail", "sprit_topsail"} <= set(her.sails)
    assert len(her.groups["plain sail"]) == 11


def test_her_polar_lies_between_the_74s_and_the_frigates():
    """Con-D §9 (Brenton, James): abeam in 15 kn she sails between the 74 and the frigate-36, as
    measured: 8.02 kn against 7.87 and 8.19."""
    from freesail.world.ships import polar_of

    def abeam(path):
        p = polar_of(path)
        return p.speeds_kn[p.winds_kn.index(15.0)][p.angles_deg.index(90)]

    assert abeam(SEVENTY_FOUR) < abeam(HER) < abeam(FRIGATE)


# ---------------------------------------------------------------------------
# Her truths, 7-735 to 7-739 (Con-D §14; Plan-Package90.md §10.3), drafted here as states
# ---------------------------------------------------------------------------


def test_truth_7_735_her_particulars_hold_their_sources():
    """Con-D §14, truth a, in the 74's 7-194 form: her length PB-039's 61.26 m, Winfield's rebuilt
    eslora 61.30 within 0.1% (ruling 3); her breadth James's 16.54 m; three gun decks of sixteen
    ports a side, the lower's sixteenth the aftmost and empty; her two fits 112 and 116 pieces,
    their halves summing to Winfield's 1,188 and 1,508 libras; 877 men by the regulation of 1788,
    of whom 225 soldiers, the 1809 fit's note giving the 1803 regulation's 1,015 and 275 and her
    file her own 839; her mass her drawn body, about 4,440 t, with Winfield's 5,167 t in her
    record. States, no digest."""
    spec = load_spec(HER)
    h = spec.hull
    assert h.length_waterline_m == 61.26 and abs(h.length_waterline_m / 61.30 - 1.0) <= 0.001
    assert h.beam_m == 16.54
    assert {d: len(ports_of(h.profile, d)) for d in GUN_DECKS} == dict.fromkeys(GUN_DECKS, 16)
    for name, pieces, libras in ((FIT_1797, 112, 1188), (FIT_1809, 116, 1508)):
        fit = _fit(spec, name)
        assert (len(fit.guns), _broadside(fit)) == (pieces, libras)
        assert not [g for g in fit.guns if g.deck == "lower" and g.number == 16]
    assert spec.crew.complement == 877 and dict(spec.crew.stations)["marines"] == 225
    text = (ROOT / HER).read_text(encoding="utf-8")
    assert "1,015, of whom 275 soldiers" in text and "Her own 839" in text
    assert 4_421_000 <= h.displacement_kg <= 4_473_000
    assert "Winfield's 5,167 t" in text


def _engaged_at_quarters():
    """At quarters, her guns cast loose, a mark engaged to starboard (test_three_decks's world)."""
    from tests.test_brains import world_at

    w = world_at(49.5, -5.5, HER)
    w.run(10)
    said = w.submit("beat to quarters")
    w.run(5)
    w.submit("cast loose the guns")
    w.run(200)
    w.submit("engage a mark four cables on the starboard beam")
    return w, said


def test_truth_7_736_three_gun_decks_at_quarters():
    """Con-D §14, truth b (B7.b and B7.d on three decks, A9): the beat says her lower, middle and
    upper decks' crews in that order, then the quarterdeck's and the forecastle's, every crew of
    her default fit manned (as measured with the regulation's soldiers: none at a long gun);
    "fire the starboard middle deck" names her sixteen starboard 24-pounders; "fire the second
    deck" the same deck; a bare number is refused naming her decks; "the main deck" is refused
    naming her three gun decks."""
    from freesail.combat.guns import battery_of

    w, said = _engaged_at_quarters()
    assert (
        "The lower deck: 15 gun crews, 210 men. The middle deck: 16 gun crews, 176 men. The "
        "upper deck: 16 gun crews, 112 men. The quarterdeck: six gun crews, 36 men. The "
        "forecastle: three gun crews, 18 men." in said.text
    )
    assert "Not hands enough" not in said.text
    fired = w.submit("fire the starboard middle deck")
    assert (
        fired.text == "The starboard middle-deck guns to fire each as soon as it is ready, 16 guns."
    )
    single = battery_of(w.ship).single
    assert {(w.ship.guns[g].deck, w.ship.guns[g].side) for g in single} == {("middle", "starboard")}
    assert {w.ship.guns[g].pounder for g in single} == {24}
    bare = w.submit("fire No. 3 gun")
    assert bare.kind == "order.rejected"
    assert (
        "the lower deck, the middle deck, the upper deck, the quarterdeck and the forecastle"
        in (bare.text)
    )
    main = w.submit("fire the main deck")
    assert main.kind == "order.rejected"
    assert (
        "She has three gun decks, the lower deck, the middle deck and the upper deck" in main.text
    )


def test_truth_7_736_b_a_tack_at_quarters_robs_her_upper_works_and_upper_deck_and_no_lower():
    """Con-D §14, truth b, its tack at quarters (the lead's nudge 97, item 7), in the frigate's
    7-136 form: close-hauled on the starboard tack from 292.5 deg in 15 kn, seed 7. Cleared, she
    tacks in 276 s. At quarters, her guns run out, under `sail before guns` the tack's watch of 398
    is worked first by the 240 of hers idle at quarters, her 15 trimmers and her 225 soldiers in
    their division (her helm, powder, carpenter's crew and surgeon's mates keeping their stations),
    and the bill lends the other 158 by A9's order: the upper deck's crews, Nos. 2
    to 16, the quarterdeck's and the forecastle's, the lighter metal first, and none of her middle
    or her lower deck's, which keep their guns served; she tacks in 276 s. Under `guns before sail`
    nothing is lent, the tack goes short, 240 of 398 (said), and she tacks in 452 s. In a player's
    words: to work her at quarters she robs her guns, her upper deck's first."""
    from tests.test_known_truths import _guns_ready, close_hauled_on_starboard, until

    def tack(at_quarters: bool, priority: str = "sail before guns"):
        w = close_hauled_on_starboard(HER, heading=292.5)
        if at_quarters:
            _guns_ready(w)
            w.run(40)
            w.submit("run out the guns")
            assert w.submit(priority).kind == "guns.priority"
            w.run(120)
        t0 = w.clock.tick
        w.submit("tack ship")
        runner = w.ship.extra["evolutions"]
        inst = next(i for i in runner.instances if i.evo.id == "tack")
        factor = runner._crew_factor(inst, False)
        done, seconds = until(w, ("ship.tacked", "ship.missed_stays"), 1200)
        assert [e.kind for e in done] == ["ship.tacked"], (priority, [e.text for e in done])
        robbed = [e for e in w.log if e.tick > t0 and e.kind == "quarters.robbed"]
        short = [e for e in w.log if e.tick > t0 and e.kind == "evolution.short_handed"]
        return seconds, robbed, short, factor

    cleared, none_robbed, _, _ = tack(False)
    assert not none_robbed and cleared == 276
    sail_first, robbed, short, factor = tack(True)
    assert [r.data["hands"] for r in robbed] == [158], [r.text for r in robbed]
    assert robbed[0].text == (
        "Tacking ship at quarters: 158 hands taken from the upper deck, Nos. 2 to 16, the "
        "quarterdeck, Nos. 1 to 6, and the forecastle, Nos. 1 to 3; the guns go on short-handed."
    )
    assert "middle deck" not in robbed[0].text and "lower deck" not in robbed[0].text
    assert not short and factor == pytest.approx(1.0, abs=1e-3)
    assert sail_first == 276
    guns_first, robbed2, short2, factor2 = tack(True, "guns before sail")
    assert not robbed2
    assert [(s.data["hands_got"], s.data["hands_wanted"]) for s in short2] == [(240, 398)]
    assert short2[0].text == "Only 240 hands to tack ship; there are no more on deck."
    assert factor2 == pytest.approx(398 / 240, abs=1e-3)
    assert guns_first == 452


def test_truth_7_737_her_lower_ports_shut_at_the_heel_her_plan_gives():
    """Con-D §14, truth c, in the 74's 7-195 form: her midship lower port, No. 8 at x +0.18, 1.89 m
    over her water at a half-breadth of 8.07 m, dips at 13.2 deg (13.3 on L0, Pages §5.2; ruling
    5), and by the engine's rule, its sill within a foot of the water (`shot.lee_port_shut`), it
    shuts at 11.3 deg (the 74's lowest at 10.35: her sill 0.32 m higher, her breadth keeping the
    angle within a degree); her lowest middle-deck port shuts at 33.7 deg and her lowest
    upper-deck port at 65.4 deg. On her battery, heeled by hand to starboard and engaged that
    side: open at 11.0 deg, at 11.6 her lee lower tier amidships shut and said once, her middle
    tier open."""
    from freesail.combat import action, ports, shot
    from freesail.combat.guns import battery_of

    p = load_spec(HER).hull.profile
    x, sill, half = next(t for t in ports_of(p, "lower") if t[0] == 0.18)
    assert 13.0 <= math.degrees(math.atan2(sill, half)) <= 13.5
    threshold = math.degrees(math.asin((sill - shot.PORT_SHUT_M) / half))
    assert 11.2 <= threshold <= 11.45, threshold
    middle = min(
        math.degrees(math.asin((z - shot.PORT_SHUT_M) / hb)) for _x, z, hb in ports_of(p, "middle")
    )
    assert 33.5 <= middle <= 34.0, middle
    upper = min(
        math.degrees(math.asin((z - shot.PORT_SHUT_M) / hb))
        for _x, z, hb in ports_of(p, "upper")
        if z - shot.PORT_SHUT_M < hb
    )
    assert 65.0 <= upper <= 66.0, upper
    w, _said = _engaged_at_quarters()
    b = battery_of(w.ship)
    w.ship.drain_notes()

    def shut_at(heel):
        w.ship.dyn.heel = math.radians(heel)
        ports.update(b, action._firer(w, w.ship), w.clock.tick)
        return {g for g in b._shut if w.ship.guns[g].side == "starboard"}

    assert not shut_at(11.0)
    shut = shut_at(11.6)
    assert shut and {w.ship.guns[g].deck for g in shut} == {"lower"}
    lines = [n for n in w.ship.drain_notes() if len(n) == 5 and n[1] == "guns.ports_shut"]
    assert [n[2] for n in lines] == ["The lee lower-deck ports are shut, the sea at their sills."]


def test_truth_7_738_she_sails_as_a_fast_first_rate():
    """Con-D §14, truth d (Brenton via Winfield; James vol. 6 pp. 3-4; Luce): her best speed in 15
    kn at least the 74's and no more than the frigate-36's (measured: 8.02 kn abeam against 7.87
    and 8.19); her tack from truth 10's three headings each no quicker than the 74's from the same
    heading and inside 600 s (measured: 258, 276 and 293 s against the 74's 237, 243 and 258, her
    rudder's greatest angle 25 deg and her helm's lead 6.3 m as tuned: docs/dev/TuningNotes.md);
    she wears in truth 11's six to twelve minutes (503 s; the 74's 499) and lies to in truth 12's
    band, under 1.6 kn and 45 to 65 deg off (1.31 kn, 55 to 64 deg). **Plainly:** Luce's five to
    ten minutes, her brief's band for the tack, is not reached at any helm's lead that keeps her
    from being taken aback getting under way (truth 17's form): the band is the lead's."""
    from freesail.world.ships import polar_of
    from tests.test_known_truths import (
        close_hauled_on_starboard,
        knots,
        off_wind,
        run,
        until,
    )

    def best(path):
        p = polar_of(path)
        return max(p.speeds_kn[p.winds_kn.index(15.0)])

    assert best(SEVENTY_FOUR) <= best(HER) <= best(FRIGATE)
    for heading in (290.0, 292.5, 295.0):
        tacks = {}
        for path in (SEVENTY_FOUR, HER):
            w = close_hauled_on_starboard(path, heading=heading)
            w.submit("tack ship")
            done, seconds = until(w, ("ship.tacked", "ship.missed_stays"), 900)
            assert [e.kind for e in done] == ["ship.tacked"], (path, heading)
            tacks[path] = seconds
        assert tacks[SEVENTY_FOUR] <= tacks[HER] <= 600, (heading, tacks)
    w = close_hauled_on_starboard(HER)
    w.submit("wear ship")
    done, seconds = until(w, ("ship.wore", "evolution.failed"), 1200)
    assert [e.kind for e in done] == ["ship.wore"] and 360 <= seconds <= 720, seconds
    w = close_hauled_on_starboard(HER, speed_kn=5.0)
    w.submit("heave to")
    run(w, 300)
    offs, speeds = [], []
    for _ in range(600):
        w.tick()
        offs.append(off_wind(w))
        speeds.append(knots(w))
    assert max(speeds) < 1.6
    assert all(45.0 <= o <= 65.0 for o in offs), (min(offs), max(offs))


@pytest.mark.pace
def test_truth_7_739_three_of_her_crewed_hold_the_crewed_floor():
    """Con-D §14, truth e, in the 74's 7-196 form (tests/test_known_truths.py), her file in the
    74's place: the frigate about three miles south of the Lizard, her plain sail set and hove to,
    three of the three-decker put one to three miles from her in her squadron under her orders; a
    thousand ticks to settle, then the best of three timed thousands, at the end of each the
    crewed ships at `CREWED_CAP`, every three-decker within `CREWED_NM` of her and in company, and
    no line of an action in her log nor in any of theirs; at least `CREWED_FLOOR_TICKS_S` (60) a
    second on the build machine. Marked `pace`, so that tests/conftest.py routes it to the pace
    run, alone after the rest: measured on the build machine by the coordinating session, its
    figure to be recorded here then (the engine note's three-decker probe, 72 to 75 a second, Eng
    §7)."""
    import time

    from freesail import units
    from freesail.world import crews as K
    from freesail.world import squadrons as Q
    from freesail.world.geo import bearing_and_distance
    from tests.test_bellerophon import OFF_THE_LIZARD, SEVENTY_FOURS_AT
    from tests.test_brains import put, world_at

    w = world_at(*OFF_THE_LIZARD)
    w.submit("set plain sail")
    w.run(900)
    assert w.submit("heave to").kind == "order.accepted"
    goal = "patrolling off the Lizard within 2 miles"
    intent = "keep the station off the Lizard within 2 miles"
    threes = [
        put(w, "three-decker", "britain", where, goal, intent, name=f"S{i}")
        for i, where in enumerate(SEVENTY_FOURS_AT)
    ]
    assert all(v.ship_file == HER for v in threes)
    ours = Q.Squadron(
        id="ours",
        name="our squadron",
        kind="squadron",
        nation="britain",
        members=["the ship"] + [v.id for v in threes],
        goal=goal,
        formation="line ahead",
    )
    w.squadrons.add(ours, w)
    assert ours.commander == "the ship"
    w.run(1000)
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
        assert len(w.vessels.crewed_ids) == K.CREWED_CAP
        for v in threes:
            nm = bearing_and_distance(w.position, v.position)[1] / units.NAUTICAL_MILE
            assert nm <= K.CREWED_NM, (v.name, nm)
            assert v.crew.captain.state == "in company", (v.name, v.crew.captain.state)
    assert not [e.text for e in w.log if e.kind.startswith("action.")]
    for v in threes:
        assert not [e.text for e in v.crew.log.all() if e.kind.startswith("action.")], v.name
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"
