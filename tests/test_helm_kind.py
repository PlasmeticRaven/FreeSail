"""Package 90, A3: the helm's kind (docs/design/Plan-Package90.md §6 A3; the ground report,
docs/design/GroundReport-Package90-2026-11.md §2.2 and §3; docs/dev/TuningNotes.md, "Package
90, A3").

The cause: every line where a helm is shot away, rigged round or mended was the wheel's, so that a
hull steered by a tiller was told her wheel is shot away and mended with new wheel-ropes. Mended
where it lives: the helm's words come from one place keyed on what her file says she steers by
(`evolutions.scripts.HELM_WORDS`, read by `helm_words(ship)` off `HullSpec.helm`), and every line
reads them there: the hit, the refusal, the heave-to's aside, the tackles' lines, the mend's lines,
the order given twice, the work's name in the log, and the captain's reason and mend order.
Here:
- every helm the schema takes has its words, the same lines in each; the wheel's are package
  116's exactly, and the tiller's name no wheel;
- the six tiller files (the cutter, the lugger, the smack, the two schooners and the hermaphrodite
  brig) carry `helm: tiller` with a sourced note, the brig's marked JUDGEMENT with the two draughts
  that would settle it, and the other twelve, the bilander among them, steer by the wheel;
- on each of the six, and on two wheel ships, the helm shot away by the hit itself and mended, line
  by line in her helm's words and no other's, the tackles and the mend in their times as they were;
- the lines no passage reaches in a short run: the tackles not wanted, the mend belayed and
  failing, and the captain's reason, in either helm's words;
- the captain's mend order, the table's (`world/captains.py`'s repairs; built on the lead's word
  of nudge 31, the third line of that file the lead allowed): on a tiller hull he orders the
  spare tiller shipped, and on a wheel ship the wheel repaired, as before.
"""

from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from freesail.api.session import make_world
from freesail.combat import hits
from freesail.core.world import Scenario
from freesail.evolutions import registry
from freesail.evolutions.repair_scripts import RelievingTacklesScript, RepairWheelScript
from freesail.evolutions.runner import gerund_words
from freesail.evolutions.scripts import (
    HELM_LOST_ASIDE,
    HELM_LOST_WORDS,
    HELM_WORDS,
    SCRIPTS,
    helm_words,
)
from freesail.ship.loader import load_ship
from freesail.ship.schema import HELM_KINDS

ROOT = Path(__file__).resolve().parents[1]
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
# The six files whose notes say tiller (the ground report's §3), and the tartane's two (package
# 90, her builder: her design's tiller; old: the six), and every other a wheel's
TILLER_FILES = {
    "cutter",
    "lugger",
    "smack",
    "topsail-schooner",
    "privateer-schooner",
    "hermaphrodite-brig",
    "tartane",
    "coastguard-tartane",
}

