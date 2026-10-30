"""The nations table (spec M5 §24; package 35): who is at war with whom, who issues
letters of marque, what the flags say, and each port's nation, from `data/nations.yaml`.

The table is small on purpose. What the game reads from it now is the **stance** of a
port toward a ship (spec M5 §23: open, neutral, closed, hostile), which decides whether
the pilot comes off and whether she is entered at all (`Nations.stance`), and the words
of a nation's colours for the lookout's "a stranger, her colours not made out" (package
36). A blockaded port (package 39d; its file's `state:`) is closed to the blockaders'
enemies (`Nations.stance`'s `blockaded_by`). Prizes, convoys and the blockading squadrons
are milestone 7's; the table is theirs to read.

The wars change in play: the news of a war declared or a peace made arrives by the pilot
or the boat (never a line from nowhere) and moves the table (`declare_war`, `make_peace`),
and the market's war rule reads it the next time a price is asked (truth 69's "a week's
war news moves a price"). The table's state is a function of the seed and the journal,
as every state is, so a replay has it again; a checkpoint holds it whole.

Every date in the file is from memory and the file says so; nothing here is a reading.
"""

from __future__ import annotations

import functools
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path
from typing import Any

import yaml

__all__ = ["DEFAULT_HABITS", "NATIONS_PATH", "STANCES", "Nation", "Nations", "load_nations"]

NATIONS_PATH = Path(__file__).resolve().parents[2] / "data" / "nations.yaml"

# The four stances of spec M5 §23, in the order of welcome.
STANCES = ("open", "neutral", "closed", "hostile")

# The names lists of data/crew/names.yaml and the nation a ship whose company is drawn
# from each belongs to by default (the scenario may say otherwise).
NAMES_TO_NATION = {"english": "britain", "american": "united-states", "french": "france"}


