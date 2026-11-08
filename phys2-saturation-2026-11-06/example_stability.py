"""Report-only: eigenvalues at the three balances of N3's worked example (open level, draw 4891)."""
import json
import numpy as np
from checks import stability, make_rhs
r = json.load(open("result_N3.json"))["example_open_three"]
k = np.array(r["k"])
out = []
for b in r["bal"]:
    y = [b["C"], b["V"], b["L"], b["P"]]
    res = np.abs(make_rhs(k, "TH", r["m"], r["kr"], 1, 1)(0, y)).max()
    ev = stability(k, r["m"], r["kr"], y, 1)
    out.append(dict(C=b["C"], V=b["V"], residual=float(res), eig=[[float(z.real), float(z.imag)] for z in ev],
                    stable=bool(np.all(ev.real < 0))))
    print(f"C={b['C']:.4f} V={b['V']:.4f} residual={res:.2e} stable={np.all(ev.real<0)} eig={np.round(ev,4)}")
json.dump(out, open("result_example_stability.json", "w"), indent=1)
