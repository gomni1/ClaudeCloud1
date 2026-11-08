"""Harness H1-H3 and planted checks P1-P2 (SPEC §6). All must pass."""
import os, sys, json, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim_patches as SP
import measure as ME

SEED_BASE = 7_000_000
DT = 0.01
DT_REC = 0.2
TAU_F = 0.3


def _load():
    d = np.load(os.path.join(HERE, "deterministic.npz"))
    z = np.load(os.path.join(HERE, "graphs.npz"))
    c = np.load(os.path.join(HERE, "topo_cache.npz"))
    return d, z, c


def _site0(cyc, Om):
    f = cyc[0]
    C = int(round(f[0] * Om)); V = int(round(f[1] * Om)); L = int(round(f[2] * Om))
    return C, V, L, Om - C - V - L


def init_sites(cyc, N, Om, seed):
    """Each site at a uniformly random point of the deterministic cycle."""
    rng = np.random.default_rng(seed)
    fr = cyc[rng.integers(0, cyc.shape[0], N)]
    C = np.rint(fr[:, 0] * Om).astype(np.int64)
    V = np.rint(fr[:, 1] * Om).astype(np.int64)
    L = np.rint(fr[:, 2] * Om).astype(np.int64)
    return C, V, L, Om - C - V - L


def h2(n_periods=2000):
    """Tau-leap against exact Gillespie at one isolated site."""
    d, _, _ = _load()
    T = float(d['T'][0]); bal = d['balance']; s_c, s_v = d['s']
    cyc = d['cycle']
    tot = n_periods * T; burn = 30 * T
    nfr = int((tot - burn) / DT_REC)
    out = {}
    for Om in (200, 800):
        C, V, L, P = _site0(cyc, Om)
        ph = np.zeros(nfr)
        SP.seed_rng(np.int64(SEED_BASE + 10 + Om))
        n = SP.ssa_site(C, V, L, P, float(Om), SP.K, tot, DT_REC, burn,
                        TAU_F, bal[0], bal[1], s_c, s_v, ph)
        m_s, cv_s, k_s = ME.period_stats(ph[:n], DT_REC)
        C, V, L, P = _site0(cyc, Om)
        ph = np.zeros(nfr)
        SP.seed_rng(np.int64(SEED_BASE + 20 + Om))
        n = SP.leap_site(C, V, L, P, float(Om), SP.K, DT, int(round(tot / DT)),
                         int(round(DT_REC / DT)), int(round(burn / DT)),
                         TAU_F, bal[0], bal[1], s_c, s_v, ph)
        m_l, cv_l, k_l = ME.period_stats(ph[:n], DT_REC)
        e_m = abs(m_l - m_s) / m_s; e_c = abs(cv_l - cv_s) / cv_s
        out[Om] = dict(ssa_period=m_s, ssa_cv=cv_s, ssa_n=k_s,
                       leap_period=m_l, leap_cv=cv_l, leap_n=k_l,
                       err_period=e_m, err_cv=e_c, passed=bool(max(e_m, e_c) < 0.05))
    return dict(check="H2", per_Omega={str(k): v for k, v in out.items()},
                passed=all(v['passed'] for v in out.values()),
                ssa_period_800=out[800]['ssa_period'])


def h1_h3(ref_period_800, n_periods=200, burn_periods=30):
    """H1: median per-site period at w=0, Omega=800 against the H2 SSA period.
    H3: total winding over all faces of S is zero in every frame."""
    d, z, c = _load()
    T = float(d['T'][0]); bal = d['balance']; s_c, s_v = d['s']; cyc = d['cycle']
    ip, ix, tri = z['ip_s'], z['ix_s'], z['tri_s']
    N = len(ip) - 1
    nfr = int(round((n_periods - burn_periods) * T / DT_REC))
    ph = np.zeros((nfr, N), np.float32); am = np.zeros((nfr, N), np.float32)
    C, V, L, P = init_sites(cyc, N, 800, SEED_BASE + 31)
    SP.seed_rng(np.int64(SEED_BASE + 32))
    t0 = time.process_time()
    nf = SP.tau_leap(C, V, L, P, ip, ix, 800.0, 0.0, SP.K, DT,
                     int(round(n_periods * T / DT)), int(round(DT_REC / DT)),
                     int(round(burn_periods * T / DT)), TAU_F,
                     bal[0], bal[1], s_c, s_v, ph, am)
    cpu = time.process_time() - t0
    pers = np.array([ME.period_stats(ph[:nf, i], DT_REC)[0] for i in range(N)])
    med = float(np.nanmedian(pers))
    err = abs(med - ref_period_800) / ref_period_800
    w = np.zeros(tri.shape[0], np.int8)
    tot = np.empty(nf, np.int64)
    for f in range(nf):
        ME.windings(ph[f], tri, w)
        tot[f] = int(w.sum())
    H1 = dict(check="H1", median_site_period=med, reference=ref_period_800,
              err=err, n_sites=N, passed=bool(err < 0.05), cpu_s=cpu)
    H3 = dict(check="H3", n_frames=int(nf), max_abs_total_winding=int(np.abs(tot).max()),
              passed=bool(np.all(tot == 0)))
    return H1, H3, ph, am, nf


