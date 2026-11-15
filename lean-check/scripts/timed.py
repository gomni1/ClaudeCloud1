"""Run a command, stream its output to a log, and record wall and CPU time (self + children)."""
import json, os, resource, subprocess, sys, time
out_json, log = sys.argv[1], sys.argv[2]
cmd = sys.argv[3:]
t0 = time.time()
with open(log, "ab") as f:
    f.write(("$ %s\n[start %s]\n" % (" ".join(cmd), time.strftime("%Y-%m-%d %H:%M:%S"))).encode())
    f.flush()
    p = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
ru = resource.getrusage(resource.RUSAGE_CHILDREN)
rec = dict(cmd=cmd, returncode=p.returncode, wall_s=time.time() - t0, cpu_user_s=ru.ru_utime, cpu_sys_s=ru.ru_stime,
           cpu_s=ru.ru_utime + ru.ru_stime, maxrss_kb=ru.ru_maxrss, end=time.strftime("%Y-%m-%d %H:%M:%S"))
json.dump(rec, open(out_json, "w"), indent=1)
print(json.dumps(rec))
