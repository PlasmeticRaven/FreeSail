"""The verb table (spec §8.2): what each parsed order does to the ship.

Three kinds of verb live here:

- **Level 1 sail and yard verbs** (`set`, `take in`, `furl`, `reef`, `shake
  out`, `brace`, `square`, `back`, `trim`) and the **whole-ship evolutions**
  (`tack ship`, `wear ship`, `heave to`, `fill away`) start an evolution
  through the runner kept in `ship.extra["evolutions"]` (package 7). The
  verb and the sail's class pick the evolution id from `vocabulary.yaml`
  (`set` + `square` = `set_square`). A group object starts one evolution per
  member; if some fail, the rest still start and the failures are reported
  in the log text. `scandalise` is in the table only to be refused.
  Milestone 3 adds the sail verbs `bend`, `unbend`, `shift` and `goose wing`
  on the same path, `rig out` and `rig in` for a studding sail boom (or the
  studding sail it carries), and whole-ship orders (`send down the topgallant
  masts`, `strike the topmasts`, `box haul`, `lie a try`, `scud`, `back and
  fill`, `loose sails to dry`, `furl all` and the rest) on the tack's path.
- **Level 0 line verbs** (`haul`, `ease`, `check`, `let go`, `belay`, and
  `sheet home` on a sail) act on the part at once: a brace shifts its yard's
  angle by five degrees, a sheet of a fore-and-aft sail shifts the sail's
  sheet angle by five degrees, a halyard (or any other line) shifts its
  hoist by a tenth; `home` or `aft` takes it all the way.
- **Helm verbs** (`steer`, `come up`, `bear away`, `keep her full`) set the
  helm targets in `ship.dyn` for the helmsman in the physics to follow; the
  **conning words** (`steady`, `meet her`, `right the helm`, `helm a-lee`,
  `helm a-weather`) speak to the wheel itself.

Each returns `(kind, log_text, data)` for the World to log, or raises
`OrderError` with a sentence saying why the order was not carried out.
"""

from __future__ import annotations

import math
from typing import Any

from freesail import units
from freesail.orders import crew as crew_orders
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
    ship: Ship,
    order: Order,
    vocab: Vocabulary | None = None,
    skip: frozenset[str] = frozenset(),
    group: str | None = None,
) -> Result:
    """Carry out a parsed order. Group evolutions are expanded in `orders.handle`, not here.

    `skip` names parts to pass over in silence: the group expander uses it
    so that a sail listed twice ("set the plain sail", then "set the
    staysails") is set once. If nothing is left, NothingToDoError is raised.
    `group` is the work in words when the order is one line of a group
    evolution ("setting plain sail"); the runner writes one line for the
    group when the first of its evolutions must wait for hands.
    """
    vocab = vocab or load_vocabulary()
    spec = vocab.verbs[order.verb]
    if order.verb in crew_orders.CREW_VERBS:
        _no_stray_modifiers(order, set())
        return crew_orders.CREW_VERBS[order.verb](ship, order)
    if order.verb in BRACE_VERBS:
        return _brace(ship, order, vocab, skip, group)
    if order.verb == "trim":
        return _trim(ship, order, vocab, skip, group=group)
    if order.verb == "sheet home":
        return _sheet_home(ship, order, vocab)
    if order.verb in BOOM_VERBS:
        return _boom_evolution(ship, order, vocab, skip, group)
    if spec.object == "sail":
        return _sail_evolution(ship, order, vocab, skip, group)
    if spec.object == "line":
        return _line_action(ship, order, vocab)
    if spec.object in ("heading", "points") or order.verb in HELM_VERBS:
        return _helm(ship, order)
    if order.verb in vocab.evolutions and isinstance(vocab.evolutions[order.verb], str):
        return _ship_evolution(ship, order, vocab)
    raise OrderError(f"'{order.verb}' is in the vocabulary but has no meaning yet.")


