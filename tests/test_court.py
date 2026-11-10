"""The court martial, the new command and the adversarial seat's refusal (spec M7 §20; package
74, step 6; the design in `docs/design/Design-Prizes.md` §6 and §7): the court as the director's
proceeding at a place of the port, its questions through the channel and the accused's own words,
the log of the action read, the verdict journaled and read as the court's; a new command written
as a scenario under the saves with the record and the followers; a seat at the captain of a hull
adversarial to a human refused in words behind the flag."""

from __future__ import annotations

import json
from types import SimpleNamespace

import pytest

from freesail.world import captive as C
from freesail.world import court as CM
from freesail.world import orders as WO
from freesail.world import prizes as P
from freesail.world import seats
from tests.test_brains import put, world_at
from tests.test_captive import BREST_ROAD, OFF_BREST, _kinds, _struck_to_a_crewed_frigate
from tests.test_director import SEATED, directed, granted


def _landed_at_brest():
    """The player struck to a French frigate in Brest's road, carried in and landed to the
    commissaire with his officers prisoners in the prize (the captive tests' road)."""
    w, enemy = _struck_to_a_crewed_frigate(position=BREST_ROAD, her_goal=OFF_BREST)
    out = enemy.captain.give("come to an anchor", why="the prisoners landed")
    assert out.kind != "order.rejected", out.text
    for _ in range(10):
        w.run(60)
        if enemy.dealings.in_port() is not None:
            break
    for _ in range(3):
        w.run(60)
        if _kinds(enemy.log, "prize.prisoners_landed"):
            break
    assert _kinds(enemy.log, "prize.prisoners_landed")
    return w, enemy


