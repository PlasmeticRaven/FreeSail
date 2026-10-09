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
  angle by five degrees, a sheet of a fore-and-aft sail takes in or gives a
  fathom of its fall, which moves the sail by the boom's geometry (package
  32e: the sheet holds the trim, `evolutions/trim.py`), a halyard (or any
  other line) shifts its hoist by a tenth; `home` or `aft` takes it all the
  way. A sheet hauled `to windward` holds its sail aback; `let fly` lets it
  run and the sail flogs; `draw <the sail>` lets it draw again. `trim the
  <sail>` is an evolution on the sheet with hands and time.
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
from freesail.crew.model import number_words
from freesail.evolutions import scripts
from freesail.evolutions import trim as yard_trim
from freesail.evolutions.runner import PartyTooSmall
from freesail.orders import crew as crew_orders
from freesail.orders import errors, resolve, work
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.vocabulary import Vocabulary, load_vocabulary
from freesail.physics.sails import BOWLINE_SLACK_ANGLE_DEG
from freesail.ship.graph import Ship
from freesail.ship.parts import (
    CATHARPIN_GAIN_DEG,
    HelmMode,
    Line,
    LineState,
    Sail,
    SailState,
    Spar,
    lower_yards,
    sync_catharpins,
)

BRACE_STEP = units.deg_to_rad(5.0)  # one haul or ease on a brace
HOIST_STEP = 0.1  # one haul or ease on a halyard or any other line
# One haul or ease on a fore-and-aft sheet takes in or gives a fathom of the fall (package
# 32e); "two fathoms" two. The sail's angle follows by the sheet's geometry.
SHEET_TRIM_TOLERANCE = units.deg_to_rad(1.0)  # a sheet within this of its trim stands
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
    if (
        spec.object in ("heading", "points")
        or order.verb in HELM_VERBS
        or order.verb == "trim"
        or _under_way_only(vocab, order.verb)
    ):
        _not_riding(ship, order)  # the helm, the trim and the manoeuvres want her under way
    if order.verb in work.WORK_VERBS:
        return work.execute(ship, order, vocab)  # belaying work (package 29c)
    if order.verb in crew_orders.CREW_VERBS:
        _no_stray_modifiers(order, set())
        return crew_orders.CREW_VERBS[order.verb](ship, order)
    if order.verb in BRACE_VERBS:
        return _brace(ship, order, vocab, skip, group)
    if order.verb == "trim":
        return _trim(ship, order, vocab, skip, group=group)
    if order.verb == "sheet home":
        return _sheet_home(ship, order, vocab)
    if order.verb in REEVE_VERBS:
        return _reeve(ship, order, vocab)  # a parted line rove afresh or spliced (31b)
    if order.verb in BOOM_VERBS or (order.verb == "reef" and _names_bowsprit(ship, order)):
        # a studding sail boom rigged out or in; a running bowsprit rigged out or reefed
        # ("reef the bowsprit", package 32b), the evolution refusing a standing one in words
        return _boom_evolution(ship, order, vocab, skip, group)
    if order.verb in CATHARPIN_VERBS:
        return _catharpins(ship, order, vocab)
    if spec.object == "query":
        return _query(ship, order)
    if spec.object == "wreck":
        return _clear_wreck(ship, order, vocab)
    if order.verb == "let go" and order.verb_phrase == "clear away" and _names_no_line(ship, order):
        # "clear away the larboard studdingsail boom": a spar or a sail is cleared away as
        # a wreck; a line is let go, as "clear away the bowlines" always was (package 30b)
        return _clear_wreck(ship, order, vocab)
    if order.verb == "shift" and _names_spars(ship, order):
        return _shift_spar(ship, order, vocab)
    if order.verb == "draw":
        return _draw(ship, order, vocab)  # a head sail let draw (package 32e)
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
# The whole-ship evolutions a ship at anchor or aground is refused (`_not_riding`): the
# manoeuvres, which want her under way. Until package 37f every whole-ship order was
# refused there, twenty-six verbs with the helm's (the review of gate 5c's playtests,
# 5.8): `furl all sail`, `furl sails`, `square the yards` and `brace the yards square`
# were each answered "She is at anchor; ... must wait till she weighs", and the primer's
# own `at aground then furl all sail` was refused. Sail handed, furled or loosed to dry,
# yards squared or braced, the upper masts and yards sent down or swayed up, a wreck
# cleared and a line rove are a ship's work at anchor as at sea, and are taken.
UNDER_WAY_ONLY = frozenset(
    {
        "tack",
        "wear",
        "heave_to",
        "fill_away",
        "boxhaul",
        "wear_short_round",
        "lie_a_try",
        "scud",
        "back_and_fill",
    }
)


def _under_way_only(vocab: Vocabulary, verb: str) -> bool:
    """Whether the verb is a manoeuvre, which a ship at anchor or aground is refused."""
    evo = vocab.evolutions.get(verb)
    return isinstance(evo, str) and evo in UNDER_WAY_ONLY


BOOM_VERBS = ("rig out", "rig in")  # a studding sail boom, or the studding sail on it
# The lower rigging (milestone 3b): one evolution per lower mast. True: swiftering in.
CATHARPIN_VERBS = {"swifter in the catharpins": True, "ease the catharpins": False}
# The modifier that reverses the head and after yards' trim (Fincham art. 96), set by
# the verb phrases "brace sharp up with the head yards sharper", "trim sails with the
# head yards sharper" (vocabulary.yaml, `phrase_modifiers`).
HEAD_YARDS_SHARPER = "head_sharper"
# Adjacent yards (spec 3b §5): however near two yards' lengths, the small trims of
# §2.2 always pass. Spec 3b §5's floor.
ADJACENT_YARD_FLOOR_DEG = 10.0
# Studding sail booms and the lee rigging (spec 3b §7). A boom rigged out on a yard braced
# up runs out beyond the yardarm that is braced aft, the lee one, and past this angle from
# square it lies against the lee topmast rigging and backstays. Judgement (spec 3b §7): the
# model has no spar collision to find it, and no source gives the angle; half a right angle,
# where the lee yardarm has come aft of the shrouds' spread. The weather boom points forward
# and is not fouled: Luce's weather studding sails are set a point free, with the yards
# braced up (Luce 1866 ch. XXIII, line 26509). The one hard rule of the studding sails.
BOOM_FOUL_BRACE_DEG = 45.0
# Sail verbs whose evolution is a script that works on the sail it is given
# (`params["sail"]`), and which make sense for a sail that is blown out.
SAIL_SCRIPT_VERBS = ("bend", "unbend", "shift")
# The grammar's words for which sail the sail room gives (spec 3b §6.3), passed to the script.
CANVAS_PARAMS = ("canvas_no", "heavy", "for")
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
        "afresh": "'afresh' belongs with 'reeve'",
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


def _refused(name: str, e: OrderError) -> str:
    """One part's refusal for the order's line: 'the fore royal: the yard is sent down'.
    A party too small for the work names the work itself, and stands alone (package
    29c): 'The idlers are four; reefing the mainsail wants ten. ...'."""
    if isinstance(e, PartyTooSmall):
        return str(e)
    return f"{name}: {e}"


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
    if verb in SAIL_SCRIPT_VERBS:
        allowed |= set(CANVAS_PARAMS)  # which sail from the sail room (spec 3b §6.3)
    _no_stray_modifiers(order, allowed)
    res = resolve.resolve(ship, order.object or "", order.side_word, verb)
    mapping: dict[str, str] = vocab.evolutions.get(verb, {})
    if verb == "furl":
        # a jib, a staysail or a studding sail (the water sail among them), which is not
        # furled on a spar, is handed and stowed: `furl` takes it in, as the captain means
        # (package 37l; the review of gate 5c's playtests, G17: "furl the jibs" was
        # answered "take it in"); a gaff sail keeps its refusal, which names its own words
        take_in = vocab.evolutions.get("take in", {})
        handed = {c: take_in[c] for c in FURLED_AS_TAKEN_IN if c in take_in}
        mapping = {**handed, **mapping}
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
            failed.append(_refused(resolve.the(ship, sail.id), e))
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


# The classes of sail that `furl` takes in (package 37l): handed and stowed, not furled on
# a spar.
FURLED_AS_TAKEN_IN = ("jibheaded", "studding")


