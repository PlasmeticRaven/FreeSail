"""Hunger, thirst and fatigue (spec M7b §20; package 54): the named people's needs, in a
few steps each, rising with the ship's time, eased by eating, drinking and sleeping.

**By hand at a filled station, automatic elsewhere** (the owner's ruling of 2026-10-15). A
person is *stationed* while a station bound to him is held: by a model (a harness), by the
player at his seat (`agents.seat`), or, for the captain, by the player at the prompt while
no model holds the captain's station and the player is seated nowhere else (the rule of
reach's `held_stations`, package 52). A stationed person's needs are his to see to by his
own orders (`eat`, `drink`, `sleep`; `stand by, asleep below until called` at a model's
station); everyone else's are the game's, reckoned from the clock as the routine keeps the
company (fed at the meals, asleep at night) and never shown. When a person comes to be
stationed his needs are taken up from what the routine had made of them (`take_in_hand`),
and when nobody holds him any longer the routine has him again.

**The steps** are `data/crew/needs.yaml`'s: the hours since he last ate or drank, and for
fatigue the hours of waking he owes, which a sleep below makes up eight to the hour and a
sleep where he fell asleep four. A person who is also a hand (drawn from a station of the
muster) has the crew's fatigue (`crew/hands.py`), read at the file's bounds: the watch bill
rests him, and he never falls asleep where he is.

**Never busywork.** No line until the second step; a notable line waits for the change of
the watch and there is at most one a watch, every need that has risen since said together;
an urgent line is said at once. A line goes only to the person stationed: into a model's
next sample as a notice (and the sample's `needs` while any need shows), or to the player
through the keeper's listeners (the console prints it, the browser's page shows it), never
into the log, so that no passage's log or pin moves for the needs. While he sleeps he is
told nothing; what rose meanwhile is told when he wakes. The ends (death by hunger or
thirst, collapse by fatigue, the surgeon) are M7's: the needs stop at the last step's
urgent line, and for fatigue at a man who falls asleep where he is (a model's station
standing by, asleep, until called; the player woken by his next order).

Nothing here draws randomness or writes the log: the needs are a function of the clock,
the stations held and the persons' own orders, which the save replays.
"""

from __future__ import annotations

import functools
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

import yaml

from freesail.core.events import Event, Severity
from freesail.world.places import PLACES, place_words

__all__ = [
    "FATIGUE",
    "HUNGER",
    "NEEDS_PATH",
    "THIRST",
    "Needs",
    "NeedsKeeper",
    "NeedsTable",
    "Step",
    "load_needs",
    "needs_of",
]

NEEDS_PATH = Path(__file__).resolve().parents[2] / "data" / "crew" / "needs.yaml"

HUNGER, THIRST, FATIGUE = "hunger", "thirst", "fatigue"
# the order a line names them in: what is most pressing in a man's day first
NEED_ORDER = (THIRST, HUNGER, FATIGUE)

SILENT, NOTABLE, URGENT = "silent", "notable", "urgent"

# The kind of a line to the player (never in the log), and of an answer to a person's own
# order (`core.world.UNLOGGED_KINDS`: an answer for the one who asked).
FELT_KIND = "needs.felt"
ANSWER_KIND = "needs.answer"

# Under this many hours of waking a man has slept his fill and would wake at once: he does
# not turn in (judgement).
RESTED_UNDER_H = 1.0

# The routine's night, as the watch routine has it (`crew.routine`): an unseated person is
# reckoned asleep from the end of the second dog watch to the start of the morning watch.
NIGHT_ENDS_HOUR = 4


@dataclass(frozen=True)
class Step:
    hours: float
    words: str
    severity: str = SILENT
    asleep: bool = False


