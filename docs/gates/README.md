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
2. **A GitHub release**, created automatically when a tag named `gate-mN` is pushed. The release carries the gate report as its notes and a zip of everything needed to run it. Download the zip from the release page; there is no need to use git.
3. **The automated checks** (`pytest`, `ruff`) passing on GitHub's own machine for the tagged commit, visible under the repository's *Actions* tab. This is the programmer's half of the gate; it runs before the report is trusted.
4. **The owner's verdict**, recorded at the top of the gate report as *Pending*, *Passed*, or *Passed with notes*, with the notes. The next milestone does not start until the verdict is in.

## How to run a gate

1. Open the repository's *Releases* page and download the zip for `gate-mN`.
2. Extract it somewhere convenient, for example `D:\Projects\FreeSail-gates\gate-m0`.
3. Open the gate report (`docs/gates/gate-mN.md` inside the zip, or the release notes on GitHub, which are the same text).
4. Follow *Setup*, then work down the *Checklist*, ticking each item.
5. Report the result in the session: pass or fail per item, plus anything that felt wrong even if it passed.

## Why a zip and not git

Because the gate is meant to be runnable by anyone with a computer. The zip is exactly the tagged commit; if a fault is found, the tag says which code it was.

## Naming

Tags: `gate-m0`, `gate-m1`, ... Reports: `docs/gates/gate-m0.md`, ... A milestone that needs a second try gets `gate-m1-2`, with a second report explaining what changed.
