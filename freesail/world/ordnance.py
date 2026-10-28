"""Powder and shot taken in at a port (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §1.3, §1.4, §3.2, §5): the port file's
`ordnance:` block, the demand and its refusals, and the hoy's two stages.

**The block.** A port that supplies powder and shot says how in its file:

    ordnance:
      kind: ordnance                 # the storekeeper of the Ordnance, free and vouched to
                                     # the King's ships of the port's nation; merchants: at
                                     # a price
      sells: false                   # an ordnance port: whether the town's merchants sell
      roads: [outer_road, anchorage] # the spots where powder is taken in; omitted: anywhere
      roads_words: Plymouth Sound or Cawsand Bay
      hoy_hours: 4                   # the demand and the hoy's errand
      barrels_an_hour: 20            # the taking in
      shot_tons_an_hour: 2
      powder_per_barrel_pounds: 5.0  # a sale's price
      shot_per_ton_pounds: 12.0
      sells_in_war_to: [britain]     # a neutral's knob: a belligerent not listed is not served
      source: "..."

A port with no block has none to be had. `parse_block` refuses a key it does not know in
words; `block_of` reads a port's block, and for a `Port` pickled before this build reads
it once from the port's file.

**Who gets what** (the owner's ruling of 2026-10-25). The Ordnance issues free and vouched
to the King's ships of the port's own nation (`world.service.service_of`), at the roads
only where the block names them: the Regulations of 1806 (1808 printing), the Gunner, Art.
VI (l.12833-12839), "Plymouth Sound or Cawsand Bay, Spithead, ...". Everyone else buys of
the merchants, at an Ordnance port only where it `sells`; a King's ship bound by the
Regulations (`service.under_the_regulations`: of Britain's) buys of them only of necessity,
from the purse, "Captains are strictly charged not to purchase Stores of any description
without an absolute necessity" (the Captain, Art. VII, l.6220-6252); a man of war of another
nation buys of them as everyone else does. A neutral's merchants may serve only the
belligerents its knob lists. The port's stance is read first, as the yard reads it.

**The hoy** is a port job (`Ports.jobs`, the lighter's precedent), never a vessel: it
draws nothing and adds no serial. At `hoy_hours` it comes **alongside**: she must still
lie in the port, and for an issue at its roads, or it goes back with the powder; a sale is
paid now from the purse, or the hoy goes back. With powder in her the galley fire is put
out, no light allowed but in the light room, and no man to smoke (Art. V, l.12800-12809);
the galley's state is the purser's stores' (`Stores.galley_fire_out`), which the person's
meal and the company's read. After the taking in, a barrel's and a ton's pace, at least an
hour, the powder and shot are **stowed**: received into the magazine as one transaction,
the magazine secured and the keys to the captain (l.12815-12827), the galley fire lit
again, the gunner's empty barrels returned to the storekeeper at a shilling apiece his own
(Art. IX, l.12887-12902), and the gunner's account written up. If she weighs while the hoy
is alongside, the stowed stage comes at the next minute (`left_behind`): nothing received,
a sale's money given back, and the galley fire lit again as she goes. A hoy that goes back
goes back with what it brought: the powder, or the shot of a hoy with no barrel in her
(`_cargo`, as the port's reading says it).

Everything here is read from the state the World has and the port's file; nothing is drawn,
so a replay has it again and a checkpoint holds the jobs whole.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from datetime import timedelta
from pathlib import Path
from typing import Any

import yaml

from freesail.core.events import Severity
from freesail.world.places import pounds_words

__all__ = [
    "ALONGSIDE",
    "BLOCK_KEYS",
    "ISSUE",
    "JOB_KIND",
    "KINDS",
    "SALE",
    "STOWED",
    "TON_LB",
    "Ask",
    "Part",
    "apply_job",
    "at_the_roads",
    "block_of",
    "goods_words",
    "hoy_words",
    "left_behind",
    "parse_block",
    "pending",
    "take_in",
]

# The block's kinds: the storekeeper of the Ordnance at the port (the Regulations of 1806,
# the Gunner, Art. I, l.12722-12738: the gunner applies "to the Store-keeper of the
# Ordnance at the Port" for the ammunition put into the hoys), or the port's merchants.
KINDS: tuple[str, ...] = ("ordnance", "merchants")
BLOCK_KEYS: tuple[str, ...] = (
    "kind",
    "sells",
    "roads",
    "roads_words",
    "hoy_hours",
    "barrels_an_hour",
    "shot_tons_an_hour",
    "powder_per_barrel_pounds",
    "shot_per_ton_pounds",
    "sells_in_war_to",
    "source",
)
# The spots of a port a block's `roads` may name (`Port.spots`).
SPOT_KEYS: tuple[str, ...] = ("outer_road", "anchorage", "mooring")
# The figures a block leaves out (judgement, as the block's own are).
DEFAULTS: dict[str, float] = {
    "hoy_hours": 3.0,
    "barrels_an_hour": 20.0,
    "shot_tons_an_hour": 2.0,
    "powder_per_barrel_pounds": 5.0,
    "shot_per_ton_pounds": 12.0,
}
# The long ton of 2240 pounds, the weight shot was reckoned by.
TON_LB = 2240.0
# The hoy's job (`Ports.jobs`): its kind, its two stages, and how she has it.
JOB_KIND = "ordnance"
ALONGSIDE = "alongside"
STOWED = "stowed"
ISSUE = "issue"
SALE = "sale"
# A shot's kinds as the lockers hold them (`Magazine.shot`), in the order the words give.
SHOT_KINDS: tuple[str, ...] = ("round", "grape", "chain")

NO_GUNS_WORDS = "She carries no guns; there is no magazine to fill."
NOT_IN_PORT_WORDS = (
    "She is not in port: powder and shot are taken in at a port, of the Ordnance or a merchant."
)
NECESSITY_WORDS = "of absolute necessity, on the captain's word, for the Admiralty's account"


# ---------------------------------------------------------------------------
# The block
# ---------------------------------------------------------------------------


def parse_block(raw: Any, where: str) -> dict[str, Any] | None:
    """The port file's `ordnance:` block as data, or None when the file has none; refused
    in words for a key it does not know, a kind not one of `KINDS`, a road that is not a
    spot of the port, or a figure that is not a positive number."""
    if raw is None:
        return None
    if not isinstance(raw, dict):
        raise ValueError(f"{where}: 'ordnance' is not a mapping")
    unknown = [str(k) for k in raw if str(k) not in BLOCK_KEYS]
    if unknown:
        raise ValueError(
            f"{where}: the ordnance block has no key '{unknown[0]}'; its keys are "
            f"{', '.join(BLOCK_KEYS)}"
        )
    kind = str(raw.get("kind") or "")
    if kind not in KINDS:
        raise ValueError(
            f"{where}: the ordnance block's kind '{kind}' is not one of {', '.join(KINDS)}"
        )
    roads = raw.get("roads")
    if roads is not None:
        if not isinstance(roads, list) or not roads:
            raise ValueError(f"{where}: the ordnance block's roads are a list of the port's spots")
        roads = [str(r) for r in roads]
        bad = [r for r in roads if r not in SPOT_KEYS]
        if bad:
            raise ValueError(
                f"{where}: the ordnance block's road '{bad[0]}' is not a spot of the port "
                f"({', '.join(SPOT_KEYS)})"
            )
        if not raw.get("roads_words"):
            raise ValueError(f"{where}: the ordnance block names its roads in roads_words")
    out: dict[str, Any] = {
        "kind": kind,
        "sells": bool(raw.get("sells", kind == "merchants")),
        "roads": tuple(roads) if roads is not None else None,
        "roads_words": str(raw.get("roads_words") or ""),
        "sells_in_war_to": None,
        "source": str(raw.get("source") or ""),
    }
    for key, default in DEFAULTS.items():
        value = raw.get(key, default)
        try:
            figure = float(value)
        except (TypeError, ValueError):
            figure = math.nan
        # a price may be nothing; a time or a pace must be more than nothing
        least_ok = figure >= 0.0 if key.endswith("_pounds") else figure > 0.0
        if not least_ok:
            raise ValueError(
                f"{where}: the ordnance block's {key} '{value}' is not a positive number"
            )
        out[key] = figure
    listed = raw.get("sells_in_war_to")
    if listed is not None:
        if not isinstance(listed, list):
            raise ValueError(f"{where}: the ordnance block's sells_in_war_to is a list of nations")
        out["sells_in_war_to"] = tuple(str(n).lower() for n in listed)
    return out


def block_of(port: Any) -> dict[str, Any] | None:
    """The port's block, or None when it has none. A `Port` pickled before this build has
    no `ordnance` of its own: it is read once and kept, from this build's file of the same
    port (`ports.PORTS_DIR`), and only when there is none such from the file the port was
    loaded from (`port.path`); None when neither is there. The pickled path is absolute and
    names the folder the game was first played in, an older checkout whose file has no
    block (every port of the kept saves in tests/fixtures/saves names another folder), so
    it is read last."""
    if "ordnance" not in vars(port):
        from freesail.world.ports import PORTS_DIR

        pid = str(getattr(port, "id", "") or "")
        old = str(getattr(port, "path", "") or "")
        paths = [PORTS_DIR / f"{pid}.yaml"] if pid else []
        paths += [Path(old)] if old else []
        block = None
        for path in paths:
            try:
                doc = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
            except (OSError, ValueError):
                continue
            block = parse_block(doc.get("ordnance"), str(path))
            break
        port.ordnance = block
    return port.ordnance


def at_the_roads(world: Any, port: Any, block: dict[str, Any]) -> bool:
    """Whether she lies where the block takes powder in: at one of its roads by the spot
    nearest her (`Port.nearest_spot`), or anywhere in the port when it names none."""
    roads = block.get("roads")
    if not roads:
        return True
    pos = getattr(world, "position", None)
    if pos is None:
        return False
    spot = port.nearest_spot(pos)[0]
    return any(spot == getattr(port, key, None) for key in roads)


def _refused_in_war(world: Any, block: dict[str, Any]) -> bool:
    """A neutral's knob: a ship whose nation has an enemy and is not listed is not served."""
    listed = block.get("sells_in_war_to")
    if listed is None:
        return False
    nation = str(world.ports.ship_nation).lower()
    if not world.nations.enemies_of(nation):
        return False
    return nation not in listed


