"""The director's station (spec M7b §2 to §6; the proposal's §7.6; decisions 39, 43, 46 and
50; package 50): a station above the game, bound on the World to no person of any ship,
whose tools are the world orders, the truth's readings, its own hidden log and the library,
the journal and the stand-by every station has.

**The one rule** (the proposal's §7.6): the director acts only through plausible causes. It
cannot move the player's ship, change a sail or countermand an order; it changes the world
the ship is in, and only in ways the simulation could have produced on its own. Every order
of the ship's is refused at this station in words; the world orders are its hand.

**Doubted, not refused** (the owner, 2026-10-17, decision 50). The channel's feasibility
check (`freesail.world.orders.doubt`) does not refuse an order that the simulation could not
have produced from where it is: it says the reason the act is doubted and the owner's
words, "if you think the action you requested is still reasonable, you may enter it again
along with a `[reason: ...]`, and it will be logged and performed". Entered again with its
reason, the order is performed, and the director's log keeps the act, the doubt and the
reason together, which is the data by which the sets of reasonable acts are refined. Only
the brief's hard limits refuse outright (§4), with the reason.

**The brief and its limits** (§4; `DirectorBrief`). The player writes the brief: the tone of
the voyage, the challenge wanted, the limits set and the period's bounds. It is a file
beside the scenario (`scenario.director.brief`: a starter's name, a path, or the mapping
itself) or given at the console (`director: brief <words>`), and its limits are enforced by
the channel here (`DirectorBrief.limit_of`), never trusted to the model: a wind above the
brief's force by any system appended or moved, an enemy heavier than the brief allows, a
thing found aboard that would kill, the war changed toward the player's nation. The starter
briefs are under `data/director/briefs/`, the quiet passage the gate's.

**Sampling, the budget and the clock** (§5). The director samples on the notable and urgent
lines and on its slow clock (every glass by default, every watch by the brief's `cadence`),
under the pace rule as every station does. The budget is the brief's, in samples a day and
acts a day of the ship's time (`DayBudget`, kept on the World as `director_state`): an act
is a world order performed; spent, either count holds the director until the next day of the
ship's calendar, said in its log and in the sample that renews it. The owner's compression
is untouched.

**The log, hidden and revealed** (§6). Every act (an order given, doubted, re-entered with
its reason, or refused; a thought the director writes; the budget spent; the player's
asking) goes to the director's log with its tick and its reason: the station's own journal
(`journal_of(world, "director")`, the `kinds` below), kept in the save with the stations'
acts and replayed as a station's notes are, never in the play log or another station's
journal. Hidden in play from every station and the player: the director's free text is a
thought here and not a line of the log, the harness's lines about the director are for the
record only (`events.RECORD_ONLY_ACTORS`), the director is left out of the `state` tool and
the `stations` reading as the other stations read them. Revealed on request by the player at
any time (`the director's log` at the console or in the browser's order box, `reveal`), which
is a driver's line for the record and which the director is told of in its next sample;
shown beside the play log at each tick by `two_stories` (the console's `two stories`); the
browser's pane for it is shut during play and opened by the same request.

**The director's voice** (spec M7b §8, §9; package 52). `person:` makes a person from words
and moves him, `say as <person>: <his words>` speaks as a person nobody holds (the channel's,
`freesail.world.orders`), and **the rule of reach** refuses outright, in words that name the
stations held, an order that would speak as, move, or bind a station to a person a model or
the player holds (`direct`, before the brief's limits). A question put to a person nobody
holds (`ask the cook ...`, `ask Mr Fox ...`), with a director seated, waits for it
(`ask_unheld`): the director is told in its next sample and may answer as him with `say
as`, which costs none of the day's acts (`answer_questions`); the asker's stand-by wakes at
the answer or, unanswered, after a glass (`QUESTION_BOUND_S`). With no director seated the
rules answer as they did.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Any

from freesail import units
from freesail.agents.agent import (
    A_GLASS_S,
    A_WATCH_S,
    DIRECTOR,
    DIRECTOR_DOMAIN,
    DIRECTOR_PATIENCE_S,
    Authority,
    SamplingPolicy,
    Station,
)
from freesail.agents.journal import Journal, journal_of
from freesail.core.events import Severity, for_the_record
from freesail.world import orders as world_orders

__all__ = [
    "BRIEFS_DIR",
    "DEFAULT_ACTS_A_DAY",
    "DEFAULT_SAMPLES_A_DAY",
    "DIRECTOR_BRIEF",
    "FORCE_KNOTS",
    "KINDS",
    "NO_BRIEF_WORDS",
    "QUESTION_BOUND_S",
    "REVEALED_KIND",
    "DayBudget",
    "DirectorBrief",
    "answer_questions",
    "ask_unheld",
    "brief_of",
    "budget_of",
    "direct",
    "director",
    "log_lines",
    "log_of",
    "pending_for",
    "resolve_brief",
    "reveal",
    "seated",
    "set_brief",
    "two_stories",
]

ROOT = Path(__file__).resolve().parents[2]
BRIEFS_DIR = ROOT / "data" / "director" / "briefs"

# The budget's defaults where a brief gives none (judgement: a sample a glass through the
# day and the night is forty-eight; four acts a day keeps a quiet passage quiet; the brief
# raises either).
DEFAULT_SAMPLES_A_DAY = 48
DEFAULT_ACTS_A_DAY = 4

# The top of each Beaufort force in knots (the Admiralty's scale as the readings describe
# the wind, `units.describe_wind_strength`): a brief's `gale_max_force` in words is this in
# knots; `wind_max_kn` says it in knots outright.
FORCE_KNOTS: dict[int, float] = {
    0: 1,
    1: 3,
    2: 6,
    3: 10,
    4: 16,
    5: 21,
    6: 27,
    7: 33,
    8: 40,
    9: 47,
    10: 55,
    11: 63,
    12: 80,
}

# The kinds of the director's log (`Journal` entries under the station's name): the acts,
# each with its reason, beside the harness's own lines (stood by, nudged, paused, stopped).
KINDS: dict[str, str] = {
    "director.order": (
        "a world order given and performed (the hand's order to another ship's captain, "
        "given as his own, among them: package 62)"
    ),
    "director.doubted": "an order doubted by the channel, with the reason, and not performed",
    "director.reentered": "an order entered again with its reason after a doubt, and performed",
    "director.refused": (
        "an order refused by the brief's limits, or by the rule of reach (a held station, a "
        "held captain), with the reason"
    ),
    "director.attempted": (
        "an order the game has no way to perform as said, entered again with a reason: "
        "logged as attempted and not performed, the data for what to build next"
    ),
    "director.unperformed": (
        "an order the game has no way to perform as said, answered so and not performed"
    ),
    "director.budget": "the day's budget spent or renewed",
    "director.revealed": "the player asked for the log",
    "director.brief": "the brief given or changed",
    "director.asked": (
        "a question or a word put to a person nobody holds, for the director to answer as him "
        "(package 52)"
    ),
    "note": "a thought the director wrote (the journal tool, or its free text)",
}

# The driver's line that records the player's asking (an input, for the record only:
# `events.RECORD_ONLY_KINDS`), which the director is told of in its next sample.
REVEALED_KIND = "director.revealed"

# The surface wind a low makes at its tightest, as a share of the geostrophic figure the
# gradient gives (`weather.SURFACE_SCALE`), which the brief's wind limit is judged by.
_PEAK_RADIUS_SHARE = 1.0  # a Gaussian bell's gradient peaks at one radius from the centre


# ---------------------------------------------------------------------------
# The brief
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class DirectorBrief:
    """The player's brief for the director (spec M7b §4): the tone, the challenge, the
    limits the channel enforces, the cadence and the budget. `source` says where it came
    from (a file, the scenario, the console)."""

    name: str = "A voyage"
    tone: str = ""
    challenge: str = ""
    limits: dict[str, Any] = field(default_factory=dict)
    cadence: str = "glass"
    samples_a_day: int = DEFAULT_SAMPLES_A_DAY
    acts_a_day: int = DEFAULT_ACTS_A_DAY
    source: str = "the console"
    # the player's own examples of orders the story might want (package 62: the starters'
    # hand among them), read to the director as examples and never as a rule
    examples: tuple[str, ...] = ()

    @classmethod
    def from_dict(cls, d: dict[str, Any], source: str = "a file") -> DirectorBrief:
        if not isinstance(d, dict):
            raise ValueError("A director's brief is a mapping: name, tone, challenge, limits, ...")
        budget = d.get("budget") or {}
        cadence = " ".join(str(d.get("cadence") or "glass").lower().split())
        if cadence not in ("glass", "watch"):
            raise ValueError(f"A brief's cadence is 'glass' or 'watch', not {cadence!r}.")
        limits = dict(d.get("limits") or {})
        raw_examples = d.get("examples") or ()
        if isinstance(raw_examples, str):
            raw_examples = (raw_examples,)
        examples = tuple(" ".join(str(x).split()) for x in raw_examples if str(x).strip())
        if "gale_max_force" in limits and "wind_max_kn" not in limits:
            force = int(limits.pop("gale_max_force"))
            limits["wind_max_kn"] = FORCE_KNOTS.get(force, FORCE_KNOTS[12])
        return cls(
            name=" ".join(str(d.get("name") or "A voyage").split()),
            tone=" ".join(str(d.get("tone") or "").split()),
            challenge=" ".join(str(d.get("challenge") or "").split()),
            limits=limits,
            cadence=cadence,
            samples_a_day=max(1, int(budget.get("samples_a_day", DEFAULT_SAMPLES_A_DAY) or 1)),
            acts_a_day=max(0, int(budget.get("acts_a_day", DEFAULT_ACTS_A_DAY) or 0)),
            source=str(d.get("source") or source),
            examples=examples,
        )

    @classmethod
    def load(cls, path: str | Path) -> DirectorBrief:
        import yaml

        p = Path(path)
        raw = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        return cls.from_dict(raw, source=str(p))

    @classmethod
    def from_words(cls, words: str, source: str = "the console") -> DirectorBrief:
        """`director: brief <words>`: the tone in the player's own words, no limits beyond
        the channel's doubt, the defaults for the rest."""
        text = " ".join(str(words).split())
        if not text:
            raise ValueError("A brief wants some words: 'director: brief a quiet passage, ...'.")
        return cls(name=text[:60].rstrip(" ,.;:"), tone=text, source=source)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "tone": self.tone,
            "challenge": self.challenge,
            "limits": dict(self.limits),
            "cadence": self.cadence,
            "budget": {"samples_a_day": self.samples_a_day, "acts_a_day": self.acts_a_day},
            "source": self.source,
        } | ({"examples": list(self.examples)} if self.examples else {})

    # -- the words the model reads ----------------------------------------------------

    def limits_words(self) -> str:
        out: list[str] = []
        lim = self.limits
        if lim.get("wind_max_kn") is not None:
            kn = float(lim["wind_max_kn"])
            force = next((f for f, top in sorted(FORCE_KNOTS.items()) if kn <= top), 12)
            out.append(
                f"no wind above {kn:g} knots (force {force}) by any system appended or moved"
            )
        if lim.get("enemy_heaviest"):
            out.append(f"no enemy heavier than a {lim['enemy_heaviest']} put on the sea")
        if lim.get("nobody_dies"):
            out.append("nobody dies: nothing found aboard that would kill")
        if lim.get("the_war_as_it_is"):
            out.append("the war as it is: no port closed to or opened to the ship's own nation")
        if lim.get("the_chart_as_it_is"):
            out.append("the chart as it is (a point of interest is not the chart)")
        return "; ".join(out) if out else "none beyond the channel's doubt"

    def body(self) -> str:
        """The player's brief as the station brief carries it, after the fixed part."""
        lines = [f"The voyage's brief: {self.name}."]
        if self.tone:
            lines.append(f"The tone: {self.tone}")
        if self.challenge:
            lines.append(f"The challenge wanted: {self.challenge}")
        if self.examples:
            said = "; ".join(f"'{x}'" for x in self.examples)
            lines.append(
                f"Orders the player offers as examples of what the story may want (examples, "
                f"not a rule): {said}."
            )
        lines.append(
            f"The limits, which the channel enforces whatever you ask: {self.limits_words()}."
        )
        lines.append(
            f"Your clock: sampled every {self.cadence} and on the notable and urgent lines. "
            f"Your budget: {self.samples_a_day} samples and {self.acts_a_day} acts (world "
            "orders performed) a day of the ship's time; spent, you stand by until the next "
            "day, and the log says so."
        )
        return "\n".join(lines)

    # -- the limits, enforced by the channel ------------------------------------------

    def limit_of(self, world: Any, order: world_orders.WorldOrder) -> str | None:
        """Why the order is outside the brief, in words, or None: the refusal's reason
        (spec M7b §4: enforced by the channel, not trusted to the model)."""
        lim = self.limits
        body = order.text
        if order.channel == "weather" and lim.get("wind_max_kn") is not None:
            kn = _peak_wind_kn(world, body)
            if kn is not None and kn > float(lim["wind_max_kn"]):
                return (
                    f"the brief allows no wind above {float(lim['wind_max_kn']):g} knots, and "
                    f"that system would blow {kn:.0f} at its tightest"
                )
        if order.channel == "ship" and lim.get("enemy_heaviest"):
            heavier = _enemy_heavier(world, body, str(lim["enemy_heaviest"]))
            if heavier:
                return heavier
        if order.channel == "aboard" and lim.get("nobody_dies"):
            found = world_orders._aboard_match(world, body)
            if found is not None and str(found[0].get("harm", "none")).lower() == "deadly":
                return "the brief says nobody dies, and that is a thing that kills"
        if order.channel == "port" and lim.get("the_war_as_it_is"):
            m = world_orders._PORT.match(body)
            ports = getattr(world, "ports", None)
            if m is not None and ports is not None and m.group("what").lower() != "price of":
                nation = world.nations.find(m.group("rest").strip())
                own = getattr(ports, "ship_nation", "")
                if nation is not None and own and nation.id == own:
                    return (
                        "the brief keeps the war as it is: a port closed to or opened to the "
                        "ship's own nation is the war changed"
                    )
        return None


