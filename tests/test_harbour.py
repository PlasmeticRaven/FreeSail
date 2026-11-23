"""The harbour (package 59; spec M7b §21d, §21e; `freesail/ui/harbour.py`,
`client/harbour.html` and `harbour.js`): the launcher as a page of the game's own server.

On FastAPI's `TestClient`: the game page leads to the harbour while no game is in play; the
catalogue; a game started from the page's choices by the server's own `prepare_game` and
taken up in place (one server, the harbour still at its path); the scenario maker's
read, proof (the loader's refusal in the form's words) and save in the player's place; the
desktop client's entries shown first and written on the word; the settings kept without a
key. On a live server: the API door and the local runner started as the server's
subprocesses, one seated and stopped (its station released), one that dies and says so.
In the browser the tests drive (the pre-installed Chromium through Playwright): a game
started with a seat and a director's brief, and the owner's four scenarios read into the
maker's form and written again byte for byte.

The model names are made up; the settings, the records, the saves and the client's file
go to a temporary directory.
"""

from __future__ import annotations

import json
import os
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

import pytest

pytest.importorskip("fastapi")
pytest.importorskip("httpx")

from own_page import PageClient  # noqa: E402

from freesail import settings as S  # noqa: E402
from freesail.core.world import Scenario, World  # noqa: E402
from freesail.ui.harbour import Harbour  # noqa: E402
from freesail.ui.server import Driver, create_app  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ROOT / "data" / "scenarios"
THE_FOUR = ("smack-falmouth", "lugger-roscoff", "directed-passage", "dispatches-falmouth")
PLACEHOLDER = "placeholder-model-for-the-harbour"  # no model is named here


class Port:
    """A harbour on a world with no game yet, as `py -m freesail` starts one."""

    def __init__(self, tmp: Path, settings: dict[str, Any] | None = None):
        self.tmp = tmp
        self.settings_path = tmp / "player" / "settings.yaml"
        s = S.load_settings(self.settings_path)
        s["places"]["desktop_config"] = str(tmp / "Claude" / "claude_desktop_config.json")
        for k, v in (settings or {}).items():
            s[k] = S._merge(s[k], v)
        S.save_settings(s, self.settings_path)
        self.driver = Driver(World(seed=1805, scenario=Scenario()))
        self.records = tmp / "consent"
        self.harbour = Harbour(
            self.driver,
            settings_path=self.settings_path,
            consent_records=self.records,
            saves_dir=tmp / "saves",
            started=False,
        )
        self.app = create_app(
            self.driver,
            harbour=self.harbour,
            consent_records=self.records,
            saves_dir=tmp / "saves",
        )

    @property
    def place(self) -> Path:
        return self.settings_path.parent / "scenarios"


@pytest.fixture
def port(tmp_path):
    return Port(tmp_path)


@pytest.fixture
def client(port):
    with PageClient(port.app) as c:
        yield c


# ---------------------------------------------------------------------------
# The page, the catalogue and a game started
# ---------------------------------------------------------------------------


def test_with_no_game_the_game_page_leads_to_the_harbour(client):
    r = client.get("/", follow_redirects=False)
    assert r.status_code == 307 and r.headers["location"] == "/harbour"
    page = client.get("/harbour")
    assert page.status_code == 200 and "scenario maker" in page.text
    assert "/client/harbour.js" in page.text
    state = client.get("/api/harbour/state").json()
    assert state["game"]["started"] is False and state["doors"] == []


def test_the_catalogue_lists_the_scenarios_ships_seats_stations_briefs_and_ports(client):
    cat = client.get("/api/harbour/catalogue").json()
    paths = {s["path"] for s in cat["scenarios"]}
    assert {f"data/scenarios/{n}.yaml" for n in THE_FOUR} <= paths
    assert "data/ships/smack.yaml" in cat["ships"] and "director" in cat["seats"]
    assert {"captain", "officer", "director"} <= set(cat["stations"])
    assert {"quiet-passage", "dispatches"} <= set(cat["briefs"])
    falmouth = next(p for p in cat["ports"] if p["id"] == "falmouth")
    assert falmouth["road"] == "Carrick Road" and falmouth["region"] == "channel-west"
    assert "data/standing_orders/starter.orders" in cat["books"]


def test_the_scenarios_stand_on_their_shelves_and_the_boats_are_no_ship_to_start_in(port, client):
    """Package 96b, step 1 (docs/design/Design-Harbour.md §3.2): the catalogue gives each
    scenario its shelf and its sentence in the shelves' order, the player's own first; the
    gates' and the tests' scenarios on a shelf marked hidden; a scenario of the game that
    the shelves' file does not name on the last shelf, shown; the ship's boats out of the
    ships offered for a bare start."""
    port.place.mkdir(parents=True, exist_ok=True)
    (port.place / "mine.yaml").write_text("name: A passage of mine\n", encoding="utf-8")
    cat = client.get("/api/harbour/catalogue").json()
    by_id = {s["id"]: s for s in cat["shelves"]}
    assert [s["id"] for s in cat["shelves"]][:3] == ["yours", "first", "lessons"]
    assert by_id["tests"]["hidden"] is True
    assert not any(s["hidden"] for s in cat["shelves"] if s["id"] != "tests")
    assert "unsorted" not in by_id  # every scenario of the game is named on a shelf
    entries = {Path(s["path"]).stem: s for s in cat["scenarios"]}
    assert entries["mine"]["shelf"] == "yours" and entries["mine"]["own"] is True
    assert cat["scenarios"][0]["path"].endswith("mine.yaml")
    assert entries["gate-4c-day"]["shelf"] == "tests"
    assert entries["squadron"]["shelf"] == "tests" and entries["tender"]["shelf"] == "tests"
    assert entries["first-action"]["shelf"] == "actions" and entries["first-action"]["says"]
    lessons = [Path(s["path"]).stem for s in cat["scenarios"] if s["shelf"] == "lessons"]
    assert lessons == ["lesson-landfall", "lesson-reckoning", "lesson-falmouth", "lesson-lee-shore"]
    assert [s["order"] for s in cat["scenarios"]] == list(range(len(cat["scenarios"])))
    # the boats are carried by the ships, and are not ships to start in
    assert "data/ships/frigate-36.yaml" in cat["ships"]
    assert not [s for s in cat["ships"] if "boat-" in s]
    # a scenario the file does not name is never hidden: the last shelf, shown
    shelved = port.harbour._shelve(
        [
            {"path": "data/scenarios/a-new-one.yaml", "name": "A new one", "own": False},
            {"path": "data/scenarios/gate-4c-day.yaml", "name": "The gate's day", "own": False},
        ]
    )
    assert [s["id"] for s in shelved] == ["tests", "unsorted"]
    assert shelved[-1]["hidden"] is False


def test_the_first_game_is_the_primers_chapter_7_and_its_log_is_the_bare_ships(client):
    """Package 96b, step 2 (docs/design/Design-Harbour.md §3.3): the first panel's game is
    the scenario "A first passage", the primer's chapter 7 made startable from the page.
    The chapter's own command is a bare frigate with `--seed 7 --wind 0,15 --heading 293`;
    the scenario gives the same log line for line through all five of the chapter's
    frigate blocks, typed as the chapter has them (an hour and a quarter: plain sail and
    the braces, the tack, the wear and the rest), but for the opening line, which carries
    the scenario's name where the bare ship's says "Open water"."""
    import re

    from freesail.api.session import make_world
    from freesail.world.scenarios import begin, load_scenario, make_scenario_world

    cat = client.get("/api/harbour/catalogue").json()
    first = cat["first_game"]
    assert first["path"] == "data/scenarios/first-passage.yaml"
    assert first["name"] == "A first passage" and len(first["says"]) == 3
    entry = next(s for s in cat["scenarios"] if s["path"] == first["path"])
    assert entry["shelf"] == "first" and cat["scenarios"][0] == entry
    reckoning = next(s for s in cat["scenarios"] if s["path"].endswith("lesson-reckoning.yaml"))
    assert reckoning["seat"] == "officer" and entry["seat"] == ""

    bare = Scenario()
    bare.wind_from_deg, bare.wind_speed_kn, bare.ship_heading_deg = 0.0, 15.0, 293.0
    a = make_world(7, "data/ships/frigate-36.yaml", bare)
    sf = load_scenario(SCENARIOS / "first-passage.yaml")
    assert sf.seed == 7 and not sf.standing_orders and not sf.orders
    b = make_scenario_world(sf)
    begin(b, sf)
    chapter = (ROOT / "docs" / "primer" / "07-a-first-passage.md").read_text(encoding="utf-8")
    blocks = re.findall(r"```orders frigate[^\n]*\n(.*?)```", chapter, re.S)[:5]
    assert len(blocks) == 5
    given = 0
    for block in blocks:
        for line in (ln.strip() for ln in block.strip().splitlines()):
            if not line or line.startswith("#") or line == "state":
                continue
            ticks = re.fullmatch(r"tick (\d+)", line)
            for w in (a, b):
                if ticks:
                    w.run(int(ticks.group(1)))
                else:
                    w.submit(line)
            given += 1
    assert given > 20 and a.clock.tick == b.clock.tick > 4000
    la = [(e.tick, e.kind, e.text) for e in a.log]
    lb = [(e.tick, e.kind, e.text) for e in b.log]
    assert la[0][2].startswith("Open water.") and lb[0][2].startswith("A first passage.")
    assert la[0][2].split(". ", 1)[1] == lb[0][2].split(". ", 1)[1]
    assert la[1:] == lb[1:] and len(la) > 150


def test_the_state_lists_the_saves_by_name_newest_first_and_opens_none(port, client):
    saves = port.tmp / "saves"
    saves.mkdir(parents=True, exist_ok=True)
    (saves / "older.json").write_text("not a save: its name alone is listed", encoding="utf-8")
    (saves / "newer.json").write_text("{}", encoding="utf-8")
    os.utime(saves / "older.json", (1_700_000_000, 1_700_000_000))
    (saves / "newer.checkpoint").write_text("", encoding="utf-8")
    (saves / "notes.txt").write_text("", encoding="utf-8")
    state = client.get("/api/harbour/state").json()["saves"]
    assert state["place"] == str(saves.resolve())
    assert [s["name"] for s in state["saves"]] == ["newer", "older"]
    assert state["saves"][1]["written"].startswith("2023-11-1")


def test_a_scenario_says_what_it_is_before_it_is_started_and_who_may_be_gone_aboard(client):
    """Package 96b, step 3: the page asks what a scenario is before the start: its own
    lines as a driver prints them (the file's path left out), and the other ships with a
    captain of their own, which the player may be aboard from the first minute."""
    r = client.get("/api/harbour/scenario", params={"path": "data/scenarios/tender.yaml"}).json()
    assert r["lines"][0] == "Scenario: The tender, Torbay for Plymouth and home."
    assert any(ln.startswith("She starts at") for ln in r["lines"]) and r["refusal"] == ""
    assert r["aboard"] == ["Raven"]
    first = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/first-passage.yaml"}
    ).json()
    assert first["aboard"] == [] and first["lines"] == ["Scenario: A first passage."]


def test_a_game_is_started_aboard_another_ship_and_a_bare_ship_with_her_wind_and_heading(
    port, client
):
    """Package 96b, step 3: what the command line alone could say (`--ship NAME`, `--wind`,
    `--heading`) said from the page's start; each refused in words when it is not so."""
    r = client.post(
        "/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml", "aboard": "Raven"}
    )
    assert r.status_code == 200, r.text
    assert "Following the Raven." in r.json()["lines"]
    assert r.json()["game"]["chosen"]["aboard"] == "Raven"
    with port.driver.lock:
        assert port.driver.world.followed_words == "Raven"
    r = client.post(
        "/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml", "aboard": "Nobody"}
    )
    assert r.status_code == 400 and "Nobody" in r.json()["detail"]
    # a bare ship with the primer's chapter 7 wind and heading
    r = client.post(
        "/api/harbour/start",
        json={"ship": "data/ships/frigate-36.yaml", "seed": 7, "wind": "0, 15", "heading": "293"},
    )
    assert r.status_code == 200, r.text
    with port.driver.lock:
        opening = next(e.text for e in port.driver.world.log if e.kind == "world.start")
    assert opening == "Open water. Wind N, 15 knots, a moderate breeze. Heading WNW (293°)."
    for bad in ({"wind": "north"}, {"wind": "400,15"}, {"wind": "10"}, {"heading": "999"}):
        r = client.post("/api/harbour/start", json={"ship": "data/ships/cutter.yaml", **bad})
        assert r.status_code == 400, (bad, r.text)
        assert "wind" in r.json()["detail"] or "heading" in r.json()["detail"]


