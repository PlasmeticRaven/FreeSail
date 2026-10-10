"""Storm canvas (package 37p): the storm staysails set, the head sails taken in by their
ratings, and what `shorten sail` adds to its list as the wind rises.

The captain's trials (package 40c) found the frigate in a westerly gale with nothing set
forward: `shorten sail` took in the light sails and reefed the topsails and never touched
the head sails, so the jib and the fore topmast staysail blew out of their bolt-ropes in
a gust of forty-five knots, and with her courses, topsails and spanker and nothing
before the foremast she came to against the helm and lay aback for an hour. The storm
staysails were in the sail room and nothing set them.

- `shorten sail` (the group evolution, `orders._group_evolution`) takes in, after its
  list, every jib whose load is `HEAD_SAIL_IN_RATIO` of its own rating or more ("the jib
  first, before it blows out of the bolt-ropes: the sail's own rating is the rule"), and
  over `STORM_CANVAS_KN` of true wind sets the storm staysails (`shorten_sail_lines`).
- `set the storm staysails` sets each storm staysail of the ship file's group (a
  fore-and-after's storm jib where she carries no storm staysail), bending it from the
  sail room first where it is not bent, and takes in what each replaces as it goes up:
  the head sails for the foremost (Luce 1884, ch. XXIX, p. 477: "To set fore-storm
  staysail, and haul down fore topmast staysail"), the spanker for one abaft it, whose
  place it takes as the ship's after sail ("the main trysail may be set next ... If
  additional after-sail is required, the spanker may be reefed"). A sail being bent is
  set when it is bent (`keep_storm_canvas`, once a tick from the runner), so that she is
  never left without her head sail while the hands rouse the storm staysail up.
"""

from __future__ import annotations

from typing import Any

from freesail import units
from freesail.orders import errors
from freesail.orders.grammar import Order
from freesail.orders.vocabulary import Vocabulary, load_vocabulary
from freesail.ship.graph import Ship
from freesail.ship.parts import Sail, SailState
from freesail.ship.stub import OrderError

# The storm staysails are set over this much true wind (the storm line): a gale, Beaufort's
# force 8 begins at 34 and his strong gale at 41; Luce 1866's journal scale (ch. XXVIII),
# "9. Strong gale; close reefs. 10. Whole gale; close reefed main topsail", and his order
# of reducing sail (Luce 1884, ch. XXIX, p. 477), the fore storm staysail set as the
# topsails are close-reefed. Forty knots is the starter book's heavy weather and the
# King's ship's gale (data/captains/kings-ship.yaml); judgement on the scale.
STORM_CANVAS_KN = 40.0

# A jib is taken in by `shorten sail` when its load is this part of its own rating or more
# (the strain model's ratio, physics/strain.py: a sail strains and wears above 1.0 and
# blows out for certain at 1.8). Judgement: three quarters, so that a gust of a third
# more wind than the mean (the gusts of physics/wind.py at a gustiness of 0.3) loads it
# 1.3 squared, 1.7 times, and still short of blowing it out.
HEAD_SAIL_IN_RATIO = 0.75

# Where the storm staysails being bent are kept until they can be set (`keep_storm_canvas`).
PENDING = "storm_canvas_pending"

STORM_VERBS = frozenset({"set the storm staysails"})


def storm_staysails(ship: Ship) -> list[Sail]:
    """The ship's storm staysails, foremost first: the file's `storm staysails` group, or
    where she has none (a fore-and-after) the jib-headed sails of her storm canvas (the
    storm jib)."""
    ids = list(ship.groups.get("storm staysails") or [])
    if not ids:
        ids = [
            sid
            for sid in ship.groups.get("storm canvas") or []
            if sid in ship.sails and ship.sails[sid].cls == "jibheaded"
        ]
    sails = [ship.sails[sid] for sid in ids if sid in ship.sails]
    return sorted(sails, key=lambda sl: -sl.x_m)


def _replaced(ship: Ship, storm: Sail, foremost: bool) -> list[Sail]:
    """What a storm staysail takes the place of as it is set: for the foremost, the
    ordinary head sails on its stay and forward of it (`REPLACED_AFT_M`: a fore-and-after
    keeps her fore staysail under her storm jib); for one abaft it, the spanker (the
    after gaff sails)."""
    from freesail.evolutions.scripts import after_gaff_sails

    stormy = {sl.id for sl in storm_staysails(ship)}
    if foremost:
        ids = ship.groups.get("headsails") or []
        return [
            ship.sails[sid]
            for sid in ids
            if sid in ship.sails
            and sid not in stormy
            and ship.sails[sid].is_set
            and ship.sails[sid].x_m >= storm.x_m - REPLACED_AFT_M
        ]
    return [sl for sl in after_gaff_sails(ship) if sl.is_set and sl.id not in stormy]


