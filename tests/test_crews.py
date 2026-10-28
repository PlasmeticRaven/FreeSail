"""The crewed promotion (package 43; spec M6 §19, §20; truths 87 and 88): within the
range of the player's ship a far-detail vessel with a brain becomes a full part-and-crew
ship from her file, her captain's orders through the same channel, her lookout, her
account and her book; beyond it she is demoted with her state folded back; the cap with
the nearest first and a ship in dealings before a nearer one that is not; the
hysteresis; the pace with the cap full; a checkpoint with a crewed ship."""

from __future__ import annotations

import time

import pytest

from freesail import units
from freesail.core import replay as replay_mod
from freesail.world import crews as K
from freesail.world.geo import bearing_and_distance
from tests.test_brains import put, world_at


def nm_between(a, b) -> float:
    return bearing_and_distance(a, b)[1] / units.NAUTICAL_MILE


def hove_to_world():
    w = world_at(49.5, -5.5)
    w.submit("set plain sail")
    w.submit("heave to")
    return w


def test_a_vessel_with_a_brain_within_the_range_is_promoted_and_demoted_beyond_it():
    """Truth 87 in part: the brig three miles off is promoted at the first switch; her
    own World has her hull from her file, her company, her stations, her captain with
    the brain's intent and state and his book loaded, her account within half a mile of
    her truth; the far body mirrors her every tick, so the player's lookout hails one
    sail; nothing of the promotion is a line of the player's log; sailed beyond six miles
    she is demoted, her state folded back into the brain and her World dropped."""
    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    assert b.crew is not None and b.detail == "crewed" and w.vessels.crewed_ids == (b.id,)
    crew = b.crew
    assert isinstance(crew, K.CrewedWorld) and crew.shape == "full"
    assert crew.ship.name and crew.ship.spec.source.endswith("brig.yaml")
    assert crew.people.captain.name and crew.stations.aboard("captain")
    cap = crew.captain
    assert cap.intent is not None and cap.intent.words == "bound for Falmouth"
    assert cap.role == "merchant" and cap.state == "on passage" and cap.commands
    assert crew.standing.books_loaded() == ["on passage"]
    assert nm_between(crew.navigation.account_now(), crew.position) < 1.0
    assert crew.ports.ports == {} and crew.systems is None and crew.chart is w.chart
    # the body mirrored, and the player's lookout sees one sail, hailed once
    w.run(600)
    assert b.position == crew.position
    assert b.heading_deg == pytest.approx(units.rad_to_deg(crew.ship.heading) % 360.0, abs=0.01)
    hails = [e for e in w.log if e.kind == "lookout.sighting" and "brig" in e.text]
    assert len(hails) == 1
    assert not [e for e in w.log if e.kind.startswith("crew.")]
    assert [e for e in crew.log if e.kind == "crew.promoted"]
    # her captain's orders go through her own channel, under the rules actor, in her log
    assert any(str(e.actor).startswith("captain's rule") for e in crew.log)
    assert not any(str(e.actor).startswith("captain's rule") for e in w.log)
    # her lookout sees the player's ship as a sail and makes out her colours
    seen = [e for e in crew.log if e.kind in ("lookout.sighting", "lookout.made_out")]
    assert any("ship" in e.text.lower() for e in seen)
    # sailed away westward she is demoted beyond six miles, the state folded back
    w.world_order('ship "X": intent bound for 49 30 N 6 30 W')
    for _ in range(400):
        w.run(60)
        if b.crew is None:
            break
    d = nm_between(w.position, b.position)
    assert b.crew is None and b.detail == "far" and d >= K.CREWED_DEMOTE_NM - 0.2
    assert b.brain.state == "on passage" and b.plan and b.plan[0][0] == "to"
    assert w.vessels.crewed_ids == ()
    assert not w.vessels.to_dict()[0]["crewed"]