@dataclass(frozen=True)
class NeedsTable:
    steps: dict[str, tuple[Step, ...]]
    sleep_below_per_hour: float
    sleep_where_per_hour: float
    hand_bounds: tuple[float, ...]
    places_with_food: frozenset[str]
    short_allowance_hours_left: float
    berths: dict[str, str]
    foul_water_hours: float

    def step(self, need: str, hours: float) -> int:
        """The step a need is at after so many hours: 0 below the first."""
        return sum(1 for s in self.steps[need] if hours >= s.hours)

    def berth(self, role: str) -> str:
        return self.berths.get(role, self.berths.get("default", "gunroom"))


@functools.lru_cache(maxsize=4)
def load_needs(path: str | Path = NEEDS_PATH) -> NeedsTable:
    raw = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    steps: dict[str, tuple[Step, ...]] = {}
    for need in (HUNGER, THIRST, FATIGUE):
        entries = (raw.get(need) or {}).get("steps") or []
        made = tuple(
            Step(
                float(e["hours"]),
                str(e["words"]),
                str(e.get("severity") or SILENT),
                bool(e.get("asleep", False)),
            )
            for e in entries
        )
        if any(b.hours <= a.hours for a, b in zip(made, made[1:], strict=False)):
            raise ValueError(f"{path}: the {need} steps must rise with the hours.")
        steps[need] = made
    fatigue = raw.get(FATIGUE) or {}
    return NeedsTable(
        steps=steps,
        sleep_below_per_hour=float(fatigue.get("sleep_below_per_hour", 8)),
        sleep_where_per_hour=float(fatigue.get("sleep_where_he_is_per_hour", 4)),
        hand_bounds=tuple(float(b) for b in fatigue.get("hand_bounds") or ()),
        places_with_food=frozenset(str(p) for p in raw.get("places_with_food") or ()),
        short_allowance_hours_left=float(raw.get("short_allowance_hours_left", 8)),
        berths={str(k): str(v) for k, v in (raw.get("berths") or {}).items()},
        foul_water_hours=float(raw.get("foul_water_hours", 6)),
    )


@dataclass
class Needs:
    """One person's needs: when he last ate and drank (ticks), the hours of waking he owes
    as at `at`, whether he is asleep (below, or where he fell asleep), whether they are his
    by hand, and the step of each need he was last told of."""

    ate: int = 0
    drank: int = 0
    awake_h: float = 0.0
    at: int = 0
    asleep: str = ""  # "", "below" or "where he is"
    by_hand: bool = False
    told: dict[str, int] = field(default_factory=dict)
    # where he turned in from, to go back to when he is called
    turned_in_from: str = ""


def needs_of(person: Any) -> Needs:
    """The person's needs, made at the first look (a person of a checkpoint from before
    package 54 has none)."""
    n = getattr(person, "needs", None)
    if n is None:
        n = Needs()
        person.needs = n
    return n


Listener = Callable[[Event], None]


