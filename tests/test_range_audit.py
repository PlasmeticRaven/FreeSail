"""Package 103a: the range's audit (`tools/audit_range.py`) and its ratchet.

Decision 69: a game begun on any day from 1792 to 1825 finds a world depicted accurately
and working. The audit measures how far the tree is from that: it seeds sampled days
through the game's own readers, makes a whole world on a few, and reports what it finds;
the known list (`data/range/audit-known.yaml`) holds every finding, owned. The fast tier
runs the sampled sweep and fails on a finding the list lacks and on a listed finding the
sweep no longer makes; the slow tier runs the full sweep and holds the list exactly, the
years and the ceilings with it. The findings that rest on the reference
(`data/range/reference.yaml`, FROM MEMORY, read by nothing in the game) are a kind of
their own, and the mechanical ones stand whole without it. The checks are proved by
planting: a port held by no nation, a war listed twice, a blockade with no dates, a fit of
a later year, a year fixed in the code, a dated key in no row of the classing.
Truths 7-590 to 7-592 are in test_known_truths.py.
"""

from __future__ import annotations

import copy
import importlib.util
import sys
from datetime import date
from pathlib import Path

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


@pytest.fixture(scope="module")
def tree():
    return A.load_tree()


@pytest.fixture(scope="module")
def sampled(tree):
    """The sampled sweep, whole worlds and all: once a run."""
    return A.run(tree=tree)


@pytest.fixture(scope="module")
def days(tree):
    return A.sample_days(tree)


def _planted(tree, **changes):
    """The tree with some of its parts replaced, the rest shared."""
    return A.Tree(**{**{f: getattr(tree, f) for f in tree.__dataclass_fields__}, **changes})


# ---------------------------------------------------------------------------
# The known list and the ratchet
# ---------------------------------------------------------------------------


def test_the_known_list_holds_each_finding_owned():
    """Every entry its key, what it is, the years it bites, its basis, whose it is and a
    reason in a line; no key twice; every key of one of the checks; a finding that rests
    on the reference is a judgement to be read against a source, and no other is said to
    rest on it."""
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


