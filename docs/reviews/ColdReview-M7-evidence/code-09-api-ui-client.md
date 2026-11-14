# Code reader 09: what the player sees and touches (freesail/api, freesail/ui, client)

Commit 504a25066c6995ce9829a19ffc597feb510a1870. Read under READERS.md and CODEREADERS.md.
Nothing under docs/dev, docs/design, docs/playtests or docs/gates was opened. No test suite
was run. The only file written is this one (and a two-line scratch file outside the tree,
for one demonstration below). Short Python commands were run to import modules and call
single functions; each is quoted where it bears.

## 1. What it is

Size: freesail/api 12 files, 8,752 lines (readings.py 4,865; queries.py 768;
action_readings.py 717; viewer_guns.py 514; damage_readings.py 430; practice_readings.py 334;
prize_readings.py 301; squadron_readings.py 262; signal_readings.py 249; viewer_flags.py 206;
session.py 97; `__init__` 9). freesail/ui 4 files, 4,379 lines (server.py 1,887; console.py
1,255; harbour.py 1,236). client/ 13 files, 9,870 lines (projection.js 4,764; map.js 1,408;
harbour.js 875; app.js 852; library.js 463; style.css 429; harbour.html 277; instruments.js
243; units.js 113; index.html 145; shipview.js 141; log.js 135; library.html 25).

What each does, for a newcomer:

- `api/session.py` composes a world from a ship file (runner, physics stepper, order
  handler, crew). The drivers' and the replay's way in.
- `api/readings.py` is the readings registry: 118 rows (counted by importing it), 214
  events, 31 comparison kinds. Each row is an id, the words the standing-order grammar
  accepts, a getter over the World and where on the ship the reading is to be had. The
  same rows feed the standing orders, the browser snapshot and a model's `readings()`
  tool. The file also holds three other things that are not the registry: the event
  table for `at` (3100-3360), the danger lines (3420-3455), the "station's line" that opens
  every sample (3907-4091) and the director's whole truth surface (4094-4833:
  `director_readings`, `truth_ports`, `truth_grounds`, `truth_systems`, `truth_at`). The
  five companion modules (action, signal, squadron, damage, practice, prize) register more
  rows and events into the same module globals when `readings` imports them at its foot
  (4835-4865).
- `api/queries.py` builds the snapshot (`snapshot`, 221-371) a view redraws from and the
  ship graph (`ship_graph`, 556-597) a view builds the drawing from, plus the console's
  muster, sail room and booms lines.
- `api/viewer_guns.py` and `api/viewer_flags.py` place guns and ports on the drawn hull and
  say what flags fly, for the snapshot and the graph.
