# N-2026-11-11-2: 50-digit re-verification of outer-unstable flags (first 20 as frozen;
# then, report-only, every low-share flag stored).
import json, mpmath as mp
mp.mp.dps = 50
d = json.load(open('N-2026-11-11-2-num-output.json'))
def verify(case):
    k1,k2,k3,k5,k6,k7,k8,k10 = [mp.mpf(v) for v in case['k']]
    m, kr = case['m'], case['kr']; a, b = kr, m-kr+1
    F = lambda x: mp.betainc(a, b, 0, x, regularized=True)
    Fp = lambda x: x**(a-1)*(1-x)**(b-1)/mp.beta(a, b)
    D = k2 + k7 + k1*k5/(k5+k6); c = 1 + k1/(k5+k6) + k7/k8
    G = lambda x: (k10 + k3*F(x))*(1 - c*x) - D*x
    x = mp.findroot(G, mp.mpf(case['x']), tol=mp.mpf(10)**-45)
    C = x; L = k1*x/(k5+k6); P = k7*x/k8; V = 1 - c*x
    rho = k3*F(x); rp = k3*Fp(x)
    dx = [1-C, -C, -C, -C]
    J = mp.matrix([[-(k1+k2+k7), k10+rho, k6, 0], [k2, -(k10+rho), k5, k8], [k1, 0, -(k5+k6), 0], [k7, 0, 0, -k8]])
    for j in range(4): J[0, j] += V*rp*dx[j]; J[1, j] -= V*rp*dx[j]
    B = mp.matrix([[1,0,0],[-1,-1,-1],[0,1,0],[0,0,1]])
    M = (B.T*B)**-1*B.T*J*B
    ev = mp.eig(M)[0]
    return float(abs(G(x))), max(float(mp.re(e)) for e in ev), [complex(e) for e in ev]
out = dict(frozen=[], report_only_low=[])
for case in d['outer_unstable'][:20]:
    r, mx, ev = verify(case)
    out['frozen'].append(dict(which=case['which'], m=case['m'], kr=case['kr'], residual=r, maxre=mx, ev=[[e.real, e.imag] for e in ev], unstable=mx > 0))
for case in [c for c in d['outer_unstable'] if c['which'] == 'low-share']:
    r, mx, ev = verify(case)
    out['report_only_low'].append(dict(m=case['m'], kr=case['kr'], residual=r, maxre=mx, ev=[[e.real, e.imag] for e in ev], unstable=mx > 0, k=case['k'], x=case['x']))
json.dump(out, open('N-2026-11-11-2-mpverify-output.json', 'w'), indent=1)
print('frozen: verified unstable', sum(o['unstable'] for o in out['frozen']), 'of', len(out['frozen']), '; max residual', max(o['residual'] for o in out['frozen']))
print('low-share stored:', len(out['report_only_low']), 'verified unstable', sum(o['unstable'] for o in out['report_only_low']))
for o in out['report_only_low']: print(o['m'], o['kr'], o['maxre'], [ (round(a,4),round(b,4)) for a,b in o['ev']])
from collections import Counter
print('which in stored 200:', Counter(c['which'] for c in d['outer_unstable']))
print('kr of first 20 frozen', [o['kr'] for o in out['frozen']], 'complex?', [any(abs(b)>1e-12 for a,b in o['ev'] if a>0) for o in out['frozen']])