def test_the_catalogue_gives_each_kind_her_file_fit_and_roles_and_each_file_her_fits(client):
    """Package 96b, step 5: what the ship's card fills its blanks from, the game's own
    (`world.ships.description`, each ship file's `armament`): nothing invented by the page."""
    cat = client.get("/api/harbour/catalogue").json()
    kinds = {k["id"]: k for k in cat["kinds"]}
    assert list(kinds) == cat["descriptions"]
    revenue = kinds["revenue cutter"]
    assert revenue["file"] == "data/ships/cutter.yaml" and revenue["fit"] == "long guns"
    assert revenue["roles"] == ["revenue"] and "cutter" in revenue["rig"]
    assert kinds["merchant brig"]["roles"] == ["merchant", "packet", "indiaman"]
    assert kinds["sixty-four"]["roles"] == []  # her file gives her kind none
    cutter = cat["fits"]["data/ships/cutter.yaml"]
    assert cutter == {"fits": ["carronades", "long guns"], "default": "carronades"}
    assert len(cat["fits"]["data/ships/seventy-four.yaml"]["fits"]) == 3
    assert set(cat["fits"]) == set(cat["ships"])  # every ship offered, and no boat
    # step 7: each ship's wardroom posts, and the signal books there are
    posts = cat["posts"]["data/ships/frigate-36.yaml"]
    assert posts[:2] == ["captain", "first lieutenant"] and "master" in posts
    assert cat["posts"]["data/ships/privateer-schooner.yaml"] == []  # no wardroom file
    assert {"britain", "france"} <= set(cat["signal_books"]) and "basic" not in cat["signal_books"]
    # step 6: what a squadron's card chooses from, the game's own
    assert cat["squadrons"] == {
        "kinds": ["squadron", "convoy"],
        "formations": ["line ahead", "line abreast", "order of sailing", "close order"],
        "books": ["blockade", "convoy", "squadron"],
        "player": "the ship",
    }


def test_the_proof_says_a_fit_her_kind_has_not_and_a_heading_read_by_nothing(client):
    """Package 96b, step 5 (the design's traps 4 and 5): the loader takes another ship's
    fit unchecked and refuses her only when she is promoted, and reads her heading
    nowhere; the maker's proof says both, and proves the scenario as the game does."""
    fields = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/first-action.yaml"}
    ).json()["fields"]
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})

    def of_ships(lines):  # the proof's lines on the ships (step 8 added others)
        return [ln for ln in lines if "To know" in ln and ("fit" in ln or "heading" in ln)]

    assert r.status_code == 200 and not of_ships(r.json()["lines"])
    fields["ships"][0]["fit"] = "forty carronades"
    fields["ships"][0]["heading_deg"] = 90
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert r.status_code == 200, r.text
    said = of_ships(r.json()["lines"])
    assert len(said) == 2 and "forty carronades" in said[0] and "is none of her file's" in said[0]
    assert "heading is read by nothing" in said[1]
    fields["ships"][0]["fit"] = "unarmed"
    del fields["ships"][0]["heading_deg"]
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert not of_ships(r.json()["lines"])


def test_the_keys_the_proof_takes_for_the_loaders_are_the_keys_the_loader_reads():
    """Package 96b, step 8: the maker's proof says of a key the loader does not read that it
    does nothing. The page's server keeps the loader's keys as a list (it may not change
    the loader); this holds the list to the loader's own source, every key it asks its
    file for, so that a key the loader learns to read is not said to be read by nothing."""
    import re

    from freesail.ui.harbour import LOADER_KEYS

    source = (ROOT / "freesail" / "world" / "scenarios.py").read_text(encoding="utf-8")
    body = source[source.index("def load_scenario(") : source.index("STATION_HOLDERS = (")]
    asked = set(re.findall(r'(?<![a-z_])raw\.get\("([a-z_]+)"', body))
    asked |= set(re.findall(r'raw\["([a-z_]+)"\]', body))
    asked |= set(re.findall(r'"([a-z_]+)" in raw\b', body))
    assert asked == set(LOADER_KEYS), sorted(asked ^ set(LOADER_KEYS))


def test_the_proof_says_what_the_game_reads_nowhere_and_the_year_that_is_not_1805(client):
    """Package 96b, step 8 (the design's traps 1, 2, 3 and 6)."""
    fields = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/the-faro.yaml"}
    ).json()["fields"]
    fields["weather_bund"] = "seasonal"  # a key misspelt
    fields["stations"] = {"captain": "model", "officer": "player"}
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert r.status_code == 200, r.text
    said = [ln.strip() for ln in r.json()["lines"] if "To know" in ln]
    assert any("'weather_bund' is no key the game reads" in ln for ln in said)
    assert any(
        "the chart's year and the almanac in her papers are read by nothing" in ln for ln in said
    )
    assert any("'model' and 'rules' (captain) seat nobody" in ln for ln in said)
    assert any(
        "she begins in 1808" in ln and "the wars are those of June 1805" in ln for ln in said
    )
    cat = client.get("/api/harbour/catalogue").json()
    years = {Path(s["path"]).stem: s["year"] for s in cat["scenarios"]}
    assert years["the-faro"] == 1808 and years["tarragona"] == 1809
    assert years["first-action"] == 1805 and years["first-passage"] is None


def test_the_systems_and_the_ports_state_are_read_as_words_and_refused_in_words(client):
    """Package 96b, step 8 (the design's §2.5): the two blocks offered as the file's own
    words. A scenario's systems and its ports' state come to the page as text; text sent
    back is read into the fields before the proof (only the blocks sent), and words that
    are no YAML, or not of the block's shape, are refused in words; what a system may say
    is the loader's to refuse, as ever."""
    read = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/blockade.yaml"}
    ).json()
    fields, blocks = read["fields"], read["blocks"]
    # the blockade's ports are a list: the box holds it as the mapping it means, each port
    # with nothing said of it, so that a state added there keeps the other ports
    assert blocks["ports"] == "brest: {}\nfalmouth: {}\nplymouth: {}\ntorbay: {}\n"
    assert "name: the low" in blocks["systems"]

    def prove(**sent):
        return client.post(
            "/api/harbour/scenario/prove",
            json={"fields": fields, "source": read["path"], "blocks": sent},
        )

    assert prove().json()["text"] == read["text"]  # nothing sent: the file as it was
    assert prove(systems=blocks["systems"]).json()["text"] == read["text"]  # the same words
    renamed = prove(systems=blocks["systems"].replace("the low", "the deep low"))
    assert renamed.status_code == 200 and "the deep low (low" in "\n".join(renamed.json()["lines"])
    none = prove(systems="")
    assert none.status_code == 400 and "pinned sky" in none.json()["detail"]  # the loader's
    for words, why in (
        ("- name: [", "could not be read"),
        ("name: the low", "are a list"),
        ("- {name: a low, kind: typhoon, track: []}", "typhoon"),
    ):
        r = prove(systems=words)
        assert r.status_code == 400 and why in r.json()["detail"], (words, r.text)
    state = prove(
        ports="brest:\n  closed_to: [britain]\n  news: ['The fleet is in.']\nfalmouth: {}\n"
    )
    assert state.status_code == 200, state.text
    assert "The ports: brest, falmouth." in state.json()["lines"]
    assert "closed_to: [britain]" in state.json()["text"]
    assert prove(ports="- brest").status_code == 400
    assert prove(tides="x").status_code == 400
    # a port closed in the box as it came up: the other ports are still in play
    closed = prove(ports=blocks["ports"].replace("brest: {}", "brest: {closed_to: [britain]}"))
    assert "The ports: brest, falmouth, plymouth, torbay." in closed.json()["lines"]


def test_a_box_of_the_files_words_takes_no_anchor_no_alias_and_no_more_than_its_length(
    port, client, monkeypatch
):
    """Package 96b, the final list, item 1 (the whole-page reader's finding): 574 bytes of
    nested YAML aliases in the ports' box held the server at full CPU and gigabytes. The
    box's words take no anchor and no alias, and no more than their length: refused in
    words by the text's tokens before anything is loaded (the loader is never called), at
    the proof and at the save; words with none pass as before."""
    import yaml as yaml_mod

    fields = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/blockade.yaml"}
    ).json()["fields"]
    bomb = "a: &a [x, x, x, x, x, x, x, x, x]\nb: &b [*a, *a, *a, *a, *a, *a, *a, *a, *a]\n"
    bomb += "c: &c [*b, *b, *b, *b, *b, *b, *b, *b, *b]\nbrest: {news: *c}\n"
    # A Harbour begins reading the ships' fits on a thread as it is built (`Harbour.fits`,
    # every ship's file, each longer than a box may be), and a loader patched while that
    # thread reads is given their texts. Wait for it first, so that what the loader is
    # given below is the box's words alone, whichever test this process ran before (the
    # test failed where it ran first in its worker: the cloud's run 147).
    port.harbour.fits()
    loads: list[str] = []
    real = yaml_mod.safe_load
    monkeypatch.setattr(yaml_mod, "safe_load", lambda text: loads.append(str(text)) or real(text))
    started = time.monotonic()
    for route, body in (
        ("/api/harbour/scenario/prove", {"fields": fields, "blocks": {"ports": bomb}}),
        ("/api/harbour/scenario", {"fields": fields, "blocks": {"ports": bomb}, "name": "bomb"}),
        (
            "/api/harbour/scenario/prove",
            {"fields": fields, "blocks": {"systems": "- &s {name: a}"}},
        ),
        ("/api/harbour/scenario/prove", {"fields": fields, "blocks": {"ports": "x: 1\n" * 5000}}),
    ):
        r = client.post(route, json=body)
        assert r.status_code == 400, (route, r.text[:200])
        why = r.json()["detail"]
        assert "an anchor or an alias (& or *)" in why or "at most" in why, why
    assert time.monotonic() - started < 5.0
    assert not [text for text in loads if "&" in text or len(text) > 20_000]
    assert not (port.place / "bomb.yaml").exists()
    ok = client.post(
        "/api/harbour/scenario/prove",
        json={"fields": fields, "blocks": {"ports": "brest: {news: ['R & R, *as ever*']}\n"}},
    )
    assert ok.status_code == 200, ok.text  # the signs within a quoted word are words


def test_the_proof_says_a_port_leaned_on_that_is_not_in_play(client):
    """The final list, item 2: the ports in play named, and a port a ship is leaving or a
    price list aboard not among them, said at the proof."""
    fields = client.get(
        "/api/harbour/scenario", params={"path": "data/scenarios/merchant-passage.yaml"}
    ).json()["fields"]
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    assert not [ln for ln in r.json()["lines"] if "ports in play" in ln or "port in play" in ln]
    fields["ports"] = ["brest"]
    fields["ships"][0]["departing"] = "plymouth"
    r = client.post("/api/harbour/scenario/prove", json={"fields": fields})
    said = [ln.strip() for ln in r.json().get("lines", []) if "To know" in ln]
    if r.status_code == 200:
        assert any("is leaving plymouth, which is not among the ports in play" in ln for ln in said)
        assert any("the price list of falmouth is aboard" in ln for ln in said)
    else:  # the game's own refusal of the port she leaves comes first, in its words
        assert "plymouth" in r.json()["detail"].lower()
        warned = port_warnings(fields)
        assert any("is leaving plymouth" in ln for ln in warned)
        assert any("the price list of falmouth is aboard" in ln for ln in warned)


def port_warnings(fields: dict[str, Any]) -> list[str]:
    return Harbour.unread_warnings(None, fields)


# The controls whose own label is their sentence (a tick box's words, a box of the file's
# words with its explanation above it), and the one that is a button's choice.
SAID_BY_ITS_LABEL = {"#m-chron-on", "#m-systems", "#m-ports-state", "#m-brief-from"}


def page_controls() -> list[str]:
    """Every control written in the page's HTML, by the selector the sentences are kept
    under: its id, else its data-field, data-set, data-brief or data-chron."""
    import re

    page = (ROOT / "client" / "harbour.html").read_text(encoding="utf-8")
    out = []
    for attrs in re.findall(r"<(?:input|select|textarea)\b([^>]*)>", page):
        ident = re.search(r'\bid="([^"]+)"', attrs)
        data = re.search(r'data-(field|set|brief|chron)="([^"]+)"', attrs)
        assert ident or data, attrs
        out.append(f"#{ident.group(1)}" if ident else f'[data-{data.group(1)}="{data.group(2)}"]')
    return out


def page_words() -> dict[str, str]:
    text = (ROOT / "client" / "harbour-words.js").read_text(encoding="utf-8")
    start = text.index("window.freesailHarbourWords = ") + len("window.freesailHarbourWords = ")
    return json.loads(text[start : text.rindex(";")])


def test_every_control_of_the_page_has_its_sentence_in_the_one_file():
    """Package 96b, step 10 (docs/design/Design-Harbour.md §2.7; the owner's point of
    2026-10-18: the flags unexplained where they are set): the page's sentences are one
    file, one for each control the page's HTML has; none is left without, none of the
    file's is for a control that is not there, and no sentence is left as a hover text."""
    controls, words = page_controls(), page_words()
    assert len(controls) > 110 and len(set(controls)) == len(controls)
    assert set(controls) - set(words) == SAID_BY_ITS_LABEL
    assert set(words) <= set(controls), sorted(set(words) - set(controls))
    assert all(len(w) > 12 and w.endswith((".", ")")) for w in words.values())
    page = (ROOT / "client" / "harbour.html").read_text(encoding="utf-8")
    import re

    assert not re.search(r"<label\b[^>]*\btitle=", page)  # a control's words are under it
    assert '<script src="/client/harbour-words.js"></script>' in page