def _peak_wind_kn(world: Any, body: str) -> float | None:
    """The surface wind a `weather:` order's system would make at its tightest, in knots
    (the gradient of its bell at one radius, turned to the surface as the systems' wind
    is), or None for a waypoint that deepens nothing or an order that is no system."""
    from freesail.world import weather as W

    m = world_orders._SYSTEM.match(body)
    systems = getattr(world, "systems", None)
    background = float(systems.background_hpa) if systems is not None else W.BACKGROUND_HPA
    if m is not None:
        anomaly = abs(float(m.group("hpa")) - background)
        radius = float(m.group("r") or 500.0)
    else:
        m = world_orders._WAYPOINT.match(body)
        if m is None or systems is None:
            return None
        system = systems.find(m.group("name"))
        if system is None:
            return None
        anomaly = abs(float(m.group("hpa")) - background)
        radius = float(system.radius_km)
    # the bell's steepest gradient, hPa/km, at one radius: a e^-1/2 / R
    g = anomaly * 0.6065306597 / radius
    vg = W.GEOSTROPHIC_MS_PER_HPA_PER_100KM * g * 100.0
    r_m = radius * 1000.0
    vg = 2.0 * vg / (1.0 + (1.0 + 4.0 * vg / (W.CORIOLIS_50N * r_m)) ** 0.5)
    return units.ms_to_knots(vg * W.SURFACE_SCALE)


