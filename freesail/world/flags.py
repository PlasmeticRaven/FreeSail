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
from dataclasses import dataclass, field, replace
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
# package 102 (step 3): the yardarm places beside the mastheads: a mast's lower yard's arm
# ('main yardarm') or a named yard's ('fore topsail yardarm'), the arm to windward
# (JUDGEMENT, as the rigging's flags are drawn on the weather side). The 1796 book's private
# ships' table flies its first signal 'at the topsail or topgallant yard arm' (leaf 77, in
# ink) and the private tables name 'the fore yardarm' and 'the main yardarm'.
_YARDARM = re.compile(r"(fore|main|mizen)(?: (topsail|topgallant|royal))? yardarm")
# Where a hoist flies when no order and no book's practice names a place: 'at the main', the
# signal halyards at the main topgallant masthead (JUDGEMENT; the viewer falls back to the
# mast's truck where she has no such piece, Design-ViewerAction.md §12.2)
HOIST_PLACE = "main topgallant masthead"
# A hoist's place words as an order or a private table names them, to the place words
_PLACE_WORDS = {
    "mizen peak": "peak",
    "peak": "peak",
    "ensign staff": "staff",
    "the ensign staff": "staff",
}

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
    """Whether `word` is one of 81's place words (package 102: or a yardarm's)."""
    return word in PLACES_FIXED or bool(_MASTHEAD.fullmatch(word)) or bool(_YARDARM.fullmatch(word))


def place_of_words(words: str) -> str:
    """The place word for a place as an order or a private table says it ('main topmast
    head' the main top masthead, 'mizen peak' the peak, 'ensign staff' the staff, 'the fore'
    the fore topgallant masthead, 'fore yardarm' as it is); '' for words naming none."""
    w = " ".join(str(words or "").lower().replace("-", " ").split())
    w = w.removeprefix("the ")
    if w in _PLACE_WORDS:
        return _PLACE_WORDS[w]
    m = re.fullmatch(r"(fore|main|mizen|mizzen) (top|topgallant|royal) ?mast ?head", w)
    if m:
        return f"{m.group(1).replace('mizzen', 'mizen')} {m.group(2)} masthead"
    if w in ("fore", "main", "mizen", "mizzen"):
        return f"{w.replace('mizzen', 'mizen')} topgallant masthead"
    w = w.replace("mizzen", "mizen").replace("yard arm", "yardarm")
    return w if place_ok(w) else ""


# Package 102 (step 1): the drawing's form widened by the least the plates ask. A part is a
# `rect` ([x0, y0, x1, y1]), a `line` ([[x, y], [x, y]] with a `width`, a share of the hoist),
# or a `poly` (three or more [x, y] points: a flag halved or quartered on the diagonal, a
# lozenge, a triangle, a bend's band), each coloured, on the flag's own square. A flag's
# `shape` is its outline: '' a plain rectangle (every flag before the package); 'swallowtail'
# cut from the fly to `cut` of its length at the middle (a cornet, a guidon: the 1796 book's
# leaf 28, the Naples plate of 1807, Audibert's Pl. 3); 'triangle' tapered to a point at the
# fly (the United States' repeaters, Preble 1894). A pendant keeps the taper the viewer gives
# a flag named a pendant.
SHAPES = ("", "swallowtail", "triangle")
# A swallow tail's cut, a share of the fly, where the drawing gives none (judgement, read off
# the plates: the 1796 cornet and Audibert's guidons are cut about a third of their length)
SWALLOWTAIL_CUT = 1 / 3


