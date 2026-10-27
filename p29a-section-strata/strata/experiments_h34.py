"""Explicit constructions for H3 and H4. Every function returns a JSON-able dict."""
from itertools import product

import numpy as np

from .experiments import MAPS5, _bisect_change, _loop_argmin, _w, _witness
from .loops import (TWO_PI, connection_rotation, max_step, passage_loop, path_down,
                    path_family, path_up, sector_loop, square_weights, stratum_audit,
                    unit_weights)
from .orientation import theta_M, theta_P, theta_Pprime
from .sections import area_moment, classify, rotate, section, stratum_distance, symmetry_order

# Two reference shapes per stratum: index 0 serves class A, index 1 class B.
REF = {
    "C1": (section(M=5, z2=0.12, z3=0.06j, z4=0.03, z5=0.02 * np.exp(0.4j)),
           section(M=5, z2=0.10 * np.exp(0.5j), z3=0.05, z4=0.02j, z5=0.03)),
    "C2": (section(M=5, z2=0.15, z4=0.04 * np.exp(0.7j)),
           section(M=5, z2=0.13 * np.exp(0.3j), z4=0.05)),
    "C3": (section(M=5, z3=0.12), section(M=5, z3=0.10 * np.exp(0.6j))),
    "C4": (section(M=5, z4=0.12), section(M=5, z4=0.10 * np.exp(0.9j))),
}
CLOSE = 1e-9


# --- H3 ------------------------------------------------------------------------

def _closures(classes, shapes, c, explicit=False):
    """(j, residual) for every relabel choice. explicit=True scores the
    representative closure, so the closing identification must be a listed relabel
    (attribution S); explicit=False scores section closure (attribution R)."""
    ks = [symmetry_order(shapes[X]) for X in classes]
    out = []
    for j in product(*(range(k) for k in ks)):
        _, info = sector_loop(classes, shapes, c, list(j))
        out.append((j, info["rep_residual"] if explicit else info["residual"]))
    return out


def _check_loop(classes, shapes, c, j):
    g, info = sector_loop(classes, shapes, c, list(j))
    return {"j": list(j), "residual": info["residual"], "T": info["T"],
            "A_1/2pi": round(connection_rotation(g, unit_weights(5), 2000) / TWO_PI, 9),
            "A_m2/2pi": round(connection_rotation(g, square_weights(5), 2000) / TWO_PI, 9),
            "max_step": max_step(g, 4000),
            "min_norm": stratum_audit(g, 1000)["circle"]}


def h3():
    cells = {}
    for SA, SB in product(REF, REF):
        shapes = {"A": REF[SA][0], "B": REF[SB][1]}
        aba = _closures(["A", "B", "A"], shapes, [0, 0.5, 0])
        bab = _closures(["B", "A", "B"], shapes, [0.5, 0, -0.5])
        closed_aba = [j for j, res in aba if res < CLOSE]
        closed_bab = [j for j, res in bab if res < CLOSE]
        exact_aba = [j for j, res in _closures(["A", "B", "A"], shapes, [0, 0.5, 0], True)
                     if res < CLOSE]
        exact_bab = [j for j, res in _closures(["B", "A", "B"], shapes, [0.5, 0, -0.5], True)
                     if res < CLOSE]
        aba_B = [j for j in exact_aba if j[0] == 0 and j[2] == 0]    # only B relabels
        aba_A = [j for j in exact_aba if j[1] == 0]                  # only A relabels
        bab_S = [j for j in exact_bab if j[1] == 0]
        cell = {
            "k_A": symmetry_order(shapes["A"]), "k_B": symmetry_order(shapes["B"]),
            "ABA_min_residual": min(res for _, res in aba),
            "ABA_section_closing_j": [list(j) for j in closed_aba],
            "ABA_explicit_closing_j": [list(j) for j in exact_aba],
            "BAB_section_closing_j": [list(j) for j in closed_bab],
            "survive_S": bool(aba_B and bab_S),
            "A_could_carry_instead": bool(aba_A),
            "survive_R": bool(closed_aba and closed_bab),
        }
        if closed_aba:
            pick = aba_B[0] if aba_B else closed_aba[0]
            cell["ABA_check"] = _check_loop(["A", "B", "A"], shapes, [0, 0.5, 0], pick)
        if closed_bab:
            cell["BAB_check"] = _check_loop(["B", "A", "B"], shapes, [0.5, 0, -0.5],
                                            bab_S[0] if bab_S else closed_bab[0])
        cells[f"S_A={SA},S_B={SB}"] = cell
    return cells


def h3_redistribution():
    """Attribution R is not deformation-invariant: in (C1, C2) A-B-A the half-turn
    moves continuously out of the B sector into the A sectors, closure held."""
    shapes = {"A": REF["C1"][0], "B": REF["C2"][1]}
    rows = []
    for s in (0.0, 0.5, 1.0):
        c = [s / 4, 0.5 - s / 2, s / 4]
        rows.append({"s": s, "c": c, **_check_loop(["A", "B", "A"], shapes, c, (0, 1, 0))})
    return rows


# --- H4a -----------------------------------------------------------------------

def h4a_rigid():
    shapes = {"A": REF["C1"][0], "B": REF["C2"][1]}
    out = {}
    for label, classes, c in (("A-B+-A", "ABA", [0, 0.5, 0]), ("A-B--A", "ABA", [0, -0.5, 0]),
                              ("B+-A-B-", "BAB", [0.5, 0, -0.5]),
                              ("B+-A-B+", "BAB", [0.5, 0, 0.5])):
        closing = [j for j, res in _closures(list(classes), shapes, c) if res < CLOSE]
        out[label] = {"2T": 2 * sum(c), "closing_j": [list(j) for j in closing]}
    # c_B off the half-turn with A held: no relabel closes the loop, so T is pinned
    for dc in (-0.01, 0.01):
        res = min(r for _, r in _closures(["A", "B", "A"], shapes, [0, 0.5 + dc, 0]))
        out[f"c_B = 0.5{dc:+.2f}"] = {"min_residual": res}
    return out


