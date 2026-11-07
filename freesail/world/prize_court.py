"""The prize court and the money (spec M7 §18 and §20; package 74, step 5; the design in
`docs/design/Design-Prizes.md` §5). Every figure is `data/business.yaml`'s (`prize_values`,
`prize_courts`, `prize_money`, `prize_shares`), its source or FROM MEMORY beside it.

**The valuation** (§5.1): her tons burthen (the file gives none of its own: her displacement
over 1.36 and the tonne, the usual ratio for the type, which `data/ships/frigate-36.yaml`
states for the frigate: judgement) at a price a ton by her kind (a merchant hull, a man of
war's), worn by age at two per cent a year (a file with no build year ten years old); her
guns at the Ordnance's price a hundredweight; her stores nothing (said). **The cargo** at the
port's market, each good at its price of the day, the supply moved by the tons sold. **The
prize goods**: her powder and shot at the port's `ordnance:` prices (86's keys, the merchants'
defaults else) and her purse as it stands.

**The court** (§5.2) sits where she is brought in: a prize hull lying in a port open to her
captor's nation queues the port's job `prize_court` due in the court's days by the port's
nation (Britain 7, France 7, Spain 10: judgement, decision 64), and the sentence is
**condemned** where her old nation was at war with the captor's at the taking (the wars'
dates), or she was an outlaw, or a neutral carrying an enemy's cargo for an enemy's port;
**restored** with costs against the captor where she was a neutral wrongly taken (given back
whole by `prizes.retake`'s swap); **salvage** on a recapture (an eighth to the recaptors, she
restored). A far prize with no hull is sentenced on her record when she lies in her goal's
road for the court's days. The director overrides by `port <id>: the court condemns |
restores the <prize>` (doubted where the rule gives otherwise).

**The money** (§5.3): the valuation, the cargo and the goods less the agent's five per cent
and the court's fees, plus the head money (five pounds a head of the men aboard a ship of war
or a privateer at the start of the engagement; paid though she was burnt), three fourths now
and a fourth reserved where a King's ship's prize of war is purchased for the service; the
sum **shared among all the ships in sight at the moment the enemy surrendered**, a ship that
took no part included (Lavery, Nelson's Navy, p. 116; the division among them by their
complements: judgement, FROM MEMORY), each ship's part into her purse where she has one, by
the eighths of the scheme in force at the court's date (the two British schemes confirmed by
Lavery; a privateer's by her articles; France's and Spain's the British eighths, said so);
the account's lines as `paper.written` lines of the prize account and one urgent line of the
log, the purse's line saying so.
"""

from __future__ import annotations

import math
from datetime import date
from typing import Any

from freesail.core.events import Severity

__all__ = [
    "SHIP_OF_WAR_ROLES",
    "accounts_of",
    "court_rows",
    "head_money",
    "in_sight_at_strike",
    "money_rows",
    "note_in_sight",
    "scheme_for",
    "sentence",
    "share_out",
    "shares_words",
    "tons_burthen",
    "valuation",
    "value_rows",
]

SHIP_OF_WAR_ROLES: frozenset[str] = frozenset(
    {"kings-ship", "cruiser", "commodore", "privateer", "cartel"}
)
TONS_PER_DISPLACEMENT = 1.36  # the frigate's file: 1,270 t displacement for 933 tons burthen
TONNE_KG = 1000.0
_LB_PER_TON = 2240.0
_POWDER_LB_PER_BARREL = 100.0  # the Ordnance's barrel (the magazine's own figure where it has one)


# -- the rows --------------------------------------------------------------------------------------


def _business() -> dict[str, Any]:
    from freesail.world.business import load_business

    return load_business()


def value_rows() -> dict[str, Any]:
    return dict(_business().get("prize_values") or {})


def court_rows(nation_id: str) -> dict[str, Any]:
    rows = _business().get("prize_courts") or {}
    return dict(
        rows.get(nation_id) or rows.get("default") or {"days": 7, "name": "the prize court"}
    )


def money_rows() -> dict[str, Any]:
    return dict(_business().get("prize_money") or {})