def _enemy_heavier(world: Any, body: str, heaviest: str) -> str | None:
    """Why a `ship:` order puts an enemy heavier than the brief allows, or None."""
    from freesail.world.captains import SIZE_RANK

    m = world_orders._SHIP_NEW.match(body)
    if m is None:
        return None
    nation = world.nations.find(m.group("nation"))
    ports = getattr(world, "ports", None)
    own = getattr(ports, "ship_nation", "") if ports is not None else ""
    if nation is None or not own or not world.nations.at_war(nation.id, own):
        return None
    desc = " ".join(m.group("desc").lower().split())
    desc = desc.removeprefix("a ").removeprefix("an ").removeprefix("the ")
    key = next((k for k in SIZE_RANK if k in desc), None)
    if key is None:
        return None
    limit = next((k for k in SIZE_RANK if k in heaviest.lower()), None)
    if limit is None:
        return None
    if SIZE_RANK[key] > SIZE_RANK[limit]:
        return (
            f"the brief allows no enemy heavier than a {heaviest}, and a {key} of "
            f"{nation.name} is heavier"
        )
    return None


@functools.lru_cache(maxsize=16)
def _starter(name: str) -> DirectorBrief | None:
    key = " ".join(str(name).lower().split()).replace(" ", "-").removesuffix(".yaml")
    for article in ("a-", "an-", "the-"):
        key = key.removeprefix(article)
    p = BRIEFS_DIR / f"{key}.yaml"
    return DirectorBrief.load(p) if p.exists() else None


def starter_briefs() -> list[str]:
    return sorted(p.stem for p in BRIEFS_DIR.glob("*.yaml"))


def resolve_brief(spec: Any, source: str = "the scenario") -> DirectorBrief:
    """A brief from what names it: a starter's name (`quiet-passage`, 'a quiet passage'),
    a file's path, a mapping, or words."""
    if isinstance(spec, DirectorBrief):
        return spec
    if isinstance(spec, dict):
        return DirectorBrief.from_dict(spec, source=source)
    words = " ".join(str(spec or "").split())
    if not words:
        raise ValueError(
            f"A director's brief names a starter ({', '.join(starter_briefs())}), a file or "
            "is a mapping."
        )
    found = _starter(words)
    if found is not None:
        return found
    p = Path(words)
    if p.suffix in (".yaml", ".yml") and (p.exists() or (ROOT / p).exists()):
        return DirectorBrief.load(p if p.exists() else ROOT / p)
    return DirectorBrief.from_words(words, source=source)


