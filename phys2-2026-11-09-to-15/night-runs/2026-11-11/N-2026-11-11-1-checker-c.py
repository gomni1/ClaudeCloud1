exec(open('a.py').read().split('eqs=[]')[0])
eqs=np.load('eqs.npy'); lo,mid,hi=eqs
rng=np.random.default_rng(7); bad=0; N=60
for i in range(N):
    y0=np.array([rng.uniform(0,200),10**rng.uniform(-1,3.7),rng.uniform(0,400),rng.uniform(0,60)])
    sol=solve_ivp(f,[0,5e4],y0,method='LSODA',rtol=1e-9,atol=1e-9)
    t=sol.t;C=sol.y[0]; late=t>2.5e4
    dC=np.diff(C[late]); signchg=np.sum(np.diff(np.sign(dC))!=0)
    d=np.linalg.norm(sol.y[:,-1]-hi)/np.linalg.norm(hi)
    if d>0.05 or signchg>2: bad+=1; print(i,y0,d,signchg)
print("anomalous",bad,"of",N)
# slow approach: residual time series along slow eigvec for loRe start
w,v=np.linalg.eig(J(lo)); u=v[:,np.argmax(w.real)].real
y0=lo+1e-4*np.linalg.norm(lo)*u/np.linalg.norm(u)
sol=solve_ivp(f,[0,2e5],y0,method='LSODA',rtol=1e-10,atol=1e-10,dense_output=True)
for T in [10,20,50,100,1e3,1e4,2e4,5e4,1e5]:
    y=sol.sol(T); print(T, np.round(y,3), '%.3e'%(np.linalg.norm(y-hi)/np.linalg.norm(hi)))
# total T and slow mode: T* dynamics
