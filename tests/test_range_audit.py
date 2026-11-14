"""Package 103a: the range's audit (`tools/audit_range.py`) and its ratchet.

Decision 69: a game begun on any day from 1792 to 1825 finds a world depicted accurately
and working. The audit measures how far the tree is from that: it seeds sampled days
through the game's own readers, makes a whole world on a few, and reports what it finds;
the known list (`tools/range/audit-known.yaml`) holds every finding, owned.

**Two tiers.** The fast tier holds what is cheap by any YAML loader: the known list's and
the reference's form, the key a path makes on any machine, the audit's files outside the
build's fingerprint, the classing's table, and every check planted on small made data.
The slow tier (the fixtures `tree` and `sampled` in `tests/conftest.py`'s `DAY_FIXTURES`,
and the tests marked here) holds the ratchet: the sampled sweep with its four whole worlds
is the known list's, the full sweep is the known list's exactly with its years and its
ceilings, the mechanical findings stand without the reference, the sweep is the same
twice, and the quick loader reads every data file as the game's own does.

**Planted, check by check.** Every finding the tool can make is made here on purpose from
planted data, by its key: the ports' (p-undated, p-holder-unknown, p-blockade-words,
p-blockade-before, p-blockade-no-war), the wars' (w-before-since, w-court, w-no-end,
w-twice, w-allied, w-relations, w-block-unread), the blockades' (b-undated, b-no-port),
the vessels' (v-fit-ahead, v-scenario, v-nation-unknown), the flags' (f-colours,
f-dates-form, f-signal-nearest, f-fashion), the days' (d-none, d-gap), the lights'
(l-by-year), the words' (x-as-of, x-words), the code's years (e-year), the classing's
(c-unclassed, c-unparsed, c-dead-row, c-snap-back, c-unread), the reference's (r-holder,
r-port-blockade, r-nation, r-war-at-peace, r-war-absent, r-blockade, r-vessel) and the
two roads' (a-wars, a-holder, a-state, a-blockade). The ten of check (u) count what a
tree holds and are counted here on a small one; they are not planted otherwise.
Truths 7-590 to 7-593 are in test_known_truths.py.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from datetime import UTC, date, datetime, timedelta, timezone
from pathlib import Path, PurePosixPath, PureWindowsPath
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location("audit_range", ROOT / "tools" / "audit_range.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("audit_range", mod)
    spec.loader.exec_module(mod)
    return mod


A = _tool()

# A small tree: the ports the plantings want and two ship files, no scenarios.
SMALL_PORTS = (
    "brest",
    "cadiz",
    "civita-vecchia",
    "ferrol",
    "genoa",
    "leghorn",
    "lorient",
    "plymouth",
    "rochefort",
    "valletta",
)
SMALL_SHIPS = ("brig.yaml", "smack.yaml")
# A day in every year, with the days either side of three dates of the small ports'.
SOME_DAYS = sorted(
    {
        *A.yearly_days(),
        date(1800, 9, 4),
        date(1800, 9, 5),
        date(1803, 5, 31),
        date(1803, 6, 1),
        date(1805, 6, 3),
        date(1805, 6, 4),
    }
)
# every check of the cheap road but the code's own years, which take two seconds a run
QUICK = "".join(c for c in A.LETTERS if c not in "ea")


@pytest.fixture(scope="module")
def small():
    """A few ports and two ships read by the game's own readers: a second by any loader."""
    return A.load_tree(ports=SMALL_PORTS, ships=SMALL_SHIPS, scenarios=False)


@pytest.fixture(scope="module")
def tree():
    """The whole tree (slow: `tests/conftest.py`, `DAY_FIXTURES`)."""
    return A.load_tree()


@pytest.fixture(scope="module")
def sampled(tree):
    """The sampled sweep, whole worlds and all: once a run (slow)."""
    return A.run(tree=tree)


CEILING_WORDS = (
    "counts above their ceiling (a port or a ship added with a value where the range wants "
    "dated rows raises the count: date it, or raise the ceiling in "
    "tools/range/audit-known.yaml with its reason):\n"
)


def _planted(tree, **changes):
    """The tree with some of its parts replaced, the rest shared."""
    return A.Tree(**{**{f: getattr(tree, f) for f in tree.__dataclass_fields__}, **changes})


def _years(words: str) -> set[int]:
    out: set[int] = set()
    for part in str(words).split(","):
        lo, sep, hi = part.strip().partition("-")
        if lo.isdigit():
            out.update(range(int(lo), int(hi if sep else lo) + 1))
    return out


def _years_of(finding) -> set[int]:
    return {d.year for d in finding.days}


# ---------------------------------------------------------------------------
# The known list, the reference, the keys and the build (fast)
# ---------------------------------------------------------------------------


def test_the_known_list_holds_each_finding_owned():
    """Every entry its key, what it is, the years it bites, its basis, whose it is and a
    reason in a line; no key twice; every key of one of the checks; a finding that rests
    on the reference is a judgement to be read against a source, and no other is said to
    rest on it. What no data can mend is the engine's: the wars' want of an end, the
    nations' want of a lifetime, the colours worn whatever the year."""
    doc = yaml.safe_load(A.KNOWN_PATH.read_text(encoding="utf-8"))
    entries = doc["known"]
    assert entries
    keys = [e["key"] for e in entries]
    assert len(keys) == len(set(keys))
    for e in entries:
        assert set(e) >= {"key", "what", "years", "basis", "owner", "reason"}, e
        assert e["key"][0] in A.LETTERS and e["key"][1] == "-", e["key"]
        assert e["basis"] in (A.MECHANICAL, A.REFERENCE), e["key"]
        assert e["owner"] in A.OWNERS, e["key"]
        assert (e["basis"] == A.REFERENCE) == (e["key"][0] == "r"), e["key"]
        if e["basis"] == A.REFERENCE:
            assert e["owner"] == "a judgement to be read against a source", e["key"]
        for word in ("what", "years", "reason"):
            text = str(e[word])
            assert text.strip() and "\n" not in text, (e["key"], word)
        if "most" in e:
            assert isinstance(e["most"], int) and e["most"] >= 1, e["key"]
        assert e.get("sweep", "full") == "full", e["key"]
    # the rule of the owners: a finding is the data's only if a change to data alone,
    # read by today's readers, clears it, and every kind so owned has that planting
    # (`DATA_CLEARS`, below); where a reader or a key must come first it is the engine's,
    # and where the check itself must change its reason says what it must become
    by_owner = {e["key"]: e for e in entries}
    data = {k for k, e in by_owner.items() if e["owner"] == A.OWNERS[0]}
    engine = {k for k, e in by_owner.items() if e["owner"] == A.OWNERS[1]}
    assert {k.split(":")[0] for k in data} <= set(DATA_CLEARS), sorted(
        {k.split(":")[0] for k in data} - set(DATA_CLEARS)
    )
    assert len(data) == 28 and len(engine) == 38
    engines = [k for k in by_owner if k[0] in "ue" or k.startswith(("f-colours:", "c-"))]
    engines += ["w-no-end", "l-by-year", "x-as-of", "w-block-unread"]
    engines += [k for k in by_owner if k.startswith(("w-before-since:", "w-court:"))]
    engines.remove("u-prize-shares")
    for key in engines:
        assert by_owner[key]["owner"] == "an engine fault", key
    assert set(engines) | {k for k in by_owner if k.startswith("f-dates-form:")} == engine
    must_change = [k for k in engine if k[0] in "ul" or k.startswith("f-dates-form:")]
    must_change += ["w-no-end", "c-unread:nations-relations"]
    assert len(must_change) == 13
    for key in must_change:
        reason = by_owner[key]["reason"]
        assert "When " in reason and "the check " in reason, key
    head = A.KNOWN_PATH.read_text(encoding="utf-8").split("known:")[0]
    assert "a change to data alone" in head and "FOR A BUILDER" in head
    assert "fails at the merge" in head and "--known --no-worlds" in head


