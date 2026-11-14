"""Work held and taken up again, and a post's leaving said (package 75's close: the lead's readings
of cda12ec9, 2026-11-14, the crew and the evolutions, (C1), (C3), (C6) and (C7)).

**The cause, (C1).** Work paused and begun again as if new. The pause has one road (`Runner._hold`,
the lead's (C6)): a manoeuvre's belay of the step-list work in hand (decision 25) and a post's
leaving work under half its hands (the lead's ruling 11 of 2026-11-13) hold it, its hands let go
and its progress kept, said "Belayed ...", and take it up again where it stood when hands come
(`Runner._try_resume`). The resume read a script's own check again (`Script.check`), which is the
beginning's: it reads the world as the work finds it and lays its plan from it, and the work's own
going makes it false. So a kedge held while its boat was hoisting out was refused ("Could not lay
out the kedge: the long-boat is away.") and a veer of twenty fathoms laid a new target from the
scope it had veered to (fifty-eight fathoms where fifty-six were ordered), on every road that takes
a post off: quarters, all hands called, a manoeuvre begun and the master going below. Mended where
the cause lives: a resume never reads the beginning's check (`Runner._failing_condition`'s
`begun`), only the file's `requires`, which hold through the work. The test at that level is the
first: every scripted evolution of the registry, held and taken up again by the one road, never
reads its check again. Then every scripted work a post may hold in the bilander at her nine, sailed
with the post taken off it mid-work by each road that can reach it, finishes as ordered.

**(C3).** Where the work goes on short the post's leaving is said in the short line's words ("Only
four hands to the foresail; the master gone below."), as the belayed line says it where the work is
held. **(C7).** A post taken off by all hands called, at the sight and sent for, each sailed to the
work's end; the old mark of package 109's road on a world written on the trunk, loaded and sailed
on.

The figures are measured on the owner's machine (Windows 11, 2026-11-14) at seed 7; old is
53c14457, the branch before these mends.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import pytest

from freesail.api.session import make_world
from freesail.core import replay
from freesail.core.world import Scenario
from freesail.crew.model import Watch
from freesail.evolutions import registry
from freesail.evolutions.runner import Instance
from freesail.evolutions.scripts import SCRIPTS, _tackle
from freesail.ship.parts import Line, Sail, SailState, Spar

HER = "data/ships/bilander.yaml"
SAVES = Path(__file__).resolve().parent / "fixtures" / "saves"
# A real checkpoint written on the trunk at 1eea8d18 (the bilander at her eight, package 109's road
# for the boat): package 109's Torbay world at 04:10, her larboard watch of two, saved the moment
# "go ashore" had called all hands to man the boat, the boat's params carrying that road's mark
# (`hands_called_for`). A kept save: a change that breaks it is mended in the code, never by
# changing it.
BOAT_CALLED = SAVES / "pre-75-bilander-eight-boat-called.checkpoint"
# The trunk's own lines for the 1,200 s after it, sailed on the trunk from the same world: ticks
# from the save, kinds and words, the wind's gusts and the bells left out.
BOAT_CALLED_TRUNK = [
    (1, "crew.all_hands", "All hands! (to send boat)"),
    (1, "evolution.short_handed", "Only four hands to send boat; there are no more on deck."),
    (1, "crew.piped_down", "Piped down; the larboard watch has the deck."),
    (1, "evolution.started", "Away the long-boat's crew! Hoist out the long-boat."),
    (1, "ship.command_devolved", "The command devolves on Mr Pearce, the captain in the boat."),
    (
        401,
        "boat.away",
        "The long-boat away for the quay at Brixham with Mr Bowen, to land a person who stays "
        "ashore.",
    ),
]
QUIET = ("evolution.step", "wind.gust", "clock.bell")


def _lines(world, n: int, start: int) -> list[tuple[int, str, str]]:
    return [
        (e.tick - start, e.kind, e.text)
        for e in list(world.log)[n:]
        if not e.kind.startswith(QUIET)
    ]


# -- the cause's level: every scripted evolution, held and taken up again ------------------------


def _subject(ship, cls: str):
    """The first part of `ship` an evolution of `cls` applies to, or the ship herself."""
    if cls == "ship":
        return ship, ship.name
    for part in ship.parts.values():
        fits = {
            "sail": isinstance(part, Sail),
            "part": isinstance(part, Sail | Spar),
            "spar": isinstance(part, Spar),
            "line": isinstance(part, Line),
            "flying": isinstance(part, Sail) and part.flying,
            "settee": isinstance(part, Sail) and part.settee,
        }.get(cls, getattr(part, "cls", None) == cls)
        if fits:
            return part, part.id
    return None, None


def test_every_scripted_work_held_and_taken_up_again_never_reads_its_beginning_again():
    """The lead's (C1) of 2026-11-14 at the cause's level: every scripted evolution of the registry,
    begun (its check read once, as `Runner.start` reads it), held as the pause's one road leaves it
    (`Runner._hold`: paused, its hands let go) and taken up again (`Runner._try_resume`) with hands
    enough, goes on: the script's own check is never read again, so no work is refused or
    replanned by what its own going has made so (`Runner._failing_condition`'s `begun`). Each on
    the first of three ships at seed 7 with a part of its class: the bilander, the topsail
    schooner (her gaffs) and the 74 (her mizen lateen), the check made to give a reason, so that a
    reading of it on the resume would fail the work. Old (53c14457): the check read again on every
    resume, and every one of them failed on its taking up ("Could not lay out the kedge: the
    long-boat is away.", read as the work's own going had made it).

    And (the whole-change review of 80e703c7, sailing-2): what of the script's own conditions stands
    through the work (`Script.standing`: what the world can make false while the work is held and
    its own going never does) is read on every taking up, as the file's `requires` are, so that a
    mast carried away while her cutting away lay held is not cut away again. Old (80e703c7): no
    script's standing conditions were read on a resume."""
    worlds = [
        make_world(7, f"data/ships/{stem}.yaml", Scenario())
        for stem in ("bilander", "topsail-schooner", "seventy-four")
    ]
    tried = set()
    for eid, evo in sorted(registry.EVOLUTIONS.items()):
        if evo.script is None:
            continue
        for w in worlds:
            ship = w.ship
            subject, sid = _subject(ship, str(evo.applies_to.get("class")))
            if subject is not None:
                break
        assert subject is not None, eid
        runner, crew = ship.extra["evolutions"], ship.extra["crew"]
        params = dict(evo.params)
        inst = Instance(evo=evo, subject=subject, subject_id=sid, params=params)
        runner._counter += 1
        inst.order = runner._counter
        inst.script = SCRIPTS[evo.script](ship, params, runner._timing(ship, evo))
        inst.holds = runner._holds(ship, inst)
        read: list[str] = []
        stood: list[str] = []
        inst.script.check = lambda words, read=read: read.append("read") or "it is done already"
        inst.script.standing = lambda words, stood=stood: stood.append("read") or None
        runner.instances.append(inst)
        assert runner._failing_condition(ship, inst, evo.requires) == "it is done already", eid
        assert read == ["read"] and stood == [], eid  # the beginning reads its check alone
        inst.waiting, inst.paused, inst.assignment = False, True, None
        runner._try_resume(ship, inst, crew)
        assert read == ["read"], eid  # the resume does not read the check
        assert stood == ["read"], eid  # and reads what stands through the work
        assert inst in runner.instances, (eid, "failed on its taking up")
        assert not inst.paused, (eid, "not taken up: too few hands, the check not reached")
        runner._remove(ship, inst)
        tried.add(eid)
    assert len(tried) == sum(1 for e in registry.EVOLUTIONS.values() if e.script is not None)


# -- (C6): the pause's one road --------------------------------------------------------------------


def test_a_manoeuvres_belay_and_a_posts_leaving_hold_work_by_the_one_road(held_worlds, monkeypatch):
    """The lead's (C6) of 2026-11-14: `Runner._post_off` repeated `Runner._call_all_hands`'s pause,
    release and "Belayed" block, and (C1) lived in that block: now one road, `Runner._hold`, taken
    by both. Under sail at her nine, her larboard watch by night: "take in the jib" by the three
    and the master, and "wear ship" 8 s on: the wear's belay holds the jib by the road ("Belayed
    taking in the jib: stations for wearing ship.", for the wear); at anchor, "batten down the
    hatches" by the three and the master, and the master going below: the post's leaving holds it
    by the road ("Belayed battening down: the master gone below.", for the post). Old (53c14457):
    two copies of the block, the one in `_post_off` holding scripted work the other never held."""
    from freesail.evolutions.runner import Runner

    roads: list[tuple[str, str]] = []
    hold = Runner._hold

    def spied(self, ship, crew, work, reason, data):
        roads.append((work.evo.id, data["for"]))
        return hold(self, ship, crew, work, reason, data)

    monkeypatch.setattr(Runner, "_hold", spied)
    world = _held_world(held_worlds, "sailing")
    world.ship.sails["jib"].state = SailState.SET
    n, start = len(world.log), world.clock.tick
    assert world.submit("take in the jib").kind == "order.accepted"
    world.run(8)
    assert world.submit("wear ship").kind == "order.accepted"
    world.tick()
    said = [text for _, kind, text in _lines(world, n, start) if kind == "evolution.belayed"]
    assert roads == [("take_in_jibheaded", "wear")], roads
    assert said == ["Belayed taking in the jib: stations for wearing ship."], said
    world = _held_world(held_worlds, "anchored")
    n, start = len(world.log), world.clock.tick
    assert world.submit("batten down the hatches").kind == "order.accepted"
    world.run(8)
    assert world.submit("go below").kind == "captain.below"
    world.tick()
    said = [text for _, kind, text in _lines(world, n, start) if kind == "evolution.belayed"]
    assert roads[1:] == [("batten_down", "post")], roads
    assert said == ["Belayed battening down: the master gone below."], said


# -- the bilander at her nine: every scripted work a post may hold, the post taken off mid-work ---


@pytest.fixture(scope="module")
def held_worlds(tmp_path_factory):
    """Two worlds of hers at nine, checkpointed once and read again for each case. At anchor:
    package 109's Torbay world, the best bower let go and 600 s on (02:10), her larboard watch
    given the deck by the bill's own override, so that its three and the master work (the master
    is her captain). Under sail: her settle from 00:00 (all hands, plain sail set and braced sharp
    up, tests/test_bilander.py), the hands piped down and 30 s, her larboard watch by night."""
    from tests.test_bilander import _her_settle
    from tests.test_mends_109 import bilander

    d = tmp_path_factory.mktemp("held")
    w = bilander()
    w.submit("let go the anchor")
    w.run(600)
    anchored = replay.write_checkpoint(w, d / "anchored.checkpoint")
    w = _her_settle(15.0, start_time=datetime(1805, 6, 1, 0, 0))
    assert w.submit("pipe down").kind == "crew.piped_down"
    w.run(30)
    sailing = replay.write_checkpoint(w, d / "sailing.checkpoint")
    return {"anchored": anchored, "sailing": sailing}


def _held_world(held_worlds, where: str):
    world = replay.read_checkpoint(held_worlds[where])[1]
    if where == "anchored":
        world.ship.extra["crew"].watch_on_deck = Watch.LARBOARD
    return world


# work: (world, order, evolution, its name in the log, the line its end says, its end's kind)
WORKS = {
    "veer": ("anchored", "veer 20 fathoms", "veer_cable", "veering the cable", "cable.veered"),
    "kedge": (
        "anchored",
        "lay out a kedge to the E",
        "lay_out_kedge",
        "laying out the kedge",
        "ship.kedged",
    ),
    "let go": (
        "anchored",
        "let go the small bower",
        "let_go_anchor",
        "letting go the anchor",
        "ship.anchored",
    ),
    "boat": (
        "anchored",
        "send the boat ashore for the prices",
        "send_boat",
        "sending the boat",
        "boat.away",
    ),
    "batten down": (
        "anchored",
        "batten down the hatches",
        "batten_down",
        "battening down",
        "hatches.battened",
    ),
    "batten down under sail": (
        "sailing",
        "batten down the hatches",
        "batten_down",
        "battening down",
        "hatches.battened",
    ),
    "small arms": (
        "sailing",
        "serve out the small arms",
        "serve_small_arms",
        "serving small arms",
        "small_arms.served",
    ),
}
# what takes the post off, and the words of their leaving: held (three of seven, under half) or
# going on short (three of six, half)
CAUSES = {
    "quarters": ("beat to quarters", "the master to the conn at quarters"),
    "all hands": ("call all hands", "the master to the conn, all hands called"),
    "below": ("go below", "the master gone below"),
    "manoeuvre": ("wear ship", None),
}
CASES = [
    (work, cause)
    for work in WORKS
    for cause in CAUSES
    if cause != "manoeuvre" or work in ("batten down under sail", "small arms")
]


@pytest.mark.parametrize("work, cause", CASES, ids=[f"{w}-{c}" for w, c in CASES])
def test_every_scripted_work_a_post_may_hold_finishes_as_ordered_whatever_takes_the_post_off(
    held_worlds, work, cause
):
    """The lead's (C1) of 2026-11-14, every scripted work and every road: each scripted work a
    post of hers may hold at her nine (numbered work on deck whose want her watch's three are
    under: the veer, the kedge, letting go the small bower and the boat at anchor, battening down
    at anchor and under sail, serving out the small arms), begun by the larboard watch's three and
    the master, with the master taken off it 8 s on by each road that can reach it: beating to
    quarters, all hands called, the master going below (and on deck again 130 s from the order) and,
    for work that does not hold the ship, a manoeuvre begun (a wear). Each finishes as ordered: its
    end's line said, nothing failed or refused, its check never read again (the veer to fifty-six
    fathoms, thirty-six and twenty), and the post's leaving said once, by name: held where its
    three are under half its seven ("Belayed laying out the kedge: the master gone below."), going
    on short where they are half its six ("Only three hands to serve small arms; the master to the
    conn for wearing ship."). The manoeuvre's own belay keeps its words ("Belayed battening down:
    stations for wearing ship."). Work that holds the ship (the anchor's, the boat's hoisting out
    is not) is never met by a manoeuvre begun: the manoeuvre waits for it.
    Old (53c14457): the check read again on every resume; the kedge refused on each road ("Could
    not lay out the kedge: the long-boat is away."), the veer to fifty-eight fathoms and a third;
    the belayed lines named the works by their ids ("Belayed laying out kedge"); and work going on
    short said nothing of the post.
    Not sailed here, each tried at the cause's level by the test before: backing and catting the
    anchor (she carries no stream anchor; an anchor left aweigh is a weigh belayed), the trims (her
    sheets stand as trimmed at her settle), the guns' and the damage's work (a fight's), and the
    signal and the mark (their want is her watch's three, so no post is counted)."""
    where, order, eid, doing, done = WORKS[work]
    world = _held_world(held_worlds, where)
    runner = world.ship.extra["evolutions"]
    tackle = _tackle(world.ship)
    before = {a.name: a.scope_fathoms for a in tackle.anchors if a.down} if tackle else {}
    n, start = len(world.log), world.clock.tick
    assert world.submit(order).kind == "order.accepted"
    (inst,) = [i for i in runner.instances if i.evo.id == eid]
    assert [h.post for h in inst.assignment.hands if h.post] == ["master"]
    read: list[str] = []
    check = inst.script.check
    inst.script.check = lambda words: read.append("read") or check(words)
    world.run(8)
    words, gone = CAUSES[cause]
    assert world.submit(words).kind != "order.rejected"
    for _ in range(3000):
        world.tick()
        if cause == "below" and world.clock.tick - start == 130:
            assert world.submit("come on deck").kind == "captain.on_deck"
        if any(e.kind == done for e in list(world.log)[n:]):
            break
    lines = _lines(world, n, start)
    assert [ln for ln in lines if ln[1] == done], (work, cause, lines)
    assert not [ln for ln in lines if ln[1] == "evolution.failed"], lines
    assert read == [], "the check was read again on the work's taking up"
    held = [(t, text) for t, kind, text in lines if kind == "evolution.belayed"]
    short = [(t, text) for t, kind, text in lines if kind == "evolution.short_handed" and t == 9]
    if cause == "manoeuvre" and eid == "batten_down":
        assert held == [(9, f"Belayed {doing}: stations for wearing ship.")]
    elif cause == "manoeuvre":
        said = "Only three hands to serve small arms; the master to the conn for wearing ship."
        assert held == [] and short[0] == (9, said), short
    elif eid == "serve_small_arms":
        assert held == [] and short == [(9, f"Only three hands to serve small arms; {gone}.")]
    else:
        assert held == [(9, f"Belayed {doing}: {gone}.")] and short == [], (held, short)
    if eid == "veer_cable":
        (after,) = [a.scope_fathoms for a in tackle.anchors if a.down]
        assert after == pytest.approx(before["the best bower"] + 20.0, abs=0.05)
        assert ("cable.veered", "Veered to fifty-six fathoms on the best bower.") in [
            (k, x) for _, k, x in lines
        ]
    if eid == "lay_out_kedge":
        kedge = next(a for a in tackle.anchors if a.kind == "kedge")
        assert kedge.down and kedge.scope_fathoms == pytest.approx(90.4, abs=0.1)


def test_the_kedge_and_the_veer_held_when_all_hands_are_called_finish_as_ordered(held_worlds):
    """The reading's own two (the lead's (C1) of 2026-11-14): her kedge laid out by the larboard's
    three and the master, all hands called 8 s later: "Belayed laying out the kedge: the master to
    the conn, all hands called.", taken up on that tick by the hands up, and laid out ninety fathoms
    to the east at +1,611 s, nothing refused. "veer 20 fathoms" with the same pause veers to the
    scope ordered, thirty-six and twenty: "Veered to fifty-six fathoms on the best bower." at +66 s.
    Old (53c14457): "Belayed laying out kedge: the master to the conn, all hands called." and on the
    same tick "Could not lay out the kedge: the long-boat is away."; the veer "Veered to fifty-eight
    fathoms on the best bower." (58.33 fathoms), its target laid again from the scope it had
    veered to by the pause."""
    for order, doing, done, end_s in (
        ("lay out a kedge to the E", "laying out the kedge", "ship.kedged", 1611),
        ("veer 20 fathoms", "veering the cable", "cable.veered", 66),
    ):
        world = _held_world(held_worlds, "anchored")
        n, start = len(world.log), world.clock.tick
        assert world.submit(order).kind == "order.accepted"
        world.run(8)
        assert world.submit("call all hands").kind == "crew.order"
        for _ in range(2000):
            world.tick()
            if any(e.kind == done for e in list(world.log)[n:]):
                break
        lines = _lines(world, n, start)
        said = f"Belayed {doing}: the master to the conn, all hands called."
        assert (9, "evolution.belayed", said) in lines, lines
        assert not [ln for ln in lines if ln[1] == "evolution.failed"], lines
        (end,) = [t for t, kind, _ in lines if kind == done]
        assert abs(end - end_s) <= 10, end
        if done == "cable.veered":
            assert (end, done, "Veered to fifty-six fathoms on the best bower.") in lines


# -- (C3) and (C7): the post's leaving said where the work goes on short, and every road sailed ---


def _her_world(hour: int, minute: int = 0, watch: Watch | None = None):
    """Her World at nine at seed 7 off the Lizard at the hour (tests/test_brains.py's world), her
    people made, the fore course in the gear; `watch` given the deck by the bill's own override."""
    sc = Scenario(
        start_time=datetime(1805, 6, 12, hour, minute),
        wind_from_deg=270.0,
        wind_speed_kn=14.0,
        gustiness=0.0,
        variability=0.0,
        position={"lat_deg": 49.5, "lon_deg": -5.5},
        region="channel-west",
        ports=["falmouth", "plymouth", "brest"],
        nation="britain",
    )
    w = make_world(7, HER, sc)
    _ = w.people.all
    w.ship.sails["fore.course"].state = SailState.IN_THE_GEAR
    if watch is not None:
        w.ship.extra["crew"].watch_on_deck = watch
    return w


def _set_the_fore_course(world):
    """ "Set the fore course" given: the log's length and the tick at the order, and her posts."""
    crew = world.ship.extra["crew"]
    posts = {s.post: s for s in crew.sailors if s.post}
    n, start = len(world.log), world.clock.tick
    assert world.submit("set the fore course").kind == "order.accepted"
    return n, start, posts


def test_the_posts_leaving_is_said_where_the_work_goes_on_short():
    """The lead's (C3) of 2026-11-14: the fore course set at noon by the larboard watch's three,
    the cook and the master, five of the seven it wants ("Only five hands to the foresail; there are
    no more on deck."); the captain, who is her master, goes below 5 s on: the work goes on short
    with four, over half its seven, and the post's leaving is said where it goes on, in the short
    line's words: "Only four hands to the foresail; the master gone below." The foresail is set at
    +304 s by the four. Old (53c14457): nothing said of the master's leaving, the log's last word of
    the hands "Only five hands to the foresail" though four set it."""
    world = _her_world(12, watch=Watch.LARBOARD)
    world.run(30)
    n, start, posts = _set_the_fore_course(world)
    world.run(5)
    assert world.submit("go below").kind == "captain.below"
    for _ in range(900):
        world.tick()
        if world.ship.sails["fore.course"].state is SailState.SET:
            break
    lines = _lines(world, n, start)
    shorts = [(t, text) for t, kind, text in lines if kind == "evolution.short_handed"]
    assert shorts == [
        (1, "Only five hands to the foresail; there are no more on deck."),
        (6, "Only four hands to the foresail; the master gone below."),
    ], shorts
    assert not [ln for ln in lines if ln[1] == "evolution.belayed"]
    (done,) = [t for t, kind, _ in lines if kind == "sail.set"]
    assert abs(done - 304) <= 10, done
    assert posts["master"].at is None


def test_a_post_taken_off_by_all_hands_called_at_the_sight_and_sent_for_sailed_to_the_end():
    """The lead's (C7) of 2026-11-14: the three roads by which a post's person leaves the deck that
    no test sailed, each with the fore course set by the watch and its post, sailed to the
    foresail set. **All hands called**: at 04:00 her larboard watch by night, the three and the
    master; "call all hands" 5 s on takes the master to the conn, three under half its seven:
    "Belayed setting the foresail: the master to the conn, all hands called.", taken up on that
    tick by the hands up and set at +178 s, the master never at it again. **At the sight**: at
    11:43 her larboard watch by day, the three, the cook and the master (five of seven); at 11:45
    the master goes up with the instrument for the noon sight and leaves the sheet, the four going
    on: "Only four hands to the foresail; the master at the sight.", set at +262 s. **Sent for**: at
    02:00 her starboard watch by night, the three and the mate; the captain goes below and sends
    for the mate, who leaves the work on the way: "Belayed setting the foresail: the mate sent
    for.", held (the three under half); the captain on deck again sends for the mate, who comes to
    the quarterdeck, and the work is taken up with the mate on that tick and set. Old (53c14457):
    the same roads held or left the work as now, the going on short unsaid."""
    # all hands called
    world = _her_world(4)
    world.run(30)
    n, start, posts = _set_the_fore_course(world)
    world.run(5)
    assert world.submit("call all hands").kind == "crew.order"
    world.run(400)
    lines = _lines(world, n, start)
    said = "Belayed setting the foresail: the master to the conn, all hands called."
    assert (6, "evolution.belayed", said) in lines, lines
    (done,) = [t for t, kind, _ in lines if kind == "sail.set"]
    assert abs(done - 178) <= 10, done
    assert posts["master"].at is None
    # at the sight
    world = _her_world(11, 43, watch=Watch.LARBOARD)
    n, start, posts = _set_the_fore_course(world)
    assert [h.post for h in world.ship.extra["evolutions"].instances[0].assignment.hands if h.post]
    world.run(600)
    lines = _lines(world, n, start)
    shorts = [text for _, kind, text in lines if kind == "evolution.short_handed"]
    assert "Only four hands to the foresail; the master at the sight." in shorts, shorts
    (done,) = [t for t, kind, _ in lines if kind == "sail.set"]
    assert abs(done - 262) <= 10, done
    # sent for
    world = _her_world(2)
    world.run(30)
    n, start, posts = _set_the_fore_course(world)
    (work,) = world.ship.extra["evolutions"].instances
    assert [h.post for h in work.assignment.hands if h.post] == ["mate"]
    world.run(5)
    assert world.submit("go below").kind == "captain.below"
    assert world.submit("send for the mate").kind != "order.rejected"
    world.run(120)
    lines = _lines(world, n, start)
    said = "Belayed setting the foresail: the mate sent for."
    assert [text for _, kind, text in lines if kind == "evolution.belayed"] == [said], lines
    assert work.paused
    assert world.submit("come on deck").kind == "captain.on_deck"
    assert world.submit("send for the mate").kind != "order.rejected"
    for _ in range(900):
        world.tick()
        if world.ship.sails["fore.course"].state is SailState.SET:
            break
    assert world.ship.sails["fore.course"].state is SailState.SET
    lines = _lines(world, n, start)
    assert [text for _, kind, text in lines if kind == "evolution.belayed"] == [said], lines


def test_the_old_mark_of_the_boats_call_loads_from_a_trunk_save_and_she_sails_as_on_the_trunk():
    """The lead's (C7) of 2026-11-14: the old mark's test on a world that goes on to finish. A real
    checkpoint written on the trunk at 1eea8d18 (`BOAT_CALLED`: the bilander at her eight, her
    larboard watch of two, saved the moment "go ashore" had called all hands to man the boat by
    package 109's own road, its mark `hands_called_for` on the boat's params) loads in this build
    with her eight (no watch for her posts to head) and the boat held up for the hands called, the
    mark read as this road's (`Instance.__setstate__`) and gone from her params; sailed 1,200 s on,
    she gives the trunk's own lines for the same 1,200 s from the same world, line for line: all
    hands, the boat manned by four, the hands piped down at once, the long-boat away at +401 s."""
    header, world = replay.read_checkpoint(BOAT_CALLED)
    crew = world.ship.extra["crew"]
    assert len(crew.sailors) == 8 and not getattr(crew, "post_watches", None)
    (boat,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "send_boat"]
    assert boat.held_up and boat.waiting and "hands_called_for" not in boat.params
    n, start = len(world.log), world.clock.tick
    world.run(1200)
    assert _lines(world, n, start) == BOAT_CALLED_TRUNK
    assert json.dumps(header["build"])  # written by another build than this


# -- (C8): the works by their names ----------------------------------------------------------------

# Every work whose subject is the ship, by the name the log gives it in hand (`Runner._doing`):
# the belayed lines, the captain's belay and its listing, the work the rest are at, the readings.
# Those named by their files (`doing:`) are marked; the rest are their verb's own gerund.
SHIP_WORK_NAMES = {
    "back_anchor": "backing the anchor",  # file
    "back_and_fill": "backing and filling",  # file
    "batten_down": "battening down",
    "box_off": "boxing off",
    "boxhaul": "boxhauling",
    "cast_loose_guns": "casting loose the guns",  # file
    "cat_and_fish_anchor": "catting and fishing the anchor",  # file
    "clear_for_action": "clearing for action",
    "come_to_anchor": "coming to anchor",
    "cross_topgallant_yards": "crossing topgallant yards",
    "fid_topmasts": "fidding topmasts",
    "fill_away": "filling away",
    "fother_sail": "fothering a sail over the leak",  # file
    "furl_all": "furling all sail",  # file
    "get_under_way": "getting under way",
    "grapple": "grappling",
    "haul_lines": "hauling the lines",
    "haul_nets": "hauling the nets",
    "haul_seine": "hauling the seine",
    "haul_trawl": "hauling the trawl",
    "heave_deep_sea_lead": "heaving the deep-sea lead",  # file
    "heave_in": "heaving in",
    "heave_lead": "heaving the lead",  # file
    "heave_log": "heaving the log",  # file
    "heave_mark": "heaving a mark",  # file
    "heave_short": "heaving short",
    "heave_to": "heaving to",
    "jury_mast": "rigging a jury mast",  # file
    "lay_out_kedge": "laying out the kedge",  # file
    "let_go_anchor": "letting go the anchor",  # file
    "lie_a_try": "lying a-try",  # file
    "loose_sails_to_dry": "loosing sails to dry",
    "make_signal": "making the signal",  # file
    "moor": "mooring",
    "plug_shot_hole": "plugging the shot holes",  # file
    "rig_preventers": "rigging preventers",
    "scud": "scudding",
    "secure_guns": "securing the guns",  # file
    "send_boat": "sending the boat",  # file
    "send_down_topgallant_masts": "sending down topgallant masts",
    "send_down_topgallant_yards": "sending down topgallant yards",
    "serve_small_arms": "serving small arms",
    "set_lines": "setting the lines",
    "set_up_rigging": "setting up the rigging",  # file
    "shoot_nets": "shooting the nets",
    "shoot_seine": "shooting the seine",
    "shoot_trawl": "shooting the trawl",
    "strike_topmasts": "striking topmasts",
    "sway_up_topgallant_masts": "swaying up topgallant masts",
    "tack": "tacking ship",
    "take_lunar": "taking a lunar",  # file
    "unmoor": "unmooring",
    "veer_cable": "veering the cable",  # file
    "wear": "wearing ship",
    "wear_short_round": "wearing short round",
    "weigh_anchor": "weighing anchor",
}


def test_every_work_on_the_ship_is_named_by_its_name_where_the_log_names_the_work_in_hand():
    """The lead's (C8) of 2026-11-14 at the cause's level: the log named the work in hand whose
    subject is the ship by its evolution's verb with an ending, and the verb of many is its id
    ("Belayed laying out kedge", "veering cable", "sending boat"). The name is now the file's own
    where the verb's would not be one (`doing:`, `registry.Evolution.doing`), read in the one place
    the work in hand is named (`Runner._doing`), so that every reader is served: the belayed
    lines, the captain's belay and its listing, the work the rest are at, the readings and the
    lookout's glass (`world.lookout._WORK_KINDS`: "sending the boat", a boat hoisting out or in).
    Every such work of the registry is in `SHIP_WORK_NAMES`, none an id with an ending. The
    infinitive the call, the waiting line and the short line give ("All hands! (to send boat)",
    "Only four hands to send boat") is the verb's (`Runner._describe`), and stays: package 109's
    truth 7-542 and its tests pin the call's words (the lead's ruling 10). Old (53c14457): the
    twenty-one marked "file" named by their ids ("laying out kedge", "heaving lead", "lying a
    try", "catting and fish anchor")."""
    world = make_world(7, HER, Scenario())
    runner = world.ship.extra["evolutions"]
    named = {}
    for eid, evo in sorted(registry.EVOLUTIONS.items()):
        if str(evo.applies_to.get("class")) != "ship":
            continue
        inst = Instance(evo=evo, subject=world.ship, subject_id=world.ship.name, params={})
        named[eid] = runner.doing(inst)
    assert named == SHIP_WORK_NAMES
    files = {
        eid
        for eid, evo in registry.EVOLUTIONS.items()
        if evo.doing and str(evo.applies_to.get("class")) == "ship"
    }
    assert len(files) == 21 and all(
        SHIP_WORK_NAMES[eid] == registry.get(eid).doing for eid in files
    )
    assert not [n for n in named.values() if "_" in n]
    sail = Instance(
        evo=registry.get("set_square"),
        subject=world.ship.sails["fore.topsail"],
        subject_id="fore.topsail",
        params={},
    )
    assert runner.doing(sail) == "setting the fore topsail"  # a part's work: its verb and its part
    with pytest.raises(registry.EvolutionFileError, match="the part is named after them"):
        registry.parse_evolution(
            {**_file_of("set_square"), "doing": "setting the sail"}, "set_square.yaml"
        )


# A part's work whose verb's gerund is no name (the whole-change review of 80e703c7, sailing-5): its
# file's words before the part's name (`doing:`). Every other part's work is its verb and its part.
PART_WORK_NAMES = {
    "cut_away_mast": ("main.mast", "cutting away the main mast"),
    "goose_wing": ("fore.course", "goose-winging the foresail"),
}


def test_every_work_on_a_part_is_named_by_a_name_where_the_log_names_the_work_in_hand():
    """The whole-change review of 80e703c7, sailing-5: (C8)'s cause at every evolution, a part's
    work among them. A part's work was named by its verb's gerund and its part, and where the verb
    is the id ("cut_away_mast", "goose_wing") that read "cutting away mast the main mast" (newly
    served by a post's leaving it: "Belayed cutting away mast the main mast: the master gone
    below.") and "goosing wing the foresail". Now a part's file gives the words before its part
    (`doing: cutting away`), read in the one place the work in hand is named (`Runner._doing`).
    Every part's work of the registry, on the first part of its class in the bilander, the topsail
    schooner or the 74, is named with no id's underscore and no verb of two words left as its id.
    Old (80e703c7): the two above."""
    worlds = [
        make_world(7, f"data/ships/{stem}.yaml", Scenario())
        for stem in ("bilander", "topsail-schooner", "seventy-four")
    ]
    seen = {}
    for eid, evo in sorted(registry.EVOLUTIONS.items()):
        cls = str(evo.applies_to.get("class"))
        if cls == "ship":
            continue
        for w in worlds:
            subject, sid = _subject(w.ship, cls)
            if subject is not None:
                break
        assert subject is not None, eid
        if eid in PART_WORK_NAMES:
            w, sid = worlds[0], PART_WORK_NAMES[eid][0]
            subject = w.ship.parts[sid]
        runner = w.ship.extra["evolutions"]
        words = runner.doing(Instance(evo=evo, subject=subject, subject_id=sid, params={}))
        seen[eid] = words
        assert "_" not in words, (eid, words)
        verb = evo.verb.replace("_", " ")
        if " " in verb:
            assert f"{verb} " not in f"{words} " or evo.doing, (eid, words)  # an id with an ending
    assert {eid: seen[eid] for eid in PART_WORK_NAMES} == {
        eid: name for eid, (_part, name) in PART_WORK_NAMES.items()
    }
    files = {eid for eid, evo in registry.EVOLUTIONS.items() if evo.doing}
    assert files - set(SHIP_WORK_NAMES) == set(PART_WORK_NAMES)


def _file_of(eid: str) -> dict:
    import yaml

    return yaml.safe_load((Path(registry.DATA_DIR) / f"{eid}.yaml").read_text(encoding="utf-8"))
