# Milestone gates

No milestone is finished until the owner has checked it live and said so. This folder holds one **gate report** per milestone, written for a reader who is not a programmer.

## What a gate is

A gate has four parts:

1. **A gate report** in this folder, `gate-mN.md`, with:
   - a headline: what the milestone claims to do, in a few sentences;
   - what you need and how to set up, step by step, with what you should see after each step;
   - a **checklist** of things to verify live, each with the exact thing to type and the exact thing to look for;
   - a short **guide** to any technical idea the checklist relies on that is not self-explanatory (what a seed is, what a digest is, and so on);
   - what is deliberately *not* in this milestone, so it is not reported as a fault;
   - what to report back.
2. **A GitHub release**, created automatically by the `gate release` workflow when a branch named `gates/mN` is created at the gate commit (or when someone presses *Run workflow* on that workflow in the *Actions* tab and types the gate name). The workflow tags the commit `gate-mN` and publishes a release carrying the gate report as its notes and a zip of everything needed to run it. Download the zip from the release page; there is no need to use git.
3. **The automated checks** (`pytest`, `ruff`) passing on GitHub's own machine for the tagged commit, visible under the repository's *Actions* tab. This is the programmer's half of the gate; it runs before the report is trusted. The gate release runs the whole suite, both tiers (see *The two tiers of tests* below); an ordinary push runs only the fast tier, on Linux and on Windows.
4. **The owner's verdict**, recorded at the top of the gate report as *Pending*, *Passed*, or *Passed with notes*, with the notes. The next milestone does not start until the verdict is in.

## How to run a gate

1. Open the repository's *Releases* page and download the zip for `gate-mN`.
2. Extract it somewhere convenient, for example `D:\Projects\FreeSail-gates\gate-m0`.
3. Open the gate report (`docs/gates/gate-mN.md` inside the zip, or the release notes on GitHub, which are the same text).
4. Follow *Setup*, then work down the *Checklist*, ticking each item.
5. Report the result in the session: pass or fail per item, plus anything that felt wrong even if it passed.

## The two tiers of tests

The test suite is in two tiers. The **fast tier** is everything but the tests that sail a whole day or replay one, and the few truths that run long; the **slow tier** is those (they are marked `slow` in `tests/conftest.py`, which says how they were chosen).

- `py -m pytest -n auto` runs the fast tier on all the machine's cores, in a few minutes (`python -m pytest` on Linux or a Mac, as in the commands below). Its last line says how many slow tests it left out.
- `py -m pytest -n auto --slow` runs the whole suite, both tiers. This is what the gate release runs, and what a package runs before it is finished.
- `py -m pytest -n auto -m slow` runs the slow tier alone, and a test named by `-k` or by its node id (`file.py::test_name`) runs whichever tier it is in.

Every push of code runs the fast tier on GitHub's machines, on Linux and on Windows. The days the slow tests sail are each built once a run, on one core (`--dist loadgroup`, set in `pyproject.toml`), however many cores there are.

## Why a zip and not git

Because the gate is meant to be runnable by anyone with a computer. The zip is exactly the tagged commit; if a fault is found, the tag says which code it was.

## Naming

Reports: `docs/gates/gate-m0.md`, `gate-m1.md`, ... Snapshot branches: `gates/m0`, `gates/m1`, ... Release tags, made by the workflow: `gate-m0`, `gate-m1`, ... A milestone that needs a second try gets `m1-2`, with a second report explaining what changed.

## If the release does not appear

The snapshot branch is itself a complete download: on GitHub, open the branch `gates/mN`, press the green *Code* button and choose *Download ZIP*. It is the same project the release would have packaged.