def test_a_path_is_the_same_key_on_any_machine():
    """A file is keyed by its path under its folder with forward slashes (`key_of`): a
    Windows path makes the key a POSIX path makes, the classing's patterns hold it, the
    scan's skips skip it, and a file's name and stem are read from either separator."""
    data_w = PureWindowsPath(r"C:\work\FreeSail\data")
    data_p = PurePosixPath("/home/user/FreeSail/data")
    for parts, path, row in (
        (("ports", "cadiz.yaml"), "nation.#.since", "port-holder"),
        (("signals", "britain", "days.yaml"), "days.#.years", "days-years"),
        (("signals", "basic", "colours.yaml"), "nations.portugal.flags.#.dates", "colours-dates"),
        (("charts", "features", "strait.yaml"), "features.#.lit.from", "lights-years"),
        (("scenarios", "trials", "one.yaml"), "papers.almanac", "scenario-papers"),
        (("charts", "overrides", "strait", "x.yaml"), "patches.#.source", "chart-provenance"),
        (("nations.yaml",), "wars.#.since", "wars-since"),
    ):
        key_w = A.key_of(data_w.joinpath(*parts), data_w)
        assert key_w == A.key_of(data_p.joinpath(*parts), data_p) == "/".join(parts)
        assert "\\" not in key_w
        assert A.row_of(key_w, path).id == row
    tile = A.key_of(data_w / "charts" / "tiles" / "2" / "a.yaml", data_w)
    assert tile.startswith(A.SCAN_SKIP)
    code_w = PureWindowsPath(r"C:\work\FreeSail\freesail")
    assert A.key_of(code_w / "api" / "viewer_flags.py", code_w.parent) == (
        "freesail/api/viewer_flags.py"
    )
    assert A.name_of(r"data\ships\brig.yaml") == A.name_of("data/ships/brig.yaml") == "brig.yaml"
    assert A.stem_of(r"data\ships\frigate-36.yaml") == "frigate-36"
    assert A._file_kind("charts/overrides/strait/x.yaml") == "charts/overrides/strait"
    assert A._file_kind("nations.yaml") == "nations.yaml"


def test_the_scans_keys_are_made_by_the_one_function(tmp_path):
    """The scan of the data, the code's years and the scenarios' names take their keys
    from `key_of`: a nested file's key has forward slashes whatever the folder is."""
    data = tmp_path / "data"
    (data / "signals" / "made").mkdir(parents=True)
    (data / "signals" / "made" / "days.yaml").write_text(
        "days:\n  - {name: a day, date: '06-04', years: '1760-1819'}\n", encoding="utf-8"
    )
    scan = A.scan_dated(data)
    assert {rel for rel, _path, _value in scan} == {"signals/made/days.yaml"}
    code = tmp_path / "freesail"
    (code / "api").mkdir(parents=True)
    (code / "api" / "x.py").write_text("year = 1805\n", encoding="utf-8")
    assert set(A.engine_years(code)) == {"freesail/api/x.py"}


def test_the_audits_own_files_are_no_part_of_the_build(tmp_path):
    """The known list and the reference lie beside the tool, not under data/: the build's
    fingerprint (`core.world.fingerprint_of`) hashes every file under data/ but the tiles,
    and an entry taken out of the list is no change of the game's rules. A file under
    tools/ moves no fingerprint; the same file under data/ does."""
    from freesail.core.world import fingerprint_of

    for path in (A.KNOWN_PATH, A.REFERENCE_PATH):
        assert path.exists()
        assert path.relative_to(ROOT).parts[:2] == ("tools", "range"), path
    assert not (ROOT / "data" / "range").exists()
    (tmp_path / "freesail").mkdir()
    (tmp_path / "freesail" / "a.py").write_text("X = 1\n", encoding="utf-8")
    (tmp_path / "data").mkdir()
    (tmp_path / "data" / "a.yaml").write_text("a: 1\n", encoding="utf-8")
    (tmp_path / "tools" / "range").mkdir(parents=True)
    listed = tmp_path / "tools" / "range" / "audit-known.yaml"
    listed.write_text("known: [one]\n", encoding="utf-8")
    before = fingerprint_of(tmp_path)
    listed.write_text("known: []\n", encoding="utf-8")
    assert fingerprint_of(tmp_path) == before
    (tmp_path / "data" / "range").mkdir()
    (tmp_path / "data" / "range" / "audit-known.yaml").write_text("known: []\n", encoding="utf-8")
    assert fingerprint_of(tmp_path) != before


def test_the_reference_is_marked_small_and_read_by_nothing_in_the_game():
    """`tools/range/reference.yaml`: every row marked FROM MEMORY or citing where the tree
    already has it, with the writer's confidence and how far the days are known; only
    nations of the table; no row ending before it begins; and nothing under freesail/
    names the file or its folder."""
    doc = yaml.safe_load(A.REFERENCE_PATH.read_text(encoding="utf-8"))
    head = A.REFERENCE_PATH.read_text(encoding="utf-8").split("range:")[0]
    assert "NOT RESEARCH" in head and "NOT THE GAME'S DATA" in head and "FROM MEMORY" in head
    table = set(A.load_nations().nations)
    rows = [*doc["wars"], *doc["lifetimes"], *doc["peaces"]]
    assert len(doc["wars"]) <= 60 and len(doc["lifetimes"]) <= 24
    for row in rows:
        assert row.get("mark") == "FROM MEMORY" or str(row.get("source") or "").strip(), row
        assert row.get("mark") in (None, "FROM MEMORY"), row
        assert row["confidence"] in ("high", "medium", "low"), row
        assert row["days"] in ("known", "month", "year"), row
        assert str(row["note"]).strip(), row
        if row.get("since") and row.get("until"):
            assert row["since"] <= row["until"], row
    for war in doc["wars"]:
        assert len(war["between"]) == 2 and set(war["between"]) <= table, war
    assert {r["nation"] for r in doc["lifetimes"]} == table
    for path in (ROOT / "freesail").rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "tools/range" not in text and "data/range" not in text, path
        assert "reference.yaml" not in text and "audit-known" not in text, path
    ref = A.load_reference()
    assert ref.at_war("britain", "france", date(1793, 7, 1))
    assert not ref.at_war("britain", "france", date(1802, 7, 1))
    assert ref.at_war("spain", "britain", date(1805, 7, 1))
    assert not ref.at_war("britain", "spain", date(1809, 7, 1))
    assert not ref.exists("batavian-republic", date(1793, 7, 1))
    assert ref.exists("batavian-republic", date(1800, 7, 1))
    assert ref.exists("britain", date(1792, 1, 1))
    # the two rows looked at again: both low, the days by the month
    again = {
        frozenset(w["between"]): w
        for w in doc["wars"]
        if w.get("since") in (date(1801, 2, 27), date(1802, 6, 1))
    }
    for pair in (("spain", "portugal"), ("morocco", "united-states")):
        row = again[frozenset(pair)]
        assert row["confidence"] == "low" and row["days"] == "month", pair
        assert row["mark"] == "FROM MEMORY", pair
    assert again[frozenset(("morocco", "united-states"))]["until"] == date(1803, 10, 11)


# ---------------------------------------------------------------------------
# The classing (fast)
# ---------------------------------------------------------------------------


def test_the_classing_in_the_document_is_the_tools():
    """`docs/dev/RangeAudit.md` carries the classing's table as the tool prints it."""
    doc = (ROOT / "docs" / "dev" / "RangeAudit.md").read_text(encoding="utf-8")
    assert A.classing_table() in doc