class NeedsKeeper:
    """The needs of one World's people, ticked once a minute (`World._tick_needs`)."""

    def __init__(self, world: Any) -> None:
        self.world = world
        self._watch: str | None = None
        self.listeners: list[Listener] = []

    # the listeners are the drivers' (the console's print, the server's page), not state
    def __getstate__(self) -> dict[str, Any]:
        state = dict(self.__dict__)
        state["listeners"] = []
        return state

    def __setstate__(self, state: dict[str, Any]) -> None:
        self.__dict__.update(state)
        self.__dict__.setdefault("listeners", [])

    def listen(self, fn: Listener) -> None:
        self.listeners.append(fn)

    def unlisten(self, fn: Listener) -> None:
        if fn in self.listeners:
            self.listeners.remove(fn)

    @property
    def table(self) -> NeedsTable:
        return load_needs()

    # -- who is stationed --------------------------------------------------------------

    def stationed(self, prompt: bool | None = None) -> list[tuple[Any, Any]]:
        """The persons stationed now, each with what holds him: a harness (a model's
        station), the player's seat, or None for the player at the prompt as the captain.
        A station bound to nobody named, and the director's, hold no person.

        **The player at the prompt** holds the captain's station while no model holds it
        and he is seated nowhere else; he is at the prompt when a driver listens for his
        lines (the console, the browser's page) or when he has given an order of his own
        needs (`prompt=True`, which `person_of` asks for, so that a replay with no driver
        answers his `eat` as the game did). A world with neither (a test, a passage sailed
        by its book) has nobody at the prompt, and the captain is the routine's."""
        from freesail.agents.agent import CAPTAIN, DIRECTOR
        from freesail.agents.harness import _stations_held

        world = self.world
        people = getattr(world, "people", None)
        stations = getattr(world, "stations", None)
        if people is None:
            return []
        out: list[tuple[Any, Any]] = []
        seen: set[int] = set()
        held: set[str] = set()
        for h in _stations_held(world):
            name = h.station.name
            if name == DIRECTOR:
                continue
            held.add(name)
            try:
                p = stations.holder(name) if stations is not None else None
            except Exception:  # noqa: BLE001  (a people's build that cannot run binds nobody)
                p = None
            if p is None or id(p) in seen:
                continue
            seen.add(id(p))
            out.append((p, h))
        seat = getattr(world, "player_seat", None)
        if CAPTAIN not in held and (seat is None or seat.agent.released):
            built = bool(getattr(people, "_built", True))
            if prompt is None:
                prompt = bool(self.listeners)
                if not prompt and built:
                    # an order of his own needs took him in hand: his while he holds it
                    cap = _captain(people)
                    n = getattr(cap, "needs", None) if cap is not None else None
                    prompt = n is not None and n.by_hand
            if prompt:
                cap = _captain(people)
                if cap is not None and id(cap) not in seen:
                    out.append((cap, None))
        return out

    def holder_of(self, person: Any) -> tuple[bool, Any]:
        """(whether the person is stationed, what holds him)."""
        for p, h in self.stationed():
            if p is person:
                return True, h
        return False, None

    # -- the automatic reckoning ---------------------------------------------------------

    def _tick_at(self, when: datetime) -> int:
        clock = self.world.clock
        return max(0, int((when - clock.start).total_seconds()))

    def _last_meal_tick(self) -> int:
        """The tick of the last meal served (the ration's meals), or the start: the
        scenario opens on a company fed and rested (judgement)."""
        from freesail.crew.victuals import load_ration

        now = self.world.clock.ship_time
        best: datetime | None = None
        for hour, _name in load_ration().meals:
            at = now.replace(hour=hour, minute=0, second=0, microsecond=0)
            if at > now:
                at -= timedelta(days=1)
            if best is None or at > best:
                best = at
        return self._tick_at(best) if best is not None else 0

    def _automatic_awake_h(self) -> float:
        """The hours of waking an unseated person owes: since the night ended (the start
        of the morning watch), none at night, none before the scenario began."""
        clock = self.world.clock
        now = clock.ship_time
        if now.hour < NIGHT_ENDS_HOUR or now.hour >= 20:
            return 0.0
        woke = now.replace(hour=NIGHT_ENDS_HOUR, minute=0, second=0, microsecond=0)
        return max(0, clock.tick - self._tick_at(woke)) / 3600.0

    def take_in_hand(self, person: Any) -> Needs:
        """A person come to be stationed: his needs from what the routine made of them,
        his own from now on."""
        n = needs_of(person)
        if n.by_hand:
            return n
        meal = self._last_meal_tick()
        n.ate = n.drank = meal
        n.awake_h = self._automatic_awake_h()
        n.at = self.world.clock.tick
        n.asleep = ""
        n.told = {}
        n.turned_in_from = ""
        n.by_hand = True
        return n

    def let_go(self, person: Any) -> None:
        """Nobody holds him now: the routine has him again."""
        n = needs_of(person)
        n.by_hand = False
        n.asleep = ""
        n.told = {}

    # -- the reckoning of one person -----------------------------------------------------

    def _settle(self, n: Needs) -> None:
        """His fatigue brought up to now: an hour awake owes an hour; asleep, the table's
        rate is made up."""
        now = self.world.clock.tick
        dt = max(0, now - n.at) / 3600.0
        n.at = now
        if not dt:
            return
        t = self.table
        if n.asleep == "below":
            n.awake_h = max(0.0, n.awake_h - t.sleep_below_per_hour * dt)
        elif n.asleep:
            n.awake_h = max(0.0, n.awake_h - t.sleep_where_per_hour * dt)
        else:
            n.awake_h += dt

    def _hand(self, person: Any) -> Any:
        """The sailor of the muster this person is, when he is one of the hands (not of
        the quarterdeck): his fatigue is the crew's."""
        sid = getattr(person, "sailor_id", None)
        crew = (getattr(self.world.ship, "extra", None) or {}).get("crew")
        if not sid or crew is None:
            return None
        sailor = crew.by_id.get(sid)
        if sailor is None:
            return None
        from freesail.crew.model import Station

        return None if sailor.station is Station.QUARTERDECK else sailor

    def hours(self, person: Any) -> dict[str, float]:
        """The hours of each need as they stand, by hand or by the routine."""
        n = needs_of(person)
        now = self.world.clock.tick
        if not n.by_hand:
            meal = self._last_meal_tick()
            return {
                HUNGER: (now - meal) / 3600.0,
                THIRST: (now - meal) / 3600.0,
                FATIGUE: self._automatic_awake_h(),
            }
        self._settle(n)
        return {
            HUNGER: (now - n.ate) / 3600.0,
            THIRST: (now - n.drank) / 3600.0,
            FATIGUE: n.awake_h,
        }

    def steps(self, person: Any) -> dict[str, int]:
        t = self.table
        h = self.hours(person)
        out = {need: t.step(need, h[need]) for need in NEED_ORDER}
        sailor = self._hand(person)
        if sailor is not None:
            # a hand's fatigue is the crew's, read at the file's bounds (the watch bill
            # rests him: never the last step's sleep where he is)
            out[FATIGUE] = sum(1 for b in t.hand_bounds if sailor.fatigue >= b)
        return out

    def words(self, person: Any) -> str:
        """How he is, in words, every need named that is past its first hours: 'quite
        thirsty, hungry and feeling a bit drowsy'; '' when nothing is."""
        t = self.table
        st = self.steps(person)
        said = [t.steps[need][st[need] - 1].words for need in NEED_ORDER if st[need] > 0]
        return _and(said)

    def showing(self, person: Any) -> str:
        """What a station's sample carries as its `needs` (package 54): the needs at a step
        that is said (the second and on), in words; '' when none is."""
        n = needs_of(person)
        if not n.by_hand:
            return ""
        t = self.table
        st = self.steps(person)
        said = [
            t.steps[need][st[need] - 1].words
            for need in NEED_ORDER
            if st[need] > 0 and t.steps[need][st[need] - 1].severity != SILENT
        ]
        if n.asleep:
            said.append("asleep below" if n.asleep == "below" else "asleep where you stood")
        return _and(said)

    # -- the minute's tick ---------------------------------------------------------------

    def tick(self) -> None:
        world = self.world
        people = getattr(world, "people", None)
        if people is None:
            return
        watch = world.clock.watch()
        changed = self._watch is not None and watch != self._watch
        self._watch = watch
        stationed = self.stationed()
        ids = {id(p) for p, _ in stationed}
        for p in list(getattr(people, "people", None) or []):
            n = getattr(p, "needs", None)
            if n is not None and n.by_hand and id(p) not in ids:
                self.let_go(p)
        for p, holder in stationed:
            self.take_in_hand(p)
            self._look(p, holder, changed)

    def _look(self, p: Any, holder: Any, watch_changed: bool) -> None:
        n = needs_of(p)
        t = self.table
        self._settle(n)
        if n.asleep and n.awake_h <= 0.0:
            self.wake(p, holder, "rested")
            if holder is not None and hasattr(holder, "wake_rested"):
                holder.wake_rested()
        st = self.steps(p)
        last = len(t.steps[FATIGUE])
        if (
            not n.asleep
            and st[FATIGUE] >= last
            and t.steps[FATIGUE][last - 1].asleep
            and self._hand(p) is None
        ):
            self._fall_asleep(p, holder)
            st = self.steps(p)
        for need in NEED_ORDER:
            if st[need] < n.told.get(need, 0):
                n.told[need] = st[need]
        if n.asleep:
            return  # a sleeping man is told nothing; what rose is told when he wakes
        risen = [
            need
            for need in NEED_ORDER
            if st[need] > n.told.get(need, 0)
            and t.steps[need][st[need] - 1].severity != SILENT
            and not t.steps[need][st[need] - 1].asleep
        ]
        if not risen:
            return
        urgent = any(t.steps[need][st[need] - 1].severity == URGENT for need in risen)
        if not (urgent or watch_changed):
            return  # a notable line waits for the change of the watch
        for need in risen:
            n.told[need] = st[need]
        said = _and([t.steps[need][st[need] - 1].words for need in risen])
        text = f"You are {said}."
        self._tell(p, holder, text, Severity.URGENT if urgent else Severity.NOTABLE, risen)

    def _fall_asleep(self, p: Any, holder: Any) -> None:
        if holder is not None and hasattr(holder, "fall_asleep"):
            if not holder.fall_asleep():
                return  # the model has the floor: at the next minute's look
        n = needs_of(p)
        n.asleep = "where he is"
        n.turned_in_from = ""
        n.told[FATIGUE] = len(self.table.steps[FATIGUE])
        where = place_words(_place(self.world, p))
        if holder is None or getattr(holder, "model_name", "") == "the player":
            text = f"You have fallen asleep where you stood, {where}. Your next order wakes you."
        else:
            text = (
                f"You have fallen asleep where you stood, {where}. You sleep until you are "
                "called; an urgent line wakes you, and you wake when you are rested."
            )
        self._tell(p, holder, text, Severity.URGENT, [FATIGUE])

    # -- telling -------------------------------------------------------------------------

    def _tell(self, p: Any, holder: Any, text: str, severity: Severity, needs: list[str]) -> None:
        """A line to the person stationed and to nobody else: a notice in a model's next
        sample, or the player's line through the listeners. Never the log."""
        player = holder is None or getattr(holder, "model_name", "") == "the player"
        if not player:
            words = text + _remedy(needs, model=True)
            agent = getattr(holder, "agent", None)
            if agent is not None:
                agent.notices.append(words)
                if severity is Severity.URGENT and hasattr(holder, "need_urgent"):
                    holder.need_urgent(text)
            return
        world = self.world
        e = Event(
            tick=world.clock.tick,
            ship_time=world.clock.ship_time,
            severity=severity,
            kind=FELT_KIND,
            text=text + _remedy(needs, model=False),
            actor="",
            data={"person": p.name, "needs": list(needs)},
        )
        for fn in list(self.listeners):
            fn(e)

    # -- the person's own acts -----------------------------------------------------------

    def person_of(self, actor: str) -> tuple[Any, Any]:
        """The stationed person whose order this is, with what holds him; refused in
        words for an order no person gives (a standing order, the owner while a model
        holds the captain's station)."""
        from freesail.core.events import STATION_ACTORS
        from freesail.orders.errors import OrderError

        station = str(actor or "").split(" (", 1)[0]
        stationed = self.stationed(prompt=True)
        if station == "captain":
            for p, h in stationed:
                if h is None:
                    return p, None
            raise OrderError(
                "At the prompt you are the owner, not the captain, while a model holds the "
                "captain's station or you are seated at another: eating, drinking and "
                "sleeping are a person's own, at his station."
            )
        if station in STATION_ACTORS:
            name = station.removeprefix("the ")
            for p, h in stationed:
                if h is not None and h.station.name == name:
                    return p, h
            raise OrderError(f"The {name}'s station holds no person to eat, drink or sleep.")
        raise OrderError(
            "Eating, drinking and sleeping are a person's own, given at his station; a "
            "standing order or a rule does not do them for him."
        )

    def _ready(self, p: Any, holder: Any) -> Needs:
        """His needs his own and settled, and awake: an order of his own wakes him."""
        n = self.take_in_hand(p)
        self._settle(n)
        if n.asleep:
            self.wake(p, holder, "")
        return n

    def eat(self, p: Any, holder: Any) -> str:
        from freesail.orders.errors import OrderError

        world = self.world
        n = self._ready(p, holder)
        where = _place(world, p)
        stores = getattr(world, "stores", None)
        aboard = getattr(p, "aboard", True) and PLACES.get(where, PLACES["deck"]).aboard
        if aboard and _victualled(world) and stores is not None and stores.provisions_days <= 0:
            raise OrderError(
                "The provisions are all expended: there is nothing in the bread room to eat."
            )
        now = world.clock.tick
        since = _since_words(world, n.ate)
        short = aboard and stores is not None and getattr(stores, "allowance", 1.0) < 1.0
        n.ate = now - int(self.table.short_allowance_hours_left * 3600) if short else now
        n.told[HUNGER] = 0
        if aboard and where in self.table.places_with_food and _galley_out(stores):
            # practice and resupply (between packages 72 and 73): the galley fire out while
            # the powder comes aboard (the Regulations of 1806, the Gunner, Art. V), and the
            # meal cold; eaten all the same
            text = (
                "A cold meal, biscuit and cheese, the galley fire being out while the powder "
                f"comes aboard; you eat {place_words(where)}"
            )
        elif where in self.table.places_with_food or not aboard:
            text = f"You eat {place_words(where)}"
        else:
            text = (
                "A biscuit and a piece of cheese are brought up from the stores; you eat "
                f"{place_words(where)}"
            )
        text += f", the first since {since}." if since else "."
        if short:
            text += " It is a half meal: the ship is at short allowance."
        return text

    def drink(self, p: Any, holder: Any, foul_water: bool = False) -> str:
        from freesail.orders.errors import OrderError

        world = self.world
        n = self._ready(p, holder)
        where = _place(world, p)
        stores = getattr(world, "stores", None)
        aboard = getattr(p, "aboard", True) and PLACES.get(where, PLACES["deck"]).aboard
        victualled = aboard and _victualled(world) and stores is not None
        since = _since_words(world, n.drank)
        tail = f", the first since {since}." if since else "."
        foul = victualled and bool(getattr(stores, "foul", False))
        water = not victualled or stores.water_tons > 0
        beer = not victualled or stores.provisions_days > 0
        now = world.clock.tick
        if foul_water:
            if not foul:
                raise OrderError("The water is sweet; say 'drink'.")
            self._settle(n)
            n.drank = now
            n.told[THIRST] = 0
            n.awake_h += self.table.foul_water_hours
            return f"You drink the foul water {place_words(where)}; it gripes you{tail}"
        if victualled and foul and beer:
            n.drank = now
            n.told[THIRST] = 0
            return f"The water being foul, you drink your beer {place_words(where)}{tail}"
        if victualled and foul:
            raise OrderError(
                "The water is foul in the cask and the beer is all expended: say 'drink the "
                "foul water' to drink it all the same (it gripes), or go without."
            )
        if not water and not beer:
            raise OrderError("The water and the beer are all expended: there is nothing to drink.")
        n.drank = now
        n.told[THIRST] = 0
        if not water:
            return f"The water being expended, you drink your beer {place_words(where)}{tail}"
        if where in ("deck", "quarterdeck") and aboard:
            return f"You drink at the scuttle-butt{tail}"
        return f"You drink {place_words(where)}{tail}"

    def turn_in(self, p: Any, holder: Any) -> str:
        """`sleep` by the player (at the prompt or his seat): below to his berth, asleep
        until his next order, an urgent line, or he is rested."""
        from freesail.orders.errors import OrderError

        n = self.take_in_hand(p)
        self._settle(n)
        if n.asleep == "below":
            raise OrderError("You are asleep below already.")
        rested = self.too_rested(p)
        if rested:
            raise OrderError(rested)
        agent = getattr(holder, "agent", None)
        if agent is not None and agent.has_deck and holder.station.name != "captain":
            raise OrderError(
                "You have the deck: a man does not turn in on watch. Give it back to the "
                "captain first."
            )
        where = _place(self.world, p)
        aboard = getattr(p, "aboard", True) and PLACES.get(where, PLACES["deck"]).aboard
        n.turned_in_from = "" if n.asleep else where
        n.asleep = "below"
        if aboard and not PLACES.get(where, PLACES["deck"]).below:
            p.where = self._berth(p)
        return (
            f"You turn in below, {place_words(_place(self.world, p))}. Your next order wakes "
            "you, and so does an urgent line; you wake of yourself when you are rested."
        )

    def too_rested(self, p: Any) -> str:
        """Why he would not sleep yet, or '': he has slept his fill within the hour
        (`RESTED_UNDER_H`), and would wake at once."""
        n = self.take_in_hand(p)
        self._settle(n)
        if self._hand(p) is None and n.awake_h < RESTED_UNDER_H:
            return (
                "You are rested: you have slept your fill within the hour; sleep when you "
                "are tired."
            )
        return ""

    def sleep_below(self, p: Any) -> None:
        """A model's `stand by, asleep below until called` (the harness): below to his
        berth, asleep."""
        n = self.take_in_hand(p)
        self._settle(n)
        where = _place(self.world, p)
        aboard = getattr(p, "aboard", True) and PLACES.get(where, PLACES["deck"]).aboard
        n.turned_in_from = "" if n.asleep else where
        n.asleep = "below"
        if aboard and not PLACES.get(where, PLACES["deck"]).below:
            p.where = self._berth(p)

    def _berth(self, p: Any) -> str:
        """Where he turns in: the cabin for the man who commands (the master of a
        schooner or a cutter too), else his role's berth."""
        people = getattr(self.world, "people", None)
        if people is not None and _captain(people) is p:
            return "cabin"
        return self.table.berth(p.role)

    def wake(self, p: Any, holder: Any, why: str) -> str:
        """He wakes: called, by his own order, or rested. Called back from his berth, he
        goes back where he turned in from. Returns the words, told to the player."""
        n = needs_of(p)
        if not n.asleep:
            return ""
        self._settle(n)
        n.asleep = ""
        back = n.turned_in_from
        n.turned_in_from = ""
        if back and back != _place(self.world, p):
            p.where = back
        rested = "rested, " if why == "rested" or n.awake_h <= 0.0 else ""
        text = f"You wake, {rested}{place_words(_place(self.world, p))}."
        player = holder is None or getattr(holder, "model_name", "") == "the player"
        if player:
            self._tell(p, holder, text, Severity.NOTABLE, [])
        else:
            agent = getattr(holder, "agent", None)
            if agent is not None:
                agent.notices.append(text)
        return text

    def heard_order(self, actor: str) -> None:
        """An order given at the prompt or the player's seat: the player who gives it is
        awake (`World.submit`). Cheap when nobody sleeps by his needs."""
        station = str(actor or "").split(" (", 1)[0]
        if station != "captain" and not str(actor or "").endswith("(the player)"):
            return
        people = getattr(self.world, "people", None)
        if people is None or not getattr(people, "_built", False):
            return
        if not any(
            p.needs is not None and p.needs.by_hand and p.needs.asleep for p in people.people
        ):
            return
        try:
            p, holder = self.person_of(actor)
        except Exception:  # noqa: BLE001  (an order no person of the player's gives)
            return
        n = getattr(p, "needs", None)
        if n is not None and n.by_hand and n.asleep:
            self.wake(p, holder, "")

    def how(self, p: Any, holder: Any) -> str:
        """`how am I`: his needs in words and when he last ate, drank and slept."""
        n = self.take_in_hand(p)
        self._settle(n)
        world = self.world
        words = self.words(p)
        head = f"You are {words}." if words else "You are fed, watered and rested."
        ate = _since_words(world, n.ate)
        drank = _since_words(world, n.drank)
        tail = f" You last ate at {ate} and drank at {drank}"
        if self._hand(p) is None:
            tail += f"; you have been awake some {round(n.awake_h):.0f} hours"
        tail += "."
        if n.asleep:
            tail += " You are asleep."
        line = self.line(p, holder)
        return f"{line}\n{head}{tail}" if line else f"{head}{tail}"

    def line(self, p: Any, holder: Any) -> str:
        """The station's line for `how am I` (package 66): the same line a station's sample
        opens with, for the station that holds him or the captain at the prompt."""
        from freesail.api.readings import station_line

        station = getattr(getattr(holder, "station", None), "name", None)
        held = getattr(holder, "_place_since", None)
        since = held[1] if held else None
        if since is None:
            # the captain at the prompt: the last line that moved him, or the start
            from freesail.agents.harness import PLACE_KINDS

            name = str(getattr(p, "name", "") or "")
            log = self.world.log
            since = next(
                (
                    int(log[i].tick)
                    for i in range(len(log) - 1, -1, -1)
                    if log[i].kind in PLACE_KINDS and name and name in log[i].text
                ),
                0,
            )
        try:
            return station_line(self.world, station, p, since)
        except Exception:  # noqa: BLE001  (never an answer lost to the line)
            return ""


