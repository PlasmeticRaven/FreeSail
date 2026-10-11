"""The chart and the ship's view as pictures (spec M6 §13, the second paragraph; the owner's
note 7 of 2026-10-09 and his word of 2026-10-10; package 42, item 4).

**The lead's design decision:** the open browser renders the picture as the player sees
it and posts it to the server on the tool's request, since the chart's drawing lives in
`client/map.js` and the ship's in the viewer (`client/projection.js`, `shipview.js`), and
a second renderer in Python would be a second picture to keep true. So the game asks a
**painter**, which the browser's server registers for its World (`set_painter`): one
request from the server to the open page for a rendering, at an angle for the ship, and
one post back, the picture's size bounded (`MAX_BYTES`, `MAX_PX`). Where no page is open
(the console, a server with no browser on it, a replay), the tool says so in words and
gives the readings the picture would have shown instead (`CHART_WORDS`, `SHIP_WORDS`:
the ship's state readings are the words of the view, which the station has).

**Shelved as the library is.** A picture is a book (`tools.book_of`): its result in the
conversation is its handle, its words and the picture's id; a door that carries images
(the MCP bridge, the API door) fetches the picture by its id from the game and shows it,
and once the book is shelved, or goes back after its turns, the result is its line and
the picture is no longer sent. The picture itself is held by the painter in memory, the
newest `KEPT` of them, and never enters the journal, the transcript, a save or the log; a
note that it was shown, with its size and the angle asked, is kept in the transcript with
the reply that asked it (`Harness`, "shown").

The tools that make pictures (`tools.PICTURE_TOOLS`) are offered only at the doors that
carry an image (`tools.PICTURE_DOORS`): the local runner's models read words.

**Package 45.** The page draws each picture on an offscreen canvas of a fixed size that
owes nothing to its layout (`client/app.js`: the chart 1200 by 900, the ship's view 960
by 720, scaled to `MAX_PX`), with the picture's own background; the chart is centred on
the account at a **span** (`SPANS`: `harbour`, two miles across; `coast`, twenty;
`passage`, a hundred and fifty; `whole`, the chart's envelope), or at the page's own view
when none is said, and the tool's words say which. A shelved picture's stub says what it
was and that it was shown (`harness.Harness._stub`), since a model reading its own
history with the picture gone from it concluded it had never seen one (the owner's
wardroom run of gate m6a).
"""

from __future__ import annotations

import weakref
from dataclasses import dataclass
from typing import Any, Protocol

__all__ = [
    "CHART",
    "MAX_BYTES",
    "MAX_PX",
    "SHIP",
    "Painter",
    "Picture",
    "SPANS",
    "SPAN_WORDS",
    "facing_of",
    "paint",
    "painter_of",
    "set_painter",
    "span_of",
]

CHART = "chart"
SHIP = "ship"

# The chart picture's spans (package 45): miles across the shorter way, centred on the
# account; "whole" is the chart's envelope, which the page works from the chart's bounds.
# Judgement: a harbour's approach, a day's coast, a passage's leg, and the chart as built.
SPANS: dict[str, float | None] = {"harbour": 2.0, "coast": 20.0, "passage": 150.0, "whole": None}
SPAN_WORDS: dict[str, str] = {
    "harbour": "the harbour span, two miles across",
    "coast": "the coast span, twenty miles across",
    "passage": "the passage span, a hundred and fifty miles across",
    "whole": "the whole chart as built",
    "": "the page's own view",
}

# The bound on a picture (judgement: a chart or a ship's view at the page's own size is a
# few hundred kilobytes as a PNG; the Messages API takes an image of five megabytes, and a
# picture past a megabyte and a half costs more context than it shows). The page scales
# its picture so that its longer side is at most `MAX_PX` (the size above which the API
# scales an image down itself) and the server refuses a post larger than `MAX_BYTES`.
MAX_BYTES = 1_500_000
MAX_PX = 1568

# How long the tool waits for the page's picture, in real seconds (judgement: a page draws
# its chart in tens of milliseconds and the ship's view in a little more; five seconds is
# a page that is open but not drawing, a tab in the background).
PAINT_WAIT_S = 5.0

# The pictures the painter keeps for the doors to fetch (judgement: a station shelves a
# picture within its three turns; several stations at once, each with a few, fit in this).
KEPT = 24

# The media types a page may post.
MEDIA_TYPES: tuple[str, ...] = ("image/png", "image/jpeg", "image/webp")

# The readings each picture would show, given in its place where no page is open.
CHART_WORDS: tuple[str, ...] = (
    "reckoning",
    "reckoning_uncertainty",
    "heading",
    "course",
    "speed",
    "variation",
    "land",
    "nearest_land",
    "depth_of_water",
    "dangers",
    "in_sight",
    "sail_in_sight",
)
SHIP_WORDS: tuple[str, ...] = (
    "heading",
    "heel",
    "apparent_wind_angle",
    "apparent_wind_speed",
    "true_wind_from",
    "true_wind_speed",
    "helm",
    "sea",
    "motion",
    "manoeuvre_in_hand",
    "work_in_hand",
    "sails",
)


