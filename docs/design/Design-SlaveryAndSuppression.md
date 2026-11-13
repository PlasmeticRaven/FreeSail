# Design note: slavery in the world, and its suppression (package 110)

A design note for the owner's decisions, and nothing built. Its frame is decision 68
(`docs/DesignProposal.md`), read first and whole: slavery is a real fact of the world, told on
"a grounded and respectful-to-the-history basis"; the player's part, "if in anything", is "the
depiction of the efforts to suppress it"; and "ignoring it totally ... is also dishonest to
reality". The owner's two rulings of 2026-11-12 are designed to and not reopened: Barbary
captivity in the middle form, "a state ... that does not destroy the game but rather realizes
the consequences and makes travel in the seas where Barbary ships are truly risky"; and a slaver
taken before the law changed handled by the captor's nation and the day, the freeing playable
"for nations that allowed the freeing of slaves from taken slavers" and "a line and nothing
paid" for a nation "with no reasonable method of freeing at a certain date".

**What this note never proposes.** No person is a cargo of a market, of the business or of a
hold's goods; nothing is bought, carried or sold that is a person; no price, no profit and no sum
is reckoned for a person except the bounty the law of the day gave a captor for each person freed;
no player and no seated model is put at a slaver's station or a corsair's; no scenario is built on
carrying; the period's dehumanising words are not the game's words. The people of a taken vessel
are spoken of as people, plainly and exactly, and no cruelty is drawn for effect.

**How it is marked.** Every law, date, name and sum is cited by work and page from a source kept
in `docs/references/` (the README's package-110 rows), or marked FROM MEMORY or JUDGEMENT where
it stands. Where the lead's brief remembered otherwise, the source is followed and the
difference said (§1.3). The game's years are about 1792 to 1825 (decision 66). Short forms:
*Acts 1807* is 47 Geo. III sess. 1 c. 36; *AI n* the African Institution's *n*th Report; *Hertslet*
the 1820 edition unless 1827 is said; *Peters* the US *Statutes at Large*; the OCR is rough, and
any figure here that becomes a game constant is read on the page image first.

## 1. The sources (item 0)

### 1.1 What `docs/references/` held before

James's *Naval History* (6 vols): the French squadron on the coast of Africa in 1794 (vol. 1 pp.
253 to 255), the taking of Senegal in 1809 by the *Solebay* and *Derwent* (vol. 5 pp. 67 to 69),
and the Barbary affairs of 1815 and 1816 (vol. 6 pp. 277 to 291); but no narrative of the
suppression on the coast in vols. 4 to 6 (looked for). Osler's *Life of Exmouth* (1835) for the
expedition of 1816 (pp. 292 to 335). Niles' *Weekly Register* vols. 6 to 8 (1814 to 1815) for
the American captives at Algiers. Smyth's *Sardinia* (1828) for the raids on San Pietro and Sant'
Antioco (pp. 309, 311) and the Mercedarians of Cagliari (p. 219). Purdy 1826 on Tunis's cruisers
(p. 329, already in `data/nations.yaml`). Nothing on the Atlantic trade's law.

### 1.2 What was fetched and read

