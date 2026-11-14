# Second reader: refuting code reader 09 (api, ui, client)

Commit 504a250 (tree at 191b07d, 504a250 is an ancestor; the files I read are unchanged
since 504a250). Read under READERS.md and REFUTERS.md. Nothing under docs/dev, docs/design,
docs/playtests or docs/gates opened. No test suite run. I started the server once from a
scratch directory outside the repository and connected one websocket; nothing was written
inside `/home/user/FreeSail` (the save and the probe went to the scratchpad). Short python
and grep only, each quoted.

| Finding (reader) | Reader weight | My verdict | My weight |
| --- | --- | --- | --- |
| 1. Any web page drives the game and reads/writes the player's files over `/ws` | high, sure | STANDS (worse) | high |
| 2. Harbour HTTP API writes a command the desktop client runs; no auth/Host check | high, exploit a suspicion | STANDS (mechanism); vector as reader states | high |
| 3. Client not thin: rig geometry (1,613 JS lines) copied from five Python files | medium, sure | STANDS | medium |
| 4. Hidden readings only cosmetic: values still sent to the browser | medium, sure | STANDS | medium |
| 5. No first game, no lesson, no tutorial in the harbour | high for a newcomer, sure | STANDS | high |
| 7. Truth through the registry: range, prize bearing/distance, compass heading | medium, sure | STANDS IN PART | medium |

(Findings 6, 8, 9, 10 are outside the six my task singles out and I did not re-run them;
I read enough of the cited lines to see none is obviously wrong, but I did not try to
refute them. Said plainly here so the reviewer does not read silence as endorsement.)

---

## Finding 1: any web page drives the game and reads/writes the player's files over `/ws`

**Reader:** `/ws` accepts every origin with no key (server.py:1613-1615), takes `order`
messages into `driver.submit`; `read the standing orders from FILE` echoes any readable
file line by line (console.py:140-151); `save PATH` writes anywhere (server.py:746-773).
Weight high, sure.

**What I did.** Read the handler and the receive path (server.py:1612-1692), `submit`
(server.py:558-573), `save_path`/`_save` (server.py:217-224, 742-773),
`read_standing_orders_path`/`read_standing_orders` (console.py:129-151), and
`read_orders_file` (standing/book.py:306-319). Then I reproduced it from a fresh scratch
directory outside the tree. I made a two-line file `secret.txt` holding
`SECRET_TOKEN=abc123` there, started the server as the brief allows
(`python3 -m freesail --no-browser --port 18765`, from the repo, with `FREESAIL_SETTINGS`
and `HOME` pointed at the scratch dir so no real settings were touched), connected a
websocket with `origin="http://evil.example"` (the `websockets` library, 17.4), and sent
three messages: `order: read the standing orders from <scratch>/secret.txt`,
`order: save <scratch>/written.json`, `driver: go`. Then I killed the server. Output:

```
hello keys: ['log', 'marks', 'ship', 'snapshot', 'type'] log lines: 1 snapshot keys: 18
EVENT order.rejected | Order not carried out ('SECRET_TOKEN=abc123'): 'secret_token=abc123'
      is not an order this ship understands. ...
EVENT order.rejected | Order not carried out ('another harmless line'): ...
EVENT driver.standing_orders | Read 2 standing orders from <scratch>/secret.txt.
EVENT driver.saved | Saved to <scratch>/written.json at tick 0; ...
```

`written.json` and `written.checkpoint` appeared in the scratch directory. The foreign
`Origin` was not checked (grep of freesail/ for `origin`, `CORSMiddleware`, `TrustedHost`:
none in the server). The file's lines came back verbatim in the event feed, which the
socket relays to any connected page.

**Verdict: STANDS, and in one respect worse than the reader wrote.** I ran this with
**no game started at all** -- the plain harbour (`__main__.main` builds a held `World`
with no scenario, main.py:88-94). The file read and the arbitrary `save` worked anyway,
because `driver.submit` handles `read the standing orders from` and `save` before it ever
touches a ship (server.py:567-577). So the reader's framing that the attacker needs "the
player to have a game running" is too kind: file exfiltration and a destructive save
need only the server up, which it is the moment the player opens the harbour. Driving the
ship (steering, firing) does need a ship under sail.

