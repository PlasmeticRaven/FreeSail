"""Load a ship file from disk into a Ship."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from freesail.ship.graph import Ship
from freesail.ship.schema import ShipFileError, ShipSpec, parse_ship


def load_spec(path: str | Path) -> ShipSpec:
    path = Path(path)
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ShipFileError(f"{path}: no such ship file.") from None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ShipFileError(f"{path}: the file is not valid YAML ({e}).") from None
    return parse_ship(data, source=str(path))


def spec_from_dict(data: dict[str, Any], source: str = "<memory>") -> ShipSpec:
    return parse_ship(data, source=source)


def load_ship(path: str | Path) -> Ship:
    return Ship(load_spec(path))


def ship_from_dict(data: dict[str, Any], source: str = "<memory>") -> Ship:
    return Ship(spec_from_dict(data, source))
