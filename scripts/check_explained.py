"""Check one or more data/explained/book-NN.json files: python3 scripts/check_explained.py 4 5"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from medit.parse import EXPLAINED_DIR, load_passages  # noqa: E402
from tests.test_explained import FORBIDDEN, words  # noqa: E402

ok = True
ps = load_passages()
for b in map(int, sys.argv[1:]):
    f = EXPLAINED_DIR / f"book-{b:02d}.json"
    want = {p["id"] for p in ps if p["book"] == b}
    data = json.loads(f.read_text(encoding="utf-8"))
    probs = [f"missing {i}" for i in sorted(want - set(data))] + [f"extra {i}" for i in sorted(set(data) - want)]
    for i, x in data.items():
        if not isinstance(x, dict) or not set(x) <= {"summary", "today"} or "summary" not in x:
            probs.append(f"{i}: bad shape"); continue
        if not 20 <= words(x["summary"]) <= 170: probs.append(f'{i}: summary {words(x["summary"])} words')
        if "today" in x and not 12 <= words(x["today"]) <= 110: probs.append(f'{i}: today {words(x["today"])} words')
        for k, t in x.items():
            if FORBIDDEN.search(t): probs.append(f"{i}.{k}: forbidden {FORBIDDEN.search(t).group()!r}")
            if "\n" in t.replace("\n\n", "") or t != t.strip(): probs.append(f"{i}.{k}: whitespace")
    share = sum("today" in x for x in data.values()) / max(len(data), 1)
    print(f"book {b}: {len(data)}/{len(want)} passages, today on {share:.0%}, {len(probs)} problems")
    for p in probs: print("  ", p)
    ok &= not probs
sys.exit(0 if ok else 1)
