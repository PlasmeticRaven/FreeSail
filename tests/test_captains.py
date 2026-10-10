"""The rules-based captain in three layers (spec M6 §4; decision 40; package 40): the
intent read, the doctrine as data, the plan over the chart's tracks, the state machine
whose states are books loaded and unloaded by name, perception on the player's terms,
the rule of the road, the far-detail interface, and the floor under the player's ship."""

from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

import pytest

from freesail.api.session import make_world
from freesail.core import replay as replay_mod
from freesail.core.world import Scenario
from freesail.standing import grammar as standing
from freesail.world import captains as C
from freesail.world.geo import Position, destination
from freesail.world.scenarios import begin, load_scenario, make_scenario_world
from freesail.world.ships import Vessel, vessel_from_spec

ROOT = Path(__file__).resolve().parents[1]
INTENT = "data/scenarios/merchant-intent.yaml"
MERCHANT = "data/scenarios/merchant-passage.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
SHIPS = (FRIGATE, SCHOONER, "data/ships/cutter.yaml", "data/ships/brig.yaml")


def world_at(lat: float, lon: float, ship: str = SCHOONER, **kw):
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": lat, "lon_deg": lon},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        **kw,
    )
    return make_world(7, ship, sc)


# -- intent ------------------------------------------------------------------------------


def test_an_intent_is_read_from_words_against_the_chart_and_the_ports_and_refused_otherwise():
    w = world_at(49.8, -5.2)
    trade = C.read_intent(w, "trade tin from Falmouth to Brest")
    assert (trade.kind, trade.cargo, trade.origin, trade.destination) == (
        "trade",
        "tin",
        "falmouth",
        "brest",
    )
    assert trade.tons is None and trade.words == "trade tin from Falmouth to Brest"
    forty = C.read_intent(w, "trade forty tons of tin from Falmouth to Brest")
    assert forty.tons == 40.0
    station = C.read_intent(w, "keep the station off Ushant within 15 miles")
    assert (station.kind, station.destination, station.radius_nm) == ("station", "ushant", 15.0)
    letter = C.read_intent(w, "carry this letter to Brest")
    assert (letter.kind, letter.destination) == ("letter", "brest")
    home = C.read_intent(w, "run home to Plymouth")
    assert (home.kind, home.destination) == ("home", "plymouth")
    bound = C.read_intent(w, "bound for 48 30 N 5 30 W")
    assert bound.kind == "passage" and bound.destination.startswith("48")
    with pytest.raises(ValueError, match="no intent a captain knows"):
        C.read_intent(w, "fish the Wolf's ground from Falmouth")
    with pytest.raises(ValueError, match="no place named 'Atlantis'"):
        C.read_intent(w, "run home to Atlantis")
    assert C.role_for(w, trade) == "merchant"
    assert C.role_for(w, station) == "kings-ship"
    assert C.role_for(w, letter) == "packet"
    assert C.role_for(world_at(49.8, -5.2, FRIGATE), home) == "kings-ship"


# -- doctrine as data -------------------------------------------------------------------


def test_every_doctrine_loads_with_sources_states_and_stimuli_the_captain_knows():
    """Each role's file gives thresholds with a source beside each figure, books for
    every state of the machine (engaging present and empty), and transitions whose
    states and stimuli the captain judges."""
    for role in C.ROLES:
        d = C.load_doctrine(role)
        assert d.role == role and d.thresholds and d.transitions
        for key, value in d.thresholds.items():
            assert d.sources.get(key), f"{role}: {key} has no source"
            assert isinstance(value, (int, float, str))
        for state in C.STATES:
            assert state in d.books, f"{role}: no book for {state}"
        assert d.books["engaging"] == ()
        for t in d.transitions:
            assert t.frm in C.STATES and t.to in C.STATES
            assert t.on in C.STIMULI, f"{role}: {t.on}"
            assert not t.unless or t.unless in C.STIMULI
    with pytest.raises(ValueError, match="no doctrine for the role 'fisherman'"):
        C.load_doctrine("fisherman")