def test_a_dated_key_in_no_row_and_a_file_that_will_not_parse_are_found(small, tmp_path):
    data = tmp_path / "data"
    (data / "ports").mkdir(parents=True)
    (data / "ports" / "atlantis.yaml").write_text(
        "id: atlantis\n"
        "nation:\n  - {nation: britain, until: 1800-01-01, source: 'x'}\n"
        "founded: 1801-05-01\n"
        "garrison:\n  - {since: 1803-01-01, men: 1800}\n",
        encoding="utf-8",
    )
    (data / "ports" / "broken.yaml").write_text("id: [unclosed\nnation: {\n", encoding="utf-8")
    unparsed: list[str] = []
    scan = A.scan_dated(data, unparsed)
    assert ("ports/atlantis.yaml", "founded", date(1801, 5, 1)) in scan
    assert ("ports/atlantis.yaml", "garrison.#.men", 1800) not in scan  # a figure, not a year
    assert unparsed == ["ports/broken.yaml"]
    audit = A.Audit()
    A.check_classing(audit, _planted(small, data=data), SOME_DAYS, scan, unparsed)
    keys = {k for k in audit.findings if k.startswith("c-un")}
    assert keys == {
        "c-unclassed:ports:founded",
        "c-unclassed:ports:garrison.#.since",
        "c-unparsed:ports/broken.yaml",
    }
    assert A.row_of("ports/atlantis.yaml", "nation.#.until").id == "port-holder"


def test_a_row_that_holds_no_key_and_the_keys_the_clock_puts_back_are_found(small):
    """A made scan of three keys: a port's holder (read against the clock under
    `follows_history`, and play could change it), a colour's dates (read by nothing) and a
    source. The holder is on the list for the design, the colours' dates are a key the game
    reads not, and every other row of the table holds nothing but the one that may."""
    scan = [
        ("ports/genoa.yaml", "nation.#.since", date(1805, 6, 4)),
        ("signals/britain/colours.yaml", "flags.#.dates", "1801-"),
        ("regimes.yaml", "regimes.escorting.source", "the Regulations 1806"),
    ]
    audit = A.Audit()
    A.check_classing(audit, small, SOME_DAYS, scan)
    assert "c-snap-back:port-holder" in audit.findings
    assert "c-unread:colours-dates" in audit.findings
    dead = {k.split(":", 1)[1] for k in audit.findings if k.startswith("c-dead-row:")}
    held = {"port-holder", "colours-dates", "words"}
    assert dead == {r.id for r in A.CLASSING if not r.optional} - held
    assert "scenario-nations" not in dead and not [k for k in audit.findings if "unclassed" in k]
    # the five the clock would put back, by the table itself
    assert sorted(r.id for r in A.CLASSING if r.kind in (A.CALENDAR, A.BOTH) and r.play) == [
        "blockades-dates",
        "days-years",
        "port-dated-keys",
        "port-holder",
        "wars-since",
    ]


# ---------------------------------------------------------------------------
# The ports, the wars and the blockades, planted on the small tree (fast)
# ---------------------------------------------------------------------------


def test_the_readers_road_puts_a_port_as_a_scenario_begun_that_day_finds_it(small):
    """The cheap road's port of a day is `load_port`'s with the day: the holder, the
    state and its blockaders, the yard, the pilot, the closures."""
    checked = 0
    for pid, port in small.ports.items():
        path = A.PORTS_DIR / f"{pid}.yaml"
        for day in (date(1792, 7, 1), date(1798, 10, 12), date(1805, 6, 4), date(1816, 1, 1)):
            mine = A.port_on(port, day)
            theirs = A.load_port(path, small.chart, None, day)
            for name in ("nation", "state", "blockaded_by", "closed_to"):
                assert getattr(mine, name) == getattr(theirs, name), (pid, day, name)
            assert mine.dockyard == theirs.dockyard and mine.pilot == theirs.pilot, (pid, day)
            checked += 1
    assert checked == 4 * len(SMALL_PORTS)
    assert A.port_on(small.ports["valletta"], date(1798, 6, 11)).nation == "order-of-st-john"
    assert A.port_on(small.ports["valletta"], date(1799, 1, 1)).blockaded_by == "britain"
    assert A.port_on(small.ports["valletta"], date(1800, 9, 5)).nation == "britain"
    assert A.port_on(small.ports["genoa"], date(1805, 6, 3)).nation == "liguria"
    assert A.port_on(small.ports["genoa"], date(1805, 6, 4)).nation == "france"


def test_a_port_held_by_no_nation_and_its_blockade_out_of_war_and_of_its_year_are_found(small):
    ports = dict(small.ports)
    genoa = copy.copy(ports["genoa"])
    genoa.nations = tuple(
        {**row, "nation": "atlantis"} if row["nation"] == "liguria" else row
        for row in genoa.nations
    )
    ports["genoa"] = genoa
    cadiz = copy.copy(ports["cadiz"])
    cadiz.blockade = {**cadiz.blockade, "by": "portugal"}
    ports["cadiz"] = cadiz
    audit = A.Audit()
    A.check_ports(audit, _planted(small, ports=ports), SOME_DAYS, None)
    assert _years_of(audit.findings["p-holder-unknown:genoa"]) == set(range(1792, 1806))
    assert "p-blockade-no-war:cadiz" in audit.findings
    # and on the tree as it stands: Cadiz's own blockade in words and before its year, the
    # keys no file of the ten dates, and no holder out of the table
    clean = A.Audit()
    A.check_ports(clean, small, SOME_DAYS, None)
    assert not [
        k for k in clean.findings if k.startswith(("p-holder-unknown", "p-blockade-no-war"))
    ]
    assert _years_of(clean.findings["p-blockade-before:cadiz"]) == set(range(1792, 1805))
    assert "p-blockade-words:cadiz" in clean.findings
    assert clean.findings["p-undated:nation"].count == len(SMALL_PORTS) - 2  # Genoa, Valletta
    assert clean.findings["p-undated:state"].count == len(SMALL_PORTS) - 1  # Valletta
    assert clean.findings["p-undated:market"].count == len(SMALL_PORTS)


def test_a_holder_and_a_blockade_out_of_the_references_years_are_its_own_kind(small):
    """Leghorn is Etruria's in its file on every day and the reference has no Etruria
    before 1801 or after 1807; Cadiz is blockaded in its file on every day and the
    reference has Britain and Spain at peace before October 1796 and after July 1808:
    findings of the reference's kind, and nothing mechanical is made of them."""
    audit = A.Audit()
    A.check_ports(audit, small, SOME_DAYS, A.load_reference())
    leghorn = audit.findings["r-holder:leghorn"]
    assert leghorn.basis == A.REFERENCE
    assert {1792, 1800, 1808, 1825} <= _years_of(leghorn)
    assert not _years_of(leghorn) & {1802, 1803, 1804, 1805, 1806}
    cadiz = audit.findings["r-port-blockade:cadiz"]
    assert {1792, 1796, 1802, 1803, 1809, 1825} <= _years_of(cadiz)
    assert not _years_of(cadiz) & {1797, 1800, 1805, 1807}
    none = A.Audit()
    A.check_ports(none, small, SOME_DAYS, None)
    assert not none.keys(A.REFERENCE)


def test_a_war_before_its_beginning_twice_allied_and_only_in_words_is_found(small):
    nations = copy.copy(small.nations)
    nations.wars = [
        {"between": ("britain", "france"), "since": date(1810, 1, 1), "source": "planted"},
        {"between": ("britain", "france"), "since": date(1810, 1, 1), "source": "planted"},
        {"between": ("britain", "spain"), "since": None, "source": "planted"},
    ]
    nations.allies = [("britain", "spain")]
    doc = {
        "nations": {
            "algiers": {"relations": {"portugal": "war, the corsairs taking her ships"}},
            "order-of-st-john": {
                "relations": {
                    "algiers": "the Order's standing war against the corsairs",
                    "tunis": "as Algiers'",
                    "britain": "peace; JUDGEMENT",
                }
            },
        }
    }
    audit = A.Audit()
    A.check_wars(audit, _planted(small, nations=nations, nations_doc=doc), SOME_DAYS, None)
    before = audit.findings["w-before-since:britain+france"]
    assert _years_of(before) == set(range(1792, 1810))
    assert _years_of(audit.findings["w-court:britain+france"]) == set(range(1792, 1810))
    assert "w-before-since:britain+spain" not in audit.findings  # no day given: no beginning
    assert "w-court:britain+spain" not in audit.findings
    assert "w-twice:britain+france" in audit.findings
    assert "w-allied:britain+spain" in audit.findings
    assert audit.findings["w-no-end"].count == 3
    assert {k for k in audit.findings if k.startswith("w-relations:")} == {
        "w-relations:algiers+portugal",
        "w-relations:algiers+order-of-st-john",
        "w-relations:order-of-st-john+tunis",
    }
    clean = A.Audit()
    A.check_wars(clean, small, SOME_DAYS, None)
    assert not [k for k in clean.findings if k.startswith(("w-twice", "w-allied"))]