def _sail_params(order: Order) -> dict[str, Any]:
    params: dict[str, Any] = {}
    if order.verb in SAIL_SCRIPT_VERBS:
        params.update({k: order.modifiers[k] for k in CANVAS_PARAMS if k in order.modifiers})
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
    if sail.wrecked and verb != "unbend":
        # the refusal is the way out (package 30b): the wreck is cut away, or the sail cut
        # out of it and unbent; the spar is shifted for a spare
        root = scripts.wreck_root(ship, sail)
        if root is None:
            return f"{name} is wrecked"
        spar = resolve.the(ship, root.id)
        return (
            f"{name} went with {spar} when it carried away; cut away the wreck, then shift "
            f"{spar} for a spare"
        )
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
                n_in = sail.reef_bands  # "(1 reef in)", "(4 reefs in)": package 33c
                return f"{name} is already close reefed ({n_in} reef{'s' if n_in != 1 else ''} in)"
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
        body += " Not done: " + "; ".join(f.rstrip(".") for f in failed) + "."
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
    _no_stray_modifiers(
        order, {"brace_mode", "tack", "manner", "round", "hands_from", HEAD_YARDS_SHARPER}
    )
    verb = order.verb
    mode = order.modifiers.get("brace_mode")
    tack = order.modifiers.get("tack")
    if verb == "back" and order.object:
        backed = _back_headsails(ship, order, vocab)
        if backed is not None:
            return backed
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
        yards = []
        refusal: OrderError | None = None
        for pid in res.ids:
            try:
                yard = _yard_for(ship, pid)
            except OrderError as e:
                # a group of sails ("square the sails", package 33c): its square sails'
                # yards are braced and the fore-and-aft sails passed over; one sail named
                # alone is refused in words, as before
                refusal = refusal or e
                continue
            if yard not in yards:
                yards.append(yard)
        if refusal is not None and (len(res.ids) == 1 or not yards):
            raise refusal
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

    sync_catharpins(ship)  # the limits as the lower rigging stands now
    runner = runner_of(ship)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    workable = [y for y in yards if not (y.wrecked or y.sent_down)]
    # Where each yard goes: the mode's angle within its limit; sharp up on a wind
    # across the masts, the after yards sharper than the head yards (spec 3b §2.2).
    targets: dict[str, float] = {}
    for yard in workable:
        target_deg = vocab.brace_modes[mode]
        target = yard.brace_limit if isinstance(target_deg, str) else units.deg_to_rad(target_deg)
        targets[yard.id] = min(abs(target), yard.brace_limit)
    trimmed: float | None = None
    if vocab.brace_modes[mode] == "limit" and not aback:
        targets, trimmed = yard_trim.stagger(
            ship, targets, bool(order.modifiers.get(HEAD_YARDS_SHARPER))
        )
    signed = yard_trim.signed(targets, sign)
    # Checked last, after the whole-mast aback rule above, so nothing is refused twice: a
    # yard whose lee studding sail boom is out first (spec 3b §7), then the adjacent yards.
    too_far = _yard_refusals(ship, signed)
    workable = [y for y in workable if y.id not in too_far]
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
        if yard.id in too_far:
            failed.append(too_far[yard.id])
            failed_ids.append(yard.id)
            continue
        target = signed[yard.id]
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
            failed.append(_refused(name, e))
            failed_ids.append(yard.id)
            continue
        started.append({"evolution": "brace", "subject": yard.id, "params": params})
    _settle_call(ship, call, bool(started))
    if not started:
        if len(failed_ids) == 1 and failed_ids[0] in too_far:
            raise OrderError(too_far[failed_ids[0]])
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, "brace", object_name, started, texts, failed)
    how = yard_trim.difference_words(trimmed)
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
        note = f"Braced round for the {tack} tack{', ' + how if how else ''}."
        ship.note("routine", "yard.braced_round", note, data={"tack": tack})
    elif how:
        # sharp up across the masts: the log names the trim (spec 3b §2.2)
        note = f"Braced up for the {tack} tack, {how}."
        ship.note("routine", "yard.braced_up", note, data={"tack": tack, "difference": trimmed})
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
    would be, so the whole rig swings together.

    On a wind, when the lower yards would go sharper than their limits allow, the
    yards are staggered as `brace sharp up` staggers them (`trim.stagger`): the after
    yards up to `AFTER_YARDS_SHARPER_DEG` sharper than the head yards as their rigging
    allows, or the after yards eased that much with 'head yards sharper' (spec 3b §2.2,
    Fincham arts. 94 and 96)."""
    from freesail.physics.sails import SAIL_CLASSES

    named_sheets: list[Sail] | None = None  # "trim the jib": that sail's sheet only
    if order.verb == "trim":
        _no_stray_modifiers(order, {"manner", "hands_from", HEAD_YARDS_SHARPER})
        # "trim sails with the head yards sharper" trims yards and sheets alike
        phrase = order.verb_phrase.split(" with the ")[0].replace(" head yards sharper", "")
        do_yards = "sheet" not in phrase
        do_sheets = "yard" not in phrase
        if order.object is not None:
            # "trim the <sail>" (spec M4 §7): that sail's sheet, and its yard's brace if it
            # is square; "trim the topsails" and "trim the fore yard" likewise
            res = resolve.resolve(ship, order.object, order.side_word, "trim")
            yards, named_sheets = _trim_targets(ship, res)
            do_yards, do_sheets = bool(yards), bool(named_sheets)
            object_name = res.name
    else:
        do_yards, do_sheets = True, False  # "brace ... to the wind"
    head_sharper = bool(order.modifiers.get(HEAD_YARDS_SHARPER))
    d = ship.dyn
    if lying_to(ship) and (
        (order.verb == "trim" and order.object is None)
        or (order.verb != "trim" and yards is not None and _every_yard(ship, yards))
    ):
        # the owner's ruling of 2026-10-07 (package 37f; the review of gate 5c's
        # playtests, 5.7: `trim sails` filled a ship that was hove to, four times in two
        # games, her backed yards braced round with the rest and the record left standing):
        # the trim of the whole ship declines while she lies to, as `steer` and `keep her
        # full` do; a yard braced by name and a sheet hauled by name are still taken
        if do_sheets and not do_yards:  # "trim the sheets": the cure is a sheet's
            raise OrderError(HOVE_TO_TRIM_SHEETS_WORDS)
        raise OrderError(HOVE_TO_TRIM_WORDS)
    if d.apparent_wind_speed < 0.5:
        raise OrderError("There is no wind to trim to.")
    awa = abs(d.apparent_wind_angle)
    sign = 1.0 if d.tack == "starboard" else -1.0

    started: list[dict[str, Any]] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    staggered: float | None = None
    too_far: dict[str, str] = {}  # yards refused by the adjacent-yards rule, with the reason
    folded: list[str] = []  # yards whose trim in hand, not yet begun, takes the new angle
    busy: list[str] = []  # yards being braced to the wind now: that trim stands
    down: list[Spar] = []  # yards sent down on deck: said as a clause, not a refusal
    gone: list[Spar] = []  # yards carried away, likewise
    if do_yards:
        sync_catharpins(ship)  # the limits as the lower rigging stands now
        runner = runner_of(ship)
        if yards is None:
            yards = [y for y in ship.spars.values() if y.is_yard and y.id not in skip]
        # a trim in hand is not stacked behind (package 29b: a standing order that trims on a
        # shift, firing while the watch is at the braces): a yard still waiting its turn
        # takes the new angle, and one being braced now is left to finish
        in_hand = {
            i.subject_id: i
            for i in getattr(runner, "instances", ())
            if i.evo.id == vocab.evolutions["brace"] and i.params.get("mode") == "to the wind"
        }
        workable = [y for y in yards if not (y.wrecked or y.sent_down)]
        targets: dict[str, float] = {}
        on_a_wind = True  # every lower yard wants to go sharper than it can
        for yard in workable:
            sail = ship.sail_of(yard)
            cls = SAIL_CLASSES.get(sail.cls if sail else "square") or SAIL_CLASSES["square"]
            chord = min(max(awa - cls.peak_alpha, 0.0), math.pi / 2)
            want = math.pi / 2 - chord
            targets[yard.id] = min(want, yard.brace_limit)
            parent = ship.parent_of(yard)
            if parent is not None and parent.cls == "mast" and want < yard.brace_limit - 1e-9:
                on_a_wind = False
        if on_a_wind:
            targets, staggered = yard_trim.stagger(ship, targets, head_sharper)
        signed = yard_trim.signed(targets, sign)
        too_far = _yard_refusals(ship, signed)
        extra, call = _hands_params(
            ship,
            order,
            [vocab.evolutions["brace"]] * len([y for y in workable if y.id not in too_far]),
            _group_label("brace", object_name, group) if len(workable) > 1 else None,
        )
        # the trim's braces log one line when the last is done (package 29b, playtest 7:
        # twelve lines as each began and twelve as each ended); this order's own line
        # says what was ordered
        new_group = getattr(runner, "new_log_group", None)
        if len(workable) > 1 and new_group is not None:
            extra = {**extra, "log_group": new_group()}
        for yard in yards:
            name = resolve.the(ship, yard.id)
            if yard.wrecked or yard.sent_down:
                # said as one clause of the line, "the topgallant and royal yards are on
                # deck", not as a "Not ..." list (package 31b; playtest 11's finding 8)
                failed.append(f"{name} is {'carried away' if yard.wrecked else 'sent down'}")
                failed_ids.append(yard.id)
                (gone if yard.wrecked else down).append(yard)
                continue
            if yard.id in too_far:
                failed.append(too_far[yard.id])
                failed_ids.append(yard.id)
                continue
            target = signed[yard.id]
            params = {
                "target_deg": round(units.rad_to_deg(target), 2),
                "target_angle": target,
                "mode": "to the wind",
                "tack": d.tack,
                **extra,
            }
            waiting = in_hand.get(yard.id)
            if waiting is not None:
                if waiting.waiting and waiting.step_index < 0:
                    for key in ("target_deg", "target_angle", "tack"):
                        waiting.params[key] = params[key]
                    folded.append(yard.id)
                else:
                    busy.append(yard.id)
                continue
            try:
                runner.start(ship, vocab.evolutions["brace"], yard.id, params)
            except OrderError as e:
                failed.append(_refused(name, e))
                failed_ids.append(yard.id)
                continue
            started.append({"evolution": "brace", "subject": yard.id, "params": params})
        _settle_call(ship, call, bool(started))

    trimmed: list[str] = []  # the sheets whose trim was started (package 32e)
    standing: list[str] = []  # the sheets already at their trim
    sheets_started: list[dict[str, Any]] = []
    if do_sheets:
        # the sheet holds the trim (package 32e, spec M5 open item 13): each set
        # fore-and-aft sail's sheet is worked to the wind by its own evolution, with hands
        # and time; a sheet within a degree of its trim, belayed to leeward, stands
        sheet_evos = vocab.evolutions.get("trim") or {}
        candidates = [
            sail
            for sail in (named_sheets if named_sheets is not None else ship.sails.values())
            if sail.is_set and sail.is_fore_and_aft and sail.cls in sheet_evos
        ]
        runner = runner_of(ship)
        if do_yards:
            extra_s = {k: v for k, v in extra.items() if k != "log_group"}
            call_s = None
        else:
            extra_s, call_s = _hands_params(
                ship,
                order,
                [sheet_evos[sl.cls] for sl in candidates],
                _group_label("trim", "sheets", group) if len(candidates) > 1 else None,
            )
        new_group = getattr(runner, "new_log_group", None)
        if len(candidates) > 1 and new_group is not None:
            extra_s = {**extra_s, "log_group": new_group()}
        for sail in candidates:
            name = resolve.the(ship, sail.id)
            wanted = yard_trim.wanted_sheet_angle(sail.cls, d.apparent_wind_angle)
            reading = yard_trim.read_sheet(ship, sail)
            if (
                not reading.free
                and not reading.held_to_windward
                and abs(reading.angle - wanted) <= SHEET_TRIM_TOLERANCE
            ):
                standing.append(name)
                continue
            params = {"sail": sail.id, "angle_deg": None, "side": None, **extra_s}
            try:
                runner.start(ship, sheet_evos[sail.cls], sail.id, params)
            except OrderError as e:
                failed.append(_refused(name, e))
                failed_ids.append(sail.id)
                continue
            sheets_started.append(
                {"evolution": sheet_evos[sail.cls], "subject": sail.id, "params": params}
            )
            trimmed.append(name)
        _settle_call(ship, call_s, bool(trimmed))

    in_hand_words = ""
    if folded or busy:
        n = len(folded) + len(busy)
        in_hand_words = f"the {'yard is' if n == 1 else 'yards are'} being trimmed already" + (
            f", {len(folded)} still to brace taking the new angle" if folded else ""
        )
    if not started and not trimmed and not standing:
        if len(failed_ids) == 1 and failed_ids[0] in too_far:
            raise OrderError(too_far[failed_ids[0]])
        if in_hand_words and not folded:
            raise OrderError(f"{in_hand_words[0].upper()}{in_hand_words[1:]}; the trim stands.")
        if failed and not folded:
            raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
        if not folded:
            raise OrderError(
                "Nothing to trim: no sail is set." if do_sheets else "No yards to trim."
            )

    parts: list[str] = []
    if started:
        which = (
            f"the {object_name}"
            if object_name != "yards"
            else f"{number_words(len(started))} yard{'s' if len(started) != 1 else ''}"
        )
        how = yard_trim.difference_words(staggered)
        parts.append(
            f"Braced {which} to the wind, {units.rad_to_deg(awa):.0f}° "
            f"{units.wind_bearing_words(awa if d.tack == 'starboard' else -awa)}"
            + (f", {how}" if how else "")
        )
    if trimmed:
        sheets = "sheet" if len(trimmed) == 1 and named_sheets is not None else "sheets"
        parts.append(f"trimming the {sheets} of {errors.join_names(trimmed, 'and')}")
    if standing:
        sheets = "sheet" if len(standing) == 1 else "sheets"
        verb_s = "stands" if len(standing) == 1 else "stand"
        parts.append(f"the {sheets} of {errors.join_names(standing, 'and')} {verb_s} as trimmed")
    if in_hand_words:
        parts.append(in_hand_words)
    off_deck = _yards_off_words(ship, down, gone)
    if off_deck:
        parts.append(off_deck)
    text = "; ".join(parts)
    text = text[0].upper() + text[1:] + "."
    off_ids = {y.id for y in down + gone}
    refused = [f for f, i in zip(failed, failed_ids, strict=True) if i in too_far]
    others = [
        f for f, i in zip(failed, failed_ids, strict=True) if i not in too_far and i not in off_ids
    ]
    if others:
        text += f" Not {errors.sentence_list(others)}."
    if refused:
        text += " " + " ".join(refused)
    data = {
        "verb": order.verb,
        "level": 1,
        "subjects": [s["subject"] for s in started + sheets_started],
        "evolutions": started + sheets_started,
        "trimmed_sheets": trimmed,
        "standing_sheets": standing,
        "failed": failed,
        "failed_subjects": failed_ids,
        "folded": folded,
        "in_hand": busy,
    }
    if order.verb != "trim":
        data.update({"object": object_name, "mode": "to the wind", "tack": d.tack})
    # an order whose braces log as one line logs its own line too (the runner writes no
    # "Man the braces" for them)
    grouped = any(x["params"].get("log_group") for x in started)
    yards_only = started and not trimmed and not standing and not grouped
    kind = "evolution.started" if yards_only else "sail.trimmed"
    return kind, text, data


# What a trim of the whole ship is answered with while she is hove to (package 37f; the
# owner's ruling): the words carry the cure.
HOVE_TO_TRIM_WORDS = "She is hove to; fill away before trimming, or brace a yard by name."
HOVE_TO_TRIM_SHEETS_WORDS = (
    "She is hove to, and the watch tends her sheets; fill away before trimming them, or "
    "work a sheet by name."
)


def lying_to(ship: Ship) -> bool:
    """Whether she is hove to, or heaving to: the record on the ship
    (`ship.extra["hove_to"]`), or the manoeuvre in hand."""
    if "hove_to" in ship.extra:
        return True
    return any(
        inst.evo.id in ("heave_to", "lie_a_try") and inst.script is not None
        for inst in getattr(ship.extra.get("evolutions"), "instances", None) or ()
    )


def _every_yard(ship: Ship, yards: list[Spar]) -> bool:
    """Whether these are all the ship's yards (a trim of the whole ship, however said)."""
    every = [s for s in ship.spars.values() if s.is_yard]
    return len(every) > 1 and {y.id for y in yards} >= {y.id for y in every}


