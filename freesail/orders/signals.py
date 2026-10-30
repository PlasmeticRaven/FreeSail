"""The orders of the colours, the signals, the private signal, the lights and the hail
(spec M7 §1 to §5; package 71; `docs/design/Design-Signals.md`).

    hoist the colours               her own colours shown (the ensign and the jack)
    hoist French colours            another nation's: false colours, the ruse the law allowed
    hoist false colours             until the first shot (the principal enemy's when none named)
    haul down the colours           none shown; under fire it is the strike, and says so
    hoist the ensign union down     the signal of distress (with `fire a gun to leeward`, 70's)
    strike the colours              70's, kept in the gunnery; the state is written here
    show the private signal         the month's challenge, to the stranger in hand or named
    answer the private signal       the month's reply (refused in words with no table aboard)
    make the signal to tack         a signal of the book by its meaning: the numerary by day,
    make the signal: enemy in       the night book by night, the fog book's gun in fog; the
      sight bearing NW              qualifiers read from the words; `No. 16` by number
    make the telegraphic signal:    Popham's free sentence, a hoist a word (a well-built book
      England expects ...           with a dictionary; refused in words otherwise)
    answer the signal               the answering pendant to the last signal read
    repeat the signal               the last signal read, made again (the repeating ship)
    haul down the signal            the hoists flying come down
    hoist the lights                a stern lantern (or `hoist the top lights`) by night
    show no lights                  darken ship
    keep the fog signals            the bell at anchor, the gun or the drum under way, in fog
    cease the fog signals
    hail her / hail the brig        the speaking trumpet within hail: the standard hail, or
    hail the Nancy: what ship is    the words given, answered by her body (`world.hail`);
    hail the brig what ship is that the colon optional, the sail told from the words
      that?
    say to the brig: heave to

The making of a signal is an evolution (`data/evolutions/make_signal.yaml`: three hands at
the halyards, a minute a hoist); the hoist breaks out on the ship's body where every
lookout sees it. The orders are recognised by their words before the vocabulary
(`recognises`), because the signal's meaning and the hail's words are free text.
"""

from __future__ import annotations

import re
from typing import Any

from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["SIGNAL_VERBS", "execute", "handle", "read", "recognises"]

Result = tuple[str, str, dict[str, Any]]

SIGNAL_VERBS: tuple[str, ...] = (
    "hoist the colours",
    "hoist false colours",
    "haul down the colours",
    "hoist the ensign union down",
    "show the private signal",
    "answer the private signal",
    "make the signal",
    "make the telegraphic signal",
    "answer the signal",
    "repeat the signal",
    "haul down the signal",
    "hoist the lights",
    "show no lights",
    "keep the fog signals",
    "cease the fog signals",
    "hail",
)

