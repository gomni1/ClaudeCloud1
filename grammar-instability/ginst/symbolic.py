"""M0 and M1 by sympy (SPEC §2, §3)."""
import itertools

import sympy as sp

k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12 = sp.symbols("k1 k2 k3 k5 k6 k7 k8 k9 k10 k11 k12", positive=True)
y, h, lam = sp.symbols("y h lambda", positive=True)
gC, gV, gam = sp.symbols("g_C g_V gamma", real=True)
RATES = (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12)
a = k1 + k2 + k7
A = k2 + k7 + k1 * k5 / (k5 + k6)


def J_general(gc, gv, gl=0, gp=0, open_=True):
    """Jacobian with dg = (gc, gv, gl, gp)."""
    o = 1 if open_ else 0
    return sp.Matrix([
        [-a + gc, gv, k6 + gl, gp],
        [k2 - gc, -gv, k5 - gl, k8 - gp],
        [k1, 0, -(k5 + k6), 0],
        [k7, 0, 0, -(k8 + o * k9)],
    ])


def poly_sign(expr, variables, positive_symbols=()):
    """Clear denominators; classify the numerator's coefficient signs over the given variables.

    Returns ('positive' | 'negative' | 'mixed' | 'zero', numerator, denominator, n_neg_terms)."""
    expr = sp.together(sp.expand(expr))
    num, den = sp.fraction(expr)
    num = sp.expand(num)
    den = sp.expand(den)
    if num == 0:
        return "zero", num, den, 0
    P = sp.Poly(num, *variables)
    coeffs = P.coeffs()
    pos = sum(1 for c in coeffs if c > 0)
    neg = sum(1 for c in coeffs if c < 0)
    Pd = sp.Poly(den, *variables)
    dpos = all(c > 0 for c in Pd.coeffs())
    dneg = all(c < 0 for c in Pd.coeffs())
    if not (dpos or dneg):
        return "mixed-denominator", num, den, neg
    if dneg:
        pos, neg = neg, pos
    if neg == 0:
        return "positive", num, den, 0
    if pos == 0:
        return "negative", num, den, neg
    return "mixed", num, den, neg


def hurwitz_quartic(c3, c2, c1, c0):
    return dict(c3=c3, c2=c2, c1=c1, c0=c0, D2=c3 * c2 - c1, D3=c3 * c2 * c1 - c1 ** 2 - c3 ** 2 * c0)


def hurwitz_cubic(c2, c1, c0):
    return dict(c2=c2, c1=c1, c0=c0, D2=c2 * c1 - c0)


def charpoly_coeffs(M):
    """Coefficients of det(lam I - M) after the leading 1 (Berkowitz; no simplification)."""
    c = M.charpoly(lam).all_coeffs()
    return [sp.together(sp.expand(ci)) for ci in c[1:]]


