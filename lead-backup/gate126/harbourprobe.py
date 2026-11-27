"""Harbour end probe against a live server (py -m freesail --no-browser) on PORT."""
import json
import sys
import time
import urllib.request

BASE = f"http://localhost:{sys.argv[1]}"
import re
MARK = re.search(r'name="freesail-page" content="([^"]+)"', urllib.request.urlopen(BASE + "/harbour").read().decode()).group(1)


def call(method, path, body=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method,
                                 headers={"Content-Type": "application/json", "x-freesail-page": MARK, "origin": BASE})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def show(label, got):
    st, js = got
    if isinstance(js, dict) and "lines" in js:
        out = {"lines": js["lines"], "started": js.get("game", {}).get("started"),
               "games": js.get("game", {}).get("games")}
    else:
        out = js
    print(f"{label}: {st} {json.dumps(out)[:600]}")
    return got


show("1 end with no game", call("POST", "/api/harbour/end", {}))
show("2 start tender", call("POST", "/api/harbour/start", {"scenario": "data/scenarios/tender.yaml"}))
show("2b end at once", call("POST", "/api/harbour/end", {}))
show("3 end twice", call("POST", "/api/harbour/end", {}))
show("3b end twice lose", call("POST", "/api/harbour/end", {"lose_unsaved": True}))
show("4 start", call("POST", "/api/harbour/start", {"scenario": "data/scenarios/tender.yaml"}))
show("4a order", call("POST", "/api/order", {"text": "set plain sail"}))
show("4b go", call("POST", "/api/driver", {"action": "go"}))
time.sleep(3)
show("4c end unsaved", call("POST", "/api/harbour/end", {}))
show("4d state still started", (200, call("GET", "/api/harbour/state")[1]["game"]["started"]))
show("4e end lose", call("POST", "/api/harbour/end", {"lose_unsaved": True}))
show("5 start", call("POST", "/api/harbour/start", {"scenario": "data/scenarios/tender.yaml"}))
show("5a tick", call("POST", "/api/driver", {"action": "tick", "value": 120}))
show("5b save", call("POST", "/api/order", {"text": "save " + sys.argv[2] + "/probe-save.json"}))
show("5c end after save", call("POST", "/api/harbour/end", {}))
st, saves = call("GET", "/api/harbour/state")
print("5d state keys", sorted(saves.keys()) if isinstance(saves, dict) else saves)
show("6 start another", call("POST", "/api/harbour/start", {"scenario": "data/scenarios/smack-falmouth.yaml"}))
show("6a state", (200, {k: call("GET", "/api/harbour/state")[1]["game"].get(k) for k in ("started", "title", "games")}))
show("6b end", call("POST", "/api/harbour/end", {}))
# the save from 5 taken up, ended at once; again, played, ended
show("7 load save", call("POST", "/api/harbour/start", {"load": "probe-save.json"}))
show("7a end at once", call("POST", "/api/harbour/end", {}))
show("8 load save", call("POST", "/api/harbour/start", {"load": "probe-save.json"}))
show("8a tick", call("POST", "/api/driver", {"action": "tick", "value": 60}))
show("8b end", call("POST", "/api/harbour/end", {}))
show("8c end lose", call("POST", "/api/harbour/end", {"lose_unsaved": True}))
show("9 load once more after the end", call("POST", "/api/harbour/start", {"load": "probe-save.json"}))
show("9a end", call("POST", "/api/harbour/end", {}))
