import os, glob
P = os.environ.get("P126")
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
wind: {{from_deg: {frm}, knots: {kn}, gustiness: {g}, variability: {g}}}
orders:
  - set plain sail
"""
CASES = []
os.makedirs(P + "/scen4", exist_ok=True)
for ship in SHIPS:
    for tag, frm, kn, g, secs in (("12", 250, 12, 0.2, 7200), ("galeW", 270, 40, 0.0, 10800), ("gale250", 250, 40, 0.2, 10800)):
        f = f"{P}/scen4/{tag}-{ship}.yaml"
        open(f, "w").write(PASSAGE.format(ship=ship, kn=kn, frm=frm, g=g))
        CASES.append({"id": f"{tag}|{ship}", "scenario_file": f, "hash_every": 60, "steps": [["run", secs]]})
SEQ = [["order", "set plain sail"], ["run", 600], ["order", "tack"], ["run", 600], ["order", "wear"],
       ["run", 900], ["order", "heave to"], ["run", 600], ["order", "fill away"], ["run", 300],
       ["order", "shorten sail"], ["run", 900], ["order", "clear for action"], ["run", 900],
       ["order", "lie a-try"], ["run", 900]]
for ship in ("frigate-36", "brig", "cutter", "privateer-schooner", "seventy-four", "smack", "corvette-20"):
    CASES.append({"id": f"seq|{ship}", "ship": f"data/ships/{ship}.yaml", "seed": 7,
                  "scenario": {"wind_from_deg": 0, "wind_speed_kn": 14, "gustiness": 0.2, "ship_heading_deg": 70,
                               "ship_speed_kn": 4}, "hash_every": 60, "steps": SEQ})
CASES.append({"id": "anchor|first-action", "scenario_file": "data/scenarios/first-action.yaml", "hash_every": 60,
              "steps": [["run", 4 * 3600]]})
