# Gate harness (kept for the next gate)

All scripts are run from inside the tree under test (`cd <tree> && PYTHONPATH=$PWD python3 -P ...`);
the tree on PYTHONPATH is the build measured. Run OLD and NEW with the same case file, then compare.

- `run.py CASES OUT.jsonl [-j N] [--only prefix,prefix]` drives worlds through scripted steps
  (a ship file and Scenario kwargs, or a scenario file; steps `order`, `run`, `wind`, `ramp`, `py`,
  `checkpoint`, `load_checkpoint`; `"watcher": true` seats the scripted fake at the watcher's
  station and records every sample's tick and reason). One JSON line per case: every log line
  (tick, kind, severity, text, subject, turn_wait), every reply, a state hash every
  `hash_every` seconds (motion, every part's fields incl. loads and condition, the strain records,
  every vessel's place), and an end summary. CASES is a JSON list or a .py defining `CASES`.
- `compare.py OLD.jsonl NEW.jsonl [--quiet] [--rules RULES.py] [--json OUT]` aligns the two logs
  per case, classes every differing line by a rule table (`classify`; the default is package 127's,
  replace it with `--rules`), counts by label/side/severity/kind, separates lines after the first
  state divergence (or after a line of a rule that changes what she does, `DIVERGING`) as `post:`,
  and prints UNDECLARED lines, end-state differences and differing replies.
- `seat.py OUT.json [ships]` serves every ship file at a model's seat (all readings, the state,
  the library contents, every topic and section, the tool descriptions) and answers a broad order
  list on copies of one world; `seatdiff.py OLD.json NEW.json` prints every difference.
- `statedump.py CASES CASE_ID OUT.json T...` dumps the hash's components at given ticks;
  `statedump.py --diff A B` names the component that differs (use when a hash differs and the end
  summary does not).
- `traceplug.py` is a pytest plugin: `TRACE_OUT=x.json PYTHONPATH=$PWD:<gate> python3 -P -m pytest
  -p traceplug ... <one test>` records every World's state hash every 60 ticks and its log while a
  recorded-passage test runs; `python3 -I traceplug.py A.json B.json` compares two.
- `mutate.py MUTANTS.py PRISTINE SCRATCH OUT.txt [-n 4] [--slow] [--only ids]` applies each
  mutant (file, old string, new string, tests) to the scratch tree, runs its tests, restores.

Caveat measured at gate 127: hashes are of field values (dataclass defaults counted), since a
checkpoint drops attributes equal to their class default from `__dict__`.
