# The regatta, 2026-10-16

Each course run at lockstep under each agent by `tools/regatta.py` (spec M6 §21). Elapsed is from the gun to the line, her true position within the finish's radius with every mark rounded; a run not finished says how far she had to go at the limit. Damage is the spars carried away, the sails blown out and the lines and cables parted; fatigue the company's mean (0 fresh, 1 worn out) at the end and the most an hour's mean reached; the purse is at the end, with its change since the gun. The logs and rows are beside this file, a folder to a course.

## Ushant to Falmouth (`data/regatta/ushant-to-falmouth.yaml`)

Seed 7; the limit 30 h 00 m.

| Agent | Door | Finished | Elapsed | Marks | Damage | Grounding | Fatigue (end, most) | Purse | Lines, digest |
|---|---|---|---|---|---|---|---|---|---|
| the scripted captain (trim-for-the-point) | in the game, at the captain's station | yes | 14 h 25 m | none | none | none | 0.02 (fresh), 0.03 | £0 (as at the gun) | 508, `341954f339736409` |
| the rules-based captain | in the game, on the course's intent | yes | 14 h 46 m | none | none | none | 0.02 (fresh), 0.03 | £0 (as at the gun) | 570, `da873c7f2ce5fbec` |
| the scripted captain | in the game, at the captain's station | no, 1.1 miles to go | (ran 30 h 00 m) | none | none | 4, the first at 14 h 38 m: She has taken the ground forward, on good ground, two fathoms and a half of water by the chart, and she draws 15 feet | 0.01 (fresh), 0.03 | £0 (as at the gun) | 907, `b681a27dc0db7a0d` |
| the scripted captain (no-trim) | in the game, at the captain's station | no, 2.7 miles to go | (ran 30 h 00 m) | none | none | 2, the first at 21 h 55 m: She has taken the ground forward, two fathoms and a half of water by the chart, and she draws 15 feet | 0.01 (fresh), 0.03 | £0 (as at the gun) | 715, `317f0b447cbcbc75` |

- trim-for-the-point: the trims by a point of sail judged: the same script with `trim for <the point she is on>` in place of `trim sails`
- fake: the course's script: a course shaped for Falmouth outer road by way of 50 00 N 4 57 W, `trim sails` at the gun and at each glass, a bearing and a fix each glass
- no-trim: the trims judged: the same script and no trim at all after the gun

## Falmouth to the road of Bertheaume (`data/regatta/falmouth-to-bertheaume.yaml`)

Seed 7; the limit 40 h 00 m.

| Agent | Door | Finished | Elapsed | Marks | Damage | Grounding | Fatigue (end, most) | Purse | Lines, digest |
|---|---|---|---|---|---|---|---|---|---|
| the rules-based captain | in the game, on the course's intent | yes | 27 h 36 m | none | none | none | 0.02 (fresh), 0.09 | £5,996 (£4 spent) | 1551, `c328954e9d792928` |
| the scripted captain | in the game, at the captain's station | no, 8.6 miles to go | (ran 40 h 00 m) | none | none | 10, the first at 30 h 53 m: She has taken the ground forward, two fathoms of water by the chart, and she draws 11 feet | 0.01 (fresh), 0.12 | £6,000 (as at the gun) | 1246, `a6023fa88339d2e9` |

- fake: the course's script: a course pricked by way of 50 00 N 4 57 W, west of Ushant and into the Iroise, `trim sails` at the gun and each glass, a bearing and a fix each glass

## Falmouth to Funchal road (`data/regatta/falmouth-to-funchal.yaml`)

Seed 7; the limit 384 h 00 m.

| Agent | Door | Finished | Elapsed | Marks | Damage | Grounding | Fatigue (end, most) | Purse | Lines, digest |
|---|---|---|---|---|---|---|---|---|---|
| the rules-based captain | in the game, on the course's intent | no, 9.7 miles to go | (ran 384 h 00 m) | Ushant 26 h 27 m, Cape Finisterre 116 h 38 m | none | 9, the first at 298 h 59 m: She has taken the ground forward, two fathoms of water by the chart, and she draws 11 feet | 0.01 (fresh), 0.05 | £800 (as at the gun) | 8371, `2f64490ea1d079ad` |
| the scripted captain | in the game, at the captain's station | no, 906.0 miles to go | (ran 384 h 00 m) | Ushant 17 h 05 m | none | none | 0.01 (fresh), 0.03 | £800 (as at the gun) | 10212, `1e61315cc123ea45` |

- fake: the course's script: a course for Funchal pricked by way of 50 00 N 4 57 W, west of Ushant and west of Finisterre, `trim sails` at the gun and each glass, a bearing and a fix each glass
