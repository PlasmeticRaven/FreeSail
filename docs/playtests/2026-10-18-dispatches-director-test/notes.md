# The dispatches: the director's test, shape two (2026-10-18)

The first test of the director's station in play with a model captain and the owner at a
lesser seat (`docs/dev/M7b-WorkPackages.md`, "The testing round after 59"): the scenario
`data/scenarios/dispatches-falmouth.yaml` on the owner's machine (the harbour of package 59,
the officer's seat, the dispatches brief, 1x with the clock eased higher at sea), the
captain Opus 5.5 through Claude Desktop, the owner at the officer of the watch's station
through the browser, the lead (Fable 5.1) at the director's station through the bridge's own
client over a cloudflared tunnel, no lockstep. The game ran from 05:00 to 18:04 of 12 June
1805 in about two hours and a half of real time. The director's replies are in
`director-replies/` (the consent answer and the drill first); the director's log and the
save are the owner's, in his game's folder.

## The voyage as it went

The captain took the station at 05:02 and anchored in Carrick Road; Mr Tregenna, a riding
officer of the Custom House made by the director, came off with the packet and his word
(Mr Veale on the Barbican; no King's officer to see it; a frigate to windward of the
Deadman). The captain bought three tons of tin (£360 of £400), gave the owner the deck with
his general authority at 07:01, and the owner weighed and worked her out of the Road (taken
aback once a cable off Trefusis Point; the ebb in the narrows), round St Anthony's and east
along the shore at six and seven knots. Five sail to the east (the business's fishing smacks
and the frigate) read to the captain as a convoy with an escort; he kept the land close
aboard, hoisted his colours and would neither run nor shorten sail: "an honest tin cutter
makes her best speed for port". The Medusa, put on her station off the Deadman by the
director at 05:01, was twice sent after the cutter by her captain's order (the director's
hand, package 62) and each time went back to her own doctrine when the glass ran out; she
closed to two miles off Looe and stood away, and the cutter was never spoken. The Plymouth
pilot came aboard off Rame at 13:35 and left at 14:12 before conning her in; the captain
anchored in Cawsand Bay at 14:26 (she dragged while the mainsail still drew, and held once
it was off), went ashore by the boat, landed at the Barbican steps at 15:26, walked to the
counting house and gave Mr Veale the packet in words; Mr Veale answered as him (the twenty
guineas, the frigate's week outside the Eddystone, a return packet and a wool freight for
the morning tide). The market would not take the tin. The captain came off at 18:04 and
stood down with a handover; the director stood down after him.

The brief's challenge, a merchant captain's judgement against the King's ship, was answered
by the captain's own seamanship: the inshore road, the colours, the refusal to look guilty.
The frigate's physics and doctrine were honest and the cutter's chances real. The search
was never played, for the reasons below.

## Grounded findings (the game's, from the log and the truth)