def test_every_book_line_of_every_doctrine_parses_in_the_dialect_on_every_ship():
    """A state's book, its placeholders filled as the captain fills them, is standing
    orders the ship takes, on each of the four ships."""
    fills = {
        "mark": "the Lizard",
        "reached": "2",
        "station": "Ushant",
        "radius": "12",
        "radius_out": "20",
        "radius_in": "6",
        "port": "Brest",
        "road": "the road of Bertheaume",
        "anchorage": "the Bay of Brest",
        "anchorage_fathoms": "12",
        "cast_in": "larboard",
        "course_in": "E",
        "cast_out": "starboard",
        "course_out": "S by E",
    }
    for ship in SHIPS:
        w = world_at(49.8, -5.2, ship)
        fills["light_sail"] = w.captain._light_sail()
        fills["storm_topsail"] = w.captain._storm_topsail()
        for role in C.ROLES:
            d = C.load_doctrine(role)
            fills.update(d.thresholds)
            for state, lines in d.books.items():
                for line in lines:
                    text = line.format_map(fills)
                    rule = standing.parse_standing(w.ship, text)
                    assert rule.name, (role, state, line)


# -- the plan ---------------------------------------------------------------------------


def test_the_planner_joins_the_ports_tracks_and_the_common_track_by_the_iroise():
    """Falmouth to Brest: out by the port's `to_sea` track (the outer road steered to on
    the pilot's course and passed, the Manacles' and the Lizard's points), then the
    common track the features file names (the soundings south-west of Ushant, the
    Iroise), since the straight line from off the Lizard runs through the isles, then
    Brest's `from_sea` track to the road where the tide is waited for, and its `in`
    track through the Goulet to the Bay, where she comes to."""
    w = world_at(50.1631, -5.0345)
    intent = C.read_intent(w, "trade tin from Falmouth to Brest")
    planner = C.Planner(w)
    legs = planner.legs_for(intent, Position(50.1631, -5.0345), "falmouth")
    words = [lg.words for lg in legs]
    kinds = [lg.kind for lg in legs]
    assert words[:3] == ["Falmouth outer road", "50 00 N 4 57 W", "49 52 N 5 06 W"]
    assert kinds[:3] == ["out", "to", "to"]
    assert "the soundings seven leagues south-west of Ushant" in words
    assert "the Passage de l'Iroise" in words
    assert words.index("the soundings seven leagues south-west of Ushant") < words.index(
        "the Passage de l'Iroise"
    )
    assert kinds.count("road") == 1 and legs[kinds.index("road")].words == "the road of Bertheaume"
    assert kinds[-1] == "anchorage" and words[-1] == "the Bay of Brest"
    inner = legs[kinds.index("road") + 1 :]
    assert all(lg.reached_nm <= 0.5 for lg in inner)
    # the straight line from off the Lizard to the Iroise is not clear (the isles south
    # of Ushant), so the route takes the track; the open sea between is clear
    off_lizard = Position(49.8667, -5.1)
    iroise = w.chart.feature("iroise").position
    assert not planner.clear(off_lizard, iroise)
    soundings = w.chart.feature("soundings-off-ushant-near").position
    assert planner.clear(off_lizard, soundings) and planner.clear(soundings, iroise)
    assert planner.sea_route(off_lizard, iroise) == [
        ("the soundings seven leagues south-west of Ushant", soundings),
    ]
    assert planner.sea_route(off_lizard, soundings) == []
    tracks = C.load_tracks(w)
    assert [t.id for t in tracks] == ["channel-to-brest", "lizard-to-plymouth"]
    # a line that runs across the land is not clear, and a way round it is found: by a
    # track's marks, or a headland given an offing (a plain position to the tenth)
    behind = Position(50.05, -5.02)  # off Falmouth, inside the Manacles' line
    end = Position(49.95, -5.10)
    assert not planner.clear(behind, end)
    marks = planner.sea_route(behind, end)
    assert marks and all(isinstance(m[1], Position) for m in marks)
    plain = re.compile(r"^\d+ \d+\.\d [NS] \d+ \d+\.\d [EW]$")
    track_marks = {m[0] for t in tracks for m in t.marks}
    assert all(plain.match(m[0]) or m[0] in track_marks for m in marks)
    assert plain.match(C.plain_position(Position(48.275, -4.8)))
    assert C.plain_position(Position(48.275, -4.8)) == "48 16.5 N 4 48.0 W"