# Package 116's words for the wheel, each as its lines gave it before this step: kept exactly
WHEEL_116 = {
    "helm": "the wheel",  # her helm's noun, as a place's words name it (nudge 47)
    "lost": "the wheel shot away",
    "hit": "The wheel is shot away; the helm is lost until the relieving tackles are rove: "
    "'rig the relieving tackles'.",
    "refusal": "The wheel is shot away and the helm does not answer: rig the relieving tackles "
    "('rig the relieving tackles') to steer her from below, or repair the wheel "
    "('repair the wheel').",
    "aside": "the helm not answering, the wheel shot away",
    "tackles_begin": "Rig the relieving tackles! Hands below to the tiller.",
    "tackles_rove": "The relieving tackles are rove to the tiller and manned below: the helm "
    "answers again, steered by the tackles, and more slowly than by the wheel.",
    "mended": "the wheel is repaired",
    "mend": "repair the wheel",
    "mend_begin": "Repair the wheel! The carpenter's crew to the wheel; new wheel-ropes to be "
    "rove.",
    "mend_done": "The wheel is repaired and new wheel-ropes rove: she steers by the wheel again",
    "whole": "the wheel is whole and she steers by it",
    "not_mended": "the wheel not mended",
    "holds": "the wheel",
}
# The tiller's, the lead's ruling of the ground report's draft (nudge 22, "as drafted"), JUDGEMENT
TILLER_A3 = {
    "helm": "the tiller",
    "lost": "the tiller shot away",
    "hit": "The tiller is shot away; the helm is lost until the relieving tackles are rove: "
    "'rig the relieving tackles'.",
    "refusal": "The tiller is shot away and the helm does not answer: rig the relieving tackles "
    "('rig the relieving tackles') to steer her by them, or ship the spare tiller "
    "('ship the spare tiller').",
    "aside": "the helm not answering, the tiller shot away",
    "tackles_begin": "Rig the relieving tackles! Hands aft to the tiller.",
    "tackles_rove": "The relieving tackles are hooked to the stump of the tiller and manned on "
    "deck: the helm answers again, steered by the tackles, and more slowly than by the tiller.",
    "mended": "the spare tiller is shipped",
    "mend": "ship the spare tiller",
    "mend_begin": "Ship the spare tiller! The carpenter's crew aft to the rudder head.",
    "mend_done": "The spare tiller is shipped in the rudder head: she steers by the tiller again",
    "whole": "the tiller is whole and she steers by it",
    "not_mended": "the spare tiller not shipped",
    "holds": "the rudder head",
}


class _Nought:
    """A stream whose every draw is nought: the helm's share of the hit always met, nobody hurt
    (the shot's scale nought)."""

    def random(self) -> float:
        return 0.0


def _shot_away(world) -> None:
    """Her helm shot away by the hit itself (`combat.hits._deck_hit`) on her after deck."""
    ship = world.ship
    keeper = hits._damage(ship)
    aft = -float(ship.hull.length) / 4.0 - 1.0
    hits._deck_hit(ship, keeper, None, None, None, aft, "starboard", 0.0, 1.0, _Nought(),
                   world.clock.tick)  # fmt: skip


def _helm_of(path: Path) -> str:
    return "tiller" if path.stem in TILLER_FILES else "wheel"


# -- the one place ---------------------------------------------------------------------------


def test_every_helm_the_schema_takes_has_its_words_and_the_same_lines():
    assert set(HELM_WORDS) == set(HELM_KINDS)
    assert set(HELM_WORDS["wheel"]) == set(HELM_WORDS["tiller"])


def test_the_wheels_words_are_package_116s_exactly_and_its_two_constants_the_wheels():
    assert HELM_WORDS["wheel"] == WHEEL_116
    assert HELM_LOST_WORDS == WHEEL_116["refusal"] and HELM_LOST_ASIDE == WHEEL_116["aside"]


def test_the_tillers_words_are_as_ruled_and_name_no_wheel():
    assert HELM_WORDS["tiller"] == TILLER_A3
    assert [k for k, v in TILLER_A3.items() if "wheel" in v] == []


def test_a_ship_with_no_hull_spec_is_given_the_wheels_words():
    assert helm_words(object()) is HELM_WORDS["wheel"]


# -- the six files, by the generator ---------------------------------------------------------


