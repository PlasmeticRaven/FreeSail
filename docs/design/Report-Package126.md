# Report: package 126, part one: the harbour and the weather

**The brief.** `docs/dev/briefs/Brief-Package126.md`: four parts, three of them the owner's notes
2, 3 and 4 from his play of gate M7 (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`), the
fourth item 12 of section 4 of `docs/dev/CarriedForward-M7.md`, with item 6 of the same list beside
the first. The branch is `claude/pkg-126`, cut from the trunk at 112ff819.

**Part one** (the lead's split of 2026-11-27) holds the first two: the harbour's end of a game, with
the stations' table, and the fog. The captain's spar work (the owner's note 4) and the `lie a-try`
mend (item 12) are taken out whole and held for a later pass on the trunk as it then stands:
`freesail/world/captains.py` and `freesail/evolutions/runner.py` are the trunk's, byte for byte,
and their truths, figures and sections are gone from this hash. New truths here are 7-770 to
7-775 (with 7-775 b).

## 1. A game ended from the harbour (the owner's note 2), and the stations' table

**As it was.** `Harbour.start` (`freesail/ui/harbour.py`) takes a new World up in place of the old
through the driver's `replace_world`; nothing ended a game. The stations' table of the page
(`client/harbour.js`, `fillStations`) kept each row's choice of door and model by the row's key
(`station|ship`) whenever it was drawn again, so a game begun after another was offered the last
game's choices.

**As built.**

- `Harbour.end(lose_unsaved)` and `POST /api/harbour/end`. Every door the harbour started that is
  still running is closed by `stop_door`, as the harbour closes one: its own Ctrl-C, the station
  released at the game as before. The whole of the end holds the harbour's lock, so that no start,
  no other end and no door begun from another page comes between the asking and the end; the
  driver's lock is not held while the doors stop, because a stopping door asks the game to release
  its station. Then, under the driver's lock as well (the start's order: the harbour's first, then
  the driver's), the World is let go for one with no game in it, as `py -m freesail` begins, and
  any door begun from a page while the doors stopped is stopped too:
  the driver's `replace_world` stops the clock, stops hearing the old log and tells the pages to
  start again. The harbour's words of the game are emptied, `started` is false and the director's
  seats' doors are forgotten. Nothing saved is touched. The game page's `/` leads to the harbour
  again, as it does before any game, and another game is begun from the same server.
- **What is not saved is lost only on the player's word.** The driver keeps what of the game a
  save holds (`Driver.kept`: the World, its tick and its log's length after the last save's line,
  or as it was taken up, and the ship's time and day of that save). A save written to the saves
  place and a save handed down by `GET /api/save` (the download) are kept alike
  (`Driver._mark_kept`, `Driver.downloaded`). `Driver.unsaved()` gives the words
  when anything has passed since. While it does, the end is refused with them ("This game has not
  been saved; what has passed in it, to <time and day>, is lost if it is ended. End it all the same, or
  save it first.", or "This game was last saved at <time>; ..."). The page then shows "end it,
  losing what is not saved", and only that sends `lose_unsaved`. A game taken up and not played,
  or saved and not played since, ends at once.
- **The page.** "end the game" sits under the game in play, at the head of every tab (the "In
  play" panel), shown while a game is in play. Its words go under it.
- **The stations' table** keeps a row's choice only while it is drawn again for the same game. The
  state carries `games`, the count of games begun and ended from this harbour, and a game begun
  after another draws its rows as its own scenario gives them. A seat asked at the desk in the game that ended is listed by nobody after it
  (the desk lists the stations of the World in play).

**The ship's time in these words** is the log's stamp with its day after it, as "Morning watch
(05:02), 5 June 1805" (`server.dated_stamp`): the stamp alone gave no day, and a game played over
days could not be told from its words.

**As a player reads it.** The page, under the game in play: the button "end the game". With
nothing unsaved, under it: "The game is ended.", and the page's head says "no game yet". With play
since the last save, under it in the refusal's colour: "This game has not been saved; what has passed
in it, to <the ship's time now>, is lost if it is ended. End it all the same, or save it first." Or,
after a save: "This game was last saved at <its time>; what has passed since, to <now>, is lost if it
is ended. End it all the same, or save it first." Beside it is the button "end it, losing what is not
saved".

**A model's door closed by the end is said in the ended game's log before the world is let go.** The
door's own Ctrl-C stands its station down, and the game's last line is the stand-down: "The watcher
stood down by the API door: ... The station is released and may be taken again. The game is saved."
(truth 7-773 holds it the log's last line). The model's side is told by its door, as at any stop, and
the station's record is saved as at any stand-down. That save is a new file of the saves place, not a
save the player made.

**Truths.** 7-770 (the end, the refusal and its words, a save untouched, a game begun after,
`tests/test_harbour.py`); 7-771 (a page that asks at every line of the end finds the whole game or
none, never the one beside the other; the start's probe, applied to the end); 7-772 (in the
browser, by the page's road: the planned door and a door chosen by hand, a next game offered its own
stations, the end refused on its words and taken at "end it, losing what is not saved", a game begun
after offered its own; a game saved by the download ended without asking, and played on after it
asked with the download's time and day); 7-773 (a live server: the API door seated at the watcher's station is closed
by the end, its station released).

## 2. Fog comes on and clears over a time, and is said as it does (the owner's note 3)

**As it was.** `Weather.coastal_fog` (`freesail/world/weather.py`) drew fog once a sky block by the
month's chance, near the coast, in a stable warm sector or under a high, under a slack wind; and
`conditions_at` put the sky "thick", the weather "fog" and the sight "a cable" for the whole block,
from the horizon at one minute to a cable at the next ("Fog came down.") and back ("The fog
lifted.").

**As built.** `Weather.fog_degree` gives how thick the fog is, 0 to 1. The degree rises over
`FOG_SETTLE_S` (half an hour) from the edge of a block that draws fog after one that did not. It
falls over `FOG_CLEAR_S` (an hour) to the edge of a block that draws it before one that does not.
It thins within `FOG_WIND_THIN_KN` (three knots) under the wind that lifts it, and within
`FOG_COAST_THIN_KM` (five km) of its reach from the coast. All four are JUDGEMENT, their ground
written where they are defined. Which blocks draw fog is unchanged (the same seeded draw), so every
fog of the old weather is a fog of the new, beginning and ending at the same edges. `fog_sight` gives
the sky and the sight in it, through the steps the weather already has: one step thicker than the sky
gives as it first settles, the steps between in turn, and a cable at its full. The sky is "hazy"
while the sight is a few miles and "thick" at a mile or less. `Conditions` carries the degree
(`fog`, a class default of 0 for a pinned sky and for a checkpoint written before).
`coastal_fog` is now `fog_degree > 0`.

**The lines** (`World._tick_weather`, `weather.FOG_LINES`), with their severities as the lead
ruled them:

| Line | When | Severity |
|---|---|---|
| "A fog is settling in." | the weather's change to fog ("Fog came down." stays for a fog that comes on at its full) | notable |
| "The fog is thickening." | the sight closes a step short of a cable | routine |
| "The fog has shut in thick." | the sight shuts in to a cable | notable |
| "The fog seems to be clearing." | the sight first opens from a cable | notable |
| "The fog is thinning." | the sight opens a step more | routine |
| "The fog lifted." | the weather's change from fog, as before | routine |

**One fog, first to last.** Every fog now passes each step coming and going (§4 below): six
lines, three of them notable. Before, there were two, one notable. A compressed clock is eased
only by an urgent line (`Driver._on_event`), so a compressed passage runs on through a fog as
before. The three notable lines are shown singly in the roll-up where routine ones are
rolled up. A seated model whose policy samples on notable (the watcher's default, "every glass and
on notable and urgent events") is sampled three times in a fog where it was sampled once, and under
the pace rule the clock is at 1x while each sample is open.

**A game saved by another build and taken up by replay** (not its checkpoint) is played again under
this build's weather. Its fogs come on and go by degrees with these lines, and what was ordered in
them is replayed as ordered; nothing compares its log with the save's. The
steps are a new kind, `weather.fog`. The change of weather keeps its kind, `weather.change`, which the
officer's and the captain's wakes read.

**Deterministic and the same after a save.** The degree is a function of the seed, the point and
the moment alone, as the sky's noise is. Nothing is kept, so a checkpoint and a replay see the same
fog, and the World keeps no new state. Truth 7-775 saves a game in the settling, takes it up from its
checkpoint, and runs both minute by minute to the same sights and lines.

**Everything that reads the sight follows, by one road.** They all read `world.conditions`, set once
a minute from `conditions_at`: the lookout (`world/lookout.py`, the sightings, the shore's limit by
the weather, land ahead, the casks by `combat/marks.py`); the far ships' lines and who is in sight
(`world/ships.py` 2113 and 2321, `world/crews.py`); the signals' book by day, night or fog
(`world/signals.py` 899: the fog book under a mile, so it is taken up as the sight closes to a mile
and left as it opens past one); the lights' range (`world/chart.py`); the action's and the
dealings' reach (`combat/action.py`, `world/dealings.py`); the captain's and the far captains'
"thick near the land" (`world/captains.py` 2196, `world/brains.py` 102 and 666, at a mile or a
cable); a model's readings, the visibility in words and miles (`api/readings.py` 587 and 4790, as
served to a seat); and the director's weather order and its doubt (`world/orders.py`, `_weather`
appends systems whose fog is the same function; the doubt of a ship put within the horizon "in
clear daylight" reads the same conditions at 4843). No reader was changed. Truth 7-774 reads the
conditions, the reading served and the lookout's limit at every minute of a fog's coming and going.

## 3. The harbour's second pass (the lead's list of 2026-11-24, C, D and F) and the end's mends of 2026-11-27

**The end's words.**

- **The stand-downs' saves are named by the seats' own record of them** (`Seat.saves`), not by the
  saves place's names, which a save of the same name would hide.
- A game taken up from a save and played on is told since when: "This game was taken up from its save
  at <the save's time> and has not been saved since; what has passed since, to <now>, is lost if it
  is ended. End it all the same, or save it first." (`Driver.taken_up_from_a_save`, called by the
  harbour's start of a save.)
- **A model's door seated:** the stand-down's save is said before and named after. The refusal adds
  "The models' stations are stood down first, and each stand-down saves the game as it stands then,
  among your saves." The end's lines add "The models' stations were stood down, and the game as it
  stood then was saved as <its name>, among your saves." The save is kept, as at any stand-down (the
  record of a station's last word is the game as it stood), and is told apart by being named. Truth
  7-773 holds both, and that the one save named is the one file the stand-down wrote.

- **An order given with the clock held** is play not saved: truth 7-770 gives `set plain sail` at
  tick 0, and the end asks.
- **A save by the download keeps the game** (2026-11-27): `GET /api/save` marks it kept as the
  desk's save does, so the end asks nothing after it, and played on after it the words say "This
  game was last saved at <the download's time and day>". Before, a game saved that way was still
  warned as unsaved.
- **The end's words give the day** (2026-11-27), as §1 says.

**What a seat or a player is served from the files this package touches.** The primer's chapter
1 (`docs/primer/01-the-ship.md`) gained one sentence on ending a game: "A game in play is ended from
the harbour by *end the game*, under the game at the head of every tab; what has not been saved is
lost only when you say so a second time." The primer is served to every seat (its 57 entries of
what a seat reads, on every ship). The README is the player's, and gained one sentence in its
harbour paragraph: "The game in play is ended from the harbour by *end the game* under it, the harbour
kept: if anything has passed since it was last saved, the harbour says so and ends it only when you
say so again." No other file the diff touches is served to a seat or a player beyond those §5 lists:
the harbour's page and its sentences (`client/harbour.html`, `harbour.js`), and the game's lines and
readings in a fog.

## 4. The fog's second pass

**The fog, made to come and go by degrees throughout** (the lead's list of 2026-11-24, B).

1. **No jump of two steps.** The sight is stepped from the horizon in every fog (`fog_sight`): a few
   miles as it first settles, a mile at its half, a cable at its full. It is never clearer than the
   sky gives, so each step is passed coming and going whatever the fog's block's sky. Truth 7-775 b
   scans a June of minutes off Falmouth: no change of sight in or out of fog moves two steps.
2. **The air it lies in comes and goes by degrees too** (`Weather._fog_air`):
   - **In time, at the place:** read minute by minute, the fog settles over `FOG_SETTLE_S` from the
     moment the place came under a warm sector or a high, and thins over `FOG_CLEAR_S` to the moment
     it will leave it.
   - **In space:** it thins within `FOG_AIR_EDGE_KM` (5 km, JUDGEMENT, as its reach from the coast
     thins) of the edge of that air, read a kilometre at a time about her, so that a ship sailing
     across the edge has it come and go by degrees.
   - **Into other weather:** a fog that gives way to it is said to lift ("The fog lifted. Passing
     showers.").

   Truth 7-775 b: where the air is to go in half an hour the fog is half cleared, a minute before
   only just there, and gone at the moment; where it came a quarter of an hour ago, half settled;
   six km inside the edge thick, 3.5 and 1.5 km thinner by turns, gone at 0.3; the line of its
   lifting into showers.
3. **No flicker said, and nothing lost.** A step of the fog's sight is put off within
   `FOG_LINE_QUIET_S` (600 s, JUDGEMENT: a third of the settling; a watch officer says the fog's turn
   when it has held) of a step the other way, or of the same words. It is said when the quiet is
   over if the sight is not back where the log left it (`World._say_the_fog`, from the sight the log
   last said). The sight itself is read as it is. The mark is the World's (`_fog_said`: the tick,
   the way, the words and the sight said), kept by its checkpoint; truth 7-775 saves with a quiet in
   force and the loaded game holds it. Truth 7-775 b feeds the sight a mile, a few miles, a mile, a
   few miles, a mile, a minute apart: "The fog is thinning." once; then the sight holding at a mile,
   "The fog is thickening." when the quiet is over.
4. **The times pinned as figures.** Truth 7-774 holds them in seconds, not by the constants: the
   settling 1,800 s from its first line to a cable (±120) and a mile at 900; the clearing 3,600 s from
   its first opening to the fog lifted (±120) and a few miles at 1,800. Truth 7-775 b holds the edges
   at the function: thick under 9 knots, half at 10.5, gone at 12.5; thick 20 km from the coast,
   half at 27.5, gone at 31.
5. **Another build's save taken up in a fog** (by its checkpoint) reads the fog this build has at
   that moment. Its first step from the sight the save held is said as this build's steps go, and
   may run the other way to the save's last line. The lead's case is "The fog seems to be clearing."
   at once, and "The fog has shut in thick." sixteen minutes later. Nothing is owed for it.

6. **A fog shut in thick may be said clearing ten minutes later.** The quiet puts off a step the
   other way within `FOG_LINE_QUIET_S` of the last line; at the quiet's boundary, where the sight
   has opened again from a cable and held, "The fog seems to be clearing." follows "The fog has
   shut in thick." by ten minutes. That is as designed: the line says the sight as it stands once
   the quiet is over, and a fog that shuts in and opens again in a quarter of an hour is said so.

## 5. The pins moved, and the differences served

**No pin moved** (`docs/dev/TuningNotes.md`, "Package 126, part one"). The comparison of today's
ships against the trunk on this hash is being run; its table follows here before the report.

## 6. Found and not mended

- **A stand-down's save is named** `freesail-seed<seed>-tick<tick>.json` by the desk, and overwrites
  a save of that name: two stand-downs at one tick write one file, and an earlier file of the same
  name is lost. The naming is the desk's and older than this package; the end now names what the
  seats record they wrote.

## 7. Held for a later pass

The captain's spar work (clearing a wreck, shifting a spar for a spare, a jury mast, bending and
setting again) and the `lie a-try` mend for a ship with no topsail to lie under, with their truths,
figures and report, are kept on a branch of the builder's own (the second pass's hash 1f0cfa9, in
this branch's history) for the third pass the lead has listed, on the trunk as it then stands.
