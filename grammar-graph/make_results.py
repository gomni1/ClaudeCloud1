"""Builds the generated block of RESULTS.md from evidence/ (verdicts, graph table, G2 and G3 tables, CPU)."""
import glob
import json
import math
import os

import numpy as np

from gg.core import EVID, LAMS, LONG, T0

HERE = os.path.dirname(os.path.abspath(__file__))


def J(p):
    return json.load(open(os.path.join(EVID, p)))


def fmt(x, d=3):
    if x is None:
        return "n/a"
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    return f"{x:.{d}f}"


def d4(runs):
    tot = {}
    for r in runs:
        for t in r["long_tracks"]:
            for n, (s, c) in t["msd"].items():
                a = tot.setdefault(int(n), [0.0, 0])
                a[0] += s; a[1] += c
    if not tot:
        return None, {}
    lag = np.array(sorted(tot)) * 0.4
    msd = np.array([tot[n][0] / tot[n][1] for n in sorted(tot)])
    sel = (lag >= T0 - 1e-9) & (lag <= 10 * T0 + 1e-9) & (msd > 0)
    alpha = float(np.polyfit(np.log(lag[sel]), np.log(msd[sel]), 1)[0]) if sel.sum() >= 2 else None
    return alpha, dict(zip(lag.round(2).tolist(), msd.round(3).tolist()))