def test_the_primer_and_the_readme_name_the_tabs_and_the_first_game_the_page_has():
    """Package 96b, step 11: the primer's paragraph on going aboard and the README's on the
    harbour say what the page is: the tabs by the names on them, and the first game by the
    name on its button."""
    import re

    page = (ROOT / "client" / "harbour.html").read_text(encoding="utf-8")
    tabs = re.findall(r'<button type="button" data-tab="[a-z]+"[^>]*>([^<]+)</button>', page)
    assert tabs == ["begin", "game", "stations", "scenario maker", "settings"]
    first = yaml_name(SCENARIOS / "first-passage.yaml")
    for words in (
        (ROOT / "docs" / "primer" / "01-the-ship.md").read_text(encoding="utf-8"),
        (ROOT / "README.md").read_text(encoding="utf-8"),
    ):
        for tab in tabs:
            assert f"**{tab}**" in words, tab
        assert first in words and "chapter 7" in words
        assert "the server's flags as its controls" not in words


def yaml_name(path: Path) -> str:
    import yaml

    return str(yaml.safe_load(path.read_text(encoding="utf-8"))["name"])


def test_the_shelves_file_names_only_scenarios_that_are_there_and_each_once():
    from freesail.ui.harbour import SHELVES_FILE, Harbour

    # the page's own, with the page's files: not among the scenarios (the tests that walk
    # them would take it for one), and not under data/ at all (the range's audit classes
    # every dated key there, and the rules' fingerprint hashes every file there)
    assert SHELVES_FILE.parent != SCENARIOS
    assert ROOT / "data" not in SHELVES_FILE.parents
    assert SHELVES_FILE == ROOT / "client" / "harbour-shelves.yaml" and SHELVES_FILE.is_file()
    assert not (ROOT / "data" / "harbour").exists()
    named = [s["file"] for shelf in Harbour.shelves(None) for s in shelf["scenarios"]]
    assert len(named) == len(set(named))
    there = {p.stem for p in SCENARIOS.glob("*.yaml")}
    assert set(named) <= there, sorted(set(named) - there)
    assert all(s["says"] for shelf in Harbour.shelves(None) for s in shelf["scenarios"])


def _started_while_a_page_asks(port, choices: dict[str, Any]) -> tuple[dict, list[dict]]:
    """A game started with the state asked from another thread at every line `Harbour.start`
    runs, as a page's poll may land: the game's answer and all that was seen. An asking held
    by a lock reads when the lock is let go."""
    import sys
    import threading

    from freesail.ui.harbour import Harbour

    seen: list[dict] = []
    askers: list[threading.Thread] = []

    def at_each_line(frame, event, arg):
        if event == "line":
            asker = threading.Thread(target=lambda: seen.append(port.harbour.game_state()))
            asker.start()
            asker.join(0.05)
            askers.append(asker)
        return at_each_line

    def tracer(frame, event, arg):
        return at_each_line if frame.f_code is Harbour.start.__code__ else None

    sys.settrace(tracer)
    try:
        out = port.harbour.start(choices)
    finally:
        sys.settrace(None)
    for asker in askers:
        asker.join(5)
    return out["game"], seen


def test_a_page_that_asks_while_a_game_starts_finds_one_whole_game(port, client):
    """The harbour's start said the game started and then read the scenario's plan of the
    stations into its words, and `game_state` reads under the driver's lock, not the
    harbour's: a page that asked between found a game started with no plan, and its stations'
    table showed the officer with no model asked for (the browser's test of that table failed
    once in many runs beside other workers; found by package 90's engine builder); and at a
    second start it could find the new world beside the last game's words and plan (the
    lead's checker, who wrote this probe). The state is asked at every line of the start,
    twice over: whatever a page sees is one whole game."""
    (port.place / "planned.yaml").parent.mkdir(parents=True, exist_ok=True)
    (port.place / "planned.yaml").write_text(
        (SCENARIOS / "tender.yaml").read_text(encoding="utf-8") + "\nstations:\n  officer: model\n",
        encoding="utf-8",
    )
    planned = {"officer": "model"}
    game, seen = _started_while_a_page_asks(
        port, {"scenario": str(port.place / "planned.yaml"), "seed": 111}
    )
    assert game["started"] and game["chosen"]["plan"] == planned and len(seen) > 5
    torn = [
        (s["started"], s["seed"], s["chosen"].get("plan"))
        for s in seen
        if s["started"] and s["chosen"].get("plan") != planned
    ]
    assert not torn, ("the first start", torn)
    # a second game in place of the first: the world of seed 222 only with its own words (no
    # plan), the world of seed 111 only with the first's
    game, seen = _started_while_a_page_asks(
        port, {"scenario": "data/scenarios/tender.yaml", "seed": 222}
    )
    assert game["seed"] == 222 and game["chosen"]["plan"] == {} and len(seen) > 5
    torn = [
        (s["seed"], s["chosen"].get("scenario"), s["chosen"].get("plan"))
        for s in seen
        if s["chosen"].get("plan") != ({} if s["seed"] == 222 else planned)
    ]
    assert not torn, ("the second start", torn)


def test_a_game_started_with_a_seat_and_a_brief_is_the_servers_game_taken_up_in_place(port, client):
    """Truth 7b-108's middle (the whole in test_known_truths): one server, its World
    replaced, the pages told, the clock held, the seat and the director's brief given by
    the server's own start."""
    old = port.driver.world
    told: list[dict[str, Any]] = []
    port.driver.add_listener(told.append)
    refused = client.post("/api/harbour/start", json={})
    assert refused.status_code == 400 and "Choose a scenario" in refused.json()["detail"]
    bad = client.post(
        "/api/harbour/start",
        json={"scenario": "data/scenarios/lesson-falmouth.yaml", "seat": "bosun's cat"},
    )
    assert bad.status_code == 400 and "not seated" in bad.json()["detail"]
    r = client.post(
        "/api/harbour/start",
        json={
            "scenario": "data/scenarios/dispatches-falmouth.yaml",
            "seat": "officer",
            "director_brief": "quiet-passage",
            "pace": "lockstep",
            "time": 10,
        },
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["lines"][0].startswith("Scenario: The dispatches")
    game = body["game"]
    assert game["started"] and game["running"] is False  # held until the driver says go
    assert game["seat"] == "the player at the officer of the watch's station"
    assert game["director"] == "A quiet passage" and game["compression"] == 10
    assert port.driver.world is not old and port.driver.lockstep
    assert {"type": "restart"} in told
    held = client.get("/api/harbour/state").json()["stations"]
    assert [s["holder"] for s in held] == ["the player"]
    assert client.get("/", follow_redirects=False).status_code == 200
    assert client.get("/harbour").status_code == 200  # still there while the game runs
    # the game page's own routes read the new game
    assert client.get("/api/state").json()["driver"]["running"] is False
    assert client.get("/api/ship").json()["name"] == "Sherbourne"


# ---------------------------------------------------------------------------
# The scenario maker
# ---------------------------------------------------------------------------


def test_the_maker_reads_proves_and_saves_in_the_players_place(port, client):
    r = client.get("/api/harbour/scenario", params={"path": "data/scenarios/smack-falmouth.yaml"})
    assert r.status_code == 200
    got = r.json()
    assert got["fields"]["ship"]["file"] == "data/ships/smack.yaml"
    assert got["position_deg"] == [50.1631, -5.0345]
    proved = client.post(
        "/api/harbour/scenario/prove", json={"fields": got["fields"], "source": got["path"]}
    ).json()
    assert proved["lines"][0] == "Scenario: A smack out of Falmouth (this scenario)."
    # a refusal in the form's words: the loader's, with no temporary file named
    bad = dict(got["fields"], ship=dict(got["fields"]["ship"], file="data/ships/nope.yaml"))
    r = client.post("/api/harbour/scenario/prove", json={"fields": bad})
    assert r.status_code == 400 and r.json()["detail"] == "data/ships/nope.yaml: no such ship file."
    r = client.post(
        "/api/harbour/scenario/prove",
        json={"fields": dict(got["fields"], stations={"officer": "somebody"})},
    )
    assert r.status_code == 400 and r.json()["detail"].startswith("stations officer:")
    r = client.post(
        "/api/harbour/scenario/prove",
        json={"fields": dict(got["fields"], orders=["splice the main brace sideways"])},
    )
    assert r.status_code == 400 and "refused" in r.json()["detail"]
    # saved: the same bytes, with nothing changed
    saved = client.post(
        "/api/harbour/scenario",
        json={"fields": got["fields"], "source": got["path"], "name": "smack"},
    ).json()
    assert Path(saved["path"]) == port.place / "smack.yaml"
    assert (port.place / "smack.yaml").read_bytes() == (
        SCENARIOS / "smack-falmouth.yaml"
    ).read_bytes()
    again = client.post("/api/harbour/scenario", json={"fields": got["fields"], "name": "smack"})
    assert again.status_code == 409 and "there already" in again.json()["detail"]
    # listed by the harbour as the player's own, and read back from there
    cat = client.get("/api/harbour/catalogue").json()
    own = [s for s in cat["scenarios"] if s["own"]]
    assert [s["name"] for s in own] == ["A smack out of Falmouth"]
    assert client.get("/api/harbour/scenario", params={"path": own[0]["path"]}).status_code == 200
    # a drafted book goes beside it and is named in its standing orders
    fields = dict(got["fields"], name="A smack with a book of her own")
    made = client.post(
        "/api/harbour/scenario",
        json={
            "fields": fields,
            "name": "booked",
            "book": 'standing order "watch": at sunset then take in the topsail',
        },
    ).json()
    assert Path(made["book"]).read_text(encoding="utf-8").startswith("standing order")
    assert made["book"] in made["text"]


def test_the_maker_reads_only_the_games_scenarios_and_the_players_own(client):
    r = client.get("/api/harbour/scenario", params={"path": "data/ships/smack.yaml"})
    assert r.status_code == 403
    r = client.get("/api/harbour/scenario", params={"path": "/etc/hostname.yaml"})
    assert r.status_code == 403


def test_a_new_scenario_from_the_form_loads_at_the_console_and_reads_back_unchanged(port, client):
    from freesail.ui.console import start_world, station_watcher  # noqa: F401
    from freesail.ui.server import server_parser
    from freesail.world.scenarios import load_scenario

    fields = {
        "name": "A cutter to Plymouth",
        "seed": 7,
        "start": "1805-06-12T05:00",
        "position": {"lat_deg": 50.1631, "lon_deg": -5.0345},
        "region": "channel-west",
        "nation": "britain",
        "ship": {"file": "data/ships/cutter.yaml", "heading_deg": 190, "glass": True},
        "weather": {"wind": [{"at": "1805-06-12T05:00", "from_deg": 225, "knots": 15}]},
        "ships": [
            {
                "id": "lark",
                "description": "cutter",
                "name": "Lark",
                "nation": "britain",
                "position": "49 55 N 5 45 W",
                "goal": "patrolling off the Wolf within 4 miles",
            }
        ],
        "business": False,
        "orders": ["let go the best bower"],
        "stations": {"officer": "player", "director": "model"},
        "director": {"brief": "dispatches"},
    }
    saved = client.post("/api/harbour/scenario", json={"fields": fields, "name": "plymouth"})
    assert saved.status_code == 200, saved.text
    path = Path(saved.json()["path"])
    text = path.read_text(encoding="utf-8")
    assert "business: off" in text and "# The other sail on the sea" in text
    # at the console as a hand-made one: the seat the file's
    args = server_parser().parse_args(["--scenario", str(path)])
    world, sf = start_world(args)
    assert sf.player_seat == "officer" and load_scenario(path).scenario.business == "off"
    # read back into the form and written again unchanged
    got = client.get("/api/harbour/scenario", params={"path": str(path)}).json()
    assert got["fields"]["stations"] == fields["stations"]
    client.post(
        "/api/harbour/scenario",
        json={"fields": got["fields"], "source": str(path), "name": "plymouth"},
    )
    assert path.read_text(encoding="utf-8") == text


def test_the_chart_for_pricking_a_start(client):
    c = client.get("/api/harbour/chart", params={"region": "channel-west"}).json()
    assert c["bounds"] == {"south": 48.0, "north": 51.0, "west": -7.0, "east": -3.0}
    assert len(c["coast"]) > 10 and any(p["id"] == "falmouth" for p in c["ports"])
    assert client.get("/api/harbour/chart", params={"region": "atlantis"}).status_code == 404


# ---------------------------------------------------------------------------
# The settings and the desktop client
# ---------------------------------------------------------------------------


def test_the_settings_are_kept_from_the_form_and_a_key_is_refused(port, client):
    got = client.get("/api/harbour/settings").json()
    assert got["path"] == str(port.settings_path) and got["error"] == ""
    s = got["settings"]
    s["doors"]["api"]["model"] = PLACEHOLDER
    r = client.post("/api/harbour/settings", json={"settings": s})
    assert r.status_code == 200 and r.json()["settings"]["doors"]["api"]["model"] == PLACEHOLDER
    s["doors"]["api"]["api_key"] = "x"
    r = client.post("/api/harbour/settings", json={"settings": s})
    assert r.status_code == 400 and "no key" in r.json()["detail"]
    assert "api_key" not in port.settings_path.read_text(encoding="utf-8")


def test_the_desktop_entries_are_shown_first_and_written_on_the_word(port, client):
    path = port.tmp / "Claude" / "claude_desktop_config.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"mcpServers": {"another": {"command": "x"}}}), encoding="utf-8")
    shown = client.post("/api/harbour/desktop", json={"stations": ["captain", "director"]}).json()
    assert sorted(shown["entries"]) == ["freesail-captain", "freesail-director"]
    assert shown["written"] is False and shown["named"] is False
    assert json.loads(path.read_text(encoding="utf-8")) == {
        "mcpServers": {"another": {"command": "x"}}
    }
    assert '"another"' in shown["text"] and S.MODEL_NAME_PLACEHOLDER in shown["text"]
    written = client.post(
        "/api/harbour/desktop", json={"stations": ["captain", "director"], "write": True}
    ).json()
    assert written["written"] and Path(written["backup"]).exists()
    doc = json.loads(path.read_text(encoding="utf-8"))
    assert sorted(doc["mcpServers"]) == ["another", "freesail-captain", "freesail-director"]
    args = doc["mcpServers"]["freesail-director"]["args"]
    assert args[args.index("--station") + 1] == "director"
    state = client.get("/api/harbour/state").json()
    assert state["desktop"]["entries"] == ["freesail-captain", "freesail-director"]
    none = client.post("/api/harbour/desktop", json={"stations": []})
    assert none.status_code == 400


def test_the_shortcut_is_shown_before_it_is_written(client):
    r = client.post("/api/harbour/shortcut", json={}).json()
    assert r["written"] is False and "freesail" in r["text"]


# ---------------------------------------------------------------------------
# The doors as the server's subprocesses, on a live server
# ---------------------------------------------------------------------------


def _free_port() -> int:
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return int(s.getsockname()[1])


class Live:
    """The harbour's server on a port of this process, as `py -m freesail` serves it."""

    def __init__(self, port: Port):
        import uvicorn

        self.port = port
        self.number = _free_port()
        self.url = f"http://127.0.0.1:{self.number}"
        port.harbour.game_url = self.url
        self.server = uvicorn.Server(
            uvicorn.Config(port.app, host="127.0.0.1", port=self.number, log_level="warning")
        )
        self.thread = threading.Thread(target=self.server.run, daemon=True)
        self.thread.start()
        deadline = time.monotonic() + 20
        while not self.server.started:
            assert time.monotonic() < deadline and self.thread.is_alive()
            time.sleep(0.05)

    @property
    def page(self) -> dict[str, str]:
        """The headers of the game's own page (package 115): its origin and its mark."""
        return {"x-freesail-page": self.port.app.state.guard.token, "origin": self.url}

    def close(self) -> None:
        self.server.should_exit = True
        self.thread.join(timeout=15)


def _until(test: Any, seconds: float = 60.0) -> Any:
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        got = test()
        if got:
            return got
        time.sleep(0.2)
    raise AssertionError("not there in time")


def test_a_door_that_dies_is_said_so_in_its_pane(tmp_path):
    port = Port(tmp_path, {"doors": {"local": {"endpoint": "http://127.0.0.1:9"}}})
    live = Live(port)
    try:
        import httpx

        with httpx.Client(base_url=live.url, timeout=60, headers=live.page) as c:
            refused = c.post("/api/harbour/doors", json={"door": "local", "station": "watcher"})
            assert refused.status_code == 400 and "Start a game first" in refused.json()["detail"]
            c.post("/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"})
            d = c.post("/api/harbour/doors", json={"door": "local", "station": "watcher"}).json()
            assert d["state"] == "running" and d["words"].startswith(
                "The local runner at the watcher"
            )
            out = _until(
                lambda: (
                    (r := c.get(f"/api/harbour/doors/{d['id']}").json())["state"] == "ended" and r
                )
            )
            assert out["code"] == 2  # the local runner's EXIT_UNREACHABLE
            assert out["output"][-1].startswith(
                "== The local runner at the watcher has ended (exit code 2): it could not reach"
            )
            api = c.post("/api/harbour/doors", json={"door": "api", "station": "captain"})
            assert api.status_code == 400 and "Name the API door's model" in api.json()["detail"]
    finally:
        live.close()


