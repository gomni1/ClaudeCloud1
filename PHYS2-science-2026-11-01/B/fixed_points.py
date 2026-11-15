"""Part B: locate and classify the deterministic balances (SPEC §2)."""
import numpy as np
from scipy.optimize import fsolve

K = (2, 9, 47, 1, 1, 1, 1, 1, 1, 13, 0.5)
k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = K


def f(y):
    C, V, L, P = y
    x = C / (C + V) if (C + V) > 0 else 0.0
    x2 = x * x
    r3 = k3 * V * x2
    r11 = k11 * C * x2
    return np.array([-(k1 + k2 + k7) * C + r3 + k6 * L + k10 * V - r11,
                     k2 * C - r3 + k5 * L + k8 * P - k10 * V + r11 + k12,
                     k1 * C - (k5 + k6) * L,
                     k7 * C - (k8 + k9) * P])


def jac(y, h=1e-7):
    J = np.zeros((4, 4))
    f0 = f(y)
    for i in range(4):
        yp = np.array(y, float); yp[i] += h
        J[:, i] = (f(yp) - f0) / h
    return J


def main():
    rows = []
    for guess, lab in [((1, 2, 1, .5), "V=2"), ((1, 3, 1, .5), "V=3"), ((1, 4, 1, .5), "V=4")]:
        y = fsolve(f, np.array(guess, float))
        ev = np.linalg.eigvals(jac(y))
        rows.append((lab, y, float(np.abs(f(y)).max()), float(ev.real.max())))
        print("%s: fp=%s  |residual|=%.2e  max Re(eig)=%+.4f  %s" %
              (lab, np.array2string(y, precision=6), rows[-1][2], rows[-1][3],
               "stable" if rows[-1][3] < 0 else "UNSTABLE"))
    return rows


if __name__ == "__main__":
    main()
