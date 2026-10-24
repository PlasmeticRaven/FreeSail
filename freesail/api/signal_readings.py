"""The colours', the signals', the private signal's and the lights' readings and events
(spec M7 §1 to §5; package 71), registered in the readings registry from this module,
which `readings` imports at its end after the action's.

    the colours         the ship's own: 'British colours, the red ensign' (shown), 'false:
                        French colours', 'none', 'struck', 'the ensign union down'
    the signals         the hoists flying and the signals read this glass, with their
                        meanings where the book is ours, and who answered
    the private signal  this month's challenge and reply (or 'none aboard'), and the last
                        exchange's verdict
    the lights          what she shows by night: 'none', 'a stern lantern', 'the top lights'

The events, for `at` and a stand-by: `her colours change`, `she hoists her colours`, `she
hauls down her colours` (`colours.changed` seen on another ship), `our colours changed`, `a
signal made` (`signal.made`), `a signal seen`, `a signal read`, `a signal answered`, `the
private signal made` (to us), `the private signal answered`, `the private signal right`,
`the private signal wrong` (`signal.private_judged`), `hailed` (`hail.heard`), `a hail
answered` (`hail.answered`), `a light seen` (the lookout's sighting of a light), `a gun
heard` (a fog signal read).
"""

from __future__ import annotations

from typing import Any

from freesail.api import readings as R

__all__ = ["register"]


def _locker(world: Any) -> Any:
    ship = getattr(world, "ship", None)
    if ship is None or not hasattr(ship, "extra"):
        return None
    from freesail.world.signals import player_locker

    return player_locker(world)


def _colours(world: Any, _: str | None) -> dict[str, Any] | None:
    locker = _locker(world)
    if locker is None:
        return None
    c = locker.colours
    struck = bool((getattr(world.ship, "extra", None) or {}).get("struck")) or c.state == "struck"
    nations = getattr(world, "nations", None)
    if struck:
        words = "struck"
    elif c.state == "none":
        words = "none"
    elif c.state == "false":
        words = f"false: {c.words(nations)}"
    elif c.state == "distress":
        words = c.words(nations)
    else:
        words = c.words(nations)
    return {
        "words": words,
        "state": "struck" if struck else c.state,
        "nation": c.nation,
        "struck": struck,
        "false": c.state == "false",
    }


def _signals(world: Any, _: str | None) -> dict[str, Any] | None:
    locker = _locker(world)
    if locker is None:
        return None
    tick = int(world.clock.tick)
    flying = locker.flying_now(tick)
    bits: list[str] = []
    for h in flying:
        said = h.words()
        if h.answered_by:
            said += f" (answered by {', '.join(sorted(h.answered_by))})"
        bits.append(f"flying: {said}")
    recent = [e for e in locker.log if tick - int(e["tick"]) <= 1800]
    for e in recent[-6:]:
        bits.append(str(e["words"]).rstrip("."))
    return {
        "words": "; ".join(bits) if bits else "none",
        "flying": [h.to_dict() for h in flying],
        "read": [
            {"tick": e["tick"], "by": e["by"], "kind": e["kind"], "meaning": e["meaning"]}
            for e in recent
        ],
    }


def _private(world: Any, _: str | None) -> dict[str, Any] | None:
    locker = _locker(world)
    if locker is None:
        return None
    from freesail.world.signals import table_of

    table = table_of(world)
    if table is None:
        return {"words": "none aboard", "aboard": False, "lines": []}
    verdicts = {k: v.get("verdict") for k, v in locker.challenges.items() if v.get("verdict")}
    words = f"by day, {table.day_challenge}; the reply, {table.day_reply}"
    if verdicts:
        last = list(verdicts.items())[-1]
        words += f"; the last challenged ({last[0]}) answered {last[1]}"
    return {"words": words, "aboard": True, "lines": table.lines(), "verdicts": verdicts}


def _lights(world: Any, _: str | None) -> dict[str, Any] | None:
    locker = _locker(world)
    if locker is None:
        return None
    lights = locker.lights or "none"
    words = {
        "none": "none",
        "stern lantern": "a stern lantern",
        "top lights": "the top lights",
    }.get(lights, lights)
    return {"words": words, "lights": lights}


def register() -> None:
    R.REGISTRY.add(
        R.Reading(
            "colours",
            ("the colours", "our colours", "the ensign"),
            "state",
            "",
            _colours,
            description="the ship's own colours: shown and whose, false (another nation's), "
            "none, struck, or the ensign union down",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "signals",
            ("the signals", "the signal", "the flags"),
            "state",
            "",
            _signals,
            description="the hoists flying and the signals seen and read this glass, with "
            "their meanings where the book is ours; 'none'",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "private_signal",
            ("the private signal", "the private signals", "the recognition signal"),
            "state",
            "",
            _private,
            description="this month's private signal, the challenge and the reply by day, and "
            "the last stranger's answer; 'none aboard' in a ship that carries no table",
        )
    )
    R.REGISTRY.add(
        R.Reading(
            "lights",
            ("the lights", "our lights", "the lanterns"),
            "state",
            "",
            _lights,
            description="the lights she shows by night: none, a stern lantern, the top lights",
        )
    )
    ev = R.EventSpec
    for spec in (
        ev("her colours change", "colours.changed", lambda d: not d.get("own")),
        ev(
            "she hoists her colours",
            "colours.changed",
            lambda d: not d.get("own") and d.get("state") in ("shown", "false"),
        ),
        ev(
            "she hauls down her colours",
            "colours.changed",
            lambda d: not d.get("own") and d.get("state") == "none",
        ),
        ev("our colours changed", "colours.changed", lambda d: bool(d.get("own"))),
        ev("a signal made", "signal.made"),
        ev("a signal seen", "signal.seen"),
        ev("a signal read", "signal.read"),
        ev("a signal answered", "signal.answered"),
        ev("the private signal made", "signal.private"),
        ev("the private signal answered", "signal.private_judged"),
        ev(
            "the private signal right",
            "signal.private_judged",
            lambda d: d.get("verdict") == "right",
        ),
        ev(
            "the private signal wrong",
            "signal.private_judged",
            lambda d: d.get("verdict") in ("wrong", "none"),
        ),
        ev("hailed", "hail.heard"),
        ev("a hail", "hail.heard"),
        ev("a hail answered", "hail.answered"),
        ev("a light seen", "lookout.sighting", lambda d: d.get("seen_as") == "light"),
        ev("a gun heard", "signal.read", lambda d: (d.get("hoist") or {}).get("book") == "fog"),
        ev("a sail spoken", "hail.exchange"),
    ):
        R.EVENTS[spec.words] = spec