_FORMS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "hoist the colours",
        re.compile(
            r"^(?:hoist|show|run up|set|wear)\s+(?:our|the|her|your)?\s*(?:own\s+|true\s+)?"
            r"(?:colours|colors|ensign|flag)(?:\s+(?:again|up))?$"
        ),
    ),
    (
        "hoist false colours",
        re.compile(
            r"^(?:hoist|show|run up|wear)\s+(?:the\s+|a\s+)?(?P<nation>false|the enemy's|enemy|"
            r"[a-z-]+(?:\s+[a-z-]+)?)\s+(?:colours|colors|ensign|flag)$"
        ),
    ),
    (
        "haul down the colours",
        re.compile(
            r"^(?:haul down|lower|take in|douse)\s+(?:the|our)\s+(?:colours|colors|ensign|flag)$"
        ),
    ),
    (
        "hoist the ensign union down",
        re.compile(
            r"^(?:hoist|show|make)\s+(?:the\s+)?(?:ensign union down|signal of distress|"
            r"a signal of distress|the signal of distress|distress signal|union down)$"
        ),
    ),
    (
        "show the private signal",
        re.compile(
            r"^(?:show|make|hoist)\s+(?:the|our|her)\s+private signal(?:\s+to\s+(?P<to>.+))?$"
        ),
    ),
    (
        "answer the private signal",
        re.compile(r"^(?:answer|reply to)\s+(?:the|her|their)\s+private signal$"),
    ),
    (
        "make the telegraphic signal",
        re.compile(
            r"^(?:make|hoist)\s+(?:the\s+)?telegraphic signal(?:\s*[:,]\s*|\s+)(?P<words>.+)$",
            re.IGNORECASE,
        ),
    ),
    (
        "make the signal",
        re.compile(
            r"^(?:make|hoist)\s+(?:the|a)\s+(?:(?P<book>night|fog|convoy)\s+)?signal"
            r"(?:\s*[:,]\s*|\s+)(?P<words>.+)$",
            re.IGNORECASE,
        ),
    ),
    (
        "answer the signal",
        re.compile(
            r"^(?:answer|acknowledge)\s+(?:the|her|it|his|their)?\s*(?:signal|it)?$|"
            r"^hoist the answering (?:pennant|pendant)$"
        ),
    ),
    (
        "repeat the signal",
        re.compile(r"^repeat\s+(?:the|her|his|it|that)\s*(?:signal)?$|^repeat it$"),
    ),
    (
        "haul down the signal",
        re.compile(
            r"^(?:haul|take)\s+(?:it\s+)?down(?:\s+the\s+signals?)?$|^haul down the signals?$"
        ),
    ),
    (
        "hoist the lights",
        re.compile(
            r"^(?:hoist|show|light|burn)\s+(?:the|a|our)?\s*(?P<which>stern lantern|stern light|"
            r"top lights|toplights|lights|lanterns|poop lantern|a light)$"
        ),
    ),
    (
        "show no lights",
        re.compile(r"^(?:show no lights|douse (?:the|all) lights|no lights|darken ship)$"),
    ),
    (
        "keep the fog signals",
        re.compile(
            r"^(?:keep|make|begin)\s+(?:the\s+)?fog signals?$|^ring the bell$|"
            r"^(?:keep the bell going|fire the fog gun|fire the fog guns)$"
        ),
    ),
    (
        "cease the fog signals",
        re.compile(r"^(?:cease|stop|belay)\s+(?:the\s+)?(?:fog signals?|bell)$"),
    ),
)
# The addressee of a hail: 'her', a name, or 'the <sail>'; the words after a colon or a
# comma, or after a space with no colon (the colon optional: 'hail the brig what ship is
# that'), the sail's words then told from the words said by `hail_parts`.
_HAIL = re.compile(r"^hail\s+(?P<rest>(?:her|him|them|the\s|[A-Z]).*)$")
_SAY_TO = re.compile(r"^say to\s+(?P<rest>(?:her|him|them|the\s|[A-Z]).*)$")
# The words after 'the' that address the deck or a station, never a sail: a hail of these
# is the lookout's hail of the deck or a station sentence (`orders.stations`).
_NOT_A_SAIL = ("deck", "masthead", "lookout", "watcher", "master", "captain", "officer", "boat")
_SAIL_WORDS = (
    "her",
    "him",
    "them",
    "stranger",
    "sail",
    "chase",
    "enemy",
    "brig",
    "cutter",
    "frigate",
    "ship",
    "schooner",
    "lugger",
    "smack",
    "sloop",
    "privateer",
    "merchantman",
    "vessel",
    "boat",
    "stranger's",
)


def _norm(text: str) -> str:
    s = " ".join(str(text).split()).strip().rstrip(".!")
    s = s.replace("’", "'")
    return s


def recognises(text: str, ship: Any = None) -> str | None:
    """The signal order the words are (its canonical verb), or None. A hail is
    recognised only when it names a sail (else it is the lookout's hail of the deck)."""
    s = _norm(text)
    low = s.lower()
    for verb, pat in _FORMS:
        if pat.match(low if verb not in ("make the signal", "make the telegraphic signal") else s):
            if verb == "hoist false colours" and not _nation_words(
                ship, pat.match(low).group("nation")
            ):
                continue
            return verb
    m = _HAIL.match(s) or _SAY_TO.match(s)
    if m is not None and hail_parts(ship, m) is not None:
        return "hail"
    return None


