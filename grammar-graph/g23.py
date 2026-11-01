"""G2 (class S, SPEC section 6) and G3 (classes K, R, C0, C5, SPEC section 7).
Usage: python g23.py g2 | g3.  Per-run evidence in evidence/g2/, evidence/g3/."""
import json
import math
import os
import sys
from multiprocessing import Pool

import numpy as np

from gg.core import (EVID, F_WIN0, LAMS, LONG, NFRAMES, T0, T_RUN, DT_FRAME, cpu_s, graph_C, graph_R, graph_S,
                     graph_stats, long_tracks, pairing, refs, run_graph, run_lumped, seed_of, summarize, track,
                     triangles)

N = 10000


def save_run(path, g, run, tr, extra):
    """Summary JSON + compressed per-frame series."""
    life_frames = (tr["end"] - tr["start"]) if tr is not None else np.zeros(0, int)
    hist_edges = [0, 1, 2, 5, 10, 25, 50, 100, 200, 318, 500, 1000, 4000]
    extra["track_life_hist_frames"] = dict(edges=hist_edges,
                                           counts=np.histogram(life_frames, bins=hist_edges)[0].tolist())
    json.dump(extra, open(path + ".json", "w"), indent=1)
    arrs = dict(gcount=run["gcount"].astype(np.int16))
    if "fstat" in run:
        arrs.update(R=run["fstat"][:, 0].astype(np.float32), ndef=run["fstat"][:, 4].astype(np.int32))
    if "snap" in run:
        arrs.update(snap=run["snap"], snapf=run["snapf"])
    np.savez_compressed(path + ".npz", **arrs)


def analyse(g, run, lam):
    s = summarize(g, run, lam)
    tr = track(g, run)
    s["n_tracks"] = int(len(tr["start"]))
    s["longest"] = float(tr["life"].max()) if len(tr["life"]) else 0.0
    s["n_long"] = int((tr["life"] >= LONG - 1e-9).sum())
    s["pairing"] = pairing(g, run, tr)
    s["long_tracks"] = long_tracks(g, run, tr)
    reps = [x["replacement"] for x in s["long_tracks"] if x["replacement"] is not None]
    s["replacement_mean"] = float(np.mean(reps)) if reps else None
    return s, tr


def g2_rep(rep):
    c0 = cpu_s()
    os.makedirs(os.path.join(EVID, "g2"), exist_ok=True)
    g = graph_S(N, seed_of("S", rep))
    gs = graph_stats(g)
    gs.update(flips_accepted=g["flips_accepted"], flips_tried=g["flips_tried"], triangles=int(len(g["tri"])))
    json.dump(gs, open(os.path.join(EVID, "g2", f"graph_S_r{rep}.json"), "w"), indent=1)
    for li, lam in enumerate(LAMS):
        snaps = list(range(F_WIN0, NFRAMES, 400)) if rep == 0 else []
        run = run_graph(g, lam, seed_of("G2", li, rep), chg=True, snaps=snaps)
        s, tr = analyse(g, run, lam)
        s.update(lam=lam, rep=rep, cls="S", refs=list(refs(lam)))
        save_run(os.path.join(EVID, "g2", f"S_r{rep}_lam{li}"), g, run, tr, s)
        print(f"G2 rep {rep} lam {lam}: A={s['A']:.3f} R={s['Rbar']:.3f} dens={s['density']:.4f} "
              f"longest={s['longest']:.1f} nlong={s['n_long']} cpu={cpu_s() - c0:.0f}", flush=True)
    return cpu_s() - c0


def g3_job(job):
    cls, rep = job
    c0 = cpu_s()
    os.makedirs(os.path.join(EVID, "g3"), exist_ok=True)
    lam = 0.0
    if cls == "K":
        X, ev = run_lumped(N, lam, seed_of("G3", cls, rep), T_RUN, DT_FRAME)
        cs, vs, sc, sv = refs(lam)
        gc = X[F_WIN0:] / N
        s = dict(cls="K", rep=rep, A=float(gc[:, 0].std() / sc), Rbar=1.0, mean_c=float(gc[:, 0].mean()),
                 mean_v=float(gc[:, 1].mean()), density=0.0, ntri=math.comb(N, 3), longest=0.0, n_long=0,
                 events=ev, note="all local fields coincide (radius-2 ball = whole graph): phases equal, "
                                 "every winding 0, Rbar = 1 by construction")
        if rep == 0:
            s["graph"] = dict(N=N, mean_degree=N - 1, clustering=1.0, diameter=1, d_g=None)
        json.dump(s, open(os.path.join(EVID, "g3", f"K_r{rep}.json"), "w"), indent=1)
        np.savez_compressed(os.path.join(EVID, "g3", f"K_r{rep}.npz"), gcount=X.astype(np.int16))
    else:
        if cls == "R":
            g = graph_R(N, 8, seed_of("R", rep))
        else:
            g = graph_C(N, 4, 0.0 if cls == "C0" else 0.05, seed_of(cls, rep), cls)
        gs = graph_stats(g)
        gs["triangles"] = int(len(triangles(g)))
        run = run_graph(g, lam, seed_of("G3", cls, rep), chg=True)
        s, tr = analyse(g, run, lam)
        s.update(cls=cls, rep=rep, graph=gs)
        save_run(os.path.join(EVID, "g3", f"{cls}_r{rep}"), g, run, tr, s)
    print(f"G3 {cls} rep {rep}: A={s['A']:.3f} R={s['Rbar']:.3f} dens={s['density']:.4f} longest={s['longest']:.1f} "
          f"cpu={cpu_s() - c0:.0f}", flush=True)
    return cpu_s() - c0


if __name__ == "__main__":
    part = sys.argv[1]
    c0 = cpu_s()
    if part == "g2":
        with Pool(3) as p:
            cpus = p.map(g2_rep, [0, 1, 2])
    else:
        jobs = [(c, r) for c in ("R", "C0", "C5", "K") for r in (0, 1)]
        with Pool(4) as p:
            cpus = p.map(g3_job, jobs)
    tot = sum(cpus) + (cpu_s() - c0)
    json.dump(dict(part=part, cpu_s_workers=cpus, cpu_s_total=tot), open(os.path.join(EVID, f"{part}_cpu.json"), "w"))
    print(part, "done; CPU s", tot)
