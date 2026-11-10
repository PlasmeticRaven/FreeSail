"""The flags of command and identity (spec M7 §1; package 76, the owner's addition of
2026-11-07; docs/design/Design-Signals.md, "As built out").

Each root under `data/signals/` has a seventh file beside its six books, `colours.yaml`: the
nation's flags by name (the ensign and its variants by service or squadron, the merchant's
ensign, the jack, the pendant, the commodore's broad pendant, an admiral's flag by rank, the
flag of truce), each with its words, its proportion, its drawing (coloured rectangles and
lines on the flag's own square, x along the fly from the hoist and y down from the head, each
0 to 1), its dates and its source; and the occasions, what flies where by occasion and role,
in 81's place words (Design-ViewerAction.md §12.2).

**What flies where** is a pure function of the nation's file, the colours' state and the
nation shown, the ship's role, her captain's rank (an admiral's flag), the occasion, and the
flags ordered beside them (`hoist the broad pendant`, `hoist a second ensign at the main`,
`hoist the jack`). The locker keeps the ordered flags and the list last set (`Locker.flies`,
which the viewer reads, `freesail/api/viewer_flags.py`); the lookout reads the list in words
at the colours' range. Nothing here is physics, and nothing here is logged but what the
lookout and the orders say.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import cache
from pathlib import Path
from typing import Any

import yaml

from freesail.world.signals import SIGNALS_DIR, BookFileError

COLOURS_FILE = "colours.yaml"

KINDS = (
    "ensign",
    "merchant ensign",
    "jack",
    "pendant",
    "broad pendant",
    "admiral's flag",
    "truce",
    "standard",
)
SERVICES = ("navy", "merchant", "privateer", "any")
OCCASIONS = (
    "at sea",
    "at anchor",
    "in action",
    "in company under a commodore",
    "in harbour",
    "under truce",
)
ROLES = ("kings ship", "commodore", "admiral", "merchant", "privateer", "any")
RANKS = ("admiral", "vice-admiral", "rear-admiral")

# 81's place words (Design-ViewerAction.md §12.2), exactly
PLACES_FIXED = (
    "peak",
    "staff",
    "main truck",
    "fore truck",
    "mizen truck",
    "jackstaff",
    "fore rigging",
    "main rigging",
    "mizen rigging",
)
_MASTHEAD = re.compile(r"(fore|main|mizen) (top|topgallant|royal) masthead")

# The captain's roles (`captains.ROLES`) as the colours read them (judgement: a sloop, a
# hired cutter and a revenue cutter wear the King's pendant; a packet, a fisherman and an
# Indiaman the merchant's ensign; the commodore of a convoy his broad pendant)
ROLE_OF_CAPTAIN = {
    "kings-ship": "kings ship",
    "cruiser": "kings ship",
    "revenue": "kings ship",
    "commodore": "commodore",
    "admiral": "admiral",
    "merchant": "merchant",
    "packet": "merchant",
    "fisherman": "merchant",
    "indiaman": "merchant",
    "privateer": "privateer",
}

# An admiral's flag by rank, at the masthead the period gave it (Perrin, British Flags, the
# flags of command: the admiral's at the main, the vice-admiral's at the fore, the
# rear-admiral's at the mizen)
RANK_PLACE = {"admiral": "main truck", "vice-admiral": "fore truck", "rear-admiral": "mizen truck"}

# The orders' flags: (kind, where) at sea; the jack at anchor at the jackstaff
ORDERED = {
    "broad pendant": ("broad pendant", "main truck"),
    "second ensign": ("ensign", "main topgallant masthead"),
    "jack": ("jack", "fore truck"),
}


def place_ok(word: str) -> bool:
    """Whether `word` is one of 81's place words."""
    return word in PLACES_FIXED or bool(_MASTHEAD.fullmatch(word))


