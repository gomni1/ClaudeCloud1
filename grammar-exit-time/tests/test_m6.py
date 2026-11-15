"""M6: exact master-equation MFPT against the simulator (SPEC §5)."""
import json
import math
import os

import numpy as np
import pytest

from gexit import master, model, sim

EV = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "evidence", "M6.json")


def test_master_solvers_agree():
    """Direct sparse LU and multigrid solves of the same truncated system agree."""
    n0 = model.start_counts("TH2", 2)
    caps = master.initial_caps(n0)
    d = master.mfpt_D("TH", 2, n0, caps, method="direct")
    a = master.mfpt_D("TH", 2, n0, caps, method="amg")
    assert d["residual"] <= 1e-10 and a["residual"] <= 1e-10
    assert a["T"] == pytest.approx(d["T"], rel=1e-9)


@pytest.mark.parametrize("start", ["MA", "TH2", "TH4"])
def test_simulator_matches_exact_on_moderate_lattice(start):
    """Omega = 2, second truncation level, against 2000 simulator runs (truncation effect < 1 SE here)."""
    om = 2
    n0 = model.start_counts(start, om)
    ex = master.mfpt_D(model.LAW_OF[start], om, n0, master.initial_caps(n0) * 2)
    tasks = [dict(model=model.LAW_OF[start], omega=om, n0=n0, target="D", t_burn=0.0, cap=1e9, nruns=250,
                  seed=sim.seed_for("test-M6", start, b)) for b in range(8)]
    t = np.concatenate([r["time"] for r in sim.map_batches(tasks)])
    se = t.std(ddof=1) / math.sqrt(len(t))
    assert abs(t.mean() - ex["T"]) <= 3 * se


@pytest.mark.skipif(not os.path.exists(EV), reason="run python run_all.py m6 first")
def test_recorded_m6_rows():
    rows = json.load(open(EV))["rows"]
    assert len(rows) == 9
    for r in rows:
        if r["converged"]:
            assert r["agree_3se"], r
            assert max(r["residuals"]) <= 1e-10
