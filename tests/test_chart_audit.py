"""Package 111: the chart's audit (`tools/audit_chart.py`) and its ratchet.

The audit reads the chart as the game reads it and reports, by region, water nobody owns,
the seams, the tide, the weather, the streams, the ports, the marks and the scenarios; the
known list (`data/charts/audit-known.yaml`) holds every finding of its first run, owned.
The fast tier runs the audit on its sampled grid and fails on any finding the list lacks;
the slow tier runs the full sweep and fails as well on a listed finding no longer found and
on a count above its ceiling, so that a mend takes its entry out and a new block comes in
clean or says what it adds. The checks are proved by planting: a port's mooring on the
land, a headland in the sea, a bound drawn short, a climatology with a box missing, a
scenario started ashore, a block's gauge taken away, each found by its check.
Truths 7-560 to 7-566 are in test_known_truths.py.
"""

from __future__ import annotations

import copy
import importlib.util
import re
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]


def _tool():
    spec = importlib.util.spec_from_file_location("audit_chart", ROOT / "tools" / "audit_chart.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules.setdefault("audit_chart", mod)
    spec.loader.exec_module(mod)
    return mod


A = _tool()
OWNER = re.compile(r"^(package \d+[a-z]?|the lead's list)$")


@pytest.fixture(scope="module")
def sampled():
    return A.run(A.SAMPLED_STEP_DEG)


@pytest.fixture(scope="module")
def chart():
    return A.load_chart(A.CHART_NAME)


def test_the_known_list_holds_each_finding_owned():
    """Every entry its key, its place, its reason in a line and whose it is; no key twice;
    every key of one of the eight checks; the ceiling a count."""
    doc = yaml.safe_load(A.KNOWN_PATH.read_text(encoding="utf-8"))
    entries = doc["known"]
    assert entries
    keys = [e["key"] for e in entries]
    assert len(keys) == len(set(keys))
    for e in entries:
        assert set(e) >= {"key", "place", "reason", "owner"}, e
        assert e["key"][0] in A.LETTERS and e["key"][1] == "-", e["key"]
        assert str(e["place"]).strip(), e["key"]
        reason = str(e["reason"])
        assert reason.strip() and "\n" not in reason, e["key"]
        assert OWNER.match(str(e["owner"])), e["key"]
        if "most" in e:
            assert isinstance(e["most"], int) and e["most"] >= 1, e["key"]


def test_the_sampled_audit_finds_nothing_the_known_list_lacks(sampled):
    """The ratchet, fast: every finding of the sampled grid is in the known list. A new
    finding fails here with its words; own it in the list or mend it."""
    known = A.load_known()
    new = A.unlisted(sampled, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    for letter in A.LETTERS:
        assert letter in sampled.seconds, letter  # every check ran


def test_the_sampled_grid_is_within_the_full_sweeps():
    """The sampled grid's points are points of the full sweep's (a quarter of a degree is
    five twentieths, centred alike), so that a finding of the fast tier's is one the full
    sweep finds too and the known list, written from the full sweep, holds it."""
    box = (36.29334, 40.56, 4.5, 8.0)
    full = {(round(a, 6), round(b, 6)) for a, b in A.grid_points(box, A.FULL_STEP_DEG)}
    some = {(round(a, 6), round(b, 6)) for a, b in A.grid_points(box, A.SAMPLED_STEP_DEG)}
    assert some and some <= full


@pytest.mark.slow
def test_the_full_sweep_is_the_known_list_exactly():
    """The ratchet, slow: the full sweep's findings are the known list's, no more and no
    fewer, each within its ceiling: a finding mended takes its entry out."""
    audit = A.run(A.FULL_STEP_DEG)
    known = A.load_known()
    new = A.unlisted(audit, known)
    assert not new, "findings the known list lacks:\n" + "\n".join(f.line() for f in new)
    gone = sorted(set(known) - audit.keys())
    assert not gone, f"listed findings the full sweep no longer finds (take them out): {gone}"
    over = A.over_ceiling(audit, known)
    assert not over, "counts above their ceiling:\n" + "\n".join(
        f"{f.key}: {f.count} > {known[f.key]['most']}" for f in over
    )


# ---------------------------------------------------------------------------
# Each check proved by planting
# ---------------------------------------------------------------------------


def _port_file(tmp_path: Path, pid: str, edit) -> Path:
    doc = yaml.safe_load((ROOT / "data" / "ports" / f"{pid}.yaml").read_text(encoding="utf-8"))
    edit(doc)
    folder = tmp_path / "ports"
    folder.mkdir(parents=True, exist_ok=True)
    (folder / f"{pid}.yaml").write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return folder


def test_a_mooring_on_the_land_an_unknown_nation_and_overlapping_rows_are_found(tmp_path, chart):
    """(f) Bona's mooring moved onto the town's hill, its nation one the table has not, and
    Barcelona's dated rows made to overlap: each found; the port as it is, nothing of these."""

    def bona(doc):
        doc["mooring"] = {"name": "the hill", "lat_deg": 36.885, "lon_deg": 7.735}
        doc["nation"] = "atlantis"

    folder = _port_file(tmp_path, "bona", bona)

    def barcelona(doc):
        doc["nation"][1]["since"] = "1808-02-01"

    _port_file(tmp_path, "barcelona", barcelona)
    audit = A.Audit()
    A.check_ports(audit, chart, A.Water(chart), folder)
    keys = audit.keys()
    assert "f-dry:bona:mooring" in keys
    assert "f-nation:bona:atlantis" in keys
    assert "f-dated:barcelona" in keys
    plain = A.Audit()
    A.check_ports(plain, chart, A.Water(chart), _port_file(tmp_path / "x", "bona", lambda d: None))
    assert not {k for k in plain.keys() if k.startswith(("f-dry", "f-nation", "f-dated"))}


def test_a_headland_in_the_sea_and_a_rock_inland_are_found(chart):
    """(g) A headland planted in the open Sardinian sea and a rock planted on Sardinia's
    hills are found; a light-vessel afloat and a lighthouse on its rock are not."""
    from freesail.world.chart import Feature

    features = {
        "x-cape": Feature("x-cape", "headland", "Cape Nowhere", 39.0, 6.0),
        "x-rock": Feature("x-rock", "rock", "the Hill Rock", 40.0, 9.0),
        "x-lv": Feature("x-lv", "light", "the Nowhere light-vessel", 39.0, 6.1, lit={"from": 1800}),
        "seven-stones-lightvessel": chart.features["seven-stones-lightvessel"],
        "wolf-rock-light": chart.features["wolf-rock-light"],
        "wolf-rock": chart.features["wolf-rock"],
    }
    fake = SimpleNamespace(
        features=features,
        region_of={k: "test" for k in features},
        levels=chart.levels,
        elevation_at=chart.elevation_at,
    )
    audit = A.Audit()
    A.check_marks(audit, fake, A.Water(fake))
    assert audit.keys() == {"g-afloat:x-cape", "g-ashore:x-rock"}


def test_a_bound_drawn_short_leaves_water_nobody_owns(chart):
    """(a) The Sardinian sea's north bound drawn down to 40.3 N leaves the water of its
    tiles' top row nobody's; as it is, the region owns its own tiles' water to 40.56 N."""
    manifest = copy.deepcopy(A.load_manifest())
    regions = manifest["regions"]
    manifest["regions"] = {"sardinian-sea": regions["sardinian-sea"]}
    as_built = A.Audit()
    A.check_unowned(as_built, manifest)
    manifest["regions"]["sardinian-sea"]["bounds"]["north"] = 40.3
    short = A.Audit()
    A.check_unowned(short, manifest)
    before = {f.key: f.count for f in as_built.findings}
    after = {f.key: f.count for f in short.findings}
    assert after["a-unowned:sardinian-sea:north"] > before.get("a-unowned:sardinian-sea:north", 0)
    assert after["a-unowned:sardinian-sea:north"] > 10_000


def test_two_regions_claiming_the_same_water_are_found(chart):
    """(a) The bounds two regions both claim: the Ligurian sea's and the Tyrrhenian's."""
    audit = A.Audit()
    A.check_overlaps(audit, A.load_manifest(), A.Water(chart), 0.25)
    assert audit.keys() == {"a-overlap:ligurian-sea+tyrrhenian"}


def test_water_in_no_box_of_the_weather_is_found(chart):
    """(d) With the Catalan coast's box taken out of the climatology, its water lies in no
    box and takes the nearest; as the file is, it lies in its own."""
    clim = A.load_climatology()
    fake_chart = SimpleNamespace(regions=["catalan-coast"], region_bounds=chart.region_bounds)
    plain = A.Audit()
    A.check_weather(plain, fake_chart, clim, A.Water(chart), 0.25)
    assert not plain.findings
    less = SimpleNamespace(
        boxes={k: v for k, v in clim.boxes.items() if k != "catalan-coast"},
        box_at=None,
    )
    less.box_at = lambda lat, lon: type(clim).box_at(less, lat, lon)
    audit = A.Audit()
    A.check_weather(audit, fake_chart, less, A.Water(chart), 0.25)
    assert "d-no-box:catalan-coast" in audit.keys()


def test_a_block_without_its_gauge_reads_another_seas_tide(chart):
    """(c) With Barcelona's gauge taken out, the Catalan coast is no block of the tide's and
    its water the eleven's alone: beyond the reach, another sea's, a level not its sea's."""
    from freesail.world import tide as T

    c = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    s = yaml.safe_load(T.STREAMS_PATH.read_text(encoding="utf-8"))
    fake_chart = SimpleNamespace(regions=["catalan-coast"], region_bounds=chart.region_bounds)
    plain = A.Audit()
    A.check_tide(plain, fake_chart, T.Tide(c, s), A.Water(chart), 0.25)
    assert not plain.findings
    c["gauges"] = [g for g in c["gauges"] if g["id"] != "barcelona"]
    audit = A.Audit()
    A.check_tide(audit, fake_chart, T.Tide(c, s), A.Water(chart), 0.25)
    assert {
        "c-far:catalan-coast",
        "c-other-sea:catalan-coast",
        "c-level:catalan-coast",
    } <= audit.keys()


def test_a_stream_area_on_the_land_is_found(chart):
    """(e) A stream area drawn over Castile holds no water."""
    from freesail.world import tide as T

    c = yaml.safe_load(T.CONSTITUENTS_PATH.read_text(encoding="utf-8"))
    s = yaml.safe_load(T.STREAMS_PATH.read_text(encoding="utf-8"))
    s["areas"].insert(
        0,
        {
            "id": "castile",
            "name": "the plain of Castile",
            "chart": "biscay-south",
            "polygon": [[42.2, -4.5], [42.2, -4.0], [42.6, -4.0], [42.6, -4.5]],
            "axis_deg": 0,
            "spring_kn": 1,
            "neap_kn": 0.5,
            "phase_h": 0,
        },
    )
    fake_chart = SimpleNamespace(regions=[], region_bounds={})
    audit = A.Audit()
    A.check_streams(audit, fake_chart, T.Tide(c, s), T.load_directions(), A.Water(chart), 0.25)
    assert [f.key for f in audit.findings] == ["e-area-land:castile"]


def test_a_scenario_started_ashore_and_a_port_with_no_file_are_found(tmp_path):
    """(h) A scenario started on Minorca's hills and naming a port with no file."""
    raw = yaml.safe_load((ROOT / "data" / "scenarios" / "bona.yaml").read_text(encoding="utf-8"))
    raw["position"] = {"lat_deg": 39.95, "lon_deg": 4.05}
    raw["ports"] = list(raw["ports"]) + ["atlantis"]
    folder = tmp_path / "scenarios"
    folder.mkdir()
    (folder / "ashore.yaml").write_text(yaml.safe_dump(raw, sort_keys=False), encoding="utf-8")
    audit = A.Audit()
    A.check_scenarios(audit, folder)
    assert audit.keys() == {"h-dry:ashore", "h-port:ashore:atlantis"}


def test_the_report_is_by_region_and_marks_what_the_list_lacks(sampled):
    known = A.load_known()
    text = A.report(sampled, known)
    assert "== tyrrhenian" in text and "== seconds:" in text
    assert "\n! " not in text  # nothing unlisted


def test_a_region_with_no_sea_named_is_a_finding_and_not_the_mediterraneans(chart):
    """(c) A block whose sea the audit's table does not name is said so (`c-no-sea`) and its
    tide not judged, never held to the Mediterranean's ceiling by default (the lead's word,
    package 111): a box over the Canaries' water, as a block building there would bring."""
    from freesail.world import tide as T

    assert "canaries" not in A.SEAS
    fake_chart = SimpleNamespace(
        regions=["canaries"], region_bounds={"canaries": (28.0, 28.5, -16.5, -16.0)}
    )
    audit = A.Audit()
    A.check_tide(audit, fake_chart, T.load_tide(), A.Water(chart), 0.25)
    assert [f.key for f in audit.findings] == ["c-no-sea:canaries"]
    named = set(A.SEAS)
    manifest = A.load_manifest()
    assert set(manifest["regions"]) | set(manifest.get("tide_regions") or {}) <= named
