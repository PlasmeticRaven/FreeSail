"""The range's audit (package 103a): how far the world is from decision 69.

    python tools/audit_range.py [--full] [--known] [--entries] [--classing] [--no-worlds]

Decision 69 (docs/DesignProposal.md): a game begun on any day from 1792 to 1825 finds a
world depicted accurately and working. This tool measures how far the tree is from that,
as package 111's audit measures the chart: a sweep, a known list with each finding owned
(`tools/range/audit-known.yaml`), and a test that fails on a finding the list lacks and on a
listed finding the sweep no longer makes (`tests/test_range_audit.py`). It mends nothing
and changes no data.

**Two roads.** The cheap road seeds each sampled day through the game's own readers
(`nations.load_nations`, `ports.load_port` and the port's dated rows, the business's date
test `business._between`, the flags', the days', the lights' and the prize shares' readers)
without making a world. The dear road makes a whole rules-only world on a few days, for
what only a world shows: the vessels the business draws, the blockading squadrons, the
lines the world serves. On every whole-world day the two roads are compared on what both
can see (the ports' holders, the wars, the blockades), so that the cheap road is proved
against the dear one (check a).

**The days.** A day in every year of the range (1 July, JUDGEMENT) and the days either
side of every date the data itself names (a port's dated rows, a war's beginning, a
blockade's dates, a prize scheme's, the years of a flag, a fashion, a national day and a
light). `--full` adds every national day in every year of the range with the day after it,
and many more whole worlds. The reference's own dates (below) are sampled only for the
findings that rest on it. Deterministic: the same seed and tree give the same findings.

**The checks, by letter.**
(p) the ports: every holder a nation of the table; the keys no file dates; a port's own
    blockade against its own `since` and the table's wars.
(w) the wars: a war in force before its own beginning; the stance against the prize court's
    reading of the same day; no end and no peace in the table; a pair listed twice, at war
    and allied at once; what a nation's `relations` say in words against the table.
(b) the blockades: an entry with no dates; one drawn outside any war of the table's.
(v) the vessels: a fit whose name carries a year later than the day, wherever a description
    a scenario or the business may name carries it; a shipped scenario that begins before
    the year of a fit it sails.
(f) the flags: a nation's colours whose dates do not hold the day's year, flown regardless;
    dates the engine's reader cannot read; a signal flag with no drawing for the year,
    served the nearest; the dressing fashion likewise.
(d) the days: the nations that keep no day; the years in which a root keeps none.
(l) the lights: those dated within the range, by the year alone.
(x) the words: the table's day served as the day she sailed with it; served words that
    name a year yet to come on the day (JUDGEMENT: which words are served is the
    classing's).
(e) the engine: a year or a date fixed in the code.
(u) what no data dates at all, one finding to an element: the nations' lifetimes, the
    letters of marque, the ships, the signal books, the private signals, the regulations,
    the colours' words, the names, the trade, the prize shares.
(c) the classing: every dated key of the data in the table (`CLASSING`); a data file
    that will not parse; a row of the table that matches nothing; each key read against
    the running clock that play could change, and each key parsed and read by nothing.
(r) the reference: the same day's wars, nations and blockades against
    `tools/range/reference.yaml`, a table of the range's wars, peaces and nations'
    lifetimes written FROM MEMORY and read by nothing in the game. These findings are a
    kind of their own (`basis: reference`), counted and listed apart; the mechanical
    findings stand whole if the reference is thrown away (`--no-reference`).
(a) the two roads agree (whole-world days only): no finding is the proof.

**Speed.** The game reads its YAML with the pure-Python loader; a ship file takes it some
half a second and a world loads a dozen. While this tool runs, and only then, the same
call is answered by libyaml's loader where it is installed (`fast_yaml`), which reads the
same documents (the slow tier's test holds it file for file).

**Keys.** A file enters a key, and is matched against the classing, only by `key_of`:
its path under its folder with forward slashes, the same on every machine. The known list
and the reference lie under `tools/range/`, not under `data/`, which the build's
fingerprint hashes whole.

Figures marked JUDGEMENT are the audit's own choices of what counts as a finding.
"""

from __future__ import annotations

import argparse
import ast
import contextlib
import copy
import fnmatch
import re
import sys
import time
from collections import defaultdict
from collections.abc import Iterable, Iterator
from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from pathlib import Path, PurePath, PurePosixPath
from types import SimpleNamespace
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from freesail.world import business as B  # noqa: E402
from freesail.world import flags as F  # noqa: E402
from freesail.world import prize_court as PC  # noqa: E402
from freesail.world import ships as SH  # noqa: E402
from freesail.world.chart import load_chart  # noqa: E402
from freesail.world.nations import Nations, load_nations  # noqa: E402
from freesail.world.ports import DATED_KEYS, load_port  # noqa: E402

DATA = ROOT / "data"
CODE = ROOT / "freesail"
# The audit's own two files: beside the tool, not under data/, which the build's
# fingerprint hashes whole (`core.world.fingerprint_of`); the game reads neither.
RANGE_DIR = ROOT / "tools" / "range"
KNOWN_PATH = RANGE_DIR / "audit-known.yaml"
REFERENCE_PATH = RANGE_DIR / "reference.yaml"
PORTS_DIR = DATA / "ports"
SHIPS_DIR = DATA / "ships"
SCENARIOS_DIR = DATA / "scenarios"
SIGNALS_DIR = DATA / "signals"
NATIONS_PATH = DATA / "nations.yaml"
BUSINESS_PATH = DATA / "business.yaml"
CHART_NAME = "atlantic-east"

# The first episode (decision 69).
RANGE_SINCE = date(1792, 1, 1)
RANGE_UNTIL = date(1825, 12, 31)
# The day sampled in every year (JUDGEMENT: midsummer's quarter, clear of every date the
# data names).
YEAR_DAY = (7, 1)

LETTERS = "pwbvfdlxeucra"
MECHANICAL = "mechanical"
REFERENCE = "reference"
OWNERS = (
    "a data fault for milestone 7c",
    "an engine fault",
    "a judgement to be read against a source",
)

# A year in a name or in words.
YEAR = re.compile(r"(?<![A-Za-z0-9_.])(1[5-9]\d\d|20\d\d)(?![0-9A-RT-Za-rt-z_]|\.\d)")
# The keys whose whole number is a year (a number under any other key is a figure: a
# range in metres, a count of shot, half an hour in seconds).
DATE_NAMES = frozenset(
    {"since", "until", "from", "dates", "years", "year", "date", "as_of", "at", "start"}
    | {"almanac", "rated", "checked_on"}
)

# The whole worlds (JUDGEMENT): a station is a place a rules-only world is begun at, with
# the business on; the fast tier's are few and cheap, each chosen for what it shows.
STATIONS = {
    "ushant": (48.3, -5.4),  # the blockade of Brest, the Channel's trade
    "rochefort": (46.0, -1.7),  # a dated blockade (1 June 1803 to 12 July 1805)
    "cadiz": (36.4, -6.6),  # two dated blockades and the port's own
    "gibraltar": (36.144, -5.364),  # the Strait
    "toulon": (43.0, 5.9),  # the gulf of Lion
    "leghorn": (43.4, 10.0),  # the Ligurian sea: Etruria, Liguria
    "malta": (35.95, 14.65),  # the Order's, France's, the King's
}
SAMPLED_WORLDS = (
    (date(1792, 7, 1), "ushant"),  # before any war of the range
    (date(1802, 7, 1), "rochefort"),  # the peace of Amiens
    (date(1805, 7, 1), "rochefort"),  # the day the build knows best
    (date(1814, 7, 1), "cadiz"),  # the peace of Paris, Spain long an ally
)
FULL_STATIONS_EVERY_YEAR = ("ushant", "rochefort", "cadiz")
FULL_STATIONS_SOME_YEARS = ("gibraltar", "toulon", "leghorn", "malta")
FULL_SOME_YEARS_STEP = 4
WORLD_SEED = 7
WORLD_SHIP = "data/ships/frigate-36.yaml"
WORLD_NATION = "britain"

# The files that state a regulation, an instruction or a custom as a rule with no date in
# force (JUDGEMENT, for the one finding `u-regulations`).
REGULATION_FILES = (
    "regimes.yaml",
    "squadrons/blockade.yaml",
    "squadrons/convoy.yaml",
    "squadrons/squadron.yaml",
    "crew/ration.yaml",
    "crew/needs.yaml",
    "marines.yaml",
    "papers/papers.yaml",
    "standing_orders/starter.orders",
    "standing_orders/fighting.orders",
)
# A signal root's book files (the seven of every root less its colours and flags, which
# carry dates).
BOOK_FILES = ("book.yaml", "convoy.yaml", "night_fog.yaml", "numerary.yaml", "telegraphic.yaml")


# ---------------------------------------------------------------------------
# The classing: every dated key of the data, how the code reads it
# ---------------------------------------------------------------------------

SEED = "seed"
CALENDAR = "calendar-read"
BOTH = "both by the scenario's choice"
SCRIPT = "script"
UNREAD = "read by nothing"
WORDS = "words"
SERVED = "words, served"
NAME = "a name carrying a year"
BUILDERS = "the builders' own date"