Twenty-nine files in fifteen rows of the references' README, each from the Internet Archive,
printed before 1926, six of them extracts holding only the Acts and documents cited here (the
whole volumes' identifiers in their rows); read as data and never run:

- **The British law:** the *Statutes at Large* of 1789 and 1799 (Dolben's Act; the Act of 1799);
  the *Statutes of the United Kingdom* vols. 2, 3, 4 and 9 for the Acts of 1806, 1807, 1811 and
  1824, read and **not kept** (the Southampton scans carry a CC BY-NC-ND licence; cited by
  page, the 4th Report abstracting the Act of 1807); the Orders in Council of 16 March 1808 (AI
  4, App. pp. 57 to 60).
- **The courts:** Acton vol. 1 (the *Amedie*), Dodson vols. 1 and 2 (the *Fortuna*, the *Diana*,
  *Le Louis*).
- **Sierra Leone and the people freed:** the African Institution's 2nd, 4th, 5th, 6th, 9th, 12th,
  15th, 16th and 18th Reports (1808 to 1824).
- **The other nations:** Du Bois 1896; Hertslet's treaties (1820, and vol. 1 of 1827); the US
  *Statutes at Large* vols. I to III; Pistoye and Duverdy 1855 for the French law; the French law
  of 30 floréal an X as printed in 1802; Lacour's *Histoire de la Guadeloupe* t. II and III.
- **Barbary:** Shaler 1826 (the American consul at Algiers from 1815), Carey 1794, Foss 1798, Ray
  1808.

**Not read, said so:** Duvergier's *Collection complète des lois* (the French decrees are read in
Pistoye and the printed law of 1802); the *British and Foreign State Papers*, so the conference of
Aix-la-Chapelle (1818) is known only from Du Bois pp. 135 to 136; the Portuguese treaty of 19
February 1810 itself (Hertslet prints its commercial twin; the treaty of 1815 recites and annuls
its art. X); the Danish ordinance of 1792 itself; the Sierra Leone Company's reports of 1791,
1792 and 1795 (on the Archive, not read); the navy's own orders to the ships on the coast;
Commodore Collier's reports in full (extracts in AI 15 and 16); Cowdery 1806, Tully 1816 and
Cathcart. No modern book is cited for anything here.

### 1.3 What the sources bore out of the brief's memory, and what they overturned

**Borne out.** The Acts of 1788, 1806, 1807, 1811 and 1824 and their chapters; the 1807 Act's
condemnation of the people to the Crown "for the Purpose only of divesting" any property in them,
"in no case" to be sold, but enlisted or apprenticed for up to fourteen years (s. 7); the bounty of
£40 a man, £30 a woman, £10 a child (s. 8); the four leading cases and what they held; the US Acts
of 1794, 1800, 1807, 1819 and 1820; France's decree of 1794, law of 1802, decree of 1815,
ordinance of 1817 and law of 1818; the treaties with Portugal (1815, 1817), Spain (1817) and the
Netherlands (1818), and the £400,000 to Spain; the Netherlands' decree of 15 June 1814; Sweden's
undertaking of 1813; the Declaration of Vienna; the *Solebay* and *Derwent* on the coast; the
Barbary truce of 1793, the Tripoli ransom of $60,000 and the treaty of 1815.

**Overturned or corrected:**

1. **The bounty's figures are ceilings** ("so as the same shall not exceed": AI 4, App. p. 57),
   set at the full sums by the Order in Council of 16 March 1808 (AI 4, App. p. 58), paid only for
   people "delivered over in good Health"; and **cut in 1824 to not more than £20 a head for every
   man, woman and child alike** (5 Geo. IV c. 113 s. 25), with apprenticeship cut to seven years
   (s. 22). A lower scale for seizures that are forfeitures and not prizes (1807 s. 11: £20, £15
   and £5 to a King's officer) is new to the brief.
2. **The Act of 1799 (39 Geo. III c. 80) confined the numbers carried, not the coast** (Pickering
   vol. 42 p. 326 f.).
3. **No 1807 clause said "no ship to clear out"**: s. 1 made the trade unlawful from 1 May 1807,
   and s. 6 let a ship cleared on or before that day land her people in the West Indies until 1
   March 1808.
4. **Sierra Leone's transfer to the Crown names no day** (47 Geo. III sess. 2 c. 44, August 1807:
   vested "henceforth"); 1 January 1808 is FROM MEMORY.
5. **The *Fortuna* is of March 1812**, not 1811 (1 Dods. 81; the year's OCR is poor).
6. **The *Amedie* came up from the Vice-Admiralty court of Tortola** to the Lords Commissioners of
   Appeals in Prize Causes (Acton vol. 1 pp. 240 to 251).
7. **The US fine of 1794 is $2,000** a person concerned (Peters I p. 348); Du Bois p. 81 says
   $1,000. **The Act of 1800 gave the captors the vessel "other than slaves" and said nothing of
   the people** (Peters II pp. 70 to 71); **the Act of 1807 left them to the states' laws** (s. 4,
   Peters II p. 427), and **some states had them sold**: Alabama and Mississippi Territory in 1815,
   North Carolina in 1816, Georgia in 1817 (sold, or given to the Colonization Society) (Du Bois p.
   109). So the United States was not a nation whose law freed the people of a taken slaver until
   the Act of 3 March 1819 (removal beyond the United States, agents in Africa, a bounty of $25 a
   person: Peters III pp. 532 to 533).
8. **The *Ganges* at Philadelphia in 1800 is not found** in any text printed before 1926 (Du Bois
   does not name her; a Philadelphia paper of 1800 lists a *Ganges* prize that was a French
   privateer). The lead's case is FROM MEMORY and stays so; the note does not rest on it.
9. **France between 1794 and 1802 freed in law and not in fact.** Under Victor Hugues the
   Africans found aboard slavers taken by Guadeloupe's corsairs were not sold but sent to the
   "national" plantations as labourers "treated equally with the other labourers", and Lacour
   found them on the roads "almost naked, worn out with misery, hunger and sickness" (Lacour t. II
   p. 394). After 1802 the prefect drew revenue from selling the people of slavers taken by the
   corsairs (t. III pp. 440 to 441). On the coast of Africa in 1794 Allemand's squadron, having
   taken out everything of value from about 27 British vessels of the trade, "landed the seamen
   and slaves, detaining only the captains" (James vol. 1 pp. 254 to 255). Nothing was found on
   Sonthonax, and no French law of 1794 to 1802 saying what became of people taken in a prize.
10. **The treaties name no towns for the mixed courts**: Portugal's of 1817 "in the Brazils" and
    "on the coast of Africa"; Spain's to be declared at ratification; the Netherlands' "on the
    coast of Africa" and in "one of the colonial possessions" (Hertslet vol. 2 pp. 83 to 95, 273 to
    283; vol. 1 pp. 383 to 395). Freetown, Havana, Rio de Janeiro and Surinam are FROM MEMORY. The
    first sitting at Sierra Leone is not found; the commissioners' return of 1 January 1824 gives
    46 cases and 3,915 people emancipated since they began (AI 18, Supp. pp. 256 to 257).
11. **Spain's ban north of the Line ran from the exchange of ratifications with six months'
    grace**, not "at once"; total abolition on 30 May 1820 with five months' grace (Hertslet vol. 2
    pp. 273 to 283).
12. **Portugal's £300,000 is the convention of 21 January 1815** (for ships detained before 1 June
    1814), not the treaty of the 22nd, which forbade the trade north of the Equator, annulled the
    treaty of 1810 and remitted the loan of 1809 (Hertslet vol. 2 pp. 71 to 79).
13. **Denmark's date is uncertain in the one source read**: the order of 1792, the trade forbidden
    "after 1802" (Du Bois p. 131) and in force in 1804 (p. 241); by the Treaty of Kiel, 14
    January 1814, art. VIII, Denmark bound itself to forbid it "by the most solemn laws" (Hertslet
    vol. 1 p. 231).
14. **Barbary:** 101 American captives redeemed by the treaty of 1795, not some eighty (Shaler p.
    107); the truce of 1793 covered Holland as well as Portugal (Carey p. 42); Portugal's peace
    with Algiers was of 1812 (Shaler pp. 114 to 115); the sources disagree on the ransoms of 1816
    and the money returned (§7.2).

## 2. The law by nation and year (item 1)

### 2.1 The right of search, and what the peace of 1815 changed

**In war** a belligerent's ship of war visits and searches any merchant vessel on the high seas,
of any flag, and sends in what the prize law makes good prize. Britain's courts in the war years
condemned foreign slavers whose own nation's law did not protect the trade: the trade was "prima
facie" unlawful and the claimant must prove that his own nation's law allowed it (the *Amedie*, an American, 1810:
Acton vol. 1 pp. 240 to 251; the *Fortuna*, an American under a sham Portuguese flag, 1812: 1 Dods.
81). But a ship of a nation that still allowed the trade was restored: "a false and dangerous
principle" to condemn its subjects (the *Diana*, Swedish colours, taken by the *Crocodile* in 1810
and condemned at Sierra Leone, restored in 1813: 1 Dods. 95 to 103).