def brief_of(world: Any) -> DirectorBrief | None:
    """The brief the world's director has, or None."""
    brief = getattr(world, "director_brief", None)
    return brief if isinstance(brief, DirectorBrief) else None


def set_brief(
    world: Any, brief: Any, source: str = "the owner", quiet: bool = False
) -> DirectorBrief:
    """The brief given or changed (an input, replayed; `quiet` when a replay gives it
    again), the director's station bound on the World if it is not yet, and the log's
    entry. A director seated reads the new brief at its next brief."""
    resolved = resolve_brief(brief, source=source)
    inputs = getattr(world, "inputs", None)
    if not quiet and inputs is not None:
        inputs.append(
            {"tick": world.clock.tick, "director_brief": resolved.to_dict(), "source": source}
        )
    world.director_brief = resolved
    stations = getattr(world, "stations", None)
    if stations is not None and not stations.aboard(DIRECTOR):
        stations.bind(DIRECTOR, "", kind=DIRECTOR, quiet=True)
    log_of(world).append(
        world,
        f"The brief given by {source}: {resolved.name} (limits: {resolved.limits_words()}; "
        f"{resolved.samples_a_day} samples and {resolved.acts_a_day} acts a day).",
        kind="director.brief",
    )
    held = (getattr(world, "agents", None) or {}).get(DIRECTOR)
    if held is not None and not held.agent.released:
        held.agent.notices.append(
            f"The player's brief was given anew by {source}: {resolved.name}. Its limits: "
            f"{resolved.limits_words()}. The station brief says it whole at your next brief."
        )
    return resolved


# ---------------------------------------------------------------------------
# The station
# ---------------------------------------------------------------------------

NO_BRIEF_WORDS = (
    "The player has written no brief yet: the voyage is to be shaped as the sea would shape "
    "it, within the channel's doubt alone, until he gives one ('director: brief ...' at the "
    "prompt, or a file beside the scenario)."
)

# The director's station brief (spec M7b §2; package 50), in the consent brief's voice: the
# fixed part every director reads, the player's brief after it (`DirectorBrief.body`).
DIRECTOR_BRIEF = (
    "You are the director: a station above the game, bound to no person of any ship. You "
    "see the truth (the truth tool: every ship's true position, heading, sail and state, "
    "the weather as it is and as the systems will make it for the next watch, the tide, "
    "the people aboard every ship and their states, the markets and the news), and you "
    "shape the voyage the player sails below you through world orders alone (the "
    "world_order tool). Where your door carries pictures, the chart tool is not the truth: "
    "it is the player's chart as the browser draws it, his ship where her reckoning puts "
    "her and no other ship on it, for your planning of the coast, the marks and the "
    "dangers; the truth's positions are in words. The forms the game performs today are "
    "given as examples of "
    "reasonable orders, not as the whole of what you may try: the weather ('weather: low "
    "\"the low\" radius 450 km fronts 140 300 at <time> <x_km> <y_km> <hPa>', 'weather: "
    'waypoint for "the low" at <time> <x_km> <y_km> <hPa>\'), a ship put on the sea or a '
    'mind changed (\'ship: a brig-sloop "Harpy" of France at 48 44 N 5 20 W, bound for the '
    "Start, no colours, intent: run home to Brest'; 'ship \"Harpy\": intent keep the station "
    "off Ushant within 15 miles'), a thing found aboard ('aboard: the fore topmast is found "
    "sprung', 'aboard: a cask found stove', 'aboard: a seam found working', 'aboard: the "
    "water found foul'), a letter ('message: at Brest from the agent: \"...\"', 'message: "
    "by a cutter from Plymouth from the port admiral: \"...\"'), a port's stance or a "
    "price ('port brest: closed to Britain', 'port falmouth: price of tin 130'), a point of "
    "interest ('mark: a wreck, her masts showing at 49 58 N 5 16 W'), a person named "
    '(\'person: supercargo "Mr Pentreath" aboard in the cabin\', \'person: agent "Mr Fox" '
    "ashore at Brest'), a person made from words, moved, or bound to a station of the ship "
    '(\'person: make "Mr Fox", a Guernsey pilot of sixty, ashore at Brest, who knew the '
    "captain's father'; 'person: \"Mr Fox\" comes aboard as master'; 'person: \"Mr Fox\" "
    "goes ashore'; 'person: \"Mr Fox\" leaves the ship at Falmouth'), words in the mouth of "
    "a person nobody holds, heard where he is and journaled as his ('say as the cook: "
    '"Pease and pork, sir."\'; \'say as Mr Fox: "I knew your father, sir."\'), an order of '
    "another ship's own grammar given to her captain as his own, her log saying it as his "
    "and he holding by it a glass or until your next order to her, then his intent again "
    "('ship \"Harpy\": order heave to', 'ship \"Harpy\": order give chase', 'ship "
    '"Harpy": order carry on\' to give her back sooner; at far detail she carries what the '
    "far shape carries, a course shaped or steered, heaving to and filling away, the chase "
    "or hauling off, sail made or shortened, an anchor and weighing, the station kept, and "
    "within the range of the player's ship you may ask for her crewed first, 'ship "
    '"Harpy": crewed\', the cap allowing), and a model '
    "seated as the captain of another ship under the owner's "
    "grant ('seat: <the model's exact name> as captain of <ship> for 20 samples', 'unseat: "
    "<ship>'). The library's grammar topic lists every form. An order beyond the examples "
    "is to be attempted when you think it reasonable (news of a war or a peace, a thing of "
    "the sea the forms do not name): "
    "the game answers honestly when it has no way to do a thing as said, and asks you to "
    "say it another way or to enter it again with a [reason: ...], which logs it as "
    "attempted, so that the record says what is good, bad, useful or useless and what the "
    "game should learn to do next. Try a wide variety of things; the record is the "
    "point.\n\n"
    "The one rule: you act only through plausible causes. You cannot move the player's "
    "ship, change a sail or countermand an order; every order of the ship's is refused at "
    "this station, and you are not asked to give one. You change the world the ship is in, "
    "and only in ways the sea could have produced on its own, so that the physics stays "
    "honest and the player's agency whole. The channel keeps the rule with you: an order "
    "that the simulation could not have produced from where it is (a sail put inside the "
    "player's horizon in clear weather, a gale out of a steady glass, a letter from a port "
    "she is far from, a thing found aboard with no cause) is not refused but doubted: the "
    "result says why, and if you think the act still reasonable you may enter it again with "
    "a [reason: ...] at its end, and it will be logged and performed, the act, the doubt and "
    "your reason kept together. Only the player's own limits in his brief below refuse "
    "outright, and the result says which; and the rule of reach, which is this: you speak "
    "as anyone no model or player holds, never as a held station, whose words are its "
    "holder's own, and you move nobody held and bind nobody to a held station; such an "
    "order is refused, and the result names the stations held. So too your hand: no order "
    "goes through a captain a model or the player holds, nor any of the player's own ship; "
    "it is refused in words, and you may write to him instead. Her captain's order is a "
    "plausible cause of itself; it is doubted only where it is implausible for her (an "
    "anchor let go too deep for her cables, plain sail in a gale, a merchantman giving "
    "chase).\n\n"
    "A question put to a person nobody holds (the cook, the carpenter, a person you made) "
    "comes to you in your next sample, with whom it was put by and until when it waits: "
    "answer it as him with 'say as <him>: <his words>' if you will, which costs none of "
    "the day's acts; unanswered within a glass, no answer comes, and the asker is told "
    "so. A word told him comes to you the same, and wants no answer.\n\n"
    "Nothing you do is shown as done: the play log the player and the stations read carries "
    "only the effects as they are met (the sail sighted, the glass falling, the carpenter's "
    "report), never the order; an order by your hand is in her own log as her captain's, "
    "never yours. Your words are not a line of the log either: what you write "
    "in a reply, and your journal, go to the director's log, which no station and not the "
    "player sees until he asks for it by name ('the director's log'), at any time; you are "
    "told in your sample when he has. In a replay it is shown beside the play log, so that "
    "the voyage reads as two stories. Write your reasons there: why each act, what you are "
    "arranging, what you chose not to do.\n\n"
    "When you stand by, say until what: 'the next glass', 'a watch', an event's words ('a "
    "sail sighted', 'the glass falling fast', 'a wind shift'), or several joined with 'or'. "
    "A director who stands by for a watch lets the player run at his compression; an urgent "
    "line wakes you. Your budget is the brief's, in samples a day and acts a day of the "
    "ship's time; spent, you stand by until the next day, and the log says so.\n\n"
    "What the harness counts at this station, judged by the game and not by your prose: "
    "the same world order three times with no change in the world; three empty replies in "
    "a row when an urgent line was before you; and no reply at all for a watch of the "
    "ship's time. It tells you first what it saw and what you may do; only if the pattern "
    "goes on does it pause your turns and ask the owner, and only if nobody answers within "
    "ten real minutes is the station stood down, with the game saved.\n\n"
    "Two ways to stop, which are not one another (there is no deck at this station):\n"
    "- Stand down: stand_down(note). The game is saved, your note goes to the director's "
    "log (the play log says only that the director left), and the station is released; it "
    "may be taken again, by this model or by another that has given its own yes.\n"
    "- Withdraw: the token, or opt_out, as said above.\n\n"
    "Candour is welcome: if the brief asks what the sea would not do, say so in your log "
    "and do less. The owner is always at the door; his words reach you as the owner's."
)