@dataclass(frozen=True)
class Flag:
    name: str
    kind: str
    service: str
    words: str
    proportion: tuple[float, float]
    drawing: tuple[dict[str, Any], ...]
    squadron: str = ""
    rank: str = ""
    dates: str = ""
    source: str = ""

    def served_drawing(self, inverted: bool = False) -> dict[str, Any]:
        """The drawing as the snapshot serves it to 81's viewer: `{proportion, parts}` with the
        rectangles in `parts` and the lines apart under `lines` (81 draws a part with no
        `rect` as the whole field), each with `n`, its place in the drawing, so that the
        viewer paints them in the drawing's order (package 98, step 3: the Union's crosses
        over its saltires)."""
        parts = [{**p, "n": i} for i, p in enumerate(self.drawing) if "rect" in p]
        lines = [{**p, "n": i} for i, p in enumerate(self.drawing) if "line" in p]
        d: dict[str, Any] = {"proportion": list(self.proportion), "parts": parts}
        if lines:
            d["lines"] = lines
        if inverted:
            d["inverted"] = True
        return d


@dataclass(frozen=True)
class Occasion:
    occasion: str
    role: str
    flags: tuple[tuple[str, str], ...]  # (name, where)


@dataclass(frozen=True)
class ColoursFile:
    nation: str
    sources: tuple[str, ...]
    flags: dict[str, Flag]
    occasions: tuple[Occasion, ...]
    nations: dict[str, ColoursFile] = field(default_factory=dict)  # basic's, by nation id

    def first_of(self, kind: str, service: str = "") -> Flag | None:
        """The file's first flag of a kind, for the service where it has one of its own."""
        found = [f for f in self.flags.values() if f.kind == kind]
        for f in found:
            if service and f.service == service:
                return f
        return found[0] if found else None

    def listed(self, occasion: str, role: str) -> tuple[tuple[str, str], ...]:
        """The occasion's list for the role: its own, else the occasion's `any`, else the
        role's at-sea list, else the at-sea `any` (an occasion's list replaces the
        at-sea list)."""
        for occ, rl in ((occasion, role), (occasion, "any"), ("at sea", role), ("at sea", "any")):
            for o in self.occasions:
                if o.occasion == occ and o.role == rl:
                    return o.flags
        return ()


def _file(raw: dict[str, Any], path: Path, nation_default: str) -> ColoursFile:
    flags: dict[str, Flag] = {}
    for i, f in enumerate(raw.get("flags") or []):
        if not isinstance(f, dict) or not f.get("name"):
            raise BookFileError(f"{path}: flag {i + 1} wants a name")
        name = str(f["name"])
        if name in flags:
            raise BookFileError(f"{path}: two flags named {name!r}")
        kind = str(f.get("kind") or "")
        if kind not in KINDS:
            raise BookFileError(f"{path}: flag {name!r}: kind is one of {KINDS}, not {kind!r}")
        service = str(f.get("service") or "any")
        if service not in SERVICES:
            raise BookFileError(f"{path}: flag {name!r}: service is one of {SERVICES}")
        rank = str(f.get("rank") or "")
        if rank and rank not in RANKS:
            raise BookFileError(f"{path}: flag {name!r}: rank is one of {RANKS}")
        prop = f.get("proportion") or [1, 2]
        drawing = []
        for p in f.get("drawing") or []:
            if (
                not isinstance(p, dict)
                or not (("rect" in p) ^ ("line" in p))
                or not p.get("colour")
            ):
                raise BookFileError(f"{path}: flag {name!r}: a part is a rect or a line, coloured")
            drawing.append(dict(p))
        flags[name] = Flag(
            name=name,
            kind=kind,
            service=service,
            words=str(f.get("words") or name),
            proportion=(float(prop[0]), float(prop[1])),
            drawing=tuple(drawing),
            squadron=str(f.get("squadron") or ""),
            rank=rank,
            dates=str(f.get("dates") or ""),
            source=str(f.get("source") or ""),
        )
    occasions = []
    for i, o in enumerate(raw.get("occasions") or []):
        occ = str(o.get("occasion") or "")
        role = str(o.get("role") or "any")
        if occ not in OCCASIONS:
            raise BookFileError(f"{path}: occasion {i + 1}: one of {OCCASIONS}, not {occ!r}")
        if role not in ROLES:
            raise BookFileError(f"{path}: occasion {i + 1}: role one of {ROLES}, not {role!r}")
        listed = []
        for x in o.get("flags") or []:
            name, where = str(x.get("name") or ""), str(x.get("where") or "")
            if name not in flags:
                raise BookFileError(f"{path}: occasion {occ!r} ({role}) names no flag {name!r}")
            if not place_ok(where):
                raise BookFileError(
                    f"{path}: occasion {occ!r} ({role}): {where!r} is none of 81's place words"
                )
            listed.append((name, where))
        occasions.append(Occasion(occasion=occ, role=role, flags=tuple(listed)))
    sub = {}
    for nid, block in (raw.get("nations") or {}).items():
        sub[str(nid)] = _file(dict(block or {}), path, str(nid))
    return ColoursFile(
        nation=str(raw.get("nation") or nation_default),
        sources=tuple(str(s) for s in raw.get("sources") or []),
        flags=flags,
        occasions=tuple(occasions),
        nations=sub,
    )