@dataclass(frozen=True)
class Row:
    """One row of the classing: the files it holds (a pattern under data/), the key paths
    (patterns; a list's item is `#`), its class, the reader, and for a key read against the
    running clock what play could change that the clock would then put back ('' where
    nothing in play can)."""

    id: str
    files: str
    paths: tuple[str, ...]
    kind: str
    reader: str
    play: str = ""
    optional: bool = False  # a key the format has and no file yet carries


SOURCE_PATHS = (
    "*source",
    "*sources.#",
    "*source.*",
    "*note",
    "*notes",
    "*notes.#",
    "*.note.*",
)

CLASSING: tuple[Row, ...] = (
    # -- the ports
    Row(
        "port-holder",
        "ports/*.yaml",
        ("nation.#.since", "nation.#.until"),
        BOTH,
        "`ports.load_port` puts the row of the scenario's first day into `Port.nation`; under "
        "`follows_history` `Ports.tick` and `Port.on_events` put it to the record's row on "
        "each day a row begins or ends",
        "a port taken or given up in play is the record's holder's again on the next day one "
        "of its rows begins or ends (no order takes a port yet; decision 69 (c) means one "
        "will)",
    ),
    Row(
        "port-dated-keys",
        "ports/*.yaml",
        tuple(f"{k}.#.{w}" for k in DATED_KEYS for w in ("since", "until")),
        BOTH,
        "`ports.load_port` (`_dated_rows`, `_value_on`) on the first day; `Port.on_events` "
        "under `follows_history`",
        "the director's `port <id>: closed to` and `open to`, a price order, and whatever "
        "play does to a yard, a pilot or a crew's pool are overwritten on the next day a row "
        "of that key begins or ends",
    ),
    Row(
        "port-blockade-since",
        "ports/*.yaml",
        ("blockade.since", "state.#.blockade.since"),
        SERVED,
        "kept as words (`ports._port_state`) and said by `Ports.blockades`; read as no date",
    ),
    Row(
        "port-pilot-words",
        "ports/*.yaml",
        ("pilot.words.*", "pilot.#.pilot.words.*"),
        SERVED,
        "the pilot's own words, said as he comes aboard",
    ),
    Row("port-words", "ports/*.yaml", (*SOURCE_PATHS, "datum"), WORDS, "a source or a note"),
    # -- the nations
    Row(
        "nations-as-of",
        "nations.yaml",
        ("as_of",),
        SERVED,
        "`nations.load_nations`; printed by `Nations.sailed_with_words` as the day of the "
        "table she sailed with, whatever the scenario's day; read as no date",
    ),
    Row(
        "wars-since",
        "nations.yaml",
        ("wars.#.since",),
        CALENDAR,
        "`Nations.at_war` (the stance, the business) ignores it; `prize_court._at_war_at` "
        "reads it against the day of the taking",
        "a war the world is in by its table is no war to the prize court before the record's "
        "day, and a war declared in play (`Nations.declare_war`) carries its day in words or "
        "none, which the court reads as never or as always",
    ),
    Row(
        "blockades-dates",
        "nations.yaml",
        ("nations.*.naval.blockades.#.since", "nations.*.naval.blockades.#.until"),
        BOTH,
        "`business._blockades` with `business._between`: the scenario's first day, or the "
        "running day under `follows_history`, when a region is peopled",
        "a blockade raised or laid in play is drawn again or not by the record's dates the "
        "next time the region is peopled, under `follows_history`",
    ),
    Row(
        "nations-relations",
        "nations.yaml",
        ("nations.*.relations.*",),
        UNREAD,
        "nothing: `load_nations` does not take the key; war and peace between the later "
        "nations stand only in these words",
    ),
    Row(
        "nations-colours-words",
        "nations.yaml",
        ("nations.*.colours", "nations.*.flag"),
        SERVED,
        "`Nation.colours` and `Nation.flag`, the lookout's words for a ship's colours",
    ),
    Row(
        "nations-words",
        "nations.yaml",
        ("*source", "*source.*", "*.source", "*.sources.*"),
        WORDS,
        "a source",
    ),
    # -- the business and the prize court
    Row(
        "prize-shares",
        "business.yaml",
        ("prize_shares.#.from", "prize_shares.#.until"),
        CALENDAR,
        "`prize_court.scheme_for`, by the day of the court's sentence",
    ),
    # -- the signals
    Row(
        "colours-dates",
        "signals/*/colours.yaml",
        ("flags.#.dates", "nations.*.flags.#.dates"),
        UNREAD,
        "parsed into `flags.Flag.dates` and read by nothing: a ship wears the flag her "
        "occasion names whatever the year",
    ),
    Row(
        "signal-flags-dates",
        "signals/*/flags.yaml",
        ("flags.#.dates",),
        CALENDAR,
        "`flags.SignalFlagsFile.drawing_of` by the running year (`api/viewer_flags.py`); "
        "with no row for the year, the nearest",
    ),
    Row(
        "dressing-dates",
        "signals/*/dressing.yaml",
        ("fashions.#.dates",),
        CALENDAR,
        "`flags.fashion_for` by the running year; with no row for the year, the nearest earlier",
    ),
    Row(
        "days-years",
        "signals/*/days.yaml",
        ("days.#.years", "days.#.date"),
        CALENDAR,
        "`flags.days_on` by the running day (`flags.dressing_tick`)",
        "a king dead or a government fallen in play: his day is kept, or dropped, by the "
        "record's years regardless (nothing in play does either yet)",
    ),
    Row("signals-words", "signals/*/*.yaml", (*SOURCE_PATHS, "*.source"), WORDS, "a source"),
    # -- the chart's features
    Row(
        "lights-years",
        "charts/features/*.yaml",
        ("features.#.lit.from", "features.#.lit.until"),
        CALENDAR,
        "`chart.Feature.lit_in` by the running year (the lookout, the browser's map)",
    ),
    Row(
        "feature-names",
        "charts/features/*.yaml",
        ("features.#.id",),
        NAME,
        "a feature's id, a name only",
    ),
    Row(
        "feature-words",
        "charts/features/*.yaml",
        (
            "features.#.says",
            "features.#.lit.character",
            "features.#.modern",
            "features.#.fix",
            "features.#.view",
            "features.#.name",
            *SOURCE_PATHS,
            "*.source",
        ),
        WORDS,
        "a mark's words: `says` is served only for the shore and a point of interest, a "
        "light's `character` and `modern` to nobody",
    ),
    # -- the scenarios
    Row(
        "scenario-start",
        "scenarios/*.yaml|scenarios/trials/*.yaml|regatta/*.yaml",
        ("start", "start.at"),
        SEED,
        "`scenarios.load_scenario`: the clock's first day, the day every seed above is read on",
    ),
    Row(
        "scenario-papers",
        "scenarios/*.yaml|scenarios/trials/*.yaml",
        ("papers.almanac", "papers.chart.year"),
        UNREAD,
        "kept in `Scenario.papers`; no code reads either (the almanac's figures are "
        "computed from the clock)",
    ),
    Row(
        "scenario-chronometer",
        "scenarios/*.yaml|scenarios/trials/*.yaml",
        ("papers.chronometer.rated",),
        SEED,
        "`reckoning.Chronometer.from_scenario`: the day she was rated, counted from",
    ),
    Row(
        "scenario-script",
        "scenarios/*.yaml|scenarios/trials/*.yaml|director/briefs/*.yaml",
        (
            "weather.wind.#.at",
            "weather.systems.#.track.#.at",
            "weather.#.at",
            "world_orders.#.at",
            "world_orders.#.order",
            "examples.#",
        ),
        SCRIPT,
        "the author's own timed script (the weather's, the world's orders)",
    ),
    Row(
        "scenario-nations",
        "scenarios/*.yaml|scenarios/trials/*.yaml",
        ("nations.as_of", "nations.wars.#.since"),
        UNREAD,
        "`scenarios._nations_block` reads and keeps it (`Scenario.nations`); the World "
        "loads the table's wars whatever it says (no shipped scenario carries the block)",
        optional=True,
    ),
    # -- the ships
    Row(
        "ship-fit-names",
        "ships/*.yaml",
        ("armament.default", "armament.fits.*", "ship.descriptions.*.fit"),
        NAME,
        "a fit's name; no reader takes the year from it (`ships.vessel_from_spec` takes "
        "the description's fit whatever the day)",
    ),
    Row(
        "ship-words",
        "ships/*.yaml",
        ("ship.era_notes",),
        SERVED,
        "the ship's own account of herself, served by the reading of her particulars",
    ),
    # -- the people
    Row(
        "people-words",
        "people/*.yaml",
        ("wardroom.#.brief", "wardroom.#.history"),
        SERVED,
        "an officer's brief and his history, served to whoever holds his station",
    ),
    # -- the builders' own
    Row(
        "chart-provenance",
        "charts/*.yaml|charts/overrides/*/*.yaml",
        ("*",),
        BUILDERS,
        "the chart's manifest, its overrides, its checks and its audit's list: where a "
        "tile or a sounding is from and the day a builder fetched or checked it; nothing "
        "of the world's days (JUDGEMENT: these files are classed whole)",
    ),
    # -- every other word: a source, a note, a title
    Row(
        "words",
        "*",
        (
            *SOURCE_PATHS,
            "*.source",
            "*.sheet",
            "sheet",
            "*.datum",
            "datum",
            "*.title",
            "*.record",
            "*.found",
            "*.item",
            "*found_on_the_way.#",
            "*.name",
            "kits.*",
        ),
        WORDS,
        "a source, a note or a title; not served as the world's word of a day",
    ),
)