def scheme_for(nation_id: str, when: date, service: str = "") -> dict[str, Any]:
    """The eighths in force at the date for the nation (a privateer's by her articles):
    the scheme's classes and its source."""
    schemes = _business().get("prize_shares") or []
    key = "privateer" if service == "privateer" else nation_id

    def pick(nation: str) -> dict[str, Any] | None:
        for s in schemes:
            if str(s.get("nation")) != nation:
                continue
            frm, until = s.get("from"), s.get("until")
            if isinstance(frm, date) and when < frm:
                continue
            if isinstance(until, date) and when >= until:
                continue
            return s
        return None

    s = pick(key)
    if s is None:
        s = pick("britain")
    if s is not None and s.get("classes") == "british":
        b = pick("britain") or {}
        s = dict(s, classes=b.get("classes") or [], british_kept=True)
    return s or {"nation": key, "classes": [], "source": "no scheme"}


# -- the valuation ---------------------------------------------------------------------------------


def tons_burthen(spec: Any) -> float:
    hull = getattr(spec, "hull", None)
    disp = float(getattr(hull, "displacement_kg", 0.0) or 0.0)
    return disp / TONNE_KG / TONS_PER_DISPLACEMENT


def _age_years(spec: Any, when: date) -> float:
    rows = value_rows()
    built = getattr(spec, "built", None) or getattr(spec, "launched", None)
    try:
        year = int(str(built)[:4]) if built else None
    except ValueError:
        year = None
    if year is None:
        return float(rows.get("age_years_unknown", 10))
    return max(0.0, float(when.year - year))


def valuation(world: Any, vessel: Any) -> dict[str, float]:
    """{'hull': £, 'guns': £, 'stores': 0, 'tons': t} by the rows; the kind by her role before
    the taking (a man of war's price for a ship of war, the merchant's else)."""
    from freesail.ship.loader import load_spec

    rows = value_rows()
    spec = load_spec(vessel.ship_file)
    rec = getattr(vessel, "prize", None) or {}
    role_was = str(rec.get("role_was") or getattr(vessel, "role", "") or "")
    man_of_war = role_was in SHIP_OF_WAR_ROLES or "merchant" not in str(
        getattr(vessel, "description", "") or ""
    )
    per_ton = float(
        rows.get("man_of_war_hull_pounds_per_ton" if man_of_war else "merchant_hull_pounds_per_ton")
        or (12.0 if man_of_war else 8.0)
    )
    when = world.clock.ship_time.date()
    wear = max(0.0, 1.0 - float(rows.get("wear_per_year", 0.02)) * _age_years(spec, when))
    tons = tons_burthen(spec)
    hull = round(tons * per_ton * wear)
    arm = spec.armament
    fs = arm.fit(getattr(vessel, "fit", "") or None) if arm is not None else None
    cwt = sum(float(g.weight_cwt) for g in fs.guns) if fs is not None else 0.0
    guns = round(cwt * float(rows.get("guns_pounds_per_cwt", 4.0)))
    return {"hull": float(hull), "guns": float(guns), "stores": 0.0, "tons": round(tons)}


def _cargo(world: Any, prize_hull: Any, port: Any) -> tuple[float, list[str]]:
    """Her hold's goods sold to the port's market at its prices of the day."""
    if prize_hull is None or port is None:
        return 0.0, []
    hold = getattr(prize_hull, "hold", None)
    goods = dict(getattr(hold, "goods", {}) or {})
    market = getattr(port, "market", None)
    if not goods or market is None:
        return 0.0, []
    nations = getattr(world, "nations", None)
    when = world.clock.ship_time
    total = 0.0
    lines = []
    for name, tons in goods.items():
        if tons <= 0:
            continue
        try:
            price = float(market.price(name, when, nations, str(port.nation)))
        except KeyError:
            price = 0.0
        value = round(tons * price)
        total += value
        if hasattr(market, "sold_to_port"):
            market.sold_to_port(name, tons)
        lines.append(f"{tons:g} tons of {name} at the market £{value:,.0f}")
        hold.goods[name] = 0.0
    return total, lines


