# Gate M4b: The harness and the watcher (first attempt)

**Verdict:** Not passed on this build (owner, 2026-09-27); re-cut as `gate-m4b-2` after package 28b.

Part A passed on the owner's run: the proofs, the scripted watcher, and the practice consent conversation at the REPL, which found two snags in the door's prompting (the blank line that sends a reply; the `>` before a tool call), fixed the same day. Part B was begun with a Sonnet 5 session through Claude Desktop: consent recorded (`docs/agents/consent/2026-09-27-sonnet-5.md`), the watcher narrated and answered an `ask`, an order was refused with its authority, and the opt-out tool ended the session with a save (`docs/playtests/2026-09-27-gate-4b-sonnet-watcher/`). The owner then found the door's shape unplayable: the World ran inside the MCP server, so the game could be seen only through the tool calls' readouts in the chat, and the captain's orders went through a prompt menu. That was the lead's error in spec M4 §13, not the package's. §13 was revised, package 28b made the doors clients of the running game, and the gate was re-cut as `gate-m4b-2` with its items played in the browser window.

The first attempt's checklist is the text of the `gate-m4b` release's notes, kept there as the record of what was tested; this file replaces it in the repository so that the re-cut's report is the one that opens from the folder.
