# N-2026-11-15-2: closed form for grain-owned jitter J(l). Arithmetic only; nothing is simulated.
# N_un = (D1 + D2) * (1 - mu(q)), q = Delta/l ; mu(q) = 1 - q/2 (q <= 1), 1/(2q) (q > 1)
# pair term multiplied by exp(-4 sigma^2 N_un); sigma* = 1/(2 sqrt(N_un)) is where it has fallen by 1/e.
import math, json
D1, D2 = 10000, 2000
def mu(q):
    if q == 0: return 1.0
    if math.isinf(q): return 0.0
    return 1 - q/2 if q <= 1 else 1/(2*q)
def N_un(Delta, l):
    q = math.inf if l == 0 else (0.0 if math.isinf(l) else Delta/l)
    return (D1 + D2)*(1 - mu(q))
out = {}
ls = [0, 1, 5, 100, 1000, math.inf]; Ds = [1, 4, 100, 200]
print('N_un (unshared-equivalent steps) and sigma* = 1/(2 sqrt(N_un))')
print('l \\ Delta ' + ''.join(f'{d:>22d}' for d in Ds))
for l in ls:
    row = []
    for d in Ds:
        n = N_un(d, l); s = math.inf if n == 0 else 1/(2*math.sqrt(n))
        out[f'l={l},Delta={d}'] = {'N_un': n, 'sigma_star': s}
        row.append(f'{n:10.1f} / {s:9.5f}')
    print(f'{str(l):>9s} ' + ''.join(f'{r:>22s}' for r in row))
# planted limits
ok0 = all(N_un(d, 0) == 12000 for d in Ds); okinf = all(N_un(d, math.inf) == 0 for d in Ds)
print('plant l=0 gives 12000 for every pair:', ok0, '| sigma* =', 1/(2*math.sqrt(12000)))
print('plant l=inf gives 0 for every pair:', okinf)
out['plants'] = {'l0_all_12000': ok0, 'linf_all_0': okinf}
# the quoted 14 Nov sentence: at l = 1, different-slit pairs
print('l=1, Delta=100: N_un =', N_un(100, 1), ' (sentence needs about 2000)')
# contrast factor at fixed sigma for pair separations, d<l regime: exp(-2 sigma^2 (D1+D2) d/l)
for l in (1000,):
    for sig in (0.005, 0.01, 0.02):
        print(f'l={l} sigma={sig}: pair factor d=100: {math.exp(-4*sig**2*N_un(100,l)):.4f}  d=200: {math.exp(-4*sig**2*N_un(200,l)):.4f}  (independent jitter: {math.exp(-4*sig**2*12000):.2e})')
json.dump(out, open('N-2026-11-15-2-jitter-table-output.json', 'w'), indent=1, default=str)
