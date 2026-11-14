"""The whole-change review of package 75 at 80e703c7 (2026-11-14): each mend tried at the level of
its cause, then the case that was caught. The owner's word of 2026-11-14 on mends for the cause,
not the symptom, governs them: each test names the cause and the readers it serves.

- **A change of hands makes her a new party** (gundeck-1): what a captain knows of a ship is of
  the people she had; her nation's one road (`prizes._nation_words`) tells every judge on the sea
  (`relations.changed_hands`). A far prize retaken by a cruiser of her own nation fought her
  rescuer a minute later and struck to her.
- **One mark rule for both bodies** (gundeck-2): `Judgement._may_fight` is the one answer's
  `MARK` for the rules captain as for the far brain, and the order's "her" asks it; a crewed
  cruiser takes a far prize of her nation back by coming up, as a far one does.
- **The struck mark's taker within reach, and the strike's record ended with it** (gundeck-4,
  engine-2): `relations.STRUCK`.
- **How she is rigged, apart from what the tops make of her** (sources-1, gundeck-3):
  `ships.rigged`, read by the hail and the glass.
- **The files' words read from the files at load** (engine-3, engine-4): the work's name from the
  registry by id, a far vessel's rig's word from her description.
- **Why work is held** (sailing-1, engine-1): `Instance.held_for`, asked by `_belay_held_work`
  and the reading 'the work in hand'.
- **What stands through held work** (sailing-2): `Script.standing`, read on a resume.
- **A ship file's own hands** (sources-3): every file's, held to the evolutions; never an
  all-hands line numbered.
- **The pipe-down refusal reads the request as made** (sailing-6).

Measured on the owner's machine (Windows 11, 2026-11-14) at seed 7; old is 80e703c7."""

from __future__ import annotations

from pathlib import Path

import pytest

from freesail import units
from freesail.combat import far_action as FA
from freesail.core import replay
from freesail.crew.model import Watch
from freesail.evolutions import registry
from freesail.evolutions.runner import HELD_BY_BELAY, HELD_BY_POST, Runner
from freesail.ship import schema
from freesail.world import hail as H
from freesail.world import lookout as L
from freesail.world import prizes as P
from freesail.world import relations as R
from freesail.world import signalling
from freesail.world.geo import destination
from tests.test_brains import put, world_at
from tests.test_relations import _sea

ROOT = Path(__file__).resolve().parent.parent
SAVES = ROOT / "tests" / "fixtures" / "saves"
# A real checkpoint written on the trunk at 8a06cf9b (before the lead's ruling 17 reached it): the
# player's frigate at 49.5 N 5.5 W and a far British 74, the Bellerophon, three miles north, saved
# five seconds on. A kept save: a change that breaks it is mended in the code, never by changing it.
FAR_74_TRUNK = SAVES / "pre-75-far-seventy-four.checkpoint"
BOAT_CALLED = SAVES / "pre-75-bilander-eight-boat-called.checkpoint"
EIGHT_UNDER_SAIL = SAVES / "pre-75-bilander-eight-under-sail.checkpoint"


def _at(p):
    return {"lat_deg": p.lat_deg, "lon_deg": p.lon_deg}


