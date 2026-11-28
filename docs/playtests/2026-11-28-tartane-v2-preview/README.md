# The tartane with the viewer's V1 and V2, in a live preview (28 November 2026)

The owner watched the trader *Saint-Pierre* (`data/ships/tartane.yaml`) in a browser preview.
The tree was a scratch one, made on the coordinating machine and never pushed:
- the viewer's branch, `claude/pkg-90-viewer` at 0000168f (V1, the whole lateen drawn as its own;
  V2, the pole mast and a yard below that does not stand);
- her builder's branch, `claude/pkg-90-tartane` at 3c584e0f, merged in locally;
- her two files regenerated on that tree by the generator, the same byte for byte.

The game was started at seed 7, the wind N at 12 kn. These pictures check her own note of 21
November (`docs/playtests/2026-11-21-tartane-preview/`, Part F row T-v): that the topsail's loose
foot should lie square with its own yard.

## The three states of her report's §14.2, as V2 draws them

1. **Before the wind, the tréou struck** (`pictures/1-before-the-wind-treou-struck.png`): she was
   started heading S, then given `set plain sail`, and is seen from her quarter. The topsail hangs
   square under its own yard. Before V2 its foot ran fore and aft, 90° askew.
2. **By the wind, the topsail yard braced 64°** (`pictures/2-by-the-wind-braced-64.png`): after
   `bring her by the wind`, seen from leeward. The foot stays square with its yard. Before V2 it
   was 26° askew.
3. **The tréou set** (`pictures/3-treou-set.png`): after `set the treou`. The topsail's clews go
   to the tréou yard's arms, as they did before V2.

## The great yard peaked in its shift, and the frame

`pictures/4-great-yard-peaked-in-the-shift.png` shows V1 drawing the great yard peaked up abaft
the mast while `shift the mainsail` is in hand, its sail in its gear.
- **A scratch key for this picture:** her file does not yet carry the whole lateen's side key
  (`dipping`), which her builder adds when she takes the engine's steps. For this picture alone, a
  scratch copy of her file was given `dipping: true` on her whole lateens, as
  `tests/test_lateen_whole.py`'s probes are.
- **The order:** she was tacked by `tack ship and leave the lateens`, then shifted.

**The frame is the owner's choice** (the lead's nudge 88). As built, the frame holds every state's
figures, the peak among them. So she is drawn about 30% smaller in every view, and the view
never rescales. The other way draws her at today's scale, the view drawing back while the yard
stands peaked.
- **Not shown:** a one-line switch tried in the scratch copy did not change her scale, so the
  other way was put to the owner in words.
- **The owner chose (a), the fixed frame**, recorded verbatim in Part F, row T-f.

## The owner's note (a note, not a ruling)

Verbatim, recorded in `docs/design/Decisions-Package90-2026-11.md` Part F, row T-v2:

> "Only note for me so far is that there appears to be a small rendering error in the lateens, on
> the forward end of them, which appears like a pinched section. It can be seen on the mizzen in
> the preview, currently, at a few different angles."

`pictures/5-the-pinch-on-the-mizzen.jpg` shows it as the owner saw it, and
`pictures/6-the-pinch-close-up.png` close up: the ship view's own box narrowed onto the mizzen's
forward end while the clock was held.

**What the drawing does there,** read from the ship view's own paths:
- Each whole lateen is drawn as a four-cornered sail (`quadSail` in `client/projection.js`).
  Its fourth edge is the short luff at the car, the lashing, about 0.3 m long. Her file writes it
  so the sail has four corners to draw by (her module's note on the great lateen).
- `quadSail` gives every edge one belly, `2 × BELLY × min(depth, width)`, whatever that edge's own
  length.
- So the 0.3 m luff bellies forward 0.74 m on the mizzen and about 1.05 m on the great lateen: a
  thin tongue ahead of the car. That is the pinch.

Sent to the viewer, to mend at its cause: each edge's belly by its own length.

## Found on the way, for her builder

**Started from rest heading WNW 292° with the wind N at 12 kn, she would not bear away or wear.**
- `set plain sail` and `steer south`: her main topsail was taken aback and she lay at 0.5 to
  0.8 kn heading 287° to 305°.
- `take in the mizen` did not let her pay off.
- `wear ship` gave "Could not wear: she would not come round." at 15 minutes.

That was her file as committed, before the engine's steps reach her. Sent to her builder to
measure with her hash.

## The mend, seen again (the same day, later)

The viewer mended the owner's note at its cause (`edgeControl` in `client/projection.js`: each
edge of a sail bellied by its own length, capped at `BELLY` of it). The mend is in the viewer's
hash for V1 and V2, `claude/pkg-90-viewer` at 20aca5ec. It moves the outlines of sails on 15 of
the 19 committed files, declared in the viewer's report; no corner, spar, line, frame or bound
moves.

The owner looked at it live, on a scratch tree here (20aca5ec with her files merged locally, never
pushed):
- **The tartane** (`pictures/7-mended-tartane-by-the-wind.png`, and close up
  `pictures/8-mended-mizzen-forward-end-close-up.png`): by the wind with plain sail, the scratch
  `dipping` key as before. Both lateens' short luffs now stand 0.03 m off their chords, where the
  tongue stood 0.74 m on the mizen and about 1 m on the great lateen.
- **The bilander *Hopewell*** (`data/ships/bilander.yaml`; `pictures/9-mended-bilander-settee.png`,
  and close up `pictures/10-mended-bilander-settee-luff-close-up.png`): by the wind, her main
  settee set. Its 1.81 m luff now stands 0.20 m off its chord, where it stood 1.35 m.

**The owner's word**, verbatim, recorded in Part F, row T-v3:

> "Both fixes look clean to me, very good."