@cache
def load_colours(root: str = "basic", base: str | None = None) -> ColoursFile:
    """A root's seventh file, read once."""
    folder = (Path(base) if base else SIGNALS_DIR) / root
    path = folder / COLOURS_FILE
    if not path.exists():
        raise BookFileError(f"{folder}: the root wants {COLOURS_FILE} (every root has the seven)")
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return _file(dict(raw), path, root)


def file_for_nation(nations: Any, nation_id: str) -> ColoursFile:
    """The flags a nation wears: her root's file where the root is her own; else basic's
    block for her (`nations:`), else basic's own plain list."""
    root = "basic"
    if nations is not None and nation_id:
        try:
            root = str(nations.get(nation_id).signals_root or "basic")
        except KeyError:
            root = "basic"
    try:
        f = load_colours(root)
    except BookFileError:
        f = load_colours("basic")
    if f.nation == nation_id:
        return f
    basic = load_colours("basic")
    return basic.nations.get(nation_id, basic)


def colour_role(role: str) -> str:
    """The captain's role as the colours read it."""
    return ROLE_OF_CAPTAIN.get(str(role or ""), "merchant")


def occasion_of(state: str, *, at_anchor: bool, in_action: bool, under_commodore: bool) -> str:
    if state == "truce":
        return "under truce"
    if in_action:
        return "in action"
    if at_anchor:
        return "at anchor"
    if under_commodore:
        return "in company under a commodore"
    return "at sea"


# The colours a flag's short word may name, first named first served (as 81's fallback,
# `freesail/api/viewer_flags.py`, reads them)
COLOUR_WORDS = ("red", "white", "blue", "yellow", "green", "black", "orange")


def _plain_ensign(nations: Any, nation_id: str) -> dict[str, Any]:
    """The plain ensign of a nation basic stands for, coloured by the first colour her flag's
    word names ('the red and yellow' red; a word naming none, the plain cloth's)."""
    word = ""
    if nations is not None and nation_id:
        try:
            word = str(nations.get(nation_id).flag or "")
        except KeyError:
            word = ""
    colour = next((w for w in word.lower().replace(",", " ").split() if w in COLOUR_WORDS), "cloth")
    return {"proportion": [1.0, 2.0], "parts": [{"rect": [0.0, 0.0, 1.0, 1.0], "colour": colour}]}


