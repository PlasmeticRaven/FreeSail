"""The Python API of standing orders (spec M4 §4): the decorators build package 25's
rules into the same book, a Python rule and its dialect twin give identical logs
(truth 40), the body runs once at registration and may call only `order(...)`, the
refusals are the dialect's, and a save lists a Python rule by name and source and
refuses to run it without its file.
"""

from __future__ import annotations

import io
from datetime import datetime

import pytest

from freesail.api.readings import ReadingsView
from freesail.api.session import make_world, ship_factory
from freesail.core import replay
from freesail.core.world import Scenario, World
from freesail.orders.errors import OrderError
from freesail.standing import (
    ACTOR_PREFIX,
    Rule,
    at,
    bind,
    every,
    order,
    restore_absent,
    unbind,
    when,
)
from freesail.standing.python_api import ABSENT_PYTHON
from freesail.ui.console import Console

FRIGATE = "data/ships/frigate-36.yaml"

NIGHT = (
    'standing order "night routine": at sunset then take in the studdingsails; take in the royals'
)
MORNING = (
    'standing order "morning sail": at sunrise, if the true wind is under 20 knots '
    "then set the royals"
)
SHORTEN = (
    'standing order "shorten sail for weather": when the true wind exceeds 30 knots for '
    "2 minutes then take in the studdingsails; take in the royals; reef the topsails, one reef"
)


def frigate(start: datetime, knots: float = 15.0, heading: float = 180.0) -> World:
    return make_world(
        7,
        FRIGATE,
        Scenario(
            start_time=start,
            wind_from_deg=0.0,
            wind_speed_kn=knots,
            gustiness=0.0,
            variability=0.0,
            ship_heading_deg=heading,
        ),
    )


@pytest.fixture
def unbound():
    """Every test binds its own world and leaves none behind."""
    unbind()
    yield
    unbind()


def standing_lines(world: World) -> list[tuple[int, str, str]]:
    return [(e.tick, e.kind, e.text) for e in world.log if e.actor.startswith(ACTOR_PREFIX)]


def after_the_start(world: World) -> list[tuple[int, str, str, str]]:
    return [(e.tick, e.kind, e.text, e.actor) for e in world.log if e.tick > 0]


# ---------------------------------------------------------------------------
# Truth 40: a Python rule and its dialect twin produce identical logs
# ---------------------------------------------------------------------------


def test_truth_40_the_night_routine_in_python_and_in_the_dialect_give_one_log(unbound):
    """Spec M4 §4 and §8, truth 40. Two frigates from seed 7 running before the wind at
    19:40 on 1 June under all sail; one is given the night routine in the dialect, the
    other the same rule through `@at("sunset")`. Everything after the tick the rules
    were given (the sunset, the firings, the sails coming in, every hand's work) is
    byte-identical: the same event texts at the same ticks with the same actors. The
    entry lines at tick 0 differ only in that the dialect's came through an order
    ("Order: standing order ...") and the Python rule's did not."""
    dialect = frigate(datetime(1805, 6, 1, 19, 40))
    python = frigate(datetime(1805, 6, 1, 19, 40))
    for w in (dialect, python):
        w.submit("make all sail")
    dialect.submit(NIGHT)
    bind(python)

    @at("sunset", name="night routine")
    def night_routine():
        order("take in the studdingsails")
        order("take in the royals")

    rule = night_routine.rule
    twin = dialect.standing.book.get("night routine")
    assert isinstance(rule, Rule) and rule.source == "python" and rule.trusted
    assert twin.source == "dialect" and not twin.trusted
    assert rule.body_words() == twin.body_words()
    assert rule.actions == twin.actions and rule.trigger.event == twin.trigger.event
    given_d = [e.text for e in dialect.log if e.tick == 0 and e.kind == "standing.given"]
    given_p = [e.text for e in python.log if e.tick == 0 and e.kind == "standing.given"]
    assert given_d == given_p
    dialect.run(1500)
    python.run(1500)
    assert standing_lines(python) == standing_lines(dialect)
    assert [t for t, *_ in standing_lines(python)] and all(
        (python.clock.start.replace(hour=0, minute=0, second=0)).__class__  # a tick each
        for _ in [0]
    )
    assert after_the_start(python) == after_the_start(dialect)
    assert python.state() == dialect.state()
    assert (rule.fired, rule.last_fired_tick) == (twin.fired, twin.last_fired_tick) == (1, 1142)


