"""The supply's orders and the galley (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §3.2, §5; `freesail/orders/ordnance.py`): the
words read for powder, shot or both, the necessity, the guns named and the quantities
(numbers with 'and' in them read whole, and 'demand a barrel' one barrel); each quantity
cut to what the magazine wants; `buy` and `demand` naming powder, and 'take
in forty barrels of powder', routed to the supply while water, provisions, tin and the yard
are what they were; a standing order's words read whole; the meal eaten cold while the
galley fire is out, the company's meals counted cold and never said, and the stores'
words saying it only while it is so.

The magazine is the fake of `tests/test_ordnance.py` (the build design's §7.3), written
before Builder 1's was merged; the real one's words are pinned on the real magazine in
`tests/test_ordnance.py`. The example names the one gun of a kind singular (the review's
finding).
"""

from __future__ import annotations

import pytest

from freesail.api.session import make_world
from freesail.crew import victuals
from freesail.orders import _stores_order, parse, read_whole
from freesail.orders import ordnance as OO
from freesail.orders import port as port_orders
from freesail.orders.errors import OrderError
from freesail.world.places import Stores
from tests.test_ordnance import (
    CARRICK_ROAD,
    FRIGATE,
    PRIVATEER,
    THE_SOUND,
    after_the_action,
    at_anchor_in,
    fake_magazine,
    kings_cutter,
)
from tests.test_people import _at_the_prompt, _behind

CUTTER = "data/ships/cutter.yaml"


def order_of(ship, text):
    """The order as `orders.handle` reads it: the grammar's, or the stores' words."""
    try:
        return parse(ship, text)
    except OrderError:
        order = _stores_order(text)
        assert order is not None, text
        return order


def asked(ship, text):
    a = OO.read(ship, order_of(ship, text))
    parts = [(p.what, p.n, p.keys, p.kind) for p in a.parts]
    return a.powder, a.shot, a.necessity, parts, a.keys, a.error


def without_hoy(w):
    w.ports.jobs = [j for j in w.ports.jobs if j.kind != "ordnance"]


# ---------------------------------------------------------------------------
# The words
# ---------------------------------------------------------------------------


def test_the_words_say_powder_shot_or_both_the_necessity_and_the_quantities():
    """The verb phrase and the words together say powder, shot or both (neither: both);
    'of necessity' is struck out as a flag; then the number and what it counts: barrels,
    cartridges for guns, round, grape or chain shot, tons of shot."""
    ship = make_world(7, CUTTER, None).ship
    c12 = (("carronade", 12.0),)
    assert asked(ship, "take in powder and shot") == (True, True, False, [], (), "")
    assert asked(ship, "complete the magazine") == (True, True, False, [], (), "")
    assert asked(ship, "take in ammunition") == (True, True, False, [], (), "")
    assert asked(ship, "take in powder") == (True, False, False, [], (), "")
    assert asked(ship, "demand shot") == (False, True, False, [], (), "")
    assert asked(ship, "buy powder of necessity") == (True, False, True, [], (), "")
    assert asked(ship, "take in powder of absolute necessity")[2] is True
    assert asked(ship, "take in forty barrels of powder") == (
        True,
        False,
        False,
        [("barrels", 40.0, (), "round")],
        (),
        "",
    )
    assert asked(ship, "buy a barrel of powder of necessity")[2:4] == (
        True,
        [("barrels", 1.0, (), "round")],
    )
    assert asked(ship, "take in 30 cartridges for the carronades")[3] == [
        ("cartridges", 30.0, c12, "round")
    ]
    assert asked(ship, "take in 100 round shot for the 12-pounders")[3] == [
        ("shot", 100.0, c12, "round")
    ]
    assert asked(ship, "take in 30 grape shot of 12 pounds")[3] == [("shot", 30.0, c12, "grape")]
    assert asked(ship, "take in twenty chain shot")[3] == [("shot", 20.0, c12, "chain")]
    assert asked(ship, "take in two tons of shot")[3] == [("tons", 2.0, c12, "round")]
    # two quantities, split at the 'and' a number follows
    assert asked(ship, "take in 2 barrels of powder and 149 round shot for the 12-pounders")[
        :4
    ] == (True, True, False, [("barrels", 2.0, (), "round"), ("shot", 149.0, c12, "round")])
    # the powder completed and the shot counted
    assert asked(ship, "take in powder and 100 round shot")[:4] == (
        True,
        True,
        False,
        [("shot", 100.0, c12, "round")],
    )
    assert asked(ship, "take in five tons of powder")[5] == (
        "'five tons of powder' is not a quantity of powder or shot: say 'take in two barrels "
        "of powder', 'take in 100 round shot for the 12-pounders' or 'take in 20 cartridges "
        "for the 12-pounder carronades'."
    )


