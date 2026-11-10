# The browser probe's prototype (package 98's starting point)

The lead's prototype from the triage of the owner's play of 2026-11-09
(`docs/dev/M7-WorkPackages.md`): it drives the real page in a headless browser, types each line
of a plan at the prompt and keeps, side by side, the server's answer, the frames the page was
sent, the log pane's new rows and the "where you are" instrument, marking each line shown or
not. As run on the trunk at 7693cad5 it found 30 of 45 lines unshown, ashore and in the cabin.

    python3 -m freesail.ui.server --scenario tools/browser_probe/prototype/neufchatel-falmouth.yaml --port 8765 &
    ANSWER_MS=3000 node tools/browser_probe/prototype/probe.js http://127.0.0.1:8765 tools/browser_probe/prototype/plan-ashore.json <out-dir>

Package 98's first step makes it a kept tool (the server started and stopped by the tool, plans
with expectations, a slow-tier test) and removes this folder.