# -- the captain holds the ship on an intent alone ---------------------------------------


@pytest.fixture(scope="module")
def under_way():
    """The intent scenario run until she is under way for sea (the tin bought by the
    lighter, the ebb and the day serving) and the first leg shaped."""
    sf = load_scenario(INTENT)
    world = make_scenario_world(sf)
    begin(world, sf)
    world.run(19600)
    return world


def test_the_captain_buys_the_cargo_sails_on_the_ebb_and_every_doing_is_an_order(under_way):
    w = under_way
    cap = w.captain
    assert cap.active and cap.commands and cap.role == "merchant"
    assert cap.intent.words == "trade tin from Falmouth to Brest"
    log = w.log
    bought = [e for e in log if e.kind == "market.bought"]
    assert bought and bought[0].text.startswith("47 tons of tin hoisted in")
    bargain = [e for e in log if e.kind == "market.bargain"]
    assert bargain[0].actor == C.actor_for("in port")
    under = [e for e in log if e.kind == "ship.under_way"]
    assert under and "starboard tack" in under[0].text
    sailed = [e for e in log if e.kind == "order.accepted" and "getting under way" in e.text]
    assert len(sailed) == 1 and sailed[0].text.startswith(
        "By the captain, in port: getting under way"
    )
    assert "(the tide serves)" in sailed[0].text
    states = [e.data["state"] for e in log if e.kind == "captain.state"]
    assert states[:2] == ["in port", "on passage"]
    plan = [e for e in log if e.kind == "captain.plan"]
    assert (
        plan and "Falmouth outer road" in plan[0].text and "the Passage de l'Iroise" in plan[0].text
    )
    shaped = [e for e in log if e.kind == "helm.set" and C.state_of_actor(str(e.actor))]
    assert shaped and shaped[0].text.startswith("Shaped a course for 50° 00' N, 4° 57' W")
    assert shaped[0].data["place"].upper() == "50 00 N 4 57 W"  # the plain form the dialect reads
    # every doing of his is an order under the rules actor: none is journaled, none is
    # an input a replay would give again; the scenario's one order is
    actors = {e.actor for e in log if e.kind == "order.accepted"}
    assert C.actor_for("in port") in actors and C.actor_for("on passage") in actors
    assert [t for _, actor, t in w.journal if actor == "captain"] == ["let go the best bower"]
    assert all(not str(i.get("actor", "")).startswith("captain's rule") for i in w.inputs)
    # the state's book is loaded and listed as his
    listed = w.standing.book.lines()
    assert any("the book 'on passage'" in ln for ln in listed)
    assert w.standing.books_loaded() == ["on passage"]
    said = w.readings.words("captain")
    assert said.startswith(f"{cap.name}, merchant; the intent: trade tin from Falmouth to Brest")
    assert "nobody at the captain's station" in said and "the deck the captain's own" in said