def _part_ok(p: Any) -> bool:
    """A part is exactly one of a rect, a line or a poly, coloured; a poly of three or more
    points on the flag's square."""
    if not isinstance(p, dict) or not p.get("colour"):
        return False
    if sum(k in p for k in ("rect", "line", "poly")) != 1:
        return False
    if "poly" in p:
        pts = p["poly"]
        return (
            isinstance(pts, list)
            and len(pts) >= 3
            and all(isinstance(q, list) and len(q) == 2 for q in pts)
        )
    return True


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
    shape: str = ""  # package 102: the outline (SHAPES); '' the plain rectangle
    cut: float = 0.0  # a swallow tail's cut, a share of the fly; 0 the default's

    def served_drawing(self, inverted: bool = False) -> dict[str, Any]:
        """The drawing as the snapshot serves it to 81's viewer: `{proportion, parts}` with the
        rectangles in `parts` and the lines apart under `lines` (81 draws a part with no
        `rect` as the whole field), each with `n`, its place in the drawing, so that the
        viewer paints them in the drawing's order (package 98, step 3: the Union's crosses
        over its saltires). Package 102: the polygons apart under `polys`, and the outline
        under `shape` (with its `cut`), each only where the flag has one, so that every
        drawing from before is served as it was."""
        parts = [{**p, "n": i} for i, p in enumerate(self.drawing) if "rect" in p]
        lines = [{**p, "n": i} for i, p in enumerate(self.drawing) if "line" in p]
        polys = [{**p, "n": i} for i, p in enumerate(self.drawing) if "poly" in p]
        d: dict[str, Any] = {"proportion": list(self.proportion), "parts": parts}
        if lines:
            d["lines"] = lines
        if polys:
            d["polys"] = polys
        if self.shape:
            d["shape"] = self.shape
            if self.shape == "swallowtail":
                d["cut"] = self.cut or SWALLOWTAIL_CUT
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
            if not _part_ok(p):
                raise BookFileError(
                    f"{path}: flag {name!r}: a part is a rect, a line or a poly, coloured"
                )
            drawing.append(dict(p))
        shape = str(f.get("shape") or "")
        if shape not in SHAPES:
            raise BookFileError(f"{path}: flag {name!r}: shape is one of {SHAPES}")
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
            shape=shape,
            cut=float(f.get("cut") or 0.0),
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

    locker = S.vessel_locker(vessel)
    c = locker.colours
    if not c.shows or not c.nation:
        return ""
    words = flies_words(vessel_flies(world, vessel), getattr(world, "nations", None), c.nation)
    if getattr(locker, "dressed", False):
        # package 102 (step 4): a ship dressed, as the lookout sees her
        words = "; ".join(w for w in (words, "she is dressed in her flags") if w)
    return words


# ---------------------------------------------------------------------------
# Package 102 (step 2): the signal flags of every book, drawn
# ---------------------------------------------------------------------------

SIGNAL_FLAGS_FILE = "flags.yaml"
# How a flag's drawing was had: from a page image of the period's or of Perrin's plates
# (`plate`), or the builder's own from the book's words or from nothing (`made`)
MARKS = ("plate", "made")
# A signal flag is a flag or a pendant (a pendant drawn tapering, as the colours' pendant is)
SIGNAL_KINDS = ("flag", "pendant")


@dataclass(frozen=True)
class SignalFlag:
    """One drawing of a signal flag: its name in the root's file (the name a hoist holds),
    its words, its drawing in the colours' form, the years it was flown by that drawing (one
    flag may have several, each its own row: Britain's numerals changed in 1793, 1799 and
    1803), whether it was drawn from a plate or made, and its source by leaf."""

    name: str
    words: str
    flag: Flag  # the drawing, in colours.yaml's form (its kind 'pendant' for a pendant's taper)
    dates: str
    mark: str
    source: str

    def flown_in(self, year: int) -> bool:
        return _in_dates(self.dates, year)


def _in_dates(dates: str, year: int) -> bool:
    """Whether `year` falls in "1799-1803", "1804-", "-1792", "1805" or "" (always)."""
    d = str(dates or "").strip()
    if not d:
        return True
    lo, sep, hi = d.partition("-")
    if not sep:
        return int(lo) == year
    return (not lo or year >= int(lo)) and (not hi or year <= int(hi))


def _dates_distance(dates: str, year: int) -> int:
    """How many years `year` lies outside the dates (0 within them)."""
    d = str(dates or "").strip()
    if not d:
        return 0
    lo, sep, hi = d.partition("-")
    lo_y = int(lo) if lo else -(10**6)
    hi_y = (int(hi) if hi else 10**6) if sep else lo_y
    return max(0, lo_y - year, year - hi_y)


