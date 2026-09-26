"""The crew model, the muster and the watch bill (spec M3 §2; package 16)."""

from __future__ import annotations

import copy
import random
from datetime import datetime, timedelta
from pathlib import Path

import pytest
import yaml

from freesail.core.clock import Clock
from freesail.core.rng import Rng
from freesail.crew import bill
from freesail.crew.model import (
    RATING_SKILL,
    SEAMAN_STATIONS,
    TOPS,
    Crew,
    Rating,
    Station,
    Watch,
    fatigue_words,
)
from freesail.crew.muster import GIVEN_ABBREVIATIONS, NAMES_PATH, SKILL_SPREAD, muster
from freesail.ship import schema
from freesail.ship.loader import load_ship, spec_from_dict
from freesail.ship.schema import CrewSpec, ShipFileError

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = ROOT / "data" / "ships" / "frigate-36.yaml"
SCHOONER = ROOT / "data" / "ships" / "topsail-schooner.yaml"
DAY = datetime(1805, 6, 1)


def _data(path: Path) -> dict:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def frigate_data() -> dict:
    return _data(FRIGATE)


def _crew(path: Path, seed: int = 7) -> Crew:
    ship = load_ship(path)
    return muster(ship.spec.crew, Rng(seed).stream("muster"), ship_name=ship.name)


@pytest.fixture(scope="module")
def frigate_crew() -> Crew:
    return _crew(FRIGATE)


@pytest.fixture(scope="module")
def schooner_crew() -> Crew:
    return _crew(SCHOONER)


# ---------------------------------------------------------------------------
# the ship files' crew sections
# ---------------------------------------------------------------------------


def test_both_ship_files_carry_a_crew_section():
    frigate = load_ship(FRIGATE).spec
    schooner = load_ship(SCHOONER).spec
    assert isinstance(frigate.crew, CrewSpec) and isinstance(schooner.crew, CrewSpec)
    assert frigate.crew.complement == 264 and frigate.crew.names == "english"
    assert frigate.crew.stations == {
        "forecastle": 28,
        "fore_top": 24,
        "main_top": 30,
        "mizzen_top": 14,
        "afterguard": 50,
        "waisters": 36,
        "marines": 40,
        "idlers": 30,
    }
    assert [p.post for p in frigate.crew.posts] == [
        "captain",
        "first lieutenant",
        "second lieutenant",
        "third lieutenant",
        "master",
        "boatswain",
        "gunner",
        "carpenter",
        "purser",
        "surgeon",
        "sailmaker",
        "master-at-arms",
    ]
    assert frigate.crew.idlers_by_trade["master-at-arms's party"] == 3
    # milestone 3b: the stores list the sail room's sails (spec 3b §6.3), and `spare_sails` is
    # the count of them, derived: Luce's allowance for a frigate, 21 sails
    assert frigate.crew.stores.water_tons == 100 and frigate.crew.stores.spare_sails == 21
    assert len(frigate.crew.stores.sails) == 21
    assert schooner.crew.complement == 40 and schooner.crew.names == "american"
    assert schooner.crew.stations["marines"] == 0 and schooner.crew.stations["main_top"] == 0
    assert [p.post for p in schooner.crew.posts] == ["master", "mate", "boatswain"]
    assert schooner.crew.idlers_by_trade == {
        "cook": 1,
        "steward": 1,
        "carpenter's crew": 1,
        "sailmaker's crew": 1,
    }
    for spec in (frigate, schooner):
        assert sum(spec.crew.stations.values()) + len(spec.crew.posts) == spec.crew.complement
        assert spec.warnings == []


def test_a_ship_file_without_a_crew_has_none_and_no_warning(frigate_data):
    data = copy.deepcopy(frigate_data)
    del data["crew"]
    spec = spec_from_dict(data, "bare.yaml")
    assert spec.crew is None
    assert spec.warnings == []


def test_the_stations_are_the_models_stations():
    assert schema.CREW_STATIONS == tuple(s.value for s in Station if s is not Station.QUARTERDECK)
    assert schema.SEAMAN_STATIONS == tuple(s.value for s in SEAMAN_STATIONS)


def _bad(frigate_data, change) -> str:
    data = copy.deepcopy(frigate_data)
    change(data["crew"])
    with pytest.raises(ShipFileError) as e:
        spec_from_dict(data, "bad.yaml")
    return str(e.value)


