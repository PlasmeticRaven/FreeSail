"""The guns and the ports as the viewer draws them (docs/design/Design-ViewerAction.md §1-§3).

One rule places every gun of every hull from what her file already carries, and one table gives
every gun its figure by kind, calibre and weight; the server serves both (`queries.ship_graph`)
and the checker (`tools/check_viewer_guns.py`) reads the same functions, so that what is checked
is what is drawn. Pure: nothing here reads or writes the world, and the physics, the guns' cycle
and the lee ports never read it.

The rule (§2):
- a port gun (broadside, bow, stern) stands at its deck's triple whose x is its own within
  `TRIPLE_TOLERANCE_M` (Build-Ships.md §5.3, truth 7-185); none, it is refused, never placed by
  hand;
- the triple is a port where the side stands the port's depth above its sill, less `PORT_FIT_M`,
  and a place over the rail where it does not (§2.2, the side's own test; the lead's ruling of
  2026-11-07 over the generator's `OVER_THE_RAIL_M`);
- a swivel (`rail`) on its yoke on the rail at its x; a pivot on the middle line at its x.

The figure (§3): the length is the pattern of nearest weight among those Adye prints for that
kind and calibre (pp. 155 and 72, read on the page images), so that no key is asked of a file.
"""

from __future__ import annotations

import math
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from freesail.ship.parts import filed_charge_lb
from freesail.ship.profile import interp, ports_of, rail_at

FT = 0.3048
INCH = 0.0254

# The rule's tolerances (§2.1)
# a port gun on its triple, as Build-Ships.md §5.3 and truth 7-185 have it
TRIPLE_TOLERANCE_M = 0.01
# a drawn side's tolerance to a triple (§5.2); a port within it of the rail is cut to it
PORT_FIT_M = 0.05
# The 64's generator's convention for a gun over the rail (tools/ships/indefatigable.py), named
# only so that the checker can say which triples it puts over the rail by the side's test and not
# at it (§2.2); the rule does not read it.
OVER_THE_RAIL_M = 0.05

# The figure's placing (judgement, §2 and §3; the questions to the owner's shelf, §11.2)
# A port's top under the rail where it is cut (package 98, step 3): the viewer's `ON_LINE_M`
TOP_UNDER_RAIL_M = 0.002
RAIL_CLEAR_M = 0.05  # a gun over the rail: its muzzle's underside this far above the rail
SWIVEL_YOKE_M = 0.15  # a swivel's axis above the rail (question 4)
CHASE_TRAIN_DEG = 30.0  # a chaser trained toward its end from square to the side (question 5)

# The long guns' patterns by the weight of their shot: (feet, inches, cwt), Adye, The Bombardier,
# and Pocket Gunner (1804), p. 155, "Length and Weight of English Iron Guns" (IA leaf n178, read
# on the image, 2026-11-07; the 24s to the 9s read before by the ships sessions,
# tools/ships/period.py). The 4-pounder of 6 ft is printed "22 1", read 12 cwt 1 qr by its own
# column of metal to the pound of shot (343 lb).
LONG_PATTERNS: dict[float, tuple[tuple[int, int, float], ...]] = {
    42: ((10, 0, 67.0), (9, 6, 65.0)),
    32: ((10, 0, 58.0), (9, 6, 55.0)),
    24: ((10, 0, 52.0), (9, 6, 49.5), (9, 0, 47.5)),
    18: ((9, 6, 42.0), (9, 0, 40.0)),
    12: ((9, 6, 34.0), (9, 0, 32.0), (8, 6, 31.5), (7, 6, 29.25)),
    9: ((7, 6, 24.5), (7, 0, 23.0)),
    6: ((8, 0, 22.0), (6, 0, 16.5)),
    4: ((6, 0, 12.25), (5, 6, 11.25)),
    3: ((4, 6, 7.25),),
}
# The carronades: (feet, inches, cwt), and the bore in inches, Adye 1804 p. 72, "Carronades.
# Their Weight and Dimensions" (IA leaf n95, read on the image, 2026-11-07).
CARRONADE_PATTERNS: dict[float, tuple[tuple[float, float, float], ...]] = {
    68: ((5, 2, 36.0), (4, 0, 29.0)),
    42: ((4, 3.5, 22.25),),
    32: ((4, 0.5, 17.125),),
    24: ((3, 7.5, 13.0), (3, 0, 11.0 + 2 / 4 + 25 / 112)),
    18: ((3, 3, 9.0), (2, 4, 8.0 + 1 / 4 + 25 / 112)),
    12: ((2, 2, 5.0 + 3 / 4 + 10 / 112),),
}
CARRONADE_BORE_IN = {68: 8.05, 42: 6.84, 32: 6.35, 24: 5.68, 18: 5.16, 12: 4.52}
SWIVEL_LENGTH_M = 3 * FT  # judgement: neither Adye nor Falconer gives one (question 4)
# The outside by calibres of the bore (judgement until Caruana's Blomefield dimensions, question 3)
BREECH_CALIBRES = 3.4
MUZZLE_CALIBRES = 2.2
CARRONADE_CALIBRES = 2.6
# A gun of a weight more than this share off its pattern's is listed by the checker (§3.2)
WEIGHT_LISTED_SHARE = 0.10


