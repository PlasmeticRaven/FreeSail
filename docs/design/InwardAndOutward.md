# Design principle: inward and outward

From the owner's general notes of 2026-09-29, agreed the same day. A principle for every
milestone after the fourth; not itself a specification.

## The question

The ship is on the sea. The game can be built inward from here, into the ship (her
spaces, her people, her sounds), or outward, into the world around her (weather systems,
coasts, ports, other ships, news). Ideally both, but either can spiral without end, and a
feature on one side that has no meaning on the other is dead weight. Whichever way a
milestone goes, it needs a bounded goal, and everything it adds has to stay relevant to
what the game already has.

## The principle

**Everything inward must be reachable by an order or a reading; everything outward must
arrive at the ship through something the ship already models.**

Inward: a space, a person or a sound that the player cannot ask about, order, or read in
the log or the readings does not exist for the game, and is not built. The console and the
browser are text first, and a language model at a station has exactly what the human has,
so the test is the same for both: is there a line for it.

Outward: news, weather, a ship in sight, a summons from an admiral, all reach the ship the
way they reached a ship in 1805, through the lookout, the glass, the barometer, a boat
alongside, a messenger at the cabin door. The owner's picture: the captain is at his meal
in his cabin; a message from a distant port comes through the door with the messenger
who came off in the pilot cutter. Every link in that chain is something the game models
or will model (the cabin, the door, the messenger, the cutter, the port), and the message
is carried by them, not delivered to the player from nowhere.

## What it settles

- **The director fills gaps, not holes.** The director (design proposal §7.6) acts
  through world orders and plausible causes. The principle says what "plausible" means:
  a cause the ship already models. A director can send the cutter; it cannot make the
  message appear on the table.
- **Interiors are bounded** (owner, 2026-09-29). A space is defined by a name and a
  description, and named, important characters by their state and their position in the
  ship; text and data are the baseline, as always. Layouts with a visualisation are a
  long-term dream, taken up only from that data if it earns it. People are not simulated
  moving about in spaces, and the chain from a shot to a splinter to a man on the lower
  deck is drawn as a limit: a hit is an event with consequences in the ship's state and
  her people's, not a simulation of the space it happened in. It can come back as a
  bounded milestone if the outward world makes it worth having.
- **A bounded goal each way.** Milestone 5 goes outward (a world: weather, a small map,
  ports, other ships, navigation). The inward work that milestone needs is exactly what
  the outward arrivals need: named people with a position and a state, the cabin and the
  deck as places a person can be, and the boat alongside. No more than that until a later
  milestone names its inward goal.

## How to use it

When a feature is proposed, ask which way it goes and name the order or reading (inward)
or the modelled carrier (outward) that makes it real. If neither can be named, the feature
waits. This is the same test as the log's: if the log cannot say it, the game did not do
it.
