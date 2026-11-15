# N-2026-11-10-1 (a): symbolic determinant identity at an open-level balance.
# F and F' are kept as free symbols Fx, Fpx (values at x), so the result holds for ANY recruitment law rho = k3*F(x).
import sympy as sp
k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=sp.symbols('k1 k2 k3 k5 k6 k7 k8 k9 k10 k12',positive=True)
C,V,L,P,Fx,Fpx=sp.symbols('C V L P Fx Fpx',positive=True)
y=[C,V,L,P]; T=C+V+L+P; x=C/T
dx=[sp.diff(x,v) for v in y]               # gradient of x
drho=[k3*Fpx*d for d in dx]                # gradient of rho = k3 F(x)
rho=k3*Fx
# Jacobian rows built by the chain rule
def row(lin, vcoef):
    # lin: gradient of the linear part; vcoef: coefficient multiplying (k10+rho)*V (+1 in fC, -1 in fV)
    return [lin[i] + vcoef*((k10+rho)*(1 if i==1 else 0) + V*drho[i]) for i in range(4)]
JC=row([-(k1+k2+k7),0,k6,0],+1)
JV=row([k2,0,k5,k8],-1)
JL=[k1,0,-(k5+k6),0]
JP=[k7,0,0,-(k8+k9)]
J=sp.Matrix([JC,JV,JL,JP])
dfCdV=JC[1]
detJ=sp.together(J.det(method='berkowitz'))
r_gen=sp.simplify(sp.together(detJ-k7*k9*(k5+k6)*dfCdV))
print("det J - k7 k9 (k5+k6) dfC/dV  (any state, any F) =", r_gen)
# is it zero only at a balance? test with pins
Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6)
r_bal=sp.simplify(sp.together(r_gen.subs({C:Cs,L:Ls,P:Ps})))
print("same, at the S2 pins =", r_bal)
# dfC/dV equals g'(V) with g(V)=(k10+k3 F(a/(b+V)))V, a=C, b=C+L+P:  g' = k10 + k3 F + k3 V F'(x) * d/dV[a/(b+V)]
gp=k10+k3*Fx+k3*V*Fpx*sp.diff(C/(C+L+P+V),V)
print("dfC/dV - g'(V) =", sp.simplify(dfCdV-gp))
print("cofactor of (C,V) entry =", sp.factor(J.cofactor(0,1)))