@dataclass(frozen=True)
class SignalFlagsFile:
    root: str
    sources: tuple[str, ...]
    rows: tuple[SignalFlag, ...]

    def names(self) -> set[str]:
        return {r.name for r in self.rows}

    def drawing_of(self, name: str, year: int) -> SignalFlag | None:
        """The flag's drawing in `year`: the row whose dates hold it, else the nearest (a
        world on a day the data does not date answers with the nearest picture and does not
        refuse: decision 66); None where the file has no such flag."""
        rows = [r for r in self.rows if r.name == name]
        if not rows:
            return None
        return min(rows, key=lambda r: (_dates_distance(r.dates, year), -_first_year(r.dates)))


def _first_year(dates: str) -> int:
    lo = str(dates or "").partition("-")[0].strip()
    return int(lo) if lo else 0


@cache
def load_signal_flags(root: str = "basic", base: str | None = None) -> SignalFlagsFile:
    """A root's signal flags (`data/signals/<root>/flags.yaml`), read once; a root with no
    file has none of its own (the basic root's are read after it, `signal_flag`)."""
    folder = (Path(base) if base else SIGNALS_DIR) / root
    path = folder / SIGNAL_FLAGS_FILE
    if not path.exists():
        return SignalFlagsFile(root=root, sources=(), rows=())
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    colours = None
    rows = []
    for i, f in enumerate(raw.get("flags") or []):
        if not isinstance(f, dict) or not f.get("name"):
            raise BookFileError(f"{path}: flag {i + 1} wants a name")
        name = str(f["name"])
        mark = str(f.get("mark") or "")
        if mark not in MARKS:
            raise BookFileError(f"{path}: flag {name!r}: mark is one of {MARKS}, not {mark!r}")
        if not f.get("source"):
            raise BookFileError(f"{path}: flag {name!r} wants its source")
        same = str(f.get("same") or "")
        if same:
            # the drawing of a flag of the colours (the union jack, an ensign)
            colours = colours or load_colours(root, base)
            if same not in colours.flags:
                raise BookFileError(f"{path}: flag {name!r}: the colours have no {same!r}")
            drawn = colours.flags[same]
        else:
            kind = str(f.get("kind") or "flag")
            if kind not in SIGNAL_KINDS:
                raise BookFileError(f"{path}: flag {name!r}: kind is one of {SIGNAL_KINDS}")
            # read in the colours' form (its parts, its shape), then given its own kind
            one = _file({"flags": [{**f, "kind": "truce"}]}, path, root).flags[name]
            drawn = replace(one, kind=kind)
        rows.append(
            SignalFlag(
                name=name,
                words=str(f.get("words") or name),
                flag=drawn,
                dates=str(f.get("dates") or ""),
                mark=mark,
                source=str(f["source"]),
            )
        )
    for r in rows:
        if r.dates:
            lo, _, hi = r.dates.partition("-")
            for y in (lo, hi):
                if y and not y.strip().isdigit():
                    raise BookFileError(f"{path}: flag {r.name!r}: dates {r.dates!r} not years")
    return SignalFlagsFile(
        root=root, sources=tuple(str(s) for s in raw.get("sources") or []), rows=tuple(rows)
    )


def signal_flag(root: str, name: str, year: int) -> SignalFlag | None:
    """A signal flag's drawing in `year`, from the root's own file and, failing it, the basic
    root's (the private tables' plain flags are drawn once there)."""
    found = load_signal_flags(root).drawing_of(name, year)
    if found is None and root != "basic":
        found = load_signal_flags("basic").drawing_of(name, year)
    return found


# The names a hoist's flags go by in every root's flags.yaml
NUMERAL = "numeral {}"  # 'numeral 1' ... 'numeral 0'
SUBSTITUTES = ("substitute", "second substitute", "third substitute")
TABLE_FLAG = "table flag {}"  # 'table flag 1' ... 'table flag 20' (France, Spain)
# a repeated table flag: Mazarredo's universal flag "igual á todas" (the plan), Audibert's
# zero "égal à tous" (Pl. 3): the one flag that stands for the flag it flies with
UNIVERSAL = "universal flag"
ANSWERING = "answering pendant"
TELEGRAPH = "telegraph flag"
HUNDRED = "hundred pendant"
THOUSAND = "thousand pendant"
ADDED = "added pendant"  # Spain's: the signals added below the table (book.yaml), JUDGEMENT
# The private signal's words: 'a blue pendant at the fore yardarm' (each root's private.yaml)
_PRIVATE = re.compile(
    r"^an? (?P<flag>.+?) at the (?P<place>[a-z ]+?)"
    r"(?:, with the ensign at the (?P<ensign>[a-z ]+))?$"
)