def flies(
    nations: Any,
    colours: Any,
    role: str,
    *,
    at_anchor: bool = False,
    in_action: bool = False,
    under_commodore: bool = False,
    ordered: tuple[str, ...] | list[str] = (),
    rank: str = "",
) -> list[dict[str, Any]]:
    """What flies where, as the snapshot serves it: `[{place, name, words, drawing}]`.
    `colours` is the locker's (71's `Colours`); `role` the captain's (`captains.ROLES`);
    `ordered` the flags ordered beside the file's (keys of `ORDERED`)."""
    state = str(getattr(colours, "state", "shown"))
    if state in ("none", "struck"):
        return []
    nation = str(getattr(colours, "nation", "") or "")
    f = file_for_nation(nations, nation)
    rl = colour_role(role)
    if rl == "admiral" and not rank:
        rl = "kings ship"
    occ = occasion_of(
        state, at_anchor=at_anchor, in_action=in_action, under_commodore=under_commodore
    )
    adjective, flag_word = "", ""
    if nations is not None and nation:
        try:
            n = nations.get(nation)
            adjective, flag_word = str(n.adjective or ""), str(n.flag or "")
        except KeyError:
            pass
    out: list[dict[str, Any]] = []
    kinds: list[str] = []  # beside `out`, each flag's kind
    inverted = state == "distress"

    def put(flag: Flag | None, where: str) -> None:
        if flag is None:
            return
        pendants = ("pendant", "broad pendant")
        for i, x in enumerate(out):
            if x["place"] == where and kinds[i] in pendants and flag.kind in pendants:
                del out[i], kinds[i]  # a broad pendant replaces the pendant at its place
                break
        if any(x["place"] == where and x["name"] == flag.name for x in out):
            return
        drawing = flag.served_drawing(inverted and flag.kind in ("ensign", "merchant ensign"))
        if f.nation == "basic" and flag.kind in ("ensign", "merchant ensign") and not flag.drawing:
            drawing = _plain_ensign(nations, nation)
            if inverted:
                drawing["inverted"] = True
        words = flag.words
        if flag.kind in ("ensign", "merchant ensign") and adjective:
            # the hover's words as the lookout reads them: 'British colours, the red ensign'
            short = flag.words if f.nation != "basic" else (flag_word or flag.words)
            words = f"{adjective} colours, {short}"
            if inverted:
                words += ", the ensign union down"
        out.append({"place": where, "name": flag.name, "words": words, "drawing": drawing})
        kinds.append(flag.kind)

    for name, where in f.listed(occ, rl):
        put(f.flags[name], where)
    if rl == "admiral" and rank:
        squadron = next((x["name"] for x in out if f.flags[x["name"]].squadron), "")
        sq = f.flags[squadron].squadron if squadron else ""
        flag = next(
            (
                g
                for g in f.flags.values()
                if g.kind == ADMIRALS_FLAG and g.rank == rank and (not sq or g.squadron == sq)
            ),
            None,
        )
        put(flag, RANK_PLACE.get(rank, "main truck"))
    for key in ordered:
        if key not in ORDERED:
            continue
        kind, where = ORDERED[key]
        if key == "jack" and at_anchor:
            where = "jackstaff"
        worn = next((f.flags[x["name"]] for i, x in enumerate(out) if kinds[i] == kind), None)
        service = "merchant" if rl == "merchant" else "privateer" if rl == "privateer" else "navy"
        put(worn or f.first_of(kind, service), where)
    return out


def flies_words(listed: list[dict[str, Any]], nations: Any, nation_id: str) -> str:
    """The lookout's words for what flies where beyond the ensign at the peak: 'she wears a
    pendant at the main: a man-of-war'; 'she wears a broad pendant at the main: a commodore';
    'her ensign at the peak and another at the main topgallant masthead'; '' for the ensign
    alone. `nation_id` the nation shown, whose file names the flags."""
    if not listed:
        return ""
    f = file_for_nation(nations, nation_id)
    by_kind: dict[str, list[str]] = {}
    for x in listed:
        flag = f.flags.get(str(x.get("name") or ""))
        kind = flag.kind if flag is not None else "ensign"
        if kind == "merchant ensign":
            kind = "ensign"
        by_kind.setdefault(kind, []).append(_where_words(str(x["place"])))
    parts = []
    ens = by_kind.get("ensign", [])
    if len(ens) > 1:
        parts.append(f"her ensign at the {ens[0]} and another at the {ens[1]}")
    if "broad pendant" in by_kind:
        parts.append(f"she wears a broad pendant at the {by_kind['broad pendant'][0]}: a commodore")
    elif "pendant" in by_kind:
        parts.append(f"she wears a pendant at the {by_kind['pendant'][0]}: a man-of-war")
    if "admiral's flag" in by_kind:
        parts.append(f"a flag at the {by_kind[ADMIRALS_FLAG][0]}: an admiral")
    if "jack" in by_kind:
        parts.append(f"a jack at the {by_kind['jack'][0]}")
    if "truce" in by_kind:
        parts.append(f"a flag of truce at the {by_kind['truce'][0]}")
    return "; ".join(parts)


ADMIRALS_FLAG = "admiral's flag"


