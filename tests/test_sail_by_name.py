"""Package 95 (docs/design/Design-SailByName.md): the sail by her name.

One resolver for a sail named in words (`world.lookout.Lookout.sail_named`), read as the
lookout's own line backwards: a name the deck knows over all; the kind by the words made out
of her, the quarter, the bearing and the distance, each narrowing the sails in sight; the
closer where more than one remains. Used by `make her out`, `the glass on`, `hail the`, `the
bearing of`, `give chase`, `pull for` and `send the boat to the <ship>`. Truths 7-395 to
7-397 and 7-399 are in tests/test_known_truths.py, calling here.
"""

from __future__ import annotations

import math

from freesail.world.geo import destination
from freesail.world.lookout import read_sail_words
from freesail.world.ships import vessel_from_spec
from tests.test_known_truths import _gerrans_world

# Three sails about the frigate off the Lizard, all lying to, in daylight: two brig-sloops
# of war and a merchant brig, and a fourth brig-sloop far on the bow (the bearing, the
# distance and the nearest-of-kind rule each pick another sail).
NEAR = (
    # id, name, description, nation, bearing (true), miles
    ("swift", "Swift", "brig-sloop", "britain", 200.0, 0.30),
    ("raven", "Raven", "brig-sloop", "france", 45.0, 0.36),
    ("nancy", "Nancy", "merchant brig", "britain", 115.0, 0.25),
    ("wasp", "Wasp", "brig-sloop", "britain", 47.0, 1.9),
)


def sails_about(sails=NEAR, hour: int = 11, settle_s: int = 120):
    """The frigate (heading north, lying to by the scenario) with the sails placed about
    her by true bearing and miles, made out by the tops as the distance allows."""
    world = _gerrans_world(ship="data/ships/frigate-36.yaml", lat=49.80, lon=-5.0, hour=hour)
    for vid, name, description, nation, bearing, nm in sails:
        world.vessels.serial += 1
        v = vessel_from_spec(
            world,
            {
                "id": vid,
                "description": description,
                "name": name,
                "nation": nation,
                "position": destination(world.position, bearing, nm * 1852.0).to_dict(),
                "goal": "bound for 49 48 N 4 30 W",
            },
            world.vessels.serial,
        )
        v.plan = [("lie_to", math.inf)]
        world.vessels.add(v)
    world.run(settle_s)
    return world


def _id_of(world, e) -> str:
    return str(e.data.get("id") or "")


def _relative(world, vid: str) -> str:
    """The lookout's words for where a sail lies from the head, as `the strangers` say."""
    for item in world.readings["strangers"]["items"]:
        if item["id"] == vid:
            return item["relative"]
    raise AssertionError(f"{vid} not in sight")


def _point(world, vid: str) -> str:
    for item in world.readings["strangers"]["items"]:
        if item["id"] == vid:
            return item["bearing"]
    raise AssertionError(f"{vid} not in sight")


# ---------------------------------------------------------------------------
# The words read
# ---------------------------------------------------------------------------


def test_the_lookouts_line_is_read_back_into_its_clauses_commas_or_none():
    said = read_sail_words("the brig on the larboard quarter, bearing NE by N, distant a mile")
    assert said is not None
    assert said.name == "brig" and said.kind == ("brig",)
    assert said.quarter == ("quarter", "larboard")
    assert abs(said.bearing_deg - 33.75) < 1e-9
    assert abs(said.distance_m - 1852.0) < 1e-9
    same = read_sail_words("brig on the larboard quarter bearing ne by n distant a mile")
    assert same == said
    loose = read_sail_words("the sail bearing NE, four cables off, right ahead")
    assert loose.name == "" and loose.kind == () and loose.quarter == ("ahead", None)
    assert abs(loose.bearing_deg - 45.0) < 1e-9 and abs(loose.distance_m - 4 * 185.2) < 1e-9
    beam = read_sail_words("the schooner abeam to port")
    assert beam.kind == ("schooner",) and beam.quarter == ("beam", "larboard")
    war = read_sail_words("the French man-of-war distant two leagues")
    assert war.kind == ("french", "war") and abs(war.distance_m - 6 * 1852.0) < 1e-9
    assert read_sail_words("the Raven").name == "raven"


# ---------------------------------------------------------------------------
# Truth 7-395: the narrowing, four cases
# ---------------------------------------------------------------------------


