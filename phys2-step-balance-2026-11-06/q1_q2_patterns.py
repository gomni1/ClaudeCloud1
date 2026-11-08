"""Q1 and Q2: orientation shares of one pattern and of two independent patterns under R1.

The proofs are linearity of expectation. This script checks them on step
distributions of different shapes that share the same mean, and shows that a
weight that is not linear in each step does depend on shape.
"""
import numpy as np
from scipy.optimize import brentq

rng = np.random.default_rng(20261106)
NS = 2_000_000


def unit(v):
    v = np.asarray(v, float)
    return v / np.linalg.norm(v)


def basis(n):
    n = unit(n)
    t = np.array([1.0, 0, 0]) if abs(n[0]) < 0.9 else np.array([0, 1.0, 0])
    e1 = unit(np.cross(n, t))
    e2 = np.cross(n, e1)
    return n, e1, e2


def two_point(vvec, size):
    """1D-embedded: s = +n or -n, P(+n) = (1+|v|)/2."""
    n = unit(vvec); v = np.linalg.norm(vvec)
    fwd = rng.random(size) < (1 + v) / 2
    return np.where(fwd[:, None], n, -n)


def cone(vvec, size):
    """s uniform on a cone of half-angle acos(|v|) about n."""
    n, e1, e2 = basis(vvec); c = np.linalg.norm(vvec); s_ = np.sqrt(1 - c * c)
    phi = rng.random(size) * 2 * np.pi
    return c * n + s_ * (np.cos(phi)[:, None] * e1 + np.sin(phi)[:, None] * e2)


def vmf(vvec, size):
    """von Mises-Fisher on the sphere with mean resultant length |v|."""
    n, e1, e2 = basis(vvec); R = np.linalg.norm(vvec)
    kappa = brentq(lambda k: 1 / np.tanh(k) - 1 / k - R, 1e-6, 1e4)
    u = rng.random(size)
    w = 1 + np.log(u + (1 - u) * np.exp(-2 * kappa)) / kappa   # exact inverse-CDF for cos
    phi = rng.random(size) * 2 * np.pi
    sw = np.sqrt(np.clip(1 - w * w, 0, None))
    return w[:, None] * n + sw[:, None] * (np.cos(phi)[:, None] * e1 + np.sin(phi)[:, None] * e2)


shapes = {"two-point": two_point, "cone": cone, "vMF": vmf}

print("Q1  E[(1 - s.n)/2] versus (1 - |v|)/2   (N = %d samples each)" % NS)
for vvec in ([0.3, 0, 0], [0.2, 0.5, -0.4], [0, 0, 0.9]):
    vvec = np.array(vvec); v = np.linalg.norm(vvec); n = unit(vvec)
    row = []
    for name, f in shapes.items():
        s = f(vvec, NS)
        mean_s = s.mean(0)
        share = ((1 - s @ n) / 2).mean()
        row.append(f"{name}: {share:.5f} (|E[s]-v|={np.linalg.norm(mean_s - vvec):.1e})")
    print(f"  |v|={v:.4f}  predicted {(1 - v) / 2:.5f} | " + " | ".join(row))

print("\nQ1  1D: P(backward) = (1-v)/2 exactly; R2/R3 'uncommitted shares' (scalars, no direction)")
print("   v     P_b=(1-v)/2   R3: 1-v   2*P_b   R2: sqrt(1-v^2)   2*sqrt(P_f*P_b)")
for v in (0.0, 0.3, 0.6, 0.9, 0.99):
    pb, pf = (1 - v) / 2, (1 + v) / 2
    print(f"  {v:4.2f}   {pb:.6f}      {1 - v:.6f}  {2 * pb:.6f}  {np.sqrt(1 - v * v):.6f}         {2 * np.sqrt(pf * pb):.6f}")

print("\nQ2  E[(1 -/+ s_i.s_j)/2] for independent patterns, versus (1 -/+ v_i.v_j)/2")
vi = np.array([0.5, 0.2, 0.0]); vj = np.array([-0.3, 0.6, 0.4])
pred_al = (1 + vi @ vj) / 2; pred_op = (1 - vi @ vj) / 2
print(f"  v_i.v_j = {vi @ vj:.5f}; predicted ALIGNED {pred_al:.5f}, OPPOSED {pred_op:.5f}")
for ni, fi in shapes.items():
    for nj, fj in shapes.items():
        si = fi(vi, NS); sj = fj(vj, NS)
        d = np.einsum("ij,ij->i", si, sj)
        al = ((1 + d) / 2).mean(); op = ((1 - d) / 2).mean()
        sq = (((1 + d) / 2) ** 2).mean()   # a weight that is NOT linear in each step
        print(f"  {ni:>9} x {nj:<9}  ALIGNED {al:.5f}  OPPOSED {op:.5f}   nonlinear [(1+s.s)/2]^2 {sq:.5f}")
se = 0.5 / np.sqrt(NS)
print(f"  Monte Carlo standard error on each linear entry <= {se:.1e}")