def test_the_guns_are_named_by_calibre_and_kind_and_the_long_tom_by_its_name():
    """'for the 12-pounders', 'for the long 12', 'for the carronades', 'for the pivot gun',
    'for the long Tom', 'for the swivels', 'of 12 pounds': the guns named by kind and
    calibre in her own order; guns she has not got, or several calibres where one is
    wanted, refused in words."""
    tom = make_world(7, PRIVATEER, None).ship
    long12, carr12, swivel = ("long", 12.0), ("carronade", 12.0), ("swivel", 0.5)
    assert asked(tom, "take in shot for the 12-pounders")[4] == (long12, carr12)
    assert asked(tom, "take in shot for the 12s")[4] == (long12, carr12)
    assert asked(tom, "take in shot for the long 12")[4] == (long12,)
    assert asked(tom, "take in shot for the carronades")[4] == (carr12,)
    assert asked(tom, "take in powder for the pivot gun")[4] == (long12,)
    assert asked(tom, "take in powder for the long Tom")[4] == (long12,)
    assert asked(tom, "take in shot for the swivels")[4] == (swivel,)
    assert asked(tom, "take in 40 shot for the half-pounders")[3] == [
        ("shot", 40.0, (swivel,), "round")
    ]
    assert asked(tom, "take in 30 cartridges for the long tom")[3] == [
        ("cartridges", 30.0, (long12,), "round")
    ]
    # shot is by calibre: the long Tom and the carronades share the 12-pounder's
    assert asked(tom, "take in 100 round shot for the 12-pounders")[3] == [
        ("shot", 100.0, (long12,), "round")
    ]
    guns = "a long 12-pounder, 12-pounder carronades and half-pounder swivels"
    assert asked(tom, "take in 100 round shot")[5] == (
        f"Shot for which guns? She carries {guns}: say 'take in 100 round shot for the "
        "12-pounders'."
    )
    assert asked(tom, "take in 20 cartridges for the 12-pounders")[5] == (
        f"Cartridges for which guns? She carries {guns}: say 'take in 20 cartridges for the "
        "long 12-pounder'."
    )
    # the example as it is said is taken: the pivot's cartridges
    assert asked(tom, "take in 20 cartridges for the long 12-pounder")[3] == [
        ("cartridges", 20.0, (long12,), "round")
    ]
    assert asked(tom, "take in shot for the 24-pounders")[5] == (
        "She carries no 24-pounders; her calibres are 12 and the half-pounder."
    )
    assert asked(tom, "take in shot for the moon")[5] == (
        f"'for the moon' names none of her guns: she carries {guns}; say 'take in 100 round "
        "shot for the 12-pounders'."
    )
    frigate = make_world(7, FRIGATE, None).ship
    assert asked(frigate, "take in shot for the 9-pounders")[4] == (("long", 9.0),)
    assert asked(frigate, "take in two tons of shot for the long 18s")[3] == [
        ("tons", 2.0, (("long", 18.0),), "round")
    ]
    frigate_guns = "long 18-pounders, 32-pounder carronades and long 9-pounders"
    assert asked(frigate, "take in powder for the long Tom")[5] == (
        f"She carries no pivot gun; her guns are {frigate_guns}."
    )
    assert asked(frigate, "take in shot for the swivels")[5] == (
        f"She carries no swivels; her guns are {frigate_guns}."
    )
    assert asked(frigate, "take in shot for the long 32s")[5] == (
        f"She carries no long 32-pounders; her guns are {frigate_guns}."
    )
    assert asked(frigate, "take in 100 round shot for the 12-pounders")[5] == (
        "She carries no 12-pounders; her calibres are 18, 32 and 9."
    )