def hail_parts(ship: Any, m: re.Match[str]) -> tuple[str, str] | None:
    """(the sail's words, the words to say) from a hail's or a 'say to' match, or None
    when the line hails no sail (the lookout's 'hail sail ho', 'say to the watcher').
    With a colon or a comma the sail is what stands before the first of them, when that
    names a sail ('hail the brig: what ship is that?', 'say to her, heave to'); without
    one, or when it does not, the sail is the shortest head of the line that names a sail
    in sight ('the brig', 'the fore topsail schooner', 'her') and the rest is said to her
    ('hail the brig what ship is that', 'say to the Nancy heave to, I am sending a
    boat'). A name without 'the' ('hail Nancy what ship is that') is a sail only when a
    sail of that name is on the sea, so that the lookout's 'hail Sail ho' stays his."""
    rest = m.group("rest").strip()
    cut = re.match(r"^(?P<who>[^:,]+?)\s*[:,]\s*(?P<words>.*)$", rest)
    if cut is not None and _names_a_sail(ship, cut.group("who")):
        return cut.group("who"), cut.group("words")
    tokens = rest.split()
    low = tokens[0].lower()
    if low in ("her", "him", "them"):
        return tokens[0], " ".join(tokens[1:]).strip(" ,:")
    if low != "the":
        name = tokens[0].rstrip(",:")
        return (name, " ".join(tokens[1:]).strip(" ,:")) if _found_on_the_sea(ship, name) else None
    for n in range(2, len(tokens) + 1):
        head = " ".join(tokens[:n]).rstrip(",:")
        if _names_a_sail(ship, head):
            return head, " ".join(tokens[n:]).strip(" ,:")
    return None


def _found_on_the_sea(ship: Any, name: str) -> bool:
    world = world_of(ship) if ship is not None else None
    sea = getattr(world, "vessels", None) if world is not None else None
    if sea is None:
        return False
    try:
        return sea.find(name.strip()) is not None
    except Exception:  # noqa: BLE001 - a view with no finder
        return False


def _names_a_sail(ship: Any, who: str) -> bool:
    w = " ".join(str(who or "").lower().split())
    if w.startswith("the "):
        w = w[4:]
    if w.split(" ")[0] in _NOT_A_SAIL:
        return False
    if w.split()[-1] in _SAIL_WORDS or w in _SAIL_WORDS:
        return True
    world = world_of(ship) if ship is not None else None
    sea = getattr(world, "vessels", None) if world is not None else None
    if sea is not None:
        try:
            if sea.find(who.strip()) is not None:
                return True
        except Exception:  # noqa: BLE001 - a view with no finder
            pass
    return False


def _nation_words(ship: Any, words: str) -> str | None:
    """The nation id the words name ('french', 'the enemy's'), or None."""
    w = " ".join(str(words or "").lower().split())
    if w in ("false", "the enemy's", "enemy", "enemys"):
        return "enemy"
    world = world_of(ship) if ship is not None else None
    nations = getattr(world, "nations", None) if world is not None else None
    if nations is None:
        from freesail.world.nations import load_nations

        nations = load_nations()
    found = nations.find(w)
    if found is None and w.endswith("'s"):
        found = nations.find(w[:-2])
    return found.id if found is not None else None


def read(ship: Any, text: str) -> Order:
    """The order read whole (a standing order's action at give time): the verb and the
    words after it, nothing done."""
    verb = recognises(text, ship)
    if verb is None:
        raise OrderError(f"'{text}' is no signal order.")
    s = _norm(text)
    return Order(text=s.lower(), verb=verb, verb_phrase=verb, object=s)


def handle(ship: Any, text: str) -> Result:
    """Carry out a signal order from its words."""
    verb = recognises(text, ship)
    if verb is None:
        raise OrderError(f"'{text}' is no signal order.")
    return execute(
        ship, Order(text=_norm(text).lower(), verb=verb, verb_phrase=verb, object=_norm(text))
    )


