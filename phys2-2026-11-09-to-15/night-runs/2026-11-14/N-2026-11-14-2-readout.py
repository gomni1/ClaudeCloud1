#!/usr/bin/env python3
"""N-2026-11-14-2: which readouts P(R) of an additive plane resultant have no third-order term?
Follows NIGHT-QUEUE-2026-11-14.md (frozen). Plant first, then 10 000 random triples."""
import numpy as np, json
def I3(P, a, b, c):
    return P(a+b+c) - P(a+b) - P(a+c) - P(b+c) + P(a) + P(b) + P(c) - P(np.zeros_like(a))
n2 = lambda R: (R**2).sum(axis=-1)
e = np.array([0.6, 0.8])
READ = {
 '|R|^1':   lambda R: n2(R)**0.5,
 '|R|^1.5': lambda R: n2(R)**0.75,
 '|R|^2':   lambda R: n2(R),
 '|R|^2.5': lambda R: n2(R)**1.25,
 '|R|^3':   lambda R: n2(R)**1.5,
 '|R|^4':   lambda R: n2(R)**2,
 'aniso quad Rx^2+3Ry^2+RxRy': lambda R: R[...,0]**2 + 3*R[...,1]**2 + R[...,0]*R[...,1],
 '|R|^2 + e.R': lambda R: n2(R) + R @ e,
 '1-exp(-|R|^2)': lambda R: 1 - np.exp(-n2(R)),
}
one = np.array([[1.0, 0.0]])
plant = {'|R|^4 at (1,0)x3 (must be 36)': float(I3(READ['|R|^4'], one, one, one)[0]),
         '|R|^2 at (1,0)x3 (must be 0)': float(I3(READ['|R|^2'], one, one, one)[0])}
ok = plant['|R|^4 at (1,0)x3 (must be 36)'] == 36.0 and plant['|R|^2 at (1,0)x3 (must be 0)'] == 0.0
print('plant', plant, 'PASS' if ok else 'FAIL: check void')
rng = np.random.default_rng(20261114)
a, b, c = (rng.uniform(-3, 3, (10000, 2)) for _ in range(3))
res = {}
for name, P in READ.items():
    i3 = I3(P, a, b, c)
    allP = np.concatenate([P(a+b+c), P(a+b), P(a+c), P(b+c), P(a), P(b), P(c)])
    res[name] = dict(max_abs_I3=float(np.abs(i3).max()), max_abs_P=float(np.abs(allP).max()),
                     rel=float(np.abs(i3).max()/np.abs(allP).max()), min_P=float(allP.min()))
    print(f"{name:30s} max|I3|/max|P| = {res[name]['rel']:.3e}   min P = {res[name]['min_P']:.3g}")
json.dump(dict(plant=plant, plant_pass=ok, results=res), open('N-2026-11-14-2-readout-output.json', 'w'), indent=1)
