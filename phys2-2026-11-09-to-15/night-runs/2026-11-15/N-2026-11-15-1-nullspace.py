# N-2026-11-15-1: does I3 = 0 on unit triples force l(x) + quadratic form on |x| <= 3 ?
# Mechanism as frozen in NIGHT-QUEUE-2026-11-15.md. numpy, double precision.
import numpy as np, json, sys
from numpy.polynomial import chebyshev as Ch

def basis(r, K):
    # T_k(2r/3 - 1), k = 0..K ; r array -> (len, K+1)
    return Ch.chebvander(2*r/3 - 1, K)

def rows(m, K, A, B, restricted=False):
    # a at angle 0, b at angle A, c at angle B (c = -b if restricted)
    a = np.ones_like(A) + 0j
    b = np.exp(1j*A)
    c = -b if restricted else np.exp(1j*B)
    def term(z):
        r = np.abs(z); ph = np.where(r > 1e-300, z/np.where(r > 1e-300, r, 1), 1.0)
        return basis(r, K) * (ph**m)[:, None]
    zero = np.zeros_like(a)
    M = term(a+b+c) - term(a+b) - term(a+c) - term(b+c) + term(a) + term(b) + term(c) - term(zero)
    return M

def svals(M):
    Mr = np.vstack([M.real, M.imag])
    s = np.linalg.svd(Mr, compute_uv=False)
    return s / s[0]

def classify(s):
    return int((s < 1e-9).sum()), int(((s >= 1e-9) & (s < 1e-4)).sum())

out = {}
rng = np.random.default_rng(20261115)
J = 4000
A = rng.uniform(0, 2*np.pi, J); B = rng.uniform(0, 2*np.pi, J)

# ---- second plant, exact arithmetic
def I3(P, a, b, c):
    return P(a+b+c) - P(a+b) - P(a+c) - P(b+c) + P(a) + P(b) + P(c) - P(0*a)
one = np.array([1.0+0j])
p4 = float(I3(lambda z: np.abs(z)**4, one, one, one)[0]); p2 = float(I3(lambda z: np.abs(z)**2, one, one, one)[0])
out['plant2'] = {'I3_r4_at_111': p4, 'I3_r2_at_111': p2, 'pass': (p4 == 36.0 and p2 == 0.0)}
print('plant 2:', out['plant2'])

# ---- first plant: restricted family c = -b, m = 0, K = 30, f = o(r^2-2), o(u) = u^5 - 5u^3
K = 30
x = np.cos(np.pi*(np.arange(200)+0.5)/200)            # Chebyshev nodes in [-1,1]
r = 1.5*(x+1)
fvals = (r**2-2)**5 - 5*(r**2-2)**3
coef = Ch.chebfit(x, fvals, K)
fit_err = float(np.max(np.abs(Ch.chebval(x, coef) - fvals))/np.max(np.abs(fvals)))
Mres = rows(0, K, A, B, restricted=True)
s_res = svals(Mres)
nn, nu = classify(s_res)
res_restricted = float(np.linalg.norm(Mres @ coef)/np.linalg.norm(coef))
Mfull = rows(0, K, A, B)
res_full = float(np.linalg.norm(Mfull @ coef)/np.linalg.norm(coef))
out['plant1'] = {'basis_fit_rel_err': fit_err, 'restricted_null_dirs': nn, 'restricted_unresolved': nu,
                 'residual_restricted': res_restricted, 'residual_full': res_full,
                 'pass': bool(nn > 2 and res_restricted < 1e-9 and res_full > 1e-3)}
print('plant 1:', out['plant1'])
if not (out['plant1']['pass'] and out['plant2']['pass']):
    print('HARNESS BLIND: plants did not trip. Stop.')
    json.dump(out, open('N-2026-11-15-1-nullspace-output.json', 'w'), indent=1); sys.exit(1)

# ---- main run
out['main'] = {}
for K in (30, 20, 40):
    out['main'][K] = {}
    for m in range(0, 9):
        s = svals(rows(m, K, A, B))
        nn, nu = classify(s)
        out['main'][K][m] = {'null': nn, 'unresolved': nu, 'smallest6': [float(v) for v in s[-6:]]}
        print(f'K={K:2d} m={m}: null={nn} unresolved={nu} smallest: ' + ' '.join(f'{v:.2e}' for v in s[-5:]))

# ---- identify the null directions at K = 30 against the expected ones
exp = {0: [np.ones_like(r), r**2], 1: [r], 2: [r**2]}
out['identify'] = {}
for m, fl in exp.items():
    M = rows(m, 30, A, B)
    for i, fv in enumerate(fl):
        cf = Ch.chebfit(x, fv, 30)
        out['identify'][f'm{m}_{i}'] = float(np.linalg.norm(M @ cf)/np.linalg.norm(cf))
print('expected null functions, residuals:', out['identify'])

# ---- direct evaluation on fresh unit triples (seed 20261116)
rng2 = np.random.default_rng(20261116)
t = rng2.uniform(0, 2*np.pi, (3, 10000)); a, b, c = np.exp(1j*t[0]), np.exp(1j*t[1]), np.exp(1j*t[2])
def rel(P):
    v = I3(P, a, b, c); zs = np.concatenate([a+b+c, a+b, a])
    return float(np.max(np.abs(v))/np.max(np.abs(P(zs))))
readouts = {
 '|R|^1': lambda z: np.abs(z), '|R|^1.5': lambda z: np.abs(z)**1.5, '|R|^2': lambda z: np.abs(z)**2,
 '|R|^2.5': lambda z: np.abs(z)**2.5, '|R|^3': lambda z: np.abs(z)**3, '|R|^4': lambda z: np.abs(z)**4,
 'x^2+3y^2+xy': lambda z: z.real**2 + 3*z.imag**2 + z.real*z.imag,
 '|R|^2 + x (linear term)': lambda z: np.abs(z)**2 + z.real,
 '1-exp(-|R|^2)': lambda z: 1-np.exp(-np.abs(z)**2),
 'plant f=(r^2-2)^5-5(r^2-2)^3': lambda z: (np.abs(z)**2-2)**5 - 5*(np.abs(z)**2-2)**3,
 'Re z^3 (harmonic cubic)': lambda z: (z**3).real,
}
out['direct'] = {k: rel(P) for k, P in readouts.items()}
for k, v in out['direct'].items(): print(f'direct max|I3|/max|P|  {k:32s} {v:.3e}')
json.dump(out, open('N-2026-11-15-1-nullspace-output.json', 'w'), indent=1)
