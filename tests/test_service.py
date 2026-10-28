"""Whose service the ship is in (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §5; `freesail/world/service.py`): the four
sources in their order (the scenario's papers, the captain's role, the wardroom's binding
of the captain's station, a merchantman otherwise), the first action's King's cutter by
her role and her privateer by his, and nothing logged or drawn by the asking; the
Regulations binding a King's ship of Britain's alone, and the shipped merchant ship on the
frigate's file a merchantman by her papers (the review's finding)."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.world.captains import ROLES, _is_kings_ship
from freesail.world.service import (
    KINGS,
    MERCHANT,
    PRIVATEER,
    ROLE_SERVICE,
    service_of,
    under_the_regulations,
)

SEED = 7
CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
MERCHANT_BRIG = "data/ships/merchant-brig.yaml"
FIRST_ACTION = "data/scenarios/first-action.yaml"


def _scenario(**kw) -> Scenario:
    return Scenario(
        start_time=datetime(1805, 6, 12, 10, 0),
        wind_from_deg=270.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.8, "lon_deg": -5.3},
        region="channel-west",
        nation="britain",
        **kw,
    )


def test_the_papers_answer_first_over_the_role_and_the_wardroom():
    """`papers: {service: ...}` is read first, as the private signals' papers are: a
    frigate whose wardroom makes her a King's ship sails as a privateer or a merchantman
    when her papers say so, and a King's cutter on a cruise as a merchantman; a word the
    papers give that is no service gives nothing, and the next source answers."""
    w = make_world(SEED, FRIGATE, _scenario(papers={"service": "privateer"}))
    assert w.captain.role == "" and _is_kings_ship(w)
    assert service_of(w) == PRIVATEER
    w.scenario.papers["service"] = "Merchant"  # read at each asking, in any case
    assert service_of(w) == MERCHANT
    w.scenario.papers["service"] = "the moon"
    assert service_of(w) == KINGS  # no service: the wardroom answers
    cruise = "cruise off the Lizard within 10 miles"
    w = make_world(SEED, CUTTER, _scenario(intent=cruise, papers={"service": "merchant"}))
    assert w.captain.role == "kings-ship"
    assert service_of(w) == MERCHANT
    w.scenario.papers["service"] = "kings"
    assert service_of(w) == KINGS


def test_the_captains_role_answers_next_for_every_role():
    """Every role of the doctrine files has its service: a King's ship, a cruiser and a
    commodore the King's; a privateer a privateer's; a merchantman, a packet and a
    fisherman a merchant's. The role answers before the wardroom: the frigate with a
    merchant's role is a merchantman, and the merchant brig with a King's ship's role the
    King's."""
    assert set(ROLE_SERVICE) == set(ROLES)
    expected = {
        "kings-ship": KINGS,
        "cruiser": KINGS,
        "commodore": KINGS,
        "privateer": PRIVATEER,
        "merchant": MERCHANT,
        "packet": MERCHANT,
        "fisherman": MERCHANT,
    }
    w = make_world(SEED, FRIGATE, _scenario())
    for role, service in expected.items():
        w.captain.role = role
        assert service_of(w) == service, role
    w = make_world(SEED, MERCHANT_BRIG, _scenario())
    w.captain.role = "kings-ship"
    assert service_of(w) == KINGS


def test_the_wardroom_answers_when_the_captain_has_no_role_and_else_a_merchantman():
    """With no intent the captain has no role: the frigate's wardroom binds the captain's
    station to a captain, so she is the King's; the merchant brig's and the cutter's to a
    master (a merchantman, a hired cutter), so they are merchantmen; and a World with
    nothing to say is a merchantman."""
    for ship, service in ((FRIGATE, KINGS), (MERCHANT_BRIG, MERCHANT), (CUTTER, MERCHANT)):
        w = make_world(SEED, ship, _scenario())
        assert w.captain.role == "", ship
        assert service_of(w) == service, ship
    assert service_of(SimpleNamespace()) == MERCHANT
    assert service_of(SimpleNamespace(scenario=None, captain=None, ship=None)) == MERCHANT


def test_the_regulations_bind_a_kings_ship_of_britain_alone():
    """The Admiralty's Regulations (the necessity before buying stores, the allowance for
    exercise) bind a King's ship of Britain's: the frigate's wardroom makes a frigate of
    any nation a King's ship, and only the British one is bound; papers of another service
    bind nobody (the review's finding: an American ship on the frigate's file was refused
    at Falmouth under the British Regulations)."""
    w = make_world(SEED, FRIGATE, _scenario())
    assert service_of(w) == KINGS and under_the_regulations(w)
    for nation in ("united-states", "france", "portugal"):
        w.scenario.nation = nation
        assert service_of(w) == KINGS and not under_the_regulations(w), nation
    w.scenario.nation = "britain"
    w.scenario.papers = {"service": "merchant"}
    assert not under_the_regulations(w)
    w.scenario.papers = {"service": "privateer"}
    assert not under_the_regulations(w)
    assert under_the_regulations(SimpleNamespace()) is False


def test_the_merchant_ship_scenario_is_a_merchantman_by_her_papers():
    """data/scenarios/merchant-ship.yaml, "A merchant ship, free": an American on the
    Amazon's file, whose wardroom would make her a King's ship, is a merchantman by her
    papers, and the Regulations do not bind her (the review's finding: she was the
    King's)."""
    from freesail.world.scenarios import load_scenario, make_scenario_world

    sf = load_scenario("data/scenarios/merchant-ship.yaml")
    w = make_scenario_world(sf)
    assert w.dealings.ship_nation == "united-states" and _is_kings_ship(w)
    assert w.scenario.papers["service"] == "merchant"
    assert service_of(w) == MERCHANT and not under_the_regulations(w)


def test_the_first_actions_cutter_is_the_kings_and_the_renard_a_privateer():
    """The first action (data/scenarios/first-action.yaml): the Sherbourne's wardroom file
    is the cutter's (a master commands), and she is a King's ship by her captain's role on
    a cruise; the Renard, made a crewed ship, is a privateer by his. Asking logs nothing and
    opens no stream."""
    from freesail.world import crews
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    sf = load_scenario(FIRST_ACTION)
    w = make_scenario_world(sf)
    begin(w, sf)
    assert w.captain.role == "kings-ship" and not _is_kings_ship(w)
    lines, streams = len(w.log), list(w.rng.stream_names())
    assert service_of(w) == KINGS
    assert len(w.log) == lines and w.rng.stream_names() == streams
    v = w.vessels.find("Renard")
    assert v.brain.role == "privateer"
    crew = crews.promote(w, v)
    assert crew.captain.role == "privateer"
    lines, streams = len(crew.log), list(crew.rng.stream_names())
    assert service_of(crew) == PRIVATEER
    assert len(crew.log) == lines and crew.rng.stream_names() == streams
