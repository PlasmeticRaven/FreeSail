"""The hail, and the voice between ships (spec M7 §4; package 71; R-17;
`docs/design/Design-Signals.md`; the tables in `data/captains/hail.yaml`).

Within hail (`ships.HAIL_NM`, four cables) a ship is spoken by the speaking trumpet: the
words are a line of the speaker's log (`hail.made`), a line heard on the other ship's deck
(`hail.heard`, urgent, so a station there wakes), and the answer comes by her body:

- **the rules captain** answers by table (`answer_by_table`): the standard questions
  recognised in the words (what ship, whence, whither, cargo, news, the captain, the days
  out, heave to), each answered from her truth in the period's form by her role and her
  nation; a privateer under false colours lies by the merchant's table under the flag she
  shows, with a name and a port of that nation drawn under the seed; a demand to heave to
  is obeyed, declined or run from by her stance;
- **a model** at the other captain's station hears the words in his sample and answers
  with his own `say to the <hailer>: <words>`; nothing answers by table while his seat is
  live (`model_holds_her`);
- **the player** types the hail and hears the answer on his deck (`hail.answered`); a
  rules captain's hail of him is answered by `say to her: ...` and read by the table's
  nation words (`nation_in_words`), which recognises him to that captain.

Between two rules captains the standard exchange is written once (`exchange_words`) in
each one's words for the other. The hail is the first order of a search: "heave to, I am
sending a boat" from a King's ship is obeyed by a merchantman not at war with her; the
boat and the search are the director's scene and 63's.
"""

from __future__ import annotations

import random
import re
import zlib
from functools import cache
from pathlib import Path
from typing import Any

import yaml

from freesail import units
from freesail.core.events import Severity
from freesail.orders.errors import OrderError

__all__ = [
    "HAIL_PATH",
    "answer_by_table",
    "exchange_words",
    "hail_order",
    "nation_in_words",
    "questions_in",
    "standard_hail",
]

HAIL_PATH = Path(__file__).resolve().parents[2] / "data" / "captains" / "hail.yaml"


@cache
def _table() -> dict[str, Any]:
    return yaml.safe_load(HAIL_PATH.read_text(encoding="utf-8")) or {}


def standard_hail(role: str) -> str:
    return str((_table().get("standard_hail") or {}).get(role) or "What ship is that?")


def questions_in(words: str) -> list[str]:
    """The questions a hail asks, in the table's kinds; 'what ship' when none is asked
    (the hail itself)."""
    low = " ".join(str(words or "").lower().replace("?", " ").split())
    found: list[str] = []
    for kind, phrases in (_table().get("questions") or {}).items():
        if any(p in low for p in phrases) and kind not in found:
            found.append(str(kind))
    return found or ["what ship"]


def nation_in_words(nations: Any, words: str) -> str | None:
    """The nation a hail's answer names ('His Majesty's cutter', 'the Nancy of Guernsey',
    'the French national brig'), or None: the hearer's reading of a stranger's words."""
    low = " ".join(str(words or "").lower().split())
    if not low or nations is None:
        return None
    if "his majesty" in low or "king's" in low or "royal navy" in low:
        return "britain"
    if "catholic majesty" in low:
        return "spain"
    if "danish majesty" in low:
        return "denmark"
    if "most faithful" in low:
        return "portugal"
    if "united states" in low or "american" in low:
        return "united-states"
    if "batavian" in low or "dutch" in low:
        return "batavian-republic"
    if "french" in low or "republic" in low or "emperor's" in low or "national" in low:
        return "france"
    for n in nations.nations.values():
        if n.adjective.lower() in low or n.name.lower() in low:
            return n.id
    ports = _table().get("ports") or {}
    for nid, names in ports.items():
        if any(f"of {p.lower()}" in low for p in names):
            return str(nid)
    return None


# ---------------------------------------------------------------------------
# The order
# ---------------------------------------------------------------------------


