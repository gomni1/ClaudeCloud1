"""Orientation maps, lifts and windings (SPEC 1.5-1.7).

Every map returns an angle in (-pi, pi] or None when the section is within the
domain margin ETA of the map's singular set.
"""
import numpy as np

from .sections import area_moment, polygon_moment

ETA = 1e-6        # domain margin
GUARD = np.pi / 2  # sampling guard on one lift step
MAX_DEPTH = 20


def _arg(*factors_and_powers):
    """arg of prod f^p (negative p means conjugate^|p|), or None near a zero."""
    value = 1 + 0j
    for f, p in factors_and_powers:
        if abs(f) < ETA:
            return None
        value *= f ** p if p > 0 else np.conj(f) ** (-p)
    return float(np.angle(value))


def theta_P(z):
    return _arg((z[1], 1), (z[0], -1))                 # arg(z3 conj z2)


def theta_R(z):
    return _arg((z[3], 1), (z[2], -1)) if len(z) >= 4 else None  # arg(z5 conj z4)


def theta_M(z):
    return _arg((area_moment(z, 3), 1), (area_moment(z, 2), -1))


def theta_M_polygon(v):
    return _arg((polygon_moment(v, 3), 1), (polygon_moment(v, 2), -1))


def theta_Pprime(z):
    """M = 3 only: theta_P + arg(z2^3 conj(z3)^2), another weight-1 map."""
    return _arg((z[1], 1), (z[0], -1), (z[0], 3), (z[1], -2))


def psi_2(z):
    return _arg((z[0], 1))                               # weight 2


MAPS = {"theta_P": theta_P, "theta_R": theta_R, "theta_M": theta_M}


class LiftError(RuntimeError):
    pass


def wrap(x):
    return (x + np.pi) % (2 * np.pi) - np.pi


def lift_samples(raw):
    """Lift wrapped angles; raises LiftError if any step breaks the guard."""
    raw = np.asarray(raw, dtype=float)
    steps = wrap(np.diff(raw))
    bad = np.flatnonzero(np.abs(steps) > GUARD)
    if bad.size:
        raise LiftError(f"sampling guard broken at step {int(bad[0])}: "
                        f"|step| = {abs(steps[bad[0]]):.3f} > pi/2")
    return np.concatenate([[raw[0]], raw[0] + np.cumsum(steps)])


def validate_lift(raw, lifted):
    """Accept a candidate lift only if it matches raw mod 2 pi and obeys the guard."""
    raw = np.asarray(raw, dtype=float)
    lifted = np.asarray(lifted, dtype=float)
    if np.max(np.abs(wrap(lifted - raw))) > 1e-9:
        return False, "lift does not reduce to the raw angles mod 2 pi"
    if np.max(np.abs(np.diff(lifted))) > GUARD:
        k = int(np.argmax(np.abs(np.diff(lifted))))
        return False, f"lift jumps by {np.diff(lifted)[k]:.3f} at step {k}"
    return True, "ok"


def _angle_at(theta, gamma, t):
    value = theta(gamma(t))
    if value is None:
        raise LiftError(f"map undefined on the loop at t = {t:.12f}")
    return value


def lift_along(theta, gamma, t0, t1, n=256):
    """Total change of theta(gamma(t)) for t in [t0, t1], bisecting bad steps."""
    ts = np.linspace(t0, t1, n + 1)
    vals = [_angle_at(theta, gamma, t) for t in ts]
    total = 0.0
    for i in range(n):
        total += _step(theta, gamma, ts[i], ts[i + 1], vals[i], vals[i + 1], 0)
    return total


def _step(theta, gamma, a, b, va, vb, depth):
    d = wrap(vb - va)
    if abs(d) <= GUARD:
        return d
    if depth >= MAX_DEPTH:
        raise LiftError(f"step at t = {a:.12f} still breaks the guard at depth {depth}")
    m = 0.5 * (a + b)
    vm = _angle_at(theta, gamma, m)
    return (_step(theta, gamma, a, m, va, vm, depth + 1)
            + _step(theta, gamma, m, b, vm, vb, depth + 1))


def winding(theta, gamma, n=256, weight=1):
    """W = lift over one period / (2 pi weight); returns (W, distance to integer)."""
    W = lift_along(theta, gamma, 0.0, 2 * np.pi, n) / (2 * np.pi * weight)
    return W, abs(W - round(W))
