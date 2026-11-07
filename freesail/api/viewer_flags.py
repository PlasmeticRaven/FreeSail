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
        return [
            {
                "place": "peak",
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