def _french_held_hope(cap: int, cruiser_nm: float = 0.6, cruiser_first: bool = False):
    """A British merchant brig, the Hope, taken by a French frigate whose ship then leaves the sea,
    and a British frigate, the Amethyst, cruising `cruiser_nm` north of her, the player's frigate
    hove to two miles north of the brig; the cap `cap`. `cruiser_first`: the Amethyst nearer the
    player's ship (a mile south of her) and the brig 0.6 miles south of the Amethyst, so that at a
    cap of one the cruiser is crewed and the prize far."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": cap}
    w.submit("heave to")
    w.run(60)
    if cruiser_first:
        r = destination(w.position, 180.0, 1.0 * units.NAUTICAL_MILE)
        am = put(
            w,
            "frigate",
            "britain",
            _at(r),
            "cruising off the Lizard within 20 miles",
            intent="cruise off the Lizard within 20 miles",
            name="Amethyst",
        )
        here = destination(r, 180.0, 0.6 * units.NAUTICAL_MILE)
    else:
        here = destination(w.position, 180.0, 2.0 * units.NAUTICAL_MILE)
    brig = put(
        w,
        "merchant brig",
        "britain",
        _at(here),
        "bound for Falmouth",
        "bound for Falmouth",
        name="Hope",
    )
    q = destination(here, 90.0, 0.2 * units.NAUTICAL_MILE)
    fr = put(w, "frigate", "france", _at(q), "bound for Brest", "bound for Brest", name="Renard")
    brig.struck = True
    P.possess(w, fr, brig, by="a test", said=False)
    fr.done = True
    if not cruiser_first:
        r = destination(here, 0.0, cruiser_nm * units.NAUTICAL_MILE)
        am = put(
            w,
            "frigate",
            "britain",
            _at(r),
            "cruising off the Lizard within 20 miles",
            intent="cruise off the Lizard within 20 miles",
            name="Amethyst",
        )
    return w, brig, am


# -- a change of hands (gundeck-1) -----------------------------------------------------------------


def test_a_change_of_hands_makes_her_a_new_party_to_every_judge_on_the_sea():
    """The cause: what a captain knows of a ship (her shot at him, a pirate's act, the signal, the
    hail) is of the people she had, and nothing ended it when she changed hands, so the one answer's
    `MARK`, which reads it first, held her what she had been. Mended where her nation changes, the
    one road of every change of hands (`prizes._nation_words`: taken, retaken, restored): every
    judge on the sea forgets what he knew of her, and her own judges what they knew of others
    (`relations.changed_hands`, over `relations.judges`: each ship's far brain and her hull's
    captain, and the player's World's). Tried both ways at the one answer's level: the frigate fired
    on by the brig-sloop's French prize crew, and the prize's brain holding the frigate an enemy by
    the private signal answered in French hands; both a mark to the other before the retake, and
    neither after it, nor after a taking. Old (80e703c7): both still marks after the retake."""
    w, us, foe, mate = _sea()
    P.possess(w, foe, mate, by="a test", said=False)  # the brig-sloop taken by the French 74
    us.brain.fired_on.add(mate.id)  # her prize crew fire on the frigate
    signalling.recognise(mate.brain, us.id, "britain", "the private signal", True)
    w.captain.pirates.add(mate.id)
    assert R.still(w, mate, us, R.MARK)  # the prize holds the frigate her enemy
    assert us.brain._known_enemy({"id": mate.id}) is True
    P.retake(w, mate, by="the Amethyst coming up", how="retaken", captor=us)
    assert not R.still(w, us, mate, R.MARK) and not R.still(w, mate, us, R.MARK)
    assert us.brain._known_enemy({"id": mate.id}) is None
    assert mate.id not in w.captain.pirates
    assert mate.brain.recognised == {} and mate.brain.fired_on == set()
    # taken again: her captor's knowledge of her and hers of every ship go with the change
    foe.brain.fired_on.add(mate.id)
    mate.brain.fired_on.add(foe.id)
    mate.struck = True
    P.possess(w, foe, mate, by="a test", said=False)
    assert mate.id not in foe.brain.fired_on and foe.id not in mate.brain.fired_on
    assert not R.still(w, foe, mate, R.MARK)  # his prize
    judges = R.judges(w)
    assert us.brain in judges and foe.brain in judges and mate.brain in judges
    assert w.captain in judges


def test_a_far_prize_retaken_by_a_cruiser_of_her_nation_never_fights_her_rescuer():
    """The case caught: the Hope, a French prize, retaken by the Amethyst coming up at tick 180,
    paired with her in the far rounds at 240 and struck to her ("struck to the Amethyst: the hands
    would not stand to the guns", four killed), and lay struck for good. Now neither is the other's
    mark: no round between them in twenty minutes, and the Hope takes her passage under her own
    colours. Old (80e703c7): the round at 240 and the Hope struck."""
    w, brig, am = _french_held_hope(cap=0)
    paired: list[tuple[str, str]] = []
    orig = FA._pairs

    def spy(world):
        out = orig(world)
        paired.extend((a.id, getattr(b, "id", b)) for a, b in out)
        return out

    try:
        FA._pairs = spy
        w.run(20 * 60)
    finally:
        FA._pairs = orig
    rec = P.record_of(brig) or {}
    assert rec.get("retaken") and rec.get("recaptor") == am.id
    assert not [p for p in paired if {brig.id, am.id} == set(p)]
    assert not brig.struck and brig.nation == "britain" and brig.state == "on passage"
    assert not (brig.damage or {}).get("killed")


# -- one mark rule for both bodies (gundeck-2) -----------------------------------------------------


def test_the_rules_captain_fights_only_a_mark_by_the_one_answer_as_the_far_brain_does():
    """The cause: two rules for one question. The far brain asked the one answer (`MARK`) whether a
    sail may be fought; the rules captain asked only "not struck", his battery's mark was kept
    whatever she had become (`Captain._mark`), and the order's "her" took the nearest sail at war by
    her colours (`orders.gunnery._mark`). Mended: `Judgement._may_fight` is `MARK` for both
    bodies, `Captain._mark` keeps the battery's mark only while it passes, and "her" chooses among
    the sails that pass. The player's World's captain refuses a prize under a French prize crew, a
    ship struck to another and a friend by the hail, and fights the French 74 as she is. Old
    (80e703c7): he would fight all three."""
    w, us, foe, mate = _sea()
    cap = w.captain
    assert cap._may_fight({"id": foe.id}) and us.brain._may_fight({"id": foe.id})
    signalling.recognise(cap, foe.id, "france", "the hail", False)
    assert not cap._may_fight({"id": foe.id})  # a friend by the hail
    cap.recognised.clear()
    foe.struck = True
    foe.damage["struck_to"] = us.id
    assert not cap._may_fight({"id": foe.id})  # struck, and to another
    foe.struck = False
    foe.damage.pop("struck_to")
    P.possess(w, foe, mate, by="a test", said=False)
    assert not cap._may_fight({"id": mate.id}) and not us.brain._may_fight({"id": mate.id})


def test_a_crewed_cruiser_never_engages_an_enemy_held_prize_of_her_nation():
    """The case caught: at a cap of three the crewed Amethyst, beside the French-held Hope, went
    engaging her at 480 ("Engage a merchant brig to larboard"), cast loose and fired into her, and
    stayed so over an hour. Now she never engages her in a quarter of an hour, and gives no order to
    engage her. Old (80e703c7): engaging at 480."""
    w, brig, am = _french_held_hope(cap=3)
    states = set()
    for _ in range(15):
        w.run(60)
        if am.crew is not None:
            states.add(am.crew.captain.state)
    assert am.crew is not None and am.crew.shape == "full"
    assert "engaging" not in states
    engaged = [e for e in am.crew.log.all() if e.kind == "guns.engage"]
    assert not engaged and not [e for e in am.crew.log.all() if e.kind == "action.fired"]


def test_a_crewed_cruiser_takes_a_far_prize_of_her_nation_back_by_coming_up():
    """The far rule of the retake by coming up (`squadrons.far_captures`) skipped a crewed captor
    ("the near fight is 70's"), so with the near body no longer fighting her a crewed cruiser would
    never have her: it now takes a crewed cruiser for a far prize of her own nation alone, her
    hull's captain's state and mark read where the far brain's were. At a cap of one the Amethyst,
    crewed, retakes the far Hope by tick 300 and gives up her mark. Old (80e703c7): she engaged her
    and never had her."""
    w, brig, am = _french_held_hope(cap=1, cruiser_first=True)
    w.run(5 * 60)
    assert am.crew is not None and am.crew.shape == "full" and brig.crew is None
    rec = P.record_of(brig) or {}
    assert rec.get("retaken") and rec.get("recaptor") == am.id
    assert brig.nation == "britain" and not P.is_prize(brig)
    assert brig.id in am.crew.captain.spoken_ids


# -- the struck mark (gundeck-4, engine-2) ---------------------------------------------------------


def test_a_struck_ship_is_free_to_take_when_her_taker_is_out_of_reach_or_her_strike_is_over():
    """The cause: `STRUCK`'s taker "there to take her" asked only that she be on the sea, the same
    gap (F4) found in support, and the strike's record (`struck_to`, `struck_tick`) outlived the
    strike, since nothing ended it when her colours went up again. Mended at the one answer: a
    taker beyond the miles at which she could still support (`in_company_nm`, JUDGEMENT) is no
    longer there to take her; and at the one road by which a struck ship's colours go up again
    (`prizes._set_colours`), the strike's record ends. The French 74 struck to the brig-sloop is
    not the frigate's to take while the brig-sloop is within eight miles, and is when she is
    beyond them; and struck to the brig-sloop, given her colours back and struck again by a road
    that names no taker, she is anybody's. Old (80e703c7): neither."""
    w, us, foe, mate = _sea()
    foe.struck = True
    foe.damage["struck_to"] = mate.id
    foe.damage["struck_tick"] = 0
    assert not R.still(w, us, foe, R.STRUCK) and R.still(w, mate, foe, R.STRUCK)
    reach = R.in_company_nm(w, mate.id)
    near = mate.position
    mate.position = destination(foe.position, 0.0, (reach + 1.0) * units.NAUTICAL_MILE)
    assert R.still(w, us, foe, R.STRUCK)  # her taker out of reach
    mate.position = near
    P._set_colours(w, foe, foe.nation, "", int(w.clock.tick))
    assert not foe.struck and "struck_to" not in foe.damage and "struck_tick" not in foe.damage
    foe.struck = True  # struck again by the near action, a cut-out or a world order: no taker
    assert R.still(w, us, foe, R.STRUCK) and R.still(w, mate, foe, R.STRUCK)
    assert not FA.struck_within_hour(w, foe)  # her hour not counted from the old strike


# -- how she is rigged (sources-1, gundeck-3) ------------------------------------------------------


@pytest.mark.parametrize(
    "description,nation,name,answer",
    [
        ("seventy-four", "britain", "Bellerophon", "His Majesty's ship Bellerophon."),
        ("seventy-four", "france", "Tonnant", "The French national ship Tonnant."),
        ("sixty-four", "britain", "Ardent", "His Majesty's ship Ardent."),
        ("frigate", "britain", "Amethyst", "His Majesty's ship Amethyst."),
    ],
)
def test_a_two_decker_answers_the_hail_and_lies_to_as_a_ship_rigged_ship(
    description, nation, name, answer
):
    """The cause: the rig's word did two jobs, what the tops make of her at the rig's distance (for
    a two-decker her class, "a ship of the line", the lead's ruling 17) and how she is rigged, so
    the step that changed it moved every reader of the second: the hail's answer ("His Majesty's
    ship of the line Bellerophon") and the glass of a far two-decker lying to ("her sails aback",
    where her main topsail is). Mended where the word lives (`ships.rigged`: a ship of the line is a
    ship), read by both. Each answers and lies to as she did before 53c14457, as a frigate does.
    Old (80e703c7): "His Majesty's ship of the line Bellerophon", "her sails aback"."""
    w = world_at(49.5, -5.5)
    w.crewed_settings = {"cap": 0}
    w.run(10)
    here = destination(w.position, 180.0, 0.6 * units.NAUTICAL_MILE)
    v = put(
        w, description, nation, _at(here), "bound for Falmouth", "bound for Falmouth", name=name
    )
    assert H.answer_by_table(w, v, "What ship is that?").startswith(answer)
    v.plan = [("lie_to", float("inf"))]
    v.state = "hove to"
    assert L._glass_far(w, v)["words"].endswith(", main topsail aback")


# -- the files' words read from the files at load (engine-3, engine-4) -----------------------------


def test_a_far_seventy_four_saved_on_the_trunk_loads_a_ship_of_the_line():
    """The cause: a word of the files copied into the pickle (`Vessel.kind`, from her description's
    rig) and read from there, stale across a save and a load. A far 74 saved on the trunk, where her
    word was "a ship", loaded as a frigate's class at every distance, where the trunk read her a
    ship of the line's (`_size_of`, gone with ruling 17) and a new game does at her rig's distance.
    Her word is read again from her description at load (`replay._rig_word_now`), as a new game
    makes it. Old (80e703c7): "a ship", rank 3."""
    from freesail.world.captains import size_of_words

    _, w = replay.read_checkpoint(FAR_74_TRUNK)
    v = w.vessels.find("Bellerophon")
    assert v.kind == "a ship of the line"
    assert v.seen_as_feature(3.0 * units.NAUTICAL_MILE).name == "a ship of the line"
    assert size_of_words(v.words_at(1)) == 4
    w.run(60)  # and sails on


def test_work_saved_before_its_file_named_it_is_named_as_the_file_names_it_now():
    """The same cause in the work's name (the lead's (C8)): an evolution pickled before its file
    gave `doing:` read None from the class, so a boat called on the trunk was "sending boat", which
    the lookout's glass no longer knows ("sending the boat", a boat hoisting out or in). The runner
    reads the file's words from the registry by the work's id (`Runner._doing`). Old (80e703c7):
    "sending boat"."""
    _, w = replay.read_checkpoint(BOAT_CALLED)
    runner = w.ship.extra["evolutions"]
    boat = next(i for i in runner.instances if i.evo.id == "send_boat")
    assert "doing" not in boat.evo.__dict__  # the save's own evolution names nothing
    assert runner.doing(boat) == "sending the boat"
    assert "sending the boat" in dict(L._WORK_KINDS)


# -- why work is held (sailing-1, engine-1) --------------------------------------------------------


def _torbay_bilander_at_nine():
    from tests.test_mends_109 import bilander

    w = bilander()
    w.ship.extra["crew"].watch_on_deck = Watch.LARBOARD
    return w


def test_a_hold_says_why_and_the_anchor_belays_only_the_sail_work_it_held():
    """The cause: the pause got one road (`Runner._hold`, the lead's (C6)) and none for reading it.
    Two readers of a hold were written when it could only be a manoeuvre's belay of the step-list
    sail work in hand (decision 25), and read a post's leaving work under half its hands (the
    lead's ruling 11) as one: `scripts._belay_held_work`, which ends held work as she comes to
    anchor or gets under way, and the reading 'the work in hand' ("belayed while all hands are
    about ship"). The hold now records why (`Instance.held_by`, read by `held_for`: a manoeuvre's
    or a post's, a checkpoint from before read by the only holds it could carry), and each reader
    asks it: the anchor keeps the ship's own work and her repairs that a post's leaving held, to
    be taken up after the pipe-down, and belays the rest as before; the reading says "held for
    hands". Old (80e703c7): every held work ended at the anchor, and every hold read as all hands
    about ship."""
    from freesail.api import readings
    from freesail.evolutions.scripts import _belay_held_work

    w = _torbay_bilander_at_nine()
    ship, runner, crew = w.ship, w.ship.extra["evolutions"], w.ship.extra["crew"]
    assert w.submit("batten down the hatches").kind == "order.accepted"
    w.run(2)
    batten = next(i for i in runner.instances if i.evo.id == "batten_down")
    runner._hold(ship, crew, batten, "the master gone below", {"for": "post", "post": "master"})
    assert batten.held_for == HELD_BY_POST
    words = readings._work_in_hand(w, None)
    assert words["held"] == ["battening down"] and not words["belayed"]
    assert "held for hands: battening down" in words["words"]
    assert "all hands are about ship" not in words["words"]
    _belay_held_work(ship)
    assert batten in runner.instances and batten.paused  # kept for the pipe-down
    batten.held_by = None
    assert batten.held_for == HELD_BY_POST  # a checkpoint from before: scripted, so a post's
    runner._hold(ship, crew, batten, "stations for wearing ship", {"for": "wear"})
    assert batten.held_for == HELD_BY_BELAY
    _belay_held_work(ship)
    assert batten not in runner.instances  # a manoeuvre's belay ends at the anchor, as before


def test_ship_work_a_post_left_is_taken_up_after_she_comes_to_anchor():
    """The case caught: in the Torbay bilander at her nine, her larboard watch on deck, "batten down
    the hatches" begun by the three and the master, and "come to anchor" 8 s on: "Belayed
    battening down: all hands, bring ship to anchor!", and when she was brought up and piped down
    nothing more of it, the hatches open and no word. Now the hatches are battened down after the
    pipe-down. Old (80e703c7): the hatches open."""
    from freesail.api import damage_readings as DR

    w = _torbay_bilander_at_nine()
    n = len(w.log)
    assert w.submit("batten down the hatches").kind == "order.accepted"
    w.run(8)
    assert w.submit("come to anchor").kind == "order.accepted"
    w.run(2400)
    kinds = [e.kind for e in list(w.log)[n:]]
    assert "evolution.belayed" in kinds and "crew.piped_down" in kinds
    assert kinds.index("hatches.battened") > kinds.index("crew.piped_down")
    assert DR._hatches(w, None)["battened"] is True


# -- what stands through held work (sailing-2) -----------------------------------------------------


def test_a_mast_carried_away_while_her_cutting_away_lies_held_is_not_cut_away_again():
    """The case caught (the cause's level is `test_held_work`'s sweep, every scripted work reading
    `Script.standing` on its taking up): the (C1) mend left a script's whole check unread on a
    resume, the standing guards with the beginning's. In the Torbay bilander at anchor at her nine,
    "cut away the mainmast" by the three and the master, the master going below 8 s on, the main
    mast carried away while it lay held, and the master on deck again: the work is refused in the
    file's words ("Could not cut away the main mast: the main mast is carried away already; clear
    the wreck."), as cda12ec9 refused it. Old (80e703c7): cut away and wrecked a second time, "gone
    over the side" at +1820."""
    from freesail.physics import strain as ST
    from tests.test_mends_109 import bilander

    w = bilander()
    assert w.submit("let go the anchor").kind == "order.accepted"
    w.run(600)
    w.ship.extra["crew"].watch_on_deck = Watch.LARBOARD
    runner = w.ship.extra["evolutions"]
    n = len(w.log)
    assert w.submit("cut away the mainmast").kind == "order.accepted"
    w.run(8)
    assert w.submit("go below").kind == "captain.below"
    w.run(5)
    mast = w.ship.spars["main.mast"]
    ST._wreck_spar(w.ship, ST.strain_state(w.ship), mast, 0.0, how="carried away")
    w.run(5)
    assert w.submit("come on deck").kind == "captain.on_deck"
    for _ in range(3000):
        w.tick()
        if not runner.in_progress():
            break
    texts = [(e.kind, e.text) for e in list(w.log)[n:]]
    assert (
        "evolution.failed",
        "Could not cut away the main mast: the main mast is carried away already; clear the wreck.",
    ) in texts
    assert not [k for k, _t in texts if k == "mast.cut_away"]
    assert (
        "evolution.belayed",
        "Belayed cutting away the main mast: the master gone below.",
    ) in texts


# -- a ship file's own hands (sources-3) -----------------------------------------------------------


def test_every_ship_files_own_hands_name_numbered_work_and_are_refused_in_words():
    """The cause: the `hands:` section ((C2)) was held only to its shape, and its parser's word that
    "the files' tests hold every ship file's to them" was not so. Now every ship file's are held to
    the evolutions: each id one of the registry's whose file asks a number of hands, the bilander's
    alone given (heaving to and filling away, six), every other file's none; the shape refused in
    words; and the runner reads a ship's figure only over a file's number, so that a tack, all
    hands' work, is never numbered by a ship file. Old (80e703c7): `{"tack": 2}` made a tack the
    work of two."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario
    from freesail.ship.loader import load_spec

    for path in sorted((ROOT / "data" / "ships").glob("*.yaml")):
        spec = load_spec(path)
        own = dict(getattr(spec, "hands", None) or {})
        for eid, n in own.items():
            evo = registry.get(eid)
            assert evo is not None, (path.name, eid)
            line = (evo.crew or {}).get("hands")
            assert isinstance(line, int) and not isinstance(line, bool), (path.name, eid, line)
            assert isinstance(n, int) and n >= 1
        assert own == ({"heave_to": 6, "fill_away": 6} if path.stem == "bilander" else {})
    for bad in ([6], 0, -1, 2.5, True, "six"):
        raw = bad if isinstance(bad, list) else {"heave_to": bad}
        with pytest.raises(
            schema.ShipFileError, match="whole number of hands|mapping of evolutions"
        ):
            schema._parse_hands(raw, "test.yaml")
    w = make_world(7, "data/ships/bilander.yaml", Scenario())
    w.ship.spec.hands = {"tack": 2, "heave_to": 6}
    assert Runner._crew_line(w.ship, registry.get("tack"))["hands"] == "all"
    assert Runner._crew_line(w.ship, registry.get("heave_to"))["hands"] == 6


# -- the pipe-down refusal reads the request as made (sailing-6) -----------------------------------


def test_pipe_down_is_refused_while_all_hands_are_at_work_called_for_itself():
    """The cause: the plan read where the work's own state should be. The pipe-down refusal
    (`orders.crew.all_hands_work`) read the evolution file's crew line, so work that called all
    hands for itself because its watch was too few (the lead's ruling (1) of 2026-11-10) was not
    all-hands work to it: in the bilander at her eight by night (a kept save written on the trunk),
    "take in the mainsail" called all hands, and "pipe down" four seconds on was taken while they
    were at it. It reads the request as it was made (`Instance.all_hands`). Old (80e703c7): "Piped
    down; the larboard watch has the deck."."""
    _, w = replay.read_checkpoint(EIGHT_UNDER_SAIL)
    assert w.submit("take in the mainsail").kind == "order.accepted"
    w.run(5)
    r = w.submit("pipe down")
    assert r.kind == "order.rejected"
    assert "All hands are still at work (taking in the mainsail)" in r.text


def test_a_two_deckers_rig_word_is_still_her_class_for_the_tops():
    """`ships.rigged` leaves what the tops make of her as ruling 17 has it: a ship of the line, of
    rank 4 at the rig's distance, where a razee is a ship."""
    from freesail.world.captains import size_of_words
    from freesail.world.ships import DESCRIPTIONS, rigged

    assert DESCRIPTIONS["seventy-four"]["rig"] == "a ship of the line"
    assert rigged("a ship of the line") == "a ship" and rigged("a brig") == "a brig"
    assert size_of_words("a ship of the line") == 4
