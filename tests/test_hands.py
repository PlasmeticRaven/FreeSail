"""Hands and the crew factor (spec M3 §3; package 17).

The pool (`crew/hands.py`) on a hand-made company, the factor for the rating table, the
runner's three short-handed outcomes on the schooner, pre-emption by all hands across a
tack on the frigate, and the compatibility rule (spec M3 §1): every milestone 2 evolution,
run alone on the crewed frigate with the watch on deck, finishes on the same tick as on
the frigate without a crew.

Scenarios go through `make_world` and the Orders language. The composer does not yet give
the runner the World's clock (the lead adds that line to `session.py`), so these tests set
`runner.clock = world.clock` themselves, as that line will.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any

import pytest

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import bill, hands
from freesail.crew.hands import CrewRequest, CrewRequestError, crew_factor, release, request
from freesail.crew.model import Crew, Rating, Sailor, Station, Watch, number_words
from freesail.evolutions import EVOLUTIONS, registry
from freesail.evolutions.runner import DEFAULT_WATCH_TIME, Runner, gerund
from freesail.ship.parts import SailState

FRIGATE = "data/ships/frigate-36.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SEED = 7
ORD, ABLE, LAND = Rating.ORDINARY, Rating.ABLE, Rating.LANDSMAN
MARINE, IDLER = Rating.MARINE, Rating.IDLER

# The twenty evolution files of milestone 2.
M2_EVOLUTIONS = [
    "brace",
    "fill_away",
    "furl_gaff",
    "furl_jibheaded",
    "furl_square",
    "heave_to",
    "reef_gaff",
    "reef_square",
    "set_gaff",
    "set_jibheaded",
    "set_square",
    "set_studding",
    "shake_out_gaff",
    "shake_out_square",
    "tack",
    "take_in_gaff",
    "take_in_jibheaded",
    "take_in_square",
    "take_in_studding",
    "wear",
]


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------


def sailor(n: int, rating: Rating, station: Station, watch: Watch = Watch.STARBOARD) -> Sailor:
    from freesail.crew.model import RATING_SKILL

    deck, aloft = RATING_SKILL[rating]
    return Sailor(
        id=f"s{n:03d}",
        name=f"Hand {n}",
        rating=rating,
        station=station,
        watch=watch,
        skill_aloft=aloft,
        skill_deck=deck,
    )


def small_company() -> Crew:
    """A company whose books are laid out to show the preference order."""
    rows = [
        (1, ABLE, Station.AFTERGUARD),
        (2, LAND, Station.AFTERGUARD),
        (3, ORD, Station.AFTERGUARD),
        (4, ORD, Station.WAISTERS),
        (5, ABLE, Station.FORECASTLE),
        (6, ORD, Station.AFTERGUARD),
        (7, LAND, Station.WAISTERS),
        (8, MARINE, Station.MARINES),
        (9, IDLER, Station.IDLERS),
        (10, ORD, Station.MAIN_TOP),
        (11, ORD, Station.FORE_TOP),
        (12, ABLE, Station.MAIN_TOP),
    ]
    return Crew(ship_name="Test", sailors=[sailor(n, r, st) for n, r, st in rows])


def ids(sailors) -> list[str]:
    return [s.id for s in sailors]


def world(path: str, heading: float = 0.0, speed_kn: float = 0.0, crewed: bool = True, **kw):
    scenario = Scenario(
        wind_from_deg=0.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed_kn,
        **kw,
    )
    w = make_world(SEED, path, scenario)
    runner = w.ship.extra["evolutions"]
    runner.clock = w.clock  # what the lead's line in session.py will do
    if not crewed:
        w.ship.extra.pop("crew")
    return w


def runner_of(w) -> Runner:
    return w.ship.extra["evolutions"]


def log_after(w, n0: int):
    return list(w.log)[n0:]


def tick_until_idle(w, limit: int = 3000) -> int:
    runner = runner_of(w)
    t = 0
    while runner.in_progress() and t < limit:
        w.tick()
        t += 1
    return t


# ---------------------------------------------------------------------------
# the request
# ---------------------------------------------------------------------------


def test_crew_request_reads_the_files_crew_line():
    r = CrewRequest.from_mapping({"hands": 12, "rating": "ordinary", "stations": ["topmen"]})
    assert r.hands == 12 and r.rating is Rating.ORDINARY and r.stations == ("topmen",)
    assert not r.all_hands and not r.wants_none
    r = CrewRequest.from_mapping({"hands": "all", "rating": "ordinary", "stations": ["all hands"]})
    assert r.all_hands and r.stations == ("all hands",)
    assert CrewRequest.from_mapping(None).wants_none
    assert CrewRequest.from_mapping({}).wants_none
    assert CrewRequest.from_mapping({"hands": 0}).wants_none
    assert CrewRequest.from_mapping({"hands": 4, "rating": "petty_officer"}).rating is (
        Rating.PETTY_OFFICER
    )
    with pytest.raises(CrewRequestError, match="no station called 'maintop'"):
        CrewRequest.from_mapping({"hands": 4, "stations": ["maintop"]})
    with pytest.raises(CrewRequestError, match="no rating called 'bosun'"):
        CrewRequest.from_mapping({"hands": 4, "rating": "bosun"})
    with pytest.raises(CrewRequestError, match="say a number or 'all'"):
        CrewRequest.from_mapping({"hands": "a dozen"})


def test_every_evolution_file_has_a_crew_line_the_pool_can_read():
    for eid, evo in EVOLUTIONS.items():
        want = CrewRequest.from_mapping(evo.crew)
        # the routine's two (call_all_hands, pipe_down) ask for none: the lead's package 19 brief
        assert want.all_hands or want.hands > 0 or eid in ("call_all_hands", "pipe_down"), eid


def test_topmen_are_the_subjects_own_top_first():
    want = CrewRequest.from_mapping({"hands": 12, "stations": ["topmen", "afterguard"]})
    assert hands.preferred_stations(want, "main") == [
        Station.MAIN_TOP,
        Station.FORE_TOP,
        Station.MIZZEN_TOP,
        Station.AFTERGUARD,
    ]
    assert hands.preferred_stations(want, "bowsprit")[0] is Station.FORE_TOP
    everyone = CrewRequest.from_mapping({"hands": 3, "stations": ["all hands"]})
    assert Station.QUARTERDECK not in hands.preferred_stations(everyone, None)


def test_allocation_order_rating_wanted_then_better_then_lesser():
    crew = small_company()
    deck = crew.sailors
    want = CrewRequest.from_mapping({"hands": 12, "rating": "ordinary", "stations": ["afterguard"]})
    got = request(crew, deck, "x#1", want, None)
    # ordinary from the afterguard (by id); ordinary from the other stations in the bill's
    # order; able, the afterguard first; then the lesser ratings, the afterguard first.
    assert ids(got.hands) == [
        "s003",
        "s006",
        "s011",
        "s010",
        "s004",
        "s001",
        "s005",
        "s012",
        "s002",
        "s007",
        "s008",
        "s009",
    ]
    assert got.outcome == hands.ENOUGH
    assert all(s.at == "x#1" for s in got.hands)
    assert ids(release(crew, "x#1")) == sorted(ids(got.hands))
    assert all(s.at is None for s in crew.sailors)
    again = request(crew, deck, "x#2", want, None)
    assert ids(again.hands) == ids(got.hands)  # deterministic


def test_the_pool_is_on_deck_fit_and_idle():
    crew = small_company()
    crew.by_id["s003"].fit = False
    crew.by_id["s006"].at = "other#9"
    deck = [s for s in crew.sailors if s.id != "s011"]
    want = CrewRequest.from_mapping({"hands": 2, "rating": "ordinary", "stations": ["afterguard"]})
    got = request(crew, deck, "x#1", want, None)
    assert ids(got.hands) == ["s010", "s004"]


def test_marines_and_idlers_are_never_sent_aloft():
    crew = small_company()
    want = CrewRequest.from_mapping({"hands": 12, "rating": "ordinary", "stations": ["topmen"]})
    got = request(crew, crew.sailors, "x#1", want, "fore", aloft=True)
    assert "s008" not in ids(got.hands) and "s009" not in ids(got.hands)
    assert ids(got.hands)[:2] == ["s011", "s010"]  # the fore top before the main
    # the company can only ever give ten hands aloft: the request is clamped to them
    assert got.wanted == 10 and got.outcome == hands.ENOUGH


def test_short_handed_arithmetic():
    crew = small_company()
    deck = crew.sailors[:8]  # eight hands on deck
    want = CrewRequest.from_mapping({"hands": 12, "rating": "ordinary"})
    got = request(crew, deck, "x#1", want, None)
    assert got.outcome == hands.SHORT and got.got == 8 and got.wanted == 12
    assert crew_factor(got, want, aloft=False) > 1.5  # numbers 1.5, and lesser ratings
    release(crew, "x#1")
    got = request(crew, crew.sailors[:5], "x#2", want, None)
    assert got.outcome == hands.TOO_FEW and got.hands == [] and got.available == 5
    assert all(s.at is None for s in crew.sailors)  # too few: nobody is taken
    got = request(crew, crew.sailors[:6], "x#3", want, None)
    assert got.outcome == hands.SHORT  # half is workable
    nothing = request(crew, crew.sailors, "x#4", CrewRequest.from_mapping({"hands": 0}), None)
    assert nothing.outcome == hands.ENOUGH and nothing.hands == []
    assert crew_factor(nothing, CrewRequest(), aloft=False) == 1.0


# ---------------------------------------------------------------------------
# the crew factor (spec M3 §3.3)
# ---------------------------------------------------------------------------


def factor_for(rating: Rating, wanted: Rating, n: int = 12, fatigue: float = 0.0, **kw) -> float:
    station = Station.MARINES if rating is Rating.MARINE else Station.AFTERGUARD
    men = [sailor(i, rating, station) for i in range(n)]
    for s in men:
        s.fatigue = fatigue
    want = CrewRequest(hands=kw.get("hands", n), rating=wanted, stations=("afterguard",))
    assignment = hands.Assignment("x#1", wanted=want.hands or n, hands=men)
    return crew_factor(assignment, want, aloft=kw.get("aloft", False))


def test_crew_factor_for_the_rating_table():
    assert factor_for(ORD, ORD) == 1.0  # exactly: the compatibility rule rests on it
    assert factor_for(ABLE, ORD) == pytest.approx(0.75)
    assert factor_for(LAND, ORD) == pytest.approx(0.6 / 0.35)  # about 1.7
    assert 1.65 < factor_for(LAND, ORD) < 1.75
    assert factor_for(ABLE, ABLE) == 1.0 and factor_for(LAND, LAND) == 1.0
    assert factor_for(ORD, ORD, fatigue=0.3) == pytest.approx(1.125)  # 0.05 of it is 'fresh'
    assert factor_for(ORD, ORD, fatigue=1.0) == pytest.approx(
        1.0 + hands.FATIGUE_WEIGHT * (1.0 - hands.FATIGUE_FRESH)
    )
    assert factor_for(ORD, ORD, n=8, hands=12) == pytest.approx(1.5)  # twelve hands' work by eight
    assert factor_for(ORD, ORD, n=16, hands=12) == 1.0  # never faster for extra hands
    assert factor_for(ORD, ORD, aloft=True) == 1.0
    assert factor_for(Rating.MARINE, ORD) == pytest.approx(1.5)


def test_crew_factor_reads_the_rating_not_the_hands_own_skill():
    men = [sailor(i, Rating.ORDINARY, Station.AFTERGUARD) for i in range(4)]
    for i, s in enumerate(men):
        s.skill_deck = 0.55 + 0.03 * i  # the muster's seeded spread
    want = CrewRequest(hands=4, rating=Rating.ORDINARY)
    assert crew_factor(hands.Assignment("x", 4, men), want, aloft=False) == 1.0


def test_all_hands_go_at_the_files_pace_less_only_fatigue():
    crew = small_company()
    want = CrewRequest.from_mapping({"hands": "all", "rating": "ordinary"})
    got = request(crew, crew.sailors, "tack#1", want, None)
    assert got.all_hands and got.got == 12
    assert crew_factor(got, want, aloft=False) == 1.0
    for s in crew.sailors:
        s.fatigue = 0.3
    assert crew_factor(got, want, aloft=False) == pytest.approx(1.125)
    late = sailor(13, Rating.ABLE, Station.FORECASTLE, Watch.LARBOARD)
    assert hands.top_up(got, [*crew.sailors, late]) == 1
    assert late.at == "tack#1" and got.got == 13


# ---------------------------------------------------------------------------
# the registry's aloft flag
# ---------------------------------------------------------------------------


def test_steps_may_be_marked_aloft():
    base = {
        "id": "x",
        "applies_to": {"class": "square"},
        "source": "Luce 1866, ch. XXIII",
    }
    evo = registry.parse_evolution(
        {**base, "steps": [{"do": "loose", "duration_s": 90, "aloft": True}, {"do": "sheet"}]}
    )
    assert [s.aloft for s in evo.steps] == [True, False]
    with pytest.raises(registry.EvolutionFileError, match="aloft must be true or false"):
        registry.parse_evolution({**base, "steps": [{"do": "loose", "aloft": "yes"}]})


# ---------------------------------------------------------------------------
# the runner: short-handed on the schooner (truth 21's mechanism)
# ---------------------------------------------------------------------------


def test_the_schooners_watch_cannot_set_three_sails_at_once():
    w = world(SCHOONER)
    crew = w.ship.extra["crew"]
    assert 14 <= len(bill.on_deck(crew, w.clock)) <= 18  # her watch: about fifteen hands
    n0 = len(w.log)
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(order)
    runner = runner_of(w)
    snap = {s["subject"]: s for s in runner.in_progress()}
    assert snap["fore.topsail"]["hands"] == 12 and not snap["fore.topsail"]["waiting"]
    assert snap["fore.sail"]["waiting"] is False and 5 <= snap["fore.sail"]["hands"] < 10
    assert snap["main.sail"]["waiting"] is True and snap["main.sail"]["waiting_for"] == "hands"
    w.tick()
    lines = [(e.severity.value, e.kind, e.text) for e in log_after(w, n0)]
    short = [x for x in lines if x[1] == "evolution.short_handed"]
    wait = [x for x in lines if x[1] == "evolution.waiting"]
    assert short == [
        (
            "routine",
            "evolution.short_handed",
            "Only five hands to the foresail; the rest are setting the fore topsail.",
        )
    ]
    assert wait == [
        (
            "notable",
            "evolution.waiting",
            "Not hands enough on deck to set the mainsail; "
            "the watch is setting the fore topsail and the foresail.",
        )
    ]
    tick_until_idle(w)
    assert all(w.ship.sails[s].is_set for s in ("fore.topsail", "fore.sail", "main.sail"))
    kinds = [e.kind for e in log_after(w, n0)]
    assert kinds.count("evolution.waiting") == 1  # said once, though tried every tick
    # the mainsail began only when the topsail's hands came down
    topsail_set = next(e.tick for e in w.log if e.kind == "sail.set" and "topsail" in e.text)
    main_start = next(
        e.tick for e in w.log if e.kind == "evolution.started" and "mainsail" in e.text
    )
    assert main_start == topsail_set
    assert all(s.at is None for s in crew.sailors)  # every hand given back


def test_with_all_hands_called_the_schooner_sets_all_three():
    w = world(SCHOONER)
    w.ship.extra["crew"].all_hands_called = True
    n0 = len(w.log)
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(order)
    assert not any(s["waiting"] for s in runner_of(w).in_progress())
    ticks = tick_until_idle(w)
    kinds = [e.kind for e in log_after(w, n0)]
    assert "evolution.waiting" not in kinds and "evolution.short_handed" not in kinds
    bare = world(SCHOONER, crewed=False)
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        bare.submit(order)
    assert ticks == tick_until_idle(bare)  # as fast as milestone 2's unlimited hands


def test_a_ship_without_a_crew_takes_every_order_at_once():
    w = world(SCHOONER, crewed=False)
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(order)
    snap = runner_of(w).in_progress()
    assert [s["waiting"] for s in snap] == [False, False, False]
    assert [s["hands"] for s in snap] == [0, 0, 0]


def test_the_runner_reads_the_bill_at_the_default_time_without_a_clock():
    w = world(SCHOONER)
    runner = runner_of(w)
    runner.clock = None
    crew = w.ship.extra["crew"]
    w.submit("set the fore topsail")
    at_work = [s for s in crew.sailors if s.at is not None]
    on_deck = {s.id for s in bill.on_deck(crew, DEFAULT_WATCH_TIME)}
    assert len(at_work) == 12 and all(s.id in on_deck for s in at_work)


# ---------------------------------------------------------------------------
# the runner: all hands and pre-emption (truth 19's mechanism)
# ---------------------------------------------------------------------------


class FakeRoutine:
    """Stands in for package 18's routine: records the runner's calls."""

    def __init__(self, crew: Crew):
        self.crew = crew
        self.calls: list[tuple[str, Any]] = []

    def call_all_hands(self, reason: str) -> None:
        self.calls.append(("call_all_hands", reason))
        self.crew.all_hands_called = True

    def pipe_down(self) -> None:
        self.calls.append(("pipe_down", None))

    def tick(self, ship: Any, dt: float) -> list:
        return []  # the world ticks the routine; the fake has no watches to keep
        self.crew.all_hands_called = False


def close_hauled_frigate(crewed_setup: bool = True):
    """The frigate under plain sail, close-hauled on the starboard tack with way on."""
    w = world(FRIGATE, heading=292.5, speed_kn=4.0)
    crew = w.ship.extra["crew"]
    if not crewed_setup:
        w.ship.extra.pop("crew")
    w.submit("set plain sail")
    w.submit("brace sharp up on the starboard tack")
    for i in range(1200):
        if i % 120 == 0:
            w.submit("trim sails")
        w.tick()
    w.ship.extra["crew"] = crew
    assert not runner_of(w).in_progress()
    return w


def test_tack_ship_belays_the_topgallant_being_set_and_it_resumes_after():
    """Milestone 3b (spec 3b §7, spec M3 §9 item 12): told with a sail the watch may
    legitimately be setting close-hauled, the fore topgallant; studding sails are taken in
    before going about (tests/test_studding.py)."""
    w = close_hauled_frigate()
    crew = w.ship.extra["crew"]
    routine = FakeRoutine(crew)
    runner = runner_of(w)
    stun = "fore.topgallant"
    w.submit("take in the fore topgallant")
    tick_until_idle(w)
    w.ship.extra["routine"] = routine
    w.submit("set the fore topgallant")
    w.run(60)
    before = runner.in_progress()[0]
    assert before["id"] == "set_square" and before["hands"] > 0
    assert before["step"] not in ("waiting", "paused", "done")
    n0 = len(w.log)
    w.submit("tack ship")
    assert routine.calls == [("call_all_hands", "to tack ship")]
    snap = {s["id"]: s for s in runner.in_progress()}
    assert snap["set_square"]["paused"] is True and snap["set_square"]["step"] == "paused"
    assert snap["set_square"]["hands"] == 0
    held = runner.instances[0].progress
    w.tick()
    belay = [e for e in log_after(w, n0) if e.kind == "evolution.belayed"]
    assert [e.text for e in belay] == ["Belayed setting the fore topgallant: all hands about ship."]
    assert belay[0].severity.value == "notable"
    tack = next(i for i in runner.instances if i.evo.id == "tack")
    assert tack.assignment.got == len(bill.on_deck(crew, w.clock))  # everyone on deck
    w.run(30)
    assert runner.instances[0].progress == held  # its progress holds while belayed
    done = []
    t = 0
    while not done and t < 900:
        w.tick()
        t += 1
        done = [e for e in log_after(w, n0) if e.kind in ("ship.tacked", "ship.missed_stays")]
    assert [e.kind for e in done] == ["ship.tacked"]
    assert 300 <= t + 31 <= 600  # the tack takes what it took in milestone 2
    assert ("pipe_down", None) in routine.calls
    tick_until_idle(w)
    after = log_after(w, n0)
    set_at = next(e.tick for e in after if e.kind == "sail.set")
    assert set_at > done[0].tick
    assert w.ship.sails[stun].state is SailState.SET
    assert [e.kind for e in after].count("evolution.belayed") == 1
    assert all(s.at is None for s in crew.sailors)


def test_the_runner_does_not_pipe_down_when_the_captain_called_all_hands():
    w = close_hauled_frigate(crewed_setup=False)
    crew = w.ship.extra["crew"]
    routine = FakeRoutine(crew)
    w.ship.extra["routine"] = routine
    crew.all_hands_called = True
    crew.all_hands_called_by_order = True
    w.submit("tack ship")
    tick_until_idle(w, 900)
    assert routine.calls == []  # already called; and not piped down after


# ---------------------------------------------------------------------------
# log words
# ---------------------------------------------------------------------------


def test_gerunds_for_the_log():
    assert [gerund(v) for v in ("set", "take", "furl", "reef", "shake", "brace")] == [
        "setting",
        "taking",
        "furling",
        "reefing",
        "shaking",
        "bracing",
    ]
    assert [gerund(v) for v in ("tack", "wear", "heave", "fill", "fid", "lie", "sway")] == [
        "tacking",
        "wearing",
        "heaving",
        "filling",
        "fidding",
        "lying",
        "swaying",
    ]


# ---------------------------------------------------------------------------
# the compatibility rule (spec M3 §1)
# ---------------------------------------------------------------------------

_UNDER_SAIL = ["set plain sail", "brace sharp up on the starboard tack"]

# evolution: (orders that make ready, the order that runs it). The make-ready orders run
# one at a time to completion. `furl_gaff` and `furl_jibheaded` have no order in the
# language (a fore-and-aft sail is taken in, not furled), so they are started on the
# runner of the same World.
COMPAT_CASES: dict[str, tuple[list[str], str]] = {
    "set_square": ([], "set the fore topsail"),
    "take_in_square": (["set the fore topsail"], "take in the fore topsail"),
    "furl_square": (["set the fore topsail", "take in the fore topsail"], "furl the fore topsail"),
    "reef_square": (["set the main topsail"], "reef the main topsail"),
    "shake_out_square": (
        ["set the main topsail", "reef the main topsail"],
        "shake out a reef in the main topsail",
    ),
    "set_gaff": ([], "set the spanker"),
    "take_in_gaff": (["set the spanker"], "take in the spanker"),
    "furl_gaff": (["set the spanker", "take in the spanker"], "runner: furl_gaff mizzen.spanker"),
    "reef_gaff": (["set the spanker"], "reef the spanker"),
    "shake_out_gaff": (["set the spanker", "reef the spanker"], "shake out a reef in the spanker"),
    "set_jibheaded": ([], "set the jib"),
    "take_in_jibheaded": (["set the jib"], "haul down the jib"),
    "furl_jibheaded": (["set the jib", "haul down the jib"], "runner: furl_jibheaded jib"),
    # milestone 3b: the booms start rigged in (spec 3b §7); rigging one out is make-ready
    "set_studding": (
        ["set the fore topsail", "rig out the starboard fore topmast studdingsail boom"],
        "set the starboard fore topmast studdingsail",
    ),
    "take_in_studding": (
        [
            "set the fore topsail",
            "rig out the starboard fore topmast studdingsail boom",
            "set the starboard fore topmast studdingsail",
        ],
        "take in the starboard fore topmast studdingsail",
    ),
    "brace": ([], "brace the main yard in"),
    "tack": (_UNDER_SAIL, "tack ship"),
    "wear": (_UNDER_SAIL, "wear ship"),
    "heave_to": (_UNDER_SAIL, "heave to"),
    "fill_away": ([*_UNDER_SAIL, "heave to"], "fill away"),
}


def run_alone(eid: str, crewed: bool) -> tuple[int, list[str], int]:
    """Make ready without a crew, then (crewed or not) give the one order and count the
    ticks until nothing is in progress. Returns (ticks, the log's kinds, hands at it)."""
    setup, order = COMPAT_CASES[eid]
    w = world(FRIGATE, heading=292.5, speed_kn=4.0)
    crew = w.ship.extra.pop("crew")
    runner = runner_of(w)
    for text in setup:
        w.submit(text)
        tick_until_idle(w, 900)
    w.run(600 if setup == _UNDER_SAIL or "heave to" in setup else 0)
    if crewed:
        w.ship.extra["crew"] = crew
        # the watch on deck and nobody else; nobody at work
        assert not crew.all_hands_called and all(s.at is None for s in crew.sailors)
    n0 = len(w.log)
    if order.startswith("runner: "):
        evo, subject = order.removeprefix("runner: ").split()
        runner.start(w.ship, evo, subject)
    else:
        event = w.submit(order)
        assert event.kind != "order.rejected", event.text
    snap = runner.in_progress()
    assert [s["id"] for s in snap] == [eid], snap
    assert not snap[0]["waiting"], snap
    at_it = snap[0]["hands"]
    ticks = tick_until_idle(w)
    # the clock's bells and the routine's own lines (watch reliefs, all hands coming up)
    # are not the evolution's doing
    kinds = [
        e.kind
        for e in log_after(w, n0)
        if e.kind != "clock.bell" and not e.kind.startswith(("crew.", "watch."))
    ]
    return ticks, kinds, at_it


@pytest.mark.parametrize("eid", M2_EVOLUTIONS)
def test_compatibility_one_evolution_with_the_watch_on_deck(eid):
    assert set(COMPAT_CASES) == set(M2_EVOLUTIONS)
    bare, bare_kinds, _ = run_alone(eid, crewed=False)
    crewed, crewed_kinds, at_it = run_alone(eid, crewed=True)
    assert at_it > 0  # the crewed run really drew hands from the watch
    assert crewed == bare, f"{eid}: {crewed} ticks with the watch, {bare} without a crew"
    assert crewed_kinds == bare_kinds
    assert "evolution.short_handed" not in crewed_kinds
    assert "evolution.failed" not in crewed_kinds


# ---------------------------------------------------------------------------
# setting from the gear (package 29b, the owner's item 9)
# ---------------------------------------------------------------------------

# (the order's sail, its evolution, the stow step and the gear step in its file, the log's
# start from furled and from the gear)
FROM_THE_GEAR = [
    (
        "fore topsail",
        "fore.topsail",
        "set_square",
        "loose",
        "let_go_gear",
        "Hands aloft to loose the fore topsail.",
        "Man the fore topsail sheets; let go the clewlines and buntlines.",
    ),
    (
        "spanker",
        "mizzen.spanker",
        "set_gaff",
        "clear_away",
        "let_go_brails",
        "Hands to the spanker halyards and outhaul.",
        "Hands to the spanker halyards and outhaul.",
    ),
    (
        "jib",
        "jib",
        "set_jibheaded",
        "clear_away",
        "let_go_downhaul",
        "Clear away the jib; man the halyards.",
        "Let go the jib downhaul; man the halyards.",
    ),
]


def _set_once(w, name: str, sid: str) -> tuple[int, list, bool, int]:
    """Set the sail now; the ticks it took, the log since, whether its hands were taken
    as for work aloft, and how many of them go aloft by their rating."""
    runner = runner_of(w)
    n0 = len(w.log)
    w.submit(f"set the {name}")
    inst = next(i for i in runner.instances if i.subject_id == sid)
    aloft = runner._aloft(inst)
    t = tick_until_idle(w)
    return t, log_after(w, n0), aloft, inst.evo.id


@pytest.mark.parametrize("case", FROM_THE_GEAR, ids=[c[2] for c in FROM_THE_GEAR])
def test_a_sail_set_from_the_gear_skips_the_stow_and_wants_no_hands_aloft(case):
    """Each state a sail is set from is its own case: from furled the file's stow step
    runs (loosing aloft, clearing away); from in the gear a short deck step takes its
    place, no hand is sent aloft for it, the later steps are the same, and the sail ends
    set. The difference in time is the difference of the two steps at the weather's
    pace; and the log says what is done."""
    name, sid, eid, stow, gear, start_furled, start_gear = case
    w = world(FRIGATE, heading=90.0)  # the wind on the beam, 15 knots
    evo = registry.get(eid)
    steps = {s.do: s for s in evo.steps}
    assert steps[gear].aloft is False and steps[gear].duration_s < steps[stow].duration_s
    furled_t, furled_log, _, _ = _set_once(w, name, sid)
    assert w.ship.sails[sid].state is SailState.SET
    w.submit(f"take in the {name}")
    tick_until_idle(w)
    assert w.ship.sails[sid].state is SailState.IN_THE_GEAR
    factor = runner_of(w)._last_factor
    gear_t, gear_log, aloft, _ = _set_once(w, name, sid)
    assert w.ship.sails[sid].state is SailState.SET
    assert not aloft, "hands were sent aloft for a sail already loose"
    saved = (steps[stow].duration_s - steps[gear].duration_s) * factor
    assert furled_t - gear_t == pytest.approx(saved, abs=3), (furled_t, gear_t)
    started = [e.text for e in furled_log if e.kind == "evolution.started"]
    assert started[0] == start_furled
    started = [e.text for e in gear_log if e.kind == "evolution.started"]
    assert started[0] == start_gear
    assert "Laid aloft and loosed" not in " ".join(e.text for e in gear_log)


# ---------------------------------------------------------------------------
# Belaying work, and a party too small refused at once (package 29c, playtest 8)
# ---------------------------------------------------------------------------

DAYTIME = datetime(1805, 6, 1, 10, 0, 0)  # the idlers are on deck by day


def three_sails_on_the_schooner():
    """The schooner's watch told to set three sails at once: the fore topsail and the
    foresail begin, the mainsail waits for hands (as above)."""
    w = world(SCHOONER)
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(order)
    snap = {s["subject"]: s for s in runner_of(w).in_progress()}
    assert snap["main.sail"]["waiting_for"] == "hands"
    return w


def belayed_lines(w, n0: int) -> list:
    return [e for e in log_after(w, n0) if e.kind == "work.belayed"]


@pytest.mark.parametrize(
    "said",
    [
        "belay setting the mainsail",  # as the log names it
        "belay set the mainsail",  # as the order gave it
        "belay the mainsail",  # by its sail: every job on it
        "cancel setting the mainsail",
        "avast setting the mainsail",
        "belay the work on the mainsail",
    ],
)
def test_belay_the_work_by_its_name_its_order_or_its_sail(said):
    """Work waiting for hands is gone at the captain's word, and the sail it held is free
    (playtest 8: the mainsail held for a session by a reef that waited for hands)."""
    w = three_sails_on_the_schooner()
    runner = runner_of(w)
    n0 = len(w.log)
    e = w.submit(said)
    assert e.kind == "work.belayed" and e.severity.value == "notable"
    assert e.text == "Belayed setting the mainsail; not begun, it was waiting for hands."
    assert e.data["belayed"][0]["was"] == "waiting"
    assert [s["subject"] for s in runner.in_progress()] == ["fore.topsail", "fore.sail"]
    assert w.ship.sails["main.sail"].state is SailState.FURLED
    assert [x.text for x in belayed_lines(w, n0)] == [e.text]
    assert w.journal[-1][2] == said  # an order, journaled
    tick_until_idle(w)
    assert w.ship.sails["main.sail"].state is SailState.FURLED  # gone, not paused
    assert "evolution.belayed" not in [x.kind for x in log_after(w, n0)]


def test_a_sail_half_set_is_left_as_its_last_finished_step_left_it():
    w = three_sails_on_the_schooner()
    runner = runner_of(w)
    crew = w.ship.extra["crew"]
    top = w.ship.sails["fore.topsail"]
    while top.state is SailState.FURLED:  # the topmen lay aloft and loose it
        w.tick()
    assert top.state is SailState.LOOSED
    w.run(5)  # into the next step, which has not finished
    e = w.submit("belay the fore topsail")
    assert e.text == (
        "Belayed setting the fore topsail; the fore topsail left loosed and hanging from the yard."
    )
    assert e.data["belayed"][0]["was"] == "in hand" and e.data["belayed"][0]["state"] == "loosed"
    assert "fore.topsail" not in [s["subject"] for s in runner.in_progress()]
    inst_ids = {i.inst_id for i in runner.instances}
    assert all(s.at is None or s.at in inst_ids for s in crew.sailors)  # its hands released
    tick_until_idle(w)
    assert top.state is SailState.LOOSED  # nothing of it resumes
    assert w.ship.sails["main.sail"].state is SailState.SET  # the mainsail had its hands


def test_belay_that_is_the_last_order_whose_work_is_still_in_hand_or_waiting():
    w = world(FRIGATE)
    runner = runner_of(w)
    w.submit("set the courses")
    w.submit("set the topsails")  # one order, three evolutions
    w.submit("set the jib")
    while w.ship.sails["jib"].state is not SailState.SET:
        w.tick()
    # the jib is set and done: the last order with work in hand is the topsails'
    topsails = ["fore.topsail", "main.topsail", "mizzen.topsail"]
    courses = {"fore.course", "main.course"}
    assert {s["subject"] for s in runner.in_progress()} == set(topsails) | courses
    e = w.submit("belay that")
    assert e.kind == "work.belayed"
    assert e.text.startswith("Belayed setting the fore topsail (the fore topsail left ")
    assert [b["subject"] for b in e.data["belayed"]] == topsails
    assert {s["subject"] for s in runner.in_progress()} == courses
    e = w.submit("belay")  # said bare, it is "belay that": now the courses
    assert e.kind == "work.belayed" and {b["subject"] for b in e.data["belayed"]} == courses
    e = w.submit("belay that")
    assert e.kind == "order.rejected"
    assert e.text.endswith("There is no work in hand or waiting to belay.")


def test_belay_all_work_leaves_the_ship_as_she_is_and_keeps_the_line_verb():
    w = three_sails_on_the_schooner()
    w.run(30)
    e = w.submit("cancel all orders")
    assert e.kind == "work.belayed"
    assert e.text.startswith("Belayed all work, the ship left as she is: setting the ")
    assert "setting the mainsail (not begun, it was waiting for hands)" in e.text
    assert runner_of(w).in_progress() == []
    assert all(s.at is None for s in w.ship.extra["crew"].sailors)
    # a line is still belayed at its pin
    e = w.submit("belay the main sheet")
    assert e.kind == "line.belay"
    # the forms the captain of playtest 8 reached for (the save's inputs) are all taken
    for said in ("Belay that", "Belay", "Belay all", "Belay all work", "Cancel all work"):
        e = w.submit(said)
        assert e.kind == "order.rejected", said
        assert e.text.endswith("There is no work in hand or waiting to belay."), said


def test_belaying_a_tack_is_not_the_tacks_belay_and_the_work_it_held_resumes():
    """Decision 25's belay (all hands about ship) keeps its line and its hold; belaying the
    tack at the captain's word lets the work it held take up again."""
    w = close_hauled_frigate()
    runner = runner_of(w)
    w.submit("take in the fore topgallant")
    tick_until_idle(w)
    w.submit("set the fore topgallant")
    w.run(60)
    n0 = len(w.log)
    w.submit("tack ship")
    w.run(20)
    held = [e.text for e in log_after(w, n0) if e.kind == "evolution.belayed"]
    assert held == ["Belayed setting the fore topgallant: all hands about ship."]
    e = w.submit("belay that")
    assert e.kind == "work.belayed"
    assert e.text.startswith("Belayed tacking ship; the helm and the yards left as they stand")
    assert [s["id"] for s in runner.in_progress()] == ["set_square"]
    tick_until_idle(w)
    assert w.ship.sails["fore.topgallant"].state is SailState.SET


def test_belaying_refuses_in_words_and_names_the_work_in_hand():
    w = world(SCHOONER)
    e = w.submit("belay the reef")
    assert e.kind == "order.rejected"
    assert e.text.endswith("There is no work in hand or waiting to belay.")
    w.submit("set the jib")
    e = w.submit("belay the reef in the mainsail")
    assert e.kind == "order.rejected"
    assert "Nothing in hand or waiting is reefing the mainsail." in e.text
    assert e.text.endswith("The work in hand: setting the jib.")
    e = w.submit("belay the work")
    assert e.kind == "order.rejected"
    assert e.text.split("): ", 1)[1].startswith("Belay which work?")


def test_a_named_party_that_cannot_man_the_job_is_refused_at_once():
    """Playtest 8: 'reef the mainsail, one reef with the idlers' waited for hands the
    schooner's idlers could never give. A party with fewer than half the hands the work
    wants is refused, with the numbers; the general case still waits (spec M3 §3.2)."""
    w = world(SCHOONER, start_time=DAYTIME)
    crew = w.ship.extra["crew"]
    idlers = [s for s in crew.sailors if s.station is Station.IDLERS and s.fit]
    assert len(idlers) == 4
    w.submit("set the mainsail")
    w.submit("set the jib")
    tick_until_idle(w)
    e = w.submit("reef the mainsail, one reef with the idlers")
    assert e.kind == "order.rejected"
    assert e.text == (
        "Order not carried out ('reef the mainsail, one reef with the idlers'): The idlers "
        "are four; reefing the mainsail wants ten. Call all hands, or name the watch."
    )
    assert runner_of(w).in_progress() == []  # not queued
    # half the hands wanted is enough to begin, short-handed: the idlers take in the jib
    assert w.submit("take in the jib with the idlers").kind != "order.rejected"
    tick_until_idle(w)
    # a watch that can man it is taken as ever
    e = w.submit("reef the mainsail, one reef with the starboard watch")
    assert e.kind != "order.rejected"


def test_the_crew_factor_aloft_falls_with_the_roll_in_a_seaway():
    """Package 31 (spec M5 §4): the roll's table (`hands.seaway_factor`) multiplies the
    crew factor, aloft above all; under its first row (a smooth sea, or no sea) it is
    exactly 1.0, so the compatibility rule and every timed truth stand."""
    assert factor_for(ORD, ORD, aloft=True) == 1.0
    assert hands.seaway_factor(hands.SEAWAY_FACTOR_TABLE[0][0], True) == 1.0
    men = [sailor(i, ORD, Station.AFTERGUARD) for i in range(12)]
    want = CrewRequest(hands=12, rating=ORD, stations=("afterguard",))
    got = hands.Assignment("x#1", wanted=12, hands=men)
    for roll in (0.0, 2.0, 3.0):
        assert crew_factor(got, want, aloft=True, roll_deg=roll) == 1.0
    aloft = crew_factor(got, want, aloft=True, roll_deg=15.0)
    deck = crew_factor(got, want, aloft=False, roll_deg=15.0)
    assert aloft == hands.seaway_factor(15.0, True) > deck == hands.seaway_factor(15.0, False) > 1.0
    for s in men:
        s.fatigue = 0.3
    assert crew_factor(got, want, aloft=True, roll_deg=15.0) == pytest.approx(1.125 * aloft)
    # all hands too: the whole company's pace, less fatigue, times the seaway
    crew = small_company()
    call = CrewRequest.from_mapping({"hands": "all", "rating": "ordinary"})
    all_hands = request(crew, crew.sailors, "tack#1", call, None)
    assert crew_factor(all_hands, call, aloft=True, roll_deg=15.0) == pytest.approx(aloft)
    # the runner reads the ship's motion: none aboard, the factor is 1.0
    w = world(FRIGATE)
    runner = w.ship.extra["evolutions"]
    w.submit("set the fore topsail")
    w.tick()
    assert runner._roll_deg == 0.0


# ---------------------------------------------------------------------------
# all hands manned in parallel, with a bound on any one job (package 31b; spec M3 §3.2)
# ---------------------------------------------------------------------------


def test_a_party_bounds_an_all_hands_request_and_the_top_up():
    """A file's ``party: N`` beside ``hands: all`` takes N of the idle hands, the
    subject's own top and the rating wanted first, and leaves the rest idle; the top-up
    joins hands only up to the party; wanted is the party, so the numbers term is 1.0 at
    it and no less beyond it."""
    crew = small_company()
    want = CrewRequest.from_mapping(
        {"hands": "all", "party": 4, "rating": "ordinary", "stations": ["topmen", "all hands"]}
    )
    assert want.all_hands and want.party == 4
    got = request(crew, crew.sailors, "reef#1", want, "main")
    assert got.all_hands and got.party == 4 and got.wanted == 4 and got.got == 4
    assert got.outcome == hands.ENOUGH
    # the main top's ordinary seaman and the fore top's are in the party: the tops first
    assert "s010" in ids(got.hands) and "s011" in ids(got.hands)
    assert sum(1 for s in crew.sailors if s.at is None) == 8  # the surplus stays idle
    assert crew_factor(got, want, aloft=False) == 1.0
    late = sailor(13, Rating.ORDINARY, Station.MAIN_TOP, Watch.LARBOARD)
    assert hands.top_up(got, [*crew.sailors, late], want=want, subject_mast="main") == 0
    assert late.at is None and got.got == 4
    # a hand released: the top-up fills the party again, and no further
    got.hands.pop().at = None
    assert got.got == 3 and crew_factor(got, want, aloft=False) == pytest.approx(4 / 3)
    assert hands.top_up(got, [*crew.sailors, late], want=want, subject_mast="main") == 1
    assert got.got == 4 and got.wanted == 4
    # more hands than the party are never faster
    over = hands.Assignment("x", wanted=4, hands=got.hands + [late], all_hands=True, party=4)
    assert crew_factor(over, want, aloft=False) == 1.0
    # without a party everyone is taken, as before
    release(crew, "reef#1")
    everyone = CrewRequest.from_mapping({"hands": "all", "rating": "ordinary"})
    assert request(crew, crew.sailors, "tack#1", everyone, None).got == 12


def test_a_party_is_a_number_beside_hands_all_and_nothing_else():
    with pytest.raises(CrewRequestError, match="a party is a number of hands"):
        CrewRequest.from_mapping({"hands": "all", "party": 0})
    with pytest.raises(CrewRequestError, match="a party is a number of hands"):
        CrewRequest.from_mapping({"hands": "all", "party": "forty"})
    with pytest.raises(CrewRequestError, match="beside 12 hands"):
        CrewRequest.from_mapping({"hands": 12, "party": 40})
    for eid in ("reef_square", "furl_all", "loose_sails_to_dry"):
        want = CrewRequest.from_mapping(EVOLUTIONS[eid].crew)
        assert want.all_hands and want.party is not None and want.party > 0, eid
    for eid in ("tack", "wear", "send_down_topgallant_masts", "strike_topmasts"):
        assert CrewRequest.from_mapping(EVOLUTIONS[eid].crew).party is None, eid


def test_a_numbered_request_may_call_all_hands_where_the_deck_is_too_few_and_nothing_else():
    """Package 75, the lead's ruling (1) of 2026-11-10 (the bilander's short watch): a file's
    ``too_few: all hands`` beside a number (`CrewRequest.calls_all_hands`) is read; the deck is too
    few for it where its hands, idle or at other work, are fewer than half its number after the
    company's clamp (`hands.too_few_on_deck`), so that a watch busy at other work is not too few;
    called, it is all-hands work of the same rating and stations, its party its number
    (`as_all_hands`). Any other word, or the key beside all hands or none, is refused in words;
    no file but the settee's four and the boat's carries it (`tests/test_settee.py`)."""
    crew = small_company()
    want = CrewRequest.from_mapping(
        {
            "hands": 6,
            "rating": "able",
            "stations": ["forecastle", "afterguard"],
            "too_few": "all hands",
        }
    )
    assert want.calls_all_hands and want.hands == 6 and not want.all_hands
    called = want.as_all_hands()
    assert called.all_hands and called.party == 6 and not called.calls_all_hands
    assert (called.rating, called.stations) == (want.rating, want.stations)
    assert not CrewRequest.from_mapping({"hands": 6}).calls_all_hands
    deck = crew.sailors[:2]
    assert hands.too_few_on_deck(crew, deck, want)  # two of six: fewer than half
    assert not hands.too_few_on_deck(crew, crew.sailors[:3], want)  # three: begun short-handed
    for s in crew.sailors[:3]:
        s.at = "brace#1"  # at other work: waits for it, as before, and calls nobody
    assert not hands.too_few_on_deck(crew, crew.sailors[:3], want)
    assert not hands.too_few_on_deck(crew, deck, called)
    with pytest.raises(CrewRequestError, match="say 'all hands', or leave it out"):
        CrewRequest.from_mapping({"hands": 6, "too_few": "wait"})
    with pytest.raises(CrewRequestError, match="beside all hands"):
        CrewRequest.from_mapping({"hands": "all", "too_few": "all hands"})
    with pytest.raises(CrewRequestError, match="beside no hands"):
        CrewRequest.from_mapping({"hands": 0, "too_few": "all hands"})


def test_a_numbered_request_may_call_all_hands_until_it_is_manned_and_an_old_call_loads():
    """Package 75, the lead's ruling 10 of 2026-11-13 (package 109's boat and the settee's key made
    one road): a file's ``too_few: all hands until manned`` calls all hands as ``all hands`` does
    (`CrewRequest.calls_all_hands`, `too_few_on_deck`), but the work keeps its number and the hands
    are piped down once it is manned (`until_manned`; the runner's `_manning` and
    `_after_all_hands`), not when it ends; the boat's file alone says it (her short watch sailed in
    `tests/test_mends_109.py` and truth 7-542). Any other word is refused naming both. A checkpoint
    taken on the trunk while all hands came up to man the boat by package 109's own road (its mark
    `hands_called_for` on the work's params) loads as this road's mark of the same call
    (`Instance.held_up`), the mark gone; an instance without it loads as it was. The review of
    ruling 10: one taken before the boat's file said the key (on the trunk, or before package 109),
    her crew line read then and her file held as it was, loads with the key read, so that she calls
    for her hands as on the trunk; a numbered request of a file without the key loads unchanged."""
    import io
    import pickle
    from dataclasses import replace

    from freesail.core import replay
    from freesail.evolutions.runner import Instance

    want = CrewRequest.from_mapping({"hands": 6, "too_few": " All  hands until manned "})
    assert want.calls_all_hands and want.until_manned and want.hands == 6 and not want.all_hands
    assert not CrewRequest.from_mapping({"hands": 6, "too_few": "all hands"}).until_manned
    assert not CrewRequest.from_mapping({"hands": 6}).until_manned
    manned = {
        eid for eid, evo in EVOLUTIONS.items() if CrewRequest.from_mapping(evo.crew).until_manned
    }
    assert manned == {"send_boat"}
    assert CrewRequest.from_mapping(EVOLUTIONS["send_boat"].crew).calls_all_hands
    with pytest.raises(CrewRequestError, match="'all hands until manned' pipes them down"):
        CrewRequest.from_mapping({"hands": 6, "too_few": "all hands until done"})
    with pytest.raises(CrewRequestError, match="beside all hands"):
        CrewRequest.from_mapping({"hands": "all", "too_few": "all hands until manned"})

    boat = EVOLUTIONS["send_boat"]

    def loaded(
        params: dict[str, Any], evo: Any = boat, want: CrewRequest | None = None
    ) -> Instance:
        inst = Instance(evo, None, "Hopewell", params, want=want)  # type: ignore[arg-type]
        buf = io.BytesIO()
        replay._Pickler(buf, protocol=pickle.HIGHEST_PROTOCOL).dump(inst)
        return replay._Unpickler(io.BytesIO(buf.getvalue())).load()

    old = loaded({"errand": "prices", "hands_called_for": True})
    assert old.held_up and old.waiting and old.params == {"errand": "prices"}
    plain = loaded({"errand": "prices"})
    assert not plain.held_up and plain.params == {"errand": "prices"}

    # written before the key: her file and her crew line as they were then
    file_then = replace(boat, crew={k: v for k, v in boat.crew.items() if k != "too_few"})
    then = CrewRequest(hands=11, stations=("forecastle", "afterguard", "waisters"))
    assert not CrewRequest.from_mapping(file_then.crew).calls_all_hands
    waiting = loaded({"errand": "prices"}, file_then, then)
    assert waiting.want is not None
    assert waiting.want.until_manned and waiting.want.calls_all_hands
    assert waiting.want == replace(then, calls_all_hands=True, until_manned=True)
    assert not waiting.held_up and waiting.params == {"errand": "prices"}
    now = CrewRequest.from_mapping(boat.crew)
    assert loaded({"errand": "prices"}, boat, now).want == now
    log = CrewRequest.from_mapping(EVOLUTIONS["heave_log"].crew)
    assert log.hands == 3 and not log.calls_all_hands
    assert loaded({}, EVOLUTIONS["heave_log"], log).want == log


def test_three_topsails_are_reefed_together_each_up_to_its_party_and_the_surplus_goes_on():
    """Playtest 11's finding 14 and the owner's ruling (decision 28): "reef the topsails"
    on the frigate begins all three reefs on the one tick, forty hands each (the file's
    party), never more on any tick as the watch below comes up, and the surplus mans a
    fourth job given behind them; the three end together, in the time one took alone."""
    w = world(FRIGATE, heading=90.0, speed_kn=4.0)
    crew = w.ship.extra["crew"]
    runner = runner_of(w)
    w.submit("set plain sail")
    tick_until_idle(w)
    party = CrewRequest.from_mapping(EVOLUTIONS["reef_square"].crew).party
    assert party == 40
    n0 = len(w.log)
    t0 = w.clock.tick
    w.submit("reef the topsails, one reef")
    w.submit("take in the jib")
    snap = {s["subject"]: s for s in runner.in_progress()}
    topsails = ["fore.topsail", "main.topsail", "mizzen.topsail"]
    assert all(snap[s]["hands"] == party and not snap[s]["waiting"] for s in topsails)
    assert snap["jib"]["hands"] > 0 and not snap["jib"]["waiting"]  # the surplus
    most = 0
    while runner.in_progress():
        w.tick()
        for s in runner.in_progress():
            if s["id"] == "reef_square":
                most = max(most, s["hands"])
        assert w.clock.tick - t0 < 1200
    assert most == party  # never a hand over the party, though all hands came up
    reefed = [e for e in log_after(w, n0) if e.kind == "sail.reefed"]
    assert [e.subject for e in reefed] == topsails
    assert len({e.tick for e in reefed}) == 1  # together
    assert not [e for e in log_after(w, n0) if e.kind == "evolution.waiting"]
    assert [e.kind for e in log_after(w, n0)].count("crew.all_hands") == 1
    assert [e.kind for e in log_after(w, n0)].count("crew.piped_down") == 1
    assert all(s.at is None for s in crew.sailors)
    together = reefed[0].tick - t0
    # one topsail alone with all hands takes the same time (the party is at the file's pace)
    w2 = world(FRIGATE, heading=90.0, speed_kn=4.0)
    w2.submit("set plain sail")
    tick_until_idle(w2)
    t1 = w2.clock.tick
    w2.submit("reef the fore topsail, one reef")
    tick_until_idle(w2)
    alone = next(e.tick for e in w2.log if e.kind == "sail.reefed") - t1
    assert abs(together - alone) <= 2


def test_a_reef_short_of_its_party_begins_short_and_fills_as_hands_come_free():
    """The third topsail of "reef the topsails" given while the watch is setting the
    royals and the staysails: the first two take their parties from the deck and the third
    of the watch below who come up at the call, the third begins with what is left and says so once,
    routine, and fills to its party as the rest come up; the manoeuvres keep taking
    everyone (truth 19's tack), and the masts do too."""
    w = world(FRIGATE, heading=90.0, speed_kn=4.0)
    crew = w.ship.extra["crew"]
    runner = runner_of(w)
    w.submit("set plain sail")
    tick_until_idle(w)
    deck_aloft = [s for s in bill.on_deck(crew, w.clock) if hands.can_work(s, aloft=True)]
    assert 80 <= len(deck_aloft) < 120  # one watch: two parties and part of a third
    n0 = len(w.log)
    w.submit("set the royals")
    # package 57: the royals are set flying by four hands each on deck (set_flying.yaml),
    # where twelve laid aloft to loose each before; the staysails between the masts keep
    # the watch as busy as the royals did
    w.submit("set the staysails")
    w.submit("reef the topsails, one reef")
    snap = {s["subject"]: s for s in runner.in_progress()}
    assert snap["fore.topsail"]["hands"] == snap["main.topsail"]["hands"] == 40
    third = snap["mizzen.topsail"]["hands"]
    assert 0 < third < 40 and not snap["mizzen.topsail"]["waiting"]
    w.run(120)  # the watch below comes up over a minute and a half
    snap = {s["subject"]: s for s in runner.in_progress()}
    assert snap["mizzen.topsail"]["hands"] == 40
    # four hands each to sway up and set a flying royal (set_flying.yaml, package 57)
    assert all(snap[r]["hands"] == 4 for r in ("fore.royal", "main.royal", "mizzen.royal"))
    short = [e for e in log_after(w, n0) if e.kind == "evolution.short_handed"]
    assert len(short) == 1 and short[0].text.startswith(
        f"Only {number_words(third)} hands to the mizzen topsail; the rest are setting"
    )
    tick_until_idle(w)
    # the masts take everyone who goes aloft
    w.submit("send down the topgallant masts")
    w.run(120)
    (masts,) = runner.in_progress()
    assert masts["id"] == "send_down_topgallant_masts"
    assert masts["hands"] == sum(1 for s in bill.on_deck(crew, w.clock) if hands.can_work(s, True))


# ---------------------------------------------------------------------------
# A merchantman's master and mate, where the watch is too small (package 75, the lead's ruling 11)
# ---------------------------------------------------------------------------

BRIG = "data/ships/merchant-brig.yaml"


def trader_at(ship_file: str, hour: int, watch: Watch):
    """A trader at seed 7 off the Lizard (tests/test_brains.py's world, its start at `hour`), her
    people made, `watch` given the deck by the bill's own override, all hands not called."""
    from freesail.api.session import make_world as made

    sc = Scenario(
        start_time=datetime(1805, 6, 12, hour, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
    )
    w = made(SEED, ship_file, sc)
    _ = w.people.all
    crew = w.ship.extra["crew"]
    crew.watch_on_deck = watch
    return w, crew, w.ship.extra["evolutions"]


def asked(w, eid: str, sid: str | None, state: str | None = None):
    """The request made as `Runner.start` makes it, not yet given its hands."""
    from freesail.evolutions.runner import Instance
    from freesail.evolutions.scripts import SCRIPTS

    ship, runner = w.ship, w.ship.extra["evolutions"]
    if sid is not None and state is not None:
        ship.sails[sid].state = SailState(state)
    subject, subject_id = runner._resolve_subject(ship, sid or "her")
    evo = registry.get(eid)
    params = dict(evo.params)
    inst = Instance(evo=evo, subject=subject, subject_id=subject_id, params=params)
    if evo.script is not None:
        inst.script = SCRIPTS[evo.script](ship, params, runner._timing(ship, evo))
    inst.holds = runner._holds(ship, inst)
    inst.want = CrewRequest.from_mapping(evo.crew)
    runner.instances.append(inst)
    return inst


def taken(w, inst) -> list[str]:
    """Who the request takes: a post by its post, a hand by station and rating."""
    runner, crew = w.ship.extra["evolutions"], w.ship.extra["crew"]
    assert runner._take_hands(w.ship, inst, crew), inst.wait_line
    return [s.post or f"{s.station.value} {s.rating.value}" for s in inst.assignment.hands]


def test_a_merchantmans_post_hauls_only_where_the_watchs_whole_number_is_under_the_works_want():
    """The lead's ruling 11 of 2026-11-13 (the narrower form of ruling 9's probe), on the merchant
    brig at seed 7: her master and mate head the larboard and the starboard watch (her people file,
    read at the muster into `Crew.post_watches`; JUDGEMENT, the mate the starboard; their own
    `watch` stays the bill's, none), her watches seven and three hands as mustered. A
    post is counted a hand of their own watch for work on deck only where the watch's whole number
    (every hand of it on board and fit, whatever they are doing: `Runner._watch_whole`) is under the
    work's want (the request's own `wanted`, its file's number no more than the company could put to
    it), taken after every hand of the pool (`hands._tier`). By night in her larboard watch the jib
    from the gear wants six: the three are under it, so the master makes four. Her starboard's
    seven set it with six hands, the mate not counted; the braces want eight, so the mate makes
    the eighth. A watch busy at other work is not too small: with four of the starboard's seven at
    other work the jib is begun short with the three idle, the mate not taken (old, before the
    ruling, every case without the post: the larboard's three short, the brace's seven short)."""
    w, crew, runner = trader_at(BRIG, 2, Watch.LARBOARD)
    by = {s.post: s for s in crew.sailors if s.post}
    assert crew.post_watches == {"master": "larboard", "mate": "starboard"}
    heads = {p: hands.post_watch(crew, by[p]) for p in ("master", "mate", "second mate")}
    assert heads == {"master": Watch.LARBOARD, "mate": Watch.STARBOARD, "second mate": None}
    assert all(s.watch is Watch.NONE for s in crew.sailors if s.post)
    wholes = [runner._watch_whole(crew, w) for w in (Watch.STARBOARD, Watch.LARBOARD)]
    assert wholes == [7, 3]
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert taken(w, jib) == ["forecastle able", "fore_top able", "main_top able", "master"]
    assert jib.assignment.outcome == hands.SHORT and jib.assignment.wanted == 6

    w, crew, runner = trader_at(BRIG, 2, Watch.STARBOARD)
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert "mate" not in taken(w, jib) and jib.assignment.outcome == hands.ENOUGH
    brace = asked(w, "brace", None)
    hands.release(crew, jib.inst_id)
    by_brace = taken(w, brace)
    assert len(by_brace) == 8 and by_brace[-1] == "mate"

    w, crew, runner = trader_at(BRIG, 2, Watch.STARBOARD)
    busy = [s for s in crew.sailors if s.watch is Watch.STARBOARD and not s.post][:4]
    for s in busy:
        s.at = "other#1"
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert runner._working_posts(crew, jib) == []
    assert len(taken(w, jib)) == 3 and jib.assignment.outcome == hands.SHORT


def test_a_merchantmans_post_never_hauls_aloft_for_all_hands_for_a_manoeuvre_or_at_quarters():
    """Ruling 11, everything else as ruling 9's probe had it: a post is never counted for work
    aloft (her fore topsail furled: the larboard's three alone), for all-hands work, while all hands
    are called, for any of the twelve manoeuvres (`scripts.HELM_MANOEUVRES`) or while one is in
    hand, the officer of the deck giving it; and a manoeuvre begun takes a post from the work they
    hold back to the conn, the work going on short (`Runner._to_the_conn`). A post whose person is
    not free on deck (below, at a task) is not counted (`People.works_on_deck`)."""
    from freesail.evolutions.scripts import HELM_MANOEUVRES

    assert len(HELM_MANOEUVRES) == 12
    w, crew, runner = trader_at(BRIG, 2, Watch.LARBOARD)
    furl = asked(w, "furl_square", "fore.topsail", "in_the_gear")
    assert runner._aloft(furl) and runner._working_posts(crew, furl) == []
    heave = asked(w, "heave_to", None)
    assert runner._working_posts(crew, heave) == []
    runner.instances.remove(heave)
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert [s.post for s in runner._working_posts(crew, jib)] == ["master"]
    crew.all_hands_called = True
    assert runner._working_posts(crew, jib) == []
    crew.all_hands_called = False
    master = w.people.find("the master")
    master.where = "below"
    assert runner._working_posts(crew, jib) == []
    master.where = "quarterdeck"
    assert "master" in taken(w, jib)
    runner._to_the_conn(crew)  # as `Runner._begin` calls it for every manoeuvre begun
    assert next(s for s in crew.sailors if s.post == "master").at is None
    assert jib.assignment is not None and "master" not in [s.post for s in jib.assignment.hands]
    assert jib.assignment.outcome == hands.SHORT and not jib.paused


def test_a_post_is_counted_where_the_watch_is_small_on_board_and_not_where_it_is_away_working():
    """Ruling 11's whole number reads the hands on board: a hand away in the boat (held by work
    whose crew is out of the ship, `Script.crew_away`: the boat from her pull out to her pull back)
    is not on board, and one hoisting her out is. The merchant brig's starboard watch by night,
    the boat holding three of its seven: hoisting out, the whole is seven and the jib is the six's
    without the mate; pulling for the shore, the whole is four, under six, and the mate is
    counted."""
    w, crew, runner = trader_at(BRIG, 2, Watch.STARBOARD)
    boat = asked(w, "send_boat", None)
    boat.script.phase = "hoist_out"
    for s in [s for s in crew.sailors if s.watch is Watch.STARBOARD and not s.post][:3]:
        s.at = boat.inst_id
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert runner._watch_whole(crew, Watch.STARBOARD) == 7
    assert runner._working_posts(crew, jib) == []
    boat.script.phase = "pull_out"
    assert boat.script.crew_away and runner._watch_whole(crew, Watch.STARBOARD) == 4
    assert [s.post for s in runner._working_posts(crew, jib)] == ["mate"]


def test_the_schooners_whole_watches_are_over_every_want_of_her_watchs_deck_work():
    """Ruling 11's condition (a), at its root: the topsail schooner's watches are seventeen and
    sixteen hands as mustered at seed 7, each over the want of every request that is a watch's work
    on deck by her files, so that her master and mate are never counted for it, by night or by day
    (old: ruling 9's wider form took her mate where work at once used up her watch, and moved her
    passages). The armed schooner has no people file, and her posts head no watch."""
    from freesail.world import people as PE

    cases = [
        ("set_square", "fore.topsail", "in_the_gear"),
        ("take_in_square", "fore.topsail", "set"),
        ("set_gaff", "main.sail", "furled"),
        ("take_in_gaff", "main.sail", "set"),
        ("set_jibheaded", "jib", "furled"),
        ("take_in_jibheaded", "jib", "set"),
        ("set_studding", "fore.topmast.studdingsail.starboard", "furled"),
        ("brace", None, None),
        ("send_boat", None, None),
    ]
    for watch in (Watch.STARBOARD, Watch.LARBOARD):
        for hour in (2, 12):
            w, crew, runner = trader_at(SCHOONER, hour, watch)
            whole = runner._watch_whole(crew, watch)
            assert whole == (17 if watch is Watch.STARBOARD else 16)
            for eid, sid, state in cases:
                inst = asked(w, eid, sid, state)
                assert inst.want.hands <= whole and runner._working_posts(crew, inst) == [], eid
    assert PE.post_watches("data/ships/privateer-schooner.yaml") == {}


def test_a_posts_watch_is_read_from_the_people_file_in_words_and_a_save_from_before_has_none(
    tmp_path,
):
    """Ruling 11's data: the watch a post heads is its people file's (`watch:` on the post's
    wardroom entry, "starboard" or "larboard"), read at the muster into `Crew.post_watches`
    (`world.people.post_watches`, `api.session.attach_crew`), and set on that crew alone, so that
    every other crew is mustered and pickled as before: the four traders' files give the master
    the larboard and the mate the starboard (JUDGEMENT), every King's ship none. Anything else is
    refused in words, as is a watch on a role that is no post. A crew from a checkpoint written
    before it holds no watch for its posts to head, so a save from before loads with the company
    it holds and no post hauls."""
    import pickle

    from freesail.world import people as PE

    heads = {"master": "larboard", "mate": "starboard"}
    for stem in ("merchant-brig", "smack", "topsail-schooner"):
        assert PE.post_watches(f"data/ships/{stem}.yaml") == heads, stem
    for stem in ("frigate-36", "seventy-four", "cutter", "brig", "privateer-schooner"):
        assert PE.post_watches(f"data/ships/{stem}.yaml") == {}, stem
    king = make_world(SEED, FRIGATE, Scenario()).ship.extra["crew"]
    assert not hasattr(king, "post_watches")
    bad = tmp_path / "bad.yaml"
    bad.write_text(
        "wardroom:\n  - role: master\n    post: true\n    watch: port\n", encoding="utf-8"
    )
    with pytest.raises(ValueError, match="the master heads the 'port' watch; say starboard or"):
        PE._post_watches(str(bad))
    boy = tmp_path / "boy.yaml"
    boy.write_text("wardroom:\n  - role: boy\n    watch: larboard\n", encoding="utf-8")
    with pytest.raises(ValueError, match="only a post heads a watch"):
        PE._post_watches(str(boy))
    w, crew, runner = trader_at(BRIG, 2, Watch.LARBOARD)
    again = pickle.loads(pickle.dumps(crew))
    assert again.post_watches == heads
    del crew.post_watches  # as a checkpoint from before holds its crew
    jib = asked(w, "set_jibheaded", "jib", "in_the_gear")
    assert hands.post_watch(crew, next(s for s in crew.sailors if s.post == "master")) is None
    assert runner._working_posts(crew, jib) == []
