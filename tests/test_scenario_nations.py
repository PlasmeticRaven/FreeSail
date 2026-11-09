"""Package 75, the *Prince de Neufchatel*'s stage 0b: the scenario's `nations:` block, parsed
and kept (docs/design/Design-Ship-PrinceDeNeufchatel.md §11.2 and §12.1 item 2; the lead's ruling
on her §17, item 4: "laid at her stage 0b as a parsed and kept block that nothing reads until
her scenario").

A scenario may carry its own wars and letters of marque, `nations: {as_of, wars,
letters_of_marque, source}`, for a day the nations table's June 1805 does not hold.
`world/scenarios.py` reads it and validates its nations as `nation:` is (by data/nations.yaml's
ids, names and adjectives), refusing a block that is wrong in words; the World's `Scenario` keeps
it (`Scenario.nations`) through the save's dict, the checkpoint's pickle and the file written
again. Nothing reads it: a World made from a scenario carrying it has the table's wars, the
replacement of the table's wars and letters being her scenario's (B6's). Behaviour-free: no
shipped scenario carries the block, and each loads, saves and pickles as before (measured before
and after the step in scratch, every shipped scenario's pickle, dict, text and author's lines and
four Worlds' checkpoints and saves byte for byte, the rules' fingerprint held; TuningNotes)."""

from __future__ import annotations

import json
import pickle
from pathlib import Path

import pytest

from freesail.core.world import Scenario
from freesail.world.scenarios import (
    ScenarioError,
    load_scenario,
    make_scenario_world,
    read_scenario_text,
    scenario_text,
    write_scenario,
)

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios"

HEAD = (
    "name: a privateer's summer\n"
    "seed: 7\n"
    "start: 1814-08-01T10:00\n"
    "position: {lat_deg: 49.80, lon_deg: -5.30}\n"
    "region: channel-west\n"
    "nation: united-states\n"
    "ship: {file: data/ships/cutter.yaml, heading_deg: 180, speed_kn: 4}\n"
    "wind: {from_deg: 270, knots: 12, gustiness: 0.0, variability: 0.0}\n"
)

# the block in her design's form (§11.2), its nations by name and adjective as well as by id
BLOCK = (
    "# the summer of 1814: the war with the United States, the peace with France\n"
    "nations:\n"
    "  as_of: 1814-08-01\n"
    "  wars:\n"
    "    - between: [Britain, the United States]\n"
    "      since: 1812-06-18\n"
    "      source: James vol. 5 p. 253\n"
    "  letters_of_marque: [American, britain]\n"
    "  source: a test's block, in the design's form\n"
)

KEPT = {
    "as_of": "1814-08-01",
    "wars": [
        {
            "between": ["britain", "united-states"],
            "since": "1812-06-18",
            "source": "James vol. 5 p. 253",
        }
    ],
    "letters_of_marque": ["united-states", "britain"],
    "source": "a test's block, in the design's form",
}


def _file(tmp_path: Path, block: str) -> Path:
    path = tmp_path / "summer.yaml"
    path.write_text(HEAD + block, encoding="utf-8", newline="\n")
    return path


GOOD = {
    "as_of": "1814-08-01",
    "wars": "[{between: [britain, united-states], since: 1812-06-18}]",
    "letters_of_marque": "[united-states]",
    "source": "a test",
}


def _block(**changes: str | None) -> str:
    rows = dict(GOOD, **changes)
    return "nations:\n" + "".join(f"  {k}: {v}\n" for k, v in rows.items() if v is not None)


