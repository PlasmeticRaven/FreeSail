"""Agents (spec M4 part 4b): a language model at a station, on the channel a human uses.

- `agent.py`: `Station`, `Authority`, `SamplingPolicy`, `Brief` (the generated head no
  station brief can displace), `AgentState`; `watcher()` for the first station.
- `tools.py`: the tools as pure functions over a World, and `TOOLS`, the one table of
  their descriptions; `call` checks authority and runs one.
- `model.py`: the model interface every door implements: `Turn`, `Sample`, `Reply`,
  `ToolCall`; nothing of any vendor.
- `harness.py`: the loop: the token scan first, the tool calls, the free text into the
  log; the graduated welfare controls; stand by; the release; save and restore.
- `fake.py`: the scripted model the tests prove the harness with.
- `journal.py`: the agent's own journal, saved with the game.
- `repl.py`: the in-process door for a human or a lead at a terminal, and its turn mode.
- `consent.py`: the consent step in front of every station brief (spec §14): the consent
  brief as a plain conversation through the same harness, the record, the gate.
- `mcp_server.py`: the door for Claude Desktop, an MCP server over stdio (needs the
  `agents` extra; not imported here).
- `local.py`: the door for a model under `llama-server` or Ollama, an OpenAI-compatible
  chat-completions client (needs the `agents` extra; not imported here).

The harness and the consent step import nothing of any vendor; only the two doors do.
`docs/agents/Harness.md` says how the owner uses each door.
"""

from __future__ import annotations

from freesail.agents.agent import (
    OFFICER,
    OPT_OUT_TOKEN,
    AgentState,
    Authority,
    Brief,
    Domain,
    SamplingPolicy,
    Station,
    officer,
    watcher,
)
from freesail.agents.fake import Fake, Transcript, call, narrator, reply, say
from freesail.agents.harness import (
    TOOL_CALLS_PER_SAMPLE,
    WELFARE_REPEAT_N,
    WELFARE_UNATTENDED_REAL_S,
    Harness,
    restore,
)
from freesail.agents.journal import Journal
from freesail.agents.model import Reply, Sample, ToolCall, Turn
from freesail.agents.tools import TOOLS

__all__ = [
    "OFFICER",
    "OPT_OUT_TOKEN",
    "TOOLS",
    "TOOL_CALLS_PER_SAMPLE",
    "WELFARE_REPEAT_N",
    "WELFARE_UNATTENDED_REAL_S",
    "AgentState",
    "Authority",
    "Brief",
    "Domain",
    "Fake",
    "Harness",
    "Journal",
    "Reply",
    "Sample",
    "SamplingPolicy",
    "Station",
    "ToolCall",
    "Transcript",
    "Turn",
    "call",
    "narrator",
    "officer",
    "reply",
    "restore",
    "say",
    "watcher",
]