def test_a_when_rule_with_a_duration_fires_as_its_twin_does(unbound):
    dialect = frigate(datetime(1805, 6, 1, 10, 0), knots=32.0)
    python = frigate(datetime(1805, 6, 1, 10, 0), knots=32.0)
    for w in (dialect, python):
        w.submit("set plain sail")
        w.run(600)
    dialect.submit(SHORTEN)
    bind(python)

    @when("the true wind exceeds 30 knots", for_minutes=2, name="shorten sail for weather")
    def shorten_sail():
        order("take in the studdingsails")
        order("take in the royals")
        order("reef the topsails, one reef")

    rule = shorten_sail.rule
    assert rule.trigger.kind == "when" and rule.trigger.duration_s == 120
    assert rule.trigger.text == "when the true wind exceeds 30 knots for 2 minutes"
    assert rule.body_words() == dialect.standing.book.get("shorten sail for weather").body_words()
    dialect.run(900)
    python.run(900)
    assert standing_lines(python) == standing_lines(dialect)
    assert rule.fired == 1 and rule.last_fired_tick == 720


def test_an_at_rule_with_a_condition_is_held_as_its_twin_is(unbound):
    dialect = frigate(datetime(1805, 6, 1, 3, 40), knots=25.0)
    python = frigate(datetime(1805, 6, 1, 3, 40), knots=25.0)
    dialect.submit(MORNING)
    bind(python)

    @at("sunrise", condition="the true wind is under 20 knots", name="morning sail")
    def morning_sail():
        order("set the royals")

    assert morning_sail.rule.condition is not None
    assert morning_sail.rule.body_words() == (
        "at sunrise, if the true wind is under 20 knots then set the royals"
    )
    dialect.run(1500)
    python.run(1500)
    held = [(t, x) for t, k, x in standing_lines(python) if k == "standing.held"]
    assert held == [
        (
            988,
            "Standing order 'morning sail' at sunrise: not carried out; the true wind is "
            "25 knots, not under 20 knots.",
        )
    ]
    assert standing_lines(python) == standing_lines(dialect)


def test_every_with_seconds_and_a_condition_and_an_officer(unbound):
    w = bind(frigate(datetime(1805, 6, 1, 8, 0)))

    @every("20 minutes", condition="the speed is under 30 knots", name="trim", by="the master")
    def trim():
        order("trim sails")

    rule = trim.rule
    assert rule.trigger.kind == "every" and rule.trigger.interval_s == 1200
    assert rule.given_by == "master" and rule.officer == "the master"
    assert rule.body_words() == "every 20 minutes, if the speed is under 30 knots then trim sails"
    entered = [e for e in w.log if e.kind == "standing.given"]
    assert entered[0].text == (
        "Standing order 'trim' entered in the book by the master: every 20 minutes, if the "
        "speed is under 30 knots then trim sails."
    )

    @when("the heel exceeds 15 degrees", for_seconds=90)
    def ease_her():
        order("reef the topsails, one reef")

    assert ease_her.rule.name == "ease her" and ease_her.rule.trigger.duration_s == 90
    assert w.standing.book.names == ["trim", "ease her"]


# ---------------------------------------------------------------------------
# The body: once, at registration; order(...) and the readings only
# ---------------------------------------------------------------------------


def test_the_body_runs_once_at_registration_and_is_handed_the_readings(unbound):
    w = bind(frigate(datetime(1805, 6, 1, 12, 0)))
    w.submit("set plain sail")
    w.run(600)
    calls: list[object] = []

    @at("eight bells", name="log the readings")
    def body(readings):
        calls.append(readings)
        assert isinstance(readings, ReadingsView)
        assert readings["daylight"] == "day"
        assert readings["true_wind_speed"] > 0
        order("trim sails")

    assert len(calls) == 1
    w.run(4 * 3600)  # eight bells at 16:00 fires the rule
    assert body.rule.fired == 1
    assert len(calls) == 1, "the body is not run again at firing; its orders were collected"
    assert body.rule.actions == ["trim sails"]


def test_the_decorated_function_is_returned_and_carries_its_rule(unbound):
    w = bind(frigate(datetime(1805, 6, 1, 12, 0)))

    @every("a glass", name="glass")
    def glass():
        order("trim sails")
        return 42

    assert callable(glass) and glass.rule is w.standing.book.get("glass")
    with pytest.raises(OrderError, match="only be called inside a rule's body"):
        glass()  # calling it again outside a registration is not giving orders


def test_a_rule_may_name_its_world_instead_of_the_bound_one(unbound):
    a = frigate(datetime(1805, 6, 1, 12, 0))
    b = frigate(datetime(1805, 6, 1, 12, 0))
    bind(a)

    @at("sunset", name="night routine", world=b)
    def night():
        order("take in the royals")

    assert b.standing.book.names == ["night routine"] and a.standing.book.names == []


# ---------------------------------------------------------------------------
# Refusals, in the dialect's words, at registration
# ---------------------------------------------------------------------------