def hail_order(world: Any, who_words: str, words: str) -> tuple[str, str, dict[str, Any]]:
    """`hail her`, `hail the brig: what ship is that?`, `say to the Nancy: heave to`."""
    from freesail.world.ships import HAIL_NM

    vessel = _addressee(world, who_words)
    if vessel is None:
        raise OrderError(f"Nothing in sight answers to '{who_words}'; the strangers are listed.")
    here = getattr(world, "position", None)
    if here is None:
        raise OrderError("She sails alone: nobody to hail.")
    from freesail.world.geo import bearing_and_distance

    _, distance = bearing_and_distance(here, vessel.position)
    cables = distance / units.CABLE
    if distance > HAIL_NM * units.NAUTICAL_MILE:
        raise OrderError(
            f"She is beyond hail, {cables:.1f} cables off; within four cables she may be "
            "spoken by the trumpet."
        )
    captain = getattr(world, "captain", None)
    role = str(getattr(captain, "role", "") or "kings-ship")
    said = " ".join(str(words or "").split()).strip(" '\"") or standard_hail(role)
    tick = int(world.clock.tick)
    who = _words_for(world, vessel)
    text = f"Hailed {who} by the trumpet: '{said}'"
    world.record(
        Severity.NOTABLE,
        "hail.made",
        text + ".",
        data={"id": vessel.id, "words": said, "questions": questions_in(said)},
    )
    _spoken(world, vessel)
    answer = deliver(world, vessel, said, tick)
    if answer is None:
        return (
            "hail.made",
            text + ". She has a captain of her own to answer; his words will be heard when he "
            "gives them.",
            {"id": vessel.id, "words": said, "level": 1, "answered": False},
        )
    return (
        "hail.answered",
        f"{text}. {_cap(who)} answers: '{answer}'",
        {"id": vessel.id, "words": said, "answer": answer, "level": 1, "answered": True},
    )


def _addressee(world: Any, who_words: str) -> Any:
    sea = getattr(world, "vessels", None)
    if sea is None:
        return None
    w = " ".join(str(who_words or "").lower().split())
    if w.startswith("the "):
        w = w[4:]
    own = _own_id(world)  # her own body is on the sea (package 84, step 7) and no addressee
    candidates = [
        v
        for v in getattr(sea, "vessels", []) or []
        if not getattr(v, "done", False) and str(v.id) != own
    ]
    here = getattr(world, "position", None)
    if here is None:
        return None
    from freesail.world.geo import bearing_and_distance

    def near(v: Any) -> float:
        return bearing_and_distance(here, v.position)[1]

    # the sails in sight first (the model officer's second point: 'the lugger' at three
    # cables from a dismasted lugger in sight resolved to a far lugger on the world's sea):
    # a rig word or a description is matched among the sails the lookout has in sight,
    # and only a name reaches beyond them; a mark in sight that answers to the words (a
    # wreck, a hulk) is said to be no sail
    seen = getattr(getattr(world, "lookout", None), "_sails_seen", None) or {}
    pool = [v for v in candidates if f"sail:{v.id}" in seen or v.id in seen]
    if w in ("her", "him", "them", "stranger", "sail", "chase", "enemy", "vessel", "ship"):
        battery = (getattr(world.ship, "extra", None) or {}).get("battery")
        target = getattr(battery, "target", None) if battery is not None else None
        if target is not None:
            for v in candidates:
                if v.id == target:
                    return v
        return min(pool, key=near) if pool else None
    for v in candidates:
        if v.name.lower() == w or v.name.lower() == who_words.strip().lower():
            return v
    by_kind = [v for v in pool if w in (v.kind.lower(), v.kind.lower().removeprefix("a "))]
    if not by_kind:
        by_kind = [v for v in pool if w in str(v.what or "").lower() or w in v.kind.lower()]
    if by_kind:
        return min(by_kind, key=near)
    mark = _mark_in_sight(world, w)
    if mark is not None:
        raise OrderError(
            f"{mark[:1].upper()}{mark[1:]} is in sight, but she is no sail to answer a hail: "
            "nobody is aboard her to speak."
        )
    found = sea.find(who_words.strip()) if hasattr(sea, "find") else None
    return found if found is not None and str(found.id) != own else None


