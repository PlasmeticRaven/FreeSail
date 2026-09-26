# Gate M3: The crew

**Verdict:** Pending.

## Headline

Milestone 3 claims:

1. **The crew is real.** Each ship musters her company from the seed: the frigate's 264 souls (twelve officers, 182 seamen, 40 marines, 30 idlers by trade) and the schooner's forty, every hand with a name, a rating, a station and a watch, as the ship's books of 1805 would have them. `muster` reads the watch bill.
2. **Orders take hands and time.** Every evolution asks for so many hands of a rating from its stations, and the watch on deck is the pool. Enough hands, and the work goes at milestone 2's pace to the second; short, it goes slower and the log says so; too few, it waits. Two jobs cannot have the same topmen. All hands set plain sail three times as fast as the watch.
3. **The watch keeps the ship.** The watches relieve each other at eight bells, the dog watches turning the day; the idlers come up at six and go below at eight in the evening. All hands are called by the captain or by the work itself (tacking, wearing, reefing, sending down masts), come up over a minute and a half, belay the watch's work, and are piped down after. Hands tire; a night of calls makes a slow morning watch.
4. **The catalogue to thirty-nine.** Box-hauling, wearing short round, lying a-try, scudding, backing and filling, sending topgallant masts and yards down and up, striking and fidding topmasts, rigging studding sail booms out and in, bending, unbending and shifting sails, goose-winging, loosing sails to dry and furling all, each from Luce with its hands.
5. **The gale answered.** The gale of gate M2 item 9 carried the royals away. Now `send down the topgallant masts`, given in time, calls all hands off the light sails and brings the upper spars on deck, and nothing carries away.

## What you need

As before: Python 3.11 or newer (`py` works where `python` does not) and the gate zip extracted to a fresh folder.

## Setup

In a terminal in the extracted folder:

```
py -m pip install -e ".[dev,server]"
```
*Ends with "Successfully installed ...".*

```
py -m pytest
```
*Takes about eight minutes now: the truths sail real voyages with the crew aboard. Ends `886 passed, 3 xfailed` (the three xfailed are recorded exceptions: the two of milestone 2 and the absolute times of truth 18; a `failed` is a fault).*

## Checklist

Seed 7 throughout, wind from the north, so your numbers should match these within a few seconds of ship's time. The console's wind gusts a little, as at gate M2. Commands after `>` are typed at the prompt; a `tick` of many thousands takes a minute or two of real time.

### Part A: the frigate's company, in the console

```
py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **1. Muster and read the bill.** Type `muster`. Expect `Mustered the Amazon's company, 264 souls: twelve officers, 182 seamen, 40 marines and 30 idlers.`, then `The starboard watch has the deck, the idlers below: 111 hands on deck.`, a line per station (`Fore topmen, 24 (10 able, 14 ordinary): 12 on deck, 12 below, none at work; fresh.`; the marines and idlers with no ratings), the seamen by rating, the idlers by trade, and the officers from `Captain Adam Bowen.` to `Mr. Richd. Oliver, master-at-arms.` Then `state`: its last line is `Watch on deck: starboard, 111 hands, none at work; idlers below.`

- [ ] **2. Set plain sail with the watch.** Type `set plain sail`, `tick 1200`. Expect two routine lines at once, `Only seven hands to the mizzen topgallant; ...` and `Only eight hands to the spanker; ...`: the watch has 111 hands and eleven sails want more than that, so the last two go short-handed. The sails come in turn: the jib and fore topmast staysail at 04:02, the courses 04:03, the main and mizzen topsails 04:04, the fore topsail 04:05, the spanker 04:06, the fore and main topgallants 04:07 and 04:09, and the short-handed mizzen topgallant last, at 04:16: **about sixteen minutes**. Type `quit`.

- [ ] **3. All hands first.** Start again as above. Type `call all hands`. Expect `The boatswain's mates pipe all hands at the hatchways; 141 hands turning out below.` and a notable `* All hands! (by the captain's order)`. Type `tick 90`: `All hands on deck.` at 04:01. Now `set plain sail`, `tick 600`, `state`: every sail is set by 04:07, **five and a half minutes after the order**, three times as fast as the watch; the state reads `Watch on deck: starboard, 252 hands, none at work; idlers below.` and `All hands called by the captain's order.` Then `pipe down`: `Piped down; the starboard watch has the deck.` Type `quit`.

