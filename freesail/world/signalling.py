"""The rules captain's minute of signals, for both bodies (spec M7 §1 to §4; package 71;
`docs/design/Design-Signals.md`): what his people read this minute answered, obeyed when
the sender commands him (`under the orders of`), the private signal challenged to every
strange sail within the flags' range and its reply judged, the stranger recognised by it;
a privateer's false colours by her doctrine, and the true colours before the first shot.

One function a body: `near_minute(captain, p)` for the near body (the player's rules
captain or a promoted ship's), whose lookout has already read the flags into her locker's
log and whose orders go through `Captain.give`; `far_minute(brain, p)` for the far body,
which reads the flying hoists of the sail in sight here (no lookout of her own) and
performs the few orders the signals give on her plan (`signals.far_perform`). Both keep
`recognised` on the captain (a ship's id to what he knows of her: the nation, how he knows
it, whether she is an enemy), which `_is_enemy` reads before the colours.
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world import signals as S

__all__ = ["far_minute", "near_minute", "recognise", "verdict_of"]

# The switches for the bisection of what each item moved (the tuning notes, package 71):
# off, no challenge is made and no colours are shifted by doctrine.
CHALLENGES = True
DOCTRINE_COLOURS = True

# The states in which a King's captain challenges a stranger (not in action, not struck).
CHALLENGE_STATES = frozenset(
    {
        "on passage",
        "beating",
        "keeping station",
        "investigating a stranger",
        "chasing",
        "evading",
    }
)


# ---------------------------------------------------------------------------
# What a captain knows of a sail
# ---------------------------------------------------------------------------


def recognise(cap: Any, sid: str, nation: str | None, how: str, enemy: bool) -> None:
    rec = getattr(cap, "recognised", None)
    if not isinstance(rec, dict):
        rec = cap.recognised = {}
    rec[str(sid)] = {"nation": nation, "how": how, "enemy": bool(enemy)}


def verdict_of(cap: Any, sid: str) -> dict[str, Any] | None:
    rec = getattr(cap, "recognised", None)
    return rec.get(str(sid)) if isinstance(rec, dict) else None


def _own_nation(cap: Any) -> str:
    vessel = getattr(cap, "vessel", None)
    if vessel is not None:
        return str(vessel.nation)
    return S.own_nation(cap.world)


def _own_id(cap: Any) -> str:
    vessel = getattr(cap, "vessel", None)
    if vessel is not None:
        return str(vessel.id)
    return S.own_id(cap.world)


def _nations(cap: Any) -> Any:
    return getattr(cap.world, "nations", None)


def _locker(cap: Any) -> S.Locker:
    vessel = getattr(cap, "vessel", None)
    if vessel is not None:
        return S.vessel_locker(vessel)
    return S.player_locker(cap.world)


def _books(cap: Any) -> S.Books:
    return S.books_for_nation(_nations(cap), _own_nation(cap))


def _table(cap: Any) -> S.PrivateTable | None:
    vessel = getattr(cap, "vessel", None)
    if vessel is not None:
        return S.vessel_table(cap.world, vessel)
    return S.table_of(cap.world)


def _root_world(cap: Any) -> Any:
    world = cap.world
    return getattr(world, "parent", None) or world


def _body_of(cap: Any, sid: str) -> Any:
    """The body a stranger's id names, for its locker: a far vessel, or the player's
    shadow under `the ship`."""
    root = _root_world(cap)
    v = root.vessels.get(sid)
    if v is None and sid == "the ship":
        v = root.vessels.player_shadow(root)
    return v


def _light(cap: Any) -> str:
    return S.light_now(_root_world(cap))


# ---------------------------------------------------------------------------
# The near body
# ---------------------------------------------------------------------------


def near_minute(cap: Any, p: Any) -> None:
    """The near body's minute: the locker's log (filled by the lookout), the challenges,
    the verdicts, the colours by doctrine."""
    world = cap.world
    locker = _locker(cap)
    tick = int(world.clock.tick)
    _handle_log(cap, locker, tick, near=True)
    _judge_challenges(cap, locker, p, tick)
    _challenge_strangers(cap, locker, p, tick, near=True)
    _colours_by_doctrine(cap, locker, p, tick, near=True)
    _succession(cap, locker, tick, near=True)
    fog_signals_minute(cap, p, near=True)


# ---------------------------------------------------------------------------
# The far body
# ---------------------------------------------------------------------------


def far_minute(brain: Any, p: Any) -> None:
    """The far body's minute: the flying hoists of the sail in sight read here, then as
    the near body's."""
    world = brain.world
    vessel = brain.vessel
    locker = S.vessel_locker(vessel)
    tick = int(world.clock.tick)
    books = _books(brain)
    light = _light(brain)
    reader_id = str(vessel.id)
    if locker.flying and getattr(vessel, "crew", None) is None:
        locker.tidy(tick, books.flies_s)  # the far body has no lookout to tidy for her
    heard: set[str] = set()
    for s in p.strangers:
        sid = str(s.get("id") or "")
        est = s.get("estimate_m")
        if not sid or est is None:
            continue
        body = _body_of(brain, sid)
        if body is None:
            continue
        other = S.vessel_locker(body) if sid != "the ship" else getattr(body, "signals", None)
        if other is None or not other.flying:
            continue
        hoists = other.flying_now(tick)
        if not hoists:
            continue
        if light == "day" and int(s.get("made_out") or 0) < 1:
            continue
        words = str(s.get("known") or "a sail").split(",")[0]
        words = f"the {words.removeprefix('a ').removeprefix('an ')}"
        seen = S.read_flying(
            locker,
            books,
            sid,
            words,
            hoists,
            float(est),
            light,
            sid == getattr(brain, "_stranger", None),
            tick,
            reader_id,
        )
        S.note_seen(locker, seen, tick)
        heard.add(sid)
        for item in seen:
            if item.read and item.kind != "signal.answered":
                _story(vessel, tick, item.text.rstrip("."))
    if light == "fog":
        _hear_fog_guns(brain, locker, books, tick, heard)
    _handle_log(brain, locker, tick, near=False)
    _judge_challenges(brain, locker, p, tick)
    _challenge_strangers(brain, locker, p, tick, near=False)
    _colours_by_doctrine(brain, locker, p, tick, near=False)
    _succession(brain, locker, tick, near=False)
    fog_signals_minute(brain, p, near=False)