# ---------------------------------------------------------------------------
# Findings
# ---------------------------------------------------------------------------


@dataclass
class Finding:
    """One finding: its check's letter, its key (the ratchet's: the check and what it is of,
    never a count or a day), its basis (mechanical, or resting on the reference), the
    words, the sampled days it bites, how many things, and a few of them."""

    check: str
    key: str
    basis: str
    words: str
    days: set[date] = field(default_factory=set)
    count: int = 1
    worst: list[str] = field(default_factory=list)

    def years(self) -> str:
        return span_words({d.year for d in self.days})

    def line(self) -> str:
        some = f" ({'; '.join(self.worst[:4])})" if self.worst else ""
        mark = "" if self.basis == MECHANICAL else " [reference]"
        return f"[{self.check}]{mark} {self.key}: {self.words}; {self.years()}; {self.count}{some}"


@dataclass
class Audit:
    findings: dict[str, Finding] = field(default_factory=dict)
    info: list[str] = field(default_factory=list)
    seconds: dict[str, float] = field(default_factory=dict)
    days: list[date] = field(default_factory=list)
    worlds: list[tuple[date, str]] = field(default_factory=list)

    def add(
        self,
        check: str,
        key: str,
        words: str,
        days: Any = (),
        *,
        basis: str = MECHANICAL,
        count: int = 1,
        worst: Any = (),
    ) -> None:
        f = self.findings.get(key)
        if f is None:
            f = self.findings[key] = Finding(check, key, basis, words, count=0)
        f.days.update([days] if isinstance(days, date) else days)
        f.count = max(f.count, int(count))
        for w in worst:
            if w not in f.worst:
                f.worst.append(w)

    def keys(self, basis: str | None = None) -> set[str]:
        return {k for k, f in self.findings.items() if basis is None or f.basis == basis}


def span_words(years: set[int]) -> str:
    """Years as spans: '1792-1802, 1808, 1814-1825'; 'no day' for none."""
    if not years:
        return "no day"
    out, run = [], []
    for y in sorted(years):
        if run and y == run[-1] + 1:
            run.append(y)
        else:
            if run:
                out.append(run)
            run = [y]
    out.append(run)
    return ", ".join(str(r[0]) if len(r) == 1 else f"{r[0]}-{r[-1]}" for r in out)


def pair_key(a: str, b: str) -> str:
    return "+".join(sorted((str(a), str(b))))


def in_range(d: date) -> bool:
    return RANGE_SINCE <= d <= RANGE_UNTIL


def key_of(path: PurePath, base: PurePath) -> str:
    """A file as a key: its path under `base` with forward slashes, whatever the machine's
    own separator. Every path the audit matches against the classing, skips by its
    prefix or prints into a finding's key goes through here, so that the keys and the
    known list are the same on Windows as elsewhere."""
    return path.relative_to(base).as_posix()


def name_of(file: Any) -> str:
    """A file's own name from a path written with either separator."""
    return PurePosixPath(str(file).replace("\\", "/")).name


def stem_of(file: Any) -> str:
    return PurePosixPath(name_of(file)).stem


def year_of(words: Any) -> int | None:
    """The first year a name or a line of words carries, or None."""
    m = YEAR.search(str(words or ""))
    return int(m.group(1)) if m else None


# ---------------------------------------------------------------------------
# Reading the tree
# ---------------------------------------------------------------------------


def read_yaml(path: Path) -> Any:
    """A data file read by libyaml where it is installed (the same documents, faster)."""
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)
    return yaml.load(path.read_text(encoding="utf-8"), Loader=loader)  # noqa: S506


@contextlib.contextmanager
def fast_yaml() -> Iterator[None]:
    """While the audit runs, the game's `yaml.safe_load` answered by libyaml's loader
    where it is installed: the same documents (the slow tier's test holds it), a world
    made in a third of the time. Put back on the way out."""
    fast = getattr(yaml, "CSafeLoader", None)
    if fast is None:
        yield
        return
    plain = yaml.safe_load

    def quick(stream: Any) -> Any:
        return yaml.load(stream, Loader=fast)  # noqa: S506

    yaml.safe_load = quick
    try:
        yield
    finally:
        yaml.safe_load = plain


@dataclass
class Tree:
    """The tree as the audit reads it: the game's own objects where it has a reader, the
    raw documents where the game keeps none of what is asked."""

    nations: Nations
    nations_doc: dict[str, Any]
    ports: dict[str, Any]  # id -> ports.Port, loaded with no day (its first rows)
    port_docs: dict[str, dict[str, Any]]
    business_doc: dict[str, Any]
    ship_docs: dict[str, dict[str, Any]]  # the file's name -> its document
    scenario_docs: dict[str, dict[str, Any]]
    chart: Any
    data: Path = DATA
    code: Path = CODE


def load_tree(
    ports: Iterable[str] | None = None,
    ships: Iterable[str] | None = None,
    scenarios: bool = True,
) -> Tree:
    """The tree read: whole, or for a test a few ports by their files' names, a few ship
    files, and no scenarios (a small tree reads in a second by any loader)."""
    wanted = None if ports is None else set(ports)
    port_files = [p for p in sorted(PORTS_DIR.glob("*.yaml")) if wanted is None or p.stem in wanted]
    ship_names = None if ships is None else set(ships)
    ship_files = [
        p for p in sorted(SHIPS_DIR.glob("*.yaml")) if ship_names is None or p.name in ship_names
    ]
    with fast_yaml():
        chart = load_chart(CHART_NAME)
        ports = {}
        for path in port_files:
            port = load_port(path, chart)
            ports[port.id] = port
        nations = load_nations()
    port_docs = {p.stem: read_yaml(p) or {} for p in port_files}
    port_docs = {str(d.get("id") or stem): d for stem, d in port_docs.items()}
    scenarios_read = {}
    for p in sorted(SCENARIOS_DIR.rglob("*.yaml")) if scenarios else []:
        doc = read_yaml(p)
        if isinstance(doc, dict):
            scenarios_read[key_of(p, SCENARIOS_DIR)] = doc
    return Tree(
        nations=nations,
        nations_doc=read_yaml(NATIONS_PATH) or {},
        ports=ports,
        port_docs=port_docs,
        business_doc=read_yaml(BUSINESS_PATH) or {},
        ship_docs={p.name: read_yaml(p) or {} for p in ship_files},
        scenario_docs=scenarios_read,
        chart=chart,
    )


@dataclass
class Reference:
    """`tools/range/reference.yaml`: the wars and the nations' lifetimes, FROM MEMORY."""

    wars: list[dict[str, Any]]
    lifetimes: list[dict[str, Any]]
    peaces: list[dict[str, Any]]

    def at_war(self, a: str, b: str, day: date) -> bool:
        pair = {str(a), str(b)}
        return any(set(w["between"]) == pair and _holds(w, day) for w in self.wars)

    def pairs(self) -> set[frozenset[str]]:
        return {frozenset(w["between"]) for w in self.wars}

    def exists(self, nation: str, day: date) -> bool:
        rows = [r for r in self.lifetimes if r["nation"] == nation]
        return not rows or any(_holds(r, day) for r in rows)

    def dates(self) -> list[date]:
        out = []
        for row in [*self.wars, *self.lifetimes, *self.peaces]:
            if row.get("since"):
                out += [row["since"] - timedelta(days=1), row["since"]]
            if row.get("until"):
                out += [row["until"], row["until"] + timedelta(days=1)]
        return sorted({d for d in out if in_range(d)})


def _holds(row: dict[str, Any], day: date) -> bool:
    """Whether a row's `since` and `until` hold the day, both counted in."""
    since, until = row.get("since"), row.get("until")
    return not (since and day < since) and not (until and day > until)


def load_reference(path: Path = REFERENCE_PATH) -> Reference:
    doc = read_yaml(path) or {}
    return Reference(
        wars=[dict(w, between=[str(x) for x in w["between"]]) for w in doc.get("wars") or []],
        lifetimes=[dict(r) for r in doc.get("lifetimes") or []],
        peaces=[dict(r) for r in doc.get("peaces") or []],
    )


# ---------------------------------------------------------------------------
# The days
# ---------------------------------------------------------------------------


def _either_side(row: dict[str, Any], since: str = "since", until: str = "until") -> list[date]:
    out = []
    for key, before in ((since, True), (until, False)):
        d = row.get(key)
        if isinstance(d, datetime):
            d = d.date()
        if isinstance(d, str):
            try:
                d = date.fromisoformat(d)
            except ValueError:
                d = None
        if isinstance(d, date):
            out += [d - timedelta(days=1), d] if before else [d, d + timedelta(days=1)]
    return out


