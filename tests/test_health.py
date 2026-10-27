"""The muster's states, the surgeon, the sick list, the needs' ends and the station holder
hurt (spec M7 §16, §16a; package 73; `freesail/crew/health.py`; the design in
`docs/design/Design-WaterAndHealth.md`)."""

from __future__ import annotations

import random
from datetime import datetime

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.crew import health as H
from freesail.crew.model import Rating

CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"


def _scenario() -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=10.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        ports=["falmouth"],
        nation="britain",
        ship_heading_deg=180.0,
        ship_speed_kn=4.0,
    )


def _world(ship: str = FRIGATE, seed: int = 7):
    return make_world(seed, ship, _scenario())


def _events(world, kind: str) -> list:
    return [e for e in world.log if e.kind == kind]


def _hit(world, sailor, wound: str | None = None, killed: bool = False, how: str = "") -> None:
    """A man struck by the health keeper's hand, the wound forced light or grave so that
    the test reads the road it means."""
    world.health.hit(sailor, killed, random.Random(1), world.clock.tick, how=how)
    if wound is not None and not killed:
        sailor.wound = wound
        sailor.hurt_how = how or (
            "a splinter in the hand" if wound == "light" else "a splinter in the thigh"
        )


def _fit_men(world, n: int, trade: str | None = None) -> list:
    crew = world.ship.extra["crew"]
    out = [
        s
        for s in crew.sailors
        if s.fit
        and not s.hurt
        and s.trade != "surgeon's mate"
        and s.post is None
        and s.rating is not Rating.OFFICER
        and (trade is None or s.trade == trade)
        and not any(p.sailor_id == s.id for p in world.people.people)
    ]
    return out[:n]


# -- the states --------------------------------------------------------------------------------


def test_a_hit_kills_or_wounds_light_or_grave_with_the_wound_in_words():
    """§16: a man struck is killed, or wounded light or grave, the wound in the tables'
    words; off the bill at once (`fit` false, his station's post given up)."""
    w = _world(CUTTER)
    men = _fit_men(w, 12)
    rng = random.Random(3)
    for s in men:
        w.health.hit(s, rng.random() < 0.3, rng, w.clock.tick)
    states = {s.hurt for s in men}
    assert states <= {"killed", "wounded"} and "wounded" in states
    for s in men:
        assert not s.fit and s.at is None
        if s.hurt == "wounded":
            assert s.wound in ("light", "grave")
            table = H.GRAVE_WOUNDS if s.wound == "grave" else H.LIGHT_WOUNDS
            assert s.hurt_how in table
            assert not s.dressed
    assert any(s.hurt == "killed" for s in men)


def test_the_surgeon_takes_the_grave_himself_and_his_mates_the_light_in_their_times():
    """§16: the frigate's surgeon and two mates: the grave wound under the surgeon's hands
    for half an hour, the light under a mate's for ten minutes; the light man then 'hurt'
    and fit for light duty for a week or two, the grave one dressed and waiting his day."""
    w = _world(FRIGATE)
    men = _fit_men(w, 4)
    _hit(w, men[0], "grave")
    _hit(w, men[1], "light")
    _hit(w, men[2], "light")
    _hit(w, men[3], "light")
    w.run(60)
    st = w.health.state
    surgeon = w.health.surgeon()
    assert surgeon is not None and len(w.health.mates()) == 2
    assert st.at_work[surgeon.id][0] == men[0].id
    at_work = {pid for pid, _ in st.at_work.values()}
    assert men[1].id in at_work and men[2].id in at_work and men[3].id not in at_work
    w.run(H.DRESS_LIGHT_S + 60)
    assert men[1].hurt == "hurt" and men[1].fit and men[1].treated
    days = (men[1].hurt_until - w.clock.tick) / 86400.0
    assert H.HEAL_LIGHT_D[0] - 1 <= days <= H.HEAL_LIGHT_D[1]
    assert men[0].hurt == "wounded" and not men[0].dressed  # the surgeon's half hour not up
    w.run(H.DRESS_GRAVE_S)
    assert men[0].dressed and men[0].treated and men[0].hurt == "wounded"
    assert men[0].hurt_until is not None and men[0].hurt_until - w.clock.tick <= H.JUDGE_GRAVE_S
    assert men[3].hurt == "hurt"  # the third light man taken when a mate came free
    assert w.readings.words("surgeon").startswith("the surgeon, ")