@pytest.mark.slow
def test_the_court_martial_sits_by_the_form_hears_the_accused_reads_the_log_and_gives_its_verdict(
    tmp_path,
):
    """The design's §7.1 (truth 7-364): the captive landed at Brest is exchanged at Falmouth
    by the director's form (doubted within a day of his landing, performed with a reason; a
    prisoner no more, the exchange in his record), the court sat on him there by the form
    (refused for a man who lost no ship, doubted at a port not his nation's), its place made
    at the port and he before it; the president's question through `say as`, heard at the
    place; his answer his own, `say to the court: ...`; the log of the action read by the judge
    advocate; the verdict a world order journaled in the inputs, the play log carrying the
    sentence read and never the order, his record keeping the loss, the court and the
    verdict; the court risen, its place and its officers gone. Then (§7.2, truth 7-365) a new
    command written as a scenario under the saves with his name, his follower and the record,
    loaded by the loader and begun, the record read aboard the new ship."""
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    w, enemy = _landed_at_brest()
    me = C.captive_person(w)
    assert me is not None and me.port == "brest" and me.ashore_at == "agent_for_prisoners"
    ship_name = w.players.ship.name  # the prompt follows the captive aboard the captor
    losses = [e for e in CM.record_of(me) if e["kind"] == "loss"]
    assert len(losses) == 1 and losses[0]["ship_name"] == ship_name and losses[0]["command"]
    lt = next(p for p in w.players.people.people if p.role == "first lieutenant")
    assert any(e["kind"] == "loss" and not e["command"] for e in CM.record_of(lt))
    # the exchange: doubted within a day of his landing, performed with a reason
    doubt = WO.doubt(w, WO.parse('person: "Captain Bowen" is exchanged at Falmouth'))
    assert doubt is not None and "hours ago" in doubt
    e = w.world_order(
        'person: "Captain Bowen" is exchanged at Falmouth [reason: the agents\' lists]', "the test"
    )
    assert e.data.get("result") == "done", e.text
    assert C.captive_of(w) is None and me.port == "falmouth" and me.ashore_at == "quay"
    assert not me.aboard and not me.confined_to and me.where == "shore"
    assert CM.record_of(me)[-1]["kind"] == "exchanged"
    e = w.world_order('person: "Captain Bowen" is exchanged at Falmouth', "the test")
    assert e.data.get("result") != "done" and "is no prisoner" in e.text
    # the court: refused for a man who lost no ship, doubted at a port not his nation's
    other = next(p for p in enemy.people.people if p.role == "captain")
    e = w.world_order(
        f'court: sits on "{other.name}" for the loss of the Renard at Brest', "the test"
    )
    assert e.data.get("result") != "done" and ("lost no ship" in e.text or "No person" in e.text)
    doubt = WO.doubt(
        w, WO.parse(f"court: sits on Captain Bowen for the loss of the {ship_name} at Brest")
    )
    assert doubt is not None and "port of his own nation" in doubt
    assert WO.doubt(w, WO.parse("court: sits on Captain Bowen at Falmouth")) is None
    e = w.world_order(
        f"court: sits on Captain Bowen for the loss of the {ship_name} at Falmouth", "the test"
    )
    assert e.data.get("result") == "done", e.text
    sat = _kinds(w.log, "court.sits")
    assert len(sat) == 1 and "the great cabin of the flagship" in sat[0].text
    assert me.ashore_at == CM.COURT_PLACE and CM.sitting(w)["person"] == "Captain Bowen"
    assert "the court martial" in w.submit("where am i").text
    port = w.ports.ports["falmouth"]
    assert any(p.get("id") == CM.COURT_PLACE for p in port.places)
    president = w.people.find_anywhere("the president of the court")
    assert president is not None and president.ashore_at == CM.COURT_PLACE
    e = w.world_order("court: sits on Captain Bowen at Falmouth", "the test")
    assert e.data.get("result") != "done" and "sits already" in e.text
    # the court's question, in-world, heard at the place; the accused's answer his own
    e = w.world_order(
        'say as the president of the court: "Captain Bowen, state to the court the '
        f'circumstances of the loss of the {ship_name}."',
        "the test",
    )
    assert e.data.get("result") == "done", e.text
    spoke = [x for x in w.log if x.kind == "person.spoke" and "president of the court" in x.text]
    assert spoke and "ashore at Falmouth" in spoke[-1].text
    out = w.submit(
        "say to the court: I engaged a superior force and struck when the ship could fight no more"
    )
    assert out.kind == "court.said" and "before the court at Falmouth" in out.text, out.text
    # his words as he said them, and once in the log (the order's own line)
    assert out.text.endswith(
        ": I engaged a superior force and struck when the ship could fight no more"
    )
    assert len(_kinds(w.log, "court.said")) == 1
    # the log of the action read by the judge advocate
    e = w.world_order("court: read the log of the action", "the test")
    assert e.data.get("result") == "done", e.text
    read = _kinds(w.log, "court.reading")
    assert read and all(f"log of the {ship_name}" in x.text for x in read)
    assert any("struck" in x.text.lower() for x in read)
    # the verdict: a sentence the court knows, journaled, read and never shown as sent
    e = w.world_order("court: the verdict on Captain Bowen: broke on the wheel", "the test")
    assert e.data.get("result") != "done" and "knows no sentence" in e.text
    e = w.world_order("court: the verdict on Captain Bowen: acquitted with honour", "the test")
    assert e.data.get("result") == "done", e.text
    verdict = _kinds(w.log, "court.verdict")
    assert len(verdict) == 1 and verdict[0].text.startswith(
        "The sentence of the court martial is read: Captain Bowen is honourably acquitted"
    )
    assert f"loss of the {ship_name}" in verdict[0].text
    # who hears the court (the place's knowledge): the persons ashore at its port, and no
    # ship's deck, at Falmouth or elsewhere; the appointment's line is said ashore too
    from freesail.world import knowledge as K

    at_falmouth = K.Senses(frozenset({K.ASHORE}), ("ashore", "falmouth", CM.COURT_PLACE), "")
    at_brest = K.Senses(frozenset({K.ASHORE}), ("ashore", "brest", "quay"), "")
    deck = K.Senses(K.senses_of_place("quarterdeck"), ("aboard", "h", "quarterdeck"), "quarterdeck")
    said = [x for x in w.log if x.kind == "court.said"]
    for x in (sat[0], said[-1], read[0], verdict[0]):
        assert x.data.get("port") == "falmouth" and x.data.get("place") == "shore", x.kind
        assert K.reaches(w, at_falmouth, x), x.kind
        assert not K.reaches(w, at_brest, x), x.kind
        assert not K.reaches(w, deck, x), x.kind
    assert K.reach_of("command.new") == "said"
    assert any(str(i.get("world_order", "")).startswith("court: the verdict") for i in w.inputs)
    assert not any(
        x.kind != "world.order" and "the verdict on Captain Bowen" in x.text for x in w.log
    )
    assert CM.record_of(me)[-1]["kind"] == "verdict"
    assert CM.record_of(me)[-1]["verdict"] == "acquitted with honour"
    assert CM.sitting(w) is None and me.ashore_at == "quay"
    assert not any(p.get("id") == CM.COURT_PLACE for p in port.places)
    assert w.people.find_anywhere("the president of the court") is None
    said = w.readings.words("record")
    assert "Captain Bowen's record" in said and "acquitted with honour" in said
    assert f"loss of the {ship_name}" in said and "exchanged" in said
    # a new command (§7.2): his first lieutenant exchanged at the same port follows him
    e = w.world_order(f'person: "{lt.name}" is exchanged at Falmouth', "the test")
    assert e.data.get("result") == "done", e.text
    w.saves_dir = str(tmp_path / "saves")
    order = 'command: a new command for Captain Bowen: the cutter "Alert" at Falmouth'
    assert WO.doubt(w, WO.parse(order)) is None
    from freesail.agents import director as D

    dry = D.dry_run(w, order)
    assert "would be written" in dry and not (tmp_path / "saves").exists()
    e = w.world_order(order, "the test")
    assert e.data.get("result") == "done", e.text
    # the file named by its name alone, in the reply and the data (the review's (A))
    assert e.data["scenario"].startswith("saves/new-command-alert-"), e.data
    path = str(tmp_path / "saves" / e.data["scenario"].split("/", 1)[1])
    assert e.data["followers"] == [lt.name] and lt.name in e.text
    assert e.data["scenario"] in e.text and "--scenario" in e.text
    assert CM.record_of(me)[-1]["kind"] == "command"
    sf = load_scenario(path)
    assert sf.scenario.name.startswith("A new command: the cutter Alert at Falmouth")
    assert sf.ship_file == "data/ships/cutter.yaml" and sf.scenario.ports == ["falmouth"]
    w2 = make_scenario_world(sf)
    begin(w2, sf)
    assert w2.ship.name == "Alert" and w2.people.captain.name == "Captain Bowen"
    rec2 = CM.record_of(w2.people.captain)
    assert [x["kind"] for x in rec2] == ["loss", "exchanged", "court", "verdict", "command"]
    assert "acquitted with honour" in w2.readings.words("record")
    lt2 = next(p for p in w2.people.people if p.role == "first lieutenant")
    assert lt2.name == lt.name and CM.record_of(lt2)[0]["kind"] == "loss"
    # the copy of his record he carries into her: a thing with words in his keeping, made
    # by the scenario's `things:` as a letter is, read as a letter is read; no paper of a
    # kind of its own, the new ship's papers as every ship's
    copy = [t for t in w2.people.things if t.name == CM.RECORD_THING]
    assert len(copy) == 1 and copy[0].is_letter and copy[0].keeper == w2.people.captain.id
    assert "acquitted with honour" in copy[0].words
    assert copy[0].words.endswith("appointed to the cutter Alert at Falmouth.")
    out = w2.submit("read the copy of the captain's record")
    assert out.kind == "free.line" and out.data.get("thing") == copy[0].id, out.text
    read_lines = [x for x in w2.log if x.kind == "free.read"]
    assert len(read_lines) == 1 and "acquitted with honour" in read_lines[0].text
    assert read_lines[0].data.get("reader") == "Captain Bowen"
    assert w2.papers.find("the captain's record") is None
    assert len(w2.papers.pages()) == len(w2.papers.catalogue)
    # a man dismissed the service gets no command
    CM.note(w, me, "verdict", "dismissed the service by the court", verdict="dismissed the service")
    e = w.world_order(order, "the test")
    assert e.data.get("result") != "done" and "gives him no command" in e.text
    CM.record_of(me).pop()
    CM.note(w, me, "verdict", "dismissed the ship", verdict="dismissed the ship")
    doubt = WO.doubt(w, WO.parse(order))
    assert doubt is not None and "within the year" in doubt


