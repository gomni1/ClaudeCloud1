import numpy as np
from scipy.integrate import solve_ivp
from scipy.special import betainc
m,kr=18,5
K0=np.array([0.024467,0.084768,90.827,0.039721,40.114,5.9669,1.1506,0.29753])
def rhs(t,y,K,mode,T0):
    k1,k2,k3,k5,k6,k7,k8,k10=K
    C,V,L,P=y
    x = C/(C+V+L+P) if mode=='share' else min(max(C/T0,0),1)
    r=k10+k3*betainc(kr,m-kr+1,min(max(x,0),1))
    return [-(k1+k2+k7)*C+k6*L+r*V, k2*C+k5*L+k8*P-r*V, k1*C-(k5+k6)*L, k7*C-k8*P]
def run(T,s=1.0,mode='share',y0=None,tend=400.,T0=1.0):
    K=K0*s
    y0=np.array([.25,.25,.25,.25])*T if y0 is None else y0
    sol=solve_ivp(rhs,[0,tend/s],y0,method='Radau',args=(K,mode,T0),rtol=1e-11,atol=1e-14*T,dense_output=True)
    # level: midrange of C over last quarter
    tt=np.linspace(0.75*tend/s,tend/s,40001); C=sol.sol(tt)[0]
    amp=C.max()-C.min(); lev=0.5*(C.max()+C.min())
    if amp<1e-6*T: return None,amp/T,sol,None
    from scipy.optimize import brentq
    g=lambda t: sol.sol(t)[0]-lev
    idx=np.where((C[:-1]<lev)&(C[1:]>=lev))[0]
    cr=np.array([brentq(g,tt[i],tt[i+1],xtol=1e-14,rtol=1e-15) for i in idx])
    return np.diff(cr),amp/T,sol,cr
d1,a1,s1,c1=run(1.0); print('T=1    periods',d1[-3:],'amp/T',a1, 'n',len(d1))
d2,a2,s2,c2=run(7.3); print('T=7.3  periods',d2[-3:],'amp/T',a2)
d3,a3,s3,c3=run(1.0,s=2.0); print('x2 rates periods',d3[-3:])
p1,p2,p3=d1[-1],d2[-1],d3[-1]
print('rel diff T:',abs(p2/p1-1),' ratio doubled:',p3/p1, 'dev from .5:',abs(p3/p1-.5))
# other start
d4,a4,_,_=run(1.0,y0=np.array([.7,.1,.05,.15])); print('other start',None if d4 is None else d4[-1],a4)
d5,a5,_,_=run(1.0,y0=np.array([.02,.9,.04,.04])); print('other start2',None if d5 is None else d5[-1],a5)
# Floquet multipliers 4D by finite differences, at T=1 and 7.3 and doubled
def floq(T,s,sol,cr,per):
    y0=sol.sol(cr[-1]); M=np.zeros((4,4)); h=1e-6*T
    f=lambda y: solve_ivp(rhs,[0,per],y,method='Radau',args=(K0*s,'share',1.),rtol=1e-12,atol=1e-15*T).y[:,-1]
    for j in range(4):
        e=np.zeros(4); e[j]=h
        M[:,j]=(f(y0+e)-f(y0-e))/(2*h)
    return np.sort_complex(np.linalg.eigvals(M))
print('Floquet T=1  ',floq(1,1,s1,c1,p1))
print('Floquet T=7.3',floq(7.3,1,s2,c2,p2))
print('Floquet x2   ',floq(1,2,s3,c3,p3))
# real planted failure: recruitment depends on AMOUNT C (C/T0, T0=1), homogeneity broken
for T in (1.0,0.9,1.1):
    d,a,_,_=run(T,mode='amount'); print('amount-dependent rho, T=',T,'period',None if d is None else d[-1],'amp/T',a)
