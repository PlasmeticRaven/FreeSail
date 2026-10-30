"""The places aboard, what they hold, and the ship's papers (spec M5 §22; package 35;
`docs/design/InwardAndOutward.md`, the inward minimum and the sail room's worked
example; `docs/design/Papers-and-Books.md`).

A **place** is a name and a description, no more: the quarterdeck, the deck, the cabin,
the gunroom, the tops, the sail room, the hold, the boat, the shore (the port's quay).
No layout, no movement simulated: a person is in one (`freesail.world.people`), and
changes place at the moments the period's orders changed it. The words are Falconer's
where he has them (1780: CABIN, GUN-ROOM, HOLD, QUARTER-DECK, WAIST) and judgement
where he does not.

What the places hold is counted in three small ledgers: the **hold** (the room for a
cargo, from the ship file, and the goods in it by tons), the **purse** (the captain's
or the owner's money, in pounds, which the market and the yard move) and the **stores**
(water by the ton and provisions by the day, from the ship file's `crew.stores`, which
the yard and the market fill and the meals draw down by the ration, package 54).

The **papers** are things aboard, each with a keeper and a place, each only as current
as its last entry (`data/papers/papers.yaml`): the sailmaker's account, the manifest,
the purser's books, the boatswain's store book, the booms' list, the establishment of
ground tackle, the epitome's table of the establishments, and the price list once the
boat has been ashore. A paper's page is made from the store it records, in the words
its query answers at the order line (`the sail room`, `the booms`, `the boatswain's
store`, `the ground tackle`), so that the paper and the query say one thing; the
library serves every paper by handle to every station the same (`freesail.agents.tools`,
the `papers` topic) and the browser's pane reads the same topic. The log says when a
keeper writes a paper (`Papers.write`); reading one at the order line is a query line,
as the stores' queries always were.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from freesail import units

__all__ = [
    "DEFAULT_ASHORE",
    "PAPERS_PATH",
    "PLACES",
    "PORT_PLACES",
    "Hold",
    "Paper",
    "Papers",
    "Place",
    "Places",
    "PortPlace",
    "Purse",
    "Stores",
    "ashore_place_of",
    "earshot",
    "find_port_place",
    "place_words",
    "port_place_lines",
    "port_places",
]

PAPERS_PATH = Path(__file__).resolve().parents[2] / "data" / "papers" / "papers.yaml"


@dataclass(frozen=True)
class Place:
    id: str
    name: str  # as the log names it: "the quarterdeck"
    description: str
    below: bool = False  # below decks, out of the weather and the deck's business
    aboard: bool = True  # the shore and the pilot's cutter are not


# The places of the inward minimum (spec M5 §22), in the order `the places` lists them.
PLACES: dict[str, Place] = {
    p.id: p
    for p in (
        Place(
            "quarterdeck",
            "the quarterdeck",
            "the after part of the upper deck, abaft the main mast, where the captain and the "
            "officer of the watch keep the deck and the wheel is (Falconer 1780, QUARTER-DECK)",
        ),
        Place(
            "deck",
            "the deck",
            "the waist and the forecastle, where the hands work the ship (Falconer 1780, WAIST: "
            "the part between the quarter-deck and the forecastle)",
        ),
        Place(
            "cabin",
            "the cabin",
            "the captain's apartment aft, with its door and a sentry at it (Falconer 1780, CABIN: "
            "'the principal of which is designed for the captain')",
            below=True,
        ),
        Place(
            "gunroom",
            "the gunroom",
            "the officers' mess on the lower deck aft, the lieutenants' and the master's "
            "(Falconer 1780, GUN-ROOM: 'in small ones, it is used by the lieutenants as a "
            "dining-room')",
            below=True,
        ),
        Place(
            "tops",
            "the tops",
            "the platforms at the lower mastheads, the topmen's station aloft",
        ),
        Place(
            "sail_room",
            "the sail room",
            "the room below where the spare sails are stowed in the sailmaker's charge "
            "(judgement on the Regulations' sailmaker, who is 'very carefully to examine the "
            "sails')",
            below=True,
        ),
        Place(
            "hold",
            "the hold",
            "the whole interior cavity between the floor and the lower deck, the ballast, "
            "provisions and stores of a ship of war and the cargo of a merchantman (Falconer "
            "1780, HOLD)",
            below=True,
        ),
        Place(
            "galley",
            "the galley",
            "the cook-room under the forecastle, where the coppers boil the company's "
            "victuals in the cook's charge (judgement: a frigate's of the period, under the "
            "forecastle and open to the waist; a small vessel's is her caboose on deck)",
        ),
        # package 73 (spec M7 §16): the surgeon's places
        Place(
            "cockpit",
            "the cockpit",
            "the surgeon's place in action, on the orlop below the waterline, where the "
            "wounded are brought down to him (Falconer 1780, COCKPIT: 'the place where the "
            "wounded men are dressed'); the sick berth under the forecastle else",
            below=True,
        ),
        Place(
            "sick_berth",
            "the sick berth",
            "the sick berth under the forecastle, in the surgeon's charge (the frigates' sick "
            "berth of the 1800s, screened off forward on the upper deck: judgement on the "
            "Regulations' surgeon)",
            below=True,
        ),
        Place(
            "boat",
            "the boat",
            "the ship's boat, hoisted out and away on an errand, or alongside",
            aboard=False,
        ),
        Place(
            "shore",
            "the shore",
            "the port's quay, where the boat lands and the market and the yard are",
            aboard=False,
        ),
        Place(
            "cutter",
            "the pilot cutter",
            "the pilot's own vessel, come off from the port and lying under the ship's lee",
            aboard=False,
        ),
    )
}


# The places open to one another on the upper deck (package 52, spec M7b §9: a word said
# where a person is, heard by those within earshot): the quarterdeck, the waist and
# forecastle, and the galley under the forecastle, open to the waist. Below, aloft and off
# the ship, a word is heard only in its own place (judgement: the bulkheads and the height
# of the tops; the lookout's hail from the masthead carries by its own rule).
OPEN_DECK: frozenset[str] = frozenset({"quarterdeck", "deck", "galley"})


def earshot(place_id: str) -> frozenset[str]:
    """The places within earshot of a word said in `place_id`: the open deck's three for
    any of them, else the place alone."""
    return OPEN_DECK if place_id in OPEN_DECK else frozenset({place_id})


def place_words(place_id: str) -> str:
    """'on the quarterdeck', 'in the cabin', 'in the boat', 'ashore'."""
    if place_id == "shore":
        return "ashore"
    if place_id == "cutter":
        return "in the pilot cutter"
    if place_id in ("quarterdeck", "deck"):
        return f"on {PLACES[place_id].name}"
    p = PLACES.get(place_id)
    return f"in {p.name}" if p is not None else place_id


class Places:
    """The places of one ship: `describe` for `the places` and a place by any of its words."""

    def __init__(self, ship_name: str = "") -> None:
        self.ship_name = ship_name

    def find(self, words: str) -> Place | None:
        key = " ".join(str(words).lower().replace("_", " ").replace("-", " ").split())
        key = key.removeprefix("the ").strip()
        for p in PLACES.values():
            if key in (p.id.replace("_", " "), p.name.removeprefix("the ")):
                return p
        if key in ("below", "his cabin", "the great cabin", "great cabin"):
            return PLACES["cabin"]
        if key in ("on deck", "aft"):
            return PLACES["quarterdeck"]
        return None

    def describe(self) -> list[str]:
        """`the places`: each place aboard with its description."""
        return [f"{p.name[:1].upper()}{p.name[1:]}: {p.description}." for p in PLACES.values()]


# ---------------------------------------------------------------------------
# The port's places (spec M7b §14; package 53)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class PortPlace:
    """A place ashore at a port: a name, what is done there and who is found there, in
    words, no more (the owner, 2026-10-16: a place is an aspect of a person's state, not
    a simulation). `roles` are the roles of a person made ashore who is found there by
    default (`ashore_place_of`)."""

    id: str
    name: str  # "the quay"
    done: str  # what is done there
    found: str  # who is found there, in words
    roles: tuple[str, ...] = ()


# Every port's places, in the order `the port` lists them (judgement on the period's
# seaport: the quay where the boats land and the lighters load, the market and its
# dealers, the merchants' counting houses, the tavern where the talk is, the pilots'
# office or their watch-house). A port's file may add its own (`places:` in
# `data/ports/<port>.yaml`: the packet office at Falmouth, the dockyard at Plymouth).
PORT_PLACES: dict[str, PortPlace] = {
    p.id: p
    for p in (
        PortPlace(
            "quay",
            "the quay",
            "the boats land and take off people and letters, and the lighters load",
            "the harbourmaster, the watermen and the lightermen",
            ("harbourmaster", "waterman", "lighterman", "boatman"),
        ),
        PortPlace(
            "market",
            "the market",
            "the port's goods are bought and sold in person at the prices of the day, and "
            "carted to the quay for the lighter",
            "the dealers and the factors",
            ("dealer", "factor", "chandler", "trader"),
        ),
        PortPlace(
            "counting_house",
            "the counting house",
            "the merchants' business: freights, bills and cargoes for another port",
            "the merchants and their clerks",
            ("merchant", "clerk", "agent", "supercargo", "owner", "banker", "consul"),
        ),
        PortPlace(
            "tavern",
            "the tavern",
            "the talk of the port is heard, and hands and passages are asked after",
            "seamen ashore, masters of merchantmen and the talk of the quay",
            ("seaman", "master", "mate", "landlord", "publican", "smuggler"),
        ),
        PortPlace(
            "pilots_office",
            "the pilots' office",
            "a pilot is engaged and the state of the channel and the tides asked",
            "the pilots of the port not at their stations",
            ("pilot",),
        ),
    )
}

# Where a person ashore is when nothing said puts him elsewhere (judgement): the quay,
# where the boat landed him.
DEFAULT_ASHORE = "quay"


def port_places(port: Any) -> dict[str, PortPlace]:
    """A port's places: every port's (`PORT_PLACES`) and its file's own additions
    (`Port.places`, read from `places:` in the file), by id, in that order."""
    out = dict(PORT_PLACES)
    for entry in getattr(port, "places", None) or []:
        pid = _place_key(str(entry.get("id") or entry.get("name") or ""))
        if not pid:
            continue
        name = str(entry.get("name") or pid.replace("_", " "))
        if not name.lower().startswith("the "):
            name = f"the {name}"
        out[pid] = PortPlace(
            pid,
            name,
            " ".join(str(entry.get("done") or "").split()),
            " ".join(str(entry.get("found") or "").split()),
            tuple(str(r).lower() for r in (entry.get("roles") or [])),
        )
    return out


def find_port_place(port: Any, words: str) -> PortPlace | None:
    """A place of the port by any of its words ('the market', 'market', 'the pilots
    office', 'counting house'); None when the port has none so called."""
    key = _place_key(words)
    for p in port_places(port).values():
        if key in (p.id, _place_key(p.name)):
            return p
    return None


def ashore_place_of(port: Any, role: str) -> str:
    """Where a person ashore at a port is found by his role when nothing said puts him
    elsewhere: a pilot at the pilots' office, a merchant at the counting house, a dealer
    at the market; anyone else on the quay (`DEFAULT_ASHORE`)."""
    words = " ".join(str(role or "").lower().split())
    last = words.split()[-1] if words else ""
    for p in port_places(port).values():
        if words in p.roles or last in p.roles:
            return p.id
    return DEFAULT_ASHORE


def port_place_lines(
    port: Any,
    people_there: dict[str, list[str]] | None = None,
    things_there: dict[str, list[str]] | None = None,
) -> list[str]:
    """`the port`'s places in words, one a line: each with what is done there and who is
    found there, the people of the world ashore there by name after them, and the things
    lying there after them (package 53b)."""
    out = []
    for p in port_places(port).values():
        names = (people_there or {}).get(p.id) or []
        found = p.found + (f"; and {', '.join(names)}" if names else "")
        things = (things_there or {}).get(p.id) or []
        lying = f"; lying there, {', '.join(things)}" if things else ""
        out.append(f"{p.name[:1].upper()}{p.name[1:]}: {p.done}; found there, {found}{lying}.")
    return out


def _place_key(words: str) -> str:
    text = str(words).lower().replace("’", "'").replace("'", "").replace("-", " ")
    text = " ".join(text.replace("_", " ").split()).removeprefix("the ")
    return text.replace(" ", "_")


# ---------------------------------------------------------------------------
# What the places hold: the hold, the purse and the stores
# ---------------------------------------------------------------------------


@dataclass
class Hold:
    """The hold's room for a cargo and the goods in it, by tons (spec M5 §23)."""

    capacity_tons: float
    goods: dict[str, float] = field(default_factory=dict)
    # the freights engaged (package 53b; `freight`): (tick, tons, good, the words with the
    # cause); none for a hold the channel has not touched, or of a checkpoint from before
    freights: list[tuple[int, float, str, str]] = field(default_factory=list)
    # the cargo found spoiled and struck off (the director's `aboard:` table, `lose`):
    # (tick, tons, good, the words with the cause); as `freights`
    losses: list[tuple[int, float, str, str]] = field(default_factory=list)

    @property
    def stowed_tons(self) -> float:
        return sum(self.goods.values())

    @property
    def room_tons(self) -> float:
        return max(0.0, self.capacity_tons - self.stowed_tons)

    def stow(self, good: str, tons: float) -> None:
        if tons > self.room_tons + 1e-9:
            raise ValueError(f"there is room in the hold for {_tons(self.room_tons)} and no more")
        self.goods[good] = self.goods.get(good, 0.0) + float(tons)

    def break_out(self, good: str, tons: float) -> None:
        have = self.goods.get(good, 0.0)
        if tons > have + 1e-9:
            raise ValueError(f"the hold has {_tons(have)} of {good}, not {_tons(tons)}")
        left = have - float(tons)
        if left <= 1e-9:
            self.goods.pop(good, None)
        else:
            self.goods[good] = left

    def freight(self, tons: float, good: str, words: str, tick: int) -> None:
        """A cargo freighted (spec M7b §17a; package 53b): the hold's ledger line with its
        cause ('10 tons of wool freighted by Mr Veale at Plymouth for Falmouth'), written
        when the freight is engaged; the goods are stowed when they come off."""
        if getattr(self, "freights", None) is None:
            self.freights = []  # a checkpoint from before
        self.freights.append((tick, float(tons), str(good), str(words)))

    def lose(self, good: str, tons: float, words: str, tick: int) -> float:
        """Cargo found spoiled and struck off the manifest (the director's `aboard:` table):
        no more than the hold has of the good, broken out with the ledger's line and its
        cause. Returns the tons struck off."""
        tons = min(float(tons), self.goods.get(good, 0.0))
        if tons <= 1e-9:
            return 0.0
        self.break_out(good, tons)
        if getattr(self, "losses", None) is None:
            self.losses = []  # a checkpoint from before
        self.losses.append((tick, tons, str(good), str(words)))
        return tons

    def lines(self) -> list[str]:
        """The manifest's lines: the room and the cargo by tons, and the freights engaged
        and the cargo struck off with their causes where there are any."""
        if self.capacity_tons <= 0:
            return ["No room for a cargo: the hold is her own stores and ballast."]
        head = (
            f"The hold stows {_tons(self.capacity_tons)} of cargo; "
            f"{_tons(self.stowed_tons)} in it and room for {_tons(self.room_tons)}."
        )
        freights = [
            f"{w[:1].upper()}{w[1:]}." for _t, _n, _g, w in getattr(self, "freights", None) or []
        ] + [f"{w[:1].upper()}{w[1:]}." for _t, _n, _g, w in getattr(self, "losses", None) or []]
        if not self.goods:
            return [head, "No cargo aboard.", *freights]
        return [head, *(f"{_tons(t)} of {g}." for g, t in self.goods.items()), *freights]

    def words(self) -> str:
        if not self.goods:
            return f"empty, room for {_tons(self.room_tons)}"
        return (
            ", ".join(f"{_tons(t)} of {g}" for g, t in self.goods.items())
            + f"; room for {_tons(self.room_tons)}"
        )


@dataclass
class Purse:
    """The money aboard, in pounds: the captain's or the owner's (the scenario's `cargo:
    purse_pounds`), which the market, the yard, the pilot's fee and the crew pool move.
    Nothing real passes through it (docs/agents/README.md, commitment 7)."""

    pounds: float = 0.0
    entries: list[tuple[int, float, str]] = field(default_factory=list)  # (tick, change, why)
    # the transactions of the world-order channel (spec M7b §17a; package 53b): each line
    # (tick, kind, pounds, the payer or the payee, the words), the kinds `received` (paid
    # into the purse by someone), `paid` (paid from it to someone), `owed` (a debt the ship
    # owes) and `owing` (a debt owed to her); the money's own lines are in `entries` as
    # every sum's are. Empty for a purse the channel has not touched, and for a checkpoint
    # from before (`ledger_of`), so that a world without them reads as it did.
    ledger: list[tuple[int, str, float, str, str]] = field(default_factory=list)

    def receive(self, pounds: float, by: str, words: str, tick: int) -> str:
        """A sum paid into the purse by someone: the purse's line and the ledger's, with
        its cause. Returns the ledger's words ('paid by Mr Veale, twenty guineas; the purse
        £55')."""
        self.take(pounds, f"paid by {by}, {words}", tick)
        line = f"paid by {by}, {words}; the purse {self.words()}"
        self._ledger().append((tick, "received", float(pounds), by, line))
        return line

    def pay_to(self, pounds: float, to: str, words: str, tick: int) -> str:
        """A sum paid from the purse to someone; ValueError in words below nothing (a
        payment is refused, never a purse below nothing)."""
        self.pay(pounds, f"paid to {to}, {words}", tick)
        line = f"paid to {to}, {words}; the purse {self.words()}"
        self._ledger().append((tick, "paid", float(pounds), to, line))
        return line

    def owe(self, pounds: float, party: str, words: str, tick: int, to_us: bool = False) -> str:
        """A debt entered, owed by the ship to the party or (`to_us`) by the party to her:
        no money moves, the ledger keeps it."""
        line = (
            f"a debt of {words} owed by {party} to the ship"
            if to_us
            else f"a debt of {words} owed to {party}"
        )
        self._ledger().append((tick, "owing" if to_us else "owed", float(pounds), party, line))
        return line

    def _ledger(self) -> list[tuple[int, str, float, str, str]]:
        if getattr(self, "ledger", None) is None:
            self.ledger = []  # a checkpoint from before
        return self.ledger

    def ledger_lines(self, last: int = 6) -> list[str]:
        """The channel's transactions in words, the last `last` of them: what a reader of
        the purser's books sees beside the sum."""
        return [line[:1].upper() + line[1:] + "." for *_x, line in self._ledger()[-last:]]

    def debts_words(self) -> str:
        """The debts standing in words ('owed to the chandler at Plymouth, £30'), or ""."""
        out = []
        for _t, kind, pounds, party, _w in self._ledger():
            if kind == "owed":
                out.append(f"owed to {party}, {pounds_words(pounds)}")
            elif kind == "owing":
                out.append(f"owed by {party}, {pounds_words(pounds)}")
        return "; ".join(out)

    def pay(self, pounds: float, why: str, tick: int) -> None:
        if pounds > self.pounds + 1e-9:
            raise ValueError(
                f"the purse holds {pounds_words(self.pounds)}, not {pounds_words(pounds)}"
            )
        self.pounds -= float(pounds)
        self.entries.append((tick, -float(pounds), why))

    def take(self, pounds: float, why: str, tick: int) -> None:
        self.pounds += float(pounds)
        self.entries.append((tick, float(pounds), why))

    def words(self) -> str:
        return pounds_words(self.pounds)


@dataclass
class Stores:
    """The purser's stores: water by the ton and provisions by the day for the
    complement, from the ship file; filled by the yard and the market, and drawn down at
    the meals by the ration (`crew.victuals`, package 54): what remains and for how long
    is the purser's reading, never a line of the log."""

    water_tons: float = 0.0
    provisions_days: float = 0.0
    slops_issued_pounds: float = 0.0
    # the water found foul (package 50, the director's `aboard:`; the needs of package 54
    # read it): a class default, so that a checkpoint from before loads with it
    foul: bool = False
    # package 54: the share of the whole allowance served (short allowance, the
    # Regulations' Art. III), and what the meals have drawn since she was stored; class
    # defaults, as `foul`
    allowance: float = 1.0
    expended_days: float = 0.0
    expended_tons: float = 0.0
    # the tick she last took in water (the director's `aboard:` table reads the days since
    # for a thing found foul, `days_since_watered`): 0, the voyage's start, until she
    # waters; a class default, as `foul`
    watered_tick: int = 0
    # practice and resupply (between packages 72 and 73; the build design's §1.4, §5): the
    # galley fire put out while the powder comes aboard ("powder"; the Regulations of 1806,
    # the Gunner, Art. V, l.12800-12809), which the person's meal and the company's read,
    # and the meals served cold for it; class defaults, as `foul`
    galley_fire_out: str = ""
    cold_meals: int = 0

    def lines(
        self, complement: int, water_days: float | None = None, day_words: str = ""
    ) -> list[str]:
        """The purser's page: the water and how long it lasts, the provisions and how
        long, the allowance, what is expended, and the day's proportion a man."""
        foul = ", found foul" if getattr(self, "foul", False) else ""
        allowance = float(getattr(self, "allowance", 1.0))
        at = "at full allowance" if allowance >= 1.0 else "at short allowance"
        water = f"Water: {_tons(self.water_tons)} in the ground tier{foul}"
        if water_days is not None:
            water += f", for {_days(water_days)} {at}"
        out = [
            water + ".",
            f"Provisions: {self.provisions_days:.0f} days at full allowance for {complement} men"
            + (
                f", {self.provisions_days / allowance:.0f} at the short allowance the people "
                "are at."
                if allowance < 1.0
                else "."
            ),
        ]
        days = float(getattr(self, "expended_days", 0.0))
        tons = float(getattr(self, "expended_tons", 0.0))
        if days > 0 or tons > 0:
            out.append(
                f"Expended since she was stored: {_tons(tons)} of water and "
                f"{_days(days)} of provisions."
            )
        else:
            out.append(
                "Nothing is yet expended against them; the books stand as the ship was stored."
            )
        # practice and resupply: the galley's state only while it is so, and the cold meals
        # once there have been any, so that the page is otherwise what it was
        if getattr(self, "galley_fire_out", ""):
            out.append("The galley fire is out while the powder comes aboard.")
        cold = int(getattr(self, "cold_meals", 0) or 0)
        if cold > 0:
            out.append(f"{cold} meal{'s' if cold != 1 else ''} served cold.")
        if day_words:
            out.append(f"{day_words}.")
        return out

    def words(self, water_days: float | None = None) -> str:
        allowance = float(getattr(self, "allowance", 1.0))
        water = f"water {_tons(self.water_tons)}"
        if water_days is not None:
            water += f" for {_days(water_days)}"
        if getattr(self, "foul", False):
            water += ", found foul"
        provisions = f"provisions for {self.provisions_days:.0f} days"
        if allowance < 1.0:
            provisions += f" ({self.provisions_days / allowance:.0f} at short allowance)"
        if getattr(self, "galley_fire_out", ""):
            # practice and resupply: only while it is so
            provisions += ", the galley fire out while the powder comes aboard"
        return f"{water}, {provisions}"


def _days(days: float) -> str:
    n = round(float(days), 1)
    if n == int(n):
        n = int(n)
    return f"{n} day{'s' if n != 1 else ''}"


def pounds_words(pounds: float) -> str:
    """'five pounds', '£127 10s', 'nothing': the purse's figures as a clerk writes them."""
    if abs(pounds) < 0.005:
        return "nothing"
    whole = int(abs(pounds))
    shillings = int(round((abs(pounds) - whole) * 20.0))
    if shillings == 20:
        whole, shillings = whole + 1, 0
    sign = "-" if pounds < 0 else ""
    if shillings:
        return f"{sign}£{whole} {shillings}s"
    return f"{sign}£{whole}"


def _tons(tons: float) -> str:
    n = round(float(tons), 1)
    if n == int(n):
        n = int(n)
    return f"{n} ton{'s' if n != 1 else ''}"


# ---------------------------------------------------------------------------
# The ship's papers
# ---------------------------------------------------------------------------


@dataclass
class Paper:
    """One paper as the catalogue names it, with its page as made now."""

    handle: str
    keeper: str
    place: str
    source: str
    words: str
    lines: list[str] = field(default_factory=list)
    as_of_tick: int = 0
    as_of: str = ""  # the clock's stamp of the last entry


class Papers:
    """The papers aboard one World, made from `data/papers/papers.yaml`: `pages()` makes
    every paper's page from its store; `write(handle, why)` records an entry and gives
    the log's line; `page(handle)` one paper by any of its words."""

    def __init__(self, world: Any, path: str | Path = PAPERS_PATH) -> None:
        self.world = world
        doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        self.catalogue: list[dict[str, Any]] = [dict(p) for p in (doc.get("papers") or [])]
        # the catalogue's own file, for `_merge` (package 86's fold-in, the review's finding:
        # it had mended every catalogue from `PAPERS_PATH`); None for the project's file, so
        # that a checkpoint carries no machine's path and is mended by the build resuming it
        self.path: str | None = None if Path(path).resolve() == PAPERS_PATH else str(path)
        # the last entry of each paper: the tick and the clock's stamp (the muster at the
        # start, until a keeper writes it)
        self.entries: dict[str, tuple[int, str]] = {}
        self._stamp_at_start: str | None = None
        # the news of the war as the ship has heard it: the table she knows (the one she
        # sailed with, moved by each piece of news) and every change the news brought, with
        # where and when it came (`news_heard`; the paper `the news of the war`, the reading
        # `the war`)
        nations = getattr(world, "nations", None)
        self.known_wars: list[dict[str, Any]] = (
            [dict(w) for w in nations.sailed_with] if nations is not None else []
        )
        self.war_news: list[dict[str, Any]] = []

    # -- entries -------------------------------------------------------------------

    def _stamp(self) -> str:
        clock = self.world.clock
        return f"{clock.ship_time:%d %B}, {units.time_stamp(clock.ship_time)}"

    def write(self, handle: str, why: str) -> str:
        """A keeper writes the paper up: the entry dated now, and the log's line."""
        paper = self._entry(handle)
        key = paper["handle"]
        self.entries[key] = (self.world.clock.tick, self._stamp())
        head = key[:1].upper() + key[1:]
        keeper = self._keeper(paper["keeper"])
        return f"{head} written up by the {keeper}: {why}."

    # -- the news of the war --------------------------------------------------------

    def news_heard(self, how: str) -> list[str]:
        """The news of the war brought to the ship by `how` ('the pilot off Falmouth', 'the
        boat from the quay at Plymouth'): the world's table against the one she knows, each
        war declared or peace made since entered in the paper with where and when it came,
        the paper written up; the log's lines, one a change (none when nothing changed)."""
        nations = getattr(self.world, "nations", None)
        if nations is None:
            return []
        before = {frozenset(w["between"]) for w in self.known_wars}
        now = {frozenset(w["between"]) for w in nations.wars}
        lines: list[str] = []
        for pair in sorted(before ^ now, key=sorted):
            a, b = sorted(pair)
            first, second = nations.nations[a].name, nations.nations[b].name
            text = (
                f"war declared between {first} and {second}"
                if pair in now
                else f"peace made between {first} and {second}"
            )
            self.war_news.append(
                {"tick": self.world.clock.tick, "when": self._stamp(), "how": how, "text": text}
            )
            lines.append(self.write("the news of the war", f"by {how}, {text}"))
        self.known_wars = [dict(w) for w in nations.wars]
        return lines

    def war_lines(self) -> list[str]:
        """The war as the ship knows it, for the paper and the reading: the table she
        sailed with, and the news since, each with where and when it came."""
        nations = getattr(self.world, "nations", None)
        if nations is None:
            return ["No table of the nations aboard."]
        lines = [nations.sailed_with_words()]
        if not self.war_news:
            lines.append("No news of the war has reached her since she sailed.")
            return lines
        lines.append("The news since, as it came:")
        lines.extend(f"  {n['when']}, by {n['how']}: {n['text']}." for n in self.war_news)
        lines.append(f"As she knows it now: {nations.table_words(self.known_wars)}.")
        return lines

    def _keeper(self, keeper: str) -> str:
        """The keeper who holds a paper in this ship: the mate keeps the purser's papers
        where there is no purser (a merchantman), the master where there is no mate."""
        people = getattr(self.world, "people", None)
        if keeper == "purser" and people is not None and people.find("the purser") is None:
            return "mate" if people.find("the mate") is not None else "master"
        if keeper == "gunner" and people is not None and people.find("the gunner") is None:
            # practice and resupply: the gunner's account in a ship with no gunner (the
            # cutter's people, data/people/cutter.yaml) falls to the boatswain, the mate
            # and then the master
            for role in ("boatswain", "mate"):
                if people.find(f"the {role}") is not None:
                    return role
            return "master"
        return keeper

    def _entry(self, handle: str) -> dict[str, Any]:
        key = _paper_key(handle)
        found = self._match(key)
        if found is None and self._merge():
            # practice and resupply (between packages 72 and 73): a checkpoint's catalogue
            # from before a paper was added mended from the file, and looked in again
            found = self._match(key)
        if found is None:
            raise KeyError(f"no paper aboard answers to '{handle}'")
        return found

    def _match(self, key: str) -> dict[str, Any] | None:
        for p in self.catalogue:
            if _paper_key(p["handle"]) == key or key in _paper_key(p["handle"]):
                return p
        return None

    def _merge(self) -> bool:
        """The papers of this catalogue's own file (`self.path`; the project's
        `PAPERS_PATH` when it is that one, or a `Papers` pickled before the path was kept)
        that the catalogue lacks, appended in the file's order; True when any were. On every
        miss, against the file as this process has read it (`_file_papers`), and nothing is
        kept on the `Papers` to say it was done: so a checkpoint is mended by whichever
        build resumes it, a later build's new paper too, and not only by the first build
        that had this. Nothing is logged or drawn."""
        own = getattr(self, "path", None)
        source = Path(own) if own else PAPERS_PATH
        have = {_paper_key(p["handle"]) for p in self.catalogue}
        added = [dict(p) for p in _file_papers(source) if _paper_key(p["handle"]) not in have]
        if not added:
            return False
        self.catalogue = [*self.catalogue, *added]
        return True

    def find(self, handle: str) -> dict[str, Any] | None:
        try:
            return self._entry(handle)
        except KeyError:
            return None

    # -- the pages -----------------------------------------------------------------

    def pages(self) -> list[Paper]:
        return [self.page(p["handle"]) for p in self.catalogue]

    def page(self, handle: str) -> Paper:
        entry = self._entry(handle)
        lines, keeper = self._lines(entry["source"], entry["keeper"])
        tick, stamp = self.entries.get(entry["handle"], (0, ""))
        if not stamp:
            if self._stamp_at_start is None:
                start = self.world.scenario.start_time
                self._stamp_at_start = f"{start:%d %B}, {units.time_stamp(start)}"
            stamp = self._stamp_at_start
        return Paper(
            handle=entry["handle"],
            keeper=keeper,
            place=entry["place"],
            source=entry["source"],
            words=entry["words"],
            lines=lines,
            as_of_tick=tick,
            as_of=stamp,
        )

    def _lines(self, source: str, keeper: str) -> tuple[list[str], str]:
        """The page's lines from the store it records, and the keeper who holds it in
        this ship (the mate keeps the purser's papers where there is no purser)."""
        world = self.world
        ship = world.ship
        keeper = self._keeper(keeper)
        if not hasattr(ship, "spars"):
            return (["A ship with no parts keeps no such paper."], keeper)
        from freesail.ship.parts import booms, cordage, ground_tackle, sail_room

        if source == "sail_room":
            return sail_room(ship).inventory_lines(), keeper
        if source == "booms":
            return booms(ship).inventory_lines(), keeper
        if source == "cordage":
            return cordage(ship).inventory_lines(), keeper
        if source == "ground_tackle":
            tackle = ground_tackle(ship)
            return (tackle.describe() if tackle else ["She carries no ground tackle."]), keeper
        if source == "manifest":
            hold = getattr(world, "hold", None)
            purse = getattr(world, "purse", None)
            lines = hold.lines() if hold is not None else ["No hold is kept in this ship."]
            if purse is not None:
                lines.append(f"The purse: {purse.words()}.")
            return lines, keeper
        if source == "purser":
            stores = getattr(world, "stores", None)
            crew = ship.extra.get("crew") if hasattr(ship, "extra") else None
            complement = crew.complement if crew is not None else 0
            if stores is None:
                return ["No stores are kept."], keeper
            from freesail.crew import victuals

            if not victuals.victualled(world):
                return stores.lines(complement), keeper
            return stores.lines(
                complement, victuals.water_days(world), victuals.day_words(world)
            ), keeper
        if source == "epitome":
            nav = getattr(world, "navigation", None)
            if nav is None:
                return ["No epitome aboard: the ship keeps no reckoning."], keeper
            table = nav.epitome
            lines = [f"{table.title[:1].upper()}{table.title[1:]}."]
            for port in table.ports:
                words = f"{port.name}: {port.establishment_words} at full and change"
                if port.bearing:
                    words += f" (the moon {port.bearing})"
                if port.spring_rise_ft is not None:
                    words += f"; springs rise {port.spring_rise_ft:g} feet"
                lines.append(words + ".")
            return lines, keeper
        if source == "war":
            return self.war_lines(), keeper
        if source == "prices":
            ports = getattr(world, "dealings", None)
            if ports is None or not ports.price_lists:
                return ["No price list aboard: the boat has not been ashore in any port."], keeper
            lines = []
            for port_id, (_tick, when, listed) in ports.price_lists.items():
                port = ports.ports[port_id]
                lines.append(f"Prices at {port.name}, {when}, a ton at the quay:")
                lines.extend(f"  {good}, {pounds_words(price)}." for good, price in listed)
            return lines, keeper
        if source == "magazine":
            # practice and resupply (between packages 72 and 73): the gunner's count of the
            # magazine, with his account of the receipts and the practice beyond the allowance
            if not getattr(ship, "guns", None):
                return ["She carries no guns; the gunner keeps no account."], keeper
            from freesail.combat.filling import magazine_lines
            from freesail.ship.parts import magazine

            mag = magazine(ship)
            return [*magazine_lines(world, ship, mag), *mag.account_lines()], keeper
        if source == "private_signals":
            from freesail.world.signals import table_of

            table = table_of(world)
            if table is None:
                return [
                    "No private signals aboard: the month's table is issued to the King's "
                    "ships under seal, and this ship carries none."
                ], keeper
            return table.lines(), keeper
        if source == "signal_book":
            from freesail.world.signals import books_for

            books = books_for(world)
            if books.root == "basic":
                # the common book of no nation: whose it is not, said first (the model
                # officer's fifth point: a generic list taken for the ship's own)
                head = (
                    "The common signal book, in the period's general form and no nation's own: "
                    "this ship's nation keeps no book of her own in the game, so hers is this "
                    "one, and no other ship's numbers are to be read from it; "
                )
            else:
                nation = getattr(world, "nations", None)
                name = (
                    nation.get(books.nation).name
                    if nation is not None and books.nation in nation.nations
                    else books.nation
                )
                head = f"The {name} signal books, this ship's own by her service ({books.system}): "
            lines = [
                head + "the day signals by number, the night and fog signals, the convoy's "
                "instructions; a signal is made by its meaning ('make the signal to tack in "
                "succession')."
            ]
            lines.extend(
                f"  No. {e.number}: {e.meaning}" + (f" ({e.original})" if e.original else "")
                for e in books.numerary
            )
            lines.append(
                "The night signals: "
                + "; ".join(f"{e.meaning}, {e.show}" for e in books.night)
                + "."
            )
            lines.append(
                "The fog signals: " + "; ".join(f"{e.meaning}, {e.fire}" for e in books.fog) + "."
            )
            lines.append(
                "The convoy's instructions: "
                + "; ".join(f"No. {e.number} {e.meaning}" for e in books.convoy)
                + "."
            )
            if books.telegraph:
                lines.append(
                    f"The telegraphic dictionary: {len(books.words)} words and the alphabet "
                    "('make the telegraphic signal: <the words>')."
                )
            return lines, keeper
        return [f"The paper's source '{source}' is not one the ship keeps."], keeper


def _paper_key(handle: str) -> str:
    text = str(handle).lower().replace("’", "'").replace("'", "")
    return " ".join(text.replace("-", " ").split()).removeprefix("the ")


# practice and resupply (between packages 72 and 73): the papers file's catalogue as this
# process read it, by the file's path, time and size, for `Papers._merge`; the module's,
# never a `Papers`'s, so nothing of it is pickled into a checkpoint
_FILE_PAPERS: dict[tuple[str, int, int], tuple[dict[str, Any], ...]] = {}


def _file_papers(path: Path) -> tuple[dict[str, Any], ...]:
    """The papers of the file at `path`, read once while the file is unchanged; none when
    it cannot be read."""
    try:
        st = Path(path).stat()
    except OSError:
        return ()
    key = (str(path), st.st_mtime_ns, st.st_size)
    got = _FILE_PAPERS.get(key)
    if got is None:
        try:
            doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
        except OSError:
            doc = {}
        got = tuple(dict(p) for p in (doc.get("papers") or []) if isinstance(p, dict))
        _FILE_PAPERS[key] = got
    return got