@pytest.mark.parametrize("path", SHIP_FILES, ids=[p.stem for p in SHIP_FILES])
def test_the_tiller_files_steer_by_a_tiller_with_a_note_and_the_rest_by_the_wheel(path):
    """The six of A3 and the tartane's two (package 90, her builder: Chapman's plate, her source;
    old: the six, the name `test_six_files_steer_by_a_tiller_...`)."""
    text = path.read_text(encoding="utf-8")
    doc = yaml.safe_load(text)
    ship = load_ship(path)
    helm = _helm_of(path)
    assert ship.spec.hull.helm == helm
    assert helm_words(ship) is HELM_WORDS[helm]
    if helm == "wheel":
        assert "helm" not in doc["hull"]  # the key's default, said nowhere: the bilander's too
        return
    assert doc["hull"]["helm"] == "tiller"
    lines = text.split("\n")
    at = lines.index("  helm: tiller")
    note = lines[at - 1]
    assert note.startswith("  # She steers by a tiller on deck") or note.startswith(
        "  # JUDGEMENT: she steers by a tiller on deck"
    ), note
    # sourced: a book and its page or plate, or the rule's article, and its mark where it is one
    sources = (
        "Chapelle 1930 p. 83",
        "Chapelle 1930 p. 136",
        "Holdsworth 1874",
        "Falconer 1780",
        "Chapman 1768 Pl. LXII",  # the tartane's (package 90; old: the four)
    )
    assert any(src in note for src in sources), note
    assert ("Judgement." in note) or ("JUDGEMENT" in note) or ("Chapelle 1930 p. 83" in note)
    # the key is the hull's, after her existing keys and before her drawn lines
    keys = list(doc["hull"])
    assert keys[-2:] == ["helm", "profile"]


def test_the_hermaphrodite_brigs_tiller_is_judgement_and_names_the_two_draughts_to_settle_it():
    lines = (ROOT / "data/ships/hermaphrodite-brig.yaml").read_text(encoding="utf-8").split("\n")
    note = lines[lines.index("  helm: tiller") - 1]
    assert note.startswith("  # JUDGEMENT:"), note
    assert "Chapelle 1930 p. 136" in note and "Diligente" in note
    assert "ZAZ6177" in note and "ZAZ6179" in note


# -- a helm shot away and mended, in her helm's words --------------------------------------


PASSAGE = [p for p in SHIP_FILES if p.stem in TILLER_FILES or p.stem in ("brig", "bilander")]


