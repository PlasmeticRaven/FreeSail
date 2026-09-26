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

from typing import Any

import pytest

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import bill, hands
from freesail.crew.hands import CrewRequest, CrewRequestError, crew_factor, release, request
from freesail.crew.model import Crew, Rating, Sailor, Station, Watch
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
        assert want.all_hands or want.hands > 0, eid


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
    assert factor_for(ORD, ORD, fatigue=0.3) == pytest.approx(1.15)
    assert factor_for(ORD, ORD, fatigue=1.0) == pytest.approx(1.0 + hands.FATIGUE_WEIGHT)
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
    assert crew_factor(got, want, aloft=False) == pytest.approx(1.15)
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


def test_tack_ship_belays_the_studdingsails_and_they_resume_after():
    w = close_hauled_frigate()
    crew = w.ship.extra["crew"]
    routine = FakeRoutine(crew)
    w.ship.extra["routine"] = routine
    runner = runner_of(w)
    stun = "fore.topmast.studdingsail.starboard"
    w.submit("set the starboard fore topmast studdingsail")
    w.run(60)
    before = runner.in_progress()[0]
    assert before["hands"] == 8 and before["step"] == "bend_on"
    n0 = len(w.log)
    w.submit("tack ship")
    assert routine.calls == [("call_all_hands", "to tack ship")]
    snap = {s["id"]: s for s in runner.in_progress()}
    assert snap["set_studding"]["paused"] is True and snap["set_studding"]["step"] == "paused"
    assert snap["set_studding"]["hands"] == 0
    held = runner.instances[0].progress
    w.tick()
    belay = [e for e in log_after(w, n0) if e.kind == "evolution.belayed"]
    assert [e.text for e in belay] == [
        "Belayed setting the starboard fore topmast studdingsail: all hands about ship."
    ]
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
    "set_studding": (["set the fore topsail"], "set the starboard fore topmast studdingsail"),
    "take_in_studding": (
        ["set the fore topsail", "set the starboard fore topmast studdingsail"],
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
    kinds = [e.kind for e in log_after(w, n0) if e.kind != "clock.bell"]
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
