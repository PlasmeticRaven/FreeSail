"""The flags that fly, as the viewer draws them (docs/design/Design-ViewerAction.md §12).

The snapshot's `flags` is a list, each `{place, name, words, drawing}`: the place word (§12.2:
`peak`, `staff`, `<mast> truck`, `<mast> <piece> masthead`, `jackstaff`, `<mast> rigging`), the
flag's name, its words as the lookout reads them, and its drawing, a short list of coloured
rectangles in the flag's proportion. The nation's `colours.yaml` and the locker's list of what
flies where are 76's; until a locker carries that list, this serves, from 71's colours and
`data/nations.yaml`, one plain ensign at the peak while her colours show (the other nation's
under false colours, turned over under distress), the white of a flag of truce under `truce`
(74's state, by the lead's ruling of 2026-11-07), and nothing under `none` and `struck`.

Pure and read-only: the locker is read where the ship keeps one (`ship.extra["signals"]`) and
never made (`signals.locker_of` makes one on first asking, which a view must not do).
"""

from __future__ import annotations

from typing import Any

# A plain field in the proportion of hoist to fly (judgement, §12.1)
PLAIN_PROPORTION = (1.0, 2.0)
# The colours a flag's short word may name, first named first served (§12.1)
COLOUR_WORDS = ("red", "white", "blue", "yellow", "green", "black", "orange")
PLAIN_CLOTH = "cloth"  # a word naming no colour: the plain cloth's (style.css)
SHOWING = ("shown", "false", "distress")
TRUCE = "truce"
TRUCE_PLACE = "fore truck"  # where a flag of truce flies (data/signals/basic/colours.yaml)


def field_colour(flag_word: str) -> str:
    """The colour of the plain field a flag's short word names first ('the red ensign' red;
    'the white ensign with the arms' white); the plain cloth's where it names none."""
    words = flag_word.lower().replace(",", " ").split()
    for w in words:
        if w in COLOUR_WORDS:
            return w
    return PLAIN_CLOTH


def plain(colour: str, *, inverted: bool = False) -> dict[str, Any]:
    """A plain field's drawing: one rectangle over the whole flag (x along the fly, y down the
    hoist, each 0 to 1), turned over for the ensign union down."""
    d: dict[str, Any] = {
        "proportion": list(PLAIN_PROPORTION),
        "parts": [{"rect": [0.0, 0.0, 1.0, 1.0], "colour": colour}],
    }
    if inverted:
        d["inverted"] = True
    return d


def _nation(world: Any, nation_id: str) -> Any:
    nations = getattr(world, "nations", None)
    if nations is None or not nation_id:
        return None
    try:
        return nations.get(nation_id)
    except KeyError:
        return None


def _own_nation(world: Any) -> str:
    from freesail.world.signals import own_nation

    return own_nation(world)


def flags(world: Any, ship: Any) -> list[dict[str, Any]]:
    """What flies on `ship` (the player's), for the snapshot (§12.1)."""
    extra = getattr(ship, "extra", None)
    locker = extra.get("signals") if isinstance(extra, dict) else None
    listed = getattr(locker, "flies", None)  # 76's list of what flies where, when it lands
    if listed is not None:
        return [dict(f) for f in listed]
    colours = getattr(locker, "colours", None)
    state = getattr(colours, "state", "shown") if colours is not None else "shown"
    if state == TRUCE:
        # the white at the fore (package 98, step 3: the basic file's occasion `under truce`,
        # "the flag of truce at the fore"; the fallback had it at the peak)
        return [
            {
                "place": TRUCE_PLACE,
                "name": "flag of truce",
                "words": "a flag of truce",
                "drawing": plain("white"),
            }
        ]
    if state not in SHOWING:
        return []
    nation_id = (getattr(colours, "nation", "") if colours is not None else "") or _own_nation(
        world
    )
    nation = _nation(world, nation_id)
    if colours is not None and getattr(colours, "nation", ""):
        words = colours.words(getattr(world, "nations", None))
    else:
        from freesail.world.signals import Colours

        words = Colours(state=state, nation=nation_id).words(getattr(world, "nations", None))
    flag_word = getattr(nation, "flag", "") if nation is not None else ""
    if not flag_word and colours is not None:
        flag_word = getattr(colours, "flag", "")
    return [
        {
            "place": "peak",
            "name": "ensign",
            "nation": nation_id,
            "words": words,
            "drawing": plain(field_colour(flag_word or ""), inverted=state == "distress"),
        }
    ]


