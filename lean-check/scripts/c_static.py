"""Task C, steps that need no build: (1) configs, (5) source scan of the OAI/ and ComparatorChallenges/ import
closure, the external imports of that closure, family 229's configs, the formalization.yaml entry for 149, and
the state of family 149 at the 12 Oct commit.  Reads the release only; writes logs/static/static.json."""
import json
import os
import re
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_pipeline import LEAN, import_closure, scan, strip_comments, PATTERNS  # noqa: E402

REPO = os.path.dirname(LEAN)
TARGETS = [("149", "MassAction"), ("131", "SwitchChain"), ("186", "SharpThreshold"), ("176", "SecondKahnKalai"),
           ("220", "DirectionalBallisticity"), ("229", "ThreeStateSupercritical"), ("229", "ThreeStateTreeClauses")]


def external_imports(mods):
    ext = set()
    for m in mods:
        for line in open(os.path.join(LEAN, *m.split(".")) + ".lean", encoding="utf-8"):
            mm = re.match(r"^\s*(?:public\s+)?(?:meta\s+)?import\s+(.+)$", line)
            if mm:
                for tok in mm.group(1).split():
                    if not (tok.startswith("OAI.") or tok.startswith("ComparatorChallenges.")):
                        ext.add(tok)
    return sorted(ext)


def git(*a):
    return subprocess.run(["git", "-C", REPO] + list(a), capture_output=True, text=True).stdout


out = dict(release_commit=git("rev-parse", "HEAD").strip(), targets=[])
for fam, name in TARGETS:
    cfg = json.load(open(os.path.join(LEAN, "ComparatorChallenges", name + ".json")))
    sol, chal = cfg["solution_module"], cfg["challenge_module"]
    mods = sorted(set(import_closure(sol)) | set(import_closure(chal)))
    lines = sum(sum(1 for _ in open(os.path.join(LEAN, *m.split(".")) + ".lean", encoding="utf-8")) for m in mods)
    sc = scan(mods, chal)
    counts = {p: sum(len(h.get(p, [])) for h in sc["hits"].values()) for p in PATTERNS}
    ext = external_imports(mods)
    out["targets"].append(dict(family=fam, name=name, config=cfg, n_files=len(mods), n_lines=lines,
                               solution_in_closure=sol in mods, challenge_in_closure=chal in mods,
                               external_imports=ext, imports_all_of_mathlib="Mathlib" in ext,
                               scan_counts=counts, scan_hits=sc["hits"],
                               hits_outside_challenge=sc["hits_outside_challenge"]))
# family 229: every config named in docs/229.md
doc = open(os.path.join(LEAN, "docs", "229.md"), encoding="utf-8").read()
out["family_229_configs"] = re.findall(r"ComparatorChallenges/(\w+)\.lean", doc)
# formalization.yaml: entries mentioning MassAction or the 149 papers
y = open(os.path.join(LEAN, "formalization.yaml"), encoding="utf-8").read().split("\n")
hits = [i for i, l in enumerate(y) if re.search(r"MassAction|mass-action|Mass-Action|Problem326", l)]
out["formalization_yaml_149"] = [dict(line=i + 1, text=y[i]) for i in hits]
blocks = []
for i in hits:
    s = i
    while s > 0 and not re.match(r"^  - ", y[s]):
        s -= 1
    blocks.append("\n".join(y[s:s + 25]))
out["formalization_yaml_149_blocks"] = sorted(set(blocks))
# family 149 over the release history
hist = []
for c in git("log", "--format=%H %ad", "--date=short").split("\n"):
    if not c:
        continue
    h, date = c.split()
    tree = git("ls-tree", "-r", "--name-only", h, "lean/OAI/Analysis/MassAction", "lean/ComparatorChallenges")
    files = [f for f in tree.split("\n") if f.startswith("lean/OAI/Analysis/MassAction/")]
    has_cfg = "lean/ComparatorChallenges/MassAction.json" in tree
    n_sorry = 0
    sorry_files = []
    for f in files:
        src = strip_comments(git("show", "%s:%s" % (h, f)))
        k = len(re.findall(r"\bsorry\b", src))
        if k:
            n_sorry += k
            sorry_files.append(f)
    yml = git("show", "%s:lean/formalization.yaml" % h)
    hist.append(dict(commit=h[:9], date=date, massaction_files=len(files), comparator_config=has_cfg,
                     sorry_count=n_sorry, sorry_files=sorry_files,
                     docs_149=bool(git("ls-tree", h, "lean/docs/149.md").strip()),
                     yaml_mentions_massaction=bool(re.search(r"MassAction", yml))))
out["family_149_history"] = hist
json.dump(out, open("/home/user/leanwork/logs/static/static.json", "w"), indent=1)
for t in out["targets"]:
    print(t["family"], t["name"], t["n_files"], t["n_lines"], "ext", t["external_imports"][:6], t["scan_counts"],
          "outside", {m: list(h) for m, h in t["hits_outside_challenge"].items()})
print("229 configs", out["family_229_configs"])
print("yaml 149", out["formalization_yaml_149"])
for h in hist:
    print(h)