def test_the_references_wars_and_nations_are_measured_against_the_table(small):
    """A planted reference of one war and one lifetime: the table's war with France is at
    peace by it outside 1800 to 1801, a war it has and the table has not is absent in its
    years, and a nation it ends in 1799 stands in the table after."""
    ref = A.Reference(
        wars=[
            {
                "between": ["britain", "france"],
                "since": date(1800, 1, 1),
                "until": date(1801, 12, 31),
            },
            {
                "between": ["france", "naples"],
                "since": date(1806, 1, 1),
                "until": date(1806, 12, 31),
            },
        ],
        lifetimes=[{"nation": "liguria", "until": date(1799, 12, 31)}],
        peaces=[],
    )
    audit = A.Audit()
    A.check_wars(audit, small, SOME_DAYS, ref)
    at_peace = audit.findings["r-war-at-peace:britain+france"]
    assert _years_of(at_peace) == set(range(1792, 1826)) - {1800, 1801}
    assert _years_of(audit.findings["r-war-absent:france+naples"]) == {1806}
    assert _years_of(audit.findings["r-nation:liguria"]) == set(range(1800, 1826))
    assert "r-nation:britain" not in audit.findings
    assert all(f.basis == A.REFERENCE for k, f in audit.findings.items() if k.startswith("r-"))
    assert set(ref.dates()) >= {date(1799, 12, 31), date(1800, 1, 1), date(1801, 12, 31)}


def test_a_blockade_with_no_dates_one_of_no_port_and_one_in_the_references_peace(small):
    nations = copy.copy(small.nations)
    france = copy.copy(nations.nations["france"])
    object.__setattr__(france, "naval", {**france.naval, "blockades": ["plymouth", "atlantis"]})
    nations.nations = {**nations.nations, "france": france}
    planted = _planted(small, nations=nations)
    audit = A.Audit()
    A.check_blockades(audit, planted, SOME_DAYS, A.load_reference())
    assert "b-undated:france:plymouth" in audit.findings
    assert "b-no-port:france:atlantis" in audit.findings
    assert ("france", "plymouth", 0) in A.blockades_on(planted, date(1805, 7, 1))
    brest = audit.findings["r-blockade:britain:brest"]
    assert brest.basis == A.REFERENCE
    assert {1792, 1802, 1814, 1825} <= _years_of(brest) and 1805 not in _years_of(brest)
    assert "b-undated:britain:brest" in audit.findings


def test_the_blockades_of_a_day_are_the_entries_within_their_dates(small):
    """The business's own rule, by the readers: Rochefort's from 1 June 1803 to 12 July
    1805, Cadiz's two, Ferrol's and Lorient's open at the end, Brest's on every day."""

    def ports(day):
        return {pid for _n, pid, _i in A.blockades_on(small, day)}

    assert ports(date(1803, 5, 31)) == {"brest"}
    assert "rochefort" in ports(date(1803, 6, 1)) and "rochefort" in ports(date(1805, 7, 12))
    assert "rochefort" not in ports(date(1805, 7, 13))
    assert "cadiz" in ports(date(1805, 4, 9)) and "cadiz" not in ports(date(1805, 4, 10))
    assert "cadiz" in ports(date(1805, 5, 31)) and "cadiz" in ports(date(1825, 7, 1))
    assert "lorient" not in ports(date(1808, 2, 29)) and "lorient" in ports(date(1808, 3, 1))
    assert ports(date(1792, 7, 1)) == {"brest"}
    assert ports(date(1805, 7, 1)) == {"brest", "rochefort", "ferrol", "cadiz"}


# ---------------------------------------------------------------------------
# The vessels, the flags, the days, the lights, the words, planted (fast)
# ---------------------------------------------------------------------------


def test_a_fit_of_a_later_year_is_found_where_a_description_or_a_scenario_carries_it(small):
    docs = dict(small.ship_docs)
    smack = copy.deepcopy(docs["smack.yaml"])
    smack["ship"]["descriptions"]["smack"]["fit"] = "as lengthened 1819"
    docs["smack.yaml"] = smack
    audit = A.Audit()
    A.check_vessels(audit, _planted(small, ship_docs=docs), SOME_DAYS)
    f = audit.findings["v-fit-ahead:smack:as lengthened 1819"]
    assert _years_of(f) == set(range(1792, 1819))
    assert "the business draws her" in f.words
    assert _years_of(audit.findings["v-fit-ahead:brig:diligence class 1796"]) == {
        1792,
        1793,
        1794,
        1795,
    }
    brig = {"file": "data/ships/brig.yaml"}
    scenarios = {"trials/early.yaml": {"start": "1793-06-01T08:00", "ship": brig}}
    planted = A.Audit()
    A.check_vessels(planted, _planted(small, scenario_docs=scenarios), SOME_DAYS)
    found = planted.findings["v-scenario:trials/early"]
    assert found.worst == ["her own ship, 'diligence class 1796'"]


def _flag(name, dates):
    return SimpleNamespace(name=name, dates=dates, flown_in=lambda y: A.F._in_dates(dates, y))


def test_colours_out_of_their_dates_and_flags_with_no_drawing_are_found(small, monkeypatch):
    """Planted colours: an ensign dated from 1801 that her occasion names, a jack no
    occasion names, and dates in two spans; planted signal flags with rows to 1810 only;
    a planted fashion from 1800."""
    made = SimpleNamespace(
        flags={
            "ensign": _flag("ensign", "1801-"),
            "old jack": _flag("old jack", "-1700"),
            "pendant": _flag("pendant", "-1806, 1815-"),
        },
        occasions=[SimpleNamespace(flags=(("ensign", "peak"), ("pendant", "main truck")))],
        nations={},
    )
    monkeypatch.setattr(A.F, "file_for_nation", lambda nations, nid: made)
    monkeypatch.setattr(A, "flag_roots", lambda: ["made"])
    rows = [_flag("numeral 1", "1793-1798"), _flag("numeral 1", "1799-1810"), _flag("truce", "")]
    monkeypatch.setattr(A.F, "load_signal_flags", lambda root: SimpleNamespace(rows=rows))
    monkeypatch.setattr(A, "_fashions", lambda root: (_flag("the fashion", "1800-"),))
    audit = A.Audit()
    A.check_flags(audit, small, SOME_DAYS)
    worn = audit.findings["f-colours:britain"]
    assert sorted(worn.worst) == ["ensign", "pendant"]  # the jack is worn on no occasion
    assert _years_of(worn) == set(range(1792, 1801)) | set(range(1807, 1815))
    assert "f-dates-form:britain:pendant" in audit.findings
    assert "f-dates-form:britain:ensign" not in audit.findings
    nearest = audit.findings["f-signal-nearest:made"]
    assert nearest.worst == ["numeral 1"] and nearest.count == 1
    assert _years_of(nearest) == {1792} | set(range(1811, 1826))
    assert _years_of(audit.findings["f-fashion:made"]) == set(range(1792, 1800))


