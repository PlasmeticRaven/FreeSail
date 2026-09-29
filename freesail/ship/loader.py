"""Load a ship file from disk into a Ship."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from freesail.ship.graph import Ship
from freesail.ship.schema import ShipFileError, ShipSpec, parse_ship


def load_spec(path: str | Path) -> ShipSpec:
    # A ship's path is kept with forward slashes whatever the platform, so that a save or
    # a scenario written on Windows replays on Linux and the other way about (gate 4c,
    # 2026-09-29: the owner's saves carried "data\\ships\\frigate-36.yaml"); a path read
    # back with backslashes is accepted the same way.
    path = Path(str(path).replace("\\", "/"))
    try:
        text = path.read_text(encoding="utf-8")
    except FileNotFoundError:
        raise ShipFileError(f"{path}: no such ship file.") from None
    try:
        data = yaml.safe_load(text)
    except yaml.YAMLError as e:
        raise ShipFileError(f"{path}: the file is not valid YAML ({e}).") from None
    return parse_ship(data, source=path.as_posix())


def spec_from_dict(data: dict[str, Any], source: str = "<memory>") -> ShipSpec:
    return parse_ship(data, source=source)


def load_ship(path: str | Path) -> Ship:
    return Ship(load_spec(path))


def ship_from_dict(data: dict[str, Any], source: str = "<memory>") -> Ship:
    return Ship(spec_from_dict(data, source))
