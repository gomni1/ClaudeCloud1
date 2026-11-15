"""Run every exact check and construction; write evidence/results.json.

Usage: python run_all.py
"""
import hashlib
import json
import pathlib
import platform
import time

import numpy as np
import sympy

from strata import experiments as E
from strata import experiments_h34 as F
from strata import proofs
from strata.loops import h1b_homotopy_M5, passage_loop, path_up
from strata.orientation import theta_M, theta_P, theta_R, winding

HERE = pathlib.Path(__file__).parent


def convergence():
    """Windings of representative loops at two sampling densities."""
    s_B = np.array([0.15, 0, 0.04 * np.exp(0.7j), 0])
    u = np.array([0, 0.06, 0, 0.03 * np.exp(1.1j)])
    loops = {"h1b_s=0.75": h1b_homotopy_M5(0.75), "h1b_s=1.5": h1b_homotopy_M5(1.5),
             "aba_up_M5": passage_loop(s_B, u, F.ABA_WINDOWS, [0.5], path=path_up)}
    out = {}
    for name, g in loops.items():
        for mname, th in (("theta_P", theta_P), ("theta_R", theta_R), ("theta_M", theta_M)):
            out[f"{name}/{mname}"] = [round(winding(th, g, n)[0], 9) for n in (128, 1024)]
    return out


def main():
    spec_hash = hashlib.sha256((HERE / "SPEC.md").read_bytes()).hexdigest()
    started = time.time()
    record = {
        "spec_sha256": spec_hash,
        "versions": {"python": platform.python_version(), "numpy": np.__version__,
                     "sympy": sympy.__version__},
        "exact": [{"name": n, "passed": bool(ok), "detail": d} for n, ok, d in proofs.run_all()],
        "H0": E.h0(),
        "H1a": E.h1a(),
        "H1b_M5": E.h1b_m5(),
        "H1b_M3": E.h1b_m3(),
        "H2a": E.h2a(),
        "H2b_M3": E.h2b_m3(),
        "H2c": E.h2c(),
        "H3": F.h3(),
        "H3_redistribution": F.h3_redistribution(),
        "H4a_rigid": F.h4a_rigid(),
        "H4a_one_odd_M3": F.h4a_one_odd(),
        "H4a_two_odd_M5": F.h4a_two_odd(),
        "H4b": F.h4b(),
        "sampling_convergence": convergence(),
    }
    record["runtime_s"] = round(time.time() - started, 1)
    out = HERE / "evidence" / "results.json"
    out.write_text(json.dumps(record, indent=1, default=str), encoding="utf-8")
    print(f"SPEC sha256 {spec_hash}")
    print(f"exact checks passed: {sum(e['passed'] for e in record['exact'])}/{len(record['exact'])}")
    print("H3 survivors (attribution S):",
          [k for k, v in record["H3"].items() if v["survive_S"]])
    print("H3 survivors (attribution R):",
          [k for k, v in record["H3"].items() if v["survive_R"]])
    print(f"wrote {out} in {record['runtime_s']} s")


if __name__ == "__main__":
    main()