def test_the_api_door_started_from_the_harbour_seats_its_station_and_is_stopped(
    tmp_path, monkeypatch
):
    """The API door as the server's subprocess, with its model and flags from the settings
    and its key from the environment it inherits (never the settings): seated at the
    watcher's station through the game's own consent records, shown held by its model in
    the harbour's state, stopped from the harbour with its station released."""
    pytest.importorskip("anthropic")
    from messages_api import MODEL, MessagesServer

    from freesail.agents import consent

    key = "a-test-key-of-no-account-0123456789"
    with MessagesServer(key) as api:
        port = Port(
            tmp_path,
            {"doors": {"api": {"model": MODEL, "flags": ["--base-url", api.url]}}},
        )
        consent.Record(MODEL, "a test runtime", "2026-10-18", consent.YES, answer="Yes.").write(
            port.records
        )
        monkeypatch.setenv("FREESAIL_API_KEY", key)
        monkeypatch.setenv("PYTHON_KEYRING_BACKEND", "keyring.backends.null.Keyring")
        live = Live(port)
        try:
            import httpx

            with httpx.Client(base_url=live.url, timeout=60, headers=live.page) as c:
                c.post(
                    "/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"}
                )
                d = c.post("/api/harbour/doors", json={"door": "api", "station": "watcher"}).json()

                def held() -> Any:
                    st = c.get("/api/harbour/state").json()["stations"]
                    return [s for s in st if s["station"] == "watcher" and s["holder"] == MODEL]

                try:
                    seated = _until(held, 90)
                except AssertionError:
                    out = c.get(f"/api/harbour/doors/{d['id']}").json()["output"]
                    raise AssertionError("\n".join(out)) from None
                assert seated[0]["door"] == "api"
                pane = c.get(f"/api/harbour/doors/{d['id']}").json()
                assert any(
                    "credential store" not in ln and "environment" in ln for ln in pane["output"]
                )
                assert not any(key in ln for ln in pane["output"])
                stopped = c.post(f"/api/harbour/doors/{d['id']}/stop").json()
                assert stopped["state"] == "stopped"
                with port.driver.lock:
                    assert port.driver.world.agents["watcher"].agent.released
                out = c.get(f"/api/harbour/doors/{d['id']}").json()["output"]
                assert out[-1].endswith("stopped from the harbour. ==")
        finally:
            live.close()


SECOND = "made-up-model-8"  # a second name of no model


def test_a_door_is_started_for_a_station_with_a_model_chosen_from_the_settings_list(
    tmp_path, monkeypatch
):
    """Package 96b, step 9 (docs/design/Design-Harbour.md §2.6; the owner's point of
    2026-10-18: two models at two stations wanted two settings files). One settings file
    names the API door's model and a second beside it (`doors.api.models`); the page's
    state offers both; a door started for a station with the second chosen is that model's
    door (its name and its dialect on the door's own command line, no seat's fold), is
    seated through the game's own consent records as any door is, and is shown holding
    the station; a model the settings do not name is refused in words and no door is
    started, and so is a model named for the local runner."""
    pytest.importorskip("anthropic")
    from messages_api import MODEL, MessagesServer

    from freesail.agents import consent

    key = "a-test-key-of-no-account-0123456789"
    with MessagesServer(key, models={MODEL: MODEL, SECOND: SECOND}) as api:
        port = Port(
            tmp_path,
            {
                "doors": {
                    "api": {
                        "model": MODEL,
                        "models": [SECOND],
                        "flags": ["--base-url", api.url],
                        "seat_budget_tokens": "80000",
                    }
                }
            },
        )
        argv = port.harbour.door_argv("api", "watcher", model=SECOND)
        assert argv[argv.index("--model") + 1] == SECOND and "--budget-tokens" not in argv
        own = port.harbour.door_argv("api", "watcher")  # the door's own model, as before
        assert own[own.index("--model") + 1] == MODEL
        consent.Record(SECOND, "a test runtime", "2026-11-15", consent.YES, answer="Yes.").write(
            port.records
        )
        monkeypatch.setenv("FREESAIL_API_KEY", key)
        monkeypatch.setenv("PYTHON_KEYRING_BACKEND", "keyring.backends.null.Keyring")
        live = Live(port)
        try:
            import httpx

            with httpx.Client(base_url=live.url, timeout=60, headers=live.page) as c:
                # the models are the settings', given to the page by the settings' route;
                # the page's state carries no model's name of the settings (truth 7b-110)
                state = c.get("/api/harbour/state")
                assert "models" not in state.json()
                assert MODEL not in state.text and SECOND not in state.text
                api_door = c.get("/api/harbour/settings").json()["settings"]["doors"]["api"]
                assert (api_door["model"], api_door["models"]) == (MODEL, [SECOND])
                c.post(
                    "/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"}
                )
                for body in (
                    {"door": "api", "station": "watcher", "model": "a-model-nobody-named"},
                    {"door": "local", "station": "watcher", "model": SECOND},
                ):
                    r = c.post("/api/harbour/doors", json=body)
                    assert r.status_code == 400, r.text
                assert c.get("/api/harbour/state").json()["doors"] == []
                d = c.post(
                    "/api/harbour/doors",
                    json={"door": "api", "station": "watcher", "model": SECOND},
                ).json()

                def held() -> Any:
                    st = c.get("/api/harbour/state").json()["stations"]
                    return [s for s in st if s["station"] == "watcher" and s["holder"] == SECOND]

                try:
                    seated = _until(held, 90)
                except AssertionError:
                    out = c.get(f"/api/harbour/doors/{d['id']}").json()["output"]
                    raise AssertionError("\n".join(out)) from None
                assert seated[0]["door"] == "api"
                assert c.post(f"/api/harbour/doors/{d['id']}/stop").json()["state"] == "stopped"
        finally:
            live.close()


def test_the_scenarios_plan_of_its_stations_and_the_other_captains_are_in_the_state(port, client):
    """Package 96b, step 9: what the stations' table is drawn from. The scenario's
    `stations:` (which the game reads only for the player's seat) comes to the page as the
    plan of the game started; the other ships with a captain of their own are named, each
    a station a door may ask for; a game from a scenario that says nothing has no plan."""
    port.place.mkdir(parents=True, exist_ok=True)
    mine = port.place / "planned.yaml"
    mine.write_text(
        (SCENARIOS / "tender.yaml").read_text(encoding="utf-8")
        + "\nstations:\n  officer: model\n  master: rules\n",
        encoding="utf-8",
    )
    r = client.post("/api/harbour/start", json={"scenario": str(mine)})
    assert r.status_code == 200, r.text
    game = client.get("/api/harbour/state").json()["game"]
    assert game["chosen"]["plan"] == {"officer": "model", "master": "rules"}
    assert game["captains"] == ["Raven"]
    client.post("/api/harbour/start", json={"scenario": "data/scenarios/first-passage.yaml"})
    game = client.get("/api/harbour/state").json()["game"]
    assert game["chosen"]["plan"] == {} and game["captains"] == []


def test_only_a_seated_station_is_held_and_the_game_refuses_a_hostile_captains_seat(
    port, client, monkeypatch
):
    """Package 96b, step 9, mended (the independent reader's findings): the page's state
    passes on each seat's phase and its ship. A seat in its consent conversation is not a
    station held, and a seat stopped (a consent declined, a door stopped before an answer)
    is nobody's; another ship's captain asked for is said with her name, not on the
    player's own captain's row. And a row the page offers changes nothing of what the game
    admits: a model asked for as the captain of an enemy of the player's ship is refused
    by the game in its own words, before any station is made.

    Package 117 turned `seats.ADVERSARIAL_SEATS_CONSENTED`: the refusal is the gate's while
    the flag is not turned, and is held so here; at the end, the flag turned, the same seat
    is admitted to its consent conversation (a station in its consent phase, nobody's
    until it answers)."""
    from freesail.world import seats as seat_rules

    monkeypatch.setattr(seat_rules, "ADVERSARIAL_SEATS_CONSENTED", False)
    client.post("/api/harbour/start", json={"scenario": "data/scenarios/first-action.yaml"})
    assert client.get("/api/harbour/state").json()["game"]["captains"] == ["Renard"]
    seat = {"model_name": "made-up-b", "door": "api", "ship": "Renard"}
    r = client.post("/api/agents/captain", json=seat)
    assert r.status_code == 403 and "the game seats no model as the captain of the Renard" in r.text
    assert client.get("/api/harbour/state").json()["stations"] == []
    client.post("/api/harbour/start", json={"scenario": "data/scenarios/tender.yaml"})
    client.post("/api/agents/officer", json={"model_name": "made-up-a", "door": "api"})
    client.post(
        "/api/agents/captain", json={"model_name": "made-up-b", "door": "api", "ship": "Raven"}
    )

    def seats() -> list[tuple[str, str, str, str]]:
        st = client.get("/api/harbour/state").json()["stations"]
        return [(s["station"], s["ship"], s["holder"], s["phase"]) for s in st]

    assert seats() == [
        ("officer of the watch", "", "made-up-a", "consent"),
        ("captain", "Raven", "made-up-b", "consent"),
    ]
    desk = port.driver.desk
    for held in list(desk.seats.values()):
        with port.driver.lock:
            desk.release(held.station, "stopped by the test", held.key, held.ship)
    assert seats() == [
        ("officer of the watch", "", "made-up-a", "stopped"),
        ("captain", "Raven", "made-up-b", "stopped"),
    ]
    monkeypatch.setattr(seat_rules, "ADVERSARIAL_SEATS_CONSENTED", True)
    client.post("/api/harbour/start", json={"scenario": "data/scenarios/first-action.yaml"})
    r = client.post("/api/agents/captain", json=seat)
    assert r.status_code == 200, r.text
    assert seats() == [("captain", "Renard", "made-up-b", "consent")]


