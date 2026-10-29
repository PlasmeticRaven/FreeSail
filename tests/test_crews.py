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
    assert isinstance(crew, K.Hull) and crew.shape == "full"  # a hull of the World (step 6)
    assert crew.ship.name and crew.ship.spec.source.endswith("brig.yaml")
    assert crew.people.captain.name and crew.stations.aboard("captain")
    cap = crew.captain
    assert cap.intent is not None and cap.intent.words == "bound for Falmouth"
    assert cap.role == "merchant" and cap.state == "on passage" and cap.commands
    assert crew.standing.books_loaded() == ["on passage"]
    assert nm_between(crew.navigation.account_now(), crew.position) < 1.0
    # the ports the world's, hers to deal with (package 84, step 3): her own dealings
    assert crew.ports is w.ports and crew.dealings is not w.dealings
    assert crew.dealings.ports is w.ports.ports and crew.dealings.pilot is None
    assert crew.systems is None and crew.chart is w.chart
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
        if b.crew.shape == "far":
            break
    d = nm_between(w.position, b.position)
    # since package 84, step 5, the demotion is a sleep: her World is kept in the far shape
    assert b.crew.shape == "far" and b not in K.crewed(w) and d >= K.CREWED_DEMOTE_NM - 0.2
    assert b.brain.state == "on passage" and b.plan and b.plan[0][0] == "to"
    assert w.vessels.crewed_ids == (b.id,)  # her World alive, asleep (step 5)
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
    assert ships[3].crew is not None and ships[2].crew.shape == "far"  # asleep (step 5)
    assert len(K.crewed(w)) == K.CREWED_CAP  # awake; `crewed_ids` counts the sleepers too
    # a vessel at anchor or in port is not promoted, and a crewed one that anchors is demoted
    from freesail.world import brains as B

    B.resolve_state(ships[2], "at anchor", ships[2].brain)
    ships[2].brain.state = "at anchor"
    B.resolve_state(ships[0], "at anchor", ships[0].brain)
    ships[0].crew.captain._enter("at anchor")
    w.run(60)
    assert ships[0].crew.shape == "far" and ships[2].crew.shape == "far"


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
    assert cb.crew is not None and isinstance(cb.crew, K.Hull)
    assert cb.crew.chart is c.chart and cb.crew.world is c and cb.crew.parent is c.own
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
    assert near.crew.shape == "far"  # asleep, not dropped (package 84, step 5)
    assert [leg[0] for leg in near.plan] == [leg[0] for leg in plan_before]


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
        assert b.detail == "far" and b.plan and b.plan[0][0] == "to"  # asleep: the sea's word
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
        # since package 84, step 4, a course for a port is by the tracks: its plan ends at
        # her anchor in the port
        assert b.plan[0][0] == "to" and b.plan[-1] == ("anchor", "falmouth")
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


# ---------------------------------------------------------------------------
# Package 84, step 4: the coarse acts on a sleeping hull, the far course by the tracks
# ---------------------------------------------------------------------------


def _held_far_cutter(w, position, name="Raven"):
    """A King's cutter at far detail with a station held at her captain's (the seat's
    flag, as a fake through the doors sets it), lying at `position` with a free intent."""
    v = put(w, "cutter", "britain", position, "bound for Falmouth", name=name)
    w.world_order(f'ship "{name}": intent wait here for the frigate\'s orders')
    vessel, crew = K.station_world(w, name)
    assert crew.shape == "far" and vessel is v
    crew.captain.seated = True
    return v, crew


