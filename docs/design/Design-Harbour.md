# The harbour, designed (package 96a)

Written 2026-11-15 from the scope card the owner agreed that day (`docs/dev/ScopeCards-BeforeTheGate.md`, card 1). A design document only: no code, no data and no other document was changed. The trunk read is `claude/dreamy-darwin-d77nty` at `66ef77e`.

**What this document concludes, in five lines.**

1. Of 118 things the game can be told at its start, the page reaches 51 today, 53 want a file edited or a flag typed, and 14 cannot be told at all (section 1).
2. Nearly all of the 53 can be put on the page without touching how the game reads a scenario, because the page already keeps what it does not show. The 14 cannot: they are the deeper layer, and they are named as questions (sections 1.4 and 5).
3. The experienced player's page is one sheet per scenario, folded: each part says in a line what is set, and opens in place. Every ship is set up on the same card (section 2).
4. The newcomer's page is a first panel with one game named on it, the four lessons under it, and the tests' and gates' scenarios taken off the list (section 3).
5. The build before the gate is about nine to twelve working days in eleven steps, all "the page only". That is at the edge of the card's two weeks, so the steps are marked with the six that the gate needs (section 4).

**How it was made.** I read the loader (`freesail/world/scenarios.py`, `load_scenario`, whole), the page (`freesail/ui/harbour.py`, `client/harbour.html`, `client/harbour.js`, each whole), the settings (`freesail/settings.py`), and the flags of the server, the console and the three doors. Two readers traced each scenario key downstream to the code that uses it, and counted the keys the 53 scenario files use. I started the harbour once on a settings file and a saves folder of my own in a scratch place, looked at each of its four tabs, read the blockade's scenario into the maker and stopped the server. Nothing of the owner's was read or changed. What I could not determine is in section 6.

---

## 1. The inventory

**Conclusion.** The page was built when a scenario was one ship, a wind and a few other sail. Everything that has arrived since (squadrons, the papers, the people, a ship's fit and role, the year, the director's grant, several models) is read by the game and absent from the page. Three things the page appears to offer do nothing, and four things a scenario file may say are read by nothing: these are traps for the owner at the gate and are listed in 1.3.

**How to read the tables.** Each row is one thing the game can be told. The third column says where it stands today:

- **Page**: it can be set from the harbour's page.
- **File**: the game reads it, and it can only be set by editing a scenario or the settings file by hand, or by a flag typed on the command line.
- **None**: nothing the player can write sets it.

The last column says where I found it. "maker" is the scenario maker's tab; "start form" is the "A new game" panel.

### 1.1 Starting a game, and the game's own settings

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 1 | Which scenario to play, the game's or one of yours | Page | start form "Scenario"; `--scenario`; `harbour.py` `Harbour.start` |
| 2 | A bare ship on open water, with no scenario | Page | start form "a ship file"; the server's `ship` argument. The list also offers the five ship's boats (`data/ships/boat-*.yaml`) |
| 3 | A saved game taken up again | Page | start form "a save": the name must be typed, there is no list; `--load`; `ui/places.py` `save_to_load` |
| 4 | A save of an older build replayed anyway | File | flag `--replay-anyway` (`ui/server.py`) |
| 5 | The seed | Page | start form "Seed"; `--seed` |
| 6 | The station you sit at (captain, officer, master, lookout, passenger, director) | Page | start form "Your seat"; `--seat` |
| 7 | Which ship you are aboard at the start, when it is not your own | File | flag `--ship NAME` (`ui/console.py` `ABOARD_HELP`); `Harbour.start` does not pass it |
| 8 | How fast the clock runs (compression) | Page | start form; `--time` |
| 9 | The pace: the pace rule, lockstep, or free-running | Page | start form "Pace"; `--lockstep`, `--free-running` |
| 10 | The clock eased to 1x when a station is sampled or speaks | Page | start form tick box; `--ease-on-station` |
| 11 | How many other ships are fully crewed at once, and within how many miles | Page | start form "Crewed cap", "Crewed range"; `--crewed-cap`, `--crewed-range` |
| 12 | The sea's business (trade, fishermen, cruisers) on or off over the scenario | Page | start form "Business"; `--business` |
| 13 | A director's brief given at the start | Page | start form "Director's brief"; `--director-brief` |
| 14 | A book of standing orders read at the start | Page | start form "Standing orders"; `--standing-orders` |
| 15 | The wind for a bare ship | File | flag `--wind FROM,KNOTS` |
| 16 | The heading for a bare ship | File | flag `--heading` |
| 17 | The scripted watcher stationed | File | flag `--watcher fake` |
| 18 | The address the server answers at (to play from another device) | File | flag `--host`, or `server: host` in the settings file; not on the settings form |
| 19 | The server's port, and whether the browser opens | Page | settings tab; `settings.py` `server` |
| 20 | Your usual seat, compression, pace and crewed budget | Page | settings tab "The game's defaults"; `settings.py` `game` |
| 21 | Where saves are kept | Page | settings tab "Saves"; `places: saves`; taken at the server's next start (`ui/places.py`) |
| 22 | Where your own scenarios are kept | Page | settings tab; `places: scenarios` |
| 23 | Where the consent records are read and written | Page | settings tab; `places: consent_records`; `--consent-records` |
| 24 | Which settings file is used (a second profile) | File | flag `--settings`, or the variable `FREESAIL_SETTINGS` |

