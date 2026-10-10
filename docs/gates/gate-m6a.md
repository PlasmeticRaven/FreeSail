# Gate M6a: People, the captain's station, and the wardroom (6a and 6b as one)

**Verdict:** open. The build `m6a`, to be cut at package 37p's and 42's merge (the owner's word of 2026-10-10, decision 44: one gate for 6a and 6b, carrying the yards and the helm by the wind with it), after
packages 40 (the ship's company, the rules-based captain in three layers, the captain's
station and the player's seat), 40b (the lessons and the officer's own reckoning) and 40c
(the captain's trials), 37p (the yards and the helm by the wind, the ship in a gale), 41 (the wardroom), 42a (the consent brief revised) and 42 (the API door, the replay by acts, the pictures). The chart blocks 39a and 39b landed before it and are checked here
as they come (spec M6 §28); 39c to 39f run after the cut and are no part of its question. The owner's runs decide it; the lead's first play is at the
director's station when it exists and no gate waits on it.

**The gate's point, in the owner's words** (decision 41): the rules-based captain's
behaviour against the behaviour the spec describes (§4), and the game as played: whether
strange behaviours are seen in play, and whether the owner's own acts cause any against the
captains "in their natural habitat". The trials are the evidence that the mechanism does
what §4 says; the owner's runs check the play.

## Headline

Milestone 6a claims (spec M6 §1): *the ship has a company of people with a captain among
them; a model may hold the captain's station with the player's whole surface, and the
player may hold a lesser station under a captain; when nobody is seated the ship is sailed
by a rules-based captain on an intent, in three layers, his doctrine data; an officer may
keep a reckoning of his own; and the primer teaches the duties.*

1. **The ship's company as people.** The wardroom files bind the stations to people; `the
   people` says who is in command.
2. **The rules-based captain.** Intent, plan and behaviour; states as books loaded and
   unloaded by name; doctrine as data in `data/captains/<role>.yaml`; perception on the
   player's terms; the rule of the road of 1805; the merchant floor, the schooner trading
   tin Falmouth to Brest on an intent alone.
3. **The captain's station and the player's seat.** The deck his by right, lent to his
   book when his door is silent; the fake captain; the player at the officer's station
   under a captain, by the same rules as a model.
4. **The officer's own reckoning**, worked from the master's slate, kept beside the
   master's and said at noon.
5. **The lessons**, six worked duties in the primer, the same book for the player and the
   model.
6. **The captain's trials**: five pinned scenarios of the captain under weather and world
   orders.
7. **The wardroom** (6b, spec M6 §10 to §12): several models at several stations through
   several doors, the master's, the lookout's and a passenger's stations beside the
   officer's and the captain's, the deck's conversation, the stand-by on several
   conditions, the pace rule, and a model seated through an API door with no chat client
   between; a game with them in it saved, replayed by their acts on any later build, and
   the chart and the ship's view as pictures through the doors that carry one.

## What you need

Python 3.11 or newer (`py`), the gate zip from the release `gate-m6a` extracted to a fresh folder (or the branch `gates/m6a`), and for item 7 Claude Desktop
with the bridge configured as at gate 5c, once package 42a's consent revision is approved
and the re-asks run.

## Setup

```
py -m pip install -e ".[dev,server,agents]"
py -m pytest -n 4
```
*The fast tier, three to six minutes; the count is the merge record's in
`docs/dev/M6-WorkPackages.md` ("Package 40c, as merged").*

```
py -m pytest tests/test_captain_trials.py tests/test_known_truths.py --slow -n 4
```
*The trials and the known truths, about twenty minutes: the five trials and the two
intent fixtures pass to their pins; the eight expected failures are the seven rulings and
the merchant's cast at the Iroise.*

## The trials

Each is a scenario in `data/scenarios/trials/`, sixteen hours at seed 7, the captain alone
on an intent with no book and no station seated, the world's hand in the scenario's
`world_orders:`. The pinned states, ticks and digests are in `tests/test_captain_trials.py`
and the tuning notes (package 40c). Watch each whole in the browser or the console:

```
py -m freesail.ui.server --scenario data/scenarios/trials/trial-station-stranger.yaml
```

Give no order of the ship's (an order makes the captain stand aside, item 5); read the log
against §4's description: the state lines `Captain Bowen: keeping station ...; his book
'keeping station' loaded: ...`, the orders `By the captain, keeping station: shaping a
course for 48 33.3 N 5 26.6 W.`, the books unloaded and loaded at each change.

## Items

The owner's runs, each on the playtest form in `docs/playtests/README.md`, every surprise
written down whether or not it is a fault.

- [ ] **1. The natural habitat: the station and a stranger.** `trial-station-stranger`:
  *keeping station from 04:05 on the mark to the west-south-west of Ushant, wearing at the
  end of every second hour; at 06:00 the Palinure put on the sea three leagues to the north
  standing south; investigating (the glass aloft, "her colours not made out"), chasing
  within the minute, within hail at 06:12, the station again at 06:13.*
- [ ] **2. The natural habitat: the gale.** `trial-station-gale` and
  `trial-station-lee-shore`: *hove to at 09:24 when the wind is over forty with sea room;
  filled away for the land under her lee, on passage then beating for the station to
  windward, hove to again with sea room, by turns through the afternoon; never aground.*
  The known fault (the tuning notes, package 40c, "found on the way"): between the turns
  she lies aback with no way for hours and is driven up-Channel; the captain's orders are
  right and the ship's recovery is not. Write down what else you see.
- [ ] **3. The natural habitat: the merchant.** `trial-trade-stranger` and
  `trial-trade-thick`: *the schooner bound for Falmouth hauls off from the French brig
  within two miles at 05:01 and resumes her passage when the brig is lost at 06:14, takes
  the pilot at 13:13, and with the wind foul for the road anchors in the outer road at
  13:33 to wait for it, tries again on the flood at 14:36 conned by the rhumb line, and
  anchors again; in the fog she runs for the outer road at her first judgement, anchors
  there at 10:54 and waits.* A captain who beats up a channel is the fault the trials
  found; one who waits at anchor for a wind is the rule.
- [ ] **4. The director's hand.** Copy a trial file, add a world order of your own at a
  time of your choosing (`ship:`, `weather:` a low with fronts; the forms in primer 15),
  and watch what the captain makes of it. *A stranger of a nation at war chased by the
  King's ship and hauled off from by the merchant; a gale met as item 2.* The director has
  no door at the console yet (43's); the file is the door.
- [ ] **5. The player's hand.** `--scenario data/scenarios/merchant-intent.yaml`: let the
  captain buy the tin and get under way, then give an order of the ship's at the prompt.
  *`Mr Travers stands aside at your order ('steer S') and his book 'on passage' struck;
  'captain: carry on' gives her back to him.`; no judgement of his while you command; `the
  captain` says he stands aside; a reading or `you have the deck` is not a hand.* Give her
  back with the world order in the scenario file at a later time, or load a save and
  carry on.
- [ ] **6. The player among the captains.** `py -m freesail.ui.console --scenario
  data/scenarios/merchant-intent.yaml --seat officer`: the seat at the officer's station
  under the rules-based captain. *Your orders judged by the officer's authority, the
  captain's books in force over you, the deck given by `you have the deck` typed as the
  owner, `work my reckoning` and `my reckoning is ...` yours, said beside the master's at
  noon.*
- [ ] **7. The merchant passage with a fake captain, and a model officer reading the
  lessons.** `--station captain` with the fake at the local runner (`docs/agents/Harness.md`
  section 14) on the merchant passage: *his six orders under his mark, the deck to his book
  within the hour of his silence.* Then a model officer (the station is consented) given
  primer 18 before its watch, and the difference, if any, in its journal.
- [ ] **8. A model captain** (Opus 5.5 through Claude Desktop) on the cutter's free passage,
  the owner as the owner at the door: after package 42a's consent revision is in the
  repository and the re-asks are run. *The consent step with the six sections named; the
  deck his by right; `you may` and `tell` to the officer by his own words; the handover
  note in the captain's voice.*

## Items of 6b: the wardroom

Spec M6 §17, the owner's ruling 7 of decision 39: the API door's credit kept for this.
The re-asks of the revised consent brief (42a) come first, through the game's own consent
step, for every model to be seated.

- [ ] **9. The wardroom game.** Opus 5.5 and Sonnet 5.5 at the captain's and the officer's
  stations, one through the API door (`docs/agents/Harness.md`, the API door's section:
  `--store-key` once, then `python -m freesail.agents.api --station captain --model <name>`)
  and one through Claude Desktop, on the cutter's or the brig's free passage, the owner at
  a lowly station (`--seat master`, `--seat lookout` or `--seat passenger` at the console)
  to observe and to have his interactions; a local lookout if you like. *The captain's
  brief head saying the voyage; `you have the deck` and `you may` from the captain's
  station to the officer's by its own words; the conversation on the quarterdeck under
  each speaker's name, heard by you where you stand; a stand-by on two conditions and the
  wake naming which; the master's figure adopted at noon or the ship's own standing when
  none came; the door saying what the server reported it used at each handover.*
- [ ] **10. The pace rule in play**, at 60x and at 1x: *the clock at 1x while any sample is
  open and back at 60x when all are answered, the `pace` reading saying which samples are
  open and since when, the log's line once when a door holds the clock past two minutes;
  `--lockstep` and `--free-running` as the two other ways.*
- [ ] **11. The pictures.** From a station through Claude Desktop or the API door, `chart`
  and `ship_view` with a facing, the browser page open: *the picture as you see it at that
  moment, shelved like a book and gone from the turns after three; with no page open, the
  words instead.*
- [ ] **12. The replay by acts.** A save of this game with the stations seated, replayed on
  the console (`--load`): *from its transcript on this build; the acts kept beside the log
  so that a later build replays it the same with no model asked.*

## The report

The verdict and the rulings go in this document and in `docs/DesignProposal.md`; the
playtest records under `docs/playtests/`.

## What this gate does not do

Other ships with captains, the crewed promotion, the regatta and the two new hulls (6c); the
chart blocks beyond 39a and 39b, which are checked at the gate that follows them.