@dataclass(frozen=True)
class Picture:
    """A picture the page posted: its id, its media type and bytes, its size in pixels,
    which view it is and from where, and the ship's time it was asked at."""

    id: str
    media_type: str
    data: bytes
    width: int
    height: int
    view: str
    facing: str
    stamp: str
    span: str = ""  # the chart's span (package 45): a key of SPANS, or "" for the page's view

    def note(self) -> dict[str, Any]:
        """What is kept of it in the transcript: everything but the picture."""
        return {
            "id": self.id,
            "view": self.view,
            "facing": self.facing,
            "media_type": self.media_type,
            "bytes": len(self.data),
            "width": self.width,
            "height": self.height,
            "stamp": self.stamp,
            **({"span": self.span} if self.view == CHART else {}),
        }

    def title(self) -> str:
        """The short name of the picture, for its book's handle and its stub."""
        if self.view == CHART:
            return f"the chart at {self.stamp} ({SPAN_WORDS.get(self.span, self.span)})"
        return f"the ship's view from {self.facing} at {self.stamp}"

    def words(self) -> str:
        if self.view == CHART:
            what = (
                "The chart by the ship's account, the ship at the centre, "
                f"{SPAN_WORDS.get(self.span, self.span)} (the scale bar is drawn on it)"
            )
        else:
            what = f"The ship as the viewer shows her, seen from {self.facing}"
        return (
            f"{what}, at {self.stamp}: a picture of {self.width} by {self.height} pixels. It "
            "is a book: shelve puts it back, and it goes back by itself after three of your "
            "turns; once put back, your conversation holds a line saying you were shown it, "
            "and asking again draws a fresh one."
        )


class Painter(Protocol):
    def paint(self, view: str, facing: str, stamp: str, span: str = "") -> Picture | str:
        """A picture of the view, or the words why there is none."""
        ...

    def get(self, picture_id: str) -> Picture | None: ...


_PAINTERS: weakref.WeakKeyDictionary[Any, Painter] = weakref.WeakKeyDictionary()


def set_painter(world: Any, painter: Painter | None) -> None:
    """The driver's painter for its World (the browser's server); None takes it away. Kept
    beside the World and not on it, so that a save or a checkpoint never holds it."""
    if painter is None:
        _PAINTERS.pop(world, None)
    else:
        _PAINTERS[world] = painter


def painter_of(world: Any) -> Painter | None:
    return _PAINTERS.get(world)


def facing_of(words: str) -> tuple[float | None, str]:
    """Where the viewer stands, from the tool's words: degrees from the bow, clockwise (0
    right ahead, 90 the starboard beam, 180 right astern, 270 the larboard beam), or one
    of those names; "" or 'leeward' for abeam to leeward, the viewer's own default. The
    degrees (None for leeward) and the words for it. Refused in words otherwise."""
    w = " ".join(str(words or "").lower().replace("°", " ").split()).removesuffix(" degrees")
    named = {
        "ahead": 0.0,
        "right ahead": 0.0,
        "the bow": 0.0,
        "starboard beam": 90.0,
        "the starboard beam": 90.0,
        "starboard": 90.0,
        "astern": 180.0,
        "right astern": 180.0,
        "the stern": 180.0,
        "larboard beam": 270.0,
        "the larboard beam": 270.0,
        "larboard": 270.0,
        "port": 270.0,
    }
    if w in ("", "leeward", "to leeward", "abeam to leeward"):
        return None, "abeam to leeward"
    if w in named:
        deg = named[w]
    else:
        try:
            deg = float(w) % 360.0
        except ValueError:
            raise ValueError(
                f"'{words}' is not a place to stand: give degrees from the bow, clockwise "
                "(0 right ahead, 90 the starboard beam, 180 right astern, 270 the larboard "
                "beam), or 'leeward'."
            ) from None
    d = int(round(deg)) % 360
    if d == 0:
        said = "right ahead"
    elif d == 90:
        said = "the starboard beam"
    elif d == 180:
        said = "right astern"
    elif d == 270:
        said = "the larboard beam"
    else:
        said = f"{'starboard' if d < 180 else 'larboard'}, {min(d, 360 - d)} degrees from the bow"
    return float(d), said


def span_of(words: str) -> str:
    """The chart's span from the tool's words: a key of `SPANS`, or "" for none (the
    page's own view). Refused in words otherwise."""
    w = " ".join(str(words or "").lower().split()).removeprefix("the ").removesuffix(" span")
    if w in ("", "page", "the page's view", "as shown", "current"):
        return ""
    if w in SPANS:
        return w
    raise ValueError(
        f"'{words}' is not a span of the chart: say harbour (two miles across), coast "
        "(twenty), passage (a hundred and fifty) or whole (the chart as built), or nothing "
        "for the view the page shows."
    )


def paint(world: Any, view: str, facing: str = "", span: str = "") -> Picture | str:
    """The picture of a view through the World's painter, or the words why there is
    none (no page open, the page did not answer, a picture too large)."""
    from freesail import units

    painter = painter_of(world)
    if painter is None:
        return "No browser is open on this game (the picture is drawn by the open page)"
    stamp = units.time_stamp(world.clock.ship_time)
    try:
        return painter.paint(view, facing, stamp, span)
    except TypeError:
        # a painter of a test's own, from before the span (package 45)
        return painter.paint(view, facing, stamp)
