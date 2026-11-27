# The tartane in a live preview (21 November 2026)

The owner sailed the trader *Saint-Pierre* (`data/ships/tartane.yaml`) in a browser preview of her
builder's branch, `claude/pkg-90-tartane` at b9ebd761. That branch is before the engine's steps
A1a to A1d, A5 and A6 and before the viewer's V1 to V3. So her whole lateens are drawn as standing
lugs on the lee side, and her topsail is read as a course. The preview was started at seed 7, the
wind N at 12 kn, her head 292°. The owner made sail and trimmed her, and these pictures were taken
with her standing as they trimmed her.

## The owner's note (a note, not a ruling)

Verbatim, recorded in `docs/design/Decisions-Package90-2026-11.md` Part F, row T-v:

> "Definitely a solid start, though I notice that the topsail doesn't quite trim right. The sheets
> on  the loose foot should try to align with the topsail yard, I would think, whereas now they
> seem to trim directly to the wind and askew from square with the yard. I'll save any judgement
> until the final version."

## What the game's state showed, and the cause

Read from the running game's own state (`/api/state`) at 04:42 ship's time, full and by on the
starboard tack, steering WSW 252°:

- `main.topsail` set, its yard braced 50.7° from square;
- `main.treou` furled and sent down, and its yard, `main.treou.yard`, served `sound` and braced
  42.2°.

**The cause, measured by her builder** (`docs/design/Report-Package90-Tartane.md` §14, on
`claude/pkg-90-tartane` at 5a9c582a). Her tréou is set flying (`flying: true`), as her design's
decision 9 has it. So in plain sail and at her start it is on deck with its yard, and setting it
sways the yard up with the sail (package 57's set flying). The game serves that yard `sound`
and braced, because its sail says it is down, and the viewer draws it on deck. But the viewer's
`squareCut` (`client/projection.js`) still takes it as the yard below her topsail, and hangs
the topsail's clews at its arms. So the loose foot lies along the yard on deck: **90° askew of
its own yard at her start, 26° by the wind**, and square only when the tréou is set.

**The mend is V2's**, one condition in `squareCut`: a yard on deck with its flying sail read as
no yard below. Her topsail then hangs from its own yard, as every square sail with no yard below
does. Her builder measured it on a scratch copy, uncommitted. No other ship's drawing moves:
hers is the only square sail over a flying yard. **The check for her final version: her loose
foot square with its own yard**, at her start, in plain sail, and with the tréou set and taken
in.

Found beside it, for package 57's reading of a yard sent down with its sail (every ship's): the
engine braces such a yard on deck with the rest, and the trim's words count it ("Braced two
yards to the wind").

## The pictures

Each view's own caption gives the angle it is seen from.

| File | What it shows |
|---|---|
| `pictures/00-the-page-topsail-braced-51-from-square.jpg` | the whole page: the log with "Braced the main topsail yard; 51° from square.", the instruments, the map |
| `pictures/01-from-the-larboard-beam-to-leeward.png` | from the lee beam |
| `pictures/02-from-larboard-11-from-the-bow.png` | from 11° off the larboard bow: the foot twisted from the head |
| `pictures/03-from-dead-ahead.png` | from dead ahead: the head along its yard, the foot narrow and skewed toward the tréou yard's brace |
| `pictures/04-from-larboard-169-from-the-bow.png` | from nearly astern |