def _digits(number: int, units_first: bool = False) -> list[str]:
    """A number as numeral flags, the first written figure uppermost (the 1796 book, leaf 31:
    "the one answering to the Figure in any Number placed first in Writing, will be always
    hoisted uppermost"); Barry's book the units uppermost (his Essay, No. 214 by the red for
    the unit over the blue for the tens over the yellow for the hundreds). A figure a second
    time the substitute, a third time the second substitute (Perrin p. 178: "one or two
    substitute flags"; the United States' three repeaters)."""
    figures = list(str(int(number)))
    if units_first:
        figures.reverse()
    out: list[str] = []
    seen: dict[str, int] = {}
    for f in figures:
        n = seen.get(f, 0)
        seen[f] = n + 1
        out.append(NUMERAL.format(f) if n == 0 else SUBSTITUTES[min(n - 1, 2)])
    return out


def numerary_flags(root: str, number: int) -> list[str]:
    """The flags of a numbered signal in a book of the numerary form, uppermost first."""
    if root == "united-states":
        return _digits(number, units_first=True)
    if root == "britain" and int(number) == 111:
        # the hundred pendant over 1 and the substitute (the 1796 book, leaf 31: the pendant
        # "adds 100 to the Expression assigned to the Numeral Flag or Flags with which it is
        # at the same Time hoisted"), the one set of numerals holding no third 1
        return [HUNDRED, *_digits(11)]
    return _digits(number)


def table_flags(root: str, number: int) -> list[str]:
    """The flags of a numbered signal in a book of the table form (France's, Spain's), the
    upper over the lower: the cell's row the upper and its column the lower, twenty to a row
    (JUDGEMENT: Audibert § 71 reads the cell by the upper flag's row and the lower's column
    and gives no numbering; the rows taken in order); the lower the universal where it would
    be the upper again. Spain: 401 to 420 one flag alone (Mazarredo's signals of one flag),
    421 the universal alone (the annulment), and the meanings added after (made) the added
    pendant over one flag (JUDGEMENT on the book's "pendants outside the table, for the
    signals added below")."""
    n = int(number)
    if root == "spain" and 400 < n <= 420:
        return [TABLE_FLAG.format(n - 400)]
    if root == "spain" and n == 421:
        return [UNIVERSAL]
    if root == "spain" and n > 421:
        return [ADDED, TABLE_FLAG.format((n - 421 - 1) % 20 + 1)]
    upper, lower = (n - 1) // 20 % 20 + 1, (n - 1) % 20 + 1
    return [TABLE_FLAG.format(upper), UNIVERSAL if lower == upper else TABLE_FLAG.format(lower)]


def telegraphic_word_flags(number: int) -> list[str]:
    """Popham's word: its numerals under the telegraph flag; a number of the thousands with a
    pendant over the hoist (Perrin p. 178: "numbers between 1000 and 2000 by a ball or pendant
    placed above the hoist ... and numbers above 2000 by a similar ball or pendant placed
    below"; which pendant not read: JUDGEMENT, `thousand pendant`)."""
    n = int(number)
    if n >= 2000:
        return [TELEGRAPH, *_digits(n % 1000), THOUSAND]
    if n >= 1000:
        return [TELEGRAPH, THOUSAND, *_digits(n % 1000)]
    return [TELEGRAPH, *_digits(n)]


def private_parts(shown: str) -> tuple[str, str, str]:
    """(the flag's words, its place's words, the ensign's place's words or '') from a private
    signal's words ('a blue pendant at the fore yardarm, with the ensign at the mizen peak');
    ('', '', '') when the words are none of that form (a light by night)."""
    m = _PRIVATE.match(str(shown or "").strip())
    if not m:
        return "", "", ""
    return m.group("flag"), m.group("place"), m.group("ensign") or ""