def test_the_forms_of_dates_are_read_span_by_span():
    """'-1806, 1815-' is two spans to the audit and no form the engine's reader reads."""
    assert A.dates_hold("-1806, 1815-", 1800) and A.dates_hold("-1806, 1815-", 1820)
    assert not A.dates_hold("-1806, 1815-", 1810)
    assert A.dates_hold("", 1792) and A.dates_hold("1801-", 1801)
    assert not A.dates_hold("1801-", 1800)
    assert A.dates_hold("1805", 1805) and not A.dates_hold("1805", 1806)
    assert not A.engine_reads("-1806, 1815-") and A.engine_reads("1799-1803")
    assert A._year_edges("1801-") == [date(1800, 12, 31), date(1801, 1, 1)]
    assert A._year_edges("-1806, 1815-") == [
        date(1806, 12, 31),
        date(1807, 1, 1),
        date(1814, 12, 31),
        date(1815, 1, 1),
    ]


def test_nations_that_keep_no_day_and_a_year_with_none_are_found(small, monkeypatch):
    kept = (
        A.F.Day("the old king's birthday", 6, 4, "1760-1799", ("dress",), 21, "planted"),
        A.F.Day("the new king's birthday", 8, 12, "1802-", ("dress",), 21, "planted"),
    )
    monkeypatch.setattr(A.F, "load_days", lambda root: kept if root == "britain" else ())
    monkeypatch.setattr(A, "flag_roots", lambda: ["britain", "basic"])
    audit = A.Audit()
    A.check_days(audit, small, SOME_DAYS)
    assert _years_of(audit.findings["d-gap:britain"]) == {1800, 1801}
    assert "d-gap:basic" not in audit.findings  # a root with no days is the other finding
    none = audit.findings["d-none"]
    assert none.count == len(small.nations.nations) - 1 and "britain" not in none.worst


def test_a_light_dated_within_the_range_is_found_by_its_years(small):
    def light(fid, **lit):
        start, end = lit.get("from"), lit.get("until")
        return SimpleNamespace(
            id=fid,
            kind="light",
            lit=lit,
            lit_in=lambda y: (start is None or y >= start) and (end is None or y <= end),
        )

    features = {
        "new": light("new", **{"from": 1810}),
        "old": light("old", **{"from": 1700, "until": 1820}),
        "always": light("always", **{"from": 1600}),
        "head": SimpleNamespace(id="head", kind="headland", lit=None),
    }
    chart = SimpleNamespace(features=features)
    audit = A.Audit()
    A.check_lights(audit, _planted(small, chart=chart), SOME_DAYS)
    found = audit.findings["l-by-year"]
    assert found.count == 2 and found.worst == ["new", "old"]
    assert _years_of(found) == {1810, 1820}
    assert audit.info == ["the lights lit: 2 in 1792, 2 in 1805, 2 in 1825 (of 3 with years)"]


def test_the_tables_day_and_served_words_of_a_year_to_come_are_found(small):
    nations = copy.copy(small.nations)
    nations.as_of = date(1799, 3, 1)
    scan = [
        ("people/made.yaml", "wardroom.#.brief", "He keeps the Regulations of 1806 by him."),
        ("people/made.yaml", "wardroom.#.history", "Born at Saint-Malo in 1770."),
        ("ports/made.yaml", "source", "Purdy 1826, p. 80"),  # a source, not served
    ]
    audit = A.Audit()
    A.check_words(audit, _planted(small, nations=nations), SOME_DAYS, scan)
    assert _years_of(audit.findings["x-as-of"]) == set(range(1792, 1826)) - {1799}
    words = audit.findings["x-words:people-words"]
    assert words.count == 1 and _years_of(words) == set(range(1792, 1806))
    assert [k for k in audit.findings if k.startswith("x-words:")] == ["x-words:people-words"]


def test_a_year_fixed_in_the_code_is_found_and_a_seed_is_not(small, tmp_path):
    code = tmp_path / "freesail"
    code.mkdir()
    (code / "a.py").write_text(
        "from datetime import date, datetime\n"
        "START = datetime(1805, 6, 1, 4)\n"
        "def f(clock=None):\n"
        "    year = 1805\n"
        "    return date(1799, 1, 1), year\n",
        encoding="utf-8",
    )
    (code / "b.py").write_text("DEFAULT_SEED = 1805\nHALF_HOUR_S = 1800\n", encoding="utf-8")
    found = A.engine_years(code)
    assert set(found) == {"freesail/a.py"}
    assert len(found["freesail/a.py"]) == 3
    audit = A.Audit()
    A.check_engine(audit, _planted(small, code=code), SOME_DAYS)
    assert audit.findings["e-year:freesail/a.py"].count == 3


def test_what_no_data_dates_is_counted_element_by_element(small):
    """The ten of check (u) on the small tree: each counts what the tree holds, and a tree
    of two ship files has two ships with no year."""
    audit = A.Audit()
    A.check_undated(audit, small, SOME_DAYS)
    assert set(audit.findings) == {
        "u-nations",
        "u-letters",
        "u-colours-words",
        "u-ships",
        "u-books",
        "u-private",
        "u-regulations",
        "u-names",
        "u-trade",
        "u-prize-shares",
    }
    assert audit.findings["u-ships"].count == len(SMALL_SHIPS)
    assert audit.findings["u-nations"].count == len(small.nations.nations)
    assert all(_years_of(f) == set(range(1792, 1826)) for f in audit.findings.values())
    fewer = A.Audit()
    A.check_undated(fewer, _planted(small, ship_docs={}), SOME_DAYS)
    assert "u-ships" not in fewer.findings


# ---------------------------------------------------------------------------
# The rule of the owners: what a change of data alone clears (fast)
# ---------------------------------------------------------------------------


def _clear_p_undated(small, mp):
    keys = ("nation", *A.DATED_KEYS)
    rows = {
        pid: {**doc, **{k: [{k: doc.get(k), "source": "planted"}] for k in keys}}
        for pid, doc in small.port_docs.items()
    }
    before, after = A.Audit(), A.Audit()
    A.check_ports(before, small, SOME_DAYS, None)
    A.check_ports(after, _planted(small, port_docs=rows), SOME_DAYS, None)
    return before, after, [f"p-undated:{k}" for k in keys]


def _clear_p_blockade_words(small, mp):
    docs = dict(small.port_docs)
    docs["cadiz"] = {
        **docs["cadiz"],
        "blockade": {**docs["cadiz"]["blockade"], "since": "1805-01-01"},
    }
    before, after = A.Audit(), A.Audit()
    A.check_ports(before, small, SOME_DAYS, None)
    A.check_ports(after, _planted(small, port_docs=docs), SOME_DAYS, None)
    return before, after, ["p-blockade-words:cadiz"]


def _clear_p_blockade_before(small, mp):
    ports = dict(small.ports)
    cadiz = copy.copy(ports["cadiz"])
    cadiz.blockade = {**cadiz.blockade, "since": "1792-01-01"}
    ports["cadiz"] = cadiz
    before, after = A.Audit(), A.Audit()
    A.check_ports(before, small, SOME_DAYS, None)
    A.check_ports(after, _planted(small, ports=ports), SOME_DAYS, None)
    return before, after, ["p-blockade-before:cadiz"]


def _clear_w_relations(small, mp):
    nations = copy.copy(small.nations)
    nations.wars = [
        *small.nations.wars,
        *(
            {"between": pair, "since": None, "source": "planted"}
            for pair in (
                ("algiers", "portugal"),
                ("order-of-st-john", "algiers"),
                ("order-of-st-john", "tunis"),
            )
        ),
    ]
    before, after = A.Audit(), A.Audit()
    A.check_wars(before, small, SOME_DAYS, None)
    A.check_wars(after, _planted(small, nations=nations), SOME_DAYS, None)
    return (
        before,
        after,
        [
            "w-relations:algiers+portugal",
            "w-relations:algiers+order-of-st-john",
            "w-relations:order-of-st-john+tunis",
        ],
    )