# ---------------------------------------------------------------------------
# What is asked (read by `orders.ordnance` from the order's words)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class Part:
    """One quantity in the words: `what` is "barrels" (of powder), "cartridges" (powder
    for so many, at the guns' charge), "shot" (by its kind) or "tons" (of round shot);
    `keys` the guns it is for, by kind and calibre (none named: every gun of hers)."""

    what: str
    n: float
    keys: tuple[tuple[str, float], ...] = ()
    kind: str = "round"


@dataclass(frozen=True)
class Ask:
    """The order read: whether it says powder, shot or both; the necessity; the quantities
    (none: complete to what the magazine wants); the guns named without a number; and the
    words' own refusal, said after the port's (§3.2's twelfth)."""

    powder: bool = True
    shot: bool = True
    necessity: bool = False
    parts: tuple[Part, ...] = ()
    keys: tuple[tuple[str, float], ...] = ()
    error: str = ""


# ---------------------------------------------------------------------------
# The demand
# ---------------------------------------------------------------------------


def pending(ports: Any, port_id: str | None = None) -> Any:
    """The hoy's job in hand at the port (any port when `port_id` is None), or None: a hoy
    coming off at one port neither stops a demand at another nor shows in its reading."""
    for job in getattr(ports, "jobs", None) or ():
        if job.kind == JOB_KIND and (port_id is None or job.port_id == port_id):
            return job
    return None


