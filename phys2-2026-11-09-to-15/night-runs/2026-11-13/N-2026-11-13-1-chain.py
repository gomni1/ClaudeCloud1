# N-2026-11-13-1, part P2 (frozen in NIGHT-QUEUE-2026-11-13.md): one clock as a bare sequence of steps.
# The simulation receives m, kr and the seven ratios k_j/k10 only. There is no time variable and no absolute rate.
# Usage: python3 N-2026-11-13-1-chain.py <summary12.json> <psi-output.json> <out.json>
import json, sys, time, random
from scipy.special import betainc

S12 = json.load(open(sys.argv[1])); PSI = json.load(open(sys.argv[2])); OUT = sys.argv[3]
draws = [d for d in PSI if not d.startswith('_')]
d = min(draws, key=lambda q: PSI[q]['psi'])          # rule fixed in the queue: smallest Psi
rec = S12[d]; m, kr = rec['m'], rec['kr']
k = rec['k']; ref = k['k10']
r1, r2, r3, r5, r6, r7, r8 = (k[n] / ref for n in ('k1', 'k2', 'k3', 'k5', 'k6', 'k7', 'k8'))   # the only rate inputs
a, b = rec['swing_min'][0], rec['swing_max'][0]
lo, hi = a + 0.2 * (b - a), a + 0.6 * (b - a)
psi = PSI[d]['psi']; y0 = PSI[d]['runs']['s=1,T=1']['y0']
frac_pred = PSI[d]['psi_fractions']

def run(N, max_steps, max_turns, seed, every=1):
    rnd = random.Random(seed).random
    F = [float(betainc(kr, m - kr + 1, c / N)) for c in range(N + 1)]
    gV = [1.0 + r3 * f for f in F]                     # seeding (ratio 1) + recruitment, per unit of Void
    nC = round(y0[0] * N); nL = round(y0[2] * N); nP = round(y0[3] * N); nV = N - nC - nL - nP
    cC = r1 + r2 + r7; cL = r5 + r6
    cnt = [0] * 8                                      # w1 w2 w7 w6 w5 w8 w10 w3
    marks = []; armed = False; nlo = lo * N; nhi = hi * N
    step = 0; counted = 0
    while step < max_steps and len(marks) < max_turns + 1:
        wC = cC * nC; wL = cL * nL; wP = r8 * nP; wV = gV[nC] * nV
        u = rnd() * (wC + wL + wP + wV)
        if u < wC:
            nC -= 1
            if u < r1 * nC + r1: nL += 1; cnt[0] += 1          # (nC+1)*r1 before the decrement
            elif u < (r1 + r2) * (nC + 1): nV += 1; cnt[1] += 1
            else: nP += 1; cnt[2] += 1
        elif u < wC + wL:
            nL -= 1
            if u - wC < r6 * (nL + 1): nC += 1; cnt[3] += 1
            else: nV += 1; cnt[4] += 1
        elif u < wC + wL + wP:
            nP -= 1; nV += 1; cnt[5] += 1
        else:
            if (u - wC - wL - wP) < nV: cnt[6] += 1            # seeding share: 1 of gV
            else: cnt[7] += 1
            nV -= 1; nC += 1
        step += 1
        if step % every == 0: counted += 1
        if armed:
            if nC > nhi: marks.append(counted); armed = False
        elif nC < nlo: armed = True
    iv = [(marks[i + 1] - marks[i]) / N for i in range(len(marks) - 1)]
    iv = iv[1:]                                        # first interval discarded
    out = dict(N=N, steps=step, turns_counted=len(marks), intervals_used=len(iv), every=every)
    if len(iv) >= 2:
        mu = sum(iv) / len(iv); sd = (sum((x - mu)**2 for x in iv) / (len(iv) - 1))**0.5
        out.update(mean_steps_per_unit_per_turn=mu, cv=sd / mu, ratio_to_psi=mu / psi,
                   min_interval=min(iv), max_interval=max(iv))
    tot = sum(cnt)
    names = ['w1 C>L', 'w2 C>V', 'w7 C>P', 'w6 L>C', 'w5 L>V', 'w8 P>V', 'w10 V>C seed', 'w3 V>C recruit']
    out['step_fractions'] = {n: c / tot for n, c in zip(names, cnt)}
    out['final_shares'] = [nC / N, nV / N, nL / N, nP / N]
    return out

def label(o):
    ticks = o['turns_counted'] - 1 >= 20 and o.get('cv', 9) < 0.2
    agrees = ticks and abs(o['ratio_to_psi'] - 1) < 0.05
    return dict(ticks_in_step_count=bool(ticks), agrees_with_psi=bool(agrees))

res = dict(draw=d, m=m, kr=kr, ratios_to_k10=dict(r1=r1, r2=r2, r3=r3, r5=r5, r6=r6, r7=r7, r8=r8),
           psi=psi, hysteresis=[lo, hi], predicted_fractions=frac_pred)
# pilot: 2e5 steps at N = 20000, timed; choose N1
t = time.time(); run(20000, 200000, 10**9, 1); per = (time.time() - t) / 2e5
res['pilot'] = dict(seconds_per_step=per)
N1 = None
for N in (20000, 5000, 2000):
    if 30 * N * psi * per <= 600: N1 = N; break
res['pilot']['N1'] = N1; res['pilot']['projected_seconds_30_turns'] = 30 * N1 * psi * per
print('pilot', res['pilot'], flush=True)
res['runs'] = {}
for N in (N1, N1 // 4):
    t = time.time(); o = run(N, int(60 * N * psi), 30, 20261113)
    o['label'] = label(o); o['seconds'] = round(time.time() - t, 1)
    res['runs'][str(N)] = o; print(N, o, flush=True)
    if o['label']['agrees_with_psi']:
        p = run(N, int(60 * N * psi), 30, 20261113, every=2)   # planted failure F2: count every second step
        p['label'] = label(p); p['F2_tripped'] = not p['label']['agrees_with_psi']
        res['runs'][str(N) + '_F2'] = p; print(N, 'F2', {q: p[q] for q in ('ratio_to_psi', 'label', 'F2_tripped')}, flush=True)
    else:
        res['runs'][str(N) + '_F2'] = 'not applicable: main comparison did not pass'
json.dump(res, open(OUT, 'w'), indent=1)