def _trim_targets(ship: Ship, res: resolve.Resolution) -> tuple[list[Spar], list[Sail]]:
    """What "trim the <sail>" lays hands on (spec M4 §7): for a square sail (or a
    studding sail) the yard it hangs from, braced to the wind; for a fore-and-aft sail
    its sheet; for a yard named outright, the yard. A sail not set has nothing to trim
    and is refused in words; a mixed group ("the topsails") is taken as it comes."""
    yards: list[Spar] = []
    sheets: list[Sail] = []
    not_set: list[str] = []
    for pid in res.ids:
        part = ship.parts[pid]
        name = resolve.the(ship, pid)
        if isinstance(part, Spar):
            if not part.is_yard:
                raise OrderError(
                    f"{name[0].upper()}{name[1:]} is not a yard; trim a sail or a yard."
                )
            if part not in yards:
                yards.append(part)
            continue
        if not isinstance(part, Sail):
            raise OrderError(f"{name[0].upper()}{name[1:]} is not a sail; trim a sail or a yard.")
        if not part.is_set:
            not_set.append(f"{name} is {part.describe_state()}")
            continue
        if part.is_fore_and_aft:
            sheets.append(part)
            continue
        yard = ship.yard_of(part)
        if yard is None:
            raise OrderError(f"{name[0].upper()}{name[1:]} has no yard to brace.")
        if yard not in yards:
            yards.append(yard)
    if not yards and not sheets:
        # nothing named is set: "the headsails" with every headsail furled, or one sail
        if len(not_set) == 1:
            raise OrderError(f"{not_set[0][0].upper()}{not_set[0][1:]}; there is no sail to trim.")
        raise OrderError(f"Nothing to trim: {errors.sentence_list(not_set)}.")
    return yards, sheets


def adjacent_yard_max_diff(lower: Spar, upper: Spar) -> float:
    """How far apart two adjacent yards on one mast may be braced while the sail
    between them is set, in radians (spec 3b §5, ADJACENT_YARD_MAX_DIFF_DEG).

    The upper sail's clews are sheeted to the lower yard's yardarms; braced apart,
    its foot is carried across the lower yard's lifts. The spec reads the arc from
    the yards themselves: the shorter yard's half-length over the longer's, taken as
    an angle (a topsail yard three-quarters of its lower yard gives 43 degrees),
    never less than ADJACENT_YARD_FLOOR_DEG so that the small trims of spec §2.2
    always pass. No source gives a figure (RigGeometryNotes §6)."""
    a, b = lower.length_m / 2.0, upper.length_m / 2.0
    short, long_ = min(a, b), max(a, b)
    arc = short / long_ if long_ > 0.0 else 0.0
    return max(units.deg_to_rad(ADJACENT_YARD_FLOOR_DEG), arc)


_SPREAD = (SailState.SET, SailState.GOOSE_WINGED, SailState.SHEETED)  # clews at the yardarms


def _pending_braces(ship: Ship) -> dict[str, float]:
    """Where yards already ordered round are going: a brace evolution's target."""
    runner = ship.extra.get("evolutions")
    out: dict[str, float] = {}
    for inst in getattr(runner, "instances", None) or []:
        evo = getattr(inst, "evo", None)
        params = getattr(inst, "params", {}) or {}
        if getattr(evo, "id", None) == "brace" and "target_angle" in params:
            out[inst.subject_id] = float(params["target_angle"])
    return out