def _mark_in_sight(world: Any, words: str) -> str | None:
    """A mark or a danger in sight (a wreck, a hulk, a point of interest the world put on
    the sea) whose name or description carries the words: its words, or None."""
    lookout = getattr(world, "lookout", None)
    for s in getattr(lookout, "sightings", None) or []:
        if getattr(s, "seen_as", "") not in ("mark", "danger"):
            continue
        feature = getattr(s, "feature", None)
        text = " ".join(
            str(getattr(feature, a, "") or "") for a in ("name", "description", "kind")
        ).lower()
        if words and words in text:
            return str(getattr(feature, "name", "") or getattr(feature, "description", "") or words)
    return None


def _words_for(world: Any, vessel: Any) -> str:
    lookout = getattr(world, "lookout", None)
    if lookout is not None:
        try:
            name = lookout.sail_name(f"sail:{vessel.id}", "")
            if name:
                return name
        except Exception:  # noqa: BLE001
            pass
    return f"the {vessel.kind.removeprefix('a ')}"


def _spoken(world: Any, vessel: Any) -> None:
    """A sail hailed is spoken: a stranger no more to both (the lookout's flag, the
    brains' `spoken_ids`)."""
    vessel.spoken = True
    vessel.hailed = True
    brain = getattr(vessel, "brain", None)
    own = _own_id(world)
    if brain is not None:
        brain.spoken_ids.add(own)
    captain = getattr(world, "captain", None)
    ids = getattr(captain, "spoken_ids", None)
    if isinstance(ids, set):
        ids.add(str(vessel.id))
    other = getattr(vessel, "crew", None)
    if other is not None and getattr(other, "shape", "") == "full":
        pc = getattr(other, "captain", None)
        pids = getattr(pc, "spoken_ids", None)
        if isinstance(pids, set):
            pids.add(own)


def _own_id(world: Any) -> str:
    from freesail.world.signals import own_id

    return own_id(world)


# ---------------------------------------------------------------------------
# Delivering the hail and the answer by her body
# ---------------------------------------------------------------------------


def deliver(world: Any, vessel: Any, said: str, tick: int) -> str | None:
    """The hail heard on the other ship, and her answer: by table when the rules have
    her, None when a model holds her captain (the words go to his sample and he answers
    with `say to`)."""
    hailer = _own_id(world)
    hailer_words = _hailer_words(world, vessel)
    heard = f"{_cap(hailer_words)}, within hail, hails us: '{said}'"
    crew = getattr(vessel, "crew", None)
    other_world = crew if crew is not None and getattr(crew, "shape", "") == "full" else None
    if other_world is not None:
        other_world.record(
            Severity.URGENT,
            "hail.heard",
            heard + ".",
            data={"id": hailer, "words": said, "questions": questions_in(said)},
        )
        _stations_hear(other_world, heard)
        if model_holds_her(other_world):
            _remember(other_world, hailer, said, tick)
            return None
        answer = answer_by_table(world, vessel, said, other_world=other_world)
        other_world.record(
            Severity.NOTABLE,
            "hail.answered",
            f"Answered {_cap(hailer_words)}'s hail: '{answer}'.",
            data={"id": hailer, "words": said, "answer": answer, "own": True},
        )
    else:
        answer = answer_by_table(world, vessel, said, other_world=None)
        story = list(getattr(vessel, "story", ()) or ())
        story.append((tick, f"hailed by {hailer_words}: '{said}'; answered '{answer}'"))
        vessel.story = tuple(story[-20:])
    world.record(
        Severity.NOTABLE,
        "hail.answered",
        f"{_cap(_words_for(world, vessel))} answers the hail: '{answer}'.",
        data={"id": vessel.id, "words": said, "answer": answer, "own": False},
    )
    _read_answer(world, vessel, answer)
    return answer


