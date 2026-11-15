# N-2026-11-12-1 harness (frozen in NIGHT-QUEUE-2026-11-12.md; details in N-2026-11-12-1-prerun-notes.txt).
# Modes: verify | plants | pilot | draw <n> [starts]
import json, sys, time, math
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import betainc, betaln

RTOL, ATOL = 1e-10, 1e-13
DRAWS = [2045, 301417, 384616, 456280, 616482]

class Sys:
    pass

# ---------------- the closed level ----------------
Bm = np.array([[1, 0, 0], [-1, -1, -1], [0, 1, 0], [0, 0, 1]], float)

def make_model(k, m, kr, T=1.0):
    k1, k2, k3, k5, k6, k7, k8, k10 = k
    a, b = kr, m - kr + 1
    lb = betaln(a, b)
    def F(x): return betainc(a, b, np.clip(x, 0.0, 1.0))
    def Fp(x):
        x = np.clip(x, 1e-300, 1 - 1e-16)
        return np.exp((a - 1) * np.log(x) + (b - 1) * np.log1p(-x) - lb)
    S = Sys(); S.n = 4; S.B = Bm; S.sec = 0; S.T = T; S.name = 'model'
    def fvec(Y):
        C, V, L, P = Y; x = C / (C + V + L + P); r = k10 + k3 * F(x)
        return np.array([-(k1 + k2 + k7) * C + k6 * L + r * V, k2 * C + k5 * L + k8 * P - r * V,
                         k1 * C - (k5 + k6) * L, k7 * C - k8 * P])
    def gross(Y):
        C, V, L, P = np.abs(Y); x = Y[0] / Y.sum(0); r = k10 + k3 * F(x)
        return np.array([(k1 + k2 + k7) * C + k6 * L + r * V, k2 * C + k5 * L + k8 * P + r * V,
                         k1 * C + (k5 + k6) * L, k7 * C + k8 * P])
    def jac(y):
        C, V, L, P = y; Tt = C + V + L + P; x = C / Tt
        rho = k3 * F(x); rp = k3 * Fp(x)
        dx = np.array([(1 - x) / Tt, -x / Tt, -x / Tt, -x / Tt])
        J = np.array([[-(k1 + k2 + k7), k10 + rho, k6, 0], [k2, -(k10 + rho), k5, k8],
                      [k1, 0, -(k5 + k6), 0], [k7, 0, 0, -k8]], float)
        J[0] += V * rp * dx; J[1] -= V * rp * dx
        return J
    S.fvec = fvec; S.gross = gross; S.jac = jac
    S.f = lambda t, y: fvec(y)
    S.guard = (-1e-9 * T, T * (1 + 1e-9))
    D = k2 + k7 + k1 * k5 / (k5 + k6); c = 1 + k1 / (k5 + k6) + k7 / k8
    S.c = c; S.D = D
    H = lambda x: (k10 + k3 * F(x)) * (1 - c * x) - D * x
    xs = np.linspace(0, 1 / c, 4001); hv = H(xs); hv[0] = k10; hv[-1] = -D / c
    idx = np.nonzero(hv[:-1] * hv[1:] < 0)[0]
    roots = [brentq(H, xs[i], xs[i + 1], xtol=1e-15, rtol=1e-15) for i in idx]
    S.roots = roots
    S.eqs = [T * np.array([x, 1 - c * x, k1 * x / (k5 + k6), k7 * x / k8]) for x in roots]
    return S

def red(S, J):
    return np.linalg.pinv(S.B) @ J @ S.B

def draw_fn(rng):  # verbatim from N-2026-11-11-2-num.py
    k = 10 ** rng.uniform(-2, 2, 8)
    m = int(rng.integers(2, 31)); kr = int(rng.integers(2, m + 1))
    return k, m, kr

def regen():
    rng = np.random.default_rng(20261111); out = {}
    for it in range(max(DRAWS) + 1):
        k, m, kr = draw_fn(rng)
        if it in DRAWS: out[it] = (k.tolist(), m, kr)
    return out

# ---------------- planted systems (shifted centre w0) ----------------
W0 = np.array([3.0, 2.0])