def _year_edges(dates: str) -> list[date]:
    """The days either side of each year a 'YYYY-YYYY' form names: the last of the year
    before and the first of it for a beginning, the last of it and the first of the next
    for an end."""
    out = []
    for part in str(dates or "").split(","):
        lo, sep, hi = part.strip().partition("-")
        if lo.strip().isdigit():
            out += [date(int(lo) - 1, 12, 31), date(int(lo), 1, 1)]
        end = hi.strip() if sep else lo.strip()
        if end.isdigit():
            out += [date(int(end), 12, 31), date(int(end) + 1, 1, 1)]
    return out


def flag_roots() -> list[str]:
    return sorted(p.name for p in SIGNALS_DIR.iterdir() if p.is_dir())


def named_days(tree: Tree, full: bool = False) -> list[date]:
    """The days either side of every date the data itself names, within the range."""
    out: list[date] = []
    for port in tree.ports.values():
        for row in port.nations:
            out += _either_side(row)
        for _key, rows in port.dated:
            for row in rows:
                out += _either_side(row)
    as_of = tree.nations.as_of
    if as_of:
        out += [as_of - timedelta(days=1), as_of, as_of + timedelta(days=1)]
    for war in tree.nations.wars:
        out += _either_side(war)
    for nation in tree.nations.nations.values():
        for entry in nation.naval.get("blockades") or []:
            if isinstance(entry, dict):
                out += _either_side(entry)
    for scheme in tree.business_doc.get("prize_shares") or []:
        out += _either_side(scheme, "from", "until")
        if isinstance(scheme.get("until"), date):
            out.append(scheme["until"] - timedelta(days=1))
    for root in flag_roots():
        for row in F.load_signal_flags(root).rows:
            out += _year_edges(row.dates)
        colours = _colours(root)
        if colours is not None:
            for flag in _all_flags(colours):
                out += _year_edges(flag.dates)
        for fashion in _fashions(root):
            out += _year_edges(fashion.dates)
        for day in F.load_days(root):
            for edge in _year_edges(day.years):
                # the day itself in the year of the edge, and the day after
                kept = date(edge.year, day.month, day.day)
                out += [kept, kept + timedelta(days=1)]
            if full:
                for year in range(RANGE_SINCE.year, RANGE_UNTIL.year + 1):
                    kept = date(year, day.month, day.day)
                    out += [kept, kept + timedelta(days=1)]
    for f in tree.chart.features.values():
        if f.kind == "light" and f.lit:
            for key, before in (("from", True), ("until", False)):
                y = f.lit.get(key)
                if y is None:
                    continue
                out += (
                    [date(int(y) - 1, 12, 31), date(int(y), 1, 1)]
                    if before
                    else [date(int(y), 12, 31), date(int(y) + 1, 1, 1)]
                )
    return sorted({d for d in out if in_range(d)})


def yearly_days() -> list[date]:
    return [date(y, *YEAR_DAY) for y in range(RANGE_SINCE.year, RANGE_UNTIL.year + 1)]


def sample_days(tree: Tree, full: bool = False) -> list[date]:
    return sorted(set(yearly_days()) | set(named_days(tree, full)))


def world_days(full: bool = False) -> list[tuple[date, str]]:
    if not full:
        return list(SAMPLED_WORLDS)
    out = list(SAMPLED_WORLDS)
    for i, day in enumerate(yearly_days()):
        out += [(day, s) for s in FULL_STATIONS_EVERY_YEAR]
        if i % FULL_SOME_YEARS_STEP == 0:
            out += [(day, s) for s in FULL_STATIONS_SOME_YEARS]
    seen: set[tuple[date, str]] = set()
    return [x for x in out if not (x in seen or seen.add(x))]


# ---------------------------------------------------------------------------
# The cheap road: a day through the game's own readers
# ---------------------------------------------------------------------------


def port_on(port: Any, day: date) -> Any:
    """The port as a scenario begun on the day finds it: a copy with each dated key's row
    of the day in its field and the day's holder (`Port.on_day`, `Port.nation_on`; the
    same as `load_port(path, chart, None, day)`, which the test holds)."""
    p = copy.copy(port)
    p.on_day(day)
    p.nation = port.nation_on(day)
    return p


def table_at_war(tree: Tree, a: str, b: str) -> bool:
    return tree.nations.at_war(a, b)


def court_at_war(tree: Tree, a: str, b: str, day: date) -> bool:
    """The prize court's reading of the same pair on the day (`prize_court._at_war_at`,
    for a taking at this very tick)."""
    when = datetime(day.year, day.month, day.day, 12)
    world = SimpleNamespace(clock=SimpleNamespace(ship_time=when, tick=0))
    return bool(PC._at_war_at(tree.nations, a, b, 0, world))


def blockades_on(tree: Tree, day: date, ports: dict[str, Any] | None = None) -> set[tuple]:
    """The blockades the business would draw for a scenario begun on the day, by its own
    rule (`business._blockades`): the nation's entry, the port's holder of the day at war
    with her by the table, the day within the entry's dates. (nation, port, index)."""
    out = set()
    for nid in sorted(tree.nations.nations):
        entries = tree.nations.nations[nid].naval.get("blockades") or []
        for i, item in enumerate(entries):
            entry = dict(item) if isinstance(item, dict) else {"port": item}
            pid = str(entry.get("port"))
            port = (ports or tree.ports).get(pid)
            if port is None:
                continue
            holder = port.nation if ports is not None else port_on(port, day).nation
            if not tree.nations.at_war(nid, str(holder)):
                continue
            if not B._between(day, entry):
                continue
            out.add((nid, pid, i))
    return out


# ---------------------------------------------------------------------------
# (p) the ports
# ---------------------------------------------------------------------------


def check_ports(audit: Audit, tree: Tree, days: list[date], ref: Reference | None) -> None:
    table = tree.nations.nations
    # the keys no file dates: a single value read as true on every day of the range
    for key in ("nation", *DATED_KEYS):
        single = sorted(
            pid for pid, doc in tree.port_docs.items() if not _is_rows(doc.get(key), key)
        )
        if single:
            audit.add(
                "p",
                f"p-undated:{key}",
                f"`{key}` is one value in these ports' files, read as true on every day of "
                "the range",
                days,
                count=len(single),
                worst=single[:6],
            )
    for pid, port in tree.ports.items():
        doc = tree.port_docs.get(pid) or {}
        since_words = str((doc.get("blockade") or {}).get("since") or "")
        if doc.get("state") == "blockaded" and since_words and _as_day(since_words) is None:
            audit.add(
                "p",
                f"p-blockade-words:{pid}",
                f"the port's own blockade gives its beginning in words, not a day "
                f"('{since_words[:40]}')",
                days,
            )
        for day in days:
            p = port_on(port, day)
            if str(p.nation) not in table:
                audit.add("p", f"p-holder-unknown:{pid}", f"held by '{p.nation}', no nation", day)
                continue
            if ref is not None and not ref.exists(str(p.nation), day):
                audit.add(
                    "r",
                    f"r-holder:{pid}",
                    f"held by {p.nation}, which the reference has not in being on the day",
                    day,
                    basis=REFERENCE,
                )
            by = p.blockaded_by
            if not by:
                continue
            first = year_of((p.blockade or {}).get("since"))
            if first is not None and day.year < first:
                audit.add(
                    "p",
                    f"p-blockade-before:{pid}",
                    f"blockaded by {by} on days before the year its own `since` names ({first})",
                    day,
                )
            if not tree.nations.at_war(by, str(p.nation)):
                audit.add(
                    "p",
                    f"p-blockade-no-war:{pid}",
                    f"blockaded by {by}, whom the table has not at war with {p.nation}",
                    day,
                )
            if ref is not None and not ref.at_war(by, str(p.nation), day):
                audit.add(
                    "r",
                    f"r-port-blockade:{pid}",
                    f"blockaded by {by}, whom the reference has at peace with {p.nation}",
                    day,
                    basis=REFERENCE,
                )


def _is_rows(raw: Any, key: str) -> bool:
    """Whether a port file gives a key as rows (a list of mappings, each naming the key),
    as `ports._is_rows` reads it."""
    return (
        isinstance(raw, list) and bool(raw) and all(isinstance(r, dict) and key in r for r in raw)
    )


def _as_day(words: Any) -> date | None:
    if isinstance(words, datetime):
        return words.date()
    if isinstance(words, date):
        return words
    try:
        return date.fromisoformat(str(words).strip())
    except ValueError:
        return None


# ---------------------------------------------------------------------------
# (w) the wars
# ---------------------------------------------------------------------------