def _hear_fog_guns(brain: Any, locker: S.Locker, books: S.Books, tick: int, heard: set) -> None:
    """In a fog the far body hears the fog book's gun from a ship she cannot see, within
    `GUN_HEARD_NM` (the near body's lookout gives her the same as a sound sighting): the
    ship she is under the orders of by her title, any other as a ship unseen."""
    from freesail.world.geo import bearing_and_distance

    vessel = brain.vessel
    root = _root_world(brain)
    others = [o for o in root.vessels.vessels if o is not vessel and not o.done]
    shadow = root.vessels.player_shadow(root)
    if shadow is not None:
        others.append(shadow)
    orders_of = str(getattr(vessel, "under_orders_of", "") or "")
    for o in others:
        sid = str(o.id)
        if sid in heard:
            continue
        other = getattr(o, "signals", None)
        if other is None or not other.flying:
            continue
        hoists = [h for h in other.flying_now(tick) if h.book == "fog"]
        if not hoists:
            continue
        _, distance = bearing_and_distance(vessel.position, o.position)
        if distance / units.NAUTICAL_MILE > S.GUN_HEARD_NM:
            continue
        words = (
            "the commodore unseen in the fog" if sid == orders_of else "a ship unseen in the fog"
        )
        seen = S.read_flying(
            locker, books, sid, words, hoists, float(distance), "fog", False, tick, str(vessel.id)
        )
        S.note_seen(locker, seen, tick)
        for item in seen:
            if item.read:
                _story(vessel, tick, item.text.rstrip("."))