@pytest.mark.parametrize("path", PASSAGE, ids=[p.stem for p in PASSAGE])
def test_a_helm_shot_away_and_mended_is_said_in_her_helms_words_alone(path):
    """From the harbour at seed 7, her helm shot away at a minute by the hit itself: the hit, the
    refusals by the order's road and the runner's, the heave-to's aside, the tackles begun, given
    twice and rove, the mend begun and given twice and named as the log names it, belayed, begun
    again and done, and asked for with the helm whole by `repair the wheel` and the four new
    synonyms: each line her helm's, and on a tiller hull no line of the game names a wheel (the
    player's own order echoed apart)."""
    helm = _helm_of(path)
    words, other = HELM_WORDS[helm], HELM_WORDS["wheel" if helm == "tiller" else "tiller"]
    w = make_world(7, str(path.relative_to(ROOT)), Scenario())
    ship = w.ship
    w.run(60)
    n0 = len(w.log)
    _shot_away(w)
    assert ship.extra["helm_lost"] == words["lost"]
    assert hits._damage(ship).minute == [("helm", words["lost"])]
    w.run(1)  # the ship's note reaches the log with the next tick
    (hit,) = [e for e in w.log[n0:] if e.kind == "helm.shot_away"]
    assert hit.text == words["hit"]
    for order in ("steer north", "tack ship", "keep her full"):
        e = w.submit(order)
        assert e.kind == "order.rejected" and e.text.endswith(words["refusal"]), (order, e.text)
    assert SCRIPTS["heave_to"](ship, {}, {})._helm_words() == words["aside"]

    e = w.submit("rig the relieving tackles")
    assert e.kind != "order.rejected", e.text
    w.run(1)  # begun with the next tick, the hands found
    begun = [x.text for x in w.log[n0:] if x.kind == "evolution.started"]
    assert begun == [words["tackles_begin"]], begun
    twice = w.submit("rig the relieving tackles")
    assert twice.text.endswith("The hands are rigging the relieving tackles already."), twice.text
    for _ in range(40):
        w.run(30)
        if not ship.extra.get("helm_lost"):
            break
    (rove,) = [x for x in w.log[n0:] if x.kind == "helm.relieved"]
    assert rove.text == words["tackles_rove"]
    assert ship.extra["helm_by_tackles"] == words["lost"]

    n1 = len(w.log)
    e = w.submit("repair the wheel")
    assert e.kind != "order.rejected", e.text
    w.run(1)
    started = [x for x in w.log[n1:] if x.kind == "evolution.started"]
    assert [x.text for x in started] == [words["mend_begin"]]
    runner = ship.extra["evolutions"]
    (mend,) = [i for i in runner.instances if i.evo.id == "repair_wheel"]
    doing = gerund_words(words["mend"])
    assert (runner._describe(mend), runner.doing(mend)) == (words["mend"], doing)
    twice = w.submit("repair the wheel")
    assert twice.text.endswith(f"The hands are {doing} already."), twice.text
    belayed = w.submit("belay the wheel")
    assert belayed.kind == "work.belayed", belayed.text
    assert belayed.text == (
        f"Belayed {doing}; {words['not_mended']}, and she steers by the relieving tackles still."
    ), belayed.text
    n2 = len(w.log)
    e = w.submit("repair the wheel")
    assert e.kind != "order.rejected", e.text
    for _ in range(80):
        w.run(30)
        if not ship.extra.get("helm_by_tackles"):
            break
    (done,) = [x for x in w.log[n2:] if x.kind == "helm.repaired"]
    assert done.text == f"{words['mend_done']}; the relieving tackles are cast off."
    for order in ("repair the wheel", "repair the tiller", "ship the spare tiller",
                  "ship a spare tiller", "ship a new tiller"):  # fmt: skip
        e = w.submit(order)
        assert e.kind == "order.rejected" and e.text.endswith(words["whole"]), (order, e.text)

    said = [x.text for x in w.log[n0:]]
    for text in said:
        # the order as the player gave it is echoed ("Order: repair the wheel."); nothing else
        spoken = text.split("): ", 1)[-1] if text.startswith("Order not carried out (") else text
        if spoken.startswith("Order: "):
            continue
        for key in ("lost", "hit", "tackles_begin", "tackles_rove", "mend_begin", "whole"):
            assert other[key] not in spoken, (key, text)
        if helm == "tiller":
            assert "wheel" not in spoken, text


@pytest.mark.parametrize("helm", HELM_KINDS)
def test_the_lines_a_short_passage_does_not_reach_are_her_helms_words(helm):
    """The tackles not wanted, the helm mended while they lay held (their standing reason and
    their done line); the mend's two left lines and its failing line as the runner makes it; the
    captain's reason for the tackles, the hit's own words (`ship.extra["helm_lost"]`); and the
    tackles' and the mend's seconds and hands, the files' on either helm (five minutes and six
    hands, half an hour and four), the two holding no gear in common, so that they go on
    together as before."""
    path = ROOT / "data/ships" / ("cutter.yaml" if helm == "tiller" else "brig.yaml")
    words = HELM_WORDS[helm]
    w = make_world(7, str(path.relative_to(ROOT)), Scenario())
    ship = w.ship
    tackles = RelievingTacklesScript(ship, {}, {})
    assert tackles.standing({}) == f"{words['mended']}; the relieving tackles are not wanted"
    tackles.unwanted = True
    mended = words["mended"]
    assert tackles.words()["done"] == (
        f"{mended[0].upper()}{mended[1:]}; the relieving tackles are not wanted."
    )
    repair = RepairWheelScript(ship, {}, {})
    assert repair.work() == words["mend"] and repair.holds() == {words["holds"]}
    assert repair.check({}) == words["whole"]
    assert repair.left_words() == f"{words['not_mended']}, the helm lost as the shot left it"
    w.run(60)
    _shot_away(w)
    runner = ship.extra["evolutions"]
    n0 = len(w.log)
    assert w.captain._helm_first(ship, w.clock.tick)
    said = [x.text for x in w.log[n0:] if str(x.actor).startswith("captain")]
    assert said == [f"By the captain, on passage: rigging the relieving tackles ({words['lost']})."]
    w.submit("repair the wheel")
    (mend,) = [i for i in runner.instances if i.evo.id == "repair_wheel"]
    failed = runner._format(mend, registry.get("repair_wheel").on_fail.log, "a reason")
    assert failed == f"Could not {words['mend']}: a reason."
    (rig,) = [i for i in runner.instances if i.evo.id == "relieving_tackles"]
    assert runner._format(rig, rig.evo.on_start.log) == words["tackles_begin"]
    assert rig.holds & mend.holds == set()
    assert (rig.script.phase_s("reeve"), mend.script.phase_s("mend")) == (300.0, 1800.0)
    hands = {i.evo.id: runner._crew_line(ship, i.evo)["hands"] for i in (rig, mend)}
    assert hands == {"relieving_tackles": 6, "repair_wheel": 4}


