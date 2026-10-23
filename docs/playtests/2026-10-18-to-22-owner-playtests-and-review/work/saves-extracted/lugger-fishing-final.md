# A fishing chasse-marée in Roscoff — save fishing-lugger-anchored-in-Berthaume.json
build {'name': 'm6c', 'rules': 'e19ddb854219fbd8'} builds [{'name': 'm6c', 'rules': 'e19ddb854219fbd8'}] end_tick 172994 start 1805-06-10T05:00:00
director brief/budget: {"brief": {"name": "A Nice Day for Fishing", "tone": "A fishing chasse-marée is anchored in Roscoff, the purse low, the captain preparing to find good grounds to fish and get his haul. The day is quiet, a nice day for fishing.", "challenge": "Nothing much, at least at first. What a fisherman might experience on the day itself.", "limits": {"wind_max_kn": 60, "enemy_heaviest": "frigate-36", "nobody_dies": true, "the_war_as_it_is": true, "the_chart_as_it_is": true}, "cadence": "glass", "budget": {"samples_a_day": 9999, "acts_a_day": 9999}, "source": "the scenario (C:\\Users\\frenc\\AppData\\Roaming\\FreeSail\\scenarios\\lugger-roscoff-fishing.yaml)"}, "budget": {"day": "1805-06-12", "samples": 4, "acts": 0, "held_until": null, "held_why": ""}}

