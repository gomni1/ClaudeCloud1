exec(open('a.py').read().split('eqs=[]')[0])
eqs=np.load('eqs.npy')
lo,mid,hi=eqs
w,v=np.linalg.eig(J(lo)); u=v[:,np.argmax(w.real)]
starts={}
for s in [1,-1]:
    for nm,d in [('Re',u.real),('Im',u.imag)]:
        starts[f'lo{nm}{s:+d}']=lo*(1+0)+s*1e-4*np.linalg.norm(lo)*d/np.linalg.norm(d)
wm,vm=np.linalg.eig(J(mid)); um=vm[:,np.argmax(wm.real)].real
for s in [1,-1]: starts[f'mid{s:+d}']=mid+s*1e-4*np.linalg.norm(mid)*um
# large amplitude starts
rng=np.random.default_rng(1)
for i in range(6):
    starts[f'big{i}']=lo*np.exp(rng.uniform(-1.5,1.5,4))
starts['V0small']=np.array([Cs,1.0,Ls,Ps]); starts['Vlow60']=np.array([Cs,60,Ls,Ps]); starts['Vhi']=np.array([10,3000,10,5])
for k,y0 in starts.items():
    sol=solve_ivp(f,[0,2e5],y0,method='LSODA',rtol=1e-10,atol=1e-10,dense_output=True)
    t=sol.t; C=sol.y[0]
    up=np.where((C[:-1]<Cs)&(C[1:]>=Cs))[0]
    tup=t[up]
    for T in [2e4]:
        yT=sol.sol(T); dT=np.linalg.norm(yT-hi)/np.linalg.norm(hi)
    yE=sol.y[:,-1]
    dE=[np.linalg.norm(yE-e)/np.linalg.norm(e) for e in eqs]
    # late oscillation amplitude
    late=t>1e5; amp=np.ptp(C[late])
    print(f"{k:8s} ok={sol.success} ncross={len(up)} lastcross={tup[-1] if len(tup) else None:} d(2e4,hi)={dT:.4f} V(2e4)={yT[1]:.1f} dEnd={['%.2e'%x for x in dE]} lateC_ptp={amp:.2e}")