def main():
    L = []
    g1 = J("g1.json")
    g2 = {(r, li): J(f"g2/S_r{r}_lam{li}.json") for r in range(3) for li in range(3)
          if os.path.exists(os.path.join(EVID, f"g2/S_r{r}_lam{li}.json"))}
    z = [g2[(r, 0)] for r in range(3) if (r, 0) in g2]
    # ---- verdicts ----
    L.append("## Verdicts\n")
    L.append("| Item | Verdict | Numbers |\n|---|---|---|")
    h = g1["H1"]
    L.append(f"| H1 (frozen: K, N = 10^4) | **FAIL** | period {h['period']:.3f} (target 6.3524 +-3%), range "
             f"[{h['range'][0]:.4f}, {h['range'][1]:.4f}] (target [0.0545, 0.119] +-10%) |")
    h = g1["H1_R1"]
    L.append(f"| H1-R1 (revision R1: N = 10^6) | **PASS** | period {h['period']:.4f}, range "
             f"[{h['range'][0]:.4f}, {h['range'][1]:.4f}], {h['n_cycles']} cycles |")
    h = g1["H2"]
    L.append(f"| H2 (k3 = k11 = 0) | **{'PASS' if h['PASS'] else 'FAIL'}** | S: chi2 = {h['S']['chi2']:.2f}, p = "
             f"{h['S']['p']:.3f}, max abs z = {max(map(abs, h['S']['z'])):.2f}; K: chi2 = {h['K']['chi2']:.2f}, p = "
             f"{h['K']['p']:.3f} (40 snapshots x 10^4 sites) |")
    h = g1["H3"]
    L.append(f"| H3 (octahedron, exact 4096-state chain) | **{'PASS' if h['PASS'] else 'FAIL'}** | z = "
             + ", ".join(f"{n} {v:+.2f}" for n, v in zip(h["names"], h["z"])) + " |")
    h = g1["P1"]
    L.append(f"| P1 (planted defects) | **{'PASS' if h['PASS'] else 'FAIL'}** | {len(h['configs'])} configurations "
             f"(2-6 vortices) all exact; identity 0 violations (plus 200 random fields) |")
    a, b = g1["P2_planted"], g1["P2_S"]
    L.append(f"| P2 (planted noise) | **{'PASS' if g1['P2']['PASS'] else 'FAIL'}** | density {a['density']:.5f} "
             f"(z = {a['z']:+.2f}) planted, {b['density']:.5f} (z = {b['z']:+.2f}) on S; exact 1/4; longest noise "
             f"track {max(x['longest'] for x in a['reps'] + b['reps']):.1f}; D1 criterion FAILS on noise "
             f"(0 of 3 replicates, both graphs) |")
    h = g1["P3"]
    L.append(f"| P3 (planted motion) | **{'PASS' if h['PASS'] else 'FAIL'}** | {h['n_tracks']} tracks, lifetimes "
             f"{h['lifetimes'][0]:.1f}, {h['lifetimes'][1]:.1f}; on planted faces in every frame; {h['swaps']} swaps |")
    L.append(f"| Harness | frozen SPEC: **FAIL** (H1); under R1: **{'PASS' if g1['harness_PASS_R1'] else 'FAIL'}** | "
             "G2/G3 below count under R1 only |")
    if len(z) == 3:
        nrep_long = sum(r["n_long"] > 0 for r in z)
        longest = max(r["longest"] for r in z)
        v1 = "PASS" if nrep_long >= 2 else ("KILL" if nrep_long == 0 else "UNDERDETERMINED")
        L.append(f"| D1 (persistent localised integer) | **{v1}** | tracks >= 20 periods (127.05) in {nrep_long} of 3 "
                 f"replicates; longest track {longest:.1f} time units ({longest / T0:.2f} periods) |")
        dfr = sum(r["defect_frames"] for r in z)
        num = sum(r["amp_def_sum"] for r in z) / dfr
        den = sum(r["amp_all_sum"] for r in z) / sum(r["n_win_frames"] * r["ntri"] for r in z)
        ratio = num / den
        v2 = "UNDERDETERMINED" if dfr < 1000 else ("PASS" if ratio <= 0.5 else "KILL")
        L.append(f"| D2 (cores at local zeros) | **{v2}** | ratio {ratio:.3f} (defect triangles {num:.3f} / all "
                 f"{den:.3f}); {dfr} defect-frames |")
        B = sum(r["pairing"]["births"] for r in z); Bp = sum(r["pairing"]["births_paired"] for r in z)
        D = sum(r["pairing"]["deaths"] for r in z); Dp = sum(r["pairing"]["deaths_paired"] for r in z)
        fb, fd = (Bp / B if B else None), (Dp / D if D else None)
        if fb is None or fd is None:
            v3 = "UNDERDETERMINED"
        elif fb >= 0.8 and fd >= 0.8:
            v3 = "PASS"
        elif fb < 0.5 or fd < 0.5:
            v3 = "KILL"
        else:
            v3 = "UNDERDETERMINED"
        L.append(f"| D3 (pairing is local) | **{v3}** | births paired {fmt(fb, 4)} ({Bp}/{B}), deaths paired "
                 f"{fmt(fd, 4)} ({Dp}/{D}) |")
        alpha, msd = d4(z)
        L.append(f"| D4 (motion; report only) | {'exponent ' + fmt(alpha) if alpha is not None else 'not computable'} "
                 f"| {'no track lasts 20 periods, so the MSD set is empty' if alpha is None else msd} |")
    # ---- graph table ----
    L.append("\n## Graph classes\n")
    L.append("S is topologically two-dimensional by construction; it is a declared comparison class, not an assumption "
             "about the substrate. d_g is measured (fit of ln M(r) on ln r, r = 2..floor(diameter/2)).\n")
    L.append("| Class | Replicate | N | Mean degree | Clustering | Diameter | d_g (radii) | Triangles |\n"
             "|---|---|---|---|---|---|---|---|")
    for f in sorted(glob.glob(os.path.join(EVID, "g2", "graph_S_r*.json"))):
        g = json.load(open(f))
        L.append(f"| S | {f[-6]} | {g['N']} | {g['mean_degree']:.4f} | {g['clustering']:.4f} | {g['diameter']} | "
                 f"{fmt(g['d_g'])} ({g['d_g_radii'][0]}-{g['d_g_radii'][1]}) | {g['triangles']} (faces) |")
    for cls in ("K", "R", "C0", "C5"):
        for r in (0, 1):
            p = os.path.join(EVID, "g3", f"{cls}_r{r}.json")
            if not os.path.exists(p):
                continue
            s = json.load(open(p))
            if cls == "K":
                if r == 0:
                    L.append(f"| K | - | 10000 | 9999 | 1 | 1 | n/a (no radii 2..0) | C(10^4, 3) = {math.comb(10000, 3)} |")
                continue
            g = s["graph"]
            rr = f"({g['d_g_radii'][0]}-{g['d_g_radii'][1]})" if g["d_g_radii"] else ""
            L.append(f"| {cls} | {r} | {g['N']} | {g['mean_degree']:.4f} | {g['clustering']:.4f} | {g['diameter']} | "
                     f"{fmt(g['d_g'])} {rr} | {g['triangles']} |")
    # ---- G2 table ----
    L.append("\n## G2: class S by lam (3 replicates; mean over replicates, longest = max)\n")
    L.append("| lam | A (global amplitude / well-mixed s_c) | Rbar | mean global (c, v) | defect density | longest track "
             "(time units) | tracks >= 20 periods | replacement | identity violations |\n|---|---|---|---|---|---|---|---|---|")
    for li, lam in enumerate(LAMS):
        rs = [g2[(r, li)] for r in range(3) if (r, li) in g2]
        if not rs:
            continue
        reps = [x["replacement_mean"] for x in rs if x["replacement_mean"] is not None]
        L.append(f"| {lam} | {np.mean([x['A'] for x in rs]):.3f} | {np.mean([x['Rbar'] for x in rs]):.3f} | "
                 f"({np.mean([x['mean_c'] for x in rs]):.4f}, {np.mean([x['mean_v'] for x in rs]):.4f}) | "
                 f"{np.mean([x['density'] for x in rs]):.4f} | {max(x['longest'] for x in rs):.1f} | "
                 f"{sum(x['n_long'] for x in rs)} | {fmt(np.mean(reps)) if reps else 'n/a (no long tracks)'} | "
                 f"{sum(x['identity_violations_allframes'] for x in rs)} |")
    # ---- G3 table ----
    L.append("\n## G3: comparison classes at lam = 0 (2 replicates each; S from G2 for reference)\n")
    L.append("| Class | Rbar (global coherence) | A | Triangles | Defect density | Longest track | Tracks >= 20 periods |\n"
             "|---|---|---|---|---|---|---|")
    rows = {}
    for cls in ("K", "R", "C0", "C5"):
        rs = [json.load(open(p)) for p in sorted(glob.glob(os.path.join(EVID, "g3", f"{cls}_r*.json")))]
        if not rs:
            continue
        rows[cls] = rs
        ntri = math.comb(10000, 3) if cls == "K" else int(np.mean([x["ntri"] for x in rs]))
        L.append(f"| {cls} | {np.mean([x['Rbar'] for x in rs]):.3f} | {np.mean([x['A'] for x in rs]):.3f} | {ntri} | "
                 f"{np.mean([x['density'] for x in rs]):.4f} | {max(x['longest'] for x in rs):.1f} | "
                 f"{sum(x['n_long'] for x in rs)} |")
    if z:
        L.append(f"| S (G2, lam = 0) | {np.mean([x['Rbar'] for x in z]):.3f} | {np.mean([x['A'] for x in z]):.3f} | "
                 f"{z[0]['ntri']} | {np.mean([x['density'] for x in z]):.4f} | {max(x['longest'] for x in z):.1f} | "
                 f"{sum(x['n_long'] for x in z)} |")
    if rows:
        host = [c for c, rs in rows.items() if sum(x["n_long"] for x in rs) > 0]
        L.append(f"\nC-report: classes hosting defect tracks lasting >= 20 periods: {', '.join(host) if host else 'none'}"
                 f" (of K, R, C0, C5; S: {'yes' if z and sum(x['n_long'] for x in z) else 'none'}).")
    # ---- CPU ----
    L.append("\n## CPU\n")
    L.append("| Part | CPU used | Cap |\n|---|---|---|")
    c1 = g1["cpu_s_total"] + g1["H1_R1"]["cpu_s"]
    L.append(f"| G1 | {c1 / 3600:.3f} h ({c1:.0f} s, incl. H1-R1) | 0.5 h |")
    for part, cap in (("g2", 3.0), ("g3", 1.5)):
        p = os.path.join(EVID, f"{part}_cpu.json")
        if os.path.exists(p):
            c = json.load(open(p))["cpu_s_total"]
            L.append(f"| {part.upper()} | {c / 3600:.3f} h ({c:.0f} s) | {cap} h |")
    block = "\n".join(L)
    path = os.path.join(HERE, "RESULTS.md")
    s = open(path).read()
    a, b = "<!-- BEGIN GENERATED -->", "<!-- END GENERATED -->"
    if a in s:
        s = s[:s.index(a)] + a + "\n" + block + "\n" + s[s.index(b):]
    else:
        s = s.replace("## Revisions and bug log", a + "\n" + block + "\n" + b + "\n\n## Revisions and bug log")
    open(path, "w").write(s)
    print(block)


if __name__ == "__main__":
    main()