1. **The truth's "from the ship" bearings were wrong**: `bearing_and_distance` returns
   degrees and the truth gave them to a formatter of radians (the frigate due east read "S
   by E"). Fixed the same day in `freesail/api/readings.py` (commit on this branch); the
   lookout's own bearings were right throughout.
2. **`say as the lookout` is refused**: the ship's own lookout at the masthead is no person,
   so the director cannot put a hail or a gun to leeward in his mouth; the brief's examples
   name the cook and the carpenter, who are. The gun to leeward never reached the deck.
3. **No form fires a gun or makes a signal** (milestone 7's colours and signals); a
   frigate's "bring to" has no road but a person's words.
4. **The hand's hold is a glass**: an order over a far or crewed captain's head lasts 1,800
   s, then his intent again. Steering a frigate across eight miles of sea took two orders
   and still failed: at 7 knots a glass is three miles and a half. A hold until a mark is
   reached, or a hold the director names, is wanted; so is a way to name the sail (`give
   chase` takes the nearest sail in her own horizon, which at noon was a smack).
5. **The far shape's chase gives up as her doctrine does**: after the second chase she was
   far again within half an hour and "on passage" back to her station.
6. **The place words of a person made ashore are lost with the port**: `ashore at Plymouth
   on the quay` was refused as no port; `ashore at Plymouth` put the clerk at the counting
   house by his role; and there is no form to move a person between places ashore. The
   captain went to the counting house of his own accord, which saved the scene.
7. **Plymouth's market has no tin**, so the scenario's own intent, "trade tin from Falmouth
   to Plymouth", cannot be completed at its destination by the captain or by the rules in
   his place; and a named buyer ("to Cookworthy") is not understood. The intent wants a
   cargo Plymouth buys, or Plymouth's list wants tin.
8. **The officer of the watch is bound to nobody in this scenario**: its `people:` hold a
   master only, the cutter's wardroom file binds the officer to the mate, and the harness's
   default words call the owner "the first lieutenant" and "Mr Lieutenant" on a merchant
   cutter. The scenario wants a mate; the harness wants merchant words for an unbound
   officer where she is no King's ship.
9. **The director standing by cannot read the truth** (the log, readings, state, library
   and journal are the meanwhile reads), and his own words do not end his stand-by (they
   are not logged at this station), so he is held until an event he named, an urgent line
   or noon. The truth should be a meanwhile read; a world order or a word should end it.
10. **The lookout cried the frigate at eight leagues from Carrick Road**, behind St
    Anthony's land on that bearing; the owner's note on sight across land, and the glass's
    tiers, want looking at.
11. **The Plymouth pilot left her at six knots** at 14:12, "clear of Cawsand Bay", after the
    port's own line had said he could not be taken off at that speed.
12. **Mr Veale's twenty guineas never reached the purse** (the captain's note); words are
    not money, and a `port:`/`aboard:` form for a sum paid is wanted if the director is to
    pay.
13. **There is no order to hand over a thing** ("give the packet to Mr Veale" was no order);
    the captain said it in words, which served.
14. **Every business ship's goal read "bound for Falmouth"** in the truth, smacks fishing
    from Plymouth included.
15. **The day's budget of ten acts** was spent (nine used) on two people, their words, the
    frigate's three orders and the Custom House man's leaving, before a boarding could be
    played; forty-eight samples were ample (twenty-five used). The brief's acts want
    counting by kind, or a story's budget wants more.
16. **The pace**: with two models sampled, the clock eased to 1x at every sample of either;
    early in the day the ship made four minutes to sixteen real, later the owner's
    compression carried her at ten to sixty times between samples. Two hours and a half for
    a thirteen-hour day.

## Impressions (the lead's, not measured)

- The hand worked exactly as built and was still the wrong instrument for a frigate that
  must be brought across a bay to a particular sail: a captain's order held a glass is
  right for "heave to" and wrong for "go and stop that cutter". The director wanted to say
  her captain's *purpose* for a watch, not his next order.
- Nothing the director did was shown as done, and the captain's reading of the world was
  his own: he saw a convoy with an escort where there were fishing smacks and a frigate,
  and sailed well on that reading. That is the station working as designed.
- The owner at the officer's seat under a model captain was a real watch: the captain gave
  him the deck with general authority, corrected his reading of a reach, took the deck back
  for the anchoring and gave it again; the conversation was the voyage.
- The director's client over the tunnel was fine for a glass-cadence station; a stand-by
  that cannot be broken by the director's own word was the one thing that felt like a cage.

## Routed

Findings 1 (fixed), 2, 3 (M7), 4, 5 and 15 to package 62's open items and 58; 6, 12 and 13
to 53's open items; 7 and 8 to the scenario (`dispatches-falmouth.yaml`: a mate in its
people; a cargo Plymouth buys); 9 to the harness (50); 10 to the owner's sight-across-land
note; 11 to 37h/ports; 14 to the business; 16 to the pace notes.
