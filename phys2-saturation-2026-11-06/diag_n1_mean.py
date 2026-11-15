"""Report-only diagnosis of N1's second-half mean Contact vs the throughput pin (not a test)."""
import numpy as np
from scipy.integrate import solve_ivp
from checks import n1_draw, make_rhs, RTOL, ATOL, I7, I8, I9, I11, I12
import json, sys
rows = []
for i in range(600):
    law = ["TH", "MA", "SA"][i % 3]
    k, m, kr, starts = n1_draw(i, law)
    rates = np.delete(k, [I11]); t_end = min(200.0 / rates.min(), 2e5)
    pin = (k[I8] + k[I9]) * k[I12] / (k[I7] * k[I9])
    f = make_rhs(k, law, m, kr, 1, 1)
    y0 = starts[0]
    tt = np.linspace(0, t_end, 2001)
    s = solve_ivp(f, (0, t_end), y0, method="LSODA", rtol=RTOL, atol=ATOL, t_eval=tt)
    h = 1000
    ratio = s.y[0][h:].mean() / pin
    # exact identity over [t_h, t_end] with trapezoid means
    dt = tt[-1] - tt[h]
    tot = s.y.sum(0)
    avgC = np.trapezoid(s.y[0][h:], tt[h:]) / dt
    pred = ((k[I8] + k[I9]) * (k[I12] - (tot[-1] - tot[h]) / dt) / k[I9] + (s.y[3][-1] - s.y[3][h]) / dt) / k[I7]
    # longer run: does the mean approach the pin?
    s2 = solve_ivp(f, (0, 20 * t_end), y0, method="LSODA", rtol=RTOL, atol=ATOL, t_eval=np.linspace(10 * t_end, 20 * t_end, 4001))
    ratio2 = np.trapezoid(s2.y[0], s2.t) / (s2.t[-1] - s2.t[0]) / pin
    rows.append((i, law, ratio, avgC / pred, ratio2))
rows.sort(key=lambda r: abs(np.log(r[2])), reverse=True)
for r in rows[:8]:
    print("draw %d %s: mean/pin %.4f  identity %.6f  longer-run mean/pin %.4f" % r)
dev = [abs(r[2] - 1) for r in rows]; dev2 = [abs(r[4] - 1) for r in rows]
print("start 0 only, 600 draws: |mean/pin - 1| > 0.05 in %d (declared window), %d (window [10, 20] x t_end)" % (sum(d > 0.05 for d in dev), sum(d > 0.05 for d in dev2)))
print("identity max |avgC/pred - 1| = %.2e" % max(abs(r[3] - 1) for r in rows))
json.dump([list(map(lambda v: v if isinstance(v, str) else float(v), r)) for r in rows], open("result_diag_n1_mean.json", "w"))
