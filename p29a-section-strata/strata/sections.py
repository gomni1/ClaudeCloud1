"""Sections, the rotation action, strata, and the n-gon analogue (SPEC 1.1-1.4).

A section is a complex vector z with z[m - 2] = z_m for m = 2..M, so that
r(phi) = 1 + sum_m Re(z_m exp(-i m phi)).
"""
from math import gcd
from functools import reduce

import numpy as np

TAU = 1e-9      # stratum tolerance (SPEC 1.4)
NEAR = 1e-6     # "near a stratum" flag margin


def modes(z):
    return np.arange(2, len(z) + 2)


def section(**coeffs):
    """section(M=5, z2=..., z3=...) -> complex vector of length M - 1."""
    M = coeffs.pop("M")
    z = np.zeros(M - 1, dtype=complex)
    for key, value in coeffs.items():
        z[int(key[1:]) - 2] = value
    return z


def radius(z, phi):
    phi = np.asarray(phi, dtype=float)
    r = np.ones_like(phi)
    for m, zm in zip(modes(z), z):
        r = r + np.real(zm * np.exp(-1j * m * phi))
    return r


def rotate(z, beta):
    """R_beta: z_m -> exp(i m beta) z_m, i.e. r(phi) -> r(phi - beta)."""
    return z * np.exp(1j * modes(z) * beta)


def admissible(z):
    return float(np.sum(np.abs(z))) < 1.0


def symmetry_order(z, tol=TAU):
    """g(z) = gcd of the active modes; 0 for the circle."""
    active = [int(m) for m, zm in zip(modes(z), z) if abs(zm) > tol]
    return reduce(gcd, active) if active else 0


def stratum_distance(z, k):
    """d_k(z): distance from z to the closed stratum C_k."""
    off = [abs(zm) ** 2 for m, zm in zip(modes(z), z) if m % k]
    return float(np.sqrt(sum(off)))


def classify(z, tol=TAU, near=NEAR):
    """Stratum of z at tolerance tol, plus the closed strata it is near but not in."""
    g = symmetry_order(z, tol)
    near_strata = []
    for k in range(2, len(z) + 2):
        d = stratum_distance(z, k)
        if tol < d < near:
            near_strata.append(k)
    return {"g": g, "stratum": "circle" if g == 0 else f"C{g}",
            "near": near_strata}


def codimension(M, k):
    """Real codimension of C_k in V_M (SPEC H0a)."""
    return 2 * sum(1 for m in range(2, M + 1) if m % k)


# --- area moments I_a = iint zeta^a dA ---------------------------------------

def area_moment(z, a, n=None):
    """Smooth section: I_a = int r^(a+2)/(a+2) e^(i a phi) dphi.

    r^(a+2) is a trigonometric polynomial of degree (a+2)M, so the uniform rule
    with more than (a+2)M + a points is exact up to rounding.
    """
    M = len(z) + 1
    n = n or 4 * ((a + 2) * M + a + 1)
    phi = 2 * np.pi * np.arange(n) / n
    vals = radius(z, phi) ** (a + 2) / (a + 2) * np.exp(1j * a * phi)
    return complex(vals.mean() * 2 * np.pi)


# Gauss-Legendre nodes: exact for the degree-(a+1) edge integrands used here.
_GL_X, _GL_W = np.polynomial.legendre.leggauss(8)


def polygon(z, n=60):
    phi = 2 * np.pi * np.arange(n) / n
    return radius(z, phi) * np.exp(1j * phi)


def polygon_moment(v, a):
    """Polygon: I_a = (1/2i) contour-integral of conj(zeta) zeta^a dzeta (Green)."""
    total = 0j
    for p, q in zip(v, np.roll(v, -1)):
        s = (_GL_X + 1) / 2
        pts = p + s * (q - p)
        total += np.sum(_GL_W / 2 * np.conj(pts) * pts ** a) * (q - p)
    return complex(total / 2j)


def polygon_symmetry_order(v, tol=TAU):
    """Largest k dividing n with exp(2 pi i/k) v_j = v_(j + n/k) for all j."""
    n = len(v)
    best = 1
    for k in range(2, n + 1):
        if n % k == 0 and np.max(np.abs(np.exp(2j * np.pi / k) * v
                                        - np.roll(v, -n // k))) <= tol:
            best = k
    return best
