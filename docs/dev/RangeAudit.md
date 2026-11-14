# The range's audit (package 103a)

Decision 69 (docs/DesignProposal.md) fixed a goal that can be checked: a game begun on any
day from 1792 to 1825 finds a world depicted accurately and working. This document is the
measurement of how far the tree is from that, made at the trunk's 504a250 by
`tools/audit_range.py`, with the classing of every dated key of the data and the map of the
research on file. Nothing was mended and no data changed. What it finds is the brief of
milestone 7c's data work and of package 103b's design.

The tool, its known list (`data/range/audit-known.yaml`) and its test
(`tests/test_range_audit.py`) go on measuring: a finding the list lacks fails the test, and
so does a listed finding the sweep no longer makes.

    python tools/audit_range.py --known      # the sampled sweep, against the known list
    python tools/audit_range.py --full       # every day the data names, and many more worlds
    python tools/audit_range.py --classing   # the table of section 2

A figure marked FROM MEMORY is the builder's memory and no source's; a JUDGEMENT is the
builder's own choice.

## 1. How it measures

**Two roads.** The cheap road seeds a day through the game's own readers without making a
world: the nations' table (`nations.load_nations`), each port's dated rows as a scenario
begun that day would find them (`ports.load_port`'s rows through `Port.on_day` and
`Port.nation_on`), the business's rule for a blockade (`business._between` and the table's
wars), the prize court's reading of a war (`prize_court._at_war_at`), the flags', the
days' and the lights' readers. The dear road makes a whole rules-only world on a few days
(a frigate, the business on, the whole chart) for what only a world shows: the vessels the
business draws and what they wear, the blockading squadrons, the lines the world serves of
itself. On every whole-world day the two roads are compared on what both can see (the
holder and the state of each of the 121 ports, the wars, the blockades drawn), so that the
cheap road is proved against the dear one. They agreed on every day tried: no finding of
check (a).

**The days.** A day in every year of the range (1 July, JUDGEMENT) and the days either side of every date the data itself names: a port's dated rows, a war's beginning, the table's own day, a blockade's dates, a prize scheme's, and the first and last years of a flag, a fashion, a national day and a light. That is 202 days (168 of the data's naming, 34 of the years'). The findings that rest on the reference are looked for on those days and on the days either side of the reference's own dates as well, 323 in all; the mechanical findings never on the reference's days. `--full` adds every national day in every year of the range with the day after it (1146 days; 1256 with the reference's). Whole worlds: 4 in the sampled sweep (off Ushant on 1 July 1792, off Rochefort on 1 July 1802 and 1805, off Cadiz on 1 July 1814) and 138 in the full one (off Ushant, Rochefort and Cadiz on 1 July of every year; off Gibraltar, Toulon, Leghorn and Malta every fourth year). Deterministic: the same seed and tree give the same findings.