BRACE_VERBS = ("brace", "square", "back")  # "square the yards", "back the main topsail"
BOOM_VERBS = ("rig out", "rig in")  # a studding sail boom, or the studding sail on it
# Sail verbs whose evolution is a script that works on the sail it is given
# (`params["sail"]`), and which make sense for a sail that is blown out.
SAIL_SCRIPT_VERBS = ("bend", "unbend", "shift")
# The helm verbs with no heading or points after them: the conning words.
HELM_VERBS = (
    "keep her full",
    "steady",
    "meet her",
    "right the helm",
    "helm a lee",
    "helm a weather",
)


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
        "round": "'brace round' is the order that swings the yards",
        "tack": "'on the ... tack' belongs with 'brace' or 'heave to'",
        "reefs": "a number of reefs belongs with 'reef' or 'shake out'",
        "close": "'close' belongs with 'reef'",
        "fathoms": "fathoms belong with 'haul' or 'ease'",
        "a_little": "'a little' belongs with 'haul' or 'ease'",
        "home": "'home' and 'aft' belong with 'haul'",
        "manner": "'handsomely' and 'roundly' belong with 'haul' or 'ease'",
        "heading": "a heading belongs with 'steer'",
        "points": "a number of points belongs with 'steer', 'come up' or 'bear away'",
        "direction": "a direction belongs with 'steer'",
        "hands_from": (
            "a watch or a station is sent to work on a sail, a yard or the ship, not to this"
        ),
    }
    reasons = [words.get(k, f"'{k}' does not go with '{order.verb}'") for k in stray]
    raise OrderError(f"'{order.verb}' was understood, but {errors.join_names(reasons, 'and')}.")


# Groups said without 'the' in the group line: "setting plain sail".
UNCOUNTED_GROUPS = ("plain sail", "all sail")


def _group_label(verb: str, object_name: str, group: str | None) -> str:
    """The work in words for the runner's one line when a group must wait for hands:
    'setting plain sail', 'setting the topsails', 'bracing the yards'."""
    if group:
        return group
    from freesail.evolutions.runner import gerund

    first, _, rest = verb.partition(" ")
    doing = f"{gerund(first)} {rest}".strip()
    what = object_name if object_name in UNCOUNTED_GROUPS else f"the {object_name}"
    return f"{doing} {what}"


def _hands_params(
    ship: Ship, order: Order, evolution_ids: list[str], group: str | None
) -> tuple[dict[str, Any], crew_orders.WatchCall | None]:
    """The params every evolution of this order carries for the hands: the group
    label when there are several, and the hands selector (turning a watch up)."""
    params, call = crew_orders.take_hands_from(ship, order, evolution_ids)
    if group is not None and len(evolution_ids) > 1 and crew_orders.crew_of(ship) is not None:
        params["group"] = group  # without a crew nothing waits for hands: milestone 2's params
    return params, call


def _settle_call(ship: Ship, call: crew_orders.WatchCall | None, started: bool) -> None:
    """A watch turned up for this order keeps coming if the order stands, else goes below."""
    if call is None:
        return
    if started:
        crew_orders.commit(ship, call)
    else:
        call.cancel()


# ---------------------------------------------------------------------------
# Level 1: sails
# ---------------------------------------------------------------------------