- [ ] **4. A tack while the studdingsails go up.** Start again. Type `set plain sail`, `brace sharp up on the starboard tack`, `tick 1200`, `trim sails`, `tick 300`, `set the studdingsails, both sides`, `tick 60`, `tack ship`, `tick 30`. Expect `* All hands! (to tack ship)` and ten notable lines `Belayed setting the starboard fore lower studdingsail: all hands about ship.` and so on, one per studdingsail. Type `pipe down`: refused, `The hands are still about ship; wait for her to come round.` Type `tick 900`: `All hands on deck.` at 04:27, `Tacked; braced up on the larboard tack, heading ENE (68°).` at 04:32 (**six minutes**, as at gate M2), `Piped down; the starboard watch has the deck.` on the same line of time, and then the belayed studdingsails taken up again: eight set by 04:37 and the two main topgallant studdingsails still at work when you type `state` (`16 at work (8 at the starboard main topgallant studdingsail, 8 at the larboard ...)`). Type `quit`.

- [ ] **5. Box-hauling.** Start again. Type `set plain sail`, `brace sharp up on the starboard tack`, `tick 900`, `keep her full`, `tick 300`, `box haul`, `tick 900`, `state`. Expect `* All hands! (to boxhaul)`, then at 04:21 `Up mainsail and spanker! Square away the after yards! Brace abox the head yards!`, `Her head falls off.` as she makes a sternboard, `Wind aft; braced up the after yards. ...` at 04:26, and `Box-hauled; braced sharp up on the larboard tack, heading ENE (68°).` at 04:28, **about eight minutes**, then piped down; the state near `5.6 kn`, `49° on the larboard bow`. (Say `keep her full` first: after `trim sails` instead she will not come round in this wind; that is recorded as a finding.) Type `quit`.

- [ ] **6. Sending a watch, relieving the watch, and a crewed replay.** Start again. Type `send the larboard watch aloft to loose the fore topsail`, `tick 30`, `state`. Expect `Turned up the larboard watch.`, and the watch line `Watch on deck: starboard, 172 hands, 12 at work (12 at the fore topsail); the larboard watch turned up; idlers below.` (a third of the larboard watch came at once and the rest are on the ladders). `tick 600`: `Set the fore topsail.` at 04:05. `send the marines aloft to loose the main topsail`: refused, `The marines do not go aloft; send topmen, or a watch, to work aloft.` `pipe down`, then `relieve the watch`: `The larboard watch relieved the deck.`, and `state` shows `Watch on deck: larboard, 111 hands, none at work; idlers below.` Now `save voyage.json` and `replay voyage.json`: expect `Replayed. Log digest 3ecca5da12c4f860. Clock held.` and the same state, the same watch on deck. Type `quit`.

- [ ] **7. A day of watches, and the idlers.** Start again. Type `tick 59400` (a minute or two). Expect, among the bells: `Idlers up.` at 06:00; `Eight bells. The larboard watch relieved the deck.` at 08:00; the starboard at 12:00; the larboard at 16:00; `Four bells. The starboard watch relieved the deck.` at 18:00 (the dog watches turning the day); and at 20:00 `Eight bells. The larboard watch relieved the deck.` and `Piped the idlers down.` Keep this console for item 8.

- [ ] **8. The night of three calls, and the morning's pace.** Continuing from item 7 at 20:30: `set the fore topsail`, `tick 600`: set at 20:35, **341 seconds** after the order with the larboard watch, rested. `tick 15600` (to 01:00; the starboard watch relieves the deck at midnight). Then call all hands three times: `call all hands`, `tick 600`, `pipe down`, `tick 3000` for the calls at 01:00 and 02:00, and `call all hands`, `tick 600`, `pipe down`, `tick 3060` for the one at 03:00. Each call turns out `141 hands` below, the larboard watch among them. At 04:00 `Eight bells. The larboard watch relieved the deck.`: the watch that was turned out three times has the morning watch. Now `set the main topsail`, `tick 600`: set at 04:07, **395 seconds**, the same work a sixth slower. Type `quit`.