def test_a_light_wound_heals_in_its_days_and_a_grave_one_is_judged_at_a_day():
    """§16: the light man returns to duty when his days are up, said in the log; the grave
    man at a day dies or is invalided, either said, and nothing else happens to him."""
    w = _world(FRIGATE)
    light, grave = _fit_men(w, 2)
    _hit(w, light, "light")
    _hit(w, grave, "grave")
    w.run(H.DRESS_GRAVE_S + 120)
    assert light.hurt == "hurt" and grave.dressed
    light.hurt_until = w.clock.tick + 120  # his days brought near, not waited for
    w.run(240)
    assert light.hurt == "" and light.fit and light.hurt_how == ""
    assert any(light.name in e.text for e in _events(w, "health.returned"))
    grave.hurt_until = w.clock.tick + 120
    w.run(240)
    died = [e for e in _events(w, "health.died") if grave.name in e.text]
    invalided = [e for e in _events(w, "health.invalided") if grave.name in e.text]
    assert bool(died) != bool(invalided)
    if died:
        assert grave.hurt == "killed" and "of his wound" in died[0].text
    else:
        assert grave.hurt == "wounded" and grave.wound == "invalid" and not grave.fit
        assert grave.hurt_until - w.clock.tick > 30 * 86400


def test_without_a_surgeon_the_messmates_dress_a_light_wound_in_an_hour_and_it_heals_slower():
    """§16: the cutter bears no surgeon; a light wound is dressed by the man's messmates in
    an hour, untreated, and takes half as long again to heal; the reading says so."""
    w = _world(CUTTER)
    assert w.health.surgeon() is None and not w.health.mates()
    (man,) = _fit_men(w, 1)
    _hit(w, man, "light")
    w.run(H.MESSMATES_DRESS_S - 600)
    assert man.hurt == "wounded" and not man.dressed
    w.run(720)
    assert man.hurt == "hurt" and man.dressed and not man.treated
    days = (man.hurt_until - w.clock.tick) / 86400.0
    assert days >= H.HEAL_LIGHT_D[0] * H.UNTREATED_HEAL_FACTOR - 1
    assert "no surgeon borne" in w.readings.words("surgeon")


# -- the sick list and the day -----------------------------------------------------------------


def test_foul_water_puts_men_on_the_sick_list_at_the_morning_report():
    """§16: the water found foul: the flux takes some men a day, said in the surgeon's
    report at eight, and the sick list names them with the cause."""
    w = _world(FRIGATE)
    w.stores.foul = True
    assert w.readings.words("sick_list") == "none"
    w.run(23 * 3600)  # past 08:00 of the next day
    sick = [e for e in _events(w, "health.sick")]
    assert sick and "the flux, from the foul water" in sick[0].text
    crew = w.ship.extra["crew"]
    ill = [s for s in crew.sailors if s.hurt == "sick"]
    assert ill and all(not s.fit for s in ill)
    words = w.readings.words("sick_list")
    assert ill[0].name in words and "sick" in words
    assert _events(w, "health.morning_report")
    assert "sick" in w.readings.words("bill")


def test_the_water_expended_kills_by_days_with_the_log_explaining_each_death():
    """§16: with the water and the provisions out, men sicken from the second day and die
    from the fourth, each death in the log with its cause; the captain at the prompt
    collapses at three days and dies at four, told in his line, and the command passes to
    the next by the bill."""
    w = _world(CUTTER)
    told: list = []
    w.needs.listen(told.append)
    w.stores.water_tons = 0.0
    w.stores.provisions_days = 0.0
    captain = w.people.captain
    w.run(5 * 24 * 3600)
    died = _events(w, "health.died")
    assert died and all("thirst" in e.text for e in died)
    assert any("the water being expended" in e.text for e in died)
    assert _events(w, "crew.buried")
    assert captain.dead
    assert any("collapsed with thirst" in e.text for e in told)
    assert any("You are dead of thirst" in e.text for e in told)
    assert any(
        "Mr Bowen is dead of thirst" in e.text or captain.name in e.text
        for e in _events(w, "person.killed")
    )
    passes = _events(w, "ship.command_passes")
    assert passes and w.people.captain is not captain
    assert w.people.captain.name in passes[0].text
    assert "dead" in w.people.state_words(captain)


