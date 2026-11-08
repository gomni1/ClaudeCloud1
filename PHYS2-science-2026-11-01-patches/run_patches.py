"""Production runs: main grid on class S, comparison on R and C5 (SPEC §7, §9)."""
import os, sys, json, time
import numpy as np
from numba import njit

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sim_patches as SP
import measure as ME
from harness import init_sites, SEED_BASE, DT, DT_REC, TAU_F

N_PERIODS = 200
BURN_PERIODS = 30
KEY = {"S": "s", "R": "r", "C5": "c"}


@njit(cache=True)
def _tri_amp(amp, tri, out):
    for t in range(tri.shape[0]):
        out[t] = (amp[tri[t, 0]] + amp[tri[t, 1]] + amp[tri[t, 2]]) / 3.0
    return out


@njit(cache=True)
def _partner_frac(fr, tr, sg, fptr, tri, D, radius):
    """Fraction of events with an opposite-sign partner of the same kind within
    `radius` hops and one frame."""
    n = fr.shape[0]
    nF = fptr.shape[0] - 1
    good = 0
    for i in range(n):
        f = fr[i]
        found = False
        f0 = f - 1 if f > 0 else 0
        f1 = f + 1 if f + 1 < nF else nF - 1
        for g in range(f0, f1 + 1):
            for j in range(fptr[g], fptr[g + 1]):
                if j == i or sg[j] == sg[i]:
                    continue
                if ME.tri_hop(tri, D, tr[i], tr[j]) <= radius:
                    found = True
                    break
            if found:
                break
        if found:
            good += 1
    return good / n if n > 0 else np.nan


@njit(cache=True)
def _msd(traj, lengths, offsets, tri, D, max_lag, msd, cnt):
    for k in range(lengths.shape[0]):
        L = lengths[k]; o = offsets[k]
        for lag in range(1, max_lag + 1):
            if lag >= L:
                break
            for s in range(L - lag):
                h = ME.tri_hop(tri, D, traj[o + s], traj[o + s + lag])
                msd[lag] += h * h
                cnt[lag] += 1
    return 0


