"""The seeding family that keeps the balances fixed (SPEC §1) and the M0 checks."""
import numpy as np
import sympy as sp

from gexit_pr3 import model as pm

K10S = (0.5, 1.0, 2.0)


def kvec(k10):
    """(k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12)."""
    return np.array([2.0, 11 * k10 - 2, 47 * k10, 1.0, 1.0, 1.0, 1.0, 1.0, k10, 13 * k10, 0.5])


def use(k10):
    pm.set_k(kvec(k10))


def m0():
    y, q = sp.symbols("y k10", positive=True)
    k1, k5, k6, k7 = 2, 1, 1, 1
    k2, k3, k11 = 11 * q - 2, 47 * q, 13 * q
    A = k2 + k7 + sp.Rational(k1 * k5, k5 + k6)
    S = q * y + (k3 * y - k11) / (1 + y) ** 2
    ident = sp.simplify(S - A - q * (y - 2) * (y - 3) * (y - 4) / (1 + y) ** 2)
    out = dict(identity_residual=str(ident), per_k10={})
    for k10 in K10S:
        use(k10)
        rows = {}
        for v in (2.0, 3.0, 4.0):
            b = np.array([1.0, v, 1.0, 0.5])
            ev = np.linalg.eigvals(pm.jacobian(b, "TH"))
            rows[str(v)] = dict(residual=float(np.abs(pm.drift(b, "TH")).max()), max_re=float(ev.real.max()),
                                eig=[[float(z.real), float(z.imag)] for z in ev])
        lam = pm.lambda_slow(np.array([1.0, 2.0, 1.0, 0.5]), "TH")
        out["per_k10"][str(k10)] = dict(balances=rows, lambda_slow_v2=float(lam.real), t_burn_v2=10 / abs(lam.real),
                                        lambda_slow_v4=float(pm.lambda_slow(np.array([1.0, 4.0, 1.0, 0.5]), "TH").real),
                                        k=kvec(k10).tolist())
    use(1.0)
    return out
