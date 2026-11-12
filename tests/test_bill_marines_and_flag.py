"""Package 75, the 74's stage 0c: the quarter bill's `marines` and the crew's `flag:`
(docs/design/Design-Ship-Bellerophon.md §12.1, §17.0; the lead's answers to her §17.2, items 1
and 15).

The bill's `marines` is the marines it keeps in their division at the beat, a whole number no
more than the file's marines, refused in words otherwise; the crew's `flag:` is the flag party a
flagship bears beyond her company when a flag is hoisted in her, each a post in the posts' form,
counted in no station and not in the complement. Both are inert: no file carries either, nothing
reads them, and a bill and a crew without them pickle as before them (left out of the pickled
state while empty, read back as the class's plain default), so that a checkpoint written before
them loads as it did.
"""

from __future__ import annotations

import copy
import pickle
from pathlib import Path

import pytest
import yaml

from freesail.ship.loader import load_ship, spec_from_dict
from freesail.ship.schema import (
    FLAG_POST_KEYS,
    QUARTER_BILL_KEYS,
    CrewSpec,
    PostSpec,
    QuarterBillSpec,
    ShipFileError,
)

ROOT = Path(__file__).resolve().parents[1]
SIXTY_FOUR = ROOT / "data" / "ships" / "sixty-four.yaml"
SHIP_FILES = sorted((ROOT / "data" / "ships").glob("*.yaml"))
# the files that carry neither key: every file but the 74's, whose step 4 writes both (her bill's
# marines and her flag party: Design-Ship-Bellerophon.md §6.3, §17.0), held in tests/
# test_bellerophon.py (old: every file on the shelf)
# the files whose bills carry the marines: the 74's since her step 4, the 64's and the razee's since
# the lead's answer of 2026-11-10 at 19:30 (B1's module)
KEYED_FILES = ("seventy-four.yaml", "sixty-four.yaml", "razee-44.yaml")
KEYLESS_FILES = [p for p in SHIP_FILES if p.name not in KEYED_FILES]
# the pickled states' keys before the stage, in their order
BILL_STATE = ["trimmers", "helm", "powder", "priority", "small_arms", "boarders", "filling"]
CREW_STATE = [
    "complement",
    "names",
    "stations",
    "ratings",
    "posts",
    "idlers_by_trade",
    "stores",
    "people",
    "ration",
    "quarter_bill",
]
FLAG = [
    {"post": "rear-admiral"},
    {"post": "flag lieutenant"},
    {"post": "admiral's secretary", "name": "Mr Inglis"},
]


def _doc() -> dict:
    with open(SIXTY_FOUR, encoding="utf-8") as f:
        return yaml.safe_load(f)


def _crew(doc: dict) -> CrewSpec:
    crew = spec_from_dict(doc, "s.yaml").crew
    assert crew is not None
    return crew


def test_the_marines_key_is_the_bills_last_and_the_flags_posts_are_the_posts_form():
    assert QUARTER_BILL_KEYS == (*BILL_STATE, "marines")
    assert FLAG_POST_KEYS == ("post", "name")


@pytest.mark.parametrize("path", KEYLESS_FILES, ids=[p.stem for p in KEYLESS_FILES])
def test_no_file_carries_either_key_and_each_pickles_as_before(path):
    """Inert: every file on the shelf but the 74's, the 64's and the razee's reads no division kept
    and no flag party, and her bill's and her crew's pickled states hold the keys they held before
    the stage, in their order. The 74's file carries both since her step 4 (old: every file on the
    shelf); the 64's and the razee's the marines since the lead's answer of 2026-11-10 at 19:30,
    and no flag."""
    crew = load_ship(path).spec.crew
    if crew is None:
        return
    assert crew.flag == ()
    assert list(crew.__getstate__()) == CREW_STATE
    assert pickle.loads(pickle.dumps(crew)) == crew
    bill = crew.quarter_bill
    if bill is not None:
        assert bill.marines is None
        assert list(bill.__getstate__()) == BILL_STATE
        again = pickle.loads(pickle.dumps(bill))
        assert "marines" not in again.__dict__ and again.marines is None and again == bill


