"""The verb table (spec §8.2): what each parsed order does to the ship.

Three kinds of verb live here:

- **Level 1 sail and yard verbs** (`set`, `take in`, `furl`, `reef`, `shake
  out`, `brace`) and the **whole-ship evolutions** (`tack ship`, `wear ship`,
  `heave to`, `fill away`) start an evolution through the runner kept in
  `ship.extra["evolutions"]` (package 7). The verb and the sail's class pick
  the evolution id from `vocabulary.yaml` (`set` + `square` = `set_square`).
  A group object starts one evolution per member; if some fail, the rest
  still start and the failures are reported in the log text.
- **Level 0 line verbs** (`haul`, `ease`, `check`, `let go`, `belay`) act on
  the part at once: a brace shifts its yard's angle by five degrees, a sheet
  of a fore-and-aft sail shifts the sail's sheet angle by five degrees, a
  halyard (or any other line) shifts its hoist by a tenth.
- **Helm verbs** (`steer`, `come up`, `bear away`, `keep her full`) set the
  helm targets in `ship.dyn` for the helmsman in the physics to follow.

Each returns `(kind, log_text, data)` for the World to log, or raises
`OrderError` with a sentence saying why the order was not carried out.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.orders import errors, resolve
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.vocabulary import Vocabulary, load_vocabulary
from freesail.ship.graph import Ship
from freesail.ship.parts import HelmMode, Line, LineState, Sail, SailState, Spar

BRACE_STEP = units.deg_to_rad(5.0)  # one haul or ease on a brace
SHEET_STEP = units.deg_to_rad(5.0)  # one haul or ease on a fore-and-aft sheet
HOIST_STEP = 0.1  # one haul or ease on a halyard or any other line
MAX_SHEET_ANGLE = units.deg_to_rad(90.0)
SHIP_SUBJECT = "ship"  # the subject id given to the runner for tack, wear, heave to

Result = tuple[str, str, dict[str, Any]]


def execute(
    ship: Ship, order: Order, vocab: Vocabulary | None = None, skip: frozenset[str] = frozenset()
) -> Result:
    """Carry out a parsed order. Group evolutions are expanded in `orders.handle`, not here.

    `skip` names parts to pass over in silence: the group expander uses it
    so that a sail listed twice ("set the plain sail", then "set the
    staysails") is set once. If nothing is left, NothingToDoError is raised.
    """
    vocab = vocab or load_vocabulary()
    spec = vocab.verbs[order.verb]
    if order.verb == "brace":
        return _brace(ship, order, vocab, skip)
    if order.verb == "trim":
        return _trim(ship, order, vocab, skip)
    if spec.object == "sail":
        return _sail_evolution(ship, order, vocab, skip)
    if spec.object == "line":
        return _line_action(ship, order, vocab)
    if spec.object in ("heading", "points") or order.verb == "keep her full":
        return _helm(ship, order)
    if order.verb in vocab.evolutions and isinstance(vocab.evolutions[order.verb], str):
        return _ship_evolution(ship, order, vocab)
    raise OrderError(f"'{order.verb}' is in the vocabulary but has no meaning yet.")


# ---------------------------------------------------------------------------
# The runner
# ---------------------------------------------------------------------------


def runner_of(ship: Ship) -> Any:
    """The evolution runner (package 7), or a sentence if none is fitted."""
    runner = ship.extra.get("evolutions")
    if runner is None:
        raise OrderError(
            "There is no one to work the ship yet: no evolution runner is fitted "
            "(ship.extra['evolutions'])."
        )
    return runner


def _no_stray_modifiers(order: Order, allowed: set[str]) -> None:
    """Reject modifiers that belong to another verb ('set the topsail sharp up')."""
    stray = [k for k in order.modifiers if k not in allowed and k != "heading_text"]
    if not stray:
        return
    words = {
        "brace_mode": f"'{order.modifiers.get('brace_mode')}' belongs with 'brace'",
        "tack": "'on the ... tack' belongs with 'brace' or 'heave to'",
        "reefs": "a number of reefs belongs with 'reef' or 'shake out'",
        "close": "'close' belongs with 'reef'",
        "fathoms": "fathoms belong with 'haul' or 'ease'",
        "a_little": "'a little' belongs with 'haul' or 'ease'",
        "manner": "'handsomely' and 'roundly' belong with 'haul' or 'ease'",
        "heading": "a heading belongs with 'steer'",
        "points": "a number of points belongs with 'steer', 'come up' or 'bear away'",
        "direction": "a direction belongs with 'steer'",
    }
    reasons = [words.get(k, f"'{k}' does not go with '{order.verb}'") for k in stray]
    raise OrderError(f"'{order.verb}' was understood, but {errors.join_names(reasons, 'and')}.")


# ---------------------------------------------------------------------------
# Level 1: sails
# ---------------------------------------------------------------------------


def _sail_evolution(
    ship: Ship, order: Order, vocab: Vocabulary, skip: frozenset[str] = frozenset()
) -> Result:
    verb = order.verb
    _no_stray_modifiers(order, {"reefs", "close", "manner"})
    res = resolve.resolve(ship, order.object or "", order.side_word, verb)
    mapping: dict[str, str] = vocab.evolutions.get(verb, {})
    params = _sail_params(order)

    sails: list[Sail] = []
    for pid in res.ids:
        part = ship.parts[pid]
        if isinstance(part, Sail):
            if pid not in skip:
                sails.append(part)
            continue
        raise errors.wrong_kind(
            verb,
            resolve.display_name(ship, pid),
            _what(ship, part),
            "sails",
            _sail_hint(ship, part),
        )

    if not sails:
        raise errors.NothingToDoError(f"Every sail of the {res.name} was already ordered.")
    runner = runner_of(ship)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    for sail in sails:
        reason = _sail_check(ship, sail, verb, order, mapping, vocab)
        if reason:
            failed.append(reason)
            failed_ids.append(sail.id)
            continue
        evo = mapping[sail.cls]
        p = dict(params)
        if verb == "shake out" and order.modifiers.get("close"):
            p["reefs"] = sail.reefs
        try:
            texts.append(runner.start(ship, evo, sail.id, p))
        except OrderError as e:
            failed.append(f"{resolve.the(ship, sail.id)}: {e}")
            failed_ids.append(sail.id)
            continue
        started.append({"evolution": evo, "subject": sail.id, "params": p})

    if not started:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, verb, res.name, started, texts, failed)
    data = {
        "verb": verb,
        "level": 1,
        "object": res.name,
        "side": res.side,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    return "evolution.started", text, data


def _sail_params(order: Order) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if order.verb in ("reef", "shake out"):
        params["reefs"] = int(order.modifiers.get("reefs", 1))
        if order.modifiers.get("close"):
            params["close"] = True
    return params


def _sail_check(
    ship: Ship, sail: Sail, verb: str, order: Order, mapping: dict[str, str], vocab: Vocabulary
) -> str | None:
    """A sentence if the verb makes no sense for this sail right now, else None.

    Only what is plain from the part itself is checked here; the runner
    checks the evolution's own preconditions (the yard crossed, the mast
    standing) and refuses with its own sentence.
    """
    name = resolve.the(ship, sail.id)
    if sail.wrecked:
        return f"{name} is wrecked"
    if sail.state is SailState.BLOWN_OUT:
        return f"{name} is blown out; there is no sail to {verb}"
    if sail.cls not in mapping:
        template = vocab.refusals.get(verb, "'{verb}' has no meaning for a {class} sail")
        return template.format(name=name[4:], **{"class": sail.cls, "verb": verb}).rstrip(".")
    if verb == "set" and sail.state is SailState.SET:
        return f"{name} is already set"
    if verb in ("take in", "furl") and sail.state is SailState.FURLED:
        return f"{name} is already furled"
    if verb in ("reef", "shake out") and sail.reef_bands == 0:
        return vocab.refusals[verb].format(name=name[4:]).rstrip(".")
    if verb == "reef":
        n = int(order.modifiers.get("reefs", 1))
        if order.modifiers.get("close"):
            n = sail.reef_bands - sail.reefs
            if n <= 0:
                return f"{name} is already close reefed"
        elif sail.reefs + n > sail.reef_bands:
            left = sail.reef_bands - sail.reefs
            if left == 0:
                return f"{name} is already close reefed ({sail.reef_bands} reefs in)"
            return (
                f"{name} has {sail.reef_bands} reef band{'s' if sail.reef_bands > 1 else ''} "
                f"and {sail.reefs} reef{'s' if sail.reefs != 1 else ''} in; "
                f"only {left} more can be taken"
            )
    if verb == "shake out" and sail.reefs == 0:
        return f"there is no reef in {name} to shake out"
    if verb == "shake out" and not order.modifiers.get("close"):
        n = int(order.modifiers.get("reefs", 1))
        if n > sail.reefs:
            return f"{name} has only {sail.reefs} reef{'s' if sail.reefs > 1 else ''} in"
    return None


def _what(ship: Ship, part: Any) -> str:
    kind = resolve.kind_of(part)
    if isinstance(part, Line):
        return f"a {part.cls.replace('_', ' ')} (a line)" if not part.is_standing else kind
    if isinstance(part, Spar):
        return f"a {kind}"
    return f"a {kind}"


def _sail_hint(ship: Ship, part: Any) -> str:
    """'Did you mean the fore topsail?' for a yard or a line that serves a sail."""
    if isinstance(part, Spar):
        sail = ship.sail_of(part)
        if sail is not None:
            return f"Did you mean {resolve.the(ship, sail.id)}?"
    if isinstance(part, Line) and part.of in ship.parts:
        target = ship.parts[part.of]
        if isinstance(target, Sail):
            return f"Did you mean {resolve.the(ship, target.id)}?"
        if isinstance(target, Spar):
            sail = ship.sail_of(target)
            if sail is not None:
                return f"Did you mean {resolve.the(ship, sail.id)}?"
    return ""


def _summarise(
    ship: Ship,
    verb: str,
    object_name: str,
    started: list[dict[str, Any]],
    texts: list[str],
    failed: list[str],
) -> str:
    """One log line: the runner's own sentences when few, a roll-call when many."""
    if len(started) <= 3:
        body = " ".join(t.strip() for t in texts if t)
    else:
        names = [resolve.display_name(ship, s["subject"]) for s in started]
        body = f"Hands to {verb} the {object_name}: {errors.join_names(names, 'and')}."
        body = body.replace(" and 1 more", " and one more")
    if failed:
        body += " Not done: " + "; ".join(failed) + "."
    return body


