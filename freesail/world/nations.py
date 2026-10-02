"""The nations table (spec M5 §24; package 35): who is at war with whom, who issues
letters of marque, what the flags say, and each port's nation, from `data/nations.yaml`.

The table is small on purpose. What the game reads from it now is the **stance** of a
port toward a ship (spec M5 §23: open, neutral, closed, hostile), which decides whether
the pilot comes off and whether she is entered at all (`Nations.stance`), and the words
of a nation's colours for the lookout's "a stranger, her colours not made out" (package
36). Prizes, convoys and blockades are milestone 7's; the table is theirs to read.

The wars change in play: the news of a war declared or a peace made arrives by the pilot
or the boat (never a line from nowhere) and moves the table (`declare_war`, `make_peace`),
and the market's war rule reads it the next time a price is asked (truth 69's "a week's
war news moves a price"). The table's state is a function of the seed and the journal,
as every state is, so a replay has it again; a checkpoint holds it whole.

Every date in the file is from memory and the file says so; nothing here is a reading.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

__all__ = ["NATIONS_PATH", "STANCES", "Nation", "Nations", "load_nations"]

NATIONS_PATH = Path(__file__).resolve().parents[2] / "data" / "nations.yaml"

# The four stances of spec M5 §23, in the order of welcome.
STANCES = ("open", "neutral", "closed", "hostile")

# The names lists of data/crew/names.yaml and the nation a ship whose company is drawn
# from each belongs to by default (the scenario may say otherwise).
NAMES_TO_NATION = {"english": "britain", "american": "united-states", "french": "france"}


@dataclass(frozen=True)
class Nation:
    id: str
    name: str
    adjective: str
    people: str
    names: str
    colours: str
    letters_of_marque: bool
    closed_to: tuple[str, ...] = ()
    flag: str = ""  # the flag's short word for the lookout: "the red ensign" (package 36)


@dataclass
class Nations:
    """The table as loaded, and the wars as they stand now."""

    nations: dict[str, Nation]
    wars: list[dict[str, Any]]  # {"between": (a, b), "since": date, "source": str}
    allies: list[tuple[str, str]]
    port_nations: dict[str, str]
    as_of: date | None = None
    # the wars declared and the peaces made in play, in order: (what, a, b, when)
    news: list[tuple[str, str, str, str]] = field(default_factory=list)

    # -- reading ----------------------------------------------------------------------

    def get(self, nation_id: str) -> Nation:
        key = _key(nation_id)
        if key not in self.nations:
            known = ", ".join(self.nations)
            raise KeyError(f"no nation '{nation_id}' in the table (the nations are {known})")
        return self.nations[key]

    def find(self, words: str) -> Nation | None:
        """A nation by its id, its name or its adjective ('French', 'the French')."""
        key = _key(words)
        for n in self.nations.values():
            if key in (n.id, _key(n.name), _key(n.adjective), _key(n.people)):
                return n
        return None

    def at_war(self, a: str, b: str) -> bool:
        a, b = _key(a), _key(b)
        if a == b:
            return False
        return any({a, b} == set(w["between"]) for w in self.wars)

    def enemies_of(self, nation_id: str) -> list[str]:
        key = _key(nation_id)
        out = []
        for w in self.wars:
            pair = list(w["between"])
            if key in pair:
                out.append(pair[1] if pair[0] == key else pair[0])
        return sorted(out)

    def allied(self, a: str, b: str) -> bool:
        a, b = _key(a), _key(b)
        return any({a, b} == set(pair) for pair in self.allies)

    def stance(self, port_nation: str, ship_nation: str, closed_to: Any = ()) -> str:
        """A port's stance toward a ship (spec M5 §23): open to its own nation; hostile to
        a nation its own is at war with; closed to a nation the port, or its nation's
        table entry, closes its ports to without war; neutral to the rest. `closed_to`
        is the port file's own list."""
        port_nation, ship_nation = _key(port_nation), _key(ship_nation)
        if port_nation == ship_nation:
            return "open"
        if self.at_war(port_nation, ship_nation):
            return "hostile"
        closed = {_key(c) for c in closed_to} | set(self.get(port_nation).closed_to)
        if ship_nation in closed:
            return "closed"
        return "neutral"

    def nation_of_names(self, names_list: str) -> str:
        """The nation a ship belongs to by the names list her company is drawn from."""
        return NAMES_TO_NATION.get(str(names_list), "britain")

    # -- the news ---------------------------------------------------------------------

    def declare_war(self, a: str, b: str, when: str = "", source: str = "the news") -> bool:
        """A war declared between two nations: True when the table changes."""
        a, b = _key(a), _key(b)
        self.get(a), self.get(b)
        if a == b or self.at_war(a, b):
            return False
        self.wars.append({"between": (a, b), "since": when or None, "source": source})
        self.news.append(("war", a, b, when))
        return True

    def make_peace(self, a: str, b: str, when: str = "") -> bool:
        a, b = _key(a), _key(b)
        before = len(self.wars)
        self.wars = [w for w in self.wars if {a, b} != set(w["between"])]
        if len(self.wars) != before:
            self.news.append(("peace", a, b, when))
            return True
        return False

    def wars_words(self) -> str:
        """'Britain at war with France, Spain and the Batavian Republic; the United States,
        Portugal and Denmark at peace with all', each war said once."""
        said: set[str] = set()
        parts = []
        for n in self.nations.values():
            if n.id in said:
                continue
            enemies = [e for e in self.enemies_of(n.id) if e not in said]
            if enemies:
                names = [self.nations[e].name for e in enemies]
                parts.append(f"{n.name} at war with {_and(names)}")
                said.add(n.id)
        quiet = [n.name for n in self.nations.values() if not self.enemies_of(n.id)]
        if quiet:
            parts.append(f"{_and(quiet)} at peace with all")
        return "; ".join(parts) if parts else "every nation at peace"

    def to_dict(self) -> dict[str, Any]:
        return {
            "wars": [
                {"between": list(w["between"]), "since": str(w.get("since") or "")}
                for w in self.wars
            ],
            "news": [list(n) for n in self.news],
        }