def _story(vessel: Any, tick: int, words: str) -> None:
    story = list(getattr(vessel, "story", ()) or ())
    story.append((tick, words))
    vessel.story = tuple(story[-30:])


# ---------------------------------------------------------------------------
# The log handled: answers, obedience, the private signal
# ---------------------------------------------------------------------------


def _handle_log(cap: Any, locker: S.Locker, tick: int, near: bool) -> None:
    own = _own_id(cap)
    books = _books(cap)
    for entry in locker.log:
        if entry.get("handled"):
            continue
        entry["handled"] = True
        kind = str(entry.get("kind") or "")
        h = entry.get("hoist")
        sender = str(entry.get("by") or "")
        if h is None or not sender or sender == own:
            continue
        if kind == "signal.answered":
            for mine in locker.flying:
                if mine.by == own and mine.book not in ("answer", "reply") and mine.down is None:
                    mine.answered_by.add(sender)
            continue
        if kind == "signal.private":
            _answer_challenge(cap, locker, h, sender, tick, near)
            continue
        if kind == "signal.private_reply":
            continue  # judged with the challenges below
        if kind != "signal.read":
            continue  # seen and not read: nothing to answer with
        # a signal of the book read: answered with the pendant, and obeyed when he commands us
        if h.key not in locker.answered:
            _answer(cap, locker, books, sender, tick, near)  # the order marks it answered
            locker.answered.add(h.key)
        commanded = S.commanded_by(_body_or_world(cap), sender) or (h.to == own)
        if commanded:
            if h.in_succession:
                locker.challenges.setdefault("__succession__", {})
                pending = locker.challenges["__succession__"]
                pending[h.key] = {"hoist": h, "sender": sender, "tick": tick}
            else:
                _obey(cap, locker, h, sender, tick, near)


def _body_or_world(cap: Any) -> Any:
    vessel = getattr(cap, "vessel", None)
    return vessel if vessel is not None else cap.world


def _answer(cap: Any, locker: S.Locker, books: S.Books, sender: str, tick: int, near: bool) -> None:
    if near:
        try:
            cap.give("answer the signal", why="the signal read")
        except Exception:  # noqa: BLE001 - refused in words (no hands): no pendant
            pass
        return
    S.make_answer(locker, books, _own_id(cap), tick, sender)


def _obey(cap: Any, locker: S.Locker, h: S.Hoist, sender: str, tick: int, near: bool) -> None:
    """A commanded captain performs the hoist's `does`."""
    does = h.does or {}
    locker.obeyed[h.key] = tick
    why = f"the signal from {sender}: {h.meaning}"
    if does.get("release"):
        vessel = getattr(cap, "vessel", None)
        if vessel is not None:
            vessel.under_orders_of = ""
        else:
            cap.world.under_orders_of = ""
        _say(cap, tick, f"Released from {sender}'s orders by signal: she proceeds on her own.")
        return
    if does.get("closer"):
        cap._business["closer"] = True
        _say(cap, tick, "Engage the enemy more closely: the range halved by signal.")
        return
    state = does.get("state")
    if state:
        if state in ("chasing", "investigating a stranger"):
            near_s = (
                cap._nearest_stranger(_perceive(cap)) if hasattr(cap, "_nearest_stranger") else None
            )
            if near_s is not None:
                cap._stranger = near_s.get("id")
        if getattr(cap, "state", None) != state and state in (
            "chasing",
            "investigating a stranger",
            "on passage",
            "engaging",
        ):
            try:
                cap._enter(state)
            except Exception:  # noqa: BLE001
                return
            _say(cap, tick, f"By {sender}'s signal: {h.meaning.lower()}.")
        return
    order = S.order_of(h)
    if not order:
        return
    if near:
        try:
            cap.give(order, why=why)
        except Exception:  # noqa: BLE001 - refused in words: logged by the order
            pass
        return
    vessel = cap.vessel
    done = S.far_perform(_root_world(cap), vessel, order)
    if done:
        _story(vessel, tick, f"by {sender}'s signal ({h.meaning.lower()}): {done}")


