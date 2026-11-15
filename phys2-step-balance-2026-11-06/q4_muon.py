"""Q4: muon decay, massless daughters, uniform count x one pairwise orientation weight.

Units: parent mass M = 2, so x = 2E/M = E.  Daughters: 1 = e, 2 = anti-nu_e, 3 = nu_mu.
Uniform count:  d^3p1 d^3p2 d^3p3 delta^4  =  8 pi^2 E1 E2 E3 dE1 dE2   (massless).
Massless: s_i = n_i exactly, and p_i.p_j = 2(1 - E_k), so
  OPPOSED(i,j) = (1 - cos th_ij)/2 = (1 - E_k)/(E_i E_j),   ALIGNED = 1 - OPPOSED.
"""
import itertools
import numpy as np
import sympy as sp

x, y, E1, E2, E3, rho = sp.symbols("x y E1 E2 E3 rho", real=True)
names = {1: "e", 2: "nubar_e", 3: "nu_mu"}
E = {1: E1, 2: E2, 3: E3}
uniform = E1 * E2 * E3


def opp(i, j):
    k = ({1, 2, 3} - {i, j}).pop()
    return (1 - E[k]) / (E[i] * E[j])


def spectrum(density, which):
    """Normalised energy spectrum of daughter `which` (x = its E), integrating the other energy."""
    others = [q for q in (1, 2, 3) if q != which]
    a, b = others  # integrate over E_a; E_b = 2 - x - E_a ; E_a in [1-x, 1]
    d = density.subs({E[which]: x, E[b]: 2 - x - E[a]})
    f = sp.integrate(sp.expand(sp.cancel(d)), (E[a], 1 - x, 1))
    f = sp.expand(sp.simplify(f))
    Z = sp.integrate(f, (x, 0, 1))
    return sp.factor(sp.expand(f / Z)), Z


michel = 4 * x**2 * (3 * (1 - x) + sp.Rational(2, 3) * rho * (4 * x - 3))


def michel_rho(f):
    sol = sp.solve(sp.Poly(sp.expand(f - michel), x).coeffs(), rho, dict=True)
    return sol[0][rho] if sol else None


# --- uniform count alone (anchor check) ---
fu, Zu = spectrum(uniform, 1)
print("uniform count alone: f(x) =", fu, "  mean =", sp.integrate(x * fu, (x, 0, 1)), "  total =", Zu)

rows = []
for (i, j) in [(1, 2), (1, 3), (2, 3)]:
    for rel in ("ALIGNED", "OPPOSED"):
        W = opp(i, j) if rel == "OPPOSED" else 1 - opp(i, j)
        dens = sp.cancel(uniform * W)
        fe, Z = spectrum(dens, 1)
        rho_exact = michel_rho(fe)
        mean = sp.integrate(x * fe, (x, 0, 1))
        rho_mean = sp.Rational(15, 2) * (mean - sp.Rational(3, 5))
        Wavg = Z / Zu
        fnb, _ = spectrum(dens, 2)
        fnm, _ = spectrum(dens, 3)
        rows.append(((names[i], names[j]), rel, sp.simplify(dens), fe, rho_exact, mean, rho_mean, Wavg, fnb, fnm))

print("\nALL SIX CASES (reported before any comparison)")
for (pair, rel, dens, fe, rx, mean, rm, Wavg, fnb, fnm) in rows:
    print(f"\n{rel} {pair}:  weighted density in (E1,E2) ~ {dens}")
    print(f"   electron f(x) = {fe}")
    print(f"   exact Michel? {'yes, rho = ' + str(rx) if rx is not None else 'no'}")
    print(f"   <x> = {mean} = {float(mean):.6f};  rho matching mean = {rm} = {float(rm):.6f}")
    print(f"   <W> over uniform count = {Wavg} = {float(Wavg):.6f}")
    print(f"   nubar_e spectrum = {fnb};   nu_mu spectrum = {fnm}")

# --- comparison with TWIST, only after the table ---
rho_T, sT = 0.74977, (0.00012**2 + 0.00023**2) ** 0.5
print(f"\nTWIST rho = {rho_T} +/- {sT:.5f} (stat+syst in quadrature)")
for (pair, rel, *_r) in rows:
    rx = _r[2]
    if rx is not None:
        print(f"   {rel} {pair}: rho = {float(rx):.5f}  pull = {(float(rx) - rho_T) / sT:+.2f} sigma")

# --- [control] Standard Model |M|^2 ~ (p_mu.p_nubar_e)(p_e.p_nu_mu); LIPS is flat in dE1 dE2 ---
M = 2
sm_density = (M * E2) * (2 * (1 - E2))          # (p_mu.p2)(p1.p3) with p1.p3 = 2(1-E2)
ours = sp.cancel(uniform * opp(1, 3))
print("\n[control] SM Dalitz density / (uniform x OPPOSED(e,nu_mu)) =", sp.simplify(sm_density / ours))
ours2 = sp.cancel(uniform * opp(1, 2))
print("[control] SM Dalitz density / (uniform x OPPOSED(e,nubar_e)) =", sp.simplify(sm_density / ours2))

# --- independent Monte Carlo check with explicit 3-vectors (RAMBO, massless) ---
rng = np.random.default_rng(7)
N = 1_000_000


def rambo3(n):
    c = 2 * rng.random((n, 3)) - 1
    phi = 2 * np.pi * rng.random((n, 3))
    q0 = -np.log(rng.random((n, 3)) * rng.random((n, 3)))
    s = np.sqrt(1 - c**2)
    q = np.stack([q0, q0 * s * np.cos(phi), q0 * s * np.sin(phi), q0 * c], -1)
    Q = q.sum(1)
    Mq = np.sqrt(Q[:, 0]**2 - (Q[:, 1:]**2).sum(-1))
    b = -Q[:, 1:] / Mq[:, None]
    g = Q[:, 0] / Mq
    a = 1 / (1 + g)
    xs = 2.0 / Mq                          # total mass 2
    bq = (b[:, None, :] * q[:, :, 1:]).sum(-1)
    p0 = xs[:, None] * (g[:, None] * q[:, :, 0] + bq)
    pv = xs[:, None, None] * (q[:, :, 1:] + b[:, None, :] * (q[:, :, 0][..., None] + (a[:, None] * bq)[..., None]))
    return p0, pv


p0, pv = rambo3(N)
w_u = p0[:, 0] * p0[:, 1] * p0[:, 2]       # uniform count = LIPS x prod(2E)
nhat = pv / p0[..., None]
print("\nMonte Carlo (RAMBO, explicit angles), N =", N, " max|sum p| =", f"{np.abs(pv.sum(1)).max():.1e}")
for (i, j) in [(0, 1), (0, 2), (1, 2)]:
    cij = (nhat[:, i] * nhat[:, j]).sum(-1)
    for rel, W in (("ALIGNED", (1 + cij) / 2), ("OPPOSED", (1 - cij) / 2)):
        ww = w_u * W
        print(f"   {rel} ({names[i+1]},{names[j+1]}): <x_e> = {np.sum(ww * p0[:, 0]) / ww.sum():.4f}   <W> = {ww.sum() / w_u.sum():.4f}")
