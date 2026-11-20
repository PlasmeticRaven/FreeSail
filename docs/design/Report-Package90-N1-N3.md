# Report: package 90, the shared data N1 to N3 (the *Diana*'s builder, 20 November 2026)

**In short.** N1 and N3 are built, each its own commit; **N2 stopped** under the stop rule before
any file of it was written, because adding `corsair` to `ROLES` needs `freesail/world/service.py`,
which neither my row of the plan's §7.1 nor the card names (a test holds that file's table of
services equal to `ROLES`), and the role reaches three more files outside both (§3). N3 does not
depend on N2, so it went on. No ship file moved: the generator writes all eighteen byte for byte
after each step. Every test that ran passed; the final fast tier is the base's, test by test, and
the two new tests beside it; its 8 skips and 1 xfail are the base's own (§4).

**The branch.** The one my brief names, `…/pkg-90-diana`, cut from the trunk's c4e46309
(`git log -1` checked), the trunk carrying stage 0 and item 37 merged at 22422808. Nothing was
rebased, merged or forced.

## 1. The commits

| Step | Commit | Files |
|---|---|---|
| N1 | `be846e2ce12f67943f59b0a20195c0e7f88a63e2` | `data/crew/names.yaml` (the `spanish` list), `tests/test_crew_model.py` (the moved pin and a new test), `docs/dev/TuningNotes.md` ("Package 90, N1") |
| N2 | none: stopped (§3) | none |
| N3 | `b63d5e278d5896d3d242503bd0f8c35b13f71a57` | `data/marines.yaml` (the `spanish` kit), `tests/test_fight.py` (a new test), `docs/dev/TuningNotes.md` ("Package 90, N3") |
| this report | the commit that adds this file, the branch's head | `docs/design/Report-Package90-N1-N3.md` |

The report is a commit of its own, after N3, so that it can name N3's hash and the final tier's
comparison; no test reads `docs/design/` (grepped), so the final tier stands for it.

**Two files beside the row.** `tests/test_crew_model.py` and `tests/test_fight.py` are not named
in my §7.1 row, which names `tests/test_corsair.py` alone; they are the tests of `names.yaml` and
`marines.yaml`, which the card's "May change" admits ("the tests of these"). `docs/dev/TuningNotes.md`
is the brief's own place for the records. Each step's own new tests went into those files and not
into `tests/test_corsair.py`, which is N2's. If the coordinating session reads the row more
narrowly, the two additions in the test files are the ones to move.

## 2. The steps

### N1: the Spanish names list

A `spanish` list in `data/crew/names.yaml`: **68 given names and 244 surnames**, its source and its
rule at its head. Spain's row in `data/nations.yaml` keeps `names: english`. No committed file
names the list.

- **The source** (read and downloaded here on 2026-11-20, not put in the tree): Instituto Nacional
  de Estadística, "Frecuencias de apellidos", surnames borne by 100 or more as a first surname,
  from the annual population census at 1 January 2025 (`apellidos_frecuencia.xls`, sheet
  "Apellidos >=100"); and "Nombres más frecuentes por fecha de nacimiento", from the Padrón
  continuo at 1 January 2022 (`nombres_por_fecha.xls`, sheet 1, the nation's men, and sheet 3, the
  men born before 1930 by province of birth). Both are INE's tables as served at
  `www.ine.es/daco/daco42/nombyapel/`.
- **The surnames**: the table's first 250 by rank, in its order, less Singh and Chen (a modern
  immigration) and the four of more than one word (de la Fuente, de la Cruz, del Río, de la Torre).
  Checked by a script against the table, rank for rank, the accents folded.
- **The given names**: the men born before 1930, the nation's fifty (sheet 1) and each province of
  birth's twenty (sheet 3, those born abroad left out), in that order; one name to a man (José
  María and the other compounds left out); the Catalan forms in their Castilian (Josep, Joan,
  Jaume, Pere, Miquel, Jordi, Francesc, Joaquim, Lluís, Antoni); less nine names taken for later
  fashions: Jesús, Javier alone, Alfredo, Daniel, David, Eduardo, Emilio, Julio and Ricardo.