def check_wars(audit: Audit, tree: Tree, days: list[date], ref: Reference | None) -> None:
    nations = tree.nations
    seen: set[frozenset[str]] = set()
    for war in nations.wars:
        a, b = war["between"]
        pair = frozenset((a, b))
        key = pair_key(a, b)
        if pair in seen:
            audit.add("w", f"w-twice:{key}", "the pair is at war twice in the table", days)
        seen.add(pair)
        if nations.allied(a, b):
            audit.add("w", f"w-allied:{key}", "at war and allied at once", days)
        since = _as_day(war.get("since"))
        if since is not None:
            early = [d for d in days if d < since]
            if early:
                audit.add(
                    "w",
                    f"w-before-since:{key}",
                    f"the war is in force on days before its own beginning ({since})",
                    early,
                )
            split = [d for d in days if nations.at_war(a, b) != court_at_war(tree, a, b, d)]
            if split:
                audit.add(
                    "w",
                    f"w-court:{key}",
                    "at war by the stance and at peace before the prize court on the same "
                    "day (the court reads the war's `since`, the stance does not)",
                    split,
                )
    if nations.wars:
        audit.add(
            "w",
            "w-no-end",
            "no war of the table has an end and the table holds no peace: each is in force "
            "on every day",
            days,
            count=len(nations.wars),
            worst=[pair_key(*w["between"]) for w in nations.wars],
        )
    # what the nations' `relations` say in words, against the table
    said = _relations_at_war(tree.nations_doc)
    for pair in sorted(said, key=sorted):
        a, b = sorted(pair)
        if not nations.at_war(a, b):
            audit.add(
                "w",
                f"w-relations:{pair_key(a, b)}",
                "the nation's `relations` say war in words and the table has none (the "
                "words are read by nothing)",
                days,
                worst=[said[pair][:70]],
            )
    if ref is None:
        return
    ids = sorted(nations.nations)
    for day in days:
        for nid in ids:
            if not ref.exists(nid, day):
                audit.add(
                    "r",
                    f"r-nation:{nid}",
                    "stands in the table, at peace or at war, on days the reference has "
                    "it not in being",
                    day,
                    basis=REFERENCE,
                )
        for pair in sorted(seen | ref.pairs(), key=sorted):
            a, b = sorted(pair)
            if a not in nations.nations or b not in nations.nations:
                continue
            ours, theirs = nations.at_war(a, b), ref.at_war(a, b, day)
            if ours and not theirs:
                audit.add(
                    "r",
                    f"r-war-at-peace:{pair_key(a, b)}",
                    "at war in the table on days the reference has them at peace",
                    day,
                    basis=REFERENCE,
                )
            elif theirs and not ours:
                audit.add(
                    "r",
                    f"r-war-absent:{pair_key(a, b)}",
                    "at peace in the table on days the reference has them at war",
                    day,
                    basis=REFERENCE,
                )


def _relations_at_war(doc: dict[str, Any]) -> dict[frozenset[str], str]:
    """The pairs a nation's `relations` give as at war, by their words (JUDGEMENT: the
    entry begins 'war' or speaks of a 'standing war'; 'as X's' takes X's entry)."""
    out: dict[frozenset[str], str] = {}
    for nid, entry in (doc.get("nations") or {}).items():
        relations = (entry or {}).get("relations") or {}
        for other, words in relations.items():
            text = str(words)
            m = re.match(r"as (\w[\w-]*)'", text.strip())
            if m:
                text = str(relations.get(m.group(1).lower(), text))
            low = text.strip().lower()
            if low.startswith("war") or "standing war" in low:
                out[frozenset((str(nid), str(other)))] = text
    return out


# ---------------------------------------------------------------------------
# (b) the blockades
# ---------------------------------------------------------------------------


def check_blockades(audit: Audit, tree: Tree, days: list[date], ref: Reference | None) -> None:
    for nid in sorted(tree.nations.nations):
        entries = tree.nations.nations[nid].naval.get("blockades") or []
        for item in entries:
            entry = dict(item) if isinstance(item, dict) else {"port": item}
            pid = str(entry.get("port"))
            if pid not in tree.ports:
                audit.add("b", f"b-no-port:{nid}:{pid}", "a blockade of a port with no file", days)
                continue
            if not entry.get("since") and not entry.get("until"):
                audit.add(
                    "b",
                    f"b-undated:{nid}:{pid}",
                    "the blockade carries no dates: drawn on every day the table has the two "
                    "at war",
                    days,
                )
    for day in days:
        for nid, pid, _i in sorted(blockades_on(tree, day)):
            holder = str(port_on(tree.ports[pid], day).nation)
            if ref is not None and not ref.at_war(nid, holder, day):
                audit.add(
                    "r",
                    f"r-blockade:{nid}:{pid}",
                    f"drawn on days the reference has {nid} at peace with the port's holder",
                    day,
                    basis=REFERENCE,
                    worst=[holder],
                )


# ---------------------------------------------------------------------------
# (v) the vessels and their fits
# ---------------------------------------------------------------------------


def default_fit(tree: Tree, ship_file: str) -> str:
    doc = tree.ship_docs.get(name_of(ship_file)) or {}
    return str((doc.get("armament") or {}).get("default") or "")


def fit_of_description(tree: Tree, kind: str) -> tuple[str, str]:
    """(the ship file's name, the fit a far ship of the description carries): the file's
    own `ship.descriptions.<kind>.fit`, else its default, as `ships.description` and
    `ships.vessel_from_spec` have it."""
    file = name_of(SH.DESCRIPTIONS[kind]["file"])
    doc = tree.ship_docs.get(file) or {}
    own = ((doc.get("ship") or {}).get("descriptions") or {}).get(kind) or {}
    return file, str(own.get("fit") or default_fit(tree, file))


def business_kinds(tree: Tree) -> set[str]:
    """The descriptions the business's own tables name (the trade's and the fishermen's
    kinds; the frigate and the brig-sloop of the blockade and the convoy)."""
    out = {"frigate", "brig-sloop"}
    for table in ("trader_kinds", "fisher_kinds"):
        for kinds in (tree.business_doc.get(table) or {}).values():
            out.update(str(k) for k in kinds or [])
    return out


def check_vessels(audit: Audit, tree: Tree, days: list[date]) -> None:
    drawn = business_kinds(tree)
    for kind in sorted(SH.DESCRIPTIONS):
        file, fit = fit_of_description(tree, kind)
        year = year_of(fit)
        if year is None:
            continue
        early = [d for d in days if d.year < year]
        if early:
            who = "the business draws her" if kind in drawn else "a scenario may name her"
            audit.add(
                "v",
                f"v-fit-ahead:{stem_of(file)}:{fit}",
                f"a {kind} sails the fit '{fit}' on days before {year} ({who})",
                early,
                worst=[kind],
            )
    for name, doc in sorted(tree.scenario_docs.items()):
        start = doc.get("start")
        if isinstance(start, str):
            with contextlib.suppress(ValueError):
                start = datetime.fromisoformat(start)
        if not isinstance(start, date):
            continue
        day = start.date() if isinstance(start, datetime) else start
        ahead = []
        ship = doc.get("ship")
        if isinstance(ship, dict) and ship.get("file"):
            fit = str(ship.get("fit") or default_fit(tree, str(ship["file"])))
            if (year_of(fit) or 0) > day.year:
                ahead.append(f"her own ship, '{fit}'")
        for v in doc.get("ships") or []:
            if not isinstance(v, dict):
                continue
            kind = SH._DESCRIPTION_WORDS.get(str(v.get("description") or "").lower().strip())
            if kind is None:
                continue
            fit = str(v.get("fit") or fit_of_description(tree, kind)[1])
            if (year_of(fit) or 0) > day.year:
                ahead.append(f"{v.get('name') or kind}, '{fit}'")
        if ahead:
            audit.add(
                "v",
                f"v-scenario:{PurePosixPath(name).with_suffix('').as_posix()}",
                f"the scenario begins in {day.year} and sails a fit of a later year",
                [day] if in_range(day) else [],
                count=len(ahead),
                worst=ahead,
            )


# ---------------------------------------------------------------------------
# (f) the flags, (d) the days
# ---------------------------------------------------------------------------


def _colours(root: str) -> Any:
    try:
        return F.load_colours(root)
    except F.BookFileError:
        return None


def _all_flags(colours: Any) -> list[Any]:
    out = list(colours.flags.values())
    for block in colours.nations.values():
        out += list(block.flags.values())
    return out


def _fashions(root: str) -> tuple[Any, ...]:
    try:
        return tuple(F.load_dressing(root))
    except (F.BookFileError, FileNotFoundError):
        return ()


def dates_hold(dates: str, year: int) -> bool:
    """Whether a `dates` form holds the year, read span by span ('-1806, 1815-' is two):
    the audit's own reading, wider than the engine's `_in_dates`, which reads one span."""
    text = str(dates or "").strip()
    if not text:
        return True
    for part in text.split(","):
        lo, sep, hi = part.strip().partition("-")
        lo, hi = lo.strip(), hi.strip()
        if not sep:
            if lo.isdigit() and int(lo) == year:
                return True
            continue
        if (not lo or year >= int(lo)) and (not hi or year <= int(hi)):
            return True
    return False


def engine_reads(dates: str) -> bool:
    """Whether the engine's own reader of a `dates` form (`flags._in_dates`) reads it."""
    try:
        F._in_dates(dates, 1805)
    except ValueError:
        return False
    return True