def test_the_kind_by_the_words_made_out_picks_her_over_a_nearer_sail():
    """The kind: 'the brig-sloop' is no rig word of the old reading (refused before); every
    word of it among the words made out of her, the nearer merchant brig left aside."""
    world = sails_about()
    assert _relative(world, "nancy") and _relative(world, "swift")
    e = world.submit("the glass on the brig-sloop")
    assert e.kind == "lookout.glass", e.text
    assert _id_of(world, e) == "swift"  # the nearer brig-sloop, not the nearest sail (nancy)
    e = world.submit("make out the merchant brig")
    assert e.kind == "lookout.made_out" and _id_of(world, e) == "nancy", e.text


def test_the_kind_and_the_quarter_pick_the_farther_of_two_alike():
    """The kind and the quarter: of the two brig-sloops near, the one on the starboard bow,
    the farther, where 'make out the brig' gives the nearer."""
    world = sails_about()
    assert _relative(world, "raven") == "on the starboard bow"
    plain = world.submit("make out the brig")
    assert _id_of(world, plain) == "nancy" or _id_of(world, plain) == "swift"
    e = world.submit("make out the brig on the starboard bow")
    assert e.kind == "lookout.made_out" and _id_of(world, e) == "raven", e.text
    h = world.submit("hail the brig on the starboard bow: what ship is that?")
    assert h.kind in ("hail.made", "hail.answered") and h.data["id"] == "raven", h.text
    h = world.submit("hail the brig on the starboard bow what ship is that")
    assert h.data["id"] == "raven" and h.data["words"] == "what ship is that", h.text


def test_the_quarter_and_the_bearing_name_a_sail_with_no_kind_said():
    """The quarter and the bearing: 'the sail on the starboard quarter, bearing ESE' is the
    merchant brig; the bearing of her by the same words."""
    world = sails_about()
    point = _point(world, "nancy")
    where = _relative(world, "nancy")
    e = world.submit(f"make out the sail {where}, bearing {point}")
    assert e.kind == "lookout.made_out" and _id_of(world, e) == "nancy", e.text
    b = world.readings.value("bearing_of", f"the sail {where} bearing {point}")
    assert b is not None
    assert (
        abs(
            math.degrees(b)
            - next(
                i["bearing_deg"] for i in world.readings["strangers"]["items"] if i["id"] == "nancy"
            )
        )
        < 15.0
    )


def test_the_bearing_and_the_distance_pick_the_far_sail_on_the_same_bearing():
    """The bearing and the distance: the Raven and the Wasp bear NE, at a third of a mile and
    at two miles; 'distant two miles' is the Wasp, 'distant four cables' the Raven, and the
    glass, the bearing and the chase take the same words."""
    world = sails_about()
    assert _point(world, "raven") == _point(world, "wasp") == "NE"
    far = world.submit("the glass on the sail bearing NE distant two miles")
    assert far.kind == "lookout.glass" and _id_of(world, far) == "wasp", far.text
    near = world.submit("make out the sail bearing NE, distant four cables")
    assert _id_of(world, near) == "raven", near.text
    chase = world.submit("give chase to the brig bearing NE distant two miles")
    assert chase.kind == "helm.set" and "bearing NE" in chase.text, chase.text
    assert world.ship.extra.get("chase", {}).get("id", "wasp") in ("wasp", "sail:wasp")


# ---------------------------------------------------------------------------
# Truth 7-396: the closer where ambiguity remains; none refused with the strangers
# ---------------------------------------------------------------------------


def test_two_sails_answering_alike_give_the_closer_and_none_is_refused_with_the_strangers():
    world = sails_about()
    # both brig-sloops on the bow answer 'the brig-sloop bearing NE': the Raven, the closer
    e = world.submit("make out the brig-sloop bearing NE")
    assert _id_of(world, e) == "raven", e.text
    # a clause that leaves no sail is refused, the strangers' own words given
    e = world.submit("make out the brig right astern")
    assert e.kind == "order.rejected", e.text
    assert "Nothing in sight answers to 'the brig right astern'; the strangers: " in e.text
    assert "a brig-sloop of war on the starboard bow, bearing NE" in e.text
    e = world.submit("hail the sail bearing W: what ship is that?")
    assert e.kind == "order.rejected", e.text


# ---------------------------------------------------------------------------
# Truth 7-397: a name over all
# ---------------------------------------------------------------------------


