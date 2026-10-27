"""Exact checks in sympy. Each check returns (name, passed, detail).

Hand-proof steps that sympy cannot carry (the general obstruction lemma, the
pi_1 statements) are written out in RESULTS.md; the checks here verify the
algebra those proofs rest on.
"""
from math import gcd
from functools import reduce

import sympy as sp

phi, beta, eps = sp.symbols("phi beta epsilon", real=True)


def _modes(M):
    return list(range(2, M + 1))


def _z(M, prefix="z"):
    return {m: sp.Symbol(f"{prefix}{m}a", real=True) + sp.I * sp.Symbol(f"{prefix}{m}b", real=True)
            for m in _modes(M)}


def _r(z, angle):
    return 1 + sum((zm * sp.exp(-sp.I * m * angle) + sp.conjugate(zm) * sp.exp(sp.I * m * angle)) / 2
                   for m, zm in z.items())


def _rot(z, b):
    return {m: zm * sp.exp(sp.I * m * b) for m, zm in z.items()}


def check_rotation_action(M=5):
    z = _z(M)
    diff = sp.expand(_r(z, phi - beta) - _r(_rot(z, beta), phi))
    return ("rotation action r(phi - beta) <-> z_m e^(i m beta)", sp.simplify(diff) == 0,
            f"M = {M}")


def check_stabilizers(M=5):
    """C_k is fixed by R_(2pi/k); a mode with k not dividing m is moved."""
    ok, notes = True, []
    for k in range(2, M + 1):
        for m in _modes(M):
            phase = sp.simplify(sp.exp(2 * sp.pi * sp.I * m / k))
            fixed = sp.simplify(phase - 1) == 0
            if fixed != (m % k == 0):
                ok = False
                notes.append(f"k={k}, m={m}")
    return ("stabilizer of C_k contains R_(2pi/k); other modes are moved", ok,
            "all (k, m) consistent" if ok else ", ".join(notes))


def check_map_weights_and_vanishing(M=5):
    """theta_P, theta_R, theta_P' have weight 1, psi_2 weight 2, and the
    weight-1 polynomials vanish identically on every C_k, k >= 2."""
    z = _z(M)
    zr = _rot(z, beta)
    c = sp.conjugate
    polys = {
        "theta_P": (lambda w: w[3] * c(w[2]), 1),
        "theta_R": (lambda w: w[5] * c(w[4]), 1),
        "psi_2": (lambda w: w[2], 2),
    }
    ok, notes = True, []
    for name, (f, wt) in polys.items():
        ratio = sp.simplify(sp.expand(f(zr) - sp.exp(sp.I * wt * beta) * f(z)))
        if ratio != 0:
            ok = False
            notes.append(f"{name} weight")
        if wt == 1:
            for k in range(2, M + 1):
                restricted = {m: (zm if m % k == 0 else 0) for m, zm in z.items()}
                if sp.simplify(f(restricted)) != 0:
                    ok = False
                    notes.append(f"{name} nonzero on C{k}")
    prime = lambda w: w[3] * c(w[2]) * w[2] ** 3 * c(w[3]) ** 2
    z3 = _z(3)
    if sp.simplify(sp.expand(prime(_rot(z3, beta)) - sp.exp(sp.I * beta) * prime(z3))) != 0:
        ok = False
        notes.append("theta_P' weight")
    return ("map weights; weight-1 maps vanish on every symmetric stratum", ok,
            "theta_P, theta_R, theta_P' weight 1; psi_2 weight 2" if ok else "; ".join(notes))


def codimension_table(Ms=(3, 4, 5, 6)):
    table = {M: {k: 2 * sum(1 for m in range(2, M + 1) if m % k) for k in range(2, M + 1)}
             for M in Ms}
    ok = all(v >= 2 for row in table.values() for v in row.values())
    return ("codim_R C_k = 2 #{m : k does not divide m} >= 2", ok, table)


def check_flip_identity(M=5):
    """R_(2pi/k)(s + eps u) = s + eps R_(2pi/k) u for s in C_k; for k = 2 and odd u
    this is s - eps u (teardrop -> ellipse -> flipped teardrop)."""
    ok = True
    for k in (2, 3, 4):
        s = {m: (sp.Symbol(f"s{m}") if m % k == 0 else 0) for m in _modes(M)}
        u = {m: (sp.Symbol(f"u{m}") if m % k else 0) for m in _modes(M)}
        lhs = _rot({m: s[m] + eps * u[m] for m in s}, 2 * sp.pi / k)
        rhs = {m: s[m] + eps * _rot(u, 2 * sp.pi / k)[m] for m in s}
        ok &= all(sp.simplify(lhs[m] - rhs[m]) == 0 for m in s)
        if k == 2:
            flipped = {m: s[m] - eps * u[m] for m in s}
            ok &= all(sp.simplify(lhs[m] - flipped[m]) == 0 for m in s)
    return ("flip identity R_(2pi/k)(s + eps u) = s + eps R_(2pi/k) u; k = 2 gives s - eps u",
            ok, "k = 2, 3, 4 with symbolic s, u")


