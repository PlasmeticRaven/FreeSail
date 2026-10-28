# Proposed spec: powder and shot taken in, and the magazine refilled (2026-10-25)

Written at the owner's word, for the lead ("you're approved to draft that part up properly
for a fix"), after the practice-firing proposal found that **no port supplies powder or
shot, and nothing refills a magazine once fired.** Three read-only surveys stand behind it:
the ports' supplies, the magazine's state through saves and replays, and the project's own
period texts. Every figure from memory is marked so. The lead and the owner decide; nothing
here is built. Spec M7 §7 (the magazine as stores "the purser and the gunner count"), the
M5 port rules and M7b §17a ("transactions, not variables") bind.

## 1. What the period's regulations say

The project holds the Admiralty's *Regulations and Instructions relating to His Majesty's
Service at Sea* (the 1806 regulations, 1808 printing), `docs/references/admiralty/
regulations-and-instructions-1808-ocr.txt`. Its Gunner's chapter (Sect. VII ch. II, pp.
214-225) is the source. Lines are the OCR file's.

- **The Ordnance, not the Navy, supplies.** On commissioning the gunner "is to apply to the
  Store-keeper of the Ordnance at the Port for the established number of guns, with the
  proper quantity of ammunition and Stores", examined "before they are put into the hoys"
  (Art. I, l.12722-12737). Stores are demanded "from His Majesty's Dock yards, as well as
  from His Majesty's Ordnance Magazines" (l.12246), two suppliers. Abroad with no
  storekeeper on the station, demands go to the Navy Board and the Board of Ordnance, and
  captains are "strictly charged not to purchase Stores of any description without an
  absolute necessity" (l.6220-6247).
- **It comes off in a hoy, with the fires out.** The gunner tells the captain when the
  powder is ready, "that the fire in the Galley may be put out, before the Vessel which
  carries it is suffered to go alongside". While it is taken in, no candles but in the
  light room, and no man to smoke tobacco (Art. V, l.12800-12809). The magazine is first to
  be "perfectly dry" (Art. IV, l.12781-12792). After stowing, the doors and scuttle are
  secured and the keys go to the captain (l.12815-12827), and a sentinel stands at the
  scuttle (l.8450).
- **Only at certain roads.** Powder is taken in at "Plymouth Sound or Cawsand Bay, Spithead,
  Blackstakes, Longreach, River Thames". Ships ordered into port take theirs out before they
  pass those places (Art. VI, l.12833-12839).
- **Its care.** The barrels are turned once at least every three months (Art. X, l.12920).
  The shot racks are kept full (Art. XIV, l.12985). Empty barrels go back to the Ordnance's
  storekeeper, who pays the gunner "one shilling for every empty barrel he shall return in
  good condition" (Art. IX, l.12887-12902), the one price in any of the project's texts.
- **The allowance for exercise.** Each month for the first six months after the guns are
  received, "one charge of powder and one round shot for one third of the number of the
  upper deck guns, in Ships of two or three decks; or one fourth for Ships of one deck",
  and half that after (Art. XXI, l.13122-13144). The Captain's chapter gives one third with
  no one-fourth rule (l.8842-8870): a discrepancy in the source, to be read on the page.
- **The charges.** Table No. 29 of the appendix gives the charges by gun (l.27502), but the
  OCR has lost its figures: **read them from the page image** before any charge weight is
  fixed. Falconer 1780 gives "half the weight of the ball" in small guns and 7/16 for
  32-pounders (CHARGE, l.4827-4829), the earlier proof-era figure. The service charge of
  1805 was nearer a third of the shot's weight for a long gun, and a carronade's about a
  twelfth (from memory, UNVERIFIED).

**Silent in the project's texts** (memory or judgement, and marked so wherever used): the
words "powder hoy" and "gun wharf" in English; any price of powder or shot; the English
barrel's weight (Falconer's French glossary gives a hundred pounds for the *baril de
poudre*, l.22563); any red or powder flag (no period text here has one); how merchantmen
and privateers bought powder at all, beyond Falconer's "powder-chests ... particularly used
in merchant-ships" (l.13800-13810); and a shot allowance a gun.

## 2. What the game does today

- **No supply.** None of the 38 port files has powder, shot or an Ordnance. The yard's and
  chandlers' items (`data/ports/*.yaml` `dockyard:`, `world/ports.py` `YardItem`,
  `Dockyard`) are spars, sails, cordage, water and provisions. An item called "powder" added
  as data alone would fall through `_apply_job` to `booms(ship).counts["powder"] += 1`, a
  spare spar called powder, and `orders/port.py` would drop its quantity. Supply can't be
  added as data alone.