**What the attacker's page would need, and could not do (honest limits).** It needs the
port (default 8000, guessable; the reader is right) and the server process alive. It does
**not** need a game. Limits that trim "any readable file": the file must be UTF-8 text
(`Path.read_text(encoding="utf-8")`, book.py:309 -- a binary file raises and is not
echoed); `read_orders_file` drops `#`-comment lines and blank lines and joins indented
continuation lines (book.py:311-318), so the exfiltrated text is line-mangled, not a
faithful copy. A line that happens to parse as a valid order is executed rather than
echoed verbatim. The `save` writes the game's own JSON, not attacker-chosen bytes, so it
is a clobber/DoS primitive, not content injection -- the reader said exactly this. None
of these limits blunts the core: a cross-origin tab reads most of a chosen text file and
overwrites a chosen path. High.

## Finding 2: harbour HTTP API, no auth, writes a command the desktop client runs

**Reader:** `POST /api/harbour/settings` saves any settings including
`doors.desktop.command` (settings.py:522); `POST /api/harbour/desktop {write:true}` writes
that command into the desktop client's MCP file, which the client runs (harbour.py:680-718).
No auth, no Host check. Weight high; exploitability a suspicion, mechanism sure.

**What I did.** Read the two routes (harbour.py:1162-1178), `Harbour.desktop`
(harbour.py:680-718) and `desktop_entry` (settings.py:515-524). `desktop_entry` takes
`command` straight from `door.get("command")`, i.e. from saved settings, into the MCP
server command the desktop client launches. `api_settings_save` saves `body["settings"]`
with no key (the route's own comment: "no key, truth 7b-110", harbour.py:33). Both routes
take a JSON body parameter (`body: dict[str, Any]`).

**Verdict: STANDS as a mechanism; the vector is as the reader honestly bounded it.** The
chain settings->desktop is real and needs no credential. The question is reach. Because
both routes read a JSON dict body, a naive cross-origin `fetch` with
`application/json` triggers a CORS preflight the server (no CORS middleware) will not
answer, so a plain foreign tab is blocked -- the reader already said this of the JSON
routes. The routes are therefore reachable by any local process, over the LAN when
`server.host` is set to `0.0.0.0` (anticipated in __main__.py:126), or by DNS rebinding
(which makes the attacker page same-origin to the rebind target and so slips past
preflight). The reader rated exploitability "a suspicion" and the mechanism "sure"; that
is exactly right, and I could not make it reach further or less far. The payoff is
code execution on the player's machine via the desktop client, so high even behind the
preflight gate.

Note: `POST /api/harbour/doors/{id}/stop` takes no body and so is a CORS "simple request"
any tab can send (confirmed: the route has no body parameter, harbour.py:1209-1211). That
is a cross-origin DoS on running model doors, not the command-write; the reader flagged it
too.

## Finding 3: the client is not thin

**Reader:** `buildSkeleton` is 1,613 lines (projection.js:362-1975) with rules copied by
comment from trim.py, profile.py, form.py, sails.py and gen_ships.py, while the hull
stations and guns are projected in Python; `deck_slope` exists in both. Weight medium, sure.

**What I did.** `awk 'NR>=362 && NR<=1975'| wc -l` = 1614 lines; `buildSkeleton` opens at
362 and closes at the export at 1975 (one closure). Grep of projection.js confirms the five
Python sources named in comments: `gen_ships.py` (CLEW_SPREAD, projection.js:82-89),
`freesail/evolutions/trim.py` (settee sheet lead, 130-137, 465), `physics/sails.py`
(goose-wing half area, 1546), `freesail/ship/profile.py` (deck_at/interp, 2064, 2107-2138),
`freesail/ship/form.py` (stations, 162, 2183, 2695-2740). `deckSlope` at projection.js:3905,
and `viewer_guns.deck_slope` at viewer_guns.py:347-349 whose own docstring points back at
"client/projection.js, deckSlope".

**Verdict: STANDS.** Counts and sources are exactly as stated. The strongest defence of
the code is that the server genuinely cannot ship pixels for a 3D rig cheaply and some
projection must live in the page; but that defence does not save the finding, because the
reader's charge is not "there is JS" -- it is that physical *rules* (clew spread, sheet
floor, half-area, deck interpolation) are duplicated in JS with only a comment linking
them to the Python, so a change in trim.py or profile.py silently desynchronises the
drawing. That is true as written. Medium.

## Finding 4: hidden readings are cosmetic

**Reader:** `knowledge_block` lists rows not to be had (queries.py:200-218) but the snapshot
still carries their values; the page only greys some readouts (instruments.js:94-128); the
chart and ship view read no knowledge. Weight medium, sure.

