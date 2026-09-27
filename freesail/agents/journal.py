"""The agent's journal (spec M4 §11; `docs/agents/README.md` commitment 5): an audit
trail of its own, per station, saved with the game.

The `journal` tool appends a note; the harness appends its own entries (stood by, opted
out, stopped, nudged, paused) so that the exit report has a record behind it. The
journal is kept on the World by station name (`World.agent_journals`), apart from the
agent, so that a released station's journal is still shown by `show the watcher's
journal` and saved by `World.save()`. A save restores it on load, and a replay writes
it again from the recorded transcript, entry for entry (`tests/test_agents.py`).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from freesail import units

__all__ = ["Journal", "JournalEntry"]


@dataclass(frozen=True)
class JournalEntry:
    tick: int
    stamp: str  # the watch-and-bells stamp people read
    kind: str  # "note" for the tool's notes; else the harness's log kind, "agent.stood_by"
    text: str

    def line(self) -> str:
        who = "" if self.kind == "note" else f"({self.kind.removeprefix('agent.')}) "
        return f"{self.stamp}  {who}{self.text}"

    def to_dict(self) -> dict[str, Any]:
        return {"tick": self.tick, "stamp": self.stamp, "kind": self.kind, "text": self.text}


class Journal:
    def __init__(self, station: str):
        self.station = station
        self.entries: list[JournalEntry] = []

    def __len__(self) -> int:
        return len(self.entries)

    def append(self, world: Any, text: str, kind: str = "note") -> JournalEntry:
        text = " ".join(str(text).split())
        entry = JournalEntry(
            tick=world.clock.tick,
            stamp=units.time_stamp(world.clock.ship_time),
            kind=kind,
            text=text,
        )
        self.entries.append(entry)
        return entry

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
                JournalEntry(int(d["tick"]), str(d["stamp"]), str(d["kind"]), str(d["text"]))
            )
        return j
