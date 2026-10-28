"""The orders of the water and the damage (spec M7 §13, §14; package 73; the design in
`docs/design/Design-WaterAndHealth.md`): object `damage` in the vocabulary.

    man the pumps              the pumps manned from the hands' pool (a standing work, as
                               the guns' cycle is: on until the well sucks or the word)
    spell the pumps            fresh hands to the brakes, the tired ones relieved (the
                               keeper does it of itself every glass)
    secure the pumps           the pumps' crews stand down
    batten down the hatches    the hatches battened (an evolution: the tarpaulins and the
    open the hatches           battens; the sea shipped over them stops), and taken off
    plug the shot holes        the carpenter's crew to the holes, the worst leak first
    stop the leak              the ground's leak and the started seams caulked, or the
                               shot holes plugged when those are the leak
    fother a sail over the leak  a sail from the sail room thrummed and hauled under
    rig preventer braces       the preventers and the chain slings before an action
    rig preventer backstays
    sling the yards
    set up the rigging         every parted shroud, backstay and stay set up again
    set up the <line>          (`set up the larboard main shrouds`)
    reeve new lines            every parted running line rove in turn (the owner's form)
    fish the <spar>            a sprung spar fished
    rig a jury mast            a lower mast carried away replaced by a spare topmast
    cut away the <mast>        a standing lower mast cut away by the axes
    bury the dead              the burial service, the dead struck from the books

The pumps are the keeper's (`freesail/world/water.py`); the rest are evolutions
(`freesail/evolutions/repair_scripts.py`, `data/evolutions/*.yaml`) started through the
runner as any order's work is, so that they compete for hands with the guns and the sails
by the fighting book's priority. Replies are `(kind, log_text, data)` like every verb's.
"""

from __future__ import annotations

from typing import Any

from freesail.evolutions import registry
from freesail.orders.errors import OrderError
from freesail.orders.grammar import Order
from freesail.orders.prompt import world_of

__all__ = ["DAMAGE_VERBS", "execute"]

Result = tuple[str, str, dict[str, Any]]

DAMAGE_VERBS: tuple[str, ...] = (
    "man the pumps",
    "spell the pumps",
    "secure the pumps",
    "batten down the hatches",
    "open the hatches",
    "plug the shot holes",
    "stop the leak",
    "fother a sail",
    "rig preventer braces",
    "rig preventer backstays",
    "sling the yards",
    "set up the rigging",
    "set up",
    "reeve new lines",
    "fish",
    "rig a jury mast",
    "cut away the mast",
    "bury the dead",
)


def _world(ship: Any, verb: str) -> Any:
    world = world_of(ship)
    if world is None or getattr(world, "water", None) is None:
        raise OrderError(f"'{verb}' wants a ship in a world; this one sails alone.")
    _afloat(ship)
    return world


def _afloat(ship: Any) -> None:
    """A foundered ship has no work left but the boats' (75's)."""
    if (getattr(ship, "extra", None) or {}).get("foundered"):
        raise OrderError(
            "She is foundered: the water has her, and there is no work left aboard but the "
            "boats' (not yet in the game)."
        )


def _runner(ship: Any, verb: str) -> Any:
    runner = ship.extra.get("evolutions")
    if runner is None:
        raise OrderError(f"'{verb}' is work for the hands, and this ship has no runner for it.")
    return runner


def _start(ship: Any, evo_id: str, subject: str, params: dict[str, Any], verb: str) -> Result:
    if registry.get(evo_id) is None:
        raise OrderError(f"There is no such evolution as '{evo_id}'.")
    _afloat(ship)
    runner = _runner(ship, verb)
    text = runner.start(ship, evo_id, subject, params)
    # the runner writes its own started line; work that waits its turn behind other work
    # on the same hold says so in a line of its own (the World leaves the started kind's
    # text to the runner)
    kind = "evolution.queued" if "will follow" in text else "evolution.started"
    return kind, text, {"verb": verb, "level": 1, "evolution": evo_id}


_MAST_WORDS = {
    "mainmast": "main mast",
    "foremast": "fore mast",
    "mizzenmast": "mizzen mast",
    "mizenmast": "mizzen mast",
    "mizen": "mizzen mast",
    "mizzen": "mizzen mast",
}


