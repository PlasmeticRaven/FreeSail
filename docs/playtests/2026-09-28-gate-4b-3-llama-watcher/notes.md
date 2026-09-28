# Playtest 5: Llama 3.1 8B as watcher through Ollama and the local runner, gate 4b-3 build

A short run (167 ticks of ship's time) to see whether an 8-billion-parameter model can
hold the watcher's station on the third build. `save.json` is the game as the owner's
`stand down the watcher` saved it. The owner stopped the run early on seeing the brief
parroted in the log, taking it for a model that could not cope; the transcript shows it
was still working through the request between those lines, slowly and with errors. The
owner's verdict, softened on that reading: too small to handle the station comfortably;
**no design change is to be made from this record** (owner, 2026-09-28).

## What the build did

Everything the third build claims of the harness held: one `stand_by` per turn, the
captain's questions answered, the wake-ups clean, the shelf's sizes served, no runaway
request, and the stand-down saved the game with its reason.

## What the model did

- **Confused the tools' shapes.** Its second call was `readings` with the whole readings
  block it had just been shown passed back as arguments; every `journal` call used `text`
  where the tool takes `note`, so all six were refused and its journal holds only the
  stand-bys; a `shelve book 6` with no book open.
- **Parroted the brief as its own words.** Six free-text replies were the station brief
  itself ("You are the watcher. You observe what the captain observes ..."), which the
  log shows under `[watcher]`.
- **Never really read.** Asked to pick something from the library, journal about it and
  shelve it, it called `contents` four times and journaled about the listing ("42
  evolutions, about 500 tokens each") before opening the catalogue and the ship's names
  at the very end; it treated the listing as the book.
- **Could not hold a three-step intent** (read, journal, shelve) across a turn.

## An observation for the viewer (not a change to this build)

From the browser the owner could see only the model's words, which were nonsense, while
its work (reading the contents, trying to journal, opening the catalogue) was invisible;
the Stations row says "turn open" and no more. A captain should be able to see that the
watcher is at the bookshelf or writing in its journal without reading the calls: the
station's last act in the Stations row, or a routine log line when a book is opened.

## What it means

The watcher's station needs a model that can carry a tool schema and a two-step intent;
this model in this quant is below that floor. Evidence for the baseline (spec M4 open
item 10), not a defect of the build. Gemma4 26B is the real test on this build.