def test_the_captains_run_replays_to_its_digest_and_a_checkpoint_holds_him(under_way, tmp_path):
    """His judgements are a function of the seed and the journal: a replay of the save
    makes them again, and a checkpoint carries him whole."""
    from freesail.api.session import ship_factory

    w = under_way
    data = w.save()
    copy = replay_mod.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.captain.state == w.captain.state and copy.captain.leg_i == w.captain.leg_i
    assert [lg.words for lg in copy.captain.legs] == [lg.words for lg in w.captain.legs]
    path = replay_mod.write_checkpoint(w, tmp_path / "captain.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    assert c.captain.to_dict() == w.captain.to_dict()
    c.run(600)
    w.run(600)
    assert c.log.digest() == w.log.digest()


# -- perception on the player's terms ---------------------------------------------------


def test_nothing_in_captains_reads_the_worlds_truth_by_any_road():
    """37j's proof extended to the captain (truth 81's kin): two ships of one seed whose
    true places are four miles apart and whose accounts are one perceive alike and plan
    alike; and the module's source names no road to the truth."""
    source = (ROOT / "freesail" / "world" / "captains.py").read_text("utf-8")
    for road in (
        "world.position",
        ".ship.dyn",
        "world.vessels",
        "world.systems",
        "ship_x",
        "ship_y",
        "tide_state",
        "world.tide",
        "world.wind.",
        "chart.depth_at(",
        "elevation_at(",
    ):
        assert road not in source, road
    a, b = world_at(49.0, -6.5), world_at(49.05, -6.42)
    same = Position(49.02, -6.47)
    for w in (a, b):
        w.navigation.reckoning.set_position(same, 0, sigma_nm=1.0)
        w.run(120)
    pa, pb = C.Perception.read(a), C.Perception.read(b)
    # her own head and way are the ship's (two hulls on two latitudes differ at the
    # fourth decimal by the frame's arithmetic, as the readings' own proof allows)
    for p in (pa, pb):
        p.heading_deg = round(p.heading_deg, 1)
        p.speed_kn = round(p.speed_kn, 1)
    assert pa == pb
    intent = C.read_intent(a, "bound for Brest")
    legs_a = C.Planner(a).legs_for(intent, a.navigation.account_now())
    legs_b = C.Planner(b).legs_for(intent, b.navigation.account_now())
    assert [(lg.words, lg.kind) for lg in legs_a] == [(lg.words, lg.kind) for lg in legs_b]
    assert pa.tide_is("ebb") in (True, False)


# -- the books by name --------------------------------------------------------------------


def test_a_book_is_loaded_and_unloaded_by_name_and_the_players_own_rule_is_kept():
    w = world_at(49.8, -5.2)
    rt = w.standing
    given = w.submit('standing order "night routine": at sunset then take in the fore topgallant')
    assert given.kind == "standing.given"
    names = rt.load_book(
        "on passage",
        [
            'standing order "tend the sheets": every glass then trim the sheets',
            'standing order "night routine": at sunset then take in the jib',
            'standing order "bad": at the moon then do nothing',
        ],
        C.actor_for("on passage"),
    )
    assert names == ["tend the sheets"]
    kept = rt.book.get("night routine")
    assert kept.book == "" and "topgallant" in kept.actions[0]
    assert rt.book.get("tend the sheets").book == "on passage"
    assert rt.books_loaded() == ["on passage"]
    loaded = [e for e in w.log if e.kind == "standing.book_loaded"]
    assert loaded and loaded[0].text == "The book 'on passage' loaded: tend the sheets."
    refused = [e for e in w.log if e.kind == "order.rejected" and "The book 'on passage'" in e.text]
    assert len(refused) == 2
    assert any("the book 'on passage'" in ln for ln in rt.book.lines())
    gone = rt.unload_book("on passage", C.actor_for("on passage"))
    assert gone == ["tend the sheets"] and rt.book.get("tend the sheets") is None
    assert rt.book.get("night routine") is kept and rt.books_loaded() == []
    assert [e.text for e in w.log if e.kind == "standing.book_unloaded"] == [
        "The book 'on passage' unloaded: tend the sheets."
    ]
    assert rt.unload_book("on passage", C.actor_for("on passage")) == []


# -- the world order, the floor and the reading ------------------------------------------


def test_a_captain_world_order_gives_the_intent_and_a_book_scenario_keeps_its_captain_idle():
    w = world_at(50.1631, -5.0345)
    assert not w.captain.active and not w.captain.commands
    assert w.readings.words("captain").endswith(
        "; nobody at the captain's station; the deck the player's"
    )
    e = w.world_order("captain: intent bound for Plymouth")
    assert e.kind == "world.order" and "the captain's intent: bound for Plymouth" in e.text
    assert w.captain.active and w.captain.intent.kind == "passage"
    bad = w.world_order("captain: intent fish the Wolf")
    assert bad.kind == "world.order_refused" or "no intent" in bad.text
    # a scenario with a book names its captain and his book, and gives no judgement
    sf = load_scenario(MERCHANT)
    world = make_scenario_world(sf)
    begin(world, sf)
    world.run(1800)
    cap = world.captain
    assert not cap.active and list(cap.books) == ["data/scenarios/merchant-passage.orders"]
    assert cap.book_words() == "the scenario's book (merchant-passage.orders)"
    assert world.scenario.books == ["data/scenarios/merchant-passage.orders"]
    assert not any(str(e.actor).startswith("captain's rule") for e in world.log)
    assert cap.name.startswith("Mr ") and cap.name == world.people.captain.name


# -- the rule of the road ------------------------------------------------------------------


def test_the_rule_of_the_road_as_1805_had_it():
    wind = 270.0  # a westerly
    by_wind_starboard = C._tack_and_point(
        200.0, wind
    )  # heading SSW, the wind on the starboard side
    by_wind_larboard = C._tack_and_point(340.0, wind)
    running = C._tack_and_point(90.0, wind)
    assert by_wind_starboard == {"tack": "starboard", "point": "by the wind", "course_deg": 200.0}
    assert by_wind_larboard["tack"] == "larboard" and by_wind_larboard["point"] == "by the wind"
    assert running["point"] == "running"
    order, words = C._road_rule(by_wind_starboard, by_wind_larboard)
    assert order == "" and "we stand on" in words
    order, words = C._road_rule(by_wind_larboard, by_wind_starboard)
    assert order == "bear away two points" and "we give way under her stern" in words
    order, words = C._road_rule(running, by_wind_starboard)
    assert order == "bear away two points" and "we keep clear of her" in words
    order, words = C._road_rule(by_wind_starboard, running)
    assert order == "" and "she keeps clear" in words
    assert C._course_in_words("a brig, standing to the eastward (E), under plain sail") == 90.0
    assert C._course_in_words("a sail") is None


# -- the far-detail body as an interface -------------------------------------------------


def test_the_far_detail_body_resolves_on_passage_and_hove_to_and_refuses_the_rest():
    w = world_at(49.5, -5.5)
    v = vessel_from_spec(
        w,
        {
            "description": "merchant brig",
            "name": "Nancy",
            "nation": "britain",
            "position": "49 30 N 5 40 W",
            "goal": "bound for the Lizard",
        },
        1,
    )
    assert isinstance(v, Vessel) and v.state == "on passage"
    plan = list(v.plan)
    assert C.resolve_state(v, "hove to for weather") is True
    assert v.state == "hove to for weather" and v.plan[0][0] == "lie_to"
    v.tick(w, 60.0)
    assert v.sail_state == "lying to" and v.speed_kn == 0.0
    assert C.resolve_state(v, "on passage") is True
    assert v.state == "on passage" and v.plan == plan and v.saved_plan is None
    for state in ("chasing", "evading", "keeping station", "investigating a stranger"):
        assert C.resolve_state(v, state) is False and v.state == "on passage"
    with pytest.raises(ValueError):
        C.resolve_state(v, "fishing")
    # the recorded passages' vessels are on passage and their plans untouched
    sf = load_scenario(MERCHANT)
    world = make_scenario_world(sf)
    assert all(x.state == "on passage" and x.saved_plan is None for x in world.vessels.vessels)
    assert "state" not in world.vessels.to_dict()[0]  # nothing new in the pinned form
    _ = destination
