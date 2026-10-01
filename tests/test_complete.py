from freesail.core.world import World
from freesail.orders import handle
from freesail.orders.complete import suggestions
from freesail.ship.loader import load_ship


class FakeRunner:
    def __init__(self, ship):
        ship.extra["evolutions"] = self

    def start(self, ship, evolution, subject, params=None):
        return "started"

    def step(self, *a):
        pass

    def in_progress(self):
        return []


def frigate():
    ship = load_ship("data/ships/frigate-36.yaml")
    FakeRunner(ship)
    ship.dyn.apparent_wind_speed = 8.0
    ship.dyn.apparent_wind_angle = 0.7
    return ship


def test_empty_input_offers_verbs_and_driver_commands():
    s = suggestions(frigate(), "")
    assert any(x.startswith("set ") for x in s)
    assert "hold" in s or "go" in s


def test_verb_prefix_completes_to_verb_phrases():
    s = suggestions(frigate(), "tr")
    assert any(x.startswith("trim") for x in s)
    s = suggestions(frigate(), "shake")
    assert any(x.startswith("shake out") for x in s)


def test_after_a_sail_verb_the_ships_sails_are_offered():
    s = suggestions(frigate(), "set the fore t")
    assert "set the fore topsail" in s
    assert "set the fore topgallant" in s
    assert not any("brace" in x for x in s)


def test_line_verbs_offer_lines_not_sails():
    s = suggestions(frigate(), "haul the weather main ")
    assert any("brace" in x for x in s)
    assert not any(x.endswith("topsail") for x in s)


def test_modifiers_follow_a_complete_noun():
    s = suggestions(frigate(), "reef the topsails ")
    assert (
        "reef the topsails one reef" in s
        or "reef the topsails, one reef" in s
        or any("one reef" in x for x in s)
    )
    s = suggestions(frigate(), "brace the fore yards sharp up on the s")
    assert any(x.endswith("on the starboard tack") for x in s)


def test_helm_verbs_offer_compass_points():
    s = suggestions(frigate(), "steer south-w")
    assert "steer south-west" in s
    assert "steer south-west by west" in s


def test_every_suggestion_is_understood_by_the_parser():
    """A suggestion may be refused for the ship's state (a sail already furled),
    never for its words: no unknown or ambiguous noun, no unknown verb."""
    from freesail.orders.errors import AmbiguousNounError, UnknownNounError
    from freesail.ship.stub import OrderError

    ship = frigate()
    for typed in ("set the ", "take in the main ", "brace ", "haul the lee ", "reef the "):
        for cand in suggestions(ship, typed, limit=40):
            if cand.endswith(" "):
                continue  # a verb phrase awaiting its object
            try:
                handle(ship, cand)
            except (UnknownNounError, AmbiguousNounError) as e:
                raise AssertionError(f"{cand!r}: {e}") from e
            except OrderError as e:
                assert "not an order" not in str(e), f"{cand!r}: {e}"


def test_point_ship_offers_its_three_orders():
    world = World(seed=1)
    s = suggestions(world.ship, "st")
    assert "steer " in s and "stop" in s and "state" in s


def test_belay_offers_the_work_in_hand_first_then_the_lines():
    """Package 29c: completion after 'belay' offers the work in hand or waiting as the
    log names it, then 'belay that' and 'belay all work', then the lines as before."""
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    w = make_world(7, "data/ships/topsail-schooner.yaml", Scenario())
    for order in ("set the fore topsail", "set the foresail", "set the mainsail"):
        w.submit(order)
    s = suggestions(w.ship, "belay ")
    assert s[:5] == [
        "belay setting the fore topsail",
        "belay setting the foresail",
        "belay setting the mainsail",
        "belay that",
        "belay all work",
    ]
    assert any(x.startswith("belay the ") and "sheet" in x for x in s)  # the lines still
    assert suggestions(w.ship, "belay setting the m") == ["belay setting the mainsail"]
    assert suggestions(w.ship, "cancel ")[:3] == [
        "cancel setting the fore topsail",
        "cancel setting the foresail",
        "cancel setting the mainsail",
    ]
    assert "belay all standing orders" in suggestions(w.ship, "belay all")
    w.submit("belay all work")
    assert not any("setting" in x for x in suggestions(w.ship, "belay "))


def test_the_readings_and_the_aliases_are_offered_by_the_vocabulary():
    """Package 33c: a reading asked at the prompt is a query verb of the vocabulary, made
    from the registry's own phrases, so the completer offers it by the means it offers
    `the booms`; the aliases the playtests reached for likewise. Every one offered is
    understood."""
    ship = frigate()
    assert "the reckoning" in suggestions(ship, "the reck")
    assert "the reckonings uncertainty" in suggestions(ship, "the reck")
    assert "the manoeuvre in hand" in suggestions(ship, "the man")
    assert "ask the master the reckoning" in suggestions(ship, "ask the master the r")
    assert any(s.startswith("what is the glass") for s in suggestions(ship, "what is the g"))
    assert "take a sounding " in suggestions(ship, "take a s")
    assert "work up a reckoning " in suggestions(ship, "work up a")
    assert any(s.startswith("sound") for s in suggestions(ship, "sou"))
    assert not any("a sail in sight" in s for s in suggestions(ship, "take a s"))
    from freesail.api.session import make_world
    from freesail.core.world import Scenario

    world = make_world(7, "data/ships/frigate-36.yaml", Scenario())
    for typed in ("the reck", "the man", "what is the ", "ask the master the r"):
        for cand in suggestions(world.ship, typed, limit=40):
            if not cand.endswith(" "):
                e = world.submit(cand)
                assert e.kind == "query.reading", (cand, e.kind, e.text)
