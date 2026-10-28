"""Whose service the ship is in (practice and resupply, between packages 72 and 73;
docs/design/Build-PracticeAndResupply.md §5): a King's ship, a privateer (a letter of
marque cruising for prizes), or a merchantman.

The Ordnance issues powder and shot free and vouched to the King's ships of the port's own
nation, and the merchants sell to everyone else (the owner's ruling of 2026-10-25); the
Regulations' allowance for exercise is a King's ship's (the Gunner, Art. XXI). The answer
is the first of these that gives one:

1. the scenario's papers, `papers: {service: kings}` (or `privateer`, `merchant`), read as
   the private signals are (`signals.table_of`);
2. the captain's role: a King's ship, a cruiser or a commodore is the King's; a privateer
   a privateer's; a merchantman, a packet or a fisherman a merchant's;
3. her wardroom file's binding of the captain's station (`captains._is_kings_ship`): a
   captain or a commander commands a King's ship;
4. otherwise a merchantman.

The rules the Regulations make for a captain (the necessity before he buys stores of the
merchants, the allowance for exercise) are the British Admiralty's, and bind a King's ship
of Britain only (`under_the_regulations`): a man of war of another nation, a King's ship
here by her wardroom or her role, buys of the merchants as everyone else does, her own
service's rules not being in the game (the build design's §10: no national arsenal; the
review's finding, an American frigate refused at Falmouth under the British Regulations and
her purchase written "for the Admiralty's account").

Read from the state the World already has; nothing is drawn, written or logged.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "KINGS",
    "MERCHANT",
    "PRIVATEER",
    "REGULATIONS_NATION",
    "ROLE_SERVICE",
    "SERVICES",
    "service_of",
    "under_the_regulations",
]

KINGS = "kings"
PRIVATEER = "privateer"
MERCHANT = "merchant"
SERVICES: tuple[str, ...] = (KINGS, PRIVATEER, MERCHANT)

# The nation whose Regulations these are: "Regulations and Instructions relating to His
# Majesty's Service at Sea", 1806 (1808 printing; docs/references/admiralty/).
REGULATIONS_NATION = "britain"

# The captains' roles (`captains.ROLES`) by the service each is in.
ROLE_SERVICE: dict[str, str] = {
    "kings-ship": KINGS,
    "cruiser": KINGS,
    "commodore": KINGS,
    "privateer": PRIVATEER,
    "merchant": MERCHANT,
    "packet": MERCHANT,
    "fisherman": MERCHANT,
}

# The words the papers may give for each, beside the service's own name.
_PAPERS_WORDS: dict[str, str] = {
    "kings": KINGS,
    "king's": KINGS,
    "kings-ship": KINGS,
    "king's ship": KINGS,
    "privateer": PRIVATEER,
    "letter of marque": PRIVATEER,
    "merchant": MERCHANT,
    "merchantman": MERCHANT,
}


def service_of(world: Any) -> str:
    """The service of this World's ship: "kings", "privateer" or "merchant", from the
    first source that gives one (the module's head)."""
    given = _papers_service(world)
    if given is not None:
        return given
    by_role = ROLE_SERVICE.get(_role(world))
    if by_role is not None:
        return by_role
    from freesail.world.captains import _is_kings_ship

    if _is_kings_ship(world):
        return KINGS
    return MERCHANT


def under_the_regulations(world: Any) -> bool:
    """Whether the Admiralty's Regulations bind her captain: a King's ship (`service_of`)
    of Britain's (`signals.own_nation`), who buys stores of the merchants only of
    absolute necessity and for the Admiralty's account, and keeps the allowance for
    exercise (the module's head)."""
    if service_of(world) != KINGS:
        return False
    from freesail.world.signals import own_nation

    return own_nation(world) == REGULATIONS_NATION


def _papers_service(world: Any) -> str | None:
    """The scenario's `papers: {service: ...}`, when it gives one this module knows; a word
    it does not know gives nothing, and the next source answers."""
    papers = getattr(getattr(world, "scenario", None), "papers", None) or {}
    given = papers.get("service") if isinstance(papers, dict) else None
    if given is None:
        return None
    key = " ".join(str(given).lower().replace("’", "'").split())
    return _PAPERS_WORDS.get(key)


def _role(world: Any) -> str:
    """The captain's role; for a crewed World whose captain has none yet, her far brain's
    (as `signals.table_of` reads it)."""
    captain = getattr(world, "captain", None)
    role = str(getattr(captain, "role", "") or "")
    if not role:
        vessel = getattr(world, "vessel", None)
        brain = getattr(vessel, "brain", None)
        role = str(getattr(brain, "role", "") or "")
    return role