def _prize_goods(world: Any, prize_hull: Any, port: Any) -> tuple[float, list[str]]:
    """Her powder and shot at the port's ordnance prices, and her purse."""
    if prize_hull is None:
        return 0.0, []
    from freesail.world import ordnance as O

    lines = []
    total = 0.0
    block = dict(getattr(port, "ordnance", None) or {}) if port is not None else {}
    per_barrel = float(
        block.get("powder_per_barrel_pounds") or O.DEFAULTS.get("powder_per_barrel_pounds", 5.0)
    )
    per_ton = float(block.get("shot_per_ton_pounds") or O.DEFAULTS.get("shot_per_ton_pounds", 12.0))
    mag = getattr(prize_hull.ship, "magazine", None) or prize_hull.ship.extra.get("magazine")
    if mag is not None:
        powder_lb = float(getattr(mag, "powder_lb", 0.0) or 0.0)
        barrels = powder_lb / _POWDER_LB_PER_BARREL
        shot_lb = 0.0
        for pounder, kinds in (getattr(mag, "shot", {}) or {}).items():
            for _kind, n in (kinds or {}).items():
                shot_lb += float(pounder) * int(n)
        goods = round(barrels * per_barrel + shot_lb / _LB_PER_TON * per_ton)
        if goods:
            total += goods
            lines.append(
                f"her powder ({barrels:.0f} barrels) and shot ({shot_lb / _LB_PER_TON:.1f} tons) "
                f"£{goods:,.0f}"
            )
    purse = getattr(prize_hull, "purse", None)
    money = float(getattr(purse, "pounds", 0.0) or 0.0)
    if money > 0:
        total += round(money)
        lines.append(f"her purse £{money:,.0f}")
        purse.pounds = 0.0
    return total, lines


def head_money(record: dict[str, Any]) -> float:
    """Five pounds a head of the men aboard a ship of war or a privateer at the start of the
    engagement (the record's `men_at_start`); nothing for a merchantman."""
    role_was = str(record.get("role_was") or "")
    if role_was not in SHIP_OF_WAR_ROLES - {"cartel"}:
        return 0.0
    per_head = float(money_rows().get("head_money_pounds", 5.0))
    return per_head * int(record.get("men_at_start", 0) or 0)


# -- the ships in sight at the strike --------------------------------------------------------------


def in_sight_at_strike(world: Any, struck: Any) -> list[dict[str, Any]]:
    """The ships in sight from the struck ship's masthead at the moment she surrendered that
    are at war with her nation (the captor's and her allies'), each with her complement: the
    sharers of the prize money (Lavery, p. 116). Her own nation's and the neutrals' are not
    sharers."""
    from freesail.world.hulls import world_of

    root = world_of(world)
    sea = getattr(root, "vessels", None)
    nations = getattr(root, "nations", None)
    if sea is None or nations is None:
        return []
    try:
        seen = sea.strangers_of(root, struck, set())
    except Exception:  # noqa: BLE001
        return []
    out = []
    for s in seen:
        v = sea.get(str(s.get("id") or ""))
        if v is None or v.done or getattr(v, "struck", False):
            continue
        if not nations.at_war(str(v.nation), str(struck.nation)):
            continue
        out.append({"id": str(v.id), "name": str(v.name), "complement": _complement(v)})
    return out


def _complement(vessel: Any) -> int:
    crew = getattr(vessel, "crew", None)
    muster = (
        getattr(getattr(crew, "ship", None), "extra", {}).get("crew") if crew is not None else None
    )
    if muster is not None:
        return len(muster.sailors)
    try:
        from freesail.ship.loader import load_spec

        return int(getattr(load_spec(vessel.ship_file).crew, "complement", 0) or 0)
    except Exception:  # noqa: BLE001
        return 0


def note_in_sight(world: Any, struck: Any) -> None:
    """Written on the struck vessel at the strike's tick (`in_sight_at_strike`), copied into
    her prize record at the possession."""
    try:
        struck.in_sight_at_strike = in_sight_at_strike(world, struck)
    except Exception:  # noqa: BLE001
        struck.in_sight_at_strike = []


# -- the court -------------------------------------------------------------------------------------


def _at_war_at(nations: Any, a: str, b: str, when_tick: int, world: Any) -> bool:
    """Whether the two were at war at the tick (the wars' `since` dates against the clock)."""
    from datetime import timedelta

    when = world.clock.ship_time - timedelta(seconds=int(world.clock.tick) - int(when_tick))
    day = when.date()
    for w in getattr(nations, "wars", []) or []:
        if {str(x) for x in w.get("between", ())} != {a, b}:
            continue
        since = w.get("since")
        if since is None or (isinstance(since, date) and since <= day):
            return True
    return False