def _hailer_words(world: Any, vessel: Any) -> str:
    """The hailer in the hailed ship's words: her lookout's name for him, else his rig."""
    crew = getattr(vessel, "crew", None)
    other = crew if crew is not None and getattr(crew, "shape", "") == "full" else None
    own = _own_id(world)
    if other is not None:
        lookout = getattr(other, "lookout", None)
        if lookout is not None:
            try:
                name = lookout.sail_name(f"sail:{own}", "")
                if name:
                    return name
            except Exception:  # noqa: BLE001
                pass
    # his rig: his own vessel's on the sea (the player's ship one of them, package 84, step 7)
    sea = getattr(getattr(world, "parent", None) or world, "vessels", None)
    v = sea.get(own) if sea is not None else None
    kind = str(getattr(v, "kind", "") or "")
    return f"the {kind.removeprefix('a ')}" if kind else "a sail"


def _stations_hear(other_world: Any, line: str) -> None:
    try:
        from freesail.agents.harness import _stations_held
    except Exception:  # noqa: BLE001
        return
    for h in _stations_held(other_world):
        try:
            h.hear(line)
        except Exception:  # noqa: BLE001
            pass


def model_holds_her(other_world: Any) -> bool:
    """Whether a model (or the player) holds the other ship's captain, so that no table
    answers for her: the player's own ship with no rules captain commanding, or a seat at
    her captain's station."""
    captain = getattr(other_world, "captain", None)
    # the followed hull (`parent` None), whose prompt is the player's (package 84, step
    # 10; 82's §4: by the hull the player holds, which is the followed one)
    player = getattr(other_world, "parent", None) is None
    base = getattr(other_world, "world", other_world)
    is_players = other_world is getattr(base, "players", None)
    # `Captain.commands` is a property (the playtest of 2026-10-27: called as a method, the
    # TypeError was swallowed, and the player's ship answered every hail by table). The
    # player's ship alone (package 86's fold-in, the review's finding): a crewed ship whose
    # captain stands aside or holds by the director's hand is answered by the table as
    # before, for nobody else would answer her hail
    if player and captain is not None and not getattr(captain, "commands", True):
        return True
    if captain is None and (player or is_players):
        return True  # the player's ship with no rules captain at all
    stations = getattr(other_world, "stations", None)
    try:
        from freesail.agents.agent import CAPTAIN

        holder = stations.holder(CAPTAIN) if stations is not None else None
        if holder is not None and CAPTAIN in (getattr(other_world, "agents", {}) or {}):
            return True
    except Exception:  # noqa: BLE001
        pass
    return False


def _remember(other_world: Any, hailer: str, said: str, tick: int) -> None:
    """The hail awaiting the model's answer, for `say to her`."""
    extra = getattr(other_world.ship, "extra", None)
    if extra is not None:
        extra["hail_pending"] = {"from": hailer, "words": said, "tick": tick}


def _read_answer(world: Any, vessel: Any, answer: str) -> None:
    """The hailer's captain reads the nation in the answer: recognised so (a liar's
    words are believed; the private signal and the shot are the tells)."""
    nations = getattr(world, "nations", None)
    nation = nation_in_words(nations, answer)
    captain = getattr(world, "captain", None)
    rec = getattr(captain, "recognised", None)
    if nation and isinstance(rec, dict):
        own = _own_nation(world)
        enemy = nations is not None and nations.at_war(nation, own)
        rec[str(vessel.id)] = {"nation": nation, "how": "the hail", "enemy": bool(enemy)}


def _own_nation(world: Any) -> str:
    from freesail.world.signals import own_nation

    return own_nation(world)


# ---------------------------------------------------------------------------
# The answer by table
# ---------------------------------------------------------------------------