def _clear_b_undated(small, mp):
    nations = copy.copy(small.nations)
    britain = copy.copy(nations.nations["britain"])
    dated = [
        {"port": "brest", "since": date(1803, 5, 18)} if entry == "brest" else entry
        for entry in britain.naval["blockades"]
    ]
    object.__setattr__(britain, "naval", {**britain.naval, "blockades": dated})
    nations.nations = {**nations.nations, "britain": britain}
    before, after = A.Audit(), A.Audit()
    A.check_blockades(before, small, SOME_DAYS, None)
    A.check_blockades(after, _planted(small, nations=nations), SOME_DAYS, None)
    return before, after, ["b-undated:britain:brest"]


def _clear_v_fit_ahead(small, mp):
    docs = dict(small.ship_docs)
    brig = copy.deepcopy(docs["brig.yaml"])
    brig["ship"]["descriptions"]["brig-sloop"]["fit"] = "an older class's carronades"
    docs["brig.yaml"] = brig
    before, after = A.Audit(), A.Audit()
    A.check_vessels(before, small, SOME_DAYS)
    A.check_vessels(after, _planted(small, ship_docs=docs), SOME_DAYS)
    return before, after, ["v-fit-ahead:brig:diligence class 1796"]


def _clear_f_signal_nearest(small, mp):
    plain = SimpleNamespace(flags={}, occasions=[], nations={})
    mp.setattr(A.F, "file_for_nation", lambda nations, nid: plain)
    mp.setattr(A, "flag_roots", lambda: ["made"])
    mp.setattr(A, "_fashions", lambda root: ())
    some = [_flag("numeral 1", "1799-1810")]
    mp.setattr(A.F, "load_signal_flags", lambda root: SimpleNamespace(rows=some))
    before = A.Audit()
    A.check_flags(before, small, SOME_DAYS)
    more = [*some, _flag("numeral 1", "-1798"), _flag("numeral 1", "1811-")]
    mp.setattr(A.F, "load_signal_flags", lambda root: SimpleNamespace(rows=more))
    after = A.Audit()
    A.check_flags(after, small, SOME_DAYS)
    return before, after, ["f-signal-nearest:made"]


def _days_audits(small, mp, before_days, after_days, key):
    mp.setattr(A, "flag_roots", lambda: ["britain"])
    mp.setattr(A.F, "load_days", before_days)
    before = A.Audit()
    A.check_days(before, small, SOME_DAYS)
    mp.setattr(A.F, "load_days", after_days)
    after = A.Audit()
    A.check_days(after, small, SOME_DAYS)
    return before, after, [key]


def _clear_d_none(small, mp):
    day = (A.F.Day("a day", 6, 4, "", ("dress",), 21, "planted"),)
    return _days_audits(
        small, mp, lambda root: day if root == "britain" else (), lambda root: day, "d-none"
    )


def _clear_d_gap(small, mp):
    old = A.F.Day("the old king's birthday", 6, 4, "1760-1799", ("dress",), 21, "planted")
    new = A.F.Day("the new king's birthday", 8, 12, "1802-", ("dress",), 21, "planted")
    between = A.F.Day("the regent's day", 1, 1, "1800-1801", ("dress",), 21, "planted")
    return _days_audits(
        small, mp, lambda root: (old, new), lambda root: (old, between, new), "d-gap:britain"
    )


def _clear_x_words(small, mp):
    cited = [("people/made.yaml", "wardroom.#.brief", "He keeps the Regulations of 1806.")]
    plain = [("people/made.yaml", "wardroom.#.brief", "He keeps the Regulations by him.")]
    before, after = A.Audit(), A.Audit()
    A.check_words(before, small, SOME_DAYS, cited)
    A.check_words(after, small, SOME_DAYS, plain)
    return before, after, ["x-words:people-words"]


def _clear_u_prize_shares(small, mp):
    doc = dict(small.business_doc)
    doc["prize_shares"] = [
        *doc["prize_shares"],
        *({"nation": nid, "classes": "british"} for nid in small.nations.nations),
    ]
    before, after = A.Audit(), A.Audit()
    A.check_undated(before, small, SOME_DAYS)
    A.check_undated(after, _planted(small, business_doc=doc), SOME_DAYS)
    return before, after, ["u-prize-shares"]


# A kind of finding (its key before the colon) to the planting in which a change of data
# alone, read by today's readers, clears it. A finding of a kind not here cannot be owned
# as the data's (`test_the_known_list_holds_each_finding_owned`).
DATA_CLEARS = {
    "p-undated": _clear_p_undated,
    "p-blockade-words": _clear_p_blockade_words,
    "p-blockade-before": _clear_p_blockade_before,
    "w-relations": _clear_w_relations,
    "b-undated": _clear_b_undated,
    "v-fit-ahead": _clear_v_fit_ahead,
    "f-signal-nearest": _clear_f_signal_nearest,
    "d-none": _clear_d_none,
    "d-gap": _clear_d_gap,
    "x-words": _clear_x_words,
    "u-prize-shares": _clear_u_prize_shares,
}


@pytest.mark.parametrize("kind", sorted(DATA_CLEARS))
def test_a_finding_owned_as_the_datas_is_cleared_by_a_change_of_data_alone(
    kind, small, monkeypatch
):
    """The rule of the owners, held: for each kind of finding the known list owns as a
    data fault, the finding is made, then a change to the data alone (a port's rows, a
    war entered in the table, a blockade's date, another fit, a flag's row, a day, the
    words, a prize scheme), read by the readers as they are, and the finding is gone."""
    before, after, keys = DATA_CLEARS[kind](small, monkeypatch)
    assert keys
    for key in keys:
        assert key.split(":")[0] == kind
        assert key in before.findings, key
        assert key not in after.findings, key


def test_a_war_with_an_end_and_a_nation_with_its_days_are_counted_no_more(small):
    """`w-no-end` and `u-nations` count what the table as loaded lacks, not what it holds:
    a war the loader came to keep an `until` for, and a nation it gave a `since` or an
    `until`, leave the counts; no change of data does that today, the loader keeping
    neither, so both are the engine's."""
    nations = copy.copy(small.nations)
    nations.wars = [
        {"between": ("britain", "france"), "since": date(1803, 5, 18), "until": date(1814, 5, 29)},
        {"between": ("britain", "spain"), "since": date(1804, 12, 12), "until": None},
        {"between": ("britain", "batavian-republic"), "since": date(1803, 6, 17)},
    ]
    audit = A.Audit()
    A.check_wars(audit, _planted(small, nations=nations), SOME_DAYS, None)
    found = audit.findings["w-no-end"]
    assert found.count == 2 and found.worst == ["britain+spain", "batavian-republic+britain"]
    nations.wars = [dict(w, until=date(1814, 5, 29)) for w in nations.wars]
    ended = A.Audit()
    A.check_wars(ended, _planted(small, nations=nations), SOME_DAYS, None)
    assert "w-no-end" not in ended.findings
    # as loaded today no war has an end: all three are counted
    today = A.Audit()
    A.check_wars(today, small, SOME_DAYS, None)
    assert today.findings["w-no-end"].count == len(small.nations.wars) == 3

    def with_days(n, **days):
        return SimpleNamespace(**{f: getattr(n, f) for f in n.__dataclass_fields__}, **days)

    table = dict(small.nations.nations)
    table["liguria"] = with_days(table["liguria"], since=date(1797, 6, 14), until=date(1805, 6, 3))
    table["order-of-st-john"] = with_days(table["order-of-st-john"], until=date(1798, 6, 11))
    lived = copy.copy(small.nations)
    lived.nations = table
    counted = A.Audit()
    A.check_undated(counted, _planted(small, nations=lived), SOME_DAYS)
    found = counted.findings["u-nations"]
    assert found.count == len(table) - 2
    assert not {"liguria", "order-of-st-john"} & set(found.worst)
    assert today.findings.get("u-nations") is None  # another check's
    all_of_them = A.Audit()
    A.check_undated(all_of_them, small, SOME_DAYS)
    assert all_of_them.findings["u-nations"].count == len(table)


