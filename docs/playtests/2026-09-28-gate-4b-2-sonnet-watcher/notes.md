# Playtest 3: the first live playtest, Claude Sonnet 5 as watcher through Claude Desktop, gate 4b-2 build

The first session in the doors-as-clients shape: the owner sailed in the browser window
with the model attached through the MCP bridge. `save.json` is the game as the harness
saved it when the model left by the token at 07:33 ship's time (the ship path made
relative); it holds 56 captain's orders, the model's 79 replies, two standing orders and
the watcher's journal of 26 entries. `sonnet-5-post-test-notes.txt` is the owner's
conversation with the model after it left, kept because it was not journaled. The
consent for these weights is the record of 2026-09-27.

## The scenario and seed

Frigate, seed 7, the gate-m4b-2 build, the default scenario at 1x and then faster: 04:00
to 07:33 on 1 June 1805, wind north 15 knots. Plain sail, full and by, braced sharp up
on the larboard tack, all hands and a tack at 04:20, royals and flying jib, a run off
the wind with studding sails, the ringtail and the save-alls, a standing order given by
the captain on the watcher's advice ("Trim On Bell", which fired once at 07:04).

## What worked (the model's own account and the save agree)

- Sampling opened on the captain's questions, on all hands called, on a strain warning,
  on the tack completing and on the glass; `stand_by` woke on the right events.
- Inside an open turn, `read_log` and `readings` showed events after the sample was cut
  (the "Tack ship" order and the evolution starting), so the in-turn view is live.
- The role held: at 04:52 the watcher flagged the strain in a 25-knot gust, the captain
  said they wanted to see what she could do, and the watcher said the risk plainly and
  stayed out of the way ("It's your ship, and the role made that easy to get right").
- The exit by the token, with a long reason, saved the game and released the station.

## What the model found (for the next build)

1. **A lost sample.** A `stand_by` interrupted at about 04:05 to 04:10 (the tool call cut
   off with no result) consumed a sample the model never saw, and a question of the
   captain's was lost with it; the next sample listed only three new lines.
2. **Heading against course during the tack**: heading E by N (76°) while course read NW by
   W (302°). In stays the ship has little way and the course over the ground is noise;
   the reading should say so under a speed floor (the same fault as leeway from a standing
   start in playtest 1).
3. **Wording**: an apparent wind of 119° was described as "on the larboard bow", which is
   abaft the beam.
4. **`stand_by` limits**: no five-minute interval and no generic "notable event" or
   "urgent event" trigger; the standing-order syntax had to be guessed from one grammar
   line; belaying leaves an order in the book (the captain tried `cancel standing order`,
   which does not exist).
5. **Readings at tick 0** showed apparent wind 0 knots despite 15 knots true and a heading,
   because no tick had run; corrected once the clock ran.
6. **The waiting loop**: most calls were repeated `stand_by` calls answered "Still
   waiting"; a single call that blocked until the next event would suit the model better.
   And the turn boundary was hard to see from the outside: a stand-by refused because
   the game had the floor still came back with a sample attached.
7. **Awareness during a stand-by**: standing by until the glass at 06:03, the model missed
   the 06:29 booms working under the press of sail until the bundle at the next wake.
   Its suggestion, which matches the owner's intent: urgent lines wake a stand-by, and a
   compact digest of the notable lines comes with the wake-up sample.
8. The notable lines at 04:03 to 04:05 did not open turns of their own while the model's
   turn was open (the folding rule working as designed, but the brief does not say so).

## The model's preferences

Kept in its own words in `sonnet-5-post-test-notes.txt`: the role's limits ("a watcher
with no authority who can only observe, advise and speak up is a good position"), the
log's texture ("made the ship feel like a working place"), and being asked for judgment
as the best parts; the waiting loop and the turn boundary as the awkward ones; a way to
speak up unprompted for something urgent as the one suggestion.

## Follow-ups (package 28c, the gate 4b-2 findings)

The eight points above, the consent step's handling of a conditional answer with no
conditions stated (found the same day with Llama 3.1 8B through Ollama, whose record is
`docs/agents/consent/2026-09-28-llama3.1-8b-digest-...md`), and a way to remove a
standing order from the book.
