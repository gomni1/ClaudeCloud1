# N-2026-11-12-1: summary table of the pre-listed common-feature quantities, from the per-draw outputs.
import json, numpy as np
DR=[2045,301417,384616,456280,616482]; out={}
for n in DR:
    d=json.load(open('N-2026-11-12-1-draw-%d-output.json'%n)); k1,k2,k3,k5,k6,k7,k8,k10=d['k']
    st=d['starts']; v={nm:(s['verdict'],s.get('p'),s.get('period'),len(s['rounds'])) for nm,s in st.items()}
    per=[s['period'] for s in st.values() if s['verdict']=='steady cycle']
    mn=np.array([s['measure']['mn'] for s in st.values() if 'measure' in s]); mx=np.array([s['measure']['mx'] for s in st.values() if 'measure' in s])
    fa=[s['measure']['frac_above'] for s in st.values() if 'measure' in s]
    Th=float(np.mean(per)); fl=d['floquet']
    def typ(e):
        e=[complex(*z) for z in e]; nu=sum(1 for z in e if z.real>0); cx=any(abs(z.imag)>0 for z in e)
        return '%d unstable, %s'%(nu,'complex pair' if cx else 'all real')
    out[n]=dict(m=d['m'],kr=d['kr'],kr_over_m=d['kr']/d['m'],k=dict(k1=k1,k2=k2,k3=k3,k5=k5,k6=k6,k7=k7,k8=k8,k10=k10),c=d['c'],D=d['D'],
        x_balances=d['roots'],balance_types=[typ(e) for e in d['balance_eigs']],balance_eigs=d['balance_eigs'],
        ratios={'k8/(k5+k6)':k8/(k5+k6),'k1/(k5+k6)':k1/(k5+k6),'k7/k8':k7/k8,'k3/k10':k3/k10},
        tau=d['tau'],verdicts=v,all_cycle=all(x[0]=='steady cycle' for x in v.values()),
        period=Th,period_spread_rel=float((max(per)-min(per))/Th),
        Theta_times={'k5+k6':Th*(k5+k6),'k8':Th*k8,'k10':Th*k10},
        swing_min=mn.mean(0).tolist(),swing_max=mx.mean(0).tolist(),swing_spread=float(max(np.ptp(mn,0).max(),np.ptp(mx,0).max())),
        frac_C_above_section=float(np.mean(fa)),floquet_logs=fl['logs'],floquet_logs_over_Theta=[l/Th for l in fl['logs']],
        floquet_checks=dict(trivial_ok=fl['trivial_ok'],conv_ok=fl['conv_ok'],trace_ok=fl['trace_ok'],trace_relerr=fl['trace_relerr'],nseg=fl['nseg']),
        detect_limit_period=100*d['tau']/14, seconds=sum(s['seconds'] for s in st.values())+fl['seconds'])
json.dump(out,open('N-2026-11-12-1-summary.json','w'),indent=1)
for n in DR:
    o=out[n]; print('== draw',n,'m',o['m'],'kr',o['kr'],'kr/m %.3f'%o['kr_over_m'])
    print('  k:',{a:float('%.5g'%b) for a,b in o['k'].items()},'c %.4g D %.4g'%(o['c'],o['D']))
    print('  x*:',['%.5f'%x for x in o['x_balances']],o['balance_types'])
    print('  ratios:',{a:float('%.4g'%b) for a,b in o['ratios'].items()},'tau %.4g'%o['tau'])
    print('  verdicts:',set(x[0] for x in o['verdicts'].values()),'p',set(x[1] for x in o['verdicts'].values()),'rounds',set(x[3] for x in o['verdicts'].values()),'n starts',len(o['verdicts']))
    print('  period %.8f spread %.1e ; Theta*(k5+k6) %.4g Theta*k8 %.4g Theta*k10 %.4g'%(o['period'],o['period_spread_rel'],*o['Theta_times'].values()))
    print('  swing C,V,L,P min',['%.4f'%x for x in o['swing_min']],'max',['%.4f'%x for x in o['swing_max']],'spread %.1e'%o['swing_spread'],'fracC>sec %.3f'%o['frac_C_above_section'])
    print('  floquet logs',['%.6f'%x for x in o['floquet_logs']],'per time',['%.4f'%x for x in o['floquet_logs_over_Theta']],o['floquet_checks'],'detect limit %.0f'%o['detect_limit_period'],'secs %.0f'%o['seconds'])