def test_stations_and_posts_must_make_the_complement(frigate_data):
    def change(c):
        c["stations"]["waisters"] = 48

    msg = _bad(frigate_data, change)
    assert msg.startswith("bad.yaml: ")
    assert "stations hold 264 and the posts 12, which make 276; the complement is 264" in msg


def test_ratings_must_add_up_to_one(frigate_data):
    def change(c):
        c["ratings"]["able"] = 0.25

    msg = _bad(frigate_data, change)
    assert "ratings add up to 0.95" in msg and "must add up to one" in msg


def test_unknown_station_trade_rating_and_store_are_named(frigate_data):
    def station(c):
        c["stations"]["gunroom"] = 0

    def trade(c):
        c["idlers_by_trade"]["chaplain"] = c["idlers_by_trade"].pop("clerk")

    def rating(c):
        c["ratings"]["boy"] = 0.0

    def store(c):
        c["stores"]["rum_gallons"] = 400

    msg = _bad(frigate_data, station)
    assert "station 'gunroom'" in msg and "forecastle, fore_top" in msg
    assert "trade 'chaplain'" in _bad(frigate_data, trade)
    assert "rating 'boy'" in _bad(frigate_data, rating)
    assert "store 'rum_gallons'" in _bad(frigate_data, store)


def test_other_malformed_crew_sections(frigate_data):
    def trades(c):
        c["idlers_by_trade"]["servant"] = 7

    def complement(c):
        c["complement"] = "many"

    def negative(c):
        c["stations"]["marines"] = -1

    def names(c):
        del c["names"]

    def post(c):
        c["posts"][0] = {"name": "Pellew"}

    def key(c):
        c["morale"] = 1.0

    assert "30 idlers, but 'idlers_by_trade' makes 29" in _bad(frigate_data, trades)
    assert "complement is 'many'" in _bad(frigate_data, complement)
    assert "marines station's number is -1" in _bad(frigate_data, negative)
    assert "missing 'names'" in _bad(frigate_data, names)
    assert "post #1" in _bad(frigate_data, post)
    assert "'morale'" in _bad(frigate_data, key)


# ---------------------------------------------------------------------------
# the names
# ---------------------------------------------------------------------------


def test_the_name_lists():
    data = yaml.safe_load(NAMES_PATH.read_text(encoding="utf-8"))
    assert set(data) == {"english", "american"}
    for lists in data.values():
        assert len(lists["given"]) >= 60 and len(lists["surnames"]) >= 200
        for names in lists.values():
            assert len(set(names)) == len(names)
            assert all(isinstance(n, str) and n.strip() == n and n for n in names)


def test_given_names_are_abbreviated_as_a_muster_book_would(frigate_crew):
    names = [s.name for s in frigate_crew.sailors]
    assert not any(n.split()[0] in GIVEN_ABBREVIATIONS for n in names)
    assert any(n.startswith(("Wm. ", "Jno. ", "Thos. ")) for n in names)
    assert len(set(names)) == len(names)


def test_an_unknown_name_list_is_refused():
    spec = copy.deepcopy(load_ship(SCHOONER).spec.crew)
    spec.names = "french"
    with pytest.raises(ShipFileError, match="'french' names"):
        muster(spec, random.Random(1))


# ---------------------------------------------------------------------------
# the muster
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("path", [FRIGATE, SCHOONER])
def test_muster_gives_the_complement_at_the_stated_stations(path):
    spec = load_ship(path).spec.crew
    crew = _crew(path)
    assert crew.complement == spec.complement
    for name, n in spec.stations.items():
        assert len(crew.by_station[Station(name)]) == n
    assert len(crew.by_station[Station.QUARTERDECK]) == len(spec.posts)
    assert list(crew.posts) == [p.post for p in spec.posts]
    ids = [s.id for s in crew.sailors]
    assert ids == sorted(ids) and len(set(ids)) == len(ids) and ids[0] == "s001"
    assert crew.by_id["s017"].id == "s017"


