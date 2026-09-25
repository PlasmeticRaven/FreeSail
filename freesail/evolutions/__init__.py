"""Evolutions: named pieces of seamanship, read from data files and run by ticks.

- ``registry``: reads ``data/evolutions/*.yaml`` into ``EVOLUTIONS`` at import.
- ``expr``: the tiny safe expression language the files use for their
  preconditions and their ``sets``/``ramp`` entries.
- ``runner``: ``Runner(ship)``, which starts evolutions, advances them each
  tick and writes the log notes.
- ``scripts``: the scripted manoeuvres (tack, wear, heave to, fill away).
"""

from freesail.evolutions.registry import EVOLUTIONS, Evolution, EvolutionFileError
from freesail.evolutions.runner import Runner, part_name, weather_factor

__all__ = [
    "EVOLUTIONS",
    "Evolution",
    "EvolutionFileError",
    "Runner",
    "part_name",
    "weather_factor",
]
