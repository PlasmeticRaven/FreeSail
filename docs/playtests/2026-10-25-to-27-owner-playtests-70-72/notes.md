# The owner's playtests of packages 70 to 72 (2026-10-25 to 27)

Filed by the lead on 2026-10-27 from what the owner could send through the app (the whole
folder with his local hotfixes is over the app's 30 MB limit and follows by another road).
`owner-notes-2026-10-27.txt` holds his twelve notes verbatim; `saves/` the eleven saves he
sent (ten in a zip, and `m7-cutter-tender-test.json` sent alone: the frigate Amazon with a
model as captain of her armed tender, the cutter Raven, under her orders, in Torbay).

## The saves against the builds

The build's rules fingerprint (`freesail.core.world.rules_fingerprint`) at the lead's merge
points: package 70 merged (`80f64f7`) `20b5f53136824d11`; after the owner's first-action
fixes (`9488329`) `91aa8f4ea45ef9ed`; 71 merged (`142b739`) `16055993a31490e8`; 72 merged
(`29b538b`, and the head `7da0c0e`) `e363165adf2b2a28`. The owner's first-action save of
2026-10-24 was on `20b5f531` (70 as merged). **None of these eleven saves is on a lead's
build**: `fbe6b9264aee4097` (eight saves: the naval cruise free, the privateer brig free
in Torbay, the privateer schooner out of Roscoff, the frigate and cutter in Torbay),
`0a0c76dfa72752ed` (the cutter tender test and the Raven-at-full-detail save at 38494) and
`156d6782036194ca` (Raven at full detail, 1266) are the owner's own hotfixed trees, three
of them in the order he worked. Which base each hotfix tree stands on, and what each
hotfix changed, is for the review of his folder when it arrives (the reviewers compare
his patch against `80f64f7`, `142b739` and `29b538b` and say which).

| Save | Scenario | Rules | Seed | End tick | Orders |
|---|---|---|---|---|---|
| freesail-seed7-tick318 | The naval cruise, free | fbe6b926 | 7 | 318 | 14 |
| freesail-seed7-tick120919 | The naval cruise, free | fbe6b926 | 7 | 120919 | 130 |
| freesail-seed7-tick120942 | The naval cruise, free | fbe6b926 | 7 | 120942 | 130 |
| freesail-seed7-tick138464 | A privateer brig, free, in Torbay | fbe6b926 | 7 | 138464 | 216 |
| freesail-seed7-tick80693 | A privateer schooner out of Roscoff | fbe6b926 | 7 | 80693 | 372 |
| freesail-seed7-tick80824 | A privateer schooner out of Roscoff | fbe6b926 | 7 | 80824 | 373 |
| freesail-seed7-tick387 | A frigate and cutter, in Torbay | fbe6b926 | 7 | 387 | 3 |
| m7-cutter-tender-test | A frigate and cutter, in Torbay | 0a0c76df | 7 | 38587 | 76 |
| freesail-seed609627938-tick238 | ... Raven at full detail | fbe6b926 | 609627938 | 238 | 0 |
| freesail-seed609627938-tick1266 | ... Raven at full detail | 156d6782 | 609627938 | 1266 | 0 |
| freesail-seed609627938-tick38494 | ... Raven at full detail | 0a0c76df | 609627938 | 38494 | 0 |

## The owner's notes, routed (the lead's first reading; the review of the folder may move them)

1. The convoy's `full and by` pointing her too close, the convoy riding on the tide on one
   tack and never regaining way to beat: a finding for 72's captain in company and the
   helm's `full and by` under the station order; **for the review of the hotfix folder**
   (he may have mended it) and then a captain's pass.
2. The model captain of another ship could not go ashore ("no port in the world"): the
   other ship's World has no ports; **82's** (the person aboard another ship, the ship's
   World whole) and note 11's.
3. Whether the model briefings and tool descriptions mention moving about the ship, `say`,
   `say to`, eat, drink: **the first Fable reviewer's** (the orders, the primer and the
   library).
4. The date as a reading, not deduced: **the first reviewer's**, a small item.
5. The war's state readable: the initial knowledge and the news taken in from port logged
   in the papers as the prices are: **the first reviewer's**, with 71's and 72's data.
6. A primer and order-grammar completeness pass by a Fable reviewer: **the first reviewer**.
7. Signals and flags in the viewer (colours, each mast's pennant and flags), with the
   signals and the squadron system: **package 81** widened.
8. A ship view of an engaged or visible ship: longer term; booked under 81's remainder.
9. Can a model captain of another ship go ashore; does the needs system run for him: **82**
   and note 11.
10. The boat as a vessel, the player and people moving between vessels, the chart per
    station or domain: **82** (the boat, the movement) and **51's remainder** (the
    director's chart; a chart per station).
11. The world coherent for any combination of player and model, across ships, as people,
    regardless of distance to the player; a model on another ship not in a "basic" world:
    **the second Fable reviewer's** (the world refactored for a less player-centric design),
    read with 82's design.
12. National and company leaders as people that can be stationed, for the naval and the
    economic systems: **M8's**, named in 72's regimes as the hook (the director holds those
    reins today).