# ---------------------------------------------------------------------------
# Level 1: brace
# ---------------------------------------------------------------------------


def _brace(
    ship: Ship, order: Order, vocab: Vocabulary, skip: frozenset[str] = frozenset()
) -> Result:
    _no_stray_modifiers(order, {"brace_mode", "tack", "manner"})
    mode = order.modifiers.get("brace_mode")
    tack = order.modifiers.get("tack")
    if mode is None:
        if tack is None:
            raise OrderError(
                "Brace them how? Say 'sharp up', 'up', 'in' or 'square', "
                "and 'on the starboard tack' or 'on the larboard tack' if it matters."
            )
        mode = "sharp up"
    tack = tack or ship.dyn.tack
    sign = 1.0 if tack == "starboard" else -1.0

    if order.object:
        res = resolve.resolve(ship, order.object, order.side_word, "brace")
        yards = [_yard_for(ship, pid) for pid in res.ids]
        object_name = res.name
    else:
        yards = [s for s in ship.spars.values() if s.is_yard]
        object_name = "yards"
    if yards and all(y.id in skip for y in yards):
        raise errors.NothingToDoError(f"Every yard of the {object_name} was already ordered.")
    yards = [y for y in yards if y.id not in skip]
    if not yards:
        raise OrderError("This ship has no yards to brace.")

    runner = runner_of(ship)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    for yard in yards:
        name = resolve.the(ship, yard.id)
        if yard.wrecked:
            failed.append(f"{name} is carried away")
            failed_ids.append(yard.id)
            continue
        if yard.sent_down:
            failed.append(f"{name} is sent down")
            failed_ids.append(yard.id)
            continue
        target_deg = vocab.brace_modes[mode]
        target = yard.brace_limit if target_deg == "limit" else units.deg_to_rad(float(target_deg))
        target = math.copysign(min(abs(target), yard.brace_limit), sign) if target else 0.0
        params = {
            "target_deg": round(
                units.rad_to_deg(target), 2
            ),  # signed: + = larboard yardarm forward
            "target_angle": target,  # the same in radians
            "mode": mode,
            "tack": tack,
        }
        try:
            texts.append(runner.start(ship, vocab.evolutions["brace"], yard.id, params))
        except OrderError as e:
            failed.append(f"{name}: {e}")
            failed_ids.append(yard.id)
            continue
        started.append({"evolution": "brace", "subject": yard.id, "params": params})
    if not started:
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, "brace", object_name, started, texts, failed)
    data = {
        "verb": "brace",
        "level": 1,
        "object": object_name,
        "mode": mode,
        "tack": tack,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    return "evolution.started", text, data


def _trim(
    ship: Ship, order: Order, vocab: Vocabulary, skip: frozenset[str] = frozenset()
) -> Result:
    """'Trim sails': brace every yard to the present apparent wind and tend the
    fore-and-aft sheets. 'Trim the yards' and 'trim the sheets' do one or the
    other. The best angle of attack for a yard is where its sail's lift curve
    peaks (data/sail_classes.yaml); an empty yard is trimmed as a square sail
    would be, so the whole rig swings together."""
    from freesail.evolutions.trim import wanted_sheet_angle
    from freesail.physics.sails import SAIL_CLASSES

    _no_stray_modifiers(order, {"manner"})
    phrase = order.verb_phrase
    do_yards = "sheet" not in phrase
    do_sheets = "yard" not in phrase
    d = ship.dyn
    if d.apparent_wind_speed < 0.5:
        raise OrderError("There is no wind to trim to.")
    awa = abs(d.apparent_wind_angle)
    sign = 1.0 if d.tack == "starboard" else -1.0

    started: list[dict[str, Any]] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    if do_yards:
        runner = runner_of(ship)
        yards = [y for y in ship.spars.values() if y.is_yard and y.id not in skip]
        for yard in yards:
            name = resolve.the(ship, yard.id)
            if yard.wrecked or yard.sent_down:
                failed.append(f"{name} is {'carried away' if yard.wrecked else 'sent down'}")
                failed_ids.append(yard.id)
                continue
            sail = ship.sail_of(yard)
            cls = SAIL_CLASSES.get(sail.cls if sail else "square") or SAIL_CLASSES["square"]
            best_alpha = cls.alpha[max(range(len(cls.lift)), key=lambda i: cls.lift[i])]
            chord = min(max(awa - best_alpha, 0.0), math.pi / 2)
            target = math.copysign(min(math.pi / 2 - chord, yard.brace_limit), sign)
            params = {
                "target_deg": round(units.rad_to_deg(target), 2),
                "target_angle": target,
                "mode": "to the wind",
                "tack": d.tack,
            }
            try:
                runner.start(ship, vocab.evolutions["brace"], yard.id, params)
            except OrderError as e:
                failed.append(f"{name}: {e}")
                failed_ids.append(yard.id)
                continue
            started.append({"evolution": "brace", "subject": yard.id, "params": params})

    trimmed: list[str] = []
    if do_sheets:
        for sail in ship.sails.values():
            if sail.is_set and sail.is_fore_and_aft and sail.cls in ("gaff", "jibheaded"):
                sail.sheet_angle = wanted_sheet_angle(sail.cls, d.apparent_wind_angle)
                trimmed.append(resolve.the(ship, sail.id))

    if not started and not trimmed:
        if failed:
            raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
        raise OrderError("Nothing to trim: no sail is set." if do_sheets else "No yards to trim.")

    parts: list[str] = []
    if started:
        parts.append(
            f"Braced {len(started)} yard{'s' if len(started) != 1 else ''} to the wind, "
            f"{units.rad_to_deg(awa):.0f}° on the {d.tack} bow"
        )
    if trimmed:
        parts.append(f"trimmed the sheets of {errors.sentence_list(trimmed)}")
    text = "; ".join(parts)
    text = text[0].upper() + text[1:] + "."
    if failed:
        text += f" Not {errors.sentence_list(failed)}."
    data = {
        "verb": "trim",
        "level": 1,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "trimmed_sheets": trimmed,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    kind = "evolution.started" if started and not trimmed else "sail.trimmed"
    return kind, text, data


def _yard_for(ship: Ship, pid: str) -> Spar:
    """The yard an object of 'brace' names: a yard itself, or a square sail's yard."""
    part = ship.parts[pid]
    name = resolve.display_name(ship, pid)
    if isinstance(part, Spar):
        if part.is_yard:
            return part
        sail = ship.sail_of(part)
        how = " it is trimmed with its sheet and vangs" if part.cls in ("gaff", "boom") else ""
        hint = f"; the {sail.cls} sail on it is not braced;{how}" if sail else f";{how}"
        hint = hint.rstrip(";")
        raise OrderError(f"The {name} is a {part.cls.replace('_', ' ')}, not a yard{hint}.")
    if isinstance(part, Sail):
        yard = ship.yard_of(part)
        if yard is not None and yard.is_yard:
            return yard
        raise OrderError(
            f"The {name} is a {part.cls} sail; it has no yard to brace. Trim it with its sheet."
        )
    if isinstance(part, Line) and part.cls == "brace":
        return ship.spars[part.of]
    raise OrderError(f"You brace yards; the {name} is {_what(ship, part)}.")


# ---------------------------------------------------------------------------
# Level 0: lines
# ---------------------------------------------------------------------------


def _line_action(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    verb = order.verb
    _no_stray_modifiers(order, {"fathoms", "a_little", "manner"})
    res = resolve.resolve(ship, order.object or "", order.side_word, verb)
    lines: list[Line] = []
    for pid in res.ids:
        part = ship.parts[pid]
        if isinstance(part, Line) and not part.is_standing:
            lines.append(part)
            continue
        if isinstance(part, Line):
            raise OrderError(
                f"The {resolve.display_name(ship, pid)} "
                f"{'are' if pid.split('.')[-1].endswith('s') or '.shrouds' in pid else 'is'} "
                f"standing rigging; set up with deadeyes and lanyards, not {verb}ed."
            )
        raise errors.wrong_kind(
            verb,
            resolve.display_name(ship, pid),
            _what(ship, part),
            "lines",
            _line_hint(ship, part),
        )

    steps = 1.0
    if "fathoms" in order.modifiers:
        steps = float(order.modifiers["fathoms"])
    manner = order.modifiers.get("manner")
    side_note = resolve.side_phrase(res.side, res.side_word)

    texts: list[str] = []
    data: dict[str, Any] = {
        "verb": verb,
        "level": 0,
        "subjects": [ln.id for ln in lines],
        "side": res.side,
        "changes": [],
    }
    kind = {"haul": "line.hauled", "ease": "line.eased", "check": "line.eased"}.get(
        verb, f"line.{verb.replace(' ', '_')}"
    )
    for line in lines:
        name = resolve.the(ship, line.id)
        if side_note and res.kind != "part":
            name = f"the {side_note} {resolve.family_name(ship, line.id)}"
        if line.state is LineState.PARTED:
            raise OrderError(
                f"{name[0].upper()}{name[1:]} is parted; it must be spliced or rove afresh."
            )
        if verb == "let go":
            if line.state is LineState.FREE:
                raise OrderError(f"{name[0].upper()}{name[1:]} is already running free.")
            line.state = LineState.FREE
            texts.append(f"Let go {name}; it ran free.")
            data["changes"].append({"line": line.id, "state": "free"})
        elif verb == "belay":
            line.state = LineState.BELAYED
            texts.append(f"Belayed {name}.")
            data["changes"].append({"line": line.id, "state": "belayed"})
        else:
            hauling = verb == "haul"
            text, change = _haul_or_ease(ship, line, hauling, steps, name)
            line.state = LineState.BELAYED
            if manner:
                text = text.replace(";", f", {manner};", 1)
            texts.append(text)
            data["changes"].append(change)
    return kind, " ".join(texts), data


def _line_hint(ship: Ship, part: Any) -> str:
    names: list[str] = []
    for ln in ship.lines_of(part):
        if ln.is_standing:
            continue
        fam = resolve.family_name(ship, ln.id)
        if fam not in names:
            names.append(fam)
    if isinstance(part, Sail):
        yard = ship.yard_of(part)
        if yard is not None:
            for ln in ship.lines_of(yard):
                fam = resolve.family_name(ship, ln.id)
                if fam not in names:
                    names.append(fam)
    if not names:
        return ""
    return "Name one of its lines: " + errors.join_names(f"the {n}" for n in names) + "."


def _haul_or_ease(
    ship: Ship, line: Line, hauling: bool, steps: float, name: str
) -> tuple[str, dict[str, Any]]:
    """Move what the line controls one step (times `steps`) and say what happened."""
    did = "Hauled" if hauling else "Eased"
    # A line that was let go is taken up and belayed again by hauling on it,
    # even when there is nothing left to gain.
    recover = hauling and line.state is LineState.FREE
    target = ship.parts[line.of]

    if line.cls == "brace" and isinstance(target, Spar):
        # Sign convention (corrected contract, matching package 4): brace_angle is
        # positive when the yard is braced up for the starboard tack, starboard
        # yardarm forward and larboard yardarm aft. Hauling the larboard brace
        # pulls the larboard yardarm aft, so it increases the angle; hauling the
        # starboard brace decreases it.
        side_sign = 1.0 if line.side == "larboard" else -1.0
        delta = side_sign * BRACE_STEP * steps * (1.0 if hauling else -1.0)
        limit = target.brace_limit
        new = max(-limit, min(limit, target.brace_angle + delta))
        if abs(new - target.brace_angle) < 1e-9 and recover:
            return f"Hauled {name} taut and belayed it.", {"line": line.id, "yard": target.id}
        if abs(new - target.brace_angle) < 1e-9:
            where = "sharp up" if abs(target.brace_angle) >= limit - 1e-9 else "as far as it goes"
            raise OrderError(
                f"{resolve.the(ship, target.id)[0].upper()}{resolve.the(ship, target.id)[1:]} is "
                f"already braced {where} that way; it will come no further."
            )
        target.brace_angle = new
        text = f"{did} {name}; {resolve.the(ship, target.id)} now {_brace_words(new)}."
        return text, {"line": line.id, "yard": target.id, "brace_angle": new}

    if line.cls == "sheet" and isinstance(target, Sail) and target.is_fore_and_aft:
        delta = SHEET_STEP * steps * (-1.0 if hauling else 1.0)
        new = max(0.0, min(MAX_SHEET_ANGLE, target.sheet_angle + delta))
        if abs(new - target.sheet_angle) < 1e-9 and recover:
            return f"Hauled {name} taut and belayed it.", {"line": line.id, "sail": target.id}
        if abs(new - target.sheet_angle) < 1e-9:
            state = "hard in" if hauling else "eased right off"
            raise OrderError(f"{name[0].upper()}{name[1:]} is already {state}.")
        target.sheet_angle = new
        deg = units.rad_to_deg(new)
        text = (
            f"{did} {name}; {resolve.the(ship, target.id)} now "
            f"{'amidships' if deg < 0.5 else f'{deg:.0f}° off the centreline'}."
        )
        return text, {"line": line.id, "sail": target.id, "sheet_angle": new}

    # halyards, sheets of square sails, clewlines, tacks, downhauls and the rest:
    # a fraction hauled, 1 = home.
    delta = HOIST_STEP * steps * (1.0 if hauling else -1.0)
    new = max(0.0, min(1.0, line.hauled + delta))
    if abs(new - line.hauled) < 1e-9 and recover:
        return f"Hauled {name} taut and belayed it.", {"line": line.id, "hauled": new}
    if abs(new - line.hauled) < 1e-9:
        state = "hauled home" if hauling else "eased right off"
        raise OrderError(f"{name[0].upper()}{name[1:]} is already {state}.")
    line.hauled = new
    what = "home" if new >= 1.0 - 1e-9 else ("right off" if new <= 1e-9 else _tenths(new))
    text = f"{did} {name}; now {what}."
    return text, {"line": line.id, "hauled": new}


def _brace_words(angle: float) -> str:
    deg = abs(units.rad_to_deg(angle))
    if deg < 0.5:
        return "square"
    tack = "starboard" if angle > 0 else "larboard"
    return f"braced {deg:.0f}° for the {tack} tack"


_TENTHS = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]


def _tenths(fraction: float) -> str:
    n = int(round(fraction * 10))
    n = max(1, min(9, n))
    return f"{_TENTHS[n]}-tenth{'s' if n > 1 else ''} hauled"


# ---------------------------------------------------------------------------
# Helm
# ---------------------------------------------------------------------------


def _helm(ship: Ship, order: Order) -> Result:
    dyn = ship.dyn
    mods = order.modifiers
    verb = order.verb
    _no_stray_modifiers(order, {"heading", "points", "direction", "manner"})

    if verb == "keep her full":
        dyn.helm_mode = HelmMode.FULL_AND_BY
        dyn.steady = False
        return (
            "helm.order",
            "Helm ordered: keep her full and by.",
            {"helm_mode": HelmMode.FULL_AND_BY.value},
        )

    base = dyn.target_heading if dyn.helm_mode is HelmMode.HEADING else dyn.heading
    # Toward the wind is toward the side the wind is on.
    windward = 1.0 if dyn.tack == "starboard" else -1.0

    if verb == "steer":
        if "heading" in mods:
            target = units.wrap_2pi(mods["heading"])
            said = mods.get("heading_text", "")
        elif "points" in mods:
            direction = mods.get("direction")
            if direction is None:
                raise OrderError(
                    "Steer how many points which way? Say 'up', 'off', "
                    "'to starboard' or 'to larboard'."
                )
            sign = {"starboard": 1.0, "larboard": -1.0, "up": windward, "off": -windward}[direction]
            target = units.wrap_2pi(base + sign * units.points_to_rad(mods["points"]))
            way = direction if direction in ("up", "off") else f"to {direction}"
            said = f"{_points_words(mods['points'])} {way}"
        else:
            raise OrderError(
                "Steer where? Give a compass point ('south-west by west'), degrees ('245') "
                "or points ('two points to starboard')."
            )
    else:
        points = float(mods.get("points", 1.0))
        sign = windward if verb == "come up" else -windward
        target = units.wrap_2pi(base + sign * units.points_to_rad(points))
        said = _points_words(points)

    dyn.helm_mode = HelmMode.HEADING
    dyn.target_heading = target
    dyn.steady = False
    shown = units.format_heading(target)
    if verb == "steer":
        text = f"Helm ordered: steer {shown}."
        if "points" in mods:
            text = f"Helm ordered: steer {said}; {shown}."
    else:
        text = f"Helm ordered: {verb} {said}; steer {shown}."
    data = {
        "helm_mode": HelmMode.HEADING.value,
        "target_heading": target,
        "verb": verb,
        "points": mods.get("points"),
    }
    return "helm.order", text, data


_POINT_WORDS = {1: "a point", 2: "two points", 3: "three points", 4: "four points"}


def _points_words(points: float) -> str:
    if points == int(points) and int(points) in _POINT_WORDS:
        return _POINT_WORDS[int(points)]
    return f"{points:g} points"


# ---------------------------------------------------------------------------
# Whole-ship evolutions: tack, wear, heave to, fill away
# ---------------------------------------------------------------------------


def _ship_evolution(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    _no_stray_modifiers(order, {"tack", "manner"})
    evo = vocab.evolutions[order.verb]
    params: dict[str, Any] = {}
    if "tack" in order.modifiers:
        if order.verb != "heave to":
            raise OrderError(
                f"'{order.verb}' takes no tack; the ship goes onto the other one. "
                f"'Heave to on the larboard tack' is the order that takes one."
            )
        params["tack"] = order.modifiers["tack"]
    runner = runner_of(ship)
    text = runner.start(ship, evo, SHIP_SUBJECT, params)
    data = {
        "verb": order.verb,
        "level": 1,
        "subjects": [SHIP_SUBJECT],
        "evolutions": [{"evolution": evo, "subject": SHIP_SUBJECT, "params": params}],
        "failed": [],
    }
    return "evolution.started", text, data