def test_the_sampled_sweep_is_the_known_list(sampled):
    """The ratchet, fast: every finding of the sampled sweep is in the known list, and
    every listed finding but those only the full sweep makes is found, each within its
    ceiling. A new finding fails here with its words: own it in the list or mend it; a
    finding mended takes its entry out. The two roads agree on every whole-world day."""
    known = A.load_known()
    new = A.unlisted(sampled, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    gone = A.no_longer(sampled, known, full=False)
    assert not gone, f"listed findings the sampled sweep no longer makes (take them out): {gone}"
    over = A.over_ceiling(sampled, known)
    assert not over, "counts above their ceiling:\n" + "\n".join(
        f"{f.key}: {f.count} > {known[f.key]['most']}" for f in over
    )
    for f in sampled.findings.values():
        years = {d.year for d in f.days}
        listed = _years(known[f.key]["years"])
        assert years <= listed, (f.key, sorted(years - listed))
    # every check ran, the dear road on its days, and the roads agree
    for letter in A.LETTERS:
        assert letter in sampled.seconds, letter
    assert sampled.worlds == list(A.SAMPLED_WORLDS)
    assert not [k for k in sampled.findings if k.startswith("a-")]


def _years(words: str) -> set[int]:
    out: set[int] = set()
    for part in str(words).split(","):
        lo, sep, hi = part.strip().partition("-")
        if lo.isdigit():
            out.update(range(int(lo), int(hi if sep else lo) + 1))
    return out


def test_the_mechanical_findings_stand_without_the_reference(tree, sampled):
    """The findings that rest on the reference are a kind of their own: with the reference
    thrown away the cheap road makes the same mechanical findings, of the same years and
    counts, and none of the other kind (the one mechanical finding only a world makes, the
    scenario's `nations:` block read by nothing, is the dear road's; the code's own years,
    the slowest check, are left to the sampled sweep)."""
    alone = A.run(letters=QUICK, worlds=False, reference=False, tree=tree)
    assert not alone.keys(A.REFERENCE)
    both = {k for k in sampled.keys(A.MECHANICAL) if k[0] != "e"} - {"w-block-unread"}
    assert alone.keys() == both
    for key, f in alone.findings.items():
        assert f.count == sampled.findings[key].count, key
        assert {d.year for d in f.days} <= {d.year for d in sampled.findings[key].days}, key
    assert sampled.keys(A.REFERENCE) and all(k.startswith("r-") for k in sampled.keys(A.REFERENCE))


# every check of the cheap road but the code's own years, which take two seconds a run
QUICK = "".join(c for c in A.LETTERS if c not in "ea")


def test_the_sweep_is_the_same_twice(tree):
    """Deterministic: the same tree gives the same findings, days and counts."""
    one = A.run(letters=QUICK, worlds=False, tree=tree)
    two = A.run(letters=QUICK, worlds=False, tree=tree)
    assert one.days == two.days and len(one.days) > 150
    assert {k: (f.count, sorted(f.days), f.worst) for k, f in one.findings.items()} == {
        k: (f.count, sorted(f.days), f.worst) for k, f in two.findings.items()
    }


def test_the_days_are_a_day_in_every_year_and_either_side_of_each_date_named(tree, days):
    """A day in every year of the range, and the days either side of the dates the data
    names: Valletta's capitulation, the war's beginning, a blockade raised, the prize
    scheme's change, the Union of 1801, the old king's last birthday kept."""
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


def test_the_readers_road_puts_a_port_as_a_scenario_begun_that_day_finds_it(tree):
    """The cheap road's port of a day is `load_port`'s with the day: the holder, the
    state and its blockaders, the yard, the pilot, the closures, for the ports with dated
    rows on the days either side of each of their dates."""
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
    assert A.port_on(tree.ports["valletta"], date(1798, 6, 11)).nation == "order-of-st-john"
    assert A.port_on(tree.ports["valletta"], date(1799, 1, 1)).blockaded_by == "britain"
    assert A.port_on(tree.ports["valletta"], date(1800, 9, 5)).nation == "britain"


# ---------------------------------------------------------------------------
# The reference
# ---------------------------------------------------------------------------


def test_the_reference_is_marked_small_and_read_by_nothing_in_the_game(tree):
    """`data/range/reference.yaml`: every row marked FROM MEMORY or citing where the tree
    already has it, with the writer's confidence and how far the days are known; only
    nations of the table; no row ending before it begins; and nothing under freesail/
    names the file or its directory."""
    doc = yaml.safe_load(A.REFERENCE_PATH.read_text(encoding="utf-8"))
    head = A.REFERENCE_PATH.read_text(encoding="utf-8").split("range:")[0]
    assert "NOT RESEARCH" in head and "NOT THE GAME'S DATA" in head and "FROM MEMORY" in head
    table = set(tree.nations.nations)
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
        assert "data/range" not in text and "reference.yaml" not in text, path
    ref = A.load_reference()
    assert ref.at_war("britain", "france", date(1793, 7, 1))
    assert not ref.at_war("britain", "france", date(1802, 7, 1))
    assert ref.at_war("spain", "britain", date(1805, 7, 1))
    assert not ref.at_war("britain", "spain", date(1809, 7, 1))
    assert not ref.exists("batavian-republic", date(1793, 7, 1))
    assert ref.exists("batavian-republic", date(1800, 7, 1)) and ref.exists(
        "britain", date(1792, 1, 1)
    )


def test_a_holder_out_of_its_lifetime_is_the_references_finding_and_no_other(tree, days):
    """Leghorn is Etruria's in its file on every day; the reference has no Etruria before
    1801 or after 1807: a finding of the reference's kind, and nothing mechanical."""
    audit = A.Audit()
    A.check_ports(audit, tree, days, A.load_reference())
    f = audit.findings["r-holder:leghorn"]
    assert f.basis == A.REFERENCE
    years = {d.year for d in f.days}
    assert {1792, 1800, 1808, 1825} <= years and not years & {1802, 1803, 1804, 1805, 1806}
    none = A.Audit()
    A.check_ports(none, tree, days, None)
    assert not none.keys(A.REFERENCE) and "r-holder:leghorn" not in none.findings


# ---------------------------------------------------------------------------
# Each check proved by planting
# ---------------------------------------------------------------------------


def test_a_port_held_by_no_nation_and_a_blockade_out_of_any_war_are_found(tree, days):
    ports = dict(tree.ports)
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
    A.check_ports(audit, _planted(tree, ports=ports), days, None)
    f = audit.findings["p-holder-unknown:genoa"]
    assert {d.year for d in f.days} == set(range(1792, 1806))  # to the annexation of June 1805
    assert "p-blockade-no-war:cadiz" in audit.findings
    clean = A.Audit()
    A.check_ports(clean, tree, days, None)
    assert not [
        k for k in clean.findings if k.startswith(("p-holder-unknown", "p-blockade-no-war"))
    ]


def test_a_war_listed_twice_and_a_pair_at_war_and_allied_are_found(tree, days):
    nations = copy.copy(tree.nations)
    nations.wars = [*tree.nations.wars, dict(tree.nations.wars[0])]
    nations.allies = [*tree.nations.allies, ("britain", "spain")]
    audit = A.Audit()
    A.check_wars(audit, _planted(tree, nations=nations), days, None)
    assert "w-twice:britain+france" in audit.findings
    assert "w-allied:britain+spain" in audit.findings
    clean = A.Audit()
    A.check_wars(clean, tree, days, None)
    assert not [k for k in clean.findings if k.startswith(("w-twice", "w-allied", "w-asymmetric"))]


def test_a_blockade_with_no_dates_and_one_of_a_port_with_no_file_are_found(tree, days):
    nations = copy.copy(tree.nations)
    france = copy.copy(nations.nations["france"])
    object.__setattr__(france, "naval", {**france.naval, "blockades": ["plymouth", "atlantis"]})
    nations.nations = {**nations.nations, "france": france}
    audit = A.Audit()
    A.check_blockades(audit, _planted(tree, nations=nations), days, None)
    assert "b-undated:france:plymouth" in audit.findings
    assert "b-no-port:france:atlantis" in audit.findings
    assert ("france", "plymouth", 0) in A.blockades_on(
        _planted(tree, nations=nations), date(1805, 7, 1)
    )


def test_the_blockades_of_a_day_are_the_entries_within_their_dates(tree):
    """The business's own rule, by the readers: Rochefort's from 1 June 1803 to 12 July
    1805, Cadiz's two, Ferrol's and Lorient's open at the end, Brest's on every day."""

    def ports(day):
        return {pid for _n, pid, _i in A.blockades_on(tree, day)}

    assert ports(date(1803, 5, 31)) == {"brest"}
    assert "rochefort" in ports(date(1803, 6, 1)) and "rochefort" in ports(date(1805, 7, 12))
    assert "rochefort" not in ports(date(1805, 7, 13))
    assert "cadiz" in ports(date(1805, 4, 9)) and "cadiz" not in ports(date(1805, 4, 10))
    assert "cadiz" in ports(date(1805, 5, 31)) and "cadiz" in ports(date(1825, 7, 1))
    assert "lorient" not in ports(date(1808, 2, 29)) and "lorient" in ports(date(1808, 3, 1))
    assert ports(date(1792, 7, 1)) == {"brest"}


def test_a_fit_of_a_later_year_is_found_where_a_description_carries_it(tree, days):
    docs = dict(tree.ship_docs)
    smack = copy.deepcopy(docs["smack.yaml"])
    smack["ship"]["descriptions"]["smack"]["fit"] = "as lengthened 1819"
    docs["smack.yaml"] = smack
    audit = A.Audit()
    A.check_vessels(audit, _planted(tree, ship_docs=docs), days)
    f = audit.findings["v-fit-ahead:smack:as lengthened 1819"]
    assert {d.year for d in f.days} == set(range(1792, 1819))
    assert "the business draws her" in f.words
    scenarios = {
        "early.yaml": {"start": "1793-06-01T08:00", "ship": {"file": "data/ships/brig.yaml"}}
    }
    planted = A.Audit()
    A.check_vessels(planted, _planted(tree, scenario_docs=scenarios), days)
    assert planted.findings["v-scenario:early"].worst == ["her own ship, 'diligence class 1796'"]


def test_a_year_fixed_in_the_code_is_found_and_a_seed_is_not(tmp_path):
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


def test_a_dated_key_in_no_row_of_the_classing_is_found(tree, days, tmp_path):
    data = tmp_path / "data"
    (data / "ports").mkdir(parents=True)
    (data / "ports" / "atlantis.yaml").write_text(
        "id: atlantis\n"
        "nation:\n  - {nation: britain, until: 1800-01-01, source: 'x'}\n"
        "founded: 1801-05-01\n"
        "garrison:\n  - {since: 1803-01-01, men: 1800}\n",
        encoding="utf-8",
    )
    scan = A.scan_dated(data)
    assert ("ports/atlantis.yaml", "founded", date(1801, 5, 1)) in scan
    assert ("ports/atlantis.yaml", "garrison.#.men", 1800) not in scan  # a figure, not a year
    audit = A.Audit()
    A.check_classing(audit, _planted(tree, data=data), days, scan)
    keys = {k for k in audit.findings if k.startswith("c-unclassed:")}
    assert keys == {"c-unclassed:ports:founded", "c-unclassed:ports:garrison.#.since"}
    assert A.row_of("ports/atlantis.yaml", "nation.#.until").id == "port-holder"


def test_the_forms_of_dates_are_read_span_by_span(tree):
    """'-1806, 1815-' is two spans to the audit and no form the engine's reader reads;
    a British signal flag has a drawing for 1805 and none for 1811."""
    assert A.dates_hold("-1806, 1815-", 1800) and A.dates_hold("-1806, 1815-", 1820)
    assert not A.dates_hold("-1806, 1815-", 1810)
    assert (
        A.dates_hold("", 1792) and A.dates_hold("1801-", 1801) and not A.dates_hold("1801-", 1800)
    )
    assert A.dates_hold("1805", 1805) and not A.dates_hold("1805", 1806)
    assert not A.engine_reads("-1806, 1815-") and A.engine_reads("1799-1803")
    rows = [r for r in A.F.load_signal_flags("britain").rows if r.name == "numeral 1"]
    assert any(r.flown_in(1805) for r in rows) and not any(r.flown_in(1811) for r in rows)


def test_the_classing_in_the_document_is_the_tools(tree):
    """`docs/dev/RangeAudit.md` carries the classing's table as the tool prints it."""
    doc = (ROOT / "docs" / "dev" / "RangeAudit.md").read_text(encoding="utf-8")
    assert A.classing_table() in doc


def test_the_report_gives_the_two_kinds_apart_by_check_and_by_year(sampled):
    text = A.report(sampled, A.load_known())
    assert f"== mechanical: {len(sampled.keys(A.MECHANICAL))} findings" in text
    assert f"== reference: {len(sampled.keys(A.REFERENCE))} findings" in text
    assert "by year: 1792 " in text and "whole worlds: 4" in text
    assert not [ln for ln in text.splitlines() if ln.startswith("! ")]


# ---------------------------------------------------------------------------
# The slow tier
# ---------------------------------------------------------------------------


@pytest.mark.slow
def test_the_full_sweep_is_the_known_list_exactly(tree):
    """The ratchet, slow: the full sweep's findings are the known list's, no more and no
    fewer, each of the years listed and within its ceiling; the two roads agree on every
    whole-world day."""
    audit = A.run(full=True, tree=tree)
    known = A.load_known()
    new = A.unlisted(audit, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    gone = A.no_longer(audit, known, full=True)
    assert not gone, f"listed findings the full sweep no longer makes (take them out): {gone}"
    over = A.over_ceiling(audit, known)
    assert not over, [(f.key, f.count) for f in over]
    wrong = {
        k: (f.years(), known[k]["years"])
        for k, f in audit.findings.items()
        if f.years() != str(known[k]["years"])
    }
    assert not wrong, wrong
    assert len(audit.worlds) == len(A.world_days(full=True)) > 100
    assert not [k for k in audit.findings if k.startswith("a-")]


@pytest.mark.slow
def test_the_quick_loader_reads_every_file_as_the_games_own_does():
    """The audit's speed: libyaml's loader for the game's `yaml.safe_load` while it runs.
    Every ship, port, signal, scenario and top-level data file reads the same by both."""
    quick = getattr(yaml, "CSafeLoader", yaml.SafeLoader)  # the game's own where it is absent
    files = [
        *A.SHIPS_DIR.glob("*.yaml"),
        *A.PORTS_DIR.glob("*.yaml"),
        *A.SIGNALS_DIR.rglob("*.yaml"),
        *A.SCENARIOS_DIR.rglob("*.yaml"),
        *A.DATA.glob("*.yaml"),
        *(A.DATA / "captains").glob("*.yaml"),
        *(A.DATA / "squadrons").glob("*.yaml"),
        *(A.DATA / "people").glob("*.yaml"),
    ]
    assert len(files) > 250
    for path in files:
        text = path.read_text(encoding="utf-8")
        assert yaml.load(text, Loader=quick) == yaml.safe_load(text), path
    plain = yaml.safe_load
    with A.fast_yaml():
        assert (yaml.safe_load is not plain) == (quick is not yaml.SafeLoader)
    assert yaml.safe_load is plain
