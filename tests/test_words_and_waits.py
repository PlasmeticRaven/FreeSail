"""Words and waits on today's ships: the truths 7-780 to 7-786.

Each is a fault in what the log said, or failed to say, on a ship already in the game, found in
passing while the ships' files were proved unmoved (docs/dev/CarriedForward-M7.md, section 4),
reproduced here by the orders a player gives on a committed ship and pinned as the log now says
it. The log is the game: a line untrue, or a wait unsaid, was a fault of the game.

- 7-780: work queued behind other work says so in the log, at the order, once: a sail's order
  (the brig's `furl the main topsail` behind `take in the main topsail`) and a whole-ship order
  (`heave to` behind `wear ship`); an order's own line does not say it again.
- 7-781: "Filled away" is said of a ship with headway: the lugger braced full from lying to with
  sternway on her is told so and told when she gathers way; the cutter filled away after `lie
  a-try` who then loses her way and goes astern is told so then.
- 7-782 and 7-783: the dire strain warning of a part is said though a lesser one of the same part
  was within the ten minutes, and once in them (`physics.strain.warning_due`): the frigate's jib
  in a rising gale, and the one rule for a cable's warning.
- 7-784: the smack's cast names no topsail of hers, which stays furled, and sends no hand aloft.
- 7-785: a `set the topsail` the watch on deck is too few for says so, and what it waits for.
- 7-786: `clear for action` says the boats are where they are: on the booms.
- 7-787: a take-in or a furl countermands the setting of its sail in hand or waiting: the brig
  in 40 knots, `take in all sail` given while `set plain sail` is going up, is left with nothing
  of it set. This changes what she does, and is meant to.
"""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from freesail import units
from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.evolutions import action_scripts
from freesail.physics import strain

BRIG = "data/ships/brig.yaml"
CUTTER = "data/ships/cutter.yaml"
LUGGER = "data/ships/lugger.yaml"
SMACK = "data/ships/smack.yaml"
FRIGATE = "data/ships/frigate-36.yaml"


def _make(ship: str, heading: float = 90.0, knots: float = 15.0, speed: float = 4.0, **kw):
    scenario = Scenario(
        wind_from_deg=0.0,
        wind_speed_kn=knots,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=speed,
        **kw,
    )
    return make_world(7, ship, scenario)


def _lines(world, after: int, kinds: tuple[str, ...] | None = None) -> list[tuple[str, str]]:
    return [
        (e.kind, e.text) for e in world.log if e.tick > after and (kinds is None or e.kind in kinds)
    ]


# ---------------------------------------------------------------------------
# 7-780: the wait behind other work, said in the log
# ---------------------------------------------------------------------------


def test_truth_7_780_a_sails_order_queued_behind_other_work_says_so_in_the_log_once():
    """The brig under plain sail: `take in the main topsail`, then `furl the main topsail` at
    once. The furl waits its turn behind the take-in. Before, the reply was "Order: furl the main
    topsail." and no line of the log said it waited, nor what for; now the log says it at the
    order, once, and the furl's own line says when it begins."""
    w = _make(BRIG)
    w.submit("set plain sail")
    w.run(600)
    t0 = w.clock.tick
    w.submit("take in the main topsail")
    assert w.submit("furl the main topsail").text == "Order: furl the main topsail."
    w.run(400)
    waits = (
        "'Furl the main topsail' will follow 'take in the main topsail', which the hands are "
        "still at."
    )
    lines = _lines(w, t0 - 1)
    assert [x for x in lines if x[1] == waits] == [("evolution.waiting", waits)]
    # a wait for its turn is routine: it eases no compressed passage and wakes no seat
    (said,) = [e for e in w.log if e.text == waits]
    assert said.severity.value == "routine"
    begun = lines.index(("evolution.started", "Lay aloft and furl the main topsail."))
    assert begun > lines.index(("evolution.waiting", waits))


def test_truth_7_780_a_whole_ship_order_queued_behind_a_manoeuvre_says_so_in_the_log():
    """The brig: `wear ship`, then `heave to` while she wears. The heave-to waits for the wear.
    Before, nothing at all was said of it until it began; now the log says it waits, once."""
    w = _make(BRIG, heading=60.0)
    w.submit("set plain sail")
    w.run(700)
    t0 = w.clock.tick
    assert w.submit("wear ship").kind == "order.accepted"
    assert w.submit("heave to").kind == "order.accepted"
    w.run(2)
    waits = [x for x in _lines(w, t0 - 1, ("evolution.waiting",)) if "will follow" in x[1]]
    assert waits == [
        ("evolution.waiting", "'Heave to' will follow 'wear ship', which the hands are still at.")
    ]


