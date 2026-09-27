# Playtest 1: the frigate under all sail, gate 3b build

The first playtest record. It predates the playtest form (milestone 4c, spec M4 §22), so
it is kept in the form's headings as far as the material allows. `log.json` is the log
as the viewer served it (`/api/log?limit=5000`), saved from the browser; the gate 3b
build had no save from the viewer, so there is no save file. The orders in the log,
given in order under the same seed on the `gate-m3b` release, reproduce the voyage.

Drafted by the build session from the log and the owner's remarks in conversation; the
owner's own words are marked and may be amended.

## The scenario and seed

Frigate (`data/ships/frigate-36.yaml`), seed 7, the `gate-m3b` release. Open water, wind
N 15 knots gusting to 25, heading WNW at the start. Played in the viewer at 60x, from
04:00 to 12:30 ship's time on 1 June 1805: the morning watch and the forenoon watch and
half an hour of the afternoon watch. 756 log lines, 68 orders given, 46 carried out and
22 refused.

## What happened

- **04:00.** Plain sail set from a standing start, braced sharp up on the starboard tack.
  The watch on deck was short-handed for it and took the sails in turn (the log says so
  at the first tick). Leeway settled to 3 to 5 degrees within ten minutes.
- **04:16 to 04:55.** The topgallant masts sent down, all hands; the fore topsail
  goose-winged; the topgallant masts swayed up again. A drill, not a need: the owner was
  exercising the new evolutions.
- **05:08 to 05:13.** Sails trimmed, the topgallants and royals set. From 05:28 the royal
  masts and yards were logged working in the gusts (22 to 25 knots), close-hauled, and
  again at each gust through the morning watch; nothing carried away.
- **06:51 to 07:19.** The ringtail bent and set on the spanker. Steering 260 with the wind
  north, the ringtail shook and its boom whipped: "she is too near the wind to carry it".
  The owner reported this in conversation as the ringtail complaining at 260 with N 14
  gusting 20, and the depiction of the ringtail as beautiful.
- **09:20 to 09:25.** Six attempts to say "steer off the wind" before `bear off` was
  found (see the list below). Then `make all sail`, all hands, and the studding sails
  run out and set by 10:04.
- **10:08 to 10:58.** `keep her full`, steering 237 then 235, the sails trimmed
  repeatedly, `pipe down`. At 10:58 in a gust to 23 knots every studding sail boom, the
  royal masts and yards, the fore and main topgallant yards and the ringtail boom were
  logged working at once, and again at 11:26 and 12:00. Nothing carried away.
- **11:03 to 11:18.** The save-alls bent and set below the fore studding sails (the
  frigate carries save-alls, not a water sail, by the sources; the first two attempts
  asked for a water sail).
- **12:07 to 12:15.** Steered 237, 230, 225 and trimmed; the log ends at 12:30.

## What the owner ordered and why

*(Owner to amend.)* The morning was a drill of the 3b evolutions (topgallant masts down
and up, goose-winging, bowlines, the ringtail); the forenoon was a run to see the frigate
under everything she could carry: all plain sail, studding sails both sides, ringtail
and save-alls, in a fresh breeze gusting past 20 knots. The owner's screenshot of the
ship at this point: "That's a lot of sail!"

## What the owner wished to say and could not

The refused orders, grouped. Each is a vocabulary gap or a genuine refusal.

- **Steering off the wind.** `helm by and large`, `helm steer off the wind`, `helm off
  the wind`, `steer off the wind`, `bear off the wind`, `fall off`: six tries before
  `bear off`. "Off the wind" and "fall off" are sailors' words for bearing away and
  should be synonyms. "By and large" is a description, not a helm order, and is right to
  be refused.
- **Quarter points.** `steer SW by W quarter S` refused at "quarter". Quarter points are
  period-correct compass steering and should be accepted.
- **Collective parts.** `run out the stuns'l booms` / `the studdingsail booms` / `the
  booms` refused as no such part, although `run out the stuns'ls` was accepted; the
  booms should be a collective the way the sails are. `run out the ringtail outriggers` /
  `the ringtail gaff`: the part is the ringtail boom, and the refusal said so once the
  right word was tried.
- **`tend the sheets`.** Refused; it is one of the orders milestone 4a adds (spec M4 §7).
- **`muster` from the viewer.** Refused as a console command. The viewer should take the
  console's queries (`muster`, `the sail room`, `standing orders`, `state`) the same way.
- **The water sail on the frigate.** Refused correctly (she carries save-alls); the
  suggestion offered ("the all sail") was unhelpful.
- Two typos (`goose-wind`, `rintail`) were caught with a good suggestion.

## Numbers a sailor would call wrong

- **Leeway from a standing start.** "Leeway 145° to larboard", "157°", "156°" in the
  first three minutes, while the ship was gathering way from rest. Leeway has no
  meaning under about a knot and the line should not be logged until she has way on.
- **Royal masts working at 15 knots close-hauled.** Logged at every gust past about 20
  knots with the royals set close-hauled. Plausible by Luce (royals come in first when
  it freshens on a wind), but whether 20 to 25 knots is the right threshold is a
  tuning question for the rig geometry follow-ups.
- **The ringtail at 260 with the wind north.** The apparent wind was near 70 degrees
  off the bow; a boom-and-gaff ringtail on the spanker is a fair-wind sail and the
  complaint is by the sources. The owner found it right.

## How the day felt

*(Owner to amend.)* Played at 60x throughout. The strain lines during gusts were judged
"perfect so far" in conversation. The ringtail's depiction was called beautiful, with the
note that only its head should follow the gaff's angle (spec 3b open item 15).

## Follow-ups raised by this playtest

1. Synonyms `fall off`, `off the wind`, `bear off the wind` for bearing away (package 26
   has the steering verbs this wave).
2. Quarter points in compass headings.
3. Studding sail booms as a collective part for `rig out` / `run in`.
4. The viewer to accept the console's queries (`muster`, `the sail room`, `standing
   orders`, `state`) rather than refuse them as console commands.
5. No leeway line under a speed floor.
6. The ringtail's head follows the gaff (open item 15, already recorded).
7. **The agent doors are judged by a layman's first run** (owner's note at gate 4b, 2026-09-27):
   the owner's errors and misunderstandings at the harness, the doors and the setup
   documents are design notes about the doors, not about the owner. First case: the
   practice consent conversation at the REPL stumbled on the blank line that sends a
   reply and on the `>` before a tool call; both were fixed in the door the same day.
