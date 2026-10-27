"""The wounded, the sick and the dead, the surgeon and the needs' ends (spec M7 §16, §16a,
§17; package 73; the design in `docs/design/Design-WaterAndHealth.md`).

**The muster's states** are `Sailor.hurt`, one word: `""` fresh, `"hurt"` (a light wound
dressed, fit for light duty on deck and never aloft), `"wounded"` (below, the surgeon's,
`Sailor.wound` light or grave), `"sick"` (the sick list) and `"killed"`; `hurt_until` the
tick he is healed or judged, `dressed` whether the surgeon has seen him, `hurt_how` the
wound in words. A man killed stays on the books until he is buried (the morale's losses
and every index count him), then is struck from them into `Crew.dead` with a line of the
log.

**The surgeon** is the post the file has (the frigate's and the brig's; a cutter, a lugger,
a schooner and a merchant brig bore none, and their wounded are dressed by their messmates
in an hour and fare as the untreated), his mates the idlers of that trade. His work is a
queue of the wounded in the order they came (the period's rule, first come first served:
Turnbull 1806; `WORST_FIRST` the knob the owner may turn), each man his minutes of one
pair of hands (a mate dresses a light wound, the surgeon alone the grave), so that a
broadside's dozen wounded keep him two hours. A light wound dressed is `hurt`, back on the
bill in seven to fourteen days; a grave wound dressed is judged at a day, the man dying
with `DIE_GRAVE_TREATED` (the period's third: James's returns, Turnbull) or
`DIE_GRAVE_UNTREATED` else, or invalided for the voyage (`HEAL_GRAVE_D`). The draws are a
health stream opened at the first wounded man and never before (the strain's determinism
test pins the sailing's streams).

**The sick list** by the ship's condition, drawn once a day at the morning watch's eight
bells for every fit man: the water foul (the flux: Trotter's *Medicina Nautica* on the
Channel fleet's sick lists; the rate judgement), short allowance beyond a week, the water
expended (thirst's own course below); nothing else, so that a healthy ship at whole
allowance draws nothing and no recorded passage moves (the base sickness of a company,
the fever and the scurvy are M8's; the cold and the wet wait on §26's temperature).

**The needs' ends** (M7b §20 left them here): a stationed person's thirst at
`THIRST_COLLAPSE_H` puts him down and at `THIRST_DEATH_H` kills him, hunger at a week and
three weeks; for the company the water expended counts the days: from the second a tenth
of the fit men a day go on the sick list with thirst, from the fourth one in twenty of the
company a day dies of it, the log explaining it from the stores' lines before and the sick
list's.

**The lines**: the butcher's bill once after an action, the morning report (routine, only
when the list is not empty), a man taken ill, a death in the sick berth, the burial. Every
figure is judgement with its source named, tuned in play (rule 6).
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any

from freesail.core.events import Severity
from freesail.crew.model import Crew, Sailor, Station, number_words

__all__ = [
    "DIE_GRAVE_TREATED",
    "DIE_GRAVE_UNTREATED",
    "HEALTH_STREAM",
    "HUNGER_COLLAPSE_H",
    "HUNGER_DEATH_H",
    "THIRST_COLLAPSE_H",
    "THIRST_DEATH_H",
    "Health",
    "HealthState",
    "bury_the_dead",
    "health_of",
    "hurt_words",
    "sick_list",
]

HEALTH_STREAM = "health"

# -- the surgeon's work ---------------------------------------------------------------------
DRESS_LIGHT_S = 600  # a light wound dressed: ten minutes of a mate's hands (judgement)
DRESS_GRAVE_S = 1800  # a grave wound: the amputation and the ligatures, half an hour (judgement)
MESSMATES_DRESS_S = 3600  # no surgeon borne: a light wound dressed by his messmates in an hour
WORST_FIRST = False  # the period's rule was first come first served (Turnbull 1806); the knob
# The light wound heals in seven to fourteen days (Turnbull 1806 on contusions and splinter
# wounds; judgement), half as long again without a surgeon; the grave is judged at a day,
# dies with these chances (the period's mortality of the badly wounded about a third:
# James's returns; the untreated worse), else is invalided for the voyage.
HEAL_LIGHT_D = (7.0, 14.0)
UNTREATED_HEAL_FACTOR = 1.5
JUDGE_GRAVE_S = 24 * 3600
DIE_GRAVE_TREATED = 0.3
DIE_GRAVE_UNTREATED = 0.6
HEAL_GRAVE_D = 40.0
# A station holder with a grave wound undressed collapses after this long (judgement).
COLLAPSE_S = 1800

# -- the sick list ----------------------------------------------------------------------------
SICK_FOUL_WATER = 0.02  # a man a day of the flux with the water foul (Trotter; judgement)
SICK_SHORT_ALLOWANCE = 0.01  # beyond a week of it (judgement)
SHORT_ALLOWANCE_DAYS = 7.0
SICK_DAYS = (3.0, 7.0)  # the flux's course (judgement)
DIE_FLUX_AFTER_D = 5.0  # a tenth of the sick of the flux die after this long without a port's water
DIE_FLUX = 0.1
MORNING_REPORT_HOUR = 8

# -- the needs' ends ----------------------------------------------------------------------------
THIRST_COLLAPSE_H = 72.0  # three days without water puts a man down (the medical commonplaces)
THIRST_DEATH_H = 96.0  # four days kills him (judgement at the long end: the table's steps are soft)
HUNGER_COLLAPSE_H = 7 * 24.0
HUNGER_DEATH_H = 21 * 24.0
# The company with the water expended (the beer too): the days counted from the last cask
WATER_OUT_SICK_FROM_D = 2.0
WATER_OUT_SICK_SHARE = 0.1  # of the fit men a day
WATER_OUT_DEATH_FROM_D = 4.0
WATER_OUT_DEATH_SHARE = 0.05  # of the company a day
PROVISIONS_OUT_LAG_D = 14.0  # the hunger of a company takes the same road a fortnight later

# -- the butcher's bill -----------------------------------------------------------------------
BILL_AFTER_S = 600  # the bill said when ten minutes have passed with no shot fired or struck

# The wounds in words (judgement; the surgeons' journals' commonplaces), by the gravity.
LIGHT_WOUNDS = (
    "a splinter wound in the arm",
    "a cut on the head",
    "bruised by a block",
    "a splinter in the hand",
    "burnt by a cartridge",
    "a cut across the face",
)
GRAVE_WOUNDS = (
    "a splinter in the thigh",
    "a musket ball in the shoulder",
    "his leg shattered",
    "his arm taken off at the elbow",
    "a splinter in the breast",
    "a ball through the body",
)


def _since(s: Sailor, tick: int) -> int:
    """The tick the man was hurt (a hit at the world's first tick is a hit, not 'now')."""
    return int(s.hurt_tick) if s.hurt_tick is not None else tick


def hurt_words(s: Sailor) -> str:
    """'killed', 'wounded (a splinter in the thigh, dangerously)', 'hurt (a cut on the
    head), at light duty', 'sick (the flux)'; '' for a fit man."""
    how = getattr(s, "hurt_how", "") or ""
    if s.hurt == "killed":
        return "killed" + (f" ({how})" if how else "")
    if s.hurt == "wounded":
        grave = getattr(s, "wound", "") == "grave"
        tail = (
            f" ({how}{', dangerously' if grave else ''})"
            if how
            else (", dangerously" if grave else "")
        )
        return "wounded" + tail
    if s.hurt == "hurt":
        return "hurt" + (f" ({how})" if how else "") + ", at light duty"
    if s.hurt == "sick":
        return "sick" + (f" ({how})" if how else "")
    return ""


@dataclass
class HealthState:
    """The surgeon's work and the company's health, kept in `ship.extra["health"]`."""

    # the surgeon's and his mates' hands at work: worker id -> (patient id, done tick)
    at_work: dict[str, tuple[str, int]] = field(default_factory=dict)
    # the days of the water expended, from the tick the last cask ran out
    water_out_since: int | None = None
    provisions_out_since: int | None = None
    last_daily_day: str | None = None
    bill_said_tick: int | None = None  # the last butcher's bill said, by the action's hits
    bill_hits: int = 0
    stream_opened: bool = False
    persons_told: dict[str, str] = field(default_factory=dict)


def health_of(ship: Any) -> HealthState | None:
    extra = getattr(ship, "extra", None)
    if extra is None:
        return None
    st = extra.get("health")
    if not isinstance(st, HealthState):
        st = HealthState()
        extra["health"] = st
    return st


def sick_list(crew: Crew) -> list[Sailor]:
    """The men off the bill: the wounded, the sick, and the killed not yet buried."""
    return [s for s in crew.sailors if s.hurt and s.hurt != "hurt"]


class Health:
    """The World's health keeper, ticked once a minute (`World._tick_needs`)."""

    def __init__(self, world: Any) -> None:
        self.world = world

    @property
    def ship(self) -> Any:
        return self.world.ship

    @property
    def crew(self) -> Crew | None:
        crew = (getattr(self.ship, "extra", None) or {}).get("crew")
        return crew if isinstance(crew, Crew) else None

    @property
    def state(self) -> HealthState | None:
        return health_of(self.ship)

    def stream(self) -> random.Random:
        st = self.state
        if st is not None:
            st.stream_opened = True
        return self.world.rng.stream(HEALTH_STREAM)

    # -- the surgeon and his mates ---------------------------------------------------------

    def surgeon(self) -> Sailor | None:
        crew = self.crew
        if crew is None:
            return None
        s = crew.posts.get("surgeon")
        return s if s is not None and s.fit else None

    def mates(self) -> list[Sailor]:
        crew = self.crew
        if crew is None:
            return []
        return [s for s in crew.sailors if s.trade == "surgeon's mate" and s.fit]

    def has_surgeon(self) -> bool:
        return self.surgeon() is not None

    def waiting(self) -> list[Sailor]:
        """The wounded not yet dressed, in the order they came (or the worst first)."""
        crew = self.crew
        if crew is None:
            return []
        st = self.state
        busy = {pid for pid, _ in st.at_work.values()} if st is not None else set()
        on_deck = self._holders_on_deck()
        out = [
            s
            for s in crew.sailors
            if s.hurt == "wounded"
            and not getattr(s, "dressed", False)
            and s.id not in busy
            and s.id not in on_deck
        ]
        out.sort(
            key=lambda s: (
                (0 if getattr(s, "wound", "") == "grave" else 1) if WORST_FIRST else 0,
                s.hurt_tick or 0,
                s.id,
            )
        )
        return out

    def _holders_on_deck(self) -> set[str]:
        """The sailor ids of the stationed persons keeping the deck (spec M7 §16a): not in
        the surgeon's queue until they go below to him."""
        keeper = getattr(self.world, "needs", None)
        if keeper is None:
            return set()
        try:
            stationed = keeper.stationed()
        except Exception:  # noqa: BLE001
            return set()
        return {
            str(getattr(p, "sailor_id", "") or "")
            for p, _ in stationed
            if getattr(p, "where", "") != "cockpit" and getattr(p, "sailor_id", None)
        }

    # -- the hit ---------------------------------------------------------------------------

    def person_of_sailor(self, sailor: Sailor) -> Any:
        people = getattr(self.world, "people", None)
        if people is None or not getattr(people, "_built", False):
            return None
        for p in people.people:
            if p.sailor_id == sailor.id:
                return p
        return None

    def hit(self, sailor: Sailor, killed: bool, rng: Any, tick: int, how: str = "") -> None:
        """A man struck (the hit model's, the musketry's, the fight's): killed, or wounded
        light or grave half and half, the wound in words; a person's station told."""
        sailor.fit = False
        sailor.hurt_tick = tick
        sailor.dressed = False
        sailor.at = None
        if killed:
            sailor.hurt = "killed"
            sailor.wound = ""
            sailor.hurt_how = how
        else:
            grave = rng.random() < 0.5
            sailor.hurt = "wounded"
            sailor.wound = "grave" if grave else "light"
            table = GRAVE_WOUNDS if grave else LIGHT_WOUNDS
            sailor.hurt_how = how or table[int(rng.random() * len(table)) % len(table)]
            sailor.hurt_until = None
        person = self.person_of_sailor(sailor)
        if person is not None:
            self._person_hit(person, sailor, tick)

    def _person_hit(self, person: Any, sailor: Sailor, tick: int) -> None:
        """A named person hit (spec M7 §16a): his person's state, and the station holding
        him told in an urgent line of his own with his roads, at parity."""
        world = self.world
        if sailor.hurt == "killed":
            person.sick = False
            self._station_killed(person, sailor)
            return
        person.sick = False  # wounded, not sick: he keeps the deck until he goes below
        keeper = getattr(world, "needs", None)
        if keeper is None:
            return
        stationed, holder = keeper.holder_of(person)
        if not stationed:
            return
        grave = sailor.wound == "grave"
        if grave:
            text = (
                f"You are hit: {sailor.hurt_how}. You can keep the deck for a while (your "
                "orders go and your words carry; you will collapse within the half hour "
                "if the wound is not dressed), or give the deck and go below to the surgeon "
                "('go below to the surgeon')."
            )
        else:
            text = (
                f"You are hit: {sailor.hurt_how}. You can keep the deck (your orders go and "
                "your words carry, and you tire the faster), or go below to the surgeon to "
                "have it dressed ('go below to the surgeon') and come on deck again."
            )
        if not self.has_surgeon():
            text += " The ship bears no surgeon: your messmates dress it where you are."
        keeper._tell(person, holder, text, Severity.URGENT, [])
        st = self.state
        if st is not None:
            st.persons_told[person.id] = "hit"

    def _station_killed(self, person: Any, sailor: Sailor) -> None:
        """A holder killed ends his station as a death does (spec M7 §16a): the model told
        in words, the journal written, the station stood down with the reason; the
        player's seat released the same way; the deck passes by the bill."""
        world = self.world
        how = sailor.hurt_how or "a shot"
        keeper = getattr(world, "needs", None)
        stationed, holder = keeper.holder_of(person) if keeper is not None else (False, None)
        was_captain = self._is_captain(person)
        person.dead = True  # after the lookups: a dead man holds no station and no command
        # "is dead of thirst" for the needs' ends, "is killed: a splinter" for a shot
        said = f"is dead {how}" if how.startswith("of ") else f"is killed: {how}"
        world.record(
            Severity.URGENT,
            "person.killed",
            f"{person.name} {said}.",
            data={"person": person.name, "sailor": sailor.id, "how": how},
        )
        if stationed and holder is not None and hasattr(holder, "stand_down"):
            agent = getattr(holder, "agent", None)
            if agent is not None:
                agent.notices.append(
                    f"You are {'dead ' + how if how.startswith('of ') else 'killed: ' + how}. "
                    "Your person is dead and the station ends with him; the deck passes by "
                    "the bill."
                )
            try:
                holder.stand_down(f"killed: {how}", by="the world")
            except Exception:  # noqa: BLE001  (a station already released)
                pass
        elif stationed and holder is None and keeper is not None:
            keeper._tell(
                person,
                None,
                f"You are {'dead ' + how if how.startswith('of ') else 'killed: ' + how}. "
                "Your person is dead; the deck passes by the bill, and the scenario goes on "
                "under whoever commands.",
                Severity.URGENT,
                [],
            )
        if was_captain:
            self._command_passes(person)

    def _station_invalided(self, person: Any, sailor: Sailor) -> None:
        """A holder invalided (spec M7 §16a): lost to the ship for the voyage, his station
        stood down by the world with the reason; the command passes if it was his."""
        world = self.world
        keeper = getattr(world, "needs", None)
        stationed, holder = keeper.holder_of(person) if keeper is not None else (False, None)
        was_captain = self._is_captain(person)
        person.sick = True
        text = (
            f"The surgeon has judged your wound ({sailor.hurt_how}): you will live, but you "
            "are lost to the ship for the voyage. The station ends with it; the deck "
            "passes by the bill."
        )
        if stationed and holder is not None and hasattr(holder, "stand_down"):
            agent = getattr(holder, "agent", None)
            if agent is not None:
                agent.notices.append(text)
            try:
                holder.stand_down(f"invalided: {sailor.hurt_how}", by="the world")
            except Exception:  # noqa: BLE001
                pass
        elif stationed and keeper is not None:
            keeper._tell(person, None, text, Severity.URGENT, [])
        if was_captain:
            self._command_passes(person)

    def _is_captain(self, person: Any) -> bool:
        people = getattr(self.world, "people", None)
        if people is None:
            return False
        try:
            return people.captain is person
        except Exception:  # noqa: BLE001
            return False

    def _command_passes(self, person: Any) -> None:
        """The command passes by the bill when the man in command is killed: the next in
        the wardroom's order takes it, said in the log; the rules captain's doctrine
        commands as it did."""
        world = self.world
        people = getattr(world, "people", None)
        if people is None:
            return
        order = (
            "first lieutenant",
            "lieutenant",
            "second lieutenant",
            "mate",
            "master",
            "boatswain",
        )
        for role in order:
            nxt = next(
                (
                    p
                    for p in people.people
                    if p.role == role and not getattr(p, "dead", False) and p.aboard
                ),
                None,
            )
            if nxt is not None:
                people.command_passed_to = nxt.id
                world.record(
                    Severity.URGENT,
                    "ship.command_passes",
                    f"{nxt.name}, {nxt.role}, takes the command.",
                    data={"person": nxt.name, "role": nxt.role},
                )
                return

    # -- the tick ---------------------------------------------------------------------------

    def tick(self) -> None:
        world = self.world
        crew = self.crew
        st = self.state
        if crew is None or st is None:
            return
        tick = int(world.clock.tick)
        self._work_the_wounded(tick)
        self._courses(tick)
        self._holders(tick)
        self._bill(tick)
        when = world.clock.ship_time
        day = when.strftime("%Y-%m-%d")
        if when.hour == MORNING_REPORT_HOUR and when.minute == 0 and st.last_daily_day != day:
            st.last_daily_day = day
            self._daily(tick, when)
        self._needs_ends(tick)

    # -- the surgeon's queue -----------------------------------------------------------------

    def _work_the_wounded(self, tick: int) -> None:
        crew = self.crew
        st = self.state
        assert crew is not None and st is not None
        # the men done with
        for wid, (pid, done) in list(st.at_work.items()):
            if tick >= done:
                del st.at_work[wid]
                patient = crew.by_id.get(pid)
                if patient is not None and patient.hurt == "wounded" and not patient.dressed:
                    self._dressed(patient, tick, by_surgeon=True)
        surgeon = self.surgeon()
        workers: list[Sailor] = ([surgeon] if surgeon is not None else []) + self.mates()
        free = [w for w in workers if w.id not in st.at_work and w.hurt == ""]
        if free:
            for patient in self.waiting():
                if not free:
                    break
                grave = patient.wound == "grave"
                pick = None
                if grave:
                    pick = next((w for w in free if w is surgeon), None)
                else:
                    pick = next((w for w in free if w is not surgeon), None) or (
                        free[0] if free else None
                    )
                if pick is None:
                    continue
                free.remove(pick)
                st.at_work[pick.id] = (
                    patient.id,
                    tick + (DRESS_GRAVE_S if grave else DRESS_LIGHT_S),
                )
            return
        if surgeon is None and not self.mates():
            # no surgeon borne: the lightly wounded dressed by their messmates in an hour;
            # the badly wait for their day
            for patient in self.waiting():
                if patient.wound == "light" and tick - _since(patient, tick) >= MESSMATES_DRESS_S:
                    self._dressed(patient, tick, by_surgeon=False)
                elif patient.wound == "grave" and tick - _since(patient, tick) >= MESSMATES_DRESS_S:
                    patient.dressed = True
                    patient.hurt_until = tick + JUDGE_GRAVE_S
                    patient.treated = False

    def _dressed(self, patient: Sailor, tick: int, by_surgeon: bool) -> None:
        rng = self.stream()
        patient.dressed = True
        patient.treated = by_surgeon
        if patient.wound == "light":
            lo, hi = HEAL_LIGHT_D
            days = lo + rng.random() * (hi - lo)
            if not by_surgeon:
                days *= UNTREATED_HEAL_FACTOR
            patient.hurt = "hurt"
            patient.fit = True
            patient.hurt_until = tick + int(days * 86400)
            person = self.person_of_sailor(patient)
            if person is not None:
                if getattr(person, "where", "") == "cockpit":
                    text = (
                        f"Your wound is dressed ({patient.hurt_how}); you are fit for light "
                        "duty and may come on deck."
                    )
                else:
                    text = (
                        f"Your wound is dressed where you stand ({patient.hurt_how}); you "
                        "are fit for light duty."
                    )
                self._tell_person(person, text)
                self._holder_dressed(person)
        else:
            patient.hurt_until = tick + JUDGE_GRAVE_S
            person = self.person_of_sailor(patient)
            if person is not None:
                # a grave wound dressed: he stays under the surgeon's hands until judged
                self._tell_person(
                    person,
                    f"Your wound is dressed ({patient.hurt_how}), but it is a dangerous one: "
                    "you stay below under the surgeon's hands, and the deck is not yours "
                    "until he has judged it, in a day.",
                )

    def _courses(self, tick: int) -> None:
        """Each man's wound or sickness along its course: the light healed, the grave judged
        at a day, the sick recovered or dead."""
        crew = self.crew
        world = self.world
        assert crew is not None
        rng = None
        for s in crew.sailors:
            if not s.hurt or s.hurt == "killed":
                continue
            until = getattr(s, "hurt_until", None)
            if until is None or tick < until:
                continue
            if s.hurt == "hurt":
                s.hurt = ""
                s.hurt_how = ""
                s.wound = ""
                s.hurt_until = None
                world.record(
                    Severity.ROUTINE,
                    "health.returned",
                    f"{s.name} is returned to duty, his hurt healed.",
                    data={"sailor": s.id},
                )
                continue
            rng = rng or self.stream()
            if s.hurt == "wounded" and s.wound == "grave":
                p = DIE_GRAVE_TREATED if getattr(s, "treated", False) else DIE_GRAVE_UNTREATED
                if rng.random() < p:
                    self._dies(s, tick, f"of his wound, {s.hurt_how}")
                else:
                    s.hurt_until = tick + int(HEAL_GRAVE_D * 86400)
                    s.wound = "invalid"
                    world.record(
                        Severity.ROUTINE,
                        "health.invalided",
                        f"{s.name} will live, the surgeon thinks, but is lost to the ship for "
                        "the voyage.",
                        data={"sailor": s.id},
                    )
                    person = self.person_of_sailor(s)
                    if person is not None:
                        self._station_invalided(person, s)
                continue
            if s.hurt == "wounded" and s.wound == "invalid":
                s.hurt = s.hurt_how = s.wound = ""
                s.hurt_until = None
                s.fit = True
                world.record(
                    Severity.ROUTINE,
                    "health.returned",
                    f"{s.name} is returned to duty.",
                    data={"sailor": s.id},
                )
                continue
            if s.hurt == "sick":
                # the flux kills a tenth of its sick after its days without a port's water
                stores = getattr(world, "stores", None)
                foul_still = bool(getattr(stores, "foul", False)) if stores is not None else False
                thirst = (s.hurt_how or "").startswith("thirst")
                if (foul_still or thirst) and rng.random() < DIE_FLUX:
                    self._dies(s, tick, f"of {'thirst' if thirst else 'the flux'}")
                else:
                    s.hurt = s.hurt_how = ""
                    s.hurt_until = None
                    s.fit = True
                    world.record(
                        Severity.ROUTINE,
                        "health.returned",
                        f"{s.name} is off the sick list and returned to duty.",
                        data={"sailor": s.id},
                    )

    def _dies(self, s: Sailor, tick: int, how: str) -> None:
        s.hurt = "killed"
        s.fit = False
        s.hurt_tick = tick
        s.hurt_how = how
        s.hurt_until = None
        self.world.record(
            Severity.NOTABLE,
            "health.died",
            f"{s.name} died {how}.",
            data={"sailor": s.id, "how": how},
        )
        person = self.person_of_sailor(s)
        if person is not None:
            self._station_killed(person, s)

    # -- the station holders ---------------------------------------------------------------------

    def _holders(self, tick: int) -> None:
        """A holder with a grave wound undressed collapses after his half hour (his road
        of carrying on until he collapses); a holder dressed is told."""
        world = self.world
        keeper = getattr(world, "needs", None)
        crew = self.crew
        if keeper is None or crew is None:
            return
        for person, holder in keeper.stationed():
            sid = getattr(person, "sailor_id", None)
            s = crew.by_id.get(sid) if sid else None
            if s is None or s.hurt != "wounded" or s.dressed:
                continue
            if person.where in ("cockpit",):
                continue  # below with the surgeon: in his queue
            if s.wound == "grave":
                if tick - _since(s, tick) >= COLLAPSE_S:
                    self.collapse(person, holder, s)
            elif tick - _since(s, tick) >= MESSMATES_DRESS_S:
                # a light wound kept on deck: dressed where he stands after an hour, by a
                # mate sent up if one is borne, by his messmates else
                self._dressed(s, tick, by_surgeon=self.has_surgeon() or bool(self.mates()))

    def collapse(self, person: Any, holder: Any, s: Sailor) -> None:
        """He collapses where he stands and is carried below to the surgeon: the station
        stands by as it does for a man asleep where he stood, the deck passes."""
        world = self.world
        person.where = "cockpit"
        text = (
            f"You have collapsed ({s.hurt_how}) and are carried below to the surgeon; the deck "
            "passes by the bill. You are told when your wound is dressed."
        )
        if holder is not None and hasattr(holder, "carried_below"):
            holder.carried_below(text)
        else:
            keeper = getattr(world, "needs", None)
            if keeper is not None:
                keeper._tell(person, holder, text, Severity.URGENT, [])
        world.record(
            Severity.URGENT,
            "person.collapsed",
            f"{person.name} has collapsed, {s.hurt_how}, and is carried below to the surgeon.",
            data={"person": person.name, "sailor": s.id},
        )
        self._deck_by_the_bill(person, holder)

    def go_below_to_the_surgeon(self, person: Any, holder: Any) -> str:
        """The holder's road: he gives the deck and goes below to the cockpit, into the
        surgeon's queue; told when he is dressed."""
        from freesail.orders.errors import OrderError

        crew = self.crew
        sid = getattr(person, "sailor_id", None)
        s = crew.by_id.get(sid) if crew is not None and sid else None
        if s is None or s.hurt not in ("wounded", "hurt"):
            raise OrderError("You are not hurt; there is nothing for the surgeon to see to.")
        if person.where == "cockpit":
            raise OrderError("You are below with the surgeon already.")
        person.where = "cockpit"
        self._deck_by_the_bill(person, holder)
        if s.hurt == "hurt":
            return (
                "You go below to the surgeon; your hurt is dressed already, and he sends you "
                "up again."
            )
        where = "the cockpit" if self.has_surgeon() else "the sick berth"
        waiting = len(self.waiting())
        tail = f"; {number_words(waiting)} before you" if waiting > 1 else ""
        return (
            f"You give the deck and go below to {where} with your wound ({s.hurt_how}){tail}. "
            "You are told when it is dressed, and may come on deck again then."
        )

    def _deck_by_the_bill(self, person: Any, holder: Any) -> None:
        """The deck passes: the officer's station gives it back to the captain, the
        captain's station to the rules captain who carries on by the bill."""
        world = self.world
        agent = getattr(holder, "agent", None) if holder is not None else None
        if holder is not None and agent is not None and getattr(agent, "deck", False):
            try:
                holder._lose_deck("hurt", "hurt and gone below to the surgeon")
            except Exception:  # noqa: BLE001
                agent.deck = False
        cap = getattr(world, "captain", None)
        people = getattr(world, "people", None)
        if cap is not None and people is not None:
            try:
                is_captain = people.captain is person
            except Exception:  # noqa: BLE001
                is_captain = False
            if is_captain and hasattr(cap, "carry_on"):
                try:
                    cap.carry_on()
                except Exception:  # noqa: BLE001
                    pass

    def _holder_dressed(self, person: Any) -> None:
        keeper = getattr(self.world, "needs", None)
        if keeper is None:
            return
        stationed, holder = keeper.holder_of(person)
        if stationed and holder is not None and hasattr(holder, "wound_dressed"):
            holder.wound_dressed()

    def _tell_person(self, person: Any, text: str) -> None:
        keeper = getattr(self.world, "needs", None)
        if keeper is None:
            return
        stationed, holder = keeper.holder_of(person)
        if stationed:
            keeper._tell(person, holder, text, Severity.NOTABLE, [])

    # -- the butcher's bill ----------------------------------------------------------------------

    def _bill(self, tick: int) -> None:
        """The butcher's bill said once, ten minutes after the last shot fired or struck."""
        world = self.world
        crew = self.crew
        st = self.state
        assert crew is not None and st is not None
        keeper = (getattr(self.ship, "extra", None) or {}).get("damage")
        battery = (getattr(self.ship, "extra", None) or {}).get("battery")
        hits = int(getattr(keeper, "hits", 0) or 0)
        if keeper is None or hits == 0 or hits == st.bill_hits:
            return
        last_struck = max(keeper.struck_by.values()) if keeper.struck_by else 0
        last_fired = getattr(battery, "last_fired_tick", None) or 0
        if tick - max(last_struck, last_fired) < BILL_AFTER_S:
            return
        st.bill_hits = hits
        st.bill_said_tick = tick
        killed = [s for s in crew.sailors if s.hurt == "killed"] + list(
            getattr(crew, "dead", []) or []
        )
        wounded = [s for s in crew.sailors if s.hurt in ("wounded", "hurt")]
        grave = [s for s in wounded if getattr(s, "wound", "") in ("grave", "invalid")]
        parts = []
        if killed:
            names = ", ".join(s.name for s in killed[:6])
            parts.append(
                f"{number_words(len(killed))} killed ({names}{', ...' if len(killed) > 6 else ''})"
            )
        if wounded:
            tail = f", {number_words(len(grave))} of them dangerously" if grave else ""
            parts.append(f"{number_words(len(wounded))} wounded{tail}")
        text = "The butcher's bill: " + ("; ".join(parts) if parts else "nobody hurt") + "."
        world.record(
            Severity.NOTABLE,
            "action.bill",
            text,
            data={"killed": len(killed), "wounded": len(wounded), "grave": len(grave)},
        )

    # -- the day: the sick list and the morning report -----------------------------------------

    def _daily(self, tick: int, when: datetime) -> None:
        crew = self.crew
        world = self.world
        st = self.state
        assert crew is not None and st is not None
        stores = getattr(world, "stores", None)
        rng = None
        fit = [
            s for s in crew.sailors if s.fit and not s.hurt and s.station is not Station.QUARTERDECK
        ]
        hazards: list[tuple[float, str]] = []
        if stores is not None:
            from freesail.crew.victuals import victualled

            if victualled(world):
                if bool(getattr(stores, "foul", False)):
                    hazards.append((SICK_FOUL_WATER, "the flux, from the foul water"))
                allowance = float(getattr(stores, "allowance", 1.0))
                if allowance < 1.0:
                    since = int(getattr(stores, "short_since_tick", None) or tick)
                    if (tick - since) / 86400.0 >= SHORT_ALLOWANCE_DAYS:
                        hazards.append(
                            (SICK_SHORT_ALLOWANCE, "sick, worn down by the short allowance")
                        )
                water_out = (
                    float(getattr(stores, "water_tons", 1.0)) <= 0.0
                    and float(getattr(stores, "provisions_days", 1.0)) <= 0.0
                )
                if water_out and st.water_out_since is None:
                    st.water_out_since = tick
                elif not water_out:
                    st.water_out_since = None
                if st.water_out_since is not None:
                    days = (tick - st.water_out_since) / 86400.0
                    if days >= WATER_OUT_DEATH_FROM_D:
                        rng = rng or self.stream()
                        for s in [x for x in crew.sailors if x.hurt != "killed"]:
                            if rng.random() < WATER_OUT_DEATH_SHARE:
                                self._dies(s, tick, "of thirst, the water being expended")
                    if days >= WATER_OUT_SICK_FROM_D:
                        hazards.append((WATER_OUT_SICK_SHARE, "thirst, the water being expended"))
        taken: list[Sailor] = []
        if hazards:
            rng = rng or self.stream()
            for s in fit:
                for p, how in hazards:
                    if rng.random() < p:
                        s.fit = False
                        s.hurt = "sick"
                        s.hurt_how = how
                        s.hurt_tick = tick
                        lo, hi = SICK_DAYS
                        s.hurt_until = tick + int((lo + rng.random() * (hi - lo)) * 86400)
                        s.at = None
                        taken.append(s)
                        break
        if taken:
            hows = sorted({s.hurt_how for s in taken})
            world.record(
                Severity.NOTABLE,
                "health.sick",
                f"The surgeon's report: {number_words(len(taken))} "
                f"{'man' if len(taken) == 1 else 'men'} taken ill, {'; '.join(hows)}; on the "
                "sick list.",
                data={"count": len(taken), "sailors": [s.id for s in taken], "how": hows},
            )
        self._bury(tick, by_order=False)
        self.morning_report(tick)

    def morning_report(self, tick: int) -> None:
        crew = self.crew
        world = self.world
        if crew is None:
            return
        listed = sick_list(crew)
        light = [s for s in crew.sailors if s.hurt == "hurt"]
        if not listed and not light:
            return
        world.record(
            Severity.ROUTINE,
            "health.morning_report",
            self.report_words(),
            data={"sick_list": len(listed), "light_duty": len(light)},
        )

    def report_words(self) -> str:
        crew = self.crew
        if crew is None:
            return "no ship's company"
        wounded = [s for s in crew.sailors if s.hurt == "wounded"]
        grave = [s for s in wounded if getattr(s, "wound", "") in ("grave", "invalid")]
        sick = [s for s in crew.sailors if s.hurt == "sick"]
        dead = [s for s in crew.sailors if s.hurt == "killed"]
        light = [s for s in crew.sailors if s.hurt == "hurt"]
        n = len(wounded) + len(sick)
        who = "The surgeon's" if self.has_surgeon() else "The"
        parts = []
        if wounded:
            parts.append(
                f"{number_words(len(wounded))} wounded"
                + (f" ({number_words(len(grave))} dangerously)" if grave else "")
            )
        if sick:
            parts.append(f"{number_words(len(sick))} sick")
        head = f"{who} morning report: {number_words(n)} on the sick list"
        head += f" ({', '.join(parts)})" if parts else ""
        if light:
            head += f"; {number_words(len(light))} at light duty"
        if dead:
            head += f"; {number_words(len(dead))} dead to be buried"
        return head + "."

    # -- the burial ----------------------------------------------------------------------------

    def _bury(self, tick: int, by_order: bool) -> tuple[str, dict[str, Any]] | None:
        crew = self.crew
        world = self.world
        if crew is None:
            return None
        quarters = (getattr(self.ship, "extra", None) or {}).get("quarters")
        if not by_order and quarters is not None and getattr(quarters, "at_quarters", False):
            return None  # not in action
        dead = [s for s in crew.sailors if s.hurt == "killed"]
        if not dead:
            return None
        buried = getattr(crew, "dead", None)
        if buried is None:
            crew.dead = buried = []
        for s in dead:
            crew.sailors.remove(s)
            buried.append(s)
        crew.reindex()
        names = ", ".join(s.name for s in dead)
        n = len(dead)
        text = (
            f"Committed to the deep the {'body' if n == 1 else 'bodies'} of {names}, "
            f"the ship's company at the gangway and the service read; struck from the books."
        )
        data = {"count": n, "sailors": [s.id for s in dead], "names": [s.name for s in dead]}
        world.record(Severity.NOTABLE, "crew.buried", text, data=data)
        return text, data

    # -- the needs' ends -------------------------------------------------------------------------

    def _needs_ends(self, tick: int) -> None:
        """A stationed person's thirst and hunger meet their ends: collapse, then death."""
        world = self.world
        keeper = getattr(world, "needs", None)
        crew = self.crew
        if keeper is None or crew is None:
            return
        from freesail.world.needs import HUNGER, THIRST

        for person, holder in keeper.stationed():
            if getattr(person, "dead", False):
                continue
            hours = keeper.hours(person)
            thirst, hunger = hours.get(THIRST, 0.0), hours.get(HUNGER, 0.0)
            sid = getattr(person, "sailor_id", None)
            s = crew.by_id.get(sid) if sid else None
            if thirst >= THIRST_DEATH_H or hunger >= HUNGER_DEATH_H:
                how = "of thirst" if thirst >= THIRST_DEATH_H else "of hunger"
                if s is not None:
                    self._dies(s, tick, how)
                else:
                    world.record(
                        Severity.URGENT,
                        "person.killed",
                        f"{person.name} died {how}.",
                        data={"person": person.name},
                    )
                    self._station_killed(
                        person, Sailor("x", person.name, None, None, None, 0.0, 0.0)
                    )  # type: ignore[arg-type]
                continue
            down = thirst >= THIRST_COLLAPSE_H or hunger >= HUNGER_COLLAPSE_H
            if down and not person.sick:
                person.sick = True
                if s is not None and s.hurt == "":
                    s.hurt = "sick"
                    s.fit = False
                    s.hurt_how = "thirst" if thirst >= THIRST_COLLAPSE_H else "hunger"
                    s.hurt_tick = tick
                    s.at = None
                why = "thirst" if thirst >= THIRST_COLLAPSE_H else "hunger"
                person.where = "cockpit" if self.has_surgeon() else person.where
                text = (
                    f"You have collapsed with {why} and are carried below; water and food "
                    "would bring you round, and nothing else will."
                )
                if holder is not None and hasattr(holder, "carried_below"):
                    holder.carried_below(text)
                else:
                    keeper._tell(person, holder, text, Severity.URGENT, [])
                world.record(
                    Severity.URGENT,
                    "person.collapsed",
                    f"{person.name} has collapsed with {why}.",
                    data={"person": person.name, "why": why},
                )
                self._deck_by_the_bill(person, holder)
            elif (
                not down
                and person.sick
                and s is not None
                and s.hurt == "sick"
                and s.hurt_how in ("thirst", "hunger")
            ):
                # water and food brought him round
                person.sick = False
                s.hurt = s.hurt_how = ""
                s.fit = True
                s.hurt_until = None


def bury_the_dead(world: Any, by_order: bool = True) -> tuple[str, dict[str, Any]]:
    """`bury the dead`: the burial service read and the dead struck from the books."""
    from freesail.orders.errors import OrderError

    health = getattr(world, "health", None)
    if health is None:
        raise OrderError("There is nobody to bury: the ship keeps no muster.")
    out = health._bury(int(world.clock.tick), by_order=by_order)
    if out is None:
        raise OrderError(
            "There is nobody to bury; the dead are committed already, or there are none."
        )
    return out


def when_words(world: Any, tick: int) -> str:
    then = world.clock.start + timedelta(seconds=int(tick))
    return then.strftime("%H:%M")