def test_the_dead_are_buried_at_the_morning_report_and_not_in_action():
    """§16: the killed lie until the morning; at quarters nobody is buried; at eight the
    service is read, said in the log by name, and they are struck from the books but still
    counted in the bill's complement."""
    w = _world(FRIGATE)
    w.submit("beat to quarters")
    w.run(120)
    men = _fit_men(w, 3)
    for s in men:
        _hit(w, s, killed=True, how="a round shot")
    n = len(w.ship.extra["crew"].sailors)
    w.run(22 * 3600 + 60)  # past 08:00, still at quarters
    assert not _events(w, "crew.buried")
    assert "dead, to be buried" in w.readings.words("sick_list")
    w.submit("secure the guns")
    w.run(24 * 3600)
    buried = _events(w, "crew.buried")
    assert buried and all(s.name in buried[0].text for s in men)
    crew = w.ship.extra["crew"]
    assert len(crew.sailors) == n - 3 and len(crew.dead) == 3
    bill = w.readings.value("bill")
    assert bill["killed"] == 3 and bill["complement"] == n
    assert "three killed" in bill["words"]


def test_bury_the_dead_by_order_reads_the_service_at_once():
    """§16: `bury the dead` reads the service now, at quarters or not; refused in words when
    there is nobody to bury."""
    w = _world(CUTTER)
    out = w.submit("bury the dead")
    assert out.kind == "order.rejected" and "nobody to bury" in out.text
    (man,) = _fit_men(w, 1)
    _hit(w, man, killed=True, how="a musket ball")
    out = w.submit("bury the dead")
    assert out.kind != "order.refused", out.text
    w.run(1)
    buried = _events(w, "crew.buried")
    assert buried and man.name in buried[0].text


def test_the_butchers_bill_is_said_ten_minutes_after_the_last_shot():
    """§16: the butcher's bill in the log once, ten minutes after the last shot fired or
    struck, with the killed by name and the wounded counted, the dangerous apart; the bill
    reading counts the states as they stand."""
    from freesail.combat.hits import damage_of

    w = _world(FRIGATE)
    men = _fit_men(w, 4)
    _hit(w, men[0], killed=True, how="a round shot")
    _hit(w, men[1], "grave")
    _hit(w, men[2], "light")
    _hit(w, men[3], "light")
    keeper = damage_of(w.ship)
    keeper.hits = 3
    keeper.struck_by = {"enemy": w.clock.tick}
    w.run(H.BILL_AFTER_S - 120)
    assert not _events(w, "action.bill")
    w.run(240)
    bill = _events(w, "action.bill")
    assert len(bill) == 1
    assert men[0].name in bill[0].text and "three wounded, one of them dangerously" in bill[0].text
    w.run(3600)
    assert len(_events(w, "action.bill")) == 1  # said once
    words = w.readings.words("bill")
    assert "one killed" in words and "wounded (one dangerously)" in words
    assert "hurt and at light duty" in words


# -- the station holder hurt (§16a) -------------------------------------------------------------


def _officer_with_the_deck():
    from freesail.agents import Fake, Harness, SamplingPolicy, call, reply
    from freesail.agents.agent import officer

    world = _world(FRIGATE)
    world.run(60)
    script = [reply("", call("stand_by", until="a watch"))]
    oh = Harness(
        world,
        officer(SamplingPolicy.in_lockstep(600, "notable", "urgent"), world=world),
        Fake(script, when_done=reply("All well.")),
        save=lambda w, r: None,
    )
    oh.model_name, oh.door = "the fake officer", "mcp"
    oh.start()
    assert world.submit("you have the deck").kind == "agent.deck"
    person = next(p for p, h in world.needs.stationed() if h is oh)
    sailor = world.ship.extra["crew"].by_id[person.sailor_id]
    return world, oh, person, sailor


