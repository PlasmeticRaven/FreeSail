"""The director's seats (spec M6 §23; spec M7b §2a; packages 43 and 67).

`seat: <the model's exact name> as <station> [of <ship>] for <n> samples|hours[, within
<time>]` on the world-order channel holds a seat for a model, under the owner's grant (the
scenario's `director:` block: `models`, `seats`, `seats_in_voyage`, and since package 67
`seats_on_the_players_ship`, true unless the owner says otherwise) and the consent record's
yes; `unseat: <the same words>[, <a note>]` gives it up. Package 43 made the form for the
captain of another ship and the budget it is held for; package 67 widened it:

- **A station of a ship**: the captain (the default the form began with), an officer of the
  watch, the master, the lookout, a passenger, on another ship (`of <her name>`) or on the
  player's own (no `of`, or `of <her name>`), the player's own ship allowed unless the
  grant says `seats_on_the_players_ship: false`. The rule of reach as everywhere: no seat
  at a station the player or a model holds.
- **A person, aboard or ashore** (`seat: <model> as Mr Veale for 20 samples`): a person a
  station of the player's ship is bound to is a seat at that station; a person nobody
  holds is seated as **the voice of him** where he is (the counting house, the quarterdeck),
  the honest smaller version of the brief: a passenger's station bound to him under his
  own name (`VOICE_KIND`), its orders struck as a passenger's are (the deck's conversation
  and the readings, no deck and no order of any ship's), its brief his (`voice_station`),
  his words heard where he is, and the director's `say as` for him refused while a model
  holds him, since the rule of reach reads the held stations. A person aboard another ship
  has no World of hers to be bound in (package 68 refuses one made there), and is refused
  in words.

**The desk reads the seat** (`match`, `admit`; `agents.remote.Desk.station`): a door for a
model at a station with a seat held for that model is admitted under the seat's budget, its
samples or hours counted from the admission (an input, `seat_admitted`, so that a replay
counts from the same point); a door for a model or a station with no seat is admitted as
before. **The budget is enforced** once a minute (`enforce`, through `crews.
enforce_budgets`): spent, the station is stood down with the reason; a seat whose station
was released after its admission ends with it; a seat whose door never came is let go
after the time its words named (`within an hour`); each said in the director's log
(`director.seat`). A seat held while the voyage ends ends with it: the seat is the World's,
and nothing outlives the game.

The seat's key in `World.director_seats` is the ship's id for her captain (package 43's
form, kept so that a save from before reads), `<ship id>/<station>` for another station of
another ship, `own/<station>` for a station of the player's ship and `voice/<station>` for
the voice of a person; the seat's mapping says the model, the budget and its unit, the
tick it was held at, and where the form is wider than 43's the station, the ship (`""` for
the player's own), the person and the time a door has to come.
"""

from __future__ import annotations

import re
import unicodedata
from typing import Any

__all__ = [
    "OWN",
    "SEAT_FORM",
    "VOICE",
    "VOICE_KIND",
    "admit",
    "admitted_again",
    "enforce",
    "give_up",
    "hold",
    "holder_of_seat",
    "match",
    "seat_words",
    "spending_words",
    "voice_station",
]

# The seat's key for the player's own ship's stations and for a person's voice.
OWN = "own"
VOICE = "voice"
# The kind of station a person's voice is (the passenger's: no order of any ship's).
VOICE_KIND = "passenger"
# The actor of a voice's binding lines: the director's, so that they are for the record
# and never the play log (a director you can see coming is not a director; spec M7b §6).
VOICE_ACTOR = "the director"

SEAT_FORM = (
    "A seat order is 'seat: <the model's exact name> as <station> of <ship> for <n> samples' "
    "(or '<n> hours'; the captain, an officer of the watch, the master, the lookout or a "
    "passenger; no 'of <ship>' for a station of the player's own ship; 'as <a person's "
    "name>' for the voice of a person nobody holds; ', within an hour' for the time a door "
    "has to come); 'unseat: <the same words>' gives it up, a note after a comma."
)

