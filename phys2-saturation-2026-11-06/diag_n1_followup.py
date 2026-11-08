"""Report-only follow-up to diag_n1_mean.py (not declared, not a test).
Part 1: for runs below the pin whose identity holds, how much of the shortfall is the level's total still growing.
Part 2: for runs whose sampled identity fails, recompute the window mean of C by integrating it with the ODE."""
import json, numpy as np
from scipy.integrate import solve_ivp
from checks import n1_draw, make_rhs, RTOL, ATOL, I7, I8, I9, I11, I12
r = json.load(open("result_diag_n1_mean.json"))
idd = np.array([abs(x[3] - 1) for x in r])
print("sampled identity within 1e-6: %d of %d" % ((idd < 1e-6).sum(), len(r)))

def setup(i, law):
    k, m, kr, starts = n1_draw(i, law)
    rates = np.delete(k, [I11]); t_end = min(200.0 / rates.min(), 2e5)
    pin = (k[I8] + k[I9]) * k[I12] / (k[I7] * k[I9])
    return k, make_rhs(k, law, m, kr, 1, 1), starts[0], t_end, pin

print("Part 1: six lowest runs with the identity holding")
low = sorted([x for x in r if x[2] < 0.95 and abs(x[3] - 1) < 1e-6], key=lambda z: z[2])
print("runs below the pin by more than 5%% with the identity holding: %d" % len(low))
for x in low[:6]:
    i, law = int(x[0]), x[1]
    k, f, y0, t_end, pin = setup(i, law)
    tt = np.linspace(0, t_end, 2001)
    s = solve_ivp(f, (0, t_end), y0, method="LSODA", rtol=RTOL, atol=ATOL, t_eval=tt)
    h = 1000; dt = tt[-1] - tt[h]; tot = s.y.sum(0)
    a = (k[I8] + k[I9]) * ((tot[-1] - tot[h]) / dt) / k[I9] / k[I7] / pin
    b = ((s.y[3][-1] - s.y[3][h]) / dt) / k[I7] / pin
    print("draw %d %s: 1 - mean/pin %.3f | share from total still growing %.3f, from P changing %+.3f | end shares V %.3f L %.3f"
          % (i, law, 1 - x[2], a, b, s.y[1][-1] / tot[-1], s.y[2][-1] / tot[-1]))

print("Part 2: runs whose sampled identity is off by 1e-6 or more")
for x in sorted([x for x in r if abs(x[3] - 1) >= 1e-6], key=lambda z: -abs(z[3] - 1)):
    i, law = int(x[0]), x[1]
    k, f, y0, t_end, pin = setup(i, law)
    g = lambda t, y: list(f(t, y[:4])) + [y[0]]
    th = t_end / 2
    s = solve_ivp(g, (0, t_end), list(y0) + [0.0], method="LSODA", rtol=RTOL, atol=ATOL, t_eval=[th, t_end])
    a, b = s.y[:, 0], s.y[:, 1]; dt = t_end - th
    avgC = (b[4] - a[4]) / dt
    pred = ((k[I8] + k[I9]) * (k[I12] - (b[:4].sum() - a[:4].sum()) / dt) / k[I9] + (b[3] - a[3]) / dt) / k[I7]
    print("draw %d %s: sampled mean/pin %.4f, sampled identity %.4f -> integrated identity off by %.1e; integrated mean/pin %.4f"
          % (i, law, x[2], x[3], abs(avgC / pred - 1), avgC / pin))