def test_a_number_with_and_in_it_is_read_whole_and_a_half_after_its_unit_is_its_own():
    """The 'and' inside 'a hundred and fifty' or 'two and a half' splits no quantity
    (`orders.numbers`, the one reader for numbers, reads them whole), and a half or a
    quarter said after the unit is the quantity's ('two barrels and a half of powder'),
    while 'and half a ton of shot' is a quantity of its own."""
    frigate = make_world(7, FRIGATE, None).ship
    l18 = (("long", 18.0),)
    assert asked(frigate, "take in a hundred and fifty round shot for the 18-pounders")[3:] == (
        [("shot", 150.0, l18, "round")],
        (),
        "",
    )
    assert asked(frigate, "take in one hundred and twenty round shot for the 18-pounders")[3] == [
        ("shot", 120.0, l18, "round")
    ]
    assert asked(frigate, "take in two barrels and a half of powder")[3:] == (
        [("barrels", 2.5, (), "round")],
        (),
        "",
    )
    assert asked(frigate, "take in two and a half barrels of powder")[3] == [
        ("barrels", 2.5, (), "round")
    ]
    assert asked(frigate, "take in two tons and a half of shot for the long 18s")[3] == [
        ("tons", 2.5, l18, "round")
    ]
    assert asked(frigate, "take in 2 barrels of powder and half a ton of shot for the 18s")[3] == [
        ("barrels", 2.0, (), "round"),
        ("tons", 0.5, l18, "round"),
    ]
    assert asked(
        frigate,
        "take in two hundred and five round shot for the 18-pounders and a hundred and ten "
        "grape shot for the 18-pounders",
    )[3] == [("shot", 205.0, l18, "round"), ("shot", 110.0, l18, "grape")]
    # in the Sound, the frigate wanting five barrels and her 18-pounders' shot
    w = at_anchor_in(THE_SOUND, ship=FRIGATE, papers={"service": "kings"})
    fake_magazine(
        w.ship,
        powder_lb=0.0,
        reserve_barrels=5,
        shot={18.0: {"round": 100}, 32.0: {"round": 1}, 9.0: {"round": 1}},
    )
    tail = " of the Ordnance's storekeeper at Plymouth, issued and vouched"
    hoy = "; the hoy will be alongside in 4 hours."
    for order, goods in (
        (
            "take in a hundred and fifty round shot for the 18-pounders",
            "150 round shot of 18 pounds",
        ),
        # half a barrel taken as a whole one, as '2.5 barrels' is
        ("take in two barrels and a half of powder", "3 barrels of powder"),
    ):
        e = w.submit(order)
        assert (e.kind, e.text) == ("ordnance.demanded", f"Demanded {goods}{tail}{hoy}"), order
        without_hoy(w)


def test_demand_a_barrel_is_one_barrel_and_not_all_she_wants():
    """The vocabulary's 'demand a' and 'demand an' take the article into the verb's words;
    the article is the quantity's, so 'demand a barrel of powder' is one barrel and 'demand
    a ton of shot for the 18-pounders' a ton of them (2240 pounds: 124 shot), as 'buy a
    barrel of powder' is; an article before no unit ('demand a supply of powder') is no
    number, and the order completes to what the magazine wants."""
    w = at_anchor_in(THE_SOUND, ship=FRIGATE, papers={"service": "kings"})
    fake_magazine(
        w.ship,
        powder_lb=0.0,
        reserve_barrels=5,
        shot={18.0: {"round": 100}, 32.0: {"round": 1}, 9.0: {"round": 1}},
    )
    assert parse(w.ship, "demand a barrel of powder").verb_phrase == "demand a"
    assert asked(w.ship, "demand a barrel of powder")[3] == [("barrels", 1.0, (), "round")]
    assert asked(w.ship, "demand a supply of powder") == (True, False, False, [], (), "")
    assert asked(w.ship, "demand a ton of powder")[5].startswith(
        "'a ton of powder' is not a quantity of powder or shot"
    )
    tail = " of the Ordnance's storekeeper at Plymouth, issued and vouched"
    hoy = "; the hoy will be alongside in 4 hours."
    for order, goods in (
        ("demand a barrel of powder", "1 barrel of powder"),
        ("buy a barrel of powder", "1 barrel of powder"),
        ("demand a ton of shot for the 18-pounders", "124 round shot of 18 pounds"),
        ("demand an hundred round shot for the 18-pounders", "100 round shot of 18 pounds"),
        ("demand a supply of powder", "5 barrels of powder"),
    ):
        e = w.submit(order)
        assert (e.kind, e.text) == ("ordnance.demanded", f"Demanded {goods}{tail}{hoy}"), order
        without_hoy(w)