def test_a_name_over_all_against_a_nearer_sail_of_the_same_kind_and_bearing():
    """The Wasp, two miles off on the Raven's bearing, by her name: the glass, the bearing
    and make out take her though the Raven is nearer, of the same kind and quarter, and
    though the words that follow her name would give the Raven."""
    world = sails_about()
    e = world.submit("the glass on the Wasp")
    assert e.kind == "lookout.glass" and _id_of(world, e) == "wasp", e.text
    e = world.submit("make out the Wasp on the starboard bow distant four cables")
    assert _id_of(world, e) == "wasp", e.text
    assert world.readings.value("bearing_of", "the Wasp") is not None


# ---------------------------------------------------------------------------
# The boat: `pull for` and `send the boat to the <ship>` by the lookout's words
# ---------------------------------------------------------------------------


def two_brigs_by():
    """The frigate hove to; the merchant brigs Lynx a third of a mile east and Nancy a third
    of a mile west, each hove to with a captain of her own (82b's three hulls' form)."""
    from tests.test_crews import hove_to_world

    w = hove_to_world()
    for words in (
        'ship: a merchant brig "Lynx" of Britain at 49 30 N 5 29.5 W, bound for Falmouth',
        'ship "Lynx": intent bound for Falmouth',
        'ship "Lynx": order heave to for a watch',
        'ship: a merchant brig "Nancy" of Britain at 49 30 N 5 30.5 W, bound for Falmouth',
        'ship "Nancy": intent bound for Falmouth',
        'ship "Nancy": order heave to for a watch',
    ):
        e = w.world_order(words)
        assert e.data.get("result") == "done", e.text
    w.run(61)
    return w


def _bearing_of_sail(w, name: str) -> str:
    vid = w.vessels.find(name).id
    return next(i["bearing"] for i in w.readings["strangers"]["items"] if i["id"] == vid)


def test_the_boat_is_sent_to_a_sail_named_as_the_lookout_names_her_and_the_refusal_says_how():
    w = two_brigs_by()
    assert _bearing_of_sail(w, "Lynx") == "E" and _bearing_of_sail(w, "Nancy") == "W"
    # the refusal at sea names the form for a sail within a boat's pull
    e = w.submit("send the boat ashore")
    assert e.kind == "order.rejected", e.text
    assert "'send the boat to the <ship> with <persons>'" in e.text, e.text
    # the boat sent to the brig bearing E by the lookout's words, not by her name
    w.people.find("the captain")  # the company mustered
    master = next(p for p in w.own.people.people if p.id == "master")
    e = w.submit(f"send the boat to the brig bearing E with {master.name}")
    assert e.kind in ("evolution.started", "order.accepted"), e.text
    assert w.dealings.boat.away, e.text
    started = [x for x in w.log if "alongside her in some" in x.text]
    assert started and "Lynx" in started[-1].text, [x.text for x in w.log[-3:]]


def test_the_manned_boat_pulls_for_the_sail_by_the_lookouts_words():
    w = two_brigs_by()
    assert w.submit("go to the launch").kind == "person.aboard"
    e = w.submit("pull for the brig bearing W")
    assert e.kind == "boat.oars" and "Nancy" in e.text, e.text
    e = w.submit("pull for the brig bearing N")
    assert e.kind == "order.rejected" and "as the lookout names her" in e.text, e.text


# ---------------------------------------------------------------------------
# The lookout's hail of the pilot's cutter (the brig off Falmouth's lesson 2)
# ---------------------------------------------------------------------------


def test_the_lookouts_hail_of_the_pilots_cutter_is_his_hail_not_the_ports_verb():
    from freesail.agents import Reply
    from freesail.orders import stations
    from tests.test_wardroom_doors import EVERY, LOOKOUT, off_the_lizard, order, seated

    world = off_the_lizard()
    seated(
        world, LOOKOUT, [order("hail The pilot's cutter is out of sight to the westward"), Reply()]
    )
    world.run(EVERY)
    hails = [e for e in world.log if e.kind == "agent.hail"]
    assert hails and hails[0].text == (
        "The lookout, from the masthead: The pilot's cutter is out of sight to the westward"
    )
    assert not [e for e in world.log if e.kind in ("agent.refused", "order.rejected")]
    # the port's verb keeps its own words whole
    for words in ("hail the pilot", "hail the pilot's cutter", "hail for a pilot"):
        assert stations.recognises(words) is None, words
    # and the captain's `hail the pilot` at the prompt is the port's, as on the trunk
    e = off_the_lizard().submit("hail the pilot")
    assert e.kind == "order.rejected" and "There is no pilot to hail" in e.text, e.text