@dataclass(frozen=True)
class GunFigure:
    """A gun's drawn figure: its length, its bore, its outside at the breech and the muzzle,
    metres; the pattern it is drawn at, in words; how far its file's weight stands off that
    pattern's, as a share; and whether its length is a judgement (no pattern read)."""

    length_m: float
    bore_m: float
    breech_m: float
    muzzle_m: float
    pattern: str
    weight_off: float
    judged: bool = False


def _shot_bore_m(pounder: float) -> float:
    """A long gun's bore: the ball's diameter by the gunner's rule (`combat/hits.py`, Douglas),
    5.04 in for the 18-pounder, as the cube root of the weight; the windage is not drawn."""
    return INCH * 5.04 * (max(float(pounder), 0.25) / 18.0) ** (1.0 / 3.0)


def _feet(ft: float, inch: float) -> float:
    return ft * FT + inch * INCH


def _nearest(
    patterns: Sequence[tuple[float, float, float]], weight_cwt: float
) -> tuple[float, float, float]:
    return min(patterns, key=lambda p: (abs(p[2] - weight_cwt), -p[2]))


def _pattern_words(ft: float, inch: float, cwt: float) -> str:
    inches = f" {inch:g} in" if inch else ""
    return f"{ft:g} ft{inches}, {cwt:g} cwt"


def figure(kind: str, pounder: float, weight_cwt: float) -> GunFigure:
    """The figure of a gun of this kind, calibre and weight, the same on every ship (§3.1)."""
    pounder = float(pounder)
    weight = float(weight_cwt)
    if kind == "swivel":
        bore = _shot_bore_m(pounder)
        return GunFigure(SWIVEL_LENGTH_M, bore, bore * 3.0, bore * 2.0, "a swivel", 0.0, True)
    if kind == "carronade":
        patterns = CARRONADE_PATTERNS.get(pounder)
        bore = INCH * CARRONADE_BORE_IN.get(pounder, _shot_bore_m(pounder) / INCH)
        out = bore * CARRONADE_CALIBRES
        if not patterns:
            # a calibre no pattern gives: its length scaled from the 12's by the bore (judgement)
            ft, inch, _cwt = CARRONADE_PATTERNS[12][0]
            length = _feet(ft, inch) * bore / (INCH * CARRONADE_BORE_IN[12])
            return GunFigure(length, bore, out, out * 0.9, "no pattern read", 0.0, True)
        ft, inch, cwt = _nearest(patterns, weight)
        return GunFigure(
            _feet(ft, inch),
            bore,
            out,
            out * 0.9,
            _pattern_words(ft, inch, cwt),
            abs(weight - cwt) / cwt,
        )
    bore = _shot_bore_m(pounder)
    patterns = LONG_PATTERNS.get(pounder)
    if not patterns:
        # a calibre no pattern gives: the nearest calibre's longest, scaled by the bore (judgement)
        near = min(LONG_PATTERNS, key=lambda p: abs(p - pounder))
        ft, inch, _cwt = LONG_PATTERNS[near][0]
        length = _feet(ft, inch) * bore / _shot_bore_m(near)
        return GunFigure(
            length,
            bore,
            bore * BREECH_CALIBRES,
            bore * MUZZLE_CALIBRES,
            "no pattern read",
            0.0,
            True,
        )
    ft, inch, cwt = _nearest(patterns, weight)
    return GunFigure(
        _feet(ft, inch),
        bore,
        bore * BREECH_CALIBRES,
        bore * MUZZLE_CALIBRES,
        _pattern_words(ft, inch, cwt),
        abs(weight - cwt) / cwt,
    )