def verdict(world: Any, prize: Any, record: dict[str, Any], port: Any) -> tuple[str, str]:
    """(the sentence, the reason): condemned, restored or salvage by the rules of §5.2."""
    nations = getattr(world, "nations", None)
    captor_nation = str(record.get("captor_nation") or "")
    nation_was = str(record.get("nation_was") or "")
    if record.get("recaptor") and str((record.get("retaken") or ("",))[0]) == "retaken":
        return "salvage", "a ship of her own nation retaken from the enemy"
    if nations is not None and _at_war_at(
        nations, captor_nation, nation_was, int(record.get("taken_at", 0)), world
    ):
        return (
            "condemned",
            f"a ship of {_people(nations, nation_was)} at war with the captors at the taking",
        )
    if record.get("outlaw") or getattr(prize, "outlaw", False):
        return "condemned", "an armed ship without a commission, a pirate"
    hull = getattr(prize, "crew", None)
    hold = getattr(hull, "hold", None) if hull is not None else None
    goal = str(record.get("intent_was") or "")
    if hold is not None and nations is not None:
        enemies = set(nations.enemies_of(captor_nation))
        goods = getattr(hold, "goods", {}) or {}
        market = getattr(port, "market", None)
        origins = {
            str(getattr(market.goods.get(g), "origin", "") or "")
            for g in goods
            if market and g in market.goods
        }
        if origins & enemies and any(e in goal.lower() for e in enemies):
            return "condemned", "a neutral carrying an enemy's cargo to an enemy's port"
    return "restored", f"a neutral of {_people(nations, nation_was)} wrongly taken"


def _people(nations: Any, nation_id: str) -> str:
    try:
        n = nations.get(nation_id)
        return str(getattr(n, "name", None) or nation_id)
    except Exception:  # noqa: BLE001
        return nation_id or "no nation"


def court_name(port: Any, captor_home: bool) -> str:
    rows = court_rows(str(getattr(port, "nation", "") or ""))
    if captor_home and rows.get("home_name") and str(getattr(port, "nation", "")) == "britain":
        # a home port's prize goes to the High Court (the Vice-Admiralty courts sat abroad)
        return f"{rows['home_name']}, the prize lying at {port.name}"
    return f"{rows.get('name', 'the prize court')} at {port.name}"


def court_days(port: Any) -> int:
    return int(court_rows(str(getattr(port, "nation", "") or "")).get("days", 7))


# -- the money -------------------------------------------------------------------------------------


def share_out(total: float, sharers: list[dict[str, Any]]) -> list[tuple[dict[str, Any], float]]:
    """The sum divided among the ships in sight by their complements (judgement, FROM
    MEMORY), the captor among them; whole pounds, the remainder to the captor."""
    weights = [max(1, int(s.get("complement", 0) or 0)) for s in sharers]
    whole = float(sum(weights)) or 1.0
    parts = [math.floor(total * w / whole) for w in weights]
    parts[0] += round(total) - sum(parts)
    return list(zip(sharers, [float(p) for p in parts], strict=True))


def shares_words(sum_pounds: float, scheme: dict[str, Any]) -> tuple[str, list[tuple[str, float]]]:
    """'the captain £3,074, ...' by the scheme's classes."""
    out = []
    for c in scheme.get("classes") or []:
        pounds = round(sum_pounds * float(c.get("share", 0.0)))
        out.append((str(c.get("name")), float(pounds)))
    words = ", ".join(f"{name} £{p:,.0f}" for name, p in out)
    return words, out


def accounts_of(hull: Any) -> list[dict[str, Any]]:
    extra = getattr(getattr(hull, "ship", None), "extra", None)
    if extra is None:
        return []
    return extra.setdefault("prize_accounts", [])


