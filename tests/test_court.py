"""The court martial, the new command and the adversarial seat's refusal (spec M7 §20; package
74, step 6; the design in `docs/design/Design-Prizes.md` §6 and §7): the court as the director's
proceeding at a place of the port, its questions through the channel and the accused's own words,
the log of the action read, the verdict journaled and read as the court's; a new command written
as a scenario under the saves with the record and the followers; a seat at the captain of a hull
adversarial to a human refused in words behind the flag."""

from __future__ import annotations

import pytest

from freesail.world import captive as C
from freesail.world import court as CM
from freesail.world import orders as WO
from freesail.world import prizes as P
from freesail.world import seats
from tests.test_brains import put
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
    # ship's deck, at Falmouth or elsewhere; the new command's line is the record's
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
    assert K.reach_of("command.new") == "record"
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
    path = e.data["scenario"]
    assert path.startswith((tmp_path / "saves").as_posix()) and "new-command-alert" in path
    assert e.data["followers"] == [lt.name] and lt.name in e.text
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
    page = w2.papers.page("the captain's record")
    assert any("acquitted with honour" in ln for ln in page.lines)
    # the paper is aboard only where the scenario carries a record: last among the new
    # command's papers and no part of her catalogue, and no paper of the ship he lost (so
    # every other ship's papers, and every count and list pinned of them, are as they were)
    assert [p.handle for p in w2.papers.pages()][-1] == "the captain's record"
    assert len(w2.papers.pages()) == len(w2.papers.catalogue) + 1
    assert w.papers.find("the captain's record") is None
    assert len(w.papers.pages()) == len(w.papers.catalogue)
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