# -- the rule ------------------------------------------------------------------------------


PORT_PLACES = ("broadside", "bow", "stern")


@dataclass(frozen=True)
class Placing:
    """Where one gun is drawn (§2): `how` one of 'port', 'over the rail', 'rail', 'pivot', or
    None and `refused` why. `x_m` the gun's place fore and aft (the triple's for a port gun),
    `y_m` the half-breadth its muzzle comes out at (the triple's, the rail's; 0 for a pivot),
    `axis_z_m` its bore's height above the water, `deck_z_m` the deck its carriage stands on,
    `train_deg` toward its end from square to the side (a chaser's), `triple` and `port` (width,
    depth) where it has them, `port_top_m` the port's top as cut (the rail where it reaches it),
    and the checker's notes."""

    gun_id: str
    how: str | None
    refused: str | None = None
    deck: str | None = None
    x_m: float = 0.0
    y_m: float = 0.0
    axis_z_m: float = 0.0
    deck_z_m: float = 0.0
    train_deg: float = 0.0
    triple: tuple[float, float, float] | None = None
    port: tuple[float, float] | None = None
    port_top_m: float | None = None
    notes: tuple[str, ...] = field(default_factory=tuple)


def _sizes(profile: Any) -> dict[str, tuple[float, float]]:
    return {w: (float(s[0]), float(s[1])) for w, s in (profile.port_size_m or ())}


def _decks(profile: Any) -> dict[str, Sequence[Sequence[float]]]:
    return {w: pts for w, pts in (profile.decks_m or ())}


def _rail_half_breadth(profile: Any, x: float) -> float:
    return interp([(p[0], p[2]) for p in profile.breadth_m], x)


def is_port(profile: Any, deck: str, triple: Sequence[float]) -> bool:
    """Whether a triple of `deck` is a port (the side stands the port's depth above its sill,
    less PORT_FIT_M) rather than a gun's place over the rail (§2.2)."""
    size = _sizes(profile).get(deck)
    if size is None:
        return False
    return rail_at(profile, triple[0]) - float(triple[1]) >= size[1] - PORT_FIT_M


def _deck_z(profile: Any, deck: str | None, x: float) -> float:
    pts = _decks(profile).get(deck) if deck else None
    if pts:
        return interp(pts, x)
    from freesail.ship.profile import deck_at

    z = deck_at(profile, x)
    return float(z) if z is not None else 0.0


def place(profile: Any, gun: Any) -> Placing:
    """Where `gun` (a `GunSpec` or a `Gun` part: its id, kind, pounder, place, side, x_m,
    weight_cwt and deck) is drawn on the hull of `profile` (a `HullProfile`), by §2's rule."""
    gid = str(gun.id)
    if profile is None:
        return Placing(gid, None, "her file gives no profile")
    x = float(gun.x_m)
    fig = figure(gun.kind, gun.pounder, gun.weight_cwt)
    muzzle_r = fig.muzzle_m / 2.0
    if gun.place == "rail":
        rail = rail_at(profile, x)
        return Placing(
            gid,
            "rail",
            x_m=x,
            y_m=_rail_half_breadth(profile, x),
            axis_z_m=rail + SWIVEL_YOKE_M,
            deck_z_m=rail,
        )
    if gun.place == "pivot":
        rail = rail_at(profile, x)
        return Placing(
            gid,
            "pivot",
            deck=gun.deck,
            x_m=x,
            y_m=0.0,
            axis_z_m=rail + muzzle_r + RAIL_CLEAR_M,
            deck_z_m=_deck_z(profile, gun.deck, x),
        )
    if gun.place not in PORT_PLACES:
        return Placing(gid, None, f"no rule places a gun of the place '{gun.place}'")
    deck = gun.deck
    if not deck:
        return Placing(gid, None, "it names no deck")
    triples = ports_of(profile, deck)
    if not triples:
        return Placing(gid, None, f"her profile gives no ports of the {deck} deck", deck=deck)
    size = _sizes(profile).get(deck)
    if size is None:
        return Placing(gid, None, f"her profile gives no port size for the {deck} deck", deck=deck)
    t = min(triples, key=lambda p: abs(float(p[0]) - x))
    if abs(float(t[0]) - x) > TRIPLE_TOLERANCE_M + 1e-9:
        return Placing(
            gid,
            None,
            f"no port of the {deck} deck at {x:g} m (the nearest at {float(t[0]):g} m)",
            deck=deck,
        )
    triple = (float(t[0]), float(t[1]), float(t[2]))
    rail = rail_at(profile, triple[0])
    deck_z = _deck_z(profile, deck, triple[0])
    train = 0.0 if gun.place == "broadside" else CHASE_TRAIN_DEG
    notes: list[str] = []
    if is_port(profile, deck, triple):
        top = triple[1] + size[1]
        if top > rail + 0.005:
            notes.append(f"its port cut to the rail ({top - rail:.2f} m)")
        if top > rail:
            top = rail
        return Placing(
            gid,
            "port",
            deck=deck,
            x_m=triple[0],
            y_m=triple[2],
            axis_z_m=triple[1] + size[1] / 2.0,
            deck_z_m=deck_z,
            train_deg=train,
            triple=triple,
            port=size,
            port_top_m=top,
            notes=tuple(notes),
        )
    gap = rail - triple[1]
    if gap > OVER_THE_RAIL_M + TRIPLE_TOLERANCE_M:
        notes.append(
            f"over the rail by the side's test, its triple {gap:.2f} m under the rail, not at "
            f"{OVER_THE_RAIL_M:g} m"
        )
    return Placing(
        gid,
        "over the rail",
        deck=deck,
        x_m=triple[0],
        y_m=triple[2],
        axis_z_m=rail + muzzle_r + RAIL_CLEAR_M,
        deck_z_m=deck_z,
        train_deg=train,
        triple=triple,
        notes=tuple(notes),
    )