# ---------------------------------------------------------------------------
# The page in the browser
# ---------------------------------------------------------------------------


def chromium_path() -> str | None:
    named = os.environ.get("FREESAIL_CHROMIUM")
    if named and Path(named).exists():
        return named
    folder = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if folder and (Path(folder) / "chromium").exists():
        return str(Path(folder) / "chromium")
    return None


@pytest.fixture
def browser_page(tmp_path):
    sync_api = pytest.importorskip("playwright.sync_api", reason="Playwright is not installed")
    port = Port(tmp_path)
    live = Live(port)
    try:
        pw = sync_api.sync_playwright().start()
    except Exception as e:  # noqa: BLE001
        live.close()
        pytest.skip(f"Playwright could not start: {e}")
    try:
        browser = pw.chromium.launch(headless=True, executable_path=chromium_path())
    except Exception as e:  # noqa: BLE001
        pw.stop()
        live.close()
        pytest.skip(f"no browser for Playwright here: {e}")
    errors: list[str] = []
    try:
        pg = browser.new_page(viewport={"width": 1280, "height": 1000})
        pg.on("pageerror", lambda e: errors.append(str(e)))
        yield pg, live, port, errors
    finally:
        browser.close()
        pw.stop()
        live.close()


def test_in_the_browser_a_game_is_started_and_the_four_scenarios_round_trip(browser_page):
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/")
    assert pg.url.endswith("/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.inner_text("#status") == "no game yet"
    # a game with a seat and a director's brief
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/directed-passage.yaml")
    pg.select_option("#s-seat", "officer")
    assert not pg.is_visible("#s-brief")  # behind "more for this game" (package 96b, step 3)
    pg.click("#s-more summary")
    pg.select_option("#s-brief", "dispatches")
    pg.click("#btn-start")
    pg.wait_for_selector("#btn-to-game:not([hidden])", timeout=60_000)
    pg.wait_for_function(
        "document.getElementById('g-director').textContent === 'The dispatches'", timeout=10_000
    )
    pg.wait_for_function(
        "document.getElementById('g-stations').textContent.indexOf('officer of the watch') >= 0",
        timeout=10_000,
    )
    assert pg.inner_text("#status") == "a game in play"
    # the maker: each of the owner's scenarios read into the form and saved, byte for byte
    pg.click("nav.tabs button[data-tab=maker]")
    for stem in THE_FOUR:
        pg.select_option("#m-pick", f"data/scenarios/{stem}.yaml")
        pg.click("#btn-m-read")
        pg.wait_for_function(
            f"document.getElementById('m-source').textContent.indexOf('{stem}') >= 0"
        )
        pg.click("#btn-m-save")
        pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
        pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
        assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
        saved = port.place / f"{stem}.yaml"
        assert saved.read_bytes() == (SCENARIOS / f"{stem}.yaml").read_bytes(), stem
    # one field changed in the form: that field alone written again (the part opened
    # first: the sheet is folded, package 96b, step 4)
    assert not pg.is_visible('#maker [data-field="seed"]')
    pg.click("#maker fieldset[data-part=day] > legend")
    pg.fill('#maker [data-field="seed"]', "11")
    pg.fill("#m-name", "dispatches-11")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    old = (SCENARIOS / "dispatches-falmouth.yaml").read_text(encoding="utf-8")
    new = (port.place / "dispatches-11.yaml").read_text(encoding="utf-8")
    assert new == old.replace("\nseed: 7\n", "\nseed: 11\n")
    # the game's page reads the game started
    pg.goto(live.url + "/")
    pg.wait_for_function(
        "document.getElementById('status').textContent === 'connected'", timeout=30_000
    )
    assert "schooner" in pg.inner_text("#ship-name")
    assert errors == []


def test_in_the_browser_the_list_is_by_shelf_and_the_tests_scenarios_come_with_the_tick(
    browser_page,
):
    """Package 96b, step 1: the page's scenarios by shelf, the lessons first; no gate's day
    in the list until the tick box asks for the scenarios kept for tests and gates; the
    sentence of the scenario chosen said under the list; no boat among the ships."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=game]")
    shelves = pg.eval_on_selector_all("#s-scenario optgroup", "els => els.map(e => e.label)")
    assert shelves[:2] == ["Begin here", "Lessons"] and "Kept for tests and gates" not in shelves
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert listed[:2] == [
        "data/scenarios/first-passage.yaml",
        "data/scenarios/lesson-landfall.yaml",
    ]
    assert "data/scenarios/gate-4c-day.yaml" not in listed
    assert "data/scenarios/squadron.yaml" not in listed
    assert "chapter 7" in pg.inner_text("#s-says")
    pg.select_option("#s-scenario", "data/scenarios/first-action.yaml")
    assert "privateer" in pg.inner_text("#s-says") and "first-action.yaml" in pg.inner_text(
        "#s-says"
    )
    pg.check("#s-tests")
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" in listed
    assert pg.input_value("#s-scenario") == "data/scenarios/first-action.yaml"  # the choice kept
    made = pg.eval_on_selector_all("#m-pick option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" in made
    pg.uncheck("#s-tests")
    listed = pg.eval_on_selector_all("#s-scenario option", "els => els.map(e => e.value)")
    assert "data/scenarios/gate-4c-day.yaml" not in listed
    ships = pg.eval_on_selector_all("#s-ship option", "els => els.map(e => e.value)")
    assert "data/ships/cutter.yaml" in ships and not [s for s in ships if "boat-" in s]
    assert errors == []


def test_in_the_browser_the_page_opens_on_begin_and_the_first_game_is_one_button(browser_page):
    """Package 96b, step 2: a fresh page opens on the first panel, with no form on it: the
    first game named, the four lessons numbered in the primer's order, no saved game where
    there is none, and the way to all the games. The first game's button starts it and
    goes to the game's page, the clock held; back at the harbour the panel leads with the
    game in play."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.is_visible("section[data-page=begin]") and not pg.is_visible("#start-form")
    assert (
        pg.locator("section[data-page=begin] input, section[data-page=begin] select").count() == 0
    )
    assert pg.inner_text("#btn-b-first") == "begin: A first passage"
    assert "chapter 7" in pg.inner_text("#b-first-says")
    lessons = pg.eval_on_selector_all("#b-lessons button", "els => els.map(e => e.textContent)")
    assert lessons == [
        "A landfall on one headland",
        "The officer's own reckoning, off the Lizard",
        "Pilot water, Black Head to Falmouth road",
        "A night off a lee shore, the Nare Head to the Deadman",
    ]
    assert not pg.is_visible("#b-save") and not pg.is_visible("#b-playing")
    pg.click("#btn-b-all")
    assert pg.is_visible("#start-form")
    pg.click("nav.tabs button[data-tab=begin]")
    pg.click("#btn-b-first")
    pg.wait_for_url(live.url + "/", timeout=60_000)  # the game's page, before it is asked
    pg.wait_for_function(
        "document.getElementById('ship-name') && "
        "document.getElementById('status').textContent === 'connected'",
        timeout=60_000,
    )
    assert not pg.url.endswith("/harbour")
    with port.driver.lock:
        assert port.driver.world.scenario.name == "A first passage"
        assert not port.driver.running and port.driver.world.clock.tick == 0
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=begin]")
    pg.wait_for_selector("#b-playing:not([hidden])", timeout=10_000)
    assert "A first passage" in pg.inner_text("#b-playing-says")
    assert "held" in pg.inner_text("#b-playing-says")
    # a lesson that is the officer's own seats the player at the officer's station
    pg.click("#b-lessons button[data-path='data/scenarios/lesson-reckoning.yaml']")
    pg.wait_for_url(live.url + "/", timeout=60_000)
    pg.wait_for_function(
        "document.getElementById('status').textContent === 'connected'", timeout=60_000
    )
    with port.driver.lock:
        seat = port.driver.world.player_seat
        assert seat is not None and "officer" in seat.station.name
    assert errors == []