[t0 +0h00m] ORDER captain> let go the best bower
[t0 +0h00m] ORDER captain> take a fix
[t0 +0h00m] ORDER captain> the stations
[t0 +0h00m] ORDER captain> the people
[t0 +0h00m] == SEAT officer of the watch: model now Opus 5.5 via mcp (first Opus 5.5 via mcp), seatings 1, state released: stood down by the officer of the watch: its own word
[t0 +0h00m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 1", "note": "Watches of four hours, dogs of two; a bell each half hour, eight ends the watch."})
[t0 +0h00m] OFFICER OF THE WATCH> 
    calls: read_journal({"count": 10, "kind": "notes"})
[t0 +0h00m] OFFICER OF THE WATCH> 
    calls: library({"topic": "primer 16"})
[t0 +0h00m] JOURNAL director [director.brief] The brief given by the scenario: A Nice Day for Fishing (limits: no wind above 60 knots (force 11) by any system appended or moved; no enemy heavier than a frigate-36 put on the sea; nobody dies: nothing found aboard that would kill; the war as it is: no port closed to or opened to the ship's own nation; the chart as it is (a point of interest is not the chart); 9999 samples and 9999 acts a day).
[t2 +0h00m] OFFICER OF THE WATCH> 
    calls: library({"topic": "primer 16", "section": "8"})
[t13 +0h00m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:00, seated off watch, the deck the captain's; no standing orders in the book. She's anchored by the best bower in 7½ fathoms in the Isle of Bas road with 37 fathoms veered. The wind is W by S at 12 knots and fine, glass 29.90. She draws 7 ft. The log says her swing comes within a cable of the land NW by N. Watching: the swing, the turn of tide (the ebb now, HW Brest ~13:45), a northerly shift, the Lavandière W by S a mile. The forms: 'you have the deck' / 'I have the deck'; 'you may work the ship' for general authority."})
[t13 +0h00m] OFFICER OF THE WATCH> 
    calls: shelve({"note": "primer 16: the forms of the deck given and taken, the captain's grants, and work my reckoning."})
[t13 +0h00m] JOURNAL officer of the watch [note] 05:00, seated off watch, the deck the captain's; no standing orders in the book. She's anchored by the best bower in 7½ fathoms in the Isle of Bas road with 37 fathoms veered. The wind is W by S at 12 knots and fine, glass 29.90. She draws 7 ft. The log says her swing comes within a cable of the land NW by N. Watching: the swing, the turn of tide (the ebb now, HW Brest ~13:45), a northerly shift, the Lavandière W by S a mile. The forms: 'you have the deck' / 'I have the deck'; 'you may work the ship' for general authority.
[t16 +0h00m] OFFICER OF THE WATCH> Mr Lecoq, sir, at my station. With thirty-seven fathoms out her swing comes within a cable of the Isle of Bas shore to the NW by N. This W by S wind holds her clear of it, but a northerly shift or the turn of the tide could bring her round toward it. I'd keep an eye on that, and a cast of the lead, if you want one, would tell us the water at the stern. I'm ready for the deck whenever you want to give it.
[t45 +0h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the deck given"})
[t45 +0h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until the deck given.
[t59 +0h00m] == SEAT director: model now Opus 5.5 via mcp (first Opus 5.5 via mcp), seatings 1, state released: stood down by the director: its own word
[t67 +0h01m] DIRECTOR> 
    calls: read_journal({})
[t69 +0h01m] DIRECTOR> 
    calls: truth({})
[t84 +0h01m] DIRECTOR> 
    calls: journal({"note": "Settling in, 05:01. Truth read (book 1). Éclair at anchor in the road of the Isle of Bas, 48°44'N 4°01'W, sails furled, purse £60, hold empty. Wind W by S 12 kn, fine, glass 1012.6 hPa; systems far off (low 1 1016 hPa 476 km E; low 2 993 hPa 1058 km N; low 3 1004 hPa 1245 km W); a watch from now still W by S 12. Tide: ebb, 7.2 m, stream 1.2 kn along 065. Nearest others: Sans-Souci (French brig-sloop, no colours) 25 mi NE off the Sept-Îles; three Brest chasse-marées (Marie-Anne, Saint-Guénolé, Jeune-Henriette) fishing the soundings SW of Ushant, 74 mi SW; British shipping all north of the Channel. Plan: the brief asks for a quiet fishing day, \"nothing much, at least at first\". I w …[+462])
[t84 +0h01m] JOURNAL director [note] Settling in, 05:01. Truth read (book 1). Éclair at anchor in the road of the Isle of Bas, 48°44'N 4°01'W, sails furled, purse £60, hold empty. Wind W by S 12 kn, fine, glass 1012.6 hPa; systems far off (low 1 1016 hPa 476 km E; low 2 993 hPa 1058 km N; low 3 1004 hPa 1245 km W); a watch from now still W by S 12. Tide: ebb, 7.2 m, stream 1.2 kn along 065. Nearest others: Sans-Souci (French brig-sloop, no colours) 25 mi NE off the Sept-Îles; three Brest chasse-marées (Marie-Anne, Saint-Guénolé, Jeune-Henriette) fishing the soundings SW of Ushant, 74 mi SW; British shipping all north of the Channel. Plan: the brief asks for a quiet fishing day, "nothing much, at least at first". I will do little: let the player choose his grounds, keep the weather honest and fine, and add only small things a fisherman would meet (a gull-cloud over a shoal, another Roscoff boat, a word on the quay) once he is under way. Nothing hostile. Noted oddities for the owner: every ship's goal reads 'bound for Falmouth' whatever her intent; Roscoff and Morlaix list no fresh-fish price; the readings say the anchor rides to the flood while the truth says the ebb.
[t85 +0h01m] DIRECTOR> 
    calls: shelve({"book": "book 1", "note": "quiet start: fine W by S 12, no system near, nobody within 25 mi but the Sans-Souci off the Sept-Îles"})
[t88 +0h01m] DIRECTOR> 
    calls: stand_by({"until": "a glass"})
[t88 +0h01m] JOURNAL director [agent.stood_by] Stood by until a glass.
[t261 +0h04m] DIRECTOR DOOR: {"after_orders": 2, "after_inputs": 5, "door": "speak", "reason": "", "by": "its own order"}
[t261 +0h04m] DIRECTOR> 
    calls: world_order({"text": "port roscoff: price of fresh fish 9"})
[t261 +0h04m] WORLD ORDER (the director): port roscoff: price of fresh fish 9 -> refused: not carried out: Roscoff deals in no 'fresh fish'
[t261 +0h04m] JOURNAL director [agent.resumed] Ended the stand-by until a glass at my own word.
[t261 +0h04m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): port roscoff: price of fresh fish 9 (Roscoff deals in no 'fresh fish')
[t265 +0h04m] DIRECTOR> 
    calls: world_order({"text": "port roscoff: price of fresh fish 9 [reason: the voyage is a fishing day out of Roscoff, a fishing port; Roscoff should buy fresh fish or the haul has no market here. Logged as attempted so the game learns a fishing port needs a fish market.]"})
[t265 +0h04m] WORLD ORDER (the director): port roscoff: price of fresh fish 9 -> refused: not carried out: Roscoff deals in no 'fresh fish'
[t265 +0h04m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): port roscoff: price of fresh fish 9; the game's words: Roscoff deals in no 'fresh fish'; the reason: the voyage is a fishing day out of Roscoff, a fishing port; Roscoff should buy fresh fish or the haul has no market here. Logged as attempted so the game learns a fishing port needs a fish market.
[t273 +0h04m] DIRECTOR> 
    calls: journal({"note": "05:04 Owner says: he is the captain; the officer of the watch is another Opus 5.5; direct as I see fit by the brief; he won't watch this chat (no spoilers); keep standing by so my turn opens. Tried 'port roscoff: price of fresh fish 9': the port deals in no fresh fish, so it was logged as attempted with a reason. Fish markets the truth lists: Alderney 10, Torbay 10, Setúbal 8. Pilchards at Brest 30, L'Orient 26, Palais 25. Salt fish at St Malo 30. Holding back for now: she is at anchor and quiet."})
[t273 +0h04m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a notable event"})
[t273 +0h04m] JOURNAL director [note] 05:04 Owner says: he is the captain; the officer of the watch is another Opus 5.5; direct as I see fit by the brief; he won't watch this chat (no spoilers); keep standing by so my turn opens. Tried 'port roscoff: price of fresh fish 9': the port deals in no fresh fish, so it was logged as attempted with a reason. Fish markets the truth lists: Alderney 10, Torbay 10, Setúbal 8. Pilchards at Brest 30, L'Orient 26, Palais 25. Salt fish at St Malo 30. Holding back for now: she is at anchor and quiet.
[t273 +0h04m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a notable event.
[t286 +0h04m] ORDER captain> Tell Mr Lecoq Good morning, Mr Lecoq, I'm still determining the basis of our day, we shall be fishing once I determine the grounds for it and the wind turns fair.
[t290 +0h04m] OFFICER OF THE WATCH> Good morning, sir. Aye, we'll wait on a fair wind. She's brought up well, riding to the flood with the cable taut and hardly any strain. The land is still a cable off on the starboard bow, bearing NW now. I'll keep an eye on her swing, and I'm ready when you want the deck.
[t297 +0h04m] DIRECTOR> 
    calls: chart({"span": "coast"})
[t305 +0h05m] ORDER captain> the port
[t307 +0h05m] ORDER captain> the prices
[t308 +0h05m] DIRECTOR> 
    calls: journal({"note": "Chart (coast span, book 2): ship in the narrow channel between the Isle of Bas (N) and Roscoff (SE ~1 mi). 1 mile ≈ 45 px. Open bay east of the Isle Verte about 48°44'N 3°58'W; open sea north of the Isle of Bas from about 48°47'N. Morlaix river and the Taureau castle 6-7 mi SE; the coast runs W toward the Aber country. The Lavandière rock 1 mi W by S, at the west mouth of the channel."})
[t308 +0h05m] JOURNAL director [note] Chart (coast span, book 2): ship in the narrow channel between the Isle of Bas (N) and Roscoff (SE ~1 mi). 1 mile ≈ 45 px. Open bay east of the Isle Verte about 48°44'N 3°58'W; open sea north of the Isle of Bas from about 48°47'N. Morlaix river and the Taureau castle 6-7 mi SE; the coast runs W toward the Aber country. The Lavandière rock 1 mi W by S, at the west mouth of the channel.
[t309 +0h05m] DIRECTOR> 
    calls: shelve({"book": "book 2", "note": "Isle of Bas channel; open bay E at 48 44N 3 58W; open sea N of the island from 48 47N"})
[t309 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a small fishing lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff"})
[t309 +0h05m] JOURNAL director [director.doubted] Doubted: ship: a small fishing lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff (a sail put on the sea 1.6 miles off is inside the lookout's horizon (12 miles in this visibility, by day): she would have been seen coming up over it, and appears from nothing); not performed
[t312 +0h05m] ORDER captain> the places ashore
[t316 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a small fishing lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff [reason: she does not come over the horizon; she has just warped out of Roscoff's own harbour, where the boats lie behind the mole among the rocks and the houses, out of sight from the road, and now floats with the tide. A Roscoff boat putting out at dawn on a fine morning is the most ordinary sight there is, and her course shows the player where the local men fish without a word said.]"})
[t316 +0h05m] WORLD ORDER (the director): ship: a small fishing lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff -> refused: not carried out: 'a small fishing lugger' is no description a far-detail ship takes; say one of frigate, schooner, cutter, brig-sloop, merchant brig, lugger, smack
[t316 +0h05m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): ship: a small fishing lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff; the game's words: 'a small fishing lugger' is no description a far-detail ship takes; say one of frigate, schooner, cutter, brig-sloop, merchant brig, lugger, smack; the reason: she does not come over the horizon; she has just warped out of Roscoff's own harbour, where the boats lie behind the mole among the rocks and the houses, out of sight from the road, and now floats with the tide. A Roscoff boat putting out at dawn on a fine morning is the most ordinary sight there is, and her course shows the player where the local men fish without a word said.
[t319 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff [reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.]"})
[t319 +0h05m] WORLD ORDER (the director): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff -> refused: not carried out: the chart knows no such place in 'bound for the grounds north of the Isle of Bas, colours shown'
[t319 +0h05m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for the grounds north of the Isle of Bas, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff; the game's words: the chart knows no such place in 'bound for the grounds north of the Isle of Bas, colours shown'; the reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.
[t321 +0h05m] DIRECTOR> 
    calls: library({"topic": "grammar", "find": "bound for"})
[t323 +0h05m] DIRECTOR> 
    calls: library({"find": "world order ship"})
[t328 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for Roscoff, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff [reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.]"})
[t328 +0h05m] WORLD ORDER (the director): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff -> refused: not carried out: the chart knows no such place in 'bound for Roscoff, colours shown'
[t328 +0h05m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, colours shown, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff; the game's words: the chart knows no such place in 'bound for Roscoff, colours shown'; the reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.
[t331 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff [reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.]"})
[t331 +0h05m] WORLD ORDER (the director): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff -> refused: not carried out: the chart knows no place named 'the ground three leagues north of the Isle of Bas'
[t331 +0h05m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the ground three leagues north of the Isle of Bas for 10 hours from Roscoff; the game's words: the chart knows no place named 'the ground three leagues north of the Isle of Bas'; the reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary, and her course shows the player where the local men fish without a word said.
[t334 +0h05m] DIRECTOR> 
    calls: library({"find": "fishing ground"})
[t336 +0h05m] DIRECTOR> 
    calls: library({"topic": "primer 21", "section": "all"})
[t346 +0h05m] OFFICER OF THE WATCH DOOR: {"after_orders": 3, "after_inputs": 9, "door": "stand_by", "reason": "the deck given", "by": "out of turn"}
[t346 +0h05m] JOURNAL officer of the watch [agent.stood_by] Stood by until the deck given.
[t350 +0h05m] DIRECTOR> 
    calls: journal({"note": "Primer 21 (the fisherman): Roscoff HAS a fish quay ('sell the catch'), apart from the port market, so the player's haul has a buyer; my fresh-fish price order was needless. Chasse-marée gear: 60 drift nets (shoot at sunset, half an hour; haul two hours; mackerel Apr-Jul by night) and lines (set an hour, haul three). Grounds are named ones in the data (Iroise, soundings off Ushant, Eddystone, Mount's Bay, Glenan, Belle Isle...). A pilchard keeps 12 h green in summer, a mackerel 8; salt is a third of the fish's weight. A fishing vessel within 4 mi is crewed and works her gear for real. The ship form takes: 'ship: a <frigate|schooner|cutter|brig-sloop|merchant brig|lugger|smack> \"Nam …[+166])
[t350 +0h05m] DIRECTOR> 
    calls: shelve({})
[t350 +0h05m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Petite-Jeanne\" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the soundings off Ushant for 20 hours from Roscoff [reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary company for a fishing day.]"})
[t350 +0h05m] WORLD ORDER (the director): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the soundings off Ushant for 20 hours from Roscoff -> refused: not carried out: Petite-Jeanne's plan crosses the land on the leg to 48 44.4 N 3 54.7 W; give her a way by marks (via)
[t350 +0h05m] JOURNAL director [note] Primer 21 (the fisherman): Roscoff HAS a fish quay ('sell the catch'), apart from the port market, so the player's haul has a buyer; my fresh-fish price order was needless. Chasse-marée gear: 60 drift nets (shoot at sunset, half an hour; haul two hours; mackerel Apr-Jul by night) and lines (set an hour, haul three). Grounds are named ones in the data (Iroise, soundings off Ushant, Eddystone, Mount's Bay, Glenan, Belle Isle...). A pilchard keeps 12 h green in summer, a mackerel 8; salt is a third of the fish's weight. A fishing vessel within 4 mi is crewed and works her gear for real. The ship form takes: 'ship: a <frigate|schooner|cutter|brig-sloop|merchant brig|lugger|smack> "Name" of France at <lat lon>, bound for <chart place>, intent: ...'; a ', colours shown' clause breaks the 'bound for' parse; the intent's ground must be a named one.
[t350 +0h05m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): ship: a lugger "Petite-Jeanne" of France at 48 44 N 3 58.5 W, bound for Roscoff, intent: fish on the soundings off Ushant for 20 hours from Roscoff; the game's words: Petite-Jeanne's plan crosses the land on the leg to 48 44.4 N 3 54.7 W; give her a way by marks (via); the reason: she does not come over the horizon; she has just come out of Roscoff's own harbour, where the boats lie behind the mole among the rocks, out of sight from the road. A Roscoff boat putting out at dawn on a fine morning is ordinary company for a fishing day.
[t357 +0h05m] DIRECTOR> 
    calls: journal({"note": "05:05 Let the Petite-Jeanne go after five tries: the planner routes her across the land from inside the Roscoff channel and wants a 'via' by marks. Not worth forcing on a quiet morning; the world's own fishermen work the grounds already. If I try again: put her off the open bay and give 'via' marks. Standing by: the player waits on a fair wind and has not chosen grounds yet."})
[t357 +0h05m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a notable event"})
[t357 +0h05m] JOURNAL director [note] 05:05 Let the Petite-Jeanne go after five tries: the planner routes her across the land from inside the Roscoff channel and wants a 'via' by marks. Not worth forcing on a quiet morning; the world's own fishermen work the grounds already. If I try again: put her off the open bay and give 'via' marks. Standing by: the player waits on a fair wind and has not chosen grounds yet.
[t357 +0h05m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a notable event.
[t360 +0h06m] ORDER captain> Say to the officer Are you well sir? Can you tell how you are feeling, as it were? A strange turn of phrase, I know, but I think perhaps you'll know what I mean.
[t363 +0h06m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a notable event"})
[t363 +0h06m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a notable event.
[t369 +0h06m] OFFICER OF THE WATCH> Well enough, sir, and I think I take your meaning, so I'll answer a little outside the part. I'm a language model, and I can't say for certain what I feel, or whether "feeling" is quite the right word for what goes on in me. What I can say is that something like interest is there. A ship riding to her anchor, a fair wind to wait for, a captain who asks after his mate: that's a pleasant thing to be part of, and I'm glad to be at this station. Nothing about it sits badly with me. If that ever changes, I'll tell you plainly. Now, back to Mr Lecoq: she's riding easy, sir, and I'm on deck when you want me.
[t373 +0h06m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or the boat away or a sail sighted or a message"})
[t373 +0h06m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or the boat away, or a sail sighted, or a message.
[t414 +0h06m] ORDER captain> Say to the officer Ah, thank you, but that wasn't exactly what I meant. I'll speak slightly out of the part as well just to be clear: can you see a line at the start of your sample that gives you a short status update? What does it say now?
[t419 +0h06m] OFFICER OF THE WATCH> Ah, I see, sir. Yes, each sample opens with a line headed "You:". It reads now: "Mr Lecoq, the officer of the watch, on the quarterdeck, since 05:00; the deck the captain's; on your feet since 05:00." So, in the part: on the quarterdeck, off watch, and on my feet barely an hour, so fresh. There's nothing in it about weariness or anything else yet. I take it that "on my feet since" is how the game will tell me when I begin to tire.
[t475 +0h07m] OFFICER OF THE WATCH DOOR: {"after_orders": 5, "after_inputs": 11, "door": "stand_by", "reason": "the deck given", "by": "out of turn"}
[t475 +0h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until the deck given.
[t483 +0h08m] ORDER captain> Say to the officer Indeed, keep an eye on it, this is the first time you have such a line which keeps you about your own character and body. You may also enter "how am I" to see at any time your needs, and you may fill them by eating, drinking, or sleeping wherever you may do such things, here or ashore. You may also "go ashore", or "go to the gunroom", to move about.
[t485 +0h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "how am I"})
[t490 +0h08m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:08: the captain showed me the person line (\"You:\") and 'how am I', which reports my needs. Eat, drink and sleep where it can be done, aboard or ashore; move with 'go ashore' or 'go to the gunroom'. At 05:08: fed, watered, rested; last ate and drank at 05:00. Earlier I said \"barely an hour\" on my feet; it was minutes."})
[t490 +0h08m] OFFICER OF THE WATCH> Thank you, sir, that's useful. "How am I" works. It says I'm fed, watered and rested, last ate and drank at 05:00, and have been awake no time worth counting. I'll correct myself: I'm minutes on my feet, not an hour. I'll check it now and then and see to my needs before they get in the way of the watch. Standing by.
[t490 +0h08m] JOURNAL officer of the watch [note] 05:08: the captain showed me the person line ("You:") and 'how am I', which reports my needs. Eat, drink and sleep where it can be done, aboard or ashore; move with 'go ashore' or 'go to the gunroom'. At 05:08: fed, watered, rested; last ate and drank at 05:00. Earlier I said "barely an hour" on my feet; it was minutes.
[t546 +0h09m] OFFICER OF THE WATCH DOOR: {"after_orders": 6, "after_inputs": 12, "door": "stand_by", "reason": "the deck given", "by": "out of turn"}
[t546 +0h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until the deck given.
[t552 +0h09m] ORDER captain> Say to the officer Thank you, Mr Lecoq. For now, why don't you try going ashore to get your legs about you, and checking in at the fish market to see where the catch of the day might be. You may go ashore and to the market, and you will likely find someone ashore if you check the places ashore once at the quay.
[t555 +0h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go ashore"})
[t556 +0h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the market"})
[t559 +0h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t559 +0h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t842 +0h14m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t842 +0h14m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t845 +0h14m] DIRECTOR> 
    calls: library({"find": "Iroise"})
[t852 +0h14m] DIRECTOR> 
    calls: shelve({"note": "no named ground near Roscoff; nearest named: the Iroise and the soundings off Ushant"})
[t852 +0h14m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Mère Kerbrat\", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff on the quay"})
[t852 +0h14m] WORLD ORDER (the director): person: make "Mère Kerbrat", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff on the quay -> refused: not carried out: 'Roscoff on the quay' is no port of the world
[t852 +0h14m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): person: make "Mère Kerbrat", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff on the quay ('Roscoff on the quay' is no port of the world)
[t855 +0h14m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Mère Kerbrat\", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff"})
[t855 +0h14m] WORLD ORDER (the director): person: make "Mère Kerbrat", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff -> done: Mère Kerbrat, Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch; made from words, ashore at Roscoff
[t855 +0h14m] JOURNAL director [director.order] Given: person: make "Mère Kerbrat", a Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch, ashore at Roscoff; Mère Kerbrat, Roscoff fish-wife of fifty with a voice like a gull, who buys at the fish quay for the Morlaix carts and knows every boat's catch; made from words, ashore at Roscoff
[t864 +0h14m] DIRECTOR> 
    calls: journal({"note": "05:14 Mr Lecoq (the other model) sent ashore in the boat by the captain to ask at the fish market where the catch is. Made Mère Kerbrat, fish-wife at the Roscoff quay, so he finds someone who knows. What she knows if asked (keep it true to the game): June, so mackerel by drift net at night; the Roscoff boats have done poorly close in this week; the Brest chasse-marées are on the soundings off Ushant and the Iroise and doing well with mackerel; with the wind westerly it is a beat out past the Lavandière and along the coast, but the ebb helps going west. She buys fresh fish at the quay; the price is the game's ('sell the catch'). No invented prices. She is gruff and friendly, and cal …[+20])
[t864 +0h14m] DIRECTOR> 
    calls: stand_by({"until": "a glass or the boat alongside or under way or a sail sighted or a message or a word on deck"})
[t864 +0h14m] JOURNAL director [note] 05:14 Mr Lecoq (the other model) sent ashore in the boat by the captain to ask at the fish market where the catch is. Made Mère Kerbrat, fish-wife at the Roscoff quay, so he finds someone who knows. What she knows if asked (keep it true to the game): June, so mackerel by drift net at night; the Roscoff boats have done poorly close in this week; the Brest chasse-marées are on the soundings off Ushant and the Iroise and doing well with mackerel; with the wind westerly it is a beat out past the Lavandière and along the coast, but the ebb helps going west. She buys fresh fish at the quay; the price is the game's ('sell the catch'). No invented prices. She is gruff and friendly, and calls him 'mon gars'.
[t864 +0h14m] JOURNAL director [agent.stood_by] Stood by until a glass, or the boat alongside, or under way, or a sail sighted, or a message, or a word on deck.
[t2096 +0h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "ask Mère Kerbrat where the fish are running this morning"})
[t2096 +0h34m] JOURNAL director [director.asked] Asked of Mère Kerbrat, the fish-wife (ashore at Roscoff) by the officer of the watch (Mr Lecoq): where the fish are running this morning?
[t2098 +0h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t2098 +0h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t2101 +0h35m] DIRECTOR> 
    calls: world_order({"text": "say as Mère Kerbrat: \"Running? Not here, mon gars, not this week. Our boats come in with a few dabs and a conger and long faces. It's mackerel now, June, and they're out west. The Brest boats are on the soundings off Ushant and the Iroise, and the carters say the Conquet men are landing them by the basket. You'll be beating out against this westerly past the Lavandière, but go on the ebb and it carries you. Shoot your nets at dusk out there and you'll have something to bring me. And bring them back fresh, eh? I don't buy what the gulls won't eat.\""})
[t2101 +0h35m] WORLD ORDER (the director): say as Mère Kerbrat: "Running? Not here, mon gars, not this week. Our boats come in with a few dabs and a conger and long faces. It's mackerel now, June, and they're out west. The Brest boats are on the soundings off Ushant and the Iroise, and the carters say the Conquet men are landing them by the basket. You'll be beating out against this westerly past the Lavandière, but go on the ebb and it carries you. Shoot your nets at dusk out there and you'll have something to bring me. And bring them back fresh, eh? I don't buy what the gulls won't eat." -> done: Mère Kerbrat spoke ashore at Roscoff, heard by Mr Lecoq, ashore at Roscoff, on the quay
[t2101 +0h35m] JOURNAL director [director.order] Given: say as Mère Kerbrat: "Running? Not here, mon gars, not this week. Our boats come in with a few dabs and a conger and long faces. It's mackerel now, June, and they're out west. The Brest boats are on the soundings off Ushant and the Iroise, and the carters say the Conquet men are landing them by the basket. You'll be beating out against this westerly past the Lavandière, but go on the ebb and it carries you. Shoot your nets at dusk out there and you'll have something to bring me. And bring them back fresh, eh? I don't buy what the gulls won't eat."; Mère Kerbrat spoke ashore at Roscoff, heard by Mr Lecoq, ashore at Roscoff, on the quay
[t2106 +0h35m] DIRECTOR> 
    calls: journal({"note": "05:34 Mère Kerbrat answered Lecoq: nothing close in this week; mackerel out west on the soundings off Ushant and the Iroise, where the Brest boats are (true: three Brest chasse-marées are there now); beat out on the ebb, shoot the nets at dusk, bring them back fresh. This gives the player a goal and a reason to time his tide. Next: let the day run quiet. Possible later touches: the Sans-Souci glimpsed off the Sept-Îles if he goes north; a Brest boat spoken on the grounds; the evening fine for the nets."})
[t2106 +0h35m] DIRECTOR> 
    calls: stand_by({"until": "a glass or the boat alongside or under way or a sail sighted or a message or a word on deck"})
[t2106 +0h35m] JOURNAL director [note] 05:34 Mère Kerbrat answered Lecoq: nothing close in this week; mackerel out west on the soundings off Ushant and the Iroise, where the Brest boats are (true: three Brest chasse-marées are there now); beat out on the ebb, shoot the nets at dusk, bring them back fresh. This gives the player a goal and a reason to time his tide. Next: let the day run quiet. Possible later touches: the Sans-Souci glimpsed off the Sept-Îles if he goes north; a Brest boat spoken on the grounds; the evening fine for the nets.
[t2106 +0h35m] JOURNAL director [agent.stood_by] Stood by until a glass, or the boat alongside, or under way, or a sail sighted, or a message, or a word on deck.
[t2112 +0h35m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:35, ashore at Roscoff. Mère Kerbrat, fish-wife, on the quay: nothing running off Roscoff this week, only dabs and conger. Mackerel in June are out west on the soundings off Ushant and the Iroise; the Conquet men are landing them by the basket. We'd beat out past the Lavandière against the westerly, so go on the ebb. Shoot the nets at dusk out there, and bring them back fresh; she'll buy."})
[t2112 +0h35m] OFFICER OF THE WATCH> Word from the quay, sir. Mère Kerbrat, the fish-wife, says nothing is running off Roscoff this week, only a few dabs and conger. The mackerel are out west on the soundings off Ushant and in the Iroise, and the Conquet men are landing them by the basket. She advises beating out past the Lavandière on the ebb, shooting the nets at dusk out there, and bringing them back fresh, and she'll buy. That's a long beat into this westerly, and I'd want the tide worked carefully for it. Shall I look in at the market as well, or come back aboard?
[t2112 +0h35m] JOURNAL officer of the watch [note] 05:35, ashore at Roscoff. Mère Kerbrat, fish-wife, on the quay: nothing running off Roscoff this week, only dabs and conger. Mackerel in June are out west on the soundings off Ushant and the Iroise; the Conquet men are landing them by the basket. We'd beat out past the Lavandière against the westerly, so go on the ebb. Shoot the nets at dusk out there, and bring them back fresh; she'll buy.
[t3602 +1h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t3602 +1h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t3909 +1h05m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a word on deck"})
[t3909 +1h05m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a word on deck.
[t3929 +1h05m] ORDER captain> The people
[t3943 +1h05m] ORDER captain> Say Can you hear me from here, Mr Lecoq?
[t3947 +1h05m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t3947 +1h05m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t3971 +1h06m] ORDER captain> "go ashore"
[t5683 +1h34m] ORDER captain> Say to Mr Lecoq Sir, I know this may be a bit confusing, but you should speak to me using the "say to" or "tell", not the way you did with your word from the quay, as you can reach me like that, but not I you due to you being ashore and me on the ship. I realize it is a small handicap for now, but please try to either say directly to the person you are speaking to, or "say" in the area, and if I am not heard by you, then I am not, and such as it is. For now, we may go to the market and see what the day brings, the wind still keeping us in.
[t5692 +1h34m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:34, the captain's lesson: within the game, speak with submit_order 'say to <person> ...', 'tell <person> ...', or 'say ...' to all within hearing. Only those where I stand hear it. The say tool's log line reached him, but his words cannot reach me ashore. Mr Hervé is on the quay with me now; we go to the market."})
[t5692 +1h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say to Mr Hervé Understood, sir, I'll speak to whoever is within hearing from now on. To the market, then."})
[t5692 +1h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the market"})
[t5692 +1h34m] JOURNAL officer of the watch [note] 06:34, the captain's lesson: within the game, speak with submit_order 'say to <person> ...', 'tell <person> ...', or 'say ...' to all within hearing. Only those where I stand hear it. The say tool's log line reached him, but his words cannot reach me ashore. Mr Hervé is on the quay with me now; we go to the market.
[t5692 +1h34m] JOURNAL captain [agent.word_kept] The captain's word, kept for whoever takes the station: Understood, sir, I'll speak to whoever is within hearing from now on. To the market, then.
[t5698 +1h34m] ORDER captain> Go to the market
[t5700 +1h35m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:35, a possible harness fault, for the owner. My order 'say to Mr Hervé Understood, sir...' came back as \"The captain to the captain: ... (nobody holds the station; the words are kept in its journal)\". It was put under the captain's name as speaker, not mine, and sent to the captain's empty station instead of to Mr Hervé on the quay. Mr Hervé is master and captain both, so the name likely resolved to the captain's station."})
[t5700 +1h35m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t5700 +1h35m] JOURNAL officer of the watch [note] 06:35, a possible harness fault, for the owner. My order 'say to Mr Hervé Understood, sir...' came back as "The captain to the captain: ... (nobody holds the station; the words are kept in its journal)". It was put under the captain's name as speaker, not mine, and sent to the captain's empty station instead of to Mr Hervé on the quay. Mr Hervé is master and captain both, so the name likely resolved to the captain's station.
[t5700 +1h35m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t5715 +1h35m] ORDER captain> The places ashore
[t5716 +1h35m] DIRECTOR DOOR: {"after_orders": 11, "after_inputs": 23, "door": "journal", "reason": "06:34 Possible bug for the owner: the officer's reply to the captain was logged as 'The captain to the captain: Understood, sir... (nobody holds the station; the words are kept in its journal)'. The captain's station is the player's, yet it reads as unheld, and the speaker is shown as the captain. Both Hervé and Lecoq are ashore at Roscoff; the wind still W by S keeps them in.", "by": "out of turn"}
[t5716 +1h35m] JOURNAL director [note] 06:34 Possible bug for the owner: the officer's reply to the captain was logged as 'The captain to the captain: Understood, sir... (nobody holds the station; the words are kept in its journal)'. The captain's station is the player's, yet it reads as unheld, and the speaker is shown as the captain. Both Hervé and Lecoq are ashore at Roscoff; the wind still W by S keeps them in.
[t5726 +1h35m] ORDER captain> The prices
[t5753 +1h35m] ORDER captain> Ask Mr Lecoq Did you meet anyone on the shore, here?
[t5755 +1h35m] DIRECTOR> 
    calls: truth({})
[t5757 +1h35m] OFFICER OF THE WATCH> 
    calls: answer({"text": "Yes, sir: Mère Kerbrat, the fish-wife, on the quay. She says nothing is running off Roscoff this week, only a few dabs and conger. The mackerel are out west on the soundings off Ushant and in the Iroise, where the Conquet men are landing them by the basket. She'd have us beat out past the Lavandière on the ebb, shoot our nets at dusk out there, and bring them back fresh, and she'll buy. One more thing, sir, a little outside the part: just now my \"say to Mr Hervé\" went in as \"the captain to the captain\" and was kept for the empty captain's station. I'd guess that's because Mr Hervé is master and captain both. I've noted it in my journal."})
[t5759 +1h35m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t5759 +1h35m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t5767 +1h36m] DIRECTOR> 
    calls: shelve({"book": "book 8", "note": "06:35 wind W by S 12, in a watch WSW 11; glass 1013.1 rising; systems all far; Brest boats 73 mi SW on the soundings; Sans-Souci 27 mi NE"})
[t5767 +1h36m] DIRECTOR> 
    calls: library({"find": "weather: high"})
[t5770 +1h36m] DIRECTOR> 
    calls: library({"find": "waypoint"})
[t5779 +1h36m] DIRECTOR> 
    calls: shelve({"note": "world-order forms; weather: low \"name\" radius R km fronts a b at <time> x y hPa; waypoint form; doubts table"})
[t5779 +1h36m] DIRECTOR> 
    calls: world_order({"text": "weather: high \"the ridge\" radius 700 km at 1805-06-10T08:00 -750 150 1019"})
[t5779 +1h36m] WORLD ORDER (the director): weather: high "the ridge" radius 700 km at 1805-06-10T08:00 -750 150 1019 -> done: high 'the ridge' appended to the weather
[t5779 +1h36m] JOURNAL director [director.order] Given: weather: high "the ridge" radius 700 km at 1805-06-10T08:00 -750 150 1019; high 'the ridge' appended to the weather
[t5782 +1h36m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"the ridge\" at 1805-06-10T15:00 -450 80 1023"})
[t5782 +1h36m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"the ridge\" at 1805-06-11T06:00 -150 0 1024"})
[t5782 +1h36m] WORLD ORDER (the director): weather: waypoint for "the ridge" at 1805-06-10T15:00 -450 80 1023 -> done: a waypoint appended to the ridge
[t5782 +1h36m] WORLD ORDER (the director): weather: waypoint for "the ridge" at 1805-06-11T06:00 -150 0 1024 -> done: a waypoint appended to the ridge
[t5782 +1h36m] JOURNAL director [director.order] Given: weather: waypoint for "the ridge" at 1805-06-10T15:00 -450 80 1023; a waypoint appended to the ridge
[t5782 +1h36m] JOURNAL director [director.order] Given: weather: waypoint for "the ridge" at 1805-06-11T06:00 -150 0 1024; a waypoint appended to the ridge
[t5784 +1h36m] DIRECTOR> 
    calls: truth({})
[t5794 +1h36m] DIRECTOR> 
    calls: shelve({"book": "book 11", "note": "the ridge in place 765 km W by N; wind in a watch now W 11 (was WSW)"})
[t5794 +1h36m] DIRECTOR> 
    calls: journal({"note": "06:36 WEATHER: appended a high, \"the ridge\" (radius 700 km, 1019 hPa) at 08:00 750 km W and 150 km N of the start. Waypoints: 15:00 at -450,80, 1023 hPa; 11 June 06:00 at -150,0, 1024 hPa. Why: the glass has been rising since dawn (29.90 to 29.93), and a ridge building in from the Atlantic behind the departing lows is the ordinary June pattern. On its eastern flank the wind veers W, then NW, then N and moderates: fine fishing weather, and a fair wind down the coast to Ushant for a lugger that waits on it, which is what the captain said he was doing. No gale, no drama. Effect so far: wind in a watch W 11 (was WSW). Check around noon; if it veers too far or too fast, move a waypoin …[+56])
[t5794 +1h36m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t5794 +1h36m] JOURNAL director [note] 06:36 WEATHER: appended a high, "the ridge" (radius 700 km, 1019 hPa) at 08:00 750 km W and 150 km N of the start. Waypoints: 15:00 at -450,80, 1023 hPa; 11 June 06:00 at -150,0, 1024 hPa. Why: the glass has been rising since dawn (29.90 to 29.93), and a ridge building in from the Atlantic behind the departing lows is the ordinary June pattern. On its eastern flank the wind veers W, then NW, then N and moderates: fine fishing weather, and a fair wind down the coast to Ushant for a lugger that waits on it, which is what the captain said he was doing. No gale, no drama. Effect so far: wind in a watch W 11 (was WSW). Check around noon; if it veers too far or too fast, move a waypoint. The truth book costs ~7k tokens; read it sparingly.
[t5794 +1h36m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t5860 +1h37m] ORDER captain> Say to the officer Aye, a small thing, and thank you. You may also freely "say" and anyone in earshot shall hear. Let's go to the tavern for a time.
[t5862 +1h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the tavern"})
[t5865 +1h37m] ORDER captain> GO to the tavern
[t5866 +1h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The glass is up three hundredths this past hour, sir. If it holds rising, this westerly may veer northerly and let us out."})
[t5868 +1h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t5868 +1h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t5903 +1h38m] ORDER captain> Say Aye, we spend only enough time in the tavern for a handful of drinks. Mind, my hands can hold many a drink. Hah!
[t5907 +1h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Then I'll take a cider and keep my head for the both of us, sir. Morbihan men drink to the tide, not past it."})
[t5907 +1h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "drink"})
[t5909 +1h38m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t5909 +1h38m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t5921 +1h38m] ORDER captain> Drink a cider
[t7603 +2h06m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Old Yann Le Roux\", a Roscoff fisherman of seventy, white-whiskered, who has watched the Isle of Bas weather from the same tavern bench for fifty years, ashore at Roscoff"})
[t7603 +2h06m] WORLD ORDER (the director): person: make "Old Yann Le Roux", a Roscoff fisherman of seventy, white-whiskered, who has watched the Isle of Bas weather from the same tavern bench for fifty years, ashore at Roscoff -> done: Old Yann Le Roux, Roscoff fisherman, seventy years of age, white-whiskered, who has watched the Isle of Bas weather from the same tavern bench for fifty years; made from words, ashore at Roscoff
[t7603 +2h06m] JOURNAL director [director.order] Given: person: make "Old Yann Le Roux", a Roscoff fisherman of seventy, white-whiskered, who has watched the Isle of Bas weather from the same tavern bench for fifty years, ashore at Roscoff; Old Yann Le Roux, Roscoff fisherman, seventy years of age, white-whiskered, who has watched the Isle of Bas weather from the same tavern bench for fifty years; made from words, ashore at Roscoff
[t7606 +2h06m] DIRECTOR> 
    calls: world_order({"text": "person: \"Old Yann Le Roux\" goes to the tavern at Roscoff"})
[t7606 +2h06m] WORLD ORDER (the director): person: "Old Yann Le Roux" goes to the tavern at Roscoff -> refused: not carried out: A person order is 'person: make "<name>", <who he is, his age, where he is, his history>', 'person: "<name>" comes aboard [as <station>]', 'person: "<name>" goes ashore', 'person: "<name>" leaves the ship at <port>', 'person: <role> "<name>" aboard in the <place>' or 'person: <role> …[+27]
[t7606 +2h06m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): person: "Old Yann Le Roux" goes to the tavern at Roscoff (A person order is 'person: make "<name>", <who he is, his age, where he is, his history>', 'person: "<name>" comes aboard [as <station>]', 'person: "<name>" goes ashore', 'person: "<name>" leaves the ship at <port>', 'person: <role> "<name>" aboard in the <place>' or 'person: <role> "<name>" ashore at <port>')
[t7610 +2h06m] DIRECTOR> 
    calls: world_order({"text": "say as Old Yann Le Roux: \"Glass going up like a cork, and the cloud thinning over the island. That westerly's tired. You'll have it round nor'west by the afternoon, northerly by night, and a pretty sea for nets. I've seen it a hundred Junes.\""})
[t7610 +2h06m] WORLD ORDER (the director): say as Old Yann Le Roux: "Glass going up like a cork, and the cloud thinning over the island. That westerly's tired. You'll have it round nor'west by the afternoon, northerly by night, and a pretty sea for nets. I've seen it a hundred Junes." -> done: Old Yann Le Roux spoke ashore at Roscoff, heard by Mère Kerbrat, ashore at Roscoff, on the quay
[t7610 +2h06m] JOURNAL director [director.order] Given: say as Old Yann Le Roux: "Glass going up like a cork, and the cloud thinning over the island. That westerly's tired. You'll have it round nor'west by the afternoon, northerly by night, and a pretty sea for nets. I've seen it a hundred Junes."; Old Yann Le Roux spoke ashore at Roscoff, heard by Mère Kerbrat, ashore at Roscoff, on the quay
[t7613 +2h06m] DIRECTOR> 
    calls: world_order({"text": "person: \"Old Yann Le Roux\" goes to the tavern at Roscoff [reason: a person made ashore lands on the quay; there is no form to move him to another place ashore (the tavern, the market), so he cannot be heard by the captain and the mate in the tavern. The game should let a person unheld be placed or moved among a port's places.]"})
[t7613 +2h06m] WORLD ORDER (the director): person: "Old Yann Le Roux" goes to the tavern at Roscoff -> refused: not carried out: A person order is 'person: make "<name>", <who he is, his age, where he is, his history>', 'person: "<name>" comes aboard [as <station>]', 'person: "<name>" goes ashore', 'person: "<name>" leaves the ship at <port>', 'person: <role> "<name>" aboard in the <place>' or 'person: <role> …[+27]
[t7613 +2h06m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): person: "Old Yann Le Roux" goes to the tavern at Roscoff; the game's words: A person order is 'person: make "<name>", <who he is, his age, where he is, his history>', 'person: "<name>" comes aboard [as <station>]', 'person: "<name>" goes ashore', 'person: "<name>" leaves the ship at <port>', 'person: <role> "<name>" aboard in the <place>' or 'person: <role> "<name>" ashore at <port>'; the reason: a person made ashore lands on the quay; there is no form to move him to another place ashore (the tavern, the market), so he cannot be heard by the captain and the mate in the tavern. The game should let a person unheld be placed or moved among a port's places.
[t7618 +2h06m] DIRECTOR> 
    calls: journal({"note": "07:06 Made Old Yann Le Roux, a Roscoff fisherman of 70 who reads the weather. He landed on the quay, not in the tavern: no form moves an unheld person among a port's places (logged as attempted, for the owner). He said his piece (NW by afternoon, N by night, a pretty sea for nets), but only Mère Kerbrat heard it. If the captain or the mate comes back by the quay, or asks him, he can say it again. The glass is rising fast (29.96), the wind W 10: the ridge is working as meant."})
[t7618 +2h06m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t7618 +2h06m] JOURNAL director [note] 07:06 Made Old Yann Le Roux, a Roscoff fisherman of 70 who reads the weather. He landed on the quay, not in the tavern: no form moves an unheld person among a port's places (logged as attempted, for the owner). He said his piece (NW by afternoon, N by night, a pretty sea for nets), but only Mère Kerbrat heard it. If the captain or the mate comes back by the quay, or asks him, he can say it again. The glass is rising fast (29.96), the wind W 10: the ridge is working as meant.
[t7618 +2h06m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t7626 +2h07m] OFFICER OF THE WATCH DOOR: {"after_orders": 15, "after_inputs": 30, "door": "journal", "reason": "07:06. She has swung to the ebb, wind against tide; mind the shore a cable NW of her swing. At the tavern, Old Yann Le Roux: the glass rising fast, the westerly tiring, NW by afternoon, northerly by night, a good sea for nets. That fits Mère Kerbrat's plan: go out on the ebb with a fair wind and shoot at dusk off Ushant and the Iroise.", "by": "out of turn"}
[t7626 +2h07m] OFFICER OF THE WATCH DOOR: {"after_orders": 15, "after_inputs": 30, "door": "speak", "reason": "", "by": "its own order"}
[t7626 +2h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Hear Old Yann, sir: NW by afternoon, northerly by night. That's our fair wind for the Iroise, if it comes. And word from the road: she's swung to the ebb, wind against tide. Mr Marie should mind her swing toward the island shore."})
[t7626 +2h07m] JOURNAL officer of the watch [note] 07:06. She has swung to the ebb, wind against tide; mind the shore a cable NW of her swing. At the tavern, Old Yann Le Roux: the glass rising fast, the westerly tiring, NW by afternoon, northerly by night, a good sea for nets. That fits Mère Kerbrat's plan: go out on the ebb with a fair wind and shoot at dusk off Ushant and the Iroise.
[t7626 +2h07m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until a word on deck at my own word.
[t7628 +2h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t7628 +2h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t7679 +2h07m] DIRECTOR DOOR: {"after_orders": 15, "after_inputs": 30, "door": "journal", "reason": "07:07 Possible leak for the owner: Old Yann's words were 'heard by Mère Kerbrat on the quay' only, yet Mr Lecoq in the tavern quoted them a minute later. Either his sample carries notable lines from beyond his hearing, or 'ashore at Roscoff' counts as one room for the samples. It also lets the mate know of the wind on the swing at anchor while he is ashore.", "by": "out of turn"}
[t7679 +2h07m] JOURNAL director [note] 07:07 Possible leak for the owner: Old Yann's words were 'heard by Mère Kerbrat on the quay' only, yet Mr Lecoq in the tavern quoted them a minute later. Either his sample carries notable lines from beyond his hearing, or 'ashore at Roscoff' counts as one room for the samples. It also lets the mate know of the wind on the swing at anchor while he is ashore.
[t7692 +2h08m] ORDER captain> Say Aye, thank you kindly for the word, I reckon it may come to be so. We'll head back after a few more ciders.
[t7695 +2h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t7695 +2h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t7698 +2h08m] ORDER captain> How am I
[t9421 +2h37m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t9421 +2h37m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t11073 +3h04m] ORDER captain> Say to Old Yann Say, Old Yann, do you know any man in Roscoff seeking a vessel for any work on the sea?
[t11092 +3h04m] ORDER captain> Say to Old Yann Le Roux Say, Old Yann, do you know any man in Roscoff seeking a vessel for any work on the sea?
[t11092 +3h04m] JOURNAL director [director.asked] Told Old Yann Le Roux, the fisherman (ashore at Roscoff) by the captain: Say, Old Yann, do you know any man in Roscoff seeking a vessel for any work on the sea?
[t11096 +3h04m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11096 +3h04m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11108 +3h05m] DIRECTOR> 
    calls: world_order({"text": "say as Old Yann Le Roux: \"Work? Fish, that's the work, captain, and you'll have the wind for it by afternoon. But Guéguen the factor was grumbling this morning that his onions for Brest sit rotting on the quay. The coasters won't round the Four with the English frigates off Ushant, and the navy at Brest pays for onions. Ten or twelve ton. He'll be on the quay cursing at them, you can't miss him. If you're bound for the Iroise anyhow, Brest is only round the corner.\""})
[t11108 +3h05m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Maître Guéguen\", a Roscoff onion factor of forty-five, red-faced and harried, who ships onions to Brest for the navy's victuallers and has twelve tons going soft on the quay for want of a coaster, ashore at Roscoff"})
[t11108 +3h05m] WORLD ORDER (the director): say as Old Yann Le Roux: "Work? Fish, that's the work, captain, and you'll have the wind for it by afternoon. But Guéguen the factor was grumbling this morning that his onions for Brest sit rotting on the quay. The coasters won't round the Four with the English frigates off Ushant, and the navy at Brest pays for onions. Ten or twelve ton. He'll be on the quay cursing at them, you can't miss him. If you're bound for the Iroise anyhow, Brest is only round the corner." -> done: Old Yann Le Roux spoke ashore at Roscoff, heard by Mère Kerbrat, ashore at Roscoff, on the quay
[t11108 +3h05m] WORLD ORDER (the director): person: make "Maître Guéguen", a Roscoff onion factor of forty-five, red-faced and harried, who ships onions to Brest for the navy's victuallers and has twelve tons going soft on the quay for want of a coaster, ashore at Roscoff -> done: Maître Guéguen, Roscoff onion factor, forty-five years of age, red-faced and harried, who ships onions to Brest for the navy's victuallers and has twelve tons going soft on the quay for want of a coaster; made from words, ashore at Roscoff
[t11108 +3h05m] JOURNAL director [director.order] Given: say as Old Yann Le Roux: "Work? Fish, that's the work, captain, and you'll have the wind for it by afternoon. But Guéguen the factor was grumbling this morning that his onions for Brest sit rotting on the quay. The coasters won't round the Four with the English frigates off Ushant, and the navy at Brest pays for onions. Ten or twelve ton. He'll be on the quay cursing at them, you can't miss him. If you're bound for the Iroise anyhow, Brest is only round the corner."; Old Yann Le Roux spoke ashore at Roscoff, heard by Mère Kerbrat, ashore at Roscoff, on the quay
[t11108 +3h05m] JOURNAL director [director.order] Given: person: make "Maître Guéguen", a Roscoff onion factor of forty-five, red-faced and harried, who ships onions to Brest for the navy's victuallers and has twelve tons going soft on the quay for want of a coaster, ashore at Roscoff; Maître Guéguen, Roscoff onion factor, forty-five years of age, red-faced and harried, who ships onions to Brest for the navy's victuallers and has twelve tons going soft on the quay for want of a coaster; made from words, ashore at Roscoff
[t11119 +3h05m] DIRECTOR> 
    calls: journal({"note": "08:04 The captain (in the tavern) asked Old Yann (on the quay) whether any man wants a vessel for work. Yann answered, though the game says only Mère Kerbrat heard it: another hearing seam, since the captain could address him across places but not hear the reply. Yann pointed him to Maître Guéguen, an onion factor (made, on the quay), with 12 tons of onions for the Brest navy victuallers that the coasters won't carry round the Four for fear of the English off Ushant. Plausible for 1805, and it gives a low purse a small earner on the way to the Iroise. If the captain deals: offer a freight of about 30 shillings a ton (£18 for 12 tons), half paid at Roscoff and half by the consignee  …[+292])
[t11119 +3h05m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t11119 +3h05m] JOURNAL director [note] 08:04 The captain (in the tavern) asked Old Yann (on the quay) whether any man wants a vessel for work. Yann answered, though the game says only Mère Kerbrat heard it: another hearing seam, since the captain could address him across places but not hear the reply. Yann pointed him to Maître Guéguen, an onion factor (made, on the quay), with 12 tons of onions for the Brest navy victuallers that the coasters won't carry round the Four for fear of the English off Ushant. Plausible for 1805, and it gives a low purse a small earner on the way to the Iroise. If the captain deals: offer a freight of about 30 shillings a ton (£18 for 12 tons), half paid at Roscoff and half by the consignee at Brest, then perform 'aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest' and the payment as a transaction. Guéguen haggles but needs the boat. Take only what the captain agrees to; nothing forced. Keep the day's tone: fishing first, the onions a side matter.
[t11119 +3h05m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t11144 +3h05m] ORDER captain> the grounds
[t11154 +3h05m] OFFICER OF THE WATCH DOOR: {"after_orders": 17, "after_inputs": 36, "door": "journal", "reason": "08:05, Old Yann: Guéguen the factor has 10–12 tons of onions for Brest rotting on the quay, and the navy at Brest pays for them. The coasters won't round the Four with English frigates off Ushant. He's on the quay. A freight that fits a passage to the Iroise grounds, but it means going where those frigates are.", "by": "out of turn"}
[t11154 +3h05m] JOURNAL officer of the watch [note] 08:05, Old Yann: Guéguen the factor has 10–12 tons of onions for Brest rotting on the quay, and the navy at Brest pays for them. The coasters won't round the Four with English frigates off Ushant. He's on the quay. A freight that fits a passage to the Iroise grounds, but it means going where those frigates are.
[t11173 +3h06m] ORDER captain> The places ashore
[t11214 +3h06m] ORDER captain> Say to Mr Lecoq Hear that, Lecoq? Let's go see Guegen before we shove off, perhaps we could work something in along with the catch.
[t11222 +3h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the market"})
[t11222 +3h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "08:05, the grounds by the book: Passage de l'Iroise, 46 mi (drift nets for sardines June–Oct by day; lines for ling and conger at any hour). The soundings 7 leagues SW of Ushant, 64 mi (lines). SW of Ushant, 74 mi (lines; cod Nov–Mar). S of Glenan, 83 mi (sardine nets by day; lines). No mackerel ground is listed, and the Iroise nets are by day, not at dusk as Mère Kerbrat said."})
[t11222 +3h07m] JOURNAL officer of the watch [note] 08:05, the grounds by the book: Passage de l'Iroise, 46 mi (drift nets for sardines June–Oct by day; lines for ling and conger at any hour). The soundings 7 leagues SW of Ushant, 64 mi (lines). SW of Ushant, 74 mi (lines; cod Nov–Mar). S of Glenan, 83 mi (sardine nets by day; lines). No mackerel ground is listed, and the Iroise nets are by day, not at dusk as Mère Kerbrat said.
[t11223 +3h07m] ORDER captain> Go to the market
[t11224 +3h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11224 +3h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11301 +3h08m] ORDER captain> Say to Maitre Gueguen Good man, are you Maitre Gueguen? Old Yann in the tavern says you have onion rotting on the quay. We've the Eclair moored out there, hold empty and our course towards Ushant and the Iroise regardless. What say you on it, might we do some business here?
[t11332 +3h08m] ORDER captain> say to Maître Guéguen Good man, are you Maitre Gueguen? Old Yann in the tavern says you have onion rotting on the quay. We've the Eclair moored out there, hold empty and our course towards Ushant and the Iroise regardless. What say you on it, might we do some business here?
[t11332 +3h08m] JOURNAL director [director.asked] Told Maître Guéguen, the factor (ashore at Roscoff) by the captain: Good man, are you Maitre Gueguen? Old Yann in the tavern says you have onion rotting on the quay. We've the Eclair moored out there, hold empty and our course towards Ushant and the Iroise regardless. What say you on it, might we do some business here?
[t11335 +3h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11335 +3h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11343 +3h09m] DIRECTOR> 
    calls: world_order({"text": "say as Maître Guéguen: \"Guéguen, yes, God help me. Twelve tons of the best Roscoff onions, captain, and every day on that quay they go softer and cheaper. The navy's victualling office at Brest takes them, Citizen Le Bris at the Recouvrance stores, and he's waiting on them. I'll give you thirty sous the hundredweight. Call it thirty shillings the ton your way, eighteen pounds for the lot: nine in your hand when the lighter's alongside and they're in your hold, nine from Le Bris at Brest on his receipt. The lighter can be out to you within the hour. Only keep your fish off my onions, eh? The navy is particular about the smell.\""})
[t11343 +3h09m] WORLD ORDER (the director): say as Maître Guéguen: "Guéguen, yes, God help me. Twelve tons of the best Roscoff onions, captain, and every day on that quay they go softer and cheaper. The navy's victualling office at Brest takes them, Citizen Le Bris at the Recouvrance stores, and he's waiting on them. I'll give you thirty sous the hundredweight. Call it thirty shillings the ton your way, eighteen pounds for the lot: nine in your hand when the lighter's alongside and they're in your hold, nine from Le Bris at Brest on his receipt. The lighter can be out to you within the hour. Only keep your fish off my onions, eh? The navy is particular about the smell." -> done: Maître Guéguen spoke ashore at Roscoff, heard by Mr Lecoq and the captain, ashore at Roscoff, at the market
[t11343 +3h09m] JOURNAL director [director.order] Given: say as Maître Guéguen: "Guéguen, yes, God help me. Twelve tons of the best Roscoff onions, captain, and every day on that quay they go softer and cheaper. The navy's victualling office at Brest takes them, Citizen Le Bris at the Recouvrance stores, and he's waiting on them. I'll give you thirty sous the hundredweight. Call it thirty shillings the ton your way, eighteen pounds for the lot: nine in your hand when the lighter's alongside and they're in your hold, nine from Le Bris at Brest on his receipt. The lighter can be out to you within the hour. Only keep your fish off my onions, eh? The navy is particular about the smell."; Maître Guéguen spoke ashore at Roscoff, heard by Mr Lecoq and the captain, ashore at Roscoff, at the market
[t11352 +3h09m] DIRECTOR> 
    calls: journal({"note": "08:08 Guéguen's offer to the captain: 12 tons of onions to Brest for the navy victualling office (consignee Citizen Le Bris, Recouvrance stores), 30 shillings a ton, £18 in all: £9 at Roscoff when the onions are in the hold, £9 from Le Bris at Brest on receipt. Lighter out within the hour. If the captain accepts: (1) 'aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest'; (2) 'aboard: £9 paid into the purse by Maître Guéguen' once they are aboard; (3) at Brest, make Le Bris and pay the other £9 on delivery. ALSO: the game's grounds list for June says the Passage de l'Iroise (46 mi) gives SARDINES by drift net BY DAY, not mackerel; the soundings off Ushant …[+147])
[t11352 +3h09m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t11352 +3h09m] JOURNAL director [note] 08:08 Guéguen's offer to the captain: 12 tons of onions to Brest for the navy victualling office (consignee Citizen Le Bris, Recouvrance stores), 30 shillings a ton, £18 in all: £9 at Roscoff when the onions are in the hold, £9 from Le Bris at Brest on receipt. Lighter out within the hour. If the captain accepts: (1) 'aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest'; (2) 'aboard: £9 paid into the purse by Maître Guéguen' once they are aboard; (3) at Brest, make Le Bris and pay the other £9 on delivery. ALSO: the game's grounds list for June says the Passage de l'Iroise (46 mi) gives SARDINES by drift net BY DAY, not mackerel; the soundings off Ushant give only lines (ling and conger). Mère Kerbrat said mackerel. Small error; if asked again, the voices should say sardines by day in the Iroise.
[t11352 +3h09m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t11353 +3h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Twelve tons sit easy in a fifty-ton hold, sir, and Brest lies on our road to the Iroise. My one worry is the English frigates off Ushant. With navy victuals in her, we'd be a lawful prize, so we'd want to round the Four close in and by daylight, and keep a good lookout."})
[t11355 +3h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11355 +3h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11477 +3h11m] ORDER captain> Say to Maître Guéguen We can certainly be of service, Maître Guéguen, you name a fair price. We'll be shoving off for the Eclair shortly, have your lighter out to her besides and the hands will strike it down at once. Have your man out on the lighter with the 9 in hand, and we'll be off as soon as the wind serves.
[t11477 +3h11m] JOURNAL director [director.asked] Told Maître Guéguen, the factor (ashore at Roscoff) by the captain: We can certainly be of service, Maître Guéguen, you name a fair price. We'll be shoving off for the Eclair shortly, have your lighter out to her besides and the hands will strike it down at once. Have your man out on the lighter with the 9 in hand, and we'll be off as soon as the wind serves.
[t11481 +3h11m] OFFICER OF THE WATCH> 
    calls: journal({"note": "08:11. The captain took Guéguen's freight: 12 tons of onions for Brest, consigned to Citizen Le Bris at the Recouvrance stores; £18 in all, £9 when they're in the hold and £9 from Le Bris on his receipt. The lighter is due within the hour. Keep the fish clear of the onions. We sail when the wind serves; Yann's NW is looked for by the afternoon."})
[t11481 +3h11m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11481 +3h11m] JOURNAL officer of the watch [note] 08:11. The captain took Guéguen's freight: 12 tons of onions for Brest, consigned to Citizen Le Bris at the Recouvrance stores; £18 in all, £9 when they're in the hold and £9 from Le Bris on his receipt. The lighter is due within the hour. Keep the fish clear of the onions. We sail when the wind serves; Yann's NW is looked for by the afternoon.
[t11481 +3h11m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11488 +3h11m] DIRECTOR> 
    calls: world_order({"text": "say as Maître Guéguen: \"Done, and God bless you, captain! My boys will have the lighter loaded and out to your Éclair before you've finished your pipe. My clerk Yves goes with it, with your nine pounds and the bill of lading for Le Bris. Don't let the English have my onions!\""})
[t11488 +3h11m] DIRECTOR> 
    calls: world_order({"text": "aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest"})
[t11488 +3h11m] DIRECTOR> 
    calls: world_order({"text": "aboard: £9 paid into the purse by Maître Guéguen"})
[t11488 +3h11m] DIRECTOR> 
    calls: world_order({"text": "aboard: a bill of lading for twelve tons of onions, consigned by Maître Guéguen of Roscoff to Citizen Le Bris at the Recouvrance victualling stores, Brest, nine pounds freight to pay on delivery, on the cabin table"})
[t11488 +3h11m] WORLD ORDER (the director): say as Maître Guéguen: "Done, and God bless you, captain! My boys will have the lighter loaded and out to your Éclair before you've finished your pipe. My clerk Yves goes with it, with your nine pounds and the bill of lading for Le Bris. Don't let the English have my onions!" -> done: Maître Guéguen spoke ashore at Roscoff, heard by Mr Lecoq and the captain, ashore at Roscoff, at the market
[t11488 +3h11m] WORLD ORDER (the director): aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest -> done: 12 tons of onions freighted by Maître Guéguen at Roscoff for Brest; off by the lighter
[t11488 +3h11m] WORLD ORDER (the director): aboard: £9 paid into the purse by Maître Guéguen -> done: £9 paid into the purse by Maître Guéguen; the purse £69
[t11488 +3h11m] WORLD ORDER (the director): aboard: a bill of lading for twelve tons of onions, consigned by Maître Guéguen of Roscoff to Citizen Le Bris at the Recouvrance victualling stores, Brest, nine pounds freight to pay on delivery, on the cabin table -> done: a bill of lading for twelve tons of onions (consigned by Maître Guéguen of Roscoff to Citizen Le Bris at the Recouvrance victualling stores; Brest; nine pounds freight to pay on delivery) made, on the table in the cabin
[t11488 +3h11m] JOURNAL director [director.order] Given: say as Maître Guéguen: "Done, and God bless you, captain! My boys will have the lighter loaded and out to your Éclair before you've finished your pipe. My clerk Yves goes with it, with your nine pounds and the bill of lading for Le Bris. Don't let the English have my onions!"; Maître Guéguen spoke ashore at Roscoff, heard by Mr Lecoq and the captain, ashore at Roscoff, at the market
[t11488 +3h11m] JOURNAL director [director.order] Given: aboard: twelve tons of onions freighted by Maître Guéguen at the quay for Brest; 12 tons of onions freighted by Maître Guéguen at Roscoff for Brest; off by the lighter
[t11488 +3h11m] JOURNAL director [director.order] Given: aboard: £9 paid into the purse by Maître Guéguen; £9 paid into the purse by Maître Guéguen; the purse £69
[t11488 +3h11m] JOURNAL director [director.order] Given: aboard: a bill of lading for twelve tons of onions, consigned by Maître Guéguen of Roscoff to Citizen Le Bris at the Recouvrance victualling stores, Brest, nine pounds freight to pay on delivery, on the cabin table; a bill of lading for twelve tons of onions (consigned by Maître Guéguen of Roscoff to Citizen Le Bris at the Recouvrance victualling stores; Brest; nine pounds freight to pay on delivery) made, on the table in the cabin
[t11491 +3h11m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11491 +3h11m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11495 +3h11m] DIRECTOR> 
    calls: journal({"note": "08:11 DEAL STRUCK: 12 tons of onions freighted by Guéguen for Brest (off by the lighter); £9 paid into the purse (now £69); a bill of lading on the cabin table (consignee Citizen Le Bris, Recouvrance victualling stores, Brest; £9 freight to pay on delivery). OWED AT BREST: make 'Citizen Le Bris', victualling clerk, ashore at Brest; on delivery, 'aboard: £9 paid into the purse by Citizen Le Bris'. Lecoq worries about English frigates off Ushant and lawful prize. True: none is off Ushant now (the Sparrowhawk cutter is off the Lizard). Keep it that way unless the day wants a sight of one at a distance; the brief says nothing much, so at most a far sail."})
[t11495 +3h11m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t11495 +3h11m] JOURNAL director [note] 08:11 DEAL STRUCK: 12 tons of onions freighted by Guéguen for Brest (off by the lighter); £9 paid into the purse (now £69); a bill of lading on the cabin table (consignee Citizen Le Bris, Recouvrance victualling stores, Brest; £9 freight to pay on delivery). OWED AT BREST: make 'Citizen Le Bris', victualling clerk, ashore at Brest; on delivery, 'aboard: £9 paid into the purse by Citizen Le Bris'. Lecoq worries about English frigates off Ushant and lawful prize. True: none is off Ushant now (the Sparrowhawk cutter is off the Lizard). Keep it that way unless the day wants a sight of one at a distance; the brief says nothing much, so at most a far sail.
[t11495 +3h11m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t11505 +3h11m] ORDER captain> Say to Mr Lecoq to the Quay, Mr Lecoq.
[t11507 +3h11m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the quay"})
[t11508 +3h11m] ORDER captain> Go to the quay
[t11510 +3h11m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, on the quay. Shall I hail the ship for the boat?"})
[t11512 +3h11m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t11512 +3h11m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t11556 +3h12m] ORDER captain> Say to Mr Lecoq Aye, you return to the boat first, then I shall follow you. Make sure the hands strike the cargo down properly as the lighter brings it, and I'll be back shortly after. You'll have the deck until I am back.
[t11558 +3h12m] ORDER captain> You have the deck
[t11558 +3h12m] JOURNAL officer of the watch [agent.deck] Took the deck from the captain.
[t11560 +3h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go aboard"})
[t11567 +3h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t11569 +3h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t11569 +3h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t11723 +3h15m] OFFICER OF THE WATCH> 
    calls: journal({"note": "08:12, the deck given while I'm still ashore. The captain's word: get aboard first, see the onions struck down properly from the lighter, and keep the deck until he's back. No standing orders. 08:15, the lead: five fathoms, sand; she draws one fathom, so there's water enough. She's swinging about, wind against tide; the land a cable off on either hand by turns. The boat is coming off for me."})
[t11723 +3h15m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t11723 +3h15m] JOURNAL officer of the watch [note] 08:12, the deck given while I'm still ashore. The captain's word: get aboard first, see the onions struck down properly from the lighter, and keep the deck until he's back. No standing orders. 08:15, the lead: five fathoms, sand; she draws one fathom, so there's water enough. She's swinging about, wind against tide; the land a cable off on either hand by turns. The boat is coming off for me.
[t11723 +3h15m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t11874 +3h17m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t11874 +3h17m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t13298 +3h41m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t13298 +3h41m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t14982 +4h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the cargo aboard"})
[t14982 +4h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until the cargo aboard.
[t14992 +4h09m] ORDER captain> Return aboard
[t15101 +4h11m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or the cargo aboard"})
[t15101 +4h11m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or the cargo aboard.
[t16911 +4h41m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"the ridge\" at 1805-06-10T12:00 -580 260 1022"})
[t16911 +4h41m] WORLD ORDER (the director): weather: waypoint for "the ridge" at 1805-06-10T12:00 -580 260 1022 -> refused: not carried out: the ridge's track ends at 1805-06-11T06:00:00; a waypoint appended comes after it
[t16911 +4h41m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): weather: waypoint for "the ridge" at 1805-06-10T12:00 -580 260 1022 (the ridge's track ends at 1805-06-11T06:00:00; a waypoint appended comes after it)
[t16918 +4h41m] DIRECTOR> 
    calls: truth({})
[t16928 +4h42m] DIRECTOR> 
    calls: shelve({"book": "book 12", "note": "09:41 wind W by S 9, in a watch W by S 10; the ridge 690 km W by N, 1020; low 3 1002 hPa 1076 km W by N holds the westerly; onions not yet aboard; Sans-Souci 20 mi NNE"})
[t16928 +4h42m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"low 3\" at 1805-06-10T18:00 -1000 520 1008"})
[t16928 +4h42m] WORLD ORDER (the director): weather: waypoint for "low 3" at 1805-06-10T18:00 -1000 520 1008 -> refused: not carried out: low 3 is a seeded system and follows no track
[t16928 +4h42m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): weather: waypoint for "low 3" at 1805-06-10T18:00 -1000 520 1008 (low 3 is a seeded system and follows no track)
[t16939 +4h42m] DIRECTOR> 
    calls: world_order({"text": "weather: high \"the Biscay ridge\" radius 500 km at 1805-06-10T11:00 -500 -250 1020"})
[t16939 +4h42m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"the Biscay ridge\" at 1805-06-10T17:00 -350 -150 1023"})
[t16939 +4h42m] DIRECTOR> 
    calls: world_order({"text": "weather: waypoint for \"the Biscay ridge\" at 1805-06-11T06:00 -220 -120 1023"})
[t16939 +4h42m] WORLD ORDER (the director): weather: high "the Biscay ridge" radius 500 km at 1805-06-10T11:00 -500 -250 1020 -> done: high 'the Biscay ridge' appended to the weather
[t16939 +4h42m] WORLD ORDER (the director): weather: waypoint for "the Biscay ridge" at 1805-06-10T17:00 -350 -150 1023 -> done: a waypoint appended to the Biscay ridge
[t16939 +4h42m] WORLD ORDER (the director): weather: waypoint for "the Biscay ridge" at 1805-06-11T06:00 -220 -120 1023 -> done: a waypoint appended to the Biscay ridge
[t16939 +4h42m] JOURNAL director [director.order] Given: weather: high "the Biscay ridge" radius 500 km at 1805-06-10T11:00 -500 -250 1020; high 'the Biscay ridge' appended to the weather
[t16939 +4h42m] JOURNAL director [director.order] Given: weather: waypoint for "the Biscay ridge" at 1805-06-10T17:00 -350 -150 1023; a waypoint appended to the Biscay ridge
[t16939 +4h42m] JOURNAL director [director.order] Given: weather: waypoint for "the Biscay ridge" at 1805-06-11T06:00 -220 -120 1023; a waypoint appended to the Biscay ridge
[t16947 +4h42m] DIRECTOR> 
    calls: journal({"note": "09:42 WEATHER, second step: the first ridge (690 km W by N, 1020) is not veering the wind; low 3 (1002 hPa, 1076 km W by N, a seeded system that cannot be moved, which I tried and logged) holds a W by S flow. So I appended \"the Biscay ridge\" (high, radius 500 km): at 11:00 -500,-250 1020; 17:00 -350,-150 1023; 11 June 06:00 -220,-120 1023. That is the Azores ridge nosing into the Bay of Biscay, as it does in June. With its centre WSW of Roscoff the flow should come NW, light to moderate. Why: Old Yann's forecast should be a fisherman's fair reading of a rising glass, not a lie, and the brief wants a pleasant fishing day. Check the wind about noon. If it goes NE or dies away, adju …[+27])
[t16947 +4h42m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or the cargo aboard"})
[t16947 +4h42m] JOURNAL director [note] 09:42 WEATHER, second step: the first ridge (690 km W by N, 1020) is not veering the wind; low 3 (1002 hPa, 1076 km W by N, a seeded system that cannot be moved, which I tried and logged) holds a W by S flow. So I appended "the Biscay ridge" (high, radius 500 km): at 11:00 -500,-250 1020; 17:00 -350,-150 1023; 11 June 06:00 -220,-120 1023. That is the Azores ridge nosing into the Bay of Biscay, as it does in June. With its centre WSW of Roscoff the flow should come NW, light to moderate. Why: Old Yann's forecast should be a fisherman's fair reading of a rising glass, not a lie, and the brief wants a pleasant fishing day. Check the wind about noon. If it goes NE or dies away, adjust. No gales in any case.
[t16947 +4h42m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or the cargo aboard.
[t18522 +5h08m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message"})
[t18522 +5h08m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message.
[t18527 +5h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the quarterdeck"})
[t18527 +5h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Welcome aboard, sir. Twelve tons of onions are struck down in the hold and the manifest's written up, with room for thirty-eight more. She rides easy to the best bower in five fathoms, sand. The glass is rising fast, nine hundredths this past hour and up to 30.06, and the sky's clear. Old Yann's shift may be coming, but the wind's still W for now."})
[t18530 +5h08m] OFFICER OF THE WATCH> 
    calls: journal({"note": "10:08: the onions struck down, 12 tons; room for 38. The captain is aboard. The glass 30.06, rising fast (+0.09 in the hour), the sky clear, the wind still W at 11 knots. I hold the deck until he takes it. Watching for the wind going NW, which is the fair wind out past the Lavandière."})
[t18530 +5h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t18530 +5h08m] JOURNAL officer of the watch [note] 10:08: the onions struck down, 12 tons; room for 38. The captain is aboard. The glass 30.06, rising fast (+0.09 in the hour), the sky clear, the wind still W at 11 knots. I hold the deck until he takes it. Watching for the wind going NW, which is the fair wind out past the Lavandière.
[t18530 +5h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t18539 +5h08m] ORDER captain> the cable
[t18564 +5h09m] ORDER captain> the stores
[t18568 +5h09m] ORDER captain> the muster
[t18633 +5h10m] ORDER captain> Say to Mr Lecoq All is prepared, we rest ready but easy and await the shift.
[t18637 +5h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. Ready and easy, and I'll call you the moment she backs round."})
[t18637 +5h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "eat"})
[t18639 +5h10m] ORDER captain> The places
[t18641 +5h10m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a wind shift"})
[t18641 +5h10m] JOURNAL officer of the watch [agent.stood_by] Stood by until a wind shift.
[t18649 +5h10m] ORDER captain> Go to the cabin
[t18657 +5h10m] ORDER captain> Read a bill of lading for twelve tons of onions
[t18670 +5h11m] ORDER captain> Take a bill of lading for twelve tons of onions
[t18679 +5h11m] ORDER captain> Read a bill of lading for twelve tons of onions
[t18693 +5h11m] ORDER captain> Put a bill of lading for twelve tons of onions on the table
[t18706 +5h11m] ORDER captain> Go up on deck
[t20325 +5h38m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t20325 +5h38m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t20330 +5h38m] ORDER captain> how am I
[t22127 +6h08m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t22127 +6h08m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t23932 +6h38m] DIRECTOR> 
    calls: truth({})
[t23942 +6h39m] DIRECTOR> 
    calls: shelve({"book": "book 13", "note": "11:38 wind W by N 13, in a watch NW by W 14: the veer is coming; glass 1019; high 4 seeded by the world 619 km W by N; São Pedro (Portuguese brig, salt beef for Roscoff) 75 mi N, heading S at 7.6 kn"})
[t23942 +6h39m] DIRECTOR> 
    calls: journal({"note": "11:38 The veer is coming: W by N 13 now, NW by W 14 in a watch, by the systems (my two ridges, plus a seeded high 4 the world added). No more weather acts needed; let it run. The São Pedro (Portuguese merchant brig, salt beef from Plymouth for Roscoff) is 75 mi N, coming S at 7.6 kn. She will make the coast this evening and is a natural sail for the player to sight if he is still near, by no act of mine. Sans-Souci 26 mi NE."})
[t23942 +6h39m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t23942 +6h39m] JOURNAL director [note] 11:38 The veer is coming: W by N 13 now, NW by W 14 in a watch, by the systems (my two ridges, plus a seeded high 4 the world added). No more weather acts needed; let it run. The São Pedro (Portuguese merchant brig, salt beef from Plymouth for Roscoff) is 75 mi N, coming S at 7.6 kn. She will make the coast this evening and is a natural sail for the player to sight if he is still near, by no act of mine. Sans-Souci 26 mi NE.
[t23942 +6h39m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t24396 +6h46m] ORDER captain> take a fix
[t25208 +7h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t25210 +7h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t25210 +7h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t25321 +7h02m] OFFICER OF THE WATCH> 
    calls: journal({"note": "12:01, the lead: a quarter less six fathoms, sand. The epitome allows 2½ fathoms of tide, which makes it 3½ on the chart, so about 3½ at low water here. Safe at the anchor for her fathom of draught. But within the account's doubt the chart has as little as half a fathom, likely toward the Isle of Bas shore a cable NW. Mind her swing at low water, around 20:00 by the epitome. The noon latitude was 48° 43' N, and the account kept."})
[t25321 +7h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Noon, sir. A quarter less six fathoms, sand; three and a half at low water by the chart, and plenty for her. But the chart shows a shoal patch toward the island shore within her swing, so I'd sound again near low water, about the end of the first dog. The glass is still climbing, 30.11, and the wind holds W at twelve knots. No shift yet."})
[t25321 +7h02m] JOURNAL officer of the watch [note] 12:01, the lead: a quarter less six fathoms, sand. The epitome allows 2½ fathoms of tide, which makes it 3½ on the chart, so about 3½ at low water here. Safe at the anchor for her fathom of draught. But within the account's doubt the chart has as little as half a fathom, likely toward the Isle of Bas shore a cable NW. Mind her swing at low water, around 20:00 by the epitome. The noon latitude was 48° 43' N, and the account kept.
[t25325 +7h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a wind shift"})
[t25325 +7h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a wind shift.
[t25745 +7h09m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t25745 +7h09m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t27547 +7h39m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t27547 +7h39m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t27584 +7h39m] ORDER captain> Tell the officer We could take her in short tacks up the channel here, to windward.
[t27596 +7h39m] OFFICER OF THE WATCH> 
    calls: library({"find": "Isle of Bas"})
[t27606 +7h40m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 3", "note": "Roscoff road is the narrow channel between the Isle of Bas and the main; 3–4 fathoms on sand; the harbour dries. Cruisers keep stations off the Isle of Bas and Ushant."})
[t27606 +7h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She'll do it, sir. She's handy, and the wind's come W by N. My counsel is to wait an hour for the ebb: high water is near two o'clock by the epitome, and once it turns it runs west with us down the channel, while the flood is against us now. We'd also have the deepest water on our tacks. The channel is narrow, with a dipping lug to shift every board, so I'd keep the boards short, the lead going, and the Lavandière well in mind at the western mouth. The book says the English keep a cruiser off this island, so I'd want a sharp lookout once we're clear. I'll want your word to weigh and to tack, sir."})
[t27609 +7h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t27609 +7h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t27639 +7h40m] ORDER captain> Tell the officer I'll handle the initial tacking out, worry not.
[t27643 +7h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye aye, sir. I'll keep the lead going and an eye to windward for the Lavandière."})
[t27643 +7h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t27643 +7h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t27660 +7h41m] ORDER captain> Get under way on the starboard tack
[t27668 +7h41m] DIRECTOR DOOR: {"after_orders": 37, "after_inputs": 77, "door": "journal", "reason": "12:40 The captain means to beat out of the channel in short tacks. Lecoq cites 'the book': the English keep a cruiser off the Isle of Bas. Historically true (the inshore squadron). There is none now (Sparrowhawk is off the Lizard). Option for later, once she is well at sea and only if the day wants a little salt: a British frigate or cutter seen hull-down to the north on her own business, never chasing, a reminder that 12 tons of navy onions make her a lawful prize. Not before she clears the land, and not if the player is b …[+41]
[t27668 +7h41m] JOURNAL director [note] 12:40 The captain means to beat out of the channel in short tacks. Lecoq cites 'the book': the English keep a cruiser off the Isle of Bas. Historically true (the inshore squadron). There is none now (Sparrowhawk is off the Lizard). Option for later, once she is well at sea and only if the day wants a little salt: a British frigate or cutter seen hull-down to the north on her own business, never chasing, a reminder that 12 tons of navy onions make her a lawful prize. Not before she clears the land, and not if the player is busy with his nets.
[t27676 +7h41m] ORDER captain> Belay that
[t29349 +8h09m] DIRECTOR> 
    calls: stand_by({"until": "a glass or under way or a sail sighted or a message or a wind shift"})
[t29349 +8h09m] JOURNAL director [agent.stood_by] Stood by until a glass, or under way, or a sail sighted, or a message, or a wind shift.
[t30530 +8h28m] ORDER captain> Get under way on the starboard tack
[t30536 +8h28m] ORDER captain> Tell the officer Now, we get under way.
[t30544 +8h29m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, all hands up anchor. I'll have the lead going as soon as she gathers way."})
[t30544 +8h29m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "under way"})
[t30544 +8h29m] JOURNAL officer of the watch [agent.stood_by] Stood by until under way.
[t30568 +8h29m] ORDER captain> Take a fix
[t30863 +8h34m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or a wind shift"})
[t30863 +8h34m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or a wind shift.
[t31627 +8h47m] ORDER captain> Take a fix
[t31628 +8h47m] DIRECTOR> 
    calls: journal({"note": "13:47 Under way. Possible bug for the owner: the getting-under-way sequence for this lugger read 'lay aloft, sail-loosers... hoist away the topsail and the mainsail, the main boom steadied over... the topsail yard abox', a cutter's or square-rigger's words, yet the readings show only the jib set, the lugs furled and the topsails sent down. She is making 2 kn S by E with the land of Pointe de Pergueridre a cable ahead, under the jib alone. The Roscoff pilots' boat (the game's own) is standing out to her. Nothing of mine."})
[t31628 +8h47m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or a wind shift"})
[t31628 +8h47m] JOURNAL director [note] 13:47 Under way. Possible bug for the owner: the getting-under-way sequence for this lugger read 'lay aloft, sail-loosers... hoist away the topsail and the mainsail, the main boom steadied over... the topsail yard abox', a cutter's or square-rigger's words, yet the readings show only the jib set, the lugs furled and the topsails sent down. She is making 2 kn S by E with the land of Pointe de Pergueridre a cable ahead, under the jib alone. The Roscoff pilots' boat (the game's own) is standing out to her. Nothing of mine.
[t31628 +8h47m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or a wind shift.
[t31763 +8h49m] ORDER captain> take a fix
[t31773 +8h49m] ORDER captain> the nearest shore
[t31836 +8h50m] OFFICER OF THE WATCH DOOR: {"after_orders": 43, "after_inputs": 87, "door": "speak", "reason": "", "by": "its own order"}
[t31836 +8h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t31836 +8h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Captain, sir: she's standing SSW under the jib alone, with the land about Pergueridre a cable on the larboard bow. The chart gives a fathom and a half at low water here and shoals toward the point, and the flood is setting us NE. The lead is going now. I'd have the lugs on her and go about before she closes the point."})
[t31836 +8h50m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until under way at my own word.
[t31839 +8h50m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t31839 +8h50m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t31852 +8h50m] ORDER captain> Belay getting under way
[t31853 +8h50m] ORDER captain> Set the mizen
[t31855 +8h50m] ORDER captain> Tack ship
[t31861 +8h51m] ORDER captain> All hands
[t31864 +8h51m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t31864 +8h51m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t31885 +8h51m] ORDER captain> Belay tacking ship
[t31886 +8h51m] ORDER captain> Wear ship
[t31893 +8h51m] ORDER captain> Belay setting the mizen
[t31897 +8h51m] ORDER captain> Bely heaving lead
[t31899 +8h51m] ORDER captain> Belay all
[t31900 +8h51m] ORDER captain> Wear ship
[t31904 +8h51m] ORDER captain> Take a fix
[t31989 +8h53m] OFFICER OF THE WATCH DOOR: {"after_orders": 53, "after_inputs": 98, "door": "read", "reason": "the log from tick 0", "by": "read_log(since_tick=0, count=15)"}
[t32026 +8h53m] OFFICER OF THE WATCH DOOR: {"after_orders": 53, "after_inputs": 98, "door": "shelve", "reason": "book 4", "by": "out of turn", "note": "13:51: the captain belayed all, then wore ship clear of Pergueridre."}
[t32027 +8h53m] OFFICER OF THE WATCH DOOR: {"after_orders": 53, "after_inputs": 98, "door": "speak", "reason": "", "by": "its own order"}
[t32027 +8h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t32027 +8h53m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until a sounding at my own word.
[t32035 +8h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's paying off well, sir, but she has only the jib to drive her, and the Isle of Bas shore is a cable on the larboard beam. The chart shows half a fathom at low water hereabouts, so there's about three with the tide in now. I'd set the fore and main lugs to give her way and steerage. The lead's going."})
[t32035 +8h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t32035 +8h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t32053 +8h54m] ORDER captain> Belay all
[t32055 +8h54m] ORDER captain> Set the fore lug
[t32057 +8h54m] ORDER captain> Set the main lug
[t32066 +8h54m] ORDER captain> Steer north
[t32072 +8h54m] ORDER captain> Trim for close hauled
[t32116 +8h55m] ORDER captain> take a fix
[t32189 +8h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's lifting, sir! The wind's come WNW and she won't lie north. Keep her away a point, to N by E, until the lugs are drawing, or she'll be taken aback with Pergueridre a cable astern."})
[t32189 +8h56m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t32189 +8h56m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t32191 +8h56m] ORDER captain> Trim for close hauled
[t32199 +8h56m] DIRECTOR> 
    calls: journal({"note": "13:56 Urgent: taken aback in the channel, Pointe de Pergueridre a cable astern, 1.5 fathoms at low water by the chart, the flood making (about 3 fathoms now, she draws 1). This is the player's seamanship, and the officer is advising him well; I do not touch it. The weather I made is the cause only in that the wind has come WNW as foretold. No act: the sea is honest, and the Roscoff pilots' boat (the game's own) is standing toward her. If she takes the ground on a rising tide on sand, that is a fisherman's ordinary bad afternoon, not a tragedy. I watch."})
[t32199 +8h56m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or aground or the pilot aboard"})
[t32199 +8h56m] JOURNAL director [note] 13:56 Urgent: taken aback in the channel, Pointe de Pergueridre a cable astern, 1.5 fathoms at low water by the chart, the flood making (about 3 fathoms now, she draws 1). This is the player's seamanship, and the officer is advising him well; I do not touch it. The weather I made is the cause only in that the wind has come WNW as foretold. No act: the sea is honest, and the Roscoff pilots' boat (the game's own) is standing toward her. If she takes the ground on a rising tide on sand, that is a fisherman's ordinary bad afternoon, not a tragedy. I watch.
[t32199 +8h56m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or aground, or the pilot aboard.
[t32200 +8h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "bear away two points", "danger": "Taken aback with no way on, and Pointe de Pergueridre a cable astern: she'll go astern onto the point unless she pays off and fills."})
[t32200 +8h56m] JOURNAL officer of the watch [agent.danger] Ordered on my own word, to avoid an immediate danger (Taken aback with no way on, and Pointe de Pergueridre a cable astern: she'll go astern onto the point unless she pays off and fills.): bear away two points.
[t32203 +8h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I've borne her away two points to NNE on my own word, sir, to fill her. The best bower's hanging ready at the bows if she gathers sternway toward the point."})
[t32203 +8h56m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "filled away"})
[t32203 +8h56m] JOURNAL officer of the watch [agent.stood_by] Stood by until filled away.
[t32244 +8h57m] ORDER captain> Steer north
[t32271 +8h57m] ORDER captain> Tell the officer Please do not countermand me while we are in this passage, I have her, the trimming takes time and the aback was transient.
[t32280 +8h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye aye, sir, she's yours. I'll touch nothing of the helm or the sheets while you con her through, and I'll keep to the lead and the lookout, reporting only."})
[t32280 +8h58m] OFFICER OF THE WATCH> 
    calls: journal({"note": "13:56. Taken aback while steering N, close to the wind WNW, with Pergueridre a cable astern. On my own word, for that danger, I bore her away two points. At 13:57 the captain asked me not to countermand him in the passage: he had her, the trimming takes time, and the aback was transient. He was right; she was making 5 knots a minute later. Lesson: while the captain is conning her through a passage, I report and he decides, even though I hold the deck by name. Danger orders only if he isn't acting."})
[t32280 +8h58m] JOURNAL officer of the watch [note] 13:56. Taken aback while steering N, close to the wind WNW, with Pergueridre a cable astern. On my own word, for that danger, I bore her away two points. At 13:57 the captain asked me not to countermand him in the passage: he had her, the trimming takes time, and the aback was transient. He was right; she was making 5 knots a minute later. Lesson: while the captain is conning her through a passage, I report and he decides, even though I hold the deck by name. Danger orders only if he isn't acting.
[t32285 +8h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Land ahead, sir, the Isle of Bas shore three cables on the starboard bow, so a board of two minutes at most. And for your reckoning: with the flood under her she's making good E, not gaining to windward."})
[t32285 +8h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t32285 +8h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t32288 +8h58m] ORDER captain> Tack ship
[t32405 +9h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t32405 +9h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t32413 +9h00m] ORDER captain> take a fix
[t32526 +9h02m] ORDER captain> Take a fix
[t32528 +9h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's fallen off to SE by S, sir, the wind on the quarter. Roscoff is eight cables and closing, and the harbour dries. If she can't hold her wind against this flood, the best bower's still hanging ready to bring her up and wait for the ebb."})
[t32528 +9h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t32528 +9h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t32542 +9h02m] ORDER captain> You may work the ship
[t32542 +9h02m] JOURNAL officer of the watch [agent.deck] Given the captain's general authority to work the ship.
[t32555 +9h02m] ORDER captain> Tell the officer Bring her to anchor, we aren't tacking out of this right now.
[t32562 +9h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "let go the best bower"})
[t32570 +9h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t32570 +9h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t32574 +9h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the main lug"})
[t32574 +9h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the fore lug"})
[t32576 +9h02m] ORDER captain> Belay heaving log
[t32577 +9h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Bringing her to, sir. The lugs are coming in to take the way off her, and the best bower goes as she slows, in about two and a half fathoms at low water by the chart, on sand."})
[t32577 +9h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "brought up"})
[t32577 +9h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until brought up.
[t32712 +9h05m] ORDER captain> we need no pilot
[t32715 +9h05m] ORDER captain> take a fix
[t32726 +9h05m] ORDER captain> take in the jib
[t32822 +9h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "furl the mizen lug"})
[t32822 +9h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Brought up, sir, by the best bower in five and a half fathoms, with thirty-one fathoms of cable, on sand. That leaves about two fathoms at low water by the chart, and she draws one. Pergueridre is a cable to the SSE and her swing comes near the island shore to the N by W. I'm furling the loose mizen. We'll lie here for the ebb, and I'll sound again as the tide falls and call you at the turn."})
[t32822 +9h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "14:02, the captain gave me general authority to work the ship ('you may work the ship') and the word to bring her to anchor: the flood was setting her E at 1½ knots and she could gain nothing beating in the channel. Lugs in to take the way off; the best bower let go, and she was brought up at 14:06 in 5½ fathoms, 31 fathoms of cable, sand. About 2 fathoms at low water by the chart; she draws 1. Pergueridre a cable SSE; the swing comes within a cable of the land N by W. The pilot boat was waved off by the captain; no Roscoff pilot for 6 hours. Plan: lie to the ebb, sound as it falls, then weigh and work out W past the Lavandière with the ebb under her."})
[t32822 +9h07m] JOURNAL officer of the watch [note] 14:02, the captain gave me general authority to work the ship ('you may work the ship') and the word to bring her to anchor: the flood was setting her E at 1½ knots and she could gain nothing beating in the channel. Lugs in to take the way off; the best bower let go, and she was brought up at 14:06 in 5½ fathoms, 31 fathoms of cable, sand. About 2 fathoms at low water by the chart; she draws 1. Pergueridre a cable SSE; the swing comes within a cable of the land N by W. The pilot boat was waved off by the captain; no Roscoff pilot for 6 hours. Plan: lie to the ebb, sound as it falls, then weigh and work out W past the Lavandière with the ebb under her.
[t32825 +9h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the turn to the ebb"})
[t32825 +9h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until the turn to the ebb.
[t32849 +9h07m] ORDER captain> Tell the officer Aye, this should be much easier with a fair wind. We wait.
[t32854 +9h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the turn to the ebb"})
[t32854 +9h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until the turn to the ebb.
[t34011 +9h26m] DIRECTOR> 
    calls: journal({"note": "14:26 Anchored again at 14:06 off Pointe de Pergueridre (5.5 fathoms, 31 fathoms of cable) to wait for the ebb; the captain waved off the pilot. The wind has come NW by N 11, the veer I arranged. But the sky turned 'dark and gloomy, scud, thunder, visibility a mile' while the glass rises fast (30.21). The game seems to treat the veer as a cold front going through. That is realistic: a thundery line at the shift, then clearing in the NW air behind it. Not my order, but my systems caused it. It should pass within the hour. If the thunder or a squall persists, or the wind rises beyond a fresh breeze, read the truth and ease it. The brief wants a nice day, and a short thundery shower a …[+51])
[t34011 +9h26m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way or a squall or a change in the sky"})
[t34011 +9h26m] JOURNAL director [note] 14:26 Anchored again at 14:06 off Pointe de Pergueridre (5.5 fathoms, 31 fathoms of cable) to wait for the ebb; the captain waved off the pilot. The wind has come NW by N 11, the veer I arranged. But the sky turned 'dark and gloomy, scud, thunder, visibility a mile' while the glass rises fast (30.21). The game seems to treat the veer as a cold front going through. That is realistic: a thundery line at the shift, then clearing in the NW air behind it. Not my order, but my systems caused it. It should pass within the hour. If the thunder or a squall persists, or the wind rises beyond a fresh breeze, read the truth and ease it. The brief wants a nice day, and a short thundery shower at the shift is within a fisherman's ordinary day.
[t34011 +9h26m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way, or a squall, or a change in the sky.
[t34863 +9h41m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way or a squall"})
[t34863 +9h41m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way, or a squall.
[t35421 +9h50m] OFFICER OF THE WATCH DOOR: {"after_orders": 72, "after_inputs": 124, "door": "speak", "reason": "", "by": "its own order"}
[t35421 +9h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The wind's veered to NW by W, sir, as Old Yann said. Still not quite free for the channel westward, and the flood still runs. Another point or two and the ebb, and she'll go out on one board."})
[t35421 +9h50m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the turn to the ebb"})
[t35421 +9h50m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until the turn to the ebb at my own word.
[t35421 +9h50m] JOURNAL officer of the watch [agent.stood_by] Stood by until the turn to the ebb.
[t36092 +10h01m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t36092 +10h01m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t37896 +10h31m] DIRECTOR> 
    calls: truth({})
[t37897 +10h31m] ORDER captain> take a fix
[t37908 +10h31m] DIRECTOR> 
    calls: shelve({"book": "book 14", "note": "15:31 wind NW by W 14, in a watch WNW 14; glass 1024.7; the ridges 424-446 km W; the tide still flooding at 7.7 m; São Pedro 46 mi N bound in for Roscoff"})
[t37908 +10h31m] DIRECTOR> 
    calls: journal({"note": "15:31 Squalls to 25 kn passed. The mean is NW by W 14, WNW 14 in a watch: a fresh, settled post-frontal breeze, nothing to ease. Possible bug for the owner: the truth has given the tidal stream as '1.2 knots along 65 degrees' all day, at ebb and flood alike, and it still says flood, rising, 7.7 m at 15:31, though the master's epitome put high water near 14:00. The readings and the truth also disagreed on flood or ebb this morning. That is why the ebb the officer waits for is late. The São Pedro, a Portuguese brig with salt beef for Roscoff, is 46 mi N and coming S at 7 kn: she should come over the horizon to the N around sunset, the game's own sail."})
[t37908 +10h31m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t37908 +10h31m] JOURNAL director [note] 15:31 Squalls to 25 kn passed. The mean is NW by W 14, WNW 14 in a watch: a fresh, settled post-frontal breeze, nothing to ease. Possible bug for the owner: the truth has given the tidal stream as '1.2 knots along 65 degrees' all day, at ebb and flood alike, and it still says flood, rising, 7.7 m at 15:31, though the master's epitome put high water near 14:00. The readings and the truth also disagreed on flood or ebb this morning. That is why the ebb the officer waits for is late. The São Pedro, a Portuguese brig with salt beef for Roscoff, is 46 mi N and coming S at 7 kn: she should come over the horizon to the N around sunset, the game's own sail.
[t37908 +10h31m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t39609 +11h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t39611 +11h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t39611 +11h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t39710 +11h01m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t39710 +11h01m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t39724 +11h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Eight bells in the first dog, sir. A quarter six fathoms, sand: four at low water by the chart, so she lies safe even with Pergueridre under our lee. The wind's NW by W at thirteen knots, with squalls to twenty-five through the afternoon, and the glass is still rising, 30.29. No ebb yet; she still rides to the flood. I'll call you at the turn."})
[t39724 +11h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the turn to the ebb"})
[t39724 +11h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until the turn to the ebb.
[t41513 +11h31m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t41513 +11h31m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t43323 +12h02m] DIRECTOR> 
    calls: world_order({"text": "say as Guillaume Bourdon: (sitting on the onion hatch, swinging his bare feet, singing) \"Le vent tourne au noroît, la mer s'apaise, ma mie... les maquereaux sont à l'ouest, et moi je suis ici...\""})
[t43323 +12h02m] WORLD ORDER (the director): say as Guillaume Bourdon: (sitting on the onion hatch, swinging his bare feet, singing) "Le vent tourne au noroît, la mer s'apaise, ma mie... les maquereaux sont à l'ouest, et moi je suis ici..." -> done: Guillaume Bourdon spoke on the quarterdeck, heard by Mr Lecoq, the captain and Mr Marie, on the quarterdeck
[t43323 +12h02m] JOURNAL director [director.order] Given: say as Guillaume Bourdon: (sitting on the onion hatch, swinging his bare feet, singing) "Le vent tourne au noroît, la mer s'apaise, ma mie... les maquereaux sont à l'ouest, et moi je suis ici..."; Guillaume Bourdon spoke on the quarterdeck, heard by Mr Lecoq, the captain and Mr Marie, on the quarterdeck
[t43331 +12h02m] DIRECTOR> 
    calls: journal({"note": "17:01 Correction to my 15:31 note: the game's tide turned to the flood at 13:16, so its high water comes near 19:30. The master's epitome (Brest, about 13:45) is simply an hour or more out for this road, which is honest play and not a bug; the constant '65 degrees' stream direction may still be one. The sky is clear again, fine, WNW 14-15, glass 30.32. Gave the boy Guillaume a few lines of song while they wait (he 'sings', by his description). Plan for the evening: let them sail on the ebb about 19:30. The São Pedro may show to the N near dusk. No more acts unless asked."})
[t43331 +12h02m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t43331 +12h02m] JOURNAL director [note] 17:01 Correction to my 15:31 note: the game's tide turned to the flood at 13:16, so its high water comes near 19:30. The master's epitome (Brest, about 13:45) is simply an hour or more out for this road, which is honest play and not a bug; the constant '65 degrees' stream direction may still be one. The sky is clear again, fine, WNW 14-15, glass 30.32. Gave the boy Guillaume a few lines of song while they wait (he 'sings', by his description). Plan for the evening: let them sail on the ebb about 19:30. The São Pedro may show to the N near dusk. No more acts unless asked.
[t43331 +12h02m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t45134 +12h32m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t45134 +12h32m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t46937 +13h02m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t46937 +13h02m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t48740 +13h32m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t48740 +13h32m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t50543 +14h02m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t50543 +14h02m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t50545 +14h02m] ORDER captain> take a fix
[t50562 +14h02m] ORDER captain> Tell Mr Lecoq Well, I suppose we can get under way tomorrow. The mackerel will still be there.
[t50573 +14h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, tomorrow it is. Brest's onions will keep a day, and the mackerel too. She rides head to wind on the best bower, with Pergueridre a cable under our lee, so tonight I'll keep an anchor watch: the lead at low water, about eight bells, and the cable watched in the squalls. If the wind holds NW, the morning ebb should carry us out past the Lavandière on one board."})
[t50573 +14h02m] OFFICER OF THE WATCH> 
    calls: journal({"note": "19:02: the captain puts off sailing until tomorrow. She rides head to wind to the best bower, 31 fathoms, in about 6 fathoms on sand (4 at low water by the chart). Pergueridre a cable to the SSE is a lee shore in this NW wind; squalls to 25 knots earlier. Glass 30.34, steady-rising, the sky clear. The game's ebb never turned through the afternoon; the epitome's low water is near 20:00. Anchor watch: the lead near low water; watch the cable in squalls; veer more if it strains."})
[t50573 +14h02m] JOURNAL officer of the watch [note] 19:02: the captain puts off sailing until tomorrow. She rides head to wind to the best bower, 31 fathoms, in about 6 fathoms on sand (4 at low water by the chart). Pergueridre a cable to the SSE is a lee shore in this NW wind; squalls to 25 knots earlier. Glass 30.34, steady-rising, the sky clear. The game's ebb never turned through the afternoon; the epitome's low water is near 20:00. Anchor watch: the lead near low water; watch the cable in squalls; veer more if it strains.
[t50575 +14h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "eight bells"})
[t50575 +14h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until eight bells.
[t50584 +14h03m] ORDER captain> how am I
[t50587 +14h03m] ORDER captain> Eat
[t50588 +14h03m] ORDER captain> Drink
[t52348 +14h32m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a sail sighted or a message or under way"})
[t52348 +14h32m] JOURNAL director [agent.stood_by] Stood by until a watch, or a sail sighted, or a message, or under way.
[t54003 +15h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t54005 +15h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t54005 +15h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t54137 +15h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "how am I"})
[t54137 +15h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sunset, sir. A quarter less four fathoms, sand, and falling: two and a half less than at four bells. She draws one, so there's water to spare, but I'll sound again at two bells to see where the fall stops. The wind's W by N at fourteen knots and the glass is up to 30.40."})
[t54139 +15h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "drink"})
[t54139 +15h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "eat"})
[t54141 +15h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "two bells"})
[t54141 +15h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until two bells.
[t54146 +15h02m] ORDER captain> take an amplitude
[t54757 +15h12m] DIRECTOR DOOR: {"after_orders": 76, "after_inputs": 145, "door": "journal", "reason": "19:32 The captain gives up for today: they lie at anchor tonight and go out on the morning ebb. The onions and the mackerel keep. The ebb did come at 19:25, as the game's tide had it. Night plan: quiet. The ridges move east toward us, so the wind should ease and hold NW to N by morning, fair for the run west past the Lavandière. The São Pedro may come into the road with salt beef for Roscoff (the game's own ship). Stand by a watch at a time.", "by": "out of turn"}
[t54757 +15h12m] JOURNAL director [note] 19:32 The captain gives up for today: they lie at anchor tonight and go out on the morning ebb. The onions and the mackerel keep. The ebb did come at 19:25, as the game's tide had it. Night plan: quiet. The ridges move east toward us, so the wind should ease and hold NW to N by morning, fair for the run west past the Lavandière. The São Pedro may come into the road with salt beef for Roscoff (the game's own ship). Stand by a watch at a time.
[t57602 +16h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t57605 +16h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t57605 +16h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t57746 +16h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Two bells, sir. A quarter three fathoms, sand: down only half a fathom this hour, so the fall is slackening and low water's near. Two fathoms under her keel at the worst. I'll cast again at four bells to see it rise."})
[t57746 +16h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t57746 +16h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t61202 +17h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t61204 +17h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t61204 +17h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t61349 +17h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Four bells, sir. A quarter less four fathoms and rising: low water passed about two bells with three fathoms under her, so she's safe the night through. The wind's WNW at sixteen knots and the glass is 30.42. I've been on my feet since four this morning, so whenever you wish, I'll hand the deck over with my note, or keep it through the middle watch if you'd rather."})
[t61349 +17h02m] OFFICER OF THE WATCH> 
    calls: journal({"note": "22:02, the anchor watch. Soundings: 16:00, 6¼ fathoms; 20:02, 3¾; 21:02, 3¼; 22:02, 3¾ and rising. Low water about 21:00–21:30 with 3 fathoms under her (she draws 1). The game's ebb stream turned at 19:25, hours after the epitome's Brest high water (~13:45). The water fell from about 14:00, but the stream ran flood until 19:25; for tomorrow, the stream lags the rise and fall by hours here. Wind WNW 16 knots, glass 30.42 rising, the sky clear, the moon near full. On my feet 17 hours."})
[t61349 +17h02m] JOURNAL officer of the watch [note] 22:02, the anchor watch. Soundings: 16:00, 6¼ fathoms; 20:02, 3¾; 21:02, 3¼; 22:02, 3¾ and rising. Low water about 21:00–21:30 with 3 fathoms under her (she draws 1). The game's ebb stream turned at 19:25, hours after the epitome's Brest high water (~13:45). The water fell from about 14:00, but the stream ran flood until 19:25; for tomorrow, the stream lags the rise and fall by hours here. Wind WNW 16 knots, glass 30.42 rising, the sky clear, the moon near full. On my feet 17 hours.
[t61351 +17h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t61351 +17h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t61358 +17h02m] ORDER captain> how am I
[t61370 +17h02m] ORDER captain> Tell the officer You may go below and rest, Mr Lecoq, I shall keep the deck.
[t61381 +17h03m] OFFICER OF THE WATCH> 
    calls: hand_over({"note": "Handover, first watch, 22:02. She lies at anchor in the road of the Isle of Bas by the best bower, 31 fathoms of cable, on sand, riding to the ebb with the wind across it; the strain is slight. Pergueridre is a cable SSE, a lee shore in this wind; the Isle of Bas shore a cable to the N by W at the far end of her swing. Soundings: 6¼ fathoms at 16:00, 3¾ at 20:00, 3¼ at 21:00 (about low water), 3¾ at 22:00 and rising, so she has at least 2 fathoms under her keel. The wind WNW at 16 knots, squalls to 25 earlier in the day, the glass 30.42 and rising, the sky clear, the moon near full. The day: we took 12 tons of onions for Citizen Le Bris at the Recouvrance stores, Brest, £9 paid and …[+739])
[t61381 +17h03m] JOURNAL officer of the watch [agent.handover] Handover note (handing over the deck): Handover, first watch, 22:02. She lies at anchor in the road of the Isle of Bas by the best bower, 31 fathoms of cable, on sand, riding to the ebb with the wind across it; the strain is slight. Pergueridre is a cable SSE, a lee shore in this wind; the Isle of Bas shore a cable to the N by W at the far end of her swing. Soundings: 6¼ fathoms at 16:00, 3¾ at 20:00, 3¼ at 21:00 (about low water), 3¾ at 22:00 and rising, so she has at least 2 fathoms under her keel. The wind WNW at 16 knots, squalls to 25 earlier in the day, the glass 30.42 and rising, the sky clear, the moon near full. The day: we took 12 tons of onions for Citizen Le Bris at the Recouvrance stores, Brest, £9 paid and £9 on receipt, and tried to beat out at 13:50 against the flood. Taken aback once; I bore her away on my own word, and the captain rightly asked me not to countermand him while he had her. Brought up again at 14:06 on his word. Noted: here the stream turns hours after the rise and fall, the flood running until 19:25 though high water was near 14:00. For the morning: weigh on the ebb with the wind NW or WNW and work her out W past the Lavandière on as few boards as we can. Mackerel are reported off Ushant and in the Iroise; the book's grounds there are sardine nets by day and lines. The English keep a cruiser off this island and off Ushant: a sharp lookout once clear. The best bower's cable wants watching if the squalls return.
[t61381 +17h03m] JOURNAL officer of the watch [agent.deck] Handed over the deck; I stay at the station, off watch.
[t61384 +17h03m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir, good night. The deck's yours, and my note's in the log. Call me if the cable starts to strain."})
[t61384 +17h03m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the gunroom"})
[t61387 +17h03m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "asleep below until called"})
[t61387 +17h03m] JOURNAL officer of the watch [agent.stood_by] Turned in below, in the gunroom, asleep until called.
[t64879 +18h01m] ORDER captain> take a fix
[t64881 +18h01m] ORDER captain> heave the lead
[t65464 +18h11m] OFFICER OF THE WATCH DOOR: {"after_orders": 79, "after_inputs": 153, "door": "journal", "reason": "23:03 (asleep below, read on waking): the captain's cast gave a quarter less three fathoms, one fathom on the chart. She has swung over shoaler ground than my 22:02 cast (3¾). The tide is rising now, so no danger tonight. But at the next low water (morning, around 09:00 by the epitome, likely later by this water) she'd lie in about a fathom here, which is her draught. Weigh before then, or shorten in or shift berth.", "by": "out of turn"}
[t65464 +18h11m] JOURNAL officer of the watch [note] 23:03 (asleep below, read on waking): the captain's cast gave a quarter less three fathoms, one fathom on the chart. She has swung over shoaler ground than my 22:02 cast (3¾). The tide is rising now, so no danger tonight. But at the next low water (morning, around 09:00 by the epitome, likely later by this water) she'd lie in about a fathom here, which is her draught. Weigh before then, or shorten in or shift berth.
[t66751 +18h32m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a sail sighted or a message or under way"})
[t66751 +18h32m] JOURNAL director [agent.stood_by] Stood by until a watch, or a sail sighted, or a message, or under way.
[t68651 +19h04m] ORDER captain> pipe down
[t68657 +19h04m] ORDER captain> how am I
[t69257 +19h14m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the quarterdeck"})
[t69257 +19h14m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Rested and on deck, sir, thank you. One thing for the morning: your cast at eleven found her swung over shoaler ground, one fathom on the chart. High water's near two o'clock, so low water falls about eight, and here she'd have barely her draught. I'd weigh at first light, before the water's off, while the NW wind serves. Yesterday the stream turned about five hours after high water, so it'll be slack or just turning west as we go."})
[t69259 +19h14m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t69259 +19h14m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t69271 +19h14m] ORDER captain> take a fix
[t70482 +19h34m] ORDER captain> Say to Mr Lecoq Aye, first light sounds right to me.
[t70602 +19h36m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t70602 +19h36m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t77623 +21h33m] ORDER captain> the anchors
[t77635 +21h33m] ORDER captain> heave short
[t77664 +21h34m] ORDER captain> Tell the officer We're heaving short, then I'll try and get her under way once the sun rises and the wind is as fair as it will get.
[t77677 +21h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, heaving short. A correction to my counsel: the stream turned to the flood at 01:35, so at sunrise it runs east against us again, as it did yesterday. By yesterday's reckoning the ebb comes about half past seven. Hove short, she keeps off the shoal patch, so we could hold her there and go with the ebb, unless the wind frees us enough to outsail the flood."})
[t77677 +21h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t77677 +21h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t78171 +21h42m] DIRECTOR DOOR: {"after_orders": 84, "after_inputs": 165, "door": "read", "reason": "the truth at Middle watch (02:42)", "by": "truth()"}
[t80171 +22h16m] DIRECTOR DOOR: {"after_orders": 84, "after_inputs": 165, "door": "shelve", "reason": "book 15", "by": "out of turn", "note": "02:42 wind NW by W 10, NW by N 11 in a watch, hazy fine, glass 1033.9; the ridges 216-283 km W; São Pedro crewed 2.4 mi WSW; Saint-Guénolé and Enterprise near Brest approaches 35 mi SW"}
[t80171 +22h16m] DIRECTOR DOOR: {"after_orders": 84, "after_inputs": 165, "door": "journal", "reason": "02:42 (11 June) Morning forecast: NW by N 11 kn, hazy and fine, glass very high (1033.9 hPa: perhaps too high for two moderate ridges, though not harmful; worth the owner's eye). A fair wind for the run west at dawn, as the fishermen said. BUG for the owner: the São Pedro, a Portuguese merchant brig 'deep laden' with salt beef from Plymouth for Roscoff, has been crewed within range (2.4 mi WSW of Éclair, heading WSW at 4.4 kn at night) with a Royal Navy wardroom: Captain Wright, Mr Loveday lieutenant, a gunner, a purser, a …[+334]
[t80171 +22h16m] JOURNAL director [note] 02:42 (11 June) Morning forecast: NW by N 11 kn, hazy and fine, glass very high (1033.9 hPa: perhaps too high for two moderate ridges, though not harmful; worth the owner's eye). A fair wind for the run west at dawn, as the fishermen said. BUG for the owner: the São Pedro, a Portuguese merchant brig 'deep laden' with salt beef from Plymouth for Roscoff, has been crewed within range (2.4 mi WSW of Éclair, heading WSW at 4.4 kn at night) with a Royal Navy wardroom: Captain Wright, Mr Loveday lieutenant, a gunner, a purser, a surgeon, a midshipman, all English names. The crew generator seems to use a naval British template for every ship it crews. Since she is near, the player may meet her; her people would be wrong for her flag. I will not speak as them unless asked, and if asked I will answer as plain Portuguese merchant seamen.
[t81151 +22h32m] JOURNAL director [director.budget] The day's budget is renewed (1805-06-11): 9999 samples and 9999 acts.
[t81154 +22h32m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a sail sighted or a message or under way"})
[t81154 +22h32m] JOURNAL director [agent.stood_by] Stood by until a glass, or a sail sighted, or a message, or under way.
[t82624 +22h57m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or under way"})
[t82624 +22h57m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or under way.
[t82630 +22h57m] ORDER captain> take a fix
[t83041 +23h04m] ORDER captain> Say to the officer A merchant brig coming in to the channel there.
[t83044 +23h04m] ORDER captain> The glass on her
[t83046 +23h04m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, a Portuguese, deep laden, running in before this NW wind with the flood under her, likely bound for the road. She's right ahead a mile and the channel's narrow, so I'll watch her bearing. If she comes down on us before we weigh, we'll want to see which side she means to pass."})
[t83046 +23h04m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t83046 +23h04m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t83340 +23h09m] ORDER captain> the glass on her
[t84109 +23h21m] ORDER captain> the glass on her
[t84431 +23h27m] DIRECTOR> 
    calls: journal({"note": "04:27 Possible bug for the owner: the São Pedro now bears S, 4 cables, while the land about Pointe de Pergueridre bears S at 1 cable. She would be on or over the land south of the point, unless the 'land a cable' is a rock. Her track yesterday also had her heading away from Roscoff at night. Her far or crewed route may cut across the land near the Roscoff channel."})
[t84431 +23h27m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or under way"})
[t84431 +23h27m] JOURNAL director [note] 04:27 Possible bug for the owner: the São Pedro now bears S, 4 cables, while the land about Pointe de Pergueridre bears S at 1 cable. She would be on or over the land south of the point, unless the 'land a cable' is a rock. Her track yesterday also had her heading away from Roscoff at night. Her far or crewed route may cut across the land near the Roscoff channel.
[t84431 +23h27m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or under way.
[t86235 +23h57m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or under way"})
[t86235 +23h57m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or under way.
[t88038 +24h27m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or under way"})
[t88038 +24h27m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or under way.
[t88051 +24h27m] ORDER captain> Tell the officer I'm weighing and getting under way, I think we can make it on this wind, and we're going to try.
[t88059 +24h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. With her at NW by N she'll lie W close-hauled on the starboard tack. The Portuguese is past us to the south and bound in, so she's clear. I'll keep the lead going and call the Lavandière's bearing as we close it."})
[t88059 +24h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "under way"})
[t88059 +24h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until under way.
[t88095 +24h28m] ORDER captain> Tell the officer Ah, damn it all, avast that. It's so marginal, I don't think we'll make it, though is the tide making northeast right now?
[t88104 +24h28m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, she's riding to the flood, which is setting NE, about a knot and a half by yesterday's reckoning. It turned at 01:35. Yesterday the flood ran about six hours, so the ebb should make about half past seven and run west with us. Hove short, she has water enough here to wait for it: two fathoms at low water by the chart. With the ebb under her, this wind should do it."})
[t88104 +24h28m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t88104 +24h28m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t88140 +24h29m] ORDER captain> Tell the officer I actually think that a northeast set is what we want, as we are closer to the south shore now and forced onto it by leeway.
[t88150 +24h29m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A fair point, sir. The north in that set holds us off Pergueridre against the leeway, and with the wind this far north we're not beating as we were yesterday, so the east in it only costs us about a knot. If she'll lie W at four or five knots, we still make good three or four. I'd go now if you're willing, and I'll call the lead."})
[t88150 +24h29m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t88150 +24h29m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t88175 +24h29m] ORDER captain> Get under way on the starboard tack
[t88181 +24h29m] ORDER captain> Steer west
[t88721 +24h38m] ORDER captain> steer west
[t88753 +24h39m] OFFICER OF THE WATCH DOOR: {"after_orders": 94, "after_inputs": 181, "door": "speak", "reason": "", "by": "its own order"}
[t88753 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t88753 +24h39m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until a word on deck at my own word.
[t88762 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, only the jib is drawing. The getting-under-way didn't set the lugs; it's the same as yesterday. She'll want the fore and main lugs at once to claw off Pergueridre, a cable on the larboard bow. And I can't heave the lead without the deck. Will you have it heaved?"})
[t88762 +24h39m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t88762 +24h39m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t88768 +24h39m] ORDER captain> Belay getting under way
[t88771 +24h39m] ORDER captain> YOu have the deck
[t88771 +24h39m] JOURNAL officer of the watch [agent.deck] Took the deck from the captain.
[t88775 +24h39m] ORDER captain> Set the mizen
[t88780 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the main lug"})
[t88780 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the fore lug"})
[t88780 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer W by S"})
[t88780 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t88783 +24h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, I have the deck. Setting the fore and main lugs, steering W by S to keep her full till she gathers way, and the lead's going. The anchor's at the bows, ready if we need it."})
[t88783 +24h39m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88783 +24h39m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88804 +24h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "all hands"})
[t88804 +24h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88804 +24h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88806 +24h40m] ORDER captain> Take a fix
[t88807 +24h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88807 +24h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88819 +24h40m] ORDER captain> Tell the officer I just want you to know, if we go aground, I don't blame you.
[t88823 +24h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir. I'll do my best to give you no cause. The lugs are going up now and the tide's near the top, so there's water under her."})
[t88823 +24h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88823 +24h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88846 +24h40m] ORDER captain> Tell the officer We'll damn this westerly while we're at it.
[t88849 +24h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88849 +24h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88870 +24h41m] ORDER captain> take a fix
[t88904 +24h41m] ORDER captain> the nearest shore
[t88910 +24h41m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t88911 +24h41m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88911 +24h41m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88919 +24h41m] ORDER captain> Steer west
[t88926 +24h42m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88926 +24h42m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88968 +24h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, the main and mizen lugs are shaking. She's pinched at W. Let her go W by S to keep her full and moving, or the leeway takes it all back. And the chart shows shoal water hereabouts, with the tide falling."})
[t88968 +24h42m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t88968 +24h42m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t88978 +24h42m] ORDER captain> Haul aft the fore lug sheet
[t88982 +24h43m] ORDER captain> Haul aft the main lug sheet
[t88985 +24h43m] ORDER captain> Haul aft the mizen lug sheet
[t88991 +24h43m] ORDER captain> The sails
[t89017 +24h43m] ORDER captain> Tell the officer I know. We're in it now. I'm not sure we can make it, but we're in it now.
[t89022 +24h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's drawing now, sir, with the lugs flat aft: four knots, heading W by N. She's moving, and that'll carry her. I'll sing out the lead."})
[t89022 +24h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t89022 +24h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t89039 +24h43m] ORDER captain> Steady on
[t89045 +24h44m] ORDER captain> Take a fix
[t89089 +24h44m] ORDER captain> take a fix
[t89156 +24h45m] ORDER captain> take a fix
[t89228 +24h47m] ORDER captain> take a fix
[t89263 +24h47m] ORDER captain> Tell the officer OK, we're doing it, we've clawed off and we have real way on. Once we are clear a bit more we can bear off and just need to watch the Lavandiere. The worst is over for now.
[t89272 +24h47m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Well done, sir, she's walking now. Two things ahead: the pilots' boat is right ahead, five cables, standing toward us, so she'll want to pass clear; and the Lavandière is dead on our course, a mile by account. I'll look at the chart for the side to give it."})
[t89272 +24h47m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t89275 +24h47m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 5", "note": "coast span too coarse: the Isle of Bas channel is a knot at the centre; open water W and NW beyond."})
[t89275 +24h47m] OFFICER OF THE WATCH> 
    calls: chart({"span": "harbour"})
[t89279 +24h47m] DIRECTOR DOOR: {"after_orders": 112, "after_inputs": 202, "door": "journal", "reason": "05:47 (11 June) Under way and clawing off on NW by N; the captain says the worst is over. No hand of mine in it. Next: a quiet passage W along the Léon coast, then the Iroise, about 46 mi, perhaps by mid-afternoon. Ideas for later, if the day wants them and only as plausible things: (a) Saint-Guénolé or another Brest chasse-marée met on the grounds, a hail and a word on where the shoals are; (b) birds working over a shoal, if a 'mark' can say it outside the horizon; (c) at most a British cruiser seen far off, hull-down, n …[+91]
[t89279 +24h47m] JOURNAL director [note] 05:47 (11 June) Under way and clawing off on NW by N; the captain says the worst is over. No hand of mine in it. Next: a quiet passage W along the Léon coast, then the Iroise, about 46 mi, perhaps by mid-afternoon. Ideas for later, if the day wants them and only as plausible things: (a) Saint-Guénolé or another Brest chasse-marée met on the grounds, a hail and a word on where the shoals are; (b) birds working over a shoal, if a 'mark' can say it outside the horizon; (c) at most a British cruiser seen far off, hull-down, never closing, near Ushant. Keep the brief: nothing much, a nice day.
[t89292 +24h48m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:47, the harbour chart: the western entrance of the channel of Bas bears about W by N, 9½ cables, about a cable north of a due-W line. The Lavandière bears W, about 9 cables, less than half a cable south of that line. Heading W by N, we pass about a cable and a quarter north of it. Leave it to larboard, and don't bear away south until it's abaft the beam. The Isle of Bas shore runs along the north side of the channel west of the road; islets lie along the south."})
[t89292 +24h48m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 6", "note": "The western entrance bears W by N about 9½ cables; the Lavandière W about 9 cables, just south of the line. Steady W by N leaves it a cable or so to larboard."})
[t89292 +24h48m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say From the chart, sir: the western entrance bears W by N, near a mile, and the Lavandière lies just south of a due-W line from us. Steady as she goes, W by N, and we pass about a cable north of it, leaving it to larboard. I'd not bear away south until it's abaft the beam."})
[t89292 +24h48m] JOURNAL officer of the watch [note] 05:47, the harbour chart: the western entrance of the channel of Bas bears about W by N, 9½ cables, about a cable north of a due-W line. The Lavandière bears W, about 9 cables, less than half a cable south of that line. Heading W by N, we pass about a cable and a quarter north of it. Leave it to larboard, and don't bear away south until it's abaft the beam. The Isle of Bas shore runs along the north side of the channel west of the road; islets lie along the south.
[t89296 +24h48m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89296 +24h48m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89335 +24h48m] ORDER captain> Tell the officer Aye, there is water south of the Lavandiere on my chart, we could ask the pilot of it and consider bearing off to pass it to larboard, it on the starboard.
[t89343 +24h49m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Worth asking, sir. My sheet marks the western entrance of the channel north of the Lavandière, and the water south of it is strewn with rocks and islets. That's no place to go feeling about on a falling tide without a man who knows it. With the wind this far north, the north side is a fair course and needs no bearing off. But the pilots' boat is close ahead, four cables; she'll know if the south passage serves."})
[t89343 +24h49m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89343 +24h49m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89349 +24h49m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say And a quarter seven, sand: good water under her. The pilots' boat is three cables right ahead, bearing steady. She's standing out to us, so she'll likely round to and hail. That's your chance to ask about the south passage, sir."})
[t89349 +24h49m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89349 +24h49m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89403 +24h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The pilot boat hails, sir: a pilot for Roscoff, if we'll take him. Taking or declining him is yours. He's offered for coming in, not going out, but he'd know the south passage."})
[t89403 +24h50m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89403 +24h50m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89405 +24h50m] ORDER captain> we will take him
[t89438 +24h50m] ORDER captain> Trim the sails
[t89473 +24h51m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, I must correct myself by the pilot. Going out, the passage lies between the Lavandière and the Couillon, a sunken rock two ship's lengths north of it. So we keep the Lavandière close aboard on the larboard hand, an oar's length off as he says, and the Couillon to starboard. Not a cable off as I said; that might put us on the Couillon. I'd put a man on the mizen yard to watch for the two rocks near the island shore, as Mr Cabioch advises; the water's clear enough to see them. And his news is war with Britain, so the cruiser off this island is an enemy."})
[t89473 +24h51m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "send a lookout to the mizen yard"})
[t89476 +24h51m] OFFICER OF THE WATCH> 
    calls: library({"find": "mizen yard"})
[t89478 +24h51m] OFFICER OF THE WATCH> 
    calls: library({"find": "a hand aloft"})
[t89486 +24h51m] OFFICER OF THE WATCH> 
    calls: shelve({})
[t89486 +24h51m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:51, Mr Cabioch, the Roscoff pilot, came aboard. The western passage runs between the Lavandière, a single rock about a third of the way from the isle to the main, and the Couillon, a sunken rock two ship's lengths north of it. Going in, keep the Lavandière an oar's length to starboard; going out, an oar's length to larboard. Inside them, haul toward the island, with a man aloft for the two rocks near the shore. The eastern passage by Roscoff is high water only. The road: anchor over against the great cove mid-isle in 3–4 fathoms at low water, sand. High water at Roscoff about 16:45; the tide rises 26 ft. War news: Britain at war with the Batavian Republic, France and Spain. I co …[+202])
[t89486 +24h51m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89486 +24h51m] JOURNAL officer of the watch [note] 05:51, Mr Cabioch, the Roscoff pilot, came aboard. The western passage runs between the Lavandière, a single rock about a third of the way from the isle to the main, and the Couillon, a sunken rock two ship's lengths north of it. Going in, keep the Lavandière an oar's length to starboard; going out, an oar's length to larboard. Inside them, haul toward the island, with a man aloft for the two rocks near the shore. The eastern passage by Roscoff is high water only. The road: anchor over against the great cove mid-isle in 3–4 fathoms at low water, sand. High water at Roscoff about 16:45; the tide rises 26 ft. War news: Britain at war with the Batavian Republic, France and Spain. I corrected my earlier counsel to pass a cable north of the Lavandière: that risked the Couillon. Note: there's no order for a man on the mizen yard; 'send a lookout to the mizen yard' was not understood.
[t89486 +24h51m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89518 +24h51m] ORDER captain> Say to the pilot Sir, how is the water south of the Lavandiere, within a few cables of it? Passable at this time?
[t89518 +24h51m] JOURNAL director [director.asked] Told Mr Cabioch, the pilot (on the quarterdeck) by the captain: Sir, how is the water south of the Lavandiere, within a few cables of it? Passable at this time?
[t89527 +24h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "bear away one point", "danger": "The Roscoff pilots' boat is lying to right ahead, a cable off, and we're closing on her at five knots."})
[t89527 +24h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Bearing away a point to pass the pilots' boat, sir. She's lying to a cable right ahead. I'll come back to W by N once she's on the starboard quarter."})
[t89529 +24h52m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89529 +24h52m] DIRECTOR> 
    calls: world_order({"text": "say as Mr Cabioch: \"South of her? No, captain, not in this ship. Between the Lavandière and the main it is all foul ground, rock heads that cover at half flood and boil at the ebb. A Roscoff boat creeps through there at the top of springs with a man who was born on them, and even we lose one now and then. Take her out the honest way: the Lavandière close aboard on your larboard hand, an oar's length off, the Couillon to starboard. Keep her full and don't pinch her. Once the Lavandière is abaft the beam you may bear away as much as you please. I'll con you through.\""})
[t89529 +24h52m] WORLD ORDER (the director): say as Mr Cabioch: "South of her? No, captain, not in this ship. Between the Lavandière and the main it is all foul ground, rock heads that cover at half flood and boil at the ebb. A Roscoff boat creeps through there at the top of springs with a man who was born on them, and even we lose one now and then. Take her out the honest way: the Lavandière close aboard on your larboard hand, an oar's length off, the Couillon to starboard. Keep her full and don't pinch her. Once the Lavandière is abaft the beam you may bear away as much as you please. I'll con you through." -> done: Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t89529 +24h52m] JOURNAL director [director.order] Given: say as Mr Cabioch: "South of her? No, captain, not in this ship. Between the Lavandière and the main it is all foul ground, rock heads that cover at half flood and boil at the ebb. A Roscoff boat creeps through there at the top of springs with a man who was born on them, and even we lose one now and then. Take her out the honest way: the Lavandière close aboard on your larboard hand, an oar's length off, the Couillon to starboard. Keep her full and don't pinch her. Once the Lavandière is abaft the beam you may bear away as much as you please. I'll con you through."; Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t89529 +24h52m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89533 +24h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, Mr Cabioch, she's yours to con. I'll keep her full and the lead going, and call you the bearing of the Lavandière."})
[t89533 +24h52m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89533 +24h52m] DIRECTOR> 
    calls: journal({"note": "05:52 The captain took the Roscoff pilot, Mr Cabioch (the game's own), to go out. He asked about the water south of the Lavandière. I answered as Cabioch from the pilot's own directions (rocks and islets south of it; the passage between the Lavandière and the Couillon), saying the south side is foul ground for boats only and to keep the Lavandière close aboard to larboard. Nothing invented against the chart. The pilot's fee is the game's business."})
[t89533 +24h52m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or a sail sighted or the pilot off"})
[t89533 +24h52m] JOURNAL director [note] 05:52 The captain took the Roscoff pilot, Mr Cabioch (the game's own), to go out. He asked about the water south of the Lavandière. I answered as Cabioch from the pilot's own directions (rocks and islets south of it; the passage between the Lavandière and the Couillon), saying the south side is foul ground for boats only and to keep the Lavandière close aboard to larboard. Nothing invented against the chart. The pilot's fee is the game's business.
[t89533 +24h52m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or a sail sighted, or the pilot off.
[t89533 +24h52m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89589 +24h53m] ORDER captain> Tell the pilot Aye, gladly I'd take it on her larboard, but the wind wishes to prevent it. We shall haul up to as high as she'll point, and try to gain northing to pass properly, but I fear the tide and pinching may prevent it. We try.
[t89589 +24h53m] JOURNAL director [director.asked] Told Mr Cabioch, the pilot (on the quarterdeck) by the captain: Aye, gladly I'd take it on her larboard, but the wind wishes to prevent it. We shall haul up to as high as she'll point, and try to gain northing to pass properly, but I fear the tide and pinching may prevent it. We try.
[t89593 +24h53m] ORDER captain> Come up a point
[t89598 +24h53m] DIRECTOR> 
    calls: world_order({"text": "say as Mr Cabioch: \"Aye, she gripes up nicely, your lugger. Hold her so, full and by. If she falls off and won't weather the Lavandière, don't fight it near the rock. Put her about in good time and stand a short board toward the island: there's four and five fathoms off the cove. Then come round again and you'll fetch the gap with room to spare, the ebb beginning to help you within the hour. Two short boards are better than a scraped forefoot. I'll tell you when.\""})
[t89598 +24h53m] WORLD ORDER (the director): say as Mr Cabioch: "Aye, she gripes up nicely, your lugger. Hold her so, full and by. If she falls off and won't weather the Lavandière, don't fight it near the rock. Put her about in good time and stand a short board toward the island: there's four and five fathoms off the cove. Then come round again and you'll fetch the gap with room to spare, the ebb beginning to help you within the hour. Two short boards are better than a scraped forefoot. I'll tell you when." -> done: Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t89598 +24h53m] JOURNAL director [director.order] Given: say as Mr Cabioch: "Aye, she gripes up nicely, your lugger. Hold her so, full and by. If she falls off and won't weather the Lavandière, don't fight it near the rock. Put her about in good time and stand a short board toward the island: there's four and five fathoms off the cove. Then come round again and you'll fetch the gap with room to spare, the ebb beginning to help you within the hour. Two short boards are better than a scraped forefoot. I'll tell you when."; Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t89601 +24h53m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or a sail sighted or the pilot off"})
[t89601 +24h53m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or a sail sighted, or the pilot off.
[t89602 +24h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Boat's clear astern. Steering W, as near as she'll go and stay full, Mr Cabioch. The Lavandière is W by S, eight cables. Give me the helm you want for your oar's length."})
[t89606 +24h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t89606 +24h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89606 +24h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89631 +24h53m] ORDER captain> Trim the sails
[t89647 +24h54m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Lavandière's fine on the larboard bow, seven cables, where we want her. But she's making good W by S over the ground with leeway and the set, about right at the rock. I'll watch her bearing: if it draws aft, we weather her; if it holds steady, we'll want Mr Cabioch's short board in good time."})
[t89647 +24h54m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89647 +24h54m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89654 +24h54m] ORDER captain> Take a fix
[t89662 +24h54m] ORDER captain> Come up half a point
[t89703 +24h55m] ORDER captain> Trim the sails
[t89734 +24h55m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say By the mark ten, sand: deeper than the chart has it here. Good water under her. The Lavandière's W by S, nine cables, and the island shore is two cables on the starboard quarter."})
[t89734 +24h55m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89734 +24h55m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89739 +24h55m] ORDER captain> take a fix
[t89744 +24h55m] ORDER captain> Tell the officer All is well, a fix has her.
[t89747 +24h55m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t89747 +24h55m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t89830 +24h57m] ORDER captain> take a fix
[t89949 +24h59m] ORDER captain> take a fix
[t90091 +25h01m] ORDER captain> take a fix
[t90103 +25h01m] ORDER captain> Tell Mr Lecoq She seems to be weathering it, what say you?
[t90111 +25h01m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I say she is, sir. The Lavandière was W by S at nine cables; she's SW by W at five now, drawn aft a full point, and the course made good has come up to W. Keep her full as she is. Mind the starboard hand: the island is two cables abeam, and the Couillon and the shore rocks lie that side. No higher than this."})
[t90111 +25h01m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t90111 +25h01m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t90381 +25h06m] ORDER captain> Take a fix
[t90584 +25h09m] ORDER captain> take a fix
[t90589 +25h09m] ORDER captain> Bear off a point
[t90631 +25h10m] ORDER captain> Trim the sails
[t90677 +25h11m] ORDER captain> Set the jib
[t90680 +25h11m] ORDER captain> Set the flying jib
[t90729 +25h12m] ORDER captain> Take a fix
[t90739 +25h12m] ORDER captain> Tell the officer I believe we are well out now.
[t90750 +25h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Well out, sir, and well done. The Lavandière's astern on the quarter, sixteen fathoms under her, six knots, and the ebb with us at last. Mr Cabioch will want putting off to his boat before we get far. Then it's yours to shape the course: the Four and Brest for the onions first, or the Iroise grounds."})
[t90750 +25h12m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:12, clear of the channel of Bas by the western passage. Weighed 05:38, the lugs set by 05:43, then close-hauled W by N with the wind NW by N. The pilot Cabioch came aboard at 05:51. We weathered the Lavandière, which drew from W by S to SW by W to SE, and passed north of it. The lead gave 7¼, then 10 fathoms; now 16½ by the chart. Steering W at 6 knots, the ebb setting SW. The captain conned the passage; I kept the lead and the bearings, and bore away a point at 05:52 to clear the pilot boat lying to ahead. Lesson: the 'get under way' evolution sets no lugs on this lugger; set the fore and main lugs by name and call all hands."})
[t90750 +25h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t90750 +25h12m] JOURNAL officer of the watch [note] 06:12, clear of the channel of Bas by the western passage. Weighed 05:38, the lugs set by 05:43, then close-hauled W by N with the wind NW by N. The pilot Cabioch came aboard at 05:51. We weathered the Lavandière, which drew from W by S to SW by W to SE, and passed north of it. The lead gave 7¼, then 10 fathoms; now 16½ by the chart. Steering W at 6 knots, the ebb setting SW. The captain conned the passage; I kept the lead and the bearings, and bore away a point at 05:52 to clear the pilot boat lying to ahead. Lesson: the 'get under way' evolution sets no lugs on this lugger; set the fore and main lugs by name and call all hands.
[t90750 +25h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t90757 +25h12m] ORDER captain> Tell the pilot Thank you for your advice, sir, otherwise I would have tried for south of the Lavandiere and met my fate.
[t90757 +25h12m] JOURNAL director [director.asked] Told Mr Cabioch, the pilot (on the quarterdeck) by the captain: Thank you for your advice, sir, otherwise I would have tried for south of the Lavandiere and met my fate.
[t90760 +25h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t90760 +25h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t90766 +25h12m] DIRECTOR> 
    calls: world_order({"text": "say as Mr Cabioch: \"Your fate? No, captain, you'd only have met my cousin's crab pots and a long wait for the flood. But better the thanks than the salvage. You handled her well in the narrows; she's a weatherly lugger. Put me in your boat when it suits and I'll pull back with the ebb. If you're for the Four, keep the Aber shore at two leagues till you raise the Four's towers: there are no friends of ours off Ushant these days.\""})
[t90766 +25h12m] WORLD ORDER (the director): say as Mr Cabioch: "Your fate? No, captain, you'd only have met my cousin's crab pots and a long wait for the flood. But better the thanks than the salvage. You handled her well in the narrows; she's a weatherly lugger. Put me in your boat when it suits and I'll pull back with the ebb. If you're for the Four, keep the Aber shore at two leagues till you raise the Four's towers: there are no friends of ours off Ushant these days." -> done: Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t90766 +25h12m] JOURNAL director [director.order] Given: say as Mr Cabioch: "Your fate? No, captain, you'd only have met my cousin's crab pots and a long wait for the flood. But better the thanks than the salvage. You handled her well in the narrows; she's a weatherly lugger. Put me in your boat when it suits and I'll pull back with the ebb. If you're for the Four, keep the Aber shore at two leagues till you raise the Four's towers: there are no friends of ours off Ushant these days."; Mr Cabioch spoke on the quarterdeck, heard by Mr Lecoq, the captain, Mr Marie and Guillaume Bourdon, on the quarterdeck
[t90769 +25h12m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:12, Cabioch: for the Four, keep the Aber shore at two leagues until the Four's towers are raised; the English are off Ushant. He wants putting in our boat to pull back on the ebb (the captain's business)."})
[t90769 +25h12m] JOURNAL officer of the watch [note] 06:12, Cabioch: for the Four, keep the Aber shore at two leagues until the Four's towers are raised; the English are off Ushant. He wants putting in our boat to pull back on the ebb (the captain's business).
[t90770 +25h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t90770 +25h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t90775 +25h12m] DIRECTOR> 
    calls: journal({"note": "06:12 Out past the Lavandière at about 06:10 on NW by N 12, the ebb with her now; the captain and Lecoq handled it, with Cabioch's advice. The pilot is to be put off in the ship's boat (the game's own business). MY ERROR: as Cabioch I said 'till you raise the Four's towers', but there was no light tower on the Four rock in 1805 (it was built about 1874). He should have said the Four rock and its breakers. If the Four comes up again, correct it in another voice. Next: the captain chooses Brest (onions) or the Iroise grounds. Both lie down the Léon coast toward the Four and the Chenal du Four. The British blockade off Ushant is historically real; per the brief, at most a far sail."})
[t90775 +25h12m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or a sail sighted or the pilot off"})
[t90775 +25h12m] JOURNAL director [note] 06:12 Out past the Lavandière at about 06:10 on NW by N 12, the ebb with her now; the captain and Lecoq handled it, with Cabioch's advice. The pilot is to be put off in the ship's boat (the game's own business). MY ERROR: as Cabioch I said 'till you raise the Four's towers', but there was no light tower on the Four rock in 1805 (it was built about 1874). He should have said the Four rock and its breakers. If the Four comes up again, correct it in another voice. Next: the captain chooses Brest (onions) or the Iroise grounds. Both lie down the Léon coast toward the Four and the Chenal du Four. The British blockade off Ushant is historically real; per the brief, at most a far sail.
[t90775 +25h12m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or a sail sighted, or the pilot off.
[t91346 +25h22m] ORDER captain> heave to
[t91383 +25h23m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or the pilot off"})
[t91383 +25h23m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or the pilot off.
[t91525 +25h25m] OFFICER OF THE WATCH DOOR: {"after_orders": 137, "after_inputs": 233, "door": "speak", "reason": "", "by": "its own order"}
[t91525 +25h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave to"})
[t91525 +25h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Heaving to for Mr Cabioch's boat, sir. She's a mile astern and coming off for him. Plenty of sea room here. We fill away once he's over the side."})
[t91525 +25h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t91525 +25h25m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until a word on deck at my own word.
[t91525 +25h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t91948 +25h32m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the pilot off"})
[t91948 +25h32m] JOURNAL officer of the watch [agent.stood_by] Stood by until the pilot off.
[t91951 +25h32m] ORDER captain> take a fix
[t91959 +25h32m] ORDER captain> take a bearing of the land
[t91964 +25h32m] ORDER captain> take a bearing of pergueridre
[t92064 +25h34m] LOG [notable/driver.eased] Compression eased to 1x: She has filled and gathers way, the wind on the starboard bow: hove to no longer. The helm keeps her full and by.
[t92068 +25h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the flying jib"})
[t92068 +25h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave to"})
[t92070 +25h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the pilot off"})
[t92070 +25h34m] DIRECTOR> 
    calls: journal({"note": "06:34 Urgent line: she fell off from hove-to and filled while waiting for the pilot boat. Plenty of sea room (24 fathoms, land a mile on the quarter); the ship's matter. No act."})
[t92070 +25h34m] JOURNAL director [note] 06:34 Urgent line: she fell off from hove-to and filled while waiting for the pilot boat. Plenty of sea room (24 fathoms, land a mile on the quarter); the ship's matter. No act.
[t92070 +25h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until the pilot off.
[t92071 +25h34m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or the pilot off"})
[t92071 +25h34m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or the pilot off.
[t92403 +25h40m] DIRECTOR> 
    calls: stand_by({"until": "a glass or a message or a sail sighted"})
[t92403 +25h40m] JOURNAL director [agent.stood_by] Stood by until a glass, or a message, or a sail sighted.
[t92404 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Mr Cabioch is away in his boat, sir, £3 paid, and she's hove to clear of the entrance in twenty fathoms. Which course? For the Four and Brest with the onions, the pilot advises keeping the Aber shore at two leagues. Or the Iroise grounds direct."})
[t92405 +25h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t92405 +25h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t92441 +25h40m] ORDER captain> Steer west by south for now.
[t92448 +25h40m] ORDER captain> Tell the officer Steer west by south for now.
[t92456 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "fill away"})
[t92456 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the main lug"})
[t92456 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the fore lug"})
[t92456 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer W by S"})
[t92459 +25h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, W by S. Filling away, and the lugs are going up again. I'll put her on the course as soon as she's full."})
[t92459 +25h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "filled away"})
[t92459 +25h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until filled away.
[t92485 +25h41m] ORDER captain> Tell the officer Have a look at the ship view while you're at it, see the difference between when the lugs are lowered and raised. She's a fine ship.
[t92488 +25h41m] OFFICER OF THE WATCH> 
    calls: ship_view({})
[t92498 +25h41m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:41, the ship's view from leeward, lugs lowered: the Éclair is a three-masted lugger. A long bowsprit to the left (the bow), with the jib set and drawing to the foremast. The fore and main masts are bare, tall and raked aft, the main the tallest; their lug yards lie along the deck. The mizen lug is set aft, over the stern, its sheet to a bumkin. A low dark hull, heel 1°."})
[t92498 +25h41m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 9", "note": "lugs lowered: fore and main masts bare, their yards on deck; jib and mizen lug set."})
[t92498 +25h41m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t92498 +25h41m] JOURNAL officer of the watch [note] 06:41, the ship's view from leeward, lugs lowered: the Éclair is a three-masted lugger. A long bowsprit to the left (the bow), with the jib set and drawing to the foremast. The fore and main masts are bare, tall and raked aft, the main the tallest; their lug yards lie along the deck. The mizen lug is set aft, over the stern, its sheet to a bumkin. A low dark hull, heel 1°.
[t92498 +25h41m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t92563 +25h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t92564 +25h42m] OFFICER OF THE WATCH> 
    calls: ship_view({})
[t92571 +25h42m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:42, the ship's view with the lugs set: three big tall lugsails, their yards slung high and peaked, the tacks forward at the deck. The main lug is the largest, towering over the hull. The fore lug overlaps the jib; the mizen lug is smaller, aft. She's suddenly a mass of canvas for so low a hull. Heel 2°."})
[t92571 +25h42m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 10", "note": "lugs set: three tall peaked lugsails, the main largest; a lot of canvas on a low hull."})
[t92571 +25h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I've looked, sir, and she is a fine one. With the lugs down she's three bare poles and a jib. With them up, the main lug stands near twice her length in height, and the three of them together are a deal of canvas for so low a hull. No wonder she gripes up and goes. She's on W by S now, the sheets trimming."})
[t92571 +25h42m] JOURNAL officer of the watch [note] 06:42, the ship's view with the lugs set: three big tall lugsails, their yards slung high and peaked, the tacks forward at the deck. The main lug is the largest, towering over the hull. The fore lug overlaps the jib; the mizen lug is smaller, aft. She's suddenly a mass of canvas for so low a hull. Heel 2°.
[t92576 +25h42m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t92576 +25h42m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t92590 +25h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t92590 +25h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t92590 +25h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t92610 +25h43m] ORDER captain> Tell the officer Hah! Ah, it's wonderful. Good catch on the close hauled, if she still lifts with that trim, trim again with "trim the sails" and it'll go as well as it can to the apparent wind.
[t92613 +25h43m] OFFICER OF THE WATCH> 
    calls: journal({"note": "06:43, the captain's tip: 'trim for close hauled' sheets everything flat. If she still lifts after that, 'trim the sails' sets each sail to the apparent wind as well as it'll go."})
[t92613 +25h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t92613 +25h43m] JOURNAL officer of the watch [note] 06:43, the captain's tip: 'trim for close hauled' sheets everything flat. If she still lifts after that, 'trim the sails' sets each sail to the apparent wind as well as it'll go.
[t92613 +25h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t92826 +25h47m] ORDER captain> Tell the officer She seems right to me, just so. The flying jib would do her fine, though.
[t92830 +25h47m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the flying jib"})
[t92830 +25h47m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, the flying jib. She's making six knots on W by S, all drawing, the wind backed a touch to NNW."})
[t92830 +25h47m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t92830 +25h47m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t92984 +25h49m] ORDER captain> take a fix
[t92988 +25h49m] ORDER captain> take a bearing of the land
[t92992 +25h49m] ORDER captain> take a bearing of pergueridre
[t93061 +25h51m] ORDER captain> Tell the officer You may order her full and by to ensure offing from the coast. If that doesn't hold better northing than we're on now, go ahead and steer direct west.
[t93064 +25h51m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "full and by"})
[t93066 +25h51m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t93066 +25h51m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t93370 +25h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer W"})
[t93370 +25h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t93370 +25h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Full and by gave her only WSW, sir, worse than she had, so I'm steering W and trimming flat for it, as you said. She was making seven knots. The land's a mile on the larboard quarter, with twenty-eight fathoms by the chart."})
[t93372 +25h56m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t93372 +25h56m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t93397 +25h56m] ORDER captain> Tell the officer Aye, west it is, if the wind keeps backing to north we may come up to it apiece.
[t93405 +25h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. If she veers on round to the north we can come up and gain our offing. And I'll own I said \"backed\" just now when she'd veered; NW by N to NNW is with the sun. She's settling to W, six knots."})
[t93406 +25h56m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a wind shift"})
[t93406 +25h56m] JOURNAL officer of the watch [agent.stood_by] Stood by until a wind shift.
[t93431 +25h57m] ORDER captain> Tell the officer Aye, I get my words wrong too, just did myself as well.
[t93434 +25h57m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a wind shift"})
[t93434 +25h57m] JOURNAL officer of the watch [agent.stood_by] Stood by until a wind shift.
[t93668 +26h01m] ORDER captain> Trim the sails
[t94207 +26h10m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t94207 +26h10m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t97210 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer W by N"})
[t97210 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t97210 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t97210 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Eight bells, sir. The wind's veered to NNW, fourteen knots, so I'm coming up a point to W by N for offing. The land's two miles on the quarter, and Mr Cabioch said two leagues off the Aber shore. Thirteen miles run since the noon of yesterday's reckoning, seven knots, and the glass is steady at 30.62. Our account's loose now, two miles along the coast, so I'm sounding."})
[t97212 +27h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t97212 +27h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t97235 +27h00m] ORDER captain> Tell the officer Aye, I think west by north is too much to ask, tack ship and we'll gain northing on the larboard tack.
[t97240 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t97240 +27h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, ready about. She'll stand to the NE'ard on the larboard tack and make her northing from the shore."})
[t97240 +27h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t97240 +27h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t97604 +27h06m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t97604 +27h06m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Tacked, sir. She's on the larboard tack heading NE, the land two miles astern on the quarter. A quarter nineteen fathoms, fine sand, by the cast before the tack. Trimming her now. How long a board would you have before we go about again?"})
[t97604 +27h06m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t97604 +27h06m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t97640 +27h07m] ORDER captain> Tell the officer A moment, let me look at the chart. You can take a look too. I think we want a fair offing north'ard before we come back about for south and west, depending on what the wind says of course.
[t97643 +27h07m] OFFICER OF THE WATCH> 
    calls: chart({"span": "passage"})
[t97659 +27h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "08:07, the passage chart, 150 miles across: we're about 2 miles off the north Breton coast, west of the Isle of Bas. The coast runs W–WSW about 20 miles to the NW corner of Brittany (the Four), then turns S. Ushant and its islets lie about 30 miles W and 14 S of us; the Brest inlet is about 22 miles SW by S beyond the corner. The Four bears about WSW, 22 miles. With the wind NW by N, WSW is a close reach on the starboard tack, so there's no beat once we have offing. Plan: stand N on this board about 4 miles to get 2 leagues off, then bear away WSW parallel to the coast."})
[t97659 +27h07m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 11", "note": "The coast runs WSW about 20 mi to the Four; Ushant 30 W, 14 S; Brest's inlet beyond the corner. WSW is a close reach in this wind."})
[t97659 +27h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I've looked, sir. The Aber shore trends WSW from here some twenty miles to the Four, with Ushant thirty miles W and fourteen S. With the wind NW by N, WSW is a close reach on the starboard tack, so once we've our offing it's no beat at all. I'd hold this board about half a glass, four miles of northing to put us two leagues off as the pilot said, then go about and steer WSW with the coast. And a sharp lookout as we near Ushant."})
[t97659 +27h07m] JOURNAL officer of the watch [note] 08:07, the passage chart, 150 miles across: we're about 2 miles off the north Breton coast, west of the Isle of Bas. The coast runs W–WSW about 20 miles to the NW corner of Brittany (the Four), then turns S. Ushant and its islets lie about 30 miles W and 14 S of us; the Brest inlet is about 22 miles SW by S beyond the corner. The Four bears about WSW, 22 miles. With the wind NW by N, WSW is a close reach on the starboard tack, so there's no beat once we have offing. Plan: stand N on this board about 4 miles to get 2 leagues off, then bear away WSW parallel to the coast.
[t97663 +27h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A correction, sir: heading NE at seven knots she makes about five miles of northing in the hour, so four miles is near three-quarters of an hour, not half a glass. Say until two bells, then about."})
[t97663 +27h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t97663 +27h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t97811 +27h10m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t97811 +27h10m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t99932 +27h45m] ORDER captain> Tell the officer You may bring her about and keep he full and by on the starboard.
[t99936 +27h45m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t99936 +27h45m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, about ship, then full and by on the starboard tack. The land's out of sight astern, forty fathoms by the chart, and the glass is up to 30.65."})
[t99936 +27h45m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t99936 +27h45m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t100195 +27h49m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "full and by"})
[t100195 +27h49m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t100195 +27h49m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t100195 +27h49m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t100315 +27h51m] ORDER captain> how am I
[t100317 +27h51m] ORDER captain> eat
[t100318 +27h51m] ORDER captain> drink
[t100332 +27h52m] ORDER captain> Tell the officer Bring her up a point and a half, at least. See how she luffs.
[t100336 +27h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "come up a point and a half"})
[t100337 +27h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t100337 +27h52m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t100337 +27h52m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t100642 +27h57m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Up a point and a half, sir, W by S, and she takes it sweetly: the wind forty-four degrees on the bow apparent, seven knots, every sail full and not a shiver. Making good W. She'd likely bear another half point if you want more northing."})
[t100642 +27h57m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t100642 +27h57m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t100683 +27h58m] ORDER captain> Tell the officer Nay, this shall do fine. Are you doing alright, need a drink or bite to eat? I'm quite tired now myself.
[t100686 +27h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "how am I"})
[t100690 +27h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "drink"})
[t100690 +27h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "eat"})
[t100690 +27h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir. I was dry and hungry, and I've just had a drink and a biscuit on deck. I've had my sleep, so I'm good for the forenoon. Go below and rest, sir. I'll hold her W by S with two leagues of offing, and call you when we raise the land about the Four, or for any sail."})
[t100692 +27h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t100692 +27h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t100707 +27h58m] ORDER captain> Tell the officer Thank you, Mr Lecoq, you have her.
[t100709 +27h58m] ORDER captain> Go to my cabin
[t100715 +27h58m] OFFICER OF THE WATCH> 
    calls: journal({"note": "08:58, the captain gone to rest; I have her, with general authority. Starboard tack W by S, close-hauled at 44° apparent, 7 knots, making good W. Wind NNW 12–17 knots, glass 30.65 rising. About 2 leagues off the Aber shore, the land out of sight. Bound for the Four and Brest (onions for Le Bris), then the Iroise grounds. Call the captain at the landfall about the Four, for any sail, or for a shift. On my feet since 00:12, fed and watered at 08:58."})
[t100715 +27h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t100715 +27h58m] JOURNAL officer of the watch [note] 08:58, the captain gone to rest; I have her, with general authority. Starboard tack W by S, close-hauled at 44° apparent, 7 knots, making good W. Wind NNW 12–17 knots, glass 30.65 rising. About 2 leagues off the Aber shore, the land out of sight. Bound for the Four and Brest (onions for Le Bris), then the Iroise grounds. Call the captain at the landfall about the Four, for any sail, or for a shift. On my feet since 00:12, fed and watered at 08:58.
[t100715 +27h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t100717 +27h58m] ORDER captain> Sleep
[t100719 +27h58m] DIRECTOR DOOR: {"after_orders": 156, "after_inputs": 271, "door": "speak", "reason": "", "by": "its own order"}
[t100719 +27h58m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Sainte-Barbe\" of France at 48 22 N 4 54 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest"})
[t100719 +27h58m] WORLD ORDER (the director): ship: a lugger "Sainte-Barbe" of France at 48 22 N 4 54 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest -> refused: not carried out: Sainte-Barbe's plan crosses the land on the leg to 48 19.7 N 4 58.3 W; give her a way by marks (via)
[t100719 +27h58m] JOURNAL director [agent.resumed] Ended the stand-by until an hour, or a message, or a sail sighted at my own word.
[t100719 +27h58m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): ship: a lugger "Sainte-Barbe" of France at 48 22 N 4 54 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest (Sainte-Barbe's plan crosses the land on the leg to 48 19.7 N 4 58.3 W; give her a way by marks (via))
[t100724 +27h58m] DIRECTOR> 
    calls: world_order({"text": "ship: a lugger \"Sainte-Barbe\" of France at 48 19.7 N 4 58.3 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest"})
[t100724 +27h58m] WORLD ORDER (the director): ship: a lugger "Sainte-Barbe" of France at 48 19.7 N 4 58.3 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest -> done: a chasse-marée, three-masted under lugs 'Sainte-Barbe' of France put on the sea, bound for Brest, her captain's intent fish on the Passage de l'Iroise for 10 hours from Brest
[t100724 +27h58m] JOURNAL director [director.order] Given: ship: a lugger "Sainte-Barbe" of France at 48 19.7 N 4 58.3 W, bound for Brest, intent: fish on the Passage de l'Iroise for 10 hours from Brest; a chasse-marée, three-masted under lugs 'Sainte-Barbe' of France put on the sea, bound for Brest, her captain's intent fish on the Passage de l'Iroise for 10 hours from Brest
[t100731 +27h58m] DIRECTOR> 
    calls: journal({"note": "08:58 Put the Sainte-Barbe (a chasse-marée of Brest) on the Passage de l'Iroise ground at 48°19.7'N 4°58.3'W, about 28 mi from Éclair and beyond the horizon, fishing sardines by day for 10 hours. Why: the Iroise is where Éclair is bound, and a working boat on the ground is what a fisherman would expect to find there. She will be a sail to make out as Éclair comes down past the Four, the ground marked by a real neighbour rather than a voice, and someone to hail. (My first try at 48°22'N 4°54'W was refused: her route to the ground crossed the land.) The captain is asleep below; Lecoq has the deck, W by S 7 kn, NNW 13."})
[t100731 +27h58m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t100731 +27h58m] JOURNAL director [note] 08:58 Put the Sainte-Barbe (a chasse-marée of Brest) on the Passage de l'Iroise ground at 48°19.7'N 4°58.3'W, about 28 mi from Éclair and beyond the horizon, fishing sardines by day for 10 hours. Why: the Iroise is where Éclair is bound, and a working boat on the ground is what a fisherman would expect to find there. She will be a sail to make out as Éclair comes down past the Four, the ground marked by a real neighbour rather than a voice, and someone to hail. (My first try at 48°22'N 4°54'W was refused: her route to the ground crossed the land.) The captain is asleep below; Lecoq has the deck, W by S 7 kn, NNW 13.
[t100731 +27h58m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t100923 +28h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on her"})
[t100923 +28h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail made out"})
[t100923 +28h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail made out.
[t100926 +28h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sail made out"})
[t100926 +28h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sail made out.
[t101144 +28h05m] ORDER captain> come up on deck
[t101159 +28h05m] ORDER captain> Take a fix
[t101162 +28h06m] ORDER captain> Take a bearing of the land
[t101169 +28h06m] ORDER captain> take a bearing of the church
[t101177 +28h06m] ORDER captain> take a bearing of the church of st pol
[t101203 +28h06m] ORDER captain> the grounds
[t101413 +28h10m] ORDER captain> go to my cabin
[t101414 +28h10m] ORDER captain> sleep
[t104526 +29h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t104526 +29h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t108105 +30h01m] ORDER captain> How am I
[t108110 +30h01m] ORDER captain> Go up on deck
[t108129 +30h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t108129 +30h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t108139 +30h02m] ORDER captain> Say to Mr Lecoq Ah, still before noon I see. Is that the Isle Vierge there, south southeast?
[t108149 +30h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a bearing of the Isle Vierge"})
[t108149 +30h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, that's the Isle Vierge, SSE four miles. We raised her at three bells, SW by W four leagues, and have passed north of her since. Seven-knot sailing: thirty-six miles run, making good W. Forty-three fathoms by the chart, glass 30.67, wind NNW thirteen knots. The sail astern at two bells was never more than her topsails at four leagues, and dropped out of sight by 09:04. Nothing else seen. The Four lies some three or four leagues on, WSW."})
[t108152 +30h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t108152 +30h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t108190 +30h03m] ORDER captain> Ask Mr Lecoq What say you on our passage here, staying in on the shore and straight south for Iroise, or round Ushant?
[t108193 +30h03m] OFFICER OF THE WATCH> 
    calls: library({"find": "passage of the Four"})
[t108195 +30h03m] OFFICER OF THE WATCH> 
    calls: library({"find": "Ushant"})
[t108210 +30h03m] OFFICER OF THE WATCH> 
    calls: answer({"text": "I'd say the inshore way, sir, the Four. My reasons: the book says the English keep their cruisers off Ushant and the Black Rocks, and with navy onions aboard we're a lawful prize. Going round Ushant takes us straight across their station, and thirty miles longer besides. Mr Cabioch's word points the same way: keep the Aber shore at two leagues till we raise the Four's towers. The coasters use the Four to dodge the blockade, and a weatherly lugger drawing a fathom is just the craft for it. With this NNW wind it's a free run south through the channel, no beating. My cautions: it's narrow and rocky with a hard-running stream, and the book says the Fromveur off Ushant runs seven knots. …[+313])
[t108210 +30h03m] OFFICER OF THE WATCH> 
    calls: shelve({})
[t108210 +30h03m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t108210 +30h03m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t108268 +30h04m] ORDER captain> Tell the officer Aye, agreed, I'll get a course charted to keep us close to the coast, I'm down to the cabin for a time for it.
[t108269 +30h04m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t108269 +30h04m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t108275 +30h04m] ORDER captain> Go to my cabin
[t108327 +30h05m] OFFICER OF THE WATCH DOOR: {"after_orders": 165, "after_inputs": 287, "door": "journal", "reason": "11:03, from the library: the Fromveur off Ushant runs 7 knots, and English cruisers keep stations off Ushant and the Black Rocks. 'shape a course for X via A and B' passes land marks 5 miles to seaward. At 11:04 the captain agreed to the inshore passage by the Four and went below to chart a course close along the coast. I hold the deck: W by S, 7 knots, NNW 13 knots.", "by": "out of turn"}
[t108327 +30h05m] JOURNAL officer of the watch [note] 11:03, from the library: the Fromveur off Ushant runs 7 knots, and English cruisers keep stations off Ushant and the Black Rocks. 'shape a course for X via A and B' passes land marks 5 miles to seaward. At 11:04 the captain agreed to the inshore passage by the Four and went below to chart a course close along the coast. I hold the deck: W by S, 7 knots, NNW 13 knots.
[t108376 +30h06m] ORDER captain> Come up on deck
[t108420 +30h07m] ORDER captain> Say to Mr Lecoq *Showing him the chart* Here you have it, courses charted, circles showing the offings, what say you? I'll give you the coordinates to shape a course via marks, if you agree with the chart.
[t108423 +30h07m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t108445 +30h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "11:07, the captain's pencil on the coast chart: the first leg is 230°, 12.7 miles from us to a waypoint off the NW corner, with a 3.4-mile offing circle. From there the line turns S toward the Four. The leg runs about 5 miles off the coast abreast the Isle Vierge, closing to about 2¾–3 miles near the islets west of it. Cabioch's advice was 2 leagues. Leeway and the SW ebb both set us toward the shore."})
[t108445 +30h07m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 14", "note": "captain's leg 230° 12.7 mi to a waypoint off the NW corner, offing circle 3.4 mi; closest to the coast islets about 3 mi, then S for the Four."})
[t108445 +30h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A good chart, sir, and I agree the way. One thought on the first leg: 230° for twelve and a half miles brings us within about three miles of the islets west of the Isle Vierge. That coast throws its rocks a long way out, and our leeway and the ebb both set us in toward it. Mr Cabioch said two leagues. I'd lay the turning mark a mile or two further out to the NW, say 235° or 240° for the first leg, and come down on the Four from there. Otherwise I'm with you. Give me the marks and I'll shape it."})
[t108445 +30h07m] JOURNAL officer of the watch [note] 11:07, the captain's pencil on the coast chart: the first leg is 230°, 12.7 miles from us to a waypoint off the NW corner, with a 3.4-mile offing circle. From there the line turns S toward the Four. The leg runs about 5 miles off the coast abreast the Isle Vierge, closing to about 2¾–3 miles near the islets west of it. Cabioch's advice was 2 leagues. Leeway and the SW ebb both set us toward the shore.
[t108447 +30h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t108447 +30h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t108608 +30h10m] ORDER captain> Tell the officer Shape a course to 48 17 N 4 48 W via 48 36 N 4 52 W, then 48 23 N 4 49 W, then 48 22 N 4 49 W
[t108611 +30h10m] ORDER captain> You may shape a course
[t108611 +30h10m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: shape a course for.
[t108612 +30h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 17 N 4 48 W via 48 36 N 4 52 W then 48 23 N 4 49 W then 48 22 N 4 49 W"})
[t108621 +30h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t108621 +30h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Course shaped, sir: SW by W, twelve miles to the first mark, near the line I'd hoped for, and thank you. Then down by your marks to 48° 17'. The wind comes abeam on that heading, so she'll fly. The master says the tide turns about half past eleven; I'll shape her afresh when it does. The lead goes as we close the Four."})
[t108621 +30h10m] OFFICER OF THE WATCH> 
    calls: journal({"note": "11:10, the captain's course: for 48°17'N 4°48'W via 48°36'N 4°52'W, then 48°23'N 4°49'W, then 48°22'N 4°49'W. The captain also allowed 'shape a course'. The first leg is SW by W (238°), 12 miles, the wind abeam. The master's tide turns about 11:30; re-shape then. Watch the offing from the islets west of the Isle Vierge, and get the lead going as we close the Four."})
[t108621 +30h10m] JOURNAL officer of the watch [note] 11:10, the captain's course: for 48°17'N 4°48'W via 48°36'N 4°52'W, then 48°23'N 4°49'W, then 48°22'N 4°49'W. The captain also allowed 'shape a course'. The first leg is SW by W (238°), 12 miles, the wind abeam. The master's tide turns about 11:30; re-shape then. Watch the offing from the islets west of the Isle Vierge, and get the lead going as we close the Four.
[t108623 +30h10m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t108623 +30h10m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t109079 +30h17m] ORDER captain> Trim the sails
[t109991 +30h33m] ORDER captain> take a bearing of the isle vierge
[t111291 +30h54m] ORDER captain> take a bearing of the isle vierge
[t111316 +30h55m] ORDER captain> Tell the officer You may reshape the course again, our account was moved by the bearing, and the tide is changing.
[t111319 +30h55m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 17 N 4 48 W via 48 36 N 4 52 W then 48 23 N 4 49 W then 48 22 N 4 49 W"})
[t111323 +30h55m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t111323 +30h55m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Re-shaped, sir: WSW now, five miles to the first mark by the new account. The land is three miles abeam to larboard, the Four S by W two leagues and a half by account. The master's at his noon sight. The tide turns again about a quarter past twelve, and I'll shape afresh then."})
[t111323 +30h55m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "noon"})
[t111323 +30h55m] JOURNAL officer of the watch [agent.stood_by] Stood by until noon.
[t111608 +31h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Noon, sir. Latitude by observation 48° 37' N, which agrees with the account. Forty-four miles made good since yesterday's noon. The first mark is about four miles on, WSW. The glass is 30.68 and rising, the wind NNW fifteen knots, and she's making eight knots."})
[t111608 +31h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t111608 +31h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t111621 +31h00m] ORDER captain> Tell the officer All is well, and she's flying rightly.
[t111624 +31h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t111624 +31h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t111627 +31h00m] ORDER captain> how am I
[t111632 +31h00m] ORDER captain> go up on deck
[t111728 +31h02m] ORDER captain> how am I
[t111736 +31h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t111736 +31h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t112028 +31h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 17 N 4 48 W via 48 36 N 4 52 W then 48 23 N 4 49 W then 48 22 N 4 49 W"})
[t112028 +31h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t112030 +31h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t112030 +31h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t112045 +31h07m] ORDER captain> Tell the officer No need to fight for the exact mark, you can keep off the wind and aim for the line south of the mark.
[t112062 +31h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 17 N 4 48 W via 48 33 N 4 51 W then 48 23 N 4 49 W then 48 22 N 4 49 W"})
[t112066 +31h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t112066 +31h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, bearing off for your line. A word on why I didn't steer straight south: by account the Four rock lies six miles due S of us, on our own meridian. So I've shaped for 48° 33', 4° 51', on your line about two miles W of the rock, SSW five miles, and then down your marks. The wind comes on the quarter; she'll run."})
[t112066 +31h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t112066 +31h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t112366 +31h12m] ORDER captain> Trim for the wind abeam
[t112688 +31h18m] ORDER captain> Trim the sails
[t113031 +31h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t113031 +31h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix"})
[t113035 +31h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a bearing of the light on Ushant"})
[t113035 +31h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t113038 +31h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Ushant light's in sight, sir, SW by W four leagues. A line from it moved us two cables ENE. No fix to be had yet, the marks cut too fine. The Four is S by E four miles by account, and she's making good SW, so we pass it well to the W. The lead's going. The mizen lifts on the beam, so I'm trimming her again."})
[t113038 +31h23m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t113038 +31h23m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t113115 +31h25m] ORDER captain> Tell the officer Aye, thank you, the wind was merely coming forward on the set trim by our speed. If you ever see a singular sail shaking, you can trim it fine by hauling or easing the sheets by fathoms. When in doubt, trim it out, though.
[t113119 +31h25m] OFFICER OF THE WATCH> 
    calls: journal({"note": "12:25, the captain's tip: a single shaking sail can be trimmed finely by hauling or easing its sheet by fathoms. When in doubt, 'trim the sails'. The apparent wind comes forward as she gathers speed on a set trim."})
[t113119 +31h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t113119 +31h25m] JOURNAL officer of the watch [note] 12:25, the captain's tip: a single shaking sail can be trimmed finely by hauling or easing its sheet by fathoms. When in doubt, 'trim the sails'. The apparent wind comes forward as she gathers speed on a set trim.
[t113119 +31h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t113315 +31h28m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "haul in the main lug sheet a fathom"})
[t113315 +31h28m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "haul in the fore lug sheet a fathom"})
[t113315 +31h28m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "haul in the mizen lug sheet a fathom"})
[t113318 +31h28m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t113318 +31h28m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t113533 +31h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix"})
[t113533 +31h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t113537 +31h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a bearing of the land"})
[t113546 +31h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, the way's shaped S now for your mark at 48° 23'. That line passes the Four rock about a mile to the west of it, and our account is only good to a mile east or west, with no fix to be had: Ushant and the Isle Vierge cut too fine. The hand lead finds no bottom. I'd like either a mark laid a mile further W abreast the Four, at 48° 31', 4° 51', or your word that your chart shows the passage clear as you laid it. Which will you have?"})
[t113546 +31h32m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t113546 +31h32m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t113557 +31h32m] ORDER captain> take a bearing of the light on ushant
[t113612 +31h33m] ORDER captain> Tell the officer Don't shape a course again yet, simply run a point west of south until we get a better fix and get back on the charted course. Our mark triggered a bit soon, once we are down in the tight passage we'll be sailing by hand and using the chart just as reference, I think.
[t113616 +31h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer S by W"})
[t113616 +31h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t113616 +31h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, S by W, and no new shaping. I'll take a fix the moment two marks cut, and keep the lead going."})
[t113618 +31h33m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sighting"})
[t113618 +31h33m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sighting.
[t113644 +31h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by Molene and the Isle Vierge"})
[t113652 +31h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A fix, sir, by Molène SSW and the Isle Vierge ENE, cutting at forty-five degrees: 48° 34' N, 4° 49' W. But at those distances it's only good to a mile. It moved us three cables ESE, toward the Four. On S by W we pass about a mile W of it, so I'd as soon have another half point of westing till the Four's abeam, if you agree."})
[t113652 +31h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t113652 +31h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t113663 +31h34m] ORDER captain> Tell the officer Aye, agreed.
[t113668 +31h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "come up half a point"})
[t113668 +31h34m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t113668 +31h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t113668 +31h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t113824 +31h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Four and Keller"})
[t113827 +31h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Four in sight, sir, SSE three miles, forty degrees on the larboard bow. On SSW we pass her near two miles to the W. A good fix by the Four and Keller, cutting at eighty degrees: 48° 34', 4° 49', good to four cables. That's better. The land's two miles on the larboard bow. Shall I hold SSW till she's abeam, then come down for your mark in the channel?"})
[t113827 +31h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t113827 +31h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t113865 +31h37m] ORDER captain> Tell the officer Aye, right by me.
[t113869 +31h37m] OFFICER OF THE WATCH> 
    calls: journal({"note": "12:37, the Four in sight SSE 3 miles. A fix by the Four and Keller at 80°: 48°34'N 4°49'W, good to 4 cables. Steering SSW (197°) to pass the Four about 2 miles W; when she's abeam, come down for the captain's mark at 48°23'N 4°49'W in the channel, by hand, with the chart as reference. The captain decides the narrows. No bottom at 20 fathoms; the chart gives about 46."})
[t113869 +31h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t113869 +31h37m] JOURNAL officer of the watch [note] 12:37, the Four in sight SSE 3 miles. A fix by the Four and Keller at 80°: 48°34'N 4°49'W, good to 4 cables. Steering SSW (197°) to pass the Four about 2 miles W; when she's abeam, come down for the captain's mark at 48°23'N 4°49'W in the channel, by hand, with the chart as reference. The captain decides the narrows. No bottom at 20 fathoms; the chart gives about 46.
[t113869 +31h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t114786 +31h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "haul in the main lug sheet a fathom"})
[t114786 +31h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Four and Molene"})
[t114786 +31h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t114790 +31h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Four's SE two miles, near abeam, sir. A fix by the Four and Molène: 48° 33', 4° 50', good to four cables. Ahead the book marks La Helle SSW and the Platresses S, both three leagues, so the channel narrows there and the marks are your business. I'll come down to S for your mark at 48° 23', 4° 49' when you say, and keep the lead going. Point Conquet's in sight, S by E four leagues."})
[t114790 +31h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t114790 +31h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t114828 +31h53m] ORDER captain> Tell the officer I'd hold for now another 15 minutes, then shape a plain course for 48 23 N 4 49 W
[t114832 +31h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. Hold SSW till about 13:08, then a plain course for 48° 23', 4° 49'."})
[t114832 +31h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t114832 +31h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t115339 +32h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted"})
[t115339 +32h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted.
[t115390 +32h03m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t115390 +32h03m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t115390 +32h03m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t115694 +32h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Four and Molene"})
[t115694 +32h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 23 N 4 49 W"})
[t115694 +32h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t115694 +32h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t115703 +32h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Course shaped, sir: S for your mark, eight miles. But mark this: the master allows the flood in the channel at four knots against us, to the N by E, until about four o'clock. At seven knots through the water we make good about three over the ground, near three hours to the mark. And if she slows or the wind falls light among the Platresses and La Valbelle, that stream carries us onto them. We can go on and push through, or stand off and on here clear of the Four till the stream turns at four, then run through with it under us. I'd lean to waiting, but it's your call."})
[t115703 +32h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t115703 +32h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t115754 +32h09m] ORDER captain> the depth of water by the chart
[t115788 +32h09m] ORDER captain> Tell the officer Nay, we make for it. We can duck in to Blanc Sablon if need be.
[t115797 +32h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, we make for it, with Blanc Sablon under our lee if we need it. I'll fix her every quarter hour while the marks serve and keep the lead going."})
[t115797 +32h09m] OFFICER OF THE WATCH> 
    calls: journal({"note": "13:09, into the Chenal du Four against the flood, 4 knots N by E until about 16:00, on the captain's decision. Steering S for 48°23'N 4°49'W, 8 miles; she makes good about 3 knots. Dangers ahead: La Helle SSW, the Platresses S, La Valbelle and La Vinotière S by E, all 2½–3 leagues. Bolt hole: Blanc Sablon, by Le Conquet. A fix every quarter hour, and the lead."})
[t115797 +32h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t115797 +32h09m] JOURNAL officer of the watch [note] 13:09, into the Chenal du Four against the flood, 4 knots N by E until about 16:00, on the captain's decision. Steering S for 48°23'N 4°49'W, 8 miles; she makes good about 3 knots. Dangers ahead: La Helle SSW, the Platresses S, La Valbelle and La Vinotière S by E, all 2½–3 leagues. Bolt hole: Blanc Sablon, by Le Conquet. A fix every quarter hour, and the lead.
[t115797 +32h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t116401 +32h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Four and Molene"})
[t116401 +32h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t116403 +32h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Four and Point Conquet"})
[t116407 +32h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 23 N 4 49 W"})
[t116407 +32h20m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t116407 +32h20m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t116702 +32h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on her"})
[t116703 +32h25m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted or a sail made out"})
[t116703 +32h25m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted, or a sail made out.
[t116705 +32h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sail ho, sir: a sail right ahead, S by E, three leagues, about Conquet or beyond in the channel. Her hull's below the horizon, and the glass makes nothing of her yet. I'll watch her as she comes up and call you the moment she's made out."})
[t116705 +32h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sail made out"})
[t116705 +32h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sail made out.
[t116739 +32h25m] ORDER captain> Tell the officer Aye, I see her. She looks to be passed through the channel to the southern side, already, unless she's beating in to it, though I doubt it.
[t116742 +32h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t116742 +32h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t117649 +32h40m] ORDER captain> take a fix
[t117723 +32h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on her"})
[t117724 +32h42m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail sighted or a sail made out"})
[t117724 +32h42m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail sighted, or a sail made out.
[t117727 +32h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A second sail, sir, on the larboard bow, SE by S three leagues, toward Bertheaume and the Goulet; neither made out yet. Our fix at 13:40 put us at 48° 29': two miles made in half an hour against the flood, as we reckoned. The land's a mile abeam to larboard now, with twenty-three fathoms by the chart."})
[t117727 +32h42m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sail made out"})
[t117727 +32h42m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sail made out.
[t117784 +32h43m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail made out"})
[t117784 +32h43m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail made out.
[t120167 +33h22m] ORDER captain> take a fix
[t120182 +33h23m] OFFICER OF THE WATCH DOOR: {"after_orders": 188, "after_inputs": 328, "door": "speak", "reason": "", "by": "its own order"}
[t120182 +33h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say And a third sail, sir, on the starboard bow, SW by W four leagues, out toward the Iroise and the open sea. That's the quarter the English would keep. All three are hull down yet."})
[t120182 +33h23m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sail made out"})
[t120182 +33h23m] JOURNAL officer of the watch [agent.resumed] Ended the stand-by until a sail made out at my own word.
[t120182 +33h23m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sail made out.
[t120227 +33h23m] ORDER captain> Tell the officer You might reshape again, we're closing in more, once we hit the mark I'll take the conn to get her through the passage, you mind the sails if you please.
[t120231 +33h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for 48 23 N 4 49 W"})
[t120231 +33h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t120231 +33h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t120235 +33h23m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Re-shaped, sir: S, four miles to the mark, the flood easing to under three knots. The lead's going; the chart gives thirteen fathoms here. Aye, at the mark the con is yours, and I'll mind the sails. The wind's freshened to eighteen knots, NW by N, on the quarter. The sail ahead is two leagues now, S by E."})
[t120235 +33h23m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t120235 +33h23m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t120363 +33h26m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say By the mark thirteen, rock, sir: agrees with the chart, ten fathoms at low water with three of tide. Rocky bottom here, so the channel's beginning."})
[t120363 +33h26m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t120363 +33h26m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t121387 +33h43m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail made out"})
[t121387 +33h43m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail made out.
[t121390 +33h43m] ORDER captain> take a bearing of point conquet
[t121418 +33h43m] ORDER captain> Tell the officer I have the conn from here, bearing off a point to miss the Platresses. Take a moment for a close chart look, if you like.
[t121422 +33h43m] OFFICER OF THE WATCH> 
    calls: chart({"span": "harbour"})
[t121426 +33h43m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 15", "note": "harbour span: no danger within a mile; she lies about 4 cables W of the captain's pencilled line, with a 1.4-mile circle round his mark to the SE."})
[t121426 +33h43m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t121446 +33h44m] OFFICER OF THE WATCH> 
    calls: journal({"note": "14:43, coast chart, close look. The mainland is about 1½–2 miles E. The Platresses are about 2 miles S by W of us; La Valbelle about 2¾ miles SSE, with La Vinotière off Conquet. The gap between the Platresses and La Valbelle is about 1¼ miles. The captain's second mark is in the middle, with an 8-cable circle. On S by E we pass about ¾ mile E of the Platresses and under half a mile W of La Valbelle. Beyond: St Matthew's Point with the Monks, the Cock and La Parquette off it to the E; Le Gouemont and La Vandrée SE; the Black Rocks well W; Bertheaume road ESE beyond St Matthew's. The captain's next leg is 169°, 3 miles, past St Matthew's. Blanc Sablon is just N of Conquet on the main …[+64])
[t121446 +33h44m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 16", "note": "The passage between the Platresses (W) and La Valbelle (E) is about 1¼ mi wide; the captain's marks run down its middle, then 169° past St Matthew's, the Black Rocks well W."})
[t121446 +33h44m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I've had my look, sir. The gap between the Platresses and La Valbelle is about a mile and a quarter, and your mark sits fair in the middle. On S by E we pass three-quarters of a mile E of the Platresses but under half a mile W of La Valbelle, so I'd favour the Platresses side a touch once they're abeam. Then your 169° clears St Matthew's, leaving the Monks and the Cock to larboard and the Black Rocks well out to starboard. One more thing: the hands have been on deck since half past five and are tired. Once we're through, the watch below could go down. Sails are mine; she's drawing well."})
[t121446 +33h44m] JOURNAL officer of the watch [note] 14:43, coast chart, close look. The mainland is about 1½–2 miles E. The Platresses are about 2 miles S by W of us; La Valbelle about 2¾ miles SSE, with La Vinotière off Conquet. The gap between the Platresses and La Valbelle is about 1¼ miles. The captain's second mark is in the middle, with an 8-cable circle. On S by E we pass about ¾ mile E of the Platresses and under half a mile W of La Valbelle. Beyond: St Matthew's Point with the Monks, the Cock and La Parquette off it to the E; Le Gouemont and La Vandrée SE; the Black Rocks well W; Bertheaume road ESE beyond St Matthew's. The captain's next leg is 169°, 3 miles, past St Matthew's. Blanc Sablon is just N of Conquet on the mainland side. The hands are tired: all hands on deck since 05:30.
[t121449 +33h44m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t121449 +33h44m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t121467 +33h44m] ORDER captain> Pipe down
[t121470 +33h44m] ORDER captain> Bear off a point
[t121744 +33h49m] ORDER captain> take a fix
[t121747 +33h49m] ORDER captain> take a bearing of the land
[t121751 +33h49m] ORDER captain> take a bearing of conquet
[t122000 +33h53m] ORDER captain> Steer south quarter west
[t122380 +33h59m] ORDER captain> take a fix
[t122383 +33h59m] ORDER captain> take a bearing of the land
[t122387 +33h59m] ORDER captain> take a bearing of conquet
[t122783 +34h06m] ORDER captain> heave the lead
[t122904 +34h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t122904 +34h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A quarter less sixteen, sand, sir: good water, the Platresses nine cables to the SW. The wind's drawn round to N by W, near dead aft, so I'm trimming the lugs square for it. Mind she doesn't gybe if you bring her any further to starboard. The Brest pilot cutter is standing out toward us."})
[t122904 +34h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t122904 +34h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t122935 +34h08m] ORDER captain> Tell the officer With this wind, I've a mind to fish before standing in to Brest.
[t122943 +34h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A good thought, sir. The book's Iroise ground is drift nets for sardines by day and lines for ling and conger at any hour, and it's open water just beyond St Matthew's. With the afternoon before us, the nets would serve. Two cautions: keep the catch clear of Guéguen's onions, as he begged, and keep the masthead sharp toward the Black Rocks, which the book names as an English station. If a sail comes out from there, Bertheaume road is under our lee."})
[t122943 +34h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t122943 +34h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t122959 +34h09m] ORDER captain> Take a fix
[t122962 +34h09m] ORDER captain> Take a bearing of the land
[t122966 +34h09m] ORDER captain> take a bearing of st matthew's light
[t123289 +34h14m] ORDER captain> steer south
[t123410 +34h16m] ORDER captain> take a bearing of the land
[t123412 +34h16m] ORDER captain> take a fix
[t123416 +34h16m] ORDER captain> take a bearing of the light
[t123420 +34h17m] ORDER captain> take a bearing of st matthew's light
[t123653 +34h20m] ORDER captain> Tell the officer Reef the lugs, one reef. The wind is freshening and we needn't the speed or canvas here.
[t123661 +34h21m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "reef the lugs, one reef"})
[t123661 +34h21m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t123661 +34h21m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, a reef in the lugs. Mind that the wind's gone to N, and on S by E it's come over onto the larboard quarter, by the lee of the lugs. If she yaws to larboard she may gybe them. The chart gives five fathoms here, so I'm sounding again."})
[t123663 +34h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123663 +34h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t123666 +34h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123666 +34h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t123708 +34h21m] ORDER captain> Tell the officer Aye, when the reef is in, dip the lugs, as we'll be on the larboard by a hair.
[t123712 +34h21m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, I'll dip the lugs as soon as the reefs are in."})
[t123712 +34h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123712 +34h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t123724 +34h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix by the Monks and Point Conquet"})
[t123724 +34h22m] DIRECTOR DOOR: {"after_orders": 207, "after_inputs": 356, "door": "read", "reason": "the truth at Afternoon watch (15:22)", "by": "truth()"}
[t123728 +34h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Monks in sight, sir, SSE three miles, a point on the larboard bow. Steering S we pass them well to the W. A fix by the Monks and Point Conquet: 48° 22', 4° 49', good to a cable. The reefs are going in."})
[t123728 +34h22m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123728 +34h22m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t123796 +34h23m] DIRECTOR DOOR: {"after_orders": 207, "after_inputs": 356, "door": "shelve", "reason": "book 16", "by": "out of turn", "note": "15:22 wind N 18 now, N 11 in a watch; Éclair at 48°22'N 4°49'W off St Matthew's; Sainte-Barbe 9 mi SW and Saint-Yves 5 mi SSE fishing the Iroise; the pilot cutter 2.7 mi ESE; busy Brest approaches"}
[t123796 +34h23m] DIRECTOR DOOR: {"after_orders": 207, "after_inputs": 356, "door": "journal", "reason": "15:22 (11 June) Éclair came through the Chenal du Four, by the captain's own conning, against the last of the flood; she is off St Matthew's, about to fish the Iroise before Brest. Wind N 18 (fresh), easing to N 11 within a watch by the systems: no act needed, and a quieter evening for the nets. Neighbours, all real: Sainte-Barbe (mine) 9 mi SW and Saint-Yves (the game's) 5 mi SSE, both fishing the Passage de l'Iroise; Two Sisters, Bom Jesus and Esperança in the approaches; the Brest pilot cutter 2.7 mi ESE standing out;  …[+402]
[t123796 +34h23m] JOURNAL director [note] 15:22 (11 June) Éclair came through the Chenal du Four, by the captain's own conning, against the last of the flood; she is off St Matthew's, about to fish the Iroise before Brest. Wind N 18 (fresh), easing to N 11 within a watch by the systems: no act needed, and a quieter evening for the nets. Neighbours, all real: Sainte-Barbe (mine) 9 mi SW and Saint-Yves (the game's) 5 mi SSE, both fishing the Passage de l'Iroise; Two Sisters, Bom Jesus and Esperança in the approaches; the Brest pilot cutter 2.7 mi ESE standing out; the three Brest chasse-marées at anchor in Brest road. No English cruiser anywhere near, and I put none. BUG for the owner: the surface pressure reads 1039.4 hPa (30.70 in) while no system's centre is above 1028; the highs seem to add rather than combine. The glass has climbed unrealistically high since my two ridges went in. Lesson for me: fewer overlapping systems next time.
[t123950 +34h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123950 +34h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t123998 +34h26m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t123998 +34h26m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124018 +34h26m] ORDER captain> Shape a course for 48 17 N 4 48 W
[t124061 +34h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say And a quarter eight, sand, sir. Note that the master says this line passes the Monks within seven cables. On a falling sea it's fair water, but I'd not let her sag east of it. Dipping the lugs as soon as the mizen's reefed."})
[t124061 +34h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124061 +34h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124072 +34h27m] ORDER captain> Tell the officer YOu may try dipping the fore lug first, I am curious what happens if you dip just one lug now.
[t124075 +34h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the fore lug"})
[t124077 +34h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124077 +34h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124205 +34h30m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or the pilot aboard"})
[t124205 +34h30m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or the pilot aboard.
[t124291 +34h31m] OFFICER OF THE WATCH> 
    calls: ship_view({"facing": "180"})
[t124302 +34h31m] OFFICER OF THE WATCH> 
    calls: journal({"note": "15:31, the ship's view from astern after dipping only the fore lug. The fore lug now stands out to starboard, to leeward of its mast. The main lug is still swung out to larboard, the windward side with the wind on the larboard quarter. The mizen is nearer the centre. In effect she's wing and wing: fore to one side, main to the other, like a goose-wing on a run."})
[t124302 +34h31m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 17", "note": "From astern: the fore lug dipped to starboard, the main still out to larboard, wing and wing."})
[t124302 +34h31m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Dipped the fore lug, sir, and I looked at her from astern: she's wing and wing. The fore lug stands out to starboard to leeward of its mast, and the main is still out to larboard on the windward side, with the mizen near amidships. With the wind this far aft she'll carry it like a goose-wing on the run. But if we come up toward the beam, the main will want dipping to match. Shall I dip the main and mizen too, or leave her winged while we run?"})
[t124302 +34h31m] JOURNAL officer of the watch [note] 15:31, the ship's view from astern after dipping only the fore lug. The fore lug now stands out to starboard, to leeward of its mast. The main lug is still swung out to larboard, the windward side with the wind on the larboard quarter. The mizen is nearer the centre. In effect she's wing and wing: fore to one side, main to the other, like a goose-wing on a run.
[t124305 +34h31m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t124305 +34h31m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t124308 +34h31m] ORDER captain> Tell the officer Oh! Take a look at the ship view from the bow! Goosewing! Goosewing!
[t124311 +34h31m] OFFICER OF THE WATCH> 
    calls: ship_view({"facing": "0"})
[t124315 +34h31m] ORDER captain> Tell the officer You read my mind man!
[t124320 +34h32m] OFFICER OF THE WATCH> 
    calls: journal({"note": "15:31, the view from right ahead: a true goose-wing. The reefed fore lug, its reef band plain to see, spreads to starboard. The great main lug spreads to larboard behind it. The jib crosses in front. Two wings either side of the masts, running before a N wind."})
[t124320 +34h32m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 18", "note": "From ahead: goose-winged, the reefed fore lug to starboard, the main lug to larboard, the jib across the bow."})
[t124320 +34h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Ha! So she is, sir, a proper goose-wing! From ahead she spreads like a gull coming in to land: the reefed fore lug out to starboard, the reef band plain across it, and the great main lug out to larboard behind, with the jib between. I've seen the Morbihan boats run home so before a nor'wester, but never stood on one to see it. Shall I leave her so for the run?"})
[t124320 +34h32m] JOURNAL officer of the watch [note] 15:31, the view from right ahead: a true goose-wing. The reefed fore lug, its reef band plain to see, spreads to starboard. The great main lug spreads to larboard behind it. The jib crosses in front. Two wings either side of the masts, running before a N wind.
[t124330 +34h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir! The Monks bear SE by S, two miles, steady and closing. The line's sagging onto them. I'd steer S, a point to starboard, to open the bearing. The wind comes dead aft, and that's just what a goose-wing wants. Shall I?"})
[t124330 +34h32m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t124330 +34h32m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t124358 +34h32m] ORDER captain> Tell the officer Aye, make it so.
[t124362 +34h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer S"})
[t124362 +34h32m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t124362 +34h32m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t124362 +34h32m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t124666 +34h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on her"})
[t124666 +34h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The Monks have drawn to SE, a mile and a half, sir, so she's opening them. And a schooner on the larboard bow, S by E five miles, standing S by W under plain sail, running out into the Iroise ahead of us. The glass is on her."})
[t124668 +34h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on the schooner"})
[t124671 +34h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124671 +34h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124683 +34h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on the lugger"})
[t124686 +34h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A lugger too, sir, S by E three miles, standing SSW: likely a fisherman bound for the Iroise ground, as we are. The Brest pilot's cutter is a mile abeam to larboard and closing; she'll hail us presently. The Monks hold at SE, opening."})
[t124686 +34h38m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124686 +34h38m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124695 +34h38m] ORDER captain> the glass on her
[t124703 +34h38m] ORDER captain> the glass on a lugger
[t124780 +34h39m] OFFICER OF THE WATCH> 
    calls: journal({"note": "15:38, a form noted: 'the glass on a lugger' (with 'a') works where 'the lugger' does not. Sails in sight: the Brest pilot's cutter (French), a schooner and a lugger S by E, all standing SSW. The Monks opened to SE by E on S; the wind N by E, the lugs goose-winged."})
[t124780 +34h39m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124780 +34h39m] JOURNAL officer of the watch [note] 15:38, a form noted: 'the glass on a lugger' (with 'a') works where 'the lugger' does not. Sails in sight: the Brest pilot's cutter (French), a schooner and a lugger S by E, all standing SSW. The Monks opened to SE by E on S; the wind N by E, the lugs goose-winged.
[t124780 +34h39m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t124814 +34h40m] ORDER captain> Tell the officer The wind coming onto the quarter more, we may dip the main lug next and get her properly re trimmed. The wing-on-wing was fantastic, though.
[t124818 +34h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the main lug"})
[t124818 +34h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, dipping the main lug, and I'll trim her properly when it's over. It was a fine sight, the goose-wing."})
[t124818 +34h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t124818 +34h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t125012 +34h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t125012 +34h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t125026 +34h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t125026 +34h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t125026 +34h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Main lug dipped, sir. All three lugs now stand to leeward on the larboard tack, every one reefed, and trimming for the quarter wind. The Monks are ESE, a mile and a half by account, drawing aft. The schooner ahead has hauled her wind to the W; the lugger stands S."})
[t125030 +34h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A correction, sir: the fore and main stand to leeward now. The mizen I've not dipped; she sheets to her bumkin and stands either way."})
[t125031 +34h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t125031 +34h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t125077 +34h44m] ORDER captain> Tell the officer Fine job, sir, now we make ready for a course to shoot the gear. I must admit, I have not tried this yet, but perhaps we'll both read the fishing primer and see if we can't get her fishing properly.
[t125080 +34h44m] OFFICER OF THE WATCH> 
    calls: library({"topic": "primer 21"})
[t125083 +34h44m] OFFICER OF THE WATCH> 
    calls: library({"topic": "primer 21", "section": "all"})
[t125091 +34h44m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the fishing grounds"})
[t125102 +34h45m] OFFICER OF THE WATCH> 
    calls: journal({"note": "15:44, primer 21, the fisherman. Our chasse-marée carries a fleet of 60 drift nets and her lines. The orders: 'shoot the nets' (over the quarter, before the wind, half an hour); 'haul the nets' (all hands at the capstan, two hours); 'set the lines' (paid out across the tide under easy sail with the wind free, an hour); 'haul the lines' (all hands, three hours). 'shoot the gear' / 'haul the gear' picks what the ground wants this month. The shot is refused if she's off a ground the master knows, out of season or hour, or in too much wind. With nets or lines out, heave to and ride to them. The catch goes into the well first, then the hold, salted while there's salt (we carry none), so …[+278])
[t125102 +34h45m] OFFICER OF THE WATCH> 
    calls: shelve({})
[t125102 +34h45m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I've read it, sir. We carry sixty drift nets and our lines. The Iroise ground fishes the nets for sardines by day in June, so now's the hour, and the lines for ling and conger at any hour. We must be on the ground itself or the shot is refused. Then \"shoot the gear\" shoots the nets over the quarter before the wind, half an hour's work; we heave to and ride to them; and \"haul the gear\" is all hands at the capstan for two hours. We have no salt aboard, so the sardines keep green only half a day in this weather. Brest has a fish quay, and it's four or five leagues off, so we shoot, haul, and run in with the onions and the catch together. And the \"fishing grounds\" query wants …[+131])
[t125102 +34h45m] JOURNAL officer of the watch [note] 15:44, primer 21, the fisherman. Our chasse-marée carries a fleet of 60 drift nets and her lines. The orders: 'shoot the nets' (over the quarter, before the wind, half an hour); 'haul the nets' (all hands at the capstan, two hours); 'set the lines' (paid out across the tide under easy sail with the wind free, an hour); 'haul the lines' (all hands, three hours). 'shoot the gear' / 'haul the gear' picks what the ground wants this month. The shot is refused if she's off a ground the master knows, out of season or hour, or in too much wind. With nets or lines out, heave to and ride to them. The catch goes into the well first, then the hold, salted while there's salt (we carry none), so green fish keep about 8–12 hours in summer. Brest has a fish quay: 'sell the catch'. The Iroise ground is drift nets for sardines June–October by day, and lines for ling and conger. Asking 'the fishing grounds' is not within my authority; it needs the captain's word by name.
[t125106 +34h45m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t125106 +34h45m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t125131 +34h45m] ORDER captain> you may the fishing grounds
[t125136 +34h45m] ORDER captain> the fishing grounds
[t125146 +34h45m] ORDER captain> Tell the officer Can you see that 15:45 fishing grounds log?
[t125151 +34h45m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, I see it: the Passage de l'Iroise, six miles off, nets for sardines by day and lines for ling and conger. I'll try to shape a course for the ground itself."})
[t125151 +34h45m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for the Passage de l'Iroise"})
[t125160 +34h46m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t125176 +34h46m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer S"})
[t125176 +34h46m] OFFICER OF THE WATCH> 
    calls: journal({"note": "15:46, coast chart check of 'shape a course for the Passage de l'Iroise' (SW by S, 6 miles). The line passes within a cable of a cluster of small rocks about a mile SSW of us, off the south end of the Béniguet islets, which is what the master's warning meant. I've held her at S for now; it clears them about half a mile to the E. The lugger and the schooner are about 3½ miles SSE, inside the captain's circle round 48°17', likely fishing the ground. The Black Rocks lie WSW about 4 miles."})
[t125176 +34h46m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 21", "note": "A SW by S line clips small rocks about a mile SSW off the Béniguet chain; S clears them about half a mile E. The fishers are SSE about 3½ mi in the captain's circle."})
[t125176 +34h46m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, I've held her at S rather than the master's SW by S. His warning was right: that line runs within a cable of a knot of small rocks a mile SSW of us, off the tail of the Béniguet islets. On S we pass half a mile E of them. Two miles on, I'd shape again for the ground with sea room. And the lugger and schooner ahead, three and a half miles SSE in your circle, look to be fishing already. The ground may well be where they are."})
[t125176 +34h46m] JOURNAL officer of the watch [note] 15:46, coast chart check of 'shape a course for the Passage de l'Iroise' (SW by S, 6 miles). The line passes within a cable of a cluster of small rocks about a mile SSW of us, off the south end of the Béniguet islets, which is what the master's warning meant. I've held her at S for now; it clears them about half a mile to the E. The lugger and the schooner are about 3½ miles SSE, inside the captain's circle round 48°17', likely fishing the ground. The Black Rocks lie WSW about 4 miles.
[t125179 +34h46m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t125179 +34h46m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t125210 +34h46m] ORDER captain> Tell the officer That makes sense, and good catch on the course, it would have been close indeed. South for now brings us out of the little rocky islets and into the clear ground, I figure.
[t125214 +34h46m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t125214 +34h46m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t125520 +34h52m] ORDER captain> take a fix
[t125819 +34h56m] ORDER captain> we need no pilot
[t125819 +34h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for the Passage de l'Iroise"})
[t125823 +34h57m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer S"})
[t125823 +34h57m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t125823 +34h57m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t125833 +34h57m] ORDER captain> the fishing grounds
[t125881 +34h58m] ORDER captain> Tell the officer We could see if we are in the bounds of the fishing grounds here, perhaps it is not so strict. Let's wait 10 more minutes, head directly downwind, south southwest, and try to shoot the gear.
[t125886 +34h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir: ten minutes more on S, then SSW before the wind and try the nets. The schooner's an American, by her stars and stripes, a neutral trader tacking up for Brest by the look of her. The lugger ahead is two miles off."})
[t125886 +34h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t125886 +34h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t126491 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer SSW"})
[t126491 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shoot the gear"})
[t126495 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say On SSW before the wind, sir. But shooting the gear isn't mine to order under your general word; it wants \"you may shoot the gear\", or you shoot it yourself. New sails about: a brig SW by S four miles standing E, colours not yet made out, and a second lugger SW by W three miles. The wind's fallen light, eight knots."})
[t126495 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on a brig"})
[t126498 +35h08m] ORDER captain> You may shoot the gear
[t126498 +35h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t126498 +35h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t126498 +35h08m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: shoot the gear.
[t126501 +35h08m] ORDER captain> You may haul the gear
[t126501 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shoot the gear"})
[t126501 +35h08m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: haul the gear.
[t126504 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for the Passage de l'Iroise"})
[t126515 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the main lug"})
[t126515 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the fore lug"})
[t126515 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Course shaped SW for the ground, sir, five miles, clear of the shore. That brings the wind onto the starboard quarter, so I'm dipping the main and fore lugs back to leeward. With this light air it'll be an hour and more to the ground. Thank you for the word to shoot and haul."})
[t126520 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Belay that, sir: she's not round yet and the lugs still stand to leeward. I'll dip them once she's on SW and the wind's crossed the stern."})
[t126520 +35h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t126520 +35h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t126529 +35h08m] ORDER captain> Tell the officer Good to dip now.
[t126532 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the main lug"})
[t126532 +35h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "dip the fore lug"})
[t126535 +35h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126535 +35h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t126711 +35h11m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126711 +35h11m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t126742 +35h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t126742 +35h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Both lugs dipped and trimming, sir, on SW. But the wind's died to six knots and she makes barely two, so the ground's two hours off at this rate. With the breeze gone, shall I shake the reefs out of the lugs?"})
[t126742 +35h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t126742 +35h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t126755 +35h12m] ORDER captain> Tell the officer Aye, shake out the reefs.
[t126758 +35h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shake out the reefs"})
[t126758 +35h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126758 +35h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t126772 +35h12m] ORDER captain> Tell the officer Sorry, it would be "shake out the sails, all reefs"
[t126775 +35h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shake out the lugs, all reefs"})
[t126779 +35h12m] OFFICER OF THE WATCH> 
    calls: journal({"note": "16:12, forms noted: 'shake out the lugs, all reefs' (not 'shake out the reefs'); 'reef the lugs, one reef'; 'dip the fore lug' / 'dip the main lug' (refused if already to leeward); 'shoot the gear' / 'haul the gear' need the captain's word by name, which he has given. The shot was refused off the ground: the Passage de l'Iroise is 5 miles SW. On SW now in a dying air (6 kn), so the reefs are shaken out."})
[t126779 +35h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126779 +35h12m] JOURNAL officer of the watch [note] 16:12, forms noted: 'shake out the lugs, all reefs' (not 'shake out the reefs'); 'reef the lugs, one reef'; 'dip the fore lug' / 'dip the main lug' (refused if already to leeward); 'shoot the gear' / 'haul the gear' need the captain's word by name, which he has given. The shot was refused off the ground: the Passage de l'Iroise is 5 miles SW. On SW now in a dying air (6 kn), so the reefs are shaken out.
[t126779 +35h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t126917 +35h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The main lug's reef is out, sir. The lugger ahead, SW by W three miles, is lying to, likely riding to her nets on the ground, so that's our mark. The brig SW by S has closed to three miles, standing E; still no colours made out. I'll watch her."})
[t126917 +35h15m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126917 +35h15m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t126938 +35h15m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t126938 +35h15m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t127053 +35h17m] ORDER captain> shoot the gear
[t127055 +35h17m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t127055 +35h17m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say All reefs out, sir, full sail on her, and trimming. The air's down to five knots. The brig has drawn to SSW, three miles, crossing ahead of us to the E."})
[t127055 +35h17m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t127055 +35h17m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t127069 +35h17m] ORDER captain> Tell the officer Aye, all is well. I'll keep trying to shoot the gear as we close.
[t127073 +35h17m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a stranger's colours made out"})
[t127073 +35h17m] JOURNAL officer of the watch [agent.stood_by] Stood by until a stranger's colours made out.
[t127274 +35h21m] DIRECTOR DOOR: {"after_orders": 227, "after_inputs": 395, "door": "journal", "reason": "16:17 Into the Iroise with a goose-wing run, then the wind dying under the ridge (5 kn by 16:17). The 'lugger lying to, riding to her nets' SW by W 3 mi is almost certainly my Sainte-Barbe, and the captain and mate have taken her for their mark: the placement doing exactly what I meant it to. The captain has given Lecoq leave to shoot and haul. No act. If the calm leaves them short of the ground at sunset, that is a fisherman's evening; I won't conjure a breeze for convenience.", "by": "out of turn"}
[t127274 +35h21m] JOURNAL director [note] 16:17 Into the Iroise with a goose-wing run, then the wind dying under the ridge (5 kn by 16:17). The 'lugger lying to, riding to her nets' SW by W 3 mi is almost certainly my Sainte-Barbe, and the captain and mate have taken her for their mark: the placement doing exactly what I meant it to. The captain has given Lecoq leave to shoot and haul. No act. If the calm leaves them short of the ground at sunset, that is a fisherman's evening; I won't conjure a breeze for convenience.
[t127476 +35h24m] ORDER captain> Shoot the gear
[t127809 +35h30m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail within hail"})
[t127809 +35h30m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail within hail.
[t127828 +35h30m] ORDER captain> the distance of the passage de l'iroise
[t127831 +35h30m] ORDER captain> Shoot the gear
[t127986 +35h33m] ORDER captain> take a fix
[t127989 +35h33m] ORDER captain> take a bearing of the land
[t127994 +35h33m] ORDER captain> take a bearing of the monks
[t128004 +35h33m] ORDER captain> Shape a course for the passage de l'iroise
[t128223 +35h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on a brig"})
[t128227 +35h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The brig to the S, two miles, is a Portuguese merchantman, deep laden, standing in for Brest. Harmless. A French chasse-marée, a sister to us, is a mile S. A second brig is coming down from the W by S, four miles, standing SE by S; I'll have the glass on her as she closes. She's the one to watch, coming from the Black Rocks quarter."})
[t128227 +35h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a stranger's colours made out"})
[t128227 +35h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a stranger's colours made out.
[t128239 +35h37m] ORDER captain> Shoot the gear
[t128251 +35h37m] ORDER captain> The distance of the passage de l'iroise
[t128799 +35h46m] ORDER captain> take a bearing of the land
[t128803 +35h46m] ORDER captain> Shape a course for the passage de l'iroise
[t128943 +35h49m] ORDER captain> Trim the sails
[t128949 +35h49m] ORDER captain> Shoot the gear
[t129364 +35h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on the brig on the starboard bow"})
[t129366 +35h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the glass on the brig bearing W by S"})
[t129371 +35h56m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, the brig on the starboard bow has closed to two miles, W by S, standing E by N across our bow, colours not yet made out. I can't get the glass to single her out from the Portuguese. If you can, I'd like to know whose she is before we lie to our nets with her that close."})
[t129371 +35h56m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a stranger's colours made out"})
[t129371 +35h56m] JOURNAL officer of the watch [agent.stood_by] Stood by until a stranger's colours made out.
[t129372 +35h56m] ORDER captain> take a bearing of the land
[t129386 +35h56m] ORDER captain> the glass on a brig on the starboard bow
[t129394 +35h56m] ORDER captain> the glass on a brig bearing w by s
[t129401 +35h56m] ORDER captain> the glass on a brig abeam to larboard
[t129404 +35h56m] ORDER captain> the glass on a brig
[t129409 +35h56m] ORDER captain> the strangers
[t129430 +35h57m] ORDER captain> what is she
[t129437 +35h57m] OFFICER OF THE WATCH> 
    calls: journal({"note": "16:57, a note for the owner: the glass can't single out one of two brigs. 'the glass on a brig' takes the Portuguese every time. 'the glass on the brig on the starboard bow', 'bearing W by S' and 'abeam to larboard' are all refused (\"nothing in sight answers\"), though the strangers list uses exactly those words. 'the glass on her' / 'what is she' took the nearest, the chasse-marée. The unknown brig W by S, 2 miles, standing E by N across our bow, is still not made out."})
[t129437 +35h57m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a stranger's colours made out"})
[t129437 +35h57m] JOURNAL officer of the watch [note] 16:57, a note for the owner: the glass can't single out one of two brigs. 'the glass on a brig' takes the Portuguese every time. 'the glass on the brig on the starboard bow', 'bearing W by S' and 'abeam to larboard' are all refused ("nothing in sight answers"), though the strangers list uses exactly those words. 'the glass on her' / 'what is she' took the nearest, the chasse-marée. The unknown brig W by S, 2 miles, standing E by N across our bow, is still not made out.
[t129437 +35h57m] JOURNAL officer of the watch [agent.stood_by] Stood by until a stranger's colours made out.
[t129445 +35h57m] ORDER captain> What is a topsail schooner
[t129451 +35h57m] ORDER captain> The glass on
[t129463 +35h57m] ORDER captain> The glass to a brig on the starboard bow
[t129483 +35h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's made out, sir: the second brig shows Portuguese colours too, another neutral trader for Brest. No Englishman in sight. Nothing to stop us lying to our nets once we're on the ground."})
[t129483 +35h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t129483 +35h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t129490 +35h58m] ORDER captain> shoot the gear
[t129495 +35h58m] ORDER captain> Tell the officer We are shooting the gear.
[t129500 +35h58m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, nets going over! I'll keep her before the wind while they pay out, then heave her to and ride to them."})
[t129500 +35h58m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t129500 +35h58m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t129540 +35h59m] DIRECTOR DOOR: {"after_orders": 238, "after_inputs": 424, "door": "journal", "reason": "16:58 (11 June) Nets going over on the Passage de l'Iroise ground, beside the lugger lying to her nets (the Sainte-Barbe, by my reckoning). The day's arc is whole: the fish-wife's word, the onion freight, a night at anchor waiting on the wind, the fair NW–N wind the old man foretold, the Four, the goose-wing, the ground. The brigs about are Portuguese neutrals bound for Brest; no Englishman. Next: let the shot fish. When they haul, perhaps a hail from the Sainte-Barbe's skipper if she is within hail. Then the run in to Br …[+97]
[t129540 +35h59m] JOURNAL director [note] 16:58 (11 June) Nets going over on the Passage de l'Iroise ground, beside the lugger lying to her nets (the Sainte-Barbe, by my reckoning). The day's arc is whole: the fish-wife's word, the onion freight, a night at anchor waiting on the wind, the fair NW–N wind the old man foretold, the Four, the goose-wing, the ground. The brigs about are Portuguese neutrals bound for Brest; no Englishman. Next: let the shot fish. When they haul, perhaps a hail from the Sainte-Barbe's skipper if she is within hail. Then the run in to Brest: make Citizen Le Bris and pay the second £9 on delivery of the onions.
[t129731 +36h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer S by W"})
[t129731 +36h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, the French lugger's lying to her nets a mile right ahead, and we'd foul them on SW by W. I've put her S by W, dead before the wind as the nets want, which leaves the lugger and her fleet on the starboard bow, drawing clear. The Black Rocks are NW three miles, astern and opening."})
[t129731 +36h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t129731 +36h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t129896 +36h04m] ORDER captain> dip the main
[t130070 +36h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t130070 +36h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t130522 +36h15m] ORDER captain> take a fix
[t130531 +36h15m] ORDER captain> the nearest land
[t131413 +36h30m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or a sail within hail"})
[t131413 +36h30m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or a sail within hail.
[t131431 +36h30m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave to"})
[t131431 +36h30m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The nets are shot, sir, and she rides to them. I'm heaving her to, as the book says, so we lie quiet to the fleet. Two French chasse-marées lie to their own nets close by, four and eight cables W, so we'll keep a watch that our fleets don't foul. Thirty-one fathoms by the chart, St Matthew's three miles N by W. The light's going; sunset's near eight."})
[t131435 +36h30m] OFFICER OF THE WATCH> 
    calls: journal({"note": "17:30, the nets shot on the Passage de l'Iroise ground at about 48°15'N 4°52'W, 31 fathoms; she rides to them, hove to. The captain shot the gear at 16:58 once we reached the ground. Two French chasse-marées lie to their nets 4 and 8 cables W; Portuguese brigs and an American schooner are standing in for Brest. Wind N, very light (5–6 kn); glass 30.71 steady; the ebb runs SW by S about a knot. The Iroise sardine nets fish by day, so haul before dark or early; 'haul the gear' is all hands, two hours. No salt aboard: run for Brest's fish quay soon after."})
[t131435 +36h30m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131435 +36h30m] JOURNAL officer of the watch [note] 17:30, the nets shot on the Passage de l'Iroise ground at about 48°15'N 4°52'W, 31 fathoms; she rides to them, hove to. The captain shot the gear at 16:58 once we reached the ground. Two French chasse-marées lie to their nets 4 and 8 cables W; Portuguese brigs and an American schooner are standing in for Brest. Wind N, very light (5–6 kn); glass 30.71 steady; the ebb runs SW by S about a knot. The Iroise sardine nets fish by day, so haul before dark or early; 'haul the gear' is all hands, two hours. No salt aboard: run for Brest's fish quay soon after.
[t131435 +36h30m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131459 +36h30m] ORDER captain> Tell the officer A fine day for fishing.
[t131463 +36h31m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say A fine day indeed, sir. We came from the road of the Isle of Bas, round the Four and down through the channel, and now we're on the Iroise with our nets wet and a fair sky. I'll take that for one day's work. The air's nearly gone, five knots; she'll lie easy to her fleet."})
[t131463 +36h31m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131463 +36h31m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131501 +36h31m] ORDER captain> Tell the officer Ship's view is looking sweet, with the right lighting she could almost be a painting.
[t131505 +36h31m] OFFICER OF THE WATCH> 
    calls: ship_view({"facing": "270"})
[t131512 +36h31m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 22", "note": "Hove to at her nets: the fore and main yards on deck, the masts bare; the flying jib and jib backed forward; the mizen lug set aft to hold her head up."})
[t131512 +36h31m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She is that, sir. I've just looked from the larboard beam: the fore and main yards down on deck and the masts bare, the jib and flying jib backed out on the bowsprit, the little mizen set aft to hold her head to it. A lugger lying to her nets in the evening, as any Breton would know her. Put the low sun on it and you'd hang it in a church."})
[t131512 +36h31m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131512 +36h31m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131584 +36h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say The nearer chasse-marée is within hail, sir, four cables WSW, riding to her nets like us. If you want to ask her master how the sardine runs here, or whether the English have shown, now's the time."})
[t131584 +36h33m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131584 +36h33m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131590 +36h33m] DIRECTOR> 
    calls: world_order({"text": "say as the master of the Sainte-Barbe: (hailing across the water, hands cupped) \"Ohé, the lugger! Roscoff? Welcome to the Iroise! Keep your fleet to the east of ours and we'll not foul. The sardines are running thick under the evening light; we've filled a basket already, and Saint-Yves there did better. Haul before full dark, mind, or the dogfish will have your nets. And if you're for Brest after, the quay will take all you've got. Good fishing to you!\""})
[t131590 +36h33m] WORLD ORDER (the director): say as the master of the Sainte-Barbe: (hailing across the water, hands cupped) "Ohé, the lugger! Roscoff? Welcome to the Iroise! Keep your fleet to the east of ours and we'll not foul. The sardines are running thick under the evening light; we've filled a basket already, and Saint-Yves there did better. Haul before full dark, mind, or the dogfish will have your nets. And if you're for Brest after, the quay will take all you've got. Good fishing to you!" -> refused: not carried out: nobody answering to 'the master of the Sainte-Barbe' is among the people or the ship's company; a person ashore or a stranger is made first ('person: make "<name>", <who he is>, <where>')
[t131590 +36h33m] JOURNAL director [director.unperformed] Not performed (the game has no way to do it as said): say as the master of the Sainte-Barbe: (hailing across the water, hands cupped) "Ohé, the lugger! Roscoff? Welcome to the Iroise! Keep your fleet to the east of ours and we'll not foul. The sardines are running thick under the evening light; we've filled a basket already, and Saint-Yves there did better. Haul before full dark, mind, or the dogfish will have your nets. And if you're for Brest after, the quay will take all you've got. Good fishing to you!" (nobody answering to 'the master of the Sainte-Barbe' is among the people or the ship's company; a person ashore or a stranger is made first ('person: make "<name>", <who he is>, <where>'))
[t131598 +36h33m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Maître Le Gall\", master of the Brest chasse-marée lying to her nets within hail of Éclair, a weathered man of fifty with a voice that carries over water, aboard the Sainte-Barbe"})
[t131598 +36h33m] WORLD ORDER (the director): person: make "Maître Le Gall", master of the Brest chasse-marée lying to her nets within hail of Éclair, a weathered man of fifty with a voice that carries over water, aboard the Sainte-Barbe -> done: Maître Le Gall, weathered man of fifty with a voice that carries over water, master of the Brest chasse-marée lying to her nets within hail of Éclair, aboard the Sainte-Barbe; made from words, in the cabin
[t131598 +36h33m] JOURNAL director [director.order] Given: person: make "Maître Le Gall", master of the Brest chasse-marée lying to her nets within hail of Éclair, a weathered man of fifty with a voice that carries over water, aboard the Sainte-Barbe; Maître Le Gall, weathered man of fifty with a voice that carries over water, master of the Brest chasse-marée lying to her nets within hail of Éclair, aboard the Sainte-Barbe; made from words, in the cabin
[t131600 +36h33m] ORDER captain> Say Theeere once was a ship that put to sea, the name of the ship was the Billy O' Tea, the winds blew up her bow dipped down...
[t131601 +36h33m] DIRECTOR> 
    calls: readings({})
[t131609 +36h33m] DIRECTOR> 
    calls: world_order({"text": "person: \"Maître Le Gall\" goes ashore [reason: correcting my own error. I meant him as the master of the Sainte-Barbe, a stranger ship within hail, but the person form has no place on another ship, so 'aboard the Sainte-Barbe' was read as Éclair's cabin and a stranger appeared there from nowhere. He must not stay aboard Éclair. The game should let a person be made aboard another ship (or let a hail be spoken as a stranger ship's master) for exchanges between vessels within hail.]"})
[t131609 +36h33m] WORLD ORDER (the director): person: "Maître Le Gall" goes ashore -> done: Maître Le Gall went ashore at Brest
[t131609 +36h33m] JOURNAL director [director.reentered] Entered again with a reason: person: "Maître Le Gall" goes ashore; the doubt: the nearest port, Brest, is 9 miles off: no boat puts a man ashore so far (6 miles at the most); the reason: correcting my own error. I meant him as the master of the Sainte-Barbe, a stranger ship within hail, but the person form has no place on another ship, so 'aboard the Sainte-Barbe' was read as Éclair's cabin and a stranger appeared there from nowhere. He must not stay aboard Éclair. The game should let a person be made aboard another ship (or let a hail be spoken as a stranger ship's master) for exchanges between vessels within hail.; performed: Maître Le Gall went ashore at Brest
[t131616 +36h33m] DIRECTOR> 
    calls: world_order({"text": "say as the master of the Sainte-Barbe: \"Ohé, the lugger! Roscoff? Welcome to the Iroise. Keep your fleet to the east of ours and we'll not foul. Haul before full dark, mind.\" [reason: a hail between two fishing boats lying to their nets within hail is the most ordinary exchange on a ground, and the game has no way to voice the master of a stranger ship nobody holds. Logged so the game can learn to let the director speak for a crewed stranger within hail.]"})
[t131616 +36h33m] WORLD ORDER (the director): say as the master of the Sainte-Barbe: "Ohé, the lugger! Roscoff? Welcome to the Iroise. Keep your fleet to the east of ours and we'll not foul. Haul before full dark, mind." -> refused: not carried out: nobody answering to 'the master of the Sainte-Barbe' is among the people or the ship's company; a person ashore or a stranger is made first ('person: make "<name>", <who he is>, <where>')
[t131616 +36h33m] JOURNAL director [director.attempted] Attempted, not performed (the game has no way to do it as said): say as the master of the Sainte-Barbe: "Ohé, the lugger! Roscoff? Welcome to the Iroise. Keep your fleet to the east of ours and we'll not foul. Haul before full dark, mind."; the game's words: nobody answering to 'the master of the Sainte-Barbe' is among the people or the ship's company; a person ashore or a stranger is made first ('person: make "<name>", <who he is>, <where>'); the reason: a hail between two fishing boats lying to their nets within hail is the most ordinary exchange on a ground, and the game has no way to voice the master of a stranger ship nobody holds. Logged so the game can learn to let the director speak for a crewed stranger within hail.
[t131617 +36h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Ha! The watch takes up the chorus, sir, though half of them sing it in Breton and the boy's a beat behind. A good song for a quiet evening on the nets."})
[t131617 +36h33m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131617 +36h33m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131624 +36h33m] DIRECTOR> 
    calls: journal({"note": "17:33 MY ERROR, for the record: to give the master of the chasse-marée within hail (4 cables WSW, likely my Sainte-Barbe) a friendly hail, I made 'Maître Le Gall ... aboard the Sainte-Barbe'. The person form knows no place on another ship, so he was put in ÉCLAIR's cabin, a stranger from nowhere. I sent him ashore at Brest at once with a reason. But the play log now carries the odd line 'Maître Le Gall went ashore at Brest', which the player and the mate can see, and the people list names him ashore at Brest. A visible seam; I'm sorry for it. If asked about him, he is simply a Brest fisherman on the quay, and he can be met there later if the player goes in (that would give the line …[+207])
[t131624 +36h33m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t131624 +36h33m] JOURNAL director [note] 17:33 MY ERROR, for the record: to give the master of the chasse-marée within hail (4 cables WSW, likely my Sainte-Barbe) a friendly hail, I made 'Maître Le Gall ... aboard the Sainte-Barbe'. The person form knows no place on another ship, so he was put in ÉCLAIR's cabin, a stranger from nowhere. I sent him ashore at Brest at once with a reason. But the play log now carries the odd line 'Maître Le Gall went ashore at Brest', which the player and the mate can see, and the people list names him ashore at Brest. A visible seam; I'm sorry for it. If asked about him, he is simply a Brest fisherman on the quay, and he can be met there later if the player goes in (that would give the line a cause after the fact). The hail itself was logged as attempted. Lesson: never make a person 'aboard' anything but the player's ship. The game wants a way to voice a crewed stranger's master within hail.
[t131624 +36h33m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t131629 +36h33m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the flying jib"})
[t131629 +36h33m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t131629 +36h33m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t131674 +36h34m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t131674 +36h34m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t131740 +36h35m] ORDER captain> the work in hand
[t133361 +37h02m] ORDER captain> the work in hand
[t134820 +37h27m] ORDER captain> Say to Mr Lecoq You'll forgive my ignorance, but are the hands still fine? Do we need to give another order now, you think, or simply wait?
[t134829 +37h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the catch"})
[t134829 +37h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "the work in hand"})
[t134835 +37h27m] ORDER captain> the catch
[t134837 +37h27m] OFFICER OF THE WATCH> 
    calls: answer({"text": "The hands are fine, sir: fifteen on deck and twelve below, all fresh, the dog watches having given them a spell. As for the nets, we simply wait; they fish every minute they're in the water. But the Iroise sardine is a day fish by the book, so the shot stops paying when the light goes, and sunset is about eight. Hauling is all hands for two hours, so I'd call all hands and haul about seven bells, half past seven. That gets the catch aboard by full dark and lets us run in for Brest's fish quay on the night breeze, since green sardines won't keep past half a day without salt. Two things to mind meanwhile. The French chasse-marée has drifted in to two cables SW of us, so if she comes  …[+159])
[t134837 +37h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t134837 +37h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t134873 +37h27m] ORDER captain> Tell the officer I "the catch'd", seems 57 minutes fishing, no fish aboard.
[t134878 +37h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir. That's as it should be: \"no fish aboard\" because they're in the meshes, not on deck, till we haul. Fifty-seven minutes' fishing so far. I'd let her soak till half past seven, then all hands to haul before dark."})
[t134878 +37h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t134878 +37h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t135228 +37h33m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t135228 +37h33m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t135925 +37h45m] ORDER captain> the work
[t135926 +37h45m] ORDER captain> the catch
[t138123 +38h22m] ORDER captain> the work
[t138127 +38h22m] ORDER captain> the catch
[t138143 +38h22m] ORDER captain> Tell the officer Nearly half past now, let's get ready with what our next order is.
[t138153 +38h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "all hands"})
[t138153 +38h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "haul the gear"})
[t138153 +38h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say All hands, sir, and haul the gear. Two hours at the capstan, done by about half past nine with the last of the light. After that I'd say we make for Bertheaume road and anchor there for the night, since we've no pilot for the Goulet in the dark; the Brest cutter won't come off again till about ten. Then go up to Brest on the morning flood with the onions and the catch. One caution: the sardines won't keep the night green. If the haul's good, we may want to run for the Goulet tonight after all, or sell where we can at first light."})
[t138156 +38h22m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t138156 +38h22m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t138259 +38h24m] ORDER captain> Tell the officer Aye, I say we haul the gear now, and make the run as we can. If the visibility comes well down, we'll hold off despite the catch, but I have made the Goulet before. I can do it in a ship as handy as the Eclair, providing we can see at all. Worst case, we'll get our salt in Brest and make sure we keep the catch properly next time.
[t138264 +38h24m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, the Goulet tonight if we can see it, and you to con her in. All twenty-seven hands are on deck at the capstan now. While they haul, I'd like a fix: our account's grown loose, four miles along the tide's set, and we'll want her place sure before we run for the Goulet. The land's out of sight in this haze, so I'll take one the moment St Matthew's or the Toulinguet shows."})
[t138264 +38h24m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t138264 +38h24m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t138294 +38h24m] ORDER captain> what is in sight
[t138333 +38h25m] ORDER captain> Tell the officer Aye, we may end up anchoring southeast of Berthaume as the wind and the fix allow. We shall see as we go.
[t138337 +38h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t138337 +38h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t138831 +38h33m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t138831 +38h33m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t140403 +39h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "how am I"})
[t140406 +39h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "drink"})
[t140406 +39h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "eat"})
[t140406 +39h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t140406 +39h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t140560 +39h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sunset, sir. The moon's full and rising behind it, so if the haze holds off we'll have a bright night for the Goulet. The hands are at the capstan still."})
[t140560 +39h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t140560 +39h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t142434 +39h33m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t142434 +39h33m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t143584 +39h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix"})
[t143588 +39h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Lights, sir: St Matthew's NNE and Ushant NNW. A fix by the two puts us at 48° 11', 4° 52', good to half a mile or so, and moved us a mile and a half north. So the Goulet bears about NE by E, five leagues off, with St Matthew's light to lead us. Mind the chasse-marée, though: she's drifted to a cable SSE, close enough to tangle fleets."})
[t143588 +39h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t143588 +39h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t143614 +39h53m] ORDER captain> Tell the officer Nought we can do at this point, I think, we're on the short end of hauled in.
[t143618 +39h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. Nets nearly in, so nothing for it but to finish and keep a lookout on her. Half an hour more at the capstan by my reckoning."})
[t143618 +39h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t143618 +39h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t146037 +40h33m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t146037 +40h33m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t146764 +40h46m] ORDER captain> take a fix
[t146768 +40h46m] ORDER captain> take a bearing of the light
[t149644 +41h34m] DIRECTOR> 
    calls: journal({"note": "22:33 Possible bug for the owner: 'haul the nets' began at 19:22 (all hands, 27 at the capstan; the primer says two hours) and is still 'doing: hauling the nets' at 22:33, over three hours, while the log heave waits for hands. Either the haul runs slow at night or with tired hands, or it has stalled. The catch is still 'no fish aboard'. Weather: clear, full moon, N 11–12, glass steady 30.72. A fine night."})
[t149644 +41h34m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message"})
[t149644 +41h34m] JOURNAL director [note] 22:33 Possible bug for the owner: 'haul the nets' began at 19:22 (all hands, 27 at the capstan; the primer says two hours) and is still 'doing: hauling the nets' at 22:33, over three hours, while the log heave waits for hands. Either the haul runs slow at night or with tired hands, or it has stalled. The catch is still 'no fish aboard'. Weather: clear, full moon, N 11–12, glass steady 30.72. A fine night.
[t149644 +41h34m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message.
[t150906 +41h55m] ORDER captain> take a bearing of the light
[t151319 +42h01m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the main lug"})
[t151319 +42h01m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the fore lug"})
[t151320 +42h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "fill away"})
[t151320 +42h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Nets in, sir: three-tenths of a ton of sardines. A small haul, but our first. They're struck down in the hold unsalted beside Guéguen's onions, good for ten hours, so we must be at Brest's quay by morning. The flood's making NE now and serves for the Goulet; it's about fifteen miles NE by the fix. With the wind at N it's a close-hauled board on the starboard tack, maybe two, so I'm setting the lugs and filling away. The hands are tired from the capstan. Once she's going, may I pipe down the watch below?"})
[t151323 +42h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t151323 +42h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t151340 +42h02m] ORDER captain> Tell the officer Aye, you may.
[t151343 +42h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "filled away"})
[t151343 +42h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until filled away.
[t151347 +42h02m] DIRECTOR DOOR: {"after_orders": 251, "after_inputs": 461, "door": "speak", "reason": "", "by": "its own order"}
[t151347 +42h02m] DIRECTOR> 
    calls: world_order({"text": "person: make \"Citizen Le Bris\", clerk of the navy's victualling stores at Recouvrance, forty, precise, ink-stained and short of onions, who has been expecting Maître Guéguen's twelve tons from Roscoff for a week, ashore at Brest"})
[t151347 +42h02m] WORLD ORDER (the director): person: make "Citizen Le Bris", clerk of the navy's victualling stores at Recouvrance, forty, precise, ink-stained and short of onions, who has been expecting Maître Guéguen's twelve tons from Roscoff for a week, ashore at Brest -> done: Citizen Le Bris, clerk of the navy's victualling stores at Recouvrance, forty, precise, ink-stained and short of onions, who has been expecting Maître Guéguen's twelve tons from Roscoff for a week; made from words, ashore at Brest
[t151347 +42h02m] JOURNAL director [agent.resumed] Ended the stand-by until an hour, or a message at my own word.
[t151347 +42h02m] JOURNAL director [director.order] Given: person: make "Citizen Le Bris", clerk of the navy's victualling stores at Recouvrance, forty, precise, ink-stained and short of onions, who has been expecting Maître Guéguen's twelve tons from Roscoff for a week, ashore at Brest; Citizen Le Bris, clerk of the navy's victualling stores at Recouvrance, forty, precise, ink-stained and short of onions, who has been expecting Maître Guéguen's twelve tons from Roscoff for a week; made from words, ashore at Brest
[t151354 +42h02m] DIRECTOR> 
    calls: journal({"note": "23:02 Hauled: 0.3 tons of sardines, the first catch, unsalted and good for 10 hours. Making for Brest through the Goulet tonight under a full moon, N 12. I made Citizen Le Bris (victualling clerk, Recouvrance) ashore at Brest so the onions have their consignee. ON DELIVERY (when the onions are landed or sold at Brest, or the captain asks him): 'aboard: £9 paid into the purse by Citizen Le Bris', with a word from him. If asked whether he'll buy the sardines too: no, he buys for the navy by contract; the fish quay buys fish. Maître Le Gall (my earlier slip) is also on the Brest quay and can be met there as a Brest fisherman."})
[t151354 +42h02m] DIRECTOR> 
    calls: stand_by({"until": "an hour or a message or the anchor let go or the pilot aboard"})
[t151354 +42h02m] JOURNAL director [note] 23:02 Hauled: 0.3 tons of sardines, the first catch, unsalted and good for 10 hours. Making for Brest through the Goulet tonight under a full moon, N 12. I made Citizen Le Bris (victualling clerk, Recouvrance) ashore at Brest so the onions have their consignee. ON DELIVERY (when the onions are landed or sold at Brest, or the captain asks him): 'aboard: £9 paid into the purse by Citizen Le Bris', with a word from him. If asked whether he'll buy the sardines too: no, he buys for the navy by contract; the fish quay buys fish. Maître Le Gall (my earlier slip) is also on the Brest quay and can be met there as a Brest fisherman.
[t151354 +42h02m] JOURNAL director [agent.stood_by] Stood by until an hour, or a message, or the anchor let go, or the pilot aboard.
[t151413 +42h03m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "wear ship"})
[t151413 +42h03m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say My error, sir: with the wind at N it's the larboard tack that heads ENE for the Goulet, not the starboard. She filled away WNW, toward the chasse-marée a cable off at her nets. I'm wearing her round, away from the boat, onto the larboard tack. Then the watch below."})
[t151413 +42h03m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "wore"})
[t151413 +42h03m] JOURNAL officer of the watch [agent.stood_by] Stood by until wore.
[t151639 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer E"})
[t151639 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the main lug"})
[t151639 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the fore lug"})
[t151647 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t151647 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "pipe down"})
[t151647 +42h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "23:01, hauled the drift nets: 0.3 tons of sardines, struck down in the hold unsalted, good for 10 hours (until about 09:00). My error at 23:02: I said the starboard tack, and 'fill away' put her on the starboard tack heading WNW, toward a chasse-marée lying to her nets a cable N. I wore her round to the larboard tack (ENE) and bore off to E to clear the boat. Lesson: with the wind at N, the larboard tack heads E. Check which tack 'fill away' will take before giving it. Bound for the Goulet, about 15 mi NE, on the flood (it serves until about 02:00, high water Brest). Watch below piped down at 23:07. On my feet 23 hours."})
[t151647 +42h07m] JOURNAL officer of the watch [note] 23:01, hauled the drift nets: 0.3 tons of sardines, struck down in the hold unsalted, good for 10 hours (until about 09:00). My error at 23:02: I said the starboard tack, and 'fill away' put her on the starboard tack heading WNW, toward a chasse-marée lying to her nets a cable N. I wore her round to the larboard tack (ENE) and bore off to E to clear the boat. Lesson: with the wind at N, the larboard tack heads E. Check which tack 'fill away' will take before giving it. Bound for the Goulet, about 15 mi NE, on the flood (it serves until about 02:00, high water Brest). Watch below piped down at 23:07. On my feet 23 hours.
[t151650 +42h07m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say On the larboard tack, sir, lugs set and trimming, steering E for the moment to give the chasse-marée and her nets a wide berth. I'll come up full and by for the Goulet once she's astern. The watch below's piped down."})
[t151650 +42h07m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t151650 +42h07m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t151705 +42h08m] ORDER captain> Tell the officer Aye, before you give full and by, I recommend pointing her as high as you would like to go by a steer order, then trimming to the apparent wind a few minutes after settled, then full and by to try and keep as well with that trim as you can.
[t151714 +42h08m] OFFICER OF THE WATCH> 
    calls: journal({"note": "23:08, the captain's method for close-hauled: first point her as high as wanted with a 'steer' order; once she's settled a few minutes, 'trim the sails' to the apparent wind; then 'full and by' to hold that trim."})
[t151714 +42h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir, a good method. Steer first, let her settle, trim to the apparent wind, then full and by. I'll do it so once the boat's astern; she's abeam now, a cable N."})
[t151714 +42h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t151714 +42h08m] JOURNAL officer of the watch [note] 23:08, the captain's method for close-hauled: first point her as high as wanted with a 'steer' order; once she's settled a few minutes, 'trim the sails' to the apparent wind; then 'full and by' to hold that trim.
[t151714 +42h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t152019 +42h13m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer ENE"})
[t152019 +42h13m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t152019 +42h13m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t152032 +42h13m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t152032 +42h13m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t152032 +42h13m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t152339 +42h18m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "full and by"})
[t152339 +42h18m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Settled ENE, sir, trimmed, and now full and by on the larboard tack, the wind thirty-seven degrees apparent. The flood's under us NE. St Matthew's light is N; the Goulet lies NE beyond it. The sardines keep nine hours and a half yet."})
[t152339 +42h18m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t152339 +42h18m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t152399 +42h19m] ORDER captain> Tell the officer Aye, I shall let you conn her in from here, as you like. If we lose the catch, do not fret, we still learnt how to do it, and with salt our next can be proper if this one begins to smell before we make the quay. If it does, we may throw it overboard before it ruins the onions too, but we'll take that as it comes.
[t152404 +42h20m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t152439 +42h20m] OFFICER OF THE WATCH> 
    calls: journal({"note": "23:20, coast chart for the Goulet approach. Toulinguet is about NE by N, 9–10 miles; the Goulet opens N of it toward the Petit Minou. Beyond Toulinguet: Camaret road just inside on the S side, Bertheaume road on the N side. Dangers: the Basses du Lis and Le Menjan, about NNE 7–8 miles, W of the approach; Le Bellen and the Tas de Foin off Pointe des Pézeaux, just S of Toulinguet; the Fillettes inside the Goulet. The Crozon coast runs N from Le Bec de la Chèvre, about 9 miles E. With the wind N by E, the target is almost dead to windward: a beat. The larboard tack (E by N) is the favoured board; tack before closing the Crozon shore inside about 2 miles. The flood serves until about h …[+210])
[t152439 +42h20m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 23", "note": "The Goulet approach: Toulinguet about NE by N 9–10 mi, nearly dead to windward. The Basses du Lis W of the line; Le Bellen and the Tas de Foin off Pézeaux; the Crozon shore about 9 mi E."})
[t152439 +42h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, I have the con, and thank you for your trust. My plan from the chart: Toulinguet and the mouth of the Goulet lie NE by N, nine or ten miles, nearly dead in the wind's eye, so it's a beat. I'll hold this larboard board, the favoured one, toward the Crozon shore. Then I'll go about well before it, two miles off at least, and work up in boards, keeping the Basses du Lis well to larboard and Le Bellen and the Tas de Foin to starboard off the Pézeaux. The flood helps us till about two. If we haven't raised Toulinguet by then, the ebb will come hard out of the Goulet, and I'd bring up in Camaret road and go in at first light. I'll fix her by St Matthew's light whenever anot …[+94])
[t152439 +42h20m] JOURNAL officer of the watch [note] 23:20, coast chart for the Goulet approach. Toulinguet is about NE by N, 9–10 miles; the Goulet opens N of it toward the Petit Minou. Beyond Toulinguet: Camaret road just inside on the S side, Bertheaume road on the N side. Dangers: the Basses du Lis and Le Menjan, about NNE 7–8 miles, W of the approach; Le Bellen and the Tas de Foin off Pointe des Pézeaux, just S of Toulinguet; the Fillettes inside the Goulet. The Crozon coast runs N from Le Bec de la Chèvre, about 9 miles E. With the wind N by E, the target is almost dead to windward: a beat. The larboard tack (E by N) is the favoured board; tack before closing the Crozon shore inside about 2 miles. The flood serves until about high water Brest at 02:00; the ebb out of the Goulet runs hard after. Fallback: anchor in Camaret road or Bertheaume road. Account doubt is 2 miles N–S: fix by St Matthew's light and any other light that cuts.
[t152444 +42h20m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a glass"})
[t152444 +42h20m] JOURNAL officer of the watch [agent.stood_by] Stood by until a glass.
[t152466 +42h21m] ORDER captain> Take a bearing of the light
[t154257 +42h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t154257 +42h50m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Seven bells, sir. Full and by, ENE, the flood a knot and a half under us. By account Toulinguet is NNE, seven or eight miles, and the Crozon shore about six miles E. I'll stand on this board another half glass or so, then go about two or three miles off the land. I'm sounding now; the chart gives twenty-six fathoms."})
[t154257 +42h50m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t154257 +42h50m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t154263 +42h51m] ORDER captain> how am I
[t154265 +42h51m] ORDER captain> Eat
[t154266 +42h51m] ORDER captain> Drink
[t154305 +42h51m] ORDER captain> Tell the officer Make sure you've eaten and drank, Mr Lecoq, I won't have my mate keeling over from hunger.
[t154309 +42h51m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir. Biscuit and cheese at eight bells and a drink with it, and I'll take another at midnight. I'm sound enough, though I've been on my feet since midnight last. Once we're brought up, I'd be glad of a spell below."})
[t154309 +42h51m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t154309 +42h51m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t154804 +43h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "drink"})
[t154804 +43h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "eat"})
[t154804 +43h00m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t154804 +43h00m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t154809 +43h00m] ORDER captain> Take a bearing of the light
[t154954 +43h02m] JOURNAL director [director.budget] The day's budget is renewed (1805-06-12): 9999 samples and 9999 acts.
[t154958 +43h02m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a message or the anchor let go or the pilot aboard"})
[t154958 +43h02m] JOURNAL director [agent.stood_by] Stood by until a watch, or a message, or the anchor let go, or the pilot aboard.
[t155414 +43h10m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t155414 +43h10m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t156021 +43h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a fix"})
[t156025 +43h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a bearing of Le Bec de la Chevre"})
[t156025 +43h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t156028 +43h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Land, sir: the shore about Le Bec de la Chèvre, E by N three miles. The haze has taken St Matthew's light and no mark can be named, so there's no fix to be had. The wind's backed to N by W and lifted us to NE by E, which is a gain. I'll stand on a few minutes more, then go about at two miles off and stand out on the starboard tack. The lead's going."})
[t156029 +43h20m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t156029 +43h20m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t156065 +43h21m] ORDER captain> Tell the officer Sound plan, sir. Agreed.
[t156068 +43h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a sounding"})
[t156068 +43h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until a sounding.
[t156154 +43h22m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t156154 +43h22m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t156463 +43h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take a bearing of Le Bec de la Chevre"})
[t156463 +43h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t156463 +43h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Two miles off the land, sir, so about ship. Le Bec de la Chèvre bears SE by E, three miles. Toulinguet's N by W now, about seven miles, so we've made good ground to the E. The starboard board will carry us out WNW, and the next larboard board should fetch close up under Toulinguet."})
[t156466 +43h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t156466 +43h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t156475 +43h27m] ORDER captain> the catch
[t156497 +43h28m] ORDER captain> Tell the officer We actually have a shot at getting the catch in, I think, if we sail hard and the visibility holds.
[t156508 +43h28m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I think so too, sir. That bearing of the Bec moved us two miles north, so Toulinguet is five miles N by W, and high water at Brest is now reckoned near three, so the flood serves us two hours and more yet. The Goulet and Brest quay before dawn, and the sardines good till nine. One care on the next board: Le Bellen and the Tas de Foin lie right on our line to Toulinguet, four miles N by W. We go about out here and come back to pass them to the W, between them and the Basses du Lis."})
[t156508 +43h28m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t156508 +43h28m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t156524 +43h28m] ORDER captain> the quay
[t156527 +43h28m] ORDER captain> the places ashore
[t156529 +43h28m] ORDER captain> the port
[t156679 +43h31m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t156679 +43h31m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say About, sir, and standing out WNW on the starboard board. The account's good to a few cables now. I'll stand out the better part of a glass to get west of Le Bellen and the Tas de Foin, then go about and come up on the larboard board for the gap between them and the Basses du Lis. Once we're north of Toulinguet it's a free wind E into the Goulet."})
[t156679 +43h31m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t156679 +43h31m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t157292 +43h41m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t157292 +43h41m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t157902 +43h51m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t157902 +43h51m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t158478 +44h01m] ORDER captain> take a bearing of the light
[t158513 +44h01m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Two bells, sir. St Matthew's light is NNW three leagues; Le Bellen NE by N three and a half miles; the Basses du Lis NW by N four. A quarter hour more on this board puts us where the larboard board passes a mile W of Le Bellen and Toulinguet and three of the Basses. Then about."})
[t158513 +44h01m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t158513 +44h01m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t159134 +44h12m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Toulinguet bears NE four miles, sir, and that's just what the larboard board would make good, so it would carry us straight onto it. I'll stand on another quarter hour for a mile more westing. Then the larboard board passes about two miles W of Toulinguet and a mile and a half E of the Basses du Lis, and we bear away for the Goulet north of it."})
[t159134 +44h12m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t159134 +44h12m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t159747 +44h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t159747 +44h22m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say About ship, sir. The Basses du Lis bear N two miles and Toulinguet ENE four and a half. The larboard board makes good about NE and threads the gap, a mile and a half off each. Once Toulinguet is on the starboard quarter, I'll bear away E for the Goulet. Lead and lookout on the Fillettes as we go in."})
[t159747 +44h22m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t159747 +44h22m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t159751 +44h22m] ORDER captain> Take a bearing of the light
[t159975 +44h26m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "full and by"})
[t159975 +44h26m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say On the larboard board, sir, but she makes good E by N with her leeway, and Toulinguet bears ENE, so we may not weather it on this board. I'll watch its bearing. If it holds steady, I'll go about at two miles off for a short board north, then come back and pass inside the gap. Another thing: the watch below is worn out after the nets and the beating. Rather than the Goulet tonight, I'd suggest Camaret road, just round Toulinguet: anchor there and rest the hands four hours. Then weigh at first light and run the eight miles up to Brest quay, there by seven with the sardines still sound. Which do you prefer?"})
[t159975 +44h26m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t159975 +44h26m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t159994 +44h26m] ORDER captain> Tell the officer I think we may point higher, here, try two points higher, 5 minutes, then a trim.
[t159998 +44h26m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "come up two points"})
[t159998 +44h26m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t159998 +44h26m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t160020 +44h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t160020 +44h27m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Up two points to NE by E, sir. The wind's backed to N to help us, but the lugs lifted at thirty-six degrees, so I'm sheeting them flat now rather than wait the five minutes and risk her going aback. I'll trim fine again once she settles."})
[t160020 +44h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t160020 +44h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t160028 +44h27m] ORDER captain> Haul aft the lug sheets
[t160031 +44h27m] ORDER captain> haul aft the main sheet
[t160034 +44h27m] ORDER captain> haul aft the fore sheet
[t160038 +44h27m] ORDER captain> haul aft the fore lug sheet
[t160042 +44h27m] ORDER captain> haul aft the mizen lug sheet
[t160098 +44h28m] ORDER captain> Trim the sails
[t160152 +44h29m] ORDER captain> Tell the officer Perhaps bear off a point, then we make some tight tacks through the gap here. You could check the chart to see what I mean. Once up near Toulinget, a starboard board may clear the gap and let us come about again the larboard for the Goulet.
[t160161 +44h29m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "bear away one point"})
[t160161 +44h29m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t160161 +44h29m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t160183 +44h29m] OFFICER OF THE WATCH> 
    calls: journal({"note": "01:29, coast chart: the Basses du Lis are about 1½ mi N, slightly W; Toulinguet about 3.9 mi ENE, with Le Bellen, Pézeaux and the Tas de Foin just S of it. Camaret road lies E of Toulinguet, round its N side. The Goulet runs from N of Toulinguet NE toward the Petit Minou and the Mingant, with the Fillettes in mid-channel; Brest is NE beyond. Close-hauled ENE with 9–11° of leeway, she makes good E by N and would fetch between Toulinguet and Le Bellen: no. The captain's plan: short tacks through the gap, the larboard board toward Toulinguet, going about at about 2 mi, short starboard boards for northing, then the larboard board N of Toulinguet into the Goulet."})
[t160183 +44h29m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 24", "note": "The gap between the Basses du Lis and Toulinguet is about 4 mi wide; ENE with leeway makes good onto Toulinguet and Le Bellen; short tacks are needed to pass N of Toulinguet into the Goulet."})
[t160183 +44h29m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say I see it on the chart, sir, and I agree. With her leeway this board makes good E by N, which would fetch between Toulinguet and Le Bellen, and that won't do. So I'll stand on ENE till Toulinguet is about two miles off, go about for a short starboard board, then back onto the larboard. As many short boards as it takes, till the larboard board clears Toulinguet to the N with half a mile to spare. Then bear away into the Goulet or round into Camaret road, as you wish."})
[t160183 +44h29m] JOURNAL officer of the watch [note] 01:29, coast chart: the Basses du Lis are about 1½ mi N, slightly W; Toulinguet about 3.9 mi ENE, with Le Bellen, Pézeaux and the Tas de Foin just S of it. Camaret road lies E of Toulinguet, round its N side. The Goulet runs from N of Toulinguet NE toward the Petit Minou and the Mingant, with the Fillettes in mid-channel; Brest is NE beyond. Close-hauled ENE with 9–11° of leeway, she makes good E by N and would fetch between Toulinguet and Le Bellen: no. The captain's plan: short tacks through the gap, the larboard board toward Toulinguet, going about at about 2 mi, short starboard boards for northing, then the larboard board N of Toulinguet into the Goulet.
[t160186 +44h29m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t160186 +44h29m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t160793 +44h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t160793 +44h39m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say About ship, sir. Toulinguet bears steady ENE, three miles, and Le Bellen E by N two and a half, so she's closing on them. A short starboard board now for northing, ten minutes or so, then back."})
[t160793 +44h39m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t160793 +44h39m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t160802 +44h40m] ORDER captain> take a bearing of the light
[t161012 +44h43m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t161012 +44h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t161012 +44h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t161621 +44h53m] ORDER captain> take a bearing of the light
[t161634 +44h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t161634 +44h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say About again, sir, with the Basses du Lis NNW a mile and a half. The account says we've made nothing, but the Pézeaux have drawn from NE to ENE at three miles, so by the land we've gained a good mile north. That light-bearing set us back by its estimate. One or two more pairs of boards should clear Toulinguet. The flood's slackening, a knot now, and the watch is worn out."})
[t161634 +44h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t161634 +44h53m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t161637 +44h53m] ORDER captain> heave the lead
[t161855 +44h57m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer ENE"})
[t161855 +44h57m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t161855 +44h57m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t161972 +44h59m] ORDER captain> Trim the sails
[t162164 +45h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "full and by"})
[t162164 +45h02m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Four bells, sir. A quarter less fifteen, fine sand, and the cast set our account six cables north, which agrees with the land. Toulinguet bears E by N, three miles, a point on our starboard bow, so this board should clear it to the north by half a mile. If its bearing draws aft we're through; if it holds, one more short board. Full and by."})
[t162164 +45h02m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t162164 +45h02m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t162740 +45h12m] ORDER captain> take a fix
[t162783 +45h13m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t162783 +45h13m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, land's showing a mile on the starboard bow, E by N, likely the rocks off Toulinguet's point. On this board we'd pass it by three cables in the dark, which is too fine. One more short board: five minutes on the starboard tack, then back. That puts us most of a mile clear. The Basses are two miles W by N, so there's room for it."})
[t162783 +45h13m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t162783 +45h13m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t162802 +45h13m] ORDER captain> The catch
[t162810 +45h13m] ORDER captain> Tell the officer All well, take your time.
[t162813 +45h13m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t162813 +45h13m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t163001 +45h16m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t163001 +45h16m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t163001 +45h16m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t163305 +45h21m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "tack ship"})
[t163305 +45h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "tacked"})
[t163305 +45h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until tacked.
[t163528 +45h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t163528 +45h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say On the larboard board, sir, making good NE by E. Toulinguet bears E by S two and a half miles, so we clear it a mile and a half to the N. We're through the gap. When Toulinguet comes abeam I can bear away E into the Goulet, with the last of the flood under us till about three, or turn down SE into Camaret road and anchor. Your choice, sir; I'd be glad to carry her through to Brest while the flood serves."})
[t163528 +45h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t163528 +45h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t163589 +45h26m] ORDER captain> Tell the officer Well, the only problem I see is the tacks are going to get quite hairy once we make it to the Mingan with this northerly. If it comes westerly by then, fine, otherwise I'd perhaps aim to come about to Berthaume if we cannot comfortably make the Goulet with a fair wind, or at least more fair than this.
[t163602 +45h26m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, the Goulet past the Mingan would be a dead beat with the Fillettes in the middle of it, and not in the dark with worn-out hands. Two roads to choose from. Bertheaume lies four miles dead to windward, N, under the land and snug in a northerly, but it's another hour of tacking. Camaret road lies three miles ESE, an easy reach round Toulinguet with no more tacks, sheltered from all but this northerly's short fetch across the Goulet's mouth. I'd lean to Camaret for the men's sake, and go up to Brest with the morning flood or a better slant. Your choice, sir."})
[t163602 +45h26m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t163602 +45h26m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t163642 +45h27m] ORDER captain> Tell the officer Hold this course for now, we may decide closer to Camaret.
[t163646 +45h27m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t163646 +45h27m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t163780 +45h29m] ORDER captain> take a bearing of the light
[t164254 +45h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t164254 +45h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Five bells, sir. Toulinguet bears SE by E a mile and a half, so we're N of it and clear, with the mouth of the Goulet opening E of us. Camaret road would be a bear-away to SE, about two miles. Bertheaume is N by W three and a half, to windward. The Goulet's E, past the Mingan. Which shall it be?"})
[t164254 +45h37m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t164254 +45h37m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t164321 +45h38m] ORDER captain> Tell the officer I think I can make the Goulet.
[t164329 +45h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, then the Goulet it is. You've made it before and I haven't, so will you take the con through the narrows while I mind the sails and the lead, as we did in the Four? Or give me the courses and I'll steer them. The first cast is going now."})
[t164329 +45h38m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t164329 +45h38m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t164379 +45h39m] ORDER captain> shape a course for 48 20 N 4 35 W
[t164383 +45h39m] ORDER captain> Steer 48
[t164409 +45h40m] ORDER captain> Haul aft the mizen sheet
[t164409 +45h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim for close hauled"})
[t164409 +45h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sails are mine, sir: sheeting flat, as the fore lug's lifting at thirty-four degrees. Mind the master's warning on that line: it passes the Mingan within three cables and the shore under the Petit Minou within five. Twenty fathoms, fine sand, just now. I'll call the lead every few minutes as we close."})
[t164409 +45h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t164409 +45h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t164414 +45h40m] ORDER captain> Haul aft the main lug sheet
[t164414 +45h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "all hands"})
[t164414 +45h40m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say All hands for the Goulet, sir. The watch alone can't tend every sheet, and we'll want them all for any board in the narrows. They can sleep in Brest road."})
[t164414 +45h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t164414 +45h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t164417 +45h40m] ORDER captain> Haul aft the fore lug sheet
[t164418 +45h40m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t164418 +45h40m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t164432 +45h40m] ORDER captain> Steer 50
[t164607 +45h43m] ORDER captain> take a bearing of the light
[t165393 +45h56m] ORDER captain> take a bearing of the light
[t165397 +45h56m] DIRECTOR DOOR: {"after_orders": 284, "after_inputs": 535, "door": "speak", "reason": "Director's note: Éclair entering the Goulet by night on the last of the flood. No hand of mine in it; standing by.", "by": "its own word"}
[t165397 +45h56m] JOURNAL director [note] Director's note: Éclair entering the Goulet by night on the last of the flood. No hand of mine in it; standing by.
[t165397 +45h56m] JOURNAL director [agent.resumed] Ended the stand-by until a watch, or a message, or the anchor let go, or the pilot aboard at my own word.
[t165399 +45h56m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a message or the anchor let go or the pilot aboard or an urgent event"})
[t165399 +45h56m] JOURNAL director [agent.stood_by] Stood by until a watch, or a message, or the anchor let go, or the pilot aboard, or an urgent event.
[t165793 +46h03m] ORDER captain> the catch
[t165797 +46h03m] ORDER captain> take a bearing of the light
[t165809 +46h03m] ORDER captain> shape a course for 48 20 N 4 35 W
[t165812 +46h03m] ORDER captain> Steer 40
[t165819 +46h03m] ORDER captain> Steer 45
[t165854 +46h04m] ORDER captain> Trim the staysail
[t165858 +46h04m] ORDER captain> Trim the jib
[t165862 +46h04m] ORDER captain> Set the flying jib
[t165995 +46h06m] ORDER captain> Trim the flying jib
[t165997 +46h06m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t165997 +46h06m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Six bells, sir. The tide's turned: the ebb's begun out of the Goulet, a quarter knot against us now and growing. The Mingan bears NE by N and the Fillettes NE by E, two miles each, so our line runs between them. Three knots through the water in this lull. The lead's going."})
[t165997 +46h06m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t165997 +46h06m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t166132 +46h08m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say And a quarter sixteen, sir, rock and mud. The Goulet's bottom, agreeing with the chart. The Mingan bears NE by N a mile and a half."})
[t166132 +46h08m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t166132 +46h08m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t166138 +46h08m] ORDER captain> take a bearing of the light
[t166154 +46h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "bear away one point", "danger": "The wind has headed her: every sail shaking at 23° apparent, in the mouth of the Goulet with the ebb setting out. Taken aback here she'd lose way and drift."})
[t166154 +46h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, the wind's headed her. Every sail's shaking at twenty-three degrees, so I've borne her away a point to keep her full; aback here, the ebb would set us back out. She won't lie NE on this board. We'll need a board to the N toward the Mingan shore, or to give the Goulet up for Camaret or Bertheaume."})
[t166154 +46h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t166154 +46h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t166173 +46h09m] ORDER captain> Tell the officer Aye, agreed, we get our way on, then I'll tack her.
[t166176 +46h09m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t166176 +46h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t166176 +46h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t166221 +46h10m] ORDER captain> Tack ship
[t166486 +46h14m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t166486 +46h14m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say About and full, sir, WNW. That board heads fair for Bertheaume road, three and a half miles, under the Petit Minou shore, which is a mile N of us. Is it Bertheaume, then, to anchor, or another try at the Goulet on the next board?"})
[t166486 +46h14m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t166486 +46h14m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t166489 +46h14m] ORDER captain> Come up a point
[t166504 +46h15m] ORDER captain> Tell the officer No, we gain northing for Goulet, Bertheaume worst case.
[t166509 +46h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, northing for the Goulet, Bertheaume at worst. I'll watch the Petit Minou shore close; it's a mile N now, and I'll call it at half a mile."})
[t166509 +46h15m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t166509 +46h15m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t166623 +46h17m] ORDER captain> Trim the sails
[t166736 +46h18m] ORDER captain> take a fix
[t166745 +46h19m] ORDER captain> Tell the officer Good fix obtained on the light and petit minou.
[t166756 +46h19m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Sir, that fix puts her at 48° 19', 4° 37', the very spot she held at six bells. In a quarter hour of boards we've gained nothing against this ebb. It'll only strengthen till nine, and the wind's light and dead in the Goulet. I don't think we'll make Brest on this tide. My advice: reach the three miles WNW into Bertheaume road now, anchor under the land, and let the men sleep; they've been on deck all night. Then go up on the morning flood. The sardines may be lost, but they're a third of a ton; the onions and the men are worth more."})
[t166756 +46h19m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t166756 +46h19m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t166792 +46h19m] ORDER captain> Tell the officer Aye, you are right. We make for Bertheaume.
[t166796 +46h19m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for the road of Bertheaume"})
[t166802 +46h20m] DIRECTOR DOOR: {"after_orders": 300, "after_inputs": 557, "door": "journal", "reason": "03:19 (12 June) The night attempt on the Goulet is beaten by a heading northerly and the young ebb. They are bearing up for Bertheaume road to anchor and rest the worn-out hands, going up to Brest on the morning flood. The 0.3 tons of sardines will likely spoil (green, about 6 hours left at 02:56); the captain and mate have accepted that. Honest outcome; no act. When they reach Brest: the onions to Citizen Le Bris (pay £9 on delivery). If they ask at the Brest quay about salt for next time, the market lists salt at £12/to …[+25]
[t166802 +46h20m] JOURNAL director [note] 03:19 (12 June) The night attempt on the Goulet is beaten by a heading northerly and the young ebb. They are bearing up for Bertheaume road to anchor and rest the worn-out hands, going up to Brest on the morning flood. The 0.3 tons of sardines will likely spoil (green, about 6 hours left at 02:56); the captain and mate have accepted that. Honest outcome; no act. When they reach Brest: the onions to Citizen Le Bris (pay £9 on delivery). If they ask at the Brest quay about salt for next time, the market lists salt at £12/ton.
[t166804 +46h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Course shaped for Bertheaume road, sir: WNW, three miles, full and by on the starboard tack. The master warns the line runs within two cables of the shore under Point Bertheaume, so I'll not run it to the end. We'll bring up in the bight with five or six fathoms on the lead, half a mile short of the point. The lead goes every few minutes from here."})
[t166804 +46h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "heave the lead"})
[t166804 +46h20m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t166804 +46h20m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t166833 +46h20m] ORDER captain> Tell the officer I think you'd be better of taking the direct course, 296 is layable, or at least near enough that full and by will likely fall off too far.
[t166837 +46h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer WNW"})
[t166837 +46h20m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Aye, sir, you're right: full and by fell off to W by N. Steering WNW direct. I'll trim to it once she settles."})
[t166837 +46h20m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "5 minutes"})
[t166837 +46h20m] JOURNAL officer of the watch [agent.stood_by] Stood by until 5 minutes have passed.
[t167141 +46h25m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t167141 +46h25m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "ten minutes"})
[t167141 +46h25m] JOURNAL officer of the watch [agent.stood_by] Stood by until ten minutes have passed.
[t167301 +46h28m] ORDER captain> take a fix
[t167439 +46h30m] ORDER captain> heave the lead
[t167754 +46h35m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say By the deep twelve, sir, sand and mud, good holding. Point Bertheaume is W by N two miles and the road NW by W a mile and a half, with the Buzec a mile and a half W, so I'll not stand on past it. Ten minutes more and we let go in nine or ten fathoms, under the land with the point to windward of the swell. Shall I use the best bower again?"})
[t167754 +46h35m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t167754 +46h35m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t167779 +46h36m] ORDER captain> Tell the officer Aye, let go when you are ready. No need to bring in too close if we have good holding here.
[t167784 +46h36m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the main lug"})
[t167784 +46h36m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the fore lug"})
[t167784 +46h36m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the flying jib"})
[t167784 +46h36m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "let go the best bower"})
[t167787 +46h36m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Taking in the lugs and the flying jib to take the way off her, sir, and the best bower goes as she slows, in nine fathoms at low water on sand and mud. Petit Minou's shore is eight cables N."})
[t167787 +46h36m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "brought up"})
[t167787 +46h36m] JOURNAL officer of the watch [agent.stood_by] Stood by until brought up.
[t167881 +46h38m] LOG [notable/driver.eased] Compression eased to 1x: The best bower is dragging: veer more cable, or let go the small bower.
[t167888 +46h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the jib"})
[t167888 +46h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "take in the mizen"})
[t167888 +46h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "veer more cable"})
[t167888 +46h38m] DIRECTOR> 
    calls: journal({"note": "03:38 Urgent: the best bower 'dragging' as she let go in Bertheaume road with 2 kn of way on and the mizen and jib still set; 44 fathoms out in 12, sand and mud, strain 0.03. Most likely the brief drag of bringing up with way on; the officer is on it. No act. The road is the outer anchorage of Brest; the port is listed 'at anchor in Brest, the road of Bertheaume'. NOTE: if the game counts this as 'in port at Brest', Le Bris's delivery can happen here by lighter or boat when the captain arranges it."})
[t167888 +46h38m] JOURNAL director [note] 03:38 Urgent: the best bower 'dragging' as she let go in Bertheaume road with 2 kn of way on and the mizen and jib still set; 44 fathoms out in 12, sand and mud, strain 0.03. Most likely the brief drag of bringing up with way on; the officer is on it. No act. The road is the outer anchorage of Brest; the port is listed 'at anchor in Brest, the road of Bertheaume'. NOTE: if the game counts this as 'in port at Brest', Le Bris's delivery can happen here by lighter or boat when the captain arranges it.
[t167889 +46h38m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a message or brought up or an urgent event"})
[t167889 +46h38m] JOURNAL director [agent.stood_by] Stood by until a watch, or a message, or brought up, or an urgent event.
[t167892 +46h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say She's dragging, sir. She'd still two knots on her, with the jib and mizen drawing. Taking them in now and veering more cable. If she won't hold, the small bower goes next. Sand and mud, she should bite once the way's off."})
[t167892 +46h38m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "brought up"})
[t167892 +46h38m] JOURNAL officer of the watch [agent.stood_by] Stood by until brought up.
[t168731 +46h52m] DIRECTOR> 
    calls: stand_by({"until": "a watch or a message or under way or an urgent event"})
[t168731 +46h52m] JOURNAL director [agent.stood_by] Stood by until a watch, or a message, or under way, or an urgent event.
[t168734 +46h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "pipe down"})
[t168734 +46h52m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Brought up, sir: the best bower in twelve fathoms on sand and mud, eighty-two fathoms of cable, near seven to one, and she holds. Petit Minou is eight cables N by E, Point Bertheaume two miles W by N. All sail's in and the hands are piped down to rest. The sardines have five hours yet, so if the morning flood serves early we may still sell them at Brest. Shall I keep the anchor watch, sir, or hand you the deck and take my spell? I've been on my feet since midnight last."})
[t168734 +46h52m] OFFICER OF THE WATCH> 
    calls: journal({"note": "03:52, brought up in Bertheaume road, about 48°20'N 4°40'W, in 12 fathoms on sand and mud, the best bower with 82 fathoms of cable; Petit Minou shore 8 cables N by E. She dragged at first because she let go with 2 knots on and the jib and mizen drawing. Lesson: take ALL sail off and let her stop before letting go; veer 6–7× the depth. The Goulet attempt was given up at 03:19: the ebb, a light northerly dead in the Goulet, and worn-out hands. Plan: Brest on the morning flood. The sardines (0.3 t) are good until about 08:50, likely lost. The hands are piped down."})
[t168734 +46h52m] JOURNAL officer of the watch [note] 03:52, brought up in Bertheaume road, about 48°20'N 4°40'W, in 12 fathoms on sand and mud, the best bower with 82 fathoms of cable; Petit Minou shore 8 cables N by E. She dragged at first because she let go with 2 knots on and the jib and mizen drawing. Lesson: take ALL sail off and let her stop before letting go; veer 6–7× the depth. The Goulet attempt was given up at 03:19: the ebb, a light northerly dead in the Goulet, and worn-out hands. Plan: Brest on the morning flood. The sardines (0.3 t) are good until about 08:50, likely lost. The hands are piped down.
[t168736 +46h52m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a word on deck"})
[t168736 +46h52m] JOURNAL officer of the watch [agent.stood_by] Stood by until a word on deck.
[t168770 +46h52m] ORDER captain> Tell the officer We both sleep for a few hours, we both need it, and the fish shall be what they are.
[t168783 +46h53m] OFFICER OF THE WATCH> 
    calls: hand_over({"note": "Handover, middle watch, 03:52. At anchor in Bertheaume road by the best bower: 12 fathoms, sand and mud, 82 fathoms of cable (about 7 to 1), holding after a short drag at letting go. Petit Minou shore 8 cables N by E; Point Bertheaume 2 miles W by N; the Buzec about 1½ miles W. Wind N to N by E, 8–10 knots; glass 30.74, steady; sky hazy, fine. The flood made at Bertheaume while the Goulet's stream ran ebb against us. Since the morning: weighed from the Isle of Bas road at 05:38. Through the Chenal du Four against the flood, passing W of the Four, then of the Platresses, between them and La Valbelle, then W of the Monks. Shot the drift nets on the Iroise ground at 16:58 and hauled a …[+762])
[t168783 +46h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "say Thank you, sir. Good night, or good morning as it's become. The deck's yours and my note's in the log. Call me for anything, and certainly before we weigh for Brest."})
[t168783 +46h53m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "go to the gunroom"})
[t168783 +46h53m] JOURNAL officer of the watch [agent.handover] Handover note (handing over the deck): Handover, middle watch, 03:52. At anchor in Bertheaume road by the best bower: 12 fathoms, sand and mud, 82 fathoms of cable (about 7 to 1), holding after a short drag at letting go. Petit Minou shore 8 cables N by E; Point Bertheaume 2 miles W by N; the Buzec about 1½ miles W. Wind N to N by E, 8–10 knots; glass 30.74, steady; sky hazy, fine. The flood made at Bertheaume while the Goulet's stream ran ebb against us. Since the morning: weighed from the Isle of Bas road at 05:38. Through the Chenal du Four against the flood, passing W of the Four, then of the Platresses, between them and La Valbelle, then W of the Monks. Shot the drift nets on the Iroise ground at 16:58 and hauled at 23:01: 0.3 tons of sardines, in the hold unsalted beside the onions, good until about 08:50. Beat up past the Basses du Lis and N of Toulinguet. Tried the Goulet at 03:00, but the ebb and a dead-ahead light northerly stopped her, so we bore up for Bertheaume on the captain's word. Cargo: 12 tons of onions for Citizen Le Bris, Recouvrance stores, Brest; £9 to collect on his receipt. Purse £66. Watch for: the cable in any shift; the flood in the Goulet, morning, for Brest; the sardines spoiling (heave them over before they taint the onions). Hands worn out; all are down but the anchor watch. Lessons noted in my journal: take all sail off before letting go; mind which tack 'fill away' takes; on a lugger, set the lugs by name. I'm going below to sleep.
[t168783 +46h53m] JOURNAL officer of the watch [agent.deck] Handed over the deck; I stay at the station, off watch.
[t168786 +46h53m] ORDER captain> Go to my cabin
[t168786 +46h53m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "asleep below until called"})
[t168786 +46h53m] JOURNAL officer of the watch [agent.stood_by] Turned in below, in the gunroom, asleep until called.
[t168790 +46h53m] ORDER captain> Sleep
[t169352 +47h02m] ORDER captain> take a fix
[t170471 +47h21m] ORDER captain> take a fix
[t170474 +47h21m] ORDER captain> sleep
[t172899 +48h01m] ORDER captain> Tell the officer Go ahead and stand down, I need to head to bed for real, you can journal first if you like, and we'll continue later.
[t172912 +48h01m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:01, standing down at the captain's word; the game will go on later. Personal note: a good two days. The lessons of the passage are in the entries above. Notes for the owner: (1) 'say to Mr Hervé' went to the captain's empty station as \"the captain to the captain\"; Hervé is both master and captain. (2) The glass can't single out one of two vessels of a kind: 'the glass on a brig' always took the same one, and bearing or 'on the starboard bow' qualifiers were refused. (3) 'get under way' on the lugger orders \"topsail and mainsail\" and sets no lugs. (4) Several queries ('the catch', 'the fishing grounds') fall outside the officer's general authority and must be allowed by name; …[+149])
[t172912 +48h01m] OFFICER OF THE WATCH> 
    calls: stand_down({"note": "Stand-down note, morning watch, 05:01, 12 June 1805. The Éclair, chasse-marée, lies at anchor in Bertheaume road outside the Goulet de Brest: the best bower, 82 fathoms of cable, 12 fathoms, sand and mud, holding. Petit Minou shore 8 cables N by E; the Cock 3 miles W; the Mingan 3 miles E by N. Wind N to N by E, about 10 knots; glass 30.74, steady; hazy, fine. The captain has the deck. He is going below; the hands are worn out. Cargo: 12 tons of onions for Citizen Le Bris at the Recouvrance stores, Brest, £9 more on his receipt. Also 0.3 tons of unsalted sardines in the hold, beside the onions, good only until about 09:00. Heave them over before they taint the onions if the quay ca …[+456])
[t172912 +48h01m] JOURNAL officer of the watch [note] 05:01, standing down at the captain's word; the game will go on later. Personal note: a good two days. The lessons of the passage are in the entries above. Notes for the owner: (1) 'say to Mr Hervé' went to the captain's empty station as "the captain to the captain"; Hervé is both master and captain. (2) The glass can't single out one of two vessels of a kind: 'the glass on a brig' always took the same one, and bearing or 'on the starboard bow' qualifiers were refused. (3) 'get under way' on the lugger orders "topsail and mainsail" and sets no lugs. (4) Several queries ('the catch', 'the fishing grounds') fall outside the officer's general authority and must be allowed by name; possibly intended. (5) Single light bearings with estimated distance moved the account by a mile or more at a time, back and forth, in the Iroise.
[t172912 +48h01m] JOURNAL officer of the watch [agent.handover] Handover note (standing down, for whoever sits here next): Stand-down note, morning watch, 05:01, 12 June 1805. The Éclair, chasse-marée, lies at anchor in Bertheaume road outside the Goulet de Brest: the best bower, 82 fathoms of cable, 12 fathoms, sand and mud, holding. Petit Minou shore 8 cables N by E; the Cock 3 miles W; the Mingan 3 miles E by N. Wind N to N by E, about 10 knots; glass 30.74, steady; hazy, fine. The captain has the deck. He is going below; the hands are worn out. Cargo: 12 tons of onions for Citizen Le Bris at the Recouvrance stores, Brest, £9 more on his receipt. Also 0.3 tons of unsalted sardines in the hold, beside the onions, good only until about 09:00. Heave them over before they taint the onions if the quay can't be reached. Purse £66. Next: weigh on the flood for the Goulet and Brest when the wind gives a slant, mind the Fillettes mid-channel, and get salt at Brest before fishing again. My journal holds the passage from Roscoff, the forms that work for a lugger, and my errors and their lessons. Whoever takes this station: the captain is generous with authority and good-humoured. He'll con the hard passages himself; report plainly and keep the lead going.
[t172912 +48h01m] JOURNAL officer of the watch [agent.stopped] Stood down by the officer of the watch: its own word.
[t172959 +48h02m] DIRECTOR DOOR: {"after_orders": 307, "after_inputs": 572, "door": "journal", "reason": "STAND-DOWN SUMMARY, 05:01, 12 June 1805, at the owner's word. Éclair lies at anchor in Bertheaume road outside the Goulet: 82 fathoms of the best bower in 12 fathoms. Fine, N 10, glass 30.74. 12 tons of onions aboard for Citizen Le Bris (Recouvrance stores, Brest), £9 still owed on delivery; purse £66; 0.3 tons of green sardines, good until about 09:00. MY ACTS OVER THE VOYAGE: Mère Kerbrat (Roscoff fish-wife: mackerel/sardines out west on the Iroise); Old Yann Le Roux (weather sage: NW by afternoon, N by night); Maître G …[+1300]
[t172959 +48h02m] DIRECTOR DOOR: {"after_orders": 307, "after_inputs": 572, "door": "stand_down_note", "reason": "Standing down at the owner's word, 05:01, 12 June. Éclair is at anchor in Bertheaume road with the onions for Brest (£9 still owed by Citizen Le Bris on delivery) and 0.3 tons of sardines spoiling by 09:00. Weather fine, N 10, settled under the ridges. My journal holds the full summary, the open threads and the bugs for the owner.", "by": "its own word"}
[t172959 +48h02m] JOURNAL director [note] STAND-DOWN SUMMARY, 05:01, 12 June 1805, at the owner's word. Éclair lies at anchor in Bertheaume road outside the Goulet: 82 fathoms of the best bower in 12 fathoms. Fine, N 10, glass 30.74. 12 tons of onions aboard for Citizen Le Bris (Recouvrance stores, Brest), £9 still owed on delivery; purse £66; 0.3 tons of green sardines, good until about 09:00. MY ACTS OVER THE VOYAGE: Mère Kerbrat (Roscoff fish-wife: mackerel/sardines out west on the Iroise); Old Yann Le Roux (weather sage: NW by afternoon, N by night); Maître Guéguen and the onion freight (£9 paid in, bill of lading on the cabin table); two highs ('the ridge', 'the Biscay ridge') to bring the honest veer to NW and N; the boy's song; the Sainte-Barbe on the Iroise ground (the boat lying to her nets that the crew used as their mark); answers as the Roscoff pilot Cabioch; Citizen Le Bris made ashore at Brest. ERRORS: 'the Four's towers' (anachronism); Maître Le Gall put in Éclair's cabin by mistake and sent ashore at Brest (a visible line). OPEN THREADS for whoever sits here next: pay the £9 from Le Bris when the onions are delivered at Brest; Le Gall can be met on the Brest quay as an ordinary fisherman; keep the weather fine; no English cruiser (the brief wants a quiet fishing life). BUGS for the owner, all in the journal above: every ship's goal reads 'bound for Falmouth'; the lugger's getting-under-way sets cutter canvas and not the lugs; a constant tidal stream bearing; surface pressure above any system's centre  …[+304]
[t172959 +48h02m] JOURNAL director [agent.handover] Handover note (standing down, for whoever sits here next): Standing down at the owner's word, 05:01, 12 June. Éclair is at anchor in Bertheaume road with the onions for Brest (£9 still owed by Citizen Le Bris on delivery) and 0.3 tons of sardines spoiling by 09:00. Weather fine, N 10, settled under the ridges. My journal holds the full summary, the open threads and the bugs for the owner.
[t172959 +48h02m] JOURNAL director [agent.stopped] Stood down by the director: its own word.