# ---------------------------------------------------------------------------
# Truth 7-399: the recorded passages unmoved (a proof by toggle)
# ---------------------------------------------------------------------------

# The kinds of line in which a sail is named: the lookout's, the hail's, the signals', the
# chase's helm, and every order given or refused.
NAMING_KINDS = ("lookout.", "hail.", "signal.", "helm.set", "order.", "agent.")


def _passage(path: str, minutes: int, on: bool) -> tuple[dict[str, int], list[str]]:
    """The scenario at `path` played `minutes` by its rules captains with the resolver on or
    off: the count of the log's lines by kind, and the texts of the lines that name a sail."""
    from freesail.world import lookout as L
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    was = L.SAIL_BY_NAME
    L.SAIL_BY_NAME = on
    try:
        sf = load_scenario(path)
        w = make_scenario_world(sf)
        begin(w, sf)
        for _ in range(minutes):
            w.run(60)
    finally:
        L.SAIL_BY_NAME = was
    counts: dict[str, int] = {}
    for e in w.log:
        counts[e.kind] = counts.get(e.kind, 0) + 1
    named = [f"{e.tick} {e.kind} {e.text}" for e in w.log if e.kind.startswith(NAMING_KINDS)]
    return counts, named


RECORDED = (
    # the encounter's chase after the private signal (truth 7-144), the convoy's escort and
    # her charges (7-145), the first action to its strike (7-139's ground)
    ("data/scenarios/encounter.yaml", 45),
    ("data/scenarios/convoy.yaml", 40),
    ("data/scenarios/first-action.yaml", 60),
)


def recorded_passages_name_their_sails_as_before() -> None:
    """Every line of the recorded passages that names a sail (the lookout's, the hail's, the
    signals', the chase's helm, the orders given and refused) and every count of the log's
    lines by kind is the same with the resolver on as with it off; and each passage has
    sails named in it, so that the proof is not empty. Run by truth 7-399 alone (a minute:
    six passages played)."""
    for path, minutes in RECORDED:
        on_counts, on_named = _passage(path, minutes, on=True)
        off_counts, off_named = _passage(path, minutes, on=False)
        assert on_counts == off_counts, path
        assert on_named == off_named, path
        assert sum(1 for t in on_named if " lookout." in t) >= 1, path


# ---------------------------------------------------------------------------
# Truth 7-398: the identified sail named in the rows, and forgotten when lost
# ---------------------------------------------------------------------------


def _item(world, vid: str) -> dict:
    return next(i for i in world.readings["strangers"]["items"] if i["id"] == vid)


def _move(world, vid: str, bearing: float, nm: float) -> None:
    v = world.vessels.get(vid)
    v.position = destination(world.position, bearing, nm * 1852.0)


def test_a_sail_hailed_and_answered_is_named_in_the_rows_and_forgotten_when_lost():
    """The Raven and the Swift read alike ("a brig-sloop of war") until the Raven answers
    the hail with her name: then `the strangers`, `what is in sight` and `a sail in sight`
    name her, the Swift still a brig-sloop of war, and the strangers' item carries her
    name. Lost sight of, her name goes with her; closed and made out again, she is a
    brig-sloop of war until she is spoken again. The lookout's lines are his as before."""
    world = sails_about()
    raven, swift = _item(world, "raven"), _item(world, "swift")
    assert raven["name"] is None and swift["name"] is None
    assert raven["words"].startswith("a brig-sloop of war")
    assert swift["words"].startswith("a brig-sloop of war")
    e = world.submit("hail the brig bearing NE distant two cables: what ship is that?")
    assert e.kind == "hail.answered" and "Raven" in e.data["answer"], e.text
    world.run(60)  # the next look
    raven, swift = _item(world, "raven"), _item(world, "swift")
    assert raven["name"] == "Raven" and raven["words"].startswith("the Raven, a brig-sloop of war")
    assert swift["name"] is None and swift["words"].startswith("a brig-sloop of war")
    assert "Sail ho! The Raven, a brig-sloop of war" in world.readings["in_sight"]["words"]
    near = world.readings["sail_in_sight"]
    assert any(i["words"].startswith("the Raven, ") for i in near["items"])
    # her name is the deck's to name her by now
    assert _id_of(world, world.submit("make out the Raven")) == "raven"
    # the lookout's own lines are as they were: no name in them
    assert not [x for x in world.log if x.kind.startswith("lookout.") and "Raven" in x.text]
    # lost sight of: twenty-five miles off, beyond the horizon
    _move(world, "raven", 45.0, 25.0)
    world.run(60)
    assert "raven" not in {i["id"] for i in world.readings["strangers"]["items"]}
    lost = [x for x in world.log if x.kind == "lookout.sail_lost"]
    assert lost and lost[-1].data["id"] == "raven"
    # closed again and made out: a stranger, her name not known until she is spoken
    _move(world, "raven", 45.0, 0.36)
    world.run(120)
    raven = _item(world, "raven")
    assert raven["made_out"] >= 2 and raven["name"] is None
    assert raven["words"].startswith("a brig-sloop of war"), raven["words"]