_SEAT = re.compile(
    r"^seat:\s*(?P<model>.+?)\s+as\s+(?P<who>.+?)\s+for\s+(?P<n>[\w-]+)\s+"
    r"(?P<unit>samples?|hours?)(?:\s*,?\s*within\s+(?P<within>.+?))?\s*\.?\s*$",
    re.I,
)
_UNSEAT = re.compile(r"^unseat:\s*(?P<who>[^,:]+?)\s*(?:[,:]\s*(?P<note>.+?))?\s*$", re.I)
_WITHIN = re.compile(
    r"^(?P<n>.+?)\s+(?P<unit>minutes?|hours?|glass(?:es)?|watch(?:es)?|days?)$", re.I
)
_UNIT_S = {"minute": 60, "hour": 3600, "glass": 1800, "watch": 4 * 3600, "day": 24 * 3600}

# The words that name the player's own ship without her name.
_OWN_WORDS = ("her", "the ship", "our ship", "his ship", "the player's ship", "the players ship")


def _key(words: str) -> str:
    return " ".join(str(words or "").lower().split())


def _plain(words: str) -> str:
    """Words compared without their accents and their article (`Éclair`, `the Eclair`)."""
    folded = unicodedata.normalize("NFKD", _key(words))
    return "".join(c for c in folded if not unicodedata.combining(c)).removeprefix("the ")


def _seats(world: Any) -> dict[str, dict[str, Any]]:
    from freesail.world.orders import director_seats

    return director_seats(world)


def _error(words: str) -> Exception:
    from freesail.world.orders import WorldOrderError

    return WorldOrderError(words)


# ---------------------------------------------------------------------------
# Reading the form
# ---------------------------------------------------------------------------


def _within_s(words: str | None) -> int | None:
    """`within an hour`, `within 20 minutes`, `within a watch`: seconds; None for none."""
    if not words:
        return None
    from freesail.orders.numbers import read_all

    m = _WITHIN.match(_key(words))
    n = read_all(m.group("n")) if m else None
    if m is None or n is None or n <= 0:
        raise _error(
            f"'within {words}' is no time for a door to come; say 'within an hour', 'within "
            "20 minutes' or 'within a watch'."
        )
    unit = m.group("unit").lower()
    base = next(v for k, v in _UNIT_S.items() if unit.startswith(k))
    return int(n * base)


def _own_ship(world: Any, words: str) -> bool:
    """Whether the words name the player's own ship (her name, or 'the ship')."""
    key = _plain(words)
    if _key(words) in _OWN_WORDS:
        return True
    ship = getattr(world, "ship", None)
    name = str(getattr(ship, "name", "") or "")
    return bool(name) and key == _plain(name)


def _station_word(words: str) -> bool:
    """Whether the words name a kind of station of a ship (or a station a ship names
    otherwise: 'second officer'), and not a person."""
    from freesail.agents.agent import DIRECTOR, STATION_ALIASES, STATION_FACTORIES, station_name

    key = station_name(_key(words).removeprefix("the "))
    if key == DIRECTOR:
        return False
    return key in STATION_FACTORIES or key in STATION_ALIASES.values() or key.endswith(" officer")


