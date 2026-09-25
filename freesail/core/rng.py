"""Seeded, named random streams.

All randomness in the simulation comes from here. Each consumer asks for a
stream by name; the stream is seeded from the master seed and the name, so
adding a new consumer does not change the numbers an existing one sees. Never
call `random` or `numpy.random` directly anywhere else.
"""

from __future__ import annotations

import hashlib
import random


class Rng:
    def __init__(self, seed: int):
        self.seed = int(seed)
        self._streams: dict[str, random.Random] = {}

    def stream(self, name: str) -> random.Random:
        stream = self._streams.get(name)
        if stream is None:
            digest = hashlib.sha256(f"{self.seed}:{name}".encode()).digest()
            stream = random.Random(int.from_bytes(digest[:8], "big"))
            self._streams[name] = stream
        return stream

    def stream_names(self) -> list[str]:
        return sorted(self._streams)