@dataclass(frozen=True)
class Port:
    """One port of the hull on one side's pattern (§2.5): its deck, its triple, its size, its
    top as cut; the guns of the fit that stand in it by side (none: an empty port)."""

    deck: str
    x_m: float
    sill_m: float
    half_breadth_m: float
    width_m: float
    depth_m: float
    top_m: float
    guns: Mapping[str, str]


def deck_slope(profile: Any, deck: str, x: float) -> float:
    """The slope of a deck's line at x (rise over run, over a metre), as the viewer reads it
    for a port's edges parallel to its deck (`client/projection.js`, `deckSlope`)."""
    pts = dict(profile.decks_m or ()).get(deck)
    if not pts or len(pts) < 2:
        return 0.0
    return interp(pts, x + 0.5) - interp(pts, x - 0.5)


def port_top(profile: Any, deck: str, x: float, sill: float, width: float, depth: float) -> float:
    """A port's top's middle as served (§2.5; package 98, step 3, the lead's ruling of
    2026-11-07 on 81's two rules): its sill and depth, its top tilted with its deck as the
    viewer draws it, cut where either corner would stand over the rail at that corner's x
    less `TOP_UNDER_RAIL_M`, so that the drawing honours the figure served."""
    s = deck_slope(profile, deck, x)
    w = width / 2
    limit = min(rail_at(profile, x + c * w) - TOP_UNDER_RAIL_M - c * s * w for c in (-1.0, 1.0))
    if limit >= sill + depth:
        return sill + depth
    # cut: down to the millimetre the graph serves, so that the figure served is under the rail
    return math.floor(limit * 1000.0) / 1000.0


def ports(profile: Any, placings: Iterable[Placing], sides: Mapping[str, str | None]) -> list[Port]:
    """Every port of the hull (§2.5): each triple that is a port by §2.2, with the guns of the
    fit placed in it by side (`sides`: each gun id's side). A triple over the rail is no port."""
    if profile is None:
        return []
    by_triple: dict[tuple[str, float], dict[str, str]] = {}
    for p in placings:
        if p.how == "port" and p.triple is not None and p.deck is not None:
            side = sides.get(p.gun_id) or "both"
            by_triple.setdefault((p.deck, p.triple[0]), {})[side] = p.gun_id
    sizes = _sizes(profile)
    out: list[Port] = []
    for deck, triples in profile.ports_m or ():
        size = sizes.get(deck)
        if size is None:
            continue
        for t in triples:
            if not is_port(profile, deck, t):
                continue
            x = float(t[0])
            top = port_top(profile, deck, x, float(t[1]), size[0], size[1])
            out.append(
                Port(
                    deck,
                    x,
                    float(t[1]),
                    float(t[2]),
                    size[0],
                    size[1],
                    top,
                    dict(by_triple.get((deck, x), {})),
                )
            )
    return out