@pytest.mark.parametrize("helm", HELM_KINDS)
def test_the_captains_mend_order_is_her_helms(helm):
    """The tackles rove (their end as `RelievingTacklesScript` makes it) and nothing else to
    mend, out of action: the rules captain's repairs give the helm's mend from the one table, said
    in her helm's words ("By the captain, on passage: shipping the spare tiller (steering by the
    relieving tackles)."), and the work begun is the mend, named so."""
    path = ROOT / "data/ships" / ("cutter.yaml" if helm == "tiller" else "brig.yaml")
    words = HELM_WORDS[helm]
    w = make_world(7, str(path.relative_to(ROOT)), Scenario())
    ship = w.ship
    w.run(60)
    _shot_away(w)
    RelievingTacklesScript(ship, {}, {}).end_phase("reeve")
    assert ship.extra["helm_by_tackles"] == words["lost"] and "helm_lost" not in ship.extra
    n0 = len(w.log)
    w.captain._repairs(SimpleNamespace(tick=w.clock.tick, wind_kn=10.0))
    said = [x.text for x in w.log[n0:] if str(x.actor).startswith("captain")]
    doing = gerund_words(words["mend"])
    assert said == [f"By the captain, on passage: {doing} (steering by the relieving tackles)."]
    runner = ship.extra["evolutions"]
    (mend,) = [i for i in runner.instances if i.evo.id == "repair_wheel"]
    assert runner.doing(mend) == doing


# -- the list of nudge 45: the belay by the helm's words -------------------------------------


def _tackles_in_hand(path: Path):
    """From the harbour at seed 7, her helm shot away at a minute and the relieving tackles
    ordered and in hand: no mend in hand or waiting."""
    w = make_world(7, str(path.relative_to(ROOT)), Scenario())
    w.run(60)
    _shot_away(w)
    w.run(1)
    assert w.submit("rig the relieving tackles").kind != "order.rejected"
    w.run(2)
    runner = w.ship.extra["evolutions"]
    assert [i.evo.id for i in runner.instances] == ["relieving_tackles"]
    return w


@pytest.mark.parametrize("helm", HELM_KINDS)
def test_a_mend_not_in_hand_is_named_as_her_helm_names_it(helm):
    """Nudge 45, item 1. With the tackles in hand and no mend, a belay of the mend by any of its
    words is refused, naming the mend not in hand as the log would name it once begun, by her
    helm (`Script.work_of`, the one table). Old: on a tiller hull "Nothing in hand or waiting is
    repairing the wheel.", the vocabulary's verb, whatever words she was given."""
    path = ROOT / "data/ships" / ("cutter.yaml" if helm == "tiller" else "brig.yaml")
    doing = gerund_words(HELM_WORDS[helm]["mend"])
    for order in ("belay shipping the spare tiller", "belay ship the spare tiller",
                  "belay the wheel", "belay repairing the wheel"):  # fmt: skip
        w = _tackles_in_hand(path)
        e = w.submit(order)
        assert e.kind == "order.rejected", (order, e.text)
        assert e.text.endswith(
            f"Nothing in hand or waiting is {doing}. The work in hand: rigging the relieving "
            "tackles."
        ), (order, e.text)
        assert [i.evo.id for i in w.ship.extra["evolutions"].instances] == ["relieving_tackles"]


