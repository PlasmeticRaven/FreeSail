import io

from freesail.core.world import World
from freesail.ui.console import Console


def make_console():
    out = io.StringIO()
    world = World(seed=3)
    return Console(world, out=out), out


def test_driver_commands_are_not_journaled():
    con, out = make_console()
    assert con.handle_line("tick 10")
    assert con.handle_line("state")
    assert con.handle_line("time 30")
    assert con.handle_line("hold")
    assert con.world.journal == []
    assert con.world.clock.tick == 10
    text = out.getvalue()
    assert "Advanced 10 ticks" in text
    assert "Compression 30x" in text


def test_orders_go_to_the_ship_and_print():
    con, out = make_console()
    con.handle_line("steer west")
    assert con.world.journal == [(0, "captain", "steer west")]
    assert "steer W" in out.getvalue()


def test_quit_returns_false():
    con, _ = make_console()
    assert con.handle_line("quit") is False


def test_save_and_replay_from_console(tmp_path):
    con, out = make_console()
    con.handle_line("steer 45")
    con.handle_line("tick 120")
    digest = con.world.log.digest()
    path = tmp_path / "s.json"
    con.handle_line(f"save {path}")
    con.handle_line(f"replay {path}")
    assert con.world.log.digest() == digest
    assert "Replayed" in out.getvalue()


def test_rollup_at_high_compression():
    """At 60x the routine lines of each hour roll up into one line at the hour's end
    (spec M4 §20; package 29 replaced the per-bell count above 10x with the hourly
    roll-up, tests/test_rollup.py)."""
    con, out = make_console()
    con.handle_line("time 60")
    con.handle_line("go")
    con.world.run(3600)  # 04:00 to 05:00: the hour closes at the 05:00 bell
    text = out.getvalue()
    assert "1 bell" not in text  # rolled up, not printed
    assert "= Morning watch (04:00-05:00)" in text
    assert "routine entries." in text


def test_the_console_prints_the_followed_hulls_log_after_follow():
    """The owner's finding of 2026-10-31: after `follow "<ship>"` the orders went to her
    hull and their lines to her log, and the console went on printing the hull it was
    attached to, so an order, a refusal or an answer showed nothing. The listener moves
    with the followed hull (`Console._follow_log`), and back."""
    from tests.test_observer import observed_world

    w, _ = observed_world()
    out = io.StringIO()
    con = Console(w, out=out)
    assert con.handle_line('follow "Medusa"')
    mark = out.tell()
    assert con.handle_line("set the royals")
    assert "Order: set the royals." in out.getvalue()[mark:]
    assert con.handle_line("follow nobody")
    assert w.followed is None
    mark = out.tell()
    con.handle_line("tick 1")
    assert con.handle_line("set the royals")  # the observer's refusal, printed as before
    assert "No ship followed" in out.getvalue()[mark:]


def test_truth_7_798_the_console_keeps_the_records_place_as_words_and_its_save_a_checkpoint(
    tmp_path,
):
    """Truth 7-798's third road (package 129; the lead's mutant of c22aa834): the console
    hosting the agents with a records place given (`serve_agents`, as `--consent-records`
    gives it, a path object from a caller) keeps the place in the world as words, which a
    checkpoint may hold; its save is read by names without loading (no path, nothing not
    admitted) and loads by its checkpoint, the game as it was."""
    import socket
    import sys
    from pathlib import Path

    from freesail.ui.server import prepare_game, server_parser

    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))
    import checkpoint_holders as H

    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        port = s.getsockname()[1]
    con, _out = make_console()
    records = tmp_path / "consent"
    server = con.serve_agents(port, records_dir=records, saves_dir=str(tmp_path / "saves"))
    try:
        place = con.world.consent_records_dir
        assert isinstance(place, str) and Path(place) == records
        con.handle_line("steer 45")
        con.handle_line("tick 120")
        save = tmp_path / "s.json"
        con.handle_line(f"save {save}")
        body = H.pickle_of(save.with_suffix(".checkpoint"))
        assert not [h.line() for h in H.holders(body) if h.module.startswith("pathlib")]
        assert not [h.line() for h in H.not_admitted(body)]
        loaded = prepare_game(server_parser().parse_args(["--load", str(save)]), say=print)
        assert loaded.load_report.how == "checkpoint", loaded.load_report.words
        assert loaded.clock.tick == con.world.clock.tick
        assert loaded.log.digest() == con.world.log.digest()
        assert loaded.consent_records_dir == place
    finally:
        server.should_exit = True