def test_the_adversarial_seat_is_refused_in_words_behind_the_flag_and_admitted_when_turned(
    tmp_path, monkeypatch
):
    """The design's §6 (truth 7-366): a `seat:` at the captain of a hull at war with the
    player's is refused with the brief's reason before any consent record is read; her
    lookout's station is admitted (a lookout fires into nobody); the flag turned, the seat is
    admitted; the captor holding the player's person is refused for both reasons."""
    w = granted(directed(), tmp_path)
    put(
        w,
        "brig-sloop",
        "france",
        "49 32 N 5 31 W",
        "bound for Brest",
        "bound for Brest",
        name="Renard",
    )
    w.run(60)
    own = w.ship.name
    e = w.world_order(f"seat: {SEATED} as captain of Renard for 3 samples")
    assert e.data["result"] == "refused", e.text
    assert "The consent brief names no role" in e.text and f"an enemy of the {own}'s" in e.text
    assert "Her rules-based captain and the director's voice serve meanwhile" in e.text
    assert not WO.director_seats(w)
    e = w.world_order(f"seat: {SEATED} as lookout of Renard for 3 samples")
    assert e.data["result"] == "done", e.text
    monkeypatch.setattr(seats, "ADVERSARIAL_SEATS_CONSENTED", True)
    e = w.world_order(f"seat: {SEATED} as captain of Renard for 3 samples")
    assert e.data["result"] == "done", e.text
    monkeypatch.setattr(seats, "ADVERSARIAL_SEATS_CONSENTED", False)
    renard = w.vessels.find("Renard")
    assert P.adversarial_seat_why(w, renard, "captain") is not None
    assert P.adversarial_seat_why(w, renard, "lookout") is None
    # a neutral is no adversary
    put(
        w,
        "merchant brig",
        "denmark",
        "49 31 N 5 33 W",
        "bound for Brest",
        "bound for Brest",
        name="Anna",
    )
    assert P.adversarial_seat_why(w, w.vessels.find("Anna"), "captain") is None