def test_a_liar_is_named_by_the_name_she_gives():
    """A French privateer cutter under British colours answers the hail with a lie: the
    deck knows her by the name she gives, not her own."""
    from tests.test_known_truths import _frigate_and_a_cutter_under_false_colours

    w, v = _frigate_and_a_cutter_under_false_colours(cables=2.0)
    w.run(60)
    said = w.submit("hail her")
    assert said.kind == "hail.answered", said.text
    w.run(60)
    item = _item(w, v.id)
    assert item["name"] and item["name"] != "Renard" and item["name"] in said.data["answer"]
    assert item["words"].startswith(f"the {item['name']}, ")


def test_a_consort_is_named_by_her_pendant_and_a_friend_by_the_private_signal():
    """A sail under our orders is named once her colours are made out; a sail that answered
    the private signal right is named as a friend; a stranger whose colours alone are made
    out keeps her nation and not her name."""
    world = sails_about(settle_s=1)
    own = world.vessel.id if getattr(world, "vessel", None) is not None else "the ship"
    world.vessels.get("swift").under_orders_of = own
    world.run(120)
    assert _item(world, "swift")["name"] == "Swift"
    nancy = _item(world, "nancy")
    assert nancy["nation"] == "britain" and nancy["name"] is None
    from freesail.world.signals import locker_of

    locker_of(world.ship).challenges["nancy"] = {"tick": 0, "verdict": "right"}
    world.run(60)
    assert _item(world, "nancy")["name"] == "Nancy"
    assert _item(world, "raven")["name"] is None  # the French brig: her colours, no name


def test_a_sail_named_reaches_the_next_sample_of_a_station_standing_by():
    """From the model's side: a captain's station held by a fake standing by a glass, a
    brig lying to within hail, made out to her colours. With nothing changed his next sample
    carries no strangers' row; the brig hailed and answering with her name, the sample after
    carries the row again with her name; lost sight of and closed again, the row comes once
    more, nameless, a stranger until she is spoken again."""
    from tests.test_known_truths import _captain_standing_by_a_glass, _samples

    w, h = _captain_standing_by_a_glass("49 48.25 N 5 36 W", "bound for the Lizard")
    brig = next(v for v in w.vessels.active() if v.name == "Two Brothers")
    brig.plan = [("lie_to", math.inf)]
    w.run(1800 + 5)
    n = len(_samples(h))
    assert "strangers" not in _samples(h)[-1]["readings"]
    brig.position = destination(w.position, 0.0, 0.2 * 1852.0)  # kept within hail
    e = w.submit("hail the brig: what ship is that?")
    assert e.kind == "hail.answered" and "Two Brothers" in e.data["answer"], e.text
    w.run(1800)
    later = _samples(h)[n:]
    told = [s["readings"].get("strangers") for s in later if "strangers" in s["readings"]]
    assert told and told[0].startswith("the Two Brothers, a "), told
    # lost sight of, and closed again: the row once more, and nameless
    brig.position = destination(w.position, 0.0, 30 * 1852.0)
    w.run(1800)
    brig.position = destination(w.position, 0.0, 0.25 * 1852.0)
    m = len(_samples(h))
    w.run(1800)
    again = [
        s["readings"].get("strangers") for s in _samples(h)[m:] if "strangers" in s["readings"]
    ]
    assert again and "Two Brothers" not in again[-1], again
    assert again[-1].startswith("a brig") or again[-1].startswith("a merchant brig"), again
