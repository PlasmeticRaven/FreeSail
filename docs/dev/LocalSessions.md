# Packages run in the owner's local sessions

Some packages are about the owner's machine (its paths, its launcher, its timings) and
are run there, in a Claude Code session opened on a clone of the repository, rather than
in the lead's cloud worktrees. The brief stays in `docs/dev/M5-WorkPackages.md`; the text
below is what the owner pastes to start the session. Each session works on its own
branch from the lead's branch and pushes it; the lead merges it with `--no-ff`, runs the
suite and records the package as any other.

The owner's part: open the repository folder in Claude Code (the Desktop app's Code
tab), choose the model (Opus for these two), paste the prompt, and when the session
reports, paste its report to the lead.

## Package 32c: the suite in two tiers, the days built once, a Windows job

```text
You are building package 32c of FreeSail on this machine (Windows; Python is `py`).
Read `docs/dev/M5-WorkPackages.md` whole, then your package's brief in it (32c), then
`docs/design/ColdReview-2026-09-30.md` §2.1 "The test suite has become an integration
suite" and §6 item 1, `docs/gates/README.md`, `.github/workflows/ci.yml` and
`release.yml`, and `pyproject.toml`. The working rules of the earlier milestones hold
(`docs/dev/M3-WorkPackages.md`'s head): stay inside your files, build what the brief
says at the size it says, every number names its source, deterministic, ship's-log
voice in anything a player reads, run the whole suite and read the summary line
yourself, report in the set order.

Git: `git fetch origin claude/dreamy-darwin-d77nty` and work on a new branch
`package/32c` from it; commit as you go with clear messages ending in the attribution
lines your session gives you; push the branch with `git push -u origin package/32c`
when done. Never touch `tests/test_known_truths.py`: another package is editing it. Do
not merge, do not push to any other branch, do not create a pull request.

Before you finish: `py -m ruff check .` and `py -m ruff format --check .` clean; the
fast tier alone (`py -m pytest -n auto`) and the whole suite (`py -m pytest -n auto
--slow`, or whatever flag you built) both green, and their wall clocks on this machine
measured before and after your change. Report in this order: the suite's last line for
each tier; the counts and wall clocks before and after; the tests marked slow and the
rule that marked them; the CI cost per push; anything not done and why.
```

## Package 32d: the `freesail` command, the settings file and the setup step

```text
You are building package 32d of FreeSail on this machine (Windows; Python is `py`).
Read `docs/dev/M5-WorkPackages.md` whole, then your package's brief in it (32d), then
`docs/TechnicalSpec-M4.md` §24 item 6, `docs/agents/Harness.md` whole (you do not edit
it), `docs/design/ColdReview-2026-09-30.md` §6 item 9, `.mcp.json`, `pyproject.toml`,
and the `main(argv)` functions of `freesail/ui/server.py`, `freesail/ui/console.py`,
`freesail/agents/local.py`, `freesail/agents/repl.py` and
`freesail/agents/mcp_server.py`, which your command wraps and does not change. The
working rules of the earlier milestones hold (`docs/dev/M3-WorkPackages.md`'s head):
stay inside your files, build what the brief says at the size it says, deterministic,
plain words in anything the owner reads, run the whole suite and read the summary line
yourself, report in the set order.

Git: `git fetch origin claude/dreamy-darwin-d77nty` and work on a new branch
`package/32d` from it; commit as you go with clear messages ending in the attribution
lines your session gives you; push the branch with `git push -u origin package/32d`
when done. Do not edit `docs/agents/Harness.md` (another package holds it; give the
lead the lines to add in your report). Do not write into the real Claude Desktop
configuration or the real settings until the owner says so in this session: build
against temporary paths first, show the owner what `freesail setup desktop` would
write, and run it for real only on their word. Do not merge, do not push to any other
branch, do not create a pull request.

Before you finish: `py -m ruff check .` and `py -m ruff format --check .` clean; `py -m
pytest -n auto` green; `freesail check` run on this machine and its output in the
report. Report in this order: the suite's last line; the commands as they ran here with
`freesail check`'s output; the configuration files as written with the model name
blanked; the lines for `Harness.md`; what could not be done on this machine and why.
```