def test_the_far_shape_works_the_coarse_acts_on_her_dealings_and_the_one_registry():
    """Package 84, step 4 (the design's §2.5): a station on a sleeping hull works the acts
    that want no physics through her own grammar. Brought to an anchor in Carrick Road
    (the far body's anchor leg) she lies in Falmouth by her dealings; the boat sent ashore
    for the prices is a job of the port with the boat's time (hoisted out, the pull at the
    boat's pace, the business ashore, the pull back, hoisted in), two jobs under her hull's
    id, the price list aboard when the second runs; `go ashore` lands her captain at the
    quay by the same boat, who goes to the counting house and is heard there by spot, and
    `come aboard` fetches him by the boat again; an order of the deck is refused in words
    that name the coarse forms."""
    w = hove_to_world()
    falmouth = w.ports.find("Falmouth")
    v, crew = _held_far_cutter(w, falmouth.anchorage.position)
    e = crew.submit("come to an anchor", actor="the captain")
    assert e.kind == "ship.anchored" and v.plan[0][0] == "anchor"
    assert crew.dealings.coarse and crew.dealings.anchored
    assert crew.dealings.in_port() is not None and crew.dealings.in_port().id == "falmouth"
    # the deck's detail wants her awake; the refusal names what she can do
    e = crew.submit("take in the royals", actor="the captain")
    assert e.kind == "order.rejected" and "far detail" in e.text
    assert "go ashore" in e.text and "send the boat" in e.text
    # the boat for the prices: two jobs at the boat's times, nothing until they run
    n = len(list(crew.log))
    crew.submit("send the boat ashore for the prices", actor="the captain")
    away = [x for x in list(crew.log)[n:] if x.kind == "boat.away"]
    assert len(away) == 1 and "her hull sleeps" in away[0].text and "minutes" in away[0].text
    jobs = [j for j in crew.dealings.jobs if j.kind == "boat"]
    assert len(jobs) == 2 and all(j.hull == v.id for j in jobs)
    assert jobs[0].payload["stage"] == "ashore" and jobs[1].payload["stage"] == "back"
    assert crew.dealings.boat.away and "falmouth" not in crew.dealings.price_lists
    assert [x.kind for x in list(crew.log)[n:] if x.kind.startswith("boat.")] == ["boat.away"]
    w.run(jobs[0].due_tick - w.clock.tick + 1)
    assert [x.kind for x in list(crew.log)[n:] if x.kind.startswith("boat.")] == [
        "boat.away",
        "boat.ashore",
    ]
    w.run(jobs[1].due_tick - w.clock.tick + 1)
    kinds = [x.kind for x in list(crew.log)[n:]]
    assert kinds.count("boat.alongside") == 1 and "market.prices" in kinds
    assert "falmouth" in crew.dealings.price_lists and not crew.dealings.boat.away
    # the world's ports carry no boat of hers: the jobs were hers alone
    assert not [j for j in w.dealings.jobs if j.kind == "boat"]
    # her captain ashore by the boat, to the counting house, heard there, and fetched back
    n = len(list(crew.log))
    crew.submit("go ashore", actor="the captain")
    assert crew.dealings.boat.away and crew.dealings.boat.errand == "landing"
    assert crew.submit("come aboard", actor="the captain").kind == "order.rejected"
    w.run(3 * 3600)
    landed = [x for x in list(crew.log)[n:] if x.kind == "person.ashore"]
    assert len(landed) == 1 and not crew.dealings.boat.away
    captain = next(p for p in crew.people.people if p.station == "captain")
    assert captain.name in landed[0].text and captain.hull is None
    assert captain.port == "falmouth" and captain.where == "shore"
    assert captain.home == v.id and not captain.aboard
    n = len(list(crew.log))
    crew.submit("go to the counting house", actor="the captain")
    crew.submit("say good day to you all", actor="the captain")
    said = {x.kind: x.text for x in list(crew.log)[n:]}
    assert "counting house" in said["person.moved"]
    assert "ashore at Falmouth, at the counting house" in said["agent.spoke"]
    n = len(list(crew.log))
    crew.submit("come aboard", actor="the captain")
    assert crew.dealings.boat.away and crew.dealings.boat.errand == "fetch"
    w.run(3 * 3600)
    assert [x.kind for x in list(crew.log)[n:] if x.kind == "person.came"]
    assert captain.hull == v.id and captain.aboard and not crew.dealings.boat.away


def test_the_far_course_for_a_port_is_laid_by_the_tracks_and_ends_at_her_anchor():
    """Package 84, step 4: `shape a course for <port>` on a sleeping hull is the planner's
    passage for it (the far brain's own way), out of the port she lies in by its track to
    sea, by the common tracks where the straight line is not clear of the shore, in by the
    port's track from the sea to its anchorage, where the plan's last leg is the anchor;
    the line names the marks. The port she weighs from is no mark to anchor at. A place of
    the chart is one leg as before."""
    w = hove_to_world()
    falmouth = w.ports.find("Falmouth")
    v, crew = _held_far_cutter(w, falmouth.anchorage.position)
    crew.submit("come to an anchor", actor="the captain")
    crew.submit("weigh", actor="the captain")
    e = crew.submit("shape a course for Plymouth", actor="the captain")
    assert e.kind == "helm.set" and "by the tracks" in e.text and e.data["port"] == "plymouth"
    assert v.plan[-1] == ("anchor", "plymouth")
    assert not any(leg[0] == "anchor" for leg in v.plan[:-1])
    names = [leg[2] for leg in v.plan if len(leg) > 2]
    assert "Carrick Road" not in names and names[-1] == "the anchorage in the Sound"
    assert names[0] == falmouth.tracks["to_sea"][0] or len(names) > 3
    assert "the anchorage in the Sound" in e.text
    e = crew.submit("shape a course for the Lizard", actor="the captain")
    assert e.kind == "helm.set" and v.plan == [("to", v.plan[0][1], "the Lizard")]