def execute(ship: Any, order: Order) -> Result:
    from freesail.world import signals as S

    world = world_of(ship)
    if world is None:
        raise OrderError("She sails alone, with no other sail to see a flag: no world.")
    verb = order.verb
    raw = str(order.object or order.text)
    low = raw.lower()
    locker = S.player_locker(world)
    tick = int(world.clock.tick)
    nations = getattr(world, "nations", None)
    if verb == "hoist the colours":
        return _hoist_own(world, locker, tick)
    if verb == "hoist false colours":
        m = _FORMS[1][1].match(low)
        return _hoist_false(world, locker, tick, m.group("nation") if m else "false")
    if verb == "haul down the colours":
        return _haul_down_colours(world, locker, tick)
    if verb == "hoist the ensign union down":
        if locker.colours.state == "struck":
            raise OrderError("The colours are struck; nothing flies to turn union down.")
        S.set_colours(locker.colours, nations, "distress", S.own_nation(world), tick)
        text = (
            "The ensign hoisted union down: the signal of distress to every ship in sight "
            "(a gun to leeward with it is the custom: 'fire a gun to leeward')."
        )
        return (
            "colours.changed",
            text,
            {"verb": verb, "level": 1, "state": "distress", "own": True, "notable": True},
        )
    if verb == "show the private signal":
        m = _FORMS[4][1].match(low)
        return _private(world, locker, tick, reply=False, to_words=m.group("to") if m else None)
    if verb == "answer the private signal":
        return _private(world, locker, tick, reply=True)
    if verb == "make the telegraphic signal":
        m = _FORMS[6][1].match(raw)
        return _telegraphic(world, locker, tick, m.group("words") if m else "")
    if verb == "make the signal":
        m = _FORMS[7][1].match(raw)
        book = (m.group("book") or "").lower() if m else ""
        return _make(world, locker, tick, m.group("words") if m else raw, book)
    if verb == "answer the signal":
        return _answer(world, locker, tick)
    if verb == "repeat the signal":
        return _repeat(world, locker, tick)
    if verb == "haul down the signal":
        down = locker.haul_down(tick)
        if not down:
            raise OrderError("No signal is flying to haul down.")
        text = "The signal hauled down: " + "; ".join(h.words() for h in down) + "."
        return "signal.down", text, {"verb": verb, "level": 1}
    if verb == "hoist the lights":
        m = _FORMS[10][1].match(low)
        which = (m.group("which") if m else "lights") or "lights"
        kind = "top lights" if "top" in which else "stern lantern"
        locker.lights = kind
        text = (
            f"The {kind} hoisted"
            + (" (a stern lantern, as a ship in company shows)" if kind == "stern lantern" else "")
            + "; she may be seen at the range a light carries by night."
        )
        return "lights.changed", text, {"verb": verb, "level": 1, "lights": kind}
    if verb == "show no lights":
        locker.lights = "none"
        text = "No lights shown: the lanterns doused, the ship darkened."
        return "lights.changed", text, {"verb": verb, "level": 1, "lights": "none"}
    if verb == "keep the fog signals":
        return _fog_signals(world, locker, tick, True)
    if verb == "cease the fog signals":
        return _fog_signals(world, locker, tick, False)
    if verb == "hail":
        from freesail.world import hail as H

        m = _HAIL.match(raw) or _SAY_TO.match(raw)
        who, words = hail_parts(ship, m) or (m.group("rest"), "")
        return H.hail_order(world, who, words)
    raise OrderError(f"'{order.text}' is no signal order the ship knows.")


# -- the colours ---------------------------------------------------------------------------


def _sev(name: str) -> Any:
    from freesail.core.events import Severity

    return getattr(Severity, name)


def _hoist_own(world: Any, locker: Any, tick: int) -> Result:
    from freesail.world import signals as S

    own = S.own_nation(world)
    c = locker.colours
    if c.state == "struck":
        raise OrderError(
            "The colours are struck: they are not hoisted again in this game (what follows a "
            "strike is the prize's package)."
        )
    was = c.state
    if was == "shown" and c.nation == own:
        return (
            "colours.changed",
            f"Her own colours are flying already ({c.words(world.nations)}).",
            {
                "verb": "hoist the colours",
                "level": 1,
                "state": "shown",
                "own": True,
                "notable": True,
            },
        )
    S.set_colours(c, world.nations, "shown", own, tick)
    words = c.words(world.nations)
    if was == "false":
        text = f"Her true colours hoisted: {words}, the false ones down."
    elif was == "distress":
        text = f"The ensign hoisted right way up again: {words}."
    else:
        text = f"The colours hoisted: {words}."
    world.record(
        _sev("NOTABLE"),
        "colours.changed",
        text,
        data={"state": "shown", "nation": own, "own": True},
    )
    return (
        "colours.changed",
        text,
        {"verb": "hoist the colours", "level": 1, "state": "shown", "own": True, "notable": True},
    )