@pytest.mark.slow
def test_the_captor_holding_the_players_person_is_refused_for_both_reasons():
    w, enemy = _struck_to_a_crewed_frigate()
    why = P.adversarial_seat_why(w, enemy.vessel, "captain")
    assert why is not None and "holds Captain Bowen her prisoner" in why
    # his own ship, a prize, flies her captor's colours now: the enemy's reason is read of a
    # hull a human holds, and the prisoner's reason is the one that stands
    assert "an enemy of" not in why and "seats no model as the captain of the Medusa" in why


# ---------------------------------------------------------------------------
# The review's mends of 2026-11-10 (the lead's (A) to (I)), each failing before its mend
# ---------------------------------------------------------------------------


def test_a_new_command_names_its_file_by_name_alone_and_a_replay_writes_nothing(
    tmp_path, monkeypatch
):
    """(A), (B) and (H), and truth 7-365's own scene: the scenario is written under the
    saves in play; the log's line, its data, his record and the director's reply name it
    `saves/<name>` and never a machine's path; the served line is the appointment in the
    service's words, heard ashore at the port, the file and how to load it in the director's
    reply alone; saved and replayed with the saves elsewhere the world comes to the same
    digest and no file is written; a second ship whose name makes the same file's name the
    same day is refused in words and nothing is written over, in play and in the replay
    alike; the file loads and begins with him her captain and the copy of his record read."""
    from freesail.api.session import ship_factory
    from freesail.core import replay
    from freesail.world import knowledge as K
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    here, elsewhere = tmp_path / "here", tmp_path / "elsewhere"
    monkeypatch.setattr("freesail.agents.remote.SAVES_DIR", str(elsewhere))
    w = world_at(49.5, -5.5)
    w.submit("heave to")
    w.run(60)
    w.saves_dir = str(here)
    me = w.people.captain
    CM.note(w, me, "verdict", "acquitted by the test's court", verdict="acquitted")
    order = f'command: a new command for {me.name}: the cutter "Alert" at Falmouth'
    e = w.world_order(order, "the test")
    assert e.data.get("result") == "done", e.text
    shown = e.data["scenario"]
    assert shown == "saves/new-command-alert-1805-06-13.yaml"
    written = here / "new-command-alert-1805-06-13.yaml"
    assert written.exists()
    # the director's reply has the file and how to load it; no machine's path anywhere
    assert shown in e.text and "--scenario" in e.text and str(tmp_path) not in e.text
    line = _kinds(w.log, "command.new")
    assert len(line) == 1
    assert line[0].text == (
        f"{me.name} is appointed to the cutter Alert at Falmouth; nobody of his old company "
        "follows him."
    )
    assert "scenario" not in line[0].text and "saves" not in line[0].text
    assert line[0].data["scenario"] == shown and str(tmp_path) not in json.dumps(line[0].data)
    assert CM.record_of(me)[-1]["scenario"] == shown
    assert str(tmp_path) not in json.dumps(CM.record_of(me))
    assert str(tmp_path) not in json.dumps([x.text for x in w.log])
    # heard ashore at the port and on no ship's deck (the appointment is the port's news)
    at_falmouth = K.Senses(frozenset({K.ASHORE}), ("ashore", "falmouth", "quay"), "")
    deck = K.Senses(K.senses_of_place("quarterdeck"), ("aboard", "h", "quarterdeck"), "quarterdeck")
    assert K.reaches(w, at_falmouth, line[0]) and not K.reaches(w, deck, line[0])
    # (H) another ship whose name makes the same file's name the same day: refused in words
    before = written.read_text(encoding="utf-8")
    clash = f'command: a new command for {me.name}: the cutter "ALERT!" at Falmouth'
    e2 = w.world_order(clash, "the test")
    assert e2.data.get("result") != "done", e2.text
    assert "stands already" in e2.text and shown in e2.text and str(tmp_path) not in e2.text
    assert written.read_text(encoding="utf-8") == before
    assert [x["kind"] for x in CM.record_of(me)].count("command") == 1
    assert len(_kinds(w.log, "command.new")) == 1
    w.run(120)
    # the replay, the saves elsewhere: the same digest, and nothing written
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert [x.text for x in _kinds(copy.log, "command.new")] == [line[0].text]
    assert not elsewhere.exists()
    assert sorted(p.name for p in here.iterdir()) == [written.name]
    # the scenario's start: his name her captain's, the record carried, the copy read
    sf = load_scenario(str(written))
    w2 = make_scenario_world(sf)
    begin(w2, sf)
    assert w2.ship.name == "Alert" and w2.people.captain.name == me.name
    assert [x["kind"] for x in CM.record_of(w2.people.captain)] == ["verdict", "command"]
    out = w2.submit("read the copy of the captain's record")
    assert out.kind == "free.line", out.text
    assert "appointed to the cutter Alert at Falmouth" in _kinds(w2.log, "free.read")[0].text


