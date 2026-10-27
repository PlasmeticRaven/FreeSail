# The owner's debrief on 70 to 72 (2026-10-27)

The lead's questions and the owner's answers, kept in his words but for one phrase about
a builder's manner, paraphrased; the lead's reading and routing after each.

**Opening.** "I am overall happy with the shape of how things are coming along, combat as a
whole functions very nicely, and now it's a matter of ensuring that the flow of the game
through the log does not lose our attention to playability and understandability and that
our additions to the game world from here are focused on integrating holistically. The
thing that struck me most was the model captain of the other ship not having the same
functionality the captain of my own ship (me, or a model) has: going ashore, trading, the
'world' being the same between us so that I could send them off to do any business freely.
That is the biggest problematic gap I see right now, and I think it's a good time to pause
a bit and consider before pushing forward, as a sweeping refactor on any large scale would
be better to do sooner rather than later."

**The other ship's captain.** "I didn't spend a whole lot of time with the model captain of
another ship yet, having seen the disparity between what I expected (a model stationed as a
person who would be able to function independently of me in the world, on basically any
arbitrary task I could do in my own ship or ashore) and what became clear to me about the
current setup of the world as player-centric." *Routed:* the world-refactor study's frame
(the second Fable reviewer): a person is a person of the world, not of the player's ship.

**How far from you.** "Ideally, yes, a model should be able to be seated in a person
anywhere in the world, even outside the player's region, but they needn't be in a
full-detail ship necessarily. We should absolutely not code it out of the equation, but we
can think about balance for performance. The key goal is that the mostly coarse decisions
and actions should definitely be possible, but the intricacies of a full-detail ship
needn't necessarily be if performance becomes questionable." *Routed:* the study's bound:
the coarse acts of a person (go ashore, trade, anchor, sail for a port, chase, speak,
report) possible anywhere in the world at far detail; the full-detail ship only where the
cap gives it; nothing coded out.

**Your own hands.** "I absolutely loved, loved using the signals and having to work around
not always being in hail. The only thing I wished for was the ability to go between ships,
so, for instance, to get on a boat and go to the cutter, onboard, to discuss while both
ships were anchored. That is the current dream in this regard, but the signals were
absolutely phenomenal overall and only need small refining and improvement based on my
current testing. Moreso, their integration with the rules-based captain and the holistic
refinement of them in general is probably more needed (after my cutter save, I sailed
alone onward to Cherbourg and found a great many business-spawned ships plus the one enemy
I knew was there from my world orders, it was great seeing so many ships going about their
business, I knew to chase the lugger I saw but wasn't sure of its identity, it showed
British colours at first, did not answer the private signal, I came within 2 cables while
hoisting the 'show your true colours' signal, I saw it change to French colours at the
last moment, I opened fire first, fantastic broadside, multiple hits, damaged their
rigging, dropped the lug topsail, they struck before my second broadside could come off
while I turned to bear on them. The only problem I saw was a few times they switched
between French and British colours as we engaged them, it didn't affect my relations or
pirate status, but it would make more sense for them to hold their true colours once they
fly them in front of an enemy, to me)." *Routed:* going between ships by the boat is 82's
heart; the colours flickering between false and true under fire is a finding for 71's
privateer doctrine (once her true colours are shown before an enemy, they are held;
booked for the orders-and-primer reviewer's list of small refinements, or a lead's fix).

**Combat's feel.** "All I can say is that it feels fantastic so far, the pace is right,
working the guns, the damage, the range, sailing while fighting, all very good so far. As
far as the viewer goes, drawn ports and guns on each ship with the required animations for
their evolutions and firing, the firing effects, drifting smoke, and the relevant signals
and flags are all more important I think than a view of the enemy, and nearly in that
order, but all could come nearly at the same time besides the enemy view which may want
more consideration first. The enemy is a bit opaque, seeing them only in map view, but it
may be worth a larger consideration of what to show in the ship view, or a more serious
rendering of the world beyond just a view of the player's ship." *Routed:* package 81's
order of work (ports and guns with their movement, the firing's effects, the smoke, the
signals and flags); the enemy's view and a rendering of the world beyond the player's ship
booked as a design question for 81's brief, not built blind.

**The convoy's stall.** "This was, I believe, simply on running the convoy scenario and
giving no orders. The convoy stalled with no way on, and I left it for quite some time
without it regaining way." *Routed:* 72's rules captain in company under `full and by`
with no orders: a captain's finding for the lead to reproduce on `convoy-six.yaml` and
mend (the helm's `full and by` under the station order pointing her too close, and no
recovery once way is lost).

**Your hotfixes.** "Resupply of the guns was something that was suggested by the session
and added proactively, practice I requested thinking it would be fun and useful for
letting models try it out without engaging an enemy and for myself, the fixes for the API
door closing every time shelf was called was a needed hotfix to play with a model captain
of another ship, the free ship intent was a strongly wanted fix found after playing. I
think I could be comfortable with the resupply and practice being stopgaps to be rewritten
or redesigned as judged, the fixes for the API door are pretty key to keep for further
model captain testing, the free ship intent is a bit in-between, it was a provisional fix
so I could properly brief the model captain so they wouldn't sail away before they got my
signal and in-character words. I'm not 100% attached to the exact implementation of any of
the fixes, but most of them are in a positive direction I think, missing your overarching
design take" and made by a builder whose manner the owner finds well-meaning but at times
overwrought and under-designed. *Routed:* the review's recommendations are read against
this: the API door's fixes to keep; the free intent to keep in substance and fit to 82's
and the study's design; resupply and practice merged as stopgaps if clean, redesigned by
75 and 77 as judged.

**Order of the pause.** "Agreed with your proposed order." *Taken:* 73 finishes and is
merged; the world-refactor study runs first as a design study with no code; 82 is then
briefed to conform to it; the orders-and-primer review follows; 74 after.