def test_a_holder_hit_lightly_is_told_his_roads_and_keeps_the_deck_or_goes_below():
    """§16a: the officer with the deck is hit: told in an urgent line of his own with his
    two roads, his orders going on; `go below to the surgeon` gives the deck, puts him in
    the cockpit and the surgeon's queue, and he is told when dressed."""
    w, oh, person, sailor = _officer_with_the_deck()
    _hit(w, sailor, "light")
    notice = [n for n in oh.agent.notices if "You are hit" in n]
    assert notice and "go below to the surgeon" in notice[0]
    assert oh.agent.deck and not person.dead
    assert "wounded" in w.people.state_words(person)
    out = w.health.go_below_to_the_surgeon(person, oh)
    assert "go below to the cockpit" in out
    assert person.where == "cockpit" and not oh.agent.deck
    assert sailor in w.health.waiting()
    w.run(60)
    assert "at work on the wounded" in w.readings.words("surgeon")
    w.run(H.DRESS_LIGHT_S + 120)
    assert sailor.hurt == "hurt"
    assert any("Your wound is dressed" in n for n in oh.agent.notices)


def test_a_holder_with_a_grave_wound_undressed_collapses_and_is_carried_below():
    """§16a: he keeps the deck with a grave wound; at the half hour he collapses, the
    station stands by as it does for a man asleep where he stood, the deck passes, the log
    says so; dressed, the stand-by ends."""
    from freesail.agents.harness import CARRIED_BELOW, WOUND_DRESSED

    w, oh, person, sailor = _officer_with_the_deck()
    _hit(w, sailor, "grave")
    assert any("collapse within the half hour" in n for n in oh.agent.notices)
    w.run(H.COLLAPSE_S + 120)
    assert oh.agent.standing_by and oh.agent.stand_by.words == CARRIED_BELOW
    assert person.where == "cockpit" and not oh.agent.deck
    collapsed = _events(w, "person.collapsed")
    assert collapsed and person.name in collapsed[0].text
    w.run(H.DRESS_GRAVE_S + 120)
    assert sailor.dressed and oh.agent.standing_by  # under the surgeon's hands until judged
    assert any("dangerous one" in n for n in oh.agent.notices)
    assert oh._stand_by_due != WOUND_DRESSED
    # the judgement at a day: dead or invalided, the station ends either way
    sailor.hurt_until = w.clock.tick + 120
    w.run(240)
    assert oh.agent.released
    stopped = _events(w, "agent.stopped")[-1].text
    assert "the world" in stopped and ("of his wound" in stopped or "invalided" in stopped)


def test_a_holder_killed_ends_his_station_and_the_captain_killed_passes_the_command():
    """§16a: the officer killed is stood down by the world with the reason, the station
    released and the log saying so; the captain at the prompt killed, the first lieutenant
    takes the command and the people say who commands."""
    w, oh, person, sailor = _officer_with_the_deck()
    _hit(w, sailor, killed=True, how="a round shot")
    assert person.dead and oh.agent.released
    stopped = _events(w, "agent.stopped")
    assert stopped and "killed: a round shot" in stopped[-1].text
    assert "the world" in stopped[-1].text
    killed = _events(w, "person.killed")
    assert killed and person.name in killed[0].text and "is killed: a round shot" in killed[0].text
    assert "dead" in w.people.state_words(person)
    # the captain at the prompt
    captain = w.people.captain
    cs = w.ship.extra["crew"].by_id[captain.sailor_id]
    _hit(w, cs, killed=True, how="a musket ball")
    assert captain.dead
    passes = _events(w, "ship.command_passes")
    assert passes and w.people.captain is not captain
    assert w.people.captain.role != "first lieutenant" or w.people.captain.name in passes[0].text
    assert not w.people.captain.dead
