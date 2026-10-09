"""The agent's journal (spec M4 §11; `docs/agents/README.md` commitment 5): an audit
trail of its own, per station, saved with the game.

The `journal` tool appends a note; the harness appends its own entries (stood by, opted
out, stopped, nudged, paused) so that the exit report has a record behind it. The
journal is kept on the World by station name (`World.agent_journals`), apart from the
agent, so that a released station's journal is still shown by `show the watcher's
journal` and saved by `World.save()`. A save restores it on load, and a replay writes
it again from the recorded transcript, entry for entry (`tests/test_agents.py`).

**Read back, and whose** (package 37g, item 15). The journal is the station's record: the
model at the station reads it back with the `read_journal` tool (`select`: newest first,
by count or since a tick, and by kind, its own notes apart from the harness's lines),
and a model that later takes the same station reads what the holder before it wrote
there. So each entry says whose it is (`by`, the identity at the station when it was
written; "" for the game's own scripted station and for an entry from before this
package, which a save simply leaves out).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from freesail import units

__all__ = [
    "HANDOVER_KIND",
    "OWN_KINDS",
    "WORD_KEPT_KIND",
    "WORD_PASSED_KIND",
    "Journal",
    "JournalEntry",
]

# The kinds of entry that are the model's own words: the journal tool's notes, and the
# handover and stand-down notes (the harness's lines are every other kind).
HANDOVER_KIND = "agent.handover"
OWN_KINDS: tuple[str, ...] = ("note", HANDOVER_KIND)
# The captain's word to a station nobody holds (package 37l; the review of gate 5c's
# playtests, G17: "a `tell` to an unmanned station is rejected and its words are lost"):
# kept in the station's journal, and passed to whoever takes the station next, in its
# first sample, with a line that says they were passed.
WORD_KEPT_KIND = "agent.word_kept"
WORD_PASSED_KIND = "agent.word_passed"


@dataclass(frozen=True)
class JournalEntry:
    tick: int
    stamp: str  # the watch-and-bells stamp people read
    kind: str  # "note" for the tool's notes; else the harness's log kind, "agent.stood_by"
    text: str
    by: str = ""  # whose entry it is: the identity at the station then (package 37g)

    @property
    def own(self) -> bool:
        """The model's own words (a note, a handover or a stand-down note), as apart from
        the harness's lines about it."""
        return self.kind in OWN_KINDS

    def line(self) -> str:
        who = "" if self.kind == "note" else f"({self.kind.removeprefix('agent.')}) "
        return f"{self.stamp}  {who}{self.text}"

    def to_dict(self) -> dict[str, Any]:
        d = {"tick": self.tick, "stamp": self.stamp, "kind": self.kind, "text": self.text}
        if self.by:
            d["by"] = self.by
        return d


class Journal:
    def __init__(self, station: str):
        self.station = station
        self.entries: list[JournalEntry] = []

    def __len__(self) -> int:
        return len(self.entries)

    def append(self, world: Any, text: str, kind: str = "note", by: str = "") -> JournalEntry:
        text = " ".join(str(text).split())
        entry = JournalEntry(
            tick=world.clock.tick,
            stamp=units.time_stamp(world.clock.ship_time),
            kind=kind,
            text=text,
            by=by,
        )
        self.entries.append(entry)
        return entry

    def last_note(self) -> JournalEntry | None:
        """The last handover or stand-down note written at the station, by whoever held
        it (package 37g: every brief for a station taken again carries it whole)."""
        return next((e for e in reversed(self.entries) if e.kind == HANDOVER_KIND), None)

    def kept_words(self) -> list[str]:
        """The captain's words kept for the station since they were last passed to it
        (`WORD_KEPT_KIND`), oldest first; [] when there are none."""
        last = max(
            (i for i, e in enumerate(self.entries) if e.kind == WORD_PASSED_KIND), default=-1
        )
        return [e.text for e in self.entries[last + 1 :] if e.kind == WORD_KEPT_KIND]

    def size_words(self) -> str:
        """One line of the journal's size: '41 entries, the latest at Middle watch, 4 bells
        (02:00)'; '' when it is empty."""
        n = len(self.entries)
        if not n:
            return ""
        return f"{n} {'entry' if n == 1 else 'entries'}, the latest at {self.entries[-1].stamp}"

    def select(
        self, count: int | None = None, since_tick: int | None = None, kind: str = ""
    ) -> tuple[list[JournalEntry], int]:
        """The entries to read back, newest first: those of `kind` ('notes': the model's
        own words; 'harness': the harness's lines; '' or 'all': every entry; else a kind
        by its name, with or without 'agent.'), from `since_tick` on when one is given,
        the newest `count` of them. Returns them and how many older ones were left out."""
        key = " ".join(str(kind or "").lower().split())
        found = list(self.entries)
        if key in ("notes", "note", "my notes", "own", "mine"):
            found = [e for e in found if e.own]
        elif key in ("harness", "the harness", "lines"):
            found = [e for e in found if not e.own]
        elif key not in ("", "all", "every", "everything"):
            found = [e for e in found if e.kind in (key, f"agent.{key}")]
        if since_tick is not None:
            found = [e for e in found if e.tick >= int(since_tick)]
        left_out = 0
        if count is not None and count >= 0 and len(found) > count:
            left_out = len(found) - count
            found = found[len(found) - count :] if count else []
        return list(reversed(found)), left_out

    def lines(self) -> list[str]:
        """For `show the <station>'s journal`."""
        if not self.entries:
            return [f"The {self.station}'s journal is empty."]
        n = len(self.entries)
        head = f"The {self.station}'s journal ({n} {'entry' if n == 1 else 'entries'}):"
        return [head, *(f"  {e.line()}" for e in self.entries)]

    def save(self) -> list[dict[str, Any]]:
        return [e.to_dict() for e in self.entries]

    @classmethod
    def load(cls, station: str, saved: list[dict[str, Any]]) -> Journal:
        j = cls(station)
        for d in saved:
            j.entries.append(
                JournalEntry(
                    int(d["tick"]),
                    str(d["stamp"]),
                    str(d["kind"]),
                    str(d["text"]),
                    str(d.get("by") or ""),
                )
            )
        return j