def test_on_a_tiller_hull_the_tiller_and_the_spare_tiller_belay_the_mend():
    """Nudge 45, item 2. On a tiller hull `belay the tiller` and `belay the spare tiller` belay
    the mend in hand, as `belay the wheel` does (the vocabulary's work nouns, beside `wheel`), and
    the rest of the work in hand goes on. Old: "There is no such part as the tiller in this ship"
    and "... as the spare tiller in this ship; did you mean the square sail?", the mend going on."""
    for order in ("belay the tiller", "belay the spare tiller", "belay the wheel"):
        w = _tackles_in_hand(ROOT / "data/ships/cutter.yaml")
        assert w.submit("repair the wheel").kind != "order.rejected"
        w.run(2)
        e = w.submit(order)
        assert e.kind == "work.belayed", (order, e.text)
        assert e.text == (
            "Belayed shipping the spare tiller; the spare tiller not shipped, the helm lost as the "
            "shot left it."
        ), (order, e.text)
        assert [i.evo.id for i in w.ship.extra["evolutions"].instances] == ["relieving_tackles"]


def test_on_a_wheel_ship_the_tillers_words_start_and_belay_her_wheels_mend():
    """Nudge 45, item 3: the tiller's words on a wheel ship are accepted, and she answers in her
    own. On the brig, the tackles in hand: each of the tiller's four words starts the wheel's
    mend, begun in the wheel's words; each of the tiller's belays belays it, in the wheel's words;
    and with the wheel whole each is refused as the wheel's (the passage above)."""
    words = HELM_WORDS["wheel"]
    brig = ROOT / "data/ships/brig.yaml"
    for order in ("ship the spare tiller", "ship a spare tiller", "ship a new tiller",
                  "repair the tiller"):  # fmt: skip
        w = _tackles_in_hand(brig)
        n = len(w.log)
        e = w.submit(order)
        assert e.kind == "order.accepted", (order, e.text)
        w.run(2)
        begun = [x.text for x in w.log[n:] if x.kind == "evolution.started"]
        assert begun == [words["mend_begin"]], (order, begun)
        (mend,) = [i for i in w.ship.extra["evolutions"].instances if i.evo.id == "repair_wheel"]
        assert w.ship.extra["evolutions"].doing(mend) == "repairing the wheel"
    for order in ("belay the tiller", "belay the spare tiller", "belay shipping the spare tiller",
                  "belay ship the spare tiller"):  # fmt: skip
        w = _tackles_in_hand(brig)
        assert w.submit("ship the spare tiller").kind != "order.rejected"
        w.run(2)
        e = w.submit(order)
        assert e.kind == "work.belayed", (order, e.text)
        assert e.text == (
            "Belayed repairing the wheel; the wheel not mended, the helm lost as the shot left it."
        ), (order, e.text)


CONNING = ("steady", "steady as she goes", "meet her", "right the helm", "hard a-lee",
           "helm's a-lee", "hard up", "helm a-weather", "up helm", "down helm")  # fmt: skip