def _sail_evolution(
    ship: Ship,
    order: Order,
    vocab: Vocabulary,
    skip: frozenset[str] = frozenset(),
    group: str | None = None,
) -> Result:
    verb = order.verb
    allowed = {"reefs", "close", "manner"} if verb in ("reef", "shake out") else {"manner"}
    allowed.add("hands_from")
    _no_stray_modifiers(order, allowed)
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
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    checks = {sail.id: _sail_check(ship, sail, verb, order, mapping, vocab) for sail in sails}
    if all(checks.values()):
        # Nothing to start: refuse on the merits before asking for the runner.
        reasons = [r for r in checks.values() if r]
        if len(reasons) == 1:
            raise OrderError(reasons[0][0].upper() + reasons[0][1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(reasons)}.")
    runner = runner_of(ship)
    to_start = [sail for sail in sails if not checks[sail.id]]
    extra, call = _hands_params(
        ship,
        order,
        [mapping[sail.cls] for sail in to_start],
        _group_label(verb, res.name, group) if len(to_start) > 1 else None,
    )
    params.update(extra)
    for sail in sails:
        reason = checks[sail.id]
        if reason:
            failed.append(reason)
            failed_ids.append(sail.id)
            continue
        evo = mapping[sail.cls]
        p = dict(params)
        if verb in SAIL_SCRIPT_VERBS:
            p["sail"] = sail.id
        if verb == "shake out" and order.modifiers.get("close"):
            p["reefs"] = sail.reefs
        if verb == "reef" and order.modifiers.get("close"):
            p["reefs"] = sail.reef_bands - sail.reefs  # every band still out: close reefed
        try:
            texts.append(runner.start(ship, evo, sail.id, p))
        except OrderError as e:
            failed.append(f"{resolve.the(ship, sail.id)}: {e}")
            failed_ids.append(sail.id)
            continue
        started.append({"evolution": evo, "subject": sail.id, "params": p})
    _settle_call(ship, call, bool(started))

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
    if sail.state is SailState.BLOWN_OUT and verb not in SAIL_SCRIPT_VERBS:
        return f"{name} is blown out and there is no sail to {verb}; shift it for a new one"
    if sail.state is SailState.UNBENT and verb not in SAIL_SCRIPT_VERBS:
        return f"{name} is unbent; there is no sail on the yard. Bend one first"
    if verb == "scandalise":
        if sail.cls != "gaff":
            return f"{name} is a {sail.cls} sail; it has no peak to drop"
        return vocab.refusals["scandalise"].format(name=name[4:]).rstrip(".")
    if sail.cls not in mapping:
        template = vocab.refusals.get(verb, "'{verb}' has no meaning for a {class} sail")
        return template.format(name=name[4:], **{"class": sail.cls, "verb": verb}).rstrip(".")
    if verb == "set" and sail.state is SailState.SET:
        return f"{name} is already set"
    if verb == "take in":
        unsuited = _take_in_word_check(ship, sail, order.verb_phrase, vocab)
        if unsuited:
            return unsuited
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


def _take_in_kind(ship: Ship, sail: Sail) -> str:
    """The class a take-in word is chosen by: 'course' for a square sail on a lower yard."""
    if sail.cls == "square":
        yard = ship.yard_of(sail)
        parent = ship.parent_of(yard) if yard is not None else None
        if parent is not None and parent.cls == "mast":
            return "course"
    return sail.cls


_PAST = {
    "clew up": "clewed up",
    "haul up": "hauled up",
    "brail up": "brailed up",
    "brail in": "brailed in",
    "haul down": "hauled down",
    "lower": "lowered",
    "take in": "taken in",
}


def _take_in_word_check(ship: Ship, sail: Sail, phrase: str, vocab: Vocabulary) -> str | None:
    """'A topsail is clewed up, not hauled up' when the take-in word does not suit the sail."""
    if phrase not in vocab.class_bound_take_in_phrases or phrase in ("take in", "take in the"):
        return None
    kind = _take_in_kind(ship, sail)
    suits = vocab.take_in_words.get(kind, ())
    if phrase in suits:
        return None
    name = resolve.the(ship, sail.id)
    proper = suits[0] if suits else "take in"
    what = {"course": "course", "square": "topsail or light sail"}.get(kind, f"{kind} sail")
    return (
        f"a {what} is {_PAST.get(proper, proper)}, not {_PAST.get(phrase, phrase)}; "
        f"say '{proper} {name}' or 'take in {name}'"
    )


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
    ship: Ship,
    order: Order,
    vocab: Vocabulary,
    skip: frozenset[str] = frozenset(),
    group: str | None = None,
) -> Result:
    """'Brace', 'square' and 'back'. The mode says the angle: sharp up, up, in
    and square as the table gives them; 'aback' (and the verb 'back') sharp
    up for the *other* tack, the sail pressed against the mast, as heaving to
    does; 'to the wind' the best angle for the present apparent wind, as
    'trim the yards' finds it. 'Brace round' with no mode said braces sharp
    up for the tack the wind is on."""
    _no_stray_modifiers(order, {"brace_mode", "tack", "manner", "round", "hands_from"})
    verb = order.verb
    mode = order.modifiers.get("brace_mode")
    tack = order.modifiers.get("tack")
    if verb in ("square", "back"):
        if mode is not None and mode != {"square": "square", "back": "aback"}[verb]:
            raise OrderError(f"'{verb}' says how already; '{mode}' contradicts it.")
        mode = "square" if verb == "square" else "aback"
        if verb == "back" and not order.object:
            raise OrderError("Back what? Name a yard or a square sail, such as the main topsail.")
    if mode is None:
        if tack is not None or order.modifiers.get("round"):
            mode = "sharp up"  # "brace round" or "brace on the larboard tack": sharp up for it
        else:
            raise OrderError(
                "Brace them how? Say 'sharp up', 'up', 'in', 'square', 'aback' or 'to the wind', "
                "and 'on the starboard tack' or 'on the larboard tack' if it matters."
            )
    if order.object:
        res = resolve.resolve(ship, order.object, order.side_word, verb)
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
    if vocab.brace_modes[mode] == "wind":
        return _trim(ship, order, vocab, skip, yards=yards, object_name=object_name, group=group)

    tack = tack or ship.dyn.tack
    aback = vocab.brace_modes[mode] == "aback"
    if aback:
        tack = resolve.other_side(tack)  # laid aback: braced up for the other tack
        # A yard is laid aback with the rest of its mast's yards: braced the other
        # way from the yards above and below, its sail would foul theirs. "Back the
        # main topsail" is the period way of saying "brace the main yards aback".
        masts = []
        for y in yards:
            m = ship.mast_of(y)
            if m is not None and m not in masts:
                masts.append(m)
        yards = [
            y
            for y in ship.spars.values()
            if y.is_yard and ship.mast_of(y) in masts and y.id not in skip
        ]
        object_name = errors.join_names(
            [f"{resolve.display_name(ship, m.id).replace(' mast', '')} yards" for m in masts],
            "and",
        )
    sign = 1.0 if tack == "starboard" else -1.0

    runner = runner_of(ship)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    workable = [y for y in yards if not (y.wrecked or y.sent_down)]
    extra, call = _hands_params(
        ship,
        order,
        [vocab.evolutions["brace"]] * len(workable),
        _group_label("brace", object_name, group) if len(workable) > 1 else None,
    )
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
        target = yard.brace_limit if isinstance(target_deg, str) else units.deg_to_rad(target_deg)
        target = math.copysign(min(abs(target), yard.brace_limit), sign) if target else 0.0
        params = {
            # unsigned, as data/evolutions/brace.yaml reads it; `tack` gives the sign
            "target_deg": round(abs(units.rad_to_deg(target)), 2),
            "target_angle": target,  # signed radians: + = braced up for the starboard tack
            "mode": mode,
            "tack": tack,
            **extra,
        }
        try:
            texts.append(runner.start(ship, vocab.evolutions["brace"], yard.id, params))
        except OrderError as e:
            failed.append(f"{name}: {e}")
            failed_ids.append(yard.id)
            continue
        started.append({"evolution": "brace", "subject": yard.id, "params": params})
    _settle_call(ship, call, bool(started))
    if not started:
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, "brace", object_name, started, texts, failed)
    # The sentence for the log. The World drops an evolution order's own text
    # when the runner has logged its start, so it goes in as a note, which
    # the next tick writes to the log after the runner's "Man the braces".
    note: str | None = None
    if aback:
        backed = errors.join_names(
            [resolve.display_name(ship, s["subject"]) for s in started], "and"
        )
        sails = [ship.sail_of(ship.spars[s["subject"]]) for s in started]
        set_names = [
            resolve.display_name(ship, sl.id) for sl in sails if sl is not None and sl.is_set
        ]
        pressed = (
            f"the {errors.join_names(set_names, 'and')} to the mast"
            if set_names
            else f"nothing set on {'it' if len(started) == 1 else 'them'} to press against the mast"
        )
        note = f"Laid the {backed} aback, braced up for the {tack} tack; {pressed}."
        ship.note(
            "routine", "yard.laid_aback", note, data={"subjects": [s["subject"] for s in started]}
        )
    elif order.modifiers.get("round") and order.modifiers.get("brace_mode") is None:
        note = f"Braced round for the {tack} tack."
        ship.note("routine", "yard.braced_round", note, data={"tack": tack})
    elif verb == "square":
        note = f"Squared the {object_name}."
        ship.note("routine", "yard.squared", note, data={"object": object_name})
    if note:
        text = f"{note} {text}"
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
    ship: Ship,
    order: Order,
    vocab: Vocabulary,
    skip: frozenset[str] = frozenset(),
    yards: list[Spar] | None = None,
    object_name: str = "yards",
    group: str | None = None,
) -> Result:
    """'Trim sails': brace every yard to the present apparent wind and tend the
    fore-and-aft sheets. 'Trim the yards' and 'trim the sheets' do one or the
    other; 'brace the head yards to the wind' trims only the yards given.
    The best angle of attack for a yard is where its sail's lift curve
    peaks (data/sail_classes.yaml); an empty yard is trimmed as a square sail
    would be, so the whole rig swings together."""
    from freesail.evolutions.trim import wanted_sheet_angle
    from freesail.physics.sails import SAIL_CLASSES

    if order.verb == "trim":
        _no_stray_modifiers(order, {"manner", "hands_from"})
        phrase = order.verb_phrase
        do_yards = "sheet" not in phrase
        do_sheets = "yard" not in phrase
    else:
        do_yards, do_sheets = True, False  # "brace ... to the wind"
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
        if yards is None:
            yards = [y for y in ship.spars.values() if y.is_yard and y.id not in skip]
        workable = [y for y in yards if not (y.wrecked or y.sent_down)]
        extra, call = _hands_params(
            ship,
            order,
            [vocab.evolutions["brace"]] * len(workable),
            _group_label("brace", object_name, group) if len(workable) > 1 else None,
        )
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
                **extra,
            }
            try:
                runner.start(ship, vocab.evolutions["brace"], yard.id, params)
            except OrderError as e:
                failed.append(f"{name}: {e}")
                failed_ids.append(yard.id)
                continue
            started.append({"evolution": "brace", "subject": yard.id, "params": params})
        _settle_call(ship, call, bool(started))

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
        which = (
            f"the {object_name}"
            if object_name != "yards"
            else f"{len(started)} yard{'s' if len(started) != 1 else ''}"
        )
        parts.append(
            f"Braced {which} to the wind, {units.rad_to_deg(awa):.0f}° on the {d.tack} bow"
        )
    if trimmed:
        parts.append(f"trimmed the sheets of {errors.sentence_list(trimmed)}")
    text = "; ".join(parts)
    text = text[0].upper() + text[1:] + "."
    if failed:
        text += f" Not {errors.sentence_list(failed)}."
    data = {
        "verb": order.verb,
        "level": 1,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "trimmed_sheets": trimmed,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    if order.verb != "trim":
        data.update({"object": object_name, "mode": "to the wind", "tack": d.tack})
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


def _sheet_home(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Sheet home the fore topsail': its sheets hauled home and belayed; a
    fore-and-aft sail's sheet hauled flat aft. Level 0, at once."""
    _no_stray_modifiers(order, {"manner", "home"})
    res = resolve.resolve(ship, order.object or "", order.side_word, "sheet home")
    sails: list[Sail] = []
    for pid in res.ids:
        part = ship.parts[pid]
        if not isinstance(part, Sail):
            raise errors.wrong_kind(
                "sheet home",
                resolve.display_name(ship, pid),
                _what(ship, part),
                "sails",
                _sail_hint(ship, part),
            )
        sails.append(part)
    texts: list[str] = []
    failed: list[str] = []
    changes: list[dict[str, Any]] = []
    for sail in sails:
        name = resolve.the(ship, sail.id)
        sheets = [ln for ln in ship.sheets_of(sail) if ln.state is not LineState.PARTED]
        if not sheets:
            failed.append(
                f"{name} has no sheet to haul"
                + (" that is not parted" if ship.sheets_of(sail) else "")
            )
            continue
        moved = False
        if sail.is_fore_and_aft:
            if sail.sheet_angle > 1e-9:
                sail.sheet_angle = 0.0
                moved = True
        for ln in sheets:
            if ln.hauled < 1.0 - 1e-9 or ln.state is LineState.FREE:
                moved = True
            ln.hauled = 1.0
            ln.state = LineState.BELAYED
        if not moved:
            failed.append(f"{name} is sheeted home already")
            continue
        changes.append({"sail": sail.id, "sheets": [ln.id for ln in sheets]})
        if sail.is_fore_and_aft:
            texts.append(f"Hauled the {resolve.display_name(ship, sail.id)} sheet flat aft.")
        else:
            texts.append(f"Sheeted home {name}.")
    if not changes:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:] + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = " ".join(texts)
    if failed:
        text += " Not done: " + errors.sentence_list(failed) + "."
    data = {
        "verb": "sheet home",
        "level": 0,
        "subjects": [c["sail"] for c in changes],
        "side": res.side,
        "changes": changes,
        "failed": failed,
    }
    return "line.hauled", text, data


def _line_action(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    verb = order.verb
    _no_stray_modifiers(order, {"fathoms", "a_little", "manner", "home"})
    if "home" in order.modifiers and verb != "haul":
        raise OrderError(f"'{verb}' was understood, but 'home' and 'aft' belong with 'haul'.")
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
    if order.modifiers.get("home"):
        steps = math.inf  # all the way: home, aft, flat
    manner = order.modifiers.get("manner")
    side_note = resolve.side_phrase(res.side, res.side_word)

    texts: list[str] = []
    failed: list[str] = []
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
        try:
            text, change = _one_line(ship, line, verb, steps, name)
        except OrderError as e:
            # Of several lines ("both sides", "the topsail sheets"), the ones
            # that cannot be worked are reported and the rest are worked.
            failed.append(str(e))
            continue
        if manner:
            text = text.replace(";", f", {manner};", 1)
        texts.append(text)
        data["changes"].append(change)
    if not data["changes"]:
        if len(failed) == 1:
            raise OrderError(failed[0])
        raise OrderError(f"Nothing done: {errors.sentence_list(_lower(f) for f in failed)}.")
    data["subjects"] = [c["line"] for c in data["changes"]]
    text = " ".join(texts)
    if failed:
        text += " Not done: " + errors.sentence_list(_lower(f) for f in failed) + "."
        data["failed"] = failed
    return kind, text, data


def _lower(sentence: str) -> str:
    """'The main brace is parted.' -> 'the main brace is parted.', for a list."""
    return sentence[0].lower() + sentence[1:] if sentence else sentence


def _one_line(
    ship: Ship, line: Line, verb: str, steps: float, name: str
) -> tuple[str, dict[str, Any]]:
    """Work one line; the sentence and the change, or OrderError with the reason."""
    if line.state is LineState.PARTED:
        raise OrderError(
            f"{name[0].upper()}{name[1:]} is parted; it must be spliced or rove afresh."
        )
    if verb == "let go":
        if line.state is LineState.FREE:
            raise OrderError(f"{name[0].upper()}{name[1:]} is already running free.")
        line.state = LineState.FREE
        return f"Let go {name}; it ran free.", {"line": line.id, "state": "free"}
    if verb == "belay":
        line.state = LineState.BELAYED
        return f"Belayed {name}.", {"line": line.id, "state": "belayed"}
    text, change = _haul_or_ease(ship, line, verb == "haul", steps, name)
    line.state = LineState.BELAYED
    return text, change


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
    """Move what the line controls one step (times `steps`) and say what happened.

    `steps` of infinity is "home", "aft" or "flat": all the way in (or, on an
    ease, right off).
    """
    home = math.isinf(steps)
    did = "Hauled" if hauling else "Eased"
    # A line that was let go is taken up and belayed again by hauling on it,
    # even when there is nothing left to gain.
    recover = hauling and line.state is LineState.FREE
    target = ship.parts[line.of]

    if (
        home
        and hauling
        and line.cls == "sheet"
        and isinstance(target, Sail)
        and target.is_fore_and_aft
    ):
        if abs(target.sheet_angle) < 1e-9 and not recover:
            raise OrderError(f"{name[0].upper()}{name[1:]} is already hard in.")
        target.sheet_angle = 0.0
        text = f"Hauled {name} flat aft; {resolve.the(ship, target.id)} now amidships."
        return text, {"line": line.id, "sail": target.id, "sheet_angle": 0.0}
    if home and line.cls == "brace" and isinstance(target, Spar):
        steps = math.ceil(target.brace_limit / BRACE_STEP) + 1  # as far as it will go
    elif home:
        if line.hauled >= 1.0 - 1e-9 and not recover:
            raise OrderError(f"{name[0].upper()}{name[1:]} is already hauled home.")
        line.hauled = 1.0
        return f"Hauled {name} home.", {"line": line.id, "hauled": 1.0}

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
    if verb in HELM_VERBS and ("heading" in mods or "points" in mods):
        raise OrderError(
            f"'{order.verb_phrase}' takes no heading or points; it is the whole order."
        )

    if verb == "keep her full":
        dyn.helm_mode = HelmMode.FULL_AND_BY
        dyn.steady = False
        said = order.verb_phrase
        text = "Helm ordered: keep her full and by."
        if said not in ("keep her full", "full and by", "keep her full and by"):
            text = f"Helm ordered: {said}; keep her full and by."
        return "helm.order", text, {"helm_mode": HelmMode.FULL_AND_BY.value, "said": said}

    if verb in HELM_VERBS:
        return _conn(ship, order)

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


def _conn(ship: Ship, order: Order) -> Result:
    """The conning words: steady, meet her, right the helm, helm a-lee, helm a-weather.

    'Steady' and 'meet her' give the helmsman the heading she has now to
    hold (he meets her swing with the opposite helm and steadies her there).
    'Right the helm' puts the rudder amidships and leaves it: she steers
    herself until the next helm order. 'Helm a-lee' and 'helm a-weather'
    put the rudder hard over, to windward or to leeward of her course, and
    leave it there, as the tack and the wear do for their turns.
    """
    dyn = ship.dyn
    verb = order.verb
    said = order.verb_phrase.replace("a lee", "a-lee").replace("a weather", "a-weather")
    said = said.replace("helms", "helm's")
    windward = 1.0 if dyn.tack == "starboard" else -1.0
    max_rudder = units.deg_to_rad(ship.hull.spec.rudder.max_angle_deg)
    data: dict[str, Any] = {"verb": verb, "said": said}
    if verb in ("steady", "meet her"):
        dyn.helm_mode = HelmMode.HEADING
        dyn.target_heading = units.wrap_2pi(dyn.heading)
        dyn.steady = False
        shown = units.format_heading(dyn.target_heading)
        if verb == "steady":
            text = f"Helm ordered: steady; steer {shown}."
            if said != "steady":
                text = f"Helm ordered: {said}; steady on {shown}."
        else:
            text = f"Helm ordered: {said}; met her swing with the helm, steady on {shown}."
        data.update({"helm_mode": HelmMode.HEADING.value, "target_heading": dyn.target_heading})
        return "helm.order", text, data
    dyn.helm_mode = HelmMode.RUDDER
    dyn.steady = False
    if verb == "right the helm":
        dyn.target_rudder = 0.0
        text = f"Helm ordered: {said}; rudder amidships."
    else:
        sign = windward if verb == "helm a lee" else -windward
        dyn.target_rudder = sign * max_rudder
        side = "starboard" if sign > 0 else "larboard"
        where = "to windward" if verb == "helm a lee" else "to leeward"
        way = "her head coming up to the wind" if verb == "helm a lee" else "her head paying off"
        text = (
            f"Helm ordered: {said}; rudder hard over {where} "
            f"({units.rad_to_deg(max_rudder):.0f}° to {side}), {way}."
        )
    data.update({"helm_mode": HelmMode.RUDDER.value, "target_rudder": dyn.target_rudder})
    return "helm.order", text, data


_POINT_WORDS = {1: "a point", 2: "two points", 3: "three points", 4: "four points"}


def _points_words(points: float) -> str:
    if points == int(points) and int(points) in _POINT_WORDS:
        return _POINT_WORDS[int(points)]
    if points == 0.5:
        return "half a point"
    if points == 1.5:
        return "a point and a half"
    if points - 0.5 == int(points - 0.5) and int(points - 0.5) in _POINT_WORDS:
        return f"{_POINT_WORDS[int(points - 0.5)].split()[0]} and a half points"
    return f"{points:g} points"


# ---------------------------------------------------------------------------
# Level 1: studding sail booms
# ---------------------------------------------------------------------------


def _boom_evolution(
    ship: Ship,
    order: Order,
    vocab: Vocabulary,
    skip: frozenset[str] = frozenset(),
    group: str | None = None,
) -> Result:
    """'Rig out' and 'rig in' a studding sail boom. The object is the boom
    ('the starboard fore topmast studdingsail boom') or the studding sail it
    carries ('the fore topmast studdingsails, both sides'); either way the
    evolution works on the boom (Luce 1884, ch. XXIII: "Rig out! Hoist away!")."""
    _no_stray_modifiers(order, {"manner", "hands_from"})
    verb = order.verb
    res = resolve.resolve(ship, order.object or "", order.side_word, verb)
    mapping: dict[str, str] = vocab.evolutions.get(verb, {})
    booms: list[Spar] = []
    for pid in res.ids:
        part = ship.parts[pid]
        boom: Spar | None = None
        if isinstance(part, Spar) and part.cls == "studdingsail_boom":
            boom = part
        elif isinstance(part, Sail) and part.cls == "studding":
            boom = ship.spar_of_role(part, "boom")
        if boom is None:
            raise errors.wrong_kind(
                verb,
                resolve.display_name(ship, pid),
                _what(ship, part),
                "studding sail booms",
                "",
            )
        if boom.id not in skip and boom not in booms:
            booms.append(boom)
    if not booms:
        raise errors.NothingToDoError(f"Every boom of the {res.name} was already ordered.")
    runner = runner_of(ship)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    evo = mapping["studdingsail_boom"]
    extra, call = _hands_params(
        ship,
        order,
        [evo] * len(booms),
        _group_label(verb, res.name, group) if len(booms) > 1 else None,
    )
    for boom in booms:
        try:
            texts.append(runner.start(ship, evo, boom.id, dict(extra)))
        except OrderError as e:
            failed.append(f"{resolve.the(ship, boom.id)}: {e}")
            failed_ids.append(boom.id)
            continue
        started.append({"evolution": evo, "subject": boom.id, "params": dict(extra)})
    _settle_call(ship, call, bool(started))
    if not started:
        if len(failed) == 1:
            reason = failed[0].split(": ", 1)[-1]
            raise OrderError(reason[0].upper() + reason[1:].rstrip(".") + ".")
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


# ---------------------------------------------------------------------------
# Whole-ship evolutions: tack, wear, heave to, fill away, and the milestone 3
# catalogue (send down the topgallant masts, box haul, lie a-try, scud ...)
# ---------------------------------------------------------------------------


def _ship_evolution(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    _no_stray_modifiers(order, {"tack", "manner", "hands_from"})
    evo = vocab.evolutions[order.verb]
    params: dict[str, Any] = {}
    bare_poles = "bare poles" in order.verb_phrase
    if bare_poles:
        drawing = [
            sl
            for sl in ship.sails.values()
            if sl.is_set or sl.state in (SailState.SHEETED, SailState.GOOSE_WINGED)
        ]
        if drawing:
            names = errors.join_names([resolve.display_name(ship, sl.id) for sl in drawing], "and")
            raise OrderError(
                f"She has sail set ({names}); take it in to wear under bare poles, "
                f"or say 'wear ship'."
            )
        params["bare_poles"] = True
    if evo == "furl_all":
        loose = [
            sl
            for sl in ship.sails.values()
            if sl.state not in (SailState.FURLED, SailState.UNBENT, SailState.BLOWN_OUT)
            and not sl.wrecked
        ]
        if not loose:
            raise OrderError("Every sail is furled already.")
    if "tack" in order.modifiers:
        if order.verb != "heave to":
            raise OrderError(
                f"'{order.verb}' takes no tack; the ship goes onto the other one. "
                f"'Heave to on the larboard tack' is the order that takes one."
            )
        params["tack"] = order.modifiers["tack"]
    runner = runner_of(ship)
    extra, call = crew_orders.take_hands_from(ship, order, [evo])
    params.update(extra)
    try:
        text = runner.start(ship, evo, SHIP_SUBJECT, params)
    except OrderError:
        _settle_call(ship, call, False)
        raise
    _settle_call(ship, call, True)
    if order.verb_phrase.split()[0] in ("gybe", "jibe"):
        # The later word for wearing a fore-and-aft vessel: the boom comes
        # over as the wind crosses the stern. The period word is wear.
        text = (
            "Gybe, that is, wear ship (the period word); the boom will come over as the "
            "wind crosses her stern. " + text
        )
    if bare_poles:
        text = "Under bare poles: hands in the weather fore rigging for a sail. " + text
    data = {
        "verb": order.verb,
        "level": 1,
        "subjects": [SHIP_SUBJECT],
        "evolutions": [{"evolution": evo, "subject": SHIP_SUBJECT, "params": params}],
        "failed": [],
    }
    return "evolution.started", text, data
