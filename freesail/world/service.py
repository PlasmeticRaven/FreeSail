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
   a privateer's; a merchantman, a packet, a fisherman, an Indiaman or a revenue cutter a
   merchant's (package 75: the last two neither the Navy's nor a privateer's);
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

import re
from typing import Any

__all__ = [
    "KINGS",
    "MERCHANT",
    "PRIVATEER",
    "REGULATIONS_NATION",
    "ROLE_SERVICE",
    "SERVICES",
    "SERVICE_ROLE",
    "free_intent_role",
    "kings_force",
    "papers_service",
    "regulations_said",
    "service_of",
    "service_role",
    "service_word",
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
    # package 74: a prize under her prize crew is her captor's (the record's `service`
    # answers first; the King's where none is written)
    "prize-master": KINGS,
    # package 75 (docs/design/Build-Ships.md §8.3; SW-4): an East Indiaman is a merchant
    # ship, the Company's and not the King's; a revenue cutter is the Customs' or the
    # Excise's and not the Navy's, under no Admiralty Regulations, so neither is the King's
    # here, and each buys of the merchants as the hired cutter does (judgement, for the
    # lead: the Boards' own service is not in the game). Each is what her file's wardroom
    # gives without a role (a master commands the merchant brig and the cutter), so the
    # service of neither file moves with the role.
    "indiaman": MERCHANT,
    "revenue": MERCHANT,
}

# The captain's role each service stands for where a reader needs a role and her captain has
# none (package 121: the hail's words, the answer when she is hailed, a free intent's role).
SERVICE_ROLE: dict[str, str] = {KINGS: "kings-ship", PRIVATEER: "privateer", MERCHANT: "merchant"}

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
    role = _role(world)
    if role == "prize-master":
        # a prize (package 74): her captor's service, written on her record at the taking
        from freesail.world.prizes import record_of

        rec = record_of(getattr(world, "vessel", None))
        if rec and rec.get("service") in SERVICES:
            return str(rec["service"])
    by_role = ROLE_SERVICE.get(role)
    if by_role is not None:
        return by_role
    from freesail.world.captains import _is_kings_ship

    if _is_kings_ship(world):
        return KINGS
    return MERCHANT


def papers_service(world: Any) -> str | None:
    """The service her scenario's papers give, alone (package 121): None where they give
    none or a word this module does not know. For a reader that must not ask her captain,
    as the captain's own default role at his making."""
    return _papers_service(world)


def free_intent_role(world: Any) -> str:
    """The role of a captain whose intent names none (home, a passage, a free hand;
    `captains.role_for`): her papers' service first (package 121: a privateer by her papers
    on a passage sails by the privateer's book, not the King's ship's), else a King's ship
    by her wardroom (package 86), else a merchantman."""
    given = _papers_service(world)
    if given is not None:
        return SERVICE_ROLE[given]
    from freesail.world.captains import _is_kings_ship

    return "kings-ship" if _is_kings_ship(world) else "merchant"


def service_role(world: Any) -> str:
    """Her captain's role where he has one, else the role of her service (`service_of`,
    `SERVICE_ROLE`): a privateer by her papers hails and answers as a privateer, and a
    King's ship by her wardroom as a King's ship (package 121)."""
    role = _role(world)
    return role or SERVICE_ROLE[service_of(world)]


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
    return service_word(given)


def regulations_said(world: Any, words: str) -> str:
    """Words of the wardroom's file as her service binds them (package 121): the file cites
    the Regulations for each officer's duty, "(the Regulations, the Lieutenant, art. IV)";
    where they do not bind her (a privateer or a merchantman on a King's ship's file) the
    citations are not said, and the duty is."""
    if world is None or "the Regulations" not in words or under_the_regulations(world):
        return words
    return re.sub(r"\s*\((?:judgement on )?the Regulations[^()]*\)", "", words)


def kings_force(world: Any) -> bool:
    """Whether her ship is one of the King's ships of war, to blockade a port or cover the
    trade: a King's ship by `service_of`, but never a prize under her prize-master (package
    121's follow-up: a prize is not her captor's King's ship, as `readings.ship_words` says)."""
    return service_of(world) == KINGS and _role(world) != "prize-master"


def service_word(given: Any) -> str | None:
    """The service a word of the papers names ("privateer", "letter of marque", "King's
    ship", in any case), or None for a word that names none; the scenario door refuses
    such a word (package 121)."""
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