def test_each_quantity_is_cut_to_what_the_magazine_wants_and_says_so():
    """With no number the order completes to `wanting()`; any number is cut to it with
    words; what is wanted of neither is refused. The King's cutter after the first action
    wants a barrel and 149 round shot of 12 pounds."""
    w = kings_cutter()
    tail = " of the Ordnance's storekeeper at Plymouth, issued and vouched"
    hoy = "; the hoy will be alongside in 4 hours."

    def demanded(order):
        e = w.submit(order)
        assert e.kind == "ordnance.demanded", (order, e.text)
        without_hoy(w)
        return e.text

    assert demanded("take in powder") == f"Demanded 1 barrel of powder{tail}{hoy}"
    assert demanded("take in shot") == f"Demanded 149 round shot of 12 pounds{tail}{hoy}"
    assert demanded("take in forty barrels of powder") == (
        f"Demanded 1 barrel of powder{tail} (the magazine has room for 1 barrel){hoy}"
    )
    # thirty cartridges of a pound: a barrel, rounded up
    assert demanded("take in 30 cartridges for the carronades") == (
        f"Demanded 1 barrel of powder{tail}{hoy}"
    )
    assert demanded("take in 100 round shot") == f"Demanded 100 round shot of 12 pounds{tail}{hoy}"
    assert demanded("take in powder and 100 round shot") == (
        f"Demanded 1 barrel of powder and 100 round shot of 12 pounds{tail}{hoy}"
    )
    room = "the shot lockers have room for 149 round shot of 12 pounds"
    assert demanded("take in 500 round shot for the carronades") == (
        f"Demanded 149 round shot of 12 pounds{tail} ({room}){hoy}"
    )
    # two tons of 12-pound shot are 373 shot
    assert demanded("take in two tons of shot") == (
        f"Demanded 149 round shot of 12 pounds{tail} ({room}){hoy}"
    )
    assert demanded("take in 2 barrels of powder and 100 round shot for the 12-pounders") == (
        f"Demanded 1 barrel of powder and 100 round shot of 12 pounds{tail} (the magazine has "
        f"room for 1 barrel){hoy}"
    )
    first = w.ship.extra["magazine"].describe()[0]
    e = w.submit("take in 20 grape shot")
    assert e.kind == "order.rejected"
    assert e.data["reason"] == f"Her magazine wants no more shot: {first}"
    assert not w.ports.jobs


# ---------------------------------------------------------------------------
# The routes in, and the orders beside them
# ---------------------------------------------------------------------------


