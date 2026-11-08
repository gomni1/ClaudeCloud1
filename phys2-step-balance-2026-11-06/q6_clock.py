"""Q6: R1-clock, a 1D telegraph process: forward->backward at rate a, backward->forward at rate b."""
import numpy as np
import sympy as sp

a, b, m, eta, th = sp.symbols("a b m eta theta", positive=True)

# (a) stationary two-state chain: mean dwell 1/a forward, 1/b backward
pf = (1 / a) / (1 / a + 1 / b)
v = sp.simplify(pf * 1 + (1 - pf) * (-1))
print("(a) forward fraction =", sp.simplify(pf), "   net speed v =", v)

# (b) ab = m^2: a = m e^-eta, b = m e^eta
sub = {a: m * sp.exp(-eta), b: m * sp.exp(eta)}
v_eta = sp.simplify(v.subs(sub).rewrite(sp.tanh))
rev = pf * a + (1 - pf) * b                      # stationary reversals per unit time
rev_eta = sp.simplify(rev.subs(sub))
print("(b) v =", v_eta, "   reversal rate =", sp.simplify(rev), "=", rev_eta,
      "   minus m*sqrt(1-v^2):", sp.simplify((rev_eta - m * sp.sqrt(1 - sp.tanh(eta)**2)).rewrite(sp.exp)))

# (c) E = (a+b)/2, p = (b-a)/2
Ec, pc = (a + b) / 2, (b - a) / 2
print("(c) E^2 - p^2 =", sp.expand(Ec**2 - pc**2), "   p/E - v =", sp.simplify(pc / Ec - v))
# boost by rapidity theta: forward (right-moving null) dwell times scale by e^theta, backward by e^-theta
a2, b2 = a * sp.exp(-th), b * sp.exp(th)
E2, p2 = (a2 + b2) / 2, (b2 - a2) / 2
print("    under a boost: a'b' - ab =", sp.simplify(a2 * b2 - a * b),
      "  E' - (E cosh + p sinh) =", sp.simplify((E2 - (Ec * sp.cosh(th) + pc * sp.sinh(th))).rewrite(sp.exp)),
      "  p' - (p cosh + E sinh) =", sp.simplify((p2 - (pc * sp.cosh(th) + Ec * sp.sinh(th))).rewrite(sp.exp)))
print("    arithmetic mean E, geometric mean m, harmonic mean (reversal rate): E * rev =",
      sp.simplify(Ec * rev), " (= m^2)")

# (d) limits
print("(d) a -> 0 (m = 0): forward fraction ->", sp.limit(pf, a, 0), ", v ->", sp.limit(v, a, 0),
      ", reversal rate ->", sp.limit(rev, a, 0))

# ---------- simulation ----------
rng = np.random.default_rng(42)


def simulate(a_, b_, T=2.0e5):
    t, state, xpos, tf, nrev = 0.0, +1, 0.0, 0.0, 0
    durs = {+1: [], -1: []}
    while t < T:
        rate = a_ if state > 0 else b_
        d = rng.exponential(1 / rate)
        durs[state].append(d)
        t += d; xpos += state * d
        if state > 0:
            tf += d
        state = -state; nrev += 1
    return tf / t, xpos / t, nrev / t, durs


mass = 1.0
print("\nSimulation (m = 1, T = 2e5 per run)")
print("  eta    v_pred    v_sim     fwd_pred  fwd_sim   back_pred(1-v)/2  back_sim   rev_pred m*sqrt(1-v^2)  rev_sim")
for e in (0.0, 0.5, 1.0, 2.0):
    A_, B_ = mass * np.exp(-e), mass * np.exp(e)
    fwd, vs, rv, _ = simulate(A_, B_)
    vp = np.tanh(e)
    print(f"  {e:3.1f}   {vp:.5f}  {vs:.5f}   {(1 + vp) / 2:.5f}   {fwd:.5f}   {(1 - vp) / 2:.5f}           {1 - fwd:.5f}    "
          f"{mass * np.sqrt(1 - vp**2):.5f}                 {rv:.5f}")

# boost the rest-frame path explicitly with a Lorentz transformation of its vertices
from scipy import stats
_, _, _, d0 = simulate(1.0, 1.0)
seq = []
for f_, b_ in zip(d0[+1], d0[-1]):
    seq += [(+1, f_), (-1, b_)]
tt = np.concatenate([[0.0], np.cumsum([d for _, d in seq])])
xx = np.concatenate([[0.0], np.cumsum([s * d for s, d in seq])])
for e in (0.5, 1.0):
    g, beta = np.cosh(e), np.tanh(e)
    tp = g * (tt + beta * xx)               # active boost to velocity +tanh(eta)
    xp = g * (xx + beta * tt)
    dtp = np.diff(tp)
    fdur, bdur = dtp[0::2], dtp[1::2]
    ap, bp = 1 / fdur.mean(), 1 / bdur.mean()
    ks_f = stats.kstest(fdur, "expon", args=(0, fdur.mean())).pvalue
    print(f"  boosted eta={e}: a' = {ap:.4f} (pred {np.exp(-e):.4f}), b' = {bp:.4f} (pred {np.exp(e):.4f}), a'b' = {ap * bp:.4f}, "
          f"v' = {(xp[-1] - xp[0]) / (tp[-1] - tp[0]):.4f} (pred {beta:.4f}), KS p(forward dwell exponential) = {ks_f:.2f}")

# discrete ticks (one site per tick): two-state chain with flip probabilities per tick
pa, pb = 0.02, 0.05
print(f"\nDiscrete-tick chain, flip probs pa={pa}, pb={pb}: forward fraction pb/(pa+pb) = {pb / (pa + pb):.5f}, "
      f"v = {(pb - pa) / (pa + pb):.5f}, reversals/tick = 2 pa pb/(pa+pb) = {2 * pa * pb / (pa + pb):.5f}, "
      f"sqrt(pa pb) sqrt(1-v^2) = {np.sqrt(pa * pb) * np.sqrt(1 - ((pb - pa) / (pa + pb))**2):.5f}")
