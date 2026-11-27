# Report: package 126: the harbour, the weather and the captain

**The brief.** `docs/dev/briefs/Brief-Package126.md`: four parts, three of them the owner's notes
2, 3 and 4 from his play of gate M7 (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`), the
fourth item 12 of section 4 of `docs/dev/CarriedForward-M7.md`, with item 6 of the same list beside
the first. The branch is `claude/pkg-126`, cut from the trunk at 112ff819.

**Part one** (the lead's split of 2026-11-27), the harbour's end of a game with the stations' table
and the fog, **was merged at 7bc7de20** by the hash afb5a998; sections 1 to 6 are its record, as
merged. **Part two** is this hash: the captain's spar work (the owner's note 4) and the `lie a-try`
mend (item 12), a fourth pass on the trunk as it stands, by the lead's lists of 2026-11-27 (part
two, items 1 to 3; the reader's third read, items 1 to 5), his ruling of the same day on the
wreck's windage and his ruling of the afternoon on the ship that will not lie to and on the
passage rule; sections 7 to 13. Its truths are 7-776 to 7-779 (with 7-777 b to g, 7-778 b and
7-779 b).

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

**No pin moved** (`docs/dev/TuningNotes.md`, "Package 126, part one").

**Today's ships, old beside new** (this hash's code beside the trunk at f2821c7b, package 127's
words and waits merged; measured again on it, the figures the same as beside the trunk before it
at 64fcc565). The same orders at seed 7 under the game's own captain:

- every ship file (the thirteen ships and the five boats);
- four cases: a gale abeam and a gale close-hauled (bound for Falmouth from 48 40 N 5 05 W, the
  wind rising from 20 to 35 knots over an hour and held two and a half more), a cruise off the
  Lizard (12 knots pinned, three hours), and a June passage off Falmouth under a high with the
  systems' weather (six hours);
- in every run, the whole log and the ship's end state compared.

| Case | Same in every line and the end state | Differs |
|---|---|---|
| gale abeam | 18 of 18 | none |
| gale close-hauled | 18 of 18 | none |
| cruise | 18 of 18 | none |
| June off Falmouth | none of 18 | the fog's coming and going (§2, §4), on every file |

Every case with no fog in it is the trunk's, line for line. In the June fog runs:

- **The five boats** differ in the weather's lines, and in what hangs on their minutes; they end
  within 11 m of the trunk's.
- **The 74, the 64, the razee, the frigate and the brig** end where the trunk's do, their logs
  differing by the fog's lines and the soundings, bearings and fixes taken in it.
- **The others under way** differ in the fog's lines and in what hangs on its minutes: the captain's
  fog signals and their ceasing, the courses shaped and the tide's allowance at the next minute,
  the log hove, the trims. They end 0.5 to 6.3 cables from the trunk's (the cutter the most).

***The first action*, left to the game's own captains** (four hours from its start at seed 7, no
seat): **the same**, line for line (633 lines in the Sherbourne's log on both; 629 before package
127).

**What a player or a model's seat is served that differs** (every such line, by kind):

- **The fog's lines** (§2): `weather.change` "A fog is settling in." and `weather.fog` "The fog is
  thickening.", "The fog has shut in thick.", "The fog seems to be clearing." and "The fog is
  thinning."
- **The weather's words through a fog:** the sky's ("The sky hazy.", "The sky thick.") and the
  hour's ("Hazy, fog; ..."), and the reading of the visibility ("a few miles", "a mile").
- **What follows those minutes:** the lookout's sightings, the signals' book of fog under a mile,
  and the captain's orders that hang on them.
- **Package 127's wait lines where that work queues** (`evolution.waiting`, routine): in a fog the
  captain heaves the lead and trims at other minutes, so its waits fall at other minutes too, as
  "'Heave the lead' will follow the same work, which the hands are still ..." (each boat, three
  more in the six hours) and "Not hands enough on deck to trim the jib; the watch is bracing the
  ..." (the cutter, twelve more). They are 127's lines as it says them; the fog only moves the
  work they wait behind. No test counts them in a fog, and the recorded passages' digests hold
  as the trunk records them (the fast tier).
- **The fog's lifting into other weather:** "The fog lifted. <the weather's line>".
- **The harbour's page and state:** the end's button and words (with the ship's time and its day),
  and `games` in the state.
- **The primer's chapter 1 and the README:** one sentence each on ending a game (§3).

Nothing else moved.

## 6. Found and not mended

- **A stand-down's save is named** `freesail-seed<seed>-tick<tick>.json` by the desk, and overwrites
  a save of that name: two stand-downs at one tick write one file, and an earlier file of the same
  name is lost. The naming is the desk's and older than this package; the end now names what the
  seats record they wrote.

## 7. The game's own captain and a spar carried away (the owner's note 4): part two

"I noticed she did not attempt to replace the topgallant mast or yard": in the first action the
Renard sailed three hours with her main topgallant mast gone and her captain never touched it. The
work exists for a player (`clear away the wreck of the <spar>`, `shift the <spar>`, `rig a jury
mast`, `bend the <sail>`); this part gives it to the game's own captain
(`world.captains.Captain._spar_work`, given from his repairs, `Captain._repairs`). This is its
fourth pass, by the lead's list of 2026-11-27 (the reader's third read) and his ruling of the same
afternoon.

**What he does, in turn.**

1. **The wreck cleared** (`clear_wreck.yaml`): the spar's and every spar's that went with it, the
   one that keeps her manageable first (`SPAR_MEND_ORDER`: the bowsprit and the lower masts, the
   jib-boom, the topmasts, the gaff and the boom, the yards, then the topgallant masts), a light
   spar's (`light_spar`: a studding-sail boom, a royal mast, or what stands on one) last of all and
   only with nothing at all in hand. The sails that stood on it are noted to be bent again, and
   those she had set, to be set again.
2. **A head sail set once** (`_head_sail_for_the_wreck`) where the wreck took the head sails she
   had set: the first of her `headsails` that still stands, bent and stowed ("setting the fore
   staysail (to keep her head off, her head sails gone)"); none over his shortening line.
3. **A head sail the wreck took bent again** as soon as its spar stands; then **each spar shifted
   for a spare of its class** (`shift_spar.yaml`), or a lower mast stepped again as a jury mast
   (`jury_mast.yaml`), in the same order; the rest of the sails bent again; and **each sail set
   again** where she carried it set when its spar went, or where her sail as she carries it calls
   for one of its kind (`_set_again`). A spar she has no spare for is left as it is (a spare yard
   answers a topsail yard alone, `SPARE_YARD_ANSWERS`). Every order says why in his words.

**The spar's work is the last claimant of her hands, all hands called or not** (items 1 and 3).

- Any work short of hands or too few to begin that is not itself a spar's holds the spar's work in
  hand and has its hands (`runner.Runner._spar_work_gives_way`: "Belayed clearing away the wreck
  of the fore topmast: hands to take in the mainsail."). The second pass exempted work merely
  short while all hands were called by order, so that once he had turned the hands up for the
  wreck her sail work went short with the wreck named ("Only four hands to the mainsail; the rest
  are clearing away the wreck of the fore topmast."). The exemption is gone, for his all hands and
  the player's alike: no work goes short with the wreck named as what the rest are at (truth 7-777
  c, on the bilander with all hands called and without).
- **A quiet before it is taken up again**: the spar's work held is taken up where it stood only when
  nothing has waited for hands or gone on short for five minutes (`runner.SPAR_WORK_RESUME_QUIET_S`,
  300 s; truth 7-777 d). The reader's twelve belays in the bilander's passage in 25 knots on seed 3
  are six now; the most in any of the 140 cell-seeds is nine (the cutter in 25 knots, seed 3, whose
  watch tends her sheets and braces through the three hours), and the median three.
- **A spar's work held stands in no one's way** (found in this pass): held, it still held its parts,
  so that the `lie a-try` he gave in the rising gale waited behind the clearing held for the weather
  ("'Lie a-try' will follow 'clear away the wreck of the main topmast', which the hands are still
  at."), and the brig on seeds 7 and 9 and the frigate on seed 9 were never brought to. Now later
  work does not wait for it (`_start_waiting`), and it is not taken up again while work begun
  meanwhile shares its parts (`_spar_work_waits`; truth 7-777 e). All three are brought to at the
  trunk's own tick.

**He begins none** while an order of his or the watch's waits for hands or its turn, nor under fire
(a shot come aboard within ten minutes), in action or struck; **the shift** (and the bending and
setting after it) only with her under command (no manoeuvre in hand, her way on, her sails
drawing).

**Heavy weather: no spar work at all unless she lies to** (item 4 (b), the lead's leaning taken as
it stands). At his shortening line or over it, or with the weather worsening (the glass falling
fast, or the wind risen by a force within the hour: `_weather_against_spar_work`), he does no
spar's work at all, the wreck's clearing with it, unless she is brought to for the weather
(`_lying_to_for_weather`). Work in hand when the weather turns is held, its progress kept and its
hands let go ("Belayed clearing away the wreck of the main topmast: hands kept for the weather.",
`Captain._hold_spar_work_for_weather`), and none is begun or taken up again while he holds it
(`runner.SPAR_WORK_WEATHER_HELD`). So in a rising gale he is the trunk's captain until she lies to,
the wreck hanging as it hung on the trunk, save where its clearing was begun in the settled weather
before (truth 7-777 e). Lying to, the wreck is cut away whatever the wind (the lugger of the gale
from the start, §8, clears her main topmast's wreck lying to); the spar is shifted when the gale is
over.

**A wreck is never left for good while she has hands** (`WRECK_HANDS_UP_S`, an hour): where her
watch is never free of its own work, a wreck that has hung an hour has all hands turned up for it
("calling all hands (to clear away the wreck of the main topmast)") and they are piped down when it
is cleared ("piping down (the wreck cleared away)"), **in settled weather only, and never as she is
brought to** (items 3 and 4: the 74 in 20 rising to 38 on seed 3 was called all hands for the wreck
in the tick she was given `lie a-try`). Truth 7-777 f holds it at the function: at the hour and not
a second before, never at his shortening line, with the weather worsening, with a bringing-to in
hand or given that tick, and piped down when the wreck is cleared.

**The lead's question: a wreck through a gale, and after.** With the weather against it he does no
spar work, so a wreck hangs while he shortens and while she is brought to. Once she lies to for the
weather it is cut away; when the gale is over (under his shortening line, the glass no longer
falling fast, a force not risen in the hour) and she is under command, a wreck still hanging is
cleared, an hour of it with her watch never free has all hands turned up for it, and the spar is
shifted, its sails bent and set. Nothing in the captain leaves a wreck for good: the clearing waits
on her being brought to or on the weather settling, and on her hands.

**The Renard's own case** (the owner's): her main topgallant mast shot away, she carries no spare
for it (the cutter's booms: one spare topmast, one spare topsail yard). The captain clears the wreck
out of action, and the clearing's line says so: "Cleared the wreck of the main topgallant mast ...
There is no spare topgallant mast aboard." (truth 7-777); nothing is shifted, and the topgallant
yard waits on its mast. What a cutter could send up in its place from what she carries: her
topgallant "mast" is the pole of her topmast (the ship file, after Fincham: "the 8 ft pole of the
topmast, on which the topgallant sets"), so the one spar of hers that would give her a topgallant
pole again is her spare topmast, shifted whole for the topmast, at the cost of the only spare
topmast she has and a topmast's work for a light sail. The captain does not do it, and nothing is
changed for it here.

## 8. `lie a-try` with no topsail to lie under, and a refused bringing-to given again (item 2)

**What she can lie a-try under is a fact of the sail, not of the moment** (item 2). The second
pass's test read the topsail's state: the smack's light topsail, loosed by his own sail for a
strong wind, became one to lie under, and lying a-try under it in the reader's gale from the start
it strained six times and split at 6709 s; the privateer with her fore topmast gone was given `lie
a-try` four times and refused ("She has no topsail to lie a-try under."). Now
(`Captain._topsail_to_lie_under`) it is a topsail of the mast she lies to with (`yards_to_back`),
on a yard and a mast that stand, bent and sound, of working canvas, with reef bands or in her plain
sail. With none she is given `heave to` under the canvas she has, the smack, a boat and a ship whose
topmast is gone alike (truth 7-778).

- **Of working canvas** (`LIE_A_TRY_CANVAS_NO`, No. 4; JUDGEMENT, grounded where it is defined:
  courses and topsails are of No. 2, Luce and Steel; a ship's mizen topsail of No. 4 in the files;
  the sloop's topsail of No. 6 or 7, a light sail). The lead's words alone kept the cutter's
  topsail, which has a reef band and is in her plain sail but is of No. 6: lying a-try under it in
  forty knots it blew out at 3171 s (the gale from the start, below), as the trunk's own cutter's
  does in the reader's gale (the trunk's, unchanged, at 2280 s). It is a sail set in fair weather;
  she heaves to instead, and keeps it.
- **Her light square canvas taken in first** (`_light_canvas_aback`): with no topsail to lie under,
  a square sail of light canvas loosed or set on the yards a heave-to lays aback is taken in before
  she is hove to ("taking in the topsail (to heave to under her fore-and-aft canvas)"), the heave-to
  given at the next try. The smack's topsail, set by his own sail for a strong wind (the trunk's),
  was laid aback by her heave-to and blew out; the cutter's likewise.

**A refused or failed order to bring her to is given again**, ten minutes after the last
(`BRING_TO_AGAIN_S`), while she lies to for the weather and is not brought to, with nothing of the
kind in hand; **tried twice with her sail as it was, it is not given a third time until her sail
changes** (truth 7-778 b: at ten minutes and not before; the third not given; given again with her
sail changed). The second pass counted refusals in the same words only, so that a heave-to accepted
and then failing ("Could not heave to: she would not lie to") was given every ten minutes through
the gale, ten times on the smack; it now counts every try, refused, failed or done, and a try is
not counted done until she is hove to (the count was cleared while she was still heaving to). The
refusal after his own heave-to for the lead ("She is heaving to already.") is given again ten
minutes after, with the cast done.

**The lead's ruling on a ship whose `heave to` fails** (the topsail schooner with her fore topmast
gone, in 20 rising to 38): his (b) in its smallest form was tried, her course given again under
what she carries once the bringing-to rested, said once ("shaping a course for 49 52 n 5 06 w (she
will not lie to; kept away under what she carries)") with her sheets trimmed. It did not restore
her: on seed 9, 15.63 nm made good and 44 minutes astern against 15.17 and 33 without it and the
trunk's 27.37 and 3. Making her sail on as the trunk's did would be a new way of handling her in a
gale; it was not built, and the cells are declared by (a) (§9).

**The gale from the start, every ship file** (two gales: 40 knots from the west steady, sails
furled, `set plain sail`, bound for Falmouth from 48 40 N 5 05 W, seed 7, three hours; and the
reader's, 40 knots from 250 with gustiness and variability 0.2, the same; this hash beside the
trunk at f09fe283, the whole log compared):

*40 knots from the west:*

| Ship file | Trunk: brought to | This hash: brought to | First difference | Refused or failed (trunk / this hash) | Sails lost (trunk / this hash) |
|---|---|---|---|---|---|
| bilander | never | at 8788 s | 905 s | 1 / 3 | fore.topmast staysail, jib, main.settee / fore.topmast staysail, main.settee |
| boat-cutter-23 | never | never | 300 s | 2 / 3 | none / none |
| boat-cutter-28 | never | never | 300 s | 2 / 3 | none / none |
| boat-launch-25 | never | never | 300 s | 2 / 3 | none / none |
| boat-launch-31 | never | never | 300 s | 2 / 3 | none / none |
| boat-yawl-16 | never | never | 300 s | 2 / 3 | none / none |
| brig | at 4614 s | at 4614 s | none: the same in every line | 1 / 1 | none / none |
| cutter | never | at 2100 s | 300 s | 1 / 1 | none / none |
| frigate-36 | at 3909 s | at 3909 s | none: the same in every line | 2 / 2 | main.course / main.course |
| hermaphrodite-brig | at 1225 s | at 1225 s | none: the same in every line | 0 / 0 | none / none |
| lugger | at 3240 s | at 3240 s | 3600 s | 0 / 0 | main.topsail / none |
| merchant-brig | never | at 10547 s | 915 s | 1 / 4 | jib / jib |
| privateer-schooner | never | at 3895 s | 995 s | 1 / 2 | none / none |
| razee-44 | at 3511 s | at 3511 s | none: the same in every line | 1 / 1 | none / none |
| seventy-four | at 4520 s | at 4520 s | none: the same in every line | 1 / 1 | none / none |
| sixty-four | at 3578 s | at 3578 s | none: the same in every line | 0 / 0 | none / none |
| smack | never | at 1500 s | 300 s | 2 / 4 | none / none |
| topsail-schooner | never | at 3895 s | 995 s | 1 / 2 | none / none |

*the reader's: 40 knots from 250, gusty:*

| Ship file | Trunk: brought to | This hash: brought to | First difference | Refused or failed (trunk / this hash) | Sails lost (trunk / this hash) |
|---|---|---|---|---|---|
| bilander | never | at 5476 s | 985 s | 1 / 2 | fore.topmast staysail, jib / fore.topmast staysail, jib |
| boat-cutter-23 | never | never | 300 s | 2 / 3 | none / none |
| boat-cutter-28 | never | never | 300 s | 2 / 3 | none / none |
| boat-launch-25 | never | never | 300 s | 2 / 3 | none / none |
| boat-launch-31 | never | never | 300 s | 2 / 3 | none / none |
| boat-yawl-16 | never | never | 300 s | 2 / 3 | none / none |
| brig | at 3632 s | at 3632 s | none: the same in every line | 1 / 1 | none / none |
| cutter | at 2280 s | at 2100 s | 300 s | 0 / 1 | topsail / none |
| frigate-36 | at 3065 s | at 3065 s | none: the same in every line | 1 / 1 | none / none |
| hermaphrodite-brig | at 1026 s | at 1026 s | none: the same in every line | 0 / 0 | none / none |
| lugger | at 2820 s | at 2820 s | 2843 s | 0 / 0 | main.topsail / none |
| merchant-brig | never | at 5455 s | 937 s | 1 / 2 | fore.topmast staysail, jib / fore.topmast staysail, jib |
| privateer-schooner | never | at 3001 s | 901 s | 1 / 1 | none / none |
| razee-44 | at 2928 s | at 2928 s | 4277 s | 1 / 1 | main.topgallant, main.topgallant.studdingsail.larboard, main.topgallant.studdingsail.starboard / none |
| seventy-four | at 2960 s | at 2960 s | none: the same in every line | 1 / 1 | none / none |
| sixty-four | at 2951 s | at 2951 s | 4291 s | 1 / 1 | main.topgallant, main.topgallant.studdingsail.larboard, main.topgallant.studdingsail.starboard / none |
| smack | never | at 9420 s | 300 s | 2 / 5 | none / none |
| topsail-schooner | never | at 3001 s | 901 s | 1 / 1 | none / none |

- **No sail is lost that the trunk keeps**, in either gale, on any file; four keep a sail the trunk
  loses (the bilander's jib in the westerly; the lugger's main topsail, the razee's and the 64's
  main topgallant and its studding sails in the reader's; the cutter's topsail in the reader's,
  laid to under it on the trunk). The smack's topsail and the cutter's, which the second pass's
  reading lost in the reader's gale and the westerly, are kept.
- **Every ship the trunk's captain brings to is brought to**, at the same tick, save the cutter in
  the reader's gale, at 2100 s against 2280 s (hove to under her fore-and-aft canvas, where the
  trunk's lay a-try under her topsail and lost it).
- **Brought to where the trunk's captain never was:** the bilander, the cutter, the merchant brig,
  the privateer, the topsail schooner and the smack (`lie a-try` given again when the topsail is
  set; `heave to` under her fore-and-aft canvas for the cutter and the smack, their light topsails
  taken in first where set).
- **The boats:** no topsail to lie under, so `heave to` in its place, refused ("No head sail is set
  to haul to windward, nor a topsail to lay aback.") and given once more ten minutes after; then
  rested, her sail unchanged. Not brought to, as on the trunk.
- **The lugger:** brought to as on the trunk; her main topsail carried away in the gale, she clears
  its wreck lying to (§7), where the trunk's left it hanging.
- **The brig, the frigate, the hermaphrodite brig, the razee (westerly), the 74 and the 64
  (westerly):** the trunk's in every line.


## 9. The spar's work against the trunk, seed by seed (the lead's probe, his rulings)

**The probe**: bound for Falmouth from 48 40 N 5 05 W, the game's own captain, a spar carried away
by `strain._wreck_spar` at minute ten, three hours; in 12 knots, 25, 12 with the wind heading her
four points at +45 minutes, and 20 rising to 38 over +40 to +70; the bilander (fore topmast), the
merchant brig (main topmast), a topsail schooner (fore topmast), the frigate (main topmast), the
cutter (main topmast), the brig (main topmast) and the 74 (fore topmast); **seeds 3, 7, 8, 9 and
11**, the reader's (`tests/test_mends_126.py`, `_spar_passage`). Measured on the trunk itself
(f09fe283, the code of the trunk now), on the trunk with the wreck cleared at the moment it fell (no
hands spent and no time: its sails to the sail room, its spars sent down), and on this hash.

**The judging is by seed** (item 4 (a), and the lead's ruling on the rule's own fault). On each
cell-seed she passes where she is not worse than the trunk; or, where the wreck cleared at once is
the yardstick (itself worse than the trunk beyond the allowances: a wreck hanging pays some hulls
off like a head sail, the physics giving it three times its windage and none of its harm, the
carried list, fault 22), where she is not worse than that. Not worse: minutes astern not more than
five beyond, times aback not more than one beyond, brought to not later than five minutes after,
and way made good not less by more than the price of the hands' work, a tenth of the yardstick's
way and never under a mile (`PASSAGE_WAY_SHARE`, `PASSAGE_WAY_FLOOR_NM`; JUDGEMENT, grounded where
they are defined: the lead's "a mile or two behind for it is a seaman", taken at its lower bound,
and a tenth as the hour's clearing costing a third of her way for that hour of the three). And
wherever the trunk's captain brings her to, so does this one, on every seed. The cell-seeds outside
are declared in the truth (`PASSAGE_DECLARED`), each with its cause, and the truth holds the set
exactly: one more outside, or one of them come inside, fails it.

**The result: 121 of the 140 cell-seeds inside; 19 declared.** The wreck cleared at once is the
yardstick in 44. Every cell-seed on which the trunk's captain brings her to, this one does.

The nineteen, each with its cause:

- **the topsail schooner, 20 rising to 38, seeds 3, 7, 8, 9, 11**: her fore topmast gone, she has no topsail to lie a-try under and is given `heave to`, which fails in thirty-eight knots or takes late, where the trunk's captain, refused `lie a-try` once, let her sail on: tried to bring her to where the trunk's captain did not, and could not (the lead's ruling of 2026-11-27, (a)).
- **the cutter, 20 rising to 38, seeds 3, 7, 8, 9, 11**: her topsail of light canvas, she is hove to under her fore-and-aft canvas where the trunk's captain, refused `lie a-try`, let her sail on: brought to where the trunk's captain was not (the lead's ruling of 2026-11-27, (a)).
- **the frigate, 25 knots, seed 7**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): aback eleven times against eight in her wears; 4.65 nm against 4.23, 15 minutes astern against 19.
- **the frigate, 20 rising to 38, seed 3**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) before the rise: given `lie a-try` at the trunk's tick, she lies a-try 545 s after it; 13.29 nm against 12.34.
- **the brig, 20 rising to 38, seed 3**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) just before the rise: given `lie a-try` at the trunk's tick, she comes round through the wind as she is brought up and lies a-try 689 s after it; 10.61 nm against 2.70, 18 minutes astern against 44.
- **the 74, 25 knots, seed 7**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): 117 minutes astern against the wreck cleared at once's 111 and the trunk's 96.
- **the 74, 20 rising to 38, seed 3**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) before the rise: 7.30 nm against the trunk's 8.58 and the wreck cleared at once's 11.17, 97 minutes astern as the latter's.
- **the topsail schooner, 12 knots with the wind heading her, seed 11**: the clearing in hand through her wear and her tack, the hands turned up for it at the hour: 21 minutes astern against 15, and 8.98 nm made good against 6.64.
- **the cutter, 12 knots with the wind heading her, seed 7**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22) before the wind headed her: 175 minutes astern against 165 (astern most of the three hours whatever is done), aback once against three, -0.87 nm against -1.37.
- **the cutter, 12 knots with the wind heading her, seed 9**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): 178 minutes astern against 172, the wreck cleared at once's 177.
- **the 74, 12 knots with the wind heading her, seed 8**: the wreck's sails lowered to the deck, its windage gone (the carried list, fault 22): 144 minutes astern against 138, the wreck cleared at once's 143.

**What the brig loses her way to in the rising wind** (item 4): the wreck itself. Her clearing
begun at minute eleven in the settled twenty knots, its sails are lowered to the deck before the
rise, and the hanging wreck's windage, which pays her off on the trunk, is gone. Brought to at the
trunk's own tick on seeds 7 and 9 (6266 s and 6200 s), she makes 13.22 and 13.91 nm against the
trunk's 16.19 and 16.84, and the wreck cleared at once makes 12.80 and 14.60: no sail left unset, no
trim waiting, no hands kept from her; the same loss as the instant clearing's, inside the rule
against it. On seed 8 she is inside against the trunk; on seed 3 she lies a-try 689 s later, but
makes 10.61 nm against 2.70 (declared above).

**The trunk in this tree.** `_spar_passage` runs the trunk's captain within this tree (the spar's
work, the hold for the weather, the bring-to given again and the narrowed `lie a-try` patched
out); `test_truth_7_779_b_the_trunk_in_this_tree_is_the_trunk` holds one cell to the trunk's own
figures at f09fe283, and the probe's trunk and instant clearing were run on the trunk itself.

**The table, whole** (made good nm / minutes astern / times aback / tick brought to; belays: the
spar's work held for her working or the weather in the passage):

| Ship | Wind | Seed | Yardstick | Trunk | Wreck cleared at once | Package 126 | Belays | |
|---|---|---|---|---|---|---|---|---|
| bilander | 12 kn | 3 | the instant | 10.63 / 0 / 0 / - | -0.21 / 171 / 2 / - | 10.86 / 0 / 0 / - | 4 | inside |
| bilander | 12 kn | 7 | the instant | 9.94 / 0 / 1 / - | 9.88 / 22 / 1 / - | 10.19 / 0 / 1 / - | 4 | inside |
| bilander | 12 kn | 8 | the instant | 9.40 / 0 / 0 / - | 8.68 / 22 / 1 / - | 9.58 / 0 / 0 / - | 4 | inside |
| bilander | 12 kn | 9 | the instant | 10.86 / 0 / 0 / - | -0.22 / 171 / 2 / - | 10.27 / 0 / 0 / - | 3 | inside |
| bilander | 12 kn | 11 | the instant | 9.94 / 0 / 0 / - | -0.11 / 171 / 2 / - | 10.47 / 0 / 0 / - | 3 | inside |
| bilander | 25 kn | 3 | the instant | 16.10 / 0 / 0 / - | 3.90 / 85 / 5 / - | 15.88 / 5 / 0 / - | 6 | inside |
| bilander | 25 kn | 7 | the instant | 3.23 / 89 / 2 / - | 5.00 / 58 / 6 / - | 3.23 / 89 / 2 / - | 0 | inside |
| bilander | 25 kn | 8 | the instant | 15.02 / 0 / 0 / - | 12.74 / 36 / 2 / - | 15.87 / 0 / 0 / - | 3 | inside |
| bilander | 25 kn | 9 | the instant | 9.26 / 29 / 4 / - | 1.13 / 107 / 5 / - | 16.46 / 0 / 0 / - | 3 | inside |
| bilander | 25 kn | 11 | the instant | 15.41 / 0 / 0 / - | 0.90 / 114 / 2 / - | 17.50 / 0 / 0 / - | 2 | inside |
| bilander | 12 kn, heading | 3 | the instant | 5.99 / 0 / 0 / - | -1.29 / 172 / 2 / - | 6.09 / 0 / 0 / - | 4 | inside |
| bilander | 12 kn, heading | 7 | the instant | 2.62 / 76 / 0 / - | -1.10 / 168 / 2 / - | 3.01 / 81 / 1 / - | 6 | inside |
| bilander | 12 kn, heading | 8 | the instant | 5.64 / 0 / 0 / - | -0.57 / 170 / 2 / - | 5.75 / 0 / 0 / - | 4 | inside |
| bilander | 12 kn, heading | 9 | the instant | 5.91 / 0 / 0 / - | -1.26 / 173 / 2 / - | 5.99 / 0 / 0 / - | 3 | inside |
| bilander | 12 kn, heading | 11 | the instant | 6.01 / 0 / 0 / - | -1.18 / 171 / 2 / - | 6.13 / 0 / 0 / - | 4 | inside |
| bilander | 20 to 38 | 3 | the instant | 14.24 / 0 / 0 / 6889 | 0.64 / 154 / 1 / 6751 | 14.24 / 0 / 0 / 6889 | 1 | inside |
| bilander | 20 to 38 | 7 | the instant | 8.90 / 21 / 1 / 6123 | 2.28 / 141 / 1 / 6247 | 8.90 / 21 / 1 / 6123 | 3 | inside |
| bilander | 20 to 38 | 8 | the instant | 11.87 / 0 / 1 / 7103 | 0.56 / 160 / 1 / 7086 | 11.87 / 0 / 1 / 7103 | 1 | inside |
| bilander | 20 to 38 | 9 | the instant | 14.32 / 0 / 0 / 6340 | -0.71 / 163 / 1 / 6140 | 14.32 / 0 / 0 / 6340 | 1 | inside |
| bilander | 20 to 38 | 11 | the instant | 14.28 / 0 / 1 / 6502 | 0.49 / 147 / 1 / 6653 | 14.28 / 0 / 1 / 6502 | 0 | inside |
| merchant brig | 12 kn | 3 | the trunk | 9.12 / 15 / 2 / - | 12.13 / 0 / 0 / - | 9.65 / 15 / 2 / - | 4 | inside |
| merchant brig | 12 kn | 7 | the trunk | 9.52 / 5 / 1 / - | 11.34 / 0 / 0 / - | 10.02 / 5 / 1 / - | 3 | inside |
| merchant brig | 12 kn | 8 | the trunk | 9.01 / 5 / 1 / - | 10.48 / 0 / 0 / - | 9.56 / 5 / 1 / - | 4 | inside |
| merchant brig | 12 kn | 9 | the trunk | 9.34 / 7 / 1 / - | 12.00 / 0 / 0 / - | 9.76 / 7 / 1 / - | 4 | inside |
| merchant brig | 12 kn | 11 | the trunk | 9.95 / 6 / 1 / - | 11.83 / 0 / 0 / - | 10.40 / 6 / 1 / - | 4 | inside |
| merchant brig | 25 kn | 3 | the trunk | 8.67 / 27 / 6 / - | 17.99 / 0 / 1 / - | 10.32 / 21 / 4 / - | 5 | inside |
| merchant brig | 25 kn | 7 | the trunk | 10.44 / 6 / 1 / - | 16.16 / 0 / 2 / - | 10.59 / 6 / 1 / - | 4 | inside |
| merchant brig | 25 kn | 8 | the trunk | -3.76 / 22 / 11 / - | 16.60 / 0 / 1 / - | 4.42 / 19 / 12 / - | 2 | inside |
| merchant brig | 25 kn | 9 | the trunk | 10.66 / 6 / 1 / - | 15.60 / 0 / 2 / - | 10.78 / 6 / 1 / - | 4 | inside |
| merchant brig | 25 kn | 11 | the trunk | 13.49 / 17 / 3 / - | 17.39 / 0 / 3 / - | 14.60 / 16 / 2 / - | 4 | inside |
| merchant brig | 12 kn, heading | 3 | the trunk | 2.16 / 15 / 2 / - | 7.55 / 0 / 0 / - | 4.04 / 14 / 1 / - | 7 | inside |
| merchant brig | 12 kn, heading | 7 | the trunk | 4.73 / 11 / 1 / - | 5.97 / 0 / 0 / - | 4.87 / 11 / 1 / - | 5 | inside |
| merchant brig | 12 kn, heading | 8 | the trunk | 5.88 / 15 / 1 / - | 5.84 / 0 / 0 / - | 6.15 / 15 / 1 / - | 5 | inside |
| merchant brig | 12 kn, heading | 9 | the trunk | 4.23 / 32 / 2 / - | 7.37 / 0 / 0 / - | 5.16 / 25 / 2 / - | 8 | inside |
| merchant brig | 12 kn, heading | 11 | the trunk | 4.76 / 12 / 1 / - | 7.73 / 0 / 0 / - | 5.09 / 12 / 1 / - | 4 | inside |
| merchant brig | 20 to 38 | 3 | the trunk | 1.53 / 28 / 1 / 7611 | 11.16 / 0 / 0 / 6953 | 1.53 / 28 / 1 / 7611 | 1 | inside |
| merchant brig | 20 to 38 | 7 | the trunk | -5.51 / 22 / 1 / 7348 | 9.13 / 0 / 0 / 6150 | -5.51 / 22 / 1 / 7348 | 1 | inside |
| merchant brig | 20 to 38 | 8 | the trunk | 2.84 / 41 / 1 / 7706 | 9.95 / 9 / 0 / 7201 | 2.84 / 41 / 1 / 7706 | 0 | inside |
| merchant brig | 20 to 38 | 9 | the trunk | -5.81 / 28 / 1 / 6526 | 16.47 / 0 / 1 / 5119 | -5.81 / 28 / 1 / 6526 | 0 | inside |
| merchant brig | 20 to 38 | 11 | the trunk | -2.82 / 49 / 1 / 7673 | 13.74 / 0 / 0 / 7088 | -2.82 / 49 / 1 / 7673 | 1 | inside |
| topsail schooner | 12 kn | 3 | the trunk | 16.75 / 1 / 0 / - | 17.43 / 1 / 0 / - | 17.52 / 1 / 0 / - | 4 | inside |
| topsail schooner | 12 kn | 7 | the trunk | 12.41 / 1 / 0 / - | 13.60 / 1 / 0 / - | 14.57 / 1 / 0 / - | 4 | inside |
| topsail schooner | 12 kn | 8 | the trunk | 13.44 / 1 / 0 / - | 14.25 / 1 / 0 / - | 15.07 / 1 / 0 / - | 4 | inside |
| topsail schooner | 12 kn | 9 | the trunk | 16.93 / 1 / 0 / - | 17.52 / 1 / 0 / - | 17.43 / 1 / 0 / - | 5 | inside |
| topsail schooner | 12 kn | 11 | the trunk | 15.50 / 14 / 1 / - | 15.95 / 14 / 1 / - | 16.05 / 14 / 1 / - | 4 | inside |
| topsail schooner | 25 kn | 3 | the trunk | 29.61 / 1 / 0 / - | 30.09 / 3 / 0 / - | 30.22 / 1 / 0 / - | 8 | inside |
| topsail schooner | 25 kn | 7 | the trunk | 23.92 / 5 / 0 / - | 25.91 / 5 / 0 / - | 26.63 / 5 / 0 / - | 6 | inside |
| topsail schooner | 25 kn | 8 | the trunk | 27.45 / 2 / 0 / - | 27.71 / 3 / 0 / - | 27.82 / 2 / 0 / - | 8 | inside |
| topsail schooner | 25 kn | 9 | the trunk | 29.11 / 5 / 0 / - | 29.74 / 5 / 0 / - | 29.54 / 5 / 0 / - | 6 | inside |
| topsail schooner | 25 kn | 11 | the trunk | 29.95 / 1 / 0 / - | 30.19 / 2 / 0 / - | 30.31 / 1 / 0 / - | 7 | inside |
| topsail schooner | 12 kn, heading | 3 | the instant | 8.93 / 1 / 0 / - | 10.43 / 7 / 1 / - | 9.56 / 1 / 1 / - | 5 | inside |
| topsail schooner | 12 kn, heading | 7 | the trunk | 5.21 / 37 / 3 / - | 8.78 / 1 / 0 / - | 8.75 / 2 / 1 / - | 7 | inside |
| topsail schooner | 12 kn, heading | 8 | the trunk | 8.65 / 1 / 0 / - | 10.09 / 1 / 0 / - | 9.49 / 1 / 1 / - | 7 | inside |
| topsail schooner | 12 kn, heading | 9 | the trunk | 8.23 / 22 / 1 / - | 10.57 / 1 / 0 / - | 10.43 / 1 / 1 / - | 5 | inside |
| topsail schooner | 12 kn, heading | 11 | the trunk | 6.64 / 15 / 2 / - | 9.74 / 15 / 2 / - | 8.98 / 21 / 2 / - | 4 | declared: astern |
| topsail schooner | 20 to 38 | 3 | the trunk | 26.94 / 1 / 0 / - | 28.95 / 4 / 1 / - | 19.85 / 2 / 1 / 11040 | 3 | declared: way |
| topsail schooner | 20 to 38 | 7 | the instant | 27.99 / 3 / 0 / - | 23.51 / 35 / 0 / - | 10.97 / 21 / 0 / 3960 | 3 | declared: way, astern |
| topsail schooner | 20 to 38 | 8 | the trunk | 30.16 / 3 / 0 / - | 31.00 / 3 / 0 / - | 16.37 / 19 / 1 / 9180 | 3 | declared: way, astern |
| topsail schooner | 20 to 38 | 9 | the trunk | 27.37 / 3 / 0 / - | 28.70 / 3 / 1 / - | 15.17 / 33 / 0 / - | 3 | declared: way, astern |
| topsail schooner | 20 to 38 | 11 | the trunk | 27.13 / 2 / 0 / - | 28.79 / 3 / 0 / - | 15.89 / 2 / 0 / - | 3 | declared: way |
| frigate | 12 kn | 3 | the trunk | 8.06 / 3 / 1 / - | 11.67 / 0 / 0 / - | 10.41 / 4 / 1 / - | 1 | inside |
| frigate | 12 kn | 7 | the trunk | 9.39 / 0 / 0 / - | 11.47 / 0 / 0 / - | 11.66 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn | 8 | the trunk | 10.03 / 0 / 0 / - | 12.42 / 0 / 0 / - | 12.29 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn | 9 | the trunk | 9.96 / 0 / 0 / - | 12.78 / 0 / 0 / - | 12.61 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn | 11 | the trunk | 11.81 / 0 / 0 / - | 14.35 / 0 / 0 / - | 13.76 / 0 / 0 / - | 0 | inside |
| frigate | 25 kn | 3 | the trunk | 29.08 / 0 / 0 / - | 30.23 / 0 / 0 / - | 29.99 / 0 / 0 / - | 0 | inside |
| frigate | 25 kn | 7 | the trunk | 4.23 / 19 / 8 / - | 11.38 / 1 / 1 / 4054 | 4.65 / 15 / 11 / - | 3 | declared: aback |
| frigate | 25 kn | 8 | the trunk | 27.86 / 0 / 0 / - | 28.73 / 0 / 0 / - | 28.42 / 0 / 0 / - | 0 | inside |
| frigate | 25 kn | 9 | the trunk | 7.69 / 3 / 0 / 4075 | 14.48 / 3 / 1 / 4118 | 10.00 / 3 / 0 / 4073 | 2 | inside |
| frigate | 25 kn | 11 | the trunk | 27.22 / 0 / 0 / - | 30.38 / 0 / 0 / - | 28.22 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn, heading | 3 | the trunk | 4.99 / 8 / 5 / - | 6.50 / 4 / 1 / - | 6.01 / 10 / 5 / - | 2 | inside |
| frigate | 12 kn, heading | 7 | the trunk | 4.26 / 9 / 2 / - | 7.73 / 0 / 0 / - | 7.48 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn, heading | 8 | the trunk | 5.96 / 1 / 0 / - | 7.91 / 3 / 1 / - | 7.11 / 0 / 0 / - | 2 | inside |
| frigate | 12 kn, heading | 9 | the trunk | 4.33 / 9 / 2 / - | 9.15 / 0 / 0 / - | 9.07 / 0 / 0 / - | 0 | inside |
| frigate | 12 kn, heading | 11 | the instant | 8.52 / 0 / 0 / - | 6.91 / 5 / 1 / - | 10.00 / 0 / 0 / - | 0 | inside |
| frigate | 20 to 38 | 3 | the trunk | 12.34 / 17 / 5 / 5293 | 22.60 / 0 / 0 / 5442 | 13.29 / 24 / 2 / 5838 | 1 | declared: astern, brought to late |
| frigate | 20 to 38 | 7 | the trunk | 13.43 / 20 / 2 / 5480 | 15.19 / 6 / 2 / 5155 | 16.08 / 19 / 2 / 5421 | 1 | inside |
| frigate | 20 to 38 | 8 | the trunk | 18.47 / 18 / 1 / 6279 | 24.57 / 0 / 0 / 6196 | 24.07 / 0 / 0 / 6236 | 1 | inside |
| frigate | 20 to 38 | 9 | the trunk | 13.06 / 12 / 1 / 5194 | 21.70 / 0 / 0 / 5153 | 14.55 / 8 / 1 / 5194 | 3 | inside |
| frigate | 20 to 38 | 11 | the trunk | 16.49 / 13 / 0 / 5764 | 24.16 / 0 / 0 / 5877 | 22.46 / 0 / 0 / 5906 | 1 | inside |
| cutter | 12 kn | 3 | the trunk | 0.10 / 175 / 1 / - | 0.40 / 174 / 2 / - | 0.48 / 175 / 1 / - | 0 | inside |
| cutter | 12 kn | 7 | the trunk | 0.17 / 175 / 0 / - | 0.65 / 167 / 0 / - | 0.66 / 175 / 0 / - | 0 | inside |
| cutter | 12 kn | 8 | the instant | 0.39 / 175 / 1 / - | 0.70 / 174 / 3 / - | 0.77 / 175 / 1 / - | 0 | inside |
| cutter | 12 kn | 9 | the trunk | -0.11 / 178 / 2 / - | 0.16 / 177 / 2 / - | 0.28 / 178 / 2 / - | 1 | inside |
| cutter | 12 kn | 11 | the trunk | 0.22 / 175 / 1 / - | 0.49 / 174 / 1 / - | 0.60 / 175 / 1 / - | 0 | inside |
| cutter | 25 kn | 3 | the trunk | 24.31 / 0 / 0 / - | 25.31 / 0 / 0 / - | 25.18 / 0 / 0 / - | 9 | inside |
| cutter | 25 kn | 7 | the trunk | 3.73 / 153 / 1 / - | 16.00 / 60 / 1 / - | 15.81 / 57 / 0 / - | 7 | inside |
| cutter | 25 kn | 8 | the trunk | 22.02 / 0 / 0 / - | 22.90 / 0 / 0 / - | 22.69 / 0 / 0 / - | 7 | inside |
| cutter | 25 kn | 9 | the trunk | 7.85 / 122 / 1 / - | 25.12 / 0 / 0 / - | 25.02 / 0 / 0 / - | 7 | inside |
| cutter | 25 kn | 11 | the trunk | 8.26 / 122 / 0 / - | 25.52 / 0 / 0 / - | 25.53 / 0 / 0 / - | 7 | inside |
| cutter | 12 kn, heading | 3 | the instant | -1.51 / 166 / 3 / - | -1.07 / 174 / 2 / - | -1.02 / 175 / 2 / - | 3 | inside |
| cutter | 12 kn, heading | 7 | the trunk | -1.37 / 165 / 3 / - | -0.70 / 167 / 1 / - | -0.87 / 175 / 1 / - | 1 | declared: astern |
| cutter | 12 kn, heading | 8 | the trunk | -1.25 / 174 / 2 / - | -0.72 / 174 / 3 / - | -0.63 / 175 / 1 / - | 1 | inside |
| cutter | 12 kn, heading | 9 | the trunk | -1.69 / 172 / 5 / - | -1.33 / 177 / 2 / - | -1.17 / 178 / 2 / - | 2 | declared: astern |
| cutter | 12 kn, heading | 11 | the instant | -1.44 / 168 / 3 / - | -1.08 / 174 / 2 / - | -0.93 / 175 / 2 / - | 3 | inside |
| cutter | 20 to 38 | 3 | the trunk | 0.92 / 178 / 1 / - | 0.85 / 177 / 2 / - | -0.36 / 178 / 1 / 4140 | 1 | declared: way |
| cutter | 20 to 38 | 7 | the trunk | 0.69 / 177 / 1 / - | 0.60 / 177 / 1 / - | -0.82 / 177 / 1 / 3960 | 2 | declared: way |
| cutter | 20 to 38 | 8 | the trunk | 1.03 / 177 / 1 / - | 0.90 / 177 / 1 / - | -0.11 / 177 / 1 / 4128 | 1 | declared: way |
| cutter | 20 to 38 | 9 | the trunk | 0.98 / 178 / 1 / - | 0.88 / 177 / 1 / - | -0.79 / 178 / 1 / 4020 | 0 | declared: way |
| cutter | 20 to 38 | 11 | the trunk | 1.23 / 178 / 1 / - | 1.10 / 177 / 1 / - | -0.23 / 178 / 1 / 4140 | 0 | declared: way |
| brig | 12 kn | 3 | the trunk | 9.71 / 7 / 2 / - | 13.38 / 0 / 0 / - | 12.82 / 0 / 0 / - | 4 | inside |
| brig | 12 kn | 7 | the trunk | 11.04 / 0 / 0 / - | 12.34 / 0 / 0 / - | 12.27 / 0 / 0 / - | 3 | inside |
| brig | 12 kn | 8 | the trunk | 12.10 / 0 / 0 / - | 13.03 / 0 / 0 / - | 12.90 / 0 / 0 / - | 6 | inside |
| brig | 12 kn | 9 | the trunk | 11.72 / 0 / 0 / - | 13.59 / 0 / 0 / - | 13.26 / 0 / 0 / - | 3 | inside |
| brig | 12 kn | 11 | the trunk | 12.90 / 0 / 0 / - | 13.96 / 0 / 0 / - | 13.74 / 0 / 0 / - | 5 | inside |
| brig | 25 kn | 3 | the instant | 22.82 / 8 / 5 / - | 20.09 / 2 / 2 / - | 23.99 / 8 / 5 / - | 4 | inside |
| brig | 25 kn | 7 | the trunk | 23.09 / 0 / 0 / - | 25.33 / 0 / 0 / - | 24.24 / 0 / 0 / - | 2 | inside |
| brig | 25 kn | 8 | the trunk | 26.30 / 0 / 0 / - | 27.02 / 0 / 0 / - | 26.70 / 0 / 0 / - | 3 | inside |
| brig | 25 kn | 9 | the trunk | 27.56 / 0 / 0 / - | 28.86 / 0 / 0 / - | 28.21 / 0 / 0 / - | 3 | inside |
| brig | 25 kn | 11 | the trunk | 27.44 / 2 / 1 / - | 26.82 / 0 / 1 / - | 27.84 / 2 / 1 / - | 3 | inside |
| brig | 12 kn, heading | 3 | the instant | 6.83 / 8 / 2 / - | 4.36 / 2 / 12 / - | 5.99 / 3 / 1 / - | 5 | inside |
| brig | 12 kn, heading | 7 | the trunk | 7.07 / 0 / 0 / - | 9.01 / 0 / 0 / - | 8.83 / 0 / 0 / - | 3 | inside |
| brig | 12 kn, heading | 8 | the trunk | 7.13 / 7 / 1 / - | 7.85 / 1 / 1 / - | 8.21 / 0 / 1 / - | 7 | inside |
| brig | 12 kn, heading | 9 | the trunk | 6.68 / 5 / 1 / - | 9.39 / 0 / 0 / - | 9.18 / 0 / 0 / - | 3 | inside |
| brig | 12 kn, heading | 11 | the trunk | 9.01 / 0 / 0 / - | 9.97 / 0 / 0 / - | 9.75 / 0 / 0 / - | 5 | inside |
| brig | 20 to 38 | 3 | the trunk | 2.70 / 44 / 6 / 6274 | 14.19 / 2 / 1 / 6223 | 10.61 / 18 / 4 / 6963 | 5 | declared: brought to late |
| brig | 20 to 38 | 7 | the instant | 16.19 / 0 / 0 / 6266 | 12.80 / 0 / 0 / 6087 | 13.22 / 0 / 0 / 6266 | 4 | inside |
| brig | 20 to 38 | 8 | the trunk | 23.11 / 0 / 0 / 6779 | 21.78 / 0 / 0 / 6649 | 21.64 / 0 / 0 / 6697 | 4 | inside |
| brig | 20 to 38 | 9 | the instant | 16.84 / 0 / 0 / 6200 | 14.60 / 0 / 0 / 6220 | 13.91 / 0 / 0 / 6200 | 4 | inside |
| brig | 20 to 38 | 11 | the instant | 18.32 / 8 / 4 / 6424 | 13.67 / 7 / 3 / 6363 | 13.57 / 8 / 4 / 6424 | 4 | inside |
| 74 | 12 kn | 3 | the instant | 0.06 / 161 / 2 / - | -0.53 / 176 / 2 / - | 0.06 / 161 / 2 / - | 0 | inside |
| 74 | 12 kn | 7 | the trunk | 7.95 / 0 / 0 / - | 9.25 / 0 / 0 / - | 10.30 / 0 / 0 / - | 0 | inside |
| 74 | 12 kn | 8 | the instant | 9.25 / 0 / 0 / - | 4.17 / 104 / 1 / - | 11.18 / 0 / 0 / - | 0 | inside |
| 74 | 12 kn | 9 | the trunk | 8.10 / 0 / 0 / - | 10.07 / 0 / 0 / - | 10.98 / 0 / 0 / - | 0 | inside |
| 74 | 12 kn | 11 | the trunk | 10.19 / 0 / 0 / - | 12.47 / 0 / 0 / - | 12.91 / 0 / 0 / - | 0 | inside |
| 74 | 25 kn | 3 | the trunk | 26.83 / 0 / 0 / - | 27.73 / 0 / 0 / - | 27.68 / 0 / 0 / - | 0 | inside |
| 74 | 25 kn | 7 | the instant | 6.51 / 96 / 9 / - | 1.88 / 111 / 20 / - | 2.98 / 117 / 14 / - | 6 | declared: way, astern, aback |
| 74 | 25 kn | 8 | the trunk | 24.90 / 0 / 0 / - | 25.71 / 0 / 0 / - | 25.68 / 0 / 0 / - | 0 | inside |
| 74 | 25 kn | 9 | the instant | 25.50 / 8 / 1 / - | 1.51 / 120 / 21 / - | 26.28 / 8 / 1 / - | 1 | inside |
| 74 | 25 kn | 11 | the trunk | 26.00 / 0 / 0 / - | 26.85 / 0 / 0 / - | 26.78 / 0 / 0 / - | 0 | inside |
| 74 | 12 kn, heading | 3 | the instant | -1.06 / 162 / 3 / - | -1.51 / 176 / 2 / - | -1.06 / 162 / 3 / - | 0 | inside |
| 74 | 12 kn, heading | 7 | the instant | 0.62 / 131 / 2 / - | 0.56 / 143 / 2 / - | 0.41 / 144 / 2 / - | 3 | inside |
| 74 | 12 kn, heading | 8 | the trunk | 1.24 / 138 / 2 / - | 1.19 / 143 / 2 / - | 1.04 / 144 / 2 / - | 4 | declared: astern |
| 74 | 12 kn, heading | 9 | the instant | 0.48 / 136 / 2 / - | 0.50 / 144 / 2 / - | 0.31 / 142 / 2 / - | 4 | inside |
| 74 | 12 kn, heading | 11 | the instant | 1.04 / 136 / 2 / - | 0.86 / 143 / 2 / - | 0.79 / 143 / 2 / - | 4 | inside |
| 74 | 20 to 38 | 3 | the instant | 8.58 / 52 / 4 / 5351 | 11.17 / 97 / 0 / 5496 | 7.30 / 97 / 3 / 5349 | 1 | declared: way, astern |
| 74 | 20 to 38 | 7 | the instant | 9.56 / 43 / 0 / 5018 | 0.82 / 144 / 8 / 4932 | 3.99 / 116 / 1 / 4916 | 1 | inside |
| 74 | 20 to 38 | 8 | the instant | 13.03 / 59 / 1 / 5856 | 11.93 / 92 / 0 / 5806 | 11.84 / 89 / 0 / 5840 | 1 | inside |
| 74 | 20 to 38 | 9 | the instant | 13.88 / 25 / 0 / 5380 | 11.16 / 90 / 0 / 5318 | 10.83 / 86 / 0 / 5359 | 1 | inside |
| 74 | 20 to 38 | 11 | the instant | 13.67 / 34 / 0 / 5527 | 11.57 / 97 / 0 / 5462 | 11.54 / 87 / 0 / 5503 | 1 | inside |


## 10. The wreck's order pinned, and the mechanisms (items 1 and 3 of the third read)

The reader's mutant M03 (`rank` turned so that a light spar's wreck sorts first) is killed by truth
7-777 b. **Every mechanism is now pinned at the function, in the fast tier**, each truth a small
world with the state set by hand and the one behaviour asserted: 7-777 c (work short of hands, all
hands called or not, belays the spar's work and has its hands), 7-777 d (nothing taken up while
work waits, nor within five quiet minutes), 7-777 e (no spar's work with the wind at the line or the
weather worsening unless she lies to; work in hand held for the weather; held, it stands in no one's
way), 7-777 f (all hands at the hour, in settled weather, never as she is brought to; piped down),
7-777 g (the head sail after the clearing), 7-778 b (a refused bringing-to given again at ten
minutes and resting after the second try with her sail unchanged). **The mutation check** (each
mutant alone on a copy of this hash; the fast tests of `tests/test_mends_126.py`, `-x`):

| Mutant | | Whose | Killed by (fast tier) |
|---|---|---|---|
| N01 | the giving-way removed (the spar's work never yields its hands) | the reader's | 7-777 c, 7-777 d |
| N02 | the resume not waiting (`_spar_work_waits` dropped from `_try_resume`) | the reader's | 7-777 d |
| N03 | the weather gate dropped | the reader's | 7-777 e |
| N04 | `_weather_against_spar_work` blind to the trend | the reader's | 7-777 e |
| N05 | all hands for the wreck at once | the reader's | 7-777 |
| N06 | all hands never called for the wreck | the reader's | 7-777 f |
| N07 | the bring-to never given again | the reader's | 7-778 b |
| N08 | the bring-to given again for ever | the reader's | 7-778 b |
| N09 | `_topsail_to_lie_under` always true | the reader's | 7-778 |
| N10 | a light spar's wreck sorted first (M03) | the reader's | 7-777 b |
| N11 | a spar's work begun while an order waits | the reader's | 7-777 |
| N12 | no pipe-down | the reader's | 7-777 f |
| N13 | the head sail after the clearing dropped | the reader's | 7-777 g |
| N14 | no quiet before the spar's work is taken up again | this pass | 7-777 d |
| N15 | the hold for the weather not given from his work | this pass | 7-777 e |
| N16 | work merely short does not take the spar's hands (the exemption) | this pass | 7-777 c |
| N17 | all hands for the wreck in heavy weather | this pass | 7-777 f |
| N18 | all hands for the wreck as she is brought to | this pass | 7-777 f |
| N20 | the runner begins a waiting spar's work held for the weather | this pass | 7-777 e |
| N21 | the resume blind to the weather's hold | this pass | 7-777 e |
| N22 | a held spar's work in the way of later work | this pass | 7-777 e |
| N23 | taken up again under work in hand that shares its parts | this pass | 7-777 e |
| N24 | her light canvas not taken in before heaving to | this pass | 7-778 |
| N25 | the canvas not read (a light topsail lain to under) | this pass | 7-778 |

**All 24 killed.** N15, N16, N20 and N23 survived the first run of the check and are killed by the
truths as strengthened (7-777 c at the function, `Runner._short_of_hands`; 7-777 e through his
work each minute, a waiting clearing whose hands come free, and the resume with nothing but the
parts in its way). A nineteenth of this pass's, the topsail on a mast gone, was an equivalent
mutant: a yard carried away with its mast is none of `yards_to_back`'s, and the check is gone.

## 11. The differences on today's ships, and the player's orders

**Today's ships, old beside new** (this hash beside the trunk's code at f09fe283; part one's
harness, §5): every ship file in four cases at seed 7 under the game's own captain (a gale abeam and
a gale close-hauled bound for Falmouth from 48 40 N 5 05 W, the wind rising from 20 to 35 knots over
an hour; a cruise off the Lizard, 12 knots, three hours; the June passage off Falmouth under a high,
six hours), the whole log and the end state compared.

| Case | Same in every line and the end state | Differs |
|---|---|---|
| gale abeam | 11 of 18 | the five boats, the cutter, the smack |
| gale close-hauled | 11 of 18 | the five boats, the cutter, the smack |
| cruise | 18 of 18 | none |
| June off Falmouth | 18 of 18 | none |

- **The five boats in the two gales:** at the gale's line `heave to` in place of `lie a-try`, and
  refused in its own words, "Captain's rule 'hove to for weather': order not carried out ('heave
  to'): No head sail is set to haul to windward, nor a topsail to lay aback.", where the trunk's
  said "She has no topsail to lie a-try under."; given once more ten minutes after and refused, then
  rested (one line more than the trunk). Every other line and the end state the trunk's.
- **The cutter in the two gales:** at the gale's line "taking in the topsail (to heave to under her
  fore-and-aft canvas)" where the trunk's said "lying a try"; "heaving to (no topsail to lie a-try
  under; not brought to)" ten minutes after (twice close-hauled); hove to under her fore-and-aft
  canvas at 4920 s abeam and 5580 s close-hauled, where the trunk's lay a-try under her topsail at
  4536 s and 4732 s. Her end: the topsail in its gear and the head sails set, against the trunk's
  topsail set; at the third hour 0.6 knots astern abeam against 1.6, 1.5 close-hauled against 1.7; she ends 2.2
  miles (abeam) from where the trunk's did.
- **The smack in the two gales:** "heaving to (no topsail to lie a-try under)" where the trunk's
  `lie a-try` was refused and she sailed on; hove to under her fore-and-aft canvas at 4140 s, at 0.9
  knots ahead abeam and 0.3 astern close-hauled at the third hour, where the trunk's ran on at 8.6
  knots; her head sails set at the end where the trunk's had them in their gear. The lines that
  follow are the heave-to's.
- **No spar carried away** in any of the 72 runs, so the spar's work is in none of them; the
  probe's 140 cell-seeds and the gale from the start (§8, §9) are where it is measured.

***The first action*, left to the game's own captains** (four hours from its start at seed 7, no
seat): **the same**, line for line (633 lines in the Sherbourne's log on both).

**What a player or a model's seat is served that differs** (every such line, by kind): the
captain's spar orders and their reasons (§7, as before, with "calling all hands (to clear away the
wreck of the ...)" in settled weather only); the runner's hold of a spar's work, for her working
("Belayed clearing away the wreck of the fore topmast: hands to brace the fore yard.") and for the
weather ("... hands kept for the weather."); `heave to` in place of `lie a-try` with no topsail to
lie under, its reason "(no topsail to lie a-try under)", and its refusals; "taking in the topsail (to
heave to under her fore-and-aft canvas)"; a bringing-to given again, "(not brought to)", at most
twice with her sail unchanged.

**The runner's change acts on a player's orders too** (item 5). With no captain, a player's own
`clear away the wreck` is held by a later order of his that is short of hands, and taken up again
after it. The reader's case, the bilander under the player's orders alone (18 knots from the west,
plain sail set, her fore topmast carried away at 900 s, `clear away the wreck of the fore topmast`,
then `reef the main topsail`, `heave to` (refused), `take in the mainsail` at 1680 s), old beside
new:

| | The trunk | This hash |
|---|---|---|
| `take in the mainsail` | waited for hands until the clearing was done, began at 6056 s, the mainsail in at 6143 s | belays the clearing at 2113 s ("Belayed clearing away the wreck of the fore topmast: hands to take in the mainsail."), the mainsail in at 2200 s |
| the wreck cleared | at 6056 s | at 6425 s, taken up again five quiet minutes after her other work |

The brig's and the merchant brig's sequences of the reader's are the same in every line. His later
order is his present wish (the lead's word). **The primer** says it: chapter 3, after the shift,
"The work on a spar carried away ... is the last claimant of her hands: work ordered after it that
is short of hands, or too few to begin, takes its hands ... taken up again where it stood once
nothing else has waited for hands or gone on short for five minutes, with all hands called or
without"; and chapter 9 says what the captain does in a gale with no topsail to lie under and with
a spar carried away. Its words on work in hand otherwise stand: "Short-handed, the work goes slower
and the log says so; with too few it waits for hands" holds of the later work, which is short only
when the spar's hands are not enough for it; and "Belayed work is gone, not paused" is of the
order `belay`, not of the runner's hold.

## 12. The pins moved

**No pin moved.** The truths changed in their bodies are the package's own, unmerged: 7-778 (the
cutter now heaves to under her fore-and-aft canvas and keeps her topsail, where the second pass had
her lie a-try under it; the wording "no topsail to lie a-try under" for "no topsail set to lie
a-try under"; the fact of the sail asserted at the function) and 7-779 b (judged seed by seed over
five seeds, its medians and `PASSAGE_FLOORS` gone). New figures, each JUDGEMENT and grounded where
it is defined: `runner.SPAR_WORK_RESUME_QUIET_S` (300 s), `world.captains.LIE_A_TRY_CANVAS_NO`
(No. 4), and the passage truth's `PASSAGE_ASTERN_MIN` (5), `PASSAGE_ABACK` (1),
`PASSAGE_BROUGHT_S` (300 s), `PASSAGE_WAY_SHARE` (0.10) and `PASSAGE_WAY_FLOOR_NM` (1.0).
`BRING_TO_AGAIN_S` (600 s) and `WRECK_HANDS_UP_S` (3600 s) stand as they were, their rules narrowed
(every try counted; settled weather only). `docs/dev/TuningNotes.md`, "Package 126, part two", has
them.

## 13. Found and not mended, and what this pass could not do

- **A wreck left hanging helps some hulls** (§9; the carried list, fault 22): the physics', for the
  ships' session; nothing of it touched. It is the cause of most of the nineteen declared.
- **A ship with no topsail to lie under whose `heave to` will not hold her** (the topsail schooner
  with her fore topmast gone in thirty-eight knots): tried to bring her to where the trunk's captain
  did not, and could not; the lead carries it for a later package of the captain's (his ruling of
  2026-11-27).
- **A stand-down's save naming** (part one's §6; the carried list, item 21): as it was.