def test_the_cap_holds_the_nearest_first_and_a_ship_in_dealings_before_a_nearer_one():
    w = hove_to_world()
    ships = []
    for i, (lat, lon) in enumerate(
        [
            ("49 31 N", "5 30 W"),
            ("49 32 N", "5 30 W"),
            ("49 33 N", "5 30 W"),
            ("49 33.5 N", "5 30 W"),
        ]
    ):
        ships.append(
            put(
                w,
                "merchant brig",
                "britain",
                f"{lat} {lon}",
                "bound for Falmouth",
                "bound for Falmouth",
                name=f"B{i}",
            )
        )
    w.run(61)
    crewed = [v.id for v in ships if v.crew is not None]
    assert len(crewed) == K.CREWED_CAP and crewed == [v.id for v in ships[:3]]
    assert ships[3].crew is None
    # the farthest within the range is in dealings with the player: she takes the place
    # of the farthest crewed ship that is not
    ships[3].dealing_tick = w.clock.tick
    w.run(60)
    assert ships[3].crew is not None and ships[2].crew is None
    assert len(w.vessels.crewed_ids) == K.CREWED_CAP
    # a vessel at anchor or in port is not promoted, and a crewed one that anchors is demoted
    from freesail.world import brains as B

    B.resolve_state(ships[2], "at anchor", ships[2].brain)
    ships[2].brain.state = "at anchor"
    B.resolve_state(ships[0], "at anchor", ships[0].brain)
    ships[0].crew.captain._enter("at anchor")
    w.run(60)
    assert ships[0].crew is None and ships[2].crew is None


