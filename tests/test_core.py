from datetime import datetime, timedelta

from freesail.core.clock import Clock
from freesail.core.events import Event, Log, Severity
from freesail.core.rng import Rng


def test_clock_advances_and_reports_bells_once():
    clock = Clock(datetime(1805, 6, 1, 9, 29, 58))
    seen = []
    for _ in range(5):
        clock.advance()
        b = clock.bells()
        if b is not None:
            seen.append((clock.tick, b))
        # a second call in the same tick must not report again
        assert clock.bells() is None
    assert seen == [(2, 3)]
    assert clock.ship_time == datetime(1805, 6, 1, 9, 29, 58) + timedelta(seconds=5)
    assert clock.stamp().startswith("Forenoon watch")


def test_rng_streams_are_stable_and_independent():
    a = Rng(42)
    b = Rng(42)
    xs = [a.stream("wind").random() for _ in range(5)]
    ys = [b.stream("wind").random() for _ in range(5)]
    assert xs == ys
    # a different stream name gives a different sequence
    zs = [Rng(42).stream("strain").random() for _ in range(5)]
    assert zs != xs
    # consuming another stream does not disturb this one
    c = Rng(42)
    c.stream("strain").random()
    c.stream("strain").random()
    assert [c.stream("wind").random() for _ in range(5)] == xs
    # a different seed differs
    assert [Rng(43).stream("wind").random() for _ in range(5)] != xs


def _event(tick, kind="x", sev=Severity.ROUTINE, text="t"):
    return Event(tick, datetime(1805, 6, 1) + timedelta(seconds=tick), sev, kind, text)


def test_log_queries_and_subscribers():
    log = Log()
    got = []
    log.subscribe(got.append)
    log.append(_event(0, "a"))
    log.append(_event(5, "b", Severity.NOTABLE))
    log.append(_event(9, "a", Severity.URGENT))
    assert len(log) == 3
    assert len(got) == 3
    assert [e.kind for e in log.since(0)] == ["b", "a"]
    assert [e.tick for e in log.of_kind("a")] == [0, 9]
    assert [e.tick for e in log.at_least(Severity.NOTABLE)] == [5, 9]
    assert [e.tick for e in log.tail(2)] == [5, 9]


def test_log_digest_depends_on_content():
    a, b, c = Log(), Log(), Log()
    a.append(_event(0, "a"))
    b.append(_event(0, "a"))
    c.append(_event(0, "a", text="different"))
    assert a.digest() == b.digest()
    assert a.digest() != c.digest()


def test_event_line_format():
    e = _event(0, "sail.set", Severity.NOTABLE, "Set the fore topsail.")
    assert e.line() == "* Middle watch, 8 bells (00:00)  Set the fore topsail."