def check_closure_lemma():
    """R_x s = s iff x in (2 pi / g) Z, g = gcd of active modes (Bezout)."""
    cases = {"C1 {2,3,4,5}": [2, 3, 4, 5], "C1 {3,4}": [3, 4], "C1 {2,5}": [2, 5],
             "C2 {2,4}": [2, 4], "C3 {3}": [3], "C4 {4}": [4]}
    ok, detail = True, {}
    x = sp.Symbol("x", real=True)
    for name, S in cases.items():
        g = reduce(gcd, S)
        # x = 2 pi / g fixes every active mode
        fixes = all(sp.simplify(sp.exp(sp.I * m * 2 * sp.pi / g) - 1) == 0 for m in S)
        # Bezout: 1 = sum n_m (m / g), so m x in 2 pi Z for all m forces x g in 2 pi Z
        coeffs = _bezout([m // g for m in S])
        bez = sum(n * (m // g) for n, m in zip(coeffs, S)) == 1
        ok &= fixes and bez
        detail[name] = {"g": g, "bezout": coeffs}
    return ("closure lemma: rigid twist quantum is 1/g turn", ok, detail)


def _bezout(nums):
    coeffs, acc = [1], nums[0]
    for n in nums[1:]:
        s, t, h = sp.gcdex(acc, n)
        coeffs = [int(s) * c for c in coeffs] + [int(t)]
        acc = int(h)
    return coeffs


def check_h1b_homotopy_avoidance():
    """Stage 1 of h1b_homotopy_M5: z3 and z5 vanish at different s."""
    s = sp.Symbol("s", positive=True)
    s3 = sp.solve(sp.Eq((1 - s) * sp.Rational(1, 10), s * sp.Rational(1, 10)), s)
    s5 = sp.solve(sp.Eq((1 - s) * sp.Rational(1, 20), s * sp.Rational(1, 40)), s)
    ok = s3 == [sp.Rational(1, 2)] and s5 == [sp.Rational(2, 3)]
    return ("H1b homotopy: (z3, z5) never vanish together (s = 1/2 vs 2/3)", ok,
            {"z3 zero at s": str(s3), "z5 zero at s": str(s5)})


def check_one_odd_parity():
    """M = 3: pi_1(V_free) = Z^2 via (deg z2, deg z3). Orbit = (2, 3),
    meridian of C2 = (0, 1), half-loop H = (1, 2) or (1, 1). Every homomorphism
    h with h(orbit) = 0 has h(meridian) even, so the parity of the
    resolution-summed winding is the same for every weight-1 map."""
    orbit = sp.Matrix([2, 3])
    meridian = sp.Matrix([0, 1])
    halves = [sp.Matrix([1, 2]), sp.Matrix([1, 1])]
    ok = (2 * halves[0] == orbit + meridian) and (2 * halves[1] == orbit - meridian)
    null = sp.Matrix([[2, 3]]).nullspace()[0]          # h with h . orbit = 0
    # integer generator of those h, after clearing denominators
    h_int = null * sp.ilcm(*[sp.fraction(v)[1] for v in null])
    ok &= sp.Mod((h_int.T * meridian)[0], 2) == 0
    return ("M = 3: parity of the resolution-summed winding is map-independent", bool(ok),
            {"invariant-phase homomorphisms": f"lambda * {list(h_int)}",
             "h(meridian)": str((h_int.T * meridian)[0]) + " * lambda"})


def check_pf3_exact():
    """PF3: a C2 section with z3 = z5 = 10^-7 is exactly asymmetric."""
    z = {2: sp.Rational(3, 20), 3: sp.Rational(1, 10 ** 7), 4: sp.Rational(1, 25),
         5: sp.Rational(1, 10 ** 7)}
    g = reduce(gcd, [m for m, v in z.items() if v != 0])
    return ("PF3 exact: near-C2 section has g = 1", g == 1, {"g": g})


ALL = [check_rotation_action, check_stabilizers, check_map_weights_and_vanishing,
       codimension_table, check_flip_identity, check_closure_lemma,
       check_h1b_homotopy_avoidance, check_one_odd_parity, check_pf3_exact]


def run_all():
    return [f() for f in ALL]