def contract(profile: Any, guns: Iterable[Any]) -> list[str]:
    """What a hull lacks of the contract (§1), in words; empty when she gives all of it."""
    if profile is None:
        return ["a profile (hull.profile)"]
    lacks: list[str] = []
    if not profile.decks_m:
        lacks.append("her decks (decks_m)")
    words = {w for w, _ in (profile.ports_m or ())}
    sizes = _sizes(profile)
    for g in guns:
        if g.place in PORT_PLACES and g.deck and g.deck not in words:
            lacks.append(f"the ports of the {g.deck} deck (ports_m.{g.deck})")
        if g.place in PORT_PLACES and g.deck and g.deck not in sizes:
            lacks.append(f"the port size of the {g.deck} deck (port_size_m.{g.deck})")
        if g.place in PORT_PLACES and not g.deck:
            lacks.append(f"the deck of {g.id}")
    return sorted(set(lacks))


def served(
    profile: Any,
    guns: Iterable[Any],
    charges: Mapping[tuple[str, float], float] | None = None,
) -> dict[str, Any]:
    """The graph's `guns` and `ports` for the viewer (§7): each gun with its placing and figure,
    or why it is not drawn; each port with the guns that stand in it. A gun's `charge_lb` is its
    own, the fit's `charges` (package 75, SW-1: `parts.filed_charge_lb`, the shares as filed
    where the fit has none, as the magazine reads them), so the eight files' guns are served
    their files' charges and the new ships' Table No. 29's."""
    guns = list(guns)
    placings = [place(profile, g) for g in guns]
    out_guns = []
    for g, p in zip(guns, placings, strict=True):
        f = figure(g.kind, g.pounder, g.weight_cwt)
        entry: dict[str, Any] = {
            "id": g.id,
            "name": getattr(g, "name", g.id),
            "kind_words": getattr(g, "kind_words", f"{g.pounder:g}-pounder {g.kind}"),
            "kind": g.kind,
            "pounder": float(g.pounder),
            "place": g.place,
            "side": g.side,
            "deck": g.deck,
            "how": p.how,
        }
        if p.how is None:
            entry["refused"] = p.refused
        else:
            entry.update(
                {
                    "x_m": round(p.x_m, 3),
                    "y_m": round(p.y_m, 3),
                    "axis_z_m": round(p.axis_z_m, 3),
                    "deck_z_m": round(p.deck_z_m, 3),
                    "train_deg": p.train_deg,
                    "length_m": round(f.length_m, 3),
                    "bore_m": round(f.bore_m, 4),
                    "breech_m": round(f.breech_m, 3),
                    "muzzle_m": round(f.muzzle_m, 3),
                    "charge_lb": filed_charge_lb(charges, g.kind, g.pounder),
                }
            )
        out_guns.append(entry)
    sides = {g.id: g.side for g in guns}
    out_ports = [
        {
            "deck": pt.deck,
            "x_m": pt.x_m,
            "sill_m": pt.sill_m,
            "half_breadth_m": pt.half_breadth_m,
            "width_m": pt.width_m,
            "depth_m": pt.depth_m,
            "top_m": round(pt.top_m, 3),
            "guns": dict(pt.guns),
        }
        for pt in ports(profile, placings, sides)
    ]
    return {"guns": out_guns, "ports": out_ports}


def state_word(gun: Any) -> str:
    """A gun's state as the viewer draws it (§3.3): 'secured', 'run in', 'run out' or
    'dismounted'; a swivel loaded counts as run out, as the guns' reading has it."""
    if gun.dismounted:
        return "dismounted"
    if not gun.cast_loose:
        return "secured"
    if gun.run_out or (gun.kind == "swivel" and gun.loaded):
        return "run out"
    return "run in"


def snapshot_guns(guns: Iterable[Any], shut: Iterable[str]) -> list[dict[str, Any]]:
    """The snapshot's `guns` (§7): each gun's state, whether loaded, its port shut by the sea,
    its rounds fired, and a pivot's training."""
    shut = set(shut)
    out = []
    for g in guns:
        e: dict[str, Any] = {
            "id": g.id,
            "state": state_word(g),
            "loaded": bool(g.loaded),
            "shut": g.id in shut,
            "fired": int(g.fired),
        }
        if g.place == "pivot":
            e["train_deg"] = round(float(g.train_deg), 1)
        out.append(e)
    return out