def _yard_refusals(ship: Ship, proposed: dict[str, float]) -> dict[str, str]:
    """Yards an order may not brace where it would, each with the one reason: first a
    studding sail boom out on the yardarm that would go aft beyond BOOM_FOUL_BRACE_DEG
    (spec 3b §7), then the adjacent-yards rule (spec 3b §5) for the rest, which judges
    the yards refused as lying where they are. So nothing is refused twice."""
    booms = _boom_refusals(ship, proposed)
    rest = {yid: a for yid, a in proposed.items() if yid not in booms}
    return {**booms, **_adjacent_refusals(ship, rest)}


def _lee_side(angle: float) -> str | None:
    """The side whose yardarm goes aft with the yard at this signed brace angle."""
    if abs(angle) < 1e-9:
        return None
    return "larboard" if angle > 0 else "starboard"  # + : starboard yardarm forward


def _pending_rig_outs(ship: Ship) -> set[str]:
    """The booms already ordered out: a rig-out evolution in hand or waiting."""
    runner = ship.extra.get("evolutions")
    return {
        inst.subject_id
        for inst in getattr(runner, "instances", None) or []
        if getattr(getattr(inst, "evo", None), "id", None) == "rig_out_studdingsail_boom"
    }


def _booms_out(ship: Ship, yard: Spar) -> list[Spar]:
    """The studding sail booms rigged out (or ordered out) on this yard."""
    going = _pending_rig_outs(ship)
    return [
        b
        for b in ship.spars.values()
        if b.cls == "studdingsail_boom"
        and b.parent == yard.id
        and not b.wrecked
        and (b.rigged_out or b.id in going)
    ]


def _boom_refusals(ship: Ship, proposed: dict[str, float]) -> dict[str, str]:
    """Yards this order would brace beyond BOOM_FOUL_BRACE_DEG from square with the
    studding sail boom on the yardarm going aft rigged out: the boom would lie against
    the lee rigging (spec 3b §7). Bracing no sharper than a yard lies is never refused."""
    foul = units.deg_to_rad(BOOM_FOUL_BRACE_DEG)
    out: dict[str, str] = {}
    for yid, target in proposed.items():
        yard = ship.spars[yid]
        if abs(target) <= foul + 1e-6:
            continue
        now = yard.brace_angle
        if now * target > 0 and abs(target) <= abs(now) + 1e-6:
            continue  # coming in, or holding, on the same side
        lee = _lee_side(target)
        if any(b.side == lee for b in _booms_out(ship, yard)):
            out[yid] = (
                f"Rig in the studdingsail boom before bracing the "
                f"{resolve.display_name(ship, yid)} sharper."
            )
    return out


def boom_fouled_by_brace(ship: Ship, boom: Spar) -> str | None:
    """Why this studding sail boom cannot be rigged out now, or None: its yard braced (or
    ordered braced) beyond BOOM_FOUL_BRACE_DEG with this boom's yardarm the one aft
    (spec 3b §7)."""
    yard = ship.parent_of(boom)
    if yard is None or not yard.is_yard:
        return None  # the ringtail boom runs out on the spanker's boom
    angle = _pending_braces(ship).get(yard.id, yard.brace_angle)
    if abs(angle) <= units.deg_to_rad(BOOM_FOUL_BRACE_DEG) + 1e-6:
        return None
    if boom.side != _lee_side(angle):
        return None
    return f"The {resolve.display_name(ship, yard.id)} is braced too sharp for the boom to go out."


def _adjacent_refusals(ship: Ship, proposed: dict[str, float]) -> dict[str, str]:
    """Yards this order would brace too far from the yard above or below them on the
    same mast while the sail between them is set (spec 3b §5), each with the reason.

    `proposed` maps yard ids to the signed angles the order gives them; every other
    yard is taken where it is going (an order already given) or where it lies. The
    whole-mast aback rule and the studding sail boom rule come before this in the
    orders that have them, so a yard is not refused twice."""
    pending = _pending_braces(ship)

    def angle(y: Spar) -> float:
        return proposed.get(y.id, pending.get(y.id, y.brace_angle))

    masts: list[Spar] = []
    for yid in proposed:
        mast = ship.mast_of(ship.spars[yid])
        if mast is not None and mast not in masts:
            masts.append(mast)
    out: dict[str, str] = {}
    for mast in masts:
        on_mast = sorted(
            (
                y
                for y in ship.spars.values()
                if y.is_yard and not (y.wrecked or y.sent_down) and ship.mast_of(y) is mast
            ),
            key=lambda y: y.height_m,
        )
        for lower, upper in zip(on_mast, on_mast[1:], strict=False):
            if lower.id not in proposed and upper.id not in proposed:
                continue
            sail = ship.sail_of(upper)
            if sail is None or sail.wrecked or sail.state not in _SPREAD:
                continue
            apart = abs(angle(upper) - angle(lower))
            allowed = adjacent_yard_max_diff(lower, upper)
            if apart <= allowed + 1e-6:
                continue
            moved, other = (upper, lower) if upper.id in proposed else (lower, upper)
            if moved.id in out:
                continue
            sail_name = resolve.display_name(ship, sail.id)
            mast_word = resolve.display_name(ship, mast.id).replace(" mast", "")
            out[moved.id] = (
                f"The {resolve.display_name(ship, moved.id)} cannot be braced so far from the "
                f"{resolve.display_name(ship, other.id)} while the {sail_name} is set "
                f"({units.rad_to_deg(apart):.0f}° apart, {units.rad_to_deg(allowed):.0f}° at "
                f"most); brace the {mast_word} yards together, or clew up the {sail_name}."
            )
    return out


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
        parted = [ln for ln in ship.sheets_of(sail) if ln.state is LineState.PARTED]
        if parted:
            # a sail is not sheeted home on a sheet that is gone (package 31b, playtest
            # 11's finding 7): the one sheet left would only make it flog the worse
            names = errors.join_names([resolve.the(ship, ln.id) for ln in parted], "and")
            verb = "is" if len(parted) == 1 else "are"
            failed.append(f"{names} {verb} parted; reeve a new one before {name} is sheeted home")
            continue
        sheets = list(ship.sheets_of(sail))
        if not sheets:
            failed.append(f"{name} has no sheet to haul")
            continue
        moved = False
        if sail.is_fore_and_aft:
            # flat aft: the working sheet hauled to the sail's floor (package 32e)
            reading = yard_trim.read_sheet(ship, sail)
            geo = yard_trim.sheet_geometry(ship, sail)
            if reading.free or reading.held_to_windward or reading.angle > geo.floor + 1e-6:
                yard_trim.set_sheet_angle(ship, sail, geo.floor)
                moved = True
        else:
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
            texts.append(
                f"Hauled the {resolve.display_name(ship, sail.id)} sheet flat aft; {name} "
                f"{yard_trim.angle_words(sail.sheet_angle)}."
            )
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
    # Hauling a bowline is work for hands (spec 3b §4), so it may name them; and a
    # bowline hauled is the weather one unless a side is said ("haul the fore bowline").
    bowlines_hauled = verb == "haul" and "bowline" in (order.object or "")
    allowed = {"fathoms", "a_little", "manner", "home", "sheet_to"}
    _no_stray_modifiers(order, allowed | ({"hands_from"} if bowlines_hauled else set()))
    sheet_to = order.modifiers.get("sheet_to")  # "to windward", "to leeward" (package 32e)
    if sheet_to and verb not in ("haul", "ease"):
        raise OrderError(f"'{verb}' was understood, but 'to windward' belongs with 'haul'.")
    if "home" in order.modifiers and verb != "haul":
        raise OrderError(f"'{verb}' was understood, but 'home' and 'aft' belong with 'haul'.")
    side_word = order.side_word
    if bowlines_hauled and side_word is None:
        side_word = "weather"
    res = resolve.resolve(ship, order.object or "", side_word, verb)
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
    if verb == "haul" and any(ln.cls == "bowline" for ln in lines):
        return _haul_bowlines(ship, order, vocab, res, lines)
    lines = _pick_sheets(ship, lines, verb, res.side is not None, sheet_to)

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
            text, change = _one_line(ship, line, verb, steps, name, sheet_to)
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


def _pick_sheets(
    ship: Ship, lines: list[Line], verb: str, side_said: bool, sheet_to: str | None
) -> list[Line]:
    """Of a fore-and-aft sail's pair of sheets named without a side (package 32e), the
    one the order means: the lee sheet (the working one), the weather sheet 'to
    windward', and for 'let go' whichever is belayed. Other lines pass as they are."""
    out: list[Line] = []
    pairs: dict[str, list[Line]] = {}
    for ln in lines:
        target = ship.parts.get(ln.of)
        sheet = ln.cls == "sheet" and isinstance(target, Sail) and target.is_fore_and_aft
        if sheet and ln.side is not None and not side_said:
            pairs.setdefault(target.id, []).append(ln)
        else:
            out.append(ln)
    for sid, pair in pairs.items():
        sail = ship.sails[sid]
        if len(pair) < 2:
            out.extend(pair)
        elif sheet_to:
            chosen = yard_trim.working_sheet(ship, sail, sheet_to)
            out.append(chosen if chosen is not None else pair[0])
        elif verb == "let go":
            belayed = [ln for ln in pair if ln.state is LineState.BELAYED]
            out.extend(belayed or pair)
        else:
            chosen = yard_trim.working_sheet(ship, sail, None)
            out.append(chosen if chosen is not None else pair[0])
    return out