def make_sl(mu, om):
    S = Sys(); S.n = 2; S.B = np.eye(2); S.sec = 0; S.guard = None; S.name = 'SL mu=%g' % mu
    def fvec(Y):
        u = Y[0] - W0[0]; v = Y[1] - W0[1]; r2 = u * u + v * v
        return np.array([mu * u - om * v - r2 * u, om * u + mu * v - r2 * v])
    def gross(Y):
        u = Y[0] - W0[0]; v = Y[1] - W0[1]; r2 = u * u + v * v
        return np.array([abs(mu) * np.abs(Y[0]) + abs(mu * W0[0]) + abs(om) * np.abs(Y[1]) + abs(om * W0[1]) + np.abs(r2 * u),
                         abs(om) * np.abs(Y[0]) + abs(om * W0[0]) + abs(mu) * np.abs(Y[1]) + abs(mu * W0[1]) + np.abs(r2 * v)])
    def jac(y):
        u = y[0] - W0[0]; v = y[1] - W0[1]; r2 = u * u + v * v
        return np.array([[mu - r2 - 2 * u * u, -om - 2 * u * v], [om - 2 * u * v, mu - r2 - 2 * v * v]])
    S.fvec = fvec; S.gross = gross; S.jac = jac; S.f = lambda t, y: fvec(y); S.eqs = [W0.copy()]
    return S

def make_torus():
    A = make_sl(1.0, 2 * math.pi); Bq = make_sl(1.0, 2 * math.pi * math.sqrt(2))
    S = Sys(); S.n = 4; S.B = np.eye(4); S.sec = 0; S.guard = None; S.name = 'torus'
    S.fvec = lambda Y: np.concatenate([A.fvec(Y[:2]), Bq.fvec(Y[2:])])
    S.gross = lambda Y: np.concatenate([A.gross(Y[:2]), Bq.gross(Y[2:])])
    def jac(y):
        J = np.zeros((4, 4)); J[:2, :2] = A.jac(y[:2]); J[2:, 2:] = Bq.jac(y[2:]); return J
    S.jac = jac; S.f = lambda t, y: S.fvec(y); S.eqs = [np.concatenate([W0, W0])]
    return S

# ---------------- classifier ----------------
def tau_of(S):
    re = np.concatenate([np.linalg.eigvals(red(S, S.jac(e))).real for e in S.eqs])
    return 1.0 / np.min(np.abs(re))

def block(S, t0, y0, length, events=None):
    sol = solve_ivp(S.f, (t0, t0 + length), y0, method='LSODA', jac=lambda t, y: S.jac(y), rtol=RTOL, atol=ATOL, events=events)
    Y = sol.y; fv = np.abs(S.fvec(Y)); g = S.gross(Y)
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.where(g > 0, fv / g, 0.0)
    summ = dict(mn=Y.min(1), mx=Y.max(1), rmax=float(r.max()), fmax=float(fv.max()), nsteps=int(Y.shape[1]), ok=bool(sol.success))
    return sol, summ

def newton(S, y):
    Bp = np.linalg.pinv(S.B); y = y.copy()
    for _ in range(60):
        f = S.fvec(y)
        if np.max(np.abs(f)) < 1e-13: break
        y = y + S.B @ np.linalg.solve(Bp @ S.jac(y) @ S.B, -Bp @ f)
        if not np.all(np.isfinite(y)): return None, None
    if np.max(np.abs(S.fvec(y))) >= 1e-13: return None, None
    return y, np.linalg.eigvals(red(S, S.jac(y)))

def cycle_test(te, ye):
    n = len(te)
    for p in (1, 2, 3, 4):
        need = 12 + p
        if n < need: continue
        t = np.array(te[-need:]); Y = np.array(ye[-need:])
        ds = np.max(np.abs(Y[p:] - Y[:-p])); rt = t[p:] - t[:-p]
        dt = (rt.max() - rt.min()) / rt.mean()
        if ds < 1e-7 and dt < 1e-7:
            return dict(p=p, period=float(rt.mean()), state_spread=float(ds), rt_spread=float(dt))
    return None

