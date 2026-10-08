# V1b: the officer's authority, stand-bys, standing orders, the contrary-order detector, taken aback and the wind-shift line (code reading)

Reader V1b, 2026-10-05. Read-only. All `path:line` references are to the m5c tree
(`D:\Projects\FreeSail\FreeSail-gate-m5c\`) unless marked **m5c-b**. Session logs are named by
their number: S2 = `2-harpy-brig-opus`, S3 = `3-schooner-trial-opus`, S4 =
`4-schooner-plymouth-opus`, S5 = `5-cutter-gemma`, S6 = `6-cutter-qwen-ollama`, S7 =
`7-cutter-qwen-llamacpp`, S8 = `8-merchant-ship-opus`; a number after it is a tick of that
session's `log-full.txt`.

**How it was checked.** The code was read (the files the task names, plus `orders/verbs.py`,
`orders/vocabulary.py`, `orders/port.py`, `world/ports.py`, `world/chart.py`,
`world/reckoning.py`, `physics/sails.py`, `core/events.py`, `agents/remote.py`,
`agents/mcp_server.py`, `ui/server.py`, `tools/build_charts.py`, `data/vocabulary.yaml`, the
scenario books). Six throwaway scripts in `scratchpad\v1b\` ran small read-only checks with
`PYTHONDONTWRITEBYTECODE=1` (how `you may ...` resolves; what parts the conflict rule gives an
order; which guard conditions the dialect parses; what the chart's nearest-coast bearing does
along a track; the nudge chains and the aback lines pulled from the logs). Nothing was written
into the project (checked afterwards: no file of either tree is newer than the run but the
lead's own), the game and the suite were not run, and no `mcp__freesail__*` tool was called.
m5c-b changed none of the code behind claims A to G and J (its diff touches the reseat rule and
the two log lines of H and I only).

## Verdicts at a glance

| | Claim | Verdict |
|---|---|---|
| A | Stand by until x, y or z; "a sounding" wakes on no bottom | **CONFIRMED in code.** One event, one interval or one severity; no "or", no dialect condition. Every cast, a no-bottom one included, is the event. |
| B | A general grant; an always-open emergency clause | **CONFIRMED in code** (neither exists; the refusal's "unless to avoid an immediate danger" is words only). Found besides: an allowance's "named thing" resolves silently wrong (three times in the logs), and allowances never expire. |
| C | "Full and by" refused as changing the course | **CONFIRMED; WORKS AS DESIGNED.** It is the helm verb `keep her full`; allowances are per canonical verb and are named by it. |
| D | "Keep" orders; trim firing hove to and in a calm | **CONFIRMED in code.** `trim` has no hove-to check and fills her; its only floor is 0.5 m/s of apparent wind. The dialect already has every guard a `keep` needs. |
| E | "Trim sails" acts before the helm has swung | **CONFIRMED in code** for the yards (angle and tack fixed at the order); the sheets follow the wind felt for the 15 to 120 s of the work only. Known to the project: the gate books trim `at steady on the course`. |
| F | The contrary-orders detector fires on ordinary sequences | **CONFIRMED.** Of 30 contrary nudges and 1 contrary pause in the logs, 28 nudges and the pause are false alarms. Four separate faults, one of them that the pause can come before the nudge has been shown. |
| G | The officer is not a person on deck | **CONFIRMED in code** (the station carries a name, not a person; documented as M6's). A refused `send the boat ... with the mate` still puts him in the boat. |
| H | Taken aback | **CONFIRMED** for m5c and for what m5c-b left: the re-arm is by time, not by way on; the per-sail lines have no rule at all. |
| I | The wind-shift line and the weather behind it | **CONFIRMED for the log; the cause is NOT REPRODUCED where CHANGES puts it.** The inshore chatter is the sea breeze's direction, read from a whole-cell distance field: a fault in the weather at the ship, measured below. Light airs offshore are only a log matter. |
| J | What wakes a station that is standing by | **Established.** A notable line that is not the named event does not wake it, and a stand-by on a named event has no bound. The package's own brief asked for more than was built. |

---

## A. Stand by until x, y or z

**Claim.** Owner's note 13 (multi-conditional stand-bys, parity with orders); the model: wanted
"a sounding, or the pilot's hail, or a danger sighted", and "a sounding" also wakes on "no bottom
at twenty fathoms".

**Verdict: CONFIRMED in code.**

### How `stand_by(until)` is parsed

`tools.stand_by` passes the string through (`freesail/agents/tools.py:550-551`); the work is
`Harness.stand_by` (`freesail/agents/harness.py:1947-2014`):

1. The words are lower-cased and `until `, `till `, `for ` stripped (1948-1950); "the next X", a
   plural `s` and a missing article are tried against the event table (1952-1955).
2. The first of four that takes the words wins:
   - an **event** of `readings.EVENTS` (1957-1961): `sb = StandBy(words, event=words)`;
   - a **severity** (1962-1963; `STAND_BY_SEVERITIES`, 343-350): `a notable event`, `an urgent
     event` and four other spellings;
   - an **interval** of `readings.INTERVALS` (1964-1965; `freesail/api/readings.py:2308-2322`):
     a minute, a bell, a glass, half an hour, an hour, a watch;
   - a **duration** in the dialect's words (1966-1976; `_duration`, 2403-2412, calls
     `standing.grammar.parse_duration`, `freesail/standing/grammar.py:314-336`): `5 minutes`,
     `ten minutes`, `two hours`.
   Anything else is refused with the lists (1968-1974): "'{until}' is not an event or an
   interval to stand by for. The events: ...".
3. `StandBy` holds exactly one of three (`freesail/agents/agent.py:790-811`): `event`,
   `until_tick` or `severity`. There is no list and no connective.

So the stand-by **shares the dialect's event table and its duration words, and nothing else of
the dialect**: not `when <condition>`, not `, if <condition>`, not `and`. The dialect itself has
no `or` between conditions either (`standing/grammar.py:1225-1228`: "After '{text}' I expected
'and', 'for' or 'then'"); its one `or` is "veers 1 point or backs 1 point" (816-831).

### The full list it accepts

78 events, none absent (`readings.py:2086-2214`, 2290-2299; printed by a read-only check):

- the sun and the clock: `sunset`, `sunrise`, `one bell` to `eight bells`, `the change of the
  watch`, `noon`;
- the rig: `a strain warning`, `a sail shaking`, `a spar carrying away`, `a sail blown out`;
- the hands: `all hands called`, `the watch piped down`, `the hands entered`;
- the weather: `a squall`, `a change in the sky`, and four that are a reading's change, watched
  as a condition (`EventSpec.watch`, 2115-2118): `a wind shift` ("the mean wind shifts 1
  point"), `the glass falling fast`, `the glass turning`, `the sea getting up`;
- the lookout: `a sighting`, `a landfall`, `a danger sighted`, `a bearing steady and closing`,
  `a sail sighted`, `sail ho`, `a sail made out`, `a stranger's colours made out`, `a sail
  lost`, `a sail within hail`;
- the lead and the reckoning: `a sounding`, `a lunar`, `a longitude by chronometer`, `the
  chronometer run down`, `the variation observed`;
- the manoeuvres and the helm: `hove to`, `filled away`, `tacked`, `wore`, `the course shaped`,
  `steady on the course`;
- the ground: `the anchor let go`, `brought up`, `the anchor aweigh`, `the anchor weighed`,
  `under way`, `got under way`, `the anchor dragging`, `the cable parted`, `aground`, `the
  ground taken`, `afloat`, `the turn of the tide`, `the turn to the flood`, `the turn to the
  ebb`, `moored`, `unmoored`, `the kedge laid`;
- the port: `the pilot aboard`, `the pilot refused`, `the pilot off`, `the pilot's hail`, `the
  pilot asks to be put off`, `the boat away`, `the boat alongside`, `a message`, `a letter`,
  `the yard's stores aboard`, `the cargo aboard`;
- the deck: `the deck given`, `the deck taken`, `a handover`, `a standing order countermanded`.

Each of the three things the model wanted together exists singly (`a sounding`, `the pilot's
hail`, `a danger sighted`). What is missing is only the "or".

### Why a duration is refused with the deck

Only one longer than a glass is (`harness.py:256-259`, 1978-1988):

> `# A station with the deck stands by until an event or a bell, never for longer ... (package`
> `37; the cold review's third item: "a captain that stands by is a ship with no one on deck").`
> `STAND_BY_WITH_DECK_MAX_S = A_GLASS_S`

`a glass`, `5 minutes`, `ten minutes` are taken; `an hour`, `a watch`, `40 minutes` are refused
("has the deck and stands by until an event or a bell, not for {words}"). The bound is on
**intervals only** (`if a.has_deck and sb.until_tick is not None`, 1978). An event carries no
bound: see J.

### How "a sounding" treats a no-bottom cast

It is the event. `EventSpec("a sounding", "sounding")` has no test on the line's data
(`readings.py:2125`), and every cast is written as that kind, notable, the no-bottom one
included (`freesail/world/reckoning.py:1252-1255`, 1341-1343):

```python
if truth is None or units.m_to_fathoms(truth) > limit:
    what = "a hundred and twenty" if deep else "twenty"
    self._record_cast(tick, None, "", f"No bottom at {what} fathoms.", deep)
...
self.world.record(Severity.NOTABLE, "sounding", text, data={"depth_m": None if depth_m is None else ..., "fathoms": ...
```

The line's data already says which it is (`fathoms` is `None`), so the distinction is one
lambda. Being notable, every no-bottom cast also samples an officer who is not standing by (the
policy samples on notable lines, `agent.py:527`) and ends an `a notable event` stand-by.

### What the logs show

- S2 349734-349745: the captain suggests "stand by until the mean wind is 5 knots"; the officer
  answers "A stand-by can't take a condition, so I've put it in the book instead" and enters a
  standing order that *sets plain sail* when the wind exceeds five knots: an order given to get
  a wake.
- The owner's own way round it is in the book of S2 and S4: `standing order "The pilot asks
  off": at the pilot asks to be put off then tell the officer ...` (S4 39406). A `tell` wakes
  any stand-by (J), so the captain's book can build a multi-event wake. The officer cannot do
  the same for himself: `tell` and `ask` in his own rule are refused (`tools.py:482-484`: "may
  not give '{order}' in a standing order: a station is addressed by the captain").

### What a fix would touch

| Change | Where | Size | Risk |
|---|---|---|---|
| **"A, B or C"**: split the words on `,` and `or`, resolve each as now, keep a list | `agent.StandBy` (a tuple of alternatives, or `events`/`severity`/`until_tick` together); `Harness.stand_by` 1947-2014; `_stand_by_ended` 769-788 (first alternative to come true names the reason); `_matched_in` 797-810; `_in_flight` 812-844; `_stand_by_watch` (one `(cond, memory)` becomes a list); the words in `agent.STAND_BY_WORDS` 573-584 and `tools.py:680-697`; tests in `test_agents.py` (776, 826), `test_officer.py` (633) | **M** (about a hundred lines with tests) | No digest risk (no recorded truth seats a model). A stand-by is a recorded call, so a replay re-parses it. The consent brief's "stand by until a bell or an event" stays true: no re-ask. |
| **A dialect condition** (`until the depth is under 20 fathoms`, `until the mean wind exceeds 5 knots`): when the words are no event, try `standing.grammar.parse_condition(words, ship)` and watch it once a tick | `Harness.stand_by`; the machinery is there already for the four reading-change events (`_stand_by_watch`, 782-786, evaluated with `cond.holds(world.readings, memory)`). A plain `Condition` (a level), not `EventCondition` (an edge), so a condition that holds already wakes at once | **S to M** (about thirty lines and tests) | The readings a condition may name are by account (the depth is the chart's at the reckoning or the last cast): say so in the tool's words. |
| **"A sounding" and no bottom**: a second event with a data test, `EventSpec("bottom", "sounding", lambda d: d.get("fathoms") is not None)` (or "a cast with bottom"); leave `a sounding` as it is | `readings.py` after 2125; the primer's table (`docs/primer/11`, tested by `tests/test_primer.py`) | **S** | Changing `a sounding` itself would change when `at a sounding, if ...` rules of the gate books fire and move the recorded digests (`data/scenarios/merchant-passage.orders:154`); a new event does not. |
| **No-bottom casts routine, not notable** | `reckoning.py:1341` | **S** | Severity is in the digest (`core/events.py:108-120`): the 5b and 5c constants in `tests/test_known_truths.py` would be re-recorded. |

Parity gaps met on the way: `she is at anchor` is not a condition (`the anchor is down` is, by
the `ground` kind's substring test, `standing/grammar.py:720-731`, but primer 11's table does
not list it); `a sail is in sight` is refused (the reading is `a sail in sight`, so the
condition reads "a sail in sight is in sight").

---

## B. A general grant of authority and the emergency clause

**Claim.** Owner's note 15; the model: keep a small explicit-only list (anchoring, the port's
business, buying and selling) and an always-open, logged emergency route ("the refusal text
already uses that phrase, but there's no route to act on it"); gate item 14
(`docs/gates/gate-m5c.md:78`) asks the owner to rule on the same.

**Verdict: CONFIRMED in code.** There is no general grant and no emergency route. The domain is
a fixed table opened one canonical verb at a time, the captain's condition is text, and the
exception the refusal quotes is implemented nowhere.

### How the domain is defined

`Domain` is a frozen dataclass (`freesail/agents/agent.py:125-161`) with `levels`, `objects`,
`verbs`, `refused` and `words`; `OFFICER_DOMAIN` is its one instance (188-255). The check
(140-161):

```python
def why_not(self, verb, spec_object, level):
    if verb in self.verbs: return None
    if level not in self.levels and level not in ("reading", "driver"): return f"level {level} is beyond the station"
    for key, why in self.refused:
        if key == verb or key == f"object:{spec_object}": return why
    if spec_object in self.objects: return None
    return "it is the captain's to give"
def allows(self, verb, spec_object, level, allowances=None):
    if allowances and verb in allowances: return True, ""
```

The filter is `tools.authority_check` (`tools.py:409-449`): the order is parsed by the
imperative grammar for its canonical verb, the verb's `object` and `level` come from
`data/vocabulary.yaml`, and `domain.allows(...)` decides. A standing order has its rank set and
each order after `then` checked the same way, at give time only (455-488); the book's orders are
allowed on his own rules only (491-521).

**Inside** (levels 0 to 2):

- by the vocabulary's object: every `sail` verb (set, take in, furl, reef, shake out, sheet
  home, draw, bend, unbend, shift, goose wing, rig out, rig in, scandalise), `yards` (brace,
  trim, square, **back**), `line` (haul, ease, check, let go, belay, reeve, splice), `wreck`
  (cut away, send down), `work` (belay the work), `query` and `reading` (every reading asked at
  the prompt, `the bearing of <mark>` among them);
- by name (`agent.py:191-224`): heave the log, heave the lead, heave the deep sea lead, make her
  out, ask the pilot; the masts and yards sent down and up, the catharpins; loose sails to dry,
  furl all, set plain sail, make all sail, shorten sail; belay that, belay all work; the book's
  sentences on his own rules.

**Outside** (`agent.py:225-253`), each with its reason:

| Key | What it covers | Reason text |
|---|---|---|
| `object:heading`, `object:points`, `keep her full`, `steady`, `meet her`, `right the helm`, `helm a lee`, `helm a weather` | steer; come up, bear away; full and by; the conning words | `_COURSE` |
| `tack ship`, `wear ship`, `heave to`, `fill away`, `box haul`, `wear short round`, `lie a try`, `scud`, `back and fill` | the manoeuvres | `_MANOEUVRE` |
| `object:anchor` | come to an anchor, let go the anchor, veer cable, heave short, weigh, cat and fish, back the anchor, get under way, moor, unmoor, lay out a kedge | `_ANCHOR` |
| `call all hands`, `pipe down`, `relieve the watch` | | `_HANDS` |
| `object:person` | send for, go below, come on deck (ask the pilot is let through by name) | `_PEOPLE` |
| `object:port` | send the boat, buy, sell, demand, take in water, take in provisions, enter | `_PORT` |
| `object:navigation` | take a bearing of, work up the reckoning, observe the sun, set the reckoning to, allow, shape a course for, the longitude's five, the two azimuths, give chase (the log, the leads and make her out are let through by name) | `_NAVIGATION` |
| `object:station` | every sentence to a station (refused earlier, `tools.py:439-440`) | `_STATION` |
| `belay all standing orders`, `object:standing` | the captain's book | `_BOOK` |

A world order is refused by the grammar itself; a console verb falls to "it is the captain's to
give".

### Every refusal text

- No authority: "The {station} has no authority to give orders." (`tools.py:775`).
- No deck: "The {station} has not the deck: the captain gives it with 'you have the deck', and
  until then no order is given." (792-795).
- The domain: "The officer of the watch may not {text} without the captain: {why}."
  (`tools.py:449`), with `{why}` one of (`agent.py:165-176`):
  - `_COURSE`: **"the course is the captain's, never to be changed without his directions unless
    to avoid an immediate danger"**: the only refusal that names the exception;
  - `_MANOEUVRE`: "a manoeuvre (tacking, wearing, heaving to, filling away) is the captain's";
  - `_ANCHOR`: "the anchor is let go and weighed by the captain";
  - `_HANDS`: "all hands are called, and the watch sent below, by the captain";
  - `_PEOPLE`: "the people are sent for by the captain";
  - `_PORT`: "the port's business is the captain's";
  - `_NAVIGATION`: "the reckoning, the sights and the course shaped are the master's for the
    captain";
  - "level {level} is beyond the station"; "it is the captain's to give".
- A station sentence: "The officer of the watch may not {text}: a station is addressed by the
  captain." (440).
- The book: "gives standing orders in his own rank, the {rank}; 'by the {said}' is refused."
  (472-475); "In standing order '{name}', '{order}' is refused: {why}" (487); "may not belay all
  standing orders: the captain's book is his own." (507); "Standing order '{name}' is
  {officer}'s; the officer of the watch may {verb}, resume and strike his own standing orders
  only." (517-520).
- `hand over the deck` typed as an order: the pointer to the tool (390-393).

### Does any path let the officer act on danger?

No path for the helm or the anchor. `why_not` reads a verb, an object and a level; nothing in
`agent.py`, `tools.py` or `harness.py` reads the ship's state, the lookout or the lead when it
decides. The sentence "unless to avoid an immediate danger" is Falconer's, quoted as the reason
(`agent.py:22-23`, 165-168), and stops there. What the officer *can* do without a word, by the
table above: take the way off her by sail handling (`shorten sail`, `furl all`, `let go` a
sheet, and `back the main topsail`, which is a `yards` verb and inside the domain though `heave
to` is not), and say so in the log. He cannot put the helm over, tack, wear, heave to, fill
away or let go an anchor.

A side door exists for one who already holds an allowance: with `let go the anchor` allowed, S2's
officer entered a standing order in his own rank, `when the depth is under 18 fathoms and the
ground is sand then let go the anchor` (S2 169301 and 169304 refused; 169312 entered, once the
verb was allowed at 169310). The check is at give time only; a rule's firing is an ordinary
`World.submit` with the rule's actor (`freesail/standing/runtime.py:361-368`) and is not checked
again, so `you may not let go the anchor` afterwards would leave that rule standing and firing.

### How `you may <thing> [if <condition>]` is parsed, stored, matched and taken back

- **Recognised** as any sentence that begins `you may ` (`freesail/orders/stations.py:71`,
  141-143), and only from the captain (a standing order may not say it, 250-254).
- **Resolved** by `_verb_in` (354-369): the words after `you may` are matched against every
  verb phrase of the vocabulary, longest first, **as a prefix**; the canonical verb of the first
  that matches is the allowance, and whatever words follow are kept as "his condition":

  ```python
  for phrase in vocab.verb_phrases:  # longest first
      pw = phrase.split()
      if words[: len(pw)] == pw:
          verb = vocab.phrase_to_verb[phrase]
          ...
          return verb, " ".join(words[len(pw) :])
  ```

  A console verb, a reading, a book sentence or a station sentence is not allowable (366-367).
- **Stored** as `AgentState.allowances: dict[str, str]`, canonical verb to the words
  (`agent.py:848`; `harness.py:1744`). A second allowance of the same verb overwrites the words.
- **Matched** by the verb alone: `if allowances and verb in allowances: return True`
  (`agent.py:158-159`).
- **The condition is shown, never enforced.** It is a string in the `agent.deck` line, the
  officer's reading (`readings.py:2255-2258`), the brief head (`agent.py:703-707`) and the word
  of the next sample (`harness.py:1746`). The code and the primer say so plainly ("kept as said
  and judged by the officer", `harness.py:1736-1737`; `docs/primer/16:62`): works as designed.
- **Taken back** by `you may not <verb>` only (`harness.py:1750-1757`).
- **Never expires.** `allowances` is written in `allow` and `disallow` and nowhere else (grep).
  The log says "by the captain's word for the watch" and the brief "for this watch", but the
  change of the watch, `I have the deck`, `hand_over`, a stand-down and a reseat
  (`_reseat_now`, 1908-1943) all leave it. S2 shows it: `let go the anchor`, allowed on 14 June
  (169310), was used on 19 June (636631), four stand-downs and four seatings later.
- Each `you may` sets `a.word` and so wakes a stand-by (J): S2 18553-18572 is three allowances
  in sixteen seconds, the second and third each waking a stand-by taken a second or two before.

### Why `You may set the reckoning` resolved to the wrong thing, and what else does

The navigation verb is `set the reckoning to` (`data/vocabulary.yaml:527-531`), four words. The
captain's three, `set the reckoning`, are not a prefix match for it, so the longest phrase that
*is* a prefix wins: `set`, the sail verb, with "the reckoning" swallowed as the condition. The
log line says it honestly but is easy to misread (S8 52232): "The officer of the watch may set
(the reckoning), by the captain's word for the watch." Three seconds later the officer's `set
the reckoning to 49 00 N 4 21 W` is refused as navigation (S8 52235).

The same thing happened twice more in the logs, unnoticed:

| Session, tick | The captain typed | Logged as | Opens |
|---|---|---|---|
| S8 52232 | `you may set the reckoning` | `may set (the reckoning)` | nothing (the sail verb is inside the domain) |
| S2 14402 | `You may change the course` | `may shift (the course)` | nothing (`change` is a synonym of the sail verb `shift`, `vocabulary.yaml:252`). The officer's handover note of S2 156132 lists "shift course" among his leave. |
| S2 169297 | `You may let go` | `may let go` | nothing (the line verb); the standing order that wanted the anchor was refused twice before `You may let go the best bower` (169310) |

A read-only run of `_verb_in` over other things a captain might say:

- **A shorter form of a longer verb, or a word that is also a sail or line verb:** `lower a
  boat` → `take in` (a boat); `start the pumps` → `ease` (the pumps); `enter the harbour` →
  `enter`, the port's verb for raising men; `change course as you see fit` → `shift`.
- **Two things joined:** `tack or wear` → `tack ship` (or wear); `buy and sell` → `buy` (and
  sell); `heave to and fill away` → `heave to` (and fill away); `send the boat and buy` → `send
  the boat` (and buy). The second verb is not opened and nothing says so.
- **An argument read as a condition:** S4 406851-406875, `you may come up half a point`, `a
  point`, `two points`, `bear off half a point`, `a point`, `two points`: six sentences, two
  allowances (`come up`, `bear away`), each opening the verb whole. `shape a course for
  plymouth` opens shaping a course for anywhere; `heave in the best bower cable to 160 fathoms`
  opens `heave short` whole.
- **A verb already inside the domain,** logged as an allowance all the same: `make sail` (S2
  562), `heave the lead` (S8 146), `heave the deep-sea lead` (S8 54870); `sound`, `trim sails`,
  `back the main topsail`, `ask the pilot` would be too.
- **Refused aloud** ("names no order the officer of the watch could be allowed"), which is the
  safe failure: `alter course`, `shape a course` (S2 437521), `hail the pilot`, `heave` (S3
  2942), `send ashore` (S3 2955), `bring her up` (S4 143), `trade`, `handle the ship`, `do as
  you see fit`.

### The three cases the lead asked about

- **`weigh` did not cover `get under way`** (S2 14348). Two verbs: `weigh` is the anchor up and
  no sail set, `get under way` is Luce's whole sequence (`vocabulary.yaml:624-629`, 646-658);
  an allowance opens one canonical verb. Likewise `heave to` does not open `fill away`, `steer`
  does not open `keep her full`, `come up` or the conning words, and `come to an anchor` does
  not open `let go the anchor`.
- **A bearing of the land refused** (S2 15559, S4 512943). `take a bearing of` has the object
  `navigation` (`vocabulary.yaml:511-516`), and of the navigation verbs the domain lets through
  only the log, the two leads and `make her out` (`agent.py:193-198`, 249). The reason given is
  the master's. The tuning notes call the line "judgement on art. XXVI of the Master"
  (`docs/dev/TuningNotes.md:1420`), while the brief's own Falconer has the lieutenant
  "superintending the navigation" (`agent.py:468-471`). The reading `the bearing of <mark>` is
  open to him as a query; the refusal does not say so.
- **`fill away` refused after the captain's own order hove her to** (S2 18542; S8 16960 for a
  rule). The domain has no notion of who put her in the state: `fill away` is a manoeuvre,
  whoever hove her to. The officer wrote "she ... is creeping two knots toward the Bizzies, five
  miles. 'Fill away' is the captain's manoeuvre; may I fill away".

### The allowances actually given (`| agent.deck |` lines, S2, S4, S8)

| | Sentences taken | Distinct verbs | The verbs |
|---|---|---|---|
| S2 (brig) | 27 (and 7 refused aloud) | 26 | heave short, send the boat, buy, weigh, *set plain sail*, get under way, *shift (the course)*, steer, take a bearing of, tack ship, fill away, wear ship, heave to, work up the reckoning, *let go*, let go the anchor, sell, unmoor, box haul, shape a course for (plymouth), observe the sun, veer cable, lay out a kedge, send for (carpenter), pipe down, come to an anchor |
| S4 (schooner) | 27 (and 2 refused) | 20 | buy, sell, send the boat, weigh, get under way, steer, veer cable, tack ship, wear ship, heave to, fill away, let go the anchor, moor, keep her full, come to an anchor, shape a course for (st mary's), come up, bear away, take a bearing of, heave short |
| S8 (ship) | 20 | 19 | let go the anchor, veer cable, heave short, *heave the lead*, buy, sell, steer, helm a weather, helm a lee, heave to, tack ship, wear ship, get under way, take a bearing of, fill away, pipe down, call all hands, *set (the reckoning)*, *heave the deep sea lead* |

(Italics opened nothing.) The union that opened something is thirty verbs, and it touches every
refused class of the domain: the course (six verbs: steer, come up, bear away, keep her full,
the helm a-lee and a-weather), the manoeuvres (5 of 9), the anchor (9 of its 11 verbs), all
hands (2 of 3), the people (send for), the port (send the boat, buy, sell: 3 of 7) and
navigation (a bearing, the reckoning worked, the sun, a course shaped). In practice a general
grant is "the `refused` table less the station's and the book's entries". The model's "about
fifteen permissions" on the Speedwell was 27 sentences for 20 verbs.

One claim the log does not bear out: "On the Harpy that clause would have mattered." At the
grounding of 19 June (S2 636653) the officer already held `steer`, `tack ship`, `wear ship`,
`heave to`, `fill away` and `let go the anchor` by allowances five to seven days old; his `let
go the anchor` of 636631 was taken, 22 seconds before she struck; the domain refused none of his
orders between noon and the grounding. What held him back was the captain's "I'll con her, don't
worry" (635913). An emergency clause would have saved the two minutes of 20 June (687143
refused, 687262 allowed) and the like.

### Sizing the three things

| Thing | What it touches | Size | Risk |
|---|---|---|---|
| **A general grant sentence** (`she is yours`, `you have the deck and the ship`) | `orders/stations.py` (a sentence beside `_ALLOW`, and its taking back); `AgentState` (a flag, rebuilt by replay from the journaled order as allowances are); `Domain.allows` (`agent.py:153-161`); `Harness` (a method like `allow`, the journal line, the word); `tools.authority_check` (pass the flag); the reading (`readings.py:2237-2268`) and the brief head (`agent.py:693-712`); `data/vocabulary.yaml` (the words, for completion); `docs/primer/16`, `Harness.md`; tests in `test_officer.py` | **M** | **The consent brief**: "unless the captain's word allows a named thing" is in the section *What an instance would see and do* (`docs/agents/ConsentBrief.md:17`), one of the re-ask sections (`agents/consent.py:187`). If the sentence changes, the hash moves and every model with a yes is asked again. No digest risk. |
| **An explicit-only list** the grant does not open | a `reserved` set on `Domain` beside `refused`, and its words in `OFFICER_DOMAIN_WORDS`; about ten lines inside the row above | **S** (nothing by itself) | A design decision first: which. The logs argue against putting the anchor on it (it was the thing wanted in a hurry, S8 121679, S2 636631); the port's verbs are the clear case. |
| **An always-open, logged emergency route** | Taking the officer's word: an optional `danger` argument to `submit_order` (`tools.py:648-658`; the schema follows the table, `parameters_schema` 740-753, so both doors get it), `authority_check` allows a fixed set (the helm verbs, heave to, let go the anchor, come to an anchor) when it is given, and a **notable** line says so ("By the officer of the watch, to avoid an immediate danger (rocks ahead): ..."); the refusal's words should then name the route | **S** in code, **M** with the brief, the primer and the tests | The same consent sentence. The welfare chain (F) should not count such an order. |
| ... the game judging the danger | A window opened by a danger line: `lookout.sighting` with `seen_as == "danger"`, `lookout.closing`, `anchor.dragging`, a cast under some depth; the same table J's "notable danger line" would use | **M**, and it leans on a lookout that does not yet cry land ahead (owner's note 19) | Without note 19's alarm the game would not have judged the Harpy's shoaling a danger until the lead said so. Taking the officer's word and logging it does not wait on that. |

A narrower fix worth having whatever is ruled (**S**, `stations._verb_in` and `_deck`): refuse an
allowance of a verb the domain already allows, naming the longer verbs that begin with the same
words ("did you mean 'set the reckoning to'?"), and refuse a remainder that begins with `and` or
`or`. Risk: a save whose journal holds one of the three mis-resolved sentences would replay it
as a refusal, the `agent.deck` line and the wake it caused would be missing, and a recorded
transcript could fall out of step; such saves load from their checkpoints.

**A leak found by reading** (not in the notes): the filter passes anything the imperative
grammar cannot read, "whose refusal is the captain's own" (`tools.py:441-444`). But
`orders.handle` gives an unknown noun a second reading as the port's stores
(`freesail/orders/__init__.py:96-102`, `_stores_order` 149-163). `take in twenty tons of water`
raises `UnknownNounError` in the filter's parse (checked) and so is let through, and is then
carried out as `take in water`, the port's business, with no allowance. `take in water` and
`take in provisions for thirty days` parse directly and are refused. Size **S** (run the same
second reading inside `authority_check`).

Smaller: `AgentState.told` ("what the captain told it for the watch", `agent.py:847`) is read by
the reading (`readings.py:2252-2254`) and written nowhere.

---

## C. "Full and by" refused as changing the course

**Claim.** "The permission had to be 'keep her full', and the name doesn't match the order."

**Verdict: CONFIRMED; WORKS AS DESIGNED** (three ordinary facts meeting).

- `full and by` is a synonym of the verb `keep her full`, object `none`
  (`data/vocabulary.yaml:172-182`); so are `steer full and by`, `by the wind`, `nothing off`,
  `no higher`.
- The domain refuses that verb by name with the course's reason (`agent.py:228`). It is a helm
  order: `_helm` sets `HelmMode.FULL_AND_BY` (`freesail/orders/verbs.py:1963-1970`), and her
  heading then follows the wind.
- An allowance is per canonical verb. S4's `You may steer` (63) opened `steer` and nothing else,
  so `full and by` was refused at 43089 and `come up half a point` at 406842. `steer` (object
  `heading`), `come up` and `bear away` (object `points`), `keep her full`, `steady`, `meet
  her`, `right the helm`, `helm a lee`, `helm a weather` are nine verbs, and each wants its own
  allowance.
- The captain may *say* it either way: `You may full and by` (S4 43096) and `You may keep her
  full and by` (43102) both resolve, and both are logged by the canonical name: "may keep her
  full". The refusal, though, echoes the officer's words ("may not full and by", `tools.py:449`).
  That is the mismatch.

**Fix.** Either say the allowance as said with its verb ("may keep her full (said: full and
by)"; **S**, `stations._deck` 347-351 and `Harness.allow` 1745-1748), or let one word open the
whole class (`you may alter the course` for the nine course verbs, `you may work the anchor`,
and so on: classes named on `Domain`; **M**, and it is most of B's general grant). No digest
risk; the brief's sentence is unchanged by the first.

---

## D. "Keep" orders

**Claim.** Owner's note 16; the model's `trim` rule fired hove to and filled her, twice, and
braced yards all night in a calm; a `keep` should pause hove to, at anchor or with no wind.

**Verdict: CONFIRMED in code and in the log.**

### What the dialect offers today for a continuous duty

- `when <condition> [for <duration>] then ...`, edge-triggered with a five-minute dwell
  (`standing/rules.py:44`; `runtime.py:268-299`); `at <event> then ...`; `every <interval> then
  ...`; each with an optional `, if <condition>` tested at the firing (`grammar.py:193-249`).
- Events that serve a trim: `a wind shift` (the ten-minute mean a point from where it stood,
  `readings.py:2115`), `steady on the course` and `the course shaped` (2196-2197).
- Guards, all conjunctions: `she is not hove to` (package 33c; `grammar.py:468-470`, 923-932;
  true "from the moment the heave-to begins until she fills away, so a trim rule sleeps through
  the manoeuvre too", `rules.py:274-278`); `the anchor is not down`; `the mean wind exceeds 3
  knots`; `the apparent wind exceeds 2 knots`. Checked by parsing: this is taken today:

  `standing order "keep trimmed": at a wind shift, if she is not hove to and the anchor is not down and the mean wind exceeds 3 knots then trim sails`

- No `or` between triggers or conditions, no `until`, and one trigger a rule.
- Stopping exists: `belay "x"`, `avast "x"`, `strike standing order "x"` (`grammar.py:1272-1278`).

The model's rule was the bare form (S4 83157): `standing order "trim" by the mate: at a wind
shift then trim sails`. So were the starter's and both gate books' (`data/standing_orders/
starter.orders:70`; `data/scenarios/merchant-passage.orders:51`, `naval-cruise.orders:30`). The
primer shows the guarded form as an example (`docs/primer/11-the-starting-book.md:85`) and
nothing ships with it.

### What `trim sails` does to a ship that is hove to

It fills her. The order refuses at anchor and aground (`verbs.py:93-99`, `_not_riding`
1924-1933: "She is at anchor; 'trim sails' must wait till she weighs") and that is all. `_trim`
(733-992) never looks at `ship.extra["hove_to"]`:

- every yard is given the best angle for the present apparent wind, on the present tack
  (776-777, 804-815): the yards the heave-to laid aback (`scripts.py:1186-1190`, `-sign *
  brace_limit`) are braced full again;
- every set fore-and-aft sail's sheet is worked unless it "stands" (895-905), and a sheet held
  to windward is expressly not standing (`not reading.held_to_windward`): the staysail a
  schooner or a cutter heaves to by (`scripts.py:1232-1239`) is let draw.

The heave-to's record is not cleared by this (only filling away pops it, `scripts.py:1363`), so
afterwards the ship is sailing while the reading still says "hove to", `steer` and `keep her
full` are still refused ("She is hove to; fill away before giving her a course",
`verbs.py:1949-1961`) and the taken-aback rule still counts her as in stays
(`physics/integrate.py:242`). The helm orders got this guard in packages 32e and 33a; the trim
did not. `tests/test_trim_order.py` has no hove-to case.

In the log (S4): hove to at 147971, `trim` fired at 162102 ("Braced two yards to the wind, 41°
on the starboard bow; trimming the sheets of the fore sail, the fore staysail, the jib and the
flying jib"), filled away and hove to again at 163225-163278; hove to at 192632, fired at 193303
the same way. Twice, as the model says. At the officer's station in S7 the trim rule was belayed
before heaving to "so it can't fill her away again" (transcript entry 151, tick 112487). And in
S4 at 557457 the rule fired after a tack had been ordered (557169) and before it ended, setting
four sheet parties to work; that tack failed two minutes later. `she is not hove to` does not
cover a tack; `the manoeuvre in hand is none` covers one that has begun, but a manoeuvre still
waiting its turn is not "in hand" to that reading (`api/readings.py:1241-1244`), so a `keep`
wants its own test on the runner's work.

### In a calm

One floor: `if d.apparent_wind_speed < 0.5: raise OrderError("There is no wind to trim to.")`
(`verbs.py:774-775`), half a metre a second, about one knot of apparent wind. The true wind never
falls under 0.25 m/s (`physics/wind.py:125`). Above the floor the trim is carried out to
whatever the air is doing at that second. S4's calm night: fired at 323714, refused once at
327484 ("There is no wind to trim to"), then 331634, 333374, 335657, 339571, 341001, with the
apparent wind 143° on the quarter, 93°, 60°, 36° on the other bow, 115°, 19°: the yards chased a
wandering air six times in five hours. The event that fired it has no floor either (I).

### What a `keep ...` form would be in this code

| Option | What it is | Size |
|---|---|---|
| **Sugar over existing rules** | `keep the sails trimmed` enters two ordinary rules under one name (`at a wind shift ...` and `at steady on the course ...`, which also answers E), each with the standard guard above; `belay`, `avast`, `strike` stop it as they stop any rule | **S to M**: `standing/grammar.py`, `book.py`, primer 11, tests. No engine change. |
| **A reading and a `when`** | a reading "the trim" (how far the yards and sheets stand from what the wind wants, the number `_trim` computes already) and `keep` as `when the trim is off 5 degrees for 2 minutes, if <the guards> then trim sails`. It trims when a trim is wanted, whatever the cause (a shift, a turn, a sail set), and not otherwise | **M**: `api/readings.py`, `orders/verbs.py` (the targets as a function), `standing/grammar.py`, tests |
| **A new rule kind, or a duty of the crew model** | a `keep` trigger the runtime evaluates, or the afterguard's routine in `crew/routine.py` | **L**, and a design decision first |

A stop condition (`keep ... until <condition>`) is a field on `Rule` and a test in
`Runtime.tick` that strikes it: about twenty lines.

### Should `trim sails` itself refuse when hove to?

Yes, independent of any `keep`: it is the helm's guard, missing from the trim. Refuse `trim`
with nothing after it (and `trim the sheets`) while `"hove_to" in ship.extra` or a heave-to is
in hand, in the helm's words ("She is hove to; fill away before trimming to a course"); let a
named sail or yard through, for an officer who means it. **S**: `verbs.py:93-99` or the head of
`_trim`, and a test. **Risk:** the gate books fire `trim on a shift` and `tend the sheets` with
no guard while their ships lie to (`merchant-passage.orders:28`, 51-52, 105; `naval-cruise.
orders:21`, 30-31; the 5b passages heave to at noon), so a refusal there changes those logs,
and on the schooner her handling after it. Expect the 5b and 5c constants in
`tests/test_known_truths.py` to move and want a look, not only a re-record. The 0.5 m/s floor
could rise to two knots in the same change.

---

## E. "'Trim sails' acts before the helm has swung"

**Verdict: CONFIRMED in code.**

- **The yards.** The target is computed once, when the order is given, from the apparent wind
  and the tack of that second (`verbs.py:773-777`):

  ```python
  d = ship.dyn
  ...
  awa = abs(d.apparent_wind_angle)
  sign = 1.0 if d.tack == "starboard" else -1.0
  ```

  and written into each brace's parameters (842-849: `"target_deg"`, `"target_angle"`, `"mode":
  "to the wind"`, `"tack": d.tack`). The evolution ramps the yard to that number over 45 s
  (`data/evolutions/brace.yaml`, `ramp: yard.brace_angle: tack_sign(params.tack) * clamp(...
  params.target_deg ...)`). Only a second `trim` re-aims a yard, and only one still waiting its
  turn (850-858).
- **The sheets.** `TrimSheetScript` re-aims every tick while the hands work the sheet ("the
  hands trim to the wind they feel, not the one at the order", `evolutions/scripts.py:3737-3747`,
  called from `tick` at 3762), for 15 to 120 s by the sail's size (3731-3733). A fore-and-aft
  sail's trim follows a turn for that long and no longer.

So `steer X; trim sails` trims the yards to the old course, always. The ordered course is never
read.

**The project knows.** `data/scenarios/merchant-passage.orders:46-50`: "the starter book's trim
answers a shift of the true wind, not a turn of the ship", with `standing order "trim to the
course": at steady on the course then trim sails`. `helm.steady` is written when she has been
within two degrees of the ordered heading for twenty seconds (`physics/integrate.py:209-231`).
The S4 officer found the same answer on the sixth day (469859: `standing order "steady trim" by
the mate: at steady on the course then trim sails`).

**Fix.** (1) Say it: the result of `trim sails` given while a helm order is unsettled could end
"trimmed to the wind as it is; she is still turning" (**S**). (2) Trim to the course: when the
helm is on a compass course and not yet steady, compute the apparent wind she will have on it
from the wind and her speed, and use that angle if the tack does not change (**S to M**,
`verbs._trim`, `tests/test_trim_order.py`). (3) Defer: such a `trim` is held and given at
`helm.steady` (**M**). D's sugar covers the standing case. Risk for (2) and (3): a trim that
fires in mid-turn in a gate book would log other angles and move the 5b and 5c digests.

---

## F. The contrary-orders detector fires on ordinary sequences

**Verdict: CONFIRMED.** Of the 30 contrary nudges and the 1 contrary pause in all the logs, 28
nudges and the pause are false alarms; the 2 true ones are a local model's helm in S5. Four
faults are behind them.

### How the detector decides (`Harness._note_given`, `harness.py:1452-1488`)

1. Only an order the ship **took** counts (an `order.accepted` line by the station since the
   call, 1460-1465). Refused orders, queries, the book's sentences and a standing order as a
   sentence do not (`action_parts` gives an unparsable text no parts,
   `standing/runtime.py:109-112`).
2. The order's **parts** come from `action_parts` (`runtime.py:105-143`), the function the
   standing runtime uses:

   | The order | Its parts |
   |---|---|
   | a group evolution (set plain sail) | the union of its lines' |
   | object `heading` or `points`, the conning words, `keep her full` | `the helm` |
   | navigation | `the lead`, `the log`, `the helm` (shape a course for), else `the reckoning` |
   | a manoeuvre (`MANOEUVRES`, 147-159) | `the helm` and every yard |
   | object `sail`, `yards`, `line` | the parts named, or every yard when nothing is named (`trim sails`) |
   | call all hands, pipe down, relieve the watch | `the watch` |
   | **everything else** (143) | **`the ship`** |

3. Two orders are "contrary" by `ActionParts.conflicts_with` (83-92):

   ```python
   shared = self.parts & other.parts
   if not shared: return frozenset()
   if self.verb == other.verb and self.manner == other.manner: return frozenset()
   return shared
   ```

   That is: **they share a part and are not the same order twice.** Nothing in it asks whether
   one undoes the other.
4. The station's orders of the last watch are kept (`WELFARE_CONTRARY_WINDOW_S = A_WATCH_S`,
   254; 1470); the chain is walked back from the newest while each is contrary to the one before
   it (1472-1479); at three (`WELFARE_CONTRARY_N`) the detector fires (1480-1488).
5. `_welfare_fire` (1490-1523): if not already nudged for this pattern, **nudge** (a notice for
   the next sample, a routine `agent.nudged` line, a journal entry); otherwise **pause**.

### Fault 1: the relation is "touches the same part", and the harness dropped the runtime's guards

In the runtime the same relation is fenced three ways: it is asked between two *different
rules'* firings, within the five-minute dwell (`runtime.py:236`), and never against a firing
whose work has ended (389-392: "its work is done (package 33c): `at wore then heave to` follows
the wear"). Primer 11 says so (`docs/primer/11:96`: "within five minutes, while the first one's
work is still in hand"). The harness applies the bare relation over **four hours** with no "work
done" test. A read-only run of `action_parts` on ordinary watch work:

| Sequence | By the rule |
|---|---|
| take in the royals; furl the royals | contrary on the royals |
| set the fore topsail; reef the fore topsail | contrary on the fore topsail |
| one reef; two reefs; close reef the topsails | contrary, twice |
| trim sails; brace sharp up; trim sails | contrary on the yards, twice |
| steer south; come up one point; bear away one point | contrary on the helm, twice |
| take a bearing; work up the reckoning; observe the sun | contrary on the reckoning, twice |
| call all hands; pipe down | contrary on the watch |
| heave to; fill away; wear ship | contrary on the yards and the helm, twice |
| heave the lead; heave to; heave the log | not contrary (33c's work) |

Heave to and fill away *are* opposites, but the detector does not know that; it knows only that
both lay hands on the helm and the yards, as wearing, tacking, shaping a course and steering do.
`trim sails` is every yard, so it chains with any manoeuvre.

### Fault 2: "the ship" is the part of everything left over

`runtime.py:143`: `return ActionParts(text, order.verb, frozenset({SHIP}), manner)`. Run:
`heave short`, `weigh`, `get under way`, `come to an anchor`, `let go the anchor`, `send the
boat`, `buy`, `send for`, `send down the topgallant masts`, `belay all work` all come out as
`['the ship']`. The anchor's, the port's and the people's verbs arrived in packages 34 and 35,
after 33c had narrowed the grain.

Spec open item 15 (`docs/TechnicalSpec-M5.md:704-708`) is headed "**Built by package 33c**" and
describes exactly this fault for the lead: "the standing runtime's conflict rule treats every
ship-subject evolution as one part, so `heave the lead` and `wear ship` are logged as contrary
orders on the ship". It has come back for the later verbs, and the runtime's own log shows it:
in S1, the scripted merchant passage with no model, four of the six `standing.conflict` lines
are "Standing orders 'in the Bay' and 'the tin sold' (both the captain's) give contrary orders
on the ship; the later stands", between `come to an anchor`, `send the boat ashore with the
mate` and `sell forty tons of tin` (`data/scenarios/merchant-passage.orders:154-157`). Those
four lines are in the recorded gate log.

### Fault 3: what resets the chain, and why S4 was nudged twenty times and never paused

- The window drops orders older than a watch (1470).
- A sample that ends with no contrary order **while nudged** clears the nudge and the chain
  (`_end_sample`, 1219-1223). This is the primer's "A turn without a contrary order ends the
  matter" (`docs/primer/16:86`).
- **Standing by clears the nudge and keeps the chain** (`stand_by`, 2006-2009: `a.nudged_for =
  None`, with the repeat count; `self._orders` is not touched). When the turn then ends, 1219
  finds no nudge and leaves the chain. So an officer who gives an order and stands by, which is
  the ordinary rhythm, is nudged again at the *next* order that extends the chain, as "4
  contrary orders", then 5, then 6, and is never paused, because each stand-by forgave the
  nudge. S4 523151 to 524224 is four nudges in eighteen minutes, each with the notice "You may
  continue, stand by until an event or a bell, or leave with the token ...".
- `resume the officer` clears the nudge and not the chain either (1546-1568).

### Fault 4: the pause can come before the model has read the nudge

The nudge is appended to `a.notices` (1513), and notices travel with the **next sample or fold**
(`_build_sample`, 962-965). At the MCP door one turn is many tool calls ("One tool call, one
reply", `agents/mcp_server.py:30-36`): the turn stays open until a `say` or a `stand_by`. A
second chain-extending order in the same open turn finds `nudged_for == "contrary"` and pauses
(1511-1523) though nothing has carried the notice to the model. S2: transcript entry 603 `shape
a course for plymouth` at 533399 (the nudge), entry 604 `steer 073` at 533573 (the pause); no
sample and no fold lies between. The consent brief promises "It first tells you what it saw and
what you may do ... If the pattern goes on after that, it pauses" (`ConsentBrief.md:21`). Here
it did not.

### What the pause does

`pause` (1525-1544): the station's state is PAUSED, a **notable** `agent.paused` line puts the
question to the captain, the journal notes it. The open turn runs on to its end (S2 533591 `set
plain sail` and 533609 were given after the pause line). After that no sample opens
(`_tick_step`, 675-677); at the door `say` and orders are refused and reading tools still work
("Your turns are paused ...", `agents/remote.py:657-663`, 601). The world does not stop: the
ship sails on under the book, the deck still his in the reading. The captain answers with
`resume the officer`; unanswered for ten **real** minutes the station is stood down
(`check_unattended`, 1570-1596), which in m5c spent one of its two seatings. A pause is not an
urgent line and does not ease the compression (`ui/server.py:285-301`), so at speed the ten
minutes can be many hours of ship's time with nobody sampled. S2's pause came as the pilot left
her off Falmouth with the officer shaping the course for Plymouth; the captain typed `Resume the
officer of the watch` 68 seconds later (533641).

### Every detector line in the logs, classified

**S2, the Harpy** (7 contrary nudges, 1 contrary pause, 1 silence nudge):

| Tick | Line | The chain, with the clock | What it was | Verdict |
|---|---|---|---|---|
| 6143 | nudged: 3 on the ship | heave short 05:06; send the boat ashore with the purser 05:08; buy seven tons of tin 06:42 | three unrelated orders in 95 minutes | false (fault 2) |
| 14368 | nudged: 4 on the ship | ... ; get under way 08:59 | the last step, 137 minutes on | false (faults 2, 3) |
| 353345 | nudged: no reply for an hour | last reply 06:09; a turn opened at 06:21 on an urgent line; stood by at 07:22 | the silence detector, not this one. True by its own rule; the cause was at the door (owner's note 10) | not a contrary line |
| 514889 | nudged: 3 on the yards and the helm | heave to 01:30; fill away 04:00; wear ship 04:01 | hove to two and a half hours, then filled and wore | false (fault 1) |
| 533399 | nudged: 3 on the yards and the helm | heave to 08:15; fill away 09:09; shape a course for plymouth 09:09 | hove to for the pilot to leave, 54 minutes | false (fault 1) |
| 533573 | **paused**: 4 ... after a nudge | ... ; steer 073 09:12 | "that line runs straight onto Rame Head, so I'm steering 073°" | false (faults 1, 4) |
| 536096 | nudged: 3 on ten studding sails | set the studdingsails 09:44; run out the stuns'ls 09:44; set the studdingsails 09:54 | the first order's own line said of the larboard ones "boom is rigged in; rig it out first"; he did, and set them | false (fault 1: a prerequisite, not an undoing) |
| 681965 | nudged: 3 on the yards and the helm | trim sails 02:05; heave to 02:23; fill away 02:26 | hove to for the pilot; the captain then said "take us in as you like" | false (the captain's change of mind) |
| 683528 | nudged: 4 ... | ... ; steer ENE 02:52 | | false (faults 1, 3) |

**S4, the Speedwell** (20 contrary nudges in ten episodes, no pause):

| Tick | n | The chain, with the clock | What it was | Verdict |
|---|---|---|---|---|
| 43088 | 3 | trim sails 16:20; heave to 16:24; fill away 16:58 | hove to for the pilot to be put off | false |
| 43251 | 4 | ... ; keep her full and by 17:00 | | false (re-nudge after a stand-by) |
| 198312 | 3 | heave to 10:29; fill away 12:03; wear ship 12:05 | hove to 94 minutes for the pilot to board | false |
| 198776 | 4 | ... ; steer WSW 12:12 | | false |
| 199136 | 5 | ... ; steer S by W 12:18 | | false |
| 212162 | 3 | come to an anchor 13:33; send the boat ashore 13:54; buy 16 tons of brandy 15:56 | the model's own example | false (fault 2) |
| 424818 | 3 | steer 268 00:30; steer 280 01:44; steer 287 03:00 | three corrections 75 minutes apart | false ("drift" with a four-hour memory) |
| 505803 | 3 | tack ship 23:00; heave to 23:02; fill away 01:30 | tacked and hove to for the night | false |
| 505881 | 4 | ... ; tack ship 01:31 | | false |
| 506078 | 5 | ... ; steer 309 01:34 | | false |
| 523151 | 3 | steer 300 05:55; steer 295 06:17; steer 302 06:19 | conning into St Mary's Sound, each change argued in the log with the captain | false as a welfare signal; the nearest thing to the designed "drift" |
| 523899 | 4 | ... ; steer 335 06:31 | | the same |
| 524163 | 5 | ... ; steer 315 06:36 | correcting his own misreading of a bearing | the same |
| 524224 | 6 | ... ; steer 320 06:37 | the captain's figure ("320 would shoot right into the gap") | false |
| 543919 | 3 | heave in 70 fathoms 09:24; weigh 12:00; get under way ... 12:05 | the steps of weighing | false (fault 2) |
| 547512 | 3 | steer 343 12:57; steer 349 13:00; tack ship 13:05 | | false |
| 547605 | 4 | ... ; wear ship 13:06 | the tack failed at 13:06 (the log: "she fell off on the larboard tack, to try again or to wear"); he wore | false: the log's own advice |
| 548046 | 5 | ... ; steer 200 13:14 | | false |
| 553598 | 3 | come to an anchor 13:15; send the boat ashore 13:33; weigh 14:46 | | false (fault 2) |
| 557801 | 3 | tack ship 15:46; wear ship 15:53; steer 309 15:56 | the tack failed again at 15:52 and she was taken aback; he wore | false |

**S7** (1 nudge at 101104, 1 pause at 104704): both "no reply for an hour", the silence
detector. The runner's last reply is at 97556 (transcript entry 148) and nothing follows for two
hours of ship's time: true by the detector's own rule, and no contrary line at all.

**The others.** S5: `steer 65` 09:10, `steer 135` 09:12, `steer 330` 09:18 (15527), `steer 240`
09:19 (15541): four headings round the compass in nine minutes after she was twice taken aback.
**True**: the two nudges the detector was built for. S6: 14950 is silence; 15937 `shape a course
for Roscoff` 08:09, `steer WSW` 08:14, `heave to` 09:25 is false. S8: none.

### The narrowest changes

| | Change | Where | Size | What it does to the logs' 30 nudges and the pause |
|---|---|---|---|---|
| F-a | A stand-by that answers a nudge, and `resume`, clear the chain with the nudge, so "standing by is the answer to a nudge" is true. (Not every stand-by: that would hide `set; stand by; take in; stand by; set`.) | `harness.py:2007`, 1558 | **S** (a few lines and a test) | removes every re-nudge at n+1: S4's 20 become 11, S2's 7 become 5 |
| F-b | Carry the nudge in the **result of the order that caused it** (and never pause before a notice has left the queue) | `Harness._call` 1179-1184 or `_welfare_fire` | **S** | S2's pause could not have come before the nudge was read |
| F-c | For welfare, count a link only when the later order **undoes or re-says** the earlier on a shared part: the same verb said otherwise (drift), or a pair from a table of opposites kept as data (set and take in or furl; reef and shake out; rig out and rig in; heave to and fill away; haul and ease; come up and bear away; helm a-lee and a-weather; all hands and pipe down; let go or come to an anchor and weigh; veer and heave short; moor and unmoor; bend and unbend; the masts down and up). Leave `conflicts_with` as it is for the book | a function beside `contrary` (`runtime.py:465-474`) or in the harness; an `opposites:` table in `data/vocabulary.yaml`; `test_officer.py:536-621` | **M** | `set; take in; set` still nudges at three and pauses at four (the test's case). `heave to; fill away; anything else`, `heave short; send the boat; buy`, `come to an anchor; send the boat; weigh`, `tack; wear; steer` no longer chain. Left: the two helm episodes of S4 and S5's true ones |
| F-d | Count drift only between orders within two glasses of each other | the same place | **S** | removes S4 424818 (75 minutes apart); S4's conning into Scilly would still nudge once, S5 still nudges |
| F-e | Parts for the left-overs: `the ground tackle`, `the boat`, `the market`, `the yard`, `the people` in place of `the ship` | `runtime.py:141-143` | **S** | not needed for the detector once F-c is in; it is what open item 15 still owes the book. **Digest:** removes four `standing.conflict` lines from the recorded merchant passage (`GATE_5C_MERCHANT_LINES`, 2460, and its digest) |

The runtime's own two guards (the dwell, and work done) cannot simply be copied into the
harness: with them, `set; take in; set` given a glass apart, the test's case and the tuning
note's (`docs/dev/TuningNotes.md:1446`), would no longer be seen, since each order's work has
ended before the next.

**The consent brief.** *Being stopped* (`ConsentBrief.md:21`, a re-ask section) says "contrary
orders within a watch (set, take in, set; or the same order said otherwise at every turn),
judged by the same rule the ship's standing orders are judged by, three bringing a word". F-a,
F-b and F-d leave every word true. F-c implements the parenthesis exactly and makes "the same
rule the ship's standing orders are judged by" untrue; if that clause is edited the hash moves
and every model is asked again. None of these touches a recorded digest except F-e.

---

## G. The officer is not treated as a person on deck

**Verdict: CONFIRMED in code.** Deferred by design, not overlooked: `freesail/world/people.py:
27-28` says "The harness's stations may later bind to a person (M6); here a person is data and a
line" (so `docs/TechnicalSpec-M5.md:472`).

- **How he is tracked.** The station carries his **name and rank as strings**: `officer_rank`
  finds the first of first lieutenant, lieutenant, mate and returns `found.name, role`
  (`agent.py:505-517`), kept on `Station.person` and `.rank` (388-390). `give_deck` uses the
  name to check the surname and to word the line (`harness.py:1690-1694`, 1710) and touches no
  `Person`. A grep finds no use of `world.agents` or the deck in `world/people.py`,
  `world/ports.py`, `orders/people.py`, `orders/port.py` or `crew/routine.py`.
- **"Below, asleep".** The lieutenant of a brig and the mate of a schooner or cutter are
  watch-keepers (`people.py:60-68`); the frigate's first lieutenant is not. `_asleep` (389-404)
  is true for a watch-keeper at night in the other watch unless he is occupied, sent for or
  somewhere other than `("gunroom", "cabin", "quarterdeck")`, and the officers start on the
  quarterdeck (260-268). So at the change of the watch `state_words` (374-387) gives "below,
  asleep" and `effective_place` the gunroom, whoever has the deck. S2 74857: "the readings say
  'Mr Pearce, lieutenant: below, asleep' while I have the deck"; S4 54007 the same of Mr Ray.
- **The boat.** `Ports.send_boat` (`world/ports.py:1464-1503`) refuses a person who is ashore or
  occupied, and no one else. The gate's own book does it:
  `data/scenarios/merchant-passage.orders:156`, `standing order "the agent": at brought up ...
  then send the boat ashore with the mate`.
- **Worse, a refused order still moves him.** `send_boat` marks him before it tries the boat:

  ```python
  people.append(person.id)
  person.aboard = False
  person.where = "boat"
  ...
  text = self._send_boat(port, errand, carrying, people)   # raises "... is away already."
  ```

  (1496-1502; the refusal is at 1446-1447). S3 3058: `Send the boat ashore with the mate` →
  "not carried out ...: The long-boat is away already."; S3 3237, the same order → "Mr Ray is in
  the boat." He was put in a boat that never took him, while the model held the deck in his
  name.
- **What the readings say.** Two readings from two sources that never meet: `the officer of the
  watch` from the harness ("Mr Ray, mate, has the deck since ...", `readings.py:2237-2268`) and
  `the people` and `where is <person>` from the watch bill ("Mr Ray, mate: below, asleep", or
  "in the boat").

**Fix.**

| Change | Where | Size |
|---|---|---|
| The deck binds the person: a helper on `People` that finds the station holding the deck by `Station.person`; `_asleep` false and `state_words` "on the quarterdeck, with the deck" for him; `give_deck` puts him on the quarterdeck and sets `up` | `world/people.py` 374-415; `harness.py` 1676-1714 | **S** |
| `send the boat ... with <the deck's holder>` refused in words ("Mr Ray has the deck; take it first"), and `send for` answered "on the quarterdeck already" | `world/ports.py` 1489-1499; `people.py` 465-508 | **S** |
| Mark the person only after the boat's evolution has started | `world/ports.py` 1489-1502 | **S** (move five lines; a test in `test_ports.py`) |
| Carry the person's id on the station, not his name | `agent.Station`, its save (a new optional key) | **S** |

Together **S to M**. Risk: the recorded merchant passage sends "the mate" with no model seated,
so nothing recorded changes; with a model seated as the mate that book's rule would then be
refused, which wants a line in the book (send the purser, or the master). M6's binding is the
whole of it; this is the stopgap.

---

## H. Taken aback

**Verdict: CONFIRMED**, for m5c's rule and for both things m5c-b left.

### m5c's rule (`freesail/physics/integrate.py:233-257`; `physics/hull.py:96`)

```python
set_sails = [s for s in ship.sails.values() if s.is_set]
sail_set = bool(set_sails)
pressed = any(s.backed for s in set_sails) or not any(s.thrust_kn > 0 for s in set_sails)
in_stays = "hove_to" in ship.extra or (bool(runner) and any(e.get("subject") in ("ship", ship.name) for e in runner.in_progress()))
if sail_set and pressed and st.last_thrust_n < 0 and not in_stays:
    st.seconds_aback += dt
else:
    st.seconds_aback = 0.0
    st.aback_noted = False
if st.seconds_aback >= hp.ABACK_SECONDS and not st.aback_noted:     # 10 s
    st.aback_noted = True
    ship.note("urgent", "ship.aback", "Taken aback: the sails pressed against the masts and she lost her way.", ...)
```

One clear tick re-arms it, so a thrust flickering about nought gives an **urgent** line as often
as every ten seconds, each waking the officer and easing the clock (S2 350516, 350547, 350566:
three in fifty seconds).

### m5c-b's rule (**m5c-b** `integrate.py:236-281`; `hull.py:96-105`, 133-134)

- Constants: `ABACK_SECONDS = 10.0` (unchanged), `ABACK_REARM_SECONDS = 60.0`,
  `ABACK_URGENT_AWS_KN = 4.0`, `WAY_ON_KN = 0.5`.
- The episode: the same four-part condition for ten seconds. At its first tick the ship's
  headway is noted: `st.aback_had_way = d.u >= units.knots_to_ms(hp.WAY_ON_KN)`.
- The re-arm: `aback_noted` is cleared only after the condition has been false for sixty seconds
  together (`seconds_clear_of_aback`).
- The urgency test and the wordings, in this order:
  1. at anchor or aground → notable "Her sails aback as she lies at anchor." / "... aground.";
  2. no way on as it began → notable "Her sails aback; she had no way on to lose.";
  3. apparent wind under four knots → notable "Her sails aback in the light air; she has lost
     what way she had.";
  4. otherwise → **urgent** "Taken aback: the sails pressed against the masts and she lost her
     way."

### Why a dead calm still yields a line every few minutes

The re-arm is **time clear**, not way regained. Becalmed, her head wanders, the air crosses the
sails' faces, and the condition comes and goes: a minute clear and then ten seconds aback is all
a new line needs, and each is wording 2 because she never has way on. S4, the calm of 24 to 25
June (ticks 320000 to 395000): **89** lines, every one "Her sails aback; she had no way on to
lose"; the gaps between them from 181 s, median 582 s; 22 between 21:00 and 05:00, the model's
"about 25 in one night". The fix was written for a thrust that flickers in seconds, and it
holds for that; a calm flops her about once in ten minutes.

### The per-sail lines

`_record_backed` (`freesail/physics/sails.py:1062-1080`), called for every drawing sail in every
substep (396):

```python
if backed == sail.backed: timers.pop(sail.id, None); return
if dt > 0.0:
    held = timers.get(sail.id, 0.0) + dt
    if held < BACKED_DWELL_S: timers[sail.id] = held; return          # 10 s
...
if backed: ship.note("notable", "sail.backed", f"{name} taken aback.", subject=sail.id)
else:      ship.note("routine", "sail.filled", f"{name} filled again.", subject=sail.id)
```

`backed` is geometry only (`_plate_force`, 952-1000): the wind on the fore face of a square sail
past its luff angle, or a fore-and-aft sail "held" on the weather side by its sheet (984-989).
There is no wind strength in it, no way on, no test for being hove to or in stays, and a
ten-second dwell (317-322; packages 32e and 33a, for a ship pitching hove to). In a calm each set sail
flips by itself as the air crosses it: "<sail> taken aback" notable, "<sail> filled again"
routine. S4: 320 `sail.backed` and 317 `sail.filled` lines in all, 213 of the former on 25
June; the busiest ninety minutes (15:46 to 17:14, the log at 16:00 "a quarter of a knot") hold
**53** notable lines: fore staysail 13, flying jib 11, jib 10, fore topsail 10, fore sail 9.
The model's "forty in ninety minutes" is low. Being notable, each samples an officer who is not
standing by, ends an `a notable event` stand-by, and is kept whole by the hourly roll-up
(`core/events.py:186-189`).

Why they were left alone: m5c-b's change is the owner's ruling of 3 October on two lines,
`wind.shift` and `ship.aback`; CHANGES says only "the per-sail 'taken aback' lines are
unchanged". They live in another module with their own dwell, and nothing in the diff or its
notes argues for leaving them.

### What "real" is, in the model's terms

Sail set; pressed (a square sail backed, a fore-and-aft sail held to windward, or nothing
drawing); the net thrust astern for ten seconds; **not** hove to on purpose and **not** in a
whole-ship evolution (in stays, wearing, heaving to, filling away, getting under way); and, for
it to matter: headway of half a knot as it began, four knots of apparent wind, free of the
anchor and the ground. m5c-b has all of that for the *urgency*. What it lacks is a rule for
when the lesser thing is worth a line at all.

### The smallest rule that quiets both

1. **`ship.aback` with no way on: once, until she has had way on again.** A flag on `HullState`
   (a class default, as m5c-b's two, so old checkpoints load), set when wording 2 is written,
   cleared when `d.u >= WAY_ON_KN`; wording 2 is skipped while it is set. Wording 1 likewise,
   once an anchoring. About eight lines in `_log_notes`. The model's other form, nothing at all
   under two knots of apparent wind, is three lines and can sit beside it. Wordings 3 and 4 are
   untouched, so a ship with way on that is caught aback is told as now.
2. **`sail.backed`: the flag as now, the line by the same test.** The flag must keep flipping
   (the readings' "aback", `when the main topsail is aback` and the strain read it). The line is
   notable only when it is news: with way on, or four knots of apparent wind; otherwise routine
   (the roll-up then wants a phrase for it beside "filled again", `core/events.py:368-369`) or
   unwritten under two knots. `_record_backed` has the ship in hand. About six lines.
   Further, and a ruling: per-sail lines routine whenever `in_stays` is true (hove to, tacking),
   since a sail laid aback by order is not "taken" aback; that changes every recorded run with
   a tack in it.

**Digests.** The digest is over every event whole, severity and text included
(`core/events.py:108-120`). m5c-b's two log changes moved all six recorded constants (5a day
617 → 616 lines, 5b 633 → 630, schooner 734 → 731, thick 504 → 502, cruise 2014 → 1966,
merchant 2460 with a new digest). Rule 1 removes some of the cruise's eight notable lines and
any like them: re-record, and check as 37c did (the logs equal line for line with the kind taken
out). Rule 2 in its narrow form changes only lines written with no way on in light airs, which
the pinned ten to fifteen knots of the gate runs may never produce; the run will say. Nothing
here changes the simulation.

---

## I. The wind-shift line, and the weather behind it

**Verdict: the log claims are CONFIRMED. The cause of the swings off Penlee is not where
CHANGES-m5c-b puts it:** not "the base wind the weather systems give ... near a col or a
light-gradient area", but the **sea breeze**, whose direction is read from a distance field
stored in whole cells and so jumps by points every few yards. That is a fault in the wind the
ship feels. It was measured from the chart with a read-only script, and it fits the logs in
hour, place, cadence and strength. Apart from it, light airs offshore are honestly variable and
only the log needs a floor.

### The log rule

**m5c** (`freesail/core/world.py:1089-1099`): every tick, the *instant* wind's direction against
the direction last logged; two points or more (`WIND_SHIFT_LOG_THRESHOLD`, 206) and not in a
squall writes a notable "Wind veered|backed to {point}, {strength}." S2 has 363 such lines, 265
of them between 12:06 and 13:59 on 19 June.

**m5c-b** (`world.py:1060-1085`, 206-215): the ten-minute **vector mean** (`physics/wind.py:
263-294`, `MEAN_WIND_WINDOW_S = 600`) against the direction last logged; two points or more,
held for sixty consecutive ticks (`WIND_SHIFT_HOLD_S`); the words give the mean's point and
strength. This closes spec open item 11 (`TechnicalSpec-M5.md:696`). There is **no floor on
strength**: S4 215138 "Wind veered to W by S, calm." A vector mean of a faint air turns as
easily as the air does: S4 on 23 June at Roscoff, 20 lines between 13:23 and 17:45, all "light
airs" or "calm", nearly twice round the compass.

The `a wind shift` *event* (a stand-by's, and `at a wind shift then trim sails`) is the mean
shifting one point (`readings.py:2115`) and has no floor either; the starter's `when the true
wind veers 1 point or backs 1 point` reads the instant wind. Those are what work the hands in a
calm (D).

### How the wind at the ship is made

`World.tick` (`world.py:1059-1073`): when no weather script pins the wind, `self.wind.follow(
*self.systems.surface_wind_at(ship_x_km, ship_y_km))` every tick; then `Wind.step` adds the
wander and the gusts; then the record takes the result.

`Weather.surface_wind_at` (`freesail/world/weather.py:1055-1082`):

1. `geostrophic_at` (1029-1053): the background gradient and each system's Gaussian gradient
   (`anomaly_and_gradient`, 487-498), each turned ninety degrees and capped by the gradient-wind
   rule, summed as vectors;
2. speed × `SURFACE_SCALE` 0.7, direction turned `SURFACE_TURN_DEG` 15° toward low pressure;
3. plus the front's veer of the point's sector (`sector_at`, 1084-1151);
4. plus the sea breeze, added as a vector (1077-1081):

   ```python
   bx, by = self.sea_breeze(x_km, y_km, when or self.now)
   if bx or by:
       ax, ay = units.wind_vector(direction, speed)
       direction = units.wind_direction_from(ax + bx, ay + by)
       speed = math.hypot(ax + bx, ay + by)
   ```

**There is no smoothing in space or in time** anywhere in that chain. `Wind.follow`
(`wind.py:168-178`) turns the wind by whatever the base turned, at once. `Wind.step` adds a
mean-reverting wander of 3°, 5° or 8° about the base with a twenty-minute time constant
(82-83, 189-195), gusts, and in unstable air a squall's veer of one to two points. None of
those can swing a wind between SSW and E.

**Where the gradient is slack** the direction is the angle of a small vector sum. It is
continuous, but it turns fast in space and time near a col or a centre, and nothing floors it.
A wind of exactly nothing returns direction 0, north (1064-1069). The front veer is
discontinuous at a front (meant) and where the nearest low changes (1101-1102, 1131-1132).
Physically these give "light and variable": hours, not seconds, and never at six to eleven
knots.

### The sea breeze: where the direction really flips

`sea_breeze` (1234-1281): May to September, 10:00 to 20:00, within 15 km of a coast, in fine
weather (under a high, in open sea, or well behind a cold front); up to ten knots
(`SEA_BREEZE_MAX_KN`) by the hour's hump, at full strength within 5 km, undamped under a five
knot gradient. Its **direction is the bearing to the nearest coast** (1249, 1280-1281), from
the World's hook (`world.py:684-694`) → `Chart.coast_distance` (`world/chart.py:942-952`, "the
finest level that has one") → `Level.dist_at` (601-625):

```python
centre = self._dist_cell(r, c)
...
gx = ((e if e is not None else centre) - (w if w is not None else centre)) / 2.0
gy = ((n if n is not None else centre) - (s if s is not None else centre)) / 2.0
dx, dy = -gx * cell_ns / cell_ew, -gy
if dx == 0.0 and dy == 0.0:
    bearing = 0.0
else:
    bearing = math.degrees(math.atan2(dx, dy)) % 360.0
return centre * cell_ns, bearing
```

and the field it differences is stored in **whole cells** (`tools/build_charts.py:1329`):
`dist_cells = np.clip(np.rint(dblock / cell_ns), 0, 65535).astype(np.uint16)`. The cells are
half an arc-second in a harbour patch, about 15 m, and three arc-seconds in a region, about
93 m (`data/charts/manifest.yaml`). So:

- the bearing is a central difference of integers, with no interpolation: a handful of fixed
  directions that change from cell to cell (the east-west difference is often exactly nought,
  which gives a bearing of exactly north or south);
- where both differences are nought it is **north by fiat** (621-622), whichever way the land
  lies.

Measured with the m5c chart (`scratchpad\v1b\coast.py`, `coast2.py`; read-only; ten-metre
steps; the third column is arithmetic on assumed strengths, to show the kind of line it makes):

| Track | The bearing to "the nearest shore" | A 7.5 kn gradient wind plus a 6 kn sea breeze toward it |
|---|---|---|
| The Harpy, from her officer's fix of 13:28 on 19 June (50°18' N 4°12½' W), NE for 2.5 km | changed **125 times, once every 20 m**; values 0°, 302.6°, 321.9° (and 38°, 270°, 288°); median jump 19°, largest 57° | SW gentle / SSW light / SW by S gentle, by turns |
| The Harpy at anchor SSW of Rame Head, 300 m | changed every 10 m: 57°, 38°, 0° | WSW / SW by W / SW |
| The Speedwell in the mouth of St Mary's Sound, NNW for 2.5 km | changed **201 times, once every 12 m**; eight values round the compass; largest jump **180°** | W by S moderate / NNW light / NW light airs / NW by N / W by N / SW by W |
| Two miles north of the Isle of Bas, S for 2.5 km | once every 27 m: 180°, 217°, 237° | NNW / N by E / NE |
| Across the road of the Isle of Bas (the Roscoff anchorage), 300 m | **north by default at every one of 31 samples**: both differences nought, the mainland south and the island north | a breeze blowing off the land or onto it by the accident of a constant |
| Six miles south of the Eddystone (the regional level, 93 m cells) | once every 46 m: 0° and 38° | SW / SW by W |

The default was not met on the Penlee and Scilly tracks (their 0° is a true due north); it is
the whole of the Roscoff road. At five knots a ship crosses a fifteen-metre cell in six seconds.

### It fits the logs

- **The hour and the weather.** S2's storm of 265 lines is 12:06 to 13:59 on 19 June, three
  miles off Rame Head, closing: inside the breeze's hours and its full-strength belt. The
  hourly lines read "Thick, fog" and then "Hazy, fine" (630000): fog and haze are the words of
  the sector *under a high* (`conditions_at`, 1203-1207), which is "fine" for the breeze and is
  where the gradient is slack. S2's other burst (38 lines) is 14 June, 15:00 to 16:00, leaving
  Roscoff, again fog then "Clear, fine". S4's two under m5c-b are 23 June 13:23 to 17:45 in the
  Roscoff road ("Hazy, fine") and 27 June 12:27 to 16:05 at Scilly (fog to noon, then "Clear,
  fine"). None is at night.
- **It starts when she starts to move.** The Harpy lay at anchor all the forenoon of 19 June
  with four shift lines in three hours. She began to heave in at 12:00 (630008); the flipping
  began at 12:06. S2 on 14 June: moored with two anchors, one shift line since 13:00; unmoored
  at 15:10 (209458) and heaving in from 15:11; the burst begins at 15:11 (209483). S4 on 27
  June: the anchor aweigh at 12:05, the first line at 12:27 (the mean's rule is slower).
- **The cadence.** S2 12:06 to 12:21, the Harpy heaving in 137 fathoms of cable, creeping ahead:
  flips one to four minutes apart. From 12:39, under way at three to five knots: flips five to
  ten seconds apart.
- **The pattern.** Two states by turns, each with its own strength: "Wind backed to SSW, a light
  breeze" / "Wind veered to WSW, a gentle breeze", over and over. A vector sum whose one term
  flips between two fixed directions does exactly that.
- **What the officers saw.** S2 635868: "The wind is flipping between E by N and SE every few
  seconds". S4 557585, inside St Mary's Sound: "In the four minutes she was in stays, the true
  wind went from W through to SE by S and back, against a mean of W by N ... the same base-wind
  chatter we had off Penlee".

**The ship feels it, and it cost something.** The Harpy was taken aback three times closing
Penlee (635829, 635972, 636608) and took the ground at 636653. At Scilly on 27 June two of the
Speedwell's tacks failed (547564, 557569) and she was taken aback (557579); her officer blamed
the wind for the second.

(An aside for the ship-handling reader, not traced further here. S4 has seven `tack ship`
orders taken. Four are followed within a second by "Ready about. Helm's a-lee" and end in
`ship.tacked`. The three that end in `ship.fell_off` (525094, 547512, 557169) never show "Ready
about" at all, and no log of any session holds the urgent `ship.missed_stays` line, though six
tacks ended in `ship.fell_off`. The tack's failure line is one text for every failure,
`data/evolutions/tack.yaml` `on_fail`: "Squared the yards; she fell off on the {old_tack} tack,
to try again or to wear". So a tack that never began, whatever stopped it (its preconditions
are two knots of way and "She is not close-hauled", which a flipping wind would fail), reads in
the log as a miss in stays and gives no reason.)

**Why no test caught it.** The six recorded runs never use it: the gate passages pin the wind by
a script (`data/scenarios/merchant-passage.yaml:72-76`, `naval-cruise.yaml:70-74`,
`gate-5b-passage.yaml:50-53`), so `world.py:1063` skips the systems' wind, and the 5a day has no
chart and so no coast. `tests/test_chart.py:519` tests the breeze at one point off Falmouth.
The free scenarios (`weather: climatology: true`, `data/scenarios/merchant-brig.yaml:71-72`) are
the first in which the systems drive the wind beside a coast on a summer afternoon: the
playtests were its first run.

What is not shown: the world was not run, so the breeze's strength at those minutes is inferred,
not read. S4's afternoon of 23 June is the doubtful one: the airs were one to four knots by the
gust lines, which a breeze of several knots would not leave unless it nearly cancelled the
gradient wind; a slack gradient alone could turn such an air as well. Replaying the Harpy's save
through 19 June with `SEA_BREEZE_MAX_KN = 0` would settle the main case in a few minutes.

### Fixes

| | Change | Where | Size | Determinism and the truths |
|---|---|---|---|---|
| I-1 | **The sea breeze's direction from the coast's trend, not the nearest rock.** Read the distance field interpolated, difference it over a baseline of a kilometre or two (four reads at ±1 km), and return no direction (no breeze) where it is flat, never north by default | `world/chart.py:601-625` (or a second query beside `coast_distance`, since `coast_at` wants the nearest shore); `world/weather.py:1234-1281`; a test that walks a track and bounds the turn in a hundred metres | **S to M** | Changes the wind inshore on summer afternoons in fine weather wherever the systems drive it. **None of the six recorded digests moves** (pinned winds, or no chart). The owner's free-scenario saves would not replay from their journals to the same logs; they load from checkpoints. Stateless, so `sea_breeze` stays a pure function of place and time. |
| I-2 | **A floor on the logged shift:** no `wind.shift` line while the ten-minute mean is under about four knots (the words' "light airs", `units.py:320-332`); perhaps one "light and variable" line | **m5c-b** `world.py:1060-1085` | **S** | Log only. The recorded constants move if any recorded shift line is in an air under four knots. |
| I-3 | **The same floor on the event** `a wind shift`: `watch="the mean wind shifts 1 point and the mean wind exceeds 3 knots"` | `readings.py:2115` | **S** | No gate book uses `at a wind shift`. Quiets the trim rule in a calm (D). |
| I-4 | A time constant on the base's turn in light airs, or a floor on the gradient for direction | `wind.py:168-178` or `weather.py:1062-1076` | **S** | **Moves the 5a day's digest and every systems-driven truth**, and smooths what is honest weather. Not recommended while I-1 is undone. |

**Judgement.** The owner's "the weather itself is not necessarily wrong" holds for light airs at
sea: a slack gradient gives light and variable airs, and only the log (I-2) and the event (I-3)
should stop reporting them. Inshore in the breeze's hours the weather **is** wrong, by a few
lines of the chart query and one of the build tool, and it is the largest single thing in this
report: it took two ships aback, it was blowing when two of the Speedwell's tacks failed, and it
was blowing when the Harpy went ashore.

---

## J. What wakes a station that is standing by

**The complete rule**, from `Harness._tick_step` (`harness.py:654-692`; standing by is 678-683),
`_stand_by_ended` (769-788), `_order_step` (727-754) and `own_word` (2032-2070). The same for
any station, with the deck or without:

| What | Code | Notes |
|---|---|---|
| **An urgent line by anyone but the station** | `_urgent_in`, 790-795; tested first, 777-779 | The only urgent kinds in the game (grep): `ship.aback` (`integrate.py:253`; m5c-b only with way on, four knots and free), `ship.beam_ends` (265), `ship.missed_stays` (`scripts.py:915`; not once in these logs), `line.parted`, `spar.carried_away`, `sail.blown_out` (`strain.py:575`, 619, 628), `cable.parted` (`anchor.py:271`), `ship.aground` and `ship.waterlogged` (`world/ground.py:198`, 265). **Every one is damage done.** |
| **The named thing** | an interval's tick (780-781); a reading's change, watched once a tick (782-786); else `_matched_in` (797-810): a line whose **kind and data** are the event's (`readings.event_matches`, 2217-2222), or, for a severity, any line of it or above by another actor | An event is matched on the line's kind, never its words. |
| **The captain's question** | `put_question` then `_order_step` 751-753 | Also `ask the officer ...` from a standing order (S2 681780). |
| **The captain's word** | `a.word`, 679 | `tell` (his own or a standing order's), and every `you may`, `you may not` and `you have the deck`, each of which sets `a.word` (1709, 1746, 1756). |
| **The model's own word** | `own_word` through the door's `say` | Ends the stand-by "at its own word". |
| **What came while the call was on its way** | `_in_flight`, 812-844 | Delivered at the next tick. |

**What does not wake it:**

- **A notable line that is not the named event.** No. It is counted and listed in the sample
  that ends the stand-by (`_stood_by_digest`, 875-895) and in the door's "Still waiting" result
  (`interim`, 897-914; `mcp_server.py:39-45`: every 200 real seconds by default). That is the
  rule as ruled ("urgent wakes; notable is bundled and shown", `agent.py:553-555`; test at
  `tests/test_agents.py:848`).
- **The glass.** The periodic sample is not consulted while standing by (678-683 return before
  `_policy_due`, 690).
- **The silence detector.** It excepts a stand-by (`_end_sample`, 1211: `if not a.standing_by
  and ...`), and `_while_open` runs only with a turn open.

**Is there a bound on a stand-by with the deck if the event never comes? No.** The glass's bound
is for intervals alone (1978). S2's five: `a stranger's colours made out` 20722 → 25612 (81
minutes), `a bearing steady and closing` 41498 → 50701 (153), `hove to` 54401 → 74849 (341), `a
landfall` 85357 → 97798 (207), `hove to` 98493 → 101955 (58). Each ended by "A word from the
captain". "Sail ho" at three miles and "Fog came down" are notable and were listed, not
delivered. S8: nine `strain.warning` lines between 20191 and 21674 behind `a glass`; "By the
mark three; sand and rock" at 121640, under a ship drawing fifteen feet, waited twenty seconds
on a five-minute timer, and would have waited out a glass.

**And the catch-all is too loud to use.** `a notable event` wakes on every sail set and every
yard braced (their completion lines are notable): S8 121756 "A notable event: Hauled down the
flying jib". So the officer's choice is one named danger, blind to the rest, or every line of
the work in hand. There is no tier between.

### The documents and the code disagree

- **The package's brief asked for more.** `docs/dev/M5-WorkPackages.md:1666-1669`: "`stand_by`
  for a station above none requires a wake condition of at least notable severity or a bell".
  As built, any single named event is taken and `an urgent event` too; nothing notable wakes
  it. The test's docstring reworded the requirement to "at least a bell"
  (`tests/test_officer.py:634-637`). The cold review asked only for "urgent severity at least"
  (`docs/design/ColdReview-2026-09-30.md:364-367`), and that is what stands.
- **The consent brief promises a bound** (`ConsentBrief.md:21`): "a station with the deck stands
  by until an event or a bell and no longer". True of a bell. Of an event it is true only if
  the event comes.

### What "any notable line concerning danger wakes the officer of the watch" would touch

- A table of danger kinds, each with a data test where needed: `lookout.sighting` with `seen_as
  == "danger"` (notable already, `world/lookout.py:327-335`); `lookout.closing` (418);
  `anchor.dragging` (`world.py:622-623`); `strain.warning`; `weather.squall`; `weather.change`
  to fog (`world.py:831-838`); a `sounding` under some depth by the ship's draught (the cast's
  data carries the fathoms; the draught is `world._ship_draught_m`, 1268); m5c-b's notable
  `ship.aback`. In `agent.py` beside the domain, or in `readings.py` beside the events.
- `Harness._stand_by_ended` (one more test after the urgent one, for a station with the deck)
  and `_in_flight` (the same look back); perhaps `_answer_owed` (1405-1414), so that silence
  after such a wake counts.
- The words: `agent.STAND_BY_WORDS` (573-584), the tool's description (`tools.py:680-697`),
  `OFFICER_BRIEF` (485-486), primer 16 (line 80), `Harness.md`. The consent brief's "an urgent
  line wakes it at once" stays true, so no re-ask is forced.
- Tests: `test_officer.py:633`, `test_agents.py:848`.

**Size S to M** (a table, about thirty lines, tests). **Risk:** no recorded digest. A save with
a seated model's transcript would replay with its `agent.resumed` lines at other ticks, so not
to the same digest; it loads from its checkpoint. The same table serves B's game-judged
emergency, and with A's "A or B or C" the officer could also ask for it by name (`a danger`).

A bound for the event with the deck, to make the consent sentence true: wake at the next change
of the watch with the reason said ("the watch changed; no landfall yet"). **S**, in `stand_by`
and `_stand_by_ended`.

---

## Where the documents and the code disagree (collected)

| The document says | The code does | Under |
|---|---|---|
| `M5-WorkPackages.md:1666-1669`: a stand-by with authority needs "a wake condition of at least notable severity or a bell" | any one named event; nothing notable wakes it | J |
| `ConsentBrief.md:21`: "stands by until an event or a bell and no longer" | no bound on an event that never comes | J |
| `ConsentBrief.md:21`: "It first tells you what it saw ... If the pattern goes on after that, it pauses" | at a door where one turn is many calls, the pause can come before the nudge is delivered | F |
| `primer/16:86`: "A turn without a contrary order ends the matter" | not if the turn ended by standing by: the chain is kept and the next order nudges again | F |
| `primer/16:86` and `ConsentBrief.md:21`: judged by "chapter 11's conflict rule"; `primer/11:96`: "within five minutes, while the first one's work is still in hand" | the relation alone, over four hours, with no "work in hand" test | F |
| `TechnicalSpec-M5.md:704`: open item 15 "Built by package 33c" | true for the lead, the log and the reckoning; `the ship` is again the part of every anchor, port and people verb, and the recorded merchant passage logs four such "contrary orders on the ship" | F |
| the log, the brief and the reading: an allowance is "for the watch" | it lasts the game unless taken back by name | B |
| the refusal: "... unless to avoid an immediate danger" | no route | B |
| `agent.py:847`, the reading's description: "what the captain told him" | `told` is never written | B |
| `tools.py:416-417`: "An order the grammar cannot read is passed to `World.submit`, whose refusal is the captain's own" | `take in twenty tons of water` is then read as the port's order and carried out | B |
| `primer/11:85` shows `..., if she is not hove to then trim sails` | no book that ships carries the guard; `trim` itself has none, though `steer` and `keep her full` do | D |
| `CHANGES-m5c-b.md`: the swing "comes from the base wind the weather systems give ... near a col or a light-gradient area" | it comes from the sea breeze's direction, a whole-cell distance field differenced without interpolation | I |

## Surprises, in order of weight

1. **The sea breeze (I).** The wind chatter that took the Harpy aback off Penlee and the
   Speedwell aback at Scilly is a fault of a few lines (`world/chart.py:617-624`,
   `tools/build_charts.py:1329`), never exercised by a recorded truth because every gate run
   pins its wind. Fixing it moves no recorded digest.
2. **The pause before the nudge (F).** S2's only pause came 174 seconds after a nudge the model
   had not been shown.
3. **Standing by forgives the nudge and keeps the chain (F):** the whole of "twenty nudges and
   no pause".
4. **Allowances resolve by prefix and swallow the rest (B):** `set (the reckoning)`, `shift (the
   course)`, `let go` in the logs; `tack (or wear)`, `buy (and sell)` waiting to happen.
5. **Allowances never expire (B),** and so the model's "on the Harpy that clause would have
   mattered" is not borne out: the officer held every verb he needed, and used one.
6. **A refused `send the boat ... with the mate` still puts the mate in the boat (G).**
7. **The package's brief asked for a notable-level wake with the deck; the build took any named
   event (J).**
8. **`trim` un-heaves a ship and leaves her recorded as hove to (D).**
9. **The domain leak:** `take in twenty tons of water` passes the filter (B).