@pytest.mark.slow
def test_the_court_is_dissolved_for_a_dead_or_a_missing_man_and_rises_with_everyone_at_its_place():
    """(B), (C), (D), (E) and (G) on the captive's scene: the exchange is heard by the man
    exchanged and the persons ashore at that port, and wakes no deck; `court: sits on the
    captain of the <ship>` takes the man who commanded her, whoever stands first in the
    registry; the court's officers are of no ship's company; a witness's refusal is in the
    world's words; a court whose accused is dead is dissolved in words at the next minute,
    and one whose accused is gone at the next form that names it, the place and the officers
    removed and everyone at the place on the quay; a dead man is not brought before a court;
    at the verdict everyone at the place goes to the quay, not the accused alone."""
    from freesail.world import knowledge as K

    w, _enemy = _landed_at_brest()
    me = C.captive_person(w)
    ship_name = w.players.ship.name
    lt = next(p for p in w.players.people.people if p.role == "first lieutenant")
    for who in ("Captain Bowen", lt.name):
        e = w.world_order(f'person: "{who}" is exchanged at Falmouth [reason: the lists]', "t")
        assert e.data.get("result") == "done", e.text
    # (C) the exchange: his and the port's, no deck's
    line = _kinds(w.log, "prize.exchanged")[0]
    at_falmouth = K.Senses(frozenset({K.ASHORE}), ("ashore", "falmouth", "quay"), "")
    at_brest = K.Senses(frozenset({K.ASHORE}), ("ashore", "brest", "quay"), "")
    deck = K.Senses(K.senses_of_place("quarterdeck"), ("aboard", "h", "quarterdeck"), "quarterdeck")
    asleep = K.Senses(frozenset({K.ASLEEP}), ("aboard", "h", "gunroom"), "gunroom", asleep=True)
    assert K.reach_of("prize.exchanged") != "wakes"
    assert K.reaches(w, at_falmouth, line)
    assert not K.reaches(w, at_brest, line)
    assert not K.reaches(w, deck, line) and not K.reaches(w, asleep, line)
    # (E) the captain of the ship is the man who commanded her, the lieutenant first or not
    company = w.registry.by_home[lt.home]
    company.remove(lt)
    company.insert(0, lt)
    assert w.registry.persons().index(lt) < w.registry.persons().index(me)
    assert CM._by_ship(w, ship_name) is me
    e = w.world_order(f"court: sits on the captain of the {ship_name} at Falmouth", "the test")
    assert e.data.get("result") == "done", e.text
    assert CM.sitting(w)["person"] == "Captain Bowen"
    # (G) the court's officers are of no ship's company
    president = w.people.find_anywhere(CM.PRESIDENT)
    judge = w.people.find_anywhere(CM.JUDGE_ADVOCATE)
    assert president is not None and judge is not None
    for hid in w.registry.hulls:
        assert president not in w.registry.company(hid), hid
        assert judge not in w.registry.company(hid), hid
    assert president.home == CM.COURT_HOME and president not in w.players.people.people
    # (B) a witness's refusal is the world's, and names no director
    lt.ashore_at = CM.COURT_PLACE  # brought before the court as a witness
    with pytest.raises(CM.CourtError) as refused:
        CM.accused_speaks(w, lt, "I was below when she struck")
    assert "when the court calls him" in str(refused.value)
    assert "director" not in str(refused.value) and "say as" not in str(refused.value)
    # (D) the accused dead: dissolved in words at the next minute, everyone on the quay
    port = w.ports.ports["falmouth"]
    me.dead = True
    w.run(60)
    gone = _kinds(w.log, "court.dissolved")
    assert len(gone) == 1
    assert gone[0].text == "The court martial at Falmouth is dissolved: Captain Bowen is dead."
    assert K.reaches(w, at_falmouth, gone[0]) and not K.reaches(w, deck, gone[0])
    assert CM.sitting(w) is None
    assert not any(p.get("id") == CM.COURT_PLACE for p in port.places)
    assert w.people.find_anywhere(CM.PRESIDENT) is None
    assert w.people.find_anywhere(CM.JUDGE_ADVOCATE) is None
    assert CM.COURT_HOME not in w.registry.by_home
    assert lt.ashore_at == "quay" and me.ashore_at == "quay"
    e = w.world_order(f"court: sits on Captain Bowen for the loss of the {ship_name}", "t")
    assert e.data.get("result") != "done" and "sits on no dead man" in e.text
    assert CM.sitting(w) is None
    me.dead = False
    # the accused gone from the world: dissolved at the next form that names the court
    e = w.world_order("court: sits on Captain Bowen at Falmouth", "the test")
    assert e.data.get("result") == "done", e.text
    home = w.registry.by_home[me.home]
    at = home.index(me)
    w.registry.remove(me)
    e = w.world_order("court: read the log of the action", "the test")
    assert e.data.get("result") != "done" and "No court martial sits" in e.text
    gone = _kinds(w.log, "court.dissolved")
    assert len(gone) == 2 and gone[1].text.endswith("Captain Bowen is not to be found.")
    assert CM.sitting(w) is None
    assert not any(p.get("id") == CM.COURT_PLACE for p in port.places)
    home.insert(at, me)
    # a new sitting is not refused for the old one, and at the verdict everyone at the
    # place goes to the quay
    e = w.world_order("court: sits on Captain Bowen at Falmouth", "the test")
    assert e.data.get("result") == "done", e.text
    lt.ashore_at = CM.COURT_PLACE
    e = w.world_order("court: the verdict on Captain Bowen: acquitted", "the test")
    assert e.data.get("result") == "done", e.text
    assert me.ashore_at == "quay" and lt.ashore_at == "quay"
    assert w.people.find_anywhere(CM.PRESIDENT) is None
    assert CM.COURT_HOME not in w.registry.by_home