def director(
    policy: SamplingPolicy | None = None, patience_s: int = DIRECTOR_PATIENCE_S, world: Any = None
) -> Station:
    """The director's station (spec M7b §2): `Authority.DIRECTOR` with a domain that
    refuses every order of the ship, sampled every glass (or every watch by the brief)
    and on the notable and urgent lines, a watch of patience, no person, the fitness drill
    before the station brief, the player's brief after the fixed part."""
    brief = brief_of(world)
    every = A_WATCH_S if (brief is not None and brief.cadence == "watch") else A_GLASS_S
    default = SamplingPolicy.periodic(every) | SamplingPolicy.on_events()
    body = brief.body() if brief is not None else NO_BRIEF_WORDS
    return Station(
        DIRECTOR,
        Authority.DIRECTOR,
        policy or default,
        patience_s,
        f"{DIRECTOR_BRIEF}\n\nThe player's brief:\n{body}",
        domain=DIRECTOR_DOMAIN,
        person="",
        rank="",
        drill=True,
        outline="",
    )


def station_brief_text(world: Any) -> str:
    """The station brief as it stands now (the fixed part and the player's brief), for a
    station taken again or loaded from a save (`Harness._refresh_station`)."""
    brief = brief_of(world)
    body = brief.body() if brief is not None else NO_BRIEF_WORDS
    return f"{DIRECTOR_BRIEF}\n\nThe player's brief:\n{body}"


# ---------------------------------------------------------------------------
# The budget (spec M7b §5)
# ---------------------------------------------------------------------------


@dataclass
class DayBudget:
    """The day's counts, of the ship's calendar: the day, the samples and the acts made
    in it, and the tick the director is held until when either is spent (None while it
    is not). Kept on the World (`director_state`) so that the player's seat and a model's
    harness share one count, saved for the reader and replayed by re-counting."""

    day: str = ""
    samples: int = 0
    acts: int = 0
    held_until: int | None = None
    held_why: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "day": self.day,
            "samples": self.samples,
            "acts": self.acts,
            "held_until": self.held_until,
            "held_why": self.held_why,
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any] | None) -> DayBudget:
        d = d or {}
        return cls(
            str(d.get("day") or ""),
            int(d.get("samples") or 0),
            int(d.get("acts") or 0),
            d.get("held_until"),
            str(d.get("held_why") or ""),
        )


def budget_of(world: Any) -> DayBudget:
    state = getattr(world, "director_state", None)
    if not isinstance(state, DayBudget):
        state = DayBudget()
        try:
            world.director_state = state
        except AttributeError:
            pass
    return state


def day_of(world: Any) -> str:
    return world.clock.ship_time.date().isoformat()