def check_flags(audit: Audit, tree: Tree, days: list[date]) -> None:
    years = sorted({d.year for d in days})
    by_year: dict[int, list[date]] = defaultdict(list)
    for d in days:
        by_year[d.year].append(d)
    for nid in sorted(tree.nations.nations):
        colours = F.file_for_nation(tree.nations, nid)
        worn = {name for occ in colours.occasions for name, _where in occ.flags}
        out_of: dict[str, list[date]] = defaultdict(list)
        for name, flag in colours.flags.items():
            if not engine_reads(flag.dates):
                audit.add(
                    "f",
                    f"f-dates-form:{nid}:{name}",
                    f"the flag's dates '{flag.dates}' are in a form the engine's reader of "
                    "dates cannot read",
                    days,
                )
            if worn and name not in worn:
                continue
            for year in years:
                if not dates_hold(flag.dates, year):
                    out_of[name] += by_year[year]
        if out_of:
            audit.add(
                "f",
                f"f-colours:{nid}",
                "she wears colours whose own dates do not hold the day's year (the colours' "
                "dates are read by nothing)",
                {d for ds in out_of.values() for d in ds},
                count=len(out_of),
                worst=sorted(out_of),
            )
    for root in flag_roots():
        rows = F.load_signal_flags(root).rows
        names = sorted({r.name for r in rows})
        nearest: dict[str, list[date]] = defaultdict(list)
        for name in names:
            mine = [r for r in rows if r.name == name]
            for year in years:
                if not any(r.flown_in(year) for r in mine):
                    nearest[name] += by_year[year]
        if nearest:
            audit.add(
                "f",
                f"f-signal-nearest:{root}",
                "signal flags with no drawing for the day's year, served the nearest year's",
                {d for ds in nearest.values() for d in ds},
                count=len(nearest),
                worst=sorted(nearest)[:6],
            )
        fashions = _fashions(root)
        if fashions:
            off = [
                d
                for year in years
                if not any(dates_hold(f.dates, year) for f in fashions)
                for d in by_year[year]
            ]
            if off:
                audit.add(
                    "f",
                    f"f-fashion:{root}",
                    "no dressing fashion holds the day's year, the nearest served",
                    off,
                )


def check_days(audit: Audit, tree: Tree, days: list[date]) -> None:
    none = sorted(nid for nid, n in tree.nations.nations.items() if not F.load_days(n.signals_root))
    if none:
        audit.add(
            "d",
            "d-none",
            "nations whose ships dress on no day of the year (no days file)",
            days,
            count=len(none),
            worst=none[:8],
        )
    years = sorted({d.year for d in days})
    for root in flag_roots():
        kept = F.load_days(root)
        if not kept:
            continue
        bare = [y for y in years if not any(F._in_dates(k.years, y) for k in kept)]
        if bare:
            audit.add(
                "d",
                f"d-gap:{root}",
                "years in which the root keeps no day at all",
                [d for d in days if d.year in bare],
            )


# ---------------------------------------------------------------------------
# (l) the lights
# ---------------------------------------------------------------------------


def check_lights(audit: Audit, tree: Tree, days: list[date]) -> None:
    within = []
    hit: set[date] = set()
    for f in tree.chart.features.values():
        if f.kind != "light" or not f.lit:
            continue
        for key in ("from", "until"):
            y = f.lit.get(key)
            if y is not None and RANGE_SINCE.year <= int(y) <= RANGE_UNTIL.year:
                within.append(f.id)
                hit.update(d for d in days if d.year == int(y))
    lights = [f for f in tree.chart.features.values() if f.kind == "light" and f.lit]
    by_year = {
        y: sum(1 for f in lights if f.lit_in(y)) for y in (RANGE_SINCE.year, 1805, RANGE_UNTIL.year)
    }
    audit.info.append(
        "the lights lit: "
        + ", ".join(f"{n} in {y}" for y, n in sorted(by_year.items()))
        + f" (of {len(lights)} with years)"
    )
    if within:
        audit.add(
            "l",
            "l-by-year",
            "lights first lit or put out within the range are dated by the year alone: lit "
            "from its first day, dark from the day after its last",
            hit,
            count=len(set(within)),
            worst=sorted(set(within))[:6],
        )


# ---------------------------------------------------------------------------
# (x) the words
# ---------------------------------------------------------------------------


def check_words(audit: Audit, tree: Tree, days: list[date], scan: list[tuple]) -> None:
    as_of = tree.nations.as_of
    if as_of is not None:
        stamp = f"{as_of.day} {as_of:%B %Y}"
        off = [d for d in days if d < as_of or d.year > as_of.year]
        if off and stamp in tree.nations.sailed_with_words():
            audit.add(
                "x",
                "x-as-of",
                f"the table she sailed with is served as of {stamp} on a day before it or "
                "in a later year",
                off,
            )
    served = [r for r in CLASSING if r.kind == SERVED and r.id != "nations-as-of"]
    for row in served:
        ahead: dict[date, int] = defaultdict(int)
        some = []
        for rel, path, value in scan:
            if not row_holds(row, rel, path):
                continue
            named = [int(y) for y in YEAR.findall(str(value))]
            named = [y for y in named if y > RANGE_SINCE.year]
            if not named:
                continue
            latest = max(named)
            before = [d for d in days if d.year < latest]
            if before:
                some.append(f"{rel}: {path} ({latest})")
                for d in before:
                    ahead[d] += 1
        if some:
            audit.add(
                "x",
                f"x-words:{row.id}",
                "served words that name a year yet to come on the day (a work of 1806 cited "
                "in 1805, a flag of 1820 described in 1792)",
                set(ahead),
                count=len(some),
                worst=some[:5],
            )


# ---------------------------------------------------------------------------
# (e) the engine's own years
# ---------------------------------------------------------------------------