def run_one(graph, Omega, w, rep, seed, keep_periods=5.0):
    d = np.load(os.path.join(HERE, "deterministic.npz"))
    z = np.load(os.path.join(HERE, "graphs.npz"))
    c = np.load(os.path.join(HERE, "topo_cache.npz"))
    T = float(d['T'][0]); bal = d['balance']; s_c, s_v = d['s']; cyc = d['cycle']
    kk = KEY[graph]
    ip, ix, tri = z[f'ip_{kk}'], z[f'ix_{kk}'], z[f'tri_{kk}']
    D = c[f'D_{kk}']; nbp, nbi = c[f'nbptr_{kk}'], c[f'nbidx_{kk}']
    N = len(ip) - 1; nT = tri.shape[0]
    nfr = int(round((N_PERIODS - BURN_PERIODS) * T / DT_REC))
    frames_period = T / DT_REC

    phase = np.zeros((nfr, N), np.float32); amp = np.zeros((nfr, N), np.float32)
    C, V, L, P = init_sites(cyc, N, Omega, seed)
    SP.seed_rng(np.int64(seed + 1))
    t0 = time.process_time()
    nf = SP.tau_leap(C, V, L, P, ip, ix, float(Omega), float(w), SP.K, DT,
                     int(round(N_PERIODS * T / DT)), int(round(DT_REC / DT)),
                     int(round(BURN_PERIODS * T / DT)), TAU_F,
                     bal[0], bal[1], s_c, s_v, phase, amp)
    cpu_sim = time.process_time() - t0

    wv = np.zeros(nT, np.int8); ta = np.zeros(nT)
    pos_of = np.full(nT, -1, np.int32)
    R_t = np.zeros(nf); ndef_t = np.zeros(nf, np.int32); tot_w = np.zeros(nf, np.int64)
    tracker = ME.Tracker(keep_frames=int(keep_periods * frames_period))
    prev = None
    amp_sum = 0.0
    for f in range(nf):
        ME.windings(phase[f], tri, wv)
        _tri_amp(amp[f], tri, ta)
        amp_sum += ta.mean()
        R_t[f] = ME.synchrony(phase[f].astype(np.float64))
        idx = np.where(wv != 0)[0].astype(np.int32)
        sg = wv[idx].astype(np.int8)
        ndef_t[f] = idx.size; tot_w[f] = int(wv.sum())
        a_here = ta[idx]
        if prev is None:
            tracker.start(0, idx, sg, a_here)
        else:
            pos_of[:] = -1
            pos_of[idx] = np.arange(idx.size, dtype=np.int32)
            mc = np.empty(prev[0].size, np.int32); mn = np.empty(idx.size, np.int32)
            ME.match_frames(prev[0], prev[1], idx, sg, nbp, nbi, pos_of, mc, mn)
            tracker.step(f - 1, prev[0], prev[1], idx, sg, a_here, mc, mn)
        prev = (idx, sg)
    done = tracker.finish()
    baseline_amp = amp_sum / nf
    cpu_meas = time.process_time() - t0 - cpu_sim

    lens = np.array([t['length'] for t in done], np.int64)
    n5 = int(keep_periods * frames_period); n20 = int(round(20 * frames_period))
    sel5 = [t for t in done if t['length'] >= n5]
    d2_amp = (float(sum(t['amp'] for t in sel5) / sum(t['n'] for t in sel5))
              if sel5 else float('nan'))
    longest = int(lens.max()) if lens.size else 0

    # D3
    def ev_arrays(ev):
        if not ev:
            return (np.zeros(0, np.int64),) * 3 + (np.zeros(nf + 1, np.int64),)
        a = np.array(ev, np.int64)
        o = np.argsort(a[:, 0], kind='stable'); a = a[o]
        fptr = np.zeros(nf + 1, np.int64)
        np.add.at(fptr, a[:, 0] + 1, 1)
        return a[:, 0].copy(), a[:, 1].copy(), a[:, 2].copy(), np.cumsum(fptr)
    bf, bt, bs, bp = ev_arrays(tracker.births)
    df, dt_, ds, dp = ev_arrays(tracker.deaths)
    fb = float(_partner_frac(bf, bt, bs, bp, tri, D, 3)) if bf.size else float('nan')
    fd = float(_partner_frac(df, dt_, ds, dp, tri, D, 3)) if df.size else float('nan')

    # D4
    long_tracks = [t for t in done if t['length'] >= n20 and t.get('tri')]
    max_lag = 100
    msd = np.zeros(max_lag + 1); cnt = np.zeros(max_lag + 1, np.int64)
    if long_tracks:
        traj = np.concatenate([np.array(t['tri'], np.int32) for t in long_tracks])
        lengths = np.array([len(t['tri']) for t in long_tracks], np.int64)
        offs = np.concatenate([[0], np.cumsum(lengths)[:-1]]).astype(np.int64)
        _msd(traj, lengths, offs, tri, D, max_lag, msd, cnt)
    with np.errstate(invalid='ignore', divide='ignore'):
        msd_v = np.where(cnt > 0, msd / np.maximum(cnt, 1), np.nan)
    lag = np.arange(max_lag + 1)
    ok = (cnt > 0) & (msd_v > 0) & (lag > 0)
    expo = (float(np.polyfit(np.log(lag[ok]), np.log(msd_v[ok]), 1)[0])
            if ok.sum() >= 3 else float('nan'))

    return dict(graph=graph, Omega=int(Omega), w=float(w), rep=int(rep), seed=int(seed),
                N=int(N), n_triangles=int(nT), n_frames=int(nf),
                frames_per_period=float(frames_period),
                cpu_sim_s=cpu_sim, cpu_meas_s=cpu_meas,
                R_mean=float(R_t.mean()), R_last=float(R_t[-1]),
                R_t=R_t[::20].tolist(), ndef_t=ndef_t[::20].tolist(),
                defect_density_mean=float(ndef_t.mean() / nT),
                total_winding_max_abs=int(np.abs(tot_w).max()),
                n_tracks=int(lens.size), longest_track_frames=longest,
                longest_track_periods=float(longest / frames_period),
                n_tracks_ge_5periods=len(sel5), n_tracks_ge_20periods=len(long_tracks),
                d2_track_amp=d2_amp, baseline_tri_amp=float(baseline_amp),
                d2_ratio=float(d2_amp / baseline_amp) if sel5 else float('nan'),
                d3_birth_frac=fb, d3_death_frac=fd,
                n_births=int(bf.size), n_deaths=int(df.size),
                msd=msd_v[1:].tolist(), msd_counts=cnt[1:].tolist(), d4_exponent=expo,
                median_site_amp=float(np.median(amp.mean(axis=0))))


def _job(a):
    return run_one(*a)


def main(workers=8):
    jobs = []
    for Om in (200, 800):
        for w in (0.05, 0.2, 0.5):
            for rep in (0, 1):
                jobs.append(("S", Om, w, rep,
                             SEED_BASE + 100000 + 1000 * (Om == 800) + int(w * 1000) * 10 + rep))
    for g in ("R", "C5"):
        for w in (0.05, 0.2):
            jobs.append((g, 800, w, 0,
                         SEED_BASE + 200000 + 10000 * (g == "C5") + int(w * 1000)))
    from concurrent.futures import ProcessPoolExecutor
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=workers) as ex:
        res = list(ex.map(_job, jobs))
    json.dump(res, open(os.path.join(HERE, "production_patches.json"), "w"))
    print("wall %.1f s   cpu %.1f s" %
          (time.time() - t0, sum(r['cpu_sim_s'] + r['cpu_meas_s'] for r in res)))
    for r in res:
        print("%-3s Om=%3d w=%.2f rep=%d  R=%.3f  defdens=%.4f  longest=%.1f periods  "
              "tracks=%d  D2=%.3f D3b=%.2f D3d=%.2f  cpu=%.0f+%.0f" %
              (r['graph'], r['Omega'], r['w'], r['rep'], r['R_mean'],
               r['defect_density_mean'], r['longest_track_periods'], r['n_tracks'],
               r['d2_ratio'], r['d3_birth_frac'], r['d3_death_frac'],
               r['cpu_sim_s'], r['cpu_meas_s']))
    return res


if __name__ == "__main__":
    main()