- **The magazine.** `parts.Magazine` (cartridges by calibre, shot by calibre and kind, the
  rounds fired), built lazily from the fit in `ship.extra["magazine"]`, taken from by the
  battery and spoiled by the director's `cartridges_damp`. It has no add and no capacity. A
  checkpoint pickles it whole, and a replay rebuilds it from the fit and repeats the same
  inputs. Nothing about it is in the save JSON, so a refill that is an order (journaled and
  replayed) and a job (pickled in `Ports.jobs`) survives both, as water does.
- **A defect the refill must not deepen.** Cartridges are keyed by the pounds of shot alone,
  so a long gun and a carronade of one calibre draw one pool (the privateer schooner's long
  12 and her 12-pounder carronades: `Proposal-PivotGun.md` §5). The real shared store was
  **powder by weight**. The cartridges were filled from it for each gun, a long gun's
  charge three or four times a carronade's.
- **The gunner's "the magazine is out"** is said once a calibre and never again
  (`Battery._said_no_powder`, `_fell_back` are never cleared), so a refilled ship that runs
  out a second time would be silent.
- **Crewed strangers** start with a full magazine at each promotion and lose it at demotion
  (`world/crews.py`). Far vessels have none.

## 3. The proposal, in two stages

### Stage A: the refill, on the present magazine (small, safe to build now)

1. **The supplier is the port's, by data.** A new `ordnance:` block in a port file, beside
   `dockyard:` and not inside it, because the magazine is keyed by calibre and kind and a
   `YardItem` has one rate:
   ```yaml
   ordnance:
     kind: ordnance          # 'ordnance': the King's storekeeper, issued on demand to a
                             # King's ship, free, vouched; 'merchants': bought at a price;
                             # omitted: none to be had
     roads: [plymouth-sound, cawsand-bay]   # where a King's ship may take powder in
     hours: 6                # the hoy's errand and the taking in (judgement)
     powder_per_barrel_pounds: 5.0   # a merchant's price, £ a barrel (judgement, UNVERIFIED)
     shot_per_ton_pounds: 12.0       # £ a ton of shot (judgement, UNVERIFIED)
     sells_in_war_to: [...]  # optional: a neutral's powder for one belligerent, not another
   ```
   Plymouth is the Ordnance's (the game's only port of the Regulations' list; there is no
   Portsmouth file). Gibraltar is the Ordnance's abroad. The French, Spanish and Portuguese
   yards are `merchants` to their own and allies, and to a neutral by the war's knob. Every
   other port is `merchants` or none, as the owner judges a small port's trade.