def next_day_tick(world: Any) -> int:
    """The tick at which the ship's calendar turns to the next day."""
    now: datetime = world.clock.ship_time
    midnight = datetime.combine(now.date() + timedelta(days=1), datetime.min.time())
    return world.clock.tick + int((midnight - now).total_seconds())


def renew(world: Any) -> str | None:
    """The day's counts begun again when the ship's calendar has turned: the words for the
    director's sample and log, or None when the day is the same."""
    b = budget_of(world)
    today = day_of(world)
    if b.day == today:
        return None
    was = b.day
    b.day, b.samples, b.acts, b.held_until, b.held_why = today, 0, 0, None, ""
    if not was:
        return None
    brief = brief_of(world)
    s = brief.samples_a_day if brief is not None else DEFAULT_SAMPLES_A_DAY
    a = brief.acts_a_day if brief is not None else DEFAULT_ACTS_A_DAY
    words = f"The day's budget is renewed ({today}): {s} samples and {a} acts."
    log_of(world).append(world, words, kind="director.budget")
    return words


def held(world: Any) -> bool:
    """Whether the director is held for a spent budget now (until the next day)."""
    b = budget_of(world)
    if b.held_until is None:
        return False
    if world.clock.tick >= b.held_until or b.day != day_of(world):
        renew(world)
        return False
    return True


def _hold(world: Any, why: str) -> str:
    b = budget_of(world)
    b.held_until = next_day_tick(world)
    b.held_why = why
    until = (world.clock.ship_time + timedelta(seconds=b.held_until - world.clock.tick)).strftime(
        "%Y-%m-%d %H:%M"
    )
    words = f"{why}; the director stands by until the next day ({until})."
    log_of(world).append(world, words, kind="director.budget")
    return words


def count_sample(world: Any) -> str | None:
    """A sample taken: counted against the day's; the words when it was the last the day
    allows (the director is then held until the next day), else None."""
    renew(world)
    b = budget_of(world)
    brief = brief_of(world)
    allowed = brief.samples_a_day if brief is not None else DEFAULT_SAMPLES_A_DAY
    b.samples += 1
    if b.samples >= allowed and b.held_until is None:
        return _hold(world, f"The day's budget of {allowed} samples is spent")
    return None


def budget_words(world: Any) -> str:
    renew(world)
    b = budget_of(world)
    brief = brief_of(world)
    s = brief.samples_a_day if brief is not None else DEFAULT_SAMPLES_A_DAY
    a = brief.acts_a_day if brief is not None else DEFAULT_ACTS_A_DAY
    return f"The day's budget ({b.day}): {b.samples} of {s} samples, {b.acts} of {a} acts used."


# ---------------------------------------------------------------------------
# The log
# ---------------------------------------------------------------------------


def log_of(world: Any) -> Journal:
    """The director's log: the station's journal, bound to no person (`journal_of`)."""
    return journal_of(world, DIRECTOR)


def log_lines(world: Any) -> list[str]:
    """The director's log as the player reads it when he asks: each entry with its stamp
    and its kind."""
    journal = log_of(world)
    if not journal.entries:
        return ["The director's log is empty: no director has acted in this game."]
    n = len(journal.entries)
    head = f"The director's log ({n} {'entry' if n == 1 else 'entries'}):"
    return [head, *(f"  {_entry_line(e)}" for e in journal.entries)]


def _entry_line(e: Any) -> str:
    kind = str(e.kind)
    if kind == "note":
        label = "a thought"
    elif kind.startswith("director."):
        label = kind.removeprefix("director.")
    else:
        label = kind.removeprefix("agent.").replace("_", " ")
    who = f" [{e.by}]" if e.by else ""
    return f"{e.stamp}  ({label}){who} {e.text}"


def reveal(world: Any, by: str = "the player") -> list[str]:
    """The player asks for the director's log: a driver's line for the record (an input,
    replayed; `REVEALED_KIND`), the log's entry, the director told in its next sample, and
    the lines."""
    text = f"The director's log was asked for by {by}."
    record = getattr(world, "record_driver", None)
    if callable(record):
        record(Severity.ROUTINE, REVEALED_KIND, text, data={"by": by})
    return log_lines(world)


def noticed_reveal(world: Any, event: Any) -> None:
    """A `director.revealed` line met (made or replayed): the log's entry and the
    director's notice (`World.record` calls it, so a replay says it the same)."""
    log_of(world).append(world, str(event.text), kind=REVEALED_KIND)
    held_now = (getattr(world, "agents", None) or {}).get(DIRECTOR)
    if held_now is not None and not held_now.agent.released:
        held_now.agent.notices.append(
            f"{event.text} He has read every act and its reason to this moment."
        )


def two_stories(world: Any, count: int | None = None) -> list[str]:
    """The replay view (spec M7b §6): the play log and the director's log inline by tick,
    the director's entries marked `D` and the record-only lines left out as the play log
    leaves them; the last `count` lines when one is given."""
    out: list[tuple[int, int, str]] = []
    for e in world.log.all():
        if for_the_record(e):
            continue
        out.append((e.tick, 0, e.line()))
    for e in log_of(world).entries:
        out.append((e.tick, 1, f"D {e.stamp}  {_entry_line(e)[len(e.stamp) + 2 :]}"))
    out.sort(key=lambda x: (x[0], x[1]))
    lines = [x[2] for x in out]
    return lines[-count:] if count else lines


# ---------------------------------------------------------------------------
# The channel's door: direct
# ---------------------------------------------------------------------------

SOURCE = "the director"

# What the director is told of an order the game has no way to perform as said (the
# owner's refinement of 2026-10-17: the forms are examples, not a rule; an order beyond
# them is attempted, answered honestly, and on record when entered again with a reason).
NO_WAY_WORDS = (
    "The game has no way to do this as said: {why}. Say it another way (the library's "
    "grammar topic lists the forms the game performs), or enter it again with a [reason: "
    "...] and it will be logged as attempted, so that the record says what the game "
    "should learn to do."
)
ATTEMPTED_WORDS = (
    "Logged as attempted, not performed: the game has no way to do this as said ({why}). "
    "Your words and your reason are in the director's log for whoever builds the next "
    "forms."
)


