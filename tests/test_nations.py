"""The nations table (spec M5 §24; package 35): who is at war with whom in June 1805,
the stance of a port toward a ship, the flags' words, the news that moves the table,
and the market's war rule reading it."""

from __future__ import annotations

from datetime import datetime

import pytest

from freesail.world import nations as N
from freesail.world.ports import WAR_FACTOR, load_port, port_files


@pytest.fixture(scope="module")
def table() -> N.Nations:
    return N.load_nations()


@pytest.fixture(scope="module")
def chart():
    from freesail.world.chart import load_chart

    return load_chart("channel-west")


def test_the_eight_nations_and_the_wars_of_june_1805(table):
    assert list(table.nations) == [
        "britain",
        "france",
        "spain",
        "batavian-republic",
        "united-states",
        "portugal",
        "denmark",
        # package 39f: Morocco, for Tangier
        "morocco",
    ]
    assert table.at_war("britain", "france") and table.at_war("france", "britain")
    assert table.at_war("britain", "spain") and table.at_war("britain", "batavian-republic")
    for quiet in ("united-states", "portugal", "denmark"):
        assert not table.enemies_of(quiet), quiet
    assert not table.at_war("france", "spain") and table.allied("france", "spain")
    assert table.enemies_of("britain") == ["batavian-republic", "france", "spain"]
    # every war names its beginning and its source, and the file says the dates are
    # from memory
    for war in table.wars:
        assert war["since"] is not None and "memory" in war["source"]
    assert table.wars_words().startswith(
        "Britain at war with the Batavian Republic, France and Spain"
    )
    assert (
        "the United States, Portugal, Denmark and Morocco at peace with all" in table.wars_words()
    )


def test_morocco_is_at_peace_with_all_and_its_ports_neutral_to_every_flag(table):
    """Package 39f: the nations table gains Morocco for Tangier, at peace with every
    nation in June 1805 (no war in the table), so a Moorish port is neutral to the
    British, the Spaniards and the French alike and open to its own; each relation says
    its source or that it is judgement; the Strait's ports in the index."""
    import yaml

    morocco = table.get("morocco")
    assert morocco.adjective == "Moorish" and "red" in morocco.colours
    assert not morocco.letters_of_marque and not table.enemies_of("morocco")
    assert table.find("Moorish").id == "morocco"
    for other in table.nations:
        if other != "morocco":
            assert table.stance("morocco", other) == "neutral", other
    assert table.stance("morocco", "morocco") == "open"
    doc = yaml.safe_load(open(N.NATIONS_PATH, encoding="utf-8"))
    relations = doc["nations"]["morocco"]["relations"]
    assert set(relations) == set(table.nations) - {"morocco"}
    for words in relations.values():
        assert (
            "JUDGEMENT" in words
            or "MEMORY" in words
            or any(w in words for w in ("1800", "1826", "encyclopaedia"))
        )
    assert (
        table.port_nations["tangier"] == "morocco" and table.port_nations["gibraltar"] == "britain"
    )
    assert {table.port_nations[p] for p in ("algeciras", "tarifa", "ceuta")} == {"spain"}
    # Gibraltar British, hostile to the Spaniards; Ceuta and Algeciras hostile to a King's ship
    assert (
        table.stance("britain", "spain") == "hostile"
        and table.stance("spain", "britain") == "hostile"
    )


def test_letters_of_marque_colours_and_names_lists(table):
    assert table.get("britain").letters_of_marque and table.get("france").letters_of_marque
    assert not table.get("united-states").letters_of_marque
    for n in table.nations.values():
        assert n.colours, n.id  # the words for "a stranger, her colours not made out" (36)
    assert "tricolour" in table.get("france").colours
    assert "fifteen stripes" in table.get("united-states").colours
    assert table.nation_of_names("english") == "britain"
    assert table.nation_of_names("american") == "united-states"
    assert table.find("the French").id == "france" and table.find("British").id == "britain"
    assert table.find("Ruritania") is None


def test_the_stance_of_a_port_toward_a_ship(table, chart):
    # open to its own, hostile to its enemy, neutral to the rest, closed by a port's order
    assert table.stance("britain", "britain") == "open"
    assert table.stance("france", "britain") == "hostile"
    assert table.stance("britain", "france") == "hostile"
    assert table.stance("france", "united-states") == "neutral"
    assert table.stance("britain", "united-states") == "neutral"
    assert table.stance("france", "united-states", closed_to=["united-states"]) == "closed"
    # a closure never outranks a war
    assert table.stance("france", "britain", closed_to=["britain"]) == "hostile"
    assert table.port_nations == {
        "falmouth": "britain",
        "plymouth": "britain",
        "brest": "france",
        "st-marys": "britain",  # package 35b
        "roscoff": "france",
        # package 39a, the Channel east: the islands the King's, St Malo and Morlaix French
        "dartmouth": "britain",
        "torbay": "britain",
        "weymouth": "britain",
        "st-peter-port": "britain",
        "st-helier": "britain",
        "alderney": "britain",
        "st-malo": "france",
        "morlaix": "france",
        # Biscay north (package 39b)
        "lorient": "france",
        "le-palais": "france",
        "paimboeuf": "france",
        "la-rochelle": "france",
        "rochefort": "france",
        # the Strait (package 39f)
        "gibraltar": "britain",
        "algeciras": "spain",
        "tarifa": "spain",
        "ceuta": "spain",
        "tangier": "morocco",
    }
    for pid, path in port_files().items():
        assert load_port(path, chart).nation == table.port_nations[pid]


def test_the_news_moves_the_table_and_the_market_reads_it(chart):
    """A war declared or a peace made arrives as news (by the pilot or the boat, never a
    line from nowhere) and moves the table; the market's war rule reads it the next time
    a price is asked (truth 69's second clause, in freesail/world/ports.py)."""
    table = N.load_nations()
    brest = load_port(port_files()["brest"], chart)
    when = datetime(1805, 6, 12, 10, 0)
    at_war = brest.market.price("tin", when, table, brest.nation)  # English tin under the war
    assert table.make_peace("britain", "france", "1805-06-12")
    assert not table.at_war("britain", "france")
    at_peace = brest.market.price("tin", when, table, brest.nation)
    assert at_war == pytest.approx(at_peace * WAR_FACTOR, abs=0.5)
    assert table.news == [("peace", "britain", "france", "1805-06-12")]
    assert table.declare_war("britain", "france", "1805-06-19", "the pilot's news")
    assert brest.market.price("tin", when, table, brest.nation) == at_war
    assert not table.declare_war("britain", "france")  # at war already: nothing moves
    with pytest.raises(KeyError):
        table.declare_war("britain", "ruritania")