def load_nations(path: str | Path = NATIONS_PATH) -> Nations:
    doc = yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}
    nations: dict[str, Nation] = {}
    for nid, d in (doc.get("nations") or {}).items():
        nations[str(nid)] = Nation(
            id=str(nid),
            name=str(d.get("name") or nid),
            adjective=str(d.get("adjective") or nid),
            people=str(d.get("people") or d.get("name") or nid),
            names=str(d.get("names") or "english"),
            colours=str(d.get("colours") or ""),
            letters_of_marque=bool(d.get("letters_of_marque", False)),
            closed_to=tuple(str(x) for x in (d.get("closed_to") or [])),
            flag=str(d.get("flag") or ""),
        )
    wars = []
    for w in doc.get("wars") or []:
        pair = tuple(str(x) for x in w.get("between") or [])
        if len(pair) != 2:
            raise ValueError(f"{path}: a war is between two nations, not {pair}")
        for nid in pair:
            if nid not in nations:
                raise ValueError(
                    f"{path}: the war between {pair} names '{nid}', which is no nation"
                )
        wars.append({"between": pair, "since": w.get("since"), "source": str(w.get("source", ""))})
    allies = [tuple(str(x) for x in pair) for pair in (doc.get("allies") or [])]
    ports = {str(k): str(v) for k, v in (doc.get("ports") or {}).items()}
    as_of = doc.get("as_of")
    return Nations(
        nations=nations,
        wars=wars,
        allies=[(a, b) for a, b in allies],
        port_nations=ports,
        as_of=as_of if isinstance(as_of, date) else None,
    )


def _key(words: str) -> str:
    text = str(words).strip().lower().replace("_", "-").replace(" ", "-")
    return text.removeprefix("the-")


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