# The habit of a nation the table does not know (a scenario's nation is always the
# table's, so this is the floor): the common one.
DEFAULT_HABITS: dict[str, Any] = {"range_factor": 1.0, "aim": "hull", "roll": "down"}
# The marines' kits (package 73, spec M7 §11): `data/marines.yaml`, a kit a nation names
# under `marines: {kit: ...}`; the basic kit stands where none is named.
MARINES_PATH = Path(__file__).resolve().parents[2] / "data" / "marines.yaml"


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
    # package 71 (the owner, 2026-10-24): the nation's habit in action over the role's
    # figures (`range_factor`, `aim`, `roll`, `source`), read by `Captain._habit`; and her
    # signal books' root under data/signals/ with its system (`well-built` or `basic`)
    habits: dict[str, Any] = field(default_factory=dict)
    signals_root: str = "basic"
    # package 73 (spec M7 §11): the marines' kit named, a key of data/marines.yaml
    marines: dict[str, Any] = field(default_factory=dict)
    signals_system: str = "basic"
    # package 72 (spec M7 §22): the nation's naval knobs (`naval:`: who keeps the sea, who
    # keeps port and slips out when the blockade is blown off, who convoys and under what,
    # whose privateers chase what pays), read by the business and the regimes
    naval: dict[str, Any] = field(default_factory=dict)


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
    # the table as the ship sailed with it: the file's wars when the world was made, the
    # knowledge she carries until the news moves it (`sailed_with_words`; the reading
    # `the war` and the paper `the news of the war` open with it)
    sailed_with: list[dict[str, Any]] = field(default_factory=list)

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

    def stance(
        self,
        port_nation: str,
        ship_nation: str,
        closed_to: Any = (),
        blockaded_by: str | None = None,
    ) -> str:
        """A port's stance toward a ship (spec M5 §23): open to its own nation; hostile to
        a nation its own is at war with; closed to a nation the port, or its nation's
        table entry, closes its ports to without war; neutral to the rest. `closed_to`
        is the port file's own list. A blockaded port (package 39d; `blockaded_by`, the
        blockaders' nation) is closed to the blockaders' enemies, its own nation's ships
        among them, and is the table's to everyone else."""
        port_nation, ship_nation = _key(port_nation), _key(ship_nation)
        if blockaded_by and self.at_war(blockaded_by, ship_nation):
            return "closed"
        if port_nation == ship_nation:
            return "open"
        if self.at_war(port_nation, ship_nation):
            return "hostile"
        closed = {_key(c) for c in closed_to} | set(self.get(port_nation).closed_to)
        if ship_nation in closed:
            return "closed"
        return "neutral"

    def marines_kit_of(self, nation_id: str) -> dict[str, Any]:
        """The nation's marines' kit (package 73): its entry's `marines.kit` in
        `data/marines.yaml`, the basic kit where it names none or an unknown one."""
        key = _key(nation_id)
        found = self.nations.get(key)
        name = str((getattr(found, "marines", None) or {}).get("kit") or "basic")
        kits = load_marines().get("kits") or {}
        kit = dict(kits.get(name) or kits.get("basic") or {})
        kit["id"] = name if name in kits else "basic"
        return kit

    def habits_of(self, nation_id: str) -> dict[str, Any]:
        """The nation's habit in action (package 71): the table's figures over the
        common ones where the entry leaves one out."""
        key = _key(nation_id)
        found = self.nations.get(key)
        out = dict(DEFAULT_HABITS)
        if found is not None:
            out.update({k: v for k, v in found.habits.items() if k != "source"})
        return out

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
        """The pilot's news of the wars: 'Britain at war with the Batavian Republic, France
        and Spain', and what the news lately changed ('peace made between Britain and
        France'; a war declared between two others). A nation at peace with all is not
        news (the owner's ruling of 2026-10-10, decision 45): the table grows with the
        chart, the pilot's word does not."""
        parts: list[str] = []
        said: set[frozenset[str]] = set()
        britain = self.nations.get("britain")
        if britain is not None:
            enemies = self.enemies_of(britain.id)
            if enemies:
                names = [self.nations[e].name for e in enemies]
                parts.append(f"{britain.name} at war with {_and(names)}")
                said.update(frozenset((britain.id, e)) for e in enemies)
            else:
                parts.append(f"{britain.name} at peace with all")
        for _kind, a, b, _when in self.news:
            pair = frozenset((a, b))
            if pair in said or a not in self.nations or b not in self.nations:
                continue
            said.add(pair)
            first, second = self.nations[a].name, self.nations[b].name
            if self.at_war(a, b):
                parts.append(f"{first} at war with {second}")
            else:
                parts.append(f"peace made between {first} and {second}")
        return "; ".join(parts) if parts else "every nation at peace"

    def table_words(self, wars: list[dict[str, Any]] | None = None) -> str:
        """A table of wars in words, every war once and the rest at peace: 'Britain at war
        with France, Spain and the Batavian Republic; the United States, Portugal and
        Denmark at peace with all'. The table as it stands when `wars` is None."""
        table = self.wars if wars is None else wars
        enemies: dict[str, list[str]] = {}
        for w in table:
            a, b = w["between"]
            enemies.setdefault(a, []).append(b)
            enemies.setdefault(b, []).append(a)
        parts: list[str] = []
        said: set[frozenset[str]] = set()
        for nid, n in self.nations.items():
            foes = [e for e in sorted(enemies.get(nid, ())) if e in self.nations]
            pairs = [e for e in foes if frozenset((nid, e)) not in said]
            if not pairs:
                continue
            said.update(frozenset((nid, e)) for e in pairs)
            parts.append(f"{n.name} at war with {_and([self.nations[e].name for e in pairs])}")
        at_peace = [n.name for nid, n in self.nations.items() if nid not in enemies]
        if at_peace:
            parts.append(f"{_and(at_peace)} at peace with all")
        return "; ".join(parts) if parts else "every nation at peace"

    def sailed_with_words(self) -> str:
        """The table the ship sailed with, in words, dated as the file dates it."""
        as_of = getattr(self, "as_of", None)
        when = f" ({as_of.day} {as_of:%B %Y})" if as_of else ""
        return f"The nations as she sailed{when}: {self.table_words(self.sailed_with)}."

    def to_dict(self) -> dict[str, Any]:
        return {
            "wars": [
                {"between": list(w["between"]), "since": str(w.get("since") or "")}
                for w in self.wars
            ],
            "news": [list(n) for n in self.news],
        }


@functools.lru_cache(maxsize=2)
def _marines(path: str) -> dict[str, Any]:
    return yaml.safe_load(Path(path).read_text(encoding="utf-8")) or {}


def load_marines(path: str | Path = MARINES_PATH) -> dict[str, Any]:
    """The marines' kits and the small arms (`data/marines.yaml`; package 73)."""
    return _marines(str(path))


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
            habits=dict(d.get("habits") or {}),
            signals_root=str((d.get("signals") or {}).get("root") or "basic"),
            signals_system=str((d.get("signals") or {}).get("system") or "basic"),
            naval=dict(d.get("naval") or {}),
            marines=dict(d.get("marines") or {}),
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
        sailed_with=[dict(w) for w in wars],
    )


def _key(words: str) -> str:
    text = str(words).strip().lower().replace("_", "-").replace(" ", "-")
    return text.removeprefix("the-")


def _and(names: list[str]) -> str:
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]