def test_in_the_browser_a_game_says_what_it_is_and_a_save_is_taken_up_from_the_list(
    browser_page,
):
    """Package 96b, step 3: the new game's panel as three choices and "more": the scenario
    chosen says its own lines before the start; the ships to be aboard are offered where
    the scenario has one; the rest is behind a step; a bare ship takes a wind and a
    heading; and a saved game is picked from the list of the saves place."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=game]")
    pg.wait_for_function(
        "document.getElementById('s-lines').textContent.indexOf('A first passage') >= 0"
    )
    assert not pg.is_visible("#s-aboard") and not pg.is_visible("#s-seed")
    assert not pg.is_visible("#s-wind") and not pg.is_visible("#s-load-pick")
    pg.check("#s-tests")
    pg.select_option("#s-scenario", "data/scenarios/tender.yaml")
    pg.wait_for_selector("#s-aboard", state="visible", timeout=10_000)
    assert "Brixham" in pg.inner_text("#s-lines") or "50°" in pg.inner_text("#s-lines")
    pg.select_option("#s-aboard", "Raven")
    pg.click("#btn-start")
    pg.wait_for_selector("#btn-to-game:not([hidden])", timeout=60_000)
    assert "Following the Raven." in pg.inner_text("#start-words")
    # a save written by the game in play is in the list, and is taken up from it
    assert port.driver.save("step-three").kind == "driver.saved"
    pg.select_option("#s-from", "load")
    pg.wait_for_function(
        "Array.prototype.some.call(document.getElementById('s-load-pick').options, "
        "function (o) { return o.value === 'step-three'; })",
        timeout=10_000,
    )
    assert str(port.tmp / "saves") in pg.inner_text("#s-load-says")
    pg.select_option("#s-load-pick", "step-three")
    assert pg.input_value("#s-load") == "step-three"
    pg.click("#btn-start")
    pg.wait_for_function(
        "document.getElementById('start-words').textContent.indexOf('step-three') >= 0",
        timeout=60_000,
    )
    assert "refusal" not in (pg.get_attribute("#start-words", "class") or "")
    # a bare ship: her wind and her heading beside her
    pg.select_option("#s-from", "ship")
    assert pg.is_visible("#s-wind") and not pg.is_visible("#s-lines")
    pg.select_option("#s-ship", "data/ships/frigate-36.yaml")
    pg.fill("#s-wind", "0,15")
    pg.fill("#s-heading", "293")
    pg.click("#btn-start")
    pg.wait_for_function(
        "document.getElementById('g-title').textContent === 'Open water'", timeout=60_000
    )
    with port.driver.lock:
        opening = next(e.text for e in port.driver.world.log if e.kind == "world.start")
    assert "Wind N, 15 knots" in opening and "(293°)" in opening
    assert errors == []


def test_in_the_browser_the_sheet_is_folded_and_each_part_says_what_is_set(browser_page):
    """Package 96b, step 4 (docs/design/Design-Harbour.md §2.3): "change this scenario" on
    the game tab reads it into the sheet; every part is closed to a line written from the
    fields, so that the whole scenario reads with nothing opened (the squadron and the
    weather's system that the form has no field for among them); a part's name opens it,
    and a field changed changes its line; saved with nothing changed it is the same file;
    a written brief touched in the form keeps the examples the form does not show; and the
    game in play is a line at the head of every tab."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    assert pg.inner_text("#in-play-line") == "no game yet" and not pg.is_visible("#g-title")
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/blockade.yaml")
    pg.click("#btn-s-change")
    pg.wait_for_function("document.getElementById('m-source').textContent.indexOf('blockade') >= 0")
    assert pg.is_visible("#maker") and pg.is_visible("#in-play-line")
    parts = pg.eval_on_selector_all(
        "#maker fieldset[data-part]", "els => els.map(e => e.getAttribute('data-part'))"
    )
    assert parts == [
        "day",
        "ship",
        "start",
        "papers",
        "weather",
        "ships",
        "sea",
        "orders",
        "stations",
    ]
    assert pg.locator("#maker fieldset[data-part]:not(.folded)").count() == 0
    assert not pg.is_visible('#maker [data-field="seed"]') and not pg.is_visible("#m-ships")

    def line(part: str) -> str:
        return pg.inner_text(f'#maker [data-line="{part}"]')

    assert (
        line("day") == '"The blockade of Brest blown off"; 12 June 1805, 10:00; seed 7; of Britain.'
    )
    assert line("ship").startswith("The frigate-36; her file's own fit of guns; a glass aboard")
    assert "on the chart of channel-west; heading 20°" in line("start")
    assert "one weather system written out (the low)" in line("weather").lower()
    assert line("ships") == (
        "Three ships: Naiad of Britain, a frigate; Nimble of Britain, a brig-sloop; "
        "Hortense of France, a frigate; the inshore squadron, a squadron in line ahead "
        "(naiad, nimble)."
    )
    assert line("sea").startswith("Four ports: brest, falmouth, plymouth, torbay")
    assert "first order: set plain sail" in line("orders") and "Ushant" in line("orders")
    assert line("stations") == "You are the captain; nobody else is said; no director."
    # a part opened by its name; a field changed changes its line
    pg.click("#maker fieldset[data-part=day] > legend")
    assert pg.is_visible('#maker [data-field="seed"]')
    pg.fill('#maker [data-field="seed"]', "11")
    assert "seed 11" in line("day")
    pg.click("#btn-m-open")
    assert pg.is_visible("#m-ships") and pg.is_visible("#m-chart")
    pg.click("#btn-m-close")
    assert pg.locator("#maker fieldset[data-part]:not(.folded)").count() == 0
    # read again and saved with nothing changed: the same file, the squadron and all
    pg.click("#btn-m-read")
    pg.wait_for_function("window.freesailHarbour.foldLines && true")
    pg.wait_for_function(
        "document.querySelector('#maker [data-line=day]').textContent.indexOf('seed 7') >= 0"
    )
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    assert (port.place / "blockade.yaml").read_bytes() == (SCENARIOS / "blockade.yaml").read_bytes()
    # a brief written out, with examples the form has no field for: the tone changed in the
    # form, and the examples are written again with it
    own = port.place / "briefed.yaml"
    own.write_text(
        (SCENARIOS / "first-passage.yaml").read_text(encoding="utf-8")
        + "director:\n  brief:\n    name: Mine\n    tone: quiet\n"
        + "    limits: {nobody_dies: true, a_limit_of_mine: 3}\n"
        + "    examples:\n      - 'ship \"Nancy\": order heave to'\n",
        encoding="utf-8",
    )
    fields = pg.evaluate(
        """async (path) => {
            const h = window.freesailHarbour;
            await h.readScenario(path);
            const tone = document.querySelector('#m-brief-written [data-brief=tone]');
            tone.value = 'a quiet passage indeed';
            tone.dispatchEvent(new Event('input', { bubbles: true }));
            return h.collect();
        }""",
        str(own),
    )
    brief = fields["director"]["brief"]
    assert brief["tone"] == "a quiet passage indeed" and brief["name"] == "Mine"
    assert brief["examples"] == ['ship "Nancy": order heave to']
    assert brief["limits"] == {"nobody_dies": True, "a_limit_of_mine": 3}
    assert "Mine" in line("stations")
    assert errors == []


def test_in_the_browser_every_ship_is_set_up_on_her_card_and_the_scenario_made_is_played(
    browser_page,
):
    """Package 96b, step 5 (docs/design/Design-Harbour.md §2.4; its step's own trial): a
    scenario made from the form with the player's cutter named and under long guns, a
    revenue cutter under her kind's own guns and a French privateer lugger under British
    colours, each on a card whose blanks are her kind's own words; proved, saved, and
    started: the file says what was chosen and the game has the three ships. What the
    game does not take is said on the card, greyed. A scenario read with what the card
    has no plain field for (a place written as latitude and longitude) is saved the same."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=maker]")
    pg.click("#btn-m-new")
    pg.click("#btn-m-open")
    pg.select_option("#m-port", "falmouth")
    fits = pg.eval_on_selector_all("#m-ship-fit option", "els => els.map(e => e.value)")
    assert fits == ["", "carronades", "long guns", "unarmed"]
    pg.select_option("#m-ship-fit", "long guns")
    pg.fill('#maker [data-field="ship.name"]', "Swift")
    pg.select_option('#maker [data-field="papers.service"]', "kings")
    assert pg.locator("#maker fieldset[data-part=ship] p.not-yet").count() == 3
    for kind, name, nation, colours, bearing in (
        ("revenue cutter", "Vigilant", "britain", "", "160"),
        ("privateer lugger", "Furet", "france", "britain", "200"),
    ):
        pg.click("#btn-m-ship-add")
        card = pg.locator("#m-ships .ship-card").last
        card.locator("[data-col=description]").select_option(kind)
        card.locator("[data-col=name]").fill(name)
        card.locator("[data-col=nation]").select_option(nation)
        card.locator("[data-col=goal]").fill("bound for Plymouth")
        assert not card.locator("[data-col=role]").is_visible()
        card.locator("summary").click()
        if colours:
            card.locator("[data-col=colours]").select_option(colours)
        card.locator(".card-bearing").fill(bearing)
        card.locator(".card-miles").fill("6")
        card.locator(".card-put").click()
        assert card.locator("[data-col=position]").input_value().startswith("50 4.1 N")
        assert card.locator("p.not-yet").count() == 3
    first = pg.locator("#m-ships .ship-card").first
    assert "long guns" in first.locator(".card-says").inner_text()
    assert first.locator("[data-col=role] option").all_text_contents()[1:] == ["revenue"]
    assert first.locator("[data-col=fit] option").first.inner_text() == "her kind's own (long guns)"
    pg.click("#btn-m-close")
    assert pg.inner_text('#maker [data-line="ships"]') == (
        "Two ships: Vigilant of Britain, a revenue cutter; "
        "Furet of France, a privateer lugger under the colours of Britain."
    )
    assert "Swift; her fit long guns; a King's ship" in pg.inner_text('#maker [data-line="ship"]')
    pg.fill("#m-name", "two-cutters")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    import yaml

    made = yaml.safe_load((port.place / "two-cutters.yaml").read_text(encoding="utf-8"))
    assert made["ship"]["name"] == "Swift" and made["ship"]["fit"] == "long guns"
    assert made["papers"] == {"service": "kings"}
    assert [(s["description"], s["name"], s.get("colours")) for s in made["ships"]] == [
        ("revenue cutter", "Vigilant", None),
        ("privateer lugger", "Furet", "britain"),
    ]
    r = pg.evaluate(
        """async (path) => {
            const r = await fetch('/api/harbour/start', {method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({scenario: path})});
            return r.status;
        }""",
        str(port.place / "two-cutters.yaml"),
    )
    assert r == 200
    with port.driver.lock:
        world = port.driver.world
        assert world.ship.name == "Swift"
        assert {"Furet", "Vigilant"} <= {v.name for v in world.vessels.vessels}
    # the tender: the Raven's place is written as latitude and longitude, which the card
    # shows and does not change; her goal changed, the rest of her entry is as it was
    fields = pg.evaluate(
        """async () => {
            const h = window.freesailHarbour;
            await h.readScenario('data/scenarios/tender.yaml');
            const card = document.querySelector('#m-ships .ship-card');
            const where = card.querySelector('[data-col=position]');
            const goal = card.querySelector('[data-col=goal]');
            goal.value = goal.value + ' ';
            goal.dispatchEvent(new Event('input', { bubbles: true }));
            return {disabled: where.disabled, ships: h.collect().ships, was: h.loaded.fields.ships};
        }"""
    )
    assert fields["ships"] == fields["was"]
    assert fields["disabled"] == isinstance(fields["was"][0]["position"], dict)
    assert errors == []


def test_in_the_browser_a_convoy_is_built_from_an_empty_sheet_and_one_read_is_kept(
    browser_page,
):
    """Package 96b, step 6 (docs/design/Design-Harbour.md §2.3; its step's own trial): a
    convoy built from an empty sheet: a King's brig-sloop the player's, three merchant
    brigs on their cards, and a convoy's card with its kind, its formation, the player its
    commander and the three ticked as its members; proved, saved and started, the game has
    the set. A squadron read from a scenario and touched without a change is written as it
    was; a member unticked leaves it."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=maker]")
    pg.click("#btn-m-new")
    pg.click("#btn-m-open")
    pg.select_option('#maker [data-field="ship.file"]', "data/ships/brig.yaml")
    pg.fill("#m-lat", "49.85")
    pg.fill("#m-lon", "-5.2")
    pg.select_option('#maker [data-field="region"]', "channel-west")
    pg.fill('#maker [data-field="orders"]', "")
    for n, name in enumerate(("Nancy", "Hope", "Mary Ann")):
        pg.click("#btn-m-ship-add")
        card = pg.locator("#m-ships .ship-card").last
        card.locator("[data-col=description]").select_option("merchant brig")
        card.locator("[data-col=name]").fill(name)
        card.locator("[data-col=nation]").select_option("britain")
        card.locator("[data-col=goal]").fill("in company with the ship within 3 cables")
        card.locator("summary").click()
        card.locator("[data-col=id]").fill(name.lower().replace(" ", "-"))
        card.locator(".card-bearing").fill(str(120 + 60 * n))
        card.locator(".card-miles").fill("0.4")
        card.locator(".card-put").click()
        card.locator("[data-col=id]").dispatch_event("change")
    pg.click("#btn-m-squadron-add")
    sq = pg.locator("#m-squadrons .squadron-card").last
    offered = sq.locator(".card-members input").evaluate_all("els => els.map(e => e.value)")
    assert offered == ["the ship", "nancy", "hope", "mary-ann"]
    assert sq.locator("[data-col=formation] option").all_text_contents()[1:] == [
        "line ahead",
        "line abreast",
        "order of sailing",
        "close order",
    ]
    sq.locator("[data-col=name]").fill("the Falmouth trade")
    sq.locator("[data-col=kind]").select_option("convoy")
    sq.locator("[data-col=formation]").select_option("order of sailing")
    sq.locator("[data-col=commander]").select_option("the ship")
    for member in ("nancy", "hope", "mary-ann"):
        sq.locator(f".card-members input[value='{member}']").check()
    pg.click("#btn-m-close")
    assert pg.inner_text('#maker [data-line="ships"]').endswith(
        "the Falmouth trade, a convoy in order of sailing (nancy, hope, mary-ann)."
    )
    pg.fill("#m-name", "a-convoy")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    import yaml

    made = yaml.safe_load((port.place / "a-convoy.yaml").read_text(encoding="utf-8"))
    assert made["squadrons"] == [
        {
            "name": "the Falmouth trade",
            "kind": "convoy",
            "formation": "order of sailing",
            "commander": "the ship",
            "members": ["nancy", "hope", "mary-ann"],
        }
    ]
    assert all("squadron" not in s for s in made["ships"])  # said once, in the squadron's entry
    status = pg.evaluate(
        """async (path) => (await fetch('/api/harbour/start', {method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scenario: path})})).status""",
        str(port.place / "a-convoy.yaml"),
    )
    assert status == 200
    with port.driver.lock:
        sets = list(port.driver.world.squadrons.sets)
        assert (
            len(sets) == 1 and sets[0].kind == "convoy" and sets[0].formation == "order of sailing"
        )
        assert len(sets[0].members) == 4  # the commander, the player's, put first
    # the blockade's squadron read, touched without a change, and with a member unticked
    out = pg.evaluate(
        """async () => {
            const h = window.freesailHarbour;
            await h.readScenario('data/scenarios/blockade.yaml');
            const card = document.querySelector('#m-squadrons .squadron-card');
            const name = card.querySelector('[data-col=name]');
            name.dispatchEvent(new Event('input', { bubbles: true }));
            const same = h.collect().squadrons;
            const box = card.querySelector(".card-members input[value='nimble']");
            box.checked = false;
            box.dispatchEvent(new Event('change', { bubbles: true }));
            return {same: same, was: h.loaded.fields.squadrons, less: h.collect().squadrons};
        }"""
    )
    assert out["same"] == out["was"]
    assert out["less"][0]["members"] == ["naiad"] and out["less"][0]["book"] == "blockade"
    # the blockade's file says the membership on each ship too (`squadron: inshore`): the
    # Nimble unticked, her own word is cleared with the tick; the Naiad's stands
    words = pg.evaluate(
        """() => Object.fromEntries(window.freesailHarbour.collect().ships
            .map(s => [s.id, s.squadron || '']))"""
    )
    assert words["nimble"] == "" and words["naiad"] == "inshore"
    assert errors == []


def test_in_the_browser_a_chronometer_and_a_supercargo_are_added_and_are_in_the_game(
    browser_page,
):
    """Package 96b, step 7 (docs/design/Design-Harbour.md §2.3; the owner's point of
    2026-10-18, "he could not add a chronometer"; its step's own trial): the merchant
    passage read into the sheet; a chronometer added with its maker and rate, the master
    named and his skill changed, a supercargo named Mr Pentreath added beside the muster,
    a thing, goods in the hold, a price list more and the private signals withheld; saved
    and started, the game has each. A scenario read and saved with the part untouched is
    the same file."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=maker]")
    pg.select_option("#m-pick", "data/scenarios/merchant-passage.yaml")
    pg.click("#btn-m-read")
    pg.wait_for_function("document.getElementById('m-source').textContent.indexOf('merchant') >= 0")
    line = pg.inner_text('#maker [data-line="papers"]')
    assert "no chronometer" in line and "the master (skill 0.9)" in line
    pg.click("#maker fieldset[data-part=papers] > legend")
    assert not pg.is_visible("#m-chron-fields")
    assert pg.locator("#m-people tbody tr").count() == 1
    posts = pg.eval_on_selector_all("#m-posts option", "els => els.map(e => e.value)")
    assert "master" in posts and "mate" in posts
    pg.check("#m-chron-on")
    pg.fill("#m-chron [data-chron=maker]", "Earnshaw")
    pg.fill("#m-chron [data-chron=rate_s_per_day]", "1.8")
    pg.fill("#m-chron [data-chron=drift]", "0")
    master = pg.locator("#m-people tbody tr").first
    master.locator("[data-col=name]").fill("Mr Tregenza")
    master.locator("[data-col=skill]").fill("0.5")
    pg.click("#btn-m-person-add")
    extra = pg.locator("#m-people tbody tr").last
    extra.locator("[data-col=role]").fill("supercargo")
    extra.locator("[data-col=name]").fill("Mr Pentreath")
    pg.fill("#m-things", "a sealed packet, in the captain's keeping")
    pg.fill("#m-goods", "tin 12")
    pg.select_option('#maker [data-field="papers.private_signals"]', "false")
    line = pg.inner_text('#maker [data-line="papers"]')
    assert "a chronometer by Earnshaw" in line and "no private signals" in line
    assert "Mr Tregenza, the master (skill 0.5), Mr Pentreath, the supercargo" in line
    assert "in the hold 12 tons of tin" in line and "one thing aboard or ashore" in line
    pg.fill("#m-name", "with-a-chronometer")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    import yaml

    made = yaml.safe_load((port.place / "with-a-chronometer.yaml").read_text(encoding="utf-8"))
    assert made["papers"]["chronometer"] == {"maker": "Earnshaw", "rate_s_per_day": 1.8, "drift": 0}
    assert made["papers"]["private_signals"] is False
    assert made["people"] == [
        {"role": "master", "skill": 0.5, "name": "Mr Tregenza"},
        {"role": "supercargo", "name": "Mr Pentreath"},
    ]
    assert made["cargo"]["goods"] == {"tin": 12}
    assert made["things"] == ["a sealed packet, in the captain's keeping"]
    said = pg.inner_text("#m-words")
    assert "She carries a chronometer by Earnshaw" in said and "its rate right" in said
    status = pg.evaluate(
        """async (path) => (await fetch('/api/harbour/start', {method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scenario: path})})).status""",
        str(port.place / "with-a-chronometer.yaml"),
    )
    assert status == 200
    with port.driver.lock:
        world = port.driver.world
        assert world.scenario.chronometer["maker"] == "Earnshaw"
        names = {p.name for p in world.people.everyone}
        assert "Mr Pentreath" in names and "Mr Tregenza" in names
        assert world.people.by_role("master")[0].skill == 0.5
    # the naval cruise, whose papers have a chronometer already: the part opened and a
    # field of another part changed leaves the papers, the people and the hold as written
    out = pg.evaluate(
        """async () => {
            const h = window.freesailHarbour;
            await h.readScenario('data/scenarios/naval-cruise.yaml');
            const on = document.getElementById('m-chron-on').checked;
            const maker = document.querySelector('#m-chron [data-chron=maker]');
            maker.dispatchEvent(new Event('input', { bubbles: true }));
            const tr = document.querySelector('#m-people tbody tr');
            const name = tr && tr.querySelector('[data-col=name]');
            if (name) name.dispatchEvent(new Event('input', { bubbles: true }));
            const f = h.collect(), was = h.loaded.fields;
            const now = JSON.stringify([f.papers, f.people, f.cargo, f.things]);
            const then = JSON.stringify([was.papers, was.people, was.cargo, was.things]);
            return {on: on, maker: maker.value, same: now === then};
        }"""
    )
    assert out == {"on": True, "maker": "Arnold", "same": True}
    assert errors == []


def test_in_the_browser_the_day_the_weather_and_the_ports_are_set_whole(browser_page):
    """Package 96b, step 8 (its step's own trial): a scenario of 1808 says on the page that
    its ports are that day's and its wars June 1805's, on the game tab and in the sheet; a
    scenario made with the world keeping to the course of history, one fixed wind and its
    air, a current, the ports of her region, a weather system and a port's state written in
    the two boxes is proved and saved as the file a hand would write; and a scenario read
    and saved with the boxes untouched is the same file."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/the-faro.yaml")
    assert "She begins in 1808. The ports are as they stood on that day" in pg.inner_text("#s-says")
    pg.select_option("#s-scenario", "data/scenarios/first-action.yaml")
    assert "She begins in" not in pg.inner_text("#s-says")
    pg.select_option("#s-scenario", "data/scenarios/the-faro.yaml")
    pg.click("#btn-s-change")
    pg.wait_for_function("document.getElementById('m-source').textContent.indexOf('the-faro') >= 0")
    assert "the wars those of June 1805" in pg.inner_text('#maker [data-line="day"]')
    pg.click("#maker fieldset[data-part=day] > legend")
    assert "She begins in 1808" in pg.inner_text("#m-year-says")
    # the blockade read and saved with the boxes untouched: the same file
    pg.select_option("#m-pick", "data/scenarios/blockade.yaml")
    pg.click("#btn-m-read")
    pg.wait_for_function("document.getElementById('m-source').textContent.indexOf('blockade') >= 0")
    assert "name: the low" in pg.input_value("#m-systems")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert (port.place / "blockade.yaml").read_bytes() == (SCENARIOS / "blockade.yaml").read_bytes()
    # a scenario made with the day, the weather and the ports whole
    pg.click("#btn-m-new")
    pg.click("#btn-m-open")
    pg.select_option("#m-port", "falmouth")
    pg.fill('#maker [data-field="start"]', "1805-06-12T05:00")
    pg.check('#maker [data-field="follows_history"]')
    pg.select_option("#m-weather-mode", "")
    pg.fill('#maker [data-field="wind.from_deg"]', "270")
    pg.fill('#maker [data-field="wind.knots"]', "18")
    pg.select_option('#maker [data-field="wind.air_mass"]', "unstable")
    pg.fill('#maker [data-field="current.knots"]', "1.5")
    pg.fill('#maker [data-field="current.toward_deg"]', "90")
    pg.click("#btn-m-ports-region")
    listed = pg.input_value('#maker [data-field="ports"]')
    assert "falmouth" in listed and "plymouth" in listed and "brest" in listed
    pg.fill(
        "#m-systems",
        "- name: the high\n  kind: high\n  radius_km: 800\n  track:\n"
        "    - {at: 1805-06-12T05:00, x_km: 200, y_km: -300, hpa: 1026}\n"
        "    - {at: 1805-06-13T05:00, x_km: 300, y_km: -300, hpa: 1024}\n",
    )
    pg.fill("#m-ports-state", "falmouth: {}\nbrest:\n  closed_to: [britain]\n")
    assert "systems' words changed here" in pg.inner_text('#maker [data-line="weather"]')
    pg.fill("#m-name", "the-day-whole")
    pg.click("#btn-m-save")
    pg.wait_for_function("window.freesailHarbour.busy === true", timeout=10_000)
    pg.wait_for_function("window.freesailHarbour.busy === false", timeout=60_000)
    assert not pg.is_visible("#m-refusal"), pg.inner_text("#m-refusal")
    import yaml

    made = yaml.safe_load((port.place / "the-day-whole.yaml").read_text(encoding="utf-8"))
    assert made["follows_history"] is True
    assert made["wind"] == {"from_deg": 270, "knots": 18, "air_mass": "unstable"}
    assert made["current"] == {"knots": 1.5, "toward_deg": 90}
    assert made["weather"]["systems"][0]["name"] == "the high"
    assert made["ports"] == {"falmouth": {}, "brest": {"closed_to": ["britain"]}}
    said = pg.inner_text("#m-words")
    assert "The world keeps to the course of history" in said and "the high (high" in said
    assert "A current of 1.5 knots sets toward E" in said and "The ports: falmouth, brest." in said
    # read back: the sheet says it, the boxes hold the words
    assert "the high" in pg.input_value("#m-systems")
    assert "closed_to" in pg.input_value("#m-ports-state")
    assert "their state said of brest" in pg.inner_text('#maker [data-line="sea"]')
    assert "the world keeps to the course of history" in pg.inner_text('#maker [data-line="day"]')
    assert errors == []


