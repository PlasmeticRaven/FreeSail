# Report: package 126: the harbour, the weather and the captain

**The brief.** `docs/dev/briefs/Brief-Package126.md`: four parts, three of them the owner's notes
2, 3 and 4 from his play of gate M7 (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`), the
fourth item 12 of section 4 of `docs/dev/CarriedForward-M7.md`, with item 6 of the same list beside
the first. The branch is `claude/pkg-126`, cut from the trunk at 112ff819.

**Part one** (the lead's split of 2026-11-27), the harbour's end of a game with the stations' table
and the fog, **was merged at 7bc7de20** by the hash afb5a998; sections 1 to 6 are its record, as
merged. **Part two** is this hash: the captain's spar work (the owner's note 4) and the `lie a-try`
mend (item 12), a third pass on the trunk as it stands, by the lead's list of 2026-11-27 (part two,
items 1 to 3) and his ruling of the same day on the wreck's windage; sections 7 to 13. Its truths
are 7-776 to 7-779 (with 7-777 b and 7-779 b).

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
(`world.captains.Captain._spar_work`, given from his repairs, `Captain._repairs`).

**What he does, in turn.**

1. **The wreck cleared** (`clear_wreck.yaml`): the spar's and every spar's that went with it, the
   one that keeps her manageable first (`SPAR_MEND_ORDER`: the bowsprit and the lower masts, the
   jib-boom, the topmasts, the gaff and the boom, the yards, then the topgallant masts), a light
   spar's (`light_spar`: a studding-sail boom, a royal mast, or what stands on one) last of all and
   only with nothing at all in hand. The sails that stood on it are noted to be bent again, and
   those she had set, to be set again.
2. **A head sail set once** (`_head_sail_for_the_wreck`) where the wreck took the head sails she
   had set: the first of her `headsails` that still stands, bent and stowed ("setting the fore
   staysail (to keep her head off, her head sails gone)"), so that she keeps her head off while the
   spar is shifted; none over his shortening line.
3. **A head sail the wreck took bent again** as soon as its spar stands; then **each spar shifted
   for a spare of its class** (`shift_spar.yaml`), or a lower mast stepped again as a jury mast
   (`jury_mast.yaml`), in the same order; the rest of the sails bent again; and **each sail set
   again** where she carried it set when its spar went, or where her sail as she carries it calls
   for one of its kind (`_set_again`). A spar she has no spare for is left as it is (a spare yard
   answers a topsail yard alone, `SPARE_YARD_ANSWERS`). Every order says why in his words.

**When: the spar's work is the last claimant of her hands** (the lead's list, item 1). The second
pass's captain took the hands that work her: in the reader's 56 passages about twenty had trims,
braces, take-ins, reefs or a heave-to held short by the spar's work. Now:

- **The runner gives her working the spar's hands.** Any work that is short of hands or too few to
  begin and is not itself a spar's (her sails handled, her yards braced, her brought to, a repair)
  holds the spar's work in hand and has its hands (`runner.Runner._spar_work_gives_way`: "Belayed
  clearing away the wreck of the fore topmast: hands to brace the fore yard."). The spar's work is
  taken up again where it stood only when no other work waits for hands or goes on short
  (`_spar_work_waits`), as a manoeuvre's belay is (`_try_resume`). With all hands called by order
  the hands are up for the work, and work merely going on short no longer holds it; work too few to
  begin still does. The manoeuvres' belay of the spar's work (tack, wear, box off) stands as it was.
- **He begins none** while an order of his or the watch's waits for hands or its turn, nor under
  fire (a shot come aboard within ten minutes), in action or struck. **The shift** (and the
  bending and setting after it) **he begins** only with her under command (no manoeuvre in hand,
  her way on, her sails drawing), under his shortening line and with the weather not worsening
  (`_weather_against_spar_work`: the glass falling fast, or the wind risen by a force,
  `worsening_wind_kn`, within the hour: the lead's "he does not begin it with the wind rising
  toward his shortening").
- **The wreck is cut away as soon as there are hands for it**, the gale or no (the lead's ruling
  of 2026-11-27): it waits only while she is shortening in a worsening wind, and is cleared once she
  lies to for the weather (her sail work done and her hands free) or the weather has stopped
  worsening. The trunk's repairs wait for the weather to serve (never lying to, never at the
  shortening figure); a wreck's clearing alone now goes on there (`Captain._repairs`).
- **A wreck is never left for good while she has hands** (`WRECK_HANDS_UP_S`, an hour): where her
  watch is never free of its own work (the bilander's and the merchant brig's, seven on deck, whose
  sail orders waited for hands through every hour of the three in the fresher winds), a wreck that
  has hung an hour has all hands turned up for it ("calling all hands (to clear away the wreck of
  the main topmast)"), and they are piped down when it is cleared ("piping down (the wreck cleared
  away)"). Where all hands are on deck already for her own work, the hour's mark lets the clearing
  go on without a call of his.

**The lead's question: a wreck through a gale, and after.** With the weather worsening he begins no
spar work, so a wreck hangs while he shortens. Once she lies to for the weather the wreck is cleared
(the lugger of the gale from the start, §8, clears her main topmast's wreck lying to); a wreck that
has hung an hour with her watch never free has all hands turned up for it; and when the gale is
over (the wind under his shortening line, the glass no longer falling fast, a force not risen in
the hour) and she is under command again, the spar is shifted, its sails bent and set. Nothing in
the captain leaves a wreck for good: the clearing waits on her hands and on her being brought to
or snug, never on the wind alone. What the third pass found it could not do in three hours: the
bilander in 25 knots on one seed of three is never under command with hands free (aback, boxing off
and wearing in turn the whole while, as the trunk's captain's is), and on the other two has her
clearing begun with all hands up and not done; and the bilander and the merchant brig in the rising
wind have their clearing in hand, belayed in turn by her braces and the lead, and not done by the
third hour: their wreck is being worked, not left.

**The Renard's own case** (the owner's): her main topgallant mast shot away, she carries no spare
for it (the cutter's booms: one spare topmast, one spare topsail yard). The captain clears the wreck
out of action, and the clearing's line says so: "Cleared the wreck of the main topgallant mast ...
There is no spare topgallant mast aboard." (truth 7-777); nothing is shifted, and the topgallant
yard waits on its mast. What a cutter could send up in its place from what she carries: her
topgallant "mast" is the pole of her topmast (the ship file, after Fincham: "the 8 ft pole of the
topmast, on which the topgallant sets"), so the one spar of hers that would give her a topgallant
pole again is her spare topmast, shifted whole for the topmast (the work `shift the main topmast`
does), at the cost of the only spare topmast she has and a topmast's work (a stump of a sound
topmast sent down to send up a new one for a light sail). The captain does not do it, and nothing
is changed for it here: the question of spares is the lead's to put to the owner.

## 8. `lie a-try` with no topsail to lie under, and a refused bringing-to given again (item 12)

**The mend acts only where the topsail can never be set** (the lead's list, item 2). The second
pass's test (`_topsail_to_lie_under`) was false for any topsail furled, so that in a gale from the
start, the topsails furled and about to be set, he gave `heave to`, it was refused, and five more
ships than the smack were changed undeclared. Now `lie a-try` gives way to `heave to` only where
every topsail it keeps is unbent (no sail is bent in a gale) or furled and outside her plain sail
(the ship file's group, which nothing of his would set): of today's ships, the smack's light
topsail alone (no reef bands, not in her plain sail; truth 7-778).

**A refused or failed order to bring her to is given again** (`Captain._bring_to_again`), every
`BRING_TO_AGAIN_S` (ten minutes; JUDGEMENT, grounded where it is defined) while she lies to for the
weather and is not brought to, with nothing of the kind in hand ("lying a try (not brought to)").
Refused twice in the same words with her sail as it was (a boat with no topsail at all; the smack
with no head sail set), it is not given again until her sail changes, so that an order nothing in
hand will make good is not a line every ten minutes. On the trunk it was given once, on entering
the state. **The refusal after his own heave-to for the lead** ("She is heaving to already.", the
bilander of the reader's rising wind) is this case: given again ten minutes after, with the cast
done.

**The gale from the start, every ship file** (40 knots from the west from the first minute, sails
furled, `set plain sail`, bound for Falmouth from 48 40 N 5 05 W, seed 7, three hours; this hash
beside the trunk at f09fe283, the whole log compared):

| Ship file | Trunk: brought to | This hash: brought to | First difference | Bring-to refused or failed (trunk / this hash) |
|---|---|---|---|---|
| bilander | never | at 8788 s | 900 s | 1 / 3 |
| boat-cutter-23 | never | never | 900 s | 1 / 2 |
| boat-cutter-28 | never | never | 900 s | 1 / 2 |
| boat-launch-25 | never | never | 900 s | 1 / 2 |
| boat-launch-31 | never | never | 900 s | 1 / 2 |
| boat-yawl-16 | never | never | 900 s | 1 / 2 |
| brig | at 4614 s | at 4614 s | none: the same in every line | 0 / 0 |
| cutter | never | at 2589 s | 900 s | 1 / 3 |
| frigate-36 | at 3909 s | at 3909 s | none: the same in every line | 0 / 0 |
| hermaphrodite-brig | at 1225 s | at 1225 s | none: the same in every line | 0 / 0 |
| lugger | at 3240 s | at 3240 s | 3240 s | 0 / 0 |
| merchant-brig | never | at 10547 s | 900 s | 1 / 4 |
| privateer-schooner | never | at 3895 s | 900 s | 1 / 2 |
| razee-44 | at 3511 s | at 3511 s | none: the same in every line | 0 / 0 |
| seventy-four | at 4520 s | at 4520 s | none: the same in every line | 0 / 0 |
| sixty-four | at 3578 s | at 3578 s | none: the same in every line | 0 / 0 |
| smack | never | at 1500 s | 300 s | 1 / 3 |
| topsail-schooner | never | at 3895 s | 900 s | 1 / 2 |

- **Brought to where the trunk's never was:** the bilander, the cutter, the merchant brig, the
  privateer, the topsail schooner (`lie a-try` refused at the start for the topsail not set, given
  again when it is) and the smack (`heave to` under her fore-and-aft canvas). No ship the trunk's
  captain brought to is left unbrought, or brought to later.
- **The boats:** no topsail and no heave-to of theirs: "She has no topsail to lie a-try under." once
  more than on the trunk, then nothing; they are not brought to, as on the trunk.
- **The smack:** hove to at 1500 s; at 7429 s her straining foresail is taken in by the captain's
  standing work (the trunk's), which leaves her not lying to, and `heave to` is refused twice ("No
  head sail is set ...") and then not given again with her sail as it is.
- **The lugger:** brought to as on the trunk; her main topmast carried away in the gale, she clears
  its wreck lying to (§7), where the trunk's left it hanging.
- **The brig, the frigate, the hermaphrodite brig, the razee, the 74 and the 64:** the trunk's in
  every line.

## 9. The spar's work against the trunk (the lead's probe and his ruling)

**The probe** (the lead's list, item 1): bound for Falmouth from 48 40 N 5 05 W, the game's own
captain, a spar carried away by `strain._wreck_spar` at minute ten, three hours; in 12 knots, 25,
12 with the wind heading her four points at +30 minutes, and 20 rising to 38 over +30 to +60; the
bilander (fore topmast), the merchant brig (main topmast), a topsail schooner (fore topmast) and the
frigate (main topmast) beside the three of truth 7-779 (the cutter's main topmast, the brig's, the
74's fore topmast); seeds 7, 8 and 9 (`tests/test_mends_126.py`, `_spar_passage`).

**The trunk in this tree.** The trunk's captain is run in this tree with the spar's work, the
bring-to given again and the narrowed `lie a-try` test patched out. Against the trunk itself
(f09fe283, the same code as the trunk now) it is **the same in every line and end position on all
84 cell-seeds**, on this hash's code (and on the pass's before it). `test_truth_7_779_b_the_trunk_
in_this_tree_is_the_trunk` holds one of its cells to the trunk's figures.

**What was found: a wreck left hanging helps some hulls** (the carried list, fault 22). A wrecked
sail gives no drive, but its windage and its spars' count three times over
(`physics.sails._sail_windage_area`, `_spar_windage_area`, `WRECK_MULTIPLIER`), and the wreck does
her no harm: a topmast's wreck forward pays her off like a head sail. With the wreck cleared at the
moment it fell (no hands and no time spent: its sails to the sail room, its spars sent down), the
trunk's own captain does worse in some cells than with it left hanging, by much (the 74 in 25 knots
on seed 7: 1.88 miles made good, aback twenty times, against 6.51 and nine). No captain who clears
the wreck can meet "not less than the trunk's" there. **The lead's ruling** (2026-11-27): the
captain does not leave a wreck hanging because it serves her; nothing of the physics is changed; the
truth is measured cell by cell against the trunk where clearing at once is no loss, and against the
wreck cleared at once where it is; the windage is carried for the ships' session and a later physics
package.

**The truth** (`test_truth_7_779_b_her_spar_carried_away_she_does_no_worse_than_the_trunk_on_
passage`, slow, one test a cell). Each cell is judged on its three seeds together, by their
medians: way made good toward Falmouth (miles), minutes going astern, times taken aback. The margin
of each is half the trunk's own seed-to-seed range in that cell, never under three cables, five
minutes and one time aback (JUDGEMENT, grounded at `PASSAGE_FLOORS`). The yardstick is the wreck
cleared at once wherever that is itself worse than the trunk beyond the margin in any of the three,
else the trunk. And on every seed on which the trunk's captain lies a-try or heaves to in the gale,
this one does: no exception.

Medians of seeds 7, 8 and 9, made good (nm) / minutes astern / times aback:

| Ship | Wind | Yardstick | Trunk | Wreck cleared at once | This hash | Margin |
|---|---|---|---|---|---|---|
| bilander | 12 kn | **the wreck cleared at once** | 9.94 / 0 / 0 | 8.68 / 22 / 1 | 10.20 / 0 / 0 | 0.73 / 5 / 1 |
| bilander | 25 kn | **the wreck cleared at once** | 9.26 / 29 / 2 | 5.00 / 58 / 5 | 15.86 / 0 / 0 | 5.89 / 44 / 2 |
| bilander | 12 kn, heading her | **the wreck cleared at once** | 5.64 / 0 / 0 | -1.10 / 170 / 2 | 5.77 / 0 / 0 | 1.64 / 38 / 1 |
| bilander | 20 rising to 38 | **the wreck cleared at once** | 11.87 / 0 / 1 | 0.56 / 160 / 1 | 11.87 / 0 / 1 | 2.71 / 10 / 1 |
| merchant brig | 12 kn | the trunk | 9.34 / 5 / 1 | 11.34 / 0 / 0 | 9.99 / 5 / 1 | 0.30 / 5 / 1 |
| merchant brig | 25 kn | the trunk | 10.44 / 6 / 1 | 16.16 / 0 / 2 | 10.66 / 6 / 1 | 7.21 / 8 / 5 |
| merchant brig | 12 kn, heading her | the trunk | 4.73 / 15 / 1 | 5.97 / 0 / 0 | 5.25 / 15 / 1 | 0.82 / 10 / 1 |
| merchant brig | 20 rising to 38 | the trunk | -5.51 / 28 / 1 | 9.95 / 0 / 0 | -5.51 / 28 / 1 | 4.33 / 10 / 1 |
| topsail schooner | 12 kn | the trunk | 13.44 / 1 / 0 | 14.25 / 1 / 0 | 14.78 / 1 / 0 | 2.26 / 5 / 1 |
| topsail schooner | 25 kn | the trunk | 27.45 / 5 / 0 | 27.71 / 5 / 0 | 27.73 / 5 / 0 | 2.60 / 5 / 1 |
| topsail schooner | 12 kn, heading her | the trunk | 8.23 / 22 / 1 | 10.09 / 1 / 0 | 9.42 / 1 / 0 | 1.72 / 18 / 2 |
| topsail schooner | 20 rising to 38 | the trunk | 27.99 / 3 / 0 | 28.70 / 3 / 0 | 29.51 / 3 / 0 | 1.39 / 5 / 1 |
| frigate | 12 kn | the trunk | 9.96 / 0 / 0 | 12.42 / 0 / 0 | 12.29 / 0 / 0 | 0.32 / 5 / 1 |
| frigate | 25 kn | the trunk | 7.69 / 3 / 0 | 14.48 / 1 / 1 | 10.02 / 3 / 0 | 11.82 / 10 / 4 |
| frigate | 12 kn, heading her | the trunk | 4.33 / 9 / 2 | 7.91 / 0 / 0 | 7.48 / 0 / 0 | 0.85 / 5 / 1 |
| frigate | 20 rising to 38 | the trunk | 13.43 / 18 / 1 | 21.70 / 0 / 0 | 22.27 / 8 / 1 | 2.71 / 5 / 1 |
| cutter | 12 kn | the trunk | 0.17 / 175 / 1 | 0.65 / 174 / 2 | 0.66 / 175 / 1 | 0.30 / 5 / 1 |
| cutter | 25 kn | the trunk | 7.85 / 122 / 1 | 22.90 / 0 / 0 | 22.74 / 0 / 0 | 9.15 / 76 / 1 |
| cutter | 12 kn, heading her | the trunk | -1.37 / 172 / 3 | -0.72 / 174 / 2 | -0.86 / 175 / 1 | 0.30 / 5 / 2 |
| cutter | 20 rising to 38 | the trunk | 0.98 / 177 / 1 | 0.88 / 177 / 1 | 0.93 / 177 / 1 | 0.30 / 5 / 1 |
| brig | 12 kn | the trunk | 11.72 / 0 / 0 | 13.03 / 0 / 0 | 13.24 / 0 / 0 | 0.53 / 5 / 1 |
| brig | 25 kn | the trunk | 26.30 / 0 / 0 | 27.02 / 0 / 0 | 26.74 / 0 / 0 | 2.23 / 5 / 1 |
| brig | 12 kn, heading her | the trunk | 7.07 / 5 / 1 | 9.01 / 0 / 0 | 8.34 / 0 / 0 | 0.30 / 5 / 1 |
| brig | 20 rising to 38 | the trunk | 16.84 / 0 / 0 | 14.60 / 0 / 0 | 14.12 / 0 / 0 | 3.46 / 5 / 1 |
| 74 | 12 kn | the trunk | 8.10 / 0 / 0 | 9.25 / 0 / 0 | 10.98 / 0 / 0 | 0.65 / 5 / 1 |
| 74 | 25 kn | **the wreck cleared at once** | 24.90 / 8 / 1 | 1.88 / 111 / 20 | 25.68 / 8 / 1 | 9.50 / 48 / 4 |
| 74 | 12 kn, heading her | **the wreck cleared at once** | 0.62 / 136 / 2 | 0.56 / 143 / 2 | 0.41 / 144 / 2 | 0.38 / 5 / 1 |
| 74 | 20 rising to 38 | **the wreck cleared at once** | 13.03 / 43 / 0 | 11.16 / 92 / 0 | 10.62 / 91 / 1 | 2.16 / 17 / 1 |

**No cell fails.** The wreck cleared at once is the yardstick in seven: the bilander in every wind
(cleared, she goes astern in 12 knots and with the wind heading her, the hanging fore topmast having
kept her head off) and the 74 in three; and in each of the seven, **the windage is the cause**: a
wreck forward on a hull that gripes without it. They are declared for the ships' session in
`docs/dev/TuningNotes.md` in the same words. In the rest the trunk is the yardstick and this hash
is level or better, most by miles (the cutter in 25 knots 22.7 against 7.9; the bilander in 25
knots 15.9 against 9.3; the frigate in the rising wind 22.3 against 13.4).

- **The frigate in 25 knots**, seed 7 (the lead's case: -0.84 miles against the trunk's 4.23 on the
  pass he read): its log there was the trunk's to the minute until the clearing lowered the wreck's
  sails to the sail room at 2995 s, taking off their windage; from there her times aback and her
  wears drifted by seconds and her track parted. On this hash, where the clearing yields to her
  braces and the lead and goes on with the hands up, **she makes no less on any seed**: 4.65, 28.42
  and 10.02 miles against the trunk's 4.23, 27.86 and 7.69 (seed 7: 15 minutes astern against 19,
  aback eleven times against eight; the cell's medians 3 minutes and none, as the trunk's). The
  cell's margin, 11.8 miles, is the trunk's own spread in that wind (4.2 to 27.9 over three seeds):
  the measure of what one seed is worth there.
- **The three small ones** of the pass before (the bilander and the cutter a few minutes more
  astern with the wind heading her, the 74 a few cables less): on three seeds the bilander's is
  level with the trunk and its yardstick is the wreck cleared at once; the cutter's is three
  minutes astern more than the trunk's median, inside five, and better in way and aback; the 74's
  yardstick is the wreck cleared at once, which it matches.
- **The second pass's fault the reader found** (the bilander in the rising wind, 1.56 miles made
  good and ninety minutes astern): she now makes the trunk's 8.90, 11.87 and 14.32 on the three
  seeds, the clearing belayed by her shortening and her braces and taken up between them. Where the
  yardstick is the wreck cleared at once, as there, the truth would pass a captain as bad as the
  second pass's; the function's truths (7-777: no spar's order while work waits, in a manoeuvre,
  under fire, struck, in action; the belays of `_spar_work_gives_way`) are what pin the last claim
  there.

## 10. The wreck's order pinned (item 3)

The reader's mutant M03 (`rank` turned so that a light spar's wreck sorts first) survived the slow
tier: a light wreck first, with work in hand, returned None and held up the working wreck. Truth
7-777 b pins it at the function: the brig with a studding-sail boom's wreck beside her fore
topmast's clears the fore topmast's first with work in hand and with none, and the boom's only
after it and only with nothing in hand. M03 fails it (the fast tier).

## 11. The differences on today's ships

**Today's ships, old beside new** (this hash's code beside the trunk at f09fe283; the same
harness as part one's §5): every ship file (the thirteen ships and the five boats) in four cases at
seed 7 under the game's own captain (a gale abeam and a gale close-hauled bound for Falmouth from
48 40 N 5 05 W, the wind rising from 20 to 35 knots over an hour; a cruise off the Lizard, 12 knots,
three hours; the June passage off Falmouth under a high, six hours), the whole log and the end state
compared.

| Case | Same in every line and the end state | Differs |
|---|---|---|
| gale abeam | 12 of 18 | the five boats, the smack |
| gale close-hauled | 12 of 18 | the five boats, the smack |
| cruise | 18 of 18 | none |
| June off Falmouth | 18 of 18 | none |

- **The five boats in the two gales:** one line more, "Captain's rule 'hove to for weather': order
  not carried out ('lie a-try'): She has no topsail to lie a-try under.", ten minutes after the
  first (§8); every other line and the end state the trunk's.
- **The smack in the two gales:** "By the captain, hove to for weather: heaving to (no topsail set
  to lie a-try under)." where the trunk's `lie a-try` was refused ("The topsail is not set; set it to
  lie a-try under it.") and she sailed on; she lies to under her fore-and-aft canvas, at 0.9 knots
  abeam and 0.3 knots astern close-hauled at the third hour, where the trunk's ran on at 8.6 knots,
  and ends 13 miles (abeam) and 15 (close-hauled) from where the trunk's did. The lines that follow
  (the heave-to's, all hands called and piped down, her leeway, her strain warnings fewer) are its.
- **No spar carried away** in any of the 72 runs, so the spar's work is in none of them; the
  probe's 84 cell-seeds and the gale from the start (§8, §9) are where it is measured.

***The first action*, left to the game's own captains** (four hours from its start at seed 7, no
seat): **the same**, line for line (633 lines in the Sherbourne's log on both). The Renard's main
topgallant mast is not carried away by then on this seed in either; her captain's work on it is
truth 7-777's (§7).

**What a player or a model's seat is served that differs** (every such line, by kind): the
captain's spar orders and their reasons (§7: "clearing away the wreck of the ...", "shifting the
...", "bending the ...", "setting the ... (bent again to its spar)", "setting the fore staysail (to
keep her head off, her head sails gone)", "calling all hands (to clear away the wreck of the ...)",
"piping down (the wreck cleared away)"); the runner's belay of a spar's work for her working
("Belayed clearing away the wreck of the fore topmast: hands to brace the fore yard."); the
smack's heave-to for the weather (§8); a bringing-to given again, "(not brought to)", and its
refusals, once more than on the trunk where nothing will make it good. Nothing else moved.

## 12. The pins moved

**No pin moved.** The truths changed in their bodies are the package's own: 7-777 gains the wait
(an order waiting for hands has them first: nothing; none waiting, the wreck) and its under-command
cell clears the waiting work first, as the new gate asks; 7-777 b and 7-779 b are new; 7-779 is as
it was. New JUDGEMENT figures, each grounded where it is defined: `BRING_TO_AGAIN_S` (600 s),
`WRECK_HANDS_UP_S` (3600 s), `PASSAGE_FLOORS` (0.3 nm, 5 min, 1). `docs/dev/TuningNotes.md`,
"Package 126, part two", has them beside the trunk's figures.

## 13. Found and not mended, and what this pass could not do

- **A wreck left hanging helps some hulls** (§9; the carried list, fault 22): the physics', for the
  ships' session; nothing of it touched.
- **The bilander in 25 knots** (§7): on seed 7 she is never under command with hands free in three
  hours, and her wreck waits for her to be; on seeds 8 and 9 all hands are turned up for it at the
  hour and the clearing is begun, belayed in turn by her braces and taken up between them, and not
  done by the third hour.
- **The rising wind's clearing** on the bilander and the merchant brig is in hand at the third hour,
  belayed in turn by her braces and the lead, not done (§7).
- **The smack's heave-to undone by the captain's own take-in** of her straining foresail (§8): the
  trunk's standing work; her `heave to` is then refused for want of a head sail, and he does not set
  one for it. Left as found.
- **A stand-down's save naming** (part one's §6; the carried list, item 21): as it was.