def test_truth_7_780_an_orders_own_line_does_not_say_the_wait_again():
    """`shorten sail` 30 s into `set plain sail` on the brig: the reefs wait behind the topsails
    being set, and some of its lines are not done. Its own line is written (it says what was
    not done) and says no wait: each is said once, by the runner, in a line of its own."""
    w = _make(BRIG)
    w.submit("set plain sail")
    w.run(30)
    t0 = w.clock.tick
    e = w.submit("shorten sail")
    assert e.kind == "evolution.started" and "Not done" in e.text
    assert "will follow" not in e.text
    w.run(1)
    waits = [x[1] for x in _lines(w, t0 - 1, ("evolution.waiting",)) if "will follow" in x[1]]
    assert sorted(waits) == [
        "'Reef the fore topsail' will follow 'set the fore topsail', which the hands are still at.",
        "'Reef the main topsail' will follow 'set the main topsail', which the hands are still at.",
    ]


# ---------------------------------------------------------------------------
# 7-781: "Filled away" of a ship with way on her
# ---------------------------------------------------------------------------


def _filled(ship: str, pre: list[str], lie: str, heading: float, run_s: int = 900):
    w = _make(ship, heading=heading, knots=15.0)
    for o in pre:
        w.submit(o)
        w.run(600)
    w.submit(lie)
    w.run(900)
    t0 = w.clock.tick
    assert w.submit("fill away").kind == "order.accepted"
    w.run(run_s)
    return w, _lines(w, t0, ("ship.filled_away", "ship.way"))


def test_truth_7_781_braced_full_with_sternway_on_her_she_is_told_so_and_when_she_has_way():
    """The lugger hove to in 15 knots and filled away: her sheets drawn a second after the
    order, with a knot and a half of sternway on her. Before, "Filled away on the larboard
    tack; steering ENE (68°)." was said then; now that she has no headway yet, and once, when
    she has it, that she gathers headway."""
    w, lines = _filled(LUGGER, ["set plain sail"], "heave to", 60.0, 300)
    assert lines == [
        (
            "ship.filled_away",
            "Her sheets drawn on the larboard tack; steering ENE (68°); she has no headway on "
            "her yet.",
        ),
        ("ship.way", "She gathers headway; filled away on the larboard tack."),
    ]
    assert units.ms_to_knots(w.ship.dyn.u) > 1.0


def test_truth_7_781_filled_away_she_loses_her_way_and_goes_astern_and_is_told_so():
    """The cutter after `lie a-try` in 15 knots, the wind four points on her bow, and `fill
    away`: filled away with two knots of way, she loses it and goes astern at a knot and more
    for the hour. Before, "Filled away ..." was the last word of it; now a line says it when she
    has sternway, once. (That she goes astern is what she does, and is not mended here.)"""
    w, lines = _filled(CUTTER, ["set plain sail", "set the topsail"], "lie a-try", 60.0)
    assert lines[0] == (
        "ship.filled_away",
        "Filled away on the larboard tack; braced full and steering ENE (68°).",
    )
    (lost,) = lines[1:]
    assert lost[0] == "ship.way"
    assert lost[1].startswith("Filled away, she has lost her way and makes a knot of sternway")
    assert units.ms_to_knots(w.ship.dyn.u) < -0.5


# ---------------------------------------------------------------------------
# 7-782 and 7-783: the dire warning said whatever lesser one was before it
# ---------------------------------------------------------------------------


def test_truth_7_782_a_parts_dire_warning_is_not_held_back_by_a_lesser_one():
    """The frigate under plain sail in 18 knots, the wind rising to 40 over ten minutes: her jib
    strains at its bolt-ropes (at 1641 s and 2241 s, ten minutes apart, as before) and is loaded
    past where it may carry away at 2706 s. Before, its next line came at 2841 s, when the ten
    minutes from the lesser one were out; now the dire line comes on the next tick, once in its
    ten minutes, and the lesser lines keep their own count. No load moves: the jib's first dire
    tick is the same."""
    w = _make(FRIGATE, heading=90.0, knots=18.0)
    w.submit("set plain sail")
    w.submit("brace the yards up on the larboard tack")
    w.run(900)
    w.submit("set plain sail")
    w.run(300)
    t0 = w.clock.tick
    first_dire = None
    for t in range(1800):
        k = 18.0 + 22.0 * min(1.0, t / 600)
        w.wind.base_speed = w.wind.speed = units.knots_to_ms(k)
        w.tick()
        if first_dire is None and w.ship.sails["jib"].strain_ratio > strain.CARRY_AWAY_RATIO:
            first_dire = w.clock.tick
    jib = [
        (e.tick, e.text)
        for e in w.log
        if e.tick > t0 and e.kind == "strain.warning" and e.subject == "jib"
    ]
    assert first_dire == 2706
    assert jib == [
        (1641, "Jib straining at the bolt-ropes."),
        (2241, "Jib straining at the bolt-ropes."),
        (2707, "Jib stretched drum-tight; it will not stand much more."),
    ]