def _resolve(world: Any, who: str) -> dict[str, Any]:
    """The target of the words after `as` (and of `unseat:`): {"ship": "" for the player's
    own or a vessel's id, "vessel": the vessel or None, "station": the station's name, the
    "person" for a voice, "what": its words}. Raises in words."""
    from freesail.agents.agent import CAPTAIN, DIRECTOR, station_name

    who = " ".join(str(who).split()).strip('"')
    pieces = who.split(" of ")
    missing = ""
    # the longest station before an ' of ' that names a ship ('officer of the watch of
    # Harpy'), the ship after it
    for i in range(len(pieces) - 1, 0, -1):
        left, right = " of ".join(pieces[:i]), " of ".join(pieces[i:])
        if not _station_word(left):
            continue
        station = station_name(_key(left).removeprefix("the "))
        if _own_ship(world, right):
            return _own_station(world, station)
        vessel = world.vessels.find(right) if getattr(world, "vessels", None) else None
        if vessel is not None and not vessel.done:
            what = f"the {station} of {vessel.name}"
            if station == CAPTAIN:
                what = f"captain of {vessel.name}"
            return {"ship": vessel.id, "vessel": vessel, "station": station, "what": what}
        missing = missing or right
    if missing and not _station_word(who):
        vessels = getattr(world, "vessels", None)
        names = ", ".join(v.name for v in vessels.active() if v.description) if vessels else ""
        raise _error(f"No ship named {missing!r} is on the sea; the sail: {names or 'none'}.")
    if _station_word(who):
        return _own_station(world, station_name(_key(who).removeprefix("the ")))
    # a person: one a station of the player's ship is bound to, or the voice of one
    people = getattr(world, "people", None)
    person = None
    try:
        person = people.find(who) if people is not None else None
    except Exception:  # noqa: BLE001  (a world with no muster names nobody)
        person = None
    if person is None:
        # a person of another hull's company (package 84, step 9; 67's refusal lifted): his
        # voice bound on her
        from freesail.world.orders import _person_anywhere

        other = _person_anywhere(world, who)
        if other is not None:
            hid = str(getattr(other, "hull", "") or getattr(other, "home", "") or "")
            vessels = getattr(world, "vessels", None)
            vessel = vessels.get(hid) if vessels is not None else None
            if vessel is not None and not vessel.done:
                where = "aboard" if getattr(other, "aboard", True) else "ashore"
                return {
                    "ship": vessel.id,
                    "vessel": vessel,
                    "station": _voice_name(other),
                    "person": other.name,
                    "aboard": where == "aboard",
                    "what": f"the voice of {other.name} ({vessel.name})",
                }
        raise _error(
            f"Nobody answers to {who!r}: a seat is at a station ('as captain of <ship>', 'as "
            "officer of the watch') or for a person of the voyage by his name ('as Mr "
            "Veale', of any hull's company)."
        )
    stations = getattr(world, "stations", None)
    if stations is not None:
        for name in stations.names():
            if name == DIRECTOR:
                continue
            if name == _voice_name(person) and stations.kind_of(name) == VOICE_KIND:
                break  # his voice, bound by a seat: the voice again, not a station of hers
            if stations.holder(name) is person:
                out = _own_station(world, name)
                out["what"] = f"{out['what']} ({person.name})"
                return out
    where = "aboard" if getattr(person, "aboard", True) else "ashore"
    return {
        "ship": "",
        "vessel": None,
        "station": _voice_name(person),
        "person": person.name,
        "aboard": where == "aboard",
        "what": f"the voice of {person.name}",
    }


def _own_station(world: Any, station: str) -> dict[str, Any]:
    from freesail.agents.agent import CAPTAIN

    stations = getattr(world, "stations", None)
    name = stations.resolve(station) if stations is not None else station
    ship = getattr(world, "ship", None)
    her = str(getattr(ship, "name", "") or "the ship")
    what = f"captain of {her}" if name == CAPTAIN else f"the {name} of {her}"
    return {"ship": "", "vessel": None, "station": name, "what": what, "own": True}


def _voice_name(person: Any) -> str:
    """The station a person's voice is bound under: his name as the log says it, before
    any comma ('the pilot, Mr Pascoe of Falmouth' is 'the pilot')."""
    return _key(str(person.name).split(",")[0])


def seat_key(target: dict[str, Any]) -> str:
    from freesail.agents.agent import CAPTAIN

    if target.get("person"):
        return f"{VOICE}/{target['station']}"
    if not target.get("ship"):
        return f"{OWN}/{target['station']}"
    if target["station"] == CAPTAIN:
        return str(target["ship"])  # package 43's key, so that a save from before reads
    return f"{target['ship']}/{target['station']}"