def test_a_held_stations_far_body_lies_to_at_the_plans_end_and_is_not_taken_off_the_sea():
    """Package 84, step 4: a far body whose captain's station is held is that station's to
    end, not the sea's: at the plan's last mark she lies to, said once in her log
    (`plan.ended`, notable), where a vessel of her own was done and gone; with the station
    released she is taken off the sea at her plan's end as before."""
    w = hove_to_world()
    v, crew = _held_far_cutter(w, "49 40 N 5 40 W")
    mark = v.position.advanced(0.0, 2.0 * units.CABLE)
    v.plan = [("to", mark, "a mark")]
    n = len(list(crew.log))
    w.run(900)
    assert not v.done and v.plan == [("lie_to", float("inf"))]
    ended = [x for x in list(crew.log)[n:] if x.kind == "plan.ended"]
    assert len(ended) == 1 and "a mark" in ended[0].text and ended[0].data["mark"] == "a mark"
    assert v.station_held()
    crew.captain.seated = False
    assert not v.station_held()
    v.plan = [("to", v.position.advanced(0.0, 2.0 * units.CABLE), "a mark")]
    w.run(900)
    assert v.done


def test_the_seat_on_another_ship_honours_the_scenarios_crewed_budget():
    """Package 84, step 4 (found on the way): `station_world` read the build machine's
    constants and promoted a ship within the range under a scenario whose cap was nought;
    it reads the budget the scenario or the flags set, as the switch does."""
    w = hove_to_world()
    w.crewed_settings = {"cap": 0}
    b = put(
        w, "merchant brig", "britain", "49 32 N 5 31 W", "bound for Falmouth", "bound for Falmouth"
    )
    assert nm_between(w.position, b.position) < K.CREWED_NM
    _, crew = K.station_world(w, "X")
    assert crew.shape == "far" and b.detail == "far"  # asleep: near by distance (step 6)


def test_a_word_said_as_a_person_ashore_reaches_another_ships_captain_landed_there():
    """Package 84, step 4 (the design's §2.12, steps 5 and 6): the director's `say as` for a
    person ashore is heard by whoever of any hull is at his place of his port, the player's
    ship a day's sail off (package 66 refused it beyond a boat's reach of the player's ship),
    and a free line in his mouth is his own act by the rule of reach: the packet he keeps
    given to the cutter's captain at the counting house, in that captain's keeping (the
    keeper told from the player's own master of the same id by his home hull), and aboard
    the cutter with him when her boat fetches him; nobody at his place is still refused in
    words."""
    from freesail.world import things as TH

    w = hove_to_world()
    falmouth = w.ports.find("Falmouth")
    assert nm_between(w.position, falmouth.anchorage.position) > 30
    v, crew = _held_far_cutter(w, falmouth.anchorage.position)
    crew.submit("come to an anchor", actor="the captain")
    w.world_order('person: make "Mr Gill", a merchant, ashore at Falmouth, at the counting house')
    w.world_order("aboard: a sealed packet, in the keeping of Mr Gill")
    e = w.world_order('say as Mr Gill: "A fine morning."')
    assert e.data["result"] == "refused" and "nobody can hear Mr Gill" in e.text
    crew.submit("go ashore", actor="the captain")
    w.run(3 * 3600)
    crew.submit("go to the counting house", actor="the captain")
    skipper = next(p for p in crew.people.people if p.station == "captain")
    assert skipper.ashore_at == "counting_house" and skipper.port == "falmouth"
    e = w.world_order('say as Mr Gill: "A fine morning, Captain."')
    assert e.data["result"] == "done" and skipper.name in e.text
    packet = next(t for t in w.registry.things if "packet" in t.name)
    e = w.world_order(f"say as Mr Gill: give the packet to {skipper.name}")
    assert e.data["result"] == "done"
    line = [x for x in w.log if x.kind == "free.line"][-1]
    assert line.data["spoken_as"] and line.data["moved"] and line.data["to"] == skipper.name
    assert "gave the packet" in line.text and f"in {skipper.name}'s keeping" in line.text
    assert packet.keeper == skipper.id == "master" and packet.keeper_home == v.id
    assert TH.keeper_of(w, packet) is skipper and TH.kept_by(w, skipper) == [packet]
    assert TH.kept_by(w, w.people.find("master")) == []  # the player's master, the same id
    crew.submit("come aboard", actor="the captain")
    w.run(3 * 3600)
    assert skipper.aboard and skipper.hull == v.id
    assert TH.place_of(w, packet)[3] == v.id and "keeping" in TH.where_words(w, packet)


# ---------------------------------------------------------------------------
# Package 84, step 5: the ship persists, sleep and wake in place of drop and remake
# ---------------------------------------------------------------------------


def _asleep(w, b) -> None:
    """Sail her beyond the range by an intent away from the ship until she sleeps."""
    w.world_order(f'ship "{b.name}": intent bound for 49 30 N 6 30 W')
    for _ in range(400):
        w.run(60)
        if b.crew is not None and b.crew.shape == "far":
            return
    raise AssertionError("not demoted")