def test_ratings_are_shared_as_the_file_says(frigate_crew, schooner_crew):
    def count(crew, station=None):
        out = {}
        for s in crew.sailors:
            if s.station in SEAMAN_STATIONS and (station is None or s.station is station):
                out[s.rating] = out.get(s.rating, 0) + 1
        return out

    # 182 seamen at 0.30 / 0.40 / 0.30, by largest remainder
    assert count(frigate_crew) == {Rating.ABLE: 55, Rating.ORDINARY: 73, Rating.LANDSMAN: 54}
    # the topmen from the able and ordinary first, the three tops alike
    for top in TOPS:
        mix = count(frigate_crew, top)
        assert set(mix) == {Rating.ABLE, Rating.ORDINARY}
        assert 0.35 <= mix[Rating.ABLE] / sum(mix.values()) <= 0.50
    # the forecastle from the able; the waisters from the landsmen; the afterguard the rest
    assert count(frigate_crew, Station.FORECASTLE)[Rating.ABLE] >= 26
    assert count(frigate_crew, Station.WAISTERS) == {Rating.LANDSMAN: 36}
    assert count(frigate_crew, Station.AFTERGUARD) == {Rating.ORDINARY: 32, Rating.LANDSMAN: 18}
    assert count(schooner_crew) == {Rating.ABLE: 15, Rating.ORDINARY: 13, Rating.LANDSMAN: 5}
    assert count(schooner_crew, Station.WAISTERS)[Rating.LANDSMAN] == 5


def test_skills_come_from_rating_with_a_small_spread(frigate_crew):
    for s in frigate_crew.sailors:
        deck, aloft = RATING_SKILL[s.rating]
        assert abs(s.skill_deck - deck) <= SKILL_SPREAD + 1e-9
        assert abs(s.skill_aloft - aloft) <= SKILL_SPREAD + 1e-9
        assert 0.0 <= s.skill_deck <= 1.0 and 0.0 <= s.skill_aloft <= 1.0
        assert s.fatigue == 0.0 and s.fit and s.at is None and not s.turned_up
    able = [s.skill_deck for s in frigate_crew.sailors if s.rating is Rating.ABLE]
    assert len(set(able)) > 10  # two able seamen are not identical
    assert abs(sum(able) / len(able) - 0.8) < 0.02


def test_marines_and_idlers_never_have_skill_aloft(frigate_crew):
    marines = frigate_crew.by_station[Station.MARINES]
    assert len(marines) == 40 and all(s.rating is Rating.MARINE for s in marines)
    assert all(s.skill_aloft == 0.0 for s in marines)
    idlers = frigate_crew.by_station[Station.IDLERS]
    assert all(s.rating is Rating.IDLER and s.skill_aloft == 0.0 for s in idlers)


def test_idlers_by_trade_and_seamen_without(frigate_crew):
    trades: dict[str, int] = {}
    for s in frigate_crew.by_station[Station.IDLERS]:
        trades[s.trade] = trades.get(s.trade, 0) + 1
    assert trades == load_ship(FRIGATE).spec.crew.idlers_by_trade
    assert all(s.trade is None for s in frigate_crew.sailors if s.station is not Station.IDLERS)


def test_posts_are_officers_of_the_quarterdeck(frigate_crew):
    for post, s in frigate_crew.posts.items():
        assert s.post == post and s.rating is Rating.OFFICER
        assert s.station is Station.QUARTERDECK and s.watch is Watch.NONE and s.outline == ""
    assert [s.id for s in frigate_crew.posts.values()] == [f"s{i:03d}" for i in range(1, 13)]


def test_a_name_given_in_the_file_is_kept():
    spec = copy.deepcopy(load_ship(FRIGATE).spec.crew)
    spec.posts[0].name = "Edwd. Pellew"
    crew = muster(spec, Rng(7).stream("muster"))
    assert crew.posts["captain"].name == "Edwd. Pellew"


def test_watches_split_each_station_evenly_odd_one_to_starboard(frigate_crew, schooner_crew):
    for crew in (frigate_crew, schooner_crew):
        for station in Station:
            men = crew.by_station[station]
            if station in (Station.IDLERS, Station.QUARTERDECK):
                assert all(s.watch is Watch.NONE for s in men)
                continue
            star = sum(1 for s in men if s.watch is Watch.STARBOARD)
            lar = sum(1 for s in men if s.watch is Watch.LARBOARD)
            assert star + lar == len(men) and star - lar in (0, 1)
            # an equal share of the strength: each rating is split too
            for r in Rating:
                rs = [s for s in men if s.rating is r]
                a = sum(1 for s in rs if s.watch is Watch.STARBOARD)
                assert abs(2 * a - len(rs)) <= 1
    after = schooner_crew.by_station[Station.AFTERGUARD]
    assert sum(1 for s in after if s.watch is Watch.STARBOARD) == 6  # eleven: six and five
    assert len(frigate_crew.by_watch[Watch.STARBOARD]) == 111
    assert len(frigate_crew.by_watch[Watch.LARBOARD]) == 111


