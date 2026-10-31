"""After K1: pick the (at most 2) verified K1 cycles with the smallest span and write k2 start files."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import k1  # noqa: E402

EV = k1.EV
cyc = []
for fn in ("k1_records.jsonl", "k1c_records.jsonl"):
    for l in open(os.path.join(EV, fn)):
        r = json.loads(l)
        if r.get("sub") in ("K1a", "K1b"):
            pairs = [(ru["cls"], v) for ru, v in zip([x for x in r.get("runs", []) if x["cls"]["kind"] == "periodic"],
                                                     r.get("verify", []))]
        elif r.get("sub") == "K1c":
            pairs = [(it["second"], it["verify"]) for it in r.get("second", []) if "verify" in it]
        else:
            continue
        for cls, v in pairs:
            if v["verified"]:
                d = (k1.draw_b if r["sub"] == "K1b" or r.get("src") == "K1b" else k1.m2.draw_params)(r["i"])
                cyc.append(dict(span=r["span"], draw=d, point=cls["point"], period=v["periods"]["Radau"]["period"],
                                sub=r["sub"]))
                break
cyc.sort(key=lambda c: c["span"])
sel = []
for c in cyc:
    if c["draw"]["i"] not in [s["draw"]["i"] for s in sel]:
        sel.append(c)
sel = sel[:2]
for j, c in enumerate(sel):
    json.dump(c, open(os.path.join(EV, "k2_start_%d.json" % j), "w"))
print(json.dumps([(c["sub"], c["draw"]["i"], c["draw"]["level"], c["span"]) for c in sel]))
