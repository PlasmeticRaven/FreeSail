"""Powder and shot taken in at a port (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §1.3, §1.4, §3.2, §5; `freesail/world/ordnance.py`):
the eleven ports' `ordnance:` blocks and the lazy block of an old port; every refusal of
the demand in its order and words; the roads at Plymouth by spot; a neutral's knob; the
hoy's two stages, missed, paid at alongside, a short purse, stowed, the shilling and the
paper; the hoy sent back as she weighs, and a hoy at one port not another's; an issue
that moves nothing in the purse; the merged catalogue of an old `Papers`; and the gunner's
account kept by the boatswain in the cutter.

Written before Builder 1's magazine was merged, most of these tests stand on the fake the
build design's §7.3 describes, a `Magazine` subclass set in `ship.extra["magazine"]` with
`layout=2`, whose `wanting`, `describe`, `account_lines` and `return_barrels` follow §1.1,
and which uses the real `receive`, `enter` and `charge_of`. The seams the fake cannot show
are pinned on the real magazine (the review's finding): the gunner's filling emptying a
barrel through to the storekeeper's shilling in the stowed line, the account's own lines on
the paper, and the real first line in the "complete" and "no more shot" refusals. A man of
war of another nation buys of the merchants as everyone else does, the seventh refusal at
an Ordnance port names its storekeeper, and a hoy of shot alone goes back with the shot
(the review's findings).
"""

from __future__ import annotations

import pickle
from datetime import datetime

import pytest
import yaml

from freesail.api.session import make_world
from freesail.core.world import Scenario
from freesail.ship.parts import BARREL_LB, Magazine, Wanting, charge_lb, fit_levels
from freesail.world import ordnance as OR
from freesail.world import places as PL
from freesail.world import ports as PT

CUTTER = "data/ships/cutter.yaml"
FRIGATE = "data/ships/frigate-36.yaml"
MERCHANT_BRIG = "data/ships/merchant-brig.yaml"
PRIVATEER = "data/ships/privateer-schooner.yaml"
SCHOONER = "data/ships/topsail-schooner.yaml"
SMACK = "data/ships/smack.yaml"

# the spots of the roads and the harbours, from the charts' features (channel-west.yaml)
THE_SOUND = {"lat_deg": 50.345, "lon_deg": -4.150}  # the anchorage in the Sound
CAWSAND = {"lat_deg": 50.3330, "lon_deg": -4.1980}  # Cawsand Bay, Plymouth's outer road
HAMOAZE = {"lat_deg": 50.3760, "lon_deg": -4.1916}  # the Hamoaze, Plymouth's mooring
CARRICK_ROAD = {"lat_deg": 50.160, "lon_deg": -5.034}  # Falmouth's anchorage
THE_RADE_INNER = {"lat_deg": 48.345, "lon_deg": -4.470}  # the Bay of Brest
OFF_THE_LIZARD = {"lat_deg": 49.80, "lon_deg": -5.20}
GIBRALTAR_ROAD = {"lat_deg": 36.1440, "lon_deg": -5.3640}
CASCAIS_ROAD = {"lat_deg": 38.6910, "lon_deg": -9.4100}  # Lisbon's outer road
START = datetime(1805, 6, 10, 10, 0)

# The eleven blocks of the build design's §1.3: kind, sells, roads, hoy hours and prices.
BLOCKS = {
    "plymouth": ("ordnance", False, ("outer_road", "anchorage"), 4.0, 5.0, 12.0),
    "gibraltar": ("ordnance", True, None, 3.0, 6.0, 14.0),
    "falmouth": ("merchants", True, None, 3.0, 5.0, 12.0),
    "st-peter-port": ("merchants", True, None, 3.0, 5.0, 12.0),
    "brest": ("merchants", True, None, 3.0, 5.0, 12.0),
    "lorient": ("merchants", True, None, 3.0, 5.0, 12.0),
    "rochefort": ("merchants", True, None, 3.0, 5.0, 12.0),
    "st-malo": ("merchants", True, None, 3.0, 5.0, 12.0),
    "cadiz": ("merchants", True, None, 3.0, 6.0, 14.0),
    "ferrol": ("merchants", True, None, 3.0, 6.0, 14.0),
    "lisbon": ("merchants", True, None, 3.0, 6.0, 14.0),
}


