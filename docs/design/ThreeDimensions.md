# Design study: three dimensions where they matter

From the owner's question of 2026-09-28: whether the simulation should ever move toward
three dimensions, and how to keep it affordable. A design note for the milestone 5, 7
and 8 specifications; not itself a specification.

## What the game carries today

Two and a half dimensions, on purpose. Each part of the ship has a fore-and-aft position
along the keel and a height above the waterline, and no athwartships coordinate; sidedness
is a role (starboard, larboard) and a yard's angle to the keel is a number. The sail
model gives each sail a thrust and a side force from its angle to the apparent wind; the
height turns the side force into a heeling moment and the position into a yawing moment.
The ship moves in three degrees of freedom on the water (surge, sway, yaw, integrated
each tick with the hull's resistance, sway damping and the rudder), with heel as a
quasi-static fourth (the wind's moment against the ballast's righting, settling with a
time constant of seconds). No pitch, no roll, no heave, no sea state. The world is a flat
plane with a wind field; the viewer projects the rig from the same data onto hand-made
hull facings.

## Where a third dimension is genuinely needed

1. **A seaway** (milestone 5, with the world). Pitch, roll and heave in waves affect
   speed, the safety of the rig, working aloft and, later, gunnery. Nothing moves
   vertically today.
2. **Gunnery** (milestone 7). A shot has an arc, a range and an elevation; a hit lands on
   the hull or in the rigging according to the roll at the moment of firing. This is the
   problem the owner sensed coming for a 2.5D simulation.
3. **The rig's own geometry.** Booms fouling braces and studding sails against stays were
   handled in 3b with angles and got away with it. **Blanketing** cannot be: the foresail
   taking the wind out of the jibs when running, one ship lying in another's lee, the
   lee sails of a ship close-hauled in the wind shadow of her weather ones. Modelled
   crudely today (spec M0 to M2 §7.3, a shadow rule by position along the keel, since
   milestone 2; truth 5 rests on it) and not by geometry, which is what this item is
   about. (Corrected 2026-09-30 after the cold review; the first draft said "not modelled
   at all".)
4. **The view.** The deck view (gate 3b notes) and any fuller picture of the ship want
   the rig as a skeleton to project from.

## The principle: reduced models in three dimensions, never a physics engine

A general 3D engine (rigid bodies, meshes, colliders, fluid) costs a hundred to a
thousand times the compute per ship and is no more accurate for the questions the game
asks; the game's accuracy comes from the sources and the tuned models, not from
geometry. Naval architecture itself does not simulate a ship in a seaway with a mesh: it
uses response amplitude operators, reduced models of roll, pitch and heave as driven
oscillators with natural periods and damping, excited by a wave spectrum. That is a
handful of equations per ship, the same shape as the quasi-static heel, and the
professional method.

The shape to move toward:

1. **Sea state as a field** over the plane (significant wave height, period, direction),
   tied to the wind's history and fetch; reduced six-degree motion per ship driven by it,
   deterministic, cheap; the log says "she rolls her lee guns under" honestly. Sources to
   read when the time comes: the standard naval-architecture treatment of ship motions in
   waves (RAOs, Bretschneider or JONSWAP spectra), and the period's own words for a
   ship's behaviour in a sea (Falconer on rolling and pitching; Luce on scudding and
   lying to).
2. **The rig as a 3D skeleton**: masts, yards, booms, gaffs and stays as line segments
   with an athwartships coordinate (data we mostly have; the generator can supply the
   rest). Geometry checks on segments are trivial; blanketing becomes a wind-shadow test
   between sail centres along the apparent wind; the deck view and a fuller viewer
   project the same skeleton. No bodies, no collision engine.
3. **Ballistics closed-form** (a shot's arc from the gun's elevation, the charge and the
   roll), hits statistical against the target's silhouette by aspect and by the roll at
   the moment, damage to the parts the shot's height and line pass through.

## Scaling, which is not a 3D question

The frigate ticks at about 500 a second on the full rig model, so a dozen ships on it
would cap compression near 40x, whatever the geometry. The mitigation is level of detail
by distance, as every game does it: the player's ship and any ship she is engaged with
run the full rig; a ship on the horizon runs a point model with a polar diagram, which is
what the readings registry and the standing orders already treat a ship as from outside;
a ship in between runs the sail model without the crew. The reduced motion models add
almost nothing on top. A true 3D engine would break that budget; 3D-aware reduced
models keep it. Determinism under a seed holds throughout, since nothing here is more
than ordinary arithmetic.

## When

Nothing in milestone 4. The sea state and the reduced motions belong to the M5 world
specification; the rig skeleton and blanketing to the viewer and vessel-library work of
M8, or earlier if blanketing proves to matter for the pointing truths; ballistics to M7.
Each is to be specified with its sources named, as the rig geometry of 3b was.
