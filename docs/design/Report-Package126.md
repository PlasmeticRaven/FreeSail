# Report: package 126, the harbour, the weather and the captain

**The brief.** `docs/dev/briefs/Brief-Package126.md`: four parts, three of them the owner's notes
2, 3 and 4 from his play of gate M7 (`docs/playtests/2026-11-24-gate-m7-owner-runs/README.md`), the
fourth item 12 of section 4 of `docs/dev/CarriedForward-M7.md`, with item 6 of the same list beside
the first. The branch is `claude/pkg-126`, cut from the trunk at 112ff819. New truths are 7-770 to
7-778.

## 1. A game ended from the harbour (the owner's note 2), and the stations' table

**As it was.** `Harbour.start` (`freesail/ui/harbour.py`) takes a new World up in place of the old
through the driver's `replace_world`; nothing ended a game. The stations' table of the page
(`client/harbour.js`, `fillStations`) kept each row's choice of door and model by the row's key
(`station|ship`) whenever it was drawn again, so a game begun after another was offered the last
game's choices.

**As built.**

- `Harbour.end(lose_unsaved)` and `POST /api/harbour/end`. Every door the harbour started that is
  still running is closed by `stop_door`, as the harbour closes one: its own Ctrl-C, the station
  released at the game as before. The locks are not held while the doors stop, because a stopping
  door asks the game to release its station. Then, under the harbour's lock and then the driver's
  (the start's order), the World is let go for one with no game in it, as `py -m freesail` begins:
  the driver's `replace_world` stops the clock, stops hearing the old log and tells the pages to
  start again. The harbour's words of the game are emptied, `started` is false and the director's
  seats' doors are forgotten. Nothing saved is touched. The game page's `/` leads to the harbour
  again, as it does before any game, and another game is begun from the same server.
- **What is not saved is lost only on the player's word.** The driver keeps what of the game a
  save holds (`Driver.kept`: the World, its tick and its log's length after the last save's line,
  or as it was taken up, and the ship's time of that save). `Driver.unsaved()` gives the words
  when anything has passed since. While it does, the end is refused with them ("This game has not
  been saved; what has passed in it, to <time>, is lost if it is ended. End it all the same, or
  save it first.", or "This game was last saved at <time>; ..."). The page then shows "end it,
  losing what is not saved", and only that sends `lose_unsaved`. A game taken up and not played,
  or saved and not played since, ends at once.
- **The page.** "end the game" sits under the game in play, at the head of every tab (the "In
  play" panel), shown while a game is in play. Its words go under it.
- **The stations' table** keeps a row's choice only while it is drawn again for the same game. The
  state carries `games`, the count of games begun and ended from this harbour, and a game begun
  after another draws its rows as its own scenario gives them. `Harbour.stations()` lists nothing
  while no game is in play.

**Truths.** 7-770 (the end, the refusal and its words, a save untouched, a game begun after,
`tests/test_harbour.py`); 7-771 (a page that asks at every line of the end finds the whole game or
none, never the one beside the other; the start's probe, applied to the end); 7-772 (in the
browser, by the page's road: the planned door and a door chosen by hand, a next game offered its own
stations, the end refused on its words and taken at "end it, losing what is not saved", a game begun
after offered its own); 7-773 (a live server: the API door seated at the watcher's station is closed
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

**The lines** (`World._tick_weather`, `weather.FOG_LINES`): "A fog is settling in." as it first
settles (the weather's change to fog, notable as "Fog came down." was, which stays for a fog that
comes on at its full); "The fog is thickening." and "The fog has shut in thick." as the sight closes
a step and shuts in to a cable (notable); "The fog seems to be clearing." as it first opens from a
cable and "The fog is thinning." as it opens a step more (routine); "The fog lifted." as before. The
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

## 3. The game's own captain replaces a spar carried away (the owner's note 4)

**What spares a ship carries today, and where that is written.** Each ship file's
`crew.stores.spare_spars`, by class, read by `ship/parts.py` `booms` (the `Booms` store; a shift
takes one of its class):

| Ship file | Spare spars |
|---|---|
| frigate-36, razee-44, seventy-four, sixty-four | 2 topmasts, 2 stump topgallant masts, 2 topsail yards, 4 topmast studding-sail booms, 1 jib-boom (and the frigate a flying jib-boom); Luce 1866, the pairs judgement |
| brig, hermaphrodite brig | 1 topmast, 1 stump topgallant mast, 1 topsail yard, 2 studding-sail booms, 1 jib-boom (judgement after Luce 1866; the brig's topmast Chapelle after Fincham) |
| privateer schooner, topsail schooner | 1 topmast, 1 topsail yard, 2 studding-sail booms (judgement after Chapelle and Luce 1866) |
| merchant brig | 1 topmast, 1 topsail yard (judgement) |
| cutter | 1 topmast, 1 topsail yard (judgement after Luce 1866) |
| lugger | 1 lug yard, 1 topmast (judgement) |
| bilander, smack | 1 topsail yard (judgement) |
| the five boats | none |

The *Renard* of *the first action* is a cutter (`data/ships/cutter.yaml`, fit "long guns"). **She
carries no spare topgallant mast**, so in the owner's case the topgallant mast is left as it is, and
its yard, which went with it and stands on it, waits for it. What changes in his case is that her
people now clear the wreck (it hung to leeward for three hours in his save). The clearing's own line
says "There is no spare topgallant mast aboard."

**As it was.** The captain's repairs (`Captain._repairs`, `world/captains.py`) gave, one order every
ten minutes in the doctrine's `damage_priority`: the shot holes plugged, the standing rigging set
up, and out of action the running rigging rove and a sprung spar fished, then the wheel. Nothing
cleared a wreck or shifted a spar carried away, though the work is there for a player
(`clear_wreck.yaml`, `shift_spar.yaml`, `jury_mast.yaml`).

**As built.** `Captain._spar_work`, last after every other repair. It is given only out of action
(not engaging), never under fire (no shot come aboard within `SPAR_WORK_QUIET_S`, ten minutes,
JUDGEMENT, the repairs' own interval), and only with hands to spare: no repair and no all-hands
work in hand (`SPAR_WORK_BUSY`). The repairs' own rules stand before it (not lying to for weather,
not in distress, the wind under the shortening figure). In turn:

1. **The wreck cleared** ("clear away the wreck of the <spar>"), the spar and every spar that went
   with it. A hanging wreck drags and tears the sails. The sails it took, that were bent, are
   remembered to bend again.
2. **Each spar cleared that stands on what stands, shifted for a spare of its class** ("shift the
   <spar>"), or **a lower mast stepped again as a jury mast** from a spare topmast ("rig a jury
   mast"). The order is `SPAR_MEND_ORDER`, what keeps her manageable first: the bowsprit, the lower
   masts, the jib-boom, the topmasts, the gaff and the boom, the yards (the lowest first), then the
   topgallant masts, the flying jib-boom, the royal masts and the studding-sail booms (JUDGEMENT,
   after Luce 1884, ch. XXXI). A spar she has no spare for is left as it is.
3. **The sails bent again**: a head sail as soon as its spar stands, before any other spar is
   shifted (it keeps her manageable), and the rest when all are shifted.

Each order says why, in his words: "By the captain, keeping station: shifting the main topmast (the
main topmast carried away)."

**Truths.** 7-776 (the cutter's main topmast: the wreck, the topmast, the jib, the topsail yard, the
topsail, the gaff topsail; the topgallant mast left for want of a spare); 7-777 (the Renard's own
case, the wreck cleared and nothing shifted; none within ten minutes of a shot, none with a plug in
hand, none engaging; the wreck when quiet).

## 4. `lie a-try` with the wind abeam, under the game's own captain (item 12)

**Reproduced on the ships in the game.** Every committed ship of the player's own was taken through
the same probe: bound for Falmouth from 48 40 N 5 05 W, seed 7, the wind from the west (abeam) and
again from the north-east (nearer the wind), rising from 20 to 35 knots between 04:30 and 05:30 and
held to 08:00, under the game's own captain.

- **The smack: not taken.** At the gale's line the captain orders `lie a-try`. It is refused ("The
  topsail is not set; set it to lie a-try under it."): her topsail is furled under her plain sail
  (item 8 of the same list). He orders nothing in its place, and she sails on at seven to nine knots
  through the two hours of the gale, abeam and close-hauled alike. This is the captain's to mend.
- **Every other ship lies a-try, late.** The order waits behind the shortening's reefs: the
  frigate and the 74, 64 and razee 17 to 20 minutes, the cutter 17, the schooners 20, the brig 44, the
  merchant brig 90 and the bilander 107 (close-hauled). Meanwhile she sails on at 8 to 11 knots. The
  same holds close-hauled as abeam, so "abeam" is not what keeps it waiting on these ships. This is
  the order in which sail is shortened before she is brought to, which is package 125's (how ships
  shorten sail). It is reported, not mended here (§6).

**As built.** On entering "hove to for weather" the captain reads the order's own refusals first
(`Captain._topsail_to_lie_under`). With no topsail set to lie a-try under, he heaves to under the
canvas she has, as a fore-and-aft vessel lies to ("By the captain, hove to for weather: heaving to
(no topsail set to lie a-try under)."). The smack is hove to ten minutes after the line, abeam and
close-hauled, and drifts at under two knots. A ship with her topsail set lies a-try as before.

**Truth.** 7-778.

## 5. The pins moved, the differences served, and the tiers

(Filled in at the build's hash: §5 of the build report.)

## 6. Found and not mended

- `lie a-try` given after `shorten sail` waits behind every reef the shortening takes (17 to 107
  minutes by ship), and she sails on meanwhile. That is package 125's ground.
- Under the probe's gale the captain leaves "hove to for weather" for his passage once the wind's
  mean stands under `gale_over_kn` ten minutes. He is then refused his course ("She is hove to;
  fill away before giving her a course.") every minute until the lie a-try he ordered is done, and
  then fills away from it. This is the doctrine's band, and the `fill away` twice of package 122.
- The sails bent again after a shift are furled. Whether they are set is the captain's sail
  work, as after any bending.