def answer_by_table(world: Any, vessel: Any, said: str, other_world: Any = None) -> str:
    """What the hailed ship's rules captain says to the words, by the table: her role,
    her nation and the colours she shows; a privateer under false colours lies."""
    table = _table()
    brain = getattr(vessel, "brain", None)
    role = str(getattr(brain, "role", "") or "")
    if other_world is not None:
        role = str(getattr(getattr(other_world, "captain", None), "role", "") or role)
    if not role:
        role = "merchant"
    from freesail.world.signals import colours_of

    colours = colours_of(vessel if other_world is None else other_world.ship)
    lying = role == "privateer" and colours.state == "false"
    shown = colours.nation if colours.shows else str(vessel.nation)
    kind_key = "lie" if lying else role
    answers = (table.get("answers") or {}).get(kind_key) or (table.get("answers") or {}).get(
        "merchant"
    )
    fills = _fills(world, vessel, role, shown if lying else str(vessel.nation), lying, other_world)
    hailer_world = world
    questions = questions_in(said)
    # the demand answered, and obeyed or run from, only when the words make it (2026-10-27:
    # every hail had her make all sail, "hailed to heave to; she will not")
    fills["heave_to"] = (
        _heave_to(world, vessel, role, other_world, hailer_world) if "heave to" in questions else ""
    )
    out: list[str] = []
    for q in questions:
        template = str((answers or {}).get(q) or "")
        if not template:
            continue
        try:
            words = template.format(**fills)
        except (KeyError, IndexError):
            words = template
        out.append(words[:1].upper() + words[1:])  # each answer a sentence of its own
    return " ".join(out) if out else fills.get("name", "a ship")


def _fills(
    world: Any, vessel: Any, role: str, nation: str, lying: bool, other_world: Any
) -> dict[str, str]:
    table = _table()
    nations = getattr(world, "nations", None)
    rng = random.Random(zlib.crc32(f"hail:{vessel.id}:{nation}".encode()))
    ports = [str(p) for p in ((table.get("ports") or {}).get(nation) or ["the port"])]
    port = ports[rng.randrange(len(ports))]
    name = str(vessel.name or "")
    if lying:
        names = [str(n) for n in ((table.get("lies") or {}).get(nation) or ["Nancy"])]
        name = names[rng.randrange(len(names))]
    kind = str(vessel.kind or "a ship").removeprefix("a ")
    if "brig" in kind and "sloop" in str(vessel.description or ""):
        kind = "sloop"
    navy = str((table.get("navy") or {}).get(nation) or "the {kind} {name}").format(
        kind=kind, name=name
    )
    goal = str(getattr(vessel, "goal", "") or "")
    voyage, voyage_short, frm = _voyage_words(world, vessel, goal, port, lying)
    description = str(vessel.what or vessel.description or "")
    deep = "deep" in description or "laden" in description
    pool = (table.get("cargo") or {}).get("deep" if deep else "light") or ["in ballast"]
    cargo = str(pool[rng.randrange(len(pool))])
    captain = _captain_name(vessel, other_world, rng, nation)
    days = str(1 + rng.randrange(9))
    news = nations.wars_words() if nations is not None else "no news"
    return {
        "navy": navy,
        "name": name,
        "port": frm or port,
        "voyage": voyage,
        "voyage_short": voyage_short,
        "cargo": cargo,
        "captain": captain,
        "days": days,
        "news": news[:1].upper() + news[1:],
        "kind": kind,
    }


def _voyage_words(
    world: Any, vessel: Any, goal: str, home: str, lying: bool
) -> tuple[str, str, str]:
    """('from Guernsey for Falmouth', 'For Falmouth', 'Guernsey') from her goal's words
    ('bound for Falmouth', 'trading Falmouth to the Lizard', 'cruising off the Lizard');
    a liar names a port of the nation she shows as her own."""
    low = goal.lower()
    m = re.search(r"trading\s+(.+?)\s+to\s+(.+)$", low)
    if m and not lying:
        a, b = _cap(m.group(1)), _cap(m.group(2))
        return f"from {a} for {b}", f"For {b}", a
    m = re.search(r"(?:bound|passage|sail)\s+(?:from\s+(.+?)\s+)?(?:for|to)\s+(.+)$", low)
    if m:
        b = _cap(m.group(2))
        a = _cap(m.group(1)) if m.group(1) and not lying else home
        return f"from {a} for {b}", f"For {b}", a
    m = re.search(
        r"(?:cruis\w+|patrol\w+|fish\w+|keep the station)\s+off\s+(.+?)(?:\s+within.*)?$", low
    )
    if m:
        if lying:  # a cruiser's errand is no merchantman's: a passage between two ports
            return f"from {home} for Falmouth", "For Falmouth", home
        return f"from {home}, cruising off {_cap(m.group(1))}", f"For {home}", home
    return f"from {home}", f"For {home}", home