def test_truth_7_783_one_rule_counts_every_parts_warning_and_a_cables():
    """`warning_due`, read by the parts' warnings and the cable's (`physics.anchor`): a lesser
    warning once in ten minutes; a dire one after a lesser within them said, and itself once in
    ten minutes; the lesser count kept from the lesser line."""
    st = strain.StrainState()
    due = []
    for t, dire in [(0, False), (60, False), (100, True), (200, True), (600, False), (650, True)]:
        st.elapsed_s = float(t)
        due.append((t, strain.warning_due(st, "cable:best_bower", dire)))
    assert due == [(0, True), (60, False), (100, True), (200, False), (600, True), (650, False)]
    st.elapsed_s = 700.0
    assert strain.warning_due(st, "cable:best_bower", True)  # ten minutes from the dire one


def test_truth_7_783_a_part_held_over_its_dire_line_an_hour_says_so_once_in_ten_minutes():
    """The frigate's jib stay loaded to 1.55 of its rating every second for an hour (no chance
    drawn, so it stands): its dire warning six times, once in each ten minutes, and not every
    tick."""
    from freesail.api.session import make_ship

    ship = make_ship(FRIGATE)
    stay = ship.lines["jib.stay"]
    said = []
    for t in range(3600):
        stay.load_kn = 1.55 * stay.rating_kn
        strain.apply_strain(ship, 1.0, None)
        said += [(t, n[2]) for n in ship.drain_notes() if n[1] == "strain.warning"]
    dire = "Jib stay stranding; it will not hold much longer."
    assert said == [(t, dire) for t in (0, 600, 1200, 1800, 2400, 3000)]


# ---------------------------------------------------------------------------
# 7-784: the smack's cast
# ---------------------------------------------------------------------------


def _cast(ship: str) -> list[str]:
    w = make_world(
        7,
        ship,
        Scenario(
            start_time=datetime(1805, 6, 10, 10, 0),
            wind_from_deg=225.0,
            wind_speed_kn=12.0,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=225.0,
            ship_speed_kn=0.0,
            position={"lat_deg": 50.133, "lon_deg": -5.035},
            region="channel-west",
        ),
    )
    w.submit("let go the best bower")
    w.run(1200)
    t0 = w.clock.tick
    assert w.submit("get under way").kind == "order.accepted"
    w.run(1200)
    return [x for _, x in _lines(w, t0, ("evolution.started", "evolution.step"))], w


def test_truth_7_784_the_smacks_cast_names_no_topsail_and_sends_no_hand_aloft():
    """The smack at anchor in Carrick Road, `get under way`: her plain sail is her mainsail and
    her jib, and her topsail stays furled. Before, her cast said "send the ready-men aloft",
    "Lay aloft, sail-loosers! Man the topsail sheets and halliards." and "Hoist away the topsail
    and the mainsail"; now it names what she makes, on deck. The cutter's, whose topsail is of her
    plain sail, is as it was."""
    smack, w = _cast(SMACK)
    assert w.ship.sails["topsail"].state.name == "FURLED"
    assert not any("topsail" in x or "aloft" in x.replace("no hand aloft", "") for x in smack)
    assert smack[0] == (
        "All hands up anchor! Pass the messenger, ship the bars; the sails to be got ready for "
        "hoisting on deck, no hand aloft."
    )
    assert (
        "Pawl the capstan; stopper the cable. Stations for making sail! Cast off the gaskets of "
        "the mainsail; the halliards manned on deck."
    ) in smack
    assert (
        "Hoist away the mainsail, the main boom steadied over to larboard. Man the bars; heave "
        "round!"
    ) in smack
    cutter, _ = _cast(CUTTER)
    assert cutter[0].startswith("All hands up anchor! Pass the messenger, ship the bars; send the")
    assert (
        "Pawl the capstan; stopper the cable. Stations for loosing sail! Lay aloft, "
        "sail-loosers! Man the topsail sheets and halliards."
    ) in cutter
    assert any(
        x.startswith("Let fall! Sheet home! Hoist away the topsail and the mainsail")
        for x in cutter
    )


# ---------------------------------------------------------------------------
# 7-785: the wait for hands that other work is not the cause of
# ---------------------------------------------------------------------------