def _perceive(cap: Any) -> Any:
    from freesail.world.brains import perceive_vessel
    from freesail.world.captains import Perception

    vessel = getattr(cap, "vessel", None)
    if vessel is not None:
        return perceive_vessel(cap.world, vessel, cap)
    return Perception.read(cap.world)


def _say(cap: Any, tick: int, text: str) -> None:
    vessel = getattr(cap, "vessel", None)
    if vessel is not None and getattr(vessel, "crew", None) is None:
        _story(vessel, tick, text)
        return
    from freesail.world.captains import actor_for

    cap.world.record(
        Severity.NOTABLE,
        "captain.signal",
        f"{cap.name}: {text}",
        actor=actor_for(getattr(cap, "state", None) or "on passage"),
    )


def _succession(cap: Any, locker: S.Locker, tick: int, near: bool) -> None:
    """The signals to be performed in succession: each when the ship before her has."""
    pending = locker.challenges.get("__succession__")
    if not pending:
        return
    root = _root_world(cap)
    own = _own_id(cap)
    for key, item in list(pending.items()):
        h = item["hoist"]
        rank, prev = S.succession_rank(list(root.vessels.vessels), own, str(item["sender"]))
        if S.predecessor_done(prev, key, tick):
            del pending[key]
            _obey(cap, locker, h, str(item["sender"]), tick, near)


# ---------------------------------------------------------------------------
# The private signal
# ---------------------------------------------------------------------------


def _answer_challenge(
    cap: Any, locker: S.Locker, h: S.Hoist, sender: str, tick: int, near: bool
) -> None:
    """A private signal made to us (or to all within sight): answered from the table when
    we hold one; a privateer whose doctrine bluffs hoists a wrong reply; a merchant shows
    nothing."""
    own = _own_id(cap)
    if h.key in locker.answered:
        return
    locker.answered.add(h.key)
    table = _table(cap)
    books = _books(cap)
    light = _light(cap)
    if table is not None:
        if near:
            try:
                cap.give("answer the private signal", why="the challenge made to us")
            except Exception:  # noqa: BLE001
                pass
            return
        S.make_private(locker, books, table, light, own, tick, reply=True, to=sender)
        return
    d = getattr(cap, "doctrine", None)
    bluff = bool(d.threshold("bluff_private_signal", False)) if d is not None else False
    if not bluff:
        return
    root = _root_world(cap)
    now = root.clock.ship_time
    wrong = S.wrong_reply(books, _own_nation(cap), now.year, now.month, S.root_seed(root), light)
    if near:
        # the near body's bluff is a hoist by the same hands, with the wrong words
        from freesail.orders.signals import _start_hoist

        hoist = S.make_private(
            locker,
            books,
            S.PrivateTable(_own_nation(cap), now.year, now.month, "", wrong, "", wrong),
            light,
            own,
            tick,
            reply=True,
            to=sender,
        )
        try:
            _start_hoist(cap.world, locker, hoist, 1, "a reply to the private signal, a guess")
        except Exception:  # noqa: BLE001
            pass
        _say(cap, tick, "The private signal answered with a guess: a flag we hope will pass.")
        return
    S.make_private(
        locker,
        books,
        S.PrivateTable(_own_nation(cap), now.year, now.month, "", wrong, "", wrong),
        light,
        own,
        tick,
        reply=True,
        to=sender,
    )
    _story(cap.vessel, tick, "answered the private signal with a guess")