def test_the_primer_says_of_a_tiller_what_the_game_does():
    """Nudge 45, item 4: chapters 25, 22 and 2 of the primer each give the hulls steered by a
    tiller a clause, and each says what the game does, run: chapter 25's row and its tackles
    and mend in the tiller's lines (the passage above runs them) and in the mend's half hour of
    its file; chapter 22's hit, the tiller's; chapter 2's conning words, taken on a tiller hull
    in the frigate's words (chapter 2's block is the frigate's), the six it names the six."""
    primer = ROOT / "docs" / "primer"

    def flat(name: str) -> str:
        return " ".join((primer / name).read_text(encoding="utf-8").split())

    words = HELM_WORDS["tiller"]
    ch25 = flat("25-water-wounds-and-the-fight-on-deck.md")
    assert "ship the spare tiller the same where she steers by a tiller:" in ch25
    assert "the tackles hooked to the stump of the tiller and manned on deck" in ch25
    assert "hooked to the stump of the tiller and manned on deck" in words["tackles_rove"]
    assert "the spare tiller shipped in the rudder head, half an hour" in ch25
    assert words["mend_done"].startswith("The spare tiller is shipped in the rudder head")
    mend = yaml.safe_load((ROOT / "data/evolutions/repair_wheel.yaml").read_text(encoding="utf-8"))
    assert mend["timing"]["mend_s"] == 1800
    assert "With the wheel (or the tiller) shot away and no tackles rove she has no helm" in ch25
    ch22 = flat("22-an-action.md")
    hit = "the wheel shot away (or the tiller, in a hull steered by one) loses you the helm"
    assert hit in ch22
    assert words["hit"].startswith("The tiller is shot away; the helm is lost until the relieving")
    ch2 = flat("02-the-wind-and-the-points-of-sail.md")
    six = "the cutter, the lugger, the smack, the two schooners and the hermaphrodite brig"
    assert f"(to the tiller, in the same words, in {six})" in ch2
    assert TILLER_FILES == {"cutter", "lugger", "smack", "topsail-schooner",
                            "privateer-schooner", "hermaphrodite-brig"}  # fmt: skip
    said: dict[str, list[str]] = {}
    for stem in ("frigate-36", "cutter"):
        w = make_world(7, f"data/ships/{stem}.yaml", Scenario())
        w.run(30)
        for order in CONNING:
            e = w.submit(order)
            assert e.kind == "helm.order" and e.text.startswith(f"Helm ordered: {order};"), e.text
            # the words but her heading's and the rudder's side, which are her own
            said.setdefault(order, []).append(e.text.split(";", 1)[1].split(" (")[0])
            w.run(3)
    heading = {"steady", "steady as she goes", "meet her"}
    assert all(a == b for o, (a, b) in said.items() if o not in heading), said
    assert all(a.split(" N")[0] == b.split(" N")[0] for o, (a, b) in said.items()), said


@pytest.mark.parametrize("stem", ["cutter", "brig", "frigate-36"])
def test_the_places_reading_says_where_her_helm_is(stem):
    """Nudge 47 ((a)): `the places` reading describes the quarterdeck by her helm, from the one
    table, in both its forms, the items and the lines described. On the cutter "... keep the deck
    and the tiller is"; on the brig and the frigate the place's own words, byte for byte, as
    `world/places.py` gives them and as they were; every other place as it is. Old: "the wheel
    is" on every ship."""
    from freesail.world.places import PLACES

    w = make_world(7, f"data/ships/{stem}.yaml", Scenario())
    reading = w.readings["places"]
    filed = PLACES["quarterdeck"].description
    assert filed.endswith("keep the deck and the wheel is (Falconer 1780, QUARTER-DECK)")
    tiller = _helm_of(ROOT / "data/ships" / f"{stem}.yaml") == "tiller"
    # the words held literally, so that a wheel ship's case passes on the old code as well
    want = filed.replace("the wheel is", "the tiller is") if tiller else filed
    assert reading["items"]["quarterdeck"]["description"] == want
    assert f"The quarterdeck: {want}." in reading["described"]
    if tiller:
        assert "the wheel" not in " ".join(reading["described"])
        assert want.endswith("keep the deck and the tiller is (Falconer 1780, QUARTER-DECK)")
    others = {p.id: p.description for p in PLACES.values() if p.id != "quarterdeck"}
    assert {k: v["description"] for k, v in reading["items"].items() if k in others} == others
    assert reading["words"] == ", ".join(p.name for p in PLACES.values())
