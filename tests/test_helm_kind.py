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
# The six files whose notes say tiller (the ground report's §3), and every other a wheel's
TILLER_FILES = {
    "cutter",
    "lugger",
    "smack",
    "topsail-schooner",
    "privateer-schooner",
    "hermaphrodite-brig",
}

# Package 116's words for the wheel, each as its lines gave it before this step: kept exactly
WHEEL_116 = {
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
def test_six_files_steer_by_a_tiller_with_a_note_and_the_rest_by_the_wheel(path):
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
    sources = ("Chapelle 1930 p. 83", "Chapelle 1930 p. 136", "Holdsworth 1874", "Falconer 1780")
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
