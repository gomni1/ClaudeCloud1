# N-2026-11-12-2: numerical confirmation of the period scaling (frozen in NIGHT-QUEUE-2026-11-12.md).
# Uses item 1's code and rules unchanged; the cycle rule's absolute state tolerance is scaled by the total T.
import importlib.util, json, numpy as np
sp = importlib.util.spec_from_file_location('h', 'N-2026-11-12-1-run.py'); h = importlib.util.module_from_spec(sp); sp.loader.exec_module(h)
R = h.regen(); out = {}
base_ct = h.cycle_test
for n in h.DRAWS:
    k, m, kr = R[n]
    ref = json.load(open('N-2026-11-12-1-draw-%d-output.json' % n))['starts']['interior-a']['period']
    T = 7.3
    h.cycle_test = lambda te, ye, T=T: base_ct(te, [v / T for v in ye])
    S = h.make_model(k, m, kr, T=T); r1 = h.classify(S, T * np.array([0.25, 0.25, 0.25, 0.25]))
    h.cycle_test = base_ct
    S2 = h.make_model([2 * v for v in k], m, kr); r2 = h.classify(S2, np.array([0.25, 0.25, 0.25, 0.25]))
    ratT = r1.get('period', float('nan')) / ref; ratS = r2.get('period', float('nan')) / ref
    out[n] = dict(period_T1=ref, verdict_T73=r1['verdict'], period_T73=r1.get('period'), ratio_T=ratT, check_i_pass=bool(abs(ratT - 1) < 1e-6),
                  verdict_2x=r2['verdict'], period_2x=r2.get('period'), ratio_s=ratS, check_ii_pass=bool(abs(ratS - 0.5) < 1e-6),
                  plant_check_i_on_2x_run_pass=bool(abs(ratS - 1) < 1e-6))
    print(n, out[n], flush=True)
json.dump(out, open('N-2026-11-12-2-scaling-output.json', 'w'), indent=1)