def _challenge_strangers(cap: Any, locker: S.Locker, p: Any, tick: int, near: bool) -> None:
    """A King's captain makes the private signal to every strange sail within the flags'
    range by day and the lights' by night, once each; not in fog, not in action."""
    table = _table(cap)
    if not CHALLENGES or table is None or getattr(cap, "state", None) not in CHALLENGE_STATES:
        return
    light = _light(cap)
    if light == "fog":
        return
    books = _books(cap)
    reach_m = (
        books.read_nm * books.glass_factor if light == "day" else S.LIGHT_SEEN_NM
    ) * units.NAUTICAL_MILE
    own = _own_id(cap)
    for s in p.strangers:
        sid = str(s.get("id") or "")
        est = s.get("estimate_m")
        if not sid or est is None or float(est) > reach_m or sid == own:
            continue
        if sid in locker.challenges or s.get("spoken") or cap._spoken(s):
            continue
        body = _body_of(cap, sid)
        if body is not None and str(getattr(body, "under_orders_of", "") or "") == own:
            continue  # a ship under his own orders is no stranger to challenge
        if light == "day" and int(s.get("made_out") or 0) < 2:
            continue  # her colours not yet to be made out: her flags are no nearer
        if verdict_of(cap, sid) is not None:
            continue
        locker.challenges[sid] = {"tick": tick, "verdict": None}
        if near:
            name = getattr(body, "name", "") if body is not None else ""
            try:
                cap.give(
                    f"show the private signal to {name}" if name else "show the private signal",
                    why="a strange sail within signal distance",
                )
            except Exception:  # noqa: BLE001
                locker.challenges.pop(sid, None)
            return  # one challenge a minute: the halyards are one set
        S.make_private(locker, books, table, light, own, tick, reply=False, to=sid)
        _story(
            cap.vessel,
            tick,
            f"made the private signal to {str(s.get('known') or 'a sail').split(',')[0]}",
        )
        return


def _judge_challenges(cap: Any, locker: S.Locker, p: Any, tick: int) -> None:
    """Each challenge awaiting its answer: the reply hoist flying from that ship judged
    against the table, or none after the wait; the stranger recognised by the verdict."""
    table = _table(cap)
    if table is None:
        return
    books = _books(cap)
    light = _light(cap)
    own = _own_id(cap)
    nations = _nations(cap)
    own_nation = _own_nation(cap)
    for sid, c in list(locker.challenges.items()):
        if sid == "__succession__" or c.get("verdict"):
            continue
        body = _body_of(cap, sid)
        if body is None:
            continue
        mine = next((h for h in reversed(locker.made) if h.book == "private" and h.to == sid), None)
        if mine is not None:
            if mine.breaks_out >= S.NOT_YET:
                continue  # the challenge not yet run up (the hands at other work)
            c["tick"] = max(
                int(c["tick"]), int(mine.breaks_out)
            )  # the wait from the flags' breaking out
        other = getattr(body, "signals", None)
        reply = None
        if other is not None:
            for h in other.flying_now(tick):
                if (
                    h.book == "reply"
                    and (h.to is None or h.to == own)
                    and h.breaks_out >= int(c["tick"])
                ):
                    reply = h
                    break
        verdict = S.judge_private(locker, table, light, sid, reply, tick, books.answer_wait_s)
        if verdict is None:
            continue
        shown = body.nation_shown if hasattr(body, "nation_shown") else None
        enemy = None
        if verdict == "right":
            enemy = False
            recognise(cap, sid, own_nation, "the private signal", False)
            ids = getattr(cap, "spoken_ids", None)
            if isinstance(ids, set):
                ids.add(sid)
        else:
            known_words = str(
                next((s.get("known") for s in p.strangers if s.get("id") == sid), "") or ""
            )
            warlike = _man_of_war_words(known_words)
            if verdict == "wrong":
                enemy = True  # a reply, and the wrong one: she tried to pass for one of ours
            elif shown == own_nation:
                # our own colours and no answer: a man of war under false colours; a trader's
                # rig never had the table and is a stranger to be spoken
                enemy = True if warlike else None
            elif shown is not None and nations is not None and nations.at_war(shown, own_nation):
                enemy = True
            elif shown is None:
                enemy = True if warlike else None  # no colours and no answer: a man of war's rig
            else:
                enemy = None  # a neutral's colours: a stranger still, to be spoken
            if enemy is not None:
                how = "answered wrong" if verdict == "wrong" else "unanswered"
                recognise(cap, sid, shown, f"the private signal {how}", enemy)
        who = str(
            next((s.get("known") for s in p.strangers if s.get("id") == sid), "") or "the stranger"
        ).split(",")[0]
        who = (
            f"the {who.removeprefix('a ').removeprefix('an ')}"
            if not who.startswith("the ")
            else who
        )
        head = f"{_cap(who)} "
        if verdict == "right":
            text = head + "answers the private signal rightly: one of ours."
        elif verdict == "wrong":
            text = (
                head + "answers the private signal wrong: a stranger under false colours, an enemy."
            )
        elif enemy and shown == own_nation:
            text = head + (
                "makes no answer to the private signal: a man of war under false colours, an enemy."
            )
        elif enemy:
            text = head + "makes no answer to the private signal: an enemy."
        elif shown == own_nation:
            text = head + (
                "makes no answer to the private signal: a merchantman, who has none; a stranger to "
                "be spoken."
            )
        else:
            text = head + "makes no answer to the private signal: a stranger, to be spoken."
        _record(
            cap,
            tick,
            "signal.private_judged",
            text,
            {"id": sid, "verdict": verdict, "enemy": enemy},
        )