def test_buy_and_demand_naming_powder_are_the_supplys_and_water_provisions_and_tin_are_not():
    """`buy` and `demand` whose words name powder come to the supply before the yard and
    the market, and 'take in a barrel of powder' through the stores' reading of 'take in';
    `take in twenty tons of water`, `take in provisions for thirty days`, `buy twenty tons
    of tin` and the yard's topmast give the kinds, texts and data they gave before this
    build (measured on the stage-0 tree)."""
    w = at_anchor_in(
        CARRICK_ROAD,
        papers={"service": "kings", "price_lists": ["falmouth"]},
        cargo={"purse_pounds": 5000.0},
    )
    after_the_action(w.ship)
    for order in (
        "buy two barrels of powder of necessity",
        "demand a barrel of powder of necessity",
        "take in a barrel of powder of necessity",
        "buy shot of necessity",
    ):
        e = w.submit(order)
        assert e.kind == "ordnance.demanded", (order, e.text)
        assert "of the merchants at Falmouth for £" in e.text
        without_hoy(w)
    assert w.purse.pounds == 5000.0  # a sale is paid at alongside
    assert _stores_order("take in forty barrels of powder").verb == OO.TAKE_IN
    assert _stores_order("take in 100 round shot for the 12-pounders").verb == OO.TAKE_IN
    assert _stores_order("take in twenty tons of water").verb == "take in water"
    assert _stores_order("take in the fore topsail") is None
    assert OO.names_powder("twenty barrels of powder") and OO.names_powder("ball")
    assert not OO.names_powder("twenty tons of tin") and not OO.names_powder("a shotgun")
    expected = [
        (
            "take in twenty tons of water",
            "yard.demanded",
            "Demanded 20 tons of water from the chandlers for £2 at Falmouth; it will be "
            "alongside in 2 hours.",
            {"item": "water", "quantity": 20.0, "cost_pounds": 2.0, "hours": 2.0},
        ),
        (
            "take in provisions for thirty days",
            "yard.demanded",
            "Demanded provisions for 30 days from the chandlers for £45 at Falmouth; it will "
            "be alongside in 1.5 hours.",
            {"item": "provisions", "quantity": 30.0, "cost_pounds": 45.0, "hours": 1.5},
        ),
        (
            "buy twenty tons of tin",
            "market.bargain",
            "Bought 20 tons of tin at Falmouth at £120 a ton, £2400 paid; the boat goes for "
            "it. The purse: £2553.",
            {"good": "tin", "tons": 20.0, "sum_pounds": 2400.0, "purse_pounds": 2553.0},
        ),
        (
            "buy a topmast",
            "yard.demanded",
            "Demanded a spare topmast from the chandlers for £40 at Falmouth; it will be "
            "alongside in 8 hours.",
            {"item": "topmast", "quantity": 1.0, "cost_pounds": 40.0, "hours": 8.0},
        ),
    ]
    for order, kind, text, data in expected:
        e = w.submit(order)
        assert (e.kind, e.text) == (kind, text), order
        assert {k: e.data[k] for k in data} == data, order


def test_a_standing_orders_powder_words_are_read_whole_when_it_is_given():
    """`port.check` reads the supply's words as `execute` does, so that a standing order
    naming guns she has not got is refused when it is given, not at its firing; whether
    she is in port is the firing's own business."""
    w = make_world(7, CUTTER, None)
    assert read_whole(w.ship, "take in powder and shot").verb == OO.TAKE_IN
    assert read_whole(w.ship, "buy powder of necessity").verb == OO.TAKE_IN
    with pytest.raises(OrderError, match=r"She carries no 24-pounders; her calibres are 12\."):
        read_whole(w.ship, "take in shot for the 24-pounders")
    with pytest.raises(OrderError, match="'for the moon' names none of her guns"):
        port_orders.check(w.ship, parse(w.ship, "buy twenty barrels of powder for the moon"))
    port_orders.check(w.ship, parse(w.ship, "buy twenty tons of tin"))  # the market's, as before
    e = w.submit('standing order "magazine": every glass then take in shot for the 24-pounders')
    assert e.kind == "order.rejected"
    assert e.data["reason"] == (
        "In standing order 'magazine', 'take in shot for the 24-pounders' is refused: She "
        "carries no 24-pounders; her calibres are 12."
    )


# ---------------------------------------------------------------------------
# The galley
# ---------------------------------------------------------------------------


