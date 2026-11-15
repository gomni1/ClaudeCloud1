# N-2026-11-11-1: the resting-ticking pair, and the cycle's multipliers.
# Mechanism as frozen in NIGHT-QUEUE-2026-11-11.md. Python 3, numpy, scipy.
import json, sys, time
import numpy as np
from scipy.integrate import solve_ivp
from scipy.optimize import brentq
from scipy.special import betainc, beta as Bfun

OUT = {}
k1,k2,k3,k5,k6,k7,k8,k9,k10,k12 = (17.452344563736048, 0.41372216747103946, 44.67737830552512,
    8.05086975924266, 0.06903256564057879, 0.03229295995554182, 0.083706798767576,
    0.010174673348427083, 0.609928184398708, 0.15342684932155354)
m, kr = 27, 7
a_, b_ = kr, m-kr+1
F  = lambda x: betainc(a_, b_, x)
Fp = lambda x: x**(a_-1)*(1-x)**(b_-1)/Bfun(a_, b_)

def f(t, y):
    C,V,L,P = y
    T = C+V+L+P; x = C/T; rho = k3*F(x)
    return [-(k1+k2+k7)*C + k6*L + (k10+rho)*V,
            k2*C + k5*L + k8*P - (k10+rho)*V + k12,
            k1*C - (k5+k6)*L,
            k7*C - (k8+k9)*P]

def jac(y):
    C,V,L,P = y
    T = C+V+L+P; x = C/T; rho = k3*F(x); rp = k3*Fp(x)
    dx = np.array([(T-C)/T**2, -C/T**2, -C/T**2, -C/T**2])  # dx/d(C,V,L,P)
    drho = rp*dx
    J = np.zeros((4,4))
    J[0] = [-(k1+k2+k7), k10+rho, k6, 0]; J[0] += V*drho
    J[1] = [k2, -(k10+rho), k5, k8];      J[1] -= V*drho
    J[2] = [k1, 0, -(k5+k6), 0]
    J[3] = [k7, 0, 0, -(k8+k9)]
    return J

# balances
Cs = (k8+k9)*k12/(k7*k9); Ls = k1*Cs/(k5+k6); Ps = k12/k9
D = k2 + k7 + k1*k5/(k5+k6)
al, be, ga = Cs, Cs+Ls+Ps, D*Cs
G = lambda x: (k10 + k3*F(x))*(al - be*x) - ga*x
xe = al/be
xs = np.linspace(0, xe, 4001)
gv = np.array([G(x) for x in xs]); gv[0] = k10*al; gv[-1] = -ga*xe
roots = [brentq(G, xs[i], xs[i+1], xtol=1e-15, rtol=1e-15) for i in range(4000) if gv[i]*gv[i+1] < 0]
assert len(roots) == 3, roots
bal = []
for x in roots:
    V = al/x - be
    y = np.array([Cs, V, Ls, Ps]); ev = np.linalg.eigvals(jac(y))
    bal.append(dict(x=x, V=V, y=y, ev=ev, res=float(np.max(np.abs(f(0,y))))))
bal.sort(key=lambda b: b['V'])
lo, mid, hi = bal
OUT['balances'] = [dict(V=b['V'], residual=b['res'], eig=[[float(e.real), float(e.imag)] for e in sorted(b['ev'], key=lambda e:-e.real)]) for b in bal]
# reproduction check against 10 Nov
ok = (abs(lo['V']-41.1404511944)/41.14 < 1e-3)
evs = sorted(lo['ev'], key=lambda e:-e.real)
ok &= abs(evs[0].real-0.8664)/0.8664 < 5e-3 and abs(abs(evs[0].imag)-15.778)/15.778 < 5e-3
ok &= any(abs(e.real+0.000795)/0.000795 < 5e-3 for e in evs) and any(abs(e.real+0.1127)/0.1127 < 5e-3 for e in evs)
OUT['reproduction_ok'] = bool(ok)
print('balances', OUT['balances'], 'repro', ok, flush=True)
if not ok: json.dump(OUT, open('N-2026-11-11-1-cycle-output.json','w'), indent=1, default=str); sys.exit(1)

# ---------- generic harness ----------
def run(fun, y0, t_end, sec, guard, rtol=1e-10, atol=1e-12):
    def ev_sec(t, y): return sec(y)
    ev_sec.direction = 1
    def ev_guard(t, y): return guard(y)
    ev_guard.terminal = True; ev_guard.direction = 1
    s = solve_ivp(fun, (0, t_end), y0, method='LSODA', rtol=rtol, atol=atol,
                  t_eval=[t_end], events=[ev_sec, ev_guard])
    return s

