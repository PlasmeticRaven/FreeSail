"""The director's seat hook and the live world order (spec M6 §23; package 43): `seat:
<model> as captain of <ship> for <budget>` and `unseat: <ship>` on the world-order channel,
refused without a consent record, an owner's grant or budget; the budget counted and the
station stood down when it is spent; `world: <order>` at the console and in the browser the
owner's live order, the bare order still refused at the prompt (truth 71)."""

from __future__ import annotations

import pytest

from freesail.agents import consent
from freesail.core.world import World
from freesail.world import orders as WO
from tests.test_brains import put, world_at

WEIGHTS = "made-up-director-model-9b.Q4_K_M.gguf"
OTHER = "another-made-up-model.gguf"


def granted_world(tmp_path, models=(WEIGHTS,), seats=1, in_voyage=2) -> World:
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    w.scenario.director = {"models": list(models), "seats": seats, "seats_in_voyage": in_voyage}
    records = tmp_path / "consent"
    records.mkdir(exist_ok=True)
    consent.Record(
        WEIGHTS, "a test runtime", "2026-10-16", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    consent.Record(
        OTHER, "a test runtime", "2026-10-16", consent.NO, answer="No.", conditions="a reason"
    ).write(records)
    w.consent_records_dir = records
    put(w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth")
    put(w, "cutter", "britain", "49 20 N 5 32 W", "bound for Falmouth", name="Lark")
    put(
        w,
        "merchant brig",
        "britain",
        "49 10 N 5 20 W",
        "bound for Falmouth",
        "bound for Falmouth",
        name="Nancy",
    )
    return w


def test_the_seat_is_refused_without_a_record_a_grant_or_budget_and_held_with_them(tmp_path):
    w = granted_world(tmp_path)
    assert WO.recognises("seat: x as captain of y for 3 samples")
    assert WO.recognises("unseat: y")
    e = w.world_order(f"seat: {OTHER} as captain of X for 3 samples")
    assert e.data["result"] == "refused" and "no yes" in e.text
    e = w.world_order("seat: nobody-at-all as captain of X for 3 samples")
    assert e.data["result"] == "refused" and "No consent is on record" in e.text
    w.scenario.director = {}
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for 3 samples")
    assert e.data["result"] == "refused" and "granted the director no seats" in e.text
    w.scenario.director = {"models": ["some-other-name"], "seats": 1, "seats_in_voyage": 2}
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for 3 samples")
    assert e.data["result"] == "refused" and "grant does not name" in e.text
    w.scenario.director = {"models": [WEIGHTS], "seats": 1, "seats_in_voyage": 2}
    e = w.world_order(f"seat: {WEIGHTS} as captain of Lark for 3 samples")
    assert e.data["result"] == "refused" and "no captain of her own" in e.text
    e = w.world_order(f"seat: {WEIGHTS} as captain of Z for 3 samples")
    assert e.data["result"] == "refused" and "No ship named" in e.text
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for no samples")
    assert e.data["result"] == "refused"
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for 3 samples")
    assert e.data["result"] == "done" and "held for" in e.text
    assert WO.director_seats(w) == {
        "ship-1": {"model": WEIGHTS, "budget": 3, "unit": "samples", "tick": w.clock.tick}
    }
    v = w.vessels.find("X")
    assert v.crew is not None  # her World made, in the shape her distance gives
    # the seats at once are spent; unseat gives the place back; the voyage's count holds
    e = w.world_order(f"seat: {WEIGHTS} as captain of Nancy for 2 hours")
    assert e.data["result"] == "refused" and "at once are spent" in e.text
    e = w.world_order("unseat: X, the director has seen enough")
    assert e.data["result"] == "done" and "the director has seen enough" in e.text
    assert WO.director_seats(w) == {}
    e = w.world_order("unseat: X")
    assert e.data["result"] == "refused" and "holds no seat" in e.text
    e = w.world_order(f"seat: {WEIGHTS} as captain of Nancy for two hours")
    assert e.data["result"] == "done" and "2 hours" in e.text
    w.world_order("unseat: Nancy")
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for 3 samples")
    assert e.data["result"] == "refused" and "in this voyage are spent" in e.text
    # the seat hook assumes no player's ship where that costs nothing: a bare World
    bare = World(seed=1)
    e = bare.world_order(f"seat: {WEIGHTS} as captain of X for 3 samples")
    assert e.data["result"] == "refused"


def test_a_door_under_a_directors_seat_is_stood_down_when_the_budget_is_spent(tmp_path):
    pytest.importorskip("fastapi")
    from own_page import DoorClient

    from freesail.ui.server import Driver, create_app

    w = granted_world(tmp_path)
    w.run(61)
    e = w.world_order(f"seat: {WEIGHTS} as captain of X for 2 samples")
    assert e.data["result"] == "done"
    driver = Driver(w, compression=60.0)
    app = create_app(
        driver, game="a test", consent_records=w.consent_records_dir, saves_dir=tmp_path / "saves"
    )
    with DoorClient(app) as http:
        a = http.post(
            "/api/agents/captain", json={"model_name": WEIGHTS, "door": "mcp", "ship": "X"}
        ).json()
        key = a["key"]
        crew = w.vessels.find("X").crew
        h = crew.agents["captain"]
        for _ in range(3):
            http.post(
                "/api/agents/captain/reply",
                json={
                    "text": "",
                    "calls": [{"name": "stand_by", "args": {"until": "eight bells"}}],
                    "key": key,
                    "ship": "X",
                },
            )
            for _ in range(130):
                driver.tick(60)
                if h.agent.released:
                    break
            if h.agent.released:
                break
        assert h.agent.released and "director's budget" in (h.agent.released_reason or "")
        assert WO.director_seats(w) == {}


def test_the_live_world_order_at_the_console_and_the_browser_and_the_bare_order_refused():
    from freesail.ui.console import Console, live_world_order

    assert live_world_order('world: ship "X": intent bound for Brest') == (
        'ship "X": intent bound for Brest'
    )
    assert (
        live_world_order("World:  port brest: closed to Britain") == "port brest: closed to Britain"
    )
    assert live_world_order("the world") is None and live_world_order("world:") is None
    w = world_at(49.5, -5.5)
    console = Console(w, compression=1.0)
    console.handle_line(
        'world: ship: a merchant brig "Nancy" of Britain at 49 20 N 5 40 W, bound for Falmouth, '
        "intent: bound for Falmouth"
    )
    v = w.vessels.find("Nancy")
    assert v is not None and v.brain is not None
    orders = [o for o in w.world_orders if o["source"] == "the owner"]
    assert orders and orders[-1]["result"] == "done"
    assert w.inputs[-1]["source"] == "the owner" and "world_order" in w.inputs[-1]
    # a bare world order at the prompt is still the captain's grammar's refusal (truth 71)
    e = console.world.submit('ship "Nancy": intent run home to Brest')
    assert e.kind == "order.rejected" and "order to the world" in e.text
    # the browser's driver takes the same prefix
    pytest.importorskip("fastapi")
    from freesail.ui.server import Driver

    driver = Driver(w, compression=60.0)
    e = driver.submit('world: ship "Nancy": intent run home to Brest')
    assert e.kind == "world.order" and e.data["result"] == "done"
    assert v.brain.intent.words == "run home to Brest"
    # the live order is replayed from the save as the harness's are (truth 72)
    from freesail.api.session import ship_factory
    from freesail.core import replay as replay_mod

    w.run(120)
    copy = replay_mod.replay(w.save(), ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert copy.vessels.find("Nancy").brain.intent.words == "run home to Brest"


def test_the_director_stands_down_only_the_seats_given_under_the_grant(tmp_path):
    """Package 117 (decision 70; the consent brief: the director "may seat models ... under
    the owner's grant and stand down those so seated"). A station the owner seated at a
    door, with no seat of the director's, is refused to `unseat:` in the world's words,
    by the station's form and by the ship's, and keeps its holder; a seat the director
    held under the grant is given up and its holder stood down, as before; on a ship where
    both are held, `unseat: <ship>` stands down the seat's and keeps the owner's."""
    pytest.importorskip("fastapi")
    from own_page import DoorClient

    from freesail.ui.server import Driver, create_app

    w = granted_world(tmp_path, seats=2, in_voyage=3)
    w.run(61)
    x = w.vessels.find("X")
    assert x.crew is not None and x.crew.shape == "full"
    driver = Driver(w, compression=60.0)
    app = create_app(
        driver, game="a test", consent_records=w.consent_records_dir, saves_dir=tmp_path / "s"
    )
    with DoorClient(app) as http:
        # the owner's door: the captain of the X, and the officer of the watch of his own ship
        a = http.post(
            "/api/agents/captain", json={"model_name": WEIGHTS, "door": "mcp", "ship": "X"}
        ).json()
        assert a["phase"] == "station"
        b = http.post("/api/agents/officer", json={"model_name": WEIGHTS, "door": "mcp"}).json()
        assert b["phase"] in ("station", "drill"), b
        with driver.lock:
            theirs = x.crew.agents["captain"]
            ours = w.agents["officer of the watch"]
            assert WO.director_seats(w) == {}
            e = w.world_order("unseat: X, enough of her")
            assert e.data["result"] == "refused"
            assert "The director holds no seat on X." in e.text
            assert "was seated by the owner and not under a seat of the director's" in e.text
            e = w.world_order("unseat: officer, the watch is over")
            assert e.data["result"] == "refused"
            assert "it is not the director's to stand down, and keeps its station" in e.text
            assert not theirs.agent.released and not ours.agent.released
            # a seat under the grant on the same ship as the owner's: the seat's holder stood
            # down, the owner's captain kept, and the words say which
            e = w.world_order(f"seat: {WEIGHTS} as lookout of X for 3 samples")
            assert e.data["result"] == "done", e.text
    with DoorClient(app) as http:
        lk = http.post(
            "/api/agents/lookout", json={"model_name": WEIGHTS, "door": "mcp", "ship": "X"}
        ).json()
        assert lk["phase"] == "station", lk
        with driver.lock:
            lookout = x.crew.agents["lookout"]
            e = w.world_order("unseat: X, the lookout is done")
            assert e.data["result"] == "done" and "stood down" in e.text, e.text
            assert "was seated by the owner and not under a seat of the director's" in e.text
            assert lookout.agent.released and not theirs.agent.released
            # a seat under the grant, on another ship: given up, its holder stood down
            e = w.world_order(f"seat: {WEIGHTS} as captain of Nancy for 3 samples")
            assert e.data["result"] == "done", e.text
    with DoorClient(app) as http:
        n = http.post(
            "/api/agents/captain", json={"model_name": WEIGHTS, "door": "mcp", "ship": "Nancy"}
        ).json()
        assert n["phase"] == "station", n
        with driver.lock:
            nancy = w.vessels.find("Nancy").crew.agents["captain"]
            e = w.world_order("unseat: Nancy, the director has seen enough")
            assert e.data["result"] == "done" and "stood down" in e.text, e.text
            assert nancy.agent.released and not theirs.agent.released
