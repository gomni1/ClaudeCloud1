# N-2026-11-11-1 report-only diagnostic (written after the run, not a check):
# where the six 'other' starts are at t_end, relative to each balance, and the decay expected
# from the high-Void balance's slowest eigenvalue.
import json, numpy as np
d = json.load(open('N-2026-11-11-1-cycle-output.json'))
B = [np.array([d['pins']['C'], b['V'], d['pins']['L'], d['pins']['P']]) for b in d['balances']]
lam_slow = d['balances'][2]['eig'][0][0]
for k, v in d['starts'].items():
    y = np.array(v['yT'])
    dist = [float(np.linalg.norm(y-b)/np.linalg.norm(b)) for b in B]
    print(k, 'crossings', v['n_crossings'], 'yT', np.round(y, 4).tolist(), 'reldist(low,mid,high)', [round(x, 4) for x in dist])
print('slowest eigenvalue at high-Void balance', lam_slow, '; exp(lam*2e4) =', np.exp(lam_slow*2e4))
print('expected relative V offset if started at the low-Void V:', (d['balances'][0]['V']-d['balances'][2]['V'])/d['balances'][2]['V']*np.exp(lam_slow*2e4))
