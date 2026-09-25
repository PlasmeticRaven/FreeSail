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