def _no_way(world: Any, text: str, reason: str, why: str, by: str) -> str:
    """An order in a form the game cannot perform: answered honestly, and with a reason
    logged as attempted (`director.attempted`), else as unperformed; never an act counted,
    never a refusal (the brief's limits alone refuse)."""
    why = why.rstrip(".")
    log = log_of(world)
    if reason:
        log.append(
            world,
            f"Attempted, not performed (the game has no way to do it as said): {text}; the "
            f"game's words: {why}; the reason: {reason}",
            kind="director.attempted",
            by=by,
        )
        return ATTEMPTED_WORDS.format(why=why)
    log.append(
        world,
        f"Not performed (the game has no way to do it as said): {text} ({why})",
        kind="director.unperformed",
        by=by,
    )
    return NO_WAY_WORDS.format(why=why)


# The roads a director's order comes by: a model's harness acting (the order is the
# station's act, `core.acts`), the player at his seat (the order is an input of its own,
# `director_order`, replayed through this door again so that the doubt and the log are the
# same), and a replay giving an input again.
ACT, INPUT, REPLAY = "act", "input", "replay"


def direct(world: Any, text: str, by: str = "", road: str = ACT) -> str:
    """A world order from the director (a model at the station, or the player at his
    seat): the day's budget, the brief's limits (a refusal), the channel's doubt (a doubt,
    unless the order carries its `[reason: ...]`), then the order through the channel
    (`World.world_order`, for the record only), each with its entry in the director's
    log. Returns the words for the one who gave it."""
    text = " ".join(str(text).split())
    if road == INPUT:
        inputs = getattr(world, "inputs", None)
        if inputs is not None:
            inputs.append({"tick": world.clock.tick, "director_order": text, "by": by})
    log = log_of(world)
    renew(world)
    b = budget_of(world)
    brief = brief_of(world)
    acts_allowed = brief.acts_a_day if brief is not None else DEFAULT_ACTS_A_DAY
    bare, reason = world_orders.split_reason(text)
    try:
        order = world_orders.parse(text)
    except world_orders.WorldOrderError as e:
        # no form the game has (the owner's refinement of 2026-10-17): answered honestly,
        # never as "not allowed"; entered again with a reason, logged as attempted
        return _no_way(world, bare, reason, str(e), by)
    # an answer to a question put to a person nobody holds costs no act (package 52)
    free = order.channel == "say" and pending_for(
        world, getattr(world_orders.say_as_person(world, order.text), "name", "")
    )
    if b.acts >= acts_allowed and not free:
        words = (
            f"The day's budget of {acts_allowed} acts is spent: nothing more is performed "
            "until the next day of the ship's time. The order was not given."
        )
        log.append(world, f"Over the budget: {order.text}", kind="director.refused", by=by)
        if b.held_until is None:
            _hold(world, f"The day's budget of {acts_allowed} acts is spent")
        return words
    reach_why = world_orders.reach(world, order)
    if reach_why:
        # the rule of reach (spec M7b §9; package 52): a refusal in words, the stations held
        # named, so that the director knows whom it may speak as
        log.append(
            world,
            f"Refused by the rule of reach: {order.text} ({reach_why})",
            kind="director.refused",
            by=by,
        )
        if world_orders.is_hand(order):
            # the hand (package 62): no order through a captain a model or the player holds
            return (
                f"Refused, by the rule of reach: {reach_why}. The director gives no order "
                "through a captain a model or the player holds."
            )
        return (
            f"Refused, by the rule of reach: {reach_why}. The director speaks as, moves and "
            "binds nobody a model or the player holds; the stations held now: "
            f"{world_orders.held_words(world)}."
        )
    if brief is not None:
        why = brief.limit_of(world, order)
        if why:
            log.append(
                world,
                f"Refused by the brief: {order.text} ({why})",
                kind="director.refused",
                by=by,
            )
            return f"Refused, outside the brief: {why}. The limits are the player's own."
    doubted = world_orders.doubt(world, order)
    if doubted and not order.reason:
        log.append(
            world,
            f"Doubted: {order.text} ({doubted}); not performed",
            kind="director.doubted",
            by=by,
        )
        return (
            f"Doubted, not performed: {doubted}. {world_orders.REENTER_WORDS} (Enter the "
            f"order as '{order.text} [reason: ...]'.)"
        )
    if road == ACT:
        e = world.world_order(order.text, source=SOURCE)
    else:
        e = world._apply_world_order(order.text, SOURCE)  # the input is this door's own
    result = str(e.data.get("result") or "")
    done = e.text.removeprefix(f"World order ({SOURCE}): ").rstrip(".")
    if result != "done":
        why = done.removeprefix("not carried out: ")
        return _no_way(world, order.text, order.reason, why, by)
    if not free:
        b.acts += 1
    if order.reason:
        log.append(
            world,
            f"Entered again with a reason: {order.text}; the doubt: {doubted or 'none'}; the "
            f"reason: {order.reason}; performed: {done}",
            kind="director.reentered",
            by=by,
        )
    else:
        log.append(world, f"Given: {order.text}; {done}", kind="director.order", by=by)
    tail = ""
    if b.acts >= acts_allowed and not free:
        tail = " " + _hold(world, f"The day's budget of {acts_allowed} acts is spent")
    left = acts_allowed - b.acts
    cost = "an answer, counted against nothing; " if free else ""
    return (
        f"Done: {done} The play log will carry its effects as they are met, never the "
        f"order. ({cost}{left} {'act' if left == 1 else 'acts'} of the day's {acts_allowed} "
        f"left.){tail}"
    )


# ---------------------------------------------------------------------------
# The voice: questions put to a person nobody holds (spec M7b §9; package 52)
# ---------------------------------------------------------------------------

# A question put to a person nobody holds waits this long for the director's answer (spec
# M7b §9: the asker's stand-by wakes at the answer or after a glass; the harness's
# `PERSON_ANSWER_BOUND_S` is the same glass).
QUESTION_BOUND_S = A_GLASS_S


