# Copied from grammar-exit-time/gexit/ (PR 3, gomni1/ClaudeCloud1#3) for task grammar-idsize; changes are marked "idsize:".
"""Post-freeze supplementary check for M6 (not preregistered; logged in RESULTS.md).

For the cases the frozen rule leaves unconverged, refine the truncation one species at a
time: from the finest preregistered level, double each cap on its own; keep the doublings
that change the start-state MFPT by more than 0.1%; stop when no single-cap doubling
does, or when the lattice would exceed the preregistered 4e6-state limit."""
import json
import sys

import numpy as np

from . import master, model

SPECIES = ("C", "V", "L", "P")


def refine(law, om, n0, caps, rel=1e-3, log=print):
    caps = np.array(caps, int)
    base = master.mfpt_D(law, om, n0, caps)
    steps = [dict(caps=caps.tolist(), T=base["T"], states=base["states"], residual=base["residual"])]
    log("  supp %s Omega=%d caps=%s T=%.8g" % (law, om, caps.tolist(), base["T"]))
    T = base["T"]
    for _ in range(12):
        changes = {}
        for s in range(4):
            c = caps.copy()
            c[s] *= 2
            if np.prod(c + 1) > master.MAX_STATES:
                changes[SPECIES[s]] = None
                continue
            r = master.mfpt_D(law, om, n0, c)
            changes[SPECIES[s]] = (r["T"] - T) / T
            steps.append(dict(caps=c.tolist(), T=r["T"], states=r["states"], residual=r["residual"],
                              probe=SPECIES[s]))
            log("  supp %s Omega=%d probe %s caps=%s T=%.8g change=%+.2e" % (law, om, SPECIES[s], c.tolist(),
                                                                          r["T"], changes[SPECIES[s]]))
        big = [s for s in range(4) if changes[SPECIES[s]] is not None and abs(changes[SPECIES[s]]) > rel]
        blocked = [SPECIES[s] for s in range(4) if changes[SPECIES[s]] is None]
        if not big:
            return dict(converged=not blocked, blocked=blocked, T=T, caps=caps.tolist(), steps=steps,
                        last_changes=changes)
        for s in big:
            caps[s] *= 2
        if np.prod(caps + 1) > master.MAX_STATES:
            return dict(converged=False, blocked=["joint"], T=T, caps=caps.tolist(), steps=steps,
                        last_changes=changes)
        r = master.mfpt_D(law, om, n0, caps)
        T = r["T"]
        steps.append(dict(caps=caps.tolist(), T=T, states=r["states"], residual=r["residual"]))
        log("  supp %s Omega=%d joint caps=%s T=%.8g" % (law, om, caps.tolist(), T))
    return dict(converged=False, blocked=["iterations"], T=T, caps=caps.tolist(), steps=steps)


if __name__ == "__main__":
    exact = json.load(open(sys.argv[1]))
    only = sys.argv[3].split(",") if len(sys.argv) > 3 else None
    out = []
    for e in exact:
        if e["converged"] or (only and e["start"] not in only):
            continue
        start, om = e["start"], e["Omega"]
        n0 = model.start_counts(start, om)
        r = refine(model.LAW_OF[start], om, n0, e["levels"][-1]["caps"])
        r.update(start=start, Omega=om)
        out.append(r)
        print(start, om, r["converged"], r["T"], r["caps"], flush=True)
        json.dump(out, open(sys.argv[2], "w"), indent=1)