def _hoist_false(world: Any, locker: Any, tick: int, nation_words: str) -> Result:
    from freesail.world import signals as S

    own = S.own_nation(world)
    nations = world.nations
    nid = _nation_words(world.ship, nation_words)
    if nid == "enemy":
        enemies = nations.enemies_of(own)
        if not enemies:
            raise OrderError(
                f"{nations.get(own).name} is at war with nobody: say whose colours to show "
                "('hoist Danish colours')."
            )
        nid = enemies[0]
    if nid is None:
        raise OrderError(f"'{nation_words}' names no nation of the table.")
    if nid == own:
        return _hoist_own(world, locker, tick)
    c = locker.colours
    if c.state == "struck":
        raise OrderError("The colours are struck; no flag is hoisted over a strike.")
    S.set_colours(c, nations, "false", nid, tick)
    words = c.words(nations)
    text = (
        f"False colours hoisted: {words}. The ruse is the law's until the first shot; a gun "
        "fired under them makes her a pirate to every nation."
    )
    world.record(
        _sev("NOTABLE"),
        "colours.changed",
        text,
        data={"state": "false", "nation": nid, "own": True},
    )
    return (
        "colours.changed",
        text,
        {"verb": "hoist false colours", "level": 1, "state": "false", "own": True, "notable": True},
    )


def _haul_down_colours(world: Any, locker: Any, tick: int) -> Result:
    from freesail.world import signals as S

    c = locker.colours
    if c.state == "struck":
        return ("action.struck", "The colours are struck already.", {"level": 1})
    if c.state == "none":
        return ("colours.changed", "No colours are flying.", {"level": 1, "state": "none"})
    # under fire, hauling down the colours is the strike by the custom of the sea
    keeper = (getattr(world.ship, "extra", None) or {}).get("damage")
    under_fire = False
    if keeper is not None:
        from freesail.combat.morale import UNDER_FIRE_S

        under_fire = any(tick - t <= UNDER_FIRE_S for t in keeper.struck_by.values())
    if under_fire:
        from freesail.combat.action import strike

        text = strike(world, by_rule=False, words="the colours hauled down under fire")
        return (
            "action.struck",
            text,
            {"verb": "haul down the colours", "level": 1, "by_rule": False},
        )
    S.set_colours(c, world.nations, "none", "", tick)
    text = "The colours hauled down: she shows none."
    return (
        "colours.changed",
        text,
        {
            "verb": "haul down the colours",
            "level": 1,
            "state": "none",
            "own": True,
            "notable": True,
        },
    )


# -- the signals -----------------------------------------------------------------------------


def _start_hoist(world: Any, locker: Any, hoist: Any, hoists: int, words: str) -> str:
    """The evolution that makes it: the hands at the halyards; the hoist breaks out at the
    end of its minute (`MakeSignalScript` sets the tick when the work begins)."""
    from freesail.world import signals as S

    ship = world.ship
    runner = (getattr(ship, "extra", None) or {}).get("evolutions")
    if runner is None:
        return ""
    # the hoist breaks out when the hands run it up, not when it was ordered (a hoist
    # queued behind a wear was read by the other ship before it was up)
    hoist.breaks_out = S.NOT_YET
    hoist.complete_at = None if hoist.complete_at is None else S.NOT_YET
    try:
        return runner.start(
            ship,
            "make_signal",
            None,
            {"hoists": int(hoists), "hoist_key": hoist.key, "words": words},
        )
    except OrderError:
        locker.flying = [h for h in locker.flying if h is not hoist]
        raise


def _make(world: Any, locker: Any, tick: int, words: str, book_said: str) -> Result:
    from freesail.world import signals as S

    books = S.books_for(world)
    light = S.light_now(world)
    book = book_said or S.BOOKS_BY_LIGHT[light]
    if book == "numerary" and _convoy_commodore(world):
        found = books.find(words, "convoy") or books.find(words, "numerary")
    else:
        found = books.find(words, book)
        if found is None and book == "numerary":
            found = books.find(words, "convoy")
    if found is None:
        hint = {
            "numerary": "the book's meanings ('make the signal to chase', 'make the signal: "
            "enemy in sight bearing NW', 'make the signal No. 16')",
            "night": "the night book's few meanings (tack, wear, make sail, shorten sail, "
            "bring to, anchor, chase, the enemy in sight)",
            "fog": "the fog book's few meanings (tack, wear, make sail, shorten sail, bring "
            "to, anchor, the enemy in sight)",
            "convoy": "the convoy instructions' meanings",
        }[book]
        raise OrderError(
            f"'{words}' is no signal of the {books.nation} {book} book; say one of {hint}."
        )
    entry, qualifiers = found
    if (
        "compass" in entry.qualifiers
        and "compass" not in qualifiers
        and "{compass}" in str(entry.does.get("order", ""))
    ):
        raise OrderError(f"'{entry.meaning}' wants a bearing: '{entry.meaning} bearing NW'.")
    to = None
    if qualifiers.get("ship"):
        v = world.vessels.find(str(qualifiers["ship"]))
        to = v.id if v is not None else None
    hoist = S.make_hoist(locker, books, entry, qualifiers, S.own_id(world), tick, to=to)
    if entry.book == "fog":
        # a gun is the signal: the battery fires it when it is ready (the gunnery's), and
        # the flags are not to be seen; the hoist is heard when the gun fires
        hoist.breaks_out = tick + 30
        text = f"In the fog the signal is made by gun: {entry.fire}, {_lower(entry.meaning)}."
        _fire_signal_gun(world)
        return (
            "signal.made",
            text,
            {"verb": "make the signal", "level": 1, "hoist": hoist.to_dict(), "notable": True},
        )
    line = _start_hoist(world, locker, hoist, 1, hoist.words())
    text = (
        f"{line.rstrip('.')} ({hoist.words()}, the {_adjective(world)} {entry.book} book; a "
        "minute to run it up)."
    )
    return "signal.ordered", text, {"verb": "make the signal", "level": 1, "hoist": hoist.to_dict()}


