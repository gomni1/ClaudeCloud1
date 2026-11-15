import numpy as np, sys
from scipy.stats import binom
from scipy.optimize import brentq
rng=np.random.default_rng(int(sys.argv[1]))
N=int(sys.argv[2])
def jac(k,x,r,rp):
    k1,k2,k3,k5,k6,k7,k8,k10=k
    # numeric Jacobian at T=1 by finite-free analytic: build f and use complex step
    c=1+k1/(k5+k6)+k7/k8
    y0=np.array([x,1-c*x,k1*x/(k5+k6),k7*x/k8])
    return y0
def f(y,k,m,kr):
    k1,k2,k3,k5,k6,k7,k8,k10=k
    C,V,L,P=y; X=C/(C+V+L+P)
    rh=k3*binom.sf(kr-1,m,X)
    return np.array([-(k1+k2+k7)*C+k6*L+(k10+rh)*V, k2*C+k5*L+k8*P-(k10+rh)*V, k1*C-(k5+k6)*L, k7*C-k8*P])
def rho(X,k3,m,kr): return k3*binom.sf(kr-1,m,X)
def drho(X,k3,m,kr): return k3*m*binom.pmf(kr-1,m-1,X)
def J(y,k,m,kr):
    k1,k2,k3,k5,k6,k7,k8,k10=k
    C,V,L,P=y;T=y.sum();X=C/T
    r=rho(X,k3,m,kr);rp=drho(X,k3,m,kr)
    dX=np.array([(1-X)/T,-X/T,-X/T,-X/T])
    A=np.array([[-(k1+k2+k7),k10+r,k6,0],[k2,-(k10+r),k5,k8],[k1,0,-(k5+k6),0],[k7,0,0,-k8]],float)
    A[0]+=rp*V*dX; A[1]-=rp*V*dX
    return A
B=np.array([[1,0,0],[-1,1,1],[0,-1,0],[0,0,-1]],float);Bp=np.linalg.pinv(B)
xs=np.linspace(0,1,4001)[1:]
n3=0;out={'low':[],'high':[]};midstable=0;maxerr=0
for it in range(N):
    k=10**rng.uniform(-2,2,8); m=rng.integers(2,31); kr=rng.integers(2,m+1)
    k1,k2,k3,k5,k6,k7,k8,k10=k
    c=1+k1/(k5+k6)+k7/k8; D=k2+k7+k1*k5/(k5+k6)
    g=xs/c
    H=(k10+rho(g,k3,m,kr))*(1-c*g)-D*g
    s=np.where(np.sign(H[:-1])!=np.sign(H[1:]))[0]
    if len(s)!=3: continue
    n3+=1
    Hf=lambda z:(k10+rho(z,k3,m,kr))*(1-c*z)-D*z
    roots=[brentq(Hf,g[i],g[i+1],xtol=1e-15) for i in s]
    for j,xr in enumerate(roots):
        y=np.array([xr,1-c*xr,k1*xr/(k5+k6),k7*xr/k8])
        A=J(y,k,m,kr); M=Bp@A@B
        Hp=drho(xr,k3,m,kr)*(1-c*xr)-c*(k10+rho(xr,k3,m,kr))-D
        err=abs(np.linalg.det(M)/(k8*(k5+k6)*Hp)-1); maxerr=max(maxerr,err)
        mr=np.linalg.eigvals(M).real.max()
        if j==1 and mr<0: midstable+=1
        if j!=1 and mr>0:
            side='low' if j==0 else 'high'
            out[side].append((it,m,kr,list(k),xr,np.linalg.eigvals(M)))
print('three',n3,'maxerr',maxerr,'midstable',midstable,'low',len(out['low']),'high',len(out['high']))
for side in out:
    for e in out[side][:2]: print(side,e)
