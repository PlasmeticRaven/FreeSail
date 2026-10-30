"""The date, and the war, as readings (the owner's fourth and fifth notes of the playtests
of packages 70 to 72: the date deduced from the log's stamps and confused; the war's state
reasoned out from a primer's example).

The date is a reading in words (`the date`) and the last words of every station's line, so
that it is known and never deduced; it changes once a day, so it rides no sample between.
The war is what the ship knows of it and never the world's table as it stands: the
nations' table she sailed with, and every change the news brought her since, each entered
in her papers as a price is, with where and when it came (`the news of the war`), readable
as `the war` and in the library's papers.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from freesail.agents import tools
from freesail.api import readings as R
from freesail.core.events import Severity

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def cutter():
    from freesail.world.scenarios import load_scenario, make_scenario_world

    sf = load_scenario(ROOT / "data" / "scenarios" / "dispatches-falmouth.yaml")
    return make_scenario_world(sf, seed=7)


def test_the_date_is_a_reading_in_words_and_closes_every_stations_line(cutter):
    w = cutter
    row = R.REGISTRY.get("date")
    assert row.kind == "query" and "the date" in row.words and "what day is it" in row.words
    assert w.submit("the date").text == "The date: Wednesday 12 June 1805."
    assert w.submit("what day is it").text == "What day is it: Wednesday 12 June 1805."
    value = w.readings.get("date")
    assert value == {
        "words": "Wednesday 12 June 1805",
        "date": "1805-06-12",
        "weekday": "Wednesday",
    }
    # the line, every station's and the director's, ends with it
    assert R.station_line(w, None).endswith("; Wednesday 12 June 1805.")
    assert R.director_line(w).endswith("; Wednesday 12 June 1805.")
    # it changes once a day, with the day, and the ship's time stays `the time`
    w.run(60 * 60 * 19 + 1)
    assert w.readings.get("date")["words"] == "Thursday 13 June 1805"
    assert R.station_line(w, None).endswith("; Thursday 13 June 1805.")
    assert w.submit("the time").kind == "query.reading"


def test_the_war_is_what_the_ship_knows_never_the_worlds_table(cutter):
    w = cutter
    row = R.REGISTRY.get("war")
    assert row.kind == "query" and set(row.words) >= {"the war", "who is at war"}
    sailed = w.nations.sailed_with_words()
    assert sailed.startswith("The nations as she sailed (1 June 1805): Britain at war with ")
    assert "France" in sailed and "Spain" in sailed and "at peace with all" in sailed
    said = w.submit("the war").text
    assert said == f"The war: {sailed} No news of the war has reached her since she sailed."
    # the world's table moves (a peace made) and she is none the wiser until the news comes
    assert w.nations.make_peace("britain", "spain", "1805-06-12")
    assert w.submit("the war").text == said
    assert w.nations.at_war("britain", "spain") is False
    # the pilot's news brings it: entered in her papers with where and when, written up
    n = len(w.log)
    lines = w.papers.news_heard("the pilot off Falmouth")
    assert lines == [
        "The news of the war written up by the captain: by the pilot off Falmouth, peace made "
        "between Britain and Spain."
    ]
    assert len(w.log) == n  # the caller records the line (the pilot's own hook does)
    assert w.papers.war_news == [
        {
            "tick": 0,
            "when": "12 June, Morning watch, 2 bells (05:00)",
            "how": "the pilot off Falmouth",
            "text": "peace made between Britain and Spain",
        }
    ]
    after = w.submit("the war").text
    assert after.startswith(f"The war: {sailed} The news since, as it came: 12 June, ")
    assert "by the pilot off Falmouth: peace made between Britain and Spain." in after
    assert "As she knows it now: Britain at war with the Batavian Republic and France;" in after
    # the same news again changes nothing; a war declared is entered the same way
    assert w.papers.news_heard("the boat from the quay at Falmouth") == []
    assert w.nations.declare_war("britain", "denmark")
    assert w.papers.news_heard("the pilot off Plymouth")[0].endswith(
        "by the pilot off Plymouth, war declared between Britain and Denmark."
    )
    assert len(w.papers.war_news) == 2
    # the paper in the library says the same, by its handle
    page = str(tools.library(w, "captain", "papers", section="the news of the war"))
    assert page.startswith("The news of the war: the nations' table the ship sailed with")
    assert "kept by the captain in the cabin" in page
    assert sailed in page and "by the pilot off Plymouth: war declared between" in page
    assert "the war's state" in str(tools.library(w, "captain", "grammar", section="the readings"))


def test_the_pilots_news_enters_what_it_changed_in_the_papers(cutter):
    """The pilot's hook: his news logged as before, and what it changed of the war the ship
    knows written up in the paper, a notable line each."""
    w = cutter
    w.nations.make_peace("britain", "france")
    port = w.dealings.ports["falmouth"]
    n = len(w.log)
    news = w.dealings.news_words(port)
    w.record(Severity.ROUTINE, "port.news", f"The pilot's news: {news}", {"port": port.id})
    for line in w.papers.news_heard(f"the pilot off {port.name}"):
        w.record(Severity.NOTABLE, "paper.written", line, {"paper": "the news of the war"})
    new = list(w.log)[n:]
    assert [e.kind for e in new] == ["port.news", "paper.written"]
    assert new[1].text.endswith("by the pilot off Falmouth, peace made between Britain and France.")
    assert new[1].severity is Severity.NOTABLE