def test_truth_7_785_a_set_the_watch_is_too_few_for_says_what_it_waits_for():
    """The smack at 09:05, her larboard watch of two on deck: `set plain sail`, and two minutes
    on `set the topsail`. Two hands are too few for it however idle (it wants five, and begins
    with half). Before, the line named the mainsail being set as the reason, and when the jib
    was set the wait went on unsaid until the watch was relieved at noon; now the line says the
    watch is too few and what it waits for, and it is taken up at the relief, as before."""
    w = _make(SMACK, heading=292.5, speed=5.0, start_time=datetime(1805, 6, 1, 9, 5))
    w.submit("set plain sail")
    w.run(120)
    t0 = w.clock.tick
    w.submit("set the topsail")
    w.run(700)
    assert _lines(w, t0, ("evolution.waiting",)) == [
        (
            "evolution.waiting",
            "Not hands enough on deck to set the topsail; the watch on deck has but two hands "
            "for it, and it waits for the watch to be relieved or all hands called.",
        )
    ]
    assert w.ship.sails["topsail"].state.name == "FURLED"  # the plain sail set, it waits on
    # all hands called by the player: it is taken up at once, and said
    called = w.clock.tick
    w.submit("all hands")
    w.run(2)
    assert ("evolution.started", "Hands aloft to loose the topsail.") in _lines(w, called)


# ---------------------------------------------------------------------------
# 7-786: the boats as the ship is cleared for action
# ---------------------------------------------------------------------------


def test_truth_7_786_clear_for_action_says_the_boats_are_on_the_booms():
    """The brig, `clear for action`: her launch, cutter and jolly boat stay griped on the booms
    (where a shot may stave them). Before, "The boats are out and towing astern; the ship is
    clear."; now the line says where they are. A boat her file tows is said to be towing astern,
    and a ship with no boat is clear."""
    w = _make(BRIG)
    w.submit("clear for action")
    w.run(700)
    steps = [x for _, x in _lines(w, 0, ("evolution.step",))]
    assert "The boats griped fast on the booms; the ship is clear." in steps
    assert not any("towing astern" in x for x in steps)

    def ship(*boats):
        return SimpleNamespace(spec=SimpleNamespace(boats=list(boats)))

    def boat(name, towed=False):
        return SimpleNamespace(name=name, towed=towed)

    words = action_scripts._boats_cleared_words
    assert words(ship(boat("the boat"))) == "The boat griped fast on the booms; the ship is clear."
    assert (
        words(ship(boat("the boat", towed=True)))
        == "The boat towing astern on her painter; the ship is clear."
    )
    assert words(ship()) == "The ship is clear."


# ---------------------------------------------------------------------------
# 7-787: the take-in countermands the set
# ---------------------------------------------------------------------------


def _all_sail_in(gap: int):
    w = _make(BRIG, heading=60.0, knots=40.0)
    w.submit("set plain sail")
    w.run(gap)
    t0 = w.clock.tick
    reply = w.submit("take in all sail")
    w.run(1500)
    standing = sorted(k for k, v in w.ship.sails.items() if v.state.name in ("SET", "LOOSED"))
    set_after = [e.text for e in w.log if e.kind == "sail.set" and e.tick > t0]
    return reply, _lines(w, t0 - 1) + [("set after", x) for x in set_after], standing


def test_truth_7_787_take_in_all_sail_belays_the_plain_sail_going_up():
    """The brig in 40 knots, `set plain sail`, and `take in all sail` 300 s on. Before, the main
    topsail, the fore and main topgallants and the spanker were set after it (at 635 s to
    1013 s) and stood in the gale; now the setting of each is belayed, said once, the fore
    topsail being loosed is taken in from where it hung, and nothing of it is set at the end."""
    reply, lines, standing = _all_sail_in(300)
    assert reply.kind == "evolution.started"
    belays = [x for x in lines if x[0] == "work.belayed"]
    assert len(belays) == 1
    for sail in ("main topsail", "fore topgallant", "main topgallant", "spanker", "fore topsail"):
        assert f"setting the {sail}" in belays[0][1]
    assert not [x for x in lines if x[0] == "set after"]  # nothing set after the order
    assert ("sail.taken_in", "Took in the fore topsail; hanging in the gear.") in lines
    assert standing == []


def test_truth_7_787_given_as_the_plain_sail_begins_the_belay_is_the_orders_line():
    """The same, `take in all sail` 30 s after `set plain sail`, every sail still furled.
    Before, the order was refused, "Nothing done: ... already furled", and every sail was then
    set in the gale; now the order is the belay of the setting, its reply and its line."""
    reply, lines, standing = _all_sail_in(30)
    assert reply.kind == "work.belayed" and reply.text.startswith("Belayed setting the foresail")
    assert [x for x in lines if x[0] == "work.belayed"] == [("work.belayed", reply.text)]
    assert not [x for x in lines if x[0] in ("sail.set", "set after")]
    assert standing == []