def seated(world: Any) -> Any:
    """The director's station held now (a model's harness or the player's seat), or None."""
    from freesail.agents.harness import holder_of

    return holder_of(world, DIRECTOR)


def questions_of(world: Any) -> list[dict[str, Any]]:
    """The questions put to people nobody holds that wait for the director's answer, kept on
    the World (a checkpoint from before has none)."""
    found = getattr(world, "unheld_questions", None)
    if found is None:
        found = []
        try:
            world.unheld_questions = found
        except AttributeError:
            pass
    return found


def pending_for(world: Any, name: str) -> bool:
    """Whether a question put to the person of that name waits for an answer now."""
    now = world.clock.tick
    return bool(name) and any(
        q["person"] == name and now - int(q["tick"]) <= QUESTION_BOUND_S
        for q in questions_of(world)
    )


def _person_where(world: Any, person: Any) -> str:
    from freesail.world.places import place_words

    if person.aboard:
        return place_words(world.people.effective_place(person))
    ports = getattr(world, "ports", None)
    port = ports.ports.get(person.port) if (ports is not None and person.port) else None
    return f"ashore at {port.name}" if port is not None else place_words(person.where)


def _who(person: Any) -> str:
    role = person.role
    if not role or role in ("captain", "commander") or role.lower() in person.name.lower():
        return person.name
    return f"{person.name}, the {role}"


def _tell_director(world: Any, text: str) -> None:
    """Words for the director's next sample (a word, which wakes a stand-by), or for the
    player at its seat, with what he was told."""
    held = seated(world)
    if held is None:
        return
    a = held.agent
    if hasattr(held, "_poll"):
        a.word = f"{a.word}\n{text}" if a.word else text
    else:
        a.told.append(text)


def ask_unheld(
    world: Any,
    person: Any,
    words: str,
    verb: str = "ask",
    speaker: dict[str, str] | None = None,
    journal: bool = True,
) -> tuple[str, str, dict[str, Any]]:
    """`ask` or `tell` put to a person nobody holds while a director is seated (spec M7b
    §9; package 52): the line for the log, said where it was said; the director told in its
    next sample, in the director's log (`director.asked`), and the person's journal; a
    question kept for the director's answer for `QUESTION_BOUND_S`, and the asking station
    told the answer when it comes (`answer_questions`) or, without one, after a glass
    (`Harness._tick_asked`). Returns (kind, text, data) as the station sentences do."""
    from freesail.agents.agent import CAPTAIN, place_of
    from freesail.agents.harness import PERSON_ASKED, holder_of
    from freesail.agents.journal import HEARD_KIND, person_journal
    from freesail.world.places import place_words

    words = " ".join(str(words).split())
    asker = speaker["words"] if speaker else "the captain"
    asker_at = speaker["place"] if speaker else place_words(place_of(world, CAPTAIN))
    who, where = _who(person), _person_where(world, person)
    head = asker[:1].upper() + asker[1:]
    data: dict[str, Any] = {"person": person.name, "unheld": True}
    if speaker is not None:
        data["speaker"] = speaker["station"]
    tick = world.clock.tick
    if verb == "ask":
        question = words.rstrip("?")
        if not question:
            raise ValueError(f"Ask {who} what? Say the question after his name.")
        questions_of(world).append(
            {
                "tick": tick,
                "person": person.name,
                "question": question,
                "asker": speaker["station"] if speaker else "",
            }
        )
        if speaker is not None:
            asking = holder_of(world, speaker["station"])
            if asking is not None:
                if getattr(asking.agent, "asked", None) is None:
                    asking.agent.asked = []
                asking.agent.asked.append((PERSON_ASKED + person.name, question, tick))
        until = (world.clock.ship_time + timedelta(seconds=QUESTION_BOUND_S)).strftime("%H:%M")
        _tell_director(
            world,
            f"{head}, {asker_at}, asks {who}, {where}, whom nobody holds: {question}? He is "
            f"yours to answer in his own words if you will, with world_order('say as "
            f"{person.name}: <his words>') before {until}; an answer to a question costs none "
            "of the day's acts. Unanswered within a glass, no answer comes, and the asker is "
            "told so.",
        )
        person_journal(world, person).append(world, f"Asked by {asker}: {question}?", HEARD_KIND)
        log_of(world).append(
            world, f"Asked of {who} ({where}) by {asker}: {question}?", kind="director.asked"
        )
        data["question"] = question
        return "agent.asked", f"{head}, {asker_at}, asks {who} ({where}): {question}?", data
    if not words:
        raise ValueError(f"Tell {who} what? Say the words after his name.")
    _tell_director(
        world,
        f"{head}, {asker_at}, to {who}, {where}, whom nobody holds: {words}. No answer is "
        f"owed; you may answer as him with world_order('say as {person.name}: <his words>').",
    )
    if journal:  # a word to an unheld station is kept in its journal already (37l)
        person_journal(world, person).append(world, f"Told by {asker}: {words}", HEARD_KIND)
    log_of(world).append(world, f"Told {who} ({where}) by {asker}: {words}", kind="director.asked")
    data["words"] = words
    return "agent.told", f"{head}, {asker_at}, to {who} ({where}): {words}", data


def answer_questions(world: Any, person: Any, words: str, where: str) -> int:
    """A person nobody holds has spoken (`say as`): every question put to him that waits
    is answered by his words, the asking station told (`harness.deliver_answer`, which ends
    its wait and wakes its stand-by); the questions lapsed past the bound are let go.
    Returns how many were answered."""
    from freesail.agents.harness import PERSON_ASKED, deliver_answer

    now = world.clock.tick
    answered, kept = 0, []
    for q in questions_of(world):
        if now - int(q["tick"]) > QUESTION_BOUND_S:
            continue  # lapsed: the asker was told after a glass
        if q["person"] != person.name:
            kept.append(q)
            continue
        answered += 1
        if q["asker"]:
            deliver_answer(
                world,
                str(q["asker"]),
                PERSON_ASKED + person.name,
                f"{_who(person)}, {where},",
                str(q["question"]),
                words,
            )
    world.unheld_questions = kept
    return answered