def _man_of_war_words(known: str) -> bool:
    """Whether the lookout's words make her a man of war (a frigate, a sloop of war, a
    revenue cutter); a plain 'cutter' or 'brig' is neither, which is honest."""
    from freesail.world.captains import MAN_OF_WAR_WORDS

    low = known.lower()
    return any(w in low for w in MAN_OF_WAR_WORDS)


def _record(cap: Any, tick: int, kind: str, text: str, data: dict[str, Any]) -> None:
    vessel = getattr(cap, "vessel", None)
    crew = getattr(vessel, "crew", None) if vessel is not None else None
    if vessel is not None and (crew is None or getattr(crew, "shape", "") != "full"):
        _story(vessel, tick, text.rstrip("."))
        return
    cap.world.record(
        Severity.URGENT if data.get("enemy") else Severity.NOTABLE, kind, text, data=data
    )


# ---------------------------------------------------------------------------
# The colours by doctrine
# ---------------------------------------------------------------------------


def _colours_by_doctrine(cap: Any, locker: S.Locker, p: Any, tick: int, near: bool) -> None:
    """A privateer whose doctrine sails under false colours hoists the principal enemy's
    when she has a stranger in hand and shows her own at the doctrine's range; any
    captain in action shows his true colours before his first shot (`_engage_now`)."""
    d = getattr(cap, "doctrine", None)
    if not DOCTRINE_COLOURS or d is None or not bool(d.threshold("false_colours", False)):
        return
    state = getattr(cap, "state", None)
    c = locker.colours
    own_nation = _own_nation(cap)
    nations = _nations(cap)
    if (
        state in ("investigating a stranger", "chasing")
        and c.state == "shown"
        and c.nation == own_nation
    ):
        enemies = nations.enemies_of(own_nation) if nations is not None else []
        if not enemies:
            return
        if near:
            try:
                cap.give("hoist false colours", why="the ruse, until the first shot")
            except Exception:  # noqa: BLE001
                pass
        else:
            S.set_colours(c, nations, "false", enemies[0], tick)
            _story(cap.vessel, tick, f"hoisted false colours, {c.words(nations)}")
        return
    if c.state != "false":
        return
    cables = float(d.threshold("true_colours_cables", 4.0))
    mark = cap._stranger if state in ("chasing", "investigating a stranger") else None
    if mark is None and state == "engaging":
        mark = next((s.get("id") for s in p.strangers), None)
    if state in ("engaging",) or (
        mark is not None
        and any(
            s.get("id") == mark
            and s.get("estimate_m") is not None
            and float(s["estimate_m"]) <= cables * units.CABLE
            for s in p.strangers
        )
    ):
        if near:
            try:
                cap.give("hoist the colours", why="her true colours at the doctrine's range")
            except Exception:  # noqa: BLE001
                pass
        else:
            S.set_colours(c, nations, "shown", own_nation, tick)
            _story(cap.vessel, tick, f"hoisted her true colours, {c.words(nations)}")