def test_the_meal_is_cold_while_the_galley_fire_is_out_and_as_it_was_when_it_is_lit():
    """`eat` where the food is hot: cold while the galley fire is out for the powder, the
    meal eaten all the same (`n.ate` now, either way) and never logged; today's words with
    it lit; the biscuit brought up on deck is the same either way."""
    w, cap, _told = _at_the_prompt()
    w.submit("go below")
    _behind(w, cap.needs, hours_ate=6)
    lines = len(w.log)
    lit = w.submit("eat")
    assert lit.text.startswith("You eat in the cabin, the first since")
    assert cap.needs.ate == w.clock.tick
    w.stores.galley_fire_out = "powder"
    _behind(w, cap.needs, hours_ate=6)
    cold = w.submit("eat")
    assert cold.kind == "needs.answer"
    assert cold.text.startswith(
        "A cold meal, biscuit and cheese, the galley fire being out while the powder comes "
        "aboard; you eat in the cabin, the first since"
    )
    assert cap.needs.ate == w.clock.tick
    assert cold.text.removeprefix(
        "A cold meal, biscuit and cheese, the galley fire being out while the powder comes "
        "aboard; you eat"
    ) == lit.text.removeprefix("You eat")
    assert len(w.log) == lines
    w.submit("go on deck")
    _behind(w, cap.needs, hours_ate=6)
    on_deck = w.submit("eat").text
    w.stores.galley_fire_out = ""
    _behind(w, cap.needs, hours_ate=6)
    assert w.submit("eat").text == on_deck
    assert on_deck.startswith(
        "A biscuit and a piece of cheese are brought up from the stores; you eat on the quarterdeck"
    )


def test_the_meals_served_while_the_fire_is_out_are_counted_cold_and_never_said():
    """`victuals.serve`: each meal served while the galley fire is out adds one to the cold
    meals; the stores fall as they would, the lines are what they would be (none), and the
    hardship is unchanged."""
    lit = make_world(7, FRIGATE, None)
    out = make_world(7, FRIGATE, None)
    assert victuals.victualled(lit)
    out.stores.galley_fire_out = "powder"
    meal = victuals.load_ration().meals[1][1]
    assert victuals.serve(lit, meal) == victuals.serve(out, meal) == []
    assert out.stores.cold_meals == 1 and lit.stores.cold_meals == 0
    for name in ("provisions_days", "water_tons", "expended_days", "expended_tons"):
        assert getattr(out.stores, name) == getattr(lit.stores, name), name
    assert victuals.hardship(out) == victuals.hardship(lit)
    victuals.serve(out, meal)
    assert out.stores.cold_meals == 2
    out.stores.galley_fire_out = ""
    victuals.serve(out, meal)
    assert out.stores.cold_meals == 2


def test_the_stores_say_the_galley_fire_only_while_it_is_out():
    """`Stores.words` and `Stores.lines` are what they were with the fire lit and no cold
    meal; while it is out they say so, and once meals were served cold the page counts
    them. A `Stores` pickled before reads the class defaults."""
    w = make_world(7, FRIGATE, None)
    stores = w.stores
    words, lines = stores.words(30.0), stores.lines(250, 30.0)
    plain = Stores(stores.water_tons, stores.provisions_days)
    assert plain.words(30.0) == words and plain.lines(250, 30.0) == lines
    assert ", the galley fire out" not in words
    assert not any("galley" in line or "cold" in line for line in lines)
    reading = w.readings["stores"]["words"]
    stores.galley_fire_out = "powder"
    assert stores.words(30.0) == words + ", the galley fire out while the powder comes aboard"
    w.run(1)  # the readings are the tick's
    assert w.readings["stores"]["words"] == (
        reading + ", the galley fire out while the powder comes aboard"
    )
    assert stores.lines(250, 30.0) == [
        *lines[:3],
        "The galley fire is out while the powder comes aboard.",
        *lines[3:],
    ]
    stores.galley_fire_out = ""
    stores.cold_meals = 3
    assert stores.words(30.0) == words
    assert stores.lines(250, 30.0) == [*lines[:3], "3 meals served cold.", *lines[3:]]
    old = Stores.__new__(Stores)  # as a checkpoint from before this build restores it
    old.__dict__.update(
        {k: v for k, v in vars(plain).items() if k not in ("galley_fire_out", "cold_meals")}
    )
    assert old.galley_fire_out == "" and old.cold_meals == 0 and old.words() == plain.words()
