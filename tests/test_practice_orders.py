"""Practice at the great guns: the orders (practice and resupply, between packages 72 and
73; docs/design/Build-PracticeAndResupply.md §3.3, §6, §8.1).

Every form of `heave a cask overboard`, `engage the cask` and the notional mark, `exercise
the guns`, `cease exercising`, `fill cartridges` and `cease filling` in `execute` and in
`check`, and every refusal in its words; "the mark" meaning the cask only while one is in
the water; `secure the guns` ending the exercise and giving up a mark; the heave holding
nothing of the ship's (a wear goes on beside it); `heave_mark.yaml` in the catalogue; the
scenario's round trip and load; and a rules captain in the scenario with a cask engaged
for half an hour.

Written before Builder 1's battery was merged, these tests stand a fake in for
`begin_exercise` where the loaded guns' words are wanted, and build the magazine at layout 2
themselves; they hold with the battery merged. A gun fired by name in dumb show from empty
firing (run in the world), and the `fill cartridges` answer's words for powder too little
to fill and for the one gun of a kind, are the review's findings.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

import pytest
import yaml

from freesail import orders, units
from freesail.api import readings  # noqa: F401 - first: it imports the rows' modules
from freesail.api.action_readings import _guns, idle_rows
from freesail.api.session import make_world
from freesail.combat import action, marks
from freesail.combat.guns import Battery, FireMode, battery_of
from freesail.core.world import Scenario
from freesail.orders import gunnery
from freesail.orders.errors import OrderError
from freesail.ship.graph import Ship
from freesail.ship.loader import load_spec
from freesail.ship.parts import Magazine
from freesail.world.geo import destination
from tests.test_brains import world_at

ROOT = Path(__file__).resolve().parents[1]
FRIGATE = "data/ships/frigate-36.yaml"
CUTTER = "data/ships/cutter.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"
SCENARIO = ROOT / "data" / "scenarios" / "exercising-the-great-guns.yaml"
NOTIONAL = "engage a mark four cables on the starboard beam"


def frigate(**kw):
    w = world_at(49.5, -5.5, FRIGATE, **kw)
    w.run(60)
    return w


def at_quarters(w, cast_loose=True):
    w.submit("beat to quarters")
    w.run(5)
    if cast_loose:
        w.submit("cast loose the guns")
        w.run(200)
    return battery_of(w.ship)


def say(w, text):
    """The order carried out at once: (kind, text, data); raises OrderError in words."""
    return orders.handle(w.ship, text)


def refused(w, text) -> str:
    with pytest.raises(OrderError) as e:
        orders.handle(w.ship, text)
    return str(e.value)


def kinds(w, kind):
    return [e for e in w.log if e.kind == kind]


def heave_and_see(w, side="starboard"):
    """The cask over the side by the order, the minute's work done and the lookout's look:
    the cask in the water and in sight."""
    kind, text, data = say(w, f"heave a cask overboard from the {side} quarter")
    assert kind == "evolution.started" and data["side"] == side
    w.run(150)
    cask = marks.cask_in_water(w.ship)
    assert cask is not None and marks.cask_in_sight(w, cask)
    return cask


# -- the heave ------------------------------------------------------------------------------


def test_the_heave_goes_out_of_quarters_from_the_quarter_named_or_the_lee():
    w = frigate()
    kind, text, data = say(w, "heave a cask overboard from the starboard quarter")
    assert kind == "evolution.started"
    assert text == "Hands to the quarter: an empty cask over the side for a mark."
    assert data == {"verb": "heave a cask overboard", "level": 1, "side": "starboard"}
    assert marks.cask_in_water(w.ship) is None  # a minute's work
    w.run(90)
    over = kinds(w, "practice.mark_over")
    assert len(over) == 1 and str(over[0].severity) == "notable"
    assert over[0].text == (
        "The mark is over the side from the starboard quarter, an empty cask with a flag on a "
        "staff."
    )
    assert marks.cask_in_water(w.ship) is not None
    # no side named: the lee quarter by her heel
    lee = "starboard" if float(w.ship.dyn.heel) > 0.0 else "larboard"
    assert say(w, "heave a cask overboard")[2]["side"] == lee
    assert say(w, "drop a cask for a mark")[2]["side"] == lee
    assert say(w, "heave a cask overboard from the lee quarter")[2]["side"] == lee
    weather = "larboard" if lee == "starboard" else "starboard"
    assert say(w, "put a cask over the side to windward")[2]["side"] == weather
    assert say(w, "heave a mark overboard from the port quarter")[2]["side"] == "larboard"
    assert refused(w, "heave a cask overboard from the bowsprit").startswith(
        "Heave it over from which quarter?"
    )


def test_a_fresh_heave_gives_up_the_cask_in_the_water():
    w = frigate()
    first = heave_and_see(w)
    battery = battery_of(w.ship)
    battery.target = first.id
    say(w, "heave a cask overboard from the larboard quarter")
    given_up = kinds(w, "practice.mark_lost")
    assert [e.data["gone"] for e in given_up] == ["abandoned"]
    assert first.gone == "abandoned" and battery.target is None
    w.run(90)
    second = marks.cask_in_water(w.ship)
    assert second is not None and second.id == "practice:cask-2"
    assert len(kinds(w, "practice.mark_lost")) == 1


def test_the_heave_is_refused_with_no_chart_and_by_night():
    alone = Ship(load_spec(FRIGATE))
    with pytest.raises(OrderError) as e:
        orders.handle(alone, "heave a cask overboard")
    assert str(e.value) == (
        "The ship sails alone, with no chart: a cask over the side could not be seen. Say "
        "'engage a mark four cables on the starboard beam'."
    )
    plane = make_world(7, FRIGATE, Scenario(start_time=datetime(1805, 6, 12, 10, 0)))
    assert plane.lookout is None
    assert refused(plane, "heave a cask overboard").startswith("The ship sails alone")
    night = _world_at_night()
    assert night.daylight == "night"
    assert refused(night, "heave a cask overboard") == (
        "It is dark: a cask over the side would not be seen from the masthead; a notional "
        "mark serves by night ('engage a mark four cables on the starboard beam')."
    )
    # the notional mark serves by night, and the range is the one laid
    at_quarters(night)
    kind, text, _ = say(night, NOTIONAL)
    assert kind == "guns.engage" and text.startswith("Engage the mark four cables")
    night.run(1)
    assert night.readings.value("range")["metres"] == pytest.approx(4 * units.CABLE)
    assert night.readings.words("range") == "4 cables"


def _world_at_night():
    sc = Scenario(
        start_time=datetime(1805, 6, 12, 2, 0),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
    )
    w = make_world(7, FRIGATE, sc)
    w.run(60)
    return w


def test_the_heave_holds_nothing_and_a_wear_goes_on_beside_it():
    w = frigate(ship_heading_deg=330.0, ship_speed_kn=6.0)
    w.submit("set plain sail")
    w.run(300)
    say(w, "heave a cask overboard")
    runner = w.ship.extra["evolutions"]
    heave = next(i for i in runner.instances if i.evo.id == "heave_mark")
    assert heave.holds == set()
    answer = w.submit("wear ship")
    assert "will follow" not in answer.text, answer.text
    wear = next(i for i in runner.instances if i.evo.id == "wear")
    assert not wear.waiting and not heave.waiting and not heave.paused
    w.run(90)
    assert kinds(w, "practice.mark_over")
    assert any(i.evo.id == "wear" for i in runner.instances)  # the wear still in hand


# -- engaging a mark ------------------------------------------------------------------------


def test_engage_the_cask_and_its_refusals():
    w = frigate()
    battery = at_quarters(w)
    assert refused(w, "engage the cask to starboard") == (
        "There is no cask in the water: say 'heave a cask overboard' first, or 'engage a "
        "mark four cables on the starboard beam'."
    )
    cask = heave_and_see(w)
    # out of the masthead's sight (beyond the mile by day), no gun is laid for it
    here = w.position
    cask.position = destination(here, 90.0, 1.5 * units.NAUTICAL_MILE)
    w.run(60)
    assert not marks.cask_in_sight(w, cask)
    assert (
        refused(w, "engage the cask to starboard") == "The mark is not in sight from the masthead."
    )
    cask.position = destination(w.position, 90.0, 0.2 * units.NAUTICAL_MILE)
    w.run(60)
    assert marks.cask_in_sight(w, cask)
    assert refused(w, "engage the cask") == (
        "Engage the cask to which side? Say 'engage the cask to starboard' or 'to larboard', "
        "or 'on both sides'."
    )
    kind, text, data = say(w, "engage the cask to starboard")
    assert kind == "guns.engage"
    assert (
        text
        == "Engage the cask to starboard: the starboard battery, the guns to fire as they bear."
    )
    assert data["target"] == cask.id and data["mark"] == "cask" and data["side"] == "starboard"
    assert battery.target == cask.id and battery.mode is FireMode.AS_THEY_BEAR
    assert say(w, "engage the cask to starboard")[1] == (
        "She is engaging the cask to starboard already."
    )
    # the mark and the target mean the cask while it is in the water
    assert say(w, "engage the mark to larboard")[2]["target"] == cask.id
    assert say(w, "engage the target on both sides")[1].startswith("Engage the cask on both sides:")
    # knocked to staves: the cask's words refused, the mark's are a sail's again
    cask.gone = "struck"
    assert refused(w, "engage the cask to starboard") == (
        "The mark is knocked to pieces: heave another cask overboard for a mark."
    )
    assert refused(w, "engage the mark to starboard") == "There is no sail in sight to engage."


def test_the_mark_means_the_cask_only_while_one_is_in_the_water():
    w = frigate()
    at_quarters(w)
    assert not gunnery._names_the_cask(w.ship, "the mark")
    assert gunnery._names_the_cask(w.ship, "the cask")
    assert refused(w, "engage the mark to starboard") == "There is no sail in sight to engage."
    cask = heave_and_see(w)
    for words in ("the mark", "the target", "mark", "the cask"):
        assert gunnery._names_the_cask(w.ship, words), words
    assert not gunnery._names_the_cask(w.ship, "her")
    assert not gunnery._names_the_cask(w.ship, "the brig")
    cask.gone = "lost"
    assert not gunnery._names_the_cask(w.ship, "the mark")


@pytest.mark.parametrize(
    "ship,words,relative,cables,side",
    [
        (FRIGATE, "engage a mark four cables on the starboard beam", 90.0, 4.0, "starboard"),
        (FRIGATE, "engage a mark 2 cables off the port beam", -90.0, 2.0, "larboard"),
        (
            FRIGATE,
            "engage the notional mark three cables broad on the larboard beam",
            -90.0,
            3.0,
            "larboard",
        ),
        (
            FRIGATE,
            "engage the mark two and a half cables on the starboard beam",
            90.0,
            2.5,
            "starboard",
        ),
        # the bow and the quarter where a gun bears: the privateer's swivels on the bow, her
        # pivot gun on the quarter (no gun of the frigate's bears on either)
        (PRIVATEER, "engage a mark one cable on the starboard bow", 45.0, 1.0, "starboard"),
        (
            PRIVATEER,
            "engage the notional mark one cable broad on the larboard bow",
            -45.0,
            1.0,
            "larboard",
        ),
        (PRIVATEER, "engage a mark 3 cables off the port quarter", -135.0, 3.0, "larboard"),
        (
            PRIVATEER,
            "engage the mark two and a half cables on the starboard quarter",
            135.0,
            2.5,
            "starboard",
        ),
    ],
)
def test_a_notional_mark_by_its_bearing_and_range(ship, words, relative, cables, side):
    w = world_at(49.5, -5.5, ship)
    w.run(60)
    battery = at_quarters(w)
    kind, text, data = say(w, words)
    assert kind == "guns.engage" and data["target"] == marks.NOTIONAL_ID
    assert data["mark"] == "notional" and data["side"] == side
    p = marks.practice_of(w.ship)
    assert p.notional[0] == relative and p.notional[1] == pytest.approx(cables * units.CABLE)
    assert battery.target == marks.NOTIONAL_ID and battery.engaged == side
    assert battery.target_words == p.notional[2]
    assert text.startswith(
        f"Engage {p.notional[2]}: the {side} battery, the guns to fire as they bear"
    )
    if ship == FRIGATE:
        assert text.endswith("as they bear.")
    # read before the side's words in `check` too
    assert orders.read_whole(w.ship, words).verb == "engage"


def test_a_notional_mark_where_no_gun_bears_is_refused():
    """The mark keeps its bearing from her head as she turns, so a mark on the bow or the
    quarter of the frigate, where neither her broadside (thirty-five degrees about the beam)
    nor her chasers bear, would never be fired at (the review's finding)."""
    w = frigate()
    at_quarters(w)
    for point in ("bow", "quarter"):
        for side in ("starboard", "larboard"):
            assert refused(w, f"engage a mark three cables on the {side} {point}") == (
                f"No gun of hers bears on the {side} {point}, and a notional mark keeps its "
                f"bearing from her head as she turns: say 'engage a mark three cables on the "
                f"{side} beam'."
            )
    # a range beyond her reach is not suggested again
    assert refused(w, "engage a mark twelve cables on the starboard quarter").endswith(
        "say 'engage a mark four cables on the starboard beam'."
    )
    with pytest.raises(OrderError) as e:
        orders.read_whole(w.ship, "engage a mark three cables on the starboard bow")
    assert "No gun of hers bears on the starboard bow" in str(e.value)
    assert battery_of(w.ship).target is None
    # the privateer's bow is the swivels' alone, and they throw two cables
    p = world_at(49.5, -5.5, PRIVATEER)
    p.run(60)
    at_quarters(p)
    assert refused(p, "engage a mark three cables on the larboard bow") == (
        "No gun of hers that bears on the larboard bow carries three cables: her half-pounder "
        "swivels' random shot is 2.0 cables."
    )
    assert say(p, "engage a mark 2 cables off the port quarter")[1].endswith(
        "; her half-pounder swivels do not carry two cables."
    )


def test_the_notional_marks_range_from_a_cable_to_her_longest_random_shot():
    w = frigate()
    at_quarters(w)
    text = say(w, "engage a mark six cables on the starboard beam")[1]
    assert text == (
        "Engage the mark six cables on the starboard beam: the starboard battery, the guns to "
        "fire as they bear; her 32-pounder carronades do not carry six cables."
    )
    assert refused(w, "engage a mark ten cables on the starboard beam") == (
        "No gun of hers carries ten cables: her long 18-pounders' random shot is 9.9 cables."
    )
    assert refused(w, "engage a mark half a cable on the starboard beam") == (
        "A notional mark is laid no nearer than a cable: say 'engage a mark one cable on the "
        "starboard beam' or further off."
    )
    assert refused(w, "engage a mark some cables on the port quarter") == (
        "A mark how many cables off? Say 'engage a mark four cables on the starboard beam'; "
        "'some' is no number of cables."
    )
    for bad in (
        "engage a mark twenty cables on the larboard beam",
        "engage a mark 0.5 cables on the starboard beam",
    ):
        with pytest.raises(OrderError):
            orders.read_whole(w.ship, bad)
    # the King's cutter's carronades throw under four cables
    c = world_at(49.5, -5.5, CUTTER)
    c.run(60)
    at_quarters(c)
    assert refused(c, NOTIONAL) == (
        "No gun of hers carries four cables: her 12-pounder carronades' random shot is 3.9 cables."
    )
    assert say(c, "engage a mark three cables on the starboard beam")[0] == "guns.engage"


def test_the_refusals_suggest_a_mark_within_her_reach():
    """The refusals' example is laid at four cables, or at the whole cables her guns throw
    when that is less: the King's cutter's carronades reach 3.95 (the review's finding)."""
    assert gunnery._example(frigate().ship) == NOTIONAL
    c = world_at(49.5, -5.5, CUTTER)
    c.run(60)
    example = "engage a mark three cables on the starboard beam"
    assert gunnery._example(c.ship) == example
    assert gunnery._example(c.ship, "larboard") == example.replace("starboard", "larboard")
    at_quarters(c)
    assert refused(c, "engage the cask to starboard") == (
        f"There is no cask in the water: say 'heave a cask overboard' first, or '{example}'."
    )
    assert refused(c, "engage a mark some cables on the starboard beam") == (
        f"A mark how many cables off? Say '{example}'; 'some' is no number of cables."
    )
    # and the example itself is taken
    assert say(c, example)[0] == "guns.engage"
    alone = Ship(load_spec(CUTTER))
    with pytest.raises(OrderError) as e:
        orders.handle(alone, "heave a cask overboard")
    assert str(e.value).endswith(f"Say '{example}'.")


def test_aim_at_the_mark_keeps_its_refusal_and_says_the_way_to_it():
    w = frigate()
    at_quarters(w)
    for words in ("fire at the mark", "aim at the mark", "fire at the cask"):
        said = words.split(" at ", 1)[1]
        assert refused(w, words) == (
            f"Aim at what? Say her rigging, her hull, or between wind and water; '{said}' is "
            "none of them; to fire at the mark, say 'engage the mark to starboard' and 'fire'."
        )
    assert refused(w, "aim at the moon").endswith("'the moon' is none of them.")
    with pytest.raises(OrderError) as e:
        orders.read_whole(w.ship, "aim at the mark")
    assert "say 'engage the mark to starboard' and 'fire'" in str(e.value)


# -- the dumb show --------------------------------------------------------------------------


def test_exercise_the_guns_by_its_sides_and_before_cast_loose():
    w = frigate()
    assert refused(w, "exercise the guns").startswith("The hands are not at quarters")
    battery = at_quarters(w, cast_loose=False)
    kind, text, data = say(w, "exercise the guns")
    assert kind == "guns.exercise" and data["side"] == "both" and battery.exercise == "both"
    assert text == (
        "Exercise both batteries in dumb show: the guns served without powder, and no shot "
        "leaves the ship. The guns are not yet cast loose: say 'cast loose the guns'."
    )
    assert (
        say(w, "exercise both batteries")[1]
        == "Both batteries are exercising in dumb show already."
    )
    assert say(w, "exercise the starboard battery")[2]["side"] == "starboard"
    assert say(w, "exercise the starboard guns")[1] == (
        "The starboard battery is exercising in dumb show already."
    )
    assert say(w, "exercise the guns to larboard")[2]["side"] == "larboard"
    assert say(w, "exercise the larboard battery in dumb show")[2]["side"] == "larboard"
    # with no side said, the engaged side
    say(w, "cease exercising")
    battery.engaged = "starboard"
    assert say(w, "exercise the great guns")[2]["side"] == "starboard"
    w.submit("cast loose the guns")
    w.run(200)
    say(w, "cease exercising")
    text = say(w, "exercise the battery")[1]
    assert text == (
        "Exercise the starboard battery in dumb show: the guns served without powder, and no "
        "shot leaves the ship."
    )


def test_the_loaded_guns_keep_their_charges_in_the_answer(monkeypatch):
    w = frigate()
    at_quarters(w)
    monkeypatch.setattr(Battery, "begin_exercise", _begin(["No. 1 starboard gun"]))
    assert say(w, "exercise the starboard battery")[1] == (
        "Exercise the starboard battery in dumb show: the guns served without powder, and no "
        "shot leaves the ship; the one gun loaded keeps its charge and is run out and pointed "
        "only."
    )
    say(w, "cease exercising")
    names = [f"No. {n} larboard gun" for n in range(1, 9)]
    monkeypatch.setattr(Battery, "begin_exercise", _begin(names))
    kind, text, data = say(w, "exercise the larboard battery")
    assert text.endswith("; the 8 guns loaded keep their charges and are run out and pointed only.")
    assert data["loaded"] == names


def _begin(names):
    def begin_exercise(self, side):  # Builder 1's: the side kept, the loaded guns named
        self.exercise = side
        return list(names)

    return begin_exercise


def test_the_exercise_is_refused_while_a_sail_is_engaged_and_allowed_at_a_mark():
    w = frigate()
    battery = at_quarters(w)
    battery.target, battery.target_words = "renard", "the cutter"
    assert refused(w, "exercise the guns") == (
        "She is engaged with the cutter; the guns are not exercised in dumb show while an "
        "enemy is engaged."
    )
    battery.target, battery.target_words = None, ""
    say(w, NOTIONAL)
    assert say(w, "exercise the guns")[2]["side"] == "starboard"


def test_cease_exercising_and_every_way_the_exercise_ends():
    w = frigate()
    battery = at_quarters(w)
    assert say(w, "cease exercising") == (
        "guns.exercise",
        "The guns are not being exercised.",
        {"verb": "cease exercising", "level": 1},
    )
    say(w, "exercise the guns")
    kind, text, _ = say(w, "stop exercising")
    assert text.startswith("Cease exercising: the dumb show is over;")
    assert battery.exercise is None
    # an engage ends it
    say(w, "exercise the guns")
    text = say(w, NOTIONAL)[1]
    assert battery.exercise is None and text.endswith("as they bear, the exercise over.")
    # the colours struck end it
    say(w, "exercise the guns")
    action.strike(w, by_rule=False, words="by the captain's order")
    assert battery.exercise is None


def test_the_exercise_ends_when_the_hands_are_piped_down_from_quarters():
    """Begun before the guns are cast loose and then piped down, the exercise was left on
    with no order to end it (`cease exercising` wants quarters, `secure the guns` finds
    them secured): the action's tick ends it once the hands are not at quarters (the
    review's finding)."""
    w = frigate()
    battery = at_quarters(w, cast_loose=False)
    say(w, "exercise the guns")
    assert battery.exercise == "both"
    w.submit("pipe down")
    w.run(3)
    assert not w.ship.extra["quarters"].at_quarters
    assert battery.exercise is None
    assert "exercising" not in _guns(w, None)["words"]
    assert "exercise" not in _guns(w, None)
    assert "practice" in idle_rows(w)
    # at quarters it lasts as before
    at_quarters(w, cast_loose=False)
    say(w, "exercise the starboard battery")
    w.run(60)
    assert battery.exercise == "starboard"


def test_the_word_to_fire_is_refused_in_dumb_show_and_a_gun_by_name_fires():
    w = frigate()
    at_quarters(w)
    say(w, NOTIONAL)
    say(w, "exercise the starboard battery")
    for words in ("fire", "fire the starboard broadside", "fire both broadsides", "open fire"):
        assert refused(w, words) == (
            "The battery is exercising in dumb show: no gun is fired at the word; say "
            "'cease exercising' first."
        ), words
    kind, text, data = say(w, "fire No. 3 starboard gun")
    assert kind == "guns.fire" and data["guns"]
    assert say(w, "fire a gun to leeward")[0] == "guns.fire"
    battery = battery_of(w.ship)
    before = battery.rounds_fired
    w.run(5 * 60)
    assert battery.single == [] and battery.rounds_fired == before + 2
    assert battery.exercise == "starboard"


def test_in_dumb_show_from_empty_a_gun_fired_by_name_takes_a_cartridge_and_fires():
    """Decision 21's way, the exercise given before the guns are cast loose so that every
    cycle starts empty: a gun fired by name and the gun to leeward leave the dumb show, are
    served live with a cartridge each, and fire as they would (decision 20; §3.3 "fire as
    today"), the rest of the battery still in dumb show (the review's finding: neither ever
    loaded, both waited in `single` the whole exercise and fired only after `cease
    exercising`)."""
    w = frigate()
    battery = at_quarters(w, cast_loose=False)
    say(w, "exercise the starboard battery")
    w.submit("cast loose the guns")
    w.run(150)  # the dumb rounds begun
    assert not any(g.loaded for g in w.ship.guns.values())
    named = say(w, "fire No. 3 starboard gun")[2]["guns"]
    leeward = say(w, "fire a gun to leeward")[2]["gun"]
    assert named == ["gun.3.starboard"] and leeward != "gun.3.starboard"
    for _ in range(10 * 60):
        w.run(1)
        if not battery.single:
            break
    assert battery.single == [] and battery.exercise == "starboard"
    assert battery.rounds_fired == 2
    for gid in (*named, leeward):
        assert w.ship.guns[gid].fired == 1 and battery.drill[gid].live == 1, gid
    # the dumb show goes on beside them, and they return to it empty
    w.run(5 * 60)
    assert battery.rounds_fired == 2 and battery.drill[named[0]].dumb > 0
    assert not any(g.loaded for g in w.ship.guns.values())
    fired = kinds(w, "action.fired")
    assert sum(e.data["fired"] for e in fired) == 2
    assert all(e.text.endswith("the shot into the sea.") for e in fired)


def test_secure_the_guns_ends_the_exercise_and_gives_up_a_mark_and_keeps_a_sail():
    w = frigate()
    battery = at_quarters(w)
    cask = heave_and_see(w)
    say(w, "engage the cask to starboard")
    say(w, "hold your fire")  # stage 0's battery fires live while exercised: nothing fires
    say(w, "exercise the guns")
    w.submit("secure the guns")
    w.run(300)
    assert kinds(w, "guns.secured")
    assert battery.exercise is None and battery.target is None and battery.target_words == ""
    assert cask.gone == ""  # the cask is still in the water, only no longer the mark
    # a sail engaged is kept through the securing, as it was
    battery = at_quarters(w)
    battery.target, battery.target_words = "renard", "the cutter"
    w.submit("secure the guns")
    w.run(300)
    assert battery.target == "renard"


# -- the gunner's filling -------------------------------------------------------------------


def _magazine(w, filled_18: int, powder_lb: float) -> Magazine:
    mag = Magazine(
        cartridges={("long", 18.0): filled_18, ("carronade", 32.0): 790, ("long", 9.0): 316},
        shot={18.0: {"round": 2000}},
        layout=2,
        level={("long", 18.0): 2054, ("carronade", 32.0): 790, ("long", 9.0): 316},
        powder_lb=powder_lb,
    )
    w.ship.extra["magazine"] = mag
    return mag


def test_fill_cartridges_and_cease_filling_out_of_quarters():
    w = frigate()
    mag = _magazine(w, 1954, 240.0)
    mag.filling_held = True
    kind, text, data = say(w, "fill cartridges")
    assert kind == "guns.fill_order" and data["short"] == 1 and data["powder_lb"] == 240.0
    assert text == (
        "The gunner fills cartridges from the powder below: 1954 of 2054 for the long "
        "18-pounders, 2 barrels and 40 pounds below; by day, and at quarters with a man of "
        "the powder to spare."
    )
    assert not mag.filling_held and mag.report_filled
    assert say(w, "cease filling")[1] == (
        "The gunner fills no more cartridges until he is ordered; the magazine shut."
    )
    assert mag.filling_held
    assert say(w, "stop filling cartridges")[1] == "The gunner is not filling."
    assert say(w, "the gunner to fill cartridges")[0] == "guns.fill_order"
    assert not mag.filling_held
    # no powder below
    mag.powder_lb = 0.0
    assert say(w, "fill the cartridges")[1] == (
        "There is no powder below to fill: the filled cartridges are all she has."
    )
    # some powder below, under an 18-pounder's six pounds (the review's finding: it was
    # "no powder below", the magazine's reading saying "too little powder below")
    mag.powder_lb = 3.0
    assert say(w, "fill the cartridges")[1] == (
        "The powder below is too little to fill another cartridge: 3 pounds below; the "
        "filled cartridges are all she has."
    )
    mag.recount()
    assert "too little powder below to fill more" in mag.describe()[0]
    mag.powder_lb = 0.0
    assert say(w, "cease filling")[1] == "The gunner is not filling."
    # complete
    _magazine(w, 2054, 100.0)
    assert say(w, "fill cartridges")[1] == (
        "The cartridges are filled to the allowance already: 2054 for the long 18-pounders, "
        "316 for the long 9-pounders, 790 for the 32-pounder carronades; 1 barrel below."
    )


def test_fill_cartridges_names_the_one_gun_of_a_kind_singular():
    """The privateer's pivot is her one long 12-pounder: the answer names "the long
    12-pounder", as the magazine's reading does (the review's finding: "the long
    12-pounders")."""
    w = world_at(49.5, -5.5, PRIVATEER)
    w.run(60)
    mag = Magazine(
        cartridges={("long", 12.0): 50, ("carronade", 12.0): 220, ("swivel", 0.5): 176},
        shot={12.0: {"round": 200}},
        layout=2,
        level={("long", 12.0): 55, ("carronade", 12.0): 220, ("swivel", 0.5): 176},
        powder_lb=300.0,
        gun_count={("long", 12.0): 1, ("carronade", 12.0): 4, ("swivel", 0.5): 4},
    )
    w.ship.extra["magazine"] = mag
    text = say(w, "fill cartridges")[1]
    assert text.startswith(
        "The gunner fills cartridges from the powder below: 50 of 55 for the long 12-pounder, "
    ), text
    assert "for the long 12-pounder" in mag.describe()[0]
    mag.cartridges[("long", 12.0)] = 55
    text = say(w, "fill cartridges")[1]
    assert text.startswith(
        "The cartridges are filled to the allowance already: 55 for the long 12-pounder, 220 "
        "for the 12-pounder carronades, 176 for the half-pounder swivels; "
    ), text


# -- the standing dialect's reading whole ---------------------------------------------------


@pytest.mark.parametrize(
    "words",
    [
        "heave a cask overboard",
        "heave a cask overboard from the starboard quarter",
        "engage the cask to starboard",
        "engage the mark to larboard",
        NOTIONAL,
        "exercise the guns",
        "exercise the starboard battery",
        "exercise the guns in dumb show",
        "cease exercising",
        "fill cartridges",
        "cease filling",
    ],
)
def test_every_form_is_read_whole(words):
    w = frigate()
    order = orders.read_whole(w.ship, words)
    assert order.verb in gunnery.GUNNERY_VERBS


@pytest.mark.parametrize(
    "words,refusal",
    [
        ("heave a cask overboard from the bowsprit", "Heave it over from which quarter?"),
        ("exercise the guns at the double", "Exercise which guns?"),
        ("engage a mark ten cables on the starboard beam", "No gun of hers carries ten cables"),
        ("engage a mark several cables on the starboard beam", "A mark how many cables off?"),
    ],
)
def test_the_standing_dialect_refuses_the_words_that_make_no_sense(words, refusal):
    w = frigate()
    with pytest.raises(OrderError) as e:
        orders.read_whole(w.ship, words)
    assert str(e.value).startswith(refusal)


def test_a_standing_order_of_practice_is_entered():
    w = frigate()
    kind, text, _ = orders.handle(
        w.ship, 'standing order "drill": at eight bells then exercise the starboard battery'
    )
    assert kind == "standing.given", text


# -- the files ------------------------------------------------------------------------------


def test_heave_mark_is_in_the_catalogue_with_every_key_of_an_evolution_file():
    from freesail.evolutions import EVOLUTIONS
    from freesail.evolutions.scripts import SCRIPTS

    evo = EVOLUTIONS["heave_mark"]
    assert evo.script == "heave_mark" and "heave_mark" in SCRIPTS
    assert evo.timing == {"heave_s": 60.0} and evo.preconditions == []
    assert evo.crew == {"hands": 2, "rating": "ordinary", "stations": ["afterguard", "quarterdeck"]}
    assert evo.on_complete.kind == "practice.mark_over" and evo.on_complete.severity == "notable"
    assert "Regulations" in evo.source and "UNVERIFIED" in evo.source
    ours = yaml.safe_load((ROOT / "data/evolutions/heave_mark.yaml").read_text(encoding="utf-8"))
    theirs = yaml.safe_load((ROOT / "data/evolutions/secure_guns.yaml").read_text(encoding="utf-8"))
    assert set(ours) == set(theirs)
    assert b"\r\n" not in (ROOT / "data/evolutions/heave_mark.yaml").read_bytes()


def test_the_scenario_is_written_again_byte_for_byte_and_loads():
    from freesail.world.scenarios import (
        begin,
        load_scenario,
        make_scenario_world,
        read_scenario_text,
        scenario_text,
    )

    raw = SCENARIO.read_bytes()
    assert b"\r\n" not in raw
    text, fields = read_scenario_text(SCENARIO)
    assert scenario_text(fields, text) == text
    doc = yaml.safe_load(text)
    assert "weather_bound" not in doc and "ships" not in doc
    sf = load_scenario(SCENARIO)
    sc = sf.scenario
    assert sf.seed == 7 and sf.ship_file == FRIGATE
    assert sf.orders == ["set plain sail"]
    assert sc.start_time == datetime(1805, 6, 14, 9, 0)
    assert sc.position == pytest.approx({"lat_deg": 49.0 + 52.0 / 60.0, "lon_deg": -5.2})
    assert sc.region == "channel-west" and sc.nation == "britain"
    assert doc["ship"]["file"] == FRIGATE and doc["ship"]["heading_deg"] == 180
    assert doc["ship"]["speed_kn"] == 5
    assert doc["wind"] == {"from_deg": 280, "knots": 10, "gustiness": 0.0, "variability": 0.0}
    assert doc["ports"] == ["falmouth", "plymouth"] and doc["orders"] == ["set plain sail"]
    assert doc["standing_orders"] == [
        "data/standing_orders/starter.orders",
        "data/standing_orders/fighting.orders",
    ]
    assert doc["intent"] == "cruise off the Lizard within 10 miles"
    assert "no model seated, nothing happens" in text
    w = make_scenario_world(sf)
    begin(w, sf)
    assert w.ship.spec.name == "Amazon" and not w.vessels.active()  # her own vessel apart
    w.run(120)
    assert not [e for e in w.log if e.kind.startswith(("practice.", "guns.", "action."))]


def test_a_rules_captain_with_a_cask_engaged_for_half_an_hour_leaves_the_guns_be():
    """The scenario under the rules captain, the player's orders given by the test: at
    quarters with the cask engaged for thirty minutes. The captain's machine and the
    fighting book let the mark be (nobody's book secures the guns, ceases fire or takes the
    cask for an enemy); the book's 'open fire' follows the range reading of the cask. The
    finding for the lead: keeping her station he stands on and the cask falls astern, out
    of the broadside's arc and then out of sight from the masthead (a mile by day), so no
    shot is fired at it at seed 7; practice wants her hove to or kept about the cask by the
    player."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(SCENARIO)
    w = make_scenario_world(sf)
    begin(w, sf)
    w.run(120)
    w.submit("beat to quarters")
    w.submit("heave a cask overboard")
    w.run(10)
    w.submit("cast loose the guns")
    w.run(120)
    cask = marks.cask_in_water(w.ship)
    assert cask is not None and marks.cask_in_sight(w, cask)
    side = "larboard" if "larboard" in kinds(w, "practice.mark_over")[0].text else "starboard"
    engaged = w.submit(f"engage the cask to {side}")
    assert engaged.kind == "guns.engage", engaged.text
    n = len(w.log)
    battery = battery_of(w.ship)
    for _ in range(30):
        w.run(60)
        assert battery.target in (cask.id, None)
        if battery.target is None:
            assert cask.gone in ("struck", "lost")
        assert w.captain.state != "engaging"
        assert w.ship.extra["quarters"].at_quarters
    after = w.log[n:]
    assert not [e for e in after if e.kind in ("guns.secured", "guns.cease", "action.fired_at")]
    assert not [e for e in after if e.kind.startswith("action.") and e.kind != "action.fired"]
    assert [e for e in w.log if "By standing order 'open fire'" in e.text]
    assert battery.mode is not FireMode.HOLD
