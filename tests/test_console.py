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
    con, out = make_console()
    con.handle_line("time 60")
    con.handle_line("go")
    con.world.run(1800)  # to the first bell; routine entries should roll up
    text = out.getvalue()
    assert "1 bell" in text
    assert "routine entries" in text or "Steady" not in text