def p1():
    """Planted fields with windings known by construction."""
    rows = []
    tet = np.array([[0, 1, 2], [0, 2, 3], [0, 3, 1], [1, 3, 2]], np.int32)
    w = np.zeros(4, np.int8)
    # (b) the vortex field
    phv = np.array([0.0, 2 * np.pi / 3, 4 * np.pi / 3, 0.0])
    ME.windings(phv, tet, w)
    exp_b = np.array([1, 0, 0, -1], np.int8)
    rows.append(dict(case="tetrahedron vortex", got=w.tolist(),
                     expected=exp_b.tolist(), exact=bool(np.array_equal(w, exp_b))))
    # (a) constant, and a small-difference field on the frozen sphere
    _, z, _ = _load()
    tri = z['tri_s']; N = int(z['ip_s'].shape[0]) - 1
    ws = np.zeros(tri.shape[0], np.int8)
    ME.windings(np.zeros(N), tri, ws)
    rows.append(dict(case="constant field on S", got=int(np.abs(ws).sum()),
                     expected=0, exact=bool(np.all(ws == 0))))
    rng = np.random.default_rng(SEED_BASE + 41)
    small = rng.uniform(-np.pi / 3.1, np.pi / 3.1, N)   # all edge gaps < 2pi/3
    ME.windings(small, tri, ws)
    rows.append(dict(case="small-gap field on S", got=int(np.abs(ws).sum()),
                     expected=0, exact=bool(np.all(ws == 0))))
    return dict(check="P1", rows=rows, passed=all(r["exact"] for r in rows))


def p2(n_frames=400):
    """Independent uniform phases: defect density 1/4 and no long track."""
    _, z, c = _load()
    tri = z['tri_s']; N = int(z['ip_s'].shape[0]) - 1
    nbp, nbi = c['nbptr_s'], c['nbidx_s']
    rng = np.random.default_rng(SEED_BASE + 42)
    w = np.zeros(tri.shape[0], np.int8)
    dens = []
    tracker = ME.Tracker(keep_frames=10 ** 9)
    pos_of = np.full(tri.shape[0], -1, np.int32)
    prev = None
    for f in range(n_frames):
        ph = rng.uniform(-np.pi, np.pi, N)
        ME.windings(ph, tri, w)
        idx = np.where(w != 0)[0].astype(np.int32)
        sg = w[idx].astype(np.int8)
        dens.append(idx.size / tri.shape[0])
        amps = np.ones(idx.size)
        if prev is None:
            tracker.start(0, idx, sg, amps)
        else:
            pos_of[:] = -1
            pos_of[idx] = np.arange(idx.size, dtype=np.int32)
            mc = np.empty(prev[0].size, np.int32); mn = np.empty(idx.size, np.int32)
            ME.match_frames(prev[0], prev[1], idx, sg, nbp, nbi, pos_of, mc, mn)
            tracker.step(f - 1, prev[0], prev[1], idx, sg, amps, mc, mn)
        prev = (idx, sg)
    done = tracker.finish()
    longest = max(t['length'] for t in done)
    dens = float(np.mean(dens))
    need = 636
    return dict(check="P2", defect_density=dens, target=0.25,
                within_tolerance=bool(abs(dens - 0.25) <= 0.01),
                longest_track_frames=int(longest), frames_for_20_periods=need,
                passed=bool(abs(dens - 0.25) <= 0.01 and longest < need))


def main():
    t0 = time.process_time()
    H2 = h2()
    H1, H3, ph, am, nf = h1_h3(H2['ssa_period_800'])
    P1 = p1(); P2 = p2()
    out = [H1, H2, H3, P1, P2]
    cpu = time.process_time() - t0
    for r in out:
        r['_cpu_total_s'] = cpu
    json.dump(out, open(os.path.join(HERE, "harness.json"), "w"), indent=1)
    print("H1 %s median site period %.4f vs SSA %.4f (err %.2f%%)" %
          ("PASS" if H1['passed'] else "FAIL", H1['median_site_period'],
           H1['reference'], 100 * H1['err']))
    for Om, v in H2['per_Omega'].items():
        print("H2 Omega=%s %s period %.4f vs %.4f (%.2f%%)  CV %.4f vs %.4f (%.2f%%)" %
              (Om, "PASS" if v['passed'] else "FAIL", v['leap_period'], v['ssa_period'],
               100 * v['err_period'], v['leap_cv'], v['ssa_cv'], 100 * v['err_cv']))
    print("H3 %s  %d frames, max |total winding| = %d" %
          ("PASS" if H3['passed'] else "FAIL", H3['n_frames'], H3['max_abs_total_winding']))
    print("P1 %s  %s" % ("PASS" if P1['passed'] else "FAIL",
                         "; ".join(f"{r['case']}: {'exact' if r['exact'] else 'WRONG'}" for r in P1['rows'])))
    print("P2 %s  defect density %.4f (target 0.25), longest track %d frames (bar %d)" %
          ("PASS" if P2['passed'] else "FAIL", P2['defect_density'],
           P2['longest_track_frames'], P2['frames_for_20_periods']))
    print("ALL HARNESS PASS:", all(r['passed'] for r in out), " CPU %.1f s" % cpu)
    return out


if __name__ == "__main__":
    main()