ABA_WINDOWS = [(1.094, 1.494, 2.694, 3.094)]
BAB_WINDOWS = [(1.094, 1.494, 2.694, 3.094), (3.189, 3.589, 4.789, 5.189)]


def _deg(m):
    idx = m - 2
    return lambda z: None if abs(z[idx]) < 1e-6 else float(np.angle(z[idx]))


def h4a_one_odd():
    """M = 3: N_3 = D_3(all-up resolution) + D_3(all-down resolution).

    D_3 is additive over windows, so the all-up and all-down pair has the same
    mean as the full set of minimal resolutions.
    """
    s_B, u = np.array([0.15, 0]), np.array([0, 0.06])
    cases = {"A-B+-A": (ABA_WINDOWS, [0.5]), "B+-A-B-": (BAB_WINDOWS, [0.5, -0.5])}
    ts = TWO_PI * np.arange(4000) / 4000
    out = {}
    for label, (windows, turns) in cases.items():
        rows = []
        for deform in (0.0, 0.5, 1.0):
            raw = passage_loop(s_B, u, windows, turns, deform)
            on_arc = [any(w[1] <= t <= w[2] for w in windows) for t in ts]
            off_win = [not any(w[0] <= t <= w[3] for w in windows) for t in ts]
            d2 = [stratum_distance(raw(t), 2) for t in ts]
            row = {"deform": deform,
                   "arc_max_d2": max(d for d, a in zip(d2, on_arc) if a),
                   "off_window_min_d2": min(d for d, o in zip(d2, off_win) if o),
                   "min_d3": min(stratum_distance(raw(t), 3) for t in ts),
                   "max_step": max_step(raw, 4000)}
            sums = {"D_3": 0.0, "theta_P": 0.0, "theta_Pprime": 0.0, "theta_M": 0.0}
            for name, p in (("up", path_up), ("down", path_down)):
                res = passage_loop(s_B, u, windows, turns, deform, path=p)
                row[f"{name}_min_d2"] = stratum_audit(res, 1000)["C2"]
                for key, th in (("D_3", _deg(3)), ("theta_P", theta_P),
                                ("theta_Pprime", theta_Pprime), ("theta_M", theta_M)):
                    w = _w(th, res)[0]
                    row[f"{name}_{key}"] = w
                    sums[key] += w
            row["N_3"] = sums["D_3"]
            row.update({f"sum_{k}": v for k, v in sums.items() if k != "D_3"})
            rows.append(row)
        out[label] = rows
    return out


def h4a_two_odd():
    """M = 5: the up and down resolutions are joined by a family of loops in V_free."""
    s_B = section(M=5, z2=0.15, z4=0.04 * np.exp(0.7j))
    u = section(M=5, z3=0.06, z5=0.03 * np.exp(1.1j))
    fam = lambda mu: passage_loop(s_B, u, ABA_WINDOWS, [0.5], path=path_family(mu))
    rows = []
    for mu in (0.0, 0.25, 0.5, 0.75, 1.0):
        g = fam(mu)
        audit = stratum_audit(g, 1000)
        rows.append({"mu": mu, **{k: _w(th, g)[0] for k, th in MAPS5.items()},
                     **{f"min_d_{k}": round(v, 6) for k, v in audit.items()}})
    singular = {"theta_P": lambda z: abs(z[0] * z[1]), "theta_R": lambda z: abs(z[2] * z[3]),
                "theta_M": lambda z: abs(area_moment(z, 2) * area_moment(z, 3))}
    mus = [r["mu"] for r in rows]
    witnesses = {}
    for name, th in MAPS5.items():
        found = []
        for lo, hi, rlo, rhi in zip(mus[:-1], mus[1:], rows[:-1], rows[1:]):
            if rlo[name] != rhi[name]:
                mu_star = _bisect_change(th, fam, lo, hi)
                g = fam(mu_star)
                t_star = _loop_argmin(lambda t: singular[name](g(t)))
                found.append({"mu": round(mu_star, 9), "t": round(t_star, 9),
                              "section": _witness(g(t_star))})
        witnesses[name] = found
    return {"rows": rows, "witnesses": witnesses}


# --- H4b -----------------------------------------------------------------------

def h4b():
    """Exact three-fold symmetry: equal sectors, gamma(t + 2pi/3) = R_alpha gamma(t)."""
    g, info = sector_loop(["B", "B", "B"], {"B": REF["C2"][1]}, [0.5, 0.5, 0.5], [0, 0, 0])
    alpha = TWO_PI * 0.5
    ts = TWO_PI * np.arange(600) / 600
    sym = max(float(np.max(np.abs(g(t + TWO_PI / 3) - rotate(g(t), alpha)))) for t in ts)
    centres = (0, TWO_PI / 3, 2 * TWO_PI / 3)
    aba, _ = sector_loop(["A", "B", "A"], {"A": REF["C1"][0], "B": REF["C2"][1]},
                         [0, 0.5, 0], [0, 1, 0])
    return {"BBB_symmetry_residual": sym, "BBB_T": info["T"],
            "BBB_closure_residual": info["residual"],
            "BBB_centre_strata": [classify(g(c))["stratum"] for c in centres],
            "ABA_centre_strata": [classify(aba(c))["stratum"] for c in centres]}