def _one_line(
    ship: Ship, line: Line, verb: str, steps: float, name: str, sheet_to: str | None = None
) -> tuple[str, dict[str, Any]]:
    """Work one line; the sentence and the change, or OrderError with the reason."""
    if line.state is LineState.PARTED:
        raise OrderError(
            f"{name[0].upper()}{name[1:]} is parted; it must be spliced or rove afresh."
        )
    target = ship.parts.get(line.of)
    fore_and_aft_sheet = line.cls == "sheet" and isinstance(target, Sail) and target.is_fore_and_aft
    if verb == "let go":
        if line.state is LineState.FREE:
            raise OrderError(f"{name[0].upper()}{name[1:]} is already running free.")
        line.state = LineState.FREE
        if fore_and_aft_sheet:
            # let fly: the sheet runs out; the sail flogs unless its other sheet holds it
            line.hauled = 0.0
            line.held_side = None
            reading = yard_trim.refresh_reading(ship, target)
            sail_name = resolve.the(ship, target.id)
            if reading.free:
                target.shivering = True
                text = f"Let fly {name}; {sail_name} flogging."
            else:
                where = yard_trim.side_name(reading.side or 1.0)
                text = (
                    f"Let go {name}; {sail_name} lies to {where}, "
                    f"{yard_trim.angle_words(reading.angle)}."
                )
            return text, {"line": line.id, "state": "free", "sail": target.id}
        return f"Let go {name}; it ran free.", {"line": line.id, "state": "free"}
    if verb == "belay":
        line.state = LineState.BELAYED
        if fore_and_aft_sheet:
            yard_trim.refresh_reading(ship, target)
        return f"Belayed {name}.", {"line": line.id, "state": "belayed"}
    if fore_and_aft_sheet:
        return _work_sheet(ship, line, target, verb == "haul", steps, name, sheet_to)
    text, change = _haul_or_ease(ship, line, verb == "haul", steps, name)
    line.state = LineState.BELAYED
    return text, change


def _work_sheet(
    ship: Ship,
    line: Line,
    sail: Sail,
    hauling: bool,
    steps: float,
    name: str,
    sheet_to: str | None,
) -> tuple[str, dict[str, Any]]:
    """Haul or ease a fore-and-aft sail's sheet a fathom of its fall (times `steps`), or
    flat aft and right off, and read the sail's angle from it (package 32e). Hauled 'to
    windward' the sheet holds the sail aback on the weather side; of a pair, hauling one
    sheet lets the other run. Returns the sentence and the change."""
    geo = yard_trim.sheet_geometry(ship, sail)
    home = math.isinf(steps)
    did = "Hauled" if hauling else "Eased"
    recover = hauling and line.state is LineState.FREE
    was = line.hauled if line.state is not LineState.FREE else 0.0
    if home or (sheet_to == "weather" and hauling and steps == 1.0):
        # flat aft, right off; a sheet hauled over to windward is hauled aft with it
        new = 1.0 if hauling else 0.0
    else:
        fall = steps * yard_trim.FATHOM_M / geo.scope_m
        new = max(0.0, min(1.0, was + (fall if hauling else -fall)))
    sail_name = resolve.the(ship, sail.id)
    if abs(new - was) < 1e-9 and not recover and not sheet_to:
        state = "hard in" if hauling else "eased right off"
        raise OrderError(f"{name[0].upper()}{name[1:]} is already {state}.")
    line.hauled = new
    line.state = LineState.BELAYED
    if line.side is None:
        # a boom's one sheet: held over to windward when so ordered, else lying to leeward
        lee = yard_trim.side_name(yard_trim.lee_side_sign(ship))
        weather = "larboard" if lee == "starboard" else "starboard"
        if sheet_to == "weather":
            line.held_side = weather
        elif sheet_to == "lee" or not hauling:
            line.held_side = None
    else:
        # of a pair, the sheet worked is the one that holds the sail: the other runs
        for other in ship.sheets_of(sail):
            if other is not line and other.state is LineState.BELAYED:
                other.state = LineState.FREE
                other.hauled = 0.0
    reading = yard_trim.refresh_reading(ship, sail)
    sail.shivering = False
    how = ""
    if home:
        how = " flat aft" if hauling else " right off"
    elif sheet_to == "weather":
        how = " to windward"
    elif sheet_to == "lee":
        how = " to leeward"
    if abs(new - was) < 1e-9 and recover:
        did = "Hauled"
        how = " taut and belayed it"
    aback = "; aback" if reading.held_to_windward else ""
    text = f"{did} {name}{how}; {sail_name} now {yard_trim.angle_words(reading.angle)}{aback}."
    change = {
        "line": line.id,
        "sail": sail.id,
        "hauled": round(new, 3),
        "sheet_angle": reading.angle,
        "held_to_windward": reading.held_to_windward,
    }
    return text, change


