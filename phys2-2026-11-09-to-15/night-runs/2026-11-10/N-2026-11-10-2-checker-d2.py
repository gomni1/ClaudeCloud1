from sympy import *
k1,k2,k5,k6,k7,k8,k9,k10,k12,rho,ka=symbols('k1 k2 k5 k6 k7 k8 k9 k10 k12 rho kappa',positive=True)
u1,u2,u5,u6,u7,u8,u9,u10,r2=symbols('u1 u2 u5 u6 u7 u8 u9 u10 r2',positive=True)
C1,V1,L1,P1,C2,V2,L2,P2=symbols('C1 V1 L1 P1 C2 V2 L2 P2')
U=ka*P1*C2
f=[-(k1+k2+k7)*C1+k6*L1+(k10+rho)*V1, k2*C1+k5*L1+k8*P1-(k10+rho)*V1+k12, k1*C1-(k5+k6)*L1, k7*C1-(k8+k9)*P1-U,
   -(u1+u2+u7)*C2+u6*L2+(u10+r2)*V2, u2*C2+u5*L2+u8*P2-(u10+r2)*V2+U, u1*C2-(u5+u6)*L2, u7*C2-(u8+u9)*P2]
print(simplify(sum(f)))
s=solve(f[:4],[C1,V1,L1,P1],dict=True)[0]
print(simplify(s[P1]),factor(s[C1]))
Ust=simplify(U.subs(s)); print(Ust)
s2=solve([fi.subs(s) for fi in f[4:]],[V2,L2,P2],dict=True)
print(s2)
# upper total balance
P2s=u7*C2/(u8+u9)
print(solve(simplify(Ust-u9*P2s),C2))
