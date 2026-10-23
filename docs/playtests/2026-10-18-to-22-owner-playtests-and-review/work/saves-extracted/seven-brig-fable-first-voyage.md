# A merchant brig, free, in Torbay — save freesail-seed7-tick4590.json
build {'name': 'm6c', 'rules': '4330be741d1580ee'} builds [{'name': 'm6c', 'rules': '4330be741d1580ee'}] end_tick 4590 start 1805-06-12T05:00:00
director brief/budget: {"brief": {"name": "An interesting passage", "tone": "A passage with things in it. Strangers that must be made out before they are trusted, a front that arrives with the glass falling, a price or a letter that tempts a change of plan, the carpenter with a report. The player should be kept thinking, never kept afraid.", "challenge": "Judgement under some pressure: what is that sail, and should she run or stand on; does the glass warrant a reef now; is the letter to be believed. Two notable things a watch at most; the weather fresh, never a gale.", "limits": {"wind_max_kn": 45, "enemy_heaviest": "frigate-36", "nobody_dies": true, "the_war_as_it_is": true, "the_chart_as_it_is": true}, "cadence": "glass", "budget": {"samples_a_day": 48, "acts_a_day": 48}, "source": "the scenario (C:\\Users\\frenc\\AppData\\Roaming\\FreeSail\\scenarios\\merchant-brig-torbay.yaml)"}}