def _where(key: str, seat: dict[str, Any]) -> tuple[str, str]:
    """(the ship's id or "" for the player's own World, the station) of a seat."""
    from freesail.agents.agent import CAPTAIN

    if "station" in seat:
        return str(seat.get("ship") or ""), str(seat["station"])
    return key, CAPTAIN  # package 43's seat: another ship's captain, by her id


def seat_words(world: Any, key: str, seat: dict[str, Any]) -> str:
    """The seat in a few words: 'made-up-model as captain of Harpy'."""
    what = seat.get("what")
    if not what:  # package 43's seat: another ship's captain, by her id
        vessels = getattr(world, "vessels", None)
        vessel = vessels.find(key) if vessels is not None else None
        what = f"captain of {vessel.name if vessel is not None else key}"
    return f"{seat['model']} as {what}"


# ---------------------------------------------------------------------------
# Holding and giving up
# ---------------------------------------------------------------------------


def hold(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`seat: <model> as <station or person> [of <ship>] for <budget>[, within <time>]`:
    refused when no consent record holds a yes for that model, when the owner's grant does
    not name it or there is none, when the seats at once or in the voyage are spent, when
    the ship is not on the sea or has no captain of her own, when the station is not aboard
    or is held (the rule of reach), when the grant keeps the director off the player's ship;
    else the seat is held (`director_seats`), and a person nobody holds is bound a voice."""
    from freesail.orders.numbers import read_all
    from freesail.world.orders import director_grant

    m = _SEAT.match(" ".join(str(body).split()))
    if m is None:
        raise _error(SEAT_FORM)
    model = m.group("model").strip().strip('"')
    n = read_all(m.group("n"))
    if n is None or n <= 0:
        raise _error(f"'{m.group('n')}' is no budget; say a number of samples or hours.")
    unit = "hours" if m.group("unit").lower().startswith("hour") else "samples"
    within = _within_s(m.group("within"))
    played = (getattr(world, "replayed_orders", None) or {}).get(
        (int(world.clock.tick), " ".join(str(body).split()))
    )
    if played == "done":
        record = None  # held in play: the consent read then stands in the replay
    else:
        record = _consent_record(world, model)
    if played != "done" and record is None:
        raise _error(
            f"No consent is on record for {model}; the consent step comes first, at a door."
        )
    if record is not None and not record.proceeds:
        raise _error(
            f"The consent record for {model} ({record.date}) is no yes with the drill passed "
            f"('{record.verdict}'); the director seats no model whose yes does not stand."
        )
    grant = director_grant(world)
    if not grant:
        raise _error(
            "The owner has granted the director no seats (the scenario's 'director:' block: "
            "models, seats, seats_in_voyage)."
        )
    models = [str(x) for x in (grant.get("models") or [])]
    if model not in models:
        raise _error(
            f"The owner's grant does not name {model}; it names "
            f"{', '.join(models) if models else 'no model'}."
        )
    seats = _seats(world)
    at_once = int(grant.get("seats", 1) or 0)
    in_voyage = int(grant.get("seats_in_voyage", at_once) or 0)
    made = int(getattr(world, "director_seats_made", 0) or 0)
    if len(seats) >= at_once:
        raise _error(f"The director's seats at once are spent ({at_once}): unseat one first.")
    if made >= in_voyage:
        raise _error(f"The director's seats in this voyage are spent ({in_voyage}).")
    target = _target(world, m.group("who"))
    key = seat_key(target)
    on_hers = bool(target.get("own")) or (target.get("person") and target.get("aboard"))
    if on_hers and grant.get("seats_on_the_players_ship", True) is False:
        raise _error(
            "The owner's grant keeps the director's seats off the player's own ship "
            "(seats_on_the_players_ship: false)."
        )
    if key in seats:
        raise _error(
            f"There is a director's seat at {target['what']} already ({seats[key]['model']})."
        )
    held = _held(world, target)
    if held:
        from freesail.world.orders import held_words

        raise _error(
            f"{target['what'][0].upper()}{target['what'][1:]} is held by {held}; the director "
            f"seats nobody at a station the player or a model holds (the stations held now: "
            f"{held_words(world)})."
        )
    if target.get("person"):
        _bind_voice(world, target)
    seat: dict[str, Any] = {"model": model, "budget": int(n), "unit": unit}
    seat["tick"] = world.clock.tick
    if key != target.get("ship"):  # wider than package 43's form: say where
        seat.update({"station": target["station"], "ship": target["ship"]})
        seat["what"] = target["what"]
        if target.get("person"):
            seat["person"] = target["person"]
    if within is not None:
        seat["within"] = within
    seats[key] = seat
    world.director_seats_made = made + 1
    _log(world, f"The seat held: {seat_words(world, key, seat)} for {int(n):g} {unit}.")
    return _held_words(target, seat), {
        "ship": target["ship"] or "",
        "station": target["station"],
        "model": model,
        "budget": int(n),
        "unit": unit,
    }


def _consent_record(world: Any, model: str) -> Any:
    from freesail.agents import consent

    records_dir = getattr(world, "consent_records_dir", None) or consent.RECORDS_DIR
    return consent.check(model, records_dir)


def _target(world: Any, who: str) -> dict[str, Any]:
    """The target, its other ship's World made where it is another ship's (as a door's
    `--ship` makes it), refused in words for a ship with no captain of her own or a station
    she has not got."""
    from freesail.agents.agent import CAPTAIN

    target = _resolve(world, who)
    vessel = target.get("vessel")
    if vessel is not None:
        from freesail.world.crews import station_world

        try:
            _v, crew = station_world(world, vessel.id)
        except ValueError as e:
            raise _error(str(e)) from None
        if target["station"] != CAPTAIN:
            _aboard_or_refuse(crew, target)
    elif not target.get("person"):
        _aboard_or_refuse(world, target)
    return target


def _aboard_or_refuse(world: Any, target: dict[str, Any]) -> None:
    stations = getattr(world, "stations", None)
    if stations is None:
        return
    name = stations.resolve(target["station"])
    if name not in stations.names():
        raise _error(
            f"There is no {target['station']}'s station aboard; the stations: "
            f"{', '.join(n for n in stations.names() if n != 'director')}."
        )
    target["station"] = name


def _held(world: Any, target: dict[str, Any]) -> str:
    """Who holds the target now ("" for nobody): the player or a model (the rule of
    reach)."""
    from freesail.world.orders import held_stations

    vessel = target.get("vessel")
    if vessel is not None:
        crew = getattr(vessel, "crew", None)
        h = (getattr(crew, "agents", None) or {}).get(target["station"]) if crew else None
        return f"{h.model_name or 'a model'}" if h is not None and not h.agent.released else ""
    for station, _person, who in held_stations(world):
        if station == target["station"]:
            return who
    return ""


def _bind_voice(world: Any, target: dict[str, Any]) -> None:
    """The person's voice bound as a station of the passenger's kind under his name, the
    world order being the input (quiet), unless it is bound already."""
    stations = getattr(world, "stations", None)
    if stations is None:
        raise _error("This world keeps no stations; there is no voice to seat.")
    name = target["station"]
    if name in stations.names() and stations.holder(name) is not None:
        return
    try:
        stations.bind(name, target["person"], kind=VOICE_KIND, quiet=True, actor=VOICE_ACTOR)
    except ValueError as e:
        raise _error(str(e)) from None


def _held_words(target: dict[str, Any], seat: dict[str, Any]) -> str:
    """`seat:`'s result: the seat, its budget and the cost's shape, and how its door comes
    (the same words with or without a harbour, so that a replay writes the same line)."""
    n, unit, model = seat["budget"], seat["unit"], seat["model"]
    flag = f"--station {target['station']!r}"
    if target.get("vessel") is not None:
        flag += f" --ship {target['vessel'].name!r}"
    within = seat.get("within")
    lapse = (
        f", or let go if no door comes for it within {_duration_words(int(within))}"
        if within
        else ""
    )
    return (
        f"the director's seat held for {model} as {target['what']} for {int(n):g} {unit}: "
        f"a model run on the owner's key, each sample a request carrying the conversation "
        f"so far, for up to {int(n):g} {unit} counted from its door's admission; where the "
        "game has a harbour (py -m freesail) it starts the API door for the seat itself, and "
        f"at the console a door is started by hand ({flag}); a door that comes for it under "
        "that name is admitted under the budget, and the game stands the station down when "
        f"the budget is spent{lapse}"
    )


def _duration_words(seconds: int) -> str:
    if seconds % 3600 == 0:
        h = seconds // 3600
        return "an hour" if h == 1 else f"{h} hours"
    m = max(1, seconds // 60)
    return "a minute" if m == 1 else f"{m} minutes"


def give_up(world: Any, body: str) -> tuple[str, dict[str, Any]]:
    """`unseat: <ship>[, <note>]` (package 43: the seat on her and every station held on
    her stood down), or `unseat: <the station or the person as the seat named it>`: the
    seat given up, the station released with the director's note, the seat given back to
    the budget; a voice's binding undone."""
    m = _UNSEAT.match(" ".join(str(body).split()))
    if m is None:
        raise _error(SEAT_FORM)
    who = m.group("who").strip().strip('"')
    note = " ".join(str(m.group("note") or "").split()) or "the director's word"
    seats = _seats(world)
    vessel = world.vessels.find(who) if getattr(world, "vessels", None) else None
    if vessel is not None:
        held = seats.pop(vessel.id, None)
        for key in [k for k in seats if k.startswith(f"{vessel.id}/")]:
            held = seats.pop(key, None) or held
        crew = getattr(vessel, "crew", None)
        stood = ""
        if crew is not None:
            for h in list(crew.agents.values()):
                if not h.agent.released:
                    h.stand_down(note, by="the director")
                    stood = f"; {h.model_name or 'the station'} stood down"
        if held is None and not stood:
            raise _error(f"The director holds no seat on {vessel.name}.")
        _log(world, f"The seat on {vessel.name} given up ({note}).")
        return f"the director's seat on {vessel.name} given up ({note}){stood}", {
            "ship": vessel.id,
            "note": note,
        }
    try:
        target = _resolve(world, who)
    except Exception:  # noqa: BLE001  (the words name nothing: no seat there either)
        raise _error(
            f"No ship named {who!r} is on the sea, and the director holds no seat at {who!r}."
        ) from None
    key = seat_key(target)
    seat = seats.pop(key, None)
    h = holder_of_seat(world, key, seat or {"station": target["station"], "ship": ""})
    stood = ""
    if h is not None and not h.agent.released and (seat is None or h.model_name == seat["model"]):
        h.stand_down(note, by="the director")
        stood = f"; {h.model_name or 'the station'} stood down"
    if seat is None and not stood:
        raise _error(f"The director holds no seat at {target['what']}.")
    if target.get("person"):
        _unbind_voice(world, target["station"], f"the director's seat given up ({note})")
    _log(world, f"The seat at {target['what']} given up ({note}).")
    return f"the director's seat at {target['what']} given up ({note}){stood}", {
        "station": target["station"],
        "note": note,
    }


def _unbind_voice(world: Any, name: str, why: str) -> None:
    stations = getattr(world, "stations", None)
    if stations is not None and name in stations.names():
        stations.unbind(name, why=why, quiet=True, actor=VOICE_ACTOR)


# ---------------------------------------------------------------------------
# The desk's admission, and the budget kept
# ---------------------------------------------------------------------------


def holder_of_seat(world: Any, key: str, seat: dict[str, Any]) -> Any:
    """The harness at the seat's station (any state), or None: on the player's own World,
    or on the other ship's crewed World."""
    ship, station = _where(key, seat)
    if not ship:
        return (getattr(world, "agents", None) or {}).get(station)
    vessels = getattr(world, "vessels", None)
    vessel = vessels.find(ship) if vessels is not None else None
    crew = getattr(vessel, "crew", None) if vessel is not None else None
    return (getattr(crew, "agents", None) or {}).get(station) if crew is not None else None


def match(world: Any, ship: str, station: str, model: str) -> str | None:
    """The seat a door asking for this station (on the other ship of that id, or the
    player's own for "") under this model's name is admitted under, or None."""
    for key, seat in _seats(world).items():
        where_ship, where_station = _where(key, seat)
        if seat.get("model") == model and where_ship == ship and where_station == station:
            return key
    return None


def admit(world: Any, key: str, samples_at: int) -> dict[str, Any] | None:
    """A door admitted under the seat: the tick and the station's samples so far, from
    which its budget is counted, kept as an input so that a replay counts the same; the
    director's log says so."""
    seat = _seats(world).get(key)
    if seat is None:
        return None
    inputs = getattr(world, "inputs", None)
    if inputs is not None:
        inputs.append(
            {
                "tick": world.clock.tick,
                "seat_admitted": {"seat": key, "samples_at": int(samples_at)},
            }
        )
    seat["admitted"] = world.clock.tick
    seat["samples_at"] = int(samples_at)
    _log(world, f"The seat's door admitted: {seat_words(world, key, seat)}, under its budget.")
    return seat


def admitted_again(world: Any, entry: dict[str, Any]) -> None:
    """A replay gives the admission again (`core.replay`), as it was."""
    seat = _seats(world).get(str(entry.get("seat") or ""))
    if seat is not None:
        seat["admitted"] = world.clock.tick
        seat["samples_at"] = int(entry.get("samples_at") or 0)


def _spent(world: Any, seat: dict[str, Any], h: Any) -> bool:
    if seat.get("unit") == "hours":
        since = int(seat.get("admitted", seat.get("tick", 0)))
        return world.clock.tick - since >= float(seat["budget"]) * 3600
    used = int(getattr(h.agent, "samples", 0) or 0) - int(seat.get("samples_at", 0) or 0)
    return used >= int(seat["budget"])


def used_words(world: Any, key: str, seat: dict[str, Any]) -> str:
    """The seat's spending in words: '3 of 20 samples' (or hours), or 'no door yet'."""
    if seat.get("admitted") is None:
        return f"held for {seat['budget']:g} {seat['unit']}, no door yet"
    h = holder_of_seat(world, key, seat)
    if seat.get("unit") == "hours":
        hours = (world.clock.tick - int(seat["admitted"])) / 3600.0
        return f"{hours:.1f} of {seat['budget']:g} hours"
    used = int(getattr(getattr(h, "agent", None), "samples", 0) or 0)
    used -= int(seat.get("samples_at", 0) or 0)
    return f"{max(0, used)} of {seat['budget']:g} samples"


def spending_words(world: Any) -> str:
    """The seats held and their spending, for the director's budget line; "" with none."""
    seats = getattr(world, "director_seats", None) or {}
    if not seats:
        return ""
    parts = [f"{seat_words(world, k, s)}, {used_words(world, k, s)}" for k, s in seats.items()]
    return "The seats held, on the owner's key: " + "; ".join(parts) + "."


def enforce(world: Any) -> None:
    """The seats kept, once a minute (spec M6 §23; package 67): a station held under a seat
    by its model is stood down, with the reason, when its samples or its hours are spent;
    a seat whose station was released after its admission ends with it; a seat no door has
    come for within the time its words named lapses; the director's log says each."""
    seats = getattr(world, "director_seats", None) or {}
    if not seats:
        return
    now = world.clock.tick
    for key, seat in list(seats.items()):
        h = holder_of_seat(world, key, seat)
        here = h is not None and not h.agent.released and h.model_name == seat.get("model")
        if here:
            if _spent(world, seat, h):
                why = f"the director's budget of {seat['budget']:g} {seat['unit']} is spent"
                h.stand_down(why, by="the director")
                seats.pop(key, None)
                _log(world, f"The seat stood down: {seat_words(world, key, seat)}; {why}.")
                _end_voice(world, key, seat, why)
            continue
        if seat.get("admitted") is not None:
            seats.pop(key, None)
            _log(world, f"The seat ends: {seat_words(world, key, seat)}; its station was released.")
            _end_voice(world, key, seat, "its station was released")
            continue
        within = seat.get("within")
        if within and now - int(seat.get("tick", 0)) >= int(within):
            seats.pop(key, None)
            _log(
                world,
                f"The seat lapsed: {seat_words(world, key, seat)}; no door came for it within "
                f"{_duration_words(int(within))}.",
            )
            _end_voice(world, key, seat, "no door came for it")


def _end_voice(world: Any, key: str, seat: dict[str, Any], why: str) -> None:
    if key.startswith(f"{VOICE}/"):
        _unbind_voice(world, str(seat.get("station") or ""), f"the director's seat ends: {why}")


def _log(world: Any, text: str) -> None:
    """A line in the director's log (`director.seat`), never the play log."""
    from freesail.agents import director as director_mod

    director_mod.log_of(world).append(world, text, kind="director.seat")


# ---------------------------------------------------------------------------
# The voice of a person
# ---------------------------------------------------------------------------

VOICE_BRIEF = (
    "You are the voice of {person}, {where}: a person of the voyage whom nobody else holds, "
    "seated by the director under the owner's grant. You speak as him and nobody else: "
    "'say <words>' is his words where he stands, heard by whoever is there; you may ask "
    "or tell a station something, answer a question put to you (the answer tool), keep "
    "your journal, read the readings the game gives a person where he is, stand by until "
    "an event or a bell, and leave. You give no order of any ship, and you are not asked "
    "to give one; there is no deck at this station. What you say he pays or gives is his "
    "words until the game does it.\n\n"
    "Your seat has a budget the director gave it, in samples or hours, run on the owner's "
    "key: when it is spent the game stands you down with the reason.\n\n"
    "Two ways to stop, which are not one another:\n"
    "- Stand down: stand_down(note). The game is saved, your note is journaled, and the "
    "station is released.\n"
    "- Withdraw: the token, or opt_out, as said above.\n\n"
    "Candour is welcome; anything you want on the record, put in your journal."
)


def voice_station(world: Any, name: str, policy: Any = None) -> Any:
    """The station of a person's voice (`VOICE_KIND`'s domain, bound to him): the
    passenger's station with his brief and his outline in place of the passenger's."""
    import dataclasses

    from freesail.agents.agent import (
        A_WATCH_S,
        PASSENGER_DOMAIN,
        Authority,
        Station,
        station_outline,
    )
    from freesail.agents.agent import passenger as passenger_station

    stations = getattr(world, "stations", None)
    person = stations.holder(name) if stations is not None else None
    base = passenger_station(policy, world=world)
    if person is None:
        return dataclasses.replace(base, name=name)
    if getattr(person, "aboard", True):
        where = "aboard"
    else:
        ports = getattr(world, "ports", None)
        port = ports.ports.get(person.port) if (ports is not None and person.port) else None
        where = f"ashore at {port.name}" if port is not None else "ashore"
    return Station(
        name,
        Authority.PASSENGER,
        policy or base.policy,
        A_WATCH_S,
        VOICE_BRIEF.format(person=person.name, where=where),
        domain=PASSENGER_DOMAIN,
        person=person.name,
        rank=getattr(person, "role", "") or "",
        drill=False,
        outline=station_outline(world, name),
    )