def sentence(
    world: Any,
    prize: Any,
    port: Any,
    *,
    override: str | None = None,
    by: str = "the court",
) -> dict[str, Any]:
    """The court's sentence on a prize lying at the port, and the money paid or the costs
    awarded (the module's head). Returns the account."""
    from freesail.world import prizes as P
    from freesail.world.hulls import world_of

    root = world_of(world)
    tick = int(root.clock.tick)
    when = root.clock.ship_time.date()
    rec = dict(P.record_of(prize) or {})
    prize_hull = P._hull(prize)
    captor = P._captor_vessel(root, rec)
    captor_hull = P._hull(captor) if captor is not None else None
    captor_nation = str(rec.get("captor_nation") or (captor.nation if captor is not None else ""))
    home = str(getattr(port, "nation", "")) == captor_nation
    court = court_name(port, home)
    kind, why = (
        verdict(root, prize, rec, port) if override is None else (override, f"by {by}'s word")
    )
    if kind == "salvage":
        # the salvors are the recaptors (the design's §5.2): their purse, their nation's scheme,
        # and no consort of the enemy's shares what the enemy's strike wrote on the record
        recaptor = root.vessels.get(str(rec.get("recaptor") or ""))
        if recaptor is not None:
            captor, captor_hull = recaptor, P._hull(recaptor)
            captor_nation = str(recaptor.nation)
            home = str(getattr(port, "nation", "")) == captor_nation
            court = court_name(port, home)
    rows = money_rows()
    account: dict[str, Any] = {
        "prize": str(prize.id),
        "name": str(prize.name),
        "port": port.id,
        "court": court,
        "sentence": kind,
        "why": why,
        "tick": tick,
        "lines": [],
        "shares": [],
    }
    val = valuation(root, prize)
    if kind == "restored":
        costs = round(val["hull"] * float(rows.get("costs_share", 0.1)))
        account["costs"] = float(costs)
        text = (
            f"The {prize.name} is restored to her owners by {court}: {why}; the court awards "
            f"costs and damages against the captors, £{costs:,.0f}."
        )
        _pay_costs(root, captor_hull, costs, court, tick)
        P.retake(root, prize, by=court, how="restored")
        _say(root, prize_hull, captor_hull, text, account)
        rec = dict(P.record_of(prize) or {})
        rec["court"] = account
        prize.prize = rec
        return account
    cargo, cargo_lines = _cargo(root, prize_hull, port)
    goods, goods_lines = _prize_goods(root, prize_hull, port)
    head = head_money(rec)
    gross = val["hull"] + val["guns"] + val["stores"] + cargo + goods
    if kind == "salvage":
        gross = round(gross * float(rows.get("salvage_share", 0.125)))
        head = 0.0
    agent = round(gross * float(rows.get("agent_share", 0.05)))
    fees = float(rows.get("court_fees_pounds", 20.0))
    net = max(0.0, gross - agent - fees) + head
    reserved = 0.0
    service = str(rec.get("service") or "")
    if kind == "salvage" and captor is not None:
        service = P._service_of(captor)
    role_was = str(rec.get("role_was") or "")
    if (
        kind == "condemned"
        and bool(rows.get("purchase_for_the_service", True))
        and service == "kings"
        and role_was in SHIP_OF_WAR_ROLES
    ):
        reserved = round(net * float(rows.get("reserved_share", 0.25)))
    paid_now = net - reserved
    account.update(
        {
            "valuation": val,
            "cargo": cargo,
            "goods": goods,
            "head_money": head,
            "agent": float(agent),
            "fees": fees,
            "gross": float(gross),
            "net": float(net),
            "reserved": float(reserved),
            "paid": float(paid_now),
        }
    )
    lines = [
        f"the hull ({val['tons']:.0f} tons burthen) and her stores £{val['hull']:,.0f}",
        f"her guns £{val['guns']:,.0f}",
        *cargo_lines,
        *goods_lines,
        f"the head money £{head:,.0f}" + ("" if head else " (a merchantman)"),
        f"the agent's commission £{agent:,.0f} and the court's fees £{fees:,.0f} deducted",
    ]
    if reserved:
        lines.append(
            f"a fourth, £{reserved:,.0f}, reserved for the purchase for the service, with a later "
            "sentence of the court"
        )
    # the sharers: the captor first, then every ship in sight at the strike
    if kind == "salvage" and captor is not None:
        sharers = [
            {"id": str(captor.id), "name": str(captor.name), "complement": _complement(captor)}
        ]
    else:
        sharers = [
            {
                "id": rec.get("captor"),
                "name": rec.get("captor_name"),
                "complement": int(
                    rec.get("captor_complement") or _complement(captor) if captor else 0
                ),
            }
        ]
        for s in rec.get("in_sight") or []:
            if str(s.get("id")) != str(rec.get("captor")) and bool(
                rows.get("in_sight_shared", True)
            ):
                sharers.append(dict(s))
    parts = share_out(paid_now, sharers)
    scheme = scheme_for(captor_nation, when, service)
    for sharer, part in parts:
        words, classes = shares_words(part, scheme)
        account["shares"].append(
            {
                "ship": sharer.get("id"),
                "name": sharer.get("name"),
                "pounds": part,
                "classes": classes,
            }
        )
        hull = _hull_by_id(root, sharer.get("id"))
        who = sharer.get("name") or "the captors"
        shared = ""
        if len(parts) > 1:
            others = ", ".join(str(s.get("name")) for s, _ in parts if s is not sharer)
            shared = f" shared with {others}, in sight at the strike: the {who}'s part"
        line = (
            f"Prize money paid at {port.name} for the {prize.name}, {kind} by {court}: "
            + "; ".join(lines)
            + f";{shared} £{part:,.0f} by the eighths"
            + (f" ({scheme.get('source', '')})" if scheme.get("british_kept") else "")
            + f": {words}."
        )
        purse = getattr(hull, "purse", None) if hull is not None else None
        if purse is not None and part > 0:
            purse_line = purse.receive(part, "the court", f"prize money for the {prize.name}", tick)
            line += f" The purse: {purse.words()}."
            account.setdefault("purse_lines", []).append(purse_line)
        if hull is not None:
            accounts_of(hull).append(account)
            for text in lines:
                hull.record(
                    Severity.ROUTINE,
                    "paper.written",
                    f"The prize account: {text}.",
                    data={"paper": "the prize account", "prize": str(prize.id)},
                )
            hull.record(
                Severity.URGENT,
                "prize.money",
                line,
                data={"prize": str(prize.id), "paid": part, "sentence": kind, "court": court},
            )
    if prize_hull is not None:
        prize_hull.record(
            Severity.URGENT,
            "prize.sentenced",
            f"The {prize.name} is {kind} by {court}: {why}.",
            data={"sentence": kind, "court": court},
        )
    P._story(prize, tick, f"{kind} by {court}")
    if captor is not None:
        P._story(captor, tick, f"the {prize.name} {kind} at {port.name}: £{paid_now:,.0f}")
    rec["court"] = account
    prize.prize = rec
    if reserved:
        rec["reserved_due"] = tick + court_days(port) * 86400
    return account