def test_a_run_with_no_worlds_is_not_asked_for_what_only_a_world_makes():
    known = {
        "w-block-unread": {},
        "r-vessel:etruria": {"sweep": "full"},
        "p-undated:nation": {},
        "x-as-of": {},
    }
    audit = A.Audit()
    audit.add("x", "x-as-of", "words", [date(1792, 7, 1)])
    assert A.no_longer(audit, known, full=False) == ["p-undated:nation", "w-block-unread"]
    assert A.no_longer(audit, known, full=True) == [
        "p-undated:nation",
        "r-vessel:etruria",
        "w-block-unread",
    ]
    assert A.no_longer(audit, known, full=True, worlds=False) == ["p-undated:nation"]


# ---------------------------------------------------------------------------
# The two roads, planted on a made world (fast)
# ---------------------------------------------------------------------------


def _made_world(small, day, **changes):
    """What `check_world` reads of a world, made by hand from the readers' road: the same
    holders, wars and blockades, so that the two roads agree until something is planted."""
    ports = {pid: A.port_on(p, day) for pid, p in small.ports.items()}
    drawn = [
        SimpleNamespace(id=f"blockade-{pid}", regime="on blockade")
        for _n, pid, _i in sorted(A.blockades_on(small, day))
    ]
    world = SimpleNamespace(
        scenario=SimpleNamespace(nations=None),
        nations=small.nations,
        ports=SimpleNamespace(ports=ports),
        business=SimpleNamespace(inside=lambda pos: True),
        squadrons=SimpleNamespace(sets=drawn),
        vessels=SimpleNamespace(vessels=[]),
    )
    for name, value in changes.items():
        setattr(world, name, value)
    return world


def test_the_two_roads_agree_on_a_world_made_from_the_readers_and_differ_when_planted(small):
    day = date(1805, 7, 1)
    audit = A.Audit()
    A.check_world(audit, small, day, "rochefort", None, _made_world(small, day))
    assert not [k for k in audit.findings if k.startswith("a-")]
    assert audit.worlds == [(day, "rochefort")]
    # planted: another's wars, Genoa held by another, Valletta blockaded, Brest's squadron
    # not drawn and one drawn off Plymouth
    world = _made_world(small, day)
    nations = copy.copy(small.nations)
    nations.wars = [w for w in small.nations.wars if "spain" not in w["between"]]
    world.nations = nations
    genoa = copy.copy(world.ports.ports["genoa"])
    genoa.nation = "liguria"
    world.ports.ports["genoa"] = genoa
    valletta = copy.copy(world.ports.ports["valletta"])
    valletta.state, valletta.blockade = "blockaded", {"by": "france"}
    world.ports.ports["valletta"] = valletta
    world.squadrons.sets = [s for s in world.squadrons.sets if s.id != "blockade-brest"] + [
        SimpleNamespace(id="blockade-plymouth", regime="on blockade")
    ]
    planted = A.Audit()
    A.check_world(planted, small, day, "rochefort", None, world)
    assert {k for k in planted.findings if k.startswith("a-")} == {
        "a-wars",
        "a-holder:genoa",
        "a-state:valletta",
        "a-blockade:brest",
        "a-blockade:plymouth",
    }


def test_a_world_shows_the_block_unread_and_what_its_vessels_are_and_wear(small, monkeypatch):
    """A made world of 1 July 1792 that carries a scenario's block of no war and is at the
    table's wars; a vessel of no nation, one of a nation the reference has not yet, a brig
    of the fit of 1796, and a British ship under the ensign of 1801."""
    day = date(1792, 7, 1)
    block = {"as_of": "1792-07-01", "wars": [], "letters_of_marque": [], "source": "planted"}
    vessels = [
        SimpleNamespace(nation="atlantis", ship_file="data/ships/smack.yaml", fit=""),
        SimpleNamespace(nation="etruria", ship_file="data/ships/smack.yaml", fit=""),
        SimpleNamespace(nation="britain", ship_file=r"data\ships\brig.yaml", fit=""),
    ]
    world = _made_world(
        small,
        day,
        scenario=SimpleNamespace(nations=block),
        vessels=SimpleNamespace(vessels=vessels),
    )
    monkeypatch.setattr(
        A.F,
        "vessel_flies",
        lambda w, v: [{"name": "red ensign"}] if v.nation == "britain" else [],
    )
    audit = A.Audit()
    A.check_world(audit, small, day, "ushant", A.load_reference(), world)
    assert audit.findings["w-block-unread"].worst == ["ushant 1792-07-01"]
    assert "v-nation-unknown:atlantis" in audit.findings
    assert audit.findings["r-vessel:etruria"].basis == A.REFERENCE
    assert "v-fit-ahead:brig:diligence class 1796" in audit.findings
    assert audit.findings["f-colours:britain"].worst == ["red ensign worn off ushant 1792-07-01"]
    assert "x-as-of" in audit.findings  # the table's day, 1 June 1805, served in 1792
    assert not [k for k in audit.findings if k.startswith("a-")]
    # a world that read the block would be at peace with all: no finding, and not compared
    read = _made_world(small, day, scenario=SimpleNamespace(nations=block))
    peace = copy.copy(small.nations)
    peace.wars = []
    read.nations = peace
    none = A.Audit()
    A.check_world(none, small, day, "ushant", None, read)
    assert not none.findings and not none.worlds


# ---------------------------------------------------------------------------
# The slow tier: the ratchet
# ---------------------------------------------------------------------------


