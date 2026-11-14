import sys; sys.path.insert(0, "tests"); sys.path.insert(0, ".")  # run from the repository root
from test_fishing import world_at
from freesail.world.squadrons import Squadron
from freesail.world.captains import read_intent
w = world_at(ship="data/ships/frigate-36.yaml", lat=48.3, lon=-5.0)
sq = Squadron(id="b", name="the blockade of Brest", kind="squadron", nation="britain", commander="x", members=["x"], goal="blockade Brest", formation="line ahead", book="blockade", regime="on blockade", rendezvous="")
print(repr(sq.destination_words(w)))
i = read_intent(w, "blockade Brest"); print(i.kind, i.destination)
print("bound for {rendezvous}".replace("{rendezvous}", sq.rendezvous or sq.destination_words(w)))