### Part B: the gale

- [ ] **9. The gale answered.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,35 --heading 270`. Type `make all sail`, `brace up on the starboard tack`, `tick 600`, then as at gate M2 `make all sail` and `trim sails`, and now `send down the topgallant masts`. Expect `* All hands! (to send down topgallant masts)` and notable `Belayed setting the fore topgallant: down topgallant masts! ...` lines for the topgallants, royals and studdingsails. Then `tick 600`, `trim sails` (two `Could not brace the mizzen topgallant yard: The mizzen topgallant yard is sent down.` lines are right: its yards are on the way down), `tick 600`: at 04:34 `Sent down the fore topgallant mast, the main topgallant mast and the mizzen topgallant mast; the upper spars on deck.`, `Piped down`, and the belayed topgallants and royals refused (`... yard or mast is wrecked or sent down`). `trim sails`, `tick 600`, `state`: the sail line ends `sent down: fore.topgallant_mast, main.topgallant_mast, mizzen.topgallant_mast`, and in forty minutes **not one `carried away` line**, where gate M2 lost the royals inside the second ten minutes. `quit`.

- [ ] **10. The gale that was not.** Start the same, and give the same orders without `send down the topgallant masts`: `make all sail`, `brace up on the starboard tack`, `tick 600`, `make all sail`, `trim sails`, `tick 600`, `trim sails`, `tick 600`. Expect red `!` lines from 04:13: `Fore royal mast carried away; the fore royal, with the fore royal yard, hanging to leeward.`, the mizzen and main royal yards at 04:14 and 04:15, then studdingsail booms. Type `shift the fore royal`: refused, `The fore royal is wrecked.` The spec pictured the fore royal *blown out* and shifted for a new one; in this gale the canvas never fails before its spar, so the royal goes with its yard and mast and there is nothing aloft to bend a sail to. That is a finding, not a fault: see item 11 for the shift itself. `quit`.

- [ ] **11. Shifting a sail.** `py -m freesail.ui.console data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293`, then `shift the fore royal`, `tick 900`. Expect `Stand by to shift the fore royal! Aloft topmen; lay out, furl and unbend.`, `Unbent the fore royal and lowered it down on deck.` at 04:03, `Swayed aloft the new fore royal.` at 04:06, and `Shifted the fore royal; the new sail bent and furled, 3 spare sails left in the sail room.` at 04:11, **eleven and a half minutes** of the heaviest work the topmen do. (Three left, because a sound old sail goes back to the sail room; a blown-out one would not.) `quit`.

### Part C: the schooner, short-handed

```
py -m freesail.ui.console data/ships/topsail-schooner.yaml --seed 7 --wind 0,15 --heading 300
```

- [ ] **12. Muster, and three sails at once.** `muster`: `Mustered the Speedwell's company, 40 souls: three officers, 33 seamen and four idlers.` and `The starboard watch has the deck, the idlers below: 17 hands on deck.`, then the master, mate and boatswain by name (American names this time). Type `set the fore topsail`, `set the foresail`, `set the mainsail`, `tick 600`. Expect the routine `Only five hands to the foresail; the rest are setting the fore topsail.` and one notable `* Not hands enough on deck to set the mainsail; the watch is setting the fore topsail and the foresail.` The fore topsail is set at 04:04, the foresail at 04:08, and the mainsail, begun once hands were free, at 04:08 as well. `quit`.

- [ ] **13. One line for the group.** Start the schooner again. `set plain sail`, `tick 1200`. Expect one notable line for the whole order, `* Setting plain sail: not hands enough for all at once; the watch takes the sails in turn.`, and the sails that must wait saying so in routine lines (the fore topgallant, the fore staysail, the jib); before this milestone's last package each was a notable line of its own. The sails come in turn from 04:03 to the fore topgallant at 04:15: **fifteen minutes** for the watch of seventeen. Then `call all hands`, `tick 90`: `20 hands turning out below`, `All hands on deck.`, and `state` shows `Watch on deck: starboard, 37 hands, none at work; idlers below.` `quit`.

### Part D: the browser window

```
py -m freesail.ui.server data/ships/frigate-36.yaml --seed 7 --wind 0,15 --heading 293
```