[t0 +0h00m] ORDER captain> let go the best bower
[t0 +0h00m] LOG [routine/driver.book] The book of standing orders is empty. Begin with none, give your own, or load the starter book: read the standing orders from data/standing_orders/starter.orders (the primer's chapter 11, 'The starting book', gives each routine with its reason).
[t0 +0h00m] JOURNAL director [director.brief] The brief given by the scenario: An interesting passage (limits: no wind above 45 knots (force 9) by any system appended or moved; no enemy heavier than a frigate-36 put on the sea; nobody dies: nothing found aboard that would kill; the war as it is: no port closed to or opened to the ship's own nation; the chart as it is (a point of interest is not the chart); 48 samples and 48 acts a day).
[t432 +0h07m] == SEAT officer of the watch: model now Fable 5.1 via mcp (first Fable 5.1 via mcp), seatings 1, state released: stood down by the captain: the captain's order
[t444 +0h07m] OFFICER OF THE WATCH> 
    calls: library({})
[t455 +0h07m] OFFICER OF THE WATCH> 
    calls: library({"section": "all", "topic": "primer 16"})
[t475 +0h07m] OFFICER OF THE WATCH> 
    calls: journal({"note": "Seated 05:07 as Mr Pearce, lieutenant, a merchant brig at anchor in Brixham road, Torbay, 1 June 1805 by the game's calendar; Captain Bowen (the player) has the deck. From primer 16: with the deck I may order sail, yards, lines, lead, log, bearings, fixes, lookout, pilot's hail, and standing orders in my own rank; not the course, tack, wear, heave to, anchor, all hands, the port's business, or a station, unless the captain allows it by name or 'you may work the ship'. Way out of danger: a helm order, heave to, or an anchor, with danger='...', and the log says why. A grant means exactly what it says. Report every strange sail and shift of wind. Handover note on giving the deck back. …[+303])
[t475 +0h07m] JOURNAL officer of the watch [note] Seated 05:07 as Mr Pearce, lieutenant, a merchant brig at anchor in Brixham road, Torbay, 1 June 1805 by the game's calendar; Captain Bowen (the player) has the deck. From primer 16: with the deck I may order sail, yards, lines, lead, log, bearings, fixes, lookout, pilot's hail, and standing orders in my own rank; not the course, tack, wear, heave to, anchor, all hands, the port's business, or a station, unless the captain allows it by name or 'you may work the ship'. Way out of danger: a helm order, heave to, or an anchor, with danger='...', and the log says why. A grant means exactly what it says. Report every strange sail and shift of wind. Handover note on giving the deck back. The book is empty: no night orders. The ship as she lies: wind W by S 12 kn across the tide, riding to the flood, high water about 05:15, so the ebb comes within the glass and she will swing; the Thatcher a danger N by W three miles; Berry Head five cables on the larboard bow. Books 1 and 2 shelved.
[t477 +0h07m] ORDER captain> Stand down the captain
[t484 +0h08m] OFFICER OF THE WATCH> 
    calls: shelve({"note": "contents; primer 16 whole: the domain, the grants, the way out of danger, the handover"})
[t496 +0h08m] OFFICER OF THE WATCH> Pearce, sir, at the station and off watch. I have read the station's chapter and not yet the rest; I know the rig by its names and would read before the first order if you give me the deck. As she lies: riding to the flood in Brixham road, forty-two fathoms out and the cable bar-taut, the wind W by S across the tide. High water is about a quarter past five, so the ebb comes within the glass and she will swing to it; the Thatcher bears N by W three miles, a danger, and the Berry Head is five cables on the larboard bow. No sail in sight. The book of standing orders is empty. Ready when you are, sir.
[t703 +0h11m] OFFICER OF THE WATCH DOOR: {"after_orders": 1, "after_inputs": 3, "door": "door", "reason": "Fable 5.1", "by": "mcp"}
[t703 +0h11m] JOURNAL officer of the watch [agent.stationed] Took up the station again through the MCP bridge.
[t710 +0h11m] ORDER captain> Tell the officer Glad to have you with me, Pearce. Go ahead and take a look at the ship view and the chart, if you like, you can request different angles of the ship view to get a sense of her, and the chart to see what we're working with. There's a few things, like once you have the deck, you can move about the ship. You can also eat, drink, and sleep as necessary, and check how you are by asking "how am I". I'll give you the deck presently, and the general authority, and I'll get her under way while you get settled. Feel free to stand by on a short basis and get a feel for the ship and the hands.
[t714 +0h11m] ORDER captain> You have the deck
[t714 +0h11m] JOURNAL officer of the watch [agent.deck] Took the deck from the captain.
[t717 +0h11m] ORDER captain> You have general authority
[t717 +0h11m] JOURNAL officer of the watch [agent.deck] Given the captain's general authority to work the ship.
[t727 +0h12m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t744 +0h12m] OFFICER OF THE WATCH> 
    calls: ship_view({})
[t762 +0h12m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:12, with the deck and the captain's general authority (no destination named yet). Chart, coast span: Torbay opens east; we lie in Brixham road under the south horn, the Berry Head five cables to larboard, Brixham a mile SW, the Thatcher and Hope's Nose three miles north across the bay's mouth. Dartmouth four miles S down the coast past the Mewstone; the Blackstone and Homestone off the Dart's mouth, five miles SW by S. Wind W by S blows out of the bay: once under way she can run out east with it on the quarter and nothing in her road but the Thatcher to the north. The ebb due; she has already swung from S by W to W and pitches a little. Ship's view: she is the Harpy, a brig, two …[+164])
[t762 +0h12m] JOURNAL officer of the watch [note] 05:12, with the deck and the captain's general authority (no destination named yet). Chart, coast span: Torbay opens east; we lie in Brixham road under the south horn, the Berry Head five cables to larboard, Brixham a mile SW, the Thatcher and Hope's Nose three miles north across the bay's mouth. Dartmouth four miles S down the coast past the Mewstone; the Blackstone and Homestone off the Dart's mouth, five miles SW by S. Wind W by S blows out of the bay: once under way she can run out east with it on the quarter and nothing in her road but the Thatcher to the north. The ebb due; she has already swung from S by W to W and pitches a little. Ship's view: she is the Harpy, a brig, two masts, all furled, royals sent down, the spanker gaff and boom aft; the drawing is a schematic of spars, not a painting. No sail in sight. Books 3 and 4 shelved.
[t770 +0h12m] OFFICER OF THE WATCH> 
    calls: shelve({"note": "chart: Torbay opens east, wind off the land, Thatcher the only danger in the road out; ship: the Harpy, brig, all furled, royals down"})
[t780 +0h13m] OFFICER OF THE WATCH> Thank you, sir; I have the deck and your authority, and I have looked at the chart and at her. The Harpy lies well for getting out: the wind W by S comes off the land and the bay opens to the east, so she can weigh and run out with it on the quarter, nothing in her road but the Thatcher to the north, and the ebb coming to help her. Before I touch the cable I would know where she is bound, sir; I will not shape a course without it, and your authority keeps the destination back, rightly. If you would have me get her under way meanwhile, say so and I will loose the topsails and heave short; otherwise I hold her as she rides and wait your word.
[t836 +0h13m] ORDER captain> Tell the officer Go ahead and try the order "get under way on the larboard tack", then stand by every 2 minutes, or by notable events, and see as she gets under way. Every 2 minutes will give you the most detail of all the hands at work and the evolutions. One order is all you need until she's under way, using that specific evolution.
[t848 +0h14m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "get under way on the larboard tack"})
[t855 +0h14m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "2 minutes"})
[t855 +0h14m] JOURNAL officer of the watch [agent.stood_by] Stood by until 2 minutes have passed.
[t987 +0h16m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "2 minutes"})
[t987 +0h16m] JOURNAL officer of the watch [agent.stood_by] Stood by until 2 minutes have passed.
[t1107 +0h18m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t1117 +0h18m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t1117 +0h18m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t1119 +0h18m] ORDER captain> Tell the officer You should be able to see the hands at their work, heaving short now.
[t1129 +0h18m] OFFICER OF THE WATCH> 
    calls: read_log({"count": 60, "severity": "routine", "since_tick": 1000})
[t1139 +0h18m] OFFICER OF THE WATCH> I see them, sir: the messenger passed, the bars shipped and swiftered, and the capstan going round. Thirty-six fathoms out of the forty-two, the strain nothing yet. I will stand by on short waits and watch her come up to it.
[t1187 +0h19m] ORDER captain> Tell the officer Once we're under way, we'll steer north east for the wind large and get the sail set properly, as you like. As I'm sure you expect, I shall be no hard captain. We may simply enjoy the sail, today.
[t1200 +0h20m] OFFICER OF THE WATCH> Aye, sir. North-east once she has way on her: that puts the wind on the larboard quarter and carries her out clear of the Ore Stone and the Thatcher, which lie to the north of that line. I will give her the topsails to cast and the courses when she is round, and we shall see what she likes. Thirty fathoms out.
[t1282 +0h21m] ORDER captain> Tell the officer Here's a good procedure note for you: take a fix whenever you can near land, especially if the reckoning is out by more than a few cables. It should fix it right up to where we are, if a good fix can be had, and it's a simple and quick order to do frequently. You can also try out a standing order, if you like, they may be entered, belayed, and canceled in your name as you like. The grammar is in the library, if you need a read up first, or you may simply try it.
[t1283 +0h21m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "the anchor aweigh"})
[t1283 +0h21m] JOURNAL officer of the watch [agent.stood_by] Stood by until the anchor aweigh.
[t1305 +0h21m] ORDER captain> Take a fix
[t1786 +0h29m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t1794 +0h29m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "under way"})
[t1794 +0h29m] JOURNAL officer of the watch [agent.stood_by] Stood by until under way.
[t2213 +0h36m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t2224 +0h37m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "steer NE"})
[t2233 +0h37m] OFFICER OF THE WATCH> Under way, sir, on the larboard tack under topsails and the jib, the bower catted and fished, and I have put her round for north-east as you wished; she is coming away from the Thatcher now. A sail to report: the Torbay pilot cutter standing out toward us from the land, two miles on the starboard bow, red ensign. The pilot is yours to take or refuse, sir; I have not hailed her. When she is steady on the course I mean to give her the courses and see how she carries them with the wind on the quarter.
[t2295 +0h38m] ORDER captain> Tell the officer The pilot is yours to decide on, if you'd like to take them, heave to once they hail. I shall give you the permission to take the pilot if you like, you needn't if you prefer not to but the option shall be open.
[t2297 +0h38m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "steady on the course"})
[t2297 +0h38m] JOURNAL officer of the watch [agent.stood_by] Stood by until steady on the course.
[t2299 +0h38m] ORDER captain> You may accept the pilot
[t2299 +0h38m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: take the pilot.
[t2305 +0h38m] ORDER captain> You may decline the pilot
[t2305 +0h38m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: decline the pilot.
[t2316 +0h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the courses"})
[t2324 +0h38m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "decline the pilot"})
[t2334 +0h38m] OFFICER OF THE WATCH> I waved the cutter off, sir, with your leave: a fair wind, daylight, the bay open ahead and the Thatcher drawing aft on the quarter, and nothing a Torbay pilot could tell us that the chart does not, for his fee and a heave-to to take him. She bore away for Torbay. Steady on north-east now, the wind two points abaft the larboard beam, and the courses going on her. I will see what she makes under topsails and courses before I think about the topgallants.
[t2382 +0h39m] ORDER captain> Tell the officer Aye aye, very well. Go ahead and take another look at her, the topsails and driver are drawing well from the starboard beam view.
[t2387 +0h39m] OFFICER OF THE WATCH> 
    calls: ship_view({"facing": "90"})
[t2401 +0h40m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:39, under way. Got under way on the larboard tack with one order, 05:13 to 05:36: all hands, messenger and bars, hove short from 42 fathoms, topsails loosed and laid aback to cast her, bower aweigh 05:29, under way 05:36 under topsails and jib, bower catted and fished. Steered NE; steady 05:39, wind two to three points abaft the larboard beam, 4 knots under topsails and jib. Pilot cutter stood out; captain gave me both take and decline; I declined (fair wind, daylight, open bay) and said why. Courses going on. Ship's view from the starboard beam: both topsails full and braced for the quarter, the jib and the driver drawing, heel 2 degrees; foresail and mainsail still loosing. Th …[+70])
[t2401 +0h40m] JOURNAL officer of the watch [note] 05:39, under way. Got under way on the larboard tack with one order, 05:13 to 05:36: all hands, messenger and bars, hove short from 42 fathoms, topsails loosed and laid aback to cast her, bower aweigh 05:29, under way 05:36 under topsails and jib, bower catted and fished. Steered NE; steady 05:39, wind two to three points abaft the larboard beam, 4 knots under topsails and jib. Pilot cutter stood out; captain gave me both take and decline; I declined (fair wind, daylight, open bay) and said why. Courses going on. Ship's view from the starboard beam: both topsails full and braced for the quarter, the jib and the driver drawing, heel 2 degrees; foresail and mainsail still loosing. The wind has backed a point, W by S to WSW: to report. Book 5 shelved.
[t2413 +0h40m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 5", "note": "from the starboard beam: topsails full and braced for the quarter, jib and driver drawing, heel 2 degrees, courses loosing"})
[t2422 +0h40m] OFFICER OF THE WATCH> She looks well from the starboard beam, sir: both topsails full and braced for the quarter, the jib and the driver drawing, two degrees of heel, the foresail and mainsail still going on her. One thing to report: the wind has backed a point, W by S to WSW, since we weighed. It only puts it further on the quarter for north-east, which suits her, but you asked for every shift and that is one. I will stand by to the next bell and see what the courses give her.
[t2481 +0h41m] ORDER captain> Tell the officer Don't forget a trim there, you may order "trim the sails" to trim as the wind is at that moment, or "trim for the wind large", for example, to trim all to a rough point, then a fine trim when steady on and the apparent wind settled.
[t2494 +0h41m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t2494 +0h41m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t2509 +0h41m] ORDER captain> Tell the officer Do not forget a trim there, you may order "trim the sails" to trim as the wind is at that moment, or "trim for the wind large", for example, to trim all to a rough point, then a fine trim when steady on and the apparent wind settled.
[t2537 +0h42m] ORDER captain> Tell the officer Do not forget a trim there, an order "trim the sails" to trim as the wind is at that moment, or "trim for the wind large", for example, to trim all to a rough point, then a fine trim when steady on and the apparent wind settled.
[t2545 +0h42m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t2554 +0h42m] OFFICER OF THE WATCH> Trimmed, sir, and thank you for the nudge; I had the sails on her and the yards still braced for the cast. Eight yards braced for the wind on the larboard quarter, the driver and jib sheeted. Courses, topsails, driver and jib set; I will stand by to four bells and read the log for what she makes, and if she is easy under that I would try the topgallants on her after.
[t2609 +0h43m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t2609 +0h43m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t2632 +0h43m] ORDER captain> Tell the officer Aye, thank you kindly Mr Pearce. You have my word to steer as you like to keep the wind large and on a broad reach for good speed.
[t2641 +0h44m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t2641 +0h44m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t2658 +0h44m] OFFICER OF THE WATCH> 
    calls: chart({"span": "coast"})
[t2675 +0h44m] OFFICER OF THE WATCH> 
    calls: journal({"note": "05:44, the log called the Thatcher and the Ore Stone \"steady and closing\" at three miles. Took the chart to check rather than alter: by account she is a mile NE of Brixham road heading NE at 5 knots; the Ore Stone lies about two miles off, a little west of north, and the NE track passes it more than a mile to the eastward, the Thatcher further still. The bearings read steady because they are given to the point and the range is long; they should draw aft to the west within the glass. Holding NE; watching the Ore Stone's bearing, and if it does not start drawing aft by 05:55 I come up to E for a mile. Book 6 shelved."})
[t2675 +0h44m] JOURNAL officer of the watch [note] 05:44, the log called the Thatcher and the Ore Stone "steady and closing" at three miles. Took the chart to check rather than alter: by account she is a mile NE of Brixham road heading NE at 5 knots; the Ore Stone lies about two miles off, a little west of north, and the NE track passes it more than a mile to the eastward, the Thatcher further still. The bearings read steady because they are given to the point and the range is long; they should draw aft to the west within the glass. Holding NE; watching the Ore Stone's bearing, and if it does not start drawing aft by 05:55 I come up to E for a mile. Book 6 shelved.
[t2685 +0h44m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 6", "note": "NE track clears the Ore Stone by over a mile to the east; the steady bearing is the coarse point at long range"})
[t2694 +0h44m] OFFICER OF THE WATCH> The log has the Thatcher and the Ore Stone steady and closing, sir, and I went to the chart before I touched the helm. By account she passes the Ore Stone more than a mile to the eastward on north-east, and the Thatcher further; the bearings read steady because they are given to the point at three miles. I am holding north-east and watching the Ore Stone's bearing; if it has not begun to draw aft by the end of this glass I will come up to east for a mile, which costs us nothing with the wind where it is. Five knots under courses, topsails, driver and jib.
[t2734 +0h45m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t2734 +0h45m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t2745 +0h45m] ORDER captain> Tell the officer Aye, I worry not for it on this course. The tide is slack, and our speed well and good. We shall clear them easily today, and if not, bearing off to east shall clear them right as rain.
[t2753 +0h45m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "four bells"})
[t2753 +0h45m] JOURNAL officer of the watch [agent.stood_by] Stood by until four bells.
[t3075 +0h51m] ORDER captain> Take a fix
[t3600 +1h00m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t3609 +1h00m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the topgallants"})
[t3620 +1h00m] OFFICER OF THE WATCH> Four bells, sir, and she is clear of the bay: the Thatcher drawn aft to NW by W, the Ore Stone abeam a mile to larboard, thirteen fathoms under her and the flood setting her a knot to the north-east with us. Your fix at 05:51 moved the account five cables, which is worth knowing about the master's slate. The wind has come back to W by S, thirteen knots with gusts to seventeen, the glass risen two hundredths, fine. She is easy under all plain sail to the topsails, so I am giving her the topgallants now; if the gusts make her complain I will take them in again and say so. I mean to trim when they are on her and then let her run.
[t3691 +1h01m] ORDER captain> Tell the officer This wind seems to be driving us on to Portland and Weymouth quite readily. Shall we make that our destination? It should be a short and easy trip, with this wind, and even if it came about, an easy enough beat, if a bit slower. We could work the studdingsails on a run to Portland in this breeze quite well, I say.
[t3692 +1h01m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t3692 +1h01m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t3873 +1h04m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t3878 +1h04m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "a notable event"})
[t3878 +1h04m] JOURNAL officer of the watch [agent.stood_by] Stood by until a notable event.
[t3927 +1h05m] LOG [routine/driver.eased] Compression eased to 1x: the officer of the watch is sampled.
[t3937 +1h05m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t3946 +1h05m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "five bells"})
[t3946 +1h05m] JOURNAL officer of the watch [agent.stood_by] Stood by until five bells.
[t4154 +1h09m] ORDER captain> take a fix
[t4166 +1h09m] ORDER captain> Ask the officer What say you on Portland?
[t4192 +1h09m] OFFICER OF THE WATCH> 
    calls: answer({"text": "Portland is a fair day's sail from here, sir, and a good one with this wind. The Bill lies roughly east by north across Lyme Bay, some thirty-five miles from the Berry Head; with the wind W by S she runs for it with the wind on the quarter the whole way, and at the five or six knots she is making she would raise the Bill by the afternoon watch. The glass is steady and rising a little, the sky fine.\n\nThe thing to mind is the Bill itself. The Race off it is the worst water on this coast, and today is full moon, so the tides are springs and the Race at its strongest; and the Shambles lie beyond it to the east. We should give the Bill a wide berth, three miles or more to the southwar …[+734])
[t4199 +1h09m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "five bells"})
[t4199 +1h09m] JOURNAL officer of the watch [agent.stood_by] Stood by until five bells.
[t4249 +1h10m] ORDER captain> You may shape a course for Portland West Bay
[t4249 +1h10m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: shape a course for Portland West Bay.
[t4254 +1h10m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "shape a course for Portland West Bay"})
[t4266 +1h11m] OFFICER OF THE WATCH> Course shaped for Portland West Bay, sir: east by north, thirty-seven miles by account, steering east to allow the flood until it turns about a quarter past eight, when I will have the master work it again. That brings the wind nearly aft, so once she is steady I will trim for it and, if she will carry them, give her the studdingsails on the starboard side, where the wind is not; a run of thirty-odd miles is what they are for, and I would rather learn them in a moderate breeze than a strong one.
[t4394 +1h13m] ORDER captain> Tell the officer Let us make a standing order book for the passage. This system is mostly for you, and I do not have access to it on my end or a good view of exactly how it works, but I have seen an officer do it before, so it's somewhere in the briefing or library. You should be able to draft a book of standing orders to enter in, so let's plan some for the voyage that will be useful. One that I think is vital is a regular reshaping of the course, so that it reshapes as the tide and wind change and makes good. As well, timely, or wind shift based trims are often good, and anything else you'd like on the books so you don't need to worry about reacting instantly to certain things, or automating anything.
[t4395 +1h13m] OFFICER OF THE WATCH> 
    calls: stand_by({"until": "steady on the course"})
[t4395 +1h13m] JOURNAL officer of the watch [agent.stood_by] Stood by until steady on the course.
[t4407 +1h13m] OFFICER OF THE WATCH DOOR: {"after_orders": 22, "after_inputs": 32, "door": "read", "reason": "primer 11, the whole chapter", "by": "library(topic='primer 11', section='all')"}
[t4427 +1h13m] OFFICER OF THE WATCH DOOR: {"after_orders": 22, "after_inputs": 32, "door": "journal", "reason": "Primer 11, the standing dialect: standing order \"<name>\" [by the <officer>]: <trigger>[, if <condition>] then <order>[; <order>]. Triggers: when <condition> [for N minutes] (fires as it comes to hold, not again until false five minutes), at <event> (sunset, sunrise, eight bells, change of the watch, a squall, a wind shift, the glass falling fast, a strain warning, a sail blown out, noon, a sounding, a landfall, hove to, filled away, tacked, wore), every <interval>. Guard trims with 'and she is not hove to'. Book orders: s …[+448]
[t4427 +1h13m] JOURNAL officer of the watch [note] Primer 11, the standing dialect: standing order "<name>" [by the <officer>]: <trigger>[, if <condition>] then <order>[; <order>]. Triggers: when <condition> [for N minutes] (fires as it comes to hold, not again until false five minutes), at <event> (sunset, sunrise, eight bells, change of the watch, a squall, a wind shift, the glass falling fast, a strain warning, a sail blown out, noon, a sounding, a landfall, hove to, filled away, tacked, wore), every <interval>. Guard trims with 'and she is not hove to'. Book orders: standing orders; show/belay/resume/strike "name". Orders in a rule are checked against my domain at entry. My book for the Portland passage, in my rank: reshape every hour; trim on a one-point shift; tend the sheets every glass; studdingsails in over 20 knots; topgallants and studdingsails in over 25 for two minutes; the lead every ten minutes under 20 fathoms with land in sight; light sails in at sunset. Book 7 shelved.
[t4436 +1h13m] OFFICER OF THE WATCH DOOR: {"after_orders": 22, "after_inputs": 32, "door": "shelve", "reason": "book 7", "by": "out of turn", "note": "the standing dialect: triggers when/at/every, conditions, orders after then; guard trims against hove to"}
[t4468 +1h14m] ORDER captain> You may shape a course for Portland West Bay
[t4468 +1h14m] JOURNAL officer of the watch [agent.deck] Allowed by the captain: shape a course for Portland West Bay.
[t4469 +1h14m] OFFICER OF THE WATCH> Aye, sir, a book for the passage. I have read the starting book's chapter and I will enter these in my own rank, so that you may strike any of them: the course reshaped for Portland West Bay every hour, which takes the tide as the master allows it; the yards trimmed when the wind shifts a point; the sheets tended every glass; the studdingsails in if the true wind goes over twenty knots, and the topgallants in with them if it holds over twenty-five for two minutes; the lead every ten minutes once we are under twenty fathoms with the land in sight, for the approach; and the light sails in at sunset should we still be at sea. Entering them now.
[t4496 +1h14m] ORDER captain> Tell the officer Aye, go ahead and enter them in the book in your name.
[t4504 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"reshape for Portland\": every hour then shape a course for Portland West Bay"})
[t4513 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"trim on a shift\": when the true wind veers 1 point or backs 1 point and she is not hove to then trim sails"})
[t4517 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"tend the sheets\": every glass, if she is not hove to then trim the sheets"})
[t4521 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"studdingsails in\": when the true wind exceeds 20 knots then take in the studdingsails"})
[t4526 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"shorten for weather\": when the true wind exceeds 25 knots for 2 minutes then take in the studdingsails; take in the topgallants"})
[t4529 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"lead in soundings\": every 10 minutes, if the land is in sight and the depth is under 20 fathoms then heave the lead"})
[t4533 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "standing order \"light sails at sunset\": at sunset then take in the studdingsails; take in the topgallants"})
[t4543 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "trim the sails"})
[t4546 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "set the studdingsails"})
[t4554 +1h15m] OFFICER OF THE WATCH> 
    calls: submit_order({"text": "rig out the larboard studdingsail booms"})
[t4558 +1h15m] OFFICER OF THE WATCH> 
    calls: library({"find": "rig out"})
[t4559 +1h15m] ORDER captain> rig out the stuns'ls
[t4569 +1h16m] OFFICER OF THE WATCH> 
    calls: shelve({"book": "book 8", "note": "studdingsails: rig out first, then set, with a side (weather, lee, both); first thing in when it freshens; lee boom will not go out with yards braced past 45"})
[t4590 +1h16m] LOG [notable/driver.saved] Saved to seven-brig-first-voyage.json at tick 4590; the log's digest is d43f7a614e757fc5.
[t4590 +1h16m] ORDER captain> stand down the officer
[t4590 +1h16m] JOURNAL officer of the watch [agent.stopped] Stood down by the captain: the captain's order.