### 1.2 The doors, the stations and the models

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 25 | The desktop client's model name, command and wait | Page | settings tab; `doors.desktop` |
| 26 | The desktop client's entries written, one per station ticked | Page | doors tab; `Harbour.desktop` |
| 27 | The API door's model, dialect and effort | Page | settings tab; `doors.api` |
| 28 | The other models the API door may call (for a director's seats) | File | `doors.api.models` in the settings file (`settings.py` `callable_models`); not on the form |
| 29 | Where a director's seat's door folds its conversation | Page | settings tab "Seat's fold"; `doors.api.seat_budget_tokens` |
| 30 | The local runner's address and model | Page | settings tab; `doors.local` |
| 31 | A door's own choices (how often it is sampled, play or test, pictures, the consent question put again, the context, the reply's length) | Page | settings tab "Flags", as one line of raw flags with no explanation (`agents/api.py`, `agents/local.py`: `--cadence`, `--session`, `--pictures`, `--ask-again`, `--ctx`, `--max-reply`) |
| 32 | A door started at a station of your ship | Page | doors tab; `Harbour.start_door` |
| 33 | A door started at a station of another ship | Page | doors tab "On another ship"; the door's `--ship` |
| 34 | Two different models at two stations in one game | File | one model per door in the settings, so a second settings file (`--settings`); the owner's point of 2026-10-18, still true |
| 35 | The API door's key put in the credential store | File | `py -m freesail.agents.api --store-key`. By design: no key passes through the page |
| 36 | A shortcut that starts the harbour | Page | settings tab |

### 1.3 The scenario

**The day and the place**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 37 | The scenario's name and seed | Page | maker "The day"; `name`, `seed` |
| 38 | The day and hour it begins, and so the year | Page | maker "Start"; `start` |
| 39 | The ports as they stood on that day (who held each, its pilot, market and dockyard, a blockade) | Page | follows from `start` with nothing more said (`world/ports.py` `load_port`, the dated rows). The page does not say it happens |
| 40 | The world keeping to the course of history after the first day | File | `follows_history: true` (`scenarios.py`; decision 69). The list on the page says so of a scenario that has it; the maker cannot set it |
| 41 | The nation of your ship | Page | maker "Nation"; `nation` |
| 42 | The region she starts in | Page | maker "Region"; `region`. All 24 regions are offered |
| 43 | The whole chart named outright | File | `chart`; kept as written by the maker |
| 44 | Where she lies: a port's road, a place pricked on the chart, or a latitude and longitude | Page | maker "The start"; `position`. All 127 ports are offered |
| 45 | The sun's latitude where there is no chart | File | `latitude_deg` (two gate scenarios use it) |
| 46 | The rule of who may know what, turned off for testing | File | `knowledge: all` |

**Your ship**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 47 | Her class (her ship file) | Page | maker "Ship file"; `ship.file` |
| 48 | Her name | File | `ship.name` |
| 49 | Her fit of guns, one of her file's (the cutter with carronades or with long guns; the 74 as of 1793, 1795 or 1812) | File | `ship.fit` (package 75; `ship/schema.py`) |
| 50 | Her heading at the start | Page | maker "Heading"; `ship.heading_deg` |
| 51 | Her speed at the start | File | `ship.speed_kn` |
| 52 | Whether she carries a barometer | Page | maker "she carries a glass"; `ship.glass` |
| 53 | The master's instrument, octant or sextant | Page | maker "Instrument"; `ship.instrument` |
| 54 | The master's book for the tides, Norie's or Moore's | File | `papers.epitome` (also `ship.epitome`) |
| 55 | A chronometer: its maker, when it was rated, its rate and its drift | File | `papers.chronometer` (also `ship.chronometer`). The owner's point of 2026-10-18: he could not add one |
| 56 | The purse | Page | maker "Purse"; `cargo.purse_pounds` |
| 57 | The goods in her hold | File | `cargo.goods` |
| 58 | The price lists she starts with | File | `papers.price_lists` |
| 59 | What service she is in: a King's ship, a privateer, a merchantman | File | `papers.service` (`world/service.py`) |
| 60 | Whether she carries her nation's private signals | File | `papers.private_signals: true` or `false` (`world/signals.py`); by her captain's role when not said |
| 61 | Other nations' signal books she holds | File | `papers.signal_books` |
| 62 | Her captain's intent, which the game's own captain sails by when nobody holds the station | Page | maker "Intent"; `intent` |
| 63 | The standing orders books read at the start | Page | maker "The orders"; `standing_orders` |
| 64 | A book of your own drafted with the scenario | Page | maker "A drafted book" |
| 65 | The captain's first orders (this is also the only way to begin at anchor) | Page | maker "First orders"; `orders` |
| 66 | Her place on the endless plane, for a test with no chart | File | `ship.x_m`, `ship.y_m` |
| 67 | A world with no ship of yours, watched from the director's station | File | `ship: none`, or `director: observe` (package 82) |
| 68 | Her role (cruiser, packet, commodore) | None | no key for your own ship; another ship has `role` |
| 69 | Her colours at the start (none shown, or false colours) | None | no key: the game looks for one that the loader never fills (`signals.py` `player_locker`), so she always shows her own |
| 70 | Her company: how many, how good, short-handed | None | mustered from her ship file under the seed (`api/session.py`) |
| 71 | Her boats, her stores, water and powder, damage she begins with | None | no key |

