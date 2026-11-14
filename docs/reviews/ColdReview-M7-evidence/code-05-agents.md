# Code reader 05: `freesail/agents/` (working notes; rewritten at the end)

Status: IN PROGRESS. These are notes taken while reading; the final file replaces them.

Read whole so far: `__init__.py`, `model.py`, `watches.py`, `journal.py`, `tripwires.py`,
`pictures.py`, `seat.py`, `fake.py`; `docs/agents/ConsentBrief.md`, `README.md`, `Harness.md`.

Notes so far:

- `__init__.py:1-24` docstring lists ten modules and says "only the two doors" import a vendor;
  there are eighteen files and three vendor-speaking doors (`api.py`).
- `model.py:83-92` `Reply.pieces()`: when `raw` is set only `raw` is scanned for the token.
- `seat.py:289-299` the player's seat borrows eleven unbound methods of `Harness`.
- `seat.py:507-538` the seat's order path re-implements the "has not the deck" refusal.
- `pictures.py:27-28` docstring says the local runner's models read words; Harness.md §5 says
  pictures are offered there.
- `pictures.py:282-286` `paint` catches `TypeError` for "a painter of a test's own".
- `fake.py:318` `assert` in a library function.
- measured: 24,871 lines, 880 functions, 192 imports inside functions, 19.7% of lines comment
  or docstring.
