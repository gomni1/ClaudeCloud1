import numpy as np
from scipy.special import betainc
from scipy.optimize import brentq
from scipy.integrate import solve_ivp
k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=(17.452344563736048, 0.41372216747103946, 44.67737830552512, 8.05086975924266, 0.06903256564057879, 0.03229295995554182, 0.083706798767576, 0.010174673348427083, 0.609928184398708, 0.15342684932155354)
m,kr=27,7
F=lambda x: betainc(kr,m-kr+1,x)
def f(t,y):
    C,V,L,P=y; T=C+V+L+P; r=k3*F(C/T)
    return [-(k1+k2+k7)*C+k6*L+(k10+r)*V, k2*C+k5*L+k8*P-(k10+r)*V+k12, k1*C-(k5+k6)*L, k7*C-(k8+k9)*P]
Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); Ps=k12/k9; D=k2+k7+k1*k5/(k5+k6)
g=lambda V:(k10+k3*F(Cs/(Cs+Ls+Ps+V)))*V-D*Cs
Vg=np.logspace(-3,6,200000); s=np.sign(g(Vg)); idx=np.where(np.diff(s)!=0)[0]
roots=[brentq(g,Vg[i],Vg[i+1],xtol=1e-14) for i in idx]
print("C*,L*,P*",Cs,Ls,Ps,"roots",roots)
def J(y,h=1e-6):
    J=np.zeros((4,4))
    for j in range(4):
        e=np.zeros(4); e[j]=h*max(1,abs(y[j]))
        J[:,j]=(np.array(f(0,y+e))-np.array(f(0,y-e)))/(2*e[j])
    return J
eqs=[]
for V in roots:
    y=np.array([Cs,V,Ls,Ps]); w,v=np.linalg.eig(J(y)); eqs.append((y,w,v))
    print(V, np.sort_complex(w), "resid",np.max(np.abs(f(0,y))))
np.save('eqs.npy',np.array([e[0] for e in eqs]))