- [ ] **14. The watch in the instruments.** Two new lines under Strain: **Watch** `starboard watch, 111 on deck; idlers below` and **Hands** `none at work, 111 idle; fresh on deck, fresh below`. In the command line, `set the fore topsail`: Hands reads `12 at work (12 at the fore topsail), 99 idle; ...` and the In hand list shows `· 12 hands` after the work. Then `call all hands` and `go` at `10x`: over a few real seconds the Watch line fills to `all hands; the starboard watch has the deck, 252 on deck; idlers below`. `hold` once the fore topsail is set (the log's `Set the fore topsail.`).

- [ ] **15. The view keeps to the parts.** With the fore topsail set (item 14), type `goose-wing the fore topsail` and `tick 60` in the command line (`Goose-winged the fore topsail; the weather clew set, the lee clew hauled up.`): the fore topsail is drawn half-width, hanging from the weather half of its yard, and the Sail set line says `fore topsail (goose-winged)`. Then `send down the topgallant masts` and run the clock at `60x` until the log says `Sent down the fore topgallant mast, ...` (about fourteen game minutes with all hands already up): the topgallant and royal masts and yards disappear from the ship view, as a carried-away spar's dependents do.

- [ ] **16. Read chapter 6 of the primer and type along.** `docs/primer/06-the-watch-and-the-log.md` has new sections on the ship's company and the watch bill, all hands and piping down, sending a watch or a station, and relieving the watch. Try its orders on either ship. Its blocks are tested, so a refusal the chapter does not predict is a real finding.

## Guide

**Hands and the crew factor.** An evolution's file names the hands it wants (a topsail: twelve ordinary seamen, topmen first). Filled at the rating asked, fresh, one job at a time, the work takes exactly milestone 2's time; that is a test. Short-handed, it takes longer in proportion (eight hands for twelve: half again as long); with fewer than half it waits. Better hands than asked are quicker, worse slower, tired slower still.

**All hands.** The watch below comes up over ninety seconds, a third at once. Work that is all-hands by nature (tacking, wearing, box-hauling, reefing topsails, sending masts down) calls them itself, belays what the watch was doing, and pipes them down after; called by the captain they stay up until he pipes down. A call at night costs the watch below its sleep, and that is what slows the morning in item 8.

**The watch bill.** The two watches alternate through the seven watches of the day; the dog watches make the turn come round differently each day. Idlers (cooks, carpenters, servants) are up by day only. The officers are counted in the muster but give orders and do not haul.

**Truths 18 to 23 and the third xfail.** The spec's six crew truths are tests. Truth 18 says the watch sets plain sail in 25 to 40 minutes and all hands in 12 to 20; the ship does it in 16 and 5.6 with milestone 2's frozen durations. The ratio, the point of the truth, passes; the absolute times are a strict expected failure with the reason, for you to judge. Numbers are in `docs/dev/TuningNotes.md`.

**Replays with a crew.** A save is still the seed and the orders; the crew is mustered from the seed again on replay, so the same voyage has the same company, the same watch changes and the same fatigue to the last hand.

## Not in this milestone

- **The officer of the watch, standing orders, meals and the routine of the day** beyond the watches and the idlers. Milestone 4.
- **Water and provisions consumed.** The stores are numbers in the ship file; only spare sails are used (by shifting). Milestone 4 and 5.
- **More hands never speed a job.** Twelve hands at a topsail go no faster with twenty; Luce says more on a halyard hoist faster, up to the room on the rope. An open item.
- **Level-0 line orders** (`haul the weather main brace`) still cost no hands: they are the officer's fine adjustments.
- **The helmsman and the lookout** as sailors, morale, sickness, punishment, boys. Later milestones.
- **A blown-out sail in the gale** (item 10): the strain ratings put the spar first at every wind tried.

## What to report back

- Pass or fail for items 1 to 15, what happened for 16.
- Your reading of truth 18's times (sixteen minutes for the watch, five and a half for all hands) and of item 8's night: is a sixth slower the right price for three calls?
- Whether the log's new lines read as a ship's log: the belayed lines, the watch changes, the group line, `Turned up the larboard watch.`
- Anything in the browser that confused you, or that you looked for and could not find.