def hoists(world: Any, ship: Any) -> list[dict[str, Any]]:
    """The signals flying on `ship` (the player's: package 102, step 3), for the snapshot:
    each `{place, key, words, flags}`, `place` its place word (the order's or the private
    table's, else the main topgallant masthead, `flags.HOIST_PLACE`), `flags` its flags in
    order, the uppermost first, each `{name, words, drawing}` drawn as the colours are, by the
    scenario's year; a private reply's ensign as a hoist of its own at its place. Nothing for
    a hoist not yet broken out or hauled down, nor for the night's lights and the fog's guns.
    Pure and read-only, as `flags` is: the locker is read and never made. No other ship's
    signals are served (the owner's ruling of 2026-11-11 on the brief's step 3(c))."""
    from freesail.world import flags as F

    extra = getattr(ship, "extra", None)
    locker = extra.get("signals") if isinstance(extra, dict) else None
    if locker is None:
        return []
    clock = getattr(world, "clock", None)
    tick = int(getattr(clock, "tick", 0))
    try:
        year = int(clock.ship_time.year)
    except AttributeError:
        year = 1805
    out: list[dict[str, Any]] = []
    for h in locker.flying_now(tick):
        names = F.hoist_flags(h, tick)
        if not names:
            continue
        place = str(getattr(h, "place", "") or "")
        ensign_at = ""
        if h.book in ("private", "reply"):
            _, where, ensign_words = F.private_parts(h.shown)
            place = place or F.place_of_words(where)
            ensign_at = F.place_of_words(ensign_words) if ensign_words else ""
        flown = []
        for name in names:
            row = F.signal_flag(h.root, name, year)
            if row is None:
                continue  # every flag a hoist can hold is drawn (tools/check_signals.py)
            d = row.flag.served_drawing()
            d["kind"] = row.flag.kind
            flown.append({"name": name, "words": row.words, "drawing": d})
        if not flown:
            continue
        out.append(
            {
                "place": place or F.HOIST_PLACE,
                "key": h.key,
                "words": h.flags_words(),
                "flags": flown,
            }
        )
        if ensign_at:
            colours = getattr(locker, "colours", None)
            nation = str(getattr(colours, "nation", "") or "") or _own_nation(world)
            f = F.file_for_nation(getattr(world, "nations", None), nation)
            ensign = f.first_of("ensign", "navy")
            if ensign is not None and ensign.drawing:
                d = ensign.served_drawing()
                d["kind"] = "flag"
                out.append(
                    {
                        "place": ensign_at,
                        "key": h.key + ":ensign",
                        "words": "the ensign with the private signal",
                        "flags": [{"name": ensign.name, "words": ensign.words, "drawing": d}],
                    }
                )
    return out


def dressed(world: Any, ship: Any) -> list[dict[str, Any]]:
    """What the player's ship hangs where while she is dressed (package 102, step 4), for the
    snapshot: each place of the year's fashion with its flag (`flags.dressing_flies`), drawn
    as a hoist of one flag is; [] while she is not dressed. Pure and read-only."""
    extra = getattr(ship, "extra", None)
    locker = extra.get("signals") if isinstance(extra, dict) else None
    if locker is None or not getattr(locker, "dressed", False):
        return []
    from freesail.api import queries
    from freesail.world import flags as F

    colours = getattr(locker, "colours", None)
    nation = str(getattr(colours, "nation", "") or "") or _own_nation(world)
    try:
        year = int(world.clock.ship_time.year)
    except AttributeError:
        year = 1805
    return F.dressing_flies(
        queries.ship_graph(ship),
        getattr(world, "nations", None),
        nation,
        F.world_role(world),
        year,
    )
