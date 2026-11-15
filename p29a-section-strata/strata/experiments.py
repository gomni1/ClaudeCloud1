"""Explicit constructions for H0-H4. Every function returns a JSON-able dict."""
import numpy as np

from .loops import (TWO_PI, connection_rotation, find_passages, h1b_homotopy_M5,
                    max_step, square_weights, stratum_audit, unit_weights)
from .orientation import (LiftError, theta_M, theta_M_polygon, theta_P, theta_Pprime,
                          theta_R, winding, wrap)
from .sections import (area_moment, classify, codimension, polygon,
                       polygon_symmetry_order, rotate, section, stratum_distance)

MAPS5 = {"theta_P": theta_P, "theta_R": theta_R, "theta_M": theta_M}
MAPS3 = {"theta_P": theta_P, "theta_Pprime": theta_Pprime, "theta_M": theta_M}


def _w(theta, gamma, n=256):
    try:
        W, err = winding(theta, gamma, n)
        return round(W, 9), err
    except LiftError as exc:
        return None, str(exc)


def _witness(z):
    """Classification and stratum distances of a section where a map is singular."""
    c = classify(z)
    dists = {f"d{k}": stratum_distance(z, k) for k in range(2, len(z) + 2)}
    return {"g": c["g"], "stratum": c["stratum"],
            "min_d_k": min(dists.values()), **{k: round(v, 6) for k, v in dists.items()}}


def _golden_min(f, a, b, iters=120):
    g = (np.sqrt(5) - 1) / 2
    c, d = b - g * (b - a), a + g * (b - a)
    for _ in range(iters):
        if f(c) < f(d):
            b, d = d, c
            c = b - g * (b - a)
        else:
            a, c = c, d
            d = a + g * (b - a)
    return 0.5 * (a + b)


def _loop_argmin(f, n=512):
    ts = TWO_PI * np.arange(n) / n
    vals = [f(t) for t in ts]
    i = int(np.argmin(vals))
    return _golden_min(f, ts[i] - TWO_PI / n, ts[i] + TWO_PI / n)


# --- H0 ------------------------------------------------------------------------