def _draw(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Draw jib', 'let draw the jib' (Luce 1884, ch. XXIV, 'Missing Stays'; ch. XXXIV,
    'Sloops'): a fore-and-aft sail held to windward, or with its sheets let fly, is let
    draw: its lee sheet hauled aft to its trim and the weather one let go. Level 0, at
    once (package 32e)."""
    _no_stray_modifiers(order, {"manner"})
    res = resolve.resolve(ship, order.object or "", order.side_word, "draw")
    texts: list[str] = []
    failed: list[str] = []
    changes: list[dict[str, Any]] = []
    for pid in res.ids:
        part = ship.parts[pid]
        if not isinstance(part, Sail) or not part.is_fore_and_aft:
            raise errors.wrong_kind(
                "draw", resolve.display_name(ship, pid), _what(ship, part), "sails", ""
            )
        name = resolve.the(ship, pid)
        if not part.is_set:
            failed.append(f"{name} is {part.describe_state()}")
            continue
        if not ship.sheets_of(part):
            failed.append(f"{name} has no sheet")
            continue
        reading = yard_trim.read_sheet(ship, part)
        wanted = yard_trim.wanted_sheet_angle(part.cls, ship.dyn.apparent_wind_angle)
        if (
            not reading.free
            and not reading.held_to_windward
            and abs(reading.angle - wanted) <= SHEET_TRIM_TOLERANCE
        ):
            failed.append(f"{name} is drawing already")
            continue
        angle = yard_trim.set_sheet_angle(ship, part, wanted, None)
        part.shivering = False
        texts.append(f"Let draw {name}; the lee sheet hauled aft, {yard_trim.angle_words(angle)}.")
        changes.append({"sail": pid, "sheet_angle": angle})
    if not changes:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:] + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = " ".join(texts)
    if failed:
        text += " Not done: " + errors.sentence_list(failed) + "."
    data = {
        "verb": "draw",
        "level": 0,
        "subjects": [c["sail"] for c in changes],
        "changes": changes,
    }
    return "line.hauled", text, data


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
    # the bowline last: it is hauled only on a wind, and the hint shows the first few
    names.sort(key=lambda n: n.endswith("bowline"))
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

    if line.cls == "brace" and isinstance(target, Spar):
        sync_catharpins(ship)  # the limit as the lower rigging stands now
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
        too_far = _yard_refusals(ship, {target.id: new}).get(target.id)
        if too_far is not None:
            raise OrderError(too_far)
        target.brace_angle = new
        text = f"{did} {name}; {resolve.the(ship, target.id)} now {_brace_words(new)}."
        return text, {"line": line.id, "yard": target.id, "brace_angle": new}

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


def _yard_kind(yard_id: str) -> str:
    """'topgallant' for fore.topgallant.yard, 'topsail', 'royal'; 'lower' for a lower yard
    (fore.yard, mizzen.crossjack.yard)."""
    words = yard_id.split(".")
    if len(words) < 3 or words[1] == "crossjack":
        return "lower"
    return words[1]


def _yard_kinds_words(ship: Ship, yards: list[Spar]) -> str:
    """'the topgallant and royal yards' when every yard of those kinds is named, else the
    yards by name: 'the fore topgallant yard and the royal yards'."""
    all_yards = [s for s in ship.spars.values() if s.is_yard]
    kinds: list[str] = []
    for y in all_yards:
        k = _yard_kind(y.id)
        if k not in kinds:
            kinds.append(k)
    named = {y.id for y in yards}
    whole: list[str] = []
    rest: list[str] = []
    for kind in kinds:
        of_kind = [y for y in all_yards if _yard_kind(y.id) == kind]
        mine = [y for y in of_kind if y.id in named]
        if not mine:
            continue
        if len(mine) == len(of_kind) and len(mine) > 1:
            whole.append(kind)
        else:
            rest.extend(resolve.the(ship, y.id) for y in mine)
    phrases = ([f"the {errors.join_names(whole, 'and', limit=8)} yards"] if whole else []) + rest
    return errors.join_names(phrases, "and", limit=8)


def _yards_off_words(ship: Ship, down: list[Spar], gone: list[Spar]) -> str:
    """The trim line's clause for the yards it could not brace because they are not aloft
    (package 31b; playtest 11's finding 8): 'the topgallant and royal yards are on deck',
    'the fore topgallant yard is carried away'."""
    clauses: list[str] = []
    if down:
        verb = "is" if len(down) == 1 else "are"
        clauses.append(f"{_yard_kinds_words(ship, down)} {verb} on deck")
    if gone:
        verb = "is" if len(gone) == 1 else "are"
        clauses.append(f"{_yard_kinds_words(ship, gone)} {verb} carried away")
    return " and ".join(clauses)


def _back_headsails(ship: Ship, order: Order, vocab: Vocabulary) -> Result | None:
    """`back the fore staysail` (package 37l; the review of gate 5c's playtests, G17): a
    headsail, which has no yard to lay aback, is backed by hauling its sheet over to
    windward, as `haul the fore staysail sheet to windward` does (package 32e; Luce 1884,
    ch. XXXIV, 'Sloops', 'To Heave to'). None when the object is not one or more
    jibs or staysails without a yard; the yards' own refusals then stand (a spanker or a
    gaff mainsail is not backed by this order)."""
    from freesail.orders.grammar import parse

    try:
        res = resolve.resolve(ship, order.object or "", order.side_word, order.verb)
    except OrderError:
        return None
    sails = [ship.parts.get(pid) for pid in res.ids]
    if not sails or not all(
        isinstance(s, Sail) and s.cls == "jibheaded" and ship.yard_of(s) is None for s in sails
    ):
        return None
    texts: list[str] = []
    done: list[dict[str, Any]] = []
    failed: list[str] = []
    kind = "line.order"
    for sail in sails:
        name = resolve.display_name(ship, sail.id)
        try:
            sheet = parse(ship, f"haul the {name} sheet to windward", vocab)
            kind, text, data = execute(ship, sheet, vocab)
        except OrderError as e:
            failed.append(_refused(f"the {name}", e))
            continue
        texts.append(text)
        done.append(data)
    if not done:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    head = f"Backed the {res.name}, its sheet hauled to windward: "
    text = head + " ".join(texts)
    if failed:
        text += " Not done: " + errors.sentence_list(failed) + "."
    return kind, text, {"verb": order.verb, "level": 0, "backed": done, "failed": failed}


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
# Level 1: bowlines and catharpins (milestone 3b, spec 3b §3 and §4)
# ---------------------------------------------------------------------------


def _bowline_check(ship: Ship, line: Line) -> str | None:
    """Why this bowline cannot be hauled out now, or None. A bowline hauls the
    weather leech of a sail that is drawing, with its yard braced up for that side."""
    name = resolve.the(ship, line.id)
    if line.state is LineState.PARTED:
        return f"{name} is parted; it must be spliced or rove afresh"
    if line.bowline_hauled:
        return f"{name} is hauled out already"
    sail = ship.parts.get(line.of)
    if not isinstance(sail, Sail):
        return f"{name} has no sail to haul out"
    sail_name = resolve.the(ship, sail.id)
    if sail.wrecked or sail.state not in (SailState.SET, SailState.GOOSE_WINGED):
        state = "wrecked" if sail.wrecked else sail.describe_state()
        return f"{sail_name} is {state}; there is no leech to haul out"
    yard = ship.yard_of(sail)
    if yard is None:
        return f"{sail_name} has no yard; a bowline hauls out a square sail's leech"
    yard_name = resolve.the(ship, yard.id)
    if abs(yard.brace_angle) < units.deg_to_rad(BOWLINE_SLACK_ANGLE_DEG):
        return (
            f"{yard_name} is braced in to {abs(units.rad_to_deg(yard.brace_angle)):.0f}°; "
            "a bowline will not stand off the wind"
        )
    weather = "starboard" if yard.brace_angle > 0 else "larboard"
    if line.side != weather:
        return (
            f"{name} is on the lee side of {yard_name}, which is braced up for the {weather} "
            "tack; it is the weather leech that is hauled out"
        )
    return None


def _haul_bowlines(
    ship: Ship, order: Order, vocab: Vocabulary, res: resolve.Resolution, lines: list[Line]
) -> Result:
    """'Haul the weather bowlines', 'steady out the bowlines', 'haul the fore bowline':
    one evolution per bowline, four hands and a minute each (data/evolutions/
    haul_bowline.yaml). A bowline that cannot be hauled now is reported, the rest
    are hauled."""
    others = [ln for ln in lines if ln.cls != "bowline"]
    if others:
        names = errors.join_names([resolve.display_name(ship, ln.id) for ln in others], "and")
        raise OrderError(
            f"The bowlines are hauled out by hands, each in turn; haul them in an order of "
            f"their own, and the {names} in another."
        )
    evo = vocab.evolutions["haul"]["bowline"]
    checks = {ln.id: _bowline_check(ship, ln) for ln in lines}
    to_haul = [ln for ln in lines if checks[ln.id] is None]
    failed = [checks[ln.id] or "" for ln in lines if checks[ln.id] is not None]
    failed_ids = [ln.id for ln in lines if checks[ln.id] is not None]
    if not to_haul:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:] + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    runner = runner_of(ship)
    extra, call = _hands_params(
        ship,
        order,
        [evo] * len(to_haul),
        _group_label("haul", res.name, None) if len(to_haul) > 1 else None,
    )
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    for ln in to_haul:
        try:
            texts.append(runner.start(ship, evo, ln.id, dict(extra)))
        except OrderError as e:
            failed.append(_refused(resolve.the(ship, ln.id), e))
            failed_ids.append(ln.id)
            continue
        started.append({"evolution": evo, "subject": ln.id, "params": dict(extra)})
    _settle_call(ship, call, bool(started))
    if not started:
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    said = order.verb_phrase
    head = "Steady out the bowlines!" if said == "steady out" else ""
    text = _summarise(ship, "haul", res.name, started, texts, failed)
    text = f"{head} {text}".strip()
    data = {
        "verb": "haul",
        "level": 1,
        "object": res.name,
        "side": res.side,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    return "evolution.started", text, data


def _catharpins(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Swifter in the catharpins [on the main]', 'ease the catharpins [on the main]':
    one evolution per lower mast, the boatswain's party's work (spec 3b §3). Without
    a mast named, every lower mast; the mast is read from the words of the order."""
    _no_stray_modifiers(order, {"manner", "hands_from"})
    swiftering = CATHARPIN_VERBS[order.verb]
    evo = vocab.evolutions[order.verb]
    words = order.verb_phrase.split()
    named = next(
        ({"mizen": "mizzen"}.get(w, w) for w in words if w in ("fore", "main", "mizzen", "mizen")),
        None,
    )
    masts = [s for s in ship.spars.values() if s.cls == "mast"]
    if named is not None:
        masts = [m for m in masts if m.id == f"{named}.mast"]
        if not masts:
            from freesail.evolutions.scripts import mast_inventory

            raise OrderError(f"She has no {named} mast; {mast_inventory(ship)}.")
    sync_catharpins(ship)
    count = number_words(int(round(CATHARPIN_GAIN_DEG)))
    failed: list[str] = []
    failed_ids: list[str] = []
    todo: list[tuple[Spar, str]] = []
    for mast in masts:
        name = resolve.the(ship, mast.id)
        if mast.wrecked:
            failed.append(f"{name} is carried away")
            failed_ids.append(mast.id)
            continue
        if swiftering and mast.swiftered_in:
            failed.append(f"the catharpins on {name} are swiftered in already")
            failed_ids.append(mast.id)
            continue
        if not swiftering and not mast.swiftered_in:
            failed.append(f"the catharpins on {name} are not swiftered in")
            failed_ids.append(mast.id)
            continue
        yards = [y for y in lower_yards(ship, mast) if y.rigged_brace_limit > 0]
        yard_names = errors.join_names([resolve.display_name(ship, y.id) for y in yards], "and")
        verb3 = "brace" if len(yards) != 1 else "braces"
        if not yards:
            gain = "; she has no yard on the lower mast there to brace the sharper"
        elif swiftering:
            gain = f"; the {yard_names} will brace {count} degrees sharper"
        else:
            gain = f"; the {yard_names} {verb3} as rigged again, {count} degrees less sharp"
        todo.append((mast, gain))
    if not todo:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:] + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    runner = runner_of(ship)
    label = "swiftering in the catharpins" if swiftering else "easing the catharpins"
    extra, call = _hands_params(ship, order, [evo] * len(todo), label if len(todo) > 1 else None)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    for mast, gain in todo:
        params = {"gain": gain, **extra}
        try:
            texts.append(runner.start(ship, evo, mast.id, params))
        except OrderError as e:
            failed.append(_refused(resolve.the(ship, mast.id), e))
            failed_ids.append(mast.id)
            continue
        started.append({"evolution": evo, "subject": mast.id, "params": params})
    _settle_call(ship, call, bool(started))
    if not started:
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = " ".join(t.strip() for t in texts if t)
    if failed:
        text += " Not done: " + "; ".join(failed) + "."
    data = {
        "verb": order.verb,
        "level": 1,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    return "evolution.started", text, data


# ---------------------------------------------------------------------------
# Helm
# ---------------------------------------------------------------------------


def _not_riding(ship: Ship, order: Order) -> None:
    """At anchor or aground (package 34) the helm has no say and a manoeuvre no meaning:
    the order is refused in words, so that a book's 'keep her full' does not steer a
    ship at anchor through the night."""
    extra = getattr(ship, "extra", None) or {}
    if extra.get("aground"):
        raise OrderError(f"She is aground; '{order.verb_phrase}' must wait till she floats.")
    tackle = extra.get("ground_tackle")
    if tackle is not None and tackle.at_anchor():
        raise OrderError(f"She is at anchor; '{order.verb_phrase}' must wait till she weighs.")


def _helm(ship: Ship, order: Order) -> Result:
    dyn = ship.dyn
    mods = order.modifiers
    verb = order.verb
    _no_stray_modifiers(order, {"heading", "points", "direction", "manner"})
    if verb in HELM_VERBS and ("heading" in mods or "points" in mods):
        raise OrderError(
            f"'{order.verb_phrase}' takes no heading or points; it is the whole order."
        )
    if lying_to(ship) and (
        verb in ("keep her full", "steer") or ("points" in mods and verb not in HELM_VERBS)
    ):
        # A ship hove to has her helm a-lee by the manoeuvre and her yards set against
        # each other; a course is given her by filling away, not by the helm alone.
        # Package 33a found the starter book's "keep her full" bearing the schooner away
        # from her noon sight, her yards still aback in the record, so that a later
        # "heave to" was refused and no cast was made (package 32e): the helm orders
        # that give a course are refused while she lies to; the conning words and the
        # bare helm ("hard a-weather") are the deck's to give. The same while the
        # manoeuvre is in hand (the lead, 2026-09-30: "keep her full" fired in the twenty
        # seconds between "heave to" and the yards aback, on every passage of gate 5b).
        raise OrderError("She is hove to; fill away before giving her a course.")

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
        if "heading" in mods and "points" in mods:
            # a course and a count of points in one order (package 37l: `steer south by
            # west half west` was steered west with "half" for a count of points): which
            # was meant cannot be told, and she is not steered on a guess
            raise OrderError(
                f"'{order.text}' gives a course ({mods.get('heading_text', '')}) and a "
                f"number of points ({_points_words(mods['points'])}); say one. A half or a "
                f"quarter point is said after the point it is reckoned from, toward "
                f"another: 'steer south by west half west', 'steer S by W 1/2 W'."
            )
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
    said_text = str(mods.get("heading_text", ""))
    if verb == "steer" and "heading" in mods and any(f in said_text for f in "¼½¾"):
        # a course with a half or a quarter point (package 37l) is shown as the card has
        # it, and not as the whole point nearest it
        shown = f"{said_text} ({units.rad_to_deg(target):.0f}°)"
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
            if said == "steady on":
                text = f"Helm ordered: steady on {shown}."
            elif said != "steady":
                text = f"Helm ordered: {said}; steady on {shown}."
        else:
            text = f"Helm ordered: {said}; met her swing with the helm, steady on {shown}."
        data.update({"helm_mode": HelmMode.HEADING.value, "target_heading": dyn.target_heading})
        return "helm.order", text, data
    dyn.helm_mode = HelmMode.RUDDER
    dyn.steady = False
    record = ship.extra.get("hove_to")
    if isinstance(record, dict):
        # lying to, the helm is the watch's to tend (package 37f); a conning word puts it
        # where the captain says and the watch leaves it there, tending the sheets alone,
        # until she fills away
        record["helm_by_order"] = True
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
    evolution works on the boom (Luce 1884, ch. XXIII: "Rig out! Hoist away!").

    Package 32b: a bowsprit is taken too, for 'rig out the bowsprit', 'reef the
    bowsprit' and 'run in the bowsprit', the evolutions of a cutter's running
    bowsprit (reef_bowsprit.yaml, rig_out_bowsprit.yaml), which refuse a standing
    one in words; the vocabulary maps the verb and the spar's class to the file."""
    _no_stray_modifiers(order, {"manner", "hands_from"})
    verb = order.verb
    res = resolve.resolve(ship, order.object or "", order.side_word, verb)
    mapping: dict[str, str] = vocab.evolutions.get(verb, {})
    booms: list[Spar] = []
    for pid in res.ids:
        part = ship.parts[pid]
        boom: Spar | None = None
        if isinstance(part, Spar) and part.cls in mapping:
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
    # a lee boom will not go out past the lee rigging (spec 3b §7); one out already is
    # left to the evolution's own reason
    fouled: dict[str, str] = {}
    if verb == "rig out":
        for boom in booms:
            if boom.cls != "studdingsail_boom":
                continue
            why = None if boom.rigged_out else boom_fouled_by_brace(ship, boom)
            if why is not None:
                fouled[boom.id] = why
    extra, call = _hands_params(
        ship,
        order,
        [mapping[b.cls] for b in booms if b.id not in fouled],
        _group_label(verb, res.name, group) if len(booms) > 1 else None,
    )
    for boom in booms:
        evo = mapping[boom.cls]
        if boom.id in fouled:
            failed.append(f"{resolve.the(ship, boom.id)}: {fouled[boom.id]}")
            failed_ids.append(boom.id)
            continue
        try:
            texts.append(runner.start(ship, evo, boom.id, dict(extra)))
        except OrderError as e:
            failed.append(_refused(resolve.the(ship, boom.id), e))
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
# Wrecks and spare spars (package 30b): cut away, send down, shift a spar, the booms
# ---------------------------------------------------------------------------

CLEAR_WRECK = "clear_wreck"
SHIFT_SPAR = "shift_spar"

# A sound spar is sent down with its fellows, by the order that sends them all down.
_SEND_DOWN_ORDERS = {
    "topgallant_mast": "the topgallant masts go down together: 'send down the topgallant masts'",
    "royal_mast": "the royal masts go down with the topgallant masts: 'send down the "
    "topgallant masts'",
    "topmast": "the topmasts are struck together: 'strike the topmasts'",
    "studdingsail_boom": "a studding-sail boom is rigged in, not sent down: 'rig in the {name}'",
}


def _object_parts(ship: Ship, order: Order) -> list[Any]:
    """The parts an order's object names, or none if it names nothing this ship has."""
    if not order.object:
        return []
    try:
        res = resolve.resolve(ship, order.object, order.side_word, order.verb)
    except OrderError:
        return []
    return [ship.parts[pid] for pid in res.ids]


def _names_no_line(ship: Ship, order: Order) -> bool:
    """Whether the object is spars or sails, not lines: 'clear away' then clears a wreck."""
    found = _object_parts(ship, order)
    return bool(found) and not any(isinstance(p, Line) for p in found)


def _names_spars(ship: Ship, order: Order) -> bool:
    """Whether the object is spars alone: 'shift' then shifts a spar for a spare."""
    found = _object_parts(ship, order)
    return bool(found) and all(isinstance(p, Spar) for p in found)


def _names_bowsprit(ship: Ship, order: Order) -> bool:
    """Whether the object is a bowsprit: 'reef' then reefs a running one (package 32b)."""
    found = _object_parts(ship, order)
    return bool(found) and all(isinstance(p, Spar) and p.cls == "bowsprit" for p in found)


def _query(ship: Ship, order: Order) -> Result:
    """'The booms', 'the sail room' and 'the boatswain's store': what the ship's stores
    hold, in the log and never journaled (the World logs a `query.` kind as it is)."""
    from freesail.ship.parts import booms, cordage, ground_tackle, sail_room

    if order.verb == "the booms":
        return "query.booms", "\n".join(booms(ship).inventory_lines()), {}
    if order.verb == BOATSWAINS_STORE:
        return "query.cordage", "\n".join(cordage(ship).inventory_lines()), {}
    if order.verb == "the ground tackle":
        # the anchors and their cables (package 34)
        tackle = ground_tackle(ship)
        if tackle is None:
            return "query.ground_tackle", "She carries no ground tackle.", {}
        return "query.ground_tackle", "\n".join(tackle.describe()), {}
    return "query.sail_room", "\n".join(sail_room(ship).inventory_lines()), {}


# The verb's name as the vocabulary keys it (`vocabulary.key` drops the apostrophe).
BOATSWAINS_STORE = "the boatswains store"


# ---------------------------------------------------------------------------
# Level 1: a parted line rove afresh, or spliced (package 31b)
# ---------------------------------------------------------------------------

REEVE_VERBS = ("reeve", "splice")


def _reeve(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Reeve a new <line>', 'reeve the <line> afresh', 'splice the <line>' (package 31b,
    playtest 11's finding 7): one reeve_line evolution a line, with hands and time, from
    the coil in the boatswain's store (a splice takes none and leaves the line an eighth
    the weaker). A sound line, standing rigging, a line that went with its spar and a
    store too short for the length are refused in words; of several lines, the ones that
    can be rove are, and the rest are reported."""
    _no_stray_modifiers(order, {"afresh", "manner", "hands_from"})
    splice = order.verb == "splice"
    res = resolve.resolve(ship, order.object or "", order.side_word, order.verb)
    lines: list[Line] = []
    for pid in res.ids:
        part = ship.parts[pid]
        if not isinstance(part, Line):
            raise errors.wrong_kind(
                order.verb,
                resolve.display_name(ship, pid),
                _what(ship, part),
                "lines",
                _line_hint(ship, part),
            )
        lines.append(part)
    runner = runner_of(ship)
    evo = vocab.evolutions[order.verb]
    extra, call = _hands_params(ship, order, [evo] * len(lines), None)
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    for line in lines:
        name = resolve.the(ship, line.id)
        reason = scripts.reeve_refusal(ship, line, splice)
        if reason:
            failed.append(_lower(reason))
            failed_ids.append(line.id)
            continue
        params = {"line": line.id, "splice": splice, **extra}
        try:
            texts.append(runner.start(ship, evo, line.id, params))
        except OrderError as e:
            failed.append(_refused(name, e))
            failed_ids.append(line.id)
            continue
        started.append({"evolution": evo, "subject": line.id, "params": params})
    _settle_call(ship, call, bool(started))
    if not started:
        if len(failed) == 1:
            raise OrderError(failed[0][0].upper() + failed[0][1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = " ".join(t.strip() for t in texts if t)
    if failed:
        text += " Not done: " + errors.sentence_list(f.rstrip(".") for f in failed) + "."
    data = {
        "verb": order.verb,
        "level": 1,
        "object": res.name,
        "side": res.side,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
        "splice": splice,
    }
    return "evolution.started", text, data


def _clear_wreck(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Cut away the <part>', 'clear away the wreck of the <part>', 'clear the wreck', and
    'send down the <spar>' of a spar carried away: one clear_wreck evolution for each wreck
    the parts named are in (the whole wreck, whichever part of it is named), or for every
    wreck aboard when nothing is named. A sound part is refused in words that say what is
    done with it instead."""
    _no_stray_modifiers(order, {"manner", "hands_from"})
    send_down = order.verb == "send down"
    said = order.verb_phrase
    if not order.object:
        if send_down:
            raise OrderError(
                "Send down what? Name the spar carried away ('send down the wreck of the fore "
                "topgallant yard'), or send down sound spars together: 'send down the "
                "topgallant masts', 'send down the topgallant yards'."
            )
        subjects = scripts.wrecks(ship)
        if not subjects:
            raise OrderError(
                "There is no wreck aboard to clear: every spar stands and no sail hangs in rags."
            )
        name = "wrecks"
    else:
        res = resolve.resolve(ship, order.object, order.side_word, order.verb)
        name = res.name
        subjects = []
        refused: list[str] = []
        for pid in res.ids:
            part = ship.parts[pid]
            subject = _wreck_subject(ship, part, send_down)
            if isinstance(subject, str):
                refused.append(subject)
            elif subject not in subjects:
                subjects.append(subject)
        if not subjects:
            if len(refused) == 1:
                raise OrderError(refused[0].rstrip(".") + ".")
            raise OrderError(f"Nothing done: {errors.sentence_list(_lower(r) for r in refused)}.")
    runner = runner_of(ship)
    extra, call = _hands_params(
        ship,
        order,
        [CLEAR_WRECK] * len(subjects),
        "clearing the wreck" if len(subjects) > 1 else None,
    )
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    for subject in subjects:
        p = dict(extra, part=subject.id)
        if send_down:
            p["send_down"] = True
        try:
            texts.append(runner.start(ship, CLEAR_WRECK, subject.id, p))
        except OrderError as e:
            failed.append(_refused(resolve.the(ship, subject.id), e))
            failed_ids.append(subject.id)
            continue
        started.append({"evolution": CLEAR_WRECK, "subject": subject.id, "params": p})
    _settle_call(ship, call, bool(started))
    if not started:
        if len(failed) == 1:
            reason = failed[0].split(": ", 1)[-1]
            raise OrderError(reason[0].upper() + reason[1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, "clear", name, started, texts, failed)
    data = {
        "verb": order.verb,
        "said": said,
        "level": 1,
        "object": name,
        "subjects": [s["subject"] for s in started],
        "evolutions": started,
        "failed": failed,
        "failed_subjects": failed_ids,
    }
    return "evolution.started", text, data


def _wreck_subject(ship: Ship, part: Any, send_down: bool) -> Any:
    """The wreck a part named is in: the spar carried away (whichever part of its wreck
    was named), a blown-out sail's rags, or the refusal in words (a string)."""
    name = resolve.the(ship, part.id)
    if isinstance(part, Line):
        return (
            f"{name[0].upper()}{name[1:]} is a line; a line is let go or cast off. Name the spar "
            f"that carried away, or the sail"
        )
    root = scripts.wreck_root(ship, part)
    if root is not None:
        if root.sent_down:
            spar = resolve.the(ship, root.id)
            return f"The wreck of {spar} is cleared already; shift {spar} for a spare"
        return root
    if isinstance(part, Sail):
        if part.state is SailState.BLOWN_OUT:
            if send_down:
                return f"{name[0].upper()}{name[1:]} is blown out; unbend it to send it down"
            return part
        if part.state is SailState.UNBENT:
            return f"{name[0].upper()}{name[1:]} is unbent; there is nothing aloft to cut away"
        if send_down:
            short = name[4:]
            return (
                f"{name[0].upper()}{name[1:]} is not carried away; a sail is unbent and sent "
                f"down with 'unbend the {short}'"
            )
        return (
            f"{name[0].upper()}{name[1:]} is sound and {part.describe_state()}; there is no "
            f"wreck to cut away"
        )
    if isinstance(part, Spar):
        if part.sent_down:
            return f"{name[0].upper()}{name[1:]} is sent down on deck already, and sound"
        if send_down:
            how = _SEND_DOWN_ORDERS.get(part.cls)
            if (
                part.is_yard
                and part.parent
                and ship.spars[part.parent].cls
                in (
                    "topgallant_mast",
                    "royal_mast",
                )
            ):
                how = "the light yards go down together: 'send down the topgallant yards'"
            if how:
                return f"{name[0].upper()}{name[1:]} stands sound; " + how.format(
                    name=resolve.display_name(ship, part.id)
                )
            return (
                f"{name[0].upper()}{name[1:]} stands sound; only a spar carried away is sent "
                f"down by itself"
            )
        return f"{name[0].upper()}{name[1:]} stands sound; there is no wreck to cut away"
    return f"{name[0].upper()}{name[1:]} is not a spar or a sail"


def _shift_spar(ship: Ship, order: Order, vocab: Vocabulary) -> Result:
    """'Shift the <spar>' ('... for a spare'): a spar carried away, its wreck cleared,
    replaced by a spare of its class from the booms (shift_spar.yaml). With none aboard,
    or with the wreck still hanging, the runner's check refuses it in words."""
    _no_stray_modifiers(order, {"manner", "hands_from"} | set(CANVAS_PARAMS))
    if "canvas_no" in order.modifiers or "heavy" in order.modifiers:
        raise OrderError("A spar has no canvas; say 'shift the <spar>', or '... for a spare'.")
    if "for" in order.modifiers:
        raise OrderError(
            f"A spar is shifted for a spare of its class from the booms, not for the "
            f"{order.modifiers['for']}; say 'shift the <spar> for a spare'."
        )
    res = resolve.resolve(ship, order.object or "", order.side_word, order.verb)
    spars = [ship.spars[pid] for pid in res.ids]
    # what is plain from the part itself is refused before the runner is asked (as a
    # sail's is, `_sail_check`); the runner's check says the rest (the wreck still
    # hanging, the spar below it gone, no spare aboard)
    sound = [s for s in spars if not s.wrecked]
    if len(sound) == len(spars):
        names = errors.join_names([resolve.display_name(ship, s.id) for s in sound], "and")
        verb = "is" if len(sound) == 1 else "are"
        raise OrderError(
            f"The {names} {verb} sound; only a spar carried away is shifted for a spare."
        )
    spars = [s for s in spars if s.wrecked]
    runner = runner_of(ship)
    extra, call = _hands_params(
        ship,
        order,
        [SHIFT_SPAR] * len(spars),
        _group_label("shift", res.name, None) if len(spars) > 1 else None,
    )
    started: list[dict[str, Any]] = []
    texts: list[str] = []
    failed: list[str] = []
    failed_ids: list[str] = []
    for spar in spars:
        p = dict(extra, part=spar.id)
        try:
            texts.append(runner.start(ship, SHIFT_SPAR, spar.id, p))
        except OrderError as e:
            failed.append(_refused(resolve.the(ship, spar.id), e))
            failed_ids.append(spar.id)
            continue
        started.append({"evolution": SHIFT_SPAR, "subject": spar.id, "params": p})
    _settle_call(ship, call, bool(started))
    if not started:
        if len(failed) == 1:
            reason = failed[0].split(": ", 1)[-1]
            raise OrderError(reason[0].upper() + reason[1:].rstrip(".") + ".")
        raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
    text = _summarise(ship, "shift", res.name, started, texts, failed)
    data = {
        "verb": order.verb,
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
    allowed = {"tack", "manner", "hands_from"}
    if order.verb == "fill away":
        allowed.add("heading")  # "fill away and steer SW by W" (package 37f)
    _no_stray_modifiers(order, allowed)
    evo = vocab.evolutions[order.verb]
    params: dict[str, Any] = {}
    if order.verb == "fill away":
        if "heading" in order.modifiers:
            # she is filled on the tack she is on, and the helm then has the course
            params["course_deg"] = round(units.rad_to_deg(order.modifiers["heading"]), 3)
        elif order.verb_phrase.split()[-1] in ("steer", "steering"):
            raise OrderError(
                "Fill away and steer where? Give a compass point ('fill away and steer "
                "south-west by west') or degrees, or say 'fill away' to fill her close-hauled "
                "on the tack she is on."
            )
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
    if evo in ("heave_to", "lie_a_try"):
        # refused at once, not after the hands have shortened sail for eight minutes
        # (package 36's finding on the merchant passage's book, which gave `heave to`
        # twice: the script's own check came late and left the yards half braced)
        if "hove_to" in ship.extra:
            raise OrderError("She is hove to already; fill away before heaving to again.")
        in_hand = getattr(ship.extra.get("evolutions"), "instances", None) or []
        if any(
            inst.evo.id in ("heave_to", "lie_a_try") and inst.script is not None for inst in in_hand
        ):
            raise OrderError("She is heaving to already.")
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