# A head sail no further aft of the storm staysail than this is on its stay or forward of
# it, and is taken in for it (the brig's fore topmast staysail stands a little abaft her
# fore storm staysail in the file); a fore-and-after's fore staysail, some eleven metres
# abaft her storm jib, is kept. Judgement.
REPLACED_AFT_M = 3.0


def _in_its_place(ship: Ship, storm: Sail) -> Sail | None:
    """A sail bent in the storm sail's place (the ship file's `in_place_of`), or None."""
    for other in ship.sails.values():
        if other is storm or other.state is SailState.UNBENT:
            continue
        if storm.in_place_of == other.id or other.in_place_of == storm.id:
            return other
    return None


def _name(ship: Ship, sail: Sail) -> str:
    from freesail.orders import resolve

    return resolve.display_name(ship, sail.id)


def _run(ship: Ship, text: str, vocab: Vocabulary) -> str:
    """Carry out one plain order of the ship's, returning its words."""
    from freesail.orders import verbs
    from freesail.orders.grammar import parse

    _, words, _ = verbs.execute(ship, parse(ship, text, vocab), vocab)
    return words


def _set_now(ship: Ship, storm: Sail, vocab: Vocabulary) -> str:
    """Set a bent storm staysail; what it replaces is taken in when it is set
    (`keep_storm_canvas`), hoisting the one before hauling down the other, as Luce has
    the fore topmast staysail set and the jib taken in (1884, ch. XXIX, p. 476)."""
    text = _run(ship, f"set the {_name(ship, storm)}", vocab)
    ship.extra.setdefault(PENDING, {})[storm.id] = "set"
    return text


def set_storm_staysails(
    ship: Ship, order: Order, vocab: Vocabulary | None = None
) -> tuple[str, str, dict[str, Any]]:
    """`set the storm staysails`: see the module's head."""
    vocab = vocab or load_vocabulary()
    storms = storm_staysails(ship)
    if not storms:
        raise OrderError("She carries no storm staysails in her sail room.")
    texts: list[str] = []
    bending: list[str] = []
    failed: list[str] = []
    subjects: list[str] = []
    pending = ship.extra.get(PENDING)
    in_hand = set(pending) if isinstance(pending, dict) else set()
    for storm in storms:
        name = _name(ship, storm)
        if storm.is_set or storm.id in in_hand:
            continue  # set, or being bent and set already
        if storm.wrecked or storm.state is SailState.BLOWN_OUT:
            failed.append(f"the {name} is {storm.describe_state()}")
            continue
        try:
            rival = _in_its_place(ship, storm)
            if storm.state is SailState.UNBENT and rival is not None:
                # a fore-and-after's storm jib is bent in the jib's place: the jib is
                # shifted for it, taken in, unbent and the storm jib bent and set
                # (`ShiftScript`, Luce 1866, ch. XXXII, 'To shift a jib')
                texts.append(_run(ship, f"shift the {_name(ship, rival)} for the {name}", vocab))
                bending.append(storm.id)
                ship.extra.setdefault(PENDING, {})[storm.id] = "bend"
            elif storm.state is SailState.UNBENT:
                texts.append(_run(ship, f"bend the {name}", vocab))
                bending.append(storm.id)
                ship.extra.setdefault(PENDING, {})[storm.id] = "bend"
            else:
                texts.append(_set_now(ship, storm, vocab))
        except OrderError as e:
            failed.append(f"the {name}: {str(e).rstrip('.')}")
            continue
        subjects.append(storm.id)
    if not subjects:
        if failed:
            raise OrderError(f"Nothing done: {errors.sentence_list(failed)}.")
        raise errors.NothingToDoError("The storm staysails are set already.")
    text = " ".join(t.strip() for t in texts if t)
    if bending:
        names = errors.join_names([_name(ship, ship.sails[sid]) for sid in bending], "and")
        verb = "it is" if len(bending) == 1 else "they are"
        text += f" The {names} to be set as soon as {verb} bent."
    if failed:
        text += f" Not done: {errors.sentence_list(failed)}."
    data = {"verb": order.verb, "level": 1, "subjects": subjects, "bending": bending}
    return "evolution.started", text, data


