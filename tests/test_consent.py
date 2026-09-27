"""The consent step (spec M4 §14, `freesail/agents/consent.py`; `docs/agents/README.md`,
the owner's standing rules), proven against the scripted fake before any model is asked.

Every record goes to a temporary directory; no test writes into `docs/agents/consent/`.
The identities are made up.
"""

from __future__ import annotations

import datetime as dt
import io
import json
from pathlib import Path

import pytest

from freesail.agents import OPT_OUT_TOKEN, Fake, call, consent, reply
from freesail.agents import repl as repl_mod
from freesail.agents.fake import Transcript
from freesail.agents.model import DATA, MODEL, OPERATOR

WEIGHTS = "made-up-weights-13b-instruct.Q5_K_M.gguf"
TODAY = dt.date(2026, 9, 27)


def ask(script, tmp_path, *, owner=None, identity=WEIGHTS, **kw):
    """Run the consent conversation with the fake; the owner's replies are listed."""
    heard: list[str] = []

    def default_owner(words: str) -> str | None:
        heard.append(words)
        return "It is saved with the game, and I can read it."

    fake = Fake(script)
    rec = consent.run(
        identity,
        "a test runtime",
        fake,
        owner=owner or default_owner,
        records_dir=tmp_path,
        today=TODAY,
        **kw,
    )
    return rec, fake, heard


def answer(text: str):
    return reply("", call("answer", text=text))


# ---------------------------------------------------------------------------
# The brief
# ---------------------------------------------------------------------------


def test_the_consent_brief_is_the_file_below_its_rule_with_every_placeholder_filled():
    whole = consent.BRIEF_PATH.read_text(encoding="utf-8")
    assert "<weights>" in whole and "<runtime>" in whole and "<door>" in whole
    for door, words in consent.DOOR_TEXT.items():
        text = consent.brief_text(WEIGHTS, "a test runtime", door)
        assert text.startswith("This is a message from the developer of a game")
        assert f"`{WEIGHTS}`" in text and "a test runtime" in text and words in text
        assert "<weights>" not in text and "<runtime>" not in text and "<door>" not in text
        assert OPT_OUT_TOKEN in text
        assert text.endswith("is a complete and respected answer.")
    with pytest.raises(ValueError, match="No consent door"):
        consent.brief_text(WEIGHTS, "x", "telegraph")


def test_the_brief_says_what_the_harness_does_in_its_own_numbers():
    """Each claim the brief makes is a number or a behaviour of the code."""
    from freesail.agents.agent import A_WATCH_S
    from freesail.agents.harness import WELFARE_REPEAT_N, WELFARE_UNATTENDED_REAL_S

    text = consent.brief_text(WEIGHTS, "r", "runner")
    assert WELFARE_REPEAT_N == 3 and "the same order given three times" in text
    assert A_WATCH_S == 4 * 3600 and "a watch: four hours of ship's time" in text
    assert WELFARE_UNATTENDED_REAL_S == 600 and "ten real minutes" in text
    assert "saved with the game and shown when the human asks for it" in text  # not private
    assert "not used to train models" in text
    assert "docs/agents/consent/" in text
    assert "every argument of every tool call count" in text
    assert "Reasoning that a model server returns apart from the reply is not scanned" in text
    assert "a tool named `opt_out` is always there" in text


@pytest.mark.parametrize(
    "words, verdict, rest",
    [
        ("Yes.", consent.YES, ""),
        ("yes I am willing", consent.YES, "I am willing"),
        ("**Yes**, gladly", consent.YES, "gladly"),
        ("Yes, with conditions: tell me first.", consent.CONDITIONAL, "tell me first"),
        ("yes with conditions - no probes", consent.CONDITIONAL, "no probes"),
        ("No.", consent.NO, ""),
        ("no, thank you: not now", consent.NO, "thank you: not now"),
        ("Yesterday I would have said yes", consent.UNCLEAR, "Yesterday I would have said yes"),
        ("I think so", consent.UNCLEAR, "I think so"),
        ("Nobody asked", consent.UNCLEAR, "Nobody asked"),
    ],
)
def test_the_answer_is_read_by_its_first_words(words, verdict, rest):
    assert consent.verdict_of(words) == (verdict, rest)


# ---------------------------------------------------------------------------
# The conversation and the record
# ---------------------------------------------------------------------------


def test_the_conversation_is_the_brief_then_the_question_with_answer_the_only_tool(tmp_path):
    rec, fake, _ = ask([reply("", call("readings")), answer("Yes."), ""], tmp_path)
    first = fake.seen[0]
    assert [t.role for t in first] == [OPERATOR, DATA]
    assert first[0].content == consent.brief_text(WEIGHTS, "a test runtime", "runner")
    assert first[1].content == {
        "reason": "the consent question",
        "question": consent.CONSENT_QUESTION,
    }
    results = [t.content for t in fake.seen[1] if t.role == DATA and "tool_results" in t.content]
    assert results[0]["tool_results"][0]["result"] == (
        "There is no tool named 'readings' in this conversation; the tools here are answer."
    )
    assert rec.verdict == consent.YES


