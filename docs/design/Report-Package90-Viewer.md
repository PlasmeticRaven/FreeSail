# Report: package 90, the viewer (V1 to V3)

The viewer's session for package 90: the engine's new lateen, pole-mast and towed-boat states drawn
in the client, before the tartane's report (`docs/design/Plan-Package90.md` §6 rows V1 to V4, §7.1,
§9.1). Started by the owner on 2026-11-27. Branch `claude/pkg-90-viewer`, cut from 93cf624c (the
package's branch, carrying A1a to A1d, A4, A5 and A6).

The files this row owns, and the only ones edited for the steps: `client/projection.js` and
`tests/test_view_geometry.py`. `client/shipview.js`, `client/style.css` and `tests/test_pictures.py`
are untouched. The notes' section is "Package 90, the viewer" in `docs/dev/TuningNotes.md`.

## 2026-11-28: V1 and V2 built; V3 stopped; two questions and a choice for the lead

**Built** (each its own commit, pushed; the tiers on one hash follow in a later section):
- **V1**, the whole lateen drawn as its own (e0cba7d).
- **V2**, the pole mast and the yard below that does not stand, mended at its cause (24d239a).
- The notes' section, "Package 90, the viewer" (427ca81).

The measured figures, old beside new, the tartane's topsail among them, are in the notes' section.
In short: her topsail's loose foot is square with its own yard in each of her report's §14.2
states, 9.35 m broad, its clews 8.09 m over her water, as her builder measured in scratch; before,
90° askew before the wind and 26° by the wind braced 64°. The smack's topsail yard lies on her
square-sail yard (11.15 m over her water, against 14.35) whenever her topsail is not set, her start
and plain sail among them, since A6 furls it there: the plan's one expected move.

### Stopped: V3, the towed boat drawn astern (the stop rule)

The client is served no boat. `/api/ship` (`freesail/api/queries.py`, `ship_graph`) serves the
spars, sails, lines, hull, guns and ports, and no boats; `/api/state` (`snapshot`) serves no boat
in tow. A4 keeps her in the engine alone (`ship.extra["boat_in_tow"]`, `boats.keep_in_tow`;
TuningNotes, "Package 90, A4"). Drawing her needs `freesail/api/queries.py` to serve, for
instance:
- in the graph, each boat whose file tows her, with her `towed` key and her length (her own file's
  hull, which A4 already reads for her drag);
- in the snapshot, whether she is in tow now (A4's key: there while she is in tow, gone while she
  is away on an errand, manned or lost).

That file is neither in the viewer's row of §7.1 nor named by the card for it, so I have not
edited it. Once served, V3 is the viewer's alone: her hull on her painter A4's `TOWED_ASTERN_M`
(12 m) dead astern of the taffrail, at her file's length, and the painter from the taffrail to her
stem; nothing committed moves (no file tows a boat). **Asked:** whose step serves it, and whether
V3 waits for it in this package or goes to a later one.

### Not served: a manoeuvre's change of the lateens (V1's "peaked up its mast while it is changed")

The shift by itself is served exactly: `change_lateen` in hand on the sail, the sail in its gear.
V1 draws it peaked up the mast. A manoeuvre's change is not. In a tack, a wear, a fill away, a
box-haul or a box off (`LateenChange`, held on the manoeuvre's script), and for the yards a belay
hands on beyond the longest (the handed-on `change_lateen`'s one subject), the snapshot serves only
the manoeuvre and each sail `in_the_gear`, as it serves a lateen brailed up before the manoeuvre
began. Measured on the xebec probe (`tack ship`, 15 kn): from +60 s to +250 s her three lateens
were served `in_the_gear` with `lug_side` the old side, the only work in hand `('tack', 'Harpy',
'steady')`.

So in a manoeuvre the yards being shifted are drawn brailed up under their yards aloft, not
peaked. Guessing from "in the gear while a tack is in hand" would draw a lateen brailed up before
the tack peaked too, so I did not. The settee's mirror would serve it: a key on the snapshot's
sail, served only while its change is in hand, as `yard_lowered` is for a settee
(`api/queries.py`, and a mark the change keeps on the sail, `evolutions/scripts.py`: the engine
track's files). With it the drawing reads the key in one condition. **Asked:** is it wanted before
the tartane's report?

### A choice for the lead: the fixed frame and the peaked yard (JUDGEMENT)

The frame holds every state's figures (spec M3 §9 item 14). With her great yard peaked, the
tartane's frame top rises from 17.59 to 25.50 m (abeam 18.80 to 26.72 m high), so she is drawn about
30 per cent smaller in every view, to keep the view from rescaling for the minute her yard is
shifted. Left out of the frame, she is drawn at today's scale and the view zooms out while the yard
stands peaked. **Built the first way**; the second is one line. No committed file's frame moves.

### Found on the way (the engine's, not mine)

`ship/graph._square_foot_m`, read by A5's lateen rule, mixes a sail's centre above the water with
its yard's height above the deck. It overstates the foot by twice the deck's height: 1.08 m on the
tartane, whose topsail clears her lateen's yard by 0.03 m, not 1.11 m. It moves no classing on her
files. The viewer keeps the engine's arithmetic so that the two read every pole alike.

I carry on with the tiers on one hash for V1 and V2, and write them here when they are done.