def _convoy_commodore(world: Any) -> bool:
    """Whether this ship has merchantmen under her orders (then her signals to them are
    the convoy book's, which is what they read)."""
    own = _own_id(world)
    sea = getattr(world, "vessels", None)
    for v in getattr(sea, "vessels", []) or []:
        if str(getattr(v, "under_orders_of", "") or "") == own and "merchant" in str(
            getattr(v, "description", "")
        ):
            return True
    return False


def _own_id(world: Any) -> str:
    from freesail.world import signals as S

    return S.own_id(world)


def _telegraphic(world: Any, locker: Any, tick: int, sentence: str) -> Result:
    from freesail.world import signals as S

    books = S.books_for(world)
    light = S.light_now(world)
    if light != "day":
        raise OrderError(
            "The telegraphic signal is flags, and flags are for daylight; by night the night "
            "book's lights, in fog the gun ('make the signal to tack')."
        )
    try:
        hoists = books.encode(sentence)
    except S.BookFileError as e:
        raise OrderError(str(e)[:1].upper() + str(e)[1:] + ".") from None
    if not hoists:
        raise OrderError("Say the words of the telegraphic signal after the colon.")
    hoist = S.Hoist(
        book="telegraphic",
        meaning=sentence.strip(),
        by=S.own_id(world),
        since=tick,
        breaks_out=tick + books.hoist_s,
        numbers=tuple(n for n, _ in hoists),
        root=books.root,
        words_made=[w for _, w in hoists],
        complete_at=tick + books.hoist_s * len(hoists),
    )
    locker.hoist(hoist)
    line = _start_hoist(
        world, locker, hoist, len(hoists), f"the telegraphic signal, {sentence.strip()}"
    )
    minutes = len(hoists) * books.hoist_s // 60
    spelt = [w for n, w in hoists if len(w) == 1]
    text = (
        f"{line.rstrip('.')} ({len(hoists)} hoists, {minutes} minutes, the telegraph flag over "
        "each: "
        + ", ".join(f"{w} {n}" for n, w in hoists)
        + (
            f"; spelt letter by letter where the book has no word: {''.join(spelt)}"
            if spelt
            else ""
        )
        + ")."
    )
    return (
        "signal.ordered",
        text,
        {"verb": "make the telegraphic signal", "level": 1, "hoists": len(hoists)},
    )


def _last_read(locker: Any, kinds: tuple[str, ...] = ("signal.read",)) -> dict[str, Any] | None:
    for entry in reversed(locker.log):
        if entry.get("kind") in kinds:
            return entry
    return None


def _answer(world: Any, locker: Any, tick: int) -> Result:
    from freesail.world import signals as S

    books = S.books_for(world)
    last = _last_read(locker, ("signal.read", "signal.seen"))
    if last is None:
        raise OrderError("No signal has been seen to answer.")
    if last["key"] in locker.answered:
        return ("signal.answered", "That signal is answered already.", {"level": 1})
    locker.answered.add(last["key"])
    hoist = S.make_answer(locker, books, S.own_id(world), tick, str(last["by"]))
    line = _start_hoist(world, locker, hoist, 1, "the answering pendant")
    about = (
        f"the signal read, {_lower(last['hoist'].meaning)}"
        if last.get("kind") == "signal.read"
        else "a signal not of our book"
    )
    text = f"{line.rstrip('.')} (to {about})."
    return "signal.ordered", text, {"verb": "answer the signal", "level": 1, "to": last["by"]}