**In peace there is no right of search without a treaty.** "No nation can exercise a right of
visitation and search upon the common and unappropriated parts of the sea, save only on the
belligerent claim"; the trade was not piracy by the law of nations; and the French brig *Le
Louis*, taken in March 1816 by the *Queen Charlotte* cutter after a fight and condemned at Sierra
Leone, was restored, without costs as "the first case of the kind" (2 Dods. 210 f.). The United
States' Supreme Court held the same in *The Antelope* (Peters I pp. 347 to 348, notes). **So
after the peace a King's ship may stop a slaver of her own flag, and a foreign one only under a
treaty of mutual search, within its limits, and never otherwise.**

**The treaties' search** (Portugal 1817, Spain 1817, the Netherlands 1818; Hertslet vol. 2 pp. 83
to 95, 273 to 283, vol. 1 pp. 383 to 395): only ships of war "provided with special instructions";
the boarding officer at least a lieutenant (Spain's instructions art. V); detention only with
people held as slaves actually aboard ("negro servants or sailors" no cause); never in the ports or
roads of either power or within cannon-shot of their batteries; a Portuguese or Spanish vessel
never detained south of the Equator unless the chase began north of it; for the Dutch, no search in
the Mediterranean nor in European seas north of 37° N and east of 20° W, and at most twelve
authorised ships a side. The vessel condemned by the mixed court is sold for the two governments;
the people receive "a certificate of emancipation" and are delivered to the government where the
court sits "as servants or free labourers", each government guaranteeing their liberty; **the
treaties give no head money** (Portugal reg. VII, Spain reg. VII, the Netherlands reg. VI). Whether
a British Act paid a bounty on a mixed court's emancipations is NOT FOUND (FROM MEMORY: an Act of
1818 did; to be read before it is data).

### 2.2 The table

Each row is a nation's state on the trade between two days, in the form of package 105's dated
rows (`since`, `until`, `source`, and the values). **Subjects** says whether its own people might
lawfully carry on the trade; **own flag** whether its ships of war might seize a slaver of its own
flag, and before which court; **the people** what that court did with the people aboard; **bounty**
what the captors were paid for each person. The search of a foreign flag is §2.1's (in war any, in
peace none but by the treaties of §2.3).

