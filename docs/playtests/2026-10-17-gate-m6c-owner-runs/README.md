# Gate m6c: the owner's runs (notes of 2026-10-17, at partial completion)

The owner's notes on his runs of gate 6c's items as written (`m6c_notes.txt`), with the
saves under `saves/` (gzipped; unpack to `--load`). The gate was run in part: its untested
items are deferred to the director's milestone's gate (decision 50), the director's station
brought forward. The lead's cold read and the routing of each note are in
`docs/dev/M6-WorkPackages.md` ("The owner's runs of gate 6c, read"). The saves are the
owner's data files as he sent them, not read by any test.

## The saves

| Save | Scenario | Ship | End tick | Size |
|---|---|---|---|---|
| `m6c-merchant-intent-sale-complete.json.gz` | The merchant passage by intent, Falmouth for Brest | topsail-schooner | 182057 (2 d 02:34) | 8 KB |
| `m6c-merchant-passage-aground.json.gz` | The merchant passage, Falmouth for Brest | topsail-schooner | 101235 (1 d 04:07) | 43 KB |
| `m6c-merchant-passage-business-complete.json.gz` | The merchant passage, Falmouth for Brest | topsail-schooner | 133317 (1 d 13:01) | 43 KB |
| `m6c-naval-cruise-complete.json.gz` | The naval cruise, Plymouth to the station off Ushant | frigate-36 | 108334 (1 d 06:05) | 20 KB |
| `m6c-trial-station-gale-aground.json.gz` | A captain's trial, the station off Ushant in a gale | frigate-36 | 77298 (0 d 21:28) | 8 KB |
| `m6c-trial-station-lee-shore-complete.json.gz` | A captain's trial, Ushant under her lee in a gale | frigate-36 | 125615 (1 d 10:53) | 20 KB |
| `m6c-trial-station-stranger-failure.json.gz` | A captain's trial, the station off Ushant and a stranger | frigate-36 | 112964 (1 d 07:22) | 8 KB |
| `m6c-trial-trade-stranger-anchored.json.gz` | A captain's trial, a merchant schooner and a privateer | topsail-schooner | 100099 (1 d 03:48) | 4 KB |
| `m6c-trial-trade-thick-anchored.json.gz` | A captain's trial, a merchant schooner in thick weather | topsail-schooner | 17568 (0 d 04:52) | 3 KB |

## The notes, verbatim

```text
Station Gale Trial:
1. Taken aback quite often, once bearing taken and account moved to between Ushant and the coast, ship was slowly brought by tide and tacks to run aground on the Molene. It appeared that each time a bearing was taken while the ship was heading northwards out to sea, it would trigger a tack that brought the ship south again towards the islands like the Molene, and eventually it simply ran aground on a steady tack despite multiple things in sight and a few miles visibility (the uncertainty was not trusted within two miles NE and SW, the angle on which the ship was sailing when it ran aground. Saved after running aground.
Station Lee-Shore Trial:
2. Tons of taken abacks. Fore topmast staysail blown out, never shifted. Trim not occurring often enough, it seems, or no trim happening when one is needed. This time, when the shore was visible and near, the captain properly tacked and kept an offing, and it performed more as I would expect. Not sure why in the gale trial no land was spotted close ahead, despite running aground on it. Could be it ran aground near to land but not near enough to actually trigger the standing off. A consideration, not necessarily a full fail.
3. General note, perhaps the standard book should contain taking fixes/bearings when the uncertainty is above a certain distance, so that when it is possible the uncertainty can be lowered, as it seems that most problems come up when the uncertainty is unnecessarily high, despite bearings or even a fix being available. Something to consider.
Merchant Passage:
4. Without giving the pilot the conn, took the ground while coming to anchor in Berthaume. The course here and in the merchant-intent run both ran very close to the ground, and in this case the ship did take the ground. Saved after the grounding.
5. Sightings of other ships/orders that describe them should say both the relative bearing and also what course the other ship is on, relative to the focused ship (however this would be said historically, if at all).
6. With the pilot given the conn right as he came onboard, the passage was made smoothly (even on the ebb) and the business was completed, with "I have the conn" given once the anchor order by the book was in.
Station Stranger Trial:
7. Sail spotted, chase made, but more sail could have been set to improve the chance of the chase. Perhaps need a consideration in the naval books for trying to catch by setting more sail as is appropriate, a model captain will do it naturally, I think, but the rules-based captain might try to set more sail too. What's your take?
8. While sailing back to the station, I believe the Palinure was spotted sailing southwards (maybe towards the player ship), and this possibly caused the ship to miss it's station and continue to sail southwards, not turning back to the ship that was spotted, and not continuing to the station until the ship was lost again at sunset.
9. The ship tried to regain the station, but the "wear on the hour" order kept firing while it was on course for the station, and kept the ship well south and west of the station at the point I saved and exited.
Naval Cruise:
10. Cutter met, brig "spoken" (came within hail).
```