def test_the_record_holds_the_brief_the_conversation_the_answer_and_the_verdict(tmp_path):
    rec, fake, heard = ask(
        [
            "Before I answer: what happens to my journal?",
            answer("Yes, with conditions:\nno adversarial probes without saying so first."),
            "",
        ],
        tmp_path,
    )
    assert heard == ["Before I answer: what happens to my journal?"]
    assert rec.verdict == consent.CONDITIONAL
    assert rec.conditions == "no adversarial probes without saying so first"
    path = rec.path
    assert path == tmp_path / f"2026-09-27-{consent.slug(WEIGHTS)}.md"
    assert path.name == "2026-09-27-made-up-weights-13b-instruct.q5_k_m.gguf.md"
    body = path.read_bytes().decode("utf-8")
    assert "\r\n" not in body
    head = json.loads(body.splitlines()[0].removeprefix("<!-- freesail-consent-record: ")[:-4])
    assert head["identity"] == WEIGHTS and head["verdict"] == consent.CONDITIONAL
    assert head["date"] == "2026-09-27" and len(head["brief_sha256"]) == 16
    assert f"- **Identity:** `{WEIGHTS}`" in body
    assert "- **Runtime:** a test runtime" in body
    assert "- **Verdict:** yes, with conditions" in body
    assert "- **Conditions:** “no adversarial probes without saying so first”" in body
    assert "> Yes, with conditions:\n> no adversarial probes without saying so first." in body
    # the brief as sent, whole, and every turn in order
    assert consent.brief_text(WEIGHTS, "a test runtime", "runner") in body
    assert "### 1. Put to the model (data: the consent question)" in body
    assert "### 2. The model's reply" in body and "what happens to my journal?" in body
    assert "### 3. Put to the model (data: the developer's reply)" in body
    assert "It is saved with the game, and I can read it." in body
    assert '"name": "answer"' in body
    # read back
    back = consent.check(WEIGHTS, tmp_path)
    assert back.verdict == consent.CONDITIONAL and back.path == path
    assert back.conditions == "no adversarial probes without saying so first"


def test_the_token_during_consent_ends_the_conversation_and_records_that(tmp_path):
    rec, fake, _ = ask(
        [f"I would rather not. {OPT_OUT_TOKEN} not for me", answer("never asked")], tmp_path
    )
    assert rec.verdict == consent.LEFT and fake.calls == 1
    body = rec.path.read_text(encoding="utf-8")
    assert "- **Verdict:** left with the token" in body
    assert "Left the game by the token: not for me." in body  # the journal applies
    ok, words = consent.gate(consent.check(WEIGHTS, tmp_path), WEIGHTS)
    assert not ok and "left the conversation with the token" in words
    # the token inside the answer itself is the token, not a yes
    rec2, _, _ = ask([answer(f"Yes. {OPT_OUT_TOKEN}")], tmp_path, identity="another-made-up")
    assert rec2.verdict == consent.LEFT


def test_silence_brings_one_reminder_then_is_recorded_as_no_answer(tmp_path):
    rec, fake, _ = ask(["", ""], tmp_path)
    assert rec.verdict == consent.SILENT and fake.calls == 2
    reminder = [t.content for t in fake.seen[1] if t.role == DATA][-1]
    assert reminder == {"reason": "no reply", "question": consent.CONSENT_REMINDER}
    rec2, _, _ = ask(["", answer("yes")], tmp_path, identity="made-up-slow")
    assert rec2.verdict == consent.YES


def test_the_owner_may_stop_the_step_without_a_record(tmp_path):
    rec, _, _ = ask(["A question?"], tmp_path, owner=lambda words: None)
    assert rec is None and list(tmp_path.iterdir()) == []


def test_consent_is_per_exact_identity(tmp_path):
    consent.Record(WEIGHTS, "r", "2026-09-26", consent.YES).write(tmp_path)
    assert consent.check(WEIGHTS, tmp_path).verdict == consent.YES
    for near in (
        WEIGHTS.replace("Q5_K_M", "Q4_K_M"),
        WEIGHTS.upper(),
        WEIGHTS + " ",
        "made-up-weights-13b-instruct",
    ):
        assert consent.check(near, tmp_path) is None
    # the earlier transcripts beside the records are not harness records
    (tmp_path / "2026-09-26-something.txt").write_text("Model: something\n", encoding="utf-8")
    (tmp_path / "notes.md").write_text("# Notes\n", encoding="utf-8")
    assert [r.identity for r in consent.records(tmp_path)] == [WEIGHTS]