**What I did.** Read `snapshot` whole (queries.py:221-371). `knowledge_block` returns only
a list of row ids with where-words and a sentence (queries.py:200-218). The same snapshot
unconditionally sets `ship.speed_through_water`, `heading`, `leeway`, `heel`, the full
`wind` block, and the whole `sails` array with per-sail `state`, `thrust`, `side`,
`area_effective`, `strain_ratio` (queries.py:293-345) -- none of it gated on
`knowledge_block`. There is no branch in `snapshot` that omits a value because knowledge
hides it; the only knowledge output is the id list. The reader's own run (code-09 lines
314-321: captain sent below, `knowledge.hidden` listed speed and wind, the snapshot still
carried 1.40 m/s and all 38 sails) matches what the code must do.

**Verdict: STANDS.** The server-side comment "the player reads by his place as a model
does" (server.py:315) governs the *log*, not the snapshot; the snapshot is unredacted and
the hiding is a client-side grey. Anyone with the browser's network tab, or the
foreign-origin socket of finding 1, reads the hidden state. Medium (it is the difference
between a design promise and a cosmetic one).

## Finding 5: no first game, no lesson, no tutorial in the harbour

**Reader:** 47 scenarios listed by file path, gates and lessons unmarked
(harbour.py:365-418, harbour.js:68-83); the lessons say to use the console. Weight high for
a newcomer, sure.

**What I did.** Read `_scenario_entry` (harbour.py:397-418): the entry is
`{path, name, own}`; the only decoration is `", keeping to the course of history"` when
`follows_history` is true. Nothing marks a scenario as beginner, lesson or test. Grep of
freesail/ and client/ for `tutorial|beginner|first game|newcomer|getting started`: no hit
bearing on the harbour (the two `newcomer` hits are in evolutions/runner.py, an unrelated
sense). The lesson scenarios' own `name:` fields -- "Pilot water, Black Head to Falmouth
road", "A landfall on one headland", "A night off a lee shore...", "The officer's own
reckoning, off the Lizard" -- do not announce themselves as lessons, and
lesson-falmouth.yaml:10 says to run it from `freesail.ui.console`, not the browser.

**Verdict: STANDS.** A newcomer opening the harbour meets an alphabetof-path list in which
`gate-4c-day`, `gate-5a-day`, three `gate-5b-*` and the four lessons sit among playable
scenarios with no signpost and no "start here". Nothing in the code offers a first guided
game. High for the stated audience (the owner, not a programmer, and whoever he hands it
to).

## Finding 7: truth through the registry

**Reader:** `the range` falls back to the truth (action_readings.py:470); `the prize` gives
true bearing and distance (prize_readings `_where_words`); `the heading` "by the compass" is
true. These reach models' samples. Weight medium, sure.

**What I did.** Read each getter.
- `the heading` (`_heading`, readings.py:471-472) returns `world.ship.heading` with no
  variation; the row's description is "her head by the compass" (readings.py:1119) and
  `the variation` is a *separate* reading (readings.py:1970-1975). So the compass heading is
  the true heading, unconditionally. Firm.
- `the prize`'s `_where_words` (prize_readings.py:82-92) computes
  `bearing_and_distance(world.position, v.position)` from true positions, capped at 20
  miles, while the module docstring says "where she lies by the lookout"
  (prize_readings.py:7). True bearing and distance, unconditionally, with no lookout path.
  Firm.
- `the range`'s `_estimate_m` (action_readings.py:484-497) returns the lookout's `judged_m`
  **when a matching sighting exists**, and only *else* `target_of(...).range_m`, the true
  range. So the truth path is a fallback for "a ship without a lookout aloft" (its own
  docstring) or a sighting without a judged range.

**Verdict: STANDS IN PART.** The heading and the prize leaks are unconditional and I could
not refute them: true state reaches the standing-order grammar and a model's `readings()`
tool under labels that claim observation ("by the compass", "by the lookout"). The range
leak is real but conditional: in an action where the lookout has judged the target, the
estimate is used and the truth path is not hit, so "the range gives truth" overstates the
common case -- it is a degenerate fallback, not the normal reading. Net: the finding stands
(the proposal's spirit, that true figures are never handed over as if observed, is broken
by heading and prize), with the range portion weaker than the other two. Medium, as the
reader had it; I would not raise it.

## Found on the way

Nothing worse than the reader already recorded. One sharpening only, folded into finding 1:
the file-read and arbitrary-`save` primitives over `/ws` work before any game is started,
in the bare harbour, so the precondition is weaker (and the danger larger) than the reader
stated.
