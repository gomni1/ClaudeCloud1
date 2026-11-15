# N-2026-11-11-2 numerical harness (frozen in NIGHT-QUEUE-2026-11-11.md). Closed level, T = 1.
import json, sys, time
import numpy as np
from scipy.optimize import brentq
from scipy.special import betainc, betaln

rng = np.random.default_rng(20261111)
B = np.array([[1,0,0],[-1,-1,-1],[0,1,0],[0,0,1]], float)
BtBinvBt = np.linalg.inv(B.T@B)@B.T

def draw():
    k = 10**rng.uniform(-2, 2, 8)  # k1,k2,k3,k5,k6,k7,k8,k10
    m = int(rng.integers(2, 31)); kr = int(rng.integers(2, m+1))
    return k, m, kr

def analyse(k, m, kr, plant=False):
    k1,k2,k3,k5,k6,k7,k8,k10 = k
    a, b = kr, m-kr+1
    F = lambda x: betainc(a, b, x)
    Fp = lambda x: np.exp((a-1)*np.log(x)+(b-1)*np.log1p(-x)-betaln(a, b))
    D = k2 + k7 + k1*k5/(k5+k6); c = 1 + k1/(k5+k6) + k7/k8
    G = lambda x: (k10 + k3*F(x))*(1 - c*x) - D*x
    xe = 1/c
    xs = np.linspace(0, xe, 4001)
    gv = G(xs); gv[0] = k10; gv[-1] = -D/c
    idx = np.nonzero(gv[:-1]*gv[1:] < 0)[0]
    if len(idx) != 3: return None
    roots = [brentq(G, xs[i], xs[i+1], xtol=1e-15, rtol=1e-15) for i in idx]
    out = []
    for x in roots:
        C = x; L = k1*x/(k5+k6); P = k7*x/k8; V = 1 - c*x
        rho = k3*F(x); rp = k3*Fp(x)
        dx = np.array([(1-C), -C, -C, -C])  # T = 1
        J = np.array([[-(k1+k2+k7), k10+rho, k6, 0], [k2, -(k10+rho), k5, k8], [k1, 0, -(k5+k6), 0], [k7, 0, 0, -k8]], float)
        J[0] += V*rp*dx; J[1] -= V*rp*dx
        M = BtBinvBt@J@B
        lam = np.linalg.eigvals(M)
        e3 = float(np.real(np.prod(lam)))
        Hp = rp*(1 - c*x) - c*(k10 + rho) - D
        K = k8*(k5+k6)
        err = abs(e3 - K*Hp)/(abs(e3) + abs(K*Hp))
        mx = float(np.max(lam.real)); scale = float(np.max(np.abs(lam)))
        rec = dict(x=x, maxre=mx, scale=scale, Hp=float(Hp), relerr=float(err))
        if plant:
            pass
        out.append((rec, M))
    return out

res = dict(n_draws=0, n_three=0, identity_flags=0, max_relerr=0.0, middle_stable=0, min_middle_maxre=None,
           outer_unstable=[], outer_unstable_low=0, outer_unstable_high=0, Hp_sign_pattern_violations=0,
           P2_tested=0, P2_tripped=0)
t0 = time.time(); PILOT = 2000; pilot_done = False
while res['n_three'] < 20000 and time.time()-t0 < 1800:
    k, m, kr = draw(); res['n_draws'] += 1
    r = analyse(k, m, kr)
    if not pilot_done and res['n_draws'] == PILOT:
        res['pilot'] = dict(draws=PILOT, seconds=round(time.time()-t0, 2), three=res['n_three']); pilot_done = True
        print('pilot', res['pilot'], flush=True)
    if r is None: continue
    res['n_three'] += 1
    recs = [a for a, _ in r]
    for a in recs:
        res['max_relerr'] = max(res['max_relerr'], a['relerr'])
        if a['relerr'] > 1e-6: res['identity_flags'] += 1
    if not (recs[0]['Hp'] < 0 and recs[1]['Hp'] > 0 and recs[2]['Hp'] < 0): res['Hp_sign_pattern_violations'] += 1
    mid = recs[1]
    res['min_middle_maxre'] = mid['maxre'] if res['min_middle_maxre'] is None else min(res['min_middle_maxre'], mid['maxre'])
    if mid['maxre'] <= 0: res['middle_stable'] += 1
    for j, name in ((0, 'low-share'), (2, 'high-share')):
        a = recs[j]
        if a['maxre'] > 1e-9*a['scale']:
            if name == 'low-share': res['outer_unstable_low'] += 1
            else: res['outer_unstable_high'] += 1
            if len(res['outer_unstable']) < 200:
                res['outer_unstable'].append(dict(which=name, k=k.tolist(), m=m, kr=kr, x=a['x'], maxre=a['maxre']))
    if res['P2_tested'] < 200:
        M0 = r[0][1]; lam = np.linalg.eigvals(M0); s = 1 - np.max(lam.real)
        lam2 = np.linalg.eigvals(M0 + s*np.eye(3)); mx = np.max(lam2.real)
        res['P2_tested'] += 1
        if mx > 1e-9*np.max(np.abs(lam2)): res['P2_tripped'] += 1
res['seconds'] = round(time.time()-t0, 1)
json.dump(res, open('N-2026-11-11-2-num-output.json', 'w'), indent=1)
print({k: v for k, v in res.items() if k != 'outer_unstable'})
