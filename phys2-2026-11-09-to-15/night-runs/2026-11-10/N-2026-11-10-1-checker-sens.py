import numpy as np
from scipy.special import betainc
from scipy.optimize import brentq
m,kr=10,6
base=np.array([0.4885,0.1976,13.992,7.024,8.293,2.092,1.267,4.986,0.3117,16.654])
half=np.array([5e-5,5e-5,5e-4,5e-4,5e-4,5e-4,5e-4,5e-4,5e-5,5e-4])
def F(x): return betainc(kr,m-kr+1,x)
def bal(k):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); D=k2+k7+k1*k5/(k5+k6)
    g=lambda v:(k10+k3*F(Cs/(Cs+Ls+Ps+v)))*v-D*Cs
    vs=np.logspace(-3,4,20001); gv=g(vs); idx=np.where(np.sign(gv[:-1])!=np.sign(gv[1:]))[0]
    out=[]
    for i in idx:
        v=brentq(g,vs[i],vs[i+1],xtol=1e-14)
        def f(x):
            c,vv,l,p=x;T=c+vv+l+p;r=k3*F(c/T)
            return np.array([-(k1+k2+k7)*c+k6*l+(k10+r)*vv,k2*c+k5*l+k8*p-(k10+r)*vv+k12,k1*c-(k5+k6)*l,k7*c-(k8+k9)*p])
        x0=np.array([Cs,v,Ls,Ps]);J=np.zeros((4,4))
        for j in range(4):
            h=1e-6*max(1,x0[j]);e=np.zeros(4);e[j]=h;J[:,j]=(f(x0+e)-f(x0-e))/(2*h)
        ev=np.linalg.eigvals(J); out.append((v,sorted(ev,key=lambda z:z.real)))
    return out
rng=np.random.default_rng(1);V=[];E=[]
for t in range(300):
    k=base+half*rng.uniform(-1,1,10); b=bal(k)
    if len(b)!=3: continue
    V.append([x[0] for x in b]); E.append([b[0][1][0].real,abs(b[0][1][1].imag),b[2][1][0].real])
V=np.array(V);E=np.array(E)
print('V* ranges',V.min(0),V.max(0))
print('low eig -15.25 range',E[:,0].min(),E[:,0].max(),' imag',E[:,1].min(),E[:,1].max(),' high -15.62',E[:,2].min(),E[:,2].max())
# frac hitting published simultaneously
hit=(np.round(V[:,1],3)==14.394)&(np.round(V[:,2],3)==79.747)&(np.round(E[:,0],3)==-15.248)&(np.round(E[:,2],3)==-15.623)&(np.round(E[:,1],3)==3.527)
print('frac reproducing all published roundings',hit.mean())
from scipy.optimize import minimize
tgt=np.array([2.589,14.394,79.747,-15.248,3.527,-15.623,-1.377])
def obj(u):
    k=base+half*np.tanh(u); b=bal(k)
    if len(b)!=3: return 1e3
    y=np.array([b[0][0],b[1][0],b[2][0],b[0][1][0].real,abs(b[0][1][1].imag),b[2][1][0].real,b[0][1][3].real])
    return np.sum(((y-tgt)/5e-4)**2)
best=None
for s in range(6):
    r=minimize(obj,rng.normal(0,.5,10),method='Nelder-Mead',options={'maxfev':1500})
    if best is None or r.fun<best.fun: best=r
k=base+half*np.tanh(best.x); b=bal(k)
print('best obj',best.fun); print([round(x[0],4) for x in b],[np.round(x[1],4) for x in b])