def m0():
    out = {}
    vars_open = list(RATES[:10]) + [y, h]  # k12 does not enter J
    # open level, cv: gC = A - y h, gV = h
    J = J_general(A - y * h, h)
    c3, c2, c1, c0 = charpoly_coeffs(J)
    det_minusJ = sp.factor(sp.together(sp.expand((-J).det(method='berkowitz'))))
    conds = hurwitz_quartic(c3, c2, c1, c0)
    res = {k: poly_sign(v, vars_open)[0] for k, v in conds.items()}
    out["open_cv"] = dict(det_minus_J=str(det_minusJ), hurwitz_signs_for_h_positive=res,
                          holds=all(v == "positive" for v in res.values()))
    # closed level, cv: reduced 3x3
    Jc = J_general(A - y * h, h, open_=False)
    Jr = Jc[:3, :3] - Jc[:3, 3] * sp.Matrix([[1, 1, 1]])
    d2, d1, d0 = charpoly_coeffs(Jr)
    conds = hurwitz_cubic(d2, d1, d0)
    vars_closed = [k1, k2, k3, k5, k6, k7, k8, k10, y, h]
    res = {k: poly_sign(v, vars_closed)[0] for k, v in conds.items()}
    out["closed_cv"] = dict(det_minus_Jred=str(sp.factor(sp.together(sp.expand((-Jr).det(method='berkowitz'))))), hurwitz_signs_for_h_positive=res,
                            holds=all(v == "positive" for v in res.values()))
    # tot denominator: g homogeneous of degree 1 in (C, V, L, P) with gL = gP = gamma.
    # At a balance gC = A - y gV - (l + p) gamma (Euler), with l = L/C, p = P/C.
    l_, p_ = sp.symbols("l p", positive=True)
    for lvl, open_ in (("open", True), ("closed", False)):
        Jt = J_general(A - y * gV - (l_ + p_) * gam, gV, gam, gam, open_=open_)
        if open_:
            cs = charpoly_coeffs(Jt)
            conds = hurwitz_quartic(*cs)
            variables = list(RATES[:10]) + [y, gV, gam, l_, p_]
        else:
            Jr = Jt[:3, :3] - Jt[:3, 3] * sp.Matrix([[1, 1, 1]])
            conds = hurwitz_cubic(*charpoly_coeffs(Jr))
            variables = [k1, k2, k3, k5, k6, k7, k8, k10, y, gV, gam, l_, p_]
        res = {}
        broken = []
        for k, v in conds.items():
            s, num, den, nneg = poly_sign(v, variables)
            res[k] = s
            if s != "positive":
                # terms that are not sign-definite: those carrying gamma with a negative coefficient
                P = sp.Poly(sp.expand(num), *variables)
                negs = [sp.Mul(c, *[vv ** e for vv, e in zip(variables, mon)]) for mon, c in P.terms() if c < 0]
                broken.append(dict(condition=k, n_negative_terms=nneg, examples=[str(t) for t in negs[:4]]))
        out["%s_tot" % lvl] = dict(hurwitz_signs=res, holds=all(v == "positive" for v in res.values()),
                                   where_it_breaks=broken,
                                   note="gamma = dg/dL = dg/dP = (k3 V F'_kr - k11 C F'_kc) * (-C/N^2) has no fixed sign")
    return out


def principal_minors(M):
    n = M.shape[0]
    res = {}
    for r in range(1, n + 1):
        for S in itertools.combinations(range(n), r):
            res[S] = M.extract(list(S), list(S)).det(method="berkowitz")
    return res


def m1():
    out = {}
    names = "CVLP"
    # MA, open level, closed-form balance
    Cs = k12 * (k8 + k9) / (k7 * k9)
    Vs = (A * Cs + k11 * Cs ** 2) / (k10 + k3 * Cs)
    gc = k3 * Vs - 2 * k11 * Cs
    gv = k10 + k3 * Cs
    M = -J_general(gc, gv)
    variables = list(RATES)
    ma = {}
    for S, mnr in principal_minors(M).items():
        s, num, den, nneg = poly_sign(mnr, variables)
        ma["".join(names[i] for i in S)] = dict(sign=s, n_negative_terms=nneg, n_terms=len(sp.Poly(num, *variables).terms()))
    out["MA_open"] = dict(minors=ma, all_positive=all(v["sign"] == "positive" for v in ma.values()))
    # TH (any m, kr, kc), open level, cv: in terms of (k, y, h)
    M = -J_general(A - y * h, h)
    variables = list(RATES[:10]) + [y, h]
    th = {}
    for S, mnr in principal_minors(M).items():
        s, num, den, nneg = poly_sign(mnr, variables)
        th["".join(names[i] for i in S)] = dict(sign=s, factored=str(sp.factor(sp.together(sp.expand(mnr)))))
    out["TH_open_cv"] = dict(minors=th, all_positive_for_h_positive=all(v["sign"] == "positive" for v in th.values()))
    # any rate law with g = g(C, V): the {C, V} minor
    M = -J_general(gC, gV)
    out["general_gCV_minor_CV"] = str(sp.factor(M.extract([0, 1], [0, 1]).det()))
    return out


if __name__ == "__main__":
    import json
    import sys
    import time
    t0 = time.time()
    r = dict(M1=m1())
    json.dump(r, open(sys.argv[1], "w"), indent=1, default=str)
    print("M1 done %.0fs" % (time.time() - t0), flush=True)
    r["M0"] = m0()
    json.dump(r, open(sys.argv[1], "w"), indent=1, default=str)
    print("M0 done %.0fs" % (time.time() - t0), flush=True)