def hoist_flags(hoist: Any, tick: int | None = None) -> list[str]:
    """The names of the flags a hoist holds, uppermost first, as its root's flags.yaml names
    them: the numerals of its number (the first number: the lookout's words count those), two
    table flags a number in a table book, the telegraph flag over the word now flying, the
    answering pendant, the private signal's flag; [] for the night's lights and the fog's guns,
    which are no flags."""
    book = str(getattr(hoist, "book", ""))
    root = str(getattr(hoist, "root", "basic") or "basic")
    numbers = tuple(getattr(hoist, "numbers", ()) or ())
    if book in ("numerary", "convoy") and numbers:
        if str(getattr(hoist, "form", "numerary")) == "table":
            out: list[str] = []
            for n in numbers:
                out += table_flags(root, n)
            return out
        return numerary_flags(root, numbers[0])
    if book == "telegraphic" and numbers:
        # a word a hoist, each a hoist's minute after the one before (`_telegraphic`), the
        # word before hauled down as the next goes up; the last kept until the whole comes down
        i = len(numbers) - 1
        if tick is not None and len(numbers) > 1:
            first = int(getattr(hoist, "breaks_out", 0))
            step = max(1, (int(getattr(hoist, "done_at", first)) - first) // (len(numbers) - 1))
            i = max(0, min(len(numbers) - 1, (int(tick) - first) // step))
        return telegraphic_word_flags(numbers[i])
    if book == "answer":
        return [ANSWERING]
    if book in ("private", "reply"):
        flag, _, _ = private_parts(str(getattr(hoist, "shown", "")))
        return [flag] if flag else []
    return []


# ---------------------------------------------------------------------------
# Package 102 (step 4): dressing ship
# ---------------------------------------------------------------------------

DRESSING_FILE = "dressing.yaml"
SLOTS = ("yardarms", "stays", "rigging", "line", "mastheads")
STOCKS = ("ensigns", "signal flags", "pendants")
YARDS = ("lower", "topsail", "topgallant", "royal")
STAY_LEVELS = ("lower", "topmast", "topgallant")


@dataclass(frozen=True)
class Fashion:
    name: str
    words: str
    dates: str
    source: str
    hang: tuple[dict[str, Any], ...]


@cache
def load_dressing(root: str = "basic", base: str | None = None) -> tuple[Fashion, ...]:
    """A root's fashions of dressing ship, its own file's or else basic's."""
    folder = (Path(base) if base else SIGNALS_DIR) / root
    path = folder / DRESSING_FILE
    if not path.exists():
        if root == "basic":
            return ()
        return load_dressing("basic", base)
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = []
    for i, f in enumerate(raw.get("fashions") or []):
        name = str(f.get("name") or "")
        if not name or not f.get("source"):
            raise BookFileError(f"{path}: fashion {i + 1} wants a name and a source")
        hang = []
        for s in f.get("hang") or []:
            if str(s.get("at")) not in SLOTS:
                raise BookFileError(f"{path}: fashion {name!r}: a slot is at one of {SLOTS}")
            bad = [x for x in s.get("flags") or [] if x not in STOCKS]
            if bad or not s.get("flags"):
                raise BookFileError(f"{path}: fashion {name!r}: flags are of {STOCKS}")
            if s["at"] == "line":
                for w in s.get("through") or []:
                    if not place_ok(str(w)):
                        raise BookFileError(f"{path}: fashion {name!r}: {w!r} is no place word")
            hang.append(dict(s))
        out.append(
            Fashion(
                name=name,
                words=str(f.get("words") or name),
                dates=str(f.get("dates") or ""),
                source=str(f["source"]),
                hang=tuple(hang),
            )
        )
    return tuple(out)


def fashion_for(root: str, year: int) -> Fashion | None:
    """The fashion of `year`: the row whose dates hold it, else the nearest earlier one (a
    later fashion is never flown before its date; decision 66's nearest picture otherwise)."""
    rows = load_dressing(root)
    within = [f for f in rows if _in_dates(f.dates, year)]
    if within:
        return within[0]
    earlier = [f for f in rows if _first_year(f.dates) <= year]
    if earlier:
        return min(earlier, key=lambda f: _dates_distance(f.dates, year))
    return min(rows, key=lambda f: _dates_distance(f.dates, year)) if rows else None


def _served(drawn: Flag, name: str, words: str) -> dict[str, Any]:
    d = drawn.served_drawing()
    d["kind"] = "pendant" if drawn.kind in ("pendant", "broad pendant") else "flag"
    return {"name": name, "words": words, "drawing": d}


def dressing_stock(
    nations: Any, nation: str, role: str, year: int
) -> dict[str, list[dict[str, Any]]]:
    """Her flags for dressing, by stock: her nation's ensigns (of her service; the other
    squadrons' too for a King's ship) and her jack; her book's signal flags of the year (a
    King's ship's, in the file's order); her signal pendants, then her colours' pendant. A
    flag her data lacks (another nation's ensign, which the period hung too: Perrin p. 197)
    is not there: package 96's locker."""
    f = file_for_nation(nations, nation)
    rl = colour_role(role)
    navy = rl in ("kings ship", "commodore", "admiral")
    service = "navy" if navy else "merchant" if rl == "merchant" else "privateer"
    ensign_kind = "ensign" if navy or rl == "privateer" else "merchant ensign"
    ensigns = [
        _served(g, g.name, g.words)
        for g in f.flags.values()
        if g.drawing
        and (
            (g.kind == ensign_kind and (navy or g.service in (service, "any")))
            or (g.kind == "jack" and g.service in (service, "any"))
        )
    ]
    signal_flags: list[dict[str, Any]] = []
    pendants: list[dict[str, Any]] = []
    if navy:
        root = f.nation if f.nation != "basic" else "basic"
        try:
            root = str(nations.get(nation).signals_root or "basic") if nations is not None else root
        except KeyError:
            root = "basic"
        seen: set[str] = {x["name"] for x in ensigns}  # one of each: the jack is one flag
        for row in load_signal_flags(root).rows:
            if row.name in seen:
                continue
            seen.add(row.name)
            drawn = load_signal_flags(root).drawing_of(row.name, year)
            if drawn is None:
                continue
            item = _served(drawn.flag, row.name, drawn.words)
            (pendants if drawn.flag.kind == "pendant" else signal_flags).append(item)
    own_pendant = f.first_of("pendant", service)
    if own_pendant is not None and own_pendant.drawing and navy:
        pendants.append(_served(own_pendant, own_pendant.name, own_pendant.words))
    return {"ensigns": ensigns, "signal flags": signal_flags, "pendants": pendants}


def dressing_slots(graph: dict[str, Any], fashion: Fashion) -> list[tuple[dict[str, Any], dict]]:
    """Each place the fashion hangs a flag on this ship (her graph's yards, stays and masts),
    in the fashion's order, with its slot: [(where, slot)], `where` `{place, side}` (a
    yardarm's or the shrouds' side, 1 starboard, -1 larboard), `{stay, along}` (a stay's line
    id and how far down it from its head), `{place, to, along}` (along a span between two
    place words) or `{place}`."""
    spars = {s["id"]: s for s in graph.get("spars") or []}
    lower = [s for s in spars.values() if s.get("class") == "mast" and not s.get("parent")]
    lower.sort(key=lambda s: -float(s.get("x_m") or 0.0))  # the foremost first
    word = {
        s["id"]: ("mizen" if s["id"].split(".")[0] == "mizzen" else s["id"].split(".")[0])
        for s in lower
    }
    if len(lower) == 1:
        word[lower[0]["id"]] = "main"

    def mast_of(sid: str) -> dict | None:
        s = spars.get(sid)
        while s is not None and s.get("parent"):
            s = spars.get(s["parent"])
        return s

    out: list[tuple[dict[str, Any], dict]] = []
    for slot in fashion.hang:
        at = slot["at"]
        if at == "yardarms":
            for m in lower:
                for kind in slot.get("yards") or ["lower"]:
                    for y in spars.values():
                        if y.get("class") != "yard" or mast_of(y["id"]) is not m:
                            continue
                        if (kind == "lower" and y.get("parent") == m["id"]) or (
                            kind != "lower" and f".{kind}." in y["id"]
                        ):
                            place = (
                                f"{word[m['id']]} yardarm"
                                if kind == "lower"
                                else f"{word[m['id']]} {kind} yardarm"
                            )
                            out += [({"place": place, "side": s}, slot) for s in (1, -1)]
                            break
        elif at == "stays":
            n = int(slot.get("flags_each") or 1)
            for ln in graph.get("lines") or []:
                if ln.get("class") != "stay":
                    continue
                of = spars.get(str(ln.get("of")))
                if (
                    of is None
                    or mast_of(of["id"]) is None
                    or of.get("class")
                    not in (
                        "mast",
                        "topmast",
                        "topgallant_mast",
                    )
                ):
                    continue
                level = {"mast": "lower", "topmast": "topmast", "topgallant_mast": "topgallant"}[
                    of["class"]
                ]
                if level not in (slot.get("stays") or ["lower"]):
                    continue
                out += [({"stay": ln["id"], "along": (k + 1) / (n + 1)}, slot) for k in range(n)]
        elif at == "rigging":
            for m in lower:
                out += [({"place": f"{word[m['id']]} rigging", "side": s}, slot) for s in (1, -1)]
        elif at == "line":
            through = [str(w) for w in slot.get("through") or []]
            n = int(slot.get("flags_each") or 1)
            for a, b in zip(through, through[1:], strict=False):
                out += [({"place": a, "to": b, "along": (k + 1) / (n + 1)}, slot) for k in range(n)]
        elif at == "mastheads":
            out += [({"place": f"{word[m['id']]} truck"}, slot) for m in lower]
    return out


def dressing_flies(
    graph: dict[str, Any], nations: Any, nation: str, role: str, year: int
) -> list[dict[str, Any]]:
    """What a dressed ship hangs where, as the snapshot serves it (`dressed`): each place of
    the year's fashion with the next flag of its stocks, `{..where, flags: [flag]}`; places
    left empty when her stock is spent."""
    fashion = fashion_for("basic" if nations is None else _root_of(nations, nation), year)
    if fashion is None:
        return []
    stock = dressing_stock(nations, nation, role, year)
    taken = {k: 0 for k in STOCKS}
    out = []
    for where, slot in dressing_slots(graph, fashion):
        flag = None
        for kind in slot["flags"]:
            if taken[kind] < len(stock[kind]):
                flag = stock[kind][taken[kind]]
                taken[kind] += 1
                break
        if flag is not None:
            out.append({**where, "flags": [flag]})
    return out


def _root_of(nations: Any, nation: str) -> str:
    try:
        return str(nations.get(nation).signals_root or "basic")
    except (KeyError, AttributeError):
        return "basic"


# ---------------------------------------------------------------------------
# Package 102 (step 5): the nations' days
# ---------------------------------------------------------------------------

DAYS_FILE = "days.yaml"


@dataclass(frozen=True)
class Day:
    name: str
    month: int
    day: int
    years: str
    does: tuple[str, ...]
    guns: int
    source: str

    def kept(self, when: Any) -> bool:
        return (
            int(when.month) == self.month
            and int(when.day) == self.day
            and _in_dates(self.years, int(when.year))
        )


@cache
def load_days(root: str, base: str | None = None) -> tuple[Day, ...]:
    """A root's days (`data/signals/<root>/days.yaml`); none where the root has no file."""
    path = (Path(base) if base else SIGNALS_DIR) / root / DAYS_FILE
    if not path.exists():
        return ()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    out = []
    for i, d in enumerate(raw.get("days") or []):
        m = re.fullmatch(r"(\d\d)-(\d\d)", str(d.get("date") or ""))
        if not d.get("name") or not m or not d.get("source"):
            raise BookFileError(f"{path}: day {i + 1} wants a name, a date (MM-DD) and a source")
        does = tuple(str(x) for x in d.get("does") or [])
        if not set(does) <= {"dress"}:
            raise BookFileError(f"{path}: day {d['name']!r}: what is done is of ('dress',)")
        out.append(
            Day(
                name=str(d["name"]),
                month=int(m.group(1)),
                day=int(m.group(2)),
                years=str(d.get("years") or ""),
                does=does,
                guns=int(d.get("guns") or 0),
                source=str(d["source"]),
            )
        )
    return tuple(out)


def days_on(root: str, when: Any) -> list[Day]:
    """The root's days kept on `when` (a date or datetime), in their years."""
    return [d for d in load_days(root) if d.kept(when)]


def _vessel_root(world: Any, vessel: Any) -> str:
    nation = str(getattr(vessel, "nation", "") or "")
    return _root_of(getattr(world, "nations", None), nation) if nation else "basic"


def _harbour_dressing(world: Any, daylight: bool) -> None:
    """The ships of the sea lying at anchor under a rules captain dress of themselves by day
    on a day their nation keeps (in its years), and undress at sunset and the day after
    (package 102, step 5); never logged, read by the lookout with their flags. A ship under
    way, or one with her colours down, does not."""
    sea = getattr(world, "vessels", None)
    own = getattr(world, "vessel", None)
    now = world.clock.ship_time
    from freesail.world import signals as S

    mine = S.own_id(world)
    for v in getattr(sea, "vessels", None) or []:
        if v is own or str(getattr(v, "id", "")) == mine:
            continue
        locker = getattr(v, "signals", None)
        at_anchor = str(getattr(v, "sail_state", "")) == "at anchor"
        ruled = getattr(v, "brain", None) is not None
        want = False
        if at_anchor and ruled and daylight:
            if any("dress" in d.does for d in days_on(_vessel_root(world, v), now)):
                locker = locker or S.vessel_locker(v)
                want = locker.colours.shows and locker.colours.state == "shown"
        if locker is not None and bool(getattr(locker, "dressed", False)) != want:
            locker.dressed = want
            locker.dressed_since = int(world.clock.tick) if want else 0


def _the_day_reminded(world: Any, locker: Any) -> None:
    """The ship's own officer (`officer_rank`: the first lieutenant in a frigate, the
    lieutenant in a brig-sloop, the mate in a cutter, a schooner or a trader) reminds the
    captain once, on the morning of a day his nation keeps and his ship lying at anchor, that
    the ships in harbour will dress; the order is his (package 102, step 5). Where a party is
    seated at the officer's station no words are put in his mouth: the day is said to the deck
    with no speaker, for him to say to the captain himself (no line spoken as the officer had
    a rule for a seated one before; the lead's word of 2026-11-13). The locker keeps the day
    said, so that it is said once."""
    from freesail.agents.agent import OFFICER, officer_rank
    from freesail.agents.harness import holder_of
    from freesail.world import signals as S

    if not bool(getattr(world, "at_anchor", False)) or S.light_now(world) == "night":
        return
    now = world.clock.ship_time
    stamp = f"{now.year:04d}-{now.month:02d}-{now.day:02d}"
    if getattr(locker, "day_said", "") == stamp:
        return
    days = [d for d in days_on(S.books_for(world).root, now) if "dress" in d.does]
    if not days:
        return
    locker.day_said = stamp
    day = days[0].name
    if holder_of(world, OFFICER) is not None:
        text = f"It is {day}: the ships in harbour will be dressing."
        world.record("notable", "colours.day", text, data={"day": day})
        return
    who = officer_rank(world)[0]
    who = who[:1].upper() + who[1:]
    text = (
        f"{who}: 'It is {day}, sir: the ships in harbour will be dressing.' The order to "
        "dress her is yours ('dress ship')."
    )
    world.record("notable", "officer.reminder", text, data={"day": day, "person": who})


def dressing_tick(world: Any) -> None:
    """Once a minute with the look (package 102, step 4): the player's ship dressed undresses
    at sunset (the period's colours came down at sunset, Spavens 1796 as Perrin prints it;
    that the dressing came with them JUDGEMENT, as Luce 1884 has it) and when her colours
    come down, said in the log. Nothing while she is not dressed."""
    from freesail.world import signals as S

    night = S.light_now(world) == "night"
    _harbour_dressing(world, not night)
    ship = getattr(world, "ship", None)
    extra = getattr(ship, "extra", None)
    locker = extra.get("signals") if isinstance(extra, dict) else None
    if locker is None:
        return
    _the_day_reminded(world, locker)
    if not getattr(locker, "dressed", False):
        return
    down = locker.colours.state in ("none", "struck", "distress", "truce")
    if not (down or night):
        return
    locker.dressed, locker.dressed_since = False, 0
    text = (
        "Sunset: the dressing hauled down with the colours, and the flags stowed."
        if night and not down
        else "The dressing hauled down: a ship is not dressed with her colours down."
    )
    world.record("routine", "colours.undressed", text, data={"by": "the watch"})
