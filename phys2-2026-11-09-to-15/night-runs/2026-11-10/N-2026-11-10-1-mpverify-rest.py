# Re-verify the outer-unstable flags not stored in outer_cases (output capped at 200) by replaying the seeded draw sequence.
import json, numpy as np, importlib.util, sys
spec=importlib.util.spec_from_file_location("h","N-2026-11-10-1-num.py"); h=importlib.util.module_from_spec(spec); spec.loader.exec_module(h)
from importlib import import_module
mv=importlib.util.spec_from_file_location("mv","N-2026-11-10-1-mpverify.py"); M=importlib.util.module_from_spec(mv); mv.loader.exec_module(M)
import mpmath as mp
out=json.load(open('N-2026-11-10-1-num-output.json')); stored={c['i'] for c in out['outer_cases']}
per=json.load(open('N-2026-11-10-1-num-output-perdraw.json'))
want={r['i']:r for r in per if (r['maxre'][0]>0 or r['maxre'][2]>0) and r['i'] not in stored}
rng=np.random.default_rng(h.RNG_SEED); n=0; ok=0
while want and n<max(want):
    k,m,kr=h.draw(rng); n+=1
    if n in want:
        r=want[n]; assert (m,kr)==(r['m'],r['kr'])
        j=0 if r['maxre'][0]>0 else 2
        v=M.verify(k,m,kr,r['V'][j]); good=v['maxre']>0 and v['res']<mp.mpf('1e-30'); ok+=good
        print("draw",n,"m",m,"kr",kr,"V*",mp.nstr(v['V'],10),"maxRe",mp.nstr(v['maxre'],8),"verified" if good else "NOT verified")
print("remaining verified:",ok,"of",len(want))