def _repeat(world: Any, locker: Any, tick: int) -> Result:
    from freesail.world import signals as S

    last = _last_read(locker)
    if last is None:
        raise OrderError("No signal has been read to repeat.")
    h = last["hoist"]
    books = S.books_for(world)
    copy = S.Hoist(
        book=h.book,
        meaning=h.meaning,
        by=S.own_id(world),
        since=tick,
        breaks_out=tick + books.hoist_s,
        numbers=h.numbers,
        shown=h.shown,
        qualifiers=dict(h.qualifiers),
        does=dict(h.does),
        in_succession=h.in_succession,
        root=h.root,
        to=h.to,
    )
    locker.hoist(copy)
    line = _start_hoist(world, locker, copy, 1, copy.words())
    return (
        "signal.ordered",
        f"{line.rstrip('.')} (repeated).",
        {"verb": "repeat the signal", "level": 1},
    )


def _private(
    world: Any, locker: Any, tick: int, reply: bool, to_words: str | None = None
) -> Result:
    from freesail.world import signals as S

    books = S.books_for(world)
    table = S.table_of(world)
    if table is None:
        raise OrderError(
            "There is no private signal aboard: the month's table is issued to the King's ships "
            "under seal, and this ship carries none (a merchantman, a privateer or a prize's "
            "want of it is the tell)."
        )
    light = S.light_now(world)
    to = None
    if not reply:
        if to_words:
            v = world.vessels.find(to_words.strip())
            if v is None:
                raise OrderError(f"Nothing in sight answers to '{to_words}'.")
            to = v.id
        else:
            to = _nearest_stranger_id(world)
        if to is not None:
            locker.challenges[str(to)] = {"tick": tick, "verdict": None}
    else:
        last = _last_read(locker, ("signal.private",))
        if last is None:
            raise OrderError("No private signal has been made to us to answer.")
        to = str(last["by"])
    hoist = S.make_private(locker, books, table, light, S.own_id(world), tick, reply=reply, to=to)
    what = "the private signal's reply" if reply else "the private signal"
    line = _start_hoist(world, locker, hoist, 1, what)
    text = f"{line.rstrip('.')} ({hoist.shown}; the table for {_month_words(world)})."
    return (
        "signal.ordered",
        text,
        {"verb": "answer the private signal" if reply else "show the private signal", "level": 1},
    )


def _nearest_stranger_id(world: Any) -> str | None:
    got = world.readings.value("strangers")
    items = got.get("items") if isinstance(got, dict) else None
    return str(items[0]["id"]) if items else None


def _month_words(world: Any) -> str:
    from freesail.world.signals import _MONTHS

    now = world.clock.ship_time
    return f"{_MONTHS[now.month - 1]} {now.year}"


def _fire_signal_gun(world: Any) -> None:
    """The fog book's gun: the battery fires a gun to leeward when it is ready (70's
    order); a ship without guns beats the drum instead, which the words say."""
    ship = world.ship
    if not getattr(ship, "guns", None):
        return
    try:
        world.submit("fire a gun to leeward", actor="signals", routine=True)
    except Exception:  # noqa: BLE001 - the guns not cast loose: the signal stands by words
        pass


def _fog_signals(world: Any, locker: Any, tick: int, keep: bool) -> Result:
    from freesail.world import signals as S

    books = S.books_for(world)
    if keep and locker.fog_signals:
        return ("fog.signals", "The fog signals are kept already.", {"level": 1})
    if not keep and not locker.fog_signals:
        return ("fog.signals", "No fog signals are being made.", {"level": 1})
    locker.fog_signals = keep
    locker.fog_since = tick if keep else None
    if keep:
        text = (
            "The fog signals kept: the bell rung every two minutes at anchor, a gun every half "
            "hour under way in company and the drum beaten alone, while it is thick "
            f"(the {books.nation} book's custom)."
        )
    else:
        text = "The fog signals ceased."
    return "fog.signals", text, {"verb": "keep the fog signals", "level": 1, "kept": keep}


def _lower(s: str) -> str:
    return s[:1].lower() + s[1:] if s and not s.startswith("No.") else s


def _adjective(world: Any) -> str:
    from freesail.world import signals as S

    try:
        return str(world.nations.get(S.own_nation(world)).adjective)
    except Exception:  # noqa: BLE001
        return S.books_for(world).nation