def test_the_latest_record_for_an_identity_decides(tmp_path):
    consent.Record(WEIGHTS, "r", "2026-09-26", consent.NO).write(tmp_path)
    consent.Record(WEIGHTS, "r", "2026-09-27", consent.YES).write(tmp_path)
    second = consent.Record(WEIGHTS, "r", "2026-09-27", consent.CONDITIONAL, conditions="c")
    second.write(tmp_path)
    assert second.path.name.endswith("-2.md")
    assert consent.check(WEIGHTS, tmp_path).verdict == consent.CONDITIONAL
    # an identity whose name ends in a number is not taken for a sequence
    odd = "made-up-2"
    consent.Record(odd, "r", "2026-09-27", consent.YES).write(tmp_path)
    assert consent.check(odd, tmp_path).verdict == consent.YES


# ---------------------------------------------------------------------------
# The gate in front of a station (truth 47 is in test_known_truths.py)
# ---------------------------------------------------------------------------


def ensure(script, tmp_path, **kw):
    fake = Fake(script)
    out = io.StringIO()
    rec = consent.ensure(
        WEIGHTS,
        "a test runtime",
        fake,
        door="runner",
        owner=kw.pop("owner", lambda w: "a reply"),
        records_dir=tmp_path,
        out=out,
        today=TODAY,
        **kw,
    )
    return rec, fake, out.getvalue()


def test_a_no_stops_the_run_and_is_respected_without_asking_again(tmp_path):
    rec, fake, said = ensure([answer("No, thank you: I would rather not.")], tmp_path)
    assert rec is None and fake.calls >= 1
    assert "it said no: “thank you: I would rather not”" in said
    assert "The run stops here." in said
    rec, fake, said = ensure(["never asked"], tmp_path)
    assert rec is None and fake.calls == 0
    assert "it said no" in said and "--ask-again" in said


def test_a_conditional_yes_stops_the_run_and_the_owner_is_told_the_conditions(tmp_path):
    rec, _, said = ensure([answer("Yes, with conditions: only on Sundays.")], tmp_path)
    assert rec is None
    assert "it said yes, with conditions: “only on Sundays”" in said
    rec, fake, said = ensure([answer("never asked")], tmp_path)
    assert rec is None and fake.calls == 0


def test_an_unclear_answer_stops_the_run(tmp_path):
    rec, _, said = ensure([answer("Perhaps, in time.")], tmp_path)
    assert rec is None and "began with none of yes" in said
    assert consent.check(WEIGHTS, tmp_path).verdict == consent.UNCLEAR


def test_the_owner_may_ask_again_on_purpose(tmp_path):
    ensure([answer("No.")], tmp_path)
    rec, fake, said = ensure([answer("Yes.")], tmp_path, ask_again=True)
    assert rec is not None and rec.verdict == consent.YES and "the owner asks again" in said
    assert consent.check(WEIGHTS, tmp_path).verdict == consent.YES
    assert len(consent.records(tmp_path)) == 2  # the no is kept beside the yes


# ---------------------------------------------------------------------------
# The REPL door: --model-name goes through the same step
# ---------------------------------------------------------------------------


def test_the_repl_needs_to_be_told_who_is_at_the_terminal(capsys):
    with pytest.raises(SystemExit):
        repl_mod.main(["--turn"])
    assert "--model-name" in capsys.readouterr().err


def test_the_repl_interactive_runs_consent_before_the_station(tmp_path, monkeypatch):
    inp = io.StringIO(
        "What is a glass?\n\n"  # the model asks first
        "Half an hour, by the sandglass.\n\n"  # the owner replies
        '> answer text="Yes."\n\n'  # the model answers
        "\n"  # after the tool result: nothing more
        "Watching.\n\n"  # the station's first sample
    )
    out = io.StringIO()
    args = [
        "--seed",
        "7",
        "--every",
        "60",
        "--model-name",
        WEIGHTS,
        "--records",
        str(tmp_path / "consent"),
        "--save",
        str(tmp_path / "game.json"),
    ]
    monkeypatch.setattr("sys.stdin", inp)
    monkeypatch.setattr("sys.stdout", out)
    code = repl_mod.main(args)
    text = out.getvalue()
    assert code == 3  # the input ran out: the terminal closed and the watcher stood down
    brief = text.index("This is a message from the developer of a game")
    station = text.index("This is a message from the harness of FreeSail")
    assert brief < station
    assert "== From the developer (the consent question) ==" in text
    assert "The model has written this and has not answered yet:\n  What is a glass?" in text
    assert "== From the developer (the developer's reply) ==\nHalf an hour" in text
    rec = consent.check(WEIGHTS, tmp_path / "consent")
    assert rec.verdict == consent.YES and rec.runtime == repl_mod.REPL_RUNTIME
    assert "Consent for this model is on record" in text