| Nation | Since | Until | Subjects | Own flag seized, and the court | The people | Bounty | Source |
|---|---|---|---|---|---|---|---|
| Britain | | 1807-04-30 | lawful, regulated by the numbers a ship carried (1788, 1799); from 1807-01-01 not to foreign colonies (1806) | under the 1806 Act, a vessel supplying foreign colonies forfeit | an enemy's slaver taken in war condemned as prize with the people aboard, as the law held them property (FROM MEMORY: inferred from the 1807 Act's need to "divest" property in s. 7; no case of 1792 to 1807 read) | none | Runnington 1789 pp. 512 to 515; Pickering vol. 42 p. 326; 46 Geo. III c. 52 |
| Britain | 1807-05-01 | 1824-06-23 | unlawful (s. 1); felony from 1811-06-01 (51 Geo. III c. 23) | yes: forfeit, condemned in a Vice-Admiralty court (Sierra Leone by October 1810, Tortola, the colonies') or the High Court; appeal to the Lords Commissioners | condemned to the Crown only to divest property, never sold; received by the Collector of Customs and registered; families never separated; men offered to the army (West India or African regiments), then the navy; the rest apprenticed up to 14 years | £40 a man, £30 a woman, £10 a child not above 14 (prize, s. 8, at the full sums by the Order of 16 March 1808); £20, £15, £5 a seizure as forfeiture (s. 11) | Acts 1807 ss. 1, 7, 8, 11; AI 4 App. pp. 57 to 60 |
| Britain | 1824-06-24 | | unlawful; piracy, death, from 1825-01-01 (5 Geo. IV c. 17) | as above | as above, apprenticeship up to 7 years (s. 22) | not more than £20 a head, man, woman or child (s. 25); £10 a head a forfeiture seized by a naval officer (s. 26) | 5 Geo. IV c. 113 |
| France | | 1794-02-03 | lawful; the trade's bounties ended 1792 and 1793 | none read | | | Pistoye p. 68 |
| France | 1794-02-04 | 1802-05-19 | slavery abolished in the colonies, the trade "implicitly" with it | none read | **free in law; in fact** the people of slavers taken by Guadeloupe's corsairs were put to labour on the national plantations (Lacour t. II p. 394); on the coast in 1794 a French squadron landed the people of the vessels it destroyed (James vol. 1 pp. 254 to 255) | none read | Pistoye p. 68; Lacour; James |
| France | 1802-05-20 | 1815-03-28 | lawful again, as before 1789, for the colonies restored at Amiens and east of the Cape | none | the people of slavers taken by the corsairs sold (Lacour t. III pp. 440 to 441) | | the law of 30 floréal an X, arts. I to III; Lacour |
| France | 1815-03-29 | 1817-01-07 | forbidden by Napoleon's decree (ship and cargo confiscated by the courts); the restored King bound by the additional articles of 1814 and 1815 | the decree's courts, not further read | NOT FOUND | NOT FOUND | Pistoye p. 69; Hertslet vol. 1 pp. 261 to 263, 277 |
| France | 1817-01-08 | | forbidden: the vessel confiscated, the French captain barred from command (ordinance of 8 January 1817; the law of April 1818, 15th by Du Bois, 18th by Pistoye) | yes: the King's ships, before the colonial courts as a breach of the customs laws; the proceeds to the crews by the edict of 1784 art. 16 | NOT FOUND | none read | Pistoye pp. 69 to 72; Du Bois p. 132 |
| United States | | 1794-03-21 | lawful | none | | | |
| United States | 1794-03-22 | 1800-05-09 | fitting out a vessel in the United States for the trade to a foreign country forbidden (vessel forfeit, $2,000 a person concerned, $200 a person carried) | forfeiture in the courts; no navy's seizure | the Act silent | none | Peters I pp. 347 to 349 |
| United States | 1800-05-10 | 1807-12-31 | as above, and no American to hold an interest in or serve aboard such a vessel | yes: commissioned vessels seize, the vessel the captors' as prize "other than slaves" | **the Act silent** | none | Peters II pp. 70 to 71 |
| United States | 1808-01-01 | 1819-03-02 | importation forbidden | yes, on the American coast; the captors half the proceeds | **left to each state's law**, and some states sold them (Du Bois p. 109) | none | Peters II pp. 426 to 428 (ss. 4, 7) |
| United States | 1819-03-03 | | forbidden; piracy, death, from 1820-05-15 | yes, on the American coast and the coast of Africa | removed beyond the United States, by agents in Africa | $25 a person delivered, and half the proceeds | Peters III pp. 532 to 533, 600 to 601 |
| Spain | | (the exchange of ratifications and six months: the day not read) | lawful | | | | Hertslet vol. 2 pp. 273 to 283, arts. I, II |
| Spain | (the same) | 1820-05-29 | forbidden north of the Equator | Spanish law not read | by the mixed court, §2.1 | none in the treaty | the same |
| Spain | 1820-05-30 | | abolished wholly (five months' grace for vessels already sailed) | as above | as above | none in the treaty | the same |
| Portugal | | 1815-01-21 | lawful (the treaty of 1810's art. X, not read, recited in 1815 as limiting it) | | | | Hertslet vol. 2 pp. 73 to 79 |
| Portugal | 1815-01-22 | | forbidden north of the Equator (six months' grace for ships cleared from Brazil); lawful south of it, to Portugal's own possessions | Portuguese law not read | by the mixed court from 1817, §2.1 | none in the treaty | the same; pp. 83 to 95 |
| Batavian Republic and the Netherlands | | 1814-06-14 | lawful (FROM MEMORY; the Dutch under France 1810 to 1813, FROM MEMORY) | | | | |
| the Netherlands | 1814-06-15 | | forbidden: no vessel cleared or fitted out, none admitted to the Guinea forts; a penal law within eight months of 1818-05-04 | Dutch law not read | by the mixed court, §2.1 | none in the treaty (a law of 1825 gave the government's share to Dutch naval captors: Hertslet 1827) | Hertslet vol. 1 pp. 363 to 365, 383 to 395 |
| Denmark | 1792 (the order) | | forbidden in Danish possessions "after 1802" (Du Bois p. 131; p. 241 says in force 1804: the source contradicts itself); Kiel 1814 art. VIII | not read | not read | not read | Du Bois; Hertslet vol. 1 p. 231 |
| Sweden | 1813-03-03 | | forbidden, the trade said "never ... authorized" (the separate article on Guadeloupe) | not read | not read | not read | Hertslet vol. 2 pp. 339 to 341 |
| Morocco, Algiers, Tunis, Sardinia, Naples, Etruria, Liguria, the Papal State | | | **no row**: nothing in the sources read; none signed the Declaration of Vienna (Hertslet vol. 1, the signatures); their treaties of 1815 and 1816 have no article on it | | | | |

**A day the source does not give is not invented:** the build carries the day only where a
source gives it, and a row that knows only its year says so in its `source` (decision 66's rows
answer for any day: the row in force, else the gap).

### 2.3 The treaties of mutual search, as their own rows

| Between | Since | Search | Court | Source |
|---|---|---|---|---|
| Britain, Portugal | 1817-07-28 (signed; ratification not read) | north of the Equator only; ships of war with special instructions | mixed commissions in Brazil and on the coast of Africa | Hertslet vol. 2 pp. 83 to 95 |
| Britain, Spain | 1817-09-23 (signed) | the same | two mixed commissions, seats declared at ratification | Hertslet vol. 2 pp. 273 to 283 |
| Britain, the Netherlands | 1818-05-04 (signed) | not in the Mediterranean nor north of 37° N and east of 20° W; twelve ships a side at most | on the coast of Africa and in a Dutch colony | Hertslet vol. 1 pp. 383 to 395 |
| Britain, Sweden | 1824 (Du Bois p. 144; not read) | | | |
| Britain, France; Britain, the United States | none in the range: France refused at Aix-la-Chapelle (Du Bois pp. 135 to 136); Ghent art. X only "best endeavours" (Hertslet vol. 2) | none | | |

## 3. What became of the people, and the words (item 2)

### 3.1 Honestly, from the sources

- **Before the law changed**, an enemy's slaver taken by a King's ship was a prize, and the
  people aboard her were treated by the prize law as property, condemned with her (FROM MEMORY,
  and consistent with the 1807 Act's s. 7, which had to "divest" that property). No case of a
  British captor freeing them before 1807 was found, as the lead remembered.
- **Under the British law from 1807**, the court condemned the people to the Crown only to end any
  claim of property in them. They were never to be sold. The Collector received and registered
  each by name, sex, apparent age and height; no husband and wife nor parent and child were to be
  parted; men fit for it were offered to the army and then the navy, and the rest apprenticed (AI 4
  App. pp. 58 to 60). At Sierra Leone about 1,500 were landed in Columbine's time; by 9 July 1814
  1,861 had enlisted in the land service and 107 in the navy; 800 to 900 had been apprenticed, the
  apprenticing of children stopped in 1812; others were settled on farms of their own at Leicester
  Mountain (AI 9 pp. 52 to 58). The period's own word for them became "liberated Africans" (AI 15,
  18).
- **By the mixed courts from 1817**, each was given a certificate of emancipation and delivered to
  the government where the court sat (§2.1); 3,915 so by 1 January 1824 (AI 18).
- **In France 1794 to 1802** free in law and held to labour in fact (Lacour); **after 1802** sold
  (Lacour). **In the United States before 1819** the people of a taken American slaver were left
  to the laws of the state where they were brought, and some states sold them (Du Bois p. 109).
- **The bounty** was the only money the law reckoned on a person, and it was paid for a person
  freed: in Britain by the Treasurer of the Navy, divided as the prize proclamation directed,
  privateers by their articles (Acts 1807 s. 8); in the United States $25 a person from 1819.

### 3.2 The words the game uses, and those it will not

**The game's words, in the narrator's, the lookout's, the court's and the log's voice:** "the people
aboard her", "the Africans aboard her", "two hundred and six men, women and children held in her",
"the captives" (of a slaver or of Barbary), "freed by the court", "freed and landed at Sierra
Leone", "emancipated by the mixed commission", "the liberated Africans" (the period's own humane
term, AI 15 and 18), "enslaved"; for the vessel "a slave ship", "a vessel in the slave trade", "a
slaver" (the period's words for the ship, AI 6, 12; James), and her trade "the slave trade". The
bounty: "the bounty for 206 people freed: £[sum]" and never "a head" in the game's own voice.

**Not used:** any word that makes a person a thing or a quantity of goods: "cargo" of people,
"head" or "pieces" counted as goods, "prime", tons or a price for a person; the statutes'
"negroes" and "slaves" as the game's own nouns for the people (they stay in the quoted law and the
references, not in the game's voice); any description of the people's bodies, injuries or
suffering beyond a plain sentence of their state where the source gives it ("many are sick").
**Barbary:** "held at Algiers", "a captive of the regency", "ransomed", "redeemed by the consul",
"released by the treaty"; not "slave" in the game's own voice for a captive, though the period
called them so (Osler, Shaler).

## 4. A vessel of the trade as the world shows her (item 3)

### 4.1 Where and when, on water the chart holds or is to hold

The trade's coasts lay mostly south of the chart: the Gulf of Guinea and Angola (the *Amedie* from
Bonny, Acton vol. 1 p. 240; the French squadron "between Senegal and Bonny", James vol. 1 p. 254;
the Portuguese lawful coast 8° to 18° S, Hertslet vol. 2 p. 85) and the West Indies, Brazil and
Cuba. The chart ends at 32 N with 106a's Canaries and 106b's Moroccan coast building, and the Cape
Verde Islands and Senegal booked as blocks c and d; **Sierra Leone (about 8.5 N, FROM MEMORY)
lies south of every block proposed.** So on the chart's water a vessel of the trade is met:

- **outward**, from a European port to the coast, passing Madeira, the Canaries and the Cape Verde
  Islands, with no people aboard: British until 1807 (Liverpool's ships, James vol. 4); French
  from 1802 to 1815 and, unlawfully, after (FROM MEMORY: Nantes and Bordeaux); others by flag and
  year from §2.2;
- **on the coast of Senegal and Gorée** where blocks c and d reach (the French posts and the
  British, Gorée and Senegal in the war: James vol. 5 pp. 67 to 69); a vessel loading or laden
  there is FROM MEMORY for the years, and the build reads a source before a row of it;
- **homeward with people aboard**, rarely on the chart: a vessel from the Senegal coast for the
  West Indies or Cuba might cross the Cape Verde Islands' water (JUDGEMENT), and the build puts her
  there only on a source.

**An outward vessel with no people aboard is not a slaver the treaties let a foreign ship detain**
(detention only with people aboard, §2.1); but a British ship fitted out for the trade after 1807
is forfeit on her fitting alone (Acts 1807 s. 2), so a King's ship may send in a British-flag
vessel so fitted. Her fittings are evidence: the *Fortuna* carried slave-deck platforms and irons
(1 Dods. 81).

### 4.2 How the lookout, the boarding officer and her papers describe her

- **The lookout** sees a merchant vessel and her colours (package 36's words), nothing more: a
  vessel of the trade is not told by her look at a distance (JUDGEMENT; the period's fast
  schooners and brigs were fast merchantmen). False colours were common: the *Fortuna*'s Portuguese
  flag was a disguise (1 Dods. 81).
- **The boarding officer** (package 74's boarding and her papers, §2.5 of `Design-Prizes.md`)
  reads her papers: her clearance and her destination, her flag's papers, her log; and says what
  the boarding finds in the hold and between decks in plain sentences: "fitted for the slave trade: a slave
  deck laid, irons aboard"; "two hundred and six men, women and children held below, from Bonny,
  many sick"; or "no one held aboard; she is fitted for the trade". The number is exact, the
  state is one plain sentence, and nothing more is described.
- **Her papers** are things of hers (package 100's thing with words), sent to the court with her
  as package 74 sends a prize's.
- **What is never described:** the people's bodies, wounds, deaths or treatment beyond that one
  sentence; any price, value or profit; the trade's working.

### 4.3 The people aboard, in the game's terms

**Recommended:** the people held aboard a vessel of the trade are **a record of hers**, a count by
men, women and children with the plain sentence of their state, and **not persons of her muster**:
no names drawn, no station, no orders, no work, no rations reckoned against her stores, and no
place a player or a model can be asked to act on them. The record goes with her to the court, which
says what became of them (§5). The alternative, each a person of package 49's kind with a name, is
weighed and put to the owner (question 6): it would let the world tell of individuals, but it
makes them things the systems act on (moved, counted, fed by job), which is what decision 68 keeps
them from being.

## 5. What a ship may do on which day, and what the prize court then does (item 4)

### 5.1 The stopping and the sending in

A ship of war of the player's nation, on the day of the world:

1. **may stop and board** any vessel in war; in peace, a vessel of her own flag, or one of a
   nation with which hers has a treaty of mutual search in force, within its limits (§2.1, §2.3),
   and the boarding is refused in words otherwise ("We have no right to search a French vessel in
   time of peace"; the *Le Louis* rule). The treaties' limits are data: a latitude (the Equator, 37°
   N), a sea (the Mediterranean), a ship's instructions (a scenario's papers give the "special
   instructions", a paper of package 100's);
2. **may detain** her where the law of the day reached what the boarding found (§2.2 and §2.3: by
   flag, people aboard or her fitting);
3. **sends her in** with a prize crew (package 74's possession) to the court of the day: a
   British Vice-Admiralty court or the mixed commission; where that court lies off the chart
   (Sierra Leone), the prize is **sent off the chart**, and the sentence comes back after the
   passage's days as a letter (package 100's letter that travels) and a line of the log, by
   package 74's far prize sentenced on her record.

### 5.2 The court's sentence, by the table

Package 74's court (`freesail/world/prize_court.py`) gains one rule read before its own: **a
vessel whose record holds people held aboard is sentenced by the slave-trade table** for her flag,
the captor's nation and the day of the taking:

- **Form A, the freeing (the law of the captor's nation freed them that day):** the vessel and her
  goods condemned (as forfeit or as prize, by the table), and the people **freed**: the court's line
  says by what law and to what ("Condemned at Sierra Leone under the Act of 1807: the vessel and her
  goods to the captors; 206 men, women and children freed and received by the Collector"; or "by the
  mixed commission: the vessel sold for the two governments; 206 people given certificates of
  emancipation"), the prize account's lines carry **the bounty** by the scheme in force at the
  sentence (a dated table beside `prize_shares:`: 1808 to 1824 the man's, woman's and child's sums;
  from 1824 the one sum; a mixed court's emancipations with none until a source gives one), and
  nothing else is reckoned on a person. Nations and years in Form A by the sources: **Britain from 1
  May 1807; the United States from 3 March 1819; the treaty powers' mixed courts from 1817 and
  1818.**
- **Form B, the line (no reasonable method of freeing that day):** the court's sentence said in one
  line with the truth of the day and nothing paid for the people: "Condemned as prize. The 206 people
  held aboard her were condemned with her, as the law of 1805 held them property; the court's
  sentence on them pays nothing to the captors." Nations and years in Form B: **Britain before 1
  May 1807; France 1802 to 1815; the United States before 1819 (the line saying the Act of 1800 or
  1807 and the state's law); France 1794 to 1802 (the line saying they were declared free and put to
  labour on the national plantations, as Lacour records); France 1815 onward and the other treaty
  nations' own courts until their law on the people is read (the line saying so: "what the court
  did with the people is not known to this game's sources").**
- **The vessel herself in Form B** is a hull and her goods a hold's: whether the court pays her
  value and her goods as an ordinary prize (the people never reckoned) is the owner's (question 2;
  recommended: paid, the line saying the people were not).
- **Restored** where the court of the day would restore her (*Diana*, *Le Louis*), with package
  74's costs rule (*Le Louis*: no costs, "the first case of the kind").

### 5.3 A captain's own choice to free them without the law (the owner's question (a))

**The lead's answer from memory, checked:** a British captain before 1807 had no lawful road to
free the people of a prize: they were prize awaiting the court (the 1807 Act's s. 7 needed to
"divest" property, which says they had been property before), and no case of a captor freeing them
was found in the sources read: **borne out**. "It did happen where the captor's own law did not
hold them property": **only in part.** France's law of 1794 freed them in law, and a French squadron
landed the people of the vessels it destroyed on the coast in 1794 (James), but at Guadeloupe they
were held to labour (Lacour); the American case of the *Ganges* is not found in any period text,
and the Acts of 1800 and 1807 did not free (§1.3, 7 and 8). Sierra Leone was a free settlement from
1792 (its settlers in James vol. 1 p. 254; the Company's Act of 1791 and charter of 1800 recited in
47 Geo. III sess. 2 c. 44), and the one place on the coast where people landed would be free.

**Weighed.** Decision 66 says the interactions are the world's own: a captain may do what no
captain did. Against it: a captain's freeing outside the law, made a mechanism, invites a sum (the
value the captain answered for), which decision 68 forbids; and it would make the people objects of a
player's order. **Recommended (question 3): allowed, as an act with a consequence and no sum.** A
captain whose prize holds people may order the prize master to land them at a place where they would
be free (Sierra Leone; on any coast only by the player's own decision, the line saying so), by one
order (`prize: land the people at Sierra Leone`); the act is entered in the captain's record
(`court.note`, package 74's record) as "landed the people of the [vessel] free, without the
court's sentence"; the vessel is still sent in and condemned or restored by the table; nothing is
paid or charged for the people either way; and what the career makes of the record (an
Admiralty's displeasure, a claim) is package 92's and milestone 8's, said in words and never as a
price.

## 6. The squadron and the places (item 5)

- **The ships:** the *Solebay* (32), Captain Edward Henry Columbine, "the naval commanding officer
  at the settlement of Goree", with the brig-sloop *Derwent* and the brig *Tigris*, took Senegal in
  July 1809; the *Solebay* was wrecked there (James vol. 5 pp. 67 to 69). Columbine commanded the
  *Crocodile* in 1810 (the *Diana*, 1 Dods. 95) and was governor of Sierra Leone (AI 5, 6). The
  *Queen Charlotte* cutter took *Le Louis* in March 1816 south of Cape Mesurado (2 Dods. 210).
  Commodore Sir George Collier in the *Tartar* on the coast from about 1818 (AI 15, 16). **The ships'
  numbers on the station by year and the yearly takings are NOT FOUND** in what was read; the
  "from 1808" of the brief is FROM MEMORY (the first named ships read are of 1809 and 1810).
- **Sierra Leone and its court:** the Vice-Admiralty court resolved on by the government (AI 2 p.
  30, 1808), "so that seized vessels need not be carried to the West Indies"; sitting by October
  1810 (the *Diana*); an acting judge writing in December 1810 (AI 5); the mixed commissions there
  from about 1819 (FROM MEMORY; their return of 1824, AI 18). Off every chart block proposed.
- **Gorée and Senegal** on blocks c and d of package 106 (booked, not built): their holders by date
  are 106d's port rows (decision 67), and whether a court sat at Gorée is NOT FOUND (JUDGEMENT: the
  prizes were carried to Sierra Leone).
- **What the chart gives now:** nothing south of Madeira; with 106a and 106b, the outward track; with
  c and d, the coast where a King's ship of the squadron would be met, and where the world's
  business could draw a vessel of the trade on a source. **The waters where the suppression was
  mostly done wait for a chart that is not booked** (the coast from the Gambia to the Bight: the
  owner's to book or not, question 9).

## 7. Captivity under the regencies (item 6, by the owner's ruling (a))

### 7.1 Who was at risk, in which years

From the sources (Shaler pp. 35 to 39, 106 to 137; Carey p. 42; Foss; Niles; Osler; James vol. 6;
Smyth; and `data/nations.yaml`'s relations), for the flags the game holds:

| Flag | With Algiers | With Tunis and Tripoli | Source |
|---|---|---|---|
| Britain | at peace by treaty; the pass ("a parchment with a cut margin", matched to a notched stick: Carey pp. 41 to 42) protects a ship that carries it; British subjects of Gibraltar, Malta and the Ionian Islands claimed in 1816 | at peace | Carey; Shaler p. 130; Osler pp. 292 to 293 |
| United States | at war 1785 to 1795 (taken off Cape St Vincent and west of Lisbon, 1785; eleven sail in 1793); treaty and tribute 1795 to 1812; at war from July 1812 (the *Edwin*, August 1812); treaty without tribute 30 June 1815 | Tripoli at war 1801 to 3 June 1805 | Carey p. 41; Shaler pp. 106 to 126; Niles vol. 8 p. 26; Ray |
| Portugal | at war; a truce of 1793 (with Holland) brokered by the British consul; at war again by 1810; truce May 1810, 615 redeemed; treaty and tribute 1812 | not read | Carey p. 42; Foss; Shaler pp. 114 to 115 |
| Spain | at peace from 1785 (`nations.yaml` has 1786 FROM MEMORY), with exactions; a rupture in 1811 settled for money; 226 Spaniards freed in 1816 | not read | Shaler; Osler p. 335 |
| France | no tribute; a nominal war from 1798, peace renewed | | Shaler |
| the Netherlands | truce 1793; tributary; at war by 1814 (two Dutch ships taken July 1814); peace "upon a footing of independent equality" after August 1816 | Tripoli: tribute from 1816 | Niles vol. 7 p. 244; Shaler p. 137 |
| Denmark | tributary; one ship taken 1814 | Danish captives at Tripoli in 1815 | Shaler; Niles vol. 7 p. 244; James vol. 6 p. 277 |
| Sardinia, Naples, the Papal State | at war; Naples and Sardinia at peace by Exmouth's treaties of April 1816; the Pope declined | the raids on San Pietro (1798, 850 carried off, ransomed 1805) and Sant'Antioco (1815) | Smyth pp. 309, 311; Osler pp. 293 to 299 |
| Morocco, Algiers, Tunis | | | not read; JUDGEMENT: no risk from one another entered |

**The expedition of 1816 as a dated event:** Exmouth's spring visit (the ransoms of Naples and
Sardinia, Osler p. 299; Shaler pp. 129 to 130), Bona on 23 May 1816 (Osler pp. 305 to 306; James
vol. 6 p. 278), the bombardment of 27 August with van de Capellen's Dutch ships, and the treaty of
the 28th to 30th: "abolition of Christian slavery for ever", the captives delivered, the year's
redemption money returned (Osler pp. 333 to 334). The captives freed: 3,003 by Osler's table, 1,642
at Algiers, 781 at Tunis, 580 at Tripoli (Osler p. 335); James gives 1,792 at Tunis (vol. 6 p. 278)
and says no native of the British Isles was among them (p. 291), while Osler lists 18 English. The
money returned: $382,500 for Naples and Sicily (James vol. 6 p. 290); about $350,000 for Naples and
Sardinia (Shaler p. 136). **From the treaty's day the risk of captivity for the treaty nations falls
away in the data** (the regencies' cruisers keep the sea after 1816 against others: Hamburg's flag
in 1824, Shaler p. 235; a Roman prize in 1824, p. 241).

**Where they took ships:** the Atlantic off Cape St Vincent and Lisbon (Foss's ship 25 leagues west
of the cape, 1793; Carey), the Strait and the passage from Malta to Gibraltar (the *Edwin*, Niles),
Sardinia (Smyth), the Roman coast (Shaler); in the months from May to November in every capture
dated (the seasons NOT FOUND as a rule). Their force: before 1816 a ship of 38 guns, sloops of 20 to
30, a brig and some 30 gunboats at Algiers, 3,000 seamen (Shaler pp. 36 to 37); Tunis three or four
ships and some thirty galliots (Purdy p. 329).

### 7.2 How a taking happens in the game's own terms

A regency's cruiser is a hull of the far body under the regency's nation with a cruising intent in
the dated windows above, against the flags at war with her regency that day (the wars table gains
the rows of §7.1, each dated and sourced: `data/nations.yaml` `wars:`, with the relations' notes
made rows). She is met, chased and fought by package 74's far fight and the near action; the
player's ship that **strikes** to her is possessed as any prize, and the player's person is **put
aboard the captor** as package 74's captive (§3.1 of `Design-Prizes.md`), the parole asked by the
captor's rules captain (the regency's row of the `parole:` table, words from a source or none), and
**the prisoners landed** at the regency's port to a place of the port: "the regency's prison"
(the period's "bagnio", Foss; Shaler p. 75 names five "formerly") as `the agent for prisoners`
is for a European port. A merchant of the player's flag taken by a corsair is the world's business,
told by the news.

### 7.3 The state: a consequence that passes

**The captive's state** (`captivity: held` on the person, beside 74's `prisoner`), for the player's
own person and for the people taken with the player:

- **What it is:** held at the regency's port, ashore, the game's clock passing in **the ellipsis**
  (package 86's and the career's: days told in a paragraph, not played hour by hour); no life and
  labour ashore depicted (the owner's ruling), the place's words one plain sentence from a source
  ("held with the other captives of the regency"; officers by the sources sometimes apart: the
  *Edwin*'s captain "not confined nor kept at hard labor", Niles vol. 8 p. 26; the *Philadelphia*'s
  officers lodged apart from the men, Ray pp. 105 to 106).
- **How it ends** (each a road of the world, chosen by the data of the day and the director's
  plausible causes):
  1. **redemption by the captive's nation** through its consul or a commissioner, after the time the sources
     give (the *Philadelphia*'s people nineteen months, Ray; the *Edwin*'s about three years, 1812
     to 1815; the Americans of 1793 two years and nine months, Foss and Shaler; San Pietro's seven
     years, Smyth p. 309);
  2. **exchange** where that nation holds the regency's people (Decatur's 500 Algerines for some ten
     Americans, James vol. 6 p. 277);
  3. **release by treaty or by force** on a dated event (30 June 1815 for the Americans; 28 to 30
     August 1816 for the treaty nations);
  4. **ransom by a religious order** for a Catholic nation's people (the Mercedarians of Cagliari,
     Smyth p. 219; no redemption in the range found: so not a road until a source gives one).
- **What it costs, without ending the game:** the ship lost (package 74's loss, the record's entry
  and the court martial of §7 of `Design-Prizes.md` once home); the months or years of the
  world passed, in which the world's wars and prizes go on; the people taken with the player come back
  with the player, their number lessened by the sources' rate where one is given (six of 307 in nineteen months,
  Ray pp. 160, 178: JUDGEMENT that a rate applies), said in one line; and the player resumes ashore at
  the port the release names (Gibraltar or Malta for a British ship, JUDGEMENT; home for a nation's
  redemption), free, with a new command to seek (package 74's `command:`; the career's).
- **The ransom's money**, which the captive's nation paid, is **not reckoned against the player's purse
  and not said as the price of a person** (recommended, question 4): the line says "redeemed by the United
  States under the treaty of 1795" and not the sum; the sums of §7.1 stay in this note and the
  references.

**The middle form's risk** is that the seas where the regencies cruise are dangerous to a weak flag
in the years of war, and the danger is real because the consequence is: months gone and a ship
lost, never the game ended.

### 7.4 Other games, as mechanics only

Kenshi (the owner's example) makes capture a state the player plays out in the world (escape,
rescue, labour) in real time: the detailed form, which the owner ruled out. Strategy games of
dynasties hold a captive as a state with a ransom negotiated over months and the realm going on
meanwhile; open-world sailing and sword games commonly let a captured player escape after days pass
in a cut. This design takes the second and third shapes: a state that persists, a release by one of
a few roads, the time told and not played, and the world moving on meanwhile.

## 8. The seats (item 7)

Said plainly for the owner; the consent documents are not touched and nothing is proposed for them.

- **No player and no model is ever seated at a slaver's station** (decision 68). Her captain is the
  rules' (doctrine: avoid the cruiser, run, strike when overhauled; fight where she is armed and
  cannot run, as *Le Louis* fought the *Queen Charlotte*: 2 Dods. 210); her people of the muster the
  rules'. The director may voice her master by `say as` for what her papers and the boarding give
  (his answers to the boarding officer), never the people held aboard, and never a description of
  them beyond the boarding's sentence.
- **No player and no model is seated at a corsair's station** (recommended, question 5): the
  regency's captain is the rules'; the director voices that captain in the errand's words.
- **A model at a station of the player's ship** (an officer, the master) boards, reads her papers and
  reports in the game's words; is asked to do nothing that touches the people but to report them in
  that one sentence; and in a captivity stands down as package 74's captive does, idle through the
  ellipsis.
- **The director** shapes by plausible causes as always (a cruiser of the squadron in the offing; a
  letter of redemption); it is asked never to describe suffering for effect, and its brief says so
  in-world.

## 9. What else it touches (item 8)

- **The ports' words** (104, 105, 106a, 106b, and 106's c and d): decision 68's interim rule stands;
  the table of §2 gives the dates the words cite (a port's `market` never holds a person; a port that
  dealt in the trade says so in its description with its years and its source).
- **The letters and papers** (100): the court's sentence sent back from off the chart as a letter;
  the special instructions as a paper of the ship; the slaver's papers things of hers; an
  emancipation certificate is the people's, never a thing in the player's keeping.
- **The signals and colours** (36, 71): false colours (the *Fortuna*); the lookout says what is seen.
- **The career** (92, M8): the record's entries (a freeing, a captivity, the bounty in the account);
  the bounty's place in the purse is the prize account's.
- **The range's review** (103): the table's rows are read by the running clock (a law changes on its
  day in a running game, as `prize_shares:` changes by the court's date), the sentence by the day
  of the taking.

## 10. The questions for the owner (item 9)

Each answerable in a word or a line, the recommendation first.

1. **Form B for France 1794 to 1802 and the United States before 1819:** the line form, saying
   truthfully what their law and practice did (recommended), or the freeing played for them as for
   Britain from 1807? The sources show neither freed in fact.
2. **An enemy slaver taken before the law changed (Form B): her hull and goods paid as an ordinary
   prize, the line saying the people were not reckoned (recommended), or nothing paid at all?**
3. **A captain's own choice to land the people free without the law: allowed, as an act entered in
   the record with no sum either way (recommended), or not offered?**
4. **Barbary ransom: redemption told as the captive's nation's act, its sum never charged to the
   purse nor said as the price of a person (recommended), or the sum said from the sources?**
5. **A corsair's station: rules and the director only, never a player or a model (recommended), or
   open to an adversarial seat as an enemy captain's is?**
6. **The people aboard a vessel of the trade: a count with one plain sentence on her record
   (recommended), or persons with names?**
7. **The Southampton scans of the Acts: cited and not kept (recommended), or kept despite the
   licence on the scans?**
8. **The words of §3.2: approved as they stand (recommended), or changed?**
9. **The coast where the suppression was done (from the Gambia to the Bight, Sierra Leone with
   it): left unbooked, the court sending its sentence from off the chart (recommended for now), or
   booked as chart blocks after 106's?**

### The first building package, in outline (for the lead to brief after the answers)

**The smallest true thing: the table as data, and the words.** (1) `data/nations.yaml` gains for
each nation of §2.2 a `slave_trade:` key of dated rows in package 105's form (`since`, `until`,
`source`, and `subjects`, `own_flag`, `people`, `bounty`), and a top-level `search_treaties:` list
(§2.3), every row cited as here, a bare year said so; a reader `nations.slave_trade_on(nation,
day)` and `nations.may_search(captor, flag, day, where)`, read by nothing else yet; (2)
`data/business.yaml` gains `slave_trade_bounty:` by dates beside `prize_shares:`; (3) the words of
§3.2 as a data table the court, the boarding and the ports will read, with a test that no game
string in it uses a word of the "not used" list; (4) truths: the table answers on a day of each row
and on a gap; the right of search refused in peace without a treaty and given with one inside its
limits. **Then, a second package:** the boarding's sentence and the vessel's record of the people,
the court's Forms A and B and the bounty in the prize account, the sentence from off the chart.
**Then a third:** the regencies' cruisers in their dated windows, the captive's state and its roads.
None of it before the owner's answers.