def classify(S, y0, log=None, near=None):
    tau = tau_of(S); Bl = 10 * tau; t = 0.0; y = np.array(y0, float)
    out = dict(tau=tau, rounds=[]); prev_r = None
    for rnd in range(1, 5):
        sums = []
        for b in range(6):
            sol, s = block(S, t, y, Bl); t = sol.t[-1]; y = sol.y[:, -1].copy(); sums.append(s)
            if S.guard is not None and (s['mn'].min() < S.guard[0] or s['mx'].max() > S.guard[1]):
                out['verdict'] = 'guard fired'; out['t'] = t; return out
            if not s['ok']:
                out['verdict'] = 'unresolved'; out['why'] = 'solver failed'; return out
        last, prv = sums[-1], sums[-2]
        R = dict(round=rnd, t_endA=t, rmax_last=last['rmax'], rmax_prev=prv['rmax'], fmax_last=last['fmax'], fmax_prev=prv['fmax'], steps=sum(s['nsteps'] for s in sums))
        i_ok = last['rmax'] < 1e-8
        ii_lit = last['fmax'] <= prv['fmax']
        ii_var = ii_lit or (last['rmax'] < 1e-11 and prv['rmax'] < 1e-11)
        R.update(i=i_ok, ii_literal=bool(ii_lit), ii_variant=bool(ii_var))
        if i_ok:
            ys, lam = newton(S, y)
            if ys is not None:
                rel = float(np.linalg.norm(ys - y) / np.linalg.norm(y))
                stable = bool(np.all(lam.real < 0))
                d = [float(np.linalg.norm(ys - e) / np.linalg.norm(e)) for e in S.eqs]
                j = int(np.argmin(d))
                R.update(newton_rel=rel, newton_stable=stable, newton_lam=[[float(z.real), float(z.imag)] for z in lam],
                         point=ys.tolist(), nearest_eq=j, nearest_eq_dist=d[j])
                if rel < 1e-6 and stable and (ii_lit or ii_var):
                    out['rounds'].append(R)
                    out['verdict'] = 'at rest'
                    out['rest_literal_rule'] = bool(ii_lit)
                    out['where'] = ('balance %d' % j) if d[j] < 1e-8 else 'edge state'
                    out['point'] = ys.tolist(); out['t'] = t
                    return out
                if rel < 1e-6 and not stable: R['note'] = 'passing a saddle'
        # Stage B
        c = 0.5 * (last['mn'][S.sec] + last['mx'][S.sec])
        ev = lambda tt, yy: yy[S.sec] - c
        ev.direction = 1
        te, ye = [], []
        for b in range(10):
            sol, s = block(S, t, y, Bl, events=ev); t = sol.t[-1]; y = sol.y[:, -1].copy()
            te += list(sol.t_events[0]); ye += [v.copy() for v in sol.y_events[0]]
            if len(te) >= 40: break
        te, ye = te[:40], ye[:40]
        R.update(section=float(c), crossings=len(te), t_endB=t, rmax_B=s['rmax'])
        cy = cycle_test(te, ye)
        if len(te) >= 3:
            rts = np.diff(te); R['return_times_last'] = [float(v) for v in rts[-6:]]
            R['rt_min'] = float(rts.min()); R['rt_max'] = float(rts.max())
        out['rounds'].append(R)
        if log: log('   round %d: rmaxA %.3e crossings %d cycle %s' % (rnd, last['rmax'], len(te), cy))
        if cy:
            out['verdict'] = 'steady cycle'; out.update(cy)
            out['section'] = float(c); out['section_state'] = ye[-1].tolist(); out['t'] = t
            return out
        prev_r = R
    # after 4 rounds
    Rl, Rp = out['rounds'][-1], out['rounds'][-2]
    if near is not None and np.max(np.abs(y - near)) < 1e-3:
        out['verdict'] = 'did not leave'
    elif Rl['crossings'] >= 14 and Rl['rmax_last'] > 1e-6 and 0.5 <= Rl['rmax_last'] / Rp['rmax_last'] <= 2:
        out['verdict'] = 'other sustained motion'
        te_ = np.array(te); Ye = np.array(ye)
        out['return_time_range'] = [float(np.diff(te_).min()), float(np.diff(te_).max())]
        out['section_state_spread'] = [float(v) for v in (Ye.max(0) - Ye.min(0))]
    else:
        out['verdict'] = 'unresolved'
    out['t'] = t; out['end_state'] = y.tolist()
    return out

# ---------------- cycle measurements and Floquet logs ----------------
def measure(S, ysec, period, section):
    tt = np.linspace(0, period, 20001)
    sol = solve_ivp(S.f, (0, period), ysec, method='LSODA', jac=lambda t, y: S.jac(y), rtol=RTOL, atol=ATOL, t_eval=tt)
    Y = sol.y
    lam = max(np.max(np.sum(np.abs(S.jac(Y[:, i])), axis=1)) for i in range(0, Y.shape[1], 10))
    return dict(mn=Y.min(1).tolist(), mx=Y.max(1).tolist(), frac_above=float(np.mean(Y[S.sec] > section)),
                closure=float(np.max(np.abs(Y[:, -1] - Y[:, 0]))), Lambda=float(lam))

