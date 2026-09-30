"""The lookout (spec M5 §12; package 32): the sighting model's reading in the log's words.

Once a game minute the World asks the lookout to look (`Lookout.look`): the chart says
what is within the horizon from the masthead and the weather's visibility, by each
feature's own rule (`freesail.world.chart.Chart.in_sight`), and the lookout says it as a
lookout did, by compass bearing and an estimated distance ("The Lizard bearing N by E,
distant four leagues"; "A light on the larboard bow, bearing NW by N"). The estimate is
the period's, to the nearest league or mile (`geo.estimate_words`), never the truth to a
cable; the bearing is true, the compass's variation being the reckoning's business
(package 33). A light at night is "a light": the lookout does not know whose it is, though
the reading's data names it for the master and the tests. In 5b the lookout is the
world's own voice at routine severity, notable for a landfall or a danger; in 5c the same
model sights sail, and later a small model may hold the station (decision 24).

The reading `what is in sight` (`freesail.api.readings`) is the last look's sightings,
and `the land` whether any land is among them, so a book may say `when the land is in
sight then ...`.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Any

from freesail import units
from freesail.core.events import Severity
from freesail.world.chart import Chart, Sighting
from freesail.world.geo import estimate_words

__all__ = [
    "DEFAULT_HEIGHT_OF_EYE_M",
    "LOOKOUT_REPEAT_MIN",
    "Lookout",
    "height_of_eye",
    "relative_words",
]

# A lookout with no masthead to climb (the point ship of the early milestones) looks
# from thirty metres, a frigate's topmast head; judgement.
DEFAULT_HEIGHT_OF_EYE_M = 30.0

# A feature lost and found again within this many minutes is not hailed again
# (judgement: a headland flickering at the edge of the haze is not a line a minute).
LOOKOUT_REPEAT_MIN = 30

MAST_CLASSES = frozenset({"mast", "topmast", "topgallant_mast", "royal_mast"})


def height_of_eye(ship: Any) -> float:
    """The lookout's eye at the topmast head: the deck's height above the water plus the
    lower mast and the topmast of the tallest chain standing (a topmast sent down or
    carried away brings him to the lower masthead); the default without a rig."""
    spars = getattr(ship, "spars", None)
    hull = getattr(ship, "hull", None)
    if not spars or hull is None:
        return DEFAULT_HEIGHT_OF_EYE_M
    deck = float(hull.spec.deck_height_m)
    best = 0.0
    for spar in spars.values():
        if spar.cls not in ("mast", "topmast") or spar.wrecked or spar.sent_down:
            continue
        chain = ship.spar_chain(spar)
        if any(p.wrecked or p.sent_down for p in chain):
            continue
        height = sum(float(p.height_m) for p in chain if p.cls in MAST_CLASSES)
        best = max(best, height)
    return deck + best if best > 0.0 else DEFAULT_HEIGHT_OF_EYE_M


def relative_words(relative_rad: float) -> str:
    """Where a thing lies from the ship's head, in the lookout's words: right ahead, on
    the starboard bow, abeam to larboard, on the larboard quarter, right astern."""
    points = units.rad_to_points(abs(units.wrap_pi(relative_rad)))
    side = "starboard" if units.wrap_pi(relative_rad) >= 0 else "larboard"
    if points < 1.0:
        return "right ahead"
    if points < 6.0:
        return f"on the {side} bow"
    if points < 10.0:
        return f"abeam to {side}"
    if points < 15.0:
        return f"on the {side} quarter"
    return "right astern"


@dataclass
class Lookout:
    chart: Chart
    sightings: list[Sighting] = field(default_factory=list)
    height_of_eye_m: float = DEFAULT_HEIGHT_OF_EYE_M
    _announced: dict[str, int] = field(default_factory=dict)  # feature id -> the minute hailed
    _had_land: bool = False
    _looked: bool = False

    def look(self, world: Any) -> list[tuple[Severity, str, str, dict[str, Any]]]:
        """Look from the masthead now: the sightings kept for the reading, and the log's
        lines for what is newly in sight, a landfall or a danger notable, and for the
        land lost. Nothing on the plane."""
        pos = world.position
        if pos is None:
            return []
        conditions = getattr(world, "conditions", None)
        visibility_nm = conditions.visibility_nm if conditions is not None else None
        self.height_of_eye_m = height_of_eye(world.ship)
        found = self.chart.in_sight(
            pos, self.height_of_eye_m, visibility_nm, world.daylight, world.clock.ship_time
        )
        minute = world.clock.tick // 60
        heading = float(world.ship.heading)
        lines: list[tuple[Severity, str, str, dict[str, Any]]] = []
        land_now = any(s.seen_as in ("land", "light") for s in found)
        first_land = land_now and not self._had_land
        for s in found:
            last = self._announced.get(s.feature.id)
            if last is not None and minute - last < LOOKOUT_REPEAT_MIN:
                self._announced[s.feature.id] = minute
                continue
            self._announced[s.feature.id] = minute
            text = self.words(s, heading)
            # a danger is notable; so is everything seen in the look that makes the landfall
            notable = s.seen_as == "danger" or first_land
            data = s.to_dict() | {
                "relative": relative_words(math.radians(s.bearing_deg) - heading),
                "estimate": estimate_words(s.distance_m),
                "height_of_eye_m": round(self.height_of_eye_m, 1),
                "landfall": bool(first_land),
            }
            lines.append(
                (Severity.NOTABLE if notable else Severity.ROUTINE, "lookout.sighting", text, data)
            )
        if self._had_land and not land_now and self._looked:
            lines.append(
                (Severity.ROUTINE, "lookout.lost", "The land is out of sight.", {"count": 0})
            )
        self.sightings = found
        self._had_land = land_now
        self._looked = True
        return lines

    @staticmethod
    def words(s: Sighting, heading_rad: float) -> str:
        """The sighting in the lookout's words."""
        point = units.point_name(math.radians(s.bearing_deg))
        relative = relative_words(math.radians(s.bearing_deg) - heading_rad)
        distance = estimate_words(s.distance_m)
        if s.seen_as == "light":
            return f"A light {relative}, bearing {point}."
        name = s.feature.name
        head = name[:1].upper() + name[1:]
        if s.seen_as == "danger":
            return f"{head} bearing {point}, distant {distance}: a danger."
        return f"{head} bearing {point}, distant {distance}."

    # -- the readings -------------------------------------------------------------------

    def reading(self, heading_rad: float) -> dict[str, Any]:
        """`what is in sight`: the last look's sightings with the lookout's words, or
        nothing in sight."""
        items = []
        for s in self.sightings:
            items.append(
                s.to_dict()
                | {
                    "relative": relative_words(math.radians(s.bearing_deg) - heading_rad),
                    "estimate": estimate_words(s.distance_m),
                    "words": self.words(s, heading_rad).rstrip("."),
                }
            )
        words = (
            "; ".join(i["words"][:1].lower() + i["words"][1:] for i in items) or "nothing in sight"
        )
        return {"count": len(items), "words": words, "items": items}

    def land(self, heading_rad: float) -> dict[str, Any]:
        """`the land`: in sight or not, with the nearest land or light sighted."""
        # the land: the shore, its marks and its lights; a rock in sight is a danger, not land
        land = [s for s in self.sightings if s.seen_as in ("land", "light", "mark")]
        if not land:
            return {"in_sight": False, "words": "not in sight", "nearest": None}
        nearest = min(land, key=lambda s: s.distance_m)
        return {
            "in_sight": True,
            "words": "in sight",
            "nearest": nearest.to_dict() | {"words": self.words(nearest, heading_rad).rstrip(".")},
        }