def test_in_the_browser_the_stations_are_one_table_and_a_planned_door_is_offered(browser_page):
    """Package 96b, step 9 (its step's own trial, as far as a test may go without a model):
    the settings' form takes a second model for the API door, one a line; a scenario of the
    player's own gives the officer's station to a model; started, the stations tab shows
    one table of who is where: the player at the captain's prompt, the officer's station
    the scenario's plan with the API door chosen and both models offered, the director's
    above the game, the Raven's captain a row of her own; "start the doors the scenario
    asks for" starts the officer's door with the model chosen (its pane opens; the door
    itself asks its model's consent, and here finds no API to reach). The director's grant
    is set in the sheet."""
    pg, live, port, errors = browser_page
    port.place.mkdir(parents=True, exist_ok=True)
    (port.place / "planned.yaml").write_text(
        (SCENARIOS / "tender.yaml").read_text(encoding="utf-8") + "\nstations:\n  officer: model\n",
        encoding="utf-8",
    )
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    pg.click("nav.tabs button[data-tab=doors]")
    assert pg.is_visible("#t-none") and not pg.is_visible("#t-stations")
    assert "You sit at one" in pg.inner_text("section[data-page=doors]")
    # the settings: the door's own model and a second, one a line
    pg.click("nav.tabs button[data-tab=settings]")
    pg.fill('#settings [data-set="doors.api.model"]', PLACEHOLDER)
    pg.fill("#st-models", SECOND + "\nmade-up-model-9, openrouter")
    pg.fill("#st-api-flags", "--base-url http://127.0.0.1:9")
    pg.click("#btn-settings-save")
    pg.wait_for_function("document.getElementById('st-words').textContent.indexOf('Kept') >= 0")
    kept = S.load_settings(port.settings_path)["doors"]["api"]["models"]
    assert kept == [SECOND, {"name": "made-up-model-9", "dialect": "openrouter"}]
    assert pg.input_value("#st-models") == SECOND + "\nmade-up-model-9, openrouter"
    # the game from the planned scenario
    status = pg.evaluate(
        """async (path) => (await fetch('/api/harbour/start', {method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({scenario: path})})).status""",
        str(port.place / "planned.yaml"),
    )
    assert status == 200
    pg.click("nav.tabs button[data-tab=doors]")
    pg.wait_for_selector("#t-stations tbody tr", timeout=10_000)
    rows = pg.eval_on_selector_all(
        "#t-stations tbody tr",
        "els => els.map(e => "
        "Array.from(e.querySelectorAll('td')).slice(0, 4).map(t => t.textContent))",
    )
    assert rows[0] == ["Amazon (yours)", "the captain", "you, at the prompt", ""]
    assert rows[1] == ["Amazon (yours)", "the officer", "the game's own", "a model"]
    assert rows[5][:3] == ["Amazon (yours)", "the watcher", "the game's own"]
    assert rows[6][:3] == ["above the game", "the director", "the game's own"]
    assert rows[7][:3] == ["Raven", "the captain", "the game's own"] and len(rows) == 8
    officer = pg.locator("#t-stations tr[data-row='officer|']")
    assert officer.locator(".t-door").input_value() == "api"
    offered = officer.locator(".t-model option").evaluate_all("els => els.map(e => e.value)")
    assert offered == ["", PLACEHOLDER, SECOND, "made-up-model-9"]
    assert pg.locator("#t-stations tr[data-row='captain|'] .t-start").is_disabled()
    assert "gives one station to a model" in pg.inner_text("#t-says")
    # a row with no door chosen says so; the planned one is started with the model chosen
    pg.locator("#t-stations tr[data-row='captain|Raven'] .t-start").click()
    assert "Choose the door" in pg.inner_text("#t-error")
    officer.locator(".t-model").select_option(SECOND)
    pg.evaluate(
        "() => { const b = document.getElementById('btn-t-all'); b.click(); b.click(); "
        "document.querySelector(\"#t-stations tr[data-row='officer|'] .t-start\").click(); }"
    )
    pg.wait_for_selector(".door-pane", timeout=20_000)
    assert "API door at the officer" in pg.inner_text(".door-pane .door-words")
    door = next(iter(port.harbour.doors.values()))
    assert door.argv[door.argv.index("--model") + 1] == SECOND
    assert door.station == "officer" and door.ship == ""
    # pressed twice before the page next reads the state: one door a row, not two
    assert len(port.harbour.doors) == 1 and pg.is_disabled("#btn-t-all")
    assert officer.locator(".t-start").is_disabled()
    port.harbour.close()
    # the state the table is drawn from carries no model's name of the settings
    said = pg.evaluate("async () => (await fetch('/api/harbour/state')).text()")
    assert PLACEHOLDER not in said and SECOND not in said and "made-up-model-9" not in said
    # a seat in its consent conversation is asked, not held; stopped, the station is the
    # game's own again and its door is offered; the Raven's is on the Raven's row
    made = pg.evaluate(
        """async () => {
            const post = (path, body) => fetch(path, {method: 'POST',
                headers: {'Content-Type': 'application/json'}, body: JSON.stringify(body)});
            const a = await post('/api/agents/master', {model_name: 'made-up-a', door: 'api'});
            const b = await post('/api/agents/captain',
                {model_name: 'made-up-b', door: 'api', ship: 'Raven'});
            return [a.status, b.status];
        }"""
    )
    assert made == [200, 200]
    master = pg.locator("#t-stations tr[data-row='master|']")
    raven = pg.locator("#t-stations tr[data-row='captain|Raven']")
    pg.wait_for_function(
        "document.querySelector(\"#t-stations tr[data-row='master|'] .t-held\").textContent"
        ".indexOf('asked, not yet answered (made-up-a)') === 0",
        timeout=10_000,
    )
    assert raven.locator(".t-held").inner_text() == "asked, not yet answered (made-up-b)"
    assert master.locator(".t-start").is_disabled() and raven.locator(".t-start").is_disabled()
    own = pg.locator("#t-stations tr[data-row='captain|'] .t-held").inner_text()
    assert own == "you, at the prompt"
    desk = port.driver.desk
    for held in [s for s in desk.seats.values() if s.model_name.startswith("made-up-")]:
        with port.driver.lock:
            desk.release(held.station, "stopped by the test", held.key, held.ship)
    pg.wait_for_function(
        "document.querySelector(\"#t-stations tr[data-row='master|'] .t-held\").textContent"
        ' === "the game\'s own"',
        timeout=10_000,
    )
    assert raven.locator(".t-held").inner_text() == "the game's own"
    assert not master.locator(".t-start").is_disabled()
    assert not raven.locator(".t-start").is_disabled()
    # the director's grant, in the sheet
    grant = pg.evaluate(
        """async (names) => {
            const h = window.freesailHarbour;
            await h.readScenario('data/scenarios/directed-passage.yaml');
            const set = (sel, v) => { const el = document.querySelector(sel); el.value = v;
                el.dispatchEvent(new Event('input', { bubbles: true })); };
            set('#maker [data-field="director.models"]', names);
            set('#maker [data-field="director.seats"]', '2');
            return h.collect().director;
        }""",
        f"{PLACEHOLDER}, {SECOND}",
    )
    assert grant["models"] == [PLACEHOLDER, SECOND] and grant["seats"] == 2
    assert grant["brief"] == "quiet-passage"
    assert "the director may seat two models" in pg.inner_text('#maker [data-line="stations"]')
    assert errors == []