def floquet(S, ysec, period, Lam, nper=3, trace_shift=0.0):
    # v2 (12 Nov, after the pilot): the variational equation is integrated in class coordinates,
    # a' = M(t) a with M = pinv(B) J B, so rounding cannot leak into the neutral total direction.
    n = S.n; Bp = np.linalg.pinv(S.B); d = S.B.shape[1]; Q = np.eye(d)
    nseg = int(math.ceil(period * Lam / 5.0)); h = period / nseg
    def rhs(t, z):
        y = z[:n]; q = z[n:n + d * d].reshape(d, d); M = Bp @ S.jac(y) @ S.B
        return np.concatenate([S.fvec(y), (M @ q).ravel(), [np.trace(M) + trace_shift]])
    y = np.array(ysec, float); logs = []; trs = []
    for per in range(nper):
        acc = np.zeros(d); tr = 0.0
        for s in range(nseg):
            z0 = np.concatenate([y, Q.ravel(), [0.0]])
            sol = solve_ivp(rhs, (0, h), z0, method='LSODA', rtol=1e-10, atol=1e-13)
            z = sol.y[:, -1]; y = z[:n]; Q, R = np.linalg.qr(z[n:n + d * d].reshape(d, d))
            acc += np.log(np.abs(np.diag(R))); tr += z[-1]
        logs.append(acc.tolist()); trs.append(float(tr))
    l3 = np.array(logs[-1]); l2 = np.array(logs[-2])
    order = np.argsort(-l3)
    conv = float(np.max(np.where(np.abs(l3) > 1, np.abs(l3 - l2) / np.abs(l3), np.abs(l3 - l2))))
    trerr = float(abs(l3.sum() - trs[-1]) / abs(trs[-1]))
    return dict(nseg=nseg, logs=[float(v) for v in l3[order]], logs_prev=[float(v) for v in l2[order]],
                trivial_ok=bool(abs(l3[order][0]) < 1e-5), conv=conv, conv_ok=bool(conv < 1e-5),
                trace_integral=trs[-1], trace_relerr=trerr, trace_ok=bool(trerr < 1e-6),
                stable=bool(np.all(l3[order][1:] < 0)))

def starts_for(S):
    p = np.array([1, -0.3, -0.4, -0.3]) * 1e-6 * S.T
    st = [('interior-a', S.T * np.array([0.25, 0.25, 0.25, 0.25]), None), ('interior-b', S.T * np.array([0.02, 0.18, 0.70, 0.10]), None)]
    for j, nm in enumerate(('low', 'mid', 'high')):
        st.append((nm + '+', S.eqs[j] + p, S.eqs[j])); st.append((nm + '-', S.eqs[j] - p, S.eqs[j]))
    return st

def jsonable(o):
    if isinstance(o, dict): return {k: jsonable(v) for k, v in o.items()}
    if isinstance(o, (list, tuple)): return [jsonable(v) for v in o]
    if isinstance(o, np.ndarray): return o.tolist()
    if isinstance(o, (np.floating,)): return float(o)
    if isinstance(o, (np.integer,)): return int(o)
    if isinstance(o, (np.bool_,)): return bool(o)
    return o

def run_draw(n, k, m, kr, which=None, log=print):
    S = make_model(k, m, kr)
    res = dict(draw=n, m=m, kr=kr, k=list(k), c=S.c, D=S.D, roots=S.roots, tau=tau_of(S), starts={})
    res['balance_eigs'] = [[[float(z.real), float(z.imag)] for z in np.linalg.eigvals(red(S, S.jac(e)))] for e in S.eqs]
    for nm, y0, near in starts_for(S):
        if which and nm not in which: continue
        t0 = time.time(); log('  draw %d start %s' % (n, nm))
        r = classify(S, y0, log=log, near=near); r['seconds'] = round(time.time() - t0, 1)
        if r['verdict'] == 'steady cycle':
            r['measure'] = measure(S, np.array(r['section_state']), r['period'], r['section'])
        res['starts'][nm] = r
        log('  -> %s %s (%.0fs)' % (r['verdict'], r.get('period', ''), r['seconds']))
    cyc = [r for r in res['starts'].values() if r['verdict'] == 'steady cycle']
    if cyc:
        r = cyc[0]; t0 = time.time()
        res['floquet'] = floquet(S, np.array(r['section_state']), r['period'], r['measure']['Lambda'])
        res['floquet']['seconds'] = round(time.time() - t0, 1)
        log('  floquet %s' % res['floquet'])
    return jsonable(res)