def test_muster_is_deterministic_and_draws_only_from_its_stream():
    ship = load_ship(FRIGATE)
    state = random.getstate()
    one = muster(ship.spec.crew, Rng(7).stream("muster"), ship_name=ship.name)
    assert random.getstate() == state  # the global generator is untouched
    two = muster(ship.spec.crew, Rng(7).stream("muster"), ship_name=ship.name)
    other = muster(ship.spec.crew, Rng(8).stream("muster"), ship_name=ship.name)
    at = DAY.replace(hour=10)
    assert "\n".join(one.describe(at)) == "\n".join(two.describe(at))
    assert [vars(s) for s in one.sailors] == [vars(s) for s in two.sailors]
    assert [s.name for s in one.sailors] != [s.name for s in other.sailors]
    # the same stream state, however it was reached, gives the same crew
    stream = random.Random(99)
    stream.random()
    saved = stream.getstate()
    a = muster(ship.spec.crew, stream)
    stream.setstate(saved)
    b = muster(ship.spec.crew, stream)
    assert [vars(s) for s in a.sailors] == [vars(s) for s in b.sailors]


# ---------------------------------------------------------------------------
# the watch bill
# ---------------------------------------------------------------------------

# Who has the deck through 1 June 1805 and into the next day: the dog watches make the
# rotation, so the watch that had the middle watch has the first watch.
EXPECTED_WATCHES = [
    (0, Watch.LARBOARD),  # middle
    (4, Watch.STARBOARD),  # morning
    (8, Watch.LARBOARD),  # forenoon
    (12, Watch.STARBOARD),  # afternoon
    (16, Watch.LARBOARD),  # first dog
    (18, Watch.STARBOARD),  # last dog
    (20, Watch.LARBOARD),  # first
    (24, Watch.STARBOARD),  # the next day's middle
    (28, Watch.LARBOARD),  # and morning
]


def test_the_watch_on_duty_through_a_day_with_the_dog_watches():
    for start, watch in EXPECTED_WATCHES:
        t0 = DAY + timedelta(hours=start)
        end = next((s for s, _ in EXPECTED_WATCHES if s > start), start + 4)
        t = t0
        while t < DAY + timedelta(hours=end):
            assert bill.watch_on_duty(t) is watch, t
            t += timedelta(minutes=30)
        assert bill.watch_on_duty(t0 - timedelta(seconds=1)) is not watch


def test_idlers_are_up_from_six_until_the_dog_watches_are_out():
    assert not bill.idlers_up(DAY.replace(hour=5, minute=59, second=59))
    assert bill.idlers_up(DAY.replace(hour=6))
    assert bill.idlers_up(DAY.replace(hour=19, minute=59, second=59))
    assert not bill.idlers_up(DAY.replace(hour=20))
    assert not bill.idlers_up(DAY.replace(hour=2))


def test_on_deck_through_a_whole_day(frigate_crew):
    crew = frigate_crew
    watch_size = {w: len(crew.by_watch[w]) for w in (Watch.STARBOARD, Watch.LARBOARD)}
    idlers = len(crew.by_station[Station.IDLERS])
    t = DAY
    while t < DAY + timedelta(days=1):
        watch = bill.watch_on_duty(t)
        deck = crew.on_deck(t)
        expected = watch_size[watch] + (idlers if 6 <= t.hour < 20 else 0)
        assert len(deck) == expected, t
        assert all(s.station is not Station.QUARTERDECK for s in deck)
        assert all(s.watch in (watch, Watch.NONE) for s in deck)
        assert [s.id for s in deck] == sorted(s.id for s in deck)
        assert len(deck) + len(bill.below(crew, t)) == crew.complement - len(crew.posts)
        t += timedelta(minutes=15)


def test_on_deck_takes_a_clock_as_well_as_a_time(schooner_crew):
    clock = Clock(DAY.replace(hour=4))
    clock.tick = 3 * 3600  # 07:00, idlers up, starboard watch
    assert [s.id for s in schooner_crew.on_deck(clock)] == [
        s.id for s in schooner_crew.on_deck(DAY.replace(hour=7))
    ]
    assert len(schooner_crew.on_deck(clock)) == 17 + 4