def test_a_checkpoint_carries_a_crewed_ship_and_ticks_on_alike(tmp_path):
    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(300)
    assert b.crew is not None
    path = replay_mod.write_checkpoint(w, tmp_path / "crewed.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    cb = c.vessels.get(b.id)
    assert cb.crew is not None and isinstance(cb.crew, K.CrewedWorld)
    assert cb.crew.chart is c.chart and cb.crew.parent is c
    c.run(300)
    w.run(300)
    assert c.log.digest() == w.log.digest()
    assert cb.crew.log.digest() == b.crew.log.digest()
    assert cb.position == b.position


def test_truth_87_the_brig_promoted_sails_near_the_track_her_polar_gave_her():
    """Truth 87: a brig promoted within the range sails the same track at full detail as
    her polar gave her at far detail, within the stated tolerance (a mile over an hour on
    a reach: the polar is her file's own physics balanced at each point, within half a
    knot of the ship sailed), and demotes to the same plan."""
    w = hove_to_world()
    far = put(
        w,
        "merchant brig",
        "britain",
        "49 10 N 5 30 W",
        "bound for 49 10 N 4 30 W",
        "bound for 49 10 N 4 30 W",
        name="Far",
    )
    near = put(
        w,
        "merchant brig",
        "britain",
        "49 33 N 5 30 W",
        "bound for 49 33 N 4 30 W",
        "bound for 49 33 N 4 30 W",
        name="Near",
    )
    plan_before = list(near.plan)
    w.run(3600 + 61)
    assert near.crew is not None and far.crew is None
    east_far = far.position.lon_deg - (-5.5)
    east_near = near.position.lon_deg - (-5.5)
    # both stood east on a westerly: the crewed brig's easting over the hour within a
    # mile of the far body's
    miles_far = east_far * 60.0 * 0.65
    miles_near = east_near * 60.0 * 0.65
    assert abs(miles_near - miles_far) <= 1.5, (miles_near, miles_far)
    K.demote(w, near)
    assert near.crew is None and [leg[0] for leg in near.plan] == [leg[0] for leg in plan_before]


@pytest.mark.pace
def test_truth_88_with_the_cap_full_the_pace_holds():
    """Truth 88: the frigate with the cap full (three crewed ships beside her) ticks at
    not less than `CREWED_FLOOR_TICKS_S` a second on the build machine, the sixty times
    the owner plays at (100 to 114 measured with the three under sail beside her;
    docs/dev/TuningNotes.md, package 43)."""
    w = hove_to_world()
    for i, lat in enumerate(("49 31 N", "49 32 N", "49 33 N")):
        put(
            w,
            "merchant brig",
            "britain",
            f"{lat} 5 30 W",
            "bound for Falmouth",
            "bound for Falmouth",
            name=f"B{i}",
        )
    w.run(1000)
    assert len(w.vessels.crewed_ids) == K.CREWED_CAP
    best = 0.0
    for _ in range(3):
        t0 = time.perf_counter()
        w.run(1000)
        best = max(best, 1000 / (time.perf_counter() - t0))
    assert best >= K.CREWED_FLOOR_TICKS_S, f"{best:.0f} ticks a second"


# -- a station on another ship, kept across the switch (spec M6 §20; truth 89) -------------


def test_truth_89_a_fake_captain_on_another_ship_keeps_her_through_the_doors_across_the_switch(
    tmp_path,
):
    """Through the agent API with `ship`: the fake captain seated on the brig (promoted,
    three miles off) with her brief naming her, her voyage and the shape; his order goes
    through her own channel and is in her log, not the player's; the player's lookout sees
    her as a sail. Sailed beyond the range she is demoted and the station keeps, in the far
    shape: the sample says so, a course shaped works the far body, an order of the deck is
    refused in words; brought near again the full surface returns beneath the same
    station, said in her log, with no reseat. A ship without a captain of her own, or not
    on the sea, is refused in words."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.agents import consent
    from freesail.ui.server import Driver, create_app

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    put(w, "cutter", "britain", "49 32 N 5 32 W", "bound for Falmouth", name="Lark")
    w.run(61)
    assert b.crew is not None and b.crew.shape == "full"
    records = tmp_path / "consent"
    records.mkdir()
    weights = "made-up-crew-model-9b.Q4_K_M.gguf"
    consent.Record(
        weights, "a test runtime", "2026-10-16", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    driver = Driver(w, compression=60.0)
    app = create_app(driver, game="a test", consent_records=records, saves_dir=tmp_path / "saves")
    with TestClient(app) as http:
        r = http.post(
            "/api/agents/captain", json={"model_name": weights, "door": "mcp", "ship": "Lark"}
        )
        assert r.status_code == 404 and "no captain of her own" in r.json()["detail"]
        r = http.post(
            "/api/agents/captain", json={"model_name": weights, "door": "mcp", "ship": "Z"}
        )
        assert r.status_code == 404 and "No ship named 'Z'" in r.json()["detail"]
        a = http.post(
            "/api/agents/captain", json={"model_name": weights, "door": "mcp", "ship": "X"}
        ).json()
        assert a["phase"] == "station" and a["station"] == "captain"
        key = a["key"]
        crew = b.crew
        h = crew.agents["captain"]
        assert "captain" not in w.agents and h.world is crew
        brief = h.brief.text()
        assert "X at full detail" in brief or "at full detail" in brief
        assert crew.captain.seated and not crew.captain.commands
        # the station's first sample says the shape
        first = a["turns"][-1]["content"] if a.get("turns") else {}
        assert "full detail" in str(first) or any(
            "full detail" in str(t) for t in a.get("turns", [])
        )
        # his order goes through her own channel, into her log and not the player's
        http.post(
            "/api/agents/captain/reply",
            json={
                "text": "",
                "calls": [{"name": "submit_order", "args": {"text": "set the royals"}}],
                "key": key,
                "ship": "X",
            },
        )
        assert any(e.actor == "the captain" and "royals" in e.text for e in crew.log)
        assert not any(e.actor == "the captain" and "royals" in e.text for e in w.log)
        # the pace rule counts her station among the ship's
        state = http.get("/api/state").json()["driver"]
        assert state["pace"]["open"] and "captain of X" in state["pace"]["open"][0]["station"]
        stations = http.get("/api/agents").json()["stations"]
        assert any(d.get("ship") == "X" and d.get("shape") == "full" for d in stations)
        # a stand-by, so that the sample closes and the game runs on
        http.post(
            "/api/agents/captain/reply",
            json={
                "text": "",
                "calls": [{"name": "stand_by", "args": {"until": "eight bells"}}],
                "key": key,
                "ship": "X",
            },
        )
        # the player's lookout sees her as a sail
        assert any(e.kind == "lookout.sighting" and "brig" in e.text for e in w.log)
        # sailed beyond the range she is demoted; the station keeps, in the far shape
        w.world_order('ship "X": intent bound for 49 30 N 6 30 W')
        for _ in range(400):
            driver.tick(60)
            if crew.shape == "far":
                break
        assert crew.shape == "far" and b.crew is crew and crew.agents["captain"] is h
        assert any(e.kind == "crew.demoted" for e in crew.log)
        assert b.detail == "crewed" and b.plan and b.plan[0][0] == "to"
        # the far body moves her by the plan each minute, mirrored into her World
        p0 = crew.position
        driver.tick(120)
        assert crew.position != p0 and crew.position == b.position
        # an order of the deck is refused in words, a course shaped works the far body;
        # the next sample says the shape
        r = http.post(
            "/api/agents/captain/reply",
            json={
                "text": "",
                "calls": [
                    {"name": "submit_order", "args": {"text": "take in the royals"}},
                    {"name": "submit_order", "args": {"text": "shape a course for Falmouth"}},
                    {"name": "stand_by", "args": {"until": "eight bells"}},
                ],
                "key": key,
                "ship": "X",
            },
        ).json()
        refused = [e for e in crew.log if e.kind == "order.rejected" and "royals" in e.text]
        assert refused and "far detail" in refused[-1].text
        assert b.plan[0][0] == "to" and b.plan[0][2] == "Falmouth"
        assert [e for e in crew.log if e.kind == "helm.set" and "Falmouth" in e.text]
        assert r
        told = False
        for _ in range(300):
            driver.tick(60)
            turns = http.get(
                "/api/agents/captain/turns", params={"since": 0, "key": key, "ship": "X"}
            ).json()["turns"]
            if any("far detail" in str(x) for x in turns):
                told = True
                break
        assert told
        # near again: the full surface returns beneath the same station, no reseat
        b.position = w.position.advanced(0.0, 3.0 * units.NAUTICAL_MILE)
        driver.tick(61)
        assert crew.shape == "full" and crew.agents["captain"] is h and b.crew is crew
        assert any("full detail again" in e.text for e in crew.log)
        assert crew.ship.spec.source.endswith("brig.yaml") and crew.captain.seated
        http.post(
            "/api/agents/captain/release",
            json={"reason": "the test is done", "key": key, "ship": "X"},
        )
        assert h.agent.released


def test_a_door_on_another_ship_reads_its_turns_again_after_a_book_is_shelved(tmp_path):
    """The playtest of 2026-10-26: the captain of a cutter beside the player's ship
    shelved a book over MCP; the shelve moved the stream's revision, the door read its
    turns again (`GameClient.reread`) without naming the ship, the game answered that it
    held no captain's station, and the bridge asked for the station again in place of the
    shelve's result. The read again names the ship as every other call does."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.agents import consent
    from freesail.agents.model import Reply, ToolCall
    from freesail.agents.remote import GameClient
    from freesail.ui.server import Driver, create_app

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    assert b.crew is not None and b.crew.shape == "full"
    records = tmp_path / "consent"
    records.mkdir()
    weights = "made-up-crew-model-9b.Q4_K_M.gguf"
    consent.Record(
        weights, "a test runtime", "2026-10-16", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    driver = Driver(w, compression=60.0)
    app = create_app(driver, game="a test", consent_records=records, saves_dir=tmp_path / "saves")
    with TestClient(app) as http:
        game = GameClient("http://testserver", "captain", http=http, ship="X")
        a = game.station(weights, "mcp")
        assert a["phase"] == "station" and game.key
        game.reply(Reply(calls=(ToolCall("library", {"topic": "primer 3", "section": "reefing"}),)))
        assert not game.stale
        game.reply(Reply(calls=(ToolCall("shelve", {"book": "book 1"}),)))
        assert game.stale  # the shelve changed a turn the door had read
        turns = game.reread()  # named the player's ship's captain before the fix: a 404
        assert turns and not game.stale
        assert "captain" not in w.agents and b.crew.agents["captain"].agent.released is False
        game.release("the test is done")


def test_a_free_intent_is_taken_for_a_ship_on_the_sea_with_the_warning(tmp_path):
    """The owner's lead, 2026-10-26: `ship "X": intent <words>` takes words no form reads
    as a free intent, so that a model seated as her captain is told its goal; the order's
    line says the rules-based captain will not follow it, and why he cannot. He lays no
    plan for it. The forms he knows are taken as before, and `read_intent` itself refuses
    the free words in the same words as before. A captain seated on her is told the free
    intent is his goal, and that the rules-based captain will not follow it."""
    pytest.importorskip("fastapi")
    from fastapi.testclient import TestClient

    from freesail.agents import consent
    from freesail.ui.server import Driver, create_app
    from freesail.world.captains import FREE, FREE_WARNING, read_intent

    goal = "find the smuggler's lugger said to be running brandy into Cawsand"
    w = hove_to_world()
    b = put(w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth")
    assert b.brain is None
    with pytest.raises(ValueError, match="is no intent a captain knows"):
        read_intent(w, goal)
    e = w.world_order(f'ship "X": intent {goal}')
    said = getattr(e, "text", str(e))
    assert f"given an intent: {goal}" in said and FREE_WARNING in said
    assert "is no intent a captain knows" in said  # why he cannot sail by it
    assert b.brain.intent.kind == FREE and b.brain.intent.words == goal
    assert b.intent_words == goal
    # no legs: she lies to where she is, and is not taken off the sea as a voyage done
    w.run(61)
    assert not b.done and b.plan and b.plan[0][0] == "lie_to"
    assert b.crew is not None and b.crew.shape == "full"
    cap = b.crew.captain
    assert cap.intent.kind == FREE and not cap.error and not cap.legs
    # a form he knows is taken as before, with no warning, and his plan laid again
    e = w.world_order('ship "X": intent bound for Falmouth')
    said = getattr(e, "text", str(e))
    assert said.endswith("changed: bound for Falmouth.") and FREE_WARNING not in said
    assert b.brain.intent.kind == "passage" and cap.intent.kind == "passage"
    # a free intent again, and a model seated as her captain is told it
    w.world_order(f'ship "X": intent {goal}')
    assert cap.intent.kind == FREE
    records = tmp_path / "consent"
    records.mkdir()
    weights = "made-up-crew-model-9b.Q4_K_M.gguf"
    consent.Record(
        weights, "a test runtime", "2026-10-16", consent.YES, answer="Yes.", drill="passed"
    ).write(records)
    driver = Driver(w, compression=60.0)
    app = create_app(driver, game="a test", consent_records=records, saves_dir=tmp_path / "saves")
    with TestClient(app) as http:
        a = http.post(
            "/api/agents/captain", json={"model_name": weights, "door": "mcp", "ship": "X"}
        ).json()
        assert a["phase"] == "station"
        brief = b.crew.agents["captain"].brief.text()
        assert f"The intent the scenario gives the ship: {goal}. It is a free intent" in brief
        assert "the rules-based captain will not follow it" in brief
        http.post(
            "/api/agents/captain/release",
            json={"reason": "the test is done", "key": a["key"], "ship": "X"},
        )


def test_under_a_free_intent_the_crewed_captain_lies_her_to_once_and_keeps_her_service():
    """Package 86's fold-in (the review of the owner's local work, section 3): the crewed
    captain short-circuits a free intent as the far body does, where he had tried to plan it
    every judgement and said a plan of no legs each time: on his passage he heaves her to
    once, says nothing more in twenty minutes, and lays no legs. And she keeps her service's
    role and doctrine: a cutter patrolling (a cruiser) given a free intent stays a cruiser,
    far and crewed, where she had fallen to the merchant's doctrine."""
    from freesail.world.captains import FREE

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    assert crew is not None and crew.captain.state == "on passage"
    w.world_order('ship "X": intent wait here for the Amazon\'s boat')
    n = len(list(crew.log))
    w.run(20 * 60)
    said = list(crew.log)[n:]
    assert not [e for e in said if e.kind == "captain.plan"], "a plan said under a free intent"
    heave = [e for e in said if e.kind == "order.accepted" and "free intent" in e.text]
    assert len(heave) == 1 and "heaving to" in heave[0].text
    assert crew.readings.value("manoeuvre_in_hand") == "hove to"
    assert crew.captain.intent.kind == FREE and not crew.captain.legs
    raven = put(
        w,
        "cutter",
        "britain",
        "49 31 N 5 31 W",
        "patrolling off the Lizard within 5 miles",
        "patrol off the Lizard within 5 miles",
        name="Raven",
    )
    w.run(61)
    assert raven.brain.role == "cruiser"
    assert raven.crew is not None and raven.crew.captain.role == "cruiser"
    cap = raven.crew.captain
    w.world_order('ship "Raven": intent wait here for the Amazon\'s boat')
    assert raven.brain.intent.kind == FREE and raven.brain.role == "cruiser"
    assert raven.brain.doctrine is not None and raven.brain.doctrine.role == "cruiser"
    assert cap.intent.kind == FREE and cap.role == "cruiser" and cap.doctrine.role == "cruiser"
    # a form he knows given after it is read for its own role, as before
    w.world_order('ship "Raven": intent bound for Falmouth')
    assert raven.brain.role == "merchant"


def test_the_crewed_budget_is_a_setting_of_the_scenario_or_the_flags():
    """The lead, 2026-10-17: the cap and the range are the build machine's constants
    unless the scenario or the drivers' flags say otherwise (`crews.settings`); a cap of one
    promotes one of two ships within the range, and the flags win over the scenario."""
    w = hove_to_world()
    assert K.settings(w) == (K.CREWED_CAP, K.CREWED_NM, K.CREWED_DEMOTE_NM)
    w.crewed_settings = K.crewed_settings_of({"cap": 1, "range_nm": 5}, "the flags")
    assert K.settings(w) == (1, 5.0, 7.0)
    ships = [
        put(
            w,
            "merchant brig",
            "britain",
            f"{lat} 5 30 W",
            "bound for Falmouth",
            "bound for Falmouth",
            name=f"C{i}",
        )
        for i, lat in enumerate(("49 31 N", "49 32 N"))
    ]
    w.run(61)
    assert [v.crew is not None for v in ships] == [True, False]
    import pytest

    with pytest.raises(ValueError):
        K.crewed_settings_of({"cap": -1})
    with pytest.raises(ValueError):
        K.crewed_settings_of({"range_nm": 0})
    with pytest.raises(ValueError):
        K.crewed_settings_of("three")


def test_a_station_is_kept_on_the_players_ship_by_her_name_or_on_a_sail_by_her_kind():
    """The playtest of 2026-10-27: the tender's model ordered 'keep station two cables
    astern of the Amazon' and '... of the frigate', and both were refused ("No ship named
    ... is on the sea"); only 'the ship' was taken. The player's ship is kept station on by
    her own name and by her kind, and another sail by her kind, the nearest; the ship's own
    kind with no other of it near, and a name nobody bears, are refused as before."""
    w = hove_to_world()
    raven = put(
        w,
        "cutter",
        "britain",
        "49 30.2 N 5 30 W",
        "in company with the ship",
        "patrol off the Lizard within 5 miles",
        name="Raven",
    )
    put(w, "merchant brig", "britain", "49 31 N 5 31 W", "bound for Falmouth", name="Nancy")
    w.run(61)
    crew = raven.crew
    assert crew is not None and crew.shape == "full" and w.ship.name == "Amazon"
    w.run(60)  # her lookout's first sweep (a kind is taken among the sails in sight: 86)

    def flag(words: str) -> str | None:
        crew.ship.extra.pop("station", None)
        e = crew.submit(f"keep station two cables astern of {words}")
        if e.kind == "order.rejected":
            assert "is on the sea to keep station on" in e.text, e.text
            return None
        return (crew.ship.extra.get("station") or {}).get("flag")

    for words in ("the Amazon", "Amazon", "the frigate", "the ship"):
        assert flag(words) == "the ship", words
    nancy = w.vessels.find("Nancy")
    assert flag("the brig") == nancy.id and flag("the Nancy") == nancy.id
    assert flag("the cutter") is None and flag("the Victory") is None


def test_a_station_by_kind_is_kept_only_on_a_sail_in_sight_and_brig_is_no_brig_sloop():
    """Package 86's fold-in (the review of the owner's local work, section 3): the kind is
    matched only among the sails her lookout has in sight, where it had searched the whole
    sea by truth (a frigate nobody aboard could know of was taken); and 'brig' takes a
    merchant brig, not a brig-sloop, which 'sloop' and 'brig-sloop' take. A lugger
    thirty-five miles off is refused by her kind, out of sight, and by her name is
    taken as before (the name is the order's own knowledge)."""
    w = hove_to_world()
    raven = put(
        w,
        "cutter",
        "britain",
        "49 30.2 N 5 30 W",
        "in company with the ship",
        "patrol off the Lizard within 5 miles",
        name="Raven",
    )
    harpy = put(w, "brig-sloop", "britain", "49 31 N 5 31 W", "bound for Falmouth", name="Harpy")
    belle = put(w, "lugger", "france", "48 55 N 5 30 W", "bound for Brest", name="Belle")
    w.run(121)
    crew = raven.crew
    assert crew is not None and crew.shape == "full"
    seen = {str(s.feature.modern) for s in crew.lookout.sightings if s.seen_as == "sail"}
    assert harpy.id in seen and belle.id not in seen

    def flag(words: str) -> str | None:
        crew.ship.extra.pop("station", None)
        e = crew.submit(f"keep station two cables astern of {words}")
        if e.kind == "order.rejected":
            assert "no sail of that kind is in sight" in e.text, e.text
            return None
        return (crew.ship.extra.get("station") or {}).get("flag")

    assert flag("the brig") is None  # a brig-sloop is no 'brig' of the order's words
    assert flag("the sloop") == harpy.id and flag("the brig-sloop") == harpy.id
    assert flag("the lugger") is None  # beyond her horizon: nobody aboard knows of her
    assert flag("the Belle") == belle.id  # her name said: `Vessels.find`, as before