def _cap(words: str) -> str:
    return words[:1].upper() + words[1:]


# ---------------------------------------------------------------------------
# The fog signals kept
# ---------------------------------------------------------------------------

# A rules captain keeps the fog signals only while another sail has been in sight within
# this long (there is somebody to hear them; and a single ship's recorded passage in thick
# weather, with no other sail in it, does not move: the head rules).
FOG_SIGNALS_COMPANY_S = 3600


def fog_signals_minute(cap: Any, p: Any, near: bool) -> None:
    locker = _locker(cap)
    light = _light(cap)
    tick = int(cap.world.clock.tick)
    if p.strangers:
        cap._business["sail_seen_tick"] = tick
    company = tick - int(cap._business.get("sail_seen_tick", -(10**9))) <= FOG_SIGNALS_COMPANY_S
    if light == "fog" and company and not locker.fog_signals:
        if near:
            try:
                cap.give("keep the fog signals", why="thick weather, with a sail about")
            except Exception:  # noqa: BLE001
                pass
        else:
            locker.fog_signals, locker.fog_since = True, tick
    elif light != "fog" and locker.fog_signals:
        if near:
            try:
                cap.give("cease the fog signals", why="the weather clear")
            except Exception:  # noqa: BLE001
                pass
        else:
            locker.fog_signals, locker.fog_since = False, None


# ---------------------------------------------------------------------------
# A vessel under orders with no brain of her own
# ---------------------------------------------------------------------------


class _Reader:
    """The least captain: what a far vessel with no intent (and so no brain) needs to
    read and obey the signals of the ship she is under the orders of (a convoy's
    merchantman given only `in company with the ship`): no doctrine, no state, no
    private table, the far body's few orders performed on her plan."""

    doctrine = None
    state = "on passage"
    role = "merchant"

    def __init__(self, world: Any, vessel: Any) -> None:
        self.world = world
        self.vessel = vessel
        self._business: dict[str, Any] = {}
        self.recognised: dict[str, dict[str, Any]] = {}
        self.pirates: set[str] = set()
        self.spoken_ids: set[str] = set()
        self._stranger = None

    def _spoken(self, s: dict[str, Any]) -> bool:
        return str(s.get("id") or "") in self.spoken_ids

    def _nearest_stranger(self, p: Any) -> dict[str, Any] | None:
        return p.strangers[0] if p.strangers else None

    def _enter(self, state: str) -> None:
        self.state = state


def brainless_minute(world: Any) -> None:
    """Once a minute, for every far vessel under another's orders with no brain: her
    signals read and obeyed (`far_minute` on the least captain)."""
    from freesail.world.brains import perceive_vessel

    sea = getattr(world, "vessels", None)
    for v in list(getattr(sea, "vessels", []) or []):
        if v.brain is not None or not getattr(v, "under_orders_of", "") or v.done:
            continue
        reader = getattr(v, "_signal_reader", None)
        if reader is None:
            reader = v._signal_reader = _Reader(world, v)
        p = perceive_vessel(world, v, None)
        far_minute(reader, p)