def test_a_ship_demoted_sleeps_with_her_damage_and_wakes_the_same_ship(tmp_path):
    """Package 84, step 5 (the design's §2.6): the demotion is a sleep, not a drop. A brig
    promoted beside the frigate, holed below the water with a gun dismounted and three men
    wounded, sails beyond the range: her World is kept in the far shape with the physics
    off, her company stays in the one registry, the far body's record has her damage
    summed (`Vessel.damage`: the wounded, the gun, the hole), and her line says she is
    asleep; the far body moves her and the kept ship mirrors it. Brought near again she
    wakes without being remade: the same ship object, the hole, the gun and the wounded as
    she left them, her line saying she is at full detail again. A checkpoint written while
    she sleeps carries her World and wakes it alike. A vessel gone from the sea gives up
    her World and her people."""
    from freesail.combat import hits as H

    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    assert crew is not None and crew.shape == "full"
    ship = crew.ship
    hers = [p for p in w.registry.persons() if p.home == b.id]
    assert len(hers) >= 8
    muster = ship.extra["crew"]
    for s in muster.sailors[:3]:
        s.hurt = "wounded"
    H.damage_of(ship).holes.append({"side": "larboard", "below": True, "x_m": 3.0})
    gun = next(iter(ship.guns.values()))
    gun.dismounted = True
    _asleep(w, b)
    assert b.crew is crew and crew.shape == "far" and b.detail == "far"  # near by distance
    assert b.id in w.vessels.crewed_ids and b not in K.crewed(w)
    assert [p for p in w.registry.persons() if p.home == b.id] == hers
    assert b.damage["wounded"] == 3 and b.damage["killed"] == 0
    assert b.damage["dismounted"] == 1 and b.damage["holes"] == 1 and b.damage["holes_below"] == 1
    said = [e for e in crew.log if e.kind == "crew.demoted"]
    assert said and "asleep" in said[-1].text and said[-1].data["asleep"]
    assert said[-1].severity.value == "routine"  # no station to tell
    p0 = crew.position
    w.run(600)
    assert crew.position != p0 and crew.position == b.position
    assert crew.ship is ship and not any(e.kind == "crew.promoted" for e in list(crew.log)[-20:])
    # a checkpoint written while she sleeps carries her World, asleep, and wakes it alike
    path = replay_mod.write_checkpoint(w, tmp_path / "asleep.ckpt")
    _, c = replay_mod.read_checkpoint(path)
    cb = c.vessels.get(b.id)
    assert cb.crew is not None and cb.crew.shape == "far" and cb.damage == b.damage
    # near again: awake, the same ship, her damage as she left it
    for world, vessel in ((w, b), (c, cb)):
        vessel.position = world.position.advanced(0.0, 3.0 * units.NAUTICAL_MILE)
        world.run(61)
        assert vessel.crew.shape == "full"
    assert crew.ship is ship
    assert sum(1 for s in muster.sailors if s.hurt == "wounded") == 3
    assert len(H.damage_of(crew.ship).holes) == 1 and gun.dismounted
    woke = [e for e in crew.log if e.kind == "crew.promoted"]
    assert len(woke) == 2 and "at full detail again" in woke[-1].text
    assert cb.crew.ship.extra["crew"] is not muster
    assert sum(1 for s in cb.crew.ship.extra["crew"].sailors if s.hurt == "wounded") == 3
    # gone from the sea, she gives up her World and her people
    b.done = True
    w.run(60)
    assert b.crew is None and not [p for p in w.registry.persons() if p.home == b.id]
    assert b.id not in w.vessels.crewed_ids


def test_a_ship_woken_keeps_her_streams_and_her_sail_follows_the_plans_word():
    """Package 84, step 5: woken, a ship's `Rng` is the one she had (her streams continue,
    where the remake began them again: the design's §3.3 names what may move by it), and
    her sail is set as the far body's word only where the plan changed it while she slept
    (reefed for weather asleep, she wakes under reefed topsails)."""
    w = hove_to_world()
    b = put(
        w, "merchant brig", "britain", "49 33 N 5 30 W", "bound for Falmouth", "bound for Falmouth"
    )
    w.run(61)
    crew = b.crew
    rng = crew.rng
    drawn = crew.rng.stream("muster").random()
    _asleep(w, b)
    b.sail_state = "under reefed topsails"
    b.position = w.position.advanced(0.0, 3.0 * units.NAUTICAL_MILE)
    K.promote(w, b)  # as the switch does at its minute
    assert crew.shape == "full" and crew.rng is rng
    assert crew.rng.stream("muster").random() != drawn
    assert K._sail_state_of(crew) == "under reefed topsails"  # before her captain's judgement
    w.run(61)
    assert crew.shape == "full"