def engine_years(code: Path = CODE) -> dict[str, list[str]]:
    """A year or a date fixed in the code, by file: a `date(` or `datetime(` call with a
    year of 1700 to 1899 written in it, and a year so written given to a name with 'year'
    in it. A seed that happens to be 1805 is no date and is not found."""
    out: dict[str, list[str]] = defaultdict(list)
    for path in sorted(code.rglob("*.py")):
        try:
            tree = ast.parse(path.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        rel = key_of(path, code.parent)
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                name = getattr(node.func, "id", getattr(node.func, "attr", ""))
                first = node.args[0] if node.args else None
                if (
                    name in ("date", "datetime")
                    and isinstance(first, ast.Constant)
                    and isinstance(first.value, int)
                    and 1700 <= first.value <= 1899
                ):
                    out[rel].append(f"line {node.lineno}: {name}({first.value}, ...)")
            elif isinstance(node, ast.Assign | ast.AnnAssign):
                value = node.value
                targets = node.targets if isinstance(node, ast.Assign) else [node.target]
                names = [getattr(t, "id", getattr(t, "attr", "")) for t in targets]
                if (
                    isinstance(value, ast.Constant)
                    and isinstance(value.value, int)
                    and not isinstance(value.value, bool)
                    and 1700 <= value.value <= 1899
                    and any("year" in str(n).lower() for n in names)
                ):
                    out[rel].append(f"line {node.lineno}: {names[0]} = {value.value}")
    return dict(out)


def check_engine(audit: Audit, tree: Tree, days: list[date]) -> None:
    for rel, lines in sorted(engine_years(tree.code).items()):
        audit.add(
            "e",
            f"e-year:{rel}",
            "a year or a date fixed in the code",
            days,
            count=len(lines),
            worst=lines,
        )


# ---------------------------------------------------------------------------
# (u) what no data dates at all
# ---------------------------------------------------------------------------


def check_undated(audit: Audit, tree: Tree, days: list[date]) -> None:
    nations = tree.nations.nations
    doc = tree.nations_doc.get("nations") or {}

    def one(key: str, words: str, things: list[str]) -> None:
        if things:
            audit.add("u", key, words, days, count=len(things), worst=things[:6])

    one(
        "u-nations",
        "no nation of the table carries the days it was in being",
        sorted(nations),
    )
    one(
        "u-letters",
        "who issues letters of marque is one value for each nation, war or peace",
        sorted(n for n, d in doc.items() if "letters_of_marque" in (d or {})),
    )
    one(
        "u-colours-words",
        "the words of a nation's colours and flag are one value for each nation",
        sorted(n for n, d in doc.items() if (d or {}).get("colours") or (d or {}).get("flag")),
    )
    one(
        "u-ships",
        "no ship file dates as data when her class was afloat, or when she was so fitted "
        "and so armed: the years stand only in fits' names and in words",
        sorted(tree.ship_docs),
    )
    roots = flag_roots()
    one(
        "u-books",
        "no signal book carries the days it was in force",
        sorted(f"{r}/{b}" for r in roots for b in BOOK_FILES if (SIGNALS_DIR / r / b).exists()),
    )
    one(
        "u-private",
        "the private signals' form carries no days in force (the tables themselves are "
        "made by the running year and month)",
        sorted(f"{r}/private.yaml" for r in roots if (SIGNALS_DIR / r / "private.yaml").exists()),
    )
    one(
        "u-regulations",
        "the files that state a regulation, an instruction or a custom carry no days in force",
        sorted(f for f in REGULATION_FILES if (tree.data / f).exists()),
    )
    business = tree.business_doc
    one(
        "u-names",
        "the names the business gives its ships are one list for each nation",
        sorted(f"{t}.{n}" for t in ("names", "cruiser_names") for n in (business.get(t) or {})),
    )
    one(
        "u-trade",
        "who trades, in what, as a neutral or not, and at what price is one value for the range",
        sorted(
            k
            for k in ("trader_kinds", "fisher_kinds", "neutrals", "cargo_tons", "prize_values")
            if k in business
        ),
    )
    schemes = {str(s.get("nation")) for s in business.get("prize_shares") or []}
    one(
        "u-prize-shares",
        "nations with no prize scheme of their own, given Britain's by the day",
        sorted(n for n in nations if n not in schemes),
    )


# ---------------------------------------------------------------------------
# (c) the classing
# ---------------------------------------------------------------------------

# Under data/, what the scan leaves alone: the chart's tiles and coast (no words).
SCAN_SKIP = ("charts/tiles/", "charts/coast/")


def scan_dated(data: Path = DATA, unparsed: list[str] | None = None) -> list[tuple[str, str, Any]]:
    """Every key of the data that carries a year or a date: (the file under data/, the
    key's path with a list's items as `#`, the value). A date or a datetime always; words
    that name a year; a whole number of 1500 to 1999 under a key whose name is a date's
    (`DATE_NAMES`); and a key whose own name carries a year (a fit's). A file that will
    not parse is named in `unparsed` and is a finding of its own (`c-unparsed`)."""
    out: list[tuple[str, str, Any]] = []

    def walk(value: Any, path: tuple[str, ...], rel: str) -> None:
        if isinstance(value, dict):
            for k, v in value.items():
                name = str(k)
                if YEAR.search(name) and not name.isdigit():
                    out.append((rel, ".".join((*path, "*")), name))
                    walk(v, (*path, "*"), rel)
                else:
                    walk(v, (*path, name), rel)
            return
        if isinstance(value, list):
            for v in value:
                walk(v, (*path, "#"), rel)
            return
        last = next((p for p in reversed(path) if p != "#"), "")
        hit = isinstance(value, date)
        if isinstance(value, str):
            hit = bool(YEAR.search(value))
        elif isinstance(value, int) and not isinstance(value, bool):
            hit = last in DATE_NAMES and 1500 <= value <= 1999
        if hit:
            out.append((rel, ".".join(path), value))

    for path in sorted(data.rglob("*.yaml")):
        rel = key_of(path, data)
        if rel.startswith(SCAN_SKIP):
            continue
        try:
            doc = read_yaml(path)
        except yaml.YAMLError:
            if unparsed is not None:
                unparsed.append(rel)
            continue
        walk(doc, (), rel)
    return out


def row_holds(row: Row, rel: str, path: str) -> bool:
    return any(fnmatch.fnmatchcase(rel, f) for f in row.files.split("|")) and any(
        fnmatch.fnmatchcase(path, p) for p in row.paths
    )


def row_of(rel: str, path: str) -> Row | None:
    """The classing's row for a key: the first that holds it."""
    for row in CLASSING:
        if row_holds(row, rel, path):
            return row
    return None


def check_classing(
    audit: Audit, tree: Tree, days: list[date], scan: list[tuple], unparsed: Iterable[str] = ()
) -> None:
    for rel in sorted(unparsed):
        audit.add(
            "c",
            f"c-unparsed:{rel}",
            "a data file that will not parse: its keys are not scanned and not classed",
            days,
        )
    used: dict[str, int] = defaultdict(int)
    unclassed: dict[tuple[str, str], int] = defaultdict(int)
    for rel, path, _value in scan:
        row = row_of(rel, path)
        if row is None:
            unclassed[(_file_kind(rel), path)] += 1
        else:
            used[row.id] += 1
    for (kind, path), n in sorted(unclassed.items()):
        audit.add(
            "c",
            f"c-unclassed:{kind}:{path}",
            "a key of the data that carries a year or a date and is in no row of the classing",
            days,
            count=n,
        )
    for row in CLASSING:
        if not used.get(row.id):
            if row.optional:
                continue
            audit.add("c", f"c-dead-row:{row.id}", "a row of the classing that holds no key", days)
            continue
        if row.kind in (CALENDAR, BOTH) and row.play:
            audit.add(
                "c",
                f"c-snap-back:{row.id}",
                f"{row.kind}: {row.play}",
                days,
                count=used[row.id],
            )
        if row.kind == UNREAD:
            audit.add(
                "c",
                f"c-unread:{row.id}",
                f"the data carries it and the game reads it not: {row.reader}",
                days,
                count=used[row.id],
            )
    audit.info.append(
        f"the classing: {len(scan)} dated values in {len(used)} rows of {len(CLASSING)}"
    )


def _file_kind(rel: str) -> str:
    """A file's kind for a key: its directory, or its own name at the top."""
    parent = PurePosixPath(rel).parent.as_posix()
    return rel if parent == "." else parent


def classing_table() -> str:
    """The classing as the document's table (`docs/dev/RangeAudit.md`)."""
    lines = [
        "| Row | Files (under data/) | Keys | Class | How it is read | What play could "
        "change that the clock would put back |",
        "|---|---|---|---|---|---|",
    ]
    for row in CLASSING:
        keys = ", ".join(f"`{p}`" for p in row.paths[:6]) + (" ..." if len(row.paths) > 6 else "")
        files = row.files.replace("|", ", ")
        lines.append(
            f"| {row.id} | `{files}` | {keys} | {row.kind} | {row.reader} | {row.play or '-'} |"
        )
    return "\n".join(lines)


# ---------------------------------------------------------------------------
# The dear road: whole worlds
# ---------------------------------------------------------------------------


def make_world(day: date, station: str, nations_block: dict[str, Any] | None = None) -> Any:
    """A rules-only world begun on the day at a station, the business on, the whole chart."""
    from freesail.api.session import make_world as session_world
    from freesail.core.world import Scenario

    lat, lon = STATIONS[station]
    sc = Scenario()
    sc.name = f"the range's audit, {station}, {day}"
    sc.start_time = datetime(day.year, day.month, day.day, 8)
    sc.position = {"lat_deg": lat, "lon_deg": lon}
    sc.chart = CHART_NAME
    sc.nation = WORLD_NATION
    sc.business = "on"
    if nations_block is not None:
        sc.nations = nations_block
    return session_world(WORLD_SEED, WORLD_SHIP, sc)


def _vessels(world: Any) -> list[Any]:
    held = world.vessels.vessels
    return list(held.values()) if isinstance(held, dict) else list(held)


def _sets(world: Any) -> list[Any]:
    held = world.squadrons.sets
    return list(held.values()) if isinstance(held, dict) else list(held)


def check_world(
    audit: Audit, tree: Tree, day: date, station: str, ref: Reference | None, world: Any = None
) -> None:
    # the day's world carries a scenario's own table of no war at all: if the World read
    # the block, it would be at peace with all
    block = {"as_of": day.isoformat(), "wars": [], "letters_of_marque": [], "source": "the audit"}
    world = world if world is not None else make_world(day, station, block)
    where = f"{station} {day}"
    table = {frozenset(w["between"]) for w in tree.nations.wars}
    wars = {frozenset(w["between"]) for w in world.nations.wars}
    if getattr(world.scenario, "nations", None) is not None and not world.scenario.nations["wars"]:
        if wars:
            audit.add(
                "w",
                "w-block-unread",
                "a scenario's own `nations:` block of no war is kept and the world is at "
                "the table's wars all the same",
                day,
                worst=[where],
            )
        elif table:
            return  # the block is read: this world is the scenario's, not the table's
    # (a) the two roads agree
    if wars != table:
        audit.add("a", "a-wars", "the world's wars are not the table's", day, worst=[where])
    cheap = {pid: port_on(p, day) for pid, p in tree.ports.items()}
    for pid, port in world.ports.ports.items():
        mine = cheap.get(pid)
        if mine is None or str(port.nation) != str(mine.nation):
            audit.add(
                "a",
                f"a-holder:{pid}",
                "the world's holder is not the readers' road's",
                day,
                worst=[f"{where}: {port.nation} and {getattr(mine, 'nation', None)}"],
            )
        elif (port.state, port.blockaded_by) != (mine.state, mine.blockaded_by):
            audit.add(
                "a",
                f"a-state:{pid}",
                "the world's state of the port is not the readers' road's",
                day,
                worst=[where],
            )
    inside = {
        pid
        for pid, port in world.ports.ports.items()
        if world.business.inside(port.outer_road.position)
    }
    expected = {pid for _n, pid, _i in blockades_on(tree, day) if pid in inside}
    drawn = {
        str(s.id).removeprefix("blockade-")
        for s in _sets(world)
        if str(getattr(s, "regime", "")) == "on blockade"
    }
    for pid in sorted(expected ^ drawn):
        audit.add(
            "a",
            f"a-blockade:{pid}",
            "the world's blockade and the readers' road's differ",
            day,
            worst=[f"{where}: {'drawn' if pid in drawn else 'not drawn'}"],
        )
    # the vessels the world draws
    for v in _vessels(world):
        nid = str(getattr(v, "nation", "") or "")
        if nid and nid not in tree.nations.nations:
            audit.add("v", f"v-nation-unknown:{nid}", "a vessel of no nation", day)
        elif nid and ref is not None and not ref.exists(nid, day):
            audit.add(
                "r",
                f"r-vessel:{nid}",
                "a vessel drawn under a nation the reference has not in being on the day",
                day,
                basis=REFERENCE,
                worst=[where],
            )
        file = name_of(getattr(v, "ship_file", "") or "")
        fit = str(getattr(v, "fit", "") or default_fit(tree, file))
        year = year_of(fit)
        if year is not None and day.year < year:
            audit.add(
                "v",
                f"v-fit-ahead:{stem_of(file)}:{fit}",
                f"a vessel sails the fit '{fit}' on days before {year}",
                day,
                worst=[f"drawn off {where}"],
            )
        if nid in tree.nations.nations:
            colours = F.file_for_nation(tree.nations, nid)
            for flown in F.vessel_flies(world, v):
                flag = colours.flags.get(str(flown.get("name")))
                if flag is not None and not dates_hold(flag.dates, day.year):
                    audit.add(
                        "f",
                        f"f-colours:{nid}",
                        "she wears colours whose own dates do not hold the day's year (the "
                        "colours' dates are read by nothing)",
                        day,
                        worst=[f"{flag.name} worn off {where}"],
                    )
    # the lines the world serves of itself
    for line in (world.nations.sailed_with_words(), world.nations.wars_words()):
        named = {int(y) for y in YEAR.findall(line)}
        if named and day.year not in named:
            audit.add(
                "x",
                "x-as-of",
                "the table she sailed with is served as of a day of another year",
                day,
                worst=[f"{where}: {line[:60]}"],
            )
    audit.worlds.append((day, station))


# ---------------------------------------------------------------------------
# The run
# ---------------------------------------------------------------------------


def run(
    full: bool = False,
    letters: str = LETTERS,
    *,
    worlds: bool = True,
    reference: bool = True,
    tree: Tree | None = None,
) -> Audit:
    """The audit: the cheap road over the sampled days, the dear road on a few."""
    audit = Audit()
    t0 = time.perf_counter()
    tree = tree if tree is not None else load_tree()
    audit.seconds["the tree"] = time.perf_counter() - t0
    ref = load_reference() if reference and "r" in letters else None
    days = sample_days(tree, full)
    ref_days = sorted(set(days) | set(ref.dates())) if ref is not None else days
    audit.days = days
    unparsed: list[str] = []
    scan = scan_dated(tree.data, unparsed) if set("xc") & set(letters) else []

    def timed(letter: str, fn: Any, *args: Any) -> None:
        if letter not in letters:
            return
        t = time.perf_counter()
        fn(*args)
        audit.seconds[letter] = audit.seconds.get(letter, 0.0) + time.perf_counter() - t

    # the mechanical checks on the data's own days; the reference's on its days as well
    timed("p", check_ports, audit, tree, days, None)
    timed("w", check_wars, audit, tree, days, None)
    timed("b", check_blockades, audit, tree, days, None)
    timed("v", check_vessels, audit, tree, days)
    timed("f", check_flags, audit, tree, days)
    timed("d", check_days, audit, tree, days)
    timed("l", check_lights, audit, tree, days)
    timed("x", check_words, audit, tree, days, scan)
    timed("e", check_engine, audit, tree, days)
    timed("u", check_undated, audit, tree, days)
    timed("c", check_classing, audit, tree, days, scan, unparsed)
    if ref is not None:
        t = time.perf_counter()
        shadow = Audit()
        check_ports(shadow, tree, ref_days, ref)
        check_wars(shadow, tree, ref_days, ref)
        check_blockades(shadow, tree, ref_days, ref)
        for key, f in shadow.findings.items():
            if f.basis == REFERENCE:
                audit.findings[key] = f
        audit.seconds["r"] = time.perf_counter() - t
    if worlds and "a" in letters:
        t = time.perf_counter()
        with fast_yaml():
            for day, station in world_days(full):
                check_world(audit, tree, day, station, ref)
        audit.seconds["a"] = time.perf_counter() - t
    audit.info.append(
        f"the days: {len(days)} of the data's naming and the years'"
        + (f", {len(ref_days)} with the reference's" if ref is not None else "")
        + f"; whole worlds: {len(audit.worlds)}"
    )
    return audit


# ---------------------------------------------------------------------------
# The known list and the report
# ---------------------------------------------------------------------------


def load_known(path: Path = KNOWN_PATH) -> dict[str, dict[str, Any]]:
    """The known list: each finding owned by its key, with what it is, the years it bites,
    its basis, its owner, its reason in a line, and (`sweep: full`) whether only the full
    sweep makes it."""
    doc = read_yaml(path) or {}
    return {str(e["key"]): dict(e) for e in doc.get("known") or []}


def unlisted(audit: Audit, known: dict[str, dict[str, Any]]) -> list[Finding]:
    return [f for k, f in sorted(audit.findings.items()) if k not in known]


def no_longer(audit: Audit, known: dict[str, dict[str, Any]], full: bool) -> list[str]:
    """The listed findings the sweep no longer makes (a sampled sweep is not asked for
    those marked `sweep: full`)."""
    return sorted(
        k
        for k, e in known.items()
        if k not in audit.findings and (full or e.get("sweep") != "full")
    )


def over_ceiling(audit: Audit, known: dict[str, dict[str, Any]]) -> list[Finding]:
    return [
        f
        for k, f in sorted(audit.findings.items())
        if k in known and known[k].get("most") is not None and f.count > int(known[k]["most"])
    ]


def by_year(audit: Audit, basis: str) -> dict[int, int]:
    out: dict[int, int] = defaultdict(int)
    for f in audit.findings.values():
        if f.basis == basis:
            for y in {d.year for d in f.days}:
                out[y] += 1
    return dict(sorted(out.items()))


def report(audit: Audit, known: dict[str, dict[str, Any]] | None = None) -> str:
    lines = []
    for basis in (MECHANICAL, REFERENCE):
        found = [f for f in audit.findings.values() if f.basis == basis]
        lines.append(f"== {basis}: {len(found)} findings")
        for f in sorted(found, key=lambda f: (LETTERS.index(f.check), f.key)):
            mark = "" if known is None else ("  " if f.key in known else "! ")
            lines.append(f"{mark}{f.line()}")
        counts: dict[str, int] = defaultdict(int)
        for f in found:
            counts[f.check] += 1
        lines.append(
            "   by check: " + ", ".join(f"({k}) {counts[k]}" for k in LETTERS if counts.get(k))
        )
        years = by_year(audit, basis)
        lines.append("   by year: " + ", ".join(f"{y} {n}" for y, n in years.items()))
    lines.append("== what answers")
    lines += audit.info
    lines.append("== seconds: " + ", ".join(f"({k}) {v:.1f}" for k, v in audit.seconds.items()))
    return "\n".join(lines)


def known_entries(audit: Audit, sampled: Audit | None = None) -> list[dict[str, Any]]:
    """The findings as the known list's entries, for its writing: the key, what it is, the
    years, the basis, the count as `most`; the owner and the reason are the writer's."""
    out = []
    for key, f in sorted(
        audit.findings.items(), key=lambda kv: (LETTERS.index(kv[1].check), kv[0])
    ):
        entry: dict[str, Any] = {
            "key": key,
            "what": f.words,
            "years": f.years(),
            "basis": f.basis,
            "owner": "",
            "reason": "",
            "most": f.count,
        }
        if sampled is not None and key not in sampled.findings:
            entry["sweep"] = "full"
        out.append(entry)
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--full", action="store_true", help="every day the data names; more worlds")
    ap.add_argument("--check", default=LETTERS, help=f"the checks by letter ({LETTERS})")
    ap.add_argument("--no-worlds", action="store_true", help="the cheap road alone")
    ap.add_argument("--no-reference", action="store_true", help="the mechanical findings alone")
    ap.add_argument(
        "--known", action="store_true", help="mark the findings the known list lacks with !"
    )
    ap.add_argument(
        "--entries", action="store_true", help="print the findings as known-list entries"
    )
    ap.add_argument("--classing", action="store_true", help="print the classing's table")
    args = ap.parse_args(argv)
    if args.classing:
        print(classing_table())
        return 0
    audit = run(args.full, args.check, worlds=not args.no_worlds, reference=not args.no_reference)
    if args.entries:
        sampled = run(False, args.check, worlds=not args.no_worlds) if args.full else None
        print(
            yaml.safe_dump(
                known_entries(audit, sampled), sort_keys=False, allow_unicode=True, width=200
            )
        )
        return 0
    known = load_known() if args.known else None
    print(report(audit, known))
    if known is not None:
        new = unlisted(audit, known)
        gone = no_longer(audit, known, args.full)
        print(
            f"== {len(new)} finding(s) the known list lacks; {len(gone)} it lists and the "
            "sweep no longer makes"
        )
        return 1 if new or gone else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