@pytest.mark.slow
def test_the_players_persons_mark_is_past_when_he_is_his_own_ships_captain_again():
    """(F), reproduced: the mark of the player's person, made at his taking, outlived his
    being his own ship's captain again, and `players_person` preferred it to the check that
    a model holds her captain's station. Exchanged, he is the player's person still (his
    ship's captain is her prize master); she retaken and he her captain again, the mark is
    cleared, and with a model at her captain's station there is no player's person (the
    owner looks on), as before the taking."""
    from freesail.agents.agent import CAPTAIN
    from freesail.world import knowledge as K

    w, _enemy = _struck_to_a_crewed_frigate()
    me = C.captive_person(w)
    e = w.world_order('person: "Captain Bowen" is exchanged at Falmouth', "the test")
    assert e.data.get("result") == "done", e.text
    home = w.hulls[me.home]
    assert home.people.captain is not me  # her prize master
    assert C.remembered_person(w) is me and K.players_person(w) is me
    P.retake(w, home.vessel, by="the test", how="retaken")
    assert home.people.captain is me
    assert w.__dict__.get(C.PLAYERS_PERSON_KEY) is None and C.remembered_person(w) is None
    assert K.players_person(w) is me  # by his ship's captaincy, as before the taking
    agents = home.__dict__.setdefault("agents", {})
    agents[CAPTAIN] = SimpleNamespace(agent=SimpleNamespace(released=False), model_name="m")
    assert K.players_person(w) is None