def left_behind(ports: Any) -> list[Any]:
    """The hoys alongside a ship that is no longer in their port (she weighed while the
    powder came aboard): their stowed stage is brought forward to now, so that the galley
    fire is lit again as she goes, not hours later at sea when the taking in would have
    ended. Nothing is read but the jobs and where she lies."""
    stowing = [
        j
        for j in getattr(ports, "jobs", None) or ()
        if j.kind == JOB_KIND and j.payload.get("stage") == STOWED
    ]
    if not stowing:
        return []
    here = ports.in_port()
    return [j for j in stowing if here is None or here.id != j.port_id]


def take_in(world: Any, ask: Ask) -> tuple[str, dict[str, Any]]:
    """The order carried out: refused in words in the build design's order (§3.2), else
    the hoy's job queued and the answer's words and data."""
    from freesail.orders.errors import OrderError
    from freesail.ship.parts import BARREL_LB, magazine
    from freesail.world.ports import Job, _hours_words, _possessive
    from freesail.world.service import KINGS, service_of, under_the_regulations

    ship = world.ship
    if not getattr(ship, "guns", None):
        raise OrderError(NO_GUNS_WORDS)
    ports = world.ports
    port = ports.in_port()
    if port is None:
        raise OrderError(NOT_IN_PORT_WORDS)
    stance = ports.stance(port)
    if stance in ("hostile", "closed"):
        raise OrderError(f"{port.name} is {stance} to her; no powder will be issued or sold her.")
    block = block_of(port)
    if block is None:
        raise OrderError(
            f"There is no powder or shot to be had at {port.name}: no storekeeper of the "
            "Ordnance, and no merchant who deals in it."
        )
    now = world.clock.tick
    job = pending(ports, port.id)
    if job is not None:
        # the hours left to the minute, as a clock is read
        left = _hours_words(math.ceil(max(0, job.due_tick - now) / 60.0) / 60.0)
        if job.payload.get("stage") == STOWED:
            raise OrderError(
                f"The hoy is alongside with her powder already; it will be struck down in {left}."
            )
        raise OrderError(
            f"The hoy is coming off with her powder already; it will be alongside in {left}."
        )
    kings = service_of(world) == KINGS
    # the Regulations' necessity binds a King's ship of Britain's; a man of war of another
    # nation buys of the merchants as everyone else does (the review's finding)
    bound = under_the_regulations(world)
    issue = block["kind"] == "ordnance" and kings and stance == "open"
    if not issue and block["kind"] == "ordnance" and not block["sells"]:
        raise OrderError(
            f"The Ordnance's storekeeper at {port.name} issues to the King's ships alone, and "
            "no merchant here sells powder."
        )
    if not issue and bound and not ask.necessity:
        # at an Ordnance port whose storekeeper is not hers (its merchants selling) there is
        # a storekeeper: the words say he does not issue to her (the review's finding: "There
        # is no storekeeper of the Ordnance at Gibraltar")
        nobody = (
            f"The Ordnance's storekeeper at {port.name} does not issue to her"
            if block["kind"] == "ordnance"
            else f"There is no storekeeper of the Ordnance at {port.name}"
        )
        raise OrderError(
            f"{nobody}, and a captain is charged not to purchase stores without an absolute "
            "necessity (the Regulations): say 'buy powder of necessity' to buy it of the "
            f"merchants at {pounds_words(block['powder_per_barrel_pounds'])} a barrel."
        )
    if issue and not at_the_roads(world, port, block):
        raise OrderError(
            f"Powder is taken in at {block['roads_words']}, not in the harbour (the "
            "Regulations, the Gunner, Art. VI): weigh and bring her to the road first."
        )
    if not issue and _refused_in_war(world, block):
        adjective = world.nations.get(ports.ship_nation).adjective
        raise OrderError(
            f"{_possessive(port.name)} merchants sell no powder to {_a(adjective)} ship while "
            "the war lasts."
        )
    mag = magazine(ship)
    want = mag.wanting()
    if want.empty:
        raise OrderError(f"Her magazine is complete: {_first_line(mag, world)}")
    if ask.error:
        raise OrderError(ask.error)
    barrels, shot, cut = _quantities(mag, want, ask)
    if barrels <= 0 and not shot:
        powder_asked = ask.powder or any(p.what in ("barrels", "cartridges") for p in ask.parts)
        shot_asked = ask.shot or any(p.what in ("shot", "tons") for p in ask.parts)
        what = {(True, True): "powder or shot", (True, False): "powder"}.get(
            (powder_asked, shot_asked), "shot"
        )
        raise OrderError(f"Her magazine wants no more {what}: {_first_line(mag, world)}")
    words = goods_words(barrels, shot)
    cost = 0.0 if issue else _cost(block, barrels, shot)
    purse = world.purse
    if cost > purse.pounds + 1e-9:
        raise OrderError(
            f"{_cap(words)} costs {pounds_words(cost)} and the purse holds {purse.words()}."
        )
    hours = float(block["hoy_hours"])
    due = now + int(round(hours * 3600))
    payload = {
        "stage": ALONGSIDE,
        "how": ISSUE if issue else SALE,
        "necessity": bool(ask.necessity and not issue and bound),
        "powder_lb": barrels * BARREL_LB,
        "barrels": barrels,
        "shot": {_calibre_key(p): dict(kinds) for p, kinds in shot.items()},
        "cost": cost,
        "words": words,
    }
    ports.jobs.append(Job(due, JOB_KIND, port.id, payload))
    room = f" ({'; '.join(cut)})" if cut else ""
    if issue:
        how = f"of the Ordnance's storekeeper at {port.name}, issued and vouched{room}"
    else:
        need = f", {NECESSITY_WORDS}" if payload["necessity"] else ""
        how = (
            f"of the merchants at {port.name} for {pounds_words(cost)}{need}, paid when it "
            f"comes alongside{room}"
        )
    text = f"Demanded {words} {how}; the hoy will be alongside in {_hours_words(hours)}."
    return text, {
        "port": port.id,
        "how": payload["how"],
        "necessity": payload["necessity"],
        "barrels": barrels,
        "powder_lb": payload["powder_lb"],
        "shot": payload["shot"],
        "cost_pounds": cost,
        "hours": hours,
        "due_tick": due,
    }


