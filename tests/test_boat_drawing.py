"""Package 82, the boat's drawing (the design's §5.4; the package's last commit): each boat's
file carries her shape keys by rule through the generator's `hull_profile` and `hull_form`,
every line judged and marked so, the drawn hull checked against the file (the displacement
within the record's share); the snapshot carries a boat's `oars` block; and the viewer draws
her oars from the thwarts while they are out, one line an oar, nothing when they are laid in.
Nothing of the drawing is read by the physics (Build-Ships.md §5.0 principle 8).
"""

from __future__ import annotations

import pytest

from freesail.api.queries import snapshot
from freesail.ship import form
from freesail.ship.loader import load_spec
from freesail.ship.schema import PROFILE_KEYS
from tests.test_crews import hove_to_world
from tests.test_view_geometry import BOATS, graph_of, make_ship, needs_node, run_js, ship_state


@pytest.mark.parametrize("path", BOATS)
def test_every_boat_file_carries_a_judged_profile_that_draws_within_the_records_share(path):
    spec = load_spec(path)
    p = spec.hull.profile
    assert p is not None
    assert p.rail_m and p.breadth_m and p.keel_m and p.stem_m and p.stern_m and p.section_m
    assert p.wales_m and dict(p.decks_m).get("upper")
    assert p.form is not None and p.form.stern.type == "square" and p.form.head == "none"
    marks = dict(p.marks)
    assert all(marks.get(k) == "judged" for k in ("rail_m", "breadth_m", "section_m", "form.stern"))
    assert marks.get("form.head") == "rule"
    notes = form.check(spec.hull)
    drawn = form.drawn_displacement_kg(spec.hull)
    assert abs(drawn / spec.hull.displacement_kg - 1.0) <= form.DISPLACEMENT_RECORD_SHARE
    assert any("drawn displacement" in n for n in notes)
    hull = graph_of(path)["hull"]
    assert "profile" in hull and len(hull["stations"]) > 4
    assert set(hull["profile"]) <= set(PROFILE_KEYS)


def test_the_snapshot_carries_a_boats_oars_and_no_ships():
    w = hove_to_world()
    assert "oars" not in snapshot(w)
    w.submit("go to the launch")
    snap = snapshot(w)
    assert snap["oars"] == {"number": 10, "out": False, "manned": 0, "stroke": 0.0, "hours": 0.0}
    w.submit("give way")
    snap = snapshot(w)
    assert snap["oars"]["out"] and snap["oars"]["manned"] == 10 and snap["oars"]["stroke"] == 1.0


@needs_node
def test_the_viewer_draws_the_oars_from_the_thwarts_while_they_are_out(tmp_path):
    ship = make_ship("data/ships/boat-launch-31.yaml")
    data = ship_state(ship)
    body = """
    const sk = P.buildSkeleton(d.graph, d.snap);
    const oars = sk.figures.filter(f => f.kind === 'spar' && f.cls === 'oar');
    return {n: oars.length, states: oars.map(o => o.state), sides: oars.map(o => o.side),
            dip: oars.map(o => o.pts[1][2])};
    """
    data["snap"]["oars"] = {"number": 10, "out": False, "manned": 0, "stroke": 0.0, "hours": 0.0}
    assert run_js(tmp_path, data, body)["n"] == 0  # laid in: none drawn
    data["snap"]["oars"] = {"number": 10, "out": True, "manned": 10, "stroke": 1.0, "hours": 0.5}
    got = run_js(tmp_path, data, body)
    assert got["n"] == 10 and set(got["states"]) == {"pulling"}
    assert got["sides"].count("starboard") == 5 and got["sides"].count("larboard") == 5
    assert all(z < 0.0 for z in got["dip"])  # the blades in the water under the stroke
    data["snap"]["oars"] = {"number": 10, "out": True, "manned": 10, "stroke": 0.0, "hours": 0.5}
    got = run_js(tmp_path, data, body)
    assert (
        got["n"] == 10 and set(got["states"]) == {"lying_on"} and all(z > 0.0 for z in got["dip"])
    )
