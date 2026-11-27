import os, glob
P = os.environ.get("P126", "/tmp/claude-0/-home-user-FreeSail/e2d459f1-79d4-50d6-9285-0413fe7ccd0b/scratchpad/rev126-probes")
SHIPS = sorted(os.path.basename(f)[:-5] for f in glob.glob("data/ships/*.yaml"))
PASSAGE = """name: a passage
seed: 7
start: 1805-06-14T08:00
position: 48 40 N 5 05 W
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: 0
  speed_kn: 5
  glass: true
intent: bound for Falmouth
ports: [falmouth, plymouth, brest]
wind: {{from_deg: 250, knots: {kn}, gustiness: 0.2, variability: 0.2}}
orders:
  - set plain sail
"""
FOG = """name: a June cruise in fog
seed: 7
start: 1805-06-05T06:00
position: {{lat_deg: 50.05, lon_deg: -5.02}}
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: 180
  speed_kn: 4
  glass: true
intent: cruise off the Lizard within 10 miles
ports: [falmouth, plymouth, brest]
weather:
  systems:
    - name: the high
      kind: high
      radius_km: 1200
      track:
        - {{at: 1805-06-01T00:00, x_km: 0, y_km: 0, hpa: 1028}}
orders:
  - set plain sail
"""
WRECK = "from freesail.physics import strain as ST\nfor sid in {sids!r}:\n    ST._wreck_spar(w.ship, ST.strain_state(w.ship), w.ship.spars[sid], 2.0)"
CASES = []
os.makedirs(P + "/scen", exist_ok=True)
for ship in SHIPS:
    for kn in (12, 25, 40):
        f = f"{P}/scen/pass-{ship}-{kn}.yaml"
        open(f, "w").write(PASSAGE.format(ship=ship, kn=kn))
        CASES.append({"id": f"pass|{ship}|{kn}", "scenario_file": f, "hash_every": 60,
                      "steps": [["run", 7200]]})
    f = f"{P}/scen/fog-{ship}.yaml"
    open(f, "w").write(FOG.format(ship=ship))
    CASES.append({"id": f"fog|{ship}", "scenario_file": f, "hash_every": 60, "steps": [["run", 6 * 3600]]})
# a spar broken on passage, 12 kn and 25 kn, a main working spar per square-rigger / fore-and-after
BREAK = {"frigate-36": ["main.topmast"], "seventy-four": ["fore.topmast"], "sixty-four": ["main.topmast"],
         "razee-44": ["fore.topmast"], "brig": ["main.topmast"], "hermaphrodite-brig": ["fore.topsail.yard"],
         "merchant-brig": ["main.topmast"], "privateer-schooner": ["fore.topmast"],
         "topsail-schooner": ["fore.topmast"], "cutter": ["main.topgallant_mast"], "lugger": [],
         "bilander": ["main.topsail.yard"], "smack": []}
for ship, sids in BREAK.items():
    if not sids:
        continue
    for kn in (12, 25):
        f = f"{P}/scen/pass-{ship}-{kn}.yaml"
        CASES.append({"id": f"wreck|{ship}|{kn}", "scenario_file": f, "hash_every": 60,
                      "steps": [["run", 600], ["py", WRECK.format(sids=sids)], ["run", 7200]]})
# player-ordered sequences, no captain's intent (make_world), on five ships
SEQ = [["order", "set plain sail"], ["run", 600], ["order", "tack"], ["run", 600], ["order", "wear"],
       ["run", 900], ["order", "heave to"], ["run", 600], ["order", "fill away"], ["run", 300],
       ["order", "shorten sail"], ["run", 900], ["order", "clear for action"], ["run", 900],
       ["order", "lie a-try"], ["run", 900]]
for ship in ("frigate-36", "brig", "cutter", "privateer-schooner", "seventy-four", "smack"):
    CASES.append({"id": f"seq|{ship}", "ship": f"data/ships/{ship}.yaml", "seed": 7,
                  "scenario": {"wind_from_deg": 0, "wind_speed_kn": 14, "gustiness": 0.2, "ship_heading_deg": 70,
                               "ship_speed_kn": 4},
                  "hash_every": 60, "steps": SEQ})
CASES.append({"id": "anchor|tender", "scenario_file": "data/scenarios/tender.yaml", "hash_every": 60,
              "steps": [["order", "get under way"], ["run", 2400], ["order", "come to an anchor"], ["run", 2400]]})
CASES.append({"id": "anchor|first-action", "scenario_file": "data/scenarios/first-action.yaml", "hash_every": 60,
              "steps": [["run", 4 * 3600]]})
