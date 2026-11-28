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

## Found on the way, for her builder

**Started from rest heading WNW 292° with the wind N at 12 kn, she would not bear away or wear.**
- `set plain sail` and `steer south`: her main topsail was taken aback and she lay at 0.5 to
  0.8 kn heading 287° to 305°.
- `take in the mizen` did not let her pay off.
- `wear ship` gave "Could not wear: she would not come round." at 15 minutes.

That was her file as committed, before the engine's steps reach her. Sent to her builder to
measure with her hash.