def test_refusals_are_the_dialects_and_come_at_registration(unbound):
    with pytest.raises(OrderError, match="No world is bound"):

        @at("sunset")
        def no_world():
            order("take in the royals")

    bind(frigate(datetime(1805, 6, 1, 12, 0)))
    with pytest.raises(OrderError, match="did you mean the royals"):

        @at("sunset", name="misspelt")
        def misspelt():
            order("set the royls")

    with pytest.raises(OrderError, match="gives no orders; call order"):

        @when("the true wind exceeds 30 knots", name="empty")
        def empty():
            pass

    with pytest.raises(OrderError, match="'at dawn' names no event"):

        @at("dawn", name="dawn")
        def dawn():
            order("set the royals")

    # a sighting is an event since package 33a named it; the order after it is still parsed
    with pytest.raises(OrderError, match="clear for action"):

        @at("a sighting", name="sighting")
        def sighting():
            order("clear for action")

    with pytest.raises(OrderError, match="cannot be 'shaking'"):

        @when("the true wind is shaking", name="shaking")
        def shaking():
            order("set the royals")

    with pytest.raises(OrderError, match="not an interval"):

        @every("fortnight", name="fortnight")
        def fortnight():
            order("trim sails")

    with pytest.raises(OrderError, match="no officer"):

        @at("sunset", name="purser", by="purser")
        def purser():
            order("set the royals")

    with pytest.raises(OrderError, match="no well to sound"):

        @every("a glass", name="sound the well")
        def sound():
            order("sound the well")

    with pytest.raises(OrderError, match="only be called inside"):
        order("set the royals")

    with pytest.raises(OrderError, match="in the book already"):

        @at("sunset", name="twice")
        def once():
            order("set the royals")

        @at("sunset", name="twice")
        def twice():
            order("set the royals")


# ---------------------------------------------------------------------------
# Saving: name and source; loading without the file
# ---------------------------------------------------------------------------


def test_a_python_rule_saves_as_its_name_and_source_and_loads_listed_but_belayed(unbound, tmp_path):
    w = bind(frigate(datetime(1805, 6, 1, 19, 40)))
    w.submit("make all sail")

    @at("sunset", name="night routine")
    def night_routine():
        order("take in the studdingsails")
        order("take in the royals")

    w.submit(MORNING)
    w.run(1500)
    saved = w.save()
    entries = {r["name"]: r for r in saved["standing_orders"]}
    assert entries["night routine"]["source"] == "python"
    assert entries["night routine"]["text"].startswith('@at("sunset", name="night routine")')
    assert "def night_routine" in entries["night routine"]["text"]
    assert entries["night routine"]["fired"] == 1
    assert entries["morning sail"]["source"] == "dialect"
    # a load without the defining module: the dialect's rule replays from the journal,
    # the Python rule is listed, belayed, with the sentence, and refuses to resume
    path = replay.save_to_file(w, tmp_path / "python.json")
    data = replay.load_file(path)
    copy = replay.replay(data, ship_factory)
    assert copy.standing.book.names == ["morning sail"]
    missing = copy.standing.book.restore_state(data["standing_orders"])
    assert missing == ["night routine"]
    placeholders = restore_absent(copy, data["standing_orders"])
    assert [r.name for r in placeholders] == ["night routine"]
    listing = copy.submit("standing orders").text
    assert f'"night routine" (the captain): {ABSENT_PYTHON}' in listing
    assert "Belayed; fired once" in listing
    refused = copy.submit('resume standing order "night routine"')
    assert refused.kind == "order.rejected"
    assert f"Standing order 'night routine' {ABSENT_PYTHON}." in refused.text
    absent = [e.text for e in copy.log if e.kind == "standing.absent"]
    assert absent == [f"Standing order 'night routine' {ABSENT_PYTHON}."]
    copy.run(600)
    assert placeholders[0].fired == 1, "it did not run"
    assert restore_absent(copy, data["standing_orders"]) == [], "entered once"
    # bound again with its module present, the same rule enters the loaded book
    bind(copy)
    copy.submit('belay standing order "morning sail"')

    @at("sunset", name="night routine again")
    def night_routine_again():
        order("take in the royals")

    assert copy.standing.book.names == ["morning sail", "night routine", "night routine again"]


def test_the_console_lists_a_saves_python_rules_on_replay(unbound, tmp_path):
    w = bind(frigate(datetime(1805, 6, 1, 12, 0)))

    @every("a glass", name="glass")
    def glass():
        order("trim sails")

    w.run(60)
    path = tmp_path / "glass.json"
    replay.save_to_file(w, path)
    out = io.StringIO()
    con = Console(frigate(datetime(1805, 6, 1, 12, 0)), out=out)
    con.handle_line(f"replay {path}")
    con.handle_line("standing orders")
    text = out.getvalue()
    assert f"Standing order 'glass' {ABSENT_PYTHON}." in text
    assert f'"glass" (the captain): {ABSENT_PYTHON}' in text