def test_the_sampled_sweep_is_the_known_list(sampled):
    """The ratchet: every finding of the sampled sweep is in the known list, and every
    listed finding but those only the full sweep makes is found, each within its ceiling.
    A new finding fails here with its words: own it in the list or mend it; a finding
    mended takes its entry out. The two roads agree on every whole-world day."""
    known = A.load_known()
    new = A.unlisted(sampled, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    gone = A.no_longer(sampled, known, full=False)
    assert not gone, f"listed findings the sampled sweep no longer makes (take them out): {gone}"
    over = A.over_ceiling(sampled, known)
    assert not over, CEILING_WORDS + "\n".join(
        f"{f.key}: {f.count} > {known[f.key]['most']}" for f in over
    )
    for f in sampled.findings.values():
        listed = _years(known[f.key]["years"])
        assert _years_of(f) <= listed, (f.key, sorted(_years_of(f) - listed))
    # every check ran, the dear road on its days, and the roads agree
    for letter in A.LETTERS:
        assert letter in sampled.seconds, letter
    assert sampled.worlds == list(A.SAMPLED_WORLDS)
    assert not [k for k in sampled.findings if k.startswith("a-")]
    text = A.report(sampled, known)
    assert f"== mechanical: {len(sampled.keys(A.MECHANICAL))} findings" in text
    assert f"== reference: {len(sampled.keys(A.REFERENCE))} findings" in text
    assert "by year: 1792 " in text and "whole worlds: 4" in text
    assert not [ln for ln in text.splitlines() if ln.startswith("! ")]


def test_the_mechanical_findings_stand_without_the_reference(tree, sampled):
    """The findings that rest on the reference are a kind of their own: with the reference
    thrown away the cheap road makes the same mechanical findings, of the same years and
    counts, and none of the other kind (the one mechanical finding only a world makes, the
    scenario's `nations:` block read by nothing, is the dear road's; the code's own years
    are left to the sampled sweep)."""
    alone = A.run(letters=QUICK, worlds=False, reference=False, tree=tree)
    assert not alone.keys(A.REFERENCE)
    both = {k for k in sampled.keys(A.MECHANICAL) if k[0] != "e"} - {"w-block-unread"}
    assert alone.keys() == both
    for key, f in alone.findings.items():
        assert f.count == sampled.findings[key].count, key
        assert _years_of(f) <= _years_of(sampled.findings[key]), key
    assert sampled.keys(A.REFERENCE) and all(k.startswith("r-") for k in sampled.keys(A.REFERENCE))


def test_the_sweep_is_the_same_twice(tree):
    """Deterministic: the same tree gives the same findings, days and counts."""
    one = A.run(letters=QUICK, worlds=False, tree=tree)
    two = A.run(letters=QUICK, worlds=False, tree=tree)
    assert one.days == two.days and len(one.days) > 150
    assert {k: (f.count, sorted(f.days), f.worst) for k, f in one.findings.items()} == {
        k: (f.count, sorted(f.days), f.worst) for k, f in two.findings.items()
    }


def test_the_days_are_a_day_in_every_year_and_either_side_of_each_date_named(tree):
    """A day in every year of the range, and the days either side of the dates the data
    names: Valletta's capitulation, the war's beginning, a blockade raised, the prize
    scheme's change, the Union of 1801, the old king's last birthday kept."""
    days = A.sample_days(tree)
    assert {d.year for d in days} == set(range(1792, 1826))
    for year in range(1792, 1826):
        assert date(year, 7, 1) in days
    for d in (
        date(1800, 9, 4),  # Valletta France's
        date(1800, 9, 5),  # Valletta the King's
        date(1803, 5, 17),
        date(1803, 5, 18),  # the war
        date(1805, 7, 12),
        date(1805, 7, 13),  # the blockade of Rochefort raised
        date(1807, 12, 31),
        date(1808, 1, 1),  # the eighths
        date(1800, 12, 31),
        date(1801, 1, 1),  # the Union
        date(1819, 6, 4),
        date(1820, 6, 4),  # the King's birthday, kept and not
    ):
        assert d in days, d
    assert all(A.in_range(d) for d in days)
    full = A.sample_days(tree, full=True)
    assert set(days) < set(full)
    assert all(date(y, 6, 4) in full for y in range(1792, 1826))


def test_the_readers_road_is_load_ports_for_every_port_with_dated_rows(tree):
    """As the small tree's test, for every port of the chart that carries dated rows."""
    checked = 0
    with A.fast_yaml():
        for pid, port in tree.ports.items():
            if not port.nations and not port.dated:
                continue
            path = A.PORTS_DIR / f"{pid}.yaml"
            for day in (date(1792, 7, 1), date(1798, 10, 12), date(1806, 2, 1), date(1816, 1, 1)):
                mine = A.port_on(port, day)
                theirs = A.load_port(path, tree.chart, None, day)
                for name in ("nation", "state", "blockaded_by", "closed_to"):
                    assert getattr(mine, name) == getattr(theirs, name), (pid, day, name)
                assert mine.dockyard == theirs.dockyard and mine.pilot == theirs.pilot, (pid, day)
                checked += 1
    assert checked >= 80


@pytest.mark.slow
def test_the_full_sweep_is_the_known_list_exactly(tree):
    """The ratchet, whole: the full sweep's findings are the known list's, no more and no
    fewer, each of the years listed and within its ceiling; the two roads agree on every
    whole-world day."""
    audit = A.run(full=True, tree=tree)
    known = A.load_known()
    new = A.unlisted(audit, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    gone = A.no_longer(audit, known, full=True)
    assert not gone, f"listed findings the full sweep no longer makes (take them out): {gone}"
    over = A.over_ceiling(audit, known)
    assert not over, CEILING_WORDS + "\n".join(
        f"{f.key}: {f.count} > {known[f.key]['most']}" for f in over
    )
    wrong = {
        k: (f.years(), known[k]["years"])
        for k, f in audit.findings.items()
        if f.years() != str(known[k]["years"])
    }
    assert not wrong, wrong
    assert len(audit.worlds) == len(A.world_days(full=True)) > 100
    assert not [k for k in audit.findings if k.startswith("a-")]


def _same(a, b) -> bool:
    """Two documents the same value by value and type by type, as `==` would not have
    them: True is not 1 and 1 is not 1.0, in a list, a dict, a tuple or a set alike; a
    float is its sign and its bits (-0.0 is not 0.0, and nan is nan); a datetime is its
    instant and its offset."""
    if type(a) is not type(b):
        return False
    if isinstance(a, dict):
        return (
            len(a) == len(b)
            and all(_same(x, y) for x, y in zip(a, b, strict=True))
            and all(_same(a[k], b[k]) for k in a)
        )
    if isinstance(a, list | tuple):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b, strict=True))
    if isinstance(a, set | frozenset):

        def order(items):
            return sorted(items, key=lambda x: (type(x).__name__, repr(x)))

        return len(a) == len(b) and all(
            _same(x, y) for x, y in zip(order(a), order(b), strict=True)
        )
    if isinstance(a, float):
        return repr(a) == repr(b)
    if isinstance(a, datetime):
        return a == b and a.utcoffset() == b.utcoffset()
    return a == b


def test_same_is_by_type_as_well_as_by_value():
    assert _same({"a": [1, 1.0, True, "1", None]}, {"a": [1, 1.0, True, "1", None]})
    assert not _same({"a": 1}, {"a": 1.0}) and not _same([True], [1]) and not _same(1, True)
    assert not _same({1: "a"}, {True: "a"}) and not _same({"a": 1, "b": 2}, {"b": 2, "a": 1})
    assert not _same([1, 2], [1]) and not _same({"a": [1]}, {"a": (1,)})
    # a float by its sign and its bits
    assert _same(-0.0, -0.0) and not _same(-0.0, 0.0) and not _same([0.0], [-0.0])
    assert _same(float("nan"), float("nan")) and _same({"a": float("nan")}, {"a": float("nan")})
    assert not _same(1.0, 1.0000000000000002)
    # a set and a tuple by type, as a list and a dict
    assert _same({1, "a"}, {"a", 1}) and not _same({1}, {True}) and not _same({1, 2}, {1.0, 2})
    assert _same((1, 2.0), (1, 2.0)) and not _same((1,), (True,)) and not _same((1, 2), (1,))
    assert not _same(frozenset({1}), {1})
    # a datetime by its instant and its offset; a date is no datetime
    utc = UTC
    noon = datetime(1805, 6, 1, 12, tzinfo=utc)
    assert _same(noon, datetime(1805, 6, 1, 12, tzinfo=utc))
    assert not _same(noon, datetime(1805, 6, 1, 13, tzinfo=timezone(timedelta(hours=1))))
    assert not _same(noon, datetime(1805, 6, 1, 12))
    assert not _same(date(1805, 6, 1), datetime(1805, 6, 1))


@pytest.mark.slow
def test_the_quick_loader_reads_every_file_as_the_games_own_does():
    """The audit's speed: libyaml's loader answers the game's `yaml.safe_load` while the
    audit runs. Every YAML file under data/ (all that the game can load under the swap:
    the charts' and the evolutions' with the rest) reads the same by both loaders, value
    by value and type by type; the swap is put back on the way out."""
    quick = getattr(yaml, "CSafeLoader", None)
    if quick is None:
        pytest.skip("libyaml's loader is not installed here: there is nothing to compare")
    files = sorted(A.DATA.rglob("*.yaml"))
    assert len(files) > 400  # 437 at 504a250, the chart's and the evolutions' among them
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert _same(yaml.load(text, Loader=quick), yaml.safe_load(text)), path  # noqa: S506
    plain = yaml.safe_load
    with A.fast_yaml():
        assert yaml.safe_load is not plain
        assert _same(
            yaml.safe_load("a: [1, 1.0, true, 1805-06-01]"), plain("a: [1, 1.0, true, 1805-06-01]")
        )
    assert yaml.safe_load is plain
    with pytest.raises(RuntimeError), A.fast_yaml():
        raise RuntimeError("the swap is put back when the audit fails, too")
    assert yaml.safe_load is plain


def test_with_no_quick_loader_the_audit_reads_by_the_games_own(monkeypatch):
    """Where libyaml is not installed the swap does nothing and the audit's own reads go
    by the game's loader."""
    monkeypatch.delattr(yaml, "CSafeLoader", raising=False)
    plain = yaml.safe_load
    with A.fast_yaml():
        assert yaml.safe_load is plain
    doc = A.read_yaml(A.REFERENCE_PATH)
    assert doc["range"]["since"] == date(1792, 1, 1)
