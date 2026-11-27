import os, glob
P = os.environ.get("P125", "/tmp/claude-0/-home-user-FreeSail/e2d459f1-79d4-50d6-9285-0413fe7ccd0b/scratchpad/rev125-probes")
SHIPS = sorted(os.path.basename(f)[:-5] for f in glob.glob("data/ships/*.yaml"))
PASSAGE = """name: a passage
seed: {seed}
start: 1805-06-14T08:00
position: 48 40 N 5 05 W
region: channel-west
nation: britain
ship:
  file: data/ships/{ship}.yaml
  heading_deg: {hd}
  speed_kn: 5
  glass: true
intent: bound for Falmouth
ports: [falmouth, plymouth, brest]
wind: {{from_deg: {wfrom}, knots: {kn}, gustiness: 0.2, variability: 0.2}}
orders:
  - set plain sail
"""
CASES = []
os.makedirs(P + "/scen", exist_ok=True)
for ship in SHIPS:
    for kn in (12, 25, 40):
        f = f"{P}/scen/pass-{ship}-{kn}.yaml"
        open(f, "w").write(PASSAGE.format(ship=ship, kn=kn, seed=7, hd=0, wfrom=250))
        CASES.append({"id": f"pass|{ship}|{kn}", "scenario_file": f, "hash_every": 60, "steps": [["run", 7200]]})
# beating to a port dead to windward (Falmouth to the north, the wind from the north), 20 kn, 2 h
for ship in ("brig", "merchant-brig", "frigate-36", "hermaphrodite-brig"):
    for seed in (7, 3, 11):
        f = f"{P}/scen/beat-{ship}-{seed}.yaml"
        open(f, "w").write(PASSAGE.format(ship=ship, kn=20, seed=seed, hd=300, wfrom=0))
        CASES.append({"id": f"beat|{ship}|{seed}", "scenario_file": f, "hash_every": 60, "steps": [["run", 7200]]})
TR = "data/scenarios/trials"
# the other four trials' logs are pinned by digest in tests/test_captain_trials.py (run there)
for name in ("trial-station-lee-shore",):
    CASES.append({"id": f"trial|{name}", "scenario_file": f"{TR}/{name}.yaml", "hash_every": 300,
                  "steps": [["run", 20 * 3600]]})