def test_a_bill_and_a_crew_pickled_before_the_stage_read_their_plain_defaults():
    """The 64's bill and crew pickled with the keys they held before the stage. Her bill carries
    the marines since the lead's answer of 2026-11-10 at 19:30 (84): the bill read back is hers
    with none kept."""
    import dataclasses

    crew = load_ship(SIXTY_FOUR).spec.crew
    was_bill = QuarterBillSpec.__new__(QuarterBillSpec)
    was_bill.__dict__.update({k: copy.deepcopy(getattr(crew.quarter_bill, k)) for k in BILL_STATE})
    was_bill = pickle.loads(pickle.dumps(was_bill))
    assert crew.quarter_bill.marines == 84
    assert was_bill.marines is None
    assert was_bill == dataclasses.replace(crew.quarter_bill, marines=None)
    was_crew = CrewSpec.__new__(CrewSpec)
    was_crew.__dict__.update({k: copy.deepcopy(getattr(crew, k)) for k in CREW_STATE})
    was_crew = pickle.loads(pickle.dumps(was_crew))
    assert was_crew.flag == () and was_crew == crew


def test_a_bill_keeps_its_marines_to_the_whole_of_her_marines():
    doc = _doc()
    marines = doc["crew"]["stations"]["marines"]
    for kept in (0, 60, marines):
        doc["crew"]["quarter_bill"]["marines"] = kept
        bill = _crew(doc).quarter_bill
        assert bill.marines == kept
        assert list(bill.__getstate__()) == BILL_STATE + ["marines"]
        again = pickle.loads(pickle.dumps(bill))
        assert again.marines == kept and again == bill


@pytest.mark.parametrize(
    "value, match",
    [
        (-1, "the marines kept in their division is -1; it must be a whole number, not negative"),
        (12.5, "the marines kept in their division is 12.5; it must be a whole number"),
        (True, "the marines kept in their division is True; it must be a whole number"),
        ("ninety", "the marines kept in their division is 'ninety'; it must be a whole number"),
        (85, "keeps 85 marines in their division, but the crew has 84; it cannot keep more"),
    ],
)
def test_a_bills_marines_below_nought_or_beyond_her_marines_are_refused_in_words(value, match):
    doc = _doc()
    doc["crew"]["quarter_bill"]["marines"] = value
    with pytest.raises(ShipFileError, match=match):
        spec_from_dict(doc, "s.yaml")


def test_a_flag_party_is_borne_beyond_her_company_as_posts():
    doc = _doc()
    before = _crew(_doc())
    doc["crew"]["flag"] = copy.deepcopy(FLAG)
    crew = _crew(doc)
    assert crew.flag == (
        PostSpec("rear-admiral"),
        PostSpec("flag lieutenant"),
        PostSpec("admiral's secretary", "Mr Inglis"),
    )
    # counted in no station and not in the complement: her company as filed
    assert crew.complement == before.complement and crew.stations == before.stations
    assert crew.posts == before.posts and crew.seamen == before.seamen
    assert list(crew.__getstate__()) == CREW_STATE + ["flag"]
    again = pickle.loads(pickle.dumps(crew))
    assert again.flag == crew.flag and again == crew
    doc["crew"]["flag"] = []
    assert _crew(doc).flag == () and "flag" not in _crew(doc).__getstate__()


@pytest.mark.parametrize(
    "flag, match",
    [
        ({"post": "rear-admiral"}, "the crew's 'flag' is not a list of posts"),
        (["rear-admiral"], "post #1 of the crew's flag does not say which post it is"),
        ([{"post": "rear-admiral"}, {"name": "Mr Inglis"}], "post #2 of the crew's flag does not"),
        (
            [{"post": "rear-admiral", "station": "quarterdeck"}],
            "post #1 of the crew's flag has 'station', which a post of the flag does not take "
            r"\(post, name\)",
        ),
    ],
)
def test_a_flag_that_is_not_a_list_of_posts_is_refused_in_words(flag, match):
    doc = _doc()
    doc["crew"]["flag"] = flag
    with pytest.raises(ShipFileError, match=match):
        spec_from_dict(doc, "s.yaml")