def test_all_hands_at_work_turned_up_and_the_routines_watch():
    crew = _crew(SCHOONER)
    night = DAY.replace(hour=2)  # middle watch: larboard on deck, idlers below
    hands = crew.complement - len(crew.posts)
    assert len(crew.on_deck(night)) == 16
    crew.all_hands_called = True
    assert len(crew.on_deck(night)) == hands
    crew.sailors[-1].fit = False
    assert len(crew.on_deck(night)) == hands - 1
    crew.sailors[-1].fit = True
    crew.all_hands_called = False
    below = [s for s in crew.sailors if s.watch is Watch.STARBOARD]
    below[0].at = "reef#1"  # not relieved mid-evolution
    below[1].turned_up = True  # called up out of his watch
    deck = crew.on_deck(night)
    assert below[0] in deck and below[1] in deck and below[2] not in deck
    crew.watch_on_deck = Watch.STARBOARD  # the routine relieved the watch early
    assert bill.watch_on_deck(crew, night) is Watch.STARBOARD
    assert len(crew.on_deck(night)) == 17
    crew.watch_on_deck = None
    assert bill.watch_on_deck(crew, night) is Watch.LARBOARD


def test_fatigue_words():
    assert fatigue_words(0.0) == "fresh"
    assert fatigue_words(0.3) == "tired"
    assert fatigue_words(0.8) == "worn out"


# ---------------------------------------------------------------------------
# the muster, as the owner reads it
# ---------------------------------------------------------------------------

FRIGATE_MUSTER_SEED_7_FORENOON = """\
Mustered the Amazon's company, 264 souls: twelve officers, 182 seamen, 40 marines and 30 idlers.
The larboard watch has the deck, the idlers up: 142 hands on deck.
Forecastlemen, 28 (26 able, 2 ordinary): 15 on deck, 13 below, 2 at work; fresh.
Fore topmen, 24 (10 able, 14 ordinary): 12 on deck, 12 below, none at work; fresh.
Main topmen, 30 (13 able, 17 ordinary): 15 on deck, 15 below, none at work; fresh.
Mizzen topmen, 14 (6 able, 8 ordinary): 7 on deck, 7 below, none at work; fresh.
Afterguard, 50 (32 ordinary, 18 landsmen): 25 on deck, 25 below, none at work; tired.
Waisters, 36 (36 landsmen): 18 on deck, 18 below, none at work; fresh.
Marines, 40: 20 on deck, 20 below, none at work; fresh.
Idlers, 30: 30 on deck, none below, none at work; fresh.
Seamen by rating: 55 able, 73 ordinary, 54 landsmen.
Idlers by trade: carpenter's crew 6, sailmaker's crew 3, cooper 1, armourer 1, cook 2, \
steward 3, servant 8, surgeon's mate 2, clerk 1, master-at-arms's party 3.
Captain Adam Bowen.
Mr. Fredk. Pearce, first lieutenant.
Mr. Silas Pascoe, second lieutenant.
Mr. Abm. Russell, third lieutenant.
Mr. Peter Harvey, master.
Mr. Saml. Kemp, boatswain.
Mr. Alexr. Porter, gunner.
Mr. Henry Chambers, carpenter.
Mr. Angus Gardner, purser.
Mr. Alexr. Bailey, surgeon.
Mr. Martin Davies, sailmaker.
Mr. Richd. Oliver, master-at-arms."""


def test_the_frigates_muster_reads_as_the_owner_expects():
    crew = _crew(FRIGATE)
    # two forecastlemen of the starboard watch kept on deck at work, a tired afterguard
    crew.by_id["s021"].at = "set_sail#1"
    crew.by_id["s022"].at = "set_sail#1"
    for s in crew.by_station[Station.AFTERGUARD]:
        s.fatigue = 0.3
    text = "\n".join(crew.describe(Clock(DAY.replace(hour=9))))
    assert text == FRIGATE_MUSTER_SEED_7_FORENOON


def test_the_muster_with_all_hands_called(schooner_crew):
    crew = copy.deepcopy(schooner_crew)
    crew.all_hands_called = True
    lines = crew.describe(DAY.replace(hour=2))
    assert lines[1] == "All hands are called: 37 hands on deck."
    assert "Afterguard, 11 (2 able, 9 ordinary): 11 on deck, none below" in lines[4]
    assert lines[-3:] == [
        f"Mr. {crew.posts['master'].name}, master.",
        f"Mr. {crew.posts['mate'].name}, mate.",
        f"Mr. {crew.posts['boatswain'].name}, boatswain.",
    ]