class FakeMagazine(Magazine):
    """Builder 1's magazine as §1.1 gives it, until it is merged (§7.3): the establishment
    is the level's powder and the reserve, the barrels wanted to the nearest whole one, the
    shot wanted the level less the lockers; the reading's lines and the account's page in
    its form; the barrels emptied as the test sets them (`returning`)."""

    returning = 0  # a plain class default, reassigned per instance

    def wanting(self) -> Wanting:
        level = self.level or {}
        established = sum(n * self.charge_of(*k) for k, n in level.items()) + self.reserve_lb
        held = sum(n * self.charge_of(*k) for k, n in self.cartridges.items()) + self.powder_lb
        deficit = max(0.0, established - held)
        shot: dict[float, dict[str, int]] = {}
        for p, kinds in (self.shot_level or {}).items():
            for kind, n in kinds.items():
                short = int(n) - int(self.shot.get(p, {}).get(kind, 0))
                if short > 0:
                    shot.setdefault(float(p), {})[kind] = short
        return Wanting(deficit, int((deficit + 50) // 100), shot)

    def describe(self) -> list[str]:
        filled = ", ".join(
            f"{self.cartridges.get(k, 0)} of {n} for the {k[0]} {k[1]:g}"
            for k, n in (self.level or {}).items()
        )
        return [f"Filled cartridges: {filled}.", f"Powder below: {self.powder_lb:g} pounds."]

    def account_lines(self, last: int = 12) -> list[str]:
        return [f"{when}: {words}." for when, words in self.account[-last:]]

    def return_barrels(self) -> int:
        n, self.returning = self.returning, 0
        return n


def fake_magazine(ship, filled=None, powder_lb=None, shot=None, reserve_barrels=None):
    """A fake of the ship's fit: filled to its level (or `filled`, by kind and calibre),
    the barrels below at the reserve (or `powder_lb`), the lockers full (or `shot`); set in
    `ship.extra["magazine"]`, as `magazine(ship)` finds it."""
    fit = ship.fit_spec
    level = fit_levels(fit)
    reserve = float(reserve_barrels if reserve_barrels is not None else 2) * BARREL_LB
    mag = FakeMagazine(
        cartridges=dict(filled if filled is not None else level),
        shot={float(p): dict(k) for p, k in (shot or fit.shot).items()},
        layout=2,
        level=dict(level),
        charges={k: charge_lb(*k) for k in level},
        shot_level={float(p): dict(k) for p, k in fit.shot.items()},
        reserve_lb=reserve,
        powder_lb=reserve if powder_lb is None else float(powder_lb),
    )
    ship.extra["magazine"] = mag
    return mag


def after_the_action(ship):
    """The King's cutter as the first action leaves her (truth 7-133's figures): 181 of her
    330 carronade cartridges filled, 149 round shot fired, two barrels below."""
    return fake_magazine(
        ship,
        filled={("carronade", 12.0): 181},
        shot={12.0: {"round": 91, "grape": 36, "chain": 24}},
    )


def world_at(
    where, ship=CUTTER, chart="channel-west", ports=("plymouth", "falmouth"), heading=180.0, **kw
):
    kw.setdefault("nation", "britain")
    sc = Scenario(
        start_time=START,
        wind_from_deg=225.0,
        wind_speed_kn=12.0,
        gustiness=0.0,
        variability=0.0,
        ship_heading_deg=heading,
        ship_speed_kn=0.0,
        position=where,
        chart=chart,
        ports=list(ports),
        **kw,
    )
    return make_world(7, ship, sc)


def at_anchor_in(where, ship=CUTTER, **kw):
    w = world_at(where, ship=ship, **kw)
    w.run(60)
    w.submit("let go the best bower")
    w.run(300)
    assert w.at_anchor and w.dealings.in_port() is not None
    return w


def kings_cutter(where=THE_SOUND, **kw):
    w = at_anchor_in(where, papers={"service": "kings"}, cargo={"purse_pounds": 100.0}, **kw)
    after_the_action(w.ship)
    return w


def events(w, kind):
    return [e for e in w.log if e.kind == kind]


def refused(w, order):
    e = w.submit(order)
    assert e.kind == "order.rejected", (order, e.kind, e.text)
    return e.data["reason"]


def hurry(w):
    """The hoy's job brought due at the next tick (its hours are pinned by its due tick
    before this is called): the fast tier sails no five hours at anchor."""
    for job in w.dealings.jobs:
        if job.kind == OR.JOB_KIND:
            job.due_tick = w.clock.tick + 1
    w.run(2)


# ---------------------------------------------------------------------------
# The blocks
# ---------------------------------------------------------------------------


def test_the_eleven_ports_have_their_blocks_and_the_others_none():
    """§1.3's table: Plymouth and Gibraltar the Ordnance's (Plymouth selling nothing, its
    roads Cawsand Bay and the Sound), nine ports the merchants', each with its source and
    the prices at home or abroad; Lisbon's knob written in its file and left unset; every
    other port file with no block, so 'none to be had'."""
    w = world_at(OFF_THE_LIZARD, ports=tuple(PT.port_files()))
    with_block = {pid for pid, port in w.dealings.ports.items() if port.ordnance is not None}
    assert with_block == set(BLOCKS)
    # the other twenty-seven, the Channel's east block's eight (package 79b) and the Gulf
    # of Lion's four and the Ligurian sea's seven (package 79d), none
    assert len(w.dealings.ports) - len(with_block) == 27 + 8 + 4 + 7
    for pid, (kind, sells, roads, hours, barrel, ton) in BLOCKS.items():
        block = w.dealings.ports[pid].ordnance
        assert (block["kind"], block["sells"], block["roads"]) == (kind, sells, roads), pid
        assert block["hoy_hours"] == hours, pid
        assert (block["powder_per_barrel_pounds"], block["shot_per_ton_pounds"]) == (barrel, ton)
        assert (block["barrels_an_hour"], block["shot_tons_an_hour"]) == (20.0, 2.0), pid
        assert block["source"] and block["sells_in_war_to"] is None, pid
        assert OR.block_of(w.dealings.ports[pid]) is block
    plymouth = w.dealings.ports["plymouth"].ordnance
    assert plymouth["roads_words"] == "Plymouth Sound or Cawsand Bay"
    assert "Art. VI l.12833-12839" in plymouth["source"]
    text = open("data/ports/lisbon.yaml", encoding="utf-8").read()
    assert "  # sells_in_war_to: [britain]" in text


def test_a_block_with_a_word_it_does_not_take_is_refused_in_words(tmp_path):
    where = "data/ports/x.yaml"
    with pytest.raises(ValueError, match="the ordnance block has no key 'barrels'; its keys"):
        OR.parse_block({"kind": "ordnance", "barrels": 4}, where)
    with pytest.raises(ValueError, match="kind 'navy' is not one of ordnance, merchants"):
        OR.parse_block({"kind": "navy"}, where)
    with pytest.raises(ValueError, match="road 'quay' is not a spot of the port"):
        OR.parse_block({"kind": "ordnance", "roads": ["quay"], "roads_words": "x"}, where)
    with pytest.raises(ValueError, match="names its roads in roads_words"):
        OR.parse_block({"kind": "ordnance", "roads": ["outer_road"]}, where)
    with pytest.raises(ValueError, match="hoy_hours '0' is not a positive number"):
        OR.parse_block({"kind": "merchants", "hoy_hours": 0}, where)
    assert OR.parse_block(None, where) is None
    # merchants sell by their kind; a price may be nothing
    block = OR.parse_block({"kind": "merchants", "powder_per_barrel_pounds": 0}, where)
    assert block["sells"] is True and block["powder_per_barrel_pounds"] == 0.0
    # in a port file, as the loader reads it
    w = world_at(OFF_THE_LIZARD, ports=("plymouth",))
    text = open("data/ports/plymouth.yaml", encoding="utf-8").read()
    bad = tmp_path / "plymouth.yaml"
    bad.write_text(text.replace("  hoy_hours: 4", "  hoy_hours: 4\n  powder_hoy: yes"), "utf-8")
    with pytest.raises(ValueError, match="the ordnance block has no key 'powder_hoy'"):
        PT.load_port(bad, w.chart)


def test_a_port_pickled_before_the_block_reads_it_once_from_its_file(tmp_path):
    """A `Port` from a checkpoint of packages 70 to 72 has no `ordnance` of its own: the
    class default would say none to be had, so `block_of` reads this build's file of the
    port once and keeps it. Its pickled path names the folder the game was first played
    in, whose file has no block (the review of this build found every port of the kept
    saves naming another folder): that file is read only when this build has no file of
    the port, and with neither the port has none."""
    w = world_at(OFF_THE_LIZARD, ports=("plymouth",))
    port = w.dealings.ports["plymouth"]
    new = port.ordnance
    del port.__dict__["ordnance"]  # as a port pickled before this build
    text = open("data/ports/plymouth.yaml", encoding="utf-8").read()
    doc = yaml.safe_load(text)
    del doc["ordnance"]
    older = tmp_path / "an-older-checkout" / "plymouth.yaml"  # the file before this build
    older.parent.mkdir()
    older.write_text(yaml.safe_dump(doc), encoding="utf-8", newline="\n")
    port.path = str(older)
    old = pickle.loads(pickle.dumps(port))
    assert "ordnance" not in vars(old) and old.ordnance is None  # the class default
    assert OR.block_of(old) == new  # this build's file, not the older checkout's
    old.path = str(tmp_path / "gone.yaml")
    assert OR.block_of(old) == new  # read once and kept
    # a port this build has no file of: the file it was loaded from, then none
    (tmp_path / "plymouth.yaml").write_text(text, encoding="utf-8", newline="\n")
    elsewhere = pickle.loads(pickle.dumps(port))
    elsewhere.id = "a-port-of-another-build"
    elsewhere.path = str(tmp_path / "plymouth.yaml")
    assert OR.block_of(elsewhere) == new
    gone = pickle.loads(pickle.dumps(port))
    gone.id = "a-port-of-another-build"
    gone.path = str(tmp_path / "gone.yaml")
    assert OR.block_of(gone) is None and "ordnance" in vars(gone)


# ---------------------------------------------------------------------------
# The issue, and the hoy's two stages
# ---------------------------------------------------------------------------


def test_the_kings_cutter_completes_her_magazine_of_the_ordnance_free_in_the_sound():
    """§5: the demand issued and vouched, the purse untouched; the hoy alongside at four
    hours with the galley fire out, the port's reading saying so; the powder and shot
    struck down and stowed an hour later (a barrel and 149 shot at twenty barrels and two
    tons an hour, at least an hour), the fire lit again, the receipt in the gunner's account
    and the account written up by the boatswain, the cutter having no gunner. Nothing is
    drawn: no stream is opened by the supply."""
    w = kings_cutter()
    mag = w.ship.extra["magazine"]
    streams = w.rng.stream_names()
    purse = (w.purse.pounds, list(w.purse.entries))
    e = w.submit("take in powder and shot")
    assert e.kind == "ordnance.demanded"
    assert e.text == (
        "Demanded 1 barrel of powder and 149 round shot of 12 pounds of the Ordnance's "
        "storekeeper at Plymouth, issued and vouched; the hoy will be alongside in 4 hours."
    )
    assert e.data["how"] == "issue" and e.data["cost_pounds"] == 0.0
    assert e.data["barrels"] == 1 and e.data["powder_lb"] == 100.0
    assert e.data["shot"] == {"12": {"round": 149}}
    assert e.data["due_tick"] == e.tick + 4 * 3600
    (job,) = w.dealings.jobs
    assert (job.kind, job.port_id, job.due_tick) == ("ordnance", "plymouth", e.tick + 4 * 3600)
    assert job.payload == {
        "stage": "alongside",
        "how": "issue",
        "necessity": False,
        "powder_lb": 100.0,
        "barrels": 1,
        "shot": {"12": {"round": 149}},
        "cost": 0.0,
        "words": "1 barrel of powder and 149 round shot of 12 pounds",
    }
    port = w.readings["port"]
    assert port["words"].endswith(
        "; the Ordnance's hoy coming off with her powder, alongside about 14:06"
    )
    assert port["hoy"] == {"how": "issue", "due_tick": job.due_tick, "stage": "coming off"}
    hurry(w)
    (alongside,) = events(w, "ordnance.alongside")
    assert alongside.text == (
        "The Ordnance's hoy is alongside with the powder: the galley fire is put out, no light "
        "allowed but in the light room, and no man to smoke (the Regulations, the Gunner, "
        "Art. V)."
    )
    assert alongside.severity.value == "notable"
    assert w.stores.galley_fire_out == "powder"
    assert w.readings["port"]["words"].endswith("; the hoy alongside, the powder coming aboard")
    (stowing,) = w.dealings.jobs
    assert stowing.payload["stage"] == "stowed"
    assert stowing.due_tick == alongside.tick + 3600  # 1/20 + 0.8 tons/2, at least an hour
    hurry(w)
    (stowed,) = events(w, "ordnance.stowed")
    assert stowed.text == (
        "A barrel of powder and 149 round shot of 12 pounds struck down and stowed, issued by "
        "the Ordnance's storekeeper and vouched; the magazine secured and the keys to the "
        "captain; the galley fire lit again."
    )
    assert w.stores.galley_fire_out == "" and not w.dealings.jobs
    assert mag.powder_lb == 300.0 and mag.shot[12.0]["round"] == 240
    assert mag.report_filled is True
    (when, words) = mag.account[-1]
    assert words == (
        "Received of the Ordnance's storekeeper at Plymouth, issued and vouched: 1 barrel of "
        "powder and 149 round shot of 12 pounds"
    )
    assert when.startswith("10 June, ")
    written = events(w, "paper.written")[-1]
    assert written.text == (
        "The gunner's account written up by the boatswain: a barrel of powder and 149 round "
        "shot of 12 pounds struck down and stowed, issued by the Ordnance's storekeeper and "
        "vouched; the magazine secured and the keys to the captain; the galley fire lit again."
    )
    assert written.data == {"paper": "the gunner's account"}
    page = w.papers.page("the gunner's account")
    assert page.keeper == "boatswain" and page.place == "gunroom"
    assert page.lines == [*mag.describe(), *mag.account_lines()]
    assert page.as_of_tick == stowed.tick
    # an issue: the purse not touched at any stage, and nothing drawn
    assert (w.purse.pounds, list(w.purse.entries)) == purse
    assert w.rng.stream_names() == streams
    assert "hoy" not in w.readings["port"]


def test_powder_is_taken_in_at_the_road_and_never_in_the_hamoaze():
    """Art. VI: "Plymouth Sound or Cawsand Bay": by the spot nearest her, Cawsand Bay (the
    outer road) and the anchorage in the Sound pass, the Hamoaze (the mooring) is refused in
    the article's words; the issue is the King's ship's alone."""
    road = kings_cutter(CAWSAND)
    assert road.dealings.in_port().nearest_spot(road.position)[0].name == "Cawsand Bay"
    assert road.submit("take in powder").kind == "ordnance.demanded"
    harbour = kings_cutter(HAMOAZE)
    assert harbour.dealings.in_port().nearest_spot(harbour.position)[0].name == "the Hamoaze"
    assert refused(harbour, "take in powder and shot") == (
        "Powder is taken in at Plymouth Sound or Cawsand Bay, not in the harbour (the "
        "Regulations, the Gunner, Art. VI): weigh and bring her to the road first."
    )
    assert not harbour.dealings.jobs


def test_the_hoy_goes_back_when_she_is_gone_from_the_road_and_nothing_is_paid():
    """The job re-checks at alongside that she lies in its port, and for an issue at its
    roads: a hoy come off for her at Plymouth while she lies at Falmouth goes back, nothing
    put out and nothing paid; and one whose ship weighed before the powder was struck down
    takes nothing in, lights the fire again and gives a sale's money back."""
    w = at_anchor_in(CARRICK_ROAD, papers={"service": "kings"}, cargo={"purse_pounds": 100.0})
    after_the_action(w.ship)
    pay = {"stage": "alongside", "how": "issue", "necessity": False, "powder_lb": 100.0}
    pay |= {"barrels": 1, "shot": {}, "cost": 0.0, "words": "1 barrel of powder"}
    w.dealings.jobs.append(PT.Job(w.clock.tick + 1, "ordnance", "plymouth", dict(pay)))
    w.run(2)
    (missed,) = events(w, "ordnance.missed")
    assert missed.text == (
        "The hoy came off and found her gone from the road; it went back with the powder."
    )
    assert missed.data["why"] == "gone" and missed.severity.value == "notable"
    assert w.stores.galley_fire_out == "" and not w.dealings.jobs
    assert not events(w, "ordnance.alongside")
    # weighed with the hoy alongside: a sale at Falmouth, paid at alongside, given back
    pay |= {"stage": "stowed", "how": "sale", "cost": 5.0}
    w.stores.galley_fire_out = "powder"
    w.purse.pay(5.0, "powder and shot of the merchants at Falmouth", w.clock.tick)
    w.dealings.jobs.append(PT.Job(w.clock.tick + 1, "ordnance", "plymouth", dict(pay)))
    w.run(2)
    gone = events(w, "ordnance.missed")[-1]
    assert gone.text == (
        "She weighed before the powder was struck down: nothing was taken in, and the hoy "
        "went back with it, the £5 paid returned; the galley fire lit again."
    )
    assert w.purse.pounds == 100.0 and w.stores.galley_fire_out == ""
    assert w.ship.extra["magazine"].powder_lb == 200.0


def test_a_ship_that_weighs_with_the_hoy_alongside_has_her_galley_fire_lit_as_she_goes():
    """Weighed while the powder comes aboard, she is gone from the port as soon as her
    anchor is up: the hoy goes back then, the sale's money given back and the galley fire
    lit again within the minute, not when the taking in would have ended (an hour here,
    hours for a frigate's shot), so that she sails with no cold meals and no filling held."""
    w = kings_cutter(CARRICK_ROAD)
    w.submit("buy powder and shot of necessity")
    hurry(w)
    assert w.stores.galley_fire_out == "powder" and w.purse.pounds == pytest.approx(85.4)
    (stowing,) = w.dealings.jobs
    assert w.submit("weigh").kind == "order.accepted"
    up = None
    for _ in range(40):
        w.run(60)
        if not w.at_anchor:
            up = w.clock.tick
            break
    assert up is not None and up < stowing.due_tick
    w.run(60)
    (gone,) = events(w, "ordnance.missed")
    assert up - 60 < gone.tick <= up + 60 < stowing.due_tick
    assert gone.text == (
        "She weighed before the powder was struck down: nothing was taken in, and the hoy "
        "went back with it, the £14 12s paid returned; the galley fire lit again."
    )
    assert gone.data["why"] == "weighed"
    assert w.stores.galley_fire_out == "" and not w.dealings.jobs
    assert w.purse.pounds == pytest.approx(100.0)
    assert not events(w, "ordnance.stowed")


def test_a_hoy_at_another_port_neither_stops_a_demand_here_nor_shows_in_this_ports_reading():
    """The hoy's job is its port's: one coming off at Plymouth while she lies at Falmouth
    (she having sailed between) does not refuse a demand of Falmouth's merchants as a hoy
    already coming, and Falmouth's reading shows Falmouth's hoy alone."""
    w = kings_cutter(CARRICK_ROAD)
    pay = {"stage": "alongside", "how": "issue", "necessity": False, "powder_lb": 100.0}
    pay |= {"barrels": 1, "shot": {}, "cost": 0.0, "words": "1 barrel of powder"}
    w.dealings.jobs.append(PT.Job(w.clock.tick + 2 * 3600, "ordnance", "plymouth", dict(pay)))
    w.run(1)
    reading = w.readings["port"]
    assert reading["port"] == "falmouth" and "hoy" not in reading
    assert "hoy" not in reading["words"]
    e = w.submit("buy powder of necessity")
    assert e.kind == "ordnance.demanded" and e.data["port"] == "falmouth"
    w.run(1)
    reading = w.readings["port"]
    assert reading["hoy"]["how"] == "sale"
    assert reading["words"].endswith(
        "; the merchants' hoy coming off with her powder, alongside about 13:06"
    )


def test_the_ordnance_returns_the_gunner_a_shilling_for_each_empty_barrel():
    """Art. IX: the empty barrels returned to the storekeeper at a shilling apiece, the
    gunner's own; said in the stowed line at the Ordnance's issue, nothing in the purse."""
    w = kings_cutter()
    mag = w.ship.extra["magazine"]
    mag.returning = 3
    w.submit("take in powder")
    hurry(w)
    hurry(w)
    (stowed,) = events(w, "ordnance.stowed")
    assert stowed.text == (
        "A barrel of powder struck down and stowed, issued by the Ordnance's storekeeper and "
        "vouched; the magazine secured and the keys to the captain; the galley fire lit again; "
        "the gunner returns three empty barrels to the storekeeper, a shilling apiece his own."
    )
    assert stowed.data["barrels_returned"] == 3 and mag.returning == 0
    assert w.purse.pounds == 100.0 and w.purse.entries == []


# ---------------------------------------------------------------------------
# The refusals, in their order
# ---------------------------------------------------------------------------


def test_a_ship_with_no_guns_is_told_so_first_and_a_ship_at_sea_that_she_is_not_in_port():
    """The first two refusals: no guns (before any port is looked for, so in a world with
    no chart too), then not in port."""
    gunless = at_anchor_in(CARRICK_ROAD, ship=SCHOONER)
    assert refused(gunless, "take in powder and shot") == (
        "She carries no guns; there is no magazine to fill."
    )
    assert refused(gunless, "buy twenty barrels of powder") == (
        "She carries no guns; there is no magazine to fill."
    )
    alone = make_world(7, SCHOONER, None)
    assert refused(alone, "take in powder") == "She carries no guns; there is no magazine to fill."
    at_sea = world_at(OFF_THE_LIZARD, papers={"service": "kings"})
    after_the_action(at_sea.ship)
    assert refused(at_sea, "take in powder and shot") == (
        "She is not in port: powder and shot are taken in at a port, of the Ordnance or a merchant."
    )
    # the words' own refusal is the last: at sea she is told she is not in port
    assert refused(at_sea, "take in 100 round shot for the 24-pounders").startswith(
        "She is not in port"
    )


def test_a_hostile_port_and_a_port_with_no_block_refuse_her_in_words():
    """The third and fourth: Brest, hostile to the English, serves her nothing; a port
    whose file has no block has none to be had."""
    brest = at_anchor_in(THE_RADE_INNER, ports=("brest",), heading=250.0)
    after_the_action(brest.ship)
    assert refused(brest, "take in powder and shot") == (
        "Brest is hostile to her; no powder will be issued or sold her."
    )
    w = kings_cutter(CARRICK_ROAD)
    w.dealings.ports["falmouth"].ordnance = None  # as the twenty-seven
    assert refused(w, "buy powder of necessity") == (
        "There is no powder or shot to be had at Falmouth: no storekeeper of the Ordnance, "
        "and no merchant who deals in it."
    )


def test_one_hoy_at_a_time_and_the_ordnance_issues_to_the_kings_ships_alone():
    """The fifth and sixth: a second demand while the hoy is coming off, or alongside, is
    refused with its hours; a privateer at Plymouth, where the town sells none, is refused
    the Ordnance's issue."""
    w = kings_cutter()
    w.submit("take in powder and shot")
    w.run(3600)
    assert refused(w, "take in shot") == (
        "The hoy is coming off with her powder already; it will be alongside in 3 hours."
    )
    hurry(w)
    assert refused(w, "take in shot") == (
        "The hoy is alongside with her powder already; it will be struck down in 1 hour."
    )
    privateer = at_anchor_in(THE_SOUND, ship=PRIVATEER, papers={"service": "privateer"})
    fake_magazine(privateer.ship, filled={("long", 12.0): 20, ("carronade", 12.0): 220})
    assert refused(privateer, "take in powder and shot") == (
        "The Ordnance's storekeeper at Plymouth issues to the King's ships alone, and no "
        "merchant here sells powder."
    )


def test_a_complete_magazine_a_short_purse_and_guns_she_has_not_got_are_refused():
    """The tenth, eleventh and twelfth: complete, with the first line of the gunner's
    count; a sale the purse cannot meet, in the yard's form; and words naming guns she
    has not got, or shot for no gun in particular when she has several calibres."""
    w = kings_cutter()
    full = fake_magazine(w.ship)
    assert full.wanting().empty
    assert refused(w, "take in powder and shot") == (
        f"Her magazine is complete: {full.describe()[0]}"
    )
    assert refused(w, "take in 100 round shot for the 24-pounders") == (
        f"Her magazine is complete: {full.describe()[0]}"
    )
    after_the_action(w.ship)
    assert refused(w, "take in 100 round shot for the 24-pounders") == (
        "She carries no 24-pounders; her calibres are 12."
    )
    frigate = at_anchor_in(THE_SOUND, ship=FRIGATE, papers={"service": "kings"})
    fake_magazine(frigate.ship, filled={("long", 18.0): 1000})
    assert refused(frigate, "take in 100 round shot") == (
        "Shot for which guns? She carries long 18-pounders, 32-pounder carronades and long "
        "9-pounders: say 'take in 100 round shot for the 18-pounders'."
    )
    assert refused(frigate, "take in 100 round shot for the 12-pounders") == (
        "She carries no 12-pounders; her calibres are 18, 32 and 9."
    )
    poor = at_anchor_in(CARRICK_ROAD, ship=MERCHANT_BRIG, cargo={"purse_pounds": 1.0})
    fake_magazine(poor.ship, filled={("long", 6.0): 50}, powder_lb=0.0)
    assert refused(poor, "take in powder") == (
        "3 barrels of powder costs £15 and the purse holds £1."
    )


# ---------------------------------------------------------------------------
# The merchants: of necessity, at a price, paid at alongside
# ---------------------------------------------------------------------------


def test_a_kings_ship_buys_of_the_merchants_only_of_necessity_and_pays_at_alongside():
    """The seventh refusal, and the Regulations' necessity: at Falmouth the King's cutter is
    refused until her captain says it is of necessity; then the merchants sell at the
    port's price, nothing paid at the order, the purse paying at alongside with the cause,
    and the line keeping the captain's word."""
    w = kings_cutter(CARRICK_ROAD)
    assert refused(w, "take in powder and shot") == (
        "There is no storekeeper of the Ordnance at Falmouth, and a captain is charged not to "
        "purchase stores without an absolute necessity (the Regulations): say 'buy powder of "
        "necessity' to buy it of the merchants at £5 a barrel."
    )
    e = w.submit("buy powder and shot of necessity")
    assert e.kind == "ordnance.demanded"
    assert e.text == (
        "Demanded 1 barrel of powder and 149 round shot of 12 pounds of the merchants at "
        "Falmouth for £14 12s, of absolute necessity, on the captain's word, for the Admiralty's "
        "account, paid when it comes alongside; the hoy will be alongside in 3 hours."
    )
    # £5 a barrel, and 149 shot of 12 pounds (1788 pounds) at £12 a ton: £14 12s
    assert e.data["cost_pounds"] == 14.6 and e.data["necessity"] is True
    assert w.purse.pounds == 100.0
    hurry(w)
    assert w.purse.pounds == pytest.approx(85.4)
    assert w.purse.entries[-1][1:] == (-14.6, "powder and shot of the merchants at Falmouth")
    (alongside,) = events(w, "ordnance.alongside")
    assert alongside.text == (
        "The merchants' hoy is alongside with the powder: the galley fire is put out, no light "
        "allowed but in the light room, and no man to smoke."
    )
    hurry(w)
    (stowed,) = events(w, "ordnance.stowed")
    assert stowed.text == (
        "A barrel of powder and 149 round shot of 12 pounds struck down and stowed, bought of "
        "the merchants at Falmouth for £14 12s, of absolute necessity, on the captain's word, "
        "for the Admiralty's account; the magazine secured and the keys to the captain; the "
        "galley fire lit again."
    )
    assert w.purse.pounds == pytest.approx(85.4)  # paid once


def test_the_merchant_brig_buys_at_falmouth_and_a_short_purse_sends_the_hoy_back():
    """A merchantman buys her own of the merchants (no word of necessity wanted); the purse
    is read at alongside, and a purse spent in the meantime sends the hoy back with nothing
    paid and the galley fire never put out."""
    w = at_anchor_in(CARRICK_ROAD, ship=MERCHANT_BRIG, cargo={"purse_pounds": 50.0})
    fake_magazine(
        w.ship, filled={("long", 6.0): 50}, powder_lb=0.0, shot={6.0: {"round": 30, "grape": 16}}
    )
    e = w.submit("take in powder and shot")
    assert e.text == (
        "Demanded 3 barrels of powder and 50 round shot of 6 pounds of the merchants at "
        "Falmouth for £16 12s, paid when it comes alongside; the hoy will be alongside in 3 "
        "hours."
    )
    assert e.data["how"] == "sale" and e.data["necessity"] is False
    assert w.purse.pounds == 50.0
    w.purse.pay(40.0, "spent ashore", w.clock.tick)
    hurry(w)
    (missed,) = events(w, "ordnance.missed")
    assert missed.text == (
        "The merchants' hoy came alongside, but the purse holds £10 against £16 12s; it went "
        "back with the powder."
    )
    assert missed.data["why"] == "purse"
    assert w.purse.pounds == 10.0 and w.stores.galley_fire_out == "" and not w.dealings.jobs


def test_lisbon_sells_to_both_sides_until_its_knob_is_set():
    """A neutral's merchants sell to both sides; with `sells_in_war_to` set on the loaded
    block, a belligerent not listed is refused in words and one listed is served."""
    french = at_anchor_in(
        CASCAIS_ROAD,
        chart="atlantic-east",
        ports=("lisbon",),
        nation="france",
        papers={"service": "privateer"},
        cargo={"purse_pounds": 100.0},
    )
    after_the_action(french.ship)
    assert french.dealings.stance(french.dealings.in_port()) == "neutral"
    assert french.nations.enemies_of("france")
    assert french.submit("take in powder").kind == "ordnance.demanded"
    french.dealings.jobs = []
    french.ports.ports["lisbon"].ordnance["sells_in_war_to"] = ("britain",)
    assert refused(french, "take in powder") == (
        "Lisbon's merchants sell no powder to a French ship while the war lasts."
    )
    french.scenario.nation = "britain"
    assert french.submit("take in powder").kind == "ordnance.demanded"


def test_gibraltar_issues_to_the_kings_ship_anywhere_and_its_merchants_sell_to_the_rest():
    """Abroad the Ordnance issues wherever she lies (Art. VI names the home roads alone),
    and the Rock's merchants sell at the dearer price."""
    kings = at_anchor_in(
        GIBRALTAR_ROAD, chart="atlantic-east", ports=("gibraltar",), papers={"service": "kings"}
    )
    after_the_action(kings.ship)
    e = kings.submit("take in powder and shot")
    assert e.data["how"] == "issue" and e.data["hours"] == 3.0
    privateer = at_anchor_in(
        GIBRALTAR_ROAD,
        chart="atlantic-east",
        ports=("gibraltar",),
        papers={"service": "privateer"},
        cargo={"purse_pounds": 100.0},
    )
    after_the_action(privateer.ship)
    e = privateer.submit("take in powder and shot")
    assert e.data["how"] == "sale"
    # £6 a barrel and 1788 pounds of shot at £14 a ton
    assert e.data["cost_pounds"] == 17.2
    assert "of the merchants at Gibraltar for £17 4s, paid when it comes alongside" in e.text


def test_a_man_of_war_of_another_nation_buys_of_the_merchants_as_everyone_else_does():
    """The Regulations' necessity binds a King's ship of Britain's
    (`service.under_the_regulations`): an American frigate, a King's ship by her wardroom,
    buys at Falmouth at the order, and a Portuguese one at Gibraltar of the Rock's
    merchants, the storekeeper issuing to the King's own ships alone; neither line says
    "of necessity" or the Admiralty (the review's findings: both were refused under the
    British Regulations, at Gibraltar with "There is no storekeeper of the Ordnance at
    Gibraltar", and the American's purchase was written "for the Admiralty's account")."""
    from freesail.world.service import KINGS, service_of, under_the_regulations

    us = at_anchor_in(
        CARRICK_ROAD, ship=FRIGATE, nation="united-states", cargo={"purse_pounds": 500.0}
    )
    assert service_of(us) == KINGS and not under_the_regulations(us)
    fake_magazine(us.ship, filled={("long", 18.0): 1900})
    e = us.submit("take in powder and shot")
    assert e.kind == "ordnance.demanded" and e.data["how"] == "sale", e.text
    assert e.data["necessity"] is False
    assert "of the merchants at Falmouth for " in e.text and "necessity" not in e.text
    hurry(us)
    hurry(us)
    (stowed,) = events(us, "ordnance.stowed")
    assert "Admiralty" not in stowed.text and "necessity" not in stowed.text
    pt = at_anchor_in(
        GIBRALTAR_ROAD,
        ship=FRIGATE,
        chart="atlantic-east",
        ports=("gibraltar",),
        nation="portugal",
        cargo={"purse_pounds": 500.0},
    )
    assert pt.dealings.stance(pt.dealings.in_port()) == "neutral"
    fake_magazine(pt.ship, filled={("long", 18.0): 1900})
    e = pt.submit("take in powder and shot")
    assert e.kind == "ordnance.demanded" and e.data["how"] == "sale", e.text
    assert "of the merchants at Gibraltar for " in e.text and "necessity" not in e.text


def test_the_seventh_refusal_at_an_ordnance_port_names_its_storekeeper():
    """A King's ship of Britain's at an Ordnance port whose storekeeper is not hers and whose
    merchants sell (a block written so for Lisbon by the test: no shipped port is one) is
    told the storekeeper does not issue to her, not that there is none; at the merchants'
    ports the words are the build design's own (the review's finding)."""
    w = at_anchor_in(
        CASCAIS_ROAD,
        chart="atlantic-east",
        ports=("lisbon",),
        papers={"service": "kings"},
        cargo={"purse_pounds": 100.0},
    )
    after_the_action(w.ship)
    assert w.dealings.stance(w.dealings.in_port()) == "neutral"
    assert refused(w, "take in powder and shot") == (
        "There is no storekeeper of the Ordnance at Lisbon, and a captain is charged not to "
        "purchase stores without an absolute necessity (the Regulations): say 'buy powder of "
        "necessity' to buy it of the merchants at £6 a barrel."
    )
    w.dealings.ports["lisbon"].ordnance["kind"] = "ordnance"
    assert refused(w, "take in powder and shot") == (
        "The Ordnance's storekeeper at Lisbon does not issue to her, and a captain is charged "
        "not to purchase stores without an absolute necessity (the Regulations): say 'buy "
        "powder of necessity' to buy it of the merchants at £6 a barrel."
    )
    assert w.submit("buy powder of necessity").kind == "ordnance.demanded"


def test_a_hoy_of_shot_alone_goes_back_with_the_shot():
    """The hoy goes back with what it brought: a hoy of shot alone, sent back for a short
    purse, for her being gone from the road, or as she weighs before it is struck down,
    goes back "with the shot", as it came alongside with it (the review's finding: "went
    back with the powder"); a hoy with powder in her keeps the build design's words."""
    w = at_anchor_in(CARRICK_ROAD, ship=MERCHANT_BRIG, cargo={"purse_pounds": 100.0})
    fake_magazine(w.ship, shot={6.0: {"round": 50}})
    e = w.submit("take in shot")
    assert e.kind == "ordnance.demanded" and e.data["barrels"] == 0, e.text
    (job,) = w.dealings.jobs
    shot_only = dict(job.payload)
    w.purse.pounds = 0.0
    hurry(w)
    (short,) = events(w, "ordnance.missed")
    assert short.text.startswith("The merchants' hoy came alongside, but the purse holds ")
    assert short.text.endswith("; it went back with the shot.")
    w.purse.pounds = 100.0
    w.dealings.jobs.append(PT.Job(w.clock.tick + 1, "ordnance", "plymouth", dict(shot_only)))
    w.run(2)
    assert events(w, "ordnance.missed")[-1].text == (
        "The hoy came off and found her gone from the road; it went back with the shot."
    )
    stowing = shot_only | {"stage": "stowed"}
    w.dealings.jobs.append(PT.Job(w.clock.tick + 1, "ordnance", "plymouth", stowing))
    w.purse.pay(float(shot_only["cost"]), "the shot of the merchants at Falmouth", w.clock.tick)
    w.run(2)
    assert events(w, "ordnance.missed")[-1].text.startswith(
        "She weighed before the shot was struck down: nothing was taken in, and the hoy went "
        "back with it, the "
    )
    with_powder = shot_only | {"barrels": 1, "powder_lb": 100.0}
    w.dealings.jobs.append(PT.Job(w.clock.tick + 1, "ordnance", "plymouth", with_powder))
    w.run(2)
    assert events(w, "ordnance.missed")[-1].text == (
        "The hoy came off and found her gone from the road; it went back with the powder."
    )


def test_the_real_magazine_from_the_gunners_filling_to_the_shilling_and_the_page():
    """The seams on the real magazine (`ship.parts.Magazine`, not the fake): the gunner's
    filling empties a barrel below, the Ordnance's issue stowed returns it to the
    storekeeper at a shilling, the gunner's own (Art. IX), in the stowed line and the paper;
    the account's own lines on the page; and the first line of the real count in the
    "no more shot" and "complete" refusals."""
    from freesail.ship.parts import magazine

    w = at_anchor_in(THE_SOUND, papers={"service": "kings"}, cargo={"purse_pounds": 100.0})
    mag = magazine(w.ship)
    assert type(mag) is Magazine and mag.powder_lb == 200.0
    key = ("carronade", 12.0)
    mag.set_filled(*key, 300)
    mag.powder_lb = 105.0
    mag.fill(10 * 135.0)  # the gunner's ten cartridges: 105 pounds to 95, a barrel emptied
    assert mag.filled_of(*key) == 310 and mag.powder_lb == 95.0 and mag.barrels_emptied == 1
    first = mag.describe()[0]
    assert first == (
        "Filled cartridges: 310 of 330 for the 12-pounder carronades; the gunner filling for "
        "the 12-pounder carronades."
    )
    e = w.submit("take in 20 grape shot")
    assert e.kind == "order.rejected" and e.data["reason"] == (
        f"Her magazine wants no more shot: {first}"
    )
    mag.shot[12.0]["round"] -= 10
    e = w.submit("take in powder and shot")
    assert e.kind == "ordnance.demanded" and e.data["how"] == "issue", e.text
    hurry(w)
    hurry(w)
    (stowed,) = events(w, "ordnance.stowed")
    assert stowed.text.endswith(
        "; the galley fire lit again; the gunner returns one empty barrel to the storekeeper, "
        "a shilling apiece his own."
    )
    assert stowed.data["barrels_returned"] == 1 and mag.barrels_emptied == 0
    written = events(w, "paper.written")[-1]
    assert written.text.endswith("a shilling apiece his own.")
    (when, words) = mag.account[-1]
    assert words.startswith(
        "Received of the Ordnance's storekeeper at Plymouth, issued and vouched: "
    )
    assert mag.account_lines()[-1] == f"{when}: {words}"
    page = w.papers.page("the gunner's account")
    assert page.lines == [*mag.describe(), *mag.account_lines()]
    assert page.lines[-1] == f"{when}: {words}"
    mag.set_filled(*key, 330)
    mag.powder_lb = mag.reserve_lb
    assert mag.wanting().empty
    assert refused(w, "take in powder and shot") == (
        "Her magazine is complete: Filled cartridges: 330 of 330 for the 12-pounder carronades."
    )


# ---------------------------------------------------------------------------
# The gunner's account
# ---------------------------------------------------------------------------


def test_an_old_papers_catalogue_is_mended_on_a_miss_and_keeps_no_mark_of_it(tmp_path, monkeypatch):
    """A checkpoint's `Papers` from before has ten papers: the gunner's account is found
    by merging the file's papers the catalogue lacks, nothing logged. Nothing is kept on
    the `Papers` to say it was done, so a miss in a game of this build (a paper no file
    has) does not stop a later build's new paper being merged into its checkpoint."""
    w = world_at(OFF_THE_LIZARD, ports=("plymouth",))
    assert [p["handle"] for p in w.papers.catalogue][-1] == "the gunner's account"
    state = set(vars(w.papers))
    # as a checkpoint of packages 71 and 72 restores it: its own state, ten papers
    old = PL.Papers.__new__(PL.Papers)
    old.__dict__.update(
        {k: v for k, v in vars(w.papers).items() if k != "catalogue"},
        catalogue=[dict(p) for p in w.papers.catalogue[:10]],
    )
    assert len(old.pages()) == 10
    n = len(w.log)
    assert old.page("the gunner's account").source == "magazine"
    assert len(old.catalogue) == 11 and len(old.pages()) == 11
    assert len(w.log) == n
    with pytest.raises(KeyError, match="no paper aboard answers to 'the logbook'"):
        old.page("the logbook")
    assert len(old.catalogue) == 11
    # a miss in a game of this build, and then a later build with one more paper
    assert w.papers.find("the log of the hold") is None
    assert set(vars(w.papers)) == state == set(vars(old))
    doc = yaml.safe_load(PL.PAPERS_PATH.read_text(encoding="utf-8"))
    doc["papers"].append(
        {
            "handle": "the carpenter's book",
            "keeper": "carpenter",
            "place": "gunroom",
            "source": "booms",
            "words": "a paper of a later build",
        }
    )
    later = tmp_path / "papers.yaml"
    later.write_text(yaml.safe_dump(doc), encoding="utf-8", newline="\n")
    monkeypatch.setattr(PL, "PAPERS_PATH", later)
    for papers in (w.papers, old):
        assert papers.find("the carpenter's book")["words"] == "a paper of a later build"
        assert len(papers.catalogue) == 12


def test_a_catalogue_from_another_file_is_mended_from_its_own_file_not_the_projects(tmp_path):
    """Package 86's fold-in (the review's finding): `Papers._merge` reads the catalogue's own
    file, so a `Papers` made from another path is never given the project's papers on a
    miss; a checkpoint's `Papers` from before the path was kept (no `path`) reads the
    project's file, as before."""
    w = world_at(OFF_THE_LIZARD, ports=("plymouth",))
    assert w.papers.path is None  # the project's own file: no machine's path pickled
    doc = yaml.safe_load(PL.PAPERS_PATH.read_text(encoding="utf-8"))
    own = tmp_path / "papers.yaml"
    own.write_text(yaml.safe_dump({"papers": doc["papers"][:3]}), encoding="utf-8", newline="\n")
    papers = PL.Papers(w, own)
    assert papers.path == str(own) and len(papers.catalogue) == 3
    assert papers.find("the gunner's account") is None and len(papers.catalogue) == 3
    papers.catalogue = papers.catalogue[:2]  # a page lost: mended from its own file
    assert papers.find(doc["papers"][2]["handle"]) is not None and len(papers.catalogue) == 3
    old = PL.Papers.__new__(PL.Papers)
    old.__dict__.update(
        {k: v for k, v in vars(w.papers).items() if k not in ("catalogue", "path")},
        catalogue=[dict(p) for p in w.papers.catalogue[:10]],
    )
    assert old.page("the gunner's account").source == "magazine"
    assert len(old.catalogue) == 11


def test_the_gunners_account_is_kept_by_the_boatswain_in_the_cutter():
    """The keeper falls to the boatswain, the mate and then the master where there is no
    gunner; a ship with no guns keeps no account."""
    cutter = world_at(OFF_THE_LIZARD, ports=("plymouth",))
    assert cutter.papers.page("the gunner's account").keeper == "boatswain"
    frigate = world_at(OFF_THE_LIZARD, ship=FRIGATE, ports=("plymouth",))
    page = frigate.papers.page("gunner")
    assert page.keeper == "gunner"
    from freesail.ship.parts import magazine

    assert page.lines == magazine(frigate.ship).describe()  # no receipts yet
    smack = world_at(OFF_THE_LIZARD, ship=SMACK, ports=("plymouth",))
    page = smack.papers.page("the gunner's account")
    assert page.keeper == "mate"
    assert page.lines == ["She carries no guns; the gunner keeps no account."]
    assert PL.PLACES[page.place].name == "the gunroom"