def _captain_name(vessel: Any, other_world: Any, rng: random.Random, nation: str) -> str:
    if other_world is not None:
        captain = getattr(other_world, "captain", None)
        name = getattr(captain, "name", None)
        if name:
            return str(name)
    brain = getattr(vessel, "brain", None)
    name = getattr(brain, "name", None)
    if name and "captain" not in str(name).lower():
        return str(name)
    french = nation in ("france",)
    names = (
        ["Captain Leroux", "Captain Dubois", "Captain Marchand", "Captain Lefèvre"]
        if french
        else ["Captain Pender", "Captain Hoskin", "Captain Vosper", "Captain Bligh", "Captain Rowe"]
    )
    return names[rng.randrange(len(names))]


def _heave_to(world: Any, vessel: Any, role: str, other_world: Any, hailer_world: Any) -> str:
    """The demand to heave to, answered by her stance and performed when obeyed."""
    table = _table().get("heave_to") or {}
    nations = getattr(world, "nations", None)
    hailer_nation = _own_nation(hailer_world)
    hailer_captain = getattr(hailer_world, "captain", None)
    hailer_role = str(getattr(hailer_captain, "role", "") or "")
    hailer_navy = (
        hailer_role in ("kings-ship", "cruiser", "commodore")
        or getattr(hailer_world, "parent", None) is None
    )
    at_war = bool(nations is not None and nations.at_war(hailer_nation, str(vessel.nation)))
    if role in ("kings-ship", "cruiser", "commodore"):
        return str(table.get("declines") or "")
    if role == "privateer" or at_war or not hailer_navy:
        _make_sail(world, vessel, other_world)
        return str(table.get("runs") if role != "privateer" else table.get("privateer") or "")
    _heave_her_to(world, vessel, other_world)
    return str(table.get("obeys") or "")


def _heave_her_to(world: Any, vessel: Any, other_world: Any) -> None:
    if other_world is not None:
        captain = getattr(other_world, "captain", None)
        try:
            if captain is not None:
                captain.give("heave to", why="a King's ship's demand within hail")
                return
            other_world.submit("heave to", actor="captain", routine=True)
        except Exception:  # noqa: BLE001
            return
        return
    from freesail.world.signals import far_perform

    far_perform(getattr(world, "parent", None) or world, vessel, "heave to")


def _make_sail(world: Any, vessel: Any, other_world: Any) -> None:
    if other_world is not None:
        captain = getattr(other_world, "captain", None)
        try:
            if captain is not None:
                captain.give("make all sail", why="hailed to heave to; she will not")
        except Exception:  # noqa: BLE001
            return
        return
    from freesail.world.signals import far_perform

    far_perform(getattr(world, "parent", None) or world, vessel, "make all sail")


# ---------------------------------------------------------------------------
# Two rules captains
# ---------------------------------------------------------------------------


def exchange_words(world: Any, a: Any, b: Any) -> str:
    """The standard exchange between two far captains within hail, written once: a's
    hail and b's answer, and b's hail and a's answer, in the table's words."""
    ra = str(getattr(getattr(a, "brain", None), "role", "") or "merchant")
    rb = str(getattr(getattr(b, "brain", None), "role", "") or "merchant")
    ha, hb = standard_hail(ra), standard_hail(rb)
    answer_b = answer_by_table(world, b, ha)
    answer_a = answer_by_table(world, a, hb)
    return f"'{ha}' '{answer_b}' '{hb}' '{answer_a}'"


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]


def player_hailed(world: Any, vessel: Any, said: str) -> None:
    """A rules captain's hail of the player's ship within hail (43's line says it): the
    words heard on deck for the stations, and kept for his answer (`say to her: ...`),
    which her captain reads for his nation."""
    extra = getattr(world.ship, "extra", None)
    if extra is not None:
        extra["hail_pending"] = {"from": vessel.id, "words": said, "tick": int(world.clock.tick)}
    _stations_hear(world, f"{_cap(_words_for(world, vessel))}, within hail, hails us: '{said}'")