**The reference.** The tree is silent on which wars and which nations are a day's own (its
table is June 1805's, with no end to any war and no lifetime to any nation), so without a
measure the audit could say only "undated". By the lead's ruling the audit carries
`data/range/reference.yaml`: the wars and peaces between the nations the table names, the
general peaces, and those nations' lifetimes, every row marked FROM MEMORY with the
writer's confidence unless the tree already cites a work for it. It is not research and
not the game's data; nothing under `freesail/` reads it. A finding that rests on it is a
kind of its own (`basis: reference`, its key beginning `r-`, its owner "a judgement to be
read against a source"), counted and listed apart. The mechanical findings are the same
with the reference thrown away (`--no-reference`; the test holds it).

**What a finding is.** A key (the check and what it is of, never a count or a day), what
it is in words, the years of the sampled days it bites, a count of the things concerned,
and an owner: a data fault for milestone 7c, an engine fault, or a judgement to be read
against a source. The findings are stated as the tool makes them.

## 2. Every dated key of the data, classed

The tool scans every YAML file under `data/` (less the chart's tiles and coast, which hold
no words, and the audit's own two files) for a key that carries a year or a date: a date,
words that name a year, a whole number of a year under a key whose name is a date's, and a
key whose own name carries a year (a fit's). At 504a250 it finds 5,545 such values, in 29 of the table's 30 rows: 4,496 words, 249 script, 235 calendar-read, 207 the builders' own date, 142 read by nothing, 74 both by the scenario's choice, 54 seed, 48 a name carrying a year, 40 words, served. Every one is in a row of the table
below, which the tool holds as data (`CLASSING`) and prints (`--classing`); a key in no row
is a finding (`c-unclassed`), and truth 7-591 holds the table complete.

The classes:

- **seed**: read once, on the scenario's first day, into state that play then owns.
- **calendar-read**: read against the running clock while the game runs.
- **both by the scenario's choice**: a seed, and under `Scenario.follows_history` also put
  to the record's row on each day a row begins or ends.
- **script**: a scenario author's own timed script.
- **read by nothing**: the data carries it and no code reads it as a date.
- **words** and **words, served**: a source, a note, a title; "served" where the builder
  reads the code as giving the words to a player or a model (JUDGEMENT).
- **a name carrying a year**, **the builders' own date**: a fit's or a feature's name; the
  day a builder fetched or checked something.

| Row | Files (under data/) | Keys | Class | How it is read | What play could change that the clock would put back |
|---|---|---|---|---|---|
| port-holder | `ports/*.yaml` | `nation.#.since`, `nation.#.until` | both by the scenario's choice | `ports.load_port` puts the row of the scenario's first day into `Port.nation`; under `follows_history` `Ports.tick` and `Port.on_events` put it to the record's row on each day a row begins or ends | a port taken or given up in play is the record's holder's again on the next day one of its rows begins or ends (no order takes a port yet; decision 69 (c) means one will) |
| port-dated-keys | `ports/*.yaml` | `state.#.since`, `state.#.until`, `dockyard.#.since`, `dockyard.#.until`, `closed_to.#.since`, `closed_to.#.until` ... | both by the scenario's choice | `ports.load_port` (`_dated_rows`, `_value_on`) on the first day; `Port.on_events` under `follows_history` | the director's `port <id>: closed to` and `open to`, a price order, and whatever play does to a yard, a pilot or a crew's pool are overwritten on the next day a row of that key begins or ends |
| port-blockade-since | `ports/*.yaml` | `blockade.since`, `state.#.blockade.since` | words, served | kept as words (`ports._port_state`) and said by `Ports.blockades`; read as no date | - |
| port-pilot-words | `ports/*.yaml` | `pilot.words.*`, `pilot.#.pilot.words.*` | words, served | the pilot's own words, said as he comes aboard | - |
| port-words | `ports/*.yaml` | `*source`, `*sources.#`, `*source.*`, `*note`, `*notes`, `*notes.#` ... | words | a source or a note | - |
| nations-as-of | `nations.yaml` | `as_of` | words, served | `nations.load_nations`; printed by `Nations.sailed_with_words` as the day of the table she sailed with, whatever the scenario's day; read as no date | - |
| wars-since | `nations.yaml` | `wars.#.since` | calendar-read | `Nations.at_war` (the stance, the business) ignores it; `prize_court._at_war_at` reads it against the day of the taking | a war the world is in by its table is no war to the prize court before the record's day, and a war declared in play (`Nations.declare_war`) carries its day in words or none, which the court reads as never or as always |
| blockades-dates | `nations.yaml` | `nations.*.naval.blockades.#.since`, `nations.*.naval.blockades.#.until` | both by the scenario's choice | `business._blockades` with `business._between`: the scenario's first day, or the running day under `follows_history`, when a region is peopled | a blockade raised or laid in play is drawn again or not by the record's dates the next time the region is peopled, under `follows_history` |
| nations-relations | `nations.yaml` | `nations.*.relations.*` | read by nothing | nothing: `load_nations` does not take the key; war and peace between the later nations stand only in these words | - |
| nations-colours-words | `nations.yaml` | `nations.*.colours`, `nations.*.flag` | words, served | `Nation.colours` and `Nation.flag`, the lookout's words for a ship's colours | - |
| nations-words | `nations.yaml` | `*source`, `*source.*`, `*.source`, `*.sources.*` | words | a source | - |
| prize-shares | `business.yaml` | `prize_shares.#.from`, `prize_shares.#.until` | calendar-read | `prize_court.scheme_for`, by the day of the court's sentence | - |
| colours-dates | `signals/*/colours.yaml` | `flags.#.dates`, `nations.*.flags.#.dates` | read by nothing | parsed into `flags.Flag.dates` and read by nothing: a ship wears the flag her occasion names whatever the year | - |
| signal-flags-dates | `signals/*/flags.yaml` | `flags.#.dates` | calendar-read | `flags.SignalFlagsFile.drawing_of` by the running year (`api/viewer_flags.py`); with no row for the year, the nearest | - |
| dressing-dates | `signals/*/dressing.yaml` | `fashions.#.dates` | calendar-read | `flags.fashion_for` by the running year; with no row for the year, the nearest earlier | - |
| days-years | `signals/*/days.yaml` | `days.#.years`, `days.#.date` | calendar-read | `flags.days_on` by the running day (`flags.dressing_tick`) | a king dead or a government fallen in play: his day is kept, or dropped, by the record's years regardless (nothing in play does either yet) |
| signals-words | `signals/*/*.yaml` | `*source`, `*sources.#`, `*source.*`, `*note`, `*notes`, `*notes.#` ... | words | a source | - |
| lights-years | `charts/features/*.yaml` | `features.#.lit.from`, `features.#.lit.until` | calendar-read | `chart.Feature.lit_in` by the running year (the lookout, the browser's map) | - |
| feature-names | `charts/features/*.yaml` | `features.#.id` | a name carrying a year | a feature's id, a name only | - |
| feature-words | `charts/features/*.yaml` | `features.#.says`, `features.#.lit.character`, `features.#.modern`, `features.#.fix`, `features.#.view`, `features.#.name` ... | words | a mark's words: `says` is served only for the shore and a point of interest, a light's `character` and `modern` to nobody | - |
| scenario-start | `scenarios/*.yaml, scenarios/trials/*.yaml, regatta/*.yaml` | `start`, `start.at` | seed | `scenarios.load_scenario`: the clock's first day, the day every seed above is read on | - |
| scenario-papers | `scenarios/*.yaml, scenarios/trials/*.yaml` | `papers.almanac`, `papers.chart.year` | read by nothing | kept in `Scenario.papers`; no code reads either (the almanac's figures are computed from the clock) | - |
| scenario-chronometer | `scenarios/*.yaml, scenarios/trials/*.yaml` | `papers.chronometer.rated` | seed | `reckoning.Chronometer.from_scenario`: the day she was rated, counted from | - |
| scenario-script | `scenarios/*.yaml, scenarios/trials/*.yaml, director/briefs/*.yaml` | `weather.wind.#.at`, `weather.systems.#.track.#.at`, `weather.#.at`, `world_orders.#.at`, `world_orders.#.order`, `examples.#` | script | the author's own timed script (the weather's, the world's orders) | - |
| scenario-nations | `scenarios/*.yaml, scenarios/trials/*.yaml` | `nations.as_of`, `nations.wars.#.since` | read by nothing | `scenarios._nations_block` reads and keeps it (`Scenario.nations`); the World loads the table's wars whatever it says (no shipped scenario carries the block) | - |
| ship-fit-names | `ships/*.yaml` | `armament.default`, `armament.fits.*`, `ship.descriptions.*.fit` | a name carrying a year | a fit's name; no reader takes the year from it (`ships.vessel_from_spec` takes the description's fit whatever the day) | - |
| ship-words | `ships/*.yaml` | `ship.era_notes` | words, served | the ship's own account of herself, served by the reading of her particulars | - |
| people-words | `people/*.yaml` | `wardroom.#.brief`, `wardroom.#.history` | words, served | an officer's brief and his history, served to whoever holds his station | - |
| chart-provenance | `charts/*.yaml, charts/overrides/*/*.yaml` | `*` | the builders' own date | the chart's manifest, its overrides, its checks and its audit's list: where a tile or a sounding is from and the day a builder fetched or checked it; nothing of the world's days (JUDGEMENT: these files are classed whole) | - |
| words | `*` | `*source`, `*sources.#`, `*source.*`, `*note`, `*notes`, `*notes.#` ... | words | a source, a note or a title; not served as the world's word of a day | - |

**What the table says, shortly.**

- Only the ports are seeded by the day: their holder and their six dated keys. Of 121
  port files 20 give the holder as rows (13 with dates, the seven Canaries files one row
  that says "through the range"), Valletta dates its state, its yard and its pilot, and
  Messina its yard and its pilot. No file dates a closure, a market or a crews' pool.
- The wars are not seeded at all. The World loads the table of June 1805 whole on any
  first day; the stance and the business read no date; the prize court alone reads a war's
  `since`, against the running clock.
- Read against the running clock, and nothing in play can change them today: the lights'
  years, the signal flags' drawings, the fashion of dressing, the national days, the prize
  shares. These are the calendar's own and are no fault under decision 69 (c), unless play
  is one day to kill a king or change a government (the days) or make law (the shares).
- Read by nothing: the national colours' `dates` (a ship wears her occasion's flag
  whatever the year), a scenario's `papers.almanac` and `papers.chart.year` (set by 46
  scenarios), the nations' `relations` (where the later nations' wars stand in words), and
  a scenario's own `nations:` block.
- `Port.on_day` and `Port.nation_on`, which put a port to a day whatever play has made of
  it, have no caller in `freesail/`. The audit uses them, as the readers "that set a port
  to a day by design".

**The list package 103b needs: what the clock would put back.** Decision 69 (c): what play
owns, the calendar must not snap back. Five rows of the table are read against the running
clock (always, or under `follows_history`) and govern something play could change. Each is
a finding (`c-snap-back:`), owned as an engine fault for the design:

| Row | What play could change | What the clock then does |
|---|---|---|
| `port-holder` | a port taken or given up (no order does it yet; decision 69 (c) means one will) | under `follows_history`, the next day one of the port's rows begins or ends, `Port.on_events` sets the holder to the record's |
| `port-dated-keys` | the director's `port <id>: closed to` and `open to`, a price order; in time a yard, a pilot, a crews' pool | under `follows_history`, the next event of that key overwrites it; a key with no event keeps what play made |
| `blockades-dates` | a blockade raised or laid | under `follows_history` the business reads the running day when it next peoples the region and draws by the record's dates |
| `wars-since` | a war declared or a peace made (`Nations.declare_war`, `make_peace`; no caller in `freesail/` yet) | the prize court reads the war's `since` against the day of the taking: a war of the table is none to the court before the record's day, and a war declared in play carries its day as words (read as never at war) or as nothing (read as always) |
| `days-years` | a king dead, a government fallen | the day is kept, or not, by the record's years; nothing in play does either yet |

Not on the list, because nothing in play can change what they govern: the lights, the
signal flags, the fashion of dressing, the prize shares. JUDGEMENT: a prize is shared by
the scheme of the day of the court's sentence, not of the taking; the two can fall either
side of 1 January 1808.

## 3. The findings

The full sweep makes **105 findings: 66 mechanical and 39 that rest on the reference**. The sampled sweep (the fast tier's) makes all of them but one, which only the full sweep's worlds off Leghorn show (`r-vessel:etruria`).

| Owner | Mechanical | Reference |
|---|---|---|
| a data fault for milestone 7c | 46 | 0 |
| an engine fault | 20 | 0 |
| a judgement to be read against a source | 0 | 39 |
| all | 66 | 39 |

**By check** (the full sweep):

| Check | Findings | What they are |
|---|---|---|
| (p) the ports | 9 | seven keys no file dates, by key; Cadiz's own blockade, in words and before its year |
| (w) the wars | 11 | three wars before their beginning, the same three before the court, no end to any, three wars that stand only in words, the scenario's block unread |
| (b) the blockades | 1 | Brest's blockade undated |
| (v) the vessels and their fits | 6 | six fits of a later year than the day |
| (f) the flags | 7 | five nations' colours out of their dates, one form of dates unreadable, Britain's signal flags without a drawing |
| (d) the national days | 2 | thirteen nations with no day, France's year with none |
| (l) the lights | 1 | twelve lights dated by the year alone |
| (x) the words served | 6 | the table's day, and five kinds of served words that name a year to come |
| (e) years fixed in the code | 5 | five files |
| (u) what no data dates | 10 | ten elements with no dates |
| (c) the classing | 8 | five keys the clock would put back, three read by nothing |
| (r) the reference | 39 | 4 `r-blockade`, 3 `r-holder`, 5 `r-nation`, 1 `r-port-blockade`, 1 `r-vessel`, 22 `r-war-absent`, 3 `r-war-at-peace` |
| (a) the two roads agree | 0 | no disagreement on any of 138 whole worlds |

**By year** (how many findings bite a day sampled in the year; the full sweep):

| Year | Mechanical | Reference | | Year | Mechanical | Reference |
|---|---|---|---|---|---|---|
| 1792 | 63 | 20 | | 1809 | 45 | 21 |
| 1793 | 63 | 22 | | 1810 | 45 | 21 |
| 1794 | 61 | 20 | | 1811 | 46 | 21 |
| 1795 | 58 | 20 | | 1812 | 47 | 23 |
| 1796 | 55 | 18 | | 1813 | 46 | 22 |
| 1797 | 55 | 13 | | 1814 | 45 | 24 |
| 1798 | 55 | 17 | | 1815 | 44 | 20 |
| 1799 | 55 | 15 | | 1816 | 44 | 19 |
| 1800 | 54 | 16 | | 1817 | 45 | 13 |
| 1801 | 53 | 14 | | 1818 | 46 | 13 |
| 1802 | 53 | 13 | | 1819 | 46 | 13 |
| 1803 | 53 | 12 | | 1820 | 46 | 14 |
| 1804 | 48 | 8 | | 1821 | 46 | 13 |
| 1805 | 46 | 7 | | 1822 | 47 | 13 |
| 1806 | 44 | 10 | | 1823 | 47 | 14 |
| 1807 | 45 | 15 | | 1824 | 46 | 15 |
| 1808 | 45 | 21 | | 1825 | 47 | 13 |

The mechanical count falls from 1792 to 1805 and is nearly level after it: the tree is a
picture of June 1805, the early years lack what 1805 has (the wars' beginnings, the fits of
1795 and 1796, the Union of 1801), and the later years mostly lack nothing the tree can
see, because nothing in it ends. The reference's count is lowest in 1804 and 1805, the
years the table was written for, and highest in 1792 to 1795 and 1808 to 1814.

The whole list, each finding with its owner and its reason, is
`data/range/audit-known.yaml`.

## 4. The ten that matter most to a player beginning on an arbitrary day

JUDGEMENT throughout: the order is the builder's, by how soon a player meets the fault and
how wrong the world is when he does.

1. **The wars are June 1805's on every day** (`w-no-end`, `w-before-since:` three,
   `r-war-at-peace:` three, `r-war-absent:` 22). Britain is at war with France,
   Spain and the Batavian Republic from 1792 to 1825. By the reference, a player in 1793
   finds Spain an enemy when she was an ally, in 1802 no peace of Amiens, in 1808 the
   Spanish ports still hostile, in 1813 no American war, in 1820 a French war five years
   over. Every stance, every blockade, every prize and every price that reads the war
   follows from it.
2. **A scenario cannot say otherwise** (`w-block-unread`). The one lever an author has to
   give a day its own wars, the scenario's `nations:` block, is parsed, kept and read by
   nothing: a world begun with a block of no war at all is at the table's three wars.
3. **The stance and the prize court disagree before 1803 and 1804** (`w-court:` three).
   The court alone reads a war's beginning: before 18 May 1803 a French ship is an enemy
   to the lookout, to the pilot and to the guns, and no enemy to the court, which would
   restore her.
4. **Blockades in years of peace, and one that never lifts** (`b-undated:britain:brest`,
   `p-blockade-before:cadiz`, `p-blockade-words:cadiz`, `r-blockade:` four,
   `r-port-blockade:cadiz`). Brest's blockade has no dates and is drawn on every day; a
   world begun on 1 July 1792 off Ushant has the squadron on its station. Cadiz is
   blockaded in its own file on every day from 1792 to 1825, and Ferrol's, Cadiz's and
   Lorient's entries have no end.
5. **Nations with no lifetime** (`u-nations`, `r-nation:` five, `r-holder:` three). The
   Batavian Republic is Britain's enemy in 1792, three years before it was, and in 1825,
   nineteen after it ceased; Leghorn is Etruria's and Genoa Liguria's in 1792; the states
   that held those places before and after are not in the table at all.
6. **Most ports are held as in 1805, with nothing to say so** (`p-undated:nation`, 101
   ports; `p-undated:closed_to`, `market`, `crew_pool`, 121 each). The audit cannot see
   which of these are wrong, only that the file does not say; section 5 lists, FROM
   MEMORY, the holders a player would miss first (Toulon in 1793, Corsica in 1794 to
   1796, Minorca in 1798 to 1802, Lisbon in 1807 and 1808).
7. **The ships are of 1795 and after** (`v-fit-ahead:` six, `u-ships`). The business
   draws the frigate of the Amazon class of 1795 and the brig-sloop of 1796 in 1792; no
   ship file carries a year as data, and the fits on file leave 1797 to 1811 and
   everything after 1815 with no ship of their own.
8. **The colours are worn whatever the year** (`c-unread:colours-dates`, `f-colours:`
   five, `u-colours-words`). The colours' dates are read by nothing: British ships wear
   the Union of 1801 in 1792 (seen worn by the vessels of the whole world begun that
   year), France the tricolour ensign of 1794 before it, the United States the fifteen
   stars after 1818. What France wore after 1814 the data does not hold at all.
9. **Words that give the game away** (`x-as-of`, `x-words:` five). The table she sailed
   with is said to be of "1 June 1805" on every day. The officers' briefs cite the
   Regulations of 1806 and a seamanship of 1884 inside the words a station's holder is
   given; a ship's account of herself names later years.
10. **The books, the regulations and the days are one for the range** (`u-books`,
    `u-regulations`, `d-none`, `f-signal-nearest:britain`). Popham's telegraph of 1803
    and the Regulations of 1806 serve 1792; thirteen of sixteen nations keep no day;
    Britain's numeral flags have no drawing after 1810 and are served 1810's.

Not among the ten, and for package 103b rather than a player: the five keys the clock
would put back (section 2), and the years fixed in the code (`e-year:` five files, where a
scenario, a clock or a year is wanting and the code answers 1805).

## 5. What the sweep cannot see

**What is true only in words.** The sweep reads words only to find a year in them. It
cannot tell that a pilot's directions name a mole not yet built, that a hail or a brief
speaks of "the Emperor" in 1795 or of "His Majesty's" ship under a regency, or that a
port's description is of the town as a book of 1826 found it. Nearly every port's file is
drawn from pilots of 1787 to 1849 read as one. The primers and the agents' briefs under
`docs/` are served to a model and are not swept at all.

**What no data dates at all, beneath the ten findings of check (u).** Each of those says an
element has no dates; none can say what the dates would change. Under them, and seen by
nothing: a port's works (a breakwater, a fort, a lazaretto, a dock begun within the range),
its fees and its prices; the habits of each nation in action; what an officer or a
government is called; the instruments, the epitome and the chart a master carries in a
given year; what a ship of a given year had aboard her that an earlier one had not; and
what the sea itself carried by the 1820s (FROM MEMORY: steam packets on the Channel
crossings before the range's end).

**Whether an undated value is wrong.** `p-undated:nation` counts 101 ports whose holder is
one word. For most the word is right through the range (Falmouth, Brest). The audit
cannot tell those from the ones below, which are the builder's memory and the helpers'
reading of the files' own comments, set down so that 7c knows where to look first. All
FROM MEMORY, none checked:

- Toulon: held by the allies from late August to 19 December 1793.
- Corsica's ports (San Fiorenzo, Bastia, Ajaccio): the British kingdom of Corsica, 1794
  to October 1796 (the three files' own comments say so, from memory).
- Port Mahon: British from November 1798 to the peace of Amiens, given up in 1802.
- Porto Ferrajo: Tuscan, a British garrison in 1796 and 1797, French from 1802, Napoleon's
  own from May 1814 to February 1815.
- Leghorn: Tuscan before 1801, occupied by the French in 1796 and again from 1799 and
  1800; a French department's port from 1808 to 1814; Tuscan again after.
- Genoa: France's in its file from June 1805 with no end; a republic again for some months
  of 1814 and the King of Sardinia's from 1815.
- Naples and Gaeta: the French and the Parthenopean Republic in the first half of 1799;
  Joseph's and Murat's kingdom from 1806 to May 1815 (Reggio and Scilla are dated so;
  these two are not).
- Civita Vecchia: the Roman Republic's in 1798 and 1799, France's from 1809 to 1814.
- Lisbon, Setubal, Oporto: the French from November 1807 to the late summer of 1808,
  Oporto again in the spring of 1809.
- Corunna and Ferrol: the French in the first half of 1809; Santander from 1808 to 1812;
  Malaga and Almeria from 1810 to 1812; Cadiz besieged from 1810 to 1812 and never taken.
- Funchal: a British garrison in 1801 and 1802 and from 1807 to 1814.
- Oran: Spain's until it was given up to Algiers in 1792 (the first weeks of the range;
  `algiers.relations.spain` says so, from memory).
- La Calle: the French company's until 1799 or after, a British concession from 1807.

**What happens once the clock runs.** The sweep begins worlds and does not sail them. The
five keys the clock would put back are found by reading the code, not by play; what the
business draws on later days, what a port does when its row changes under
`follows_history`, and whether a world at peace has anything to do (decision 69 (d)) are
not measured.

**Beyond the stations.** Whole worlds were begun at seven places in seven of the chart's
twenty regions; what the business draws in the other thirteen is unseen.

**Outside `freesail/` and `data/`.** The browser's map falls back to the year 1805 where a
snapshot gives none (the client's `map.js`); the check of the code's years reads Python
only.

## 6. The research on file, mapped

No new research was done. This is what `docs/references/` (its README the index) and the
design notes already hold, by element and by year, from the second helper's reading (kept
whole in docs/dev/TuningNotes.md, package 103a). "Held" means a work on file speaks to the
years; "thin" one work, or a work of another year stretched; "bare" nothing on file.

| Element | 1792-94 | 1795-97 | 1798-1801 | 1802-03 | 1804-06 | 1807-09 | 1810-12 | 1813-15 | 1816-25 |
|---|---|---|---|---|---|---|---|---|---|
| Ports: holders, works, pilots | thin | thin | thin | thin | held | thin | thin | thin | thin |
| Ports: market prices | bare | bare | bare | bare | bare | bare | bare | bare | bare |
| Nations and wars, Britain's | thin (1792 bare) | held | held | held | held | held | held | held | thin |
| Nations and wars, the others' | thin | thin | thin | thin | thin | thin | thin | thin | thin |
| Ships, British | held | held | held | held | held | thin | thin | held | thin |
| Ships, other navies | thin | thin | thin | thin | thin | thin | thin | thin (American held) | bare |
| Flags and signals | held | held | held | held | held | thin | thin | thin | thin |
| Regulations, British | thin | thin | thin | thin | held | held | held | held | thin |
| Regulations, other nations | thin | bare | thin | thin | thin | bare | bare | thin | thin |
| Lights | thin | thin | thin | thin | held | bare | bare | thin | thin |
| The trade | thin | thin | thin | thin | thin | thin | thin | thin | thin |

JUDGEMENT (the helper's, and the builder agrees): "held" for Britain's wars means James's
Naval History is on file and covers them, not that any row of data cites it for a war. The
works on file are richer than the data made from them.

**By element, what is on file.**

- **Ports.** The pilots and directions: Faden 1793, Moore 1799, the Oriental Navigator
  1801, Norie 1805, Grasset 1807, Smyth 1824 and 1828, Purdy 1825 and 1826, with Tofiño
  1787 before the range and White 1835, Norie 1831, Purdy 1840, Bérard 1837, Lamberti
  1844, the Derrotero of 1849, Smyth 1854 and Imray 1874 after it. James (1793 to 1827) is
  the only work on file that dates who held a port; the dated rows of Valletta, Scilla,
  Rosas and Barcelona cite it, and their other dates are from memory.
- **Nations and wars.** James; Hertslet 1820 (the treaties of 1814 to 1816 and the
  Barbary treaties); Shaler 1826, Carey 1794, Foss 1798 and Ray 1808 for the regencies;
  Niles, Roosevelt and Coggeshall for 1812 to 1815; Nicolas to about 1797. The table's own
  three dates are from memory.
- **Ships.** Steel 1794 and 1805, Charnock 1802 (the British ships by rate to 1801), Lever
  1808, Falconer 1780, Röding 1794; Adye 1804 and Douglas for the guns; Jackson's Logs,
  Osler, James, Chapelle, Cobb. No list of any navy after 1801; no French, Spanish, Dutch
  or Danish man of war.
- **Flags and signals.** Perrin 1922 (every change of the British flags), Bowles 1795,
  Fisher [1820], Preble 1894, Babron 1817, France's law of 1790; the Admiralty's books of
  1796 and 1799, Popham 1803, Corbett; Mazarredo 1781 and 1799, Audibert 1802, Barry 1800,
  Naples 1807. No British book after 1803, no French after 1802.
- **Regulations.** The Regulations and Instructions of 1806; the prize cases of 1809 to
  1822 (Acton, Dodson); the slave-trade Acts of 1788 to 1820. The Regulations of 1790 are
  not held; the prize shares rest on a work cited and not held.
- **Lights.** Norie 1805 for the Channel's lights in that year; Purdy 1840 and the later
  pilots for dates; 21 feature files cite pages read online and not held.
- **The trade.** The goods from Purdy 1826 and Norie 1831; two prices (Steel); the
  fisheries from Holdsworth 1874; the convoys from the Regulations of 1806, James and
  Niles. `data/business.yaml` says of itself that every figure is judgement.

**Where the range is bare: what milestone 7c would have to find.**

1. The wars and the peaces, by day, with their sources: none is in the data before May
   1803 or after December 1804 and none ends. James on file covers most of Britain's and
   has not been read for them; Hertslet covers 1814 to 1816. The wars between the other
   nations want a history the repository does not hold.
2. The states the table lacks: the Dutch before 1795 and after 1806, Tuscany and Genoa
   before their kingdoms and after, Murat's Naples, the Porte, Tripoli, Russia, the Empire.
3. Who held each port, for the hundred that do not say: James for the British years; for
   the Peninsula from 1808 to 1814 a work not on file.
4. A price for any year: of 1,405 rows of goods one carries a price of the period.
5. The lights from 1806 to 1824: no list of lights is on file for those years.
6. Britain's flags before 1801 (Perrin, on file, has them and they are not built);
   France's from 1814; a British signal book after 1803 and a French one after 1802.
7. The regulations before 1806, the prize acts, the convoy acts.
8. A navy list after 1801, and ships of other navies.
9. The years before February 1793 and after 1815, in every element.

## 7. What it cost to run

Measured on the build's container (four cores, one process, 2026-11-14), at the tree of
504a250:

| What | Cost |
|---|---|
| The sampled sweep (`python tools/audit_range.py`) | about 20 s: the tree read in 0.6 s; every check of the cheap road over 202 days (323 with the reference's) in under half a second together, but the reading of the code for its years, 2 s; four whole worlds 15 s (two to six seconds each) |
| The fast tier's test (`tests/test_range_audit.py`, 18 tests) | about 25 s on one worker: the sampled sweep once (20 s), the sweep twice over for sameness (3 s), the rest under 2 s |
| Truths 7-590 to 7-592 | 3.4 s together |
| The full sweep (`--full`) | 11 min 18 s: 138 whole worlds 672 s; the cheap road over 1,146 days about 3 s |
| The slow tier's tests | the full sweep against the known list 674 s; the two loaders file for file 4.5 s |

The dear road is all of the cost. A whole world by the game's own YAML loader takes ten to
nineteen seconds; the audit swaps in libyaml's loader for its own run (section 8) and a
world then takes two to six, the rest being the business peopling its region. The lead
asked for about six whole worlds in the fast tier within about thirty seconds; four fit
(each chosen for a year the others do not show), and six would not.

In the building: two read-only helpers, one for the readers of each dated key and one for
the map of section 6 (their reports are in docs/dev/TuningNotes.md); no paid call, nothing
downloaded, nothing fetched from the network.

## 8. Corrections to the ground report, and what was found for others

The ground report to the lead (before anything was built) said two things the building
corrected:

- It said some 150 lights' words ("not yet built in 1805") are served on any day. They
  are not: a feature's `says` is served only for the shore and a point of interest
  (`lookout._line_data`), and a light's `character` to nobody. They are classed as words,
  not served, and make no finding.
- It put 1793's Union of 1801 down to the flags' nearest-year answer. The signal flags
  answer so; the national colours do not come to it, because their dates are read by
  nothing.

Found for others and not mended (each is in the known list or said here):

- **The engine.** The scenario's `nations:` block read by nothing; the prize court and the
  stance disagreeing before a war's `since`; `Nations.declare_war` writing a day the court
  cannot read (the first helper's reading, not measured); the colours' dates read by
  nothing; `papers.almanac` and `papers.chart.year` read by nothing; five files with 1805
  fixed in them; `Port.on_day` and `Port.nation_on` with no caller.
- **The data.** Naples's ensign's dates in a form the engine's reader of dates would
  refuse (`-1806, 1815-`); the Cadiz blockade's beginning in words; the wars written under
  `relations` and not in the table (Algiers and Portugal, the Order and the regencies).
- **The pace.** A whole world on the full chart takes ten to nineteen seconds to make by
  the game's own YAML loader, most of it in reading ship files: `ships._default_fit`
  reads the vessel's ship file again for every vessel drawn. With libyaml's loader the
  same world takes two to six seconds. Not mended; the audit uses the quicker loader for
  itself alone.