def h0():
    table = {M: {f"C{k}": codimension(M, k) for k in range(2, M + 1)} for M in (3, 4, 5)}
    n = 60
    polygon_codim = {f"C{k}": 2 * n - 2 * n // k for k in (2, 3, 4, 5)}
    free = section(M=5, z2=0.12, z3=0.06j, z4=0.03, z5=0.02 * np.exp(0.4j))
    sym = {"C2": section(M=5, z2=0.15, z4=0.04 * np.exp(0.7j)),
           "C3": section(M=5, z3=0.12), "C4": section(M=5, z4=0.12)}
    poly = {"C1": polygon_symmetry_order(polygon(free, n), 1e-12),
            **{k: polygon_symmetry_order(polygon(z, n), 1e-12) for k, z in sym.items()}}
    return {"codim_smooth": table, "codim_60gon": polygon_codim,
            "60gon_detected_order": poly,
            "min_codim": min(v for row in table.values() for v in row.values())}


# --- H1 ------------------------------------------------------------------------

def _orbit(z0):
    return lambda t: rotate(z0, t)


def h1a():
    z0 = section(M=5, z2=0.12, z3=0.06j, z4=0.03, z5=0.02 * np.exp(0.4j))
    out = {}
    for name, th in MAPS5.items():
        W, err = _w(th, _orbit(z0))
        out[name] = {"W_orbit": W, "dist_to_int": err}
    return out


H1B_S = [0.0, 0.25, 0.75, 1.0, 1.2, 1.5, 1.8, 2.0]


def _bisect_change(theta, family, lo, hi, iters=40):
    W_lo = _w(theta, family(lo))[0]
    for _ in range(iters):
        mid = 0.5 * (lo + hi)
        W_mid = _w(theta, family(mid))[0]
        if W_mid is None:
            return mid
        if W_mid == W_lo:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def h1b_m5():
    fam = h1b_homotopy_M5
    rows = []
    for s in H1B_S:
        g = fam(s)
        audit = stratum_audit(g, 600)
        row = {"s": s, **{k: _w(th, g)[0] for k, th in MAPS5.items()},
               "A_1/2pi": round(connection_rotation(g, unit_weights(5), 2000) / TWO_PI, 6),
               "A_m2/2pi": round(connection_rotation(g, square_weights(5), 2000) / TWO_PI, 6),
               "min_d_C2": round(audit["C2"], 6), "min_d_C3": round(audit["C3"], 6),
               "min_d_C5": round(audit["C5"], 6)}
        rows.append(row)
    # witnesses: where each map's winding changes, and which section it passes
    singular = {"theta_P": lambda z: abs(z[0] * z[1]),
                "theta_R": lambda z: abs(z[2] * z[3]),
                "theta_M": lambda z: abs(area_moment(z, 2) * area_moment(z, 3))}
    witnesses = {}
    for name, th in MAPS5.items():
        found = []
        for lo, hi in zip(H1B_S[:-1], H1B_S[1:]):
            if rows[H1B_S.index(lo)][name] != rows[H1B_S.index(hi)][name]:
                s_star = _bisect_change(th, fam, lo, hi)
                g = fam(s_star)
                t_star = _loop_argmin(lambda t: singular[name](g(t)))
                found.append({"s": round(s_star, 9), "t": round(t_star, 9),
                              "section": _witness(g(t_star))})
        witnesses[name] = found
    return {"rows": rows, "witnesses": witnesses}


def _m3_family(s):
    return lambda t: np.array([0.15 * np.exp(2j * t) * (1 + 0.3 * s * np.cos(t)),
                               0.08 * np.exp(3j * t) * np.exp(1j * s * np.sin(2 * t))
                               * (1 + 0.3 * s * np.sin(t))])


def h1b_m3():
    rows = []
    for s in (0.0, 0.5, 1.0):
        g = _m3_family(s)
        audit = stratum_audit(g, 600)
        rows.append({"s": s, **{k: _w(th, g)[0] for k, th in MAPS3.items()},
                     "min_d_C2": round(audit["C2"], 6), "min_d_C3": round(audit["C3"], 6)})
    return {"rows": rows}


# --- H2 ------------------------------------------------------------------------

FLIP_CASES = {
    2: (section(M=5, z2=0.15, z4=0.04 * np.exp(0.7j)),
        section(M=5, z3=0.06, z5=0.03 * np.exp(1.1j))),
    3: (section(M=5, z3=0.12),
        section(M=5, z2=0.05, z4=0.03 * np.exp(0.4j), z5=0.02 * np.exp(1.3j))),
    4: (section(M=5, z4=0.12),
        section(M=5, z2=0.05, z3=0.04 * np.exp(0.3j), z5=0.02 * np.exp(0.9j))),
}


def _turns(d):
    """An angle difference as a fraction of a turn in [0, 1)."""
    return round(float(wrap(d)) / TWO_PI % 1.0, 12)


def flip_field(k, eps=1.0):
    """Body path s + eps u -> s -> s + eps R_(2pi/k) u, in two straight halves."""
    s, u = FLIP_CASES[k]
    u_end = rotate(u, TWO_PI / k)

    def gamma(lam):
        lam = lam / TWO_PI                     # parameter in [0, 1]
        if lam <= 0.5:
            return s + eps * (1 - 2 * lam) * u
        return s + eps * (2 * lam - 1) * u_end
    return gamma


def h2a():
    out = {}
    for k, (s, u) in FLIP_CASES.items():
        g = flip_field(k)
        start, end = g(0.0), g(TWO_PI)
        same = float(np.max(np.abs(end - rotate(start, TWO_PI / k))))
        jumps = {}
        for name, th in MAPS5.items():
            jumps[name] = _turns(th(end) - th(start))
        jumps["theta_M_60gon"] = _turns(theta_M_polygon(polygon(end))
                                        - theta_M_polygon(polygon(start)))
        out[f"k={k}"] = {"expected_turns": round(1 / k, 12),
                         "jumps_turns": jumps,
                         "end_equals_R_(2pi/k)_start": same,
                         "middle_section": classify(g(np.pi))["stratum"],
                         "middle_norm": float(np.linalg.norm(g(np.pi))),
                         "max_step_N2000": max_step(g, 2000),
                         "max_step_N4000": max_step(g, 4000)}
    return out


def h2b_m3():
    """M = 3: a loop pushed across C2 (z3 -> 0) and across C3 (z2 -> 0)."""
    def across_c2(s):
        return lambda t: np.array([0.15 * np.exp(2j * t),
                                   0.08 * ((1 - s) * np.exp(3j * t) + 0.5 * s)])

    def across_c3(s):
        return lambda t: np.array([0.15 * ((1 - s) * np.exp(2j * t) + 0.5 * s),
                                   0.08 * np.exp(3j * t)])
    z3_deg = lambda z: None if abs(z[1]) < 1e-6 else float(np.angle(z[1]))
    z2_deg = lambda z: None if abs(z[0]) < 1e-6 else float(np.angle(z[0]))
    out = {}
    for label, fam, s_cross, idx in (("across_C2", across_c2, 2 / 3, 1),
                                     ("across_C3", across_c3, 2 / 3, 0)):
        rows = []
        for s in (0.5, 0.8):
            g = fam(s)
            rows.append({"s": s, "theta_P": _w(theta_P, g)[0],
                         "theta_Pprime": _w(theta_Pprime, g)[0],
                         "theta_M": _w(theta_M, g)[0],
                         "D_3": _w(z3_deg, g)[0], "D_2": _w(z2_deg, g)[0]})
        g = fam(s_cross)
        t_star = _loop_argmin(lambda t: abs(g(t)[idx]))
        out[label] = {"rows": rows, "crossing_s": s_cross,
                      "crossing_section": classify(g(t_star))["stratum"]}
    return out


def h2c():
    """No weight-1 map is defined on a symmetric section (numerical side of L1)."""
    syms = {"C2": section(M=5, z2=0.15, z4=0.04 * np.exp(0.7j)),
            "C3": section(M=5, z3=0.12), "C4": section(M=5, z4=0.12),
            "C5": section(M=5, z5=0.12), "circle": section(M=5)}
    out = {}
    for label, z in syms.items():
        out[label] = {name: th(z) for name, th in MAPS5.items()}
        out[label]["theta_M_60gon"] = theta_M_polygon(polygon(z))
    return out
