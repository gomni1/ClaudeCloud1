"""Task C pipeline: for each target in priority order -> build, #print axioms, comparator, scan.

Runs from /home/user/leanwork/math/lean without modifying the release.  Logs and JSON records go to
/home/user/leanwork/logs/<Name>/.  Usage: python c_pipeline.py Name [Name ...]"""
import json
import os
import re
import resource
import shutil
import subprocess
import sys
import time

LEAN = "/home/user/leanwork/math/lean"
LOGS = "/home/user/leanwork/logs"
PROBE = "/home/user/leanwork/probe"
TOOLS = "/home/user/leanwork/tools/bin"
BUDGET_CPU = 10 * 3600.0
ENV = dict(os.environ)
ENV["PATH"] = TOOLS + ":" + os.path.expanduser("~/.elan/bin") + ":" + ENV["PATH"]
ENV["GLIBC_TUNABLES"] = "glibc.malloc.mmap_max=0:glibc.malloc.arena_max=1"
ENV["LEAN_NUM_THREADS"] = "2"
TASKSET = ["taskset", "-c", "0,1"]


def run(cmd, log, timeout=None):
    t0 = time.time()
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    with open(log, "ab") as f:
        f.write(("$ %s\n[start %s]\n" % (" ".join(cmd), time.strftime("%Y-%m-%d %H:%M:%S"))).encode())
        f.flush()
        try:
            p = subprocess.run(TASKSET + cmd, cwd=LEAN, env=ENV, stdout=f, stderr=subprocess.STDOUT, timeout=timeout)
            rc = p.returncode
        except subprocess.TimeoutExpired:
            rc = "timeout"
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    cpu = (r1.ru_utime - r0.ru_utime) + (r1.ru_stime - r0.ru_stime)
    return dict(cmd=cmd, returncode=rc, wall_s=time.time() - t0, cpu_s=cpu)


def spent_cpu():
    tot = 0.0
    for root, _, files in os.walk(LOGS):
        for fn in files:
            if fn.endswith(".rec.json") or fn == "build_MassAction.json":
                try:
                    d = json.load(open(os.path.join(root, fn)))
                    for k, v in d.items() if isinstance(d, dict) and "cmd" not in d else [("x", d)]:
                        if isinstance(v, dict) and "cpu_s" in v:
                            tot += v["cpu_s"]
                except Exception:
                    pass
    return tot


def import_closure(module):
    """Modules reachable by imports whose files live under OAI/ or ComparatorChallenges/."""
    seen, stack = set(), [module]
    while stack:
        m = stack.pop()
        if m in seen:
            continue
        path = os.path.join(LEAN, *m.split(".")) + ".lean"
        if not os.path.exists(path):
            continue
        if not (m.startswith("OAI.") or m.startswith("ComparatorChallenges.")):
            continue
        seen.add(m)
        for line in open(path, encoding="utf-8"):
            mm = re.match(r"^\s*(?:public\s+)?(?:meta\s+)?import\s+(.+)$", line)
            if mm:
                for tok in mm.group(1).split():
                    stack.append(tok.strip())
    return sorted(seen)


PATTERNS = {
    "sorry": r"\bsorry\b",
    "admit": r"\badmit\b",
    "axiom_decl": r"^\s*(?:@\[[^\]]*\]\s*)?(?:(?:private|protected|noncomputable|unsafe|partial)\s+)*axiom\s",
    "implemented_by": r"@\[\s*implemented_by|implemented_by\b",
    "unsafe": r"\bunsafe\b",
    "native_decide": r"\bnative_decide\b",
}


def strip_comments(src):
    out, i, depth, n = [], 0, 0, len(src)
    while i < n:
        if depth == 0 and src.startswith("--", i):
            j = src.find("\n", i)
            i = n if j < 0 else j
            continue
        if src.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth > 0 and src.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth == 0:
            out.append(src[i])
        elif src[i] == "\n":
            out.append("\n")
        i += 1
    return "".join(out)


def scan(modules, challenge_module):
    res = {}
    for m in modules:
        path = os.path.join(LEAN, *m.split(".")) + ".lean"
        src = strip_comments(open(path, encoding="utf-8").read())
        hits = {}
        for name, pat in PATTERNS.items():
            lines = [i + 1 for i, l in enumerate(src.split("\n")) if re.search(pat, l)]
            if lines:
                hits[name] = lines
        if hits:
            res[m] = hits
    outside = {m: h for m, h in res.items() if m != challenge_module}
    return dict(n_files=len(modules), hits=res, hits_outside_challenge=outside)


def process(name):
    cfg_path = os.path.join(LEAN, "ComparatorChallenges", name + ".json")
    cfg = json.load(open(cfg_path))
    d = os.path.join(LOGS, name)
    os.makedirs(d, exist_ok=True)
    rec = dict(name=name, config=cfg)
    sol, chal = cfg["solution_module"], cfg["challenge_module"]
    # (2) build the solution module
    if spent_cpu() > BUDGET_CPU:
        rec["verdict_hint"] = "underdetermined: budget"
        json.dump(rec, open(os.path.join(d, "record.json"), "w"), indent=1)
        return rec
    rec["build"] = run(["lake", "build", sol], os.path.join(d, "build.log"))
    json.dump(dict(build=rec["build"]), open(os.path.join(d, "build.rec.json"), "w"), indent=1)
    # (3) #print axioms
    os.makedirs(PROBE, exist_ok=True)
    pf = os.path.join(PROBE, "axioms_%s.lean" % name)
    with open(pf, "w") as f:
        f.write("import %s\n" % sol)
        for t in cfg["theorem_names"]:
            f.write("#print axioms %s\n" % t)
    rec["axioms_run"] = run(["lake", "env", "lean", pf], os.path.join(d, "axioms.log"))
    txt = open(os.path.join(d, "axioms.log"), encoding="utf-8", errors="replace").read()
    rec["axioms_output"] = txt[txt.rfind("[start"):][:20000]
    # (4) comparator: remove the solution-side and challenge build outputs first so that comparator
    # rebuilds them inside its sandbox (its trust assumption 2); Mathlib and other packages are kept.
    removed = []
    for top in ("OAI", "ComparatorChallenges"):
        for sub in ("lib/lean", "ir"):
            p = os.path.join(LEAN, ".lake", "build", sub, top)
            if os.path.isdir(p):
                shutil.rmtree(p)
                removed.append(p)
    rec["comparator_removed_build_dirs"] = removed
    rec["comparator"] = run(["lake", "env", "comparator", "ComparatorChallenges/%s.json" % name],
                            os.path.join(d, "comparator.log"), timeout=6 * 3600)
    txt = open(os.path.join(d, "comparator.log"), encoding="utf-8", errors="replace").read()
    rec["comparator_tail"] = txt[-6000:]
    # (5) scan of the import closure under OAI/ and ComparatorChallenges/
    mods = import_closure(sol)
    if chal not in mods:
        mods = sorted(set(mods) | set(import_closure(chal)))
    rec["scan"] = scan(mods, chal)
    json.dump(dict(build=rec["build"], axioms=rec["axioms_run"], comparator=rec["comparator"]),
              open(os.path.join(d, "steps.rec.json"), "w"), indent=1)
    json.dump(rec, open(os.path.join(d, "record.json"), "w"), indent=1)
    return rec


if __name__ == "__main__":
    for nm in sys.argv[1:]:
        r = process(nm)
        print(nm, json.dumps({k: r.get(k) for k in ("build", "axioms_run", "comparator")}), flush=True)