def test_a_seat_the_journal_holds_is_held_again_in_a_replay_and_refused_before_the_consent(
    tmp_path, monkeypatch
):
    """(I): the refusal of an adversarial seat is the live door's. A seat at an enemy's
    captain held in play (the flag turned, or a save from before the rule) is held again in
    a replay with the flag as it stands, to the same digest; and in play the refusal comes
    before any consent record is read (a model with no record is refused for the brief's
    reason, not for its record)."""
    from freesail.api.session import ship_factory
    from freesail.core import replay

    w = granted(directed(), tmp_path)
    e = w.world_order(
        'ship: a brig-sloop "Renard" of France at 49 32 N 5 31 W, bound for Brest, '
        "intent: bound for Brest",
        "the test",
    )
    assert e.data.get("result") == "done", e.text
    w.run(60)
    stranger = "a-model-with-no-consent-record"
    w.scenario.director["models"].append(stranger)
    e = w.world_order(f"seat: {stranger} as captain of Renard for 3 samples")
    assert e.data["result"] == "refused", e.text
    assert "The consent brief names no role" in e.text and "No consent is on record" not in e.text
    monkeypatch.setattr(seats, "ADVERSARIAL_SEATS_CONSENTED", True)
    e = w.world_order(f"seat: {SEATED} as captain of Renard for 3 samples")
    assert e.data["result"] == "done", e.text
    monkeypatch.setattr(seats, "ADVERSARIAL_SEATS_CONSENTED", False)
    w.run(60)
    data = json.loads(json.dumps(w.save()))
    copy = replay.replay(data, ship_factory)
    assert copy.log.digest() == w.log.digest()
    assert list(WO.director_seats(copy)) == list(WO.director_seats(w))
    assert len(WO.director_seats(copy)) == 1