- `ui/server.py` is a FastAPI app around one World: a `Driver` (clock thread, lock,
  listeners, roll-up, auto-slow), the routes (`/api/state`, `/api/order`, `/api/driver`,
  `/api/log`, `/api/save`, the library, the marks, the pictures, the agents' API) and one
  websocket `/ws`.
- `ui/console.py` is the terminal driver; it also exports most of the driver vocabulary the
  server imports (server.py:136-168).
- `ui/harbour.py` is the launcher page's back end: scenarios, ships, settings, starting a
  game in place (`Driver.replace_world`), starting model "doors" as subprocesses, writing the
  desktop client's MCP file, a desktop shortcut, and the scenario maker.
- client/: `app.js` wires one websocket and POSTs; `log.js` the log pane; `instruments.js`
  the readouts; `map.js` the chart; `projection.js` builds a 3D skeleton of the ship and
  projects it; `shipview.js` draws it as SVG; `library.js` the library pane; `harbour.js`
  the launcher.

Who calls what: `freesail/__main__.py` builds `server.Driver`, `Harbour`, `create_app`;
`server.main` the same without a harbour argument; `console.main` its own `Console`.
`World.readings` hands out `ReadingsView`s (readings.py:319). 28 modules outside api/
import `api.readings`. 92 test files mention readings; the files that test this part most
directly: tests/test_server.py (831 lines, 31 tests), tests/test_harbour.py (702, 16),
tests/test_readings.py (797, 23), tests/test_view_geometry.py (7,056 lines, 139 tests,
which drives projection.js under node), tests/test_map_view.py (312). 161 test files import
something from freesail.ui or freesail.api.

What the player sees: the harbour page, then the game page: a log pane with severity marks
and an all/notable/urgent filter, an order line with completion, the ship drawn in SVG, an
instrument list, a canvas chart with pencil marks, and panes for the library, the
director's log and the director's channel.

### Against the proposal, item by item

- **Thin client.** Not thin. The log, the instruments and the library are thin: the server
  sends words and numbers and the page sets text. The ship view is not: the whole rig's 3D
  geometry is computed in JavaScript (`buildSkeleton`, projection.js:362-1975, one function
  of 1,613 lines), from the graph and the snapshot, including rules mirrored from Python:
  the square sail's cut and `CLEW_SPREAD` "from gen_ships.py" (projection.js:82-89), the
  settee's sheet lead "freesail/evolutions/trim.py, the lug's floor of 8 degrees"
  (projection.js:130-137, 465), the goose-winged sail's triangle "physics/sails.py: half the
  area" (1546), `deckAt` "freesail/ship/profile.py's `deck_at`" (2107-2138), `lineAt` ("the
  profile's `interp`", 2064), `deckSlope` (3905-3909) which Python also has as
  `viewer_guns.deck_slope` (viewer_guns.py:"as the viewer reads it ... `client/projection.js`,
  `deckSlope`"). The hull's stations and the guns' placing are projected in Python and served
  (`queries.ship_graph` -> `hull.stations`, `viewer_guns.served`); the spars, yards, sails,
  lines, flags and smoke are placed in JavaScript. So the answer to "Python, JavaScript or
  both": both, split by part, with several rules written in each. The chart is also built
  in the page (an equirectangular frame about the reckoning, map.js:813-842; strangers placed
  from bearing and estimated distance, map.js:1077-1112). `tools/python_twin.py` does not bear
  on the ship view: it is the gate 4a demonstration that a standing order in the dialect and
  its twin in Python give one log (tools/python_twin.py:1-14).
- **Views never invent state.** Mostly kept for the log and instruments. The ship view
  invents motion between snapshots: guns running out, flashes and smoke are timed in the
  page (`clockAt`, `firingsBetween`, `effects`, projection.js:4594-4672; app.js:243-289), from
  snapshot differences. That is animation, but it is state the core does not hold.
- **Log as primary view, severity, roll-up at compression.** Built, and built once: the
  server's `Driver` feeds `events.RollupView` (server.py:317, 538-551) the same view the
  console uses (console.py:548); the page shows a roll-up as a `<details>` that fetches its
  lines from `/api/log` when opened (log.js:38-81). Sound.
- **Map shows the estimated position, never the true.** On the sphere, kept: the snapshot's
  ship `x`/`y` are None when the world has a position (queries.py:265, 299-300) and the chart
  is drawn about `reckoning.lat_deg/lon_deg`. Checked by command: in
  `data/scenarios/lesson-falmouth.yaml` after 120 ticks the true position was 49.93563,
  -5.06444 and the snapshot's reckoning 49.93535, -5.06486; the true figures to four places
  did not appear in the snapshot's JSON. On the "endless plane" (a world with no position)
  the map draws the truth's metres (map.js:833-842, 1374), since no reckoning is kept there.
- **Ship view from the part graph.** Built (above); drawn from `/api/ship`, refetched when
  the followed hull changes (app.js:303-331).
- **Instrument panel.** Built (index.html:77-104, instruments.js).
- **Reference library.** Built: `/api/library`, `/api/library/topics`, `/api/library/papers`
  serve the model's own `library` tool's pages (server.py:1192-1268); library.js shows them.
- **A Sailing Master tutorial.** Not built as a tutorial. What exists is the "Sailing
  Master's Primer" as a library topic (agents/tools.py:3068) and four lesson scenarios
  (`lesson-falmouth`, `lesson-landfall`, `lesson-lee-shore`, `lesson-reckoning`) whose own
  headers say to run them from the console (lesson-falmouth.yaml:10) and whose names do not
  say they are lessons ("Pilot water, Black Head to Falmouth road").

### The harbour, and a new player's road to a ship under sail

`py -m freesail` with no game opens `/harbour` (server.py:1489-1496). The "game" tab's form
is the server's flags as controls: from (scenario, ship file, save), seed, seat, time, pace,
crewed cap and range, business, director's brief, standing orders, ease on station
(harbour.html:47-83; harbour.js:226-254; `Harbour.start` builds the flags' namespace from
`server.server_parser().parse_args([])`, harbour.py:512-588). The scenario list is every
`data/scenarios/*.yaml` sorted by path, then the player's own (harbour.py:365-370), each shown
as its `name:` and its file name (harbour.js:68-83). Today that is 47 game scenarios, among
them `gate-4c-day` ("The gate's day"), `gate-5a-day`, three `gate-5b-*` and the four lessons.
Nothing in the harbour's code, the page or the scenario entry marks a scenario as a
beginner's, a lesson's or a test's: the entry is `{path, name, own}` and the only tag added to
a name is ", keeping to the course of history" (harbour.py:399-418). Grep of freesail/ and
client/ for tutorial, beginner, first game finds nothing in either (the lesson word appears
only in unrelated modules). After "start", a button leads to the game page; the clock is held
(`--time` default and the replaced World held, harbour.py:574-577; server.py:866-867), the
book of standing orders is empty and the first driver line says how to load the starter book
(console.py:159-170, server.py:1839-1842). A player must know to press "go". The game page's
order line placeholder lists `world: ...` and `the director's log` beside `hold / go`
(index.html:45).

## 2. Is it reached?

Reached in play: every route in `create_app` and `harbour_routes`; the readings rows through
the snapshot, the standing orders and the samples; `console.main` as the terminal game.

Reached by tests and attackers only:

- The websocket's receive path (server.py:1666-1690: `order` and `driver` messages). The
  client never sends on the socket (grep `ws.send` in client/*.js: none; orders go by
  `post("/api/order")`, app.js:593). The only caller is tests/test_server.py:313. It is a
  second order door kept alive for no player, and it is the open one (section 5).
- Snapshot fields nobody reads: each sail's `thrust`, `side`, `area_effective` and the wind's
  `mean_speed` (queries.py:240, 328-330) are sent every snapshot (every tick at 1x) and no
  client file reads them (grep in client/*.js: no hit for thrust, area_effective,
  mean_speed). Dead data on the wire.
- `Harbour.chart`'s default region `channel-west` and `Harbour.ports`' hard-coded
  `load_chart("atlantic-east")` (harbour.py:438, 1233): every port is placed on one chart.
- `session.ship_factory` is reached only by replay and the console's `replay`.
- `api_director_log` (server.py:1537-1546) is a GET with a side effect ("the director is
  told of it"); the page never calls it (it asks by the order line,
  server.py:704-709).

Parameters always passed the same: `Driver.__init__` `free_running` from flags only;
`agent_routes`' `desk_options` are four keys from two callers.

## 3. Built more than once

1. **Two drivers.** `ui/console.Console` and `ui/server.Driver` each implement the clock
   thread (`_clock_thread`, `_tick_owed`: console.py:861-914, server.py:813-838), the
   auto-slow (`_ease`, console.py:575-588, server.py:459-475), the log-follow
   (`_follow_log`, console.py:497-506, server.py:395-404), `hears` (console.py:551-561,
   server.py:320-326), `held_for` (console.py:841-846, server.py:406-411), `state`, `muster`,
   sail room, booms, the director's words, `save` and `read the standing orders`. They differ
   today: the console's `save` takes `args[0]` (a path with spaces is cut,
   console.py:722) and catches no OSError (`save /nonexistent/dir/x.json` raised
   FileNotFoundError out of `handle_line`, run by command); the server's joins the words and
   refuses in words (server.py:218-224, 746-773). The console's `two stories x` raises
   ValueError (console.py:708, run by command: "invalid literal for int()"); the server's
   tests `isdigit()` (server.py:713-715). The console has `help`, `log N`, `replay`; in the
   browser `help` and `log 5` become rejected orders written to the log (run by command:
   `order.rejected`). `--ease-on-station` is the server's alone. Joining them: one driver
   class with two front ends.
2. **Two order doors on the server**: `/api/order` (HTTP) and `/ws` `order` messages, the
   second unused by the client (above).
3. **Rig geometry in JavaScript and in Python** (section 1): the physics computes sail
   chords, luffs and centres in Python (readings.py:927-948 reads `sails_mod._chord_angle`);
   the drawing computes sail corners, yard hoists and swings in JS. Port slopes exist in both
   (`deck_slope`, `deckSlope`). A change to a rule in trim.py or profile.py has no link to the
   JS copy but a comment.
4. **Constants and rules mirrored in the client**: fatigue words (instruments.js:236-240
   against crew/model.py:85-86, equal today), the points of sail (instruments.js:13-21
   against units.py:347-362; the JS does not wrap the angle first), wind strength words
   (units.js:64-79 against units.py:434-460, equal today), `KEPT_ACTORS` (log.js:12 against
   events.py:164; the server also sends `kept`), the lookout's estimate doubt (map.js:1074,
   0.15, whose comment says "a sixth"; the Python constant is 0.15, lookout.py:162), part
   names (`U.partName` replaces dots and underscores, units.js:86-88, where Python uses
   `orders.resolve.display_name`).
5. **Two ways to say a gust**: the registry's `true_wind_against_mean` (readings.py:424-429)
   and the snapshot's raw `gust_factor`, which instruments.js:34 turns into ", gusting" above
   1.05. The snapshot's docstring says the instrument values "come through the readings
   registry" (queries.py:224-227); `mean_speed`, `gust_factor`, `squall`, `weather_helm`,
   `tack`, `helm_mode`, `target_heading` do not (queries.py:237-243, 305-309).
6. **Inside the readings package**: `_damage` and `_parted_lines` compute the parted lines
   twice (action_readings.py:249-298 and 349-376); `_and` (action_readings.py) and
   `_and_words` (readings.py:2518); `_no_guns_words` in action_readings and
   practice_readings; the `colours` row registered by action_readings and then replaced by
   signal_readings (signal_readings.register; readings.py:4841-4842 says so). Events are
   added two ways: `R._event(...)` (prize_readings, which also fills `_WATCHED`) and
   `R.EVENTS[...] = ` (the other five modules), which skips `_WATCHED`.
7. **Two hidings of the player's knowledge**: the server's `knowledge_block` lists the rows
   not to be had (queries.py:200-218) but the snapshot still carries their values; the page
   then greys some readouts (instruments.js:94-128). The map and the ship view read no
   knowledge at all (grep of map.js and shipview.js for knowledge: none).

## 4. Size and shape as a hazard

Longest functions (lines, by `ast`): `readings.director_readings` 248 (4260);
`server.create_app` 240 (1424); `damage_readings.register` 170; `action_readings.register`
160; `console.Console._handle_line` 156 (an if/elif chain of about thirty branches);
`queries.snapshot` 151; `console.main` 121; `harbour_routes` 119; `signal_readings.register`
99; `action_readings._damage` 98. In the client: `Projection.buildSkeleton` 1,613 lines, one
closure holding dozens of inner functions; `formHullFigures` about 238.

Imports inside functions: 209 across the 16 Python files (readings.py 66, server.py 32,
console.py 31, harbour.py 27, action_readings 14, prize_readings 12). Many dodge cycles:
`queries` imports `viewer_flags`, which imports `queries` inside `dressed`
(viewer_flags.py:186); `readings` imports its companions at its foot, which import
`readings` (readings.py:4837-4865), and `api/__init__.py` exists only to force that order
(api/__init__.py:3-9: "found by package 81 ... tests/test_filling.py ... imports
`action_readings` before anything has loaded `readings`").

Global mutable state: `REGISTRY`, `EVENTS`, `_WATCHED`, `KINDS` (mutated after definition by
every companion and by readings.py itself, 1632, 3725), `DANGER_LINES` rebound
(readings.py:3632); `Harbour._names`, a class-level cache shared by every Harbour
(harbour.py:397); `functools.lru_cache` on `_pricked` (readings.py:1830).

Comments: by count, comment and docstring lines are 14% of readings.py, 19% of server.py,
20% of console.py; lines naming a package number: readings.py 126, server.py 82,
console.py 52, queries.py 28. Many comments carry history ("the owner's finding of
2026-10-18", "package 37d", "the cold review of 2026-10-22, R-20") in place of what the code
does; a newcomer reading server.py is told why a line came to be more often than what it is
for. Helped in places (each constant's reason); drowned in the readings and the drivers.

Shape hazards:

- `readings.py` mixes the registry the player's standing orders use with the director's
  truth (4094-4833). The module docstring says "Nothing the three consumers see comes from
  anywhere else" (readings.py:4-9); the truth sits in the same file, guarded only by who
  calls it (agents/tools.py:548-561, agents/seat.py:485).
- `_truth_weather` moves every weather system four hours on, reads, and moves them back in a
  `finally` (readings.py:4702-4724): a read that writes the world, safe only while the
  caller holds the lock and nothing it calls raises past the restore.
- `_lookout_station` scans the whole log backwards on every read for the last hail
  (readings.py:3648-3651): cost grows with the voyage.
- `viewer_flags.dressed` builds the full `queries.ship_graph` (hull stations, every gun's
  placing) on every snapshot while she is dressed (viewer_flags.py:197-205).
- `Driver.emit_snapshot` builds a snapshot at its interval whether or not any page is
  listening (server.py:421-423, 810-811).
- The websocket handler takes the World's lock on the event loop's own thread
  (server.py:1622-1631, and `driver.hold()`/`go()`/`set_compression` at 1679-1684 are called
  without `to_thread`), so a long tick batch under the clock thread's lock stalls every
  socket and async route. Each socket's queue is unbounded (server.py:1617).

## 5. Correctness and honesty

**Security of the server.**

- Binding: `--host` defaults to 127.0.0.1 (server.py:1744); `py -m freesail` takes the host
  from the settings, `server.host` (\_\_main\_\_.py:65), and anticipates 0.0.0.0
  (\_\_main\_\_.py:126). No authentication on any route of the player's (the agents' routes
  carry a seating key, server.py:1076-1079). No CORS middleware, no Origin check and no Host
  check anywhere (grep for origin, CORSMiddleware, TrustedHost in freesail/ and client/: none
  in the server).
- **The websocket accepts any origin, and it drives the game.** `ws()` calls
  `websocket.accept()` with no check (server.py:1613-1615), sends the full hello (ship graph,
  snapshot, last 500 lines) and takes `order` messages into `driver.submit`. A browser does
  not apply the same-origin rule to websockets, so any web page open in another tab can
  connect to ws://localhost:8000/ws, read every line and drive the ship. Shown by command
  with FastAPI's TestClient: a connection with `Origin: http://evil.example` received the
  hello and its orders were obeyed.
- **Any file the user can read can be read out through it.** `driver.submit` takes `read the
  standing orders from FILE` with any path (server.py:569-573, console.py:129-151); each line
  of the file is submitted as an order, and a refused order's line echoes the text. Shown by
  command: a file holding `SECRET_TOKEN=abc123` came back over the foreign-origin socket as
  "Order not carried out ('SECRET_TOKEN=abc123'): ...". The lines are also journaled into the
  save.
- **Any path the user can write can be written.** `save PATH` at the order line, and so over
  the socket, writes the save JSON and a gzip-pickle checkpoint beside it at any path
  (server.py:574-577, 746-773; core/replay.py:68-81). The content is the game's, not the
  attacker's, but it overwrites whatever is there.
- HTTP JSON routes are protected by the browser's preflight: FastAPI 0.162.7 here refuses a
  `text/plain` body for a dict parameter (shown by command: 422). Body-less POSTs are not:
  `POST /api/harbour/doors/{id}/stop` is a simple request any page can send (it answered 404
  to an unknown id, by command, so it is processed). GETs with effects: `/api/director/log`
  records a reveal.
- Without a Host check the HTTP API is open to DNS rebinding (a suspicion of exploitability,
  not shown). What it would reach: `POST /api/harbour/settings` saves any settings, including
  `doors.desktop.command` (settings.py:522), and `POST /api/harbour/desktop` with `write:
  true` writes that command into the desktop client's MCP file, which the client runs
  (harbour.py:680-718); `POST /api/harbour/shortcut` writes an executable script
  (harbour.py:720-733); `POST /api/harbour/doors` starts subprocesses with flags from the
  settings (harbour.py:735-822); `POST /api/harbour/start` with `load` takes up any path's save
  and its checkpoint, which is unpickled by a restricted unpickler (core/replay.py:491-501,
  536-542; not my part, not read further).
- Paths from a request: the harbour's scenario reader confines `path` to the game's and the
  player's scenario folders (harbour.py:955-971); `save_scenario` cleans the name to letters,
  figures, dashes and underscores (harbour.py:1069) and refuses a place inside the repository
  (1073). The order line's `save` and `read the standing orders from` are not confined at all.
- YAML: every load in my part is `yaml.safe_load` (harbour.py:377, 411); grep of freesail/ and
  tools/ for `yaml.load(` without safe: none.

**Disconnect and two browsers.** A disconnect is handled: the receiver puts `closed` on the
queue, the sender stops, the listener is removed (server.py:1636-1646, 1687-1690); the page
reconnects every two seconds and rebuilds from the hello (app.js:372-395). Two or more
browsers can attach: each socket is one more listener (server.py:1631), every page gets every
message, any page can hold, go or change speed, marks are shared, a picture request goes to
all and the first to answer is taken (server.py:929-1010). Nothing says who is who. A malformed
driver message (`float("x")`) ends that socket's receiver and so its connection
(server.py:1684, 1687).

**The player's knowledge leaks to the page.** With the captain sent below (`go below`) in
lesson-falmouth, the snapshot's `knowledge.hidden` listed the true wind, the apparent wind,
the course, the speed, the leeway, the helm, the sky, the sea, the in-sight rows; the same
snapshot still carried the speed (1.40 m/s), all 38 sails and their states (shown by command).
The page greys a subset of readouts (instruments.js:94-128) but the values are in the browser,
and the chart still draws other sail (`snap.strangers`) and the ship view still draws the sails.
The decision that "the player reads by his place as a model does" (server.py:315) is kept in the
log and not in the snapshot.

**Truth reaching the player and the models through the registry** (the registry is a model's
`readings()` too):

- `the range` and `the enemy` fall back to the truth's range when the lookout has no estimate
  (action_readings.py:470-484: "else by the truth (a ship without a lookout aloft)").
- `the prize` gives each prize's true bearing and distance up to twenty miles
  (prize_readings `_where_words`: `bearing_and_distance(world.position, v.position)`), where its
  docstring says "where she lies by the lookout".
- `the heading` is described as "her head by the compass" (readings.py:1112-1123) and returns the
  true heading (`world.ship.heading`, 471-472); no variation is applied anywhere in orders or
  readings (grep: variation appears only in the navigation's observation verbs). `the speed` "by
  the log" is the physics' own speed (502-504). These are labels, not readings.

**Other bugs.** `the record` is to be had at `("deck", "cabin", "shore", "boat")`
(prize_readings register); the knowledge's sense is `ashore` (world/knowledge.py:92, 120-121),
not `shore`, so the record cannot be read ashore, where a court sits. The event `the surgeon's
report` is mapped to `health.sick` (damage_readings register), the same line as `a man taken
ill`.

**The boundary.** My part is the client side of the boundary: nothing in core, ship, physics
or crew should import from it. In my part, `ui/server.py` imports `freesail.agents.agent`
(server.py:121) and `api/readings.py` imports `freesail.agents.harness` and `agents.director`
inside getters (3732, 3915, 4078); since the registry is read by the simulation's standing
orders, the readings module, which the core uses, reaches into the agents package. I did not
check the core's own imports.

## 6. Thin or overgrown

Overgrown at both ends of what the player touches, thin in the middle. The readings registry
is 4,865 lines plus 2,293 in companions for 118 rows; about two fifths of readings.py are not
rows at all (events, station line, the director's truth). The ship view's JavaScript (4,764
lines, with a 7,056-line test file) is the largest single file in the client and draws quarter
galleries, stern lights, figureheads, flag swallow-tails and gun smoke, while the harbour, the
first thing a new player sees, offers no first game, no lesson and a list in which the gates'
and tests' scenarios stand among the playable ones. The harbour itself is a launcher, a settings
editor, a subprocess supervisor, an MCP configuration writer, a shortcut writer and a scenario
editor in one file.

## 7. What is not tested

By grep of tests/ for the names: no test names `clean_mark` or `take_marks` (the marks routes
are exercised by tests/test_server.py), `Easel` (the picture routes are reached in
messages_api.py and test_mcp_server.py), `_drivers_eye`, `set_ease_on_station`,
`save_scenario`, `truth_systems`, `truth_at`, `truth_grounds`, `truth_ports` by name (the
director's tests may reach them through the tool), prize `_where_words`. No test checks the
websocket's Origin, the server's Host, or that the order line's file commands are confined.
No test covers the console's crash on `two stories x` or a `save` to a bad path. Nothing tests
that the snapshot withholds rows the knowledge hides (the tests can see only the greying in
instruments.js if at all). A player meets the harbour's ordering of scenarios; no test can see
whether it leads a newcomer anywhere.

## The ten findings that matter

1. **Any web page can drive the game and read the player's files.** `/ws` accepts every origin
   with no key (server.py:1613-1615) and takes orders; `read the standing orders from FILE`
   echoes any readable file line by line into the feed (console.py:140-151), and `save PATH`
   writes anywhere (server.py:746-773). Shown by command. Weight high; sure.
2. **The harbour's HTTP API has no authentication or Host check and can write a command the
   desktop client runs** (settings.py:522, harbour.py:680-718, 1162-1168). Reachable by any
   local process, by the LAN if `server.host` is set to 0.0.0.0, by DNS rebinding in principle.
   Weight high; exploitability a suspicion, mechanism sure.
3. **The client is not thin: the ship's rig geometry is computed in JavaScript**
   (`buildSkeleton`, 1,613 lines, projection.js:362-1975) with rules copied by comment from
   trim.py, profile.py, form.py, sails.py and gen_ships.py, while the hull's stations and the
   guns are projected in Python; `deck_slope` exists in both. Weight medium; sure.
4. **The player's place hides readings only cosmetically.** Values of hidden rows still go to
   the browser; the chart and ship view ignore the knowledge (queries.py:200-371;
   instruments.js:94-128; shown by command). Weight medium; sure.
5. **No first game, no lesson, no tutorial in the harbour.** 47 scenarios by file path, gates
   and lessons unmarked (harbour.py:365-418, harbour.js:68-83); the lessons say to use the
   console. Weight high for a new player; sure.
6. **Two drivers that disagree.** Console and server duplicate the clock, auto-slow, queries and
   file commands; the console crashes on `two stories x` and a failed `save` (shown by command).
   Weight medium; sure.
7. **Truth through the registry**: `the range` falls back to the truth (action_readings.py:470),
   `the prize` gives true bearing and distance (prize_readings `_where_words`), `the heading`
   "by the compass" is true. These reach models' samples. Weight medium; sure.
8. **readings.py is four modules in one** (registry, events, station line, the director's truth),
   built by import side effects into mutable globals, with a package `__init__` to fix the order
   (api/__init__.py:3-9; readings.py:4835-4865). Weight medium; sure.
9. **The event loop takes the World's lock** in the websocket handler and its driver commands
   (server.py:1622-1631, 1679-1684), with an unbounded queue per socket. Weight medium at high
   compression; likely.
10. **Dead and duplicate data on the wire**: sails' thrust, side force, effective area and the
    wind's mean speed are sent every snapshot and read by nothing; the snapshot bypasses the
    registry it claims to read (queries.py:224-243); `the record` uses a sense `shore` that does
    not exist. Weight low; sure.

## What I did not read

- projection.js was not read whole: I read its header and constants (1-200), the function
  inventory (199 functions), and sections 455-490, 1535-1560, 2060-2140, 3500-3530, 3900-3935.
  The rest (most of `buildSkeleton`, the hull form figures, flags, gun figures, effects) was not
  read line by line.
- map.js was read in its header (1-70), the frame (808-850), the strangers (1070-1120) and by
  grep; not whole. harbour.js was read 1-110 and 220-300 and by grep; not whole. library.js,
  library.html, style.css and most of harbour.html were not read.
- practice_readings.py, prize_readings.py, signal_readings.py, squadron_readings.py,
  damage_readings.py were read with blank lines stripped; viewer_flags.py and viewer_guns.py
  whole; the rest of the Python in my part whole.
- I did not read core/replay.py's allowed-module list for the unpickler, settings.py beyond
  `desktop_entry`, or the agents' Desk.