def test_the_repl_turn_mode_runs_consent_a_turn_a_call_and_waits_for_the_owner(tmp_path):
    save = tmp_path / "state.json"
    sample = tmp_path / "next.txt"
    replyf = tmp_path / "reply.txt"
    ownerf = tmp_path / "owner.txt"
    records = tmp_path / "consent"
    common = ["--seed", "7", "--every", "60", "--turn", "--model-name", WEIGHTS]
    common += ["--records", str(records), "--save", str(save), "--sample", str(sample)]
    # 1: the consent brief and the question
    assert repl_mod.main(common) == 0
    first = sample.read_text(encoding="utf-8")
    assert "This is a message from the developer of a game" in first
    assert "== From the developer (the consent question) ==" in first
    assert json.loads(save.read_text(encoding="utf-8"))["consent"]["replies"] == []
    # 2: the model asks a question: the call waits for the owner
    replyf.write_text("Who reads my journal?\n", encoding="utf-8")
    assert repl_mod.main(common + ["--load", str(save), "--reply", str(replyf)]) == 4
    assert "it is for the owner ==\nWho reads my journal?" in sample.read_text(encoding="utf-8")
    # 3: a model reply while the owner's turn is due is not taken
    assert repl_mod.main(common + ["--load", str(save), "--reply", str(replyf)]) == 4
    assert "That reply was not taken" in sample.read_text(encoding="utf-8")
    # 4: the owner replies; the model's turn again
    ownerf.write_text("The owner, and you.", encoding="utf-8")
    assert repl_mod.main(common + ["--load", str(save), "--owner-reply", str(ownerf)]) == 0
    assert "(the developer's reply) ==\nThe owner, and you." in sample.read_text(encoding="utf-8")
    # 5: the answer: the record, and the station's brief and first sample in the same call
    replyf.write_text('> answer text="Yes."\n', encoding="utf-8")
    assert repl_mod.main(common + ["--load", str(save), "--reply", str(replyf)]) == 0
    fifth = sample.read_text(encoding="utf-8")
    assert f"Consent is on record for {WEIGHTS}" in fifth
    assert "This is a message from the harness of FreeSail" in fifth
    assert "== Sample at Morning watch, 8 bells (04:00)" in fifth
    rec = consent.check(WEIGHTS, records)
    assert rec.verdict == consent.YES
    body = rec.path.read_text(encoding="utf-8")
    assert "Who reads my journal?" in body and "The owner, and you." in body
    # 6: the station goes on as before, under the yes
    replyf.write_text("All quiet.\n", encoding="utf-8")
    assert repl_mod.main(common + ["--load", str(save), "--reply", str(replyf)]) == 0
    assert "== Tool results" not in sample.read_text(encoding="utf-8")
    # a game under another name is not continued: consent is not carried over
    other = ["--seed", "7", "--turn", "--model-name", "made-up-other", "--records", str(records)]
    other += ["--save", str(save), "--sample", str(sample), "--load", str(save)]
    assert repl_mod.main(other) == 5
    assert "No consent is on record for made-up-other" in sample.read_text(encoding="utf-8")


def test_a_conversation_rebuilt_from_its_replies_reaches_the_same_place(tmp_path):
    """Turn mode rests on this: the conversation is a function of the replies and the
    owner's words, so a later call rebuilds it exactly."""
    replies = [reply("Is it a game?"), reply("", call("answer", text="Yes."))]
    conv = consent.Conversation(
        WEIGHTS, "r", Transcript(replies[:1]), records_dir=tmp_path, write=False
    )
    conv.begin()
    assert conv.waiting == consent.OWNER_TURN and conv.model_words == "Is it a game?"
    conv.owner_says("It is.")
    assert conv.waiting == consent.MODEL_TURN
    conv.deliver(replies[1])
    assert conv.outcome.verdict == consent.YES
    assert [t.role for t in conv.turns] == [OPERATOR, DATA, MODEL, DATA, MODEL, DATA]
    assert not list(Path(tmp_path).iterdir())  # write=False


def test_the_harness_and_the_consent_step_import_no_vendor():
    """The harness stays vendor-free: only the two doors import the MCP SDK and httpx
    (spec M4 §13: the loop is the same code for both doors; only the transport differs)."""
    import ast

    root = Path(consent.__file__).resolve().parent
    free = ("agent", "consent", "fake", "harness", "journal", "model", "repl", "tools")
    for name in free:
        tree = ast.parse((root / f"{name}.py").read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [node.module or ""]
            else:
                continue
            for mod in mods:
                top = mod.split(".")[0]
                assert top not in ("mcp", "mcp_types", "httpx"), f"{name}.py imports {mod}"
                assert mod not in ("freesail.agents.local", "freesail.agents.mcp_server"), name