- **JUDGEMENT, and what I was unsure of**: a table of today stands for 1795 to 1815. The surnames
  are mostly old patronymics, so their rank should hold. The given names of men born before 1930
  are the table's nearest to the period. The nine left out are my judgement and no source's:
  a reader may want some back (Daniel, Julio) or more out. The spelling is today's Academy's (the
  table prints capitals with no accents, and the period's printing varied: "Josef" in 1799), and
  one surname is given to a man, as in the other lists, where a Spanish record often gave two.
- **Its readers** (grepped: `names.yaml`, `name_lists`, `NAMES_PATH`): the muster
  (`freesail/crew/muster.py`), which takes any list a crew section names; the recruits of a port
  (`world/dealings.py`) and a prize master's surname (`world/prizes.py`), which read a nation's row
  and the English list, so nothing there moves; and `tests/test_crew_model.py`.
- **Found outside the step, not mended** (the stop rule): `freesail/world/nations.py`'s
  `NAMES_TO_NATION` gives a ship's nation by her list where the scenario gives none
  (`Dealings.ship_nation`). It has no `spanish` row, so a ship drawn from the Spanish list with
  no nation given would be taken for Britain's, the table's default. Nothing names the list yet,
  so nothing is wrong today. **The row is wanted before the first ship file with `names: spanish`**
  (the *Diana*'s own, next), in a file neither my row nor the card names.

### N3: the Spanish marines' kit

A `spanish` kit in `data/marines.yaml`. Its figures are the basic kit's, said, with its corps, its
men's kind and its share aloft from sources by page:
- `name` "the Spanish navy's infantry and artillery", `soldiers: true`: the regulation of 1788's
  infantry and infantry-artillery (Winfield et al. 2023, p. 1446 and following, by
  `VesselReferences-2026-11-Spanish.md` §15), and James's "soldiers" for the *África*'s 38
  (James vol. II p. 365, by `Design-Ship-Xebec.md` §8.1). The engine reads no `soldiers` key.
- `tops_share` 0.2 and `tops_factor` 1.0, the basic kit's. The 1748 ordinances post the troops'
  officer on the poop in action (*Ordenanzas de Su Magestad para su Real Armada*, Madrid 1748,
  tratado I, título V, art. XXXIV, p. 76; in the tree, `docs/references/signals/`), so the share
  stays under the 0.3 at which a rules captain sends them aloft, not the French habit's 0.4.
- **The musket and the drill: the basic kit's.** The same ordinances order the troops exercised
  at the musket and the great gun (tratado I, título III, art. XLV, p. 42) but give no rate, and
  no page in the tree gives the Spanish musket. So the musket, the sergeant's and the officer's
  arms, `volley_s` 25, `hit_at_50_yd` 0.04 and `boarding` 1.2 are the basic kit's (JUDGEMENT).

**Read by no ship, and why.** A ship's kit is her nation's (`Nations.marines_kit_of`), and Spain's
row in `data/nations.yaml` names `basic`, as it did. The plan's N3 row keys the kit on "the fit's
marines", **but no such key exists**: a fit's `marines` is the quarter bill's count (package 75's
B1), and the schema has no kit key on a fit. For a Spanish ship to muster with the kit, one of two
things is wanted, and neither is done here:
- Spain's row in `data/nations.yaml` names it, a file nobody touches after stage 0 (plan §7.1);
- or a fit's kit key is built in `freesail/ship/schema.py`, which is stage 0's.

The xebec's King's fit (the row's "Before") meets this first.

## 3. N2: why it stopped, and what it needs

**The stop.** `ROLES` is mine, with `data/captains/corsair.yaml`, the roles' sets in
`world/regimes.py` and `world/squadrons.py`, and `tests/test_corsair.py`. Reading every reader of
a role (grepped: `ROLES`, `ROLE_SERVICE`, `ROLE_OF_CAPTAIN`, `SHIP_OF_WAR_ROLES`,
`HAND_PEACEFUL_ROLES`, `_MAN_OF_WAR_ROLES`, `_ARMED_ROLES`, `role_of_vessel`, the seats), I found
that the role needs files outside both my row and the card. **The first is proved by a test, so
the step cannot be built whole within its files.** I wrote none of N2 and edited none of these
files.

1. **`freesail/world/service.py`, `ROLE_SERVICE`** (needed: a test fails without it).
   `tests/test_service.py::test_the_captains_role_answers_next_for_every_role` asserts
   `set(ROLE_SERVICE) == set(ROLES)`. A `corsair` in `ROLES` fails it unless the table gains her
   service: `kings`, `privateer` or `merchant`. Loosening the test is not allowed. Which service
   a regency's cruiser is in is the lead's call: a privateer's by her trade of prizes, or the
   King's as a state's ship. It decides `service_of` for a World made from her (a crewed far
   ship) and whether the Regulations bind her.
2. **`freesail/world/flags.py`, `ROLE_OF_CAPTAIN`** (wanted at the cause). `colour_role` reads an
   unknown role as `"merchant"`, so a corsair would wear a merchantman's occasions of colours. The
   table's roles are "kings ship", "commodore", "admiral", "merchant", "privateer" and "any".
3. **`freesail/world/prize_court.py`, `SHIP_OF_WAR_ROLES`** (wanted at the cause). This set holds
   the privateer beside the King's roles. It decides a taken ship's head money (`head_money`:
   nothing for a role outside it), her valuation's kind and the purchase for the service. A
   corsair taken by a King's ship would earn no head money unless the set has her.
4. **The seats** (wanted by the step's own words: "no seat for a player at it, and a model's seat
   refused in words", Design-SlaveryAndSuppression §8):
   - A model's seat at a corsair's captain is held by `freesail/world/seats.py`'s `hold`, whose
     refusal in words for an adversarial hull already runs through `freesail/world/prizes.py`'s
     `adversarial_seat_why`. The corsair's refusal belongs beside it, until the brief is in the
     consent documents.
   - The player's ship takes a role from her description's first role
     (`brains.description_role`, `captains.role_for`, `ships._role_of_spec`). No description
     carries `corsair` yet, but the polacre's and the xebec's regency rows will (Xeb-D §9.1), and a
     bare start from the harbour would then seat the player at a corsair. That refusal is in
     `world/ships.py`, `world/captains.py`'s `role_for` (beyond `ROLES`), the scenario's load or
     the harbour. None of these is mine.
   - Neither can be done in the book or in `ROLES`.

**Within my files, as found** (for whoever resumes N2):
- `freesail/world/orders.py`'s `HAND_PEACEFUL_ROLES` needs no edit; the corsair is not to be in it.
- `regimes._MAN_OF_WAR_ROLES` (a squadron in ordinary waits for an armed vessel of a power to
  leave the offing) and `squadrons._ARMED_ROLES` (a captor and a cover) take `corsair` as the plan
  says.
- **Pins that iterate over `ROLES`** and bound the book's form, besides the audit's counts:
  - `tests/test_captains.py`'s two doctrine tests (sources on every key, a book for every state,
    four fighting lines, every line parsing on four ships);
  - `tests/test_bellerophon.py:1722` (`line_of_battle_nm` only in the King's ship's and the
    commodore's books, so none in the corsair's);
  - `tests/test_subtypes.py:608-629` (only the privateer and the revenue cutter name two
    stimuli in an `unless`). A book on the privateer's form with her guarded row out of
    `evading` moves this pin, old beside new.
- `world/captains.py:1002`'s comment on the books' cache says "nine" roles. There are ten, and the
  corsair makes eleven: twelve files with the hail's, within its `maxsize=16`. The words are stale;
  there is no fault.

**What the book would hold** (not written; from the documents named in the brief, for the
resumption): the privateer's and the cruiser's form with every key under `thresholds:`, its
differences at its head with their sources (Eng §8; Pol-D §12; Xeb-D §9.2):
- boarding early and by numbers: `board_odds` 1.0, `board_when` at any time (Falconer, two-thirds
  soldiers; the *Gamo*'s two attempts, James vol. III p. 133; the Tripolitan's 80 men in a polacre
  of fourteen guns, James vol. III p. 160);
- `aim` rigging and close action;
- the thirteen prize keys, `prize_goal` home and `burns_when` never (a prize a cargo and a ransom);
- the people's fate package 110's, never the book's;
- the A1c keys `lateen_leave_kn` and `bad_hand_s` with their sources, if anywhere (Eng §2.3 item 6);
- no `stations:` table (no season key is built).

## 4. The tests

Run from the worktree's root with `python -m pytest -p no:cacheprovider -o addopts="--dist
loadgroup"`, `freesail` imported from the worktree (checked). The base ran in the main checkout,
left at c4e46309, while the steps were built in a separate worktree, so nothing the base read was
edited under it.

**How the fast tier whole ran.** The first run of the base, whole in one pytest, was cut at 69 %
by my own time limit (no failure in its log up to there); the second was cut by the container's
restart. So each fast tier whole, the base's and the final tree's, ran as four pytest runs over
the 186 test files, 38, 48, 50 and 50 of them (`tests/test_*.py`, every one, checked against the
directory; none lives deeper), each with `-n 4`, the options above and a `--junitxml` of its own,
the four junit files then read together. A `loadgroup` group lies within one file, so no group
was split. The base ran from 07:41 to 08:38 UTC, the final tree from 08:38 to 09:37.

| Set | Tree | Result |
|---|---|---|
| **The base**: the fast tier whole, `-n 4`, `--junitxml` | c4e46309 | 8440 passed, 8 skipped, 1 xfailed (8449); 583 slow left out |
| N1's own: `tests/test_crew_model.py -k "name_lists or spanish or unknown_name or abbreviated"` | N1 in the tree | 4 passed |
| N1's readers: `tests/test_crew_model.py`, `test_nations.py`, `test_people.py`, `test_ports.py`, `test_range_audit.py`, `test_service.py`, whole, `-n 2` | N1 in the tree | 165 passed (18 slow left out) |
| N1's readers: `tests/test_known_truths.py -k recruit` (a Spanish port's recruits) | N1 in the tree | 1 passed, 646 deselected |
| N3's own: `tests/test_fight.py -k "spanish_kit or hit_chance"` | N3 in the tree | 2 passed |
| N3's readers: `tests/test_fight.py`, `test_range_audit.py`, `test_nations.py`, whole, `-n 2` | N3 in the tree | 68 passed (11 slow left out) |
| The generator, `python tools/gen_ships.py <scratch>`, and a `cmp` of every committed ship file | after N1; after N3 | 18 of 18 byte for byte, twice |
| **The final tree**: the fast tier whole, `-n 4`, `--junitxml` | b63d5e27 | 8442 passed, 8 skipped, 1 xfailed (8451); 583 slow left out |
| The slow tier of the files touched and of their readers' files, `-n 4 --slow -m slow` (below) | b63d5e27; c4e46309 | 18 passed; 18 passed, the same 18 |

**The final tier beside the base, test by test** (the base's four junit files and the final
tree's four, compared by test id and outcome):

- in the base and not the final tree: none;
- in the final tree and not the base: two, both passed, the steps' own new tests,
  `tests/test_crew_model.py::test_a_company_is_drawn_from_the_spanish_list_in_full` (N1) and
  `tests/test_fight.py::test_the_spanish_kit_is_the_basic_kits_figures_soldiers_and_no_nation_names_it_yet`
  (N3);
- an outcome changed: none; a failure or an error in either: none;
- the skips, the same eight in both, each a test that reads commit f5be9110, which this clone
  lacks: one each in `test_hull_cutter.py`, `test_hull_frigate.py`, `test_hull_smack.py` and
  `test_hull_lugger.py`, and two each in `test_hull_schooner.py` and `test_hull_brig.py`;
- the xfail, the same in both: `tests/test_agents.py::test_an_empty_reply_at_an_urgent_event_counts_and_words_end_the_count`
  (decision 60, package 65, step 2).

**The slow tier.** Neither file I touched has a slow test (`--slow -m slow` collects none in
`tests/test_crew_model.py` or `tests/test_fight.py`). So I ran instead the slow tests of the
readers' files that N1 and N3 ran fast: `tests/test_crew_model.py`, `test_fight.py`,
`test_nations.py`, `test_people.py`, `test_ports.py`, `test_range_audit.py` and `test_service.py`,
whose slow tests are `test_ports.py`'s 7 (the ports and their recruits) and `test_range_audit.py`'s
11 (the audit's sweeps). The final tree: 18 passed (20 min 3 s). The base, the same set: 18
passed (20 min 14 s). Compared by test id, the same 18 with the same outcome. The full slow tier,
all 583, did not run: it is beyond what the brief asks, and the steps touch no ship, no day and no
passage.

`load_ship` and `tools/check_viewer_guns.py` on each new ship file (plan §7.3) do not apply: N1 to
N3 add none.

**Truths.** None was needed; numbers 7-660 to 7-669 are unused.

## 5. The sources used

- Instituto Nacional de Estadística: "Frecuencias de apellidos" (surnames with a frequency of 100
  or more as a first surname, the annual population census at 1 January 2025); "Nombres más
  frecuentes por fecha de nacimiento" (the Padrón continuo at 1 January 2022), its sheets 1 and 3.
  Read on 2026-11-20 (N1).
- *Ordenanzas de Su Magestad para el govierno militar, político, y económico de su Armada Naval*,
  Madrid, Juan de Zúñiga, 1748 (in the tree: `docs/references/signals/spain-1748-ordenanzas-de-su-
  magestad-para-su-real-armada-ocr.txt`): tratado I, título III, art. XLV, p. 42 (the troops
  exercised at the musket and the great gun); tratado I, título V, art. XXXIV, p. 76 (the
  captain's, the officers' and the troops' posts in action, the troops' officer on the poop) (N3).
- Winfield et al. 2023, p. 1446 and following, by `docs/design/VesselReferences-2026-11-Spanish.md`
  §15 (the regulation of 1788's infantry and infantry-artillery) (N3; and for N1's head, the
  company's columns).
- James, *Naval History*, vol. II p. 365, by `docs/design/Design-Ship-Xebec.md` §8.1 (the *África*'s
  38 soldiers) (N3).
- Looked at and not used: a 2024 study of the Trafalgar wrecks off Sanlúcar (Márquez Carmona and
  Jiménez Melero, *Gárgoris* 18, 2024), which names no crews; and the *Estado general de la Real
  Armada* for 1815 (Madrid, Imprenta Real), a scan of 142 pages under CC BY-NC-ND, which was not
  read.

## 6. Other things to know

- The commits' author is the identity this cloud session was given (`git config user.name` and
  `user.email`, as on the trunk's commits), which names a maker. I did not change it, since it is
  neither a file nor a message. The messages carry no trailer.
- The plan's §10.4 has N1 moving no pin. It moves one, `test_the_name_lists`, which pins the set
  of lists (TuningNotes, "Package 90, N1").
- I wait now for the coordinating session's message that the *Diana*'s measuring note has landed,
  and have not begun her file.