def classify(s, t_end, balances):
    if len(s.t_events[1]):
        return dict(kind='guard fired', t=float(s.t_events[1][0]))
    yT = s.y[:, -1]
    for name, yb in balances:
        nb = np.linalg.norm(yb)
        d = np.linalg.norm(yT-yb)/(nb if nb > 0 else 1.0)
        if d < 1e-6: return dict(kind='rest', at=name, reldist=float(d))
    te, ye = s.t_events[0], s.y_events[0]
    last = te > 0.9*t_end
    info = dict(n_crossings=int(len(te)), n_last10pct=int(last.sum()))
    if last.sum() >= 20:
        Y = ye[-10:]; Tr = np.diff(te[-11:])
        dy = max(np.linalg.norm(Y[i+1]-Y[i])/np.linalg.norm(Y[i]) for i in range(9))
        dT = (Tr.max()-Tr.min())/Tr.mean()
        info.update(max_rel_section_step=float(dy), rel_period_spread=float(dT), period=float(Tr.mean()))
        if dy < 1e-6 and dT < 1e-6:
            info.update(kind='cycle', y_sec=Y[-1].tolist()); return info
    info.update(kind='other', yT=yT.tolist()); return info

def monodromy(fun, jacf, y0, sec, n, Test, rtol=1e-11, atol=1e-13):
    # integrate state + variational matrix for 1.5 x the estimated period; the period is the
    # first upward section crossing after 0.5 x the estimate
    def aug(t, z):
        y = z[:n]; Phi = z[n:].reshape(n, n)
        return np.concatenate([fun(t, y), (jacf(y) @ Phi).ravel()])
    def ev(t, z): return sec(z[:n])
    ev.direction = 1
    z0 = np.concatenate([y0, np.eye(n).ravel()])
    s = solve_ivp(aug, (0, 1.5*Test), z0, method='LSODA', rtol=rtol, atol=atol, events=ev, t_eval=[])
    k = [i for i, t in enumerate(s.t_events[0]) if t > 0.5*Test][0]
    Th = float(s.t_events[0][k]); Phi = s.y_events[0][k][n:].reshape(n, n)
    return Th, Phi

def fixed_time_monodromy(fun, jacf, y0, n, tfix, rtol=1e-11, atol=1e-13):
    def aug(t, z):
        y = z[:n]; Phi = z[n:].reshape(n, n)
        return np.concatenate([fun(t, y), (jacf(y) @ Phi).ravel()])
    z0 = np.concatenate([y0, np.eye(n).ravel()])
    s = solve_ivp(aug, (0, tfix), z0, method='LSODA', rtol=rtol, atol=atol, t_eval=[tfix])
    return s.y[n:, -1].reshape(n, n)

def multipliers_report(Phi):
    mu = np.linalg.eigvals(Phi)
    i = int(np.argmin(np.abs(mu-1)))
    others = [complex(mu[j]) for j in range(len(mu)) if j != i]
    return dict(all=[[float(z.real), float(z.imag)] for z in mu], trivial=[float(mu[i].real), float(mu[i].imag)],
                trivial_dist=float(abs(mu[i]-1)), trivial_ok=bool(abs(mu[i]-1) < 1e-5),
                others_abs=[abs(z) for z in others], stable=bool(all(abs(z) < 1 for z in others)))

# ---------- controls and planted failures ----------
def SL(mu, om):
    def fun(t, y):
        u, v = y; r2 = u*u+v*v
        return [mu*u - om*v - r2*u, om*u + mu*v - r2*v]
    def jacf(y):
        u, v = y; r2 = u*u+v*v
        return np.array([[mu - r2 - 2*u*u, -om - 2*u*v], [om - 2*u*v, mu - r2 - 2*v*v]])
    return fun, jacf
secSL = lambda y: y[1]          # Im z = 0 crossed upward (dv/dt>0 at u>0)
ctrl = {}
fun, jacf = SL(1.0, 2*np.pi)
s = run(fun, [0.5, 0.0], 200.0, secSL, lambda y: abs(y[0])+abs(y[1]) - 1e6)
c = classify(s, 200.0, [('origin', np.array([0.0, 0.0]))])
ctrl['positive_control_class'] = c
if c['kind'] == 'cycle':
    Th, Phi = monodromy(fun, jacf, np.array(c['y_sec']), secSL, 2, c['period'])
    mr = multipliers_report(Phi)
    nontriv = [z for z in np.linalg.eigvals(Phi) if abs(z-1) > 1e-3]
    ctrl['positive_control'] = dict(Theta=Th, mult=mr, ok=bool(abs(Th-1) < 1e-6 and mr['trivial_ok'] and len(nontriv)==1 and abs(nontriv[0]-np.exp(-2)) < 1e-5))
