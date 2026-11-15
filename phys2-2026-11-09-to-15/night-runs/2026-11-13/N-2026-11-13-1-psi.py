# N-2026-11-13-1, part P1 (frozen in NIGHT-QUEUE-2026-11-13.md).
# Steps per unit per turn (Psi) on the five known closed-level clocks, with scaling checks and planted failure F1.
# Usage: python3 N-2026-11-13-1-psi.py <summary12.json> <out.json>
import json, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import betainc

SUM, OUT = sys.argv[1], sys.argv[2]
S12 = json.load(open(SUM))
ORDER = ['k1', 'k2', 'k3', 'k5', 'k6', 'k7', 'k8', 'k10']
NAMES = ['w1 C>L', 'w2 C>V', 'w7 C>P', 'w6 L>C', 'w5 L>V', 'w8 P>V', 'w10 V>C seed', 'w3 V>C recruit']

# --- regenerate the draws independently of the summary file (draw n = (n+1)-th call, seed 20261111)
def regen(targets):
    rng = np.random.default_rng(20261111); out = {}; last = max(targets)
    for it in range(last + 1):
        k = 10**rng.uniform(-2, 2, 8); m = int(rng.integers(2, 31)); kr = int(rng.integers(2, m + 1))
        if it in targets: out[it] = (k.copy(), m, kr)
    return out

def weights(y, k, m, kr):
    C, V, L, P = y; T = C + V + L + P
    k1, k2, k3, k5, k6, k7, k8, k10 = k
    F = betainc(kr, m - kr + 1, min(max(C / T, 0.0), 1.0))
    return np.array([k1*C, k2*C, k7*C, k6*L, k5*L, k8*P, k10*V, k3*F*V]), T

def rhs(t, z, k, m, kr):
    w, T = weights(z[:4], k, m, kr)
    w1, w2, w7, w6, w5, w8, w10, w3 = w
    dC = -(w1 + w2 + w7) + w6 + w10 + w3
    dV = w2 + w5 + w8 - w10 - w3
    dL = w1 - w6 - w5
    dP = w7 - w8
    # eight running integrals of w_j/T, and a ninth of the constant 1 (the planted fixed-rate tick, never scaled)
    return np.concatenate(([dC, dV, dL, dP], w / T, [1.0]))

def one_turn(k, m, kr, T, theta_guess, mid):
    kw = dict(method='LSODA', rtol=1e-10, atol=1e-13, args=(k, m, kr))
    z = np.concatenate((T * np.array([0.25, 0.25, 0.25, 0.25]), np.zeros(9)))
    z = solve_ivp(rhs, (0, 30 * theta_guess), z, **kw).y[:, -1]
    ev = lambda t, z, *a: z[0] / (z[0] + z[1] + z[2] + z[3]) - mid
    ev.terminal = True; ev.direction = 1
    s = solve_ivp(rhs, (0, 5 * theta_guess), z, events=ev, **kw)
    assert s.t_events[0].size == 1, 'no first crossing'
    z = s.y_events[0][0].copy(); z[4:] = 0.0; y0 = z[:4].copy()
    # step off the section, then run to the next upward crossing
    h = 1e-4 * theta_guess
    z = solve_ivp(rhs, (0, h), z, **kw).y[:, -1]
    s = solve_ivp(rhs, (h, 5 * theta_guess), z, events=ev, **kw)
    assert s.t_events[0].size == 1, 'no second crossing'
    theta = float(s.t_events[0][0]); zf = s.y_events[0][0]
    return dict(theta=theta, psi_j=zf[4:12].tolist(), psi=float(zf[4:12].sum()), tick=float(zf[12]),
                closure=float(np.max(np.abs(zf[:4] - y0)) / T), y0=(y0 / T).tolist())

def rel(a, b): return abs(a - b) / abs(b)

res = {}; t0 = time.time()
targets = [int(d) for d in S12]
RG = regen(set(targets))
for d in targets:
    rec = S12[str(d)]
    k = np.array([rec['k'][n] for n in ORDER]); m, kr = rec['m'], rec['kr']
    kg, mg, krg = RG[d]
    regen_ok = bool(np.array_equal(k, kg) and m == mg and kr == krg)
    th12 = rec['period']; a, b = rec['swing_min'][0], rec['swing_max'][0]; mid = 0.5 * (a + b)
    base = one_turn(k, m, kr, 1.0, th12, mid)
    runs = {'s=1,T=1': base,
            's=2,T=1': one_turn(2 * k, m, kr, 1.0, th12 / 2, mid),
            's=0.37,T=1': one_turn(0.37 * k, m, kr, 1.0, th12 / 0.37, mid),
            's=1,T=7.3': one_turn(k, m, kr, 7.3, th12, mid)}
    chk = {}
    chk['theta_vs_12Nov_rel'] = rel(base['theta'], th12)
    chk['well_posed'] = chk['theta_vs_12Nov_rel'] < 1e-6
    worst = 0.0; worst_j = 0.0
    for name, r in runs.items():
        if name == 's=1,T=1': continue
        worst = max(worst, rel(r['psi'], base['psi']))
        for j in range(8):
            if base['psi_j'][j] > 1e-9 * base['psi']:
                worst_j = max(worst_j, rel(r['psi_j'][j], base['psi_j'][j]))
    chk['psi_worst_rel'] = worst; chk['psi_j_worst_rel'] = worst_j
    chk['psi_invariant'] = bool(worst < 1e-6 and worst_j < 1e-6)
    chk['theta_ratio_s2'] = runs['s=2,T=1']['theta'] / base['theta']
    chk['theta_ratio_ok'] = abs(chk['theta_ratio_s2'] - 0.5) < 1e-6
    chk['theta_ratio_T7.3'] = runs['s=1,T=7.3']['theta'] / base['theta']
    p = base['psi_j']
    ids = [rel(p[0], p[4] + p[3]), rel(p[2], p[5]), rel(p[1] + p[4] + p[5], p[6] + p[7])]
    chk['flux_identities_rel'] = ids; chk['flux_ok'] = bool(max(ids) < 1e-6)
    # Planted failure F1: Psi' = Psi + (integral of the unscaled tick). Same invariance test, s=2 against s=1.
    pp1 = base['psi'] + base['tick']; pp2 = runs['s=2,T=1']['psi'] + runs['s=2,T=1']['tick']
    K = float(k.sum())
    chk['F1_rel_change'] = rel(pp2, pp1); chk['F1_guaranteed_min'] = 1 / (2 * (K + 1))
    chk['F1_tripped'] = bool(chk['F1_rel_change'] > 1e-6)
    res[str(d)] = dict(m=m, kr=kr, regen_ok=regen_ok, sum_rates=K, runs=runs, checks=chk,
                       psi=base['psi'], theta=base['theta'], mean_step_rate=base['psi'] / base['theta'],
                       psi_fractions=dict(zip(NAMES, (np.array(p) / base['psi']).tolist())),
                       turnover_per_turn=dict(C_out=p[0] + p[1] + p[2], V_out=p[6] + p[7], L_out=p[3] + p[4], P_out=p[5]))
    print(d, 'm,kr', m, kr, 'regen', regen_ok, 'theta', base['theta'], 'psi', base['psi'], 'closure', base['closure'],
          {kk: (vv if not isinstance(vv, float) else float('%.3g' % vv)) for kk, vv in chk.items()}, flush=True)
res['_seconds'] = round(time.time() - t0, 1)
json.dump(res, open(OUT, 'w'), indent=1)
print('seconds', res['_seconds'])