@pytest.mark.parametrize(
    ("block", "words"),
    [
        ("nations: [britain, france]\n", "nations: a mapping of as_of, wars, letters_of_marque"),
        (_block(peace="[france]"), "nations: 'peace' is not one of as_of, wars"),
        (_block(source=None), "nations: source wanted; the block is the wars and letters"),
        (_block(as_of="August 1814"), "nations, as_of: 'August 1814' is not a day like 1814-08-01"),
        (_block(wars="{britain: united-states}"), "nations, wars: a list of {between: [a, b]"),
        (
            _block(wars="[{between: [britain, france, spain]}]"),
            "nations, wars 1: a war is {between: [a, b], since, source}, between two nations",
        ),
        (
            _block(wars="[{between: [britain, prussia]}]"),
            "nations, wars 1: 'prussia' is not a nation of data/nations.yaml",
        ),
        (
            _block(wars="[{between: [britain, British]}]"),
            "nations, wars 1: a war is between two nations, not britain and herself",
        ),
        (
            _block(wars="[{between: [britain, united-states]}, {between: [American, Britain]}]"),
            "nations, wars 2: the war between united-states and britain is listed already",
        ),
        (
            _block(wars="[{between: [britain, united-states], since: 1815-02-18}]"),
            "nations, wars 1, since: 1815-02-18 is after the block's day, 1814-08-01",
        ),
        (
            _block(wars="[{between: [britain, united-states], declared: 1812-06-18}]"),
            "nations, wars 1: 'declared' is not one of between, since and source",
        ),
        (
            _block(letters_of_marque="united-states"),
            "nations, letters_of_marque: a list of the nations that issue letters of marque",
        ),
        (
            _block(letters_of_marque="[atlantis]"),
            "nations, letters_of_marque: 'atlantis' is not a nation of data/nations.yaml",
        ),
        (
            _block(letters_of_marque="[united-states, American]"),
            "nations, letters_of_marque: united-states is listed already",
        ),
        (
            _block(letters_of_marque="[denmark]"),
            "nations, letters_of_marque: denmark is at war with nobody in the block",
        ),
        (_block(source="''"), "nations, source: where the block's wars and letters are from"),
    ],
    ids=[
        "not a mapping",
        "a key unknown",
        "a key wanted",
        "no day",
        "the wars not a list",
        "three nations",
        "no nation",
        "a nation and herself",
        "a war twice",
        "a war not yet begun",
        "a war's key unknown",
        "the letters not a list",
        "the letters no nation",
        "the letters twice",
        "the letters at war with nobody",
        "no source",
    ],
)
def test_a_wrong_block_is_refused_at_the_load_in_words(tmp_path, block, words):
    """Each wrong block refused by the loader, naming the file, the block and the fault, as a
    wrong `nation:` is."""
    path = _file(tmp_path, block)
    with pytest.raises(ScenarioError) as refused:
        load_scenario(path)
    said = str(refused.value)
    assert said.startswith(f"{path}, ") and words in said, said


def test_an_empty_war_list_and_no_letters_is_peace_with_all(tmp_path):
    """Every peace is an absence: an empty list of wars and of letters is a block of its own."""
    sc = load_scenario(_file(tmp_path, _block(wars="[]", letters_of_marque="[]"))).scenario
    assert sc.nations == {
        "as_of": "1814-08-01",
        "wars": [],
        "letters_of_marque": [],
        "source": "a test",
    }


def test_the_block_is_kept_through_the_save_the_checkpoint_and_the_file_and_read_by_nothing(
    tmp_path,
):
    """Her design's block, its nations by name and adjective, kept by their ids on the World's
    `Scenario`: through the save's dict (and its JSON) and back, the checkpoint's pickle and back,
    and the file written again with nothing changed, byte for byte, or written new in the hand's
    form with the block after `nation:`, loading to the same. And read by nothing: a World made
    from it has the table's June 1805 wars (Britain at war with France, at peace with the United
    States), the block kept on her scenario and in her save."""
    path = _file(tmp_path, BLOCK)
    sf = load_scenario(path)
    sc = sf.scenario
    assert sc.nations == KEPT
    d = sc.to_dict()
    assert d["nations"] == KEPT
    back = Scenario.from_dict(json.loads(json.dumps(d)))
    assert back == sc and back.nations == KEPT
    assert sc.__getstate__()["nations"] == KEPT
    again = pickle.loads(pickle.dumps(sc, protocol=pickle.HIGHEST_PROTOCOL))
    assert again == sc and again.nations == KEPT
    text, fields = read_scenario_text(path)
    assert scenario_text(fields, text) == text
    new = write_scenario(fields, tmp_path / "new" / "summer.yaml")
    lines = new.read_text(encoding="utf-8").splitlines()
    assert lines.index("nation: united-states") < lines.index("nations:") < lines.index("ship:")
    above = lines[lines.index("nation: united-states") : lines.index("nations:")]
    assert any(ln.startswith("# The wars and the letters of marque") for ln in above)
    assert load_scenario(new).scenario.__dict__ == sc.__dict__
    w = make_scenario_world(sf)
    assert w.scenario.nations == KEPT
    assert w.nations.at_war("britain", "france") and not w.nations.at_war(
        "britain", "united-states"
    )
    assert w.nations.wars == w.nations.sailed_with and w.nations.as_of.isoformat() == "1805-06-01"
    assert w.save()["scenario"]["nations"] == KEPT


def test_every_shipped_scenario_is_without_the_block_and_saved_and_pickled_as_before():
    """No shipped scenario carries the block: each loads with `nations` None, which its save's
    dict and its pickled state leave out, so that every save and checkpoint before the step reads
    as it did, and one unpickled from before the field reads the class's None."""
    files = sorted(SCENARIOS.glob("*.yaml"))
    assert len(files) > 25
    for path in files:
        sc = load_scenario(path).scenario
        assert sc.nations is None, path.name
        assert "nations" not in sc.to_dict() and "nations" not in sc.__getstate__(), path.name
    again = pickle.loads(pickle.dumps(sc))
    assert "nations" not in again.__dict__ and again.nations is None and again == sc
    del sc.nations  # a Scenario pickled before the step: the class's default
    assert sc.nations is None and "nations" not in sc.to_dict()
