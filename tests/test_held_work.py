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

**The lead's last list of 2026-11-14, 8: what must still be true.** (C1)'s mend read the beginning's
check no more on a taking up, and what of it stands through the work was stated for three scripts
alone (`Script.standing`), so held work was taken up after the world had moved under it: a veer
held by the master going below, its anchor lost, veered the lost anchor's cable to fifty-six
fathoms. Every script a post can hold now states it, in its script or its file's `requires`, or is
named with the reason nothing in the world makes its beginning false while it lies held; the test at
that level holds each, moves the world and takes it up: refused in words, never run. **9: one road
for a work's words.** The file names its work once (`work:`), and both forms of its name are made
from it, read wherever a line names work; no line names a work by its evolution's id.

The figures are measured on the owner's machine (Windows 11, 2026-11-14) at seed 7; old is
53c14457, the branch before these mends, and 20a8e2e3 for the last list's two.
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
# The one of them said after the save that names the work the hands are wanted for, by the one road
# for a work's words since the lead's last list of 2026-11-14 (9): the trunk's and 20a8e2e3's named
# it by its evolution's id ("to send boat"), the file's words now ("to send the boat"); every tick,
# kind and other word as on the trunk. The call ("All hands! (to send boat)") was said on the trunk
# before the save was written, and is logged on the first tick as it was said (the ship's notes kept
# in the save).
BOAT_WORDS_MOVED = {
    "Only four hands to send boat; there are no more on deck.": (
        "Only four hands to send the boat; there are no more on deck."
    ),
}
QUIET = ("evolution.step", "wind.gust", "clock.bell")


def _lines(world, n: int, start: int) -> list[tuple[int, str, str]]:
    return [
        (e.tick - start, e.kind, e.text)
        for e in list(world.log)[n:]
        if not e.kind.startswith(QUIET)
    ]


# -- the cause's level: every scripted evolution, held and taken up again ------------------------