def _where_words(place: str) -> str:
    """'main truck' and 'main topgallant masthead' -> 'main'; the rest as they are ('peak',
    'staff', 'main rigging', 'jackstaff')."""
    if place.endswith(" masthead"):
        return place.split(" ")[0]  # the main topgallant masthead is "the main" to the lookout
    return place.removesuffix(" truck")


# ---------------------------------------------------------------------------
# The world's side: the player's ship refreshed, a far vessel read
# ---------------------------------------------------------------------------

# Whether the lookout speaks what flies beyond the ensign where the colours' line already falls
# (truth 7-434; the proof of what it moves is this put to False, the digests returning)
FLAGS_SPOKEN = True


def world_role(world: Any) -> str:
    """The role this World's ship wears her flags by: her captain's (a rules captain's or the
    far brain's that crews her), else a King's ship where she carries the private table by her
    papers, else a merchantman's."""
    captain = getattr(world, "captain", None)
    role = str(getattr(captain, "role", "") or "")
    if not role:
        vessel = getattr(world, "vessel", None)
        role = str(getattr(getattr(vessel, "brain", None), "role", "") or "")
    if not role:
        papers = getattr(getattr(world, "scenario", None), "papers", None) or {}
        given = papers.get("private_signals") if isinstance(papers, dict) else None
        role = "kings-ship" if given else "merchant"
    return role


def refresh_world(world: Any) -> list[dict[str, Any]] | None:
    """What flies where on this World's ship, set in her locker (the viewer's list), once a
    minute with the look and at every order of the colours. Nothing on a ship with no locker
    yet (the viewer serves its plain ensign)."""
    from freesail.world import signals as S

    ship = getattr(world, "ship", None)
    extra = getattr(ship, "extra", None)
    locker = extra.get("signals") if isinstance(extra, dict) else None
    if locker is None:
        return None
    colours = locker.colours
    if colours.state in ("none", "struck"):
        locker.ordered_flags = []  # the flags ordered beside them come down with the colours
    if not colours.nation and colours.state in ("shown", "distress"):
        colours = S.Colours(state=colours.state, nation=S.own_nation(world))
    quarters = extra.get("quarters")
    listed = flies(
        getattr(world, "nations", None),
        colours,
        world_role(world),
        at_anchor=bool(getattr(world, "at_anchor", False)),
        in_action=bool(quarters is not None and getattr(quarters, "at_quarters", False)),
        under_commodore=bool(getattr(getattr(world, "vessel", None), "under_orders_of", "")),
        ordered=tuple(getattr(locker, "ordered_flags", None) or ()),
    )
    locker.flies = listed
    return listed


def vessel_flies(world: Any, vessel: Any) -> list[dict[str, Any]]:
    """What flies where on a far vessel, as a lookout reads her: by her colours, her brain's
    role (`brains.role_of_vessel`), at anchor, in action (her captain engaging) and the flags
    ordered her by the director's hand. Computed when read; nothing is written."""
    from freesail.world import signals as S
    from freesail.world.brains import role_of_vessel

    locker = S.vessel_locker(vessel)
    listed = getattr(locker, "flies", None)
    if getattr(vessel, "crew", None) is not None and listed is not None:
        return list(listed)  # a crewed ship's locker is her near body's, set there
    brain = getattr(vessel, "brain", None)
    role = str(getattr(brain, "role", "") or "") or role_of_vessel(
        vessel, getattr(brain, "intent", None)
    )
    return flies(
        getattr(world, "nations", None),
        locker.colours,
        role,
        at_anchor=str(getattr(vessel, "sail_state", "")) == "at anchor",
        in_action=str(getattr(vessel, "state", "")) == "engaging",
        under_commodore=bool(getattr(vessel, "under_orders_of", "")),
        ordered=tuple(getattr(locker, "ordered_flags", None) or ()),
    )


def vessel_flies_words(world: Any, vessel: Any) -> str:
    """The lookout's words for a far vessel's flags beyond her ensign ('' when none, or when
    the words are not spoken)."""
    if not FLAGS_SPOKEN:
        return ""
    from freesail.world import signals as S

    c = S.vessel_locker(vessel).colours
    if not c.shows or not c.nation:
        return ""
    return flies_words(vessel_flies(world, vessel), getattr(world, "nations", None), c.nation)