if __name__ == '__main__':
    mode = sys.argv[1]
    if mode == 'verify':
        R = regen(); out = {}
        ref = [0.47205648482747253, 0.026204658014680544, 33.767749788910784, 0.04225910243329335, 0.030726928960954643, 36.36991748036593, 59.878770174623746, 0.8229214570079602]
        for n in DRAWS:
            k, m, kr = R[n]; S = make_model(k, m, kr)
            eig = [np.linalg.eigvals(red(S, S.jac(e))) for e in S.eqs]
            out[n] = dict(k=k, m=m, kr=kr, n_balances=len(S.roots), roots=S.roots, max_re=[float(e.real.max()) for e in eig],
                          all_unstable=bool(len(eig) == 3 and all(e.real.max() > 0 for e in eig)), tau=tau_of(S),
                          eigs=[[[float(z.real), float(z.imag)] for z in e] for e in eig])
            print(n, m, kr, len(S.roots), out[n]['max_re'], 'tau', out[n]['tau'])
        out['check_2045'] = bool(R[2045][1] == 19 and R[2045][2] == 3 and np.allclose(R[2045][0], ref, rtol=1e-15, atol=0))
        print('2045 matches the 11 Nov handoff rates:', out['check_2045'])
        json.dump(jsonable(out), open('N-2026-11-12-1-verify-output.json', 'w'), indent=1)
    elif mode == 'plants':
        out = {}; t0 = time.time()
        S = make_sl(1.0, 2 * math.pi); r = classify(S, W0 + np.array([0.5, 0.0]), log=print)
        if r['verdict'] == 'steady cycle':
            r['measure'] = measure(S, np.array(r['section_state']), r['period'], r['section'])
            r['floquet'] = floquet(S, np.array(r['section_state']), r['period'], r['measure']['Lambda'])
            r['F3_trace_plus_1'] = floquet(S, np.array(r['section_state']), r['period'], r['measure']['Lambda'], trace_shift=1.0)
        out['cycle_mu1'] = r; print('cycle mu=1:', r['verdict'], r.get('period'), r.get('floquet'), round(time.time() - t0, 1), flush=True)
        S = make_sl(400.0, 2 * math.pi); ys = W0 + np.array([20.0, 0.0])
        ms = measure(S, ys, 1.0, W0[0]); fl = floquet(S, ys, 1.0, ms['Lambda'])
        out['stiff_mu400'] = dict(measure=ms, floquet=fl); print('stiff:', fl, round(time.time() - t0, 1), flush=True)
        S = make_sl(-0.05, 2 * math.pi); r = classify(S, W0 + np.array([0.5, 0.0]), log=print)
        out['damped'] = r; print('damped:', r['verdict'], r.get('where'), 'literal(ii):', r.get('rest_literal_rule'), round(time.time() - t0, 1), flush=True)
        R = regen(); k, m, kr = R[2045]; k = list(k); k[2] = 0.0
        S = make_model(k, m, kr); r = classify(S, np.array([0.25, 0.25, 0.25, 0.25]), log=print)
        out['markov_rest'] = r; out['markov_n_balances'] = len(S.roots)
        print('markov rest:', r['verdict'], r.get('where'), 'literal(ii):', r.get('rest_literal_rule'), round(time.time() - t0, 1), flush=True)
        S = make_torus(); r = classify(S, np.concatenate([W0 + [0.5, 0.0], W0 + [0.0, 0.5]]), log=print)
        out['torus'] = r; print('torus:', r['verdict'], r.get('return_time_range'), r.get('section_state_spread'), round(time.time() - t0, 1), flush=True)
        out['seconds'] = round(time.time() - t0, 1)
        json.dump(jsonable(out), open('N-2026-11-12-1-plants-output.json', 'w'), indent=1)
    elif mode == 'pilot':
        R = regen(); k, m, kr = R[2045]; t0 = time.time()
        res = run_draw(2045, k, m, kr, which=['interior-a'])
        res['pilot_seconds'] = round(time.time() - t0, 1)
        json.dump(res, open('N-2026-11-12-1-pilot-output.json', 'w'), indent=1); print('pilot seconds', res['pilot_seconds'])
    elif mode == 'draw':
        n = int(sys.argv[2]); which = sys.argv[3].split(',') if len(sys.argv) > 3 else None
        R = regen(); k, m, kr = R[n]
        lg = lambda s: print(s, flush=True)
        res = run_draw(n, k, m, kr, which=which, log=lg)
        json.dump(res, open('N-2026-11-12-1-draw-%d-output.json' % n, 'w'), indent=1)
