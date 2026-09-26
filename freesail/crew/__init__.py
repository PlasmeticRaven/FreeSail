"""The ship's company (spec M3 §2): the model, the muster and the watch bill.

`hands.py` (the pool and the crew factor) and `routine.py` (watch changes, all hands,
fatigue) are added by packages 17 and 18.
"""

from freesail.crew.model import Crew, Rating, Sailor, Station, Watch
from freesail.crew.muster import muster

__all__ = ["Crew", "Rating", "Sailor", "Station", "Watch", "muster"]