def _work_on(ship: Ship, sail_id: str) -> bool:
    """Whether any work is in hand or waiting on this sail."""
    runner = ship.extra.get("evolutions")
    return any(
        getattr(inst, "subject_id", None) == sail_id
        for inst in getattr(runner, "instances", None) or ()
    )


def keep_storm_canvas(ship: Ship) -> None:
    """Once a tick, from the runner, for `set the storm staysails`: a storm staysail that
    was being bent is set as soon as it is bent (furled on its stay); one being set, when
    it is set, has what it replaces taken in (`_replaced`). One that will not be (blown
    out, carried away, taken in again) is let go from the record. Meanwhile, over the
    storm line, a head sail the fore storm staysail is to replace that comes to
    `HEAD_SAIL_IN_RATIO` of its rating is taken in at once,
    the storm staysail not yet up (the day under systems: the bending waited for the hands
    at the close reef and the topgallant masts, and a squall of sixty-five knots blew the
    fore topmast staysail out of its bolt-ropes)."""
    pending = ship.extra.get(PENDING)
    if not isinstance(pending, dict) or not pending:
        ship.extra.pop(PENDING, None)
        return
    vocab = load_vocabulary()
    storms = storm_staysails(ship)
    foremost = storms[0].id if storms else None
    for sid, stage in list(pending.items()):
        sail = ship.sails.get(sid)
        if sail is None or sail.wrecked or sail.state is SailState.BLOWN_OUT:
            pending.pop(sid, None)
            continue
        if not sail.is_set and sid == foremost:
            _ease_the_loaded(ship, sail, vocab)
        if stage == "bend":
            if sail.state is SailState.UNBENT:
                continue  # the bending still in hand
            if sail.is_set:
                pending[sid] = "set"
                continue
            try:
                _set_now(ship, sail, vocab)
            except OrderError as e:
                pending.pop(sid, None)
                ship.note(
                    "notable",
                    "sail.storm_canvas",
                    f"The {_name(ship, sail)} is bent, and not set: {str(e).rstrip('.')}.",
                    ship.name,
                )
            continue
        if not sail.is_set:
            if not _work_on(ship, sid):
                pending.pop(sid, None)  # the setting belayed, or refused when it began
            continue  # the setting still in hand
        pending.pop(sid, None)
        replaced = _replaced(ship, sail, sid == foremost)
        taken: list[str] = []
        for sl in replaced:
            try:
                _run(ship, f"take in the {_name(ship, sl)}", vocab)
                taken.append(_name(ship, sl))
            except OrderError:
                continue
        if taken:
            ship.note(
                "routine",
                "sail.storm_canvas",
                f"The {_name(ship, sail)} set in place of "
                f"{errors.join_names([f'the {n}' for n in taken], 'and')}.",
                ship.name,
                {"sail": sid, "replaced": [sl.id for sl in replaced]},
            )
    if not pending:
        ship.extra.pop(PENDING, None)


def _ease_the_loaded(ship: Ship, storm: Sail, vocab: Vocabulary) -> None:
    """Over the storm line, take in before the fore storm staysail is set any head sail it
    is to replace that is loaded to `HEAD_SAIL_IN_RATIO` of its rating (`keep_storm_canvas`),
    with a line. Under the line, and for the spanker, the sail stands until the storm
    staysail is up: in the lee-shore trial a guard on both at thirty knots left her with
    neither head nor after sail while the hands bent the storm staysails, and she drove
    onto Ushant in the evening."""
    wind = true_wind_kn(ship)
    if wind is None or wind < STORM_CANVAS_KN:
        return
    for sl in _replaced(ship, storm, True):
        rating = sl.effective_cloth_rating_kn
        if rating <= 0.0 or sl.load_kn / rating < HEAD_SAIL_IN_RATIO or _work_on(ship, sl.id):
            continue
        try:
            _run(ship, f"take in the {_name(ship, sl)}", vocab)
        except OrderError:
            continue
        ship.note(
            "routine",
            "sail.storm_canvas",
            f"The {_name(ship, sl)} taken in before the {_name(ship, storm)} is up: it is "
            "loaded near its rating.",
            ship.name,
            {"sail": sl.id, "storm": storm.id},
        )


