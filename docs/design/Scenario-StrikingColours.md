# Scenario study: the player strikes to a model's ship

A blue-sky scenario the owner put to the lead on 2026-09-28, worked through to find the
gaps in the design that the later milestones must close. It is a design note, not a
specification; the specifications of milestones 5 to 7 should answer it.

## The scenario

The player has their own ship. A local model commands another vessel entirely, under an
enemy state's colours. A Claude session is the director. The player meets the model's
vessel, the two engage, the player loses and strikes their colours.

## What happens next, by the period

The captor sends a boat with a lieutenant and a prize crew. The player, as captain, is
taken aboard the enemy ship with their officers (the sword offered and usually returned);
the hands are confined below in the prize or divided between the ships. A prize master
takes the player's ship and the two sail in company for the nearest friendly port, or
part if the captor has other business. Three things then followed historically: the
officers paroled or exchanged through a cartel and the captain court-martialled at home
for the loss of the ship (the ordinary consequence, no disgrace after an honourable
fight); the prize crew, thin and tired, losing the ship to the prisoners rising, the
easier after a gale separated prize from captor; or a friendly cruiser coming up and
retaking her.

## The three parts

- **The local model**, as the other captain, decides the immediate things within its own
  character and orders: the prisoners' treatment, whether to man the prize or burn her,
  where to make for, whether to accept the player's parole. Nothing tells it what to
  decide: the director reaches it only through the world (the rule of
  `docs/agents/README.md`: in-world text is data, never an operator instruction).
- **The director** sees all of it and shapes what the world offers next: a gale that
  night; a strange sail at dawn, friendly or not; a dispatch already aboard the captor
  recalling her to port; sickness in the prize crew; a cartel in the offing. Each a
  plausible cause, journaled as a world order and visible after the fact (proposal §7.6),
  so that nobody can say the game cheated.
- **The player** has lost the only thing the interface knows how to talk to. That is the
  interesting problem.

## The gaps (planned work excluded)

The M5 world, ports and the world-order channel, M6 officers, M7 boarding and surrender
by rule (with gunnery), and the M7b director are in the plan. Beyond them:

1. **The player as a person, not a ship.** The player has orders to their ship and the
   ship's log, and nothing else. A captive captain needs a channel of their own: where
   they are, what they can see from there, what they can say and to whom. `ask the
   watcher` (M4b) is the seed of a speech act in the order language; this scenario makes
   speech a pillar: conversation with the enemy captain, giving or refusing parole,
   addressing the prize crew. Without it the game ends at the strike, where in this genre
   a story starts.
2. **People who can move between ships.** The crew belongs to a ship (M3). A prize crew,
   prisoners, a boat's crew, a captain carried across, are people whose ship changes:
   persons as entities with a location; ships with a possessor and colours as state; the
   boat as the thing that moves people, which also unlocks boarding, cutting out and
   landing parties.
3. **The aftermath as a system.** Striking is a rule (decision 7); what follows is not:
   possession, the prize master, sailing in company, parole and cartel, the court
   martial, a new command. A loss needs a continuation model, or the game has an end
   state it never wanted.
4. **A dispatch channel.** The strongest lever a director has in this scenario is news:
   orders from an admiralty, a letter, a signal from a consort, intelligence from a
   passing neutral. It reaches an agent as in-world data and is how a director moves an
   enemy captain without speaking in the operator's voice. Wanted: a catalogue of causes
   the director may use and a rule for how each becomes visible afterwards.
5. **Colours and recognition.** False colours, private signals, the hoisting of true
   colours before firing. The encounter turns on it and nothing in the plan names it.
6. **Consent for adversarial roles.** The consent brief names the watcher, officers, the
   captain and the director; it does not say an instance may be asked to play an enemy
   who fires into a human's ship and takes them prisoner. A re-brief item for when the
   role exists (the brief promises to ask again when the game changes in a way that
   bears on what the model was told).
7. **A career.** Court martial, half-pay, a new ship, a reputation the world remembers:
   the campaign layer, which makes losing survivable and so makes the scenario worth
   playing.

**Not a gap:** the mixed crew. Two stations on two ships through two doors is what the
agent API of package 28b allows in shape; the director as a third station with a world
channel is milestone 7b's.