def _pay_costs(root: Any, captor_hull: Any, costs: float, court: str, tick: int) -> None:
    purse = getattr(captor_hull, "purse", None) if captor_hull is not None else None
    if purse is None or costs <= 0:
        return
    try:
        purse.pay_to(costs, court, "costs and damages awarded against us", tick)
    except ValueError:
        purse.owe(costs, court, f"£{costs:,.0f} of costs and damages", tick)


def _say(root: Any, prize_hull: Any, captor_hull: Any, text: str, account: dict[str, Any]) -> None:
    for hull in (captor_hull, prize_hull):
        if hull is not None:
            hull.record(Severity.URGENT, "prize.sentenced", text, data=dict(account))
            if hull is captor_hull:
                accounts_of(hull).append(account)


def _hull_by_id(root: Any, hid: Any) -> Any:
    from freesail.world.movement import hull_of

    hull = hull_of(root, str(hid or ""))
    if hull is None and str(hid) == getattr(getattr(root, "players", None), "id", None):
        return root.players
    return hull


def pay_reserved(world: Any, prize: Any) -> None:
    """The reserved fourth paid with the later sentence (the purchase for the service)."""
    from freesail.world import prizes as P
    from freesail.world.hulls import world_of

    root = world_of(world)
    rec = dict(P.record_of(prize) or {})
    account = rec.get("court") or {}
    reserved = float(account.get("reserved", 0.0) or 0.0)
    if not reserved or account.get("reserved_paid"):
        return
    tick = int(root.clock.tick)
    captor = P._captor_vessel(root, rec)
    hull = P._hull(captor) if captor is not None else None
    purse = getattr(hull, "purse", None) if hull is not None else None
    if purse is not None:
        purse.receive(reserved, "the court", f"the reserved fourth for the {prize.name}", tick)
    if hull is not None:
        hull.record(
            Severity.URGENT,
            "prize.money",
            f"The reserved fourth for the {prize.name}, purchased for the service, "
            f"£{reserved:,.0f}, paid by {account.get('court', 'the court')}."
            + (f" The purse: {purse.words()}." if purse is not None else ""),
            data={"prize": str(prize.id), "paid": reserved, "reserved": True},
        )
    account["reserved_paid"] = tick
    rec.pop("reserved_due", None)
    rec["court"] = account
    prize.prize = rec