def shorten_sail_lines(ship: Ship, true_wind_kn: float | None) -> list[str]:
    """What `shorten sail` adds to its list (see the module's head): each jib loaded to
    `HEAD_SAIL_IN_RATIO` of its rating or more, outermost first; and over the storm line
    `set the storm staysails`, when she carries any that are not set."""
    lines: list[str] = []
    jibs = [ship.sails[sid] for sid in ship.groups.get("jibs") or [] if sid in ship.sails]
    for sail in sorted(jibs, key=lambda sl: -sl.x_m):
        if not sail.is_set:
            continue
        rating = sail.effective_cloth_rating_kn
        if rating > 0.0 and sail.load_kn / rating >= HEAD_SAIL_IN_RATIO:
            lines.append(f"take in the {_name(ship, sail)}")
    lines += _after_sail_lines(ship)
    storms = storm_staysails(ship)
    stormy = {sl.id for sl in storms}
    # the head sails the foremost storm staysail replaces, loaded to their ratings: the
    # storm staysail goes up in their place before they blow out, whatever the wind's
    # mean (in the trials the fore topmast staysail blew out in a gust of forty knots with
    # the mean at thirty-three, and she lay three hours with nothing forward)
    heads = [
        ship.sails[sid]
        for sid in ship.groups.get("headsails") or []
        if sid in ship.sails and sid not in stormy and ship.sails[sid].is_set
    ]
    strained = any(
        sl.effective_cloth_rating_kn > 0.0
        and sl.load_kn / sl.effective_cloth_rating_kn >= HEAD_SAIL_IN_RATIO
        for sl in heads
        if f"take in the {_name(ship, sl)}" not in lines
    )
    over_the_line = true_wind_kn is not None and true_wind_kn >= STORM_CANVAS_KN
    if (over_the_line or strained) and any(not sl.is_set for sl in storms):
        lines.append("set the storm staysails")
    return lines


def _after_sail_lines(ship: Ship) -> list[str]:
    """The after sail reduced with the head sail, in a ship or a brig, by the reefs the
    topsails will have when this `shorten sail` has taken its own (Luce 1884, ch. XXIX,
    'Reducing Sail to a Gale', p. 476: "As the wind freshens, take a second reef in the
    topsails, and a single reef in the courses. The wind increasing, to take a third reef
    ... To Haul up and Furl the Mainsail"; the spanker is not set again there but reefed
    "if additional after-sail is required"): with the second reef the courses reefed, with
    the third the mainsail hauled up and the spanker taken in. In the captain's trials the
    frigate under her courses, three reefs and the spanker, the jib in, came to against a
    hard-over helm every two minutes for two hours. A fore-and-after keeps her mainsail,
    which the list reefs."""
    from freesail.evolutions.scripts import after_gaff_sails
    from freesail.physics.sails import _square_rigged

    if not _square_rigged(ship):
        return []
    topsails = [
        sl
        for sl in ship.sails.values()
        if sl.cls == "square"
        and sl.is_set
        and ship.yard_of(sl) is not None
        and getattr(ship.parent_of(ship.yard_of(sl)), "cls", "") == "topmast"
    ]
    if not topsails:
        return []
    reefs = max(min(sl.reefs + 1, sl.reef_bands) for sl in topsails)
    lines: list[str] = []
    courses = [ship.sails[sid] for sid in ship.groups.get("courses") or [] if sid in ship.sails]
    courses = [sl for sl in courses if sl.is_set]
    aftermost = min(courses, key=lambda sl: sl.x_m) if len(courses) > 1 else None
    if reefs >= 3 and aftermost is not None:
        lines.append(f"take in the {_name(ship, aftermost)}")
        courses = [sl for sl in courses if sl is not aftermost]
    if reefs >= 2:
        for sl in courses:
            if sl.reefs < sl.reef_bands:
                lines.append(f"reef the {_name(ship, sl)}, one reef")
    if reefs >= 3:
        for sl in after_gaff_sails(ship):
            if sl.is_set:
                lines.append(f"take in the {_name(ship, sl)}")
    return lines


def true_wind_kn(ship: Ship) -> float | None:
    """The true wind's mean speed at the ship, knots, as the World last gave it to her
    (`ship.extra["true_wind"]`), or None."""
    wind = ship.extra.get("true_wind_kn")
    return float(wind) if isinstance(wind, int | float) else None


__all__ = [
    "HEAD_SAIL_IN_RATIO",
    "STORM_CANVAS_KN",
    "STORM_VERBS",
    "keep_storm_canvas",
    "set_storm_staysails",
    "shorten_sail_lines",
    "storm_staysails",
    "true_wind_kn",
    "units",
]