**The people and the things**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 72 | An officer of the muster renamed, or given a skill or a place | File | `people: [{role, name, skill, place}]` (`world/people.py` `_scenario_people`) |
| 73 | A person added beyond the muster's posts (a supercargo, a passenger), aboard or ashore at a port | File | `people`, with `ashore` and `port` |
| 74 | A person's record before a court | File | `people[].record` |
| 75 | Who a person is in this story: his rank, traits, a line of history, his brief | None | the character is the ship class's wardroom file (`data/people/<ship>.yaml`), the same in every scenario. The owner's point of 2026-10-18 |
| 76 | A thing aboard or ashore (a sealed packet in the captain's keeping) | File | `things` |

**The weather and the sea**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 77 | The month's own weather | Page | maker "the month's climatology"; `weather.climatology` |
| 78 | The wind pinned by the hour | Page | maker's wind table; `weather.wind` |
| 79 | One fixed wind for the whole game | File | `wind.from_deg`, `wind.knots` |
| 80 | How gusty and how shifting the wind is; the air warm, neutral or unstable | File | `wind.gustiness`, `wind.variability`, `wind.air_mass` |
| 81 | Weather systems written out (a low and its track) | File | `weather.systems`; the maker says "written by hand, kept as written" |
| 82 | The sky, the weather and the visibility pinned | File | `weather.sky` |
| 83 | The pressure about the systems; the sea and the ship's motion kept or not | File | `weather.background`, `weather.sea` |
| 84 | The weather held within the season's bounds | File | `weather_bound: seasonal` |
| 85 | A current the master does not know of | File | `current: {knots, toward_deg}` |

**The sea about her**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 86 | The business on or off | Page | maker "Business"; `business` |
| 87 | The business thinner or thicker (a number) | File | `business: 0.5` |
| 88 | The crewed budget written into the scenario | Page | maker; `crewed.cap`, `crewed.range_nm` |
| 89 | Ships kept crewed while on their station | File | `crewed.stationed` (`world/crews.py`) |
| 90 | Which ports are in play | Page | maker "Ports", a list of ids typed; `ports` |
| 91 | A port's state at the start: closed to a nation, blockaded and by whom, letters waiting, news | File | `ports` as a mapping (`closed_to`, `state`, `blockade`, `letters`, `news`). The maker greys the field out |
| 92 | Orders to the world by the clock | Page | maker's world orders table, as a line of text; `world_orders` |

**The other ships**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 93 | Another ship: what she is, her name, nation, where she lies and what she is about | Page | maker's table; `ships[]`: `id`, `description`, `name`, `nation`, `position`, `goal` |
| 94 | Her colours shown or not | Page | maker's table "colours": shown, none |
| 95 | Her colours false (another nation's) | File | `ships[].colours: france` (`world/ships.py` `vessel_from_spec`) |
| 96 | A captain of her own who sails her by an intent | File | `ships[].intent` |
| 97 | A goal in any words for a model who is to command her | File | `ships[].free_intent` |
| 98 | Her role, one of those her kind takes (the merchant brig as merchant, packet or indiaman) | File | `ships[].role` (package 75) |
| 99 | Her fit of guns | File | `ships[].fit` |
| 100 | The squadron she belongs to | File | `ships[].squadron` |
| 101 | Whose signals she obeys | File | `ships[].under_the_orders_of` |
| 102 | Her lights at night | File | `ships[].lights` |
| 103 | The port she is leaving; how well she sails; a letter she carries; laid up in ordinary | File | `ships[].departing`, `sailing_factor`, `letter`, `regime` with `sortie` |
| 104 | Her heading at the start | None | `ships[].heading_deg` is written for five ships in two of the game's scenarios and read by nothing: she heads for her first mark |
| 105 | Her company, her named people, her cargo | None | no key; a crewed ship's company is mustered from her ship file (`world/crews.py`) |
| 106 | Fully crewed from the first minute | None | no key in her entry. A world order at the start (`ship "X": crewed`) is the nearest road, within the cap and the range |
| 107 | Who holds a station aboard her, written into the scenario | None | `stations:` is your ship's alone. In play: a door started "on another ship", or the director's `seat:` order |

**Squadrons and convoys**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 108 | A squadron or a convoy: its name, its kind, its commander, its members and its formation | File | `squadrons[]`: `id`, `name`, `kind`, `commander`, `members`, `formation` (package 72; `world/squadrons.py`). Your ship is named `the ship` |
| 109 | Its interval and columns, its rendezvous, its goal, its book and regime | File | `squadrons[]`: `interval_cables`, `columns`, `rendezvous`, `goal`, `book`, `regime` |

**The stations and the director**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 110 | The station the scenario seats you at | Page | maker "The stations": `stations: {officer: player}` |
| 111 | A director's brief in the scenario: a starter, a file, your words, or written out with its limits and budget | Page | maker "The director"; `director.brief` |
| 112 | The brief's examples of orders | File | `director.brief.examples`; see the trap below |
| 113 | What the director is granted: which models it may seat on other ships, how many at once and in the voyage | File | `director: {models, seats, seats_in_voyage}` (package 43; `world/orders.py`) |

**What cannot be told at all, beyond the rows marked None above**

| # | What the game can be told | Today | Where found |
|---|---|---|---|
| 114 | Which flags a ship has in her locker (a broad pendant, false colours carried for a ruse) | None | any ship may hoist any flag of her nation's file; the owner's addition of 2026-11-09 |
| 115 | What the private signal is | None | drawn from the seed, the nation and the month (`signals.py`); only whether she carries it can be said (row 60) |
| 116 | The wars as they stood in another year | None | the file takes a `nations:` block and the game reads it nowhere; the wars are always those of June 1805 (`data/nations.yaml`) |
| 117 | A second ship of yours from the first minute | None | in play only (`take command of`, `transfer`; package 60). The flag of row 7 puts you aboard another ship; it does not make her yours |
| 118 | A model planned for a station in the scenario, so that its door is offered | None | `stations: {captain: model}` is accepted and read by nothing (see the traps) |

**The count.** Page 51. File 53. None 14. Total 118.

### 1.4 Traps: things that look as if they work

The owner should know these before the gate, whatever is built.

1. **"model" and "rules" in the maker's stations do nothing.** The loader accepts them and its own words say "the harbour offers it" (`scenarios.py`, the docstring). Nothing reads them: only `player` has an effect (`ScenarioFile.player_seat`). No scenario of the game uses the block.
2. **The chart's year and the almanac are read by nothing.** Forty-seven scenarios write `papers: {chart: {year: 1804}, almanac: 1805}`. Neither changes anything in play.
3. **A scenario in another year has the ports of that year and the wars of June 1805.** Tarragona (1809) and the Faro (1808) are on the list. Their ports are held as on their day. Their wars are not theirs: the block that would say so is kept and unread (row 116).
4. **Another ship's heading in the file is ignored** (row 104).
5. **Another ship's fit is not checked until she comes close.** A fit her class has not is accepted when the scenario loads and refused only when she is promoted to a full crew (`world/crews.py`).
6. **A key the loader does not know is passed over in silence.** A misspelt key in a scenario does nothing and nothing says so.
7. **Touching a written brief in the maker drops its examples.** The form rebuilds the brief from the fields it shows (`harbour.js` `writtenBrief`), and it shows no examples.
8. **The primer's own first passage cannot be started from the page.** Chapter 7 starts a bare frigate with a wind and a heading given by flags (rows 15 and 16).

### 1.5 What the inventory shows about the deeper layer

The older brief feared three separate builders of ships. That is not what the code has. Every ship that is not yours is made by one function, from one list of fields, whether the scenario, the director's `ship:` order or the business asked for her (`world/ships.py` `vessel_from_spec`). What is separate is this:

- **Your own ship is made another way** (`api/session.py`, from the scenario's own fields), so she has things no other ship can be given (a name for her instrument, a chronometer, people) and lacks things every other ship has (a role, colours).
- **A ship that comes close is made a third way** (`world/crews.py`): a full crew is mustered from her class file, and nothing the scenario said about her people could reach it, because there is nowhere to say it.
- **The director's order and the business use fewer fields than the scenario** (no fit, no role), and none of the three says back what it filled in.

So "every ship set up the same way" is true on the page only as far as these three roads agree. Section 2.3 designs the card; section 2.8 designs the deeper layer that would close the gap; section 5 puts the choice to the owner.

---

## 2. The page for the experienced player

**Conclusion.** One sheet for a scenario, folded into ten parts. Each part shows, closed, one line that says what is set; it opens in place. The common case is three choices and a button. Every ship, yours and the others, is set up on the same card. Each setting has its sentence beside it. Nothing the page does not show is lost, as today.

### 2.1 The page's shape

Four tabs become five, renamed for what the player does:

| Tab | What it is for | Today's name |
|---|---|---|
| **Begin** | A first game, the lessons, and a game in play taken up again | new (section 3) |
| **Play** | Choose a game from the shelves, make three choices, start | "game" |
| **Scenario** | The sheet: every part of a scenario, read, changed, proved and saved | "scenario maker" |
| **Stations** | Who is where: you, the models and the game's own; the doors | "doors" |
| **Settings** | The machine's choices, each explained | "settings" |

The panel "In play" (the game, the ship, the clock, the stations held, the doors up) stays at the head of every tab as one line, and opens to the whole. Today it fills the top of the first tab whether or not a game is in play.

### 2.2 Play: the common case is three choices

The player picks a game from the shelves (section 3.2). The page then shows, beside the game's name:

- **What this game is**, in the scenario's own lines: where and when she starts, the weather, the other sail, the ports. The game writes these already when it proves a scenario (`ScenarioFile.lines`); the page shows them before the start instead of after.
- **Where you stand.** Your station, and your ship if the scenario has more than one a player may board. One control (rows 6 and 7).
- **The clock.** Three plain choices: "at my own pace" (free-running), "slowed while a model is thinking" (the pace rule), "waits for the models" (lockstep). The compression beside it.
- **Start.**

A step, "more for this game", opens the rest: the seed; the business; the crewed budget; a director's brief; a book of standing orders; the clock eased when a station speaks. Each with its sentence (2.6).

A second step, "change this scenario", opens the game on the Scenario tab as a copy of yours. This is the join between the two halves of today's page, which do not know of one another.

"A bare ship" stays, moved under "more ways to start", with the wind and the heading beside it (rows 15 and 16) and the ship's boats taken out of the list. "A save" becomes a list (2.7).

### 2.3 The sheet: a scenario in ten folded parts

Each part is a line when closed. The line is written by the page from the fields, so that the whole scenario can be read without opening anything. An example, for the blockade of Brest:

| Part | The closed line (an example) | Opens to |
|---|---|---|
| **The day** | 12 June 1805, ten in the forenoon. The ports as they stood that day; the world's own course after. | name, seed, day and hour, the course of history (row 40), with the sentence of trap 3 when the year is not 1805 |
| **Your ship** | The frigate *Amazon* of Britain, a King's ship, her 1795 guns. | the ship's card (2.4) |
| **The start** | Fifteen miles west of Ushant, heading north-north-east. | a port's road, the chart, latitude and longitude; heading and speed; "at anchor" (which writes the first order) |
| **Her papers and her purse** | Norie's epitome, a sextant, a glass, no chronometer. Private signals carried. £0. | rows 52 to 61, each explained: what a chronometer does for the longitude, what the private signal is and that it is drawn, not written |
| **Her people** | As her wardroom has them. The master a good one. | rows 72 to 74: each officer by his post, with a name, a skill and a place; "another person" for one beyond the muster; things (row 76) |
| **The weather** | A low passing north; the wind pinned from west-south-west. | rows 77 to 85. The month's weather and the pinned wind as now; the fixed wind, the air, the bound and the current as fields; the systems as their text (2.5) |
| **The other ships** | Three: *Naiad* and *Nimble* of Britain, *Hortense* of France. One squadron, in line ahead. | a card for each ship (2.4), and the squadrons (below) |
| **The sea about her** | Four ports. No business. Three ships crewed at once within four miles. | rows 86 to 92: the ports chosen from the chart, a port's state, the world orders |
| **The orders** | The starter book. First order: set plain sail. Intent: keep the station off Ushant. | rows 62 to 65 |
| **The stations and the director** | You are the captain. No director. | the stations' table (2.6) and the director's brief and grant |

**Squadrons** sit inside "the other ships", because a squadron is a set of the ships just listed. A squadron's card has its name, its kind (squadron or convoy), its formation (line ahead, line abreast, order of sailing, close order), its commander and its members ticked from the scenario's ships, yours among them. Its interval, columns, rendezvous and book are behind "more". Ticking a ship into a squadron writes the squadron's entry; the page does not also write the ship's own `squadron` word, so that there is one place it is said.

**Proving and saving** stay as they are, and the proof's lines stay the scenario's own. Two things are added to the proof's words: a line for each key in the file that the game does not read (traps 2, 4 and 6), and a line for a fit or a role a ship's class has not (trap 5), checked by the page against the lists it already has.

### 2.4 Every ship on the same card

One card, used for your ship and for each other ship. Its head is always the same five things; the rest is behind "more about her".

| On the card | Your ship | Another ship |
|---|---|---|
| **What she is** | her class, from the ships | her description (frigate, revenue cutter, merchant brig: 17 of them) |
| **Her name** | row 48 | row 93 |
| **Her nation** | row 41 | row 93 |
| **Her fit** | row 49, chosen from her class's fits | row 99, chosen from her class's fits |
| **What she is about** | your intent (row 62) | her goal; a captain of her own by an intent; or a goal in words for a model (rows 93, 96, 97) |
| more: **her role** | *cannot be said* (row 68); her service can (row 59) | row 98, chosen from her kind's roles |
| more: **her colours at the start** | *cannot be said* (row 69) | shown, none, or another nation's (rows 94, 95) |
| more: **where and how she lies** | "The start" part | her place by a port, the chart, or a bearing and distance from you; *her heading cannot be said* (row 104) |
| more: **her people** | "Her people" part | *cannot be said* (row 105) |
| more: **her lights, whose signals she obeys, the port she leaves, a letter she carries** | not hers to set | rows 101 to 103 |
| more: **who commands her** | the stations' table | the game's captain, or "a model, by a door": the page then offers the door when the game starts (2.6) |

Where the table says *cannot be said*, the card shows the line greyed with one sentence: "The game does not yet take this for your own ship", or "for another ship". This is the honest form of "every ship the same way" on the page layer. It is the first question for the owner (section 5, question 2).

The card fills its own blanks in words. Choosing "revenue cutter" shows "the cutter with long guns, in the revenue's service" because the description's file says so (`ship.descriptions` in each ship file: fit and roles). The page reads these; it invents nothing.

### 2.5 What is offered as text, not as fields

Two things are too large to be worth a form before the gate:

- **Weather systems** (a low, its fronts and its track by the hour). Thirty-one of the game's 48 scenarios have them, each written by a builder to make a day come out a certain way. A player making a game of his own has the month's weather and the pinned wind, which have forms already. A form for a system's track is the largest single piece of form the sheet could have.
- **A port's letters and news.** No scenario of the game has them.

For these the part shows the block of the file itself in a box that can be changed and is proved like the rest. This is editing a file's words, on the page, with the proof beside it. It is the third question for the owner (section 5, question 4).

### 2.6 The stations: one control in place of three

The owner's first point of 2026-10-18 was that the page has three notions with one word: the settings' default seat, the scenario's stations, and the doors' "on another ship". The Stations tab says it once, at its head:

> A station is a post: the captain's, the officer of the watch's, the master's, the lookout's, a passenger's; and above the game, the director's. You sit at one. A model can be given another, through a door. The game's own people hold the rest.

Under it, one table for the game in play (or the scenario chosen), a row for each station of each ship that has a captain of her own:

| Ship | Station | Held by | Through | Model |
|---|---|---|---|---|
| *Amazon* (yours) | the captain | you | this browser | |
| *Amazon* | the officer of the watch | a model | the API door | chosen from the settings' models |
| *Raven* | the captain | a model | the local runner | |
| above the game | the director | the game's own | | |

- "Held by" is one of: you, a model, the game's own.
- Choosing "a model" asks which door, and for the API door which of the models the settings name (row 28, put on the settings form). "Start" beside the row starts that door. "Start them all" starts every row that wants one.
- The row for your own seat is the same choice as "where you stand" on the Play tab: one thing, shown in two places.
- The plan is kept with the scenario for your own ship (`stations:`, which the game already accepts; the page becomes the reader its own words promise, trap 1). For another ship there is nowhere in a scenario to keep it (row 107): the page remembers it for the game in play only, and says so.
- The desktop client's entries stay on this tab, under the table: "write the entries for the rows that say the desktop client".
- **The director's grant** (row 113) is a short panel under the table: which models the director may seat, how many at once and in the voyage. The page says what a grant is: "these are the models the director may put in command of another ship, each asked for its consent first".

Several models at several stations (row 34) is then one settings file and one table. It needs the settings to hold a list of models for the API door (they do, row 28) and the door's start to take one of them by name (the page's own server does this for a director's seat already, `Harbour.door_argv`). The local runner serves one model at one address; a second local model wants a second address, and the settings would need a list of runners. That is a change to the settings file's shape and I have left it out of the build (section 5, question 8).

### 2.7 Each setting explained where it is set

Every control gets one sentence under it, in a player's words. The server's flags have help lines already; half are written for a programmer. The page's sentences are its own, kept in one file of the client so that they can be read and corrected in one place. Examples of the rewording:

| Today | On the page |
|---|---|
| Crewed cap | **Ships fully crewed at once.** Other ships near you are sailed man by man, as yours is. This is how many at a time. More is truer and slower. Empty: three. |
| Crewed range (miles) | **Within how many miles.** A ship is given her full crew inside this distance and loses it two miles beyond. Empty: four. |
| Pace: the pace rule (1x while a model's sample is open) | **Slowed while a model is thinking.** The clock drops to real time while a model at a station is answering, so that it is not left behind. |
| Business | **The sea's traffic.** Traders, fishermen and cruisers that the game puts on the sea for itself. Off: only the ships the scenario names. |
| Seed | **The seed.** The same seed gives the same weather, the same names and the same chances. Empty: the scenario's own. |
| Seat's fold | **How long a seated model's memory runs** before it is folded into a summary. Empty: two fifths of what the model can hold. |
| Flags (the API door) | Named choices in place of a line of flags: how often the model is asked (every half-hour glass, every watch); whether it is offered pictures; whether the consent question is put again. A line for "other flags" stays. |

**Saves.** "A save" on the Play tab lists what is in the saves place, newest first: each save's name, the scenario it came from, its ship's date and the day it was written. The folder is named above the list, with one sentence: "Saves are kept here. `save NAME` at the order line writes one. A save kept elsewhere can be taken up by moving it here." The settings tab says of the saves place what the code says: it is fixed while the server runs and changes at the next start.

**The guard.** The settings tab gains a short panel, "This game answers its own page alone", with what the README says of it in three sentences and the address to open from another device when the server was started for that (row 18). The page does not let another device change the settings, as now.

### 2.8 The deeper layer: designed, not to be built before the gate

This is the lower layer of the older brief. The owner has settled that it is designed here and decided after the gate.

**What it is.** One description of a ship, "her sheet", that every maker of ships fills and every ship can say back. Its fields, with where each comes from today:

| Field | Today |
|---|---|
| her class, her description, her name, an id apart from her name | class file; `description`; `name`; the id is the name as written |
| her nation, her service, her role | `nation`; `papers.service` for yours only; `role` for others only |
| her fit | `fit`, checked for yours at once, for others late |
| her commander: a name, a rank; the game's captain, a model or a player | wardroom file; `intent`; a door |
| her company: full, short by a number, and how good | class file and the seed; no key |
| her people by name, each with a line of who he is | `people` for yours, name and skill only; none for others |
| her stations and who holds each | `stations` for yours; none for others |
| her papers: books, private signals, price lists, chronometer | `papers` for yours; none for others |
| her locker: the colours she shows at the start, the flags she has, false colours carried | `colours` for others; none for yours; no locker at all |
| her lights, whose signals she obeys, her squadron | others only |
| her place, heading, speed, and whether under way, at anchor or in ordinary | split between the two forms; no heading for others |
| her purse and her hold | yours only |
| what she is about: an intent, a goal in words, or a planned goal | `intent`, `free_intent`, `goal` |

**Its rules.**

- **Complete from three words.** A class, a nation and a role make a whole, sane ship: a merchant brig of Britain, a Spanish xebec of the King's, a French privateer schooner. Every other field has a default drawn from those three, and every field can be overridden.
- **Refused in words, when she is made.** A fit her class has not, a role her kind does not take, a station her bill has not, a book her nation has not, a flag her service would not carry.
- **Said back.** Any ship can say her sheet in words: what was asked and what was filled in. The scenario's proof, the director's order and the business each show it.
- **One maker.** The scenario's ships, your own ship, the director's `ship:` order and the business all fill the same sheet and hand it to the same function. The ship that comes close is given her full crew from her sheet, not from her class file alone.
- **Nothing recorded moves.** Every field of today's files is read as before, by its present name. The sheet adds fields; it renames none. A save made before it loads after it.

**Why not now.** It changes how every ship in the game is made, including yours and every ship the tests build. The card's reason stands: it is the kind of change that could make a working game worse by degrees, and the gate should measure the game as it is.

**What the page loses by waiting** is exactly the rows marked None in section 1.3 and the greyed lines of 2.4. Nothing else.

---

## 3. The page for a newcomer

**Conclusion.** The page opens on a panel with no form on it. It names one game to begin with, lists the four lessons as lessons in the primer's order, and offers the rest by shelf. The scenarios that exist for tests and gates are not on the shelves. All of it is the page and one small file that says which scenario goes on which shelf.

**What a newcomer meets today** (the cold review of 14 November, 1.5 and 5.3 item 14, and my own look): a form headed "A new game: the server's flags, as the page's controls", with twelve fields, the first scenario in the list the Gulf of Lion, "The gate's day" and "The squadron promoting in station" beside "The first action", and no word on where to begin. I counted 48 scenario files in the list; the review counted 47.

### 3.1 The Begin panel

The first tab, and the one the page opens on when no game is in play. In order:

1. **One sentence of what the game is.** "A sailing ship of 1805, sailed by typing orders in the words of the time."
2. **Your first game**, as one button with three lines beside it: what ship, where, how long, and what you will have done at the end. Under it: "The primer's chapter 7 goes with it, line by line", with the link.
3. **The lessons**, numbered, in the primer's order (chapter 18), each with one line of what it teaches and how long it takes:
   1. A landfall on one headland
   2. Your own reckoning (you are the officer of the watch)
   3. Pilot water: cross bearings, a pilot, coming to in a tideway
   4. A night standing off a lee shore
4. **Take up a saved game**, if there is one: the newest save by name.
5. **All the games**, which goes to the Play tab's shelves.

There is no seed, no pace and no seat on this panel. Each button starts its game with the scenario's own choices and the clock held, and goes to the game's page. The lesson that seats the player at the officer's station does so because its shelf entry says so, not because the newcomer chose it.

When a game is in play the panel leads with "Go to your game" and what it is.

### 3.2 The shelves

The Play tab's list is no longer alphabetical. It is six shelves, each with a line of what is on it. My sorting of the 48, for the owner to correct:

| Shelf | What is on it | Scenarios |
|---|---|---|
| **Lessons** (4) | The primer's lessons, in order | lesson-landfall, lesson-reckoning, lesson-falmouth, lesson-lee-shore |
| **Passages** (17) | A ship, a sea and a port to make; by sea, from the Channel outward | channel-east, spithead, naval-cruise, falmouth-to-corunna, biscay-north, biscay-south, portugal, strait, madeira, azores, canaries, morocco, mahon, tarragona, agincourt-sound, bona, the-faro |
| **Trade** (8) | A merchantman, a purse and the ports | merchant-passage, merchant-intent, merchant-brig, merchant-cutter, merchant-schooner-plymouth, merchant-ship, smack-falmouth, lugger-roscoff |
| **Actions and squadrons** (7) | Guns, a chase, a convoy, a blockade | first-action, encounter, exercising-the-great-guns, leak, convoy, convoy-six, blockade |
| **With a director** (5) | A model above the game shaping the voyage; needs a model's door | directed-passage, dispatches-falmouth, captive, prize-home, the-channel-observed |
| **Kept for tests and gates** (7), not shown | The gates' days and the acceptance walks | gate-4c-day, gate-5a-day, gate-5b-passage, gate-5b-passage-schooner, gate-5b-passage-thick, squadron, tender |

- The last shelf is shown only when a tick box at the foot of the list, "show the scenarios kept for tests and gates", is set. The owner needs them at a gate; a newcomer does not see them.
- **Your own scenarios** are a seventh shelf, first in the list when there are any.
- Each scenario shows one sentence under its name: what ship, where, and what there is to do. Today that sentence exists only as a comment at the head of each file, written for the builders.
- A scenario in a year other than 1805 says its year. One that keeps to the course of history says so, as now.

**Where the sorting is kept.** In one new file beside the scenarios, read by the page alone: for each scenario its shelf, its place on the shelf and its sentence; and at its head, which scenario is the first game. No scenario file is touched, so nothing the tests have recorded moves. A scenario the file does not name (a new one, before anyone has sorted it) goes on a shelf called "Not yet sorted", so that nothing is ever hidden by forgetting. The other way to do it is a line in each scenario file; I have not chosen it because it changes 48 files that tests read (section 5, question 6).

### 3.3 The first game

This is the owner's to choose (section 5, question 1). The page needs only a name.

What the review and the primer show about the candidates:

| Candidate | For | Against |
|---|---|---|
| **The primer's chapter 7: the frigate, a north wind of fifteen knots, an hour and a quarter** | The primer walks it line by line and the logs in the book match the game at seed 7. Daylight. No land to hit, no enemy, no port. It teaches the one thing the review says is a hard first minute: the yards must be braced. | It is not a scenario today (trap 8). It needs one small scenario file written, using only keys the game reads now, and the build must show that its log still matches the book. |
| The first lesson, a landfall on one headland | It exists. | It begins at one in the morning, thirty-three miles from land, and its subject is the reckoning, not the ship. |
| The first action | A fight is what many will want first. | The review's reader lost it in silence with the guns lashed. Whether that is mended I did not determine (section 6). |
| The dispatches | The owner's own scenario. | It needs a director, and so a model's door, before the first order. |

I would choose the first. It is the only candidate where the book in the player's hand and the game on the screen say the same thing.

### 3.4 What this section does not design

The guided first passage with the sailing master is not in this package. The Begin panel is made so that it has a place to go: the first game's button is where a guide would start.

---

## 4. The build, in steps

**Size, said first.** I count nine to twelve working days for the whole of it. That is at the edge of the card's "about two weeks", not past it, so I have not stopped; but it leaves little room. The steps are therefore in two groups. **The six marked "for the gate" are about six days** and are what the card's purpose needs: the owner can start any game the build can play, and a newcomer has a place to begin. The other five make the page whole and can follow the gate without harm.

Every step is **the page only**: the page's three files, the page's own server (`freesail/ui/harbour.py`), one new file of shelves, one new scenario, and in step 9 one new list in the settings file. No step changes how the game reads a scenario. What would need that is listed after the steps and is not to be built before the gate.

| # | Step | The owner tries it by | Marked | Days |
|---|---|---|---|---|
| 1 | **The shelves.** The file of shelves; the Play tab's list by shelf with a sentence each; the tests' and gates' scenarios behind a tick box; the ship's boats out of the bare-ship list. | Opening the page: no gate's day in the list; ticking the box brings them back. | the page only. **For the gate** | 1 |
| 2 | **Begin.** The first panel: the first game, the four lessons, the newest save, "all the games". The first game's scenario written from chapter 7. | Opening the page fresh and pressing the first button; typing chapter 7's first block and seeing the book's lines. | the page only (one new scenario of today's keys). **For the gate** | 1 |
| 3 | **Play recut.** Three choices and "more"; what the game is, shown before the start; "aboard another ship"; the wind and heading for a bare ship; the saves as a list. | Starting the tender's scenario aboard the *Raven* from the page; taking up a save by picking it. | the page only. **For the gate** | 1 to 1.5 |
| 4 | **The sheet folded.** The scenario maker's parts closed to a line each, written from the fields; nothing new settable yet; "change this scenario" from the Play tab. | Reading the blockade into the sheet and reading the whole of it without opening a part; saving it unchanged and seeing the same file. | the page only | 1 |
| 5 | **The ship's card.** For your ship: name, fit, speed, service. For another: role, fit, false colours, an intent or a goal in words, lights, whose signals, the rest. The lists of fits and roles served to the page. The greyed lines of 2.4. | Making a scenario with a revenue cutter under long guns and a privateer lugger under British colours, proving it, starting it. | the page only. **For the gate** | 1.5 to 2 |
| 6 | **Squadrons.** The squadron's card inside "the other ships". | Building the convoy of six from an empty sheet. | the page only. **For the gate** | 1 |
| 7 | **Papers, purse and people.** The chronometer, the epitome, private signals carried, signal books, price lists, the hold; an officer renamed and his skill; a person added; things. | Adding a chronometer and a supercargo named Mr Pentreath, and finding both in the game. | the page only. **For the gate** | 1 |
| 8 | **The day, the weather and the ports whole.** The course of history; the year's sentence; the fixed wind, the air, the bound, the current; a port's state; the two text boxes of 2.5; the proof's new lines for keys unread. | Setting a scenario in 1808 and reading what the page says of its ports and its wars. | the page only | 1 to 1.5 |
| 9 | **The stations as one table.** The table of 2.6; the settings' list of models on the form; a door started with a model chosen; the director's grant; the scenario's plan for your own ship read by the page. | Seating two different models at two stations from one settings file. | the page only (and the settings form shows a list it already keeps) | 1.5 to 2 |
| 10 | **Each setting explained.** The sentences of 2.7 under every control on every tab; the doors' flags as named choices; the guard's panel; the saves place said. | Reading the Settings tab and finding no control without its sentence. | the page only | 1 |
| 11 | **The words.** The primer's chapter on starting a game and the README's paragraph on the harbour made true to the page. | Reading them beside the page. | documents only | 0.5 |

Each step leaves the page working and can be merged alone. Steps 1 to 3 are the newcomer's; 5 to 7 are what the owner named as missing on 6 November (a squadron, the full parameters of a ship, the papers, the private signal's carrying, the role and fit of each ship).

**What needs a change in how the game reads a scenario, and so is not built before the gate.** Each is small beside the deeper layer and each is a piece of it:

| | Change | Closes |
|---|---|---|
| a | The player's ship takes `colours` and a `role` | rows 68, 69 |
| b | Another ship's entry takes a heading, and her fit is checked when the scenario loads | row 104, trap 5 |
| c | A person in a scenario takes a line of who he is, over the wardroom file's | row 75 |
| d | `stations:` may name another ship's stations | row 107 |
| e | The `nations:` block is read, so that a scenario's wars are its year's | row 116, trap 3 |
| f | A key the loader does not know is refused in words, or at least said | trap 6 |
| g | The locker: which flags a ship has | row 114 |
| h | Another ship's company and people; fully crewed from the start | rows 105, 106 |
| i | The ship's sheet itself (2.8), which takes in a, b, c, d, g and h | the deeper layer |

---

## 5. The questions that are the owner's

Each with what I would choose and why. A yes is enough where he agrees.

**1. Which game is the first game?**
I would choose the primer's chapter 7, the frigate's hour and a quarter, written as a scenario called "A first passage" (section 3.3). It is the only one where the book and the game say the same thing line for line, and it teaches the first hard minute.

**2. "Every ship set up the same way" cannot be wholly true on the page layer. Is the card with its greyed lines acceptable before the gate?**
The game takes a role and colours for another ship and not for yours; it takes people for yours and not for another (section 2.4). The page can show one card and say plainly which lines the game does not yet take. I would choose that. The other choice is to build changes a and b of section 4 before the gate, about two days, which is the first step onto the deeper layer that the card put after the gate.

**3. The flags a ship carries cannot be set from the page at all. Does that wait?**
The owner added the ship's flags to this package on 9 November. There is no key for a locker (row 114), and none for your own ship's colours at the start (row 69). The page can set another ship's colours to shown, none or false, and nothing more. I would let it wait with the deeper layer: a locker with its defaults by nation, service and rank is a design of its own, and half a locker would be worse than the present rule that any ship may hoist any flag of her nation.

**4. Are two text boxes acceptable for the weather's systems and a port's letters and news?**
A form for each is about two days that the gate does not need (section 2.5). The systems are common in the game's own scenarios and the owner may well want to move a low; the box lets him, in the file's words. The box shows the file's own words on the page and proves them. I would say yes, and build the forms after the gate if the owner finds he uses them.

**5. A scenario in another year has that year's ports and June 1805's wars. Should the page say so, or should those scenarios come off the shelves until it is mended?**
Tarragona (1809) and the Faro (1808) are affected. I would keep them on the shelf and have the page say it in one sentence wherever the year is not 1805: "The ports are as they stood on this day. The wars are those of June 1805." Taking them off hides two of the newest seas. Mending it is change e of section 4, which is not page work.

**6. Where is a scenario's shelf kept: in one new file, or in each scenario?**
I would choose the one file (section 3.2). It touches no scenario, so no test that reads a scenario moves. Its cost is that a new scenario must be added to it; the "Not yet sorted" shelf makes forgetting visible.

**7. Is my sorting of the 48 right, and in particular the seven taken off?**
The table is in 3.2. The two I am least sure of are "The squadron promoting in station" and "The tender": their headers call them the owner's scenario and the owner's acceptance test. I took both off because their names and their headers describe a test. He may want either back under "Actions and squadrons".

**8. Several models: is one list of models for the API door enough before the gate?**
With it, any number of models that the API door can call can sit at any number of stations from one settings file (section 2.6). What it does not give is two models on two local runners at once, which wants the settings to hold a list of runners. I would build the first and leave the second: the first covers what the owner asked on 18 October, and the second changes the shape of the settings file.

**9. The scenario's stations for a model: should the page read them?**
Today the maker lets a scenario say "the captain: a model" and nothing acts on it (trap 1). I would have the page read it, for your own ship, and offer the door when the game starts (step 9). That keeps the plan in the scenario, where the file's own words already say it belongs. A plan for another ship's station has nowhere to be written until change d.

**10. If the build must be cut to the gate's six steps, is that the right six?**
Steps 1, 2, 3, 5, 6 and 7 (section 4). They leave out the folding of the sheet, the stations' table and the explanations. Without step 4 the new fields are added to today's long form, which works and is a wall. If one more can be afforded I would add step 9, because the stations are what the owner found most confusing and what a gate with models at stations will use most.

**11. Outside the card: three small faults the inventory turned up.** I have not designed around them and do not propose them for this package; they are for the gate script as known, or a mend of their own:
- another ship's heading in a scenario is ignored (trap 4), which two of the game's scenarios write for five ships in vain;
- a misspelt key in a scenario is passed over in silence (trap 6);
- touching a written brief in the maker drops its examples (trap 7). This one is the page's own and step 4 or 9 would mend it in passing.

---

## 6. What I could not determine, and how I looked

- **Whether the first action and the dispatches are mended for a newcomer** (the guns left lashed; the scenario that starts "at the usual anchorage" with no anchor down). The review lists both; the packages table records mends to "the player's road" as proposed. I did not run either scenario. It bears only on question 1.
- **Whether a `seat:` order given at the first minute by a scenario succeeds.** It would be a way to plan a model for another ship in a file. The reader of the code could not tell without running it, and it asks a model for consent, which I did not do.
- **Whether a scenario written from chapter 7 gives the book's log line for line.** The bare ship and a scenario both begin at four in the morning of 1 June at the same seed, so I expect it to. Step 2 proves it or says otherwise.
- **What reads a laid-up ship's `sortie` word**, and **whether another ship's `lights` are checked anywhere.** Both are kept by the game; I did not trace their use. Neither changes the design: both are fields on the card either way.
- **The saves' own contents.** The list of saves in 2.7 shows each save's scenario and date. I did not open a save to see that both are in its head; the owner's saves are not mine to read, and I made none. The builder checks it on a save of his own.
- **The count of scenarios.** I count 48 files in the list and five more under `trials/`, which the page does not show. The review says 47. One has been added since, or one of us miscounted; it changes nothing.
- **The page on Windows.** I looked at it on Linux in a headless browser. The owner proves it on his own machine, as he did for package 59.