def test_in_the_browser_each_setting_says_what_it_is_and_a_doors_flags_are_named_choices(
    browser_page,
):
    """Package 96b, step 10: on every tab each control has its sentence under it; the
    settings say how the game answers its own page alone, how another device is let in,
    and where the saved games are kept; and a door's flags are choices with names (how
    often its model is asked, the pictures, the context, the consent question put again)
    with one line for the rest, kept in the settings as the one list of flags the door's
    command line takes."""
    pg, live, port, errors = browser_page
    s = S.load_settings(port.settings_path)
    s["doors"]["local"]["flags"] = ["--cadence", "watch", "--seed", "7", "--pictures", "no"]
    s["doors"]["api"]["flags"] = ["--ask-again", "--cadence", "fortnightly"]
    S.save_settings(s, port.settings_path)
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    bare = pg.evaluate(
        """() => Array.from(document.querySelectorAll(
            '#start-form input, #start-form select, #settings input, #settings select, ' +
            '#settings textarea, #maker input, #maker select, #maker textarea, #d-ship'))
          .filter(el => !el.closest('table') && !el.closest('.ship-card') &&
                        !el.closest('#m-stations') && !el.closest('#m-books'))
          .filter(el => !(el.closest('label') && el.closest('label').querySelector('.says')))
          .map(el => '#' + el.id)"""
    )
    assert set(bare) == SAID_BY_ITS_LABEL
    pg.click("nav.tabs button[data-tab=game]")
    pg.click("#s-more summary")
    assert "More is truer and slower" in pg.inner_text("#start-form")
    assert "drops to real time while a model at a station is answering" in pg.inner_text(
        "#start-form"
    )
    pg.click("nav.tabs button[data-tab=settings]")
    said = pg.inner_text("section[data-page=settings]")
    assert "This game answers its own page alone" in said and "0.0.0.0" in said
    assert f"Your saved games are kept in {port.tmp / 'saves'}" in said
    # the flags read into their named choices; what the form does not know stays in the line
    assert pg.input_value("#st-local-cadence") == "watch"
    assert pg.input_value("#st-local-pictures") == "no"
    assert pg.input_value("#st-local-flags") == "--seed 7"
    assert pg.is_checked("#st-api-ask-again") and pg.input_value("#st-api-cadence") == ""
    assert pg.input_value("#st-api-flags") == "--cadence fortnightly"
    pg.select_option("#st-local-cadence", "events")
    pg.fill("#st-local-ctx", "32768")
    pg.uncheck("#st-api-ask-again")
    pg.fill("#st-api-flags", "")
    pg.select_option("#st-api-cadence", "watch")
    pg.click("#btn-settings-save")
    pg.wait_for_function("document.getElementById('st-words').textContent.indexOf('Kept') >= 0")
    kept = S.load_settings(port.settings_path)["doors"]
    assert kept["local"]["flags"] == [
        "--cadence",
        "events",
        "--pictures",
        "no",
        "--ctx",
        "32768",
        "--seed",
        "7",
    ]
    assert kept["api"]["flags"] == ["--cadence", "watch"]
    assert port.harbour.door_argv("local", "officer")[-8:] == kept["local"]["flags"]
    assert errors == []


def test_in_the_browser_the_final_lists_small_things_are_so(browser_page):
    """Package 96b, the final list, items 3 to 5: a lesson started from the game tab with
    "where you stand" left to the game is seated as its shelf entry says, and the choice
    says so; a chronometer ticked with no maker writes none, and the sheet says "a
    chronometer"; and every sentence of the words' file is ON THE PAGE under its control,
    the one whose control has no label of its own among them."""
    pg, live, port, errors = browser_page
    pg.goto(live.url + "/harbour")
    pg.wait_for_function("window.freesailHarbour && window.freesailHarbour.ready", timeout=60_000)
    words = page_words()
    shown = pg.evaluate(
        """() => Object.fromEntries(Array.from(document.querySelectorAll('.says[data-says]'))
            .map(s => [s.getAttribute('data-says'), s.textContent]))"""
    )
    assert shown == words
    assert pg.evaluate(
        """() => { const s = document.querySelector('.says[data-says="#m-pick"]');
            return s.previousElementSibling.contains(document.getElementById('m-pick')); }"""
    )
    pg.click("nav.tabs button[data-tab=game]")
    pg.select_option("#s-scenario", "data/scenarios/lesson-reckoning.yaml")
    assert pg.inner_text("#s-seat option >> nth=0") == "as this game says: the officer"
    pg.select_option("#s-scenario", "data/scenarios/lesson-landfall.yaml")
    assert pg.inner_text("#s-seat option >> nth=0") == "as the scenario says (else the captain)"
    pg.select_option("#s-scenario", "data/scenarios/lesson-reckoning.yaml")
    pg.click("#btn-start")
    pg.wait_for_selector("#btn-to-game:not([hidden])", timeout=60_000)
    with port.driver.lock:
        seat = port.driver.world.player_seat
        assert seat is not None and "officer" in seat.station.name
    pg.select_option("#s-seat", "captain")  # his own choice wins over the shelf's
    pg.click("#btn-start")
    pg.wait_for_function(
        "document.getElementById('in-play-line').textContent.indexOf(\"captain's prompt\") >= 0",
        timeout=60_000,
    )
    # a chronometer with no maker said
    pg.click("nav.tabs button[data-tab=maker]")
    pg.click("#btn-m-new")
    pg.click("#maker fieldset[data-part=papers] > legend")
    pg.check("#m-chron-on")
    line = pg.inner_text('#maker [data-line="papers"]')
    assert "a chronometer;" in line and "by the chronometer" not in line
    made = pg.evaluate("() => window.freesailHarbour.collect().papers")
    assert made == {"chronometer": {}}
    pg.fill("#m-chron [data-chron=maker]", "Arnold")
    assert "a chronometer by Arnold" in pg.inner_text('#maker [data-line="papers"]')
    assert errors == []


# ---------------------------------------------------------------------------
# Package 67: the director's seats' doors
# ---------------------------------------------------------------------------


def test_the_settings_say_the_models_they_can_call_and_the_seated_doors_fold():
    s = S.check_settings(
        {
            "doors": {
                "api": {
                    "model": PLACEHOLDER,
                    "models": [
                        "placeholder-two",
                        {"name": "placeholder-three", "dialect": "openrouter"},
                    ],
                    "seat_budget_tokens": "2/5",
                }
            }
        }
    )
    assert S.callable_models(s) == {
        PLACEHOLDER: "anthropic",
        "placeholder-two": "anthropic",
        "placeholder-three": "openrouter",
    }
    assert S.seat_budget_tokens("2/5", 200_000) == 80_000
    assert S.seat_budget_tokens("40%", 200_000) == 80_000
    assert S.seat_budget_tokens("0.4", 200_000) == 80_000
    assert S.seat_budget_tokens("60000", 200_000) == 60_000
    assert S.seat_budget_tokens("", 200_000) is None
    with pytest.raises(ValueError):
        S.seat_budget_tokens("most of it", 200_000)
    with pytest.raises(S.SettingsError):
        S.check_settings({"doors": {"api": {"models": [{"name": "x", "dialect": "a fax"}]}}})
    with pytest.raises(S.SettingsError):
        S.check_settings({"doors": {"api": {"seat_budget_tokens": "lots"}}})


def test_the_harbour_starts_a_seats_door_as_the_directors_and_stops_it_when_the_seat_goes(
    tmp_path, monkeypatch
):
    """Package 67, item 2 (without a subprocess: the door's start recorded): a seat held on
    the World in play has the API door started for it, its model the seat's, its dialect
    the settings', `--budget-tokens` the settings' figure, marked the director's and told
    to the director; a seat for a model the settings cannot call is refused at the
    director's door and at the owner's `world:`, the settings' model named to the director
    alone; a seat gone has its door stopped."""
    from freesail.agents import consent
    from freesail.agents import director as D
    from freesail.world.orders import director_seats

    port = Port(
        tmp_path,
        {
            "doors": {
                "api": {
                    "model": PLACEHOLDER,
                    "models": [{"name": "placeholder-two", "dialect": "openrouter"}],
                    "seat_budget_tokens": "0.25",
                }
            }
        },
    )
    started: list[dict[str, Any]] = []
    stopped: list[str] = []

    class FakeDoor:
        def __init__(self, ident: str, argv: list[str]):
            self.id, self.argv, self.running = ident, argv, True
            self.station, self.ship = "officer of the watch", ""

        def stop(self) -> None:
            stopped.append(self.id)
            self.running = False

    def start_door(kind, station, ship="", *, seat="", seat_model="", by=""):
        argv = port.harbour.door_argv(kind, station, ship, seat_model=seat_model)
        ident = f"d{len(started) + 1}"
        started.append({"station": station, "ship": ship, "seat": seat, "by": by, "argv": argv})
        port.harbour.doors[ident] = FakeDoor(ident, argv)
        return {"id": ident}

    monkeypatch.setattr(port.harbour, "start_door", start_door)
    monkeypatch.setattr(port.harbour, "_stop_seat_door", lambda door: door.stop())
    with PageClient(port.app) as c:
        c.post("/api/harbour/start", json={"scenario": "data/scenarios/lesson-falmouth.yaml"})
        w = port.driver.world
        for name in (PLACEHOLDER, "placeholder-two", "placeholder-four"):
            consent.Record(
                name, "a test runtime", "2026-10-23", consent.YES, answer="Yes.", drill="passed"
            ).write(port.records)
        w.consent_records_dir = port.records
        w.scenario.director = {
            "models": [PLACEHOLDER, "placeholder-two", "placeholder-four"],
            "seats": 3,
            "seats_in_voyage": 5,
        }
        D.set_brief(w, "quiet-passage", source="the test")
        refused = D.direct(w, "seat: placeholder-four as officer for 4 samples", by="the test")
        assert refused == (
            "Refused: the settings call no model by that name; the API door's model is "
            f"{PLACEHOLDER}."
        )
        r = c.post(
            "/api/order", json={"text": "world: seat: placeholder-four as master for 4 samples"}
        )
        assert "The seat was not held: the settings call no model by that name" in r.text
        assert director_seats(w) == {}
        said = D.direct(w, "seat: placeholder-two as officer for 4 samples", by="the test")
        assert said.startswith("Done:"), said
        port.harbour.tend_seats()
        port.harbour.tend_seats()  # once a seat, however often it is tended
        assert len(started) == 1
        door = started[0]
        assert door["by"] == "the director" and door["seat"] == "own/officer of the watch"
        argv = door["argv"]
        assert argv[argv.index("--model") + 1] == "placeholder-two"
        assert argv[argv.index("--dialect") + 1] == "openrouter"
        assert argv[argv.index("--station") + 1] == "officer of the watch"
        assert argv[argv.index("--budget-tokens") + 1] == "0.25"
        assert "--ship" not in argv
        assert D.direct(w, "unseat: officer, the passage is quiet", by="the test").startswith(
            "Done"
        )
        port.harbour.tend_seats()
        assert stopped == ["d1"]
        # a door of the owner's own, from the page, carries no seat's flags and no mark
        assert "--budget-tokens" not in port.harbour.door_argv("api", "watcher")


def test_the_doors_of_the_directors_seats_are_marked_in_the_pane(tmp_path):
    from freesail.ui.harbour import Door

    door = Door(
        "d9",
        "api",
        "officer of the watch",
        [sys.executable, "-c", "print('a door')"],
        by="the director",
        seat="own/officer of the watch",
    )
    door.proc.wait(timeout=30)
    door._reader.join(timeout=30)
    state = door.state()
    assert state["by"] == "the director"
    assert state["words"].startswith("The director's seat's API door at the officer of the watch")
    assert Door("d10", "api", "watcher", [sys.executable, "-c", "pass"]).state()["by"] == ""
