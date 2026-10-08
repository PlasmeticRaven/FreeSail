"""Read-only: what the harness held of the officer's conversation when the model server
refused the request for its size. Reads scratch copies of the saves' checkpoints.

usage: g10_context.py SAVE.json [SAVE.json ...]   (run from the build folder)
"""
import collections
import json
import re
import sys

from freesail.agents import tools
from freesail.core import replay as R

for path in sys.argv[1:]:
    header, world = R.read_checkpoint(R.checkpoint_path(path))
    print("=====", path.replace("\\", "/").split("/")[-1], "| end tick", header["end_tick"])
    for name, h in world.agents.items():
        turns = h.turns
        size = h._conversation_size()
        chars = sum(len(json.dumps(t.to_dict(), ensure_ascii=False)) for t in turns)
        print(f"  station {name}: {len(turns)} turns held, {chars:,} characters")
        print(f"  the harness's own count of the conversation: {size:,} tokens (4 characters to a token)")
        print(f"  budget_tokens {h.budget_tokens}, reserve {h.reserve_tokens}, threshold/again {h.handover_threshold()}, asked_at {h._handover_asked_at}")
        roles = collections.Counter(t.role for t in turns)
        print("  turns by role:", dict(roles))
        asks = 0
        folded = 0
        for i, t in enumerate(turns):
            d = t.to_dict()
            s = json.dumps(d, ensure_ascii=False)
            if "Write the watch's handover note" in s:
                asks += 1
                m = re.search(r"reached about ([\d,]+) of the ([\d,]+) tokens", s)
                print(f"    handover ASK in turn {i}: {m.group(0) if m else ''}")
            if '"reason": "the handover note"' in s:
                folded += 1
                print(f"    folded-note turn at {i}, {len(s):,} chars")
        print(f"  handover asks still in the conversation: {asks}; folded notes: {folded}")
        sizes = sorted(((len(json.dumps(t.to_dict(), ensure_ascii=False)), i) for i, t in enumerate(turns)), reverse=True)
        print("  the ten largest turns (chars, index, role, first 110 chars):")
        for n, i in sizes[:10]:
            d = turns[i].to_dict()
            print(f"    {n:>7,} [{i}] {turns[i].role}: {json.dumps(d, ensure_ascii=False)[:110]}")
        # what the text is made of: digits and punctuation tokenise worse than prose
        text = "".join(json.dumps(t.to_dict(), ensure_ascii=False) for t in turns)
        digits = sum(c.isdigit() for c in text)
        punct = sum((not c.isalnum()) and (not c.isspace()) for c in text)
        print(f"  of the characters: {digits / len(text):.1%} digits, {punct / len(text):.1%} punctuation and symbols")
        print(f"  the server counted the request at 103,679 / 103,122 tokens; that is {chars / 103679:.2f} characters to a token if the whole conversation was sent")
        ticks = [t.to_dict().get("content", {}).get("tick") if isinstance(t.to_dict().get("content"), dict) else None for t in turns]
        ticks = [x for x in ticks if isinstance(x, int)]
        if ticks:
            print(f"  the data turns run from tick {min(ticks)} to {max(ticks)}")
        print("  tools.tokens rule:", tools.tokens("x" * 400), "tokens for 400 characters")