def _quantities(
    mag: Any, want: Any, ask: Ask
) -> tuple[int, dict[float, dict[str, int]], list[str]]:
    """The barrels and the shot to take in, each cut to what the magazine wants, and the
    words for each cut ('the magazine has room for 12 barrels')."""
    from freesail.ship.parts import BARREL_LB

    cut: list[str] = []
    room_shot = {float(p): dict(kinds) for p, kinds in (want.shot or {}).items()}
    powder_parts = [p for p in ask.parts if p.what in ("barrels", "cartridges")]
    shot_parts = [p for p in ask.parts if p.what in ("shot", "tons")]
    barrels = 0
    if powder_parts:
        whole = 0
        lb = 0.0
        for part in powder_parts:
            if part.what == "barrels":
                whole += int(math.ceil(part.n - 1e-9))
            else:
                kind, pounder = part.keys[0]
                lb += part.n * mag.charge_of(kind, pounder)
        asked = whole + int(math.ceil(lb / BARREL_LB - 1e-9))
        barrels = min(asked, max(0, int(want.barrels)))
        if barrels < asked:
            cut.append(f"the magazine has room for {_barrels_words(max(0, int(want.barrels)))}")
    elif ask.powder:
        barrels = max(0, int(want.barrels))
    shot: dict[float, dict[str, int]] = {}
    if shot_parts:
        asked_shot: dict[float, dict[str, int]] = {}
        for part in shot_parts:
            pounder = float(part.keys[0][1])
            n = int(part.n) if part.what == "shot" else int(part.n * TON_LB // pounder)
            kinds = asked_shot.setdefault(pounder, {})
            kinds[part.kind] = kinds.get(part.kind, 0) + n
        for pounder, kinds in asked_shot.items():
            for kind, n in kinds.items():
                room = max(0, int(room_shot.get(pounder, {}).get(kind, 0)))
                got = min(n, room)
                if got < n:
                    cut.append(
                        f"the shot lockers have room for {room} {kind} shot of "
                        f"{_pounds_words(pounder)}"
                    )
                if got > 0:
                    shot.setdefault(pounder, {})[kind] = got
    elif ask.shot:
        calibres = {float(p) for _k, p in ask.keys}
        for pounder, kinds in room_shot.items():
            if calibres and pounder not in calibres:
                continue
            got = {k: int(n) for k, n in kinds.items() if int(n) > 0}
            if got:
                shot[pounder] = got
    return barrels, shot, cut


def _cost(block: dict[str, Any], barrels: int, shot: dict[float, dict[str, int]]) -> float:
    """A sale's price: the barrels and the shot's weight in tons at the block's prices, to
    the shilling (a shot of grape or chain weighed as the calibre's round shot: judgement)."""
    tons = _shot_tons(shot)
    raw = barrels * float(block["powder_per_barrel_pounds"])
    raw += tons * float(block["shot_per_ton_pounds"])
    return math.floor(raw * 20.0 + 0.5) / 20.0  # to the shilling, a half up


def _shot_tons(shot: dict[Any, dict[str, int]]) -> float:
    return sum(float(p) * int(n) for p, kinds in shot.items() for n in kinds.values()) / TON_LB


# ---------------------------------------------------------------------------
# The hoy's two stages (`Ports._apply_job`)
# ---------------------------------------------------------------------------


def apply_job(ports: Any, job: Any, port: Any) -> None:
    """The hoy's job when due: alongside, then stowed."""
    stage = job.payload.get("stage")
    if stage == ALONGSIDE:
        _alongside(ports, job, port)
    elif stage == STOWED:
        _stowed(ports, job, port)


def _here(ports: Any, port: Any) -> bool:
    here = ports.in_port()
    return here is not None and here.id == port.id


def _alongside(ports: Any, job: Any, port: Any) -> None:
    from freesail.world.ports import Job

    world = ports.world
    pay = dict(job.payload)
    block = block_of(port) or {}
    issue = pay.get("how") == ISSUE
    data = {"port": port.id, "how": pay.get("how"), "stage": ALONGSIDE}
    cargo = _cargo(pay)
    if not _here(ports, port) or (issue and not at_the_roads(world, port, block)):
        ports._record(
            Severity.NOTABLE,
            "ordnance.missed",
            f"The hoy came off and found her gone from the road; it went back with the {cargo}.",
            data | {"why": "gone"},
        )
        return
    now = world.clock.tick
    cost = float(pay.get("cost") or 0.0)
    if not issue and cost > 0:
        purse = world.purse
        if cost > purse.pounds + 1e-9:
            ports._record(
                Severity.NOTABLE,
                "ordnance.missed",
                f"The merchants' hoy came alongside, but the purse holds {purse.words()} "
                f"against {pounds_words(cost)}; it went back with the {cargo}.",
                data | {"why": "purse", "cost_pounds": cost},
            )
            return
        purse.pay(cost, f"powder and shot of the merchants at {port.name}", now)
    whose = "The Ordnance's hoy" if issue else "The merchants' hoy"
    powder = int(pay.get("barrels") or 0) > 0
    stores = getattr(world, "stores", None)
    if powder:
        if stores is not None:
            stores.galley_fire_out = "powder"
        rule = " (the Regulations, the Gunner, Art. V)" if issue else ""
        text = (
            f"{whose} is alongside with the powder: the galley fire is put out, no light "
            f"allowed but in the light room, and no man to smoke{rule}."
        )
    else:
        text = f"{whose} is alongside with the shot."
    ports._record(
        Severity.NOTABLE,
        "ordnance.alongside",
        text,
        data
        | {
            "barrels": int(pay.get("barrels") or 0),
            "shot": dict(pay.get("shot") or {}),
            "cost_pounds": cost,
            "galley_fire_out": powder,
        },
    )
    barrels_an_hour = float(block.get("barrels_an_hour") or DEFAULTS["barrels_an_hour"])
    tons_an_hour = float(block.get("shot_tons_an_hour") or DEFAULTS["shot_tons_an_hour"])
    hours = max(
        1.0,
        int(pay.get("barrels") or 0) / barrels_an_hour
        + _shot_tons(pay.get("shot") or {}) / tons_an_hour,
    )
    ports.jobs.append(
        Job(now + int(round(hours * 3600)), JOB_KIND, port.id, pay | {"stage": STOWED})
    )


def _stowed(ports: Any, job: Any, port: Any) -> None:
    from freesail import units
    from freesail.ship.parts import magazine
    from freesail.world.reckoning import number_words

    world = ports.world
    pay = dict(job.payload)
    issue = pay.get("how") == ISSUE
    stores = getattr(world, "stores", None)
    lit = stores is not None and getattr(stores, "galley_fire_out", "") == "powder"
    if stores is not None:
        stores.galley_fire_out = ""
    now = world.clock.tick
    cost = float(pay.get("cost") or 0.0)
    data = {"port": port.id, "how": pay.get("how"), "stage": STOWED}
    if not _here(ports, port):
        text = (
            f"She weighed before the {_cargo(pay)} was struck down: nothing was taken in, and "
            "the hoy went back with it"
        )
        if not issue and cost > 0:
            # nothing received, nothing paid: the merchants' money given back at the side
            world.purse.take(
                cost, f"the powder and shot of the merchants at {port.name} returned", now
            )
            text += f", the {pounds_words(cost)} paid returned"
        if lit:
            text += "; the galley fire lit again"
        ports._record(Severity.NOTABLE, "ordnance.missed", text + ".", data | {"why": "weighed"})
        return
    shot = {
        float(p): {str(k): int(n) for k, n in kinds.items()}
        for p, kinds in (pay.get("shot") or {}).items()
    }
    clock = world.clock
    when = f"{clock.ship_time:%d %B}, {units.time_stamp(clock.ship_time)}"
    goods = str(pay.get("words") or goods_words(int(pay.get("barrels") or 0), shot))
    if issue:
        source = "issued by the Ordnance's storekeeper and vouched"
        account = (
            f"Received of the Ordnance's storekeeper at {port.name}, issued and vouched: {goods}"
        )
    else:
        need = f", {NECESSITY_WORDS}" if pay.get("necessity") else ""
        source = f"bought of the merchants at {port.name} for {pounds_words(cost)}{need}"
        account = f"Bought of the merchants at {port.name} for {pounds_words(cost)}{need}: {goods}"
    mag = magazine(world.ship)
    mag.receive(float(pay.get("powder_lb") or 0.0), shot, when=when, words=account)
    head = goods_words(int(pay.get("barrels") or 0), shot, spelled=True)
    if int(pay.get("barrels") or 0) > 0:
        done = (
            f"{head} struck down and stowed, {source}; the magazine secured and the keys to "
            "the captain"
        )
    else:
        done = f"{head} struck down into the shot lockers, {source}"
    if lit:
        done += "; the galley fire lit again"
    returned = 0
    if issue:
        returned = int(mag.return_barrels())
        if returned:
            done += (
                f"; the gunner returns {number_words(returned)} empty "
                f"barrel{'s' if returned != 1 else ''} to the storekeeper, a shilling apiece "
                "his own"
            )
    ports._record(
        Severity.NOTABLE,
        "ordnance.stowed",
        _cap(done) + ".",
        data
        | {
            "barrels": int(pay.get("barrels") or 0),
            "powder_lb": float(pay.get("powder_lb") or 0.0),
            "shot": dict(pay.get("shot") or {}),
            "cost_pounds": cost,
            "barrels_returned": returned,
        },
    )
    papers = getattr(world, "papers", None)
    if papers is not None:
        ports._record(
            Severity.ROUTINE,
            "paper.written",
            papers.write("the gunner's account", done),
            {"paper": "the gunner's account"},
        )


def hoy_words(ports: Any, port_id: str | None = None) -> tuple[str, dict[str, Any]] | None:
    """The hoy in the port's reading while its job is in hand at that port: coming off,
    with the hour it will be alongside, or alongside with the powder coming aboard; None
    otherwise."""
    job = pending(ports, port_id)
    if job is None:
        return None
    pay = job.payload
    cargo = _cargo(pay)
    clock = ports.world.clock
    data = {"how": pay.get("how"), "due_tick": job.due_tick}
    if pay.get("stage") == STOWED:
        return f"the hoy alongside, the {cargo} coming aboard", data | {"stage": "alongside"}
    whose = "the Ordnance's hoy" if pay.get("how") == ISSUE else "the merchants' hoy"
    at = clock.ship_time + timedelta(seconds=max(0, job.due_tick - clock.tick))
    return (
        f"{whose} coming off with her {cargo}, alongside about {at:%H:%M}",
        data | {"stage": "coming off"},
    )


# ---------------------------------------------------------------------------
# Words
# ---------------------------------------------------------------------------


def goods_words(barrels: int, shot: dict[Any, dict[str, int]], spelled: bool = False) -> str:
    """'2 barrels of powder and 149 round shot of 12 pounds'; `spelled`, the barrels in
    words as a line begins with them ('two barrels of powder and ...')."""
    bits = []
    if barrels > 0:
        bits.append(_barrels_words(barrels, spelled) + " of powder")
    for pounder in sorted(shot, key=lambda p: -float(p)):
        kinds = shot[pounder]
        named = [k for k in SHOT_KINDS if int(kinds.get(k, 0)) > 0]
        named += [k for k in kinds if k not in SHOT_KINDS and int(kinds[k]) > 0]
        if not named:
            continue
        counted = [f"{int(kinds[k])} {k}" for k in named]
        bits.append(f"{_and(counted)} shot of {_pounds_words(float(pounder))}")
    return _and(bits) if bits else "nothing"


def _barrels_words(n: int, spelled: bool = False) -> str:
    if spelled:
        from freesail.world.reckoning import number_words

        if n == 1:
            return "a barrel"
        return f"{number_words(n)} barrels"
    return f"{n} barrel{'s' if n != 1 else ''}"


def _pounds_words(pounder: float) -> str:
    """'12 pounds', 'half a pound': the shot's weight as the words name its calibre."""
    if pounder == 0.5:
        return "half a pound"
    if pounder == 1.0:
        return "1 pound"
    return f"{pounder:g} pounds"


def _calibre_key(pounder: float) -> str:
    """A calibre as the job's payload and the events' data key it: '12', '0.5'."""
    return f"{float(pounder):g}"


def _cargo(pay: Any) -> str:
    """What the hoy brings, in a word: 'powder' with a barrel in her, else 'shot' (the
    review's finding: a hoy of shot alone 'went back with the powder')."""
    return "powder" if int(pay.get("barrels") or 0) > 0 else "shot"


def _first_line(mag: Any, world: Any) -> str:
    from freesail.combat.filling import magazine_lines

    lines = magazine_lines(world, world.ship, mag)
    return lines[0] if lines else "the gunner has nothing to count"


def _a(word: str) -> str:
    return f"an {word}" if word[:1].lower() in "aeiou" else f"a {word}"


def _cap(text: str) -> str:
    return text[:1].upper() + text[1:]


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