def _mast_words(ship: Any, words: str, order: Order) -> str:
    """The lower mast an order names: the words after the verb, else the mast in the phrase
    itself ("cut away the mainmast", "rig a jury foremast"), the compound names opened
    ("mainmast" is "main mast" to the ship's nouns); nothing named on a ship with one lower
    mast takes it."""
    if not words:
        last = str(order.verb_phrase or "").split()[-1] if order.verb_phrase else ""
        if last not in ("mast", "masts", "jury", ""):
            words = last
    words = " ".join(words.lower().split())
    for lead in ("the ", "a "):
        words = words.removeprefix(lead)
    words = _MAST_WORDS.get(words, words)
    if not words:
        masts = [s for s in getattr(ship, "spars", {}).values() if s.cls == "mast"]
        if len(masts) == 1:
            words = "mast"
    return words


def execute(ship: Any, order: Order) -> Result:
    verb = order.verb
    words = " ".join(str(order.object or "").split())
    if verb in ("cut away the mast", "rig a jury mast"):
        words = _mast_words(ship, words, order)
    data: dict[str, Any] = {"verb": verb, "level": 1}
    # -- the pumps --------------------------------------------------------------------
    if verb == "man the pumps":
        world = _world(ship, verb)
        text = world.water.pumps.man(int(world.clock.tick))
        return "pumps.manned", text, data | world.water.pumps.describe()
    if verb == "spell the pumps":
        world = _world(ship, verb)
        text = world.water.pumps.spell(int(world.clock.tick))
        return "pumps.spelled", text, data | world.water.pumps.describe()
    if verb == "secure the pumps":
        world = _world(ship, verb)
        if not world.water.pumps.manned:
            raise OrderError("The pumps are not manned; there is nobody at them to stand down.")
        text = world.water.pumps.stand_down(int(world.clock.tick))
        return "pumps.secured", text, data
    # -- the hatches ------------------------------------------------------------------
    if verb in ("batten down the hatches", "open the hatches"):
        world = _world(ship, verb)
        st = world.water.state
        battened = bool(st is not None and st.hatches_battened)
        if verb == "batten down the hatches" and battened:
            raise OrderError("The hatches are battened down already.")
        if verb == "open the hatches" and not battened:
            raise OrderError("The hatches are open already.")
        return _start(ship, "batten_down", "ship", {"open": verb == "open the hatches"}, verb)
    # -- the carpenter's work -------------------------------------------------------------
    if verb in ("plug the shot holes", "stop the leak"):
        world = _world(ship, verb)
        return _start(ship, "plug_shot_hole", "ship", {"verb": verb}, verb)
    if verb == "fother a sail":
        return _start(ship, "fother_sail", "ship", {}, verb)
    if verb in ("rig preventer braces", "rig preventer backstays", "sling the yards"):
        what = {
            "rig preventer braces": "braces",
            "rig preventer backstays": "backstays",
            "sling the yards": "slings",
        }[verb]
        return _start(ship, "rig_preventers", "ship", {"what": what}, verb)
    if verb in ("set up the rigging", "set up"):
        return _start(ship, "set_up_rigging", "ship", {"line_words": words or ""}, verb)
    if verb == "reeve new lines":
        from freesail.orders import verbs as V

        return V.reeve_every_parted_line(ship, order)
    if verb == "fish":
        from freesail.orders.resolve import resolve as resolve_noun_

        if not words:
            raise OrderError("Fish which spar? Name it ('fish the fore topmast').")
        ids = resolve_noun_(ship, words, order.side_word, verb).ids
        spars = [i for i in ids if i in ship.spars]
        if not spars:
            raise OrderError(f"'{words}' is no spar of this ship to fish.")
        texts = []
        for sid in spars:
            kind, text, _d = _start(ship, "fish_spar", sid, {}, verb)
            texts.append(text)
        return "evolution.started", " ".join(texts), data | {"spars": spars}
    if verb == "rig a jury mast":
        return _start(ship, "jury_mast", "ship", {"mast_words": words}, verb)
    if verb == "cut away the mast":
        from freesail.orders.resolve import resolve as resolve_noun_

        if not words:
            raise OrderError("Cut away which mast? Name it ('cut away the mainmast').")
        ids = resolve_noun_(ship, words, order.side_word, verb).ids
        masts = [i for i in ids if i in ship.spars and ship.spars[i].cls == "mast"]
        if not masts:
            raise OrderError(f"'{words}' is no lower mast of this ship to cut away.")
        return _start(ship, "cut_away_mast", masts[0], {}, verb)
    if verb == "bury the dead":
        world = _world(ship, verb)
        from freesail.crew import health

        text, more = health.bury_the_dead(world, by_order=True)
        return "crew.buried", text, data | more
    raise OrderError(f"'{verb}' is not an order of the damage.")