2. **The order is the gunner's demand.** `complete the powder and shot`, `demand powder and
   shot`, `take in powder` (and `indent for powder and shot`, the yard's own synonym).
   - With no number it completes the magazine to the fit's allowance, as `take in water`
     fills to the ship file's water.
   - With a number (`take in 200 cartridges for the 12-pounders`, `buy twenty round shot
     for the long 12`) it takes that much. `orders/port.py` must pass the number for these
     items, as it does for water and provisions.
   - It is refused, in words, in each of these cases:
     - not in port;
     - the port's `ordnance` gives her nothing (a merchantman at the Ordnance's port; a
       belligerent at a neutral's that sells to the other side);
     - a King's ship at a port with only merchants, unless the captain says it is of
       necessity (`buy powder of necessity`). That is the Regulations' "absolute necessity",
       and the log keeps his word for the Admiralty's account.
3. **It comes off in a hoy, with the fires out.** A `Job(kind="ordnance")` like the yard's,
   due after the `hours`. When the hoy comes alongside (the job's start), the log says the
   galley fire is put out and no lights are allowed but the light room's. That is a state,
   `galley_fire_out`, which the needs may read (no hot food until the powder is stowed),
   cleared when the job is done. A King's ship at the Ordnance's port is told to take it in
   at the road (`roads`); inside the harbour the order is refused, Art. VI's rule.
4. **The receipt is a transaction.**
   - `Magazine.receive(kind, pounder, cartridges, shot_by_kind)` adds to the counts, with
     **no new fields**, so old checkpoints load (the checkpoint's rule: every new field a
     class default).
   - It takes the gun's **kind** even while the keys are by calibre, so stage B changes no
     caller.
   - Refilling a calibre clears `_said_no_powder` and `_fell_back` for it, so the gunner
     speaks again.
   - The cost, for a purchase, is paid from the purse in one line. An issue from the Ordnance
     is vouched at no cost.
   - The gunner's account gets its line (a new paper in `data/papers/papers.yaml`, "the
     gunner's account", beside the purser's books).
   - The empty barrels' shilling (Art. IX) may be the gunner's own perquisite, said and not
     paid into the ship's purse, or left out (a small thing for the owner).
5. **The reading.** `the magazine` already describes the counts. It gains the allowance
   ("cartridges for the long 12-pounders: 30 of 55 of the allowance") so a captain sees what
   a completion would take, and it rides in the sample while she is in port with the
   magazine short.
6. **The docstring.** `Magazine`'s "a function of the ship file, the fit and the rounds
   fired" becomes "… and the world's orders and the ports' issues", which it already is for
   the director's damp cartridges.

### Stage B: powder by weight, and the cartridges filled (the defect's fix)

1. **The magazine holds powder in pounds** (by the barrel: a hundred pounds, Falconer's
   French figure, the English barrel's weight to be confirmed on a page), **and filled
   cartridges by gun kind and calibre.** Shot stays by calibre and kind, since a long 12 and
   a 12-pounder carronade threw the same ball.
2. **A cartridge's charge** is the gun's kind and calibre's: Table No. 29's figures once read
   from the page. Until then, a long gun's third of the shot's weight and a carronade's
   twelfth, marked UNVERIFIED. The fit's allowance is written by the generator as filled
   cartridges and a reserve of powder in barrels.
3. **The gunner and the quarter gunners fill cartridges** from the powder in the filling
   room (the light room by the Regulations' word), in hours, by the bill. That is a
   standing intention while filled cartridges for a gun of the fit are below a stated
   level. In action it goes on below if there is powder and a man to spare. Falconer gives a
   quarter-gunner "to every four cannon" (l.14283-14289), and the bill can take its count
   from that. The battery takes a filled cartridge of its gun's own kind. When a kind runs
   out with powder still below, the line says so ("no more filled cartridges for the
   carronades; the gunner is filling").
4. **The refill of stage A then takes in barrels of powder and shot**, and the ports price
   powder by the barrel. The old keys are converted inside `magazine()` once for a pickled
   magazine (by the fit: cartridges of each calibre given to the fit's kinds in proportion).
5. **The exercise allowance** (Art. XXI) becomes something the gunner can read. A King's
   ship's live practice beyond a fourth of her guns' charges a month, in her first six
   months, is the captain's own word ("beyond the allowance") and goes in the log. See
   `Proposal-PracticeFiring.md` §4.

Stage B touches `parts.Magazine`, `combat/guns._charge_for`, the generator's
`fit_magazine`, every armed ship file (regenerated) and the bill. It moves no sailing pin, and
it may move the action truths (7-133 on) if a ship ran short of a kind in them (none did at
seed 7: no truth pins a magazine figure). It is package 75's or 77's size, not a hotfix.

## 4. From another ship (deferred)

A frigate supplying a cutter of her squadron, or powder taken from a prize, wants a
transfer between two Worlds. It is deterministic only between the player's World and a
crewed one, in one journaled order valid only alongside or by the boat. Far vessels have no
magazine, and a crewed stranger's is rebuilt full at each promotion. Either the magazine
becomes one object shared with the far `Vessel` (as the fishery and the signal locker are,
`world/crews.py`) or the transfer waits. **Proposed: it waits for package 74's prizes**, where
captured powder is one of the prize's goods, and 82's boat as a vessel.

## 5. Tests and truths, proposed

- At Plymouth Sound a King's cutter that has fired half her allowance completes it from the
  Ordnance: free, the hoy alongside at the hours, the galley fire out until the powder is
  stowed, the magazine back at the fit's figures, the gunner's account written, and the
  gunner's "the magazine is out" said again when she empties it a second time.
- Inside the harbour the same order is refused in the Regulations' words.
- At Falmouth (merchants) a King's ship's demand is refused, and `buy powder of necessity`
  buys it at the price, the purse charged.
- A merchant brig buys her own at Falmouth.
- A belligerent at a neutral port that sells to the other side is refused.
- A checkpoint taken before the refill and resumed after gives the same digest as the
  uninterrupted run. A replay from the journal gives it too.
- Stage B: the privateer schooner's long Tom keeps firing when her carronades have used up
  their filled cartridges, while there is powder below and the gunner is filling.

## 6. Decisions for the owner

1. A King's ship's issue from the Ordnance free (vouched, as the Regulations have it), or
   charged to the purse for the game's economy.
2. The merchants' prices of powder and shot: judgement until a source is found. The
   project's texts have none.
3. Which ports supply what (the `ordnance:` blocks), and whether a neutral sells to both
   sides in this war.
4. Stage B now or with package 75/77, and whether the generator's allowance becomes barrels
   and filled cartridges at once.
5. Whether the galley fire out should bite the needs (no hot meal), or be only the log's
   line.
6. Ship-to-ship supply: with 74 and 82, as proposed, or sooner.