def _captain(people: Any) -> Any:
    try:
        return people.captain
    except Exception:  # noqa: BLE001  (a world with no muster)
        return None


def _victualled(world: Any) -> bool:
    from freesail.crew.victuals import victualled

    return victualled(world)


def _galley_out(stores: Any) -> bool:
    """Whether the galley fire is out for the powder (`Stores.galley_fire_out`; practice and
    resupply, between packages 72 and 73)."""
    return bool(getattr(stores, "galley_fire_out", "")) if stores is not None else False


def _place(world: Any, p: Any) -> str:
    people = getattr(world, "people", None)
    try:
        return people.effective_place(p) if people is not None else p.where
    except Exception:  # noqa: BLE001
        return getattr(p, "where", "quarterdeck")


def _since_words(world: Any, tick: int) -> str:
    """'08:00', '16:00 on 11 June': when a tick was, for 'the first since ...'."""
    clock = world.clock
    then = clock.start + timedelta(seconds=tick)
    stamp = then.strftime("%H:%M")
    if then.date() != clock.ship_time.date():
        stamp += f" on {then.day} {then:%B}"
    return stamp


def _and(items: list[str]) -> str:
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + " and " + items[-1]


# What a line says the person may do, by the needs it names: the player's orders, and a
# model's (its own orders through submit_order and the stand-by of its own).
_PLAYER_REMEDY = {THIRST: "'drink'", HUNGER: "'eat'", FATIGUE: "'sleep'"}
_MODEL_REMEDY = {
    THIRST: "submit_order('drink')",
    HUNGER: "submit_order('eat')",
    FATIGUE: "stand_by('asleep below until called')",
}


def _remedy(needs: list[str], model: bool) -> str:
    table = _MODEL_REMEDY if model else _PLAYER_REMEDY
    said = [table[n] for n in NEED_ORDER if n in needs]
    if not said:
        return ""
    return f" ({_and(said)})"