def _subject(ship, cls: str):
    """The first part of `ship` an evolution of `cls` applies to, or the ship herself; a sail of the
    class before a spar of it (a gaff sail for `trim_gaff_sheet`, not the gaff it is bent to: its
    file's `requires` read the sail since the lead's last list of 2026-11-14, 8)."""
    if cls == "ship":
        return ship, ship.name
    for sail in ship.sails.values():
        if sail.cls == cls:
            return sail, sail.id
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
        if any(c.text == "sail.state == set" for c in evo.requires):
            # what holds through a trim, its file's `requires` since the last list's 8: its sail set
            subject.state = SailState.SET
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
    hands, the boat manned by four, the hands piped down at once, the long-boat away at +401 s; the
    short line, said after the save, names the work in its words by the one road
    (`BOAT_WORDS_MOVED`, the lead's last list of 2026-11-14, 9), the trunk's id gone from it."""
    header, world = replay.read_checkpoint(BOAT_CALLED)
    crew = world.ship.extra["crew"]
    assert len(crew.sailors) == 8 and not getattr(crew, "post_watches", None)
    (boat,) = [i for i in world.ship.extra["evolutions"].instances if i.evo.id == "send_boat"]
    assert boat.held_up and boat.waiting and "hands_called_for" not in boat.params
    n, start = len(world.log), world.clock.tick
    world.run(1200)
    assert _lines(world, n, start) == [
        (t, kind, BOAT_WORDS_MOVED.get(text, text)) for t, kind, text in BOAT_CALLED_TRUNK
    ]
    assert json.dumps(header["build"])  # written by another build than this


# -- (C8) and the last list's 9: the works by their names, in both forms, by one road --------------

# Every work whose subject is the ship in both forms of its name: as an order to it is given, the
# words a line gives where it names the work the hands are wanted for ("All hands! (to send the
# boat)", "Not hands enough on deck to let go the anchor", "Only four hands to veer the cable"),
# and the gerund made from them, the work in hand ("Belayed laying out the kedge: ..."). Those
# whose file names the work (`work:`) are marked; the rest are their verb's own words.
SHIP_WORK_WORDS = {
    "back_anchor": ("back the anchor", "backing the anchor"),  # file
    "back_and_fill": ("back and fill", "backing and filling"),  # file
    "batten_down": ("batten down", "battening down"),
    "box_off": ("box off", "boxing off"),
    "boxhaul": ("boxhaul", "boxhauling"),
    "cast_loose_guns": ("cast loose the guns", "casting loose the guns"),  # file
    "cat_and_fish_anchor": ("cat and fish the anchor", "catting and fishing the anchor"),  # file
    "clear_for_action": ("clear for action", "clearing for action"),
    "come_to_anchor": ("come to anchor", "coming to anchor"),
    "cross_topgallant_yards": ("cross topgallant yards", "crossing topgallant yards"),
    "fid_topmasts": ("fid topmasts", "fidding topmasts"),
    "fill_away": ("fill away", "filling away"),
    "fother_sail": ("fother a sail over the leak", "fothering a sail over the leak"),  # file
    "furl_all": ("furl all sail", "furling all sail"),  # file
    "get_under_way": ("get under way", "getting under way"),
    "grapple": ("grapple", "grappling"),
    "haul_lines": ("haul the lines", "hauling the lines"),
    "haul_nets": ("haul the nets", "hauling the nets"),
    "haul_seine": ("haul the seine", "hauling the seine"),
    "haul_trawl": ("haul the trawl", "hauling the trawl"),
    "heave_deep_sea_lead": ("heave the deep-sea lead", "heaving the deep-sea lead"),  # file
    "heave_in": ("heave in", "heaving in"),
    "heave_lead": ("heave the lead", "heaving the lead"),  # file
    "heave_log": ("heave the log", "heaving the log"),  # file
    "heave_mark": ("heave a mark", "heaving a mark"),  # file
    "heave_short": ("heave short", "heaving short"),
    "heave_to": ("heave to", "heaving to"),
    "jury_mast": ("rig a jury mast", "rigging a jury mast"),  # file
    "lay_out_kedge": ("lay out the kedge", "laying out the kedge"),  # file
    "let_go_anchor": ("let go the anchor", "letting go the anchor"),  # file
    "lie_a_try": ("lie a-try", "lying a-try"),  # file
    "loose_sails_to_dry": ("loose sails to dry", "loosing sails to dry"),
    "make_signal": ("make the signal", "making the signal"),  # file
    "moor": ("moor", "mooring"),
    "plug_shot_hole": ("plug the shot holes", "plugging the shot holes"),  # file
    "rig_preventers": ("rig preventers", "rigging preventers"),
    "scud": ("scud", "scudding"),
    "secure_guns": ("secure the guns", "securing the guns"),  # file
    "send_boat": ("send the boat", "sending the boat"),  # file
    "send_down_topgallant_masts": ("send down topgallant masts", "sending down topgallant masts"),
    "send_down_topgallant_yards": ("send down topgallant yards", "sending down topgallant yards"),
    "serve_small_arms": ("serve small arms", "serving small arms"),
    "set_lines": ("set the lines", "setting the lines"),
    "set_up_rigging": ("set up the rigging", "setting up the rigging"),  # file
    "shoot_nets": ("shoot the nets", "shooting the nets"),
    "shoot_seine": ("shoot the seine", "shooting the seine"),
    "shoot_trawl": ("shoot the trawl", "shooting the trawl"),
    "strike_topmasts": ("strike the topmasts", "striking the topmasts"),  # file
    "sway_up_topgallant_masts": ("sway up topgallant masts", "swaying up topgallant masts"),
    "tack": ("tack ship", "tacking ship"),  # file
    "take_lunar": ("take a lunar", "taking a lunar"),  # file
    "unmoor": ("unmoor", "unmooring"),
    "veer_cable": ("veer the cable", "veering the cable"),  # file
    "wear": ("wear ship", "wearing ship"),  # file
    "wear_short_round": ("wear short round", "wearing short round"),
    "weigh_anchor": ("weigh anchor", "weighing anchor"),
}
SHIP_WORK_FILES = 24  # those marked "file"
# A part's work whose verb is no name of it (the whole-change review of 80e703c7, sailing-5, and
# the last list's 9): the words before the part's name in both forms, on the part named; the
# clearing of a wreck by its own words (the review of 0dcdb8cf, F4: with none of its own it was
# named by its verb, "cutting away the fore mast", another work's, as the lead's list found it).
# Every other part's work is its verb's own words and its part.
PART_WORK_WORDS = {
    "cut_away_mast": ("main.mast", "cut away the main mast", "cutting away the main mast"),
    "goose_wing": ("fore.course", "goose-wing the foresail", "goose-winging the foresail"),
    "clear_wreck": (
        "fore.mast",
        "clear away the wreck of the fore mast",
        "clearing away the wreck of the fore mast",
    ),
}
PART_WORK_FILES = {"cut_away_mast", "goose_wing", "clear_wreck"}


def _three_worlds():
    return [
        make_world(7, f"data/ships/{stem}.yaml", Scenario())
        for stem in ("bilander", "topsail-schooner", "seventy-four")
    ]


def _instance(world, eid: str):
    """An instance of the evolution on a subject of its class in `world` (`PART_WORK_WORDS`' part
    where it names one), made as `Runner.start` makes it: its script, its holds and its want."""
    from freesail.crew import hands

    ship = world.ship
    runner = ship.extra["evolutions"]
    evo = registry.get(eid)
    if eid in PART_WORK_WORDS:
        sid = PART_WORK_WORDS[eid][0]
        subject = ship.parts[sid]
    else:
        subject, sid = _subject(ship, str(evo.applies_to.get("class")))
    params = dict(evo.params)
    inst = Instance(evo=evo, subject=subject, subject_id=sid, params=params)
    runner._counter += 1
    inst.order = runner._counter
    if evo.script is not None:
        inst.script = SCRIPTS[evo.script](ship, params, runner._timing(ship, evo))
    inst.holds = runner._holds(ship, inst)
    inst.want = hands.CrewRequest.from_mapping(runner._crew_line(ship, evo))
    return inst


def _world_for(worlds, eid: str):
    evo = registry.get(eid)
    if eid in PART_WORK_WORDS:
        return worlds[0]
    for w in worlds:
        if _subject(w.ship, str(evo.applies_to.get("class")))[0] is not None:
            return w
    raise AssertionError(eid)


def _words_of(world, eid: str, inst) -> tuple[str, str]:
    """The work's two forms as this test pins them (`SHIP_WORK_WORDS`, `PART_WORK_WORDS`), and for
    every other part's work its verb's words and its part."""
    if eid in SHIP_WORK_WORDS:
        return SHIP_WORK_WORDS[eid]
    if eid in PART_WORK_WORDS:
        return PART_WORK_WORDS[eid][1:]
    from freesail.evolutions.runner import gerund_words, part_name

    verb = registry.get(eid).verb.replace("_", " ")
    to = f"{verb} the {part_name(world.ship, inst.subject_id)}"
    return to, gerund_words(to)


def _ids_left(text: str, eid: str, words: tuple[str, str]) -> list[str]:
    """The ids a line names (the last list's 9): any underscore of an id, and the work's verb in
    words (its file's id, where the two are one) where they are not its words, once its words in
    both forms are taken out of the line ("veer cable" in "Only four hands to veer cable"; "cut
    away mast" in "to cut away mast the main mast"; nothing of "heave to" in "Not hands enough on
    deck to heave to", nor of "weigh anchor" in "Not hands enough on deck to weigh anchor")."""
    import re

    verb = registry.get(eid).verb.replace("_", " ")
    rest = text.lower()
    for w in sorted(words, key=len, reverse=True):
        rest = rest.replace(w.lower(), " ")
    found = ["_"] if "_" in text else []
    # a verb of one word is a word, and one in the work's own words is its own ("furl all sail")
    if " " in verb and not any(verb in w for w in words):
        if re.search(rf"\b{re.escape(verb)}\b", rest):
            found.append(verb)
    return found


def test_every_work_is_named_by_one_road_in_both_forms_where_a_line_names_the_work():
    """The lead's (C8) and the last list's 9 of 2026-11-14 at the cause's level: a work's words
    lived in two places, the file's gerund (`doing:`, read for the work in hand) and the verb (read
    for the infinitive a line gives where it names the work hands are wanted for), so that half the
    lines named the work by its id. Now the file names it once, as an order to it is given
    (`work:`), and both forms are made from that one road (`Runner._describe`, the infinitive, and
    `Runner._doing` its gerund, `runner.gerund_words`). Every evolution of the registry, on the
    first subject of its class in the bilander, the topsail schooner or the 74: whose subject is the
    ship in both forms as `SHIP_WORK_WORDS` pins them, a part's work named as `PART_WORK_WORDS`
    pins it or by its verb's own words, and none of either form an id. Old (20a8e2e3): the
    infinitive the verb's, "veer cable", "let go anchor", "lay out kedge", "lie a try", "send boat",
    "cut away mast the main mast", "goose wing the foresail"; the gerunds as now."""
    worlds = _three_worlds()
    seen = {}
    for eid in sorted(registry.EVOLUTIONS):
        w = _world_for(worlds, eid)
        inst = _instance(w, eid)
        runner = w.ship.extra["evolutions"]
        got = (runner._describe(inst), runner.doing(inst))
        seen[eid] = got
        assert got == _words_of(w, eid, inst), (eid, got)
        assert _ids_left(" / ".join(got), eid, _words_of(w, eid, inst)) == [], (eid, got)
    ship_works = {e for e, v in registry.EVOLUTIONS.items() if v.applies_to.get("class") == "ship"}
    assert ship_works == set(SHIP_WORK_WORDS)
    # a part's work not pinned is named by a verb that is not its id of more than one word
    for eid in set(registry.EVOLUTIONS) - ship_works - set(PART_WORK_WORDS):
        assert "_" not in eid or registry.get(eid).verb != eid, eid
    files = {e for e, ev in registry.EVOLUTIONS.items() if getattr(ev, "work", None)}
    assert len(files - PART_WORK_FILES) == SHIP_WORK_FILES and PART_WORK_FILES <= files
    assert seen["clear_wreck"] == (
        "clear away the wreck of the fore mast",
        "clearing away the wreck of the fore mast",
    )
    assert seen["strike_topmasts"] == ("strike the topmasts", "striking the topmasts")


def test_no_line_that_names_a_work_names_it_by_its_id():
    """The last list's 9 of 2026-11-14: the sweep of every evolution's served lines for an id. For
    every evolution of the registry, on the first subject of its class in the bilander, the topsail
    schooner or the 74, every line the runner serves that names the work, made by the runner's own
    roads: the waiting line (`_waiting_line`), the short line (`_note_short`), the belayed line
    (`_hold`), the call for all hands (`_call_all_hands`, piped down after), the work that follows
    another (`Runner.start` behind a work holding what it holds), and the work in hand as the
    readings and the console give it (`Runner.doing`); and every line of its own file (its
    outcomes, its states' lines, its steps' lines and its conditions' reasons). Each names the work
    in its words, both forms by the one road, and none names an id: no underscore of an id, and no
    id or verb in words that are not the work's own. Old (20a8e2e3): "Only four hands to veer
    cable", "Not hands enough on deck to let go anchor", "All hands! (to lie a try)", "'Lay out
    kedge' will follow ...", "Not hands enough on deck to cut away mast the main mast", "Could not
    veer cable: ..." (the veer's own file), and their like for every work whose file names it."""
    from freesail.crew import hands
    from freesail.evolutions.runner import part_name

    worlds = _three_worlds()
    bad: dict[str, list[tuple[str, list[str]]]] = {}
    unnamed: dict[str, list[str]] = {}
    for eid in sorted(registry.EVOLUTIONS):
        w = _world_for(worlds, eid)
        ship = w.ship
        runner, crew = ship.extra["evolutions"], ship.extra["crew"]
        routine = ship.extra["routine"]
        inst = _instance(w, eid)
        to, ing = _words_of(w, eid, inst)
        on_the_ship = isinstance(inst.subject, type(ship))
        ship.drain_notes()
        got = hands.Assignment(inst.inst_id, wanted=7, available=2)
        named = [(runner._waiting_line(ship, inst, got), to)]
        got.hands = list(crew.sailors[:2])
        runner._note_short(ship, inst, got)
        runner._hold(ship, crew, inst, "stations for wearing ship", {"for": "wear"})
        runner._call_all_hands(ship, inst, crew)
        routine.pipe_down()
        said = {kind: text for _, kind, text, _, _ in ship.drain_notes()}
        short = said["evolution.short_handed"]
        named += [
            (short, to if on_the_ship else f"to the {part_name(ship, inst.subject_id)}"),
            (said["evolution.belayed"], ing),
            (said["crew.all_hands"], to),
            (runner.doing(inst), ing),
        ]
        if inst.holds:
            from freesail.evolutions.runner import Instance as _I

            blocker = _I(
                evo=registry.get("batten_down"), subject=ship, subject_id=ship.name, params={}
            )
            blocker.holds, blocker.waiting = set(inst.holds), False
            runner.instances.append(blocker)
            follows = runner.start(ship, eid, inst.subject_id, dict(registry.get(eid).params))
            runner.instances[:] = [i for i in runner.instances if i is not blocker]
            runner.instances[:] = [i for i in runner.instances if i.evo.id != eid]
            named.append((follows, to))
        for text, words in named:
            if words.lower() not in text.lower():
                unnamed.setdefault(eid, []).append(text)
            left = _ids_left(text, eid, (to, ing))
            if left:
                bad.setdefault(eid, []).append((text, left))
        for text in _file_lines(registry.get(eid)):
            left = _ids_left(_unbraced(text), eid, (to, ing))
            if left:
                bad.setdefault(eid, []).append((text, left))
    assert bad == {}, bad
    assert unnamed == {}, unnamed


def _unbraced(text: str) -> str:
    import re

    return re.sub(r"\{[^}]*\}", "", text)


def _file_lines(evo) -> list[str]:
    """Every line of an evolution's own file: its outcomes and their states' lines, its steps'
    lines and its conditions' reasons, as written ({sail} and its like unfilled)."""
    out = []
    for name in ("on_start", "on_complete", "on_fail", "on_refused"):
        o = getattr(evo, name)
        if o is not None:
            out += [o.log, *o.from_state.values()]
    out += [s.log for s in evo.steps if s.log]
    out += [c.reason for c in evo.preconditions + evo.requires]
    return [t for t in out if t]


def test_a_files_old_key_for_the_gerund_is_refused_in_words():
    """The last list's 9: the work is named once in its file (`work:`), and the gerund's old key
    (`doing:`, a second source of the same words) is refused in words, so that no file names its
    work twice; a part's work gives the words before its part."""
    with pytest.raises(registry.EvolutionFileError, match="the work is named once"):
        registry.parse_evolution({**_file_of("veer_cable"), "doing": "veering the cable"}, "x.yaml")
    with pytest.raises(registry.EvolutionFileError, match="the part is named after them"):
        registry.parse_evolution(
            {**_file_of("set_square"), "work": "set the sail"}, "set_square.yaml"
        )


def _file_of(eid: str) -> dict:
    import yaml

    return yaml.safe_load((Path(registry.DATA_DIR) / f"{eid}.yaml").read_text(encoding="utf-8"))


# -- the last list's 8: held work taken up after the world has moved under it --------------------

# The Torbay world's merchant brig (a stream anchor, a kedge, her master and mate working with the
# watch), the best bower let go and 600 s on, checkpointed once; the bilander (her settee, a lug)
# and the 74 (her mizen lateen) in the default scenario, for the trims of their sails.
BRIG = "data/ships/merchant-brig.yaml"


@pytest.fixture(scope="module")
def standing_worlds(tmp_path_factory):
    from freesail.world.scenarios import load_scenario, make_scenario_world
    from tests.test_mends_109 import TORBAY

    d = tmp_path_factory.mktemp("standing")
    w = make_scenario_world(load_scenario(TORBAY), ship=BRIG)
    w.submit("let go the anchor")
    w.run(600)
    out = {"brig": replay.write_checkpoint(w, d / "brig.checkpoint")}
    for key, stem in (("bilander", "bilander"), ("74", "seventy-four")):
        out[key] = replay.write_checkpoint(
            make_world(7, f"data/ships/{stem}.yaml", Scenario()), d / f"{key}.checkpoint"
        )
    return out


def _anchor(ship, name: str):
    return next(a for a in _tackle(ship).anchors if a.name == name)


def _lost(anchor) -> None:
    """The cable parted as the physics parts it (`physics.anchor`): the anchor on the bottom with
    its buoy, the cable's load gone."""
    from freesail.ship.parts import AnchorState

    anchor.state = AnchorState.LOST
    anchor.cable_load_kn = 0.0
    anchor.taut = anchor.dragging = False


def _set_sail(world, sid):
    world.ship.sails[sid].state = SailState.SET


def _nothing(world, sid):
    return None


def _hoisted(world, sid):
    from freesail.world.signals import NOT_YET, Hoist, locker_of

    h = locker_of(world.ship).hoist(
        Hoist(book="numerary", meaning="test", by="the ship", since=0, breaks_out=NOT_YET)
    )
    return {"hoist_key": h.key, "hoists": 1, "words": "the signal"}


def _aweigh(world, sid):
    from freesail.ship.parts import AnchorState

    _anchor(world.ship, "the small bower").state = AnchorState.AWEIGH


def _off_soundings(world) -> None:
    """She has drifted off soundings while the work lay held: the water's depth as the World keeps
    it (`World._tick_tide`, once a minute from the chart), none."""
    world.ship.extra["water_depth_m"] = None
    world._tick_tide = lambda: None


def _sheet_parted(world, sid) -> None:
    from freesail.ship.parts import LineState

    sail = world.ship.sails[sid]
    world.ship.sheets_of(sail)[0].state = LineState.PARTED


# Every script a post can hold whose beginning the world can make false while it lies held, each
# with the world moved so that what must still be true is not, and the line its taking up says:
# (script's evolution, the move): (world, subject or None for the ship, what readies the world for
# its beginning and gives its params, the move, the line, what its running on would have done).
def _scope(world):
    return _anchor(world.ship, "the best bower").scope_m


STANDS = {
    ("veer_cable", "the anchor lost"): (
        "brig",
        None,
        lambda w, s: {"fathoms": 20.0},
        lambda w: _lost(_anchor(w.ship, "the best bower")),
        "Could not veer the cable: no anchor is down to veer on.",
        "veers the lost anchor's cable",
    ),
    ("back_anchor", "the anchor lost"): (
        "brig",
        None,
        _nothing,
        lambda w: _lost(_anchor(w.ship, "the best bower")),
        "Could not back the best bower: no anchor is down to back.",
        "lets the stream go",
    ),
    ("back_anchor", "the stream let go"): (
        "brig",
        None,
        _nothing,
        lambda w: setattr(_anchor(w.ship, "the stream anchor"), "state", _down()),
        "Could not back the best bower: the stream anchor is down.",
        "lets the stream go",
    ),
    ("cat_and_fish_anchor", "the anchor let go again"): (
        "brig",
        None,
        _aweigh,
        lambda w: setattr(_anchor(w.ship, "the small bower"), "state", _down()),
        "Could not cat and fish the small bower: the small bower is down.",
        "cats it",
    ),
    ("lay_out_kedge", "off soundings"): (
        "brig",
        None,
        lambda w, s: {"toward_deg": 90.0},
        _off_soundings,
        "Could not lay out the kedge: no bottom here to lay a kedge in.",
        "lays the kedge out",
    ),
    ("let_go_anchor", "aground"): (
        "brig",
        None,
        lambda w, s: {"anchor": "small bower"},
        lambda w: w.ship.extra.__setitem__("aground", True),
        "Could not let go the small bower: she is aground.",
        "lets it go",
    ),
    ("cut_away_mast", "the mast carried away"): (
        "brig",
        "main.mast",
        _nothing,
        lambda w: setattr(w.ship.spars["main.mast"], "wrecked", True),
        "Could not cut away the main mast: the main mast is carried away already; clear the wreck.",
        "cuts it away",
    ),
    ("make_signal", "the hoist hauled down"): (
        "brig",
        None,
        _hoisted,
        lambda w: _locker(w).haul_down(w.clock.tick),
        "Could not make the signal: no signal is bent on.",
        "runs the hoist up",
    ),
    ("trim_jib_sheet", "the sail blown out"): (
        "brig",
        "jib",
        _set_sail,
        lambda w: setattr(w.ship.sails["jib"], "state", SailState.BLOWN_OUT),
        "Could not trim the jib sheet: the jib is blown out; there is no sail to trim.",
        "trims it",
    ),
    ("trim_jib_sheet", "the sheet parted"): (
        "brig",
        "jib",
        _set_sail,
        lambda w: _sheet_parted(w, "jib"),
        "Could not trim the jib sheet: the starboard jib sheet is parted and must be rove afresh.",
        "trims it",
    ),
    ("trim_gaff_sheet", "the sail blown out"): (
        "brig",
        "main.spanker",
        _set_sail,
        lambda w: setattr(w.ship.sails["main.spanker"], "state", SailState.BLOWN_OUT),
        "Could not trim the spanker sheet: the spanker is blown out; there is no sail to trim.",
        "trims it",
    ),
    ("trim_lug_sheet", "the sail blown out"): (
        "bilander",
        "main.settee",
        _set_sail,
        lambda w: setattr(w.ship.sails["main.settee"], "state", SailState.BLOWN_OUT),
        "Could not trim the mainsail sheet: the mainsail is blown out; there is no sail to trim.",
        "trims it",
    ),
    ("trim_lateen_sheet", "the sail blown out"): (
        "74",
        "mizzen.course",
        _set_sail,
        lambda w: setattr(w.ship.sails["mizzen.course"], "state", SailState.BLOWN_OUT),
        "Could not trim the mizzen course sheet: the mizzen course is blown out; there is no sail "
        "to trim.",
        "trims it",
    ),
}
# The scripts a post can hold whose beginning nothing in the world makes false while they lie held:
# their `Script.standing` is the base's None, and why.
NOTHING_STANDS = {
    "batten_down": "the hatches are battened or opened by this work alone, which holds them",
    "cast_loose_guns": "begun at quarters alone (its check), where no post is counted",
    "grapple": "the grapnels are thrown as it begins; held, nothing is left of it but its time",
    "heave_mark": "it reads a world with a chart, which nothing takes away; its end reads it again",
    "plug_shot_hole": "its own going plugs the holes and spends the plugs, holding the carpenter; "
    "holes the world adds are more work, not less",
    "secure_guns": "its own going secures the guns; none is cast loose but by work at quarters",
    "send_boat": "it reads a port and a boat, which nothing takes away; it holds the boat",
    "serve_small_arms": "the arms are served out by this work alone, which holds them",
    "set_lines": "the gear is shot and hauled by the fishing works alone, which hold it",
    "shoot_nets": "the gear is shot and hauled by the fishing works alone, which hold it",
    "shoot_seine": "the gear is shot and hauled by the fishing works alone, which hold it",
    "shoot_trawl": "the gear is shot and hauled by the fishing works alone, which hold it",
}


def _down():
    from freesail.ship.parts import AnchorState

    return AnchorState.DOWN


def _locker(world):
    from freesail.world.signals import locker_of

    return locker_of(world.ship)


def _scripts_a_post_can_hold() -> set[str]:
    """Every scripted evolution a post may be counted for (`Runner._working_posts`, the lead's
    ruling 11 of 2026-11-13), by the runner's own rule on the merchant brig, her watches' whole
    made nought so that any number of hands is more than they hold: numbered work on deck, no hand
    aloft, no manoeuvre, not at quarters, all hands not called."""
    from freesail.crew import hands

    w = make_world(7, BRIG, Scenario())
    runner, crew = w.ship.extra["evolutions"], w.ship.extra["crew"]
    runner._watch_whole = lambda crew, watch: 0
    out = set()
    for eid, evo in registry.EVOLUTIONS.items():
        if evo.script is None:
            continue
        params = dict(evo.params)
        inst = Instance(evo=evo, subject=w.ship, subject_id=w.ship.name, params=params)
        inst.script = SCRIPTS[evo.script](w.ship, params, runner._timing(w.ship, evo))
        inst.want = hands.CrewRequest.from_mapping(runner._crew_line(w.ship, evo))
        if runner._working_posts(crew, inst, named=True):
            out.add(eid)
    return out


def test_every_script_a_post_can_hold_states_what_must_still_be_true_or_why_nothing_need():
    """The lead's last list of 2026-11-14, 8, the sweep: every script a post can hold (by the
    runner's own rule, `_scripts_a_post_can_hold`) is either one whose beginning the world can make
    false while it lies held, which states what must still be true (`Script.standing`, or its file's
    `requires`) and is tried by the test after, or one whose beginning nothing in the world makes
    false while it lies held, named here with its reason and keeping the base's None. Twenty-three
    scripts: the reader's four (the veer, backing the anchor, the kedge, catting and fishing), the
    three given before (the letting go, the cutting away; the fish wants hands aloft, so no post
    holds it), and the sweep's own five (the signal, its hoist hauled down by the locker, and the
    four trims, their sail and sheet said as preconditions, read as they begin alone)."""
    from freesail.evolutions.scripts import Script

    can = _scripts_a_post_can_hold()
    tried = {eid for eid, _ in STANDS}
    assert can == tried | set(NOTHING_STANDS), (can - tried - set(NOTHING_STANDS), tried - can)
    assert not tried & set(NOTHING_STANDS)
    for eid in tried:  # each states what must still be true, in its script or in its file
        evo = registry.get(eid)
        assert SCRIPTS[evo.script].standing is not Script.standing or evo.requires, eid
    for eid in NOTHING_STANDS:
        evo = registry.get(eid)
        assert SCRIPTS[evo.script].standing is Script.standing, eid
        assert not evo.requires, eid


@pytest.mark.parametrize("case", sorted(STANDS), ids=[f"{e}-{m}" for e, m in sorted(STANDS)])
def test_every_script_a_post_can_hold_held_and_the_world_moved_is_refused_and_never_run(
    standing_worlds, case
):
    """The lead's last list of 2026-11-14, 8, at the cause's level: held work was taken up after the
    world had moved under it (C1's mend read the beginning's check no more, and what of it stands
    through the work was stated for three scripts alone). Every script a post can hold whose
    beginning the world can make false while it lies held: begun with all hands up, held as a post's
    leaving holds it (`Runner._hold`, the pause's one road), the world moved so that what must still
    be true is not, and taken up with hands enough (`Runner._try_resume`): refused in words (its
    `on_fail`, the beginning's words for what is not so), its hands let go, gone from the work, its
    check never read again, and never run (400 s on, nothing of its going done; the kedge's boat in
    the ship again). Old (20a8e2e3): the veer veered the lost anchor's cable, the stream went down
    beside a lost bower, the kedge was laid out off soundings, the small bower let go again was
    catted, the signal hauled down was run up, and the trims trimmed a sail blown out and a parted
    sheet; the letting go and the cutting away were refused as here."""
    eid, _move = case
    where, sid, prepare, move, said, _ran = STANDS[case]
    world = replay.read_checkpoint(standing_worlds[where])[1]
    ship = world.ship
    runner, crew = ship.extra["evolutions"], ship.extra["crew"]
    assert world.submit("call all hands").kind == "crew.order"
    world.run(120)
    params = prepare(world, sid) or {}
    runner.start(ship, eid, sid or ship.name, params)
    (inst,) = [i for i in runner.instances if i.evo.id == eid]
    assert not inst.waiting and inst.assignment is not None, inst.waiting_for
    world.run(5)
    read: list[str] = []
    check = inst.script.check
    inst.script.check = lambda words: read.append("read") or check(words)
    runner._hold(ship, crew, inst, "the master gone below", {"for": "post", "post": "master"})
    n = len(world.log)
    move(world)
    before = _effect(world, eid, sid)
    world.tick()
    lines = [(e.kind, e.text) for e in list(world.log)[n:] if not e.kind.startswith(QUIET)]
    assert ("evolution.failed", said) in lines, lines
    assert inst not in runner.instances
    assert not [s for s in crew.sailors if s.at == inst.inst_id]
    assert read == []
    world.run(400)
    assert _effect(world, eid, sid) == before, (eid, "ran on")
    done = registry.get(eid).on_complete.kind
    assert not [k for k, _ in lines if k == done]
    if eid == "lay_out_kedge":
        assert not world.dealings.boat.away  # the boat in the ship again


ANCHOR_WORKS = (
    "veer_cable",
    "back_anchor",
    "cat_and_fish_anchor",
    "lay_out_kedge",
    "let_go_anchor",
)


def _effect(world, eid: str, sid: str | None):
    """What the work's going changes, read before and after its taking up."""
    ship = world.ship
    tackle = _tackle(ship)
    if eid in ANCHOR_WORKS:
        return [(a.name, a.state, round(a.scope_m, 3)) for a in tackle.anchors]
    if eid == "cut_away_mast":
        return sorted(s.id for s in ship.spars.values() if s.wrecked)
    if eid == "make_signal":
        return [(h.key, h.breaks_out) for h in _locker(world).made]
    sail = ship.sails[sid]
    return [(ln.id, ln.state, round(ln.hauled, 4)) for ln in ship.sheets_of(sail)]


def test_a_veer_held_by_the_master_going_below_and_its_anchor_lost_is_refused_when_taken_up(
    held_worlds,
):
    """The reader's own case (the lead's last list of 2026-11-14, 8), sailed: her nine at anchor in
    Torbay, her larboard watch's three and the master veering twenty fathoms on the best bower; the
    master goes below 8 s on ("Belayed veering the cable: the master gone below.", three under half
    the veer's eight), the best bower is lost at +68 s while the work lies held (its cable parted,
    as the physics parts it), and the master comes on deck at +130 s: the veer is taken up at
    +131 s and refused in cda12ec9's words, "Could not veer the cable: no anchor is down to veer
    on." (its head the one road's, "veer cable" at cda12ec9), nothing veered. Old (20a8e2e3):
    taken up and run on, "Veered to fifty-six fathoms on the best bower." at +203 s, the lost
    anchor's scope grown from 38.33 fathoms at its loss to 56.32."""
    world = _held_world(held_worlds, "anchored")
    best = _anchor(world.ship, "the best bower")
    n, start = len(world.log), world.clock.tick
    assert world.submit("veer 20 fathoms").kind == "order.accepted"
    world.run(8)
    assert world.submit("go below").kind == "captain.below"
    world.run(60)
    _lost(best)
    scope = best.scope_m
    world.run(62)
    assert world.submit("come on deck").kind == "captain.on_deck"
    world.run(120)
    lines = _lines(world, n, start)
    said = [(t, k, x) for t, k, x in lines if k in ("evolution.belayed", "evolution.failed")]
    assert said[0] == (9, "evolution.belayed", "Belayed veering the cable: the master gone below.")
    refused = "Could not veer the cable: no anchor is down to veer on."
    assert said[1] == (131, "evolution.failed", refused), said
    assert not [x for _, k, x in lines if k == "cable.veered"], lines
    assert best.scope_m == scope
    assert not world.ship.extra["evolutions"].instances


def test_the_library_says_when_a_works_conditions_are_read_as_the_runner_reads_them():
    """The review of 0dcdb8cf, F5. The cause: the agents' library worded every file's `requires`
    as "It stops when", the step list's rule (read before every step), for scripted work too, whose
    `requires` the runner reads as it begins and as it is taken up again after a belay and never
    while it runs (`Runner._try_resume`); so that the four trims, their conditions moved into
    `requires` by the last list's 8, were said to stop when their sail is not set, and a trim runs
    on with its sail blown out (and `bend_sail` and `shift_sail` the same before). Mended in the
    library's one rule for an evolution's text (`agents.tools._evolution_text`): every evolution of
    the registry with `requires`, a script's in its own words, a step list's as before; and the
    spanker's trim on the merchant brig, its sail blown out at a twentieth done, ends trimmed, as
    the words now say. Old (0dcdb8cf): "It stops when: the {sail} is {state}; there is no sail to
    trim; {parted}." for each trim; 20a8e2e3, "It is refused when", the conditions then
    preconditions."""
    from freesail.agents import tools as T

    scripted = "It is refused, as it begins or as it is taken up again after a belay, when: "
    kinds = {True: 0, False: 0}
    for eid, evo in sorted(registry.EVOLUTIONS.items()):
        if not evo.requires:
            continue
        text = T._evolution_text(evo)
        kinds[bool(evo.script)] += 1
        if evo.script:
            assert scripted in text and "It stops when" not in text, eid
        else:
            assert "It stops when: " in text and scripted not in text, eid
    assert kinds[True] == 6 and kinds[False] > 30, kinds
    trim = T._evolution_text(registry.get("trim_gaff_sheet"))
    assert f"{scripted}the {{sail}} is {{state}}; there is no sail to trim; {{parted}}." in trim
    world = make_world(7, "data/ships/merchant-brig.yaml", Scenario())
    ship = world.ship
    sail = ship.sails["main.spanker"]
    sail.state = SailState.SET
    world.submit("call all hands")
    world.run(60)
    runner = ship.extra["evolutions"]
    runner.start(ship, "trim_gaff_sheet", "main.spanker", {"angle_deg": 40.0})
    world.run(3)
    (inst,) = runner.instances
    assert 0.0 < inst.script.progress < 0.1
    n = len(world.log)
    sail.state = SailState.BLOWN_OUT
    world.run(200)
    said = [(e.kind, e.text) for e in list(world.log)[n:] if e.kind.startswith(("sail.", "evol"))]
    assert [k for k, _ in said] == ["sail.trimmed"], said