else:
    ctrl['positive_control'] = dict(ok=False)
fun, jacf = SL(-1.0, 2*np.pi)
s = run(fun, [0.5, 0.0], 200.0, secSL, lambda y: abs(y[0])+abs(y[1]) - 1e6)
c = classify(s, 200.0, [('origin', np.array([0.0, 0.0]))])
# |y - 0|/1 used when the balance norm is 0
ctrl['PF_A'] = dict(class_=c, tripped=bool(c['kind'] != 'cycle'))
fun, jacf = SL(1.0, 2*np.pi)
Phi = fixed_time_monodromy(fun, jacf, np.array([1.0, 0.0]), 2, 1.01)
mr = multipliers_report(Phi)
ctrl['PF_B'] = dict(mult=mr, tripped=bool(not mr['trivial_ok']))
g = lambda t, y: y[0]-1e6; g.terminal = True; g.direction = 1
s = solve_ivp(lambda t, y: [1e3], (0, 2e4), [1.0], method='LSODA', t_eval=[2e4], events=[g])
ctrl['PF_G'] = dict(t=float(s.t_events[0][0]) if len(s.t_events[0]) else None, tripped=bool(len(s.t_events[0]) > 0))
ctrl['harness_is_receipt'] = bool(ctrl['positive_control']['ok'] and ctrl['PF_A']['tripped'] and ctrl['PF_B']['tripped'] and ctrl['PF_G']['tripped'])
OUT['controls'] = ctrl
print('controls', json.dumps(ctrl, default=str), flush=True)

# ---------- the six starts ----------
def unit(v): return v/np.linalg.norm(v)
ev, U = np.linalg.eig(jac(lo['y']))
iu = int(np.argmax(ev.real)); u = U[:, iu]; u = u/np.linalg.norm(u)
ru, iu_ = unit(u.real), unit(u.imag)
evm, Um = np.linalg.eig(jac(mid['y']))
im_ = int(np.argmax(evm.real)); w = unit(np.real(Um[:, im_]))
eps = 1e-4
starts = {'S1 +Re u': lo['y']+eps*np.linalg.norm(lo['y'])*ru, 'S2 -Re u': lo['y']-eps*np.linalg.norm(lo['y'])*ru,
          'S3 +Im u': lo['y']+eps*np.linalg.norm(lo['y'])*iu_, 'S4 -Im u': lo['y']-eps*np.linalg.norm(lo['y'])*iu_,
          'S5 +w mid': mid['y']+eps*np.linalg.norm(mid['y'])*w, 'S6 -w mid': mid['y']-eps*np.linalg.norm(mid['y'])*w}
secG = lambda y: y[0]-Cs
guardG = lambda y: (y[0]+y[1]+y[2]+y[3]) - 1e6
T_END = 2e4
res = {}
for name, y0 in starts.items():
    t0 = time.time()
    s = run(f, np.maximum(y0, 0), T_END, secG, guardG)
    c = classify(s, T_END, [('low-Void', lo['y']), ('middle', mid['y']), ('high-Void', hi['y'])])
    c['solver_status'] = int(s.status); c['wall_s'] = round(time.time()-t0, 1)
    if c['kind'] == 'cycle':
        Th, Phi = monodromy(lambda t, y: np.array(f(t, y)), jac, np.array(c['y_sec']), secG, 4, c['period'])
        c['Theta'] = Th; c['mult'] = multipliers_report(Phi)
        # summary of the cycle: min/max of C and V over one period from the section state
        s2 = solve_ivp(f, (0, Th), np.array(c['y_sec']), method='LSODA', rtol=1e-11, atol=1e-13, max_step=Th/400, dense_output=False)
        c['C_range'] = [float(s2.y[0].min()), float(s2.y[0].max())]; c['V_range'] = [float(s2.y[1].min()), float(s2.y[1].max())]
        c['mean_C_over_period'] = float(np.trapezoid(s2.y[0], s2.t)/Th)
    res[name] = c
    print(name, json.dumps({k: v for k, v in c.items() if k not in ('yT',)}, default=str), flush=True)
OUT['starts'] = res
OUT['pins'] = dict(C=Cs, L=Ls, P=Ps, D=D)
json.dump(OUT, open('N-2026-11-11-1-cycle-output.json', 'w'), indent=1, default=str)
