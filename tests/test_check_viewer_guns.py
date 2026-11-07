"""Package 81, item 4: the viewer's guns checked on every ship file (tools/check_viewer_guns.py;
docs/design/Design-ViewerAction.md §8, §9).

Parametrized over the files under data/ships/, so that a ship added later is checked by it with
no change: every gun placed by the one rule, every port's sill on her drawn side. And a file
written to a temporary directory with the contract and a made-up fit passes with no change of
code, the same file with a gun off its triple is refused and says why.
"""

from __future__ import annotations

import copy
import sys
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import check_viewer_guns as C  # noqa: E402

EVERY_FILE = sorted(str(p.relative_to(ROOT)) for p in (ROOT / "data" / "ships").glob("*.yaml"))


@pytest.mark.parametrize("path", EVERY_FILE)
def test_every_ship_file_passes_the_checker(path):
    rep = C.check(ROOT / path)
    assert rep.ok, rep.refused + rep.off_side


def test_the_checker_runs_clean_over_the_tree(capsys):
    assert C.main([]) == 0
    assert capsys.readouterr().out.rstrip().endswith("clean")


def _made_up(tmp_path: Path, x_off: float = 0.0) -> Path:
    """The brig's file with a fit of her own making: her bow chasers and her first two pairs of
    carronades (both kinds, so that the magazine she carries serves them), one pair moved
    `x_off` off its triple."""
    doc = yaml.safe_load((ROOT / "data" / "ships" / "brig.yaml").read_text(encoding="utf-8"))
    old = doc["armament"]["fits"][doc["armament"]["default"]]
    chasers = [g for g in old["guns"] if g["place"] == "bow"]
    carronades = [g for g in old["guns"] if g["kind"] == "carronade"][:4]
    guns = copy.deepcopy(chasers + carronades)
    for g in guns[-2:]:
        g["x_m"] = g["x_m"] + x_off
    fit = dict(old)
    fit["guns"] = guns
    fit["source"] = "made up for the test"
    doc["armament"]["fits"]["made up"] = fit
    doc["armament"]["default"] = "made up"
    path = tmp_path / "made-up.yaml"
    path.write_text(yaml.safe_dump(doc, sort_keys=False), encoding="utf-8")
    return path


def test_a_ship_written_with_the_contract_passes_with_no_change_of_code(tmp_path):
    rep = C.check(_made_up(tmp_path))
    assert rep.ok
    assert any("fit 'made up': 6 guns: 6 port" in line for line in rep.lines)


def test_the_same_ship_with_a_gun_off_its_triple_is_refused_and_says_why(tmp_path):
    rep = C.check(_made_up(tmp_path, x_off=0.3))
    assert not rep.ok
    assert len(rep.refused) == 2
    assert all("made up" in r and "no port of the upper deck" in r for r in rep.refused)
    assert C.main([str(_made_up(tmp_path, x_off=0.3))]) == 1
