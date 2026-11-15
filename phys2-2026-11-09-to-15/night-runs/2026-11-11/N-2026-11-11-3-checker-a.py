from sympy import *
k1,k2,k5,k6,k7,k8,k9,k10,k12,kap,nu,sig,r1,r2=symbols('k1 k2 k5 k6 k7 k8 k9 k10 k12 kappa nu sigma rho1 rho2',positive=True)
u1,u2,u5,u6,u7,u8,u9,u10=symbols('u1 u2 u5 u6 u7 u8 u9 u10',positive=True)
C1,V1,L1,P1,C2,V2,L2,P2=symbols('C1 V1 L1 P1 C2 V2 L2 P2',nonnegative=True)
T1=C1+V1+L1+P1; x1=C1/T1; U=(k9+kap*C2)*P1
dC1=-(k1+k2+k7)*C1+k6*L1+(k10+r1)*V1
dV1=k2*C1+k5*L1+k8*P1-(k10+r1)*V1+k12
dL1=k1*C1-(k5+k6)*L1
dP1=k7*C1-k8*P1-U
dC2=-(u1+u2+u7)*C2+u6*L2+(sig*x1+r2)*V2
dV2=u2*C2+u5*L2+u8*P2-(sig*x1+r2)*V2+U/nu
dL2=u1*C2-(u5+u6)*L2
dP2=u7*C2-(u8+u9)*P2
print('ledger',simplify(dC1+dV1+dL1+dP1+nu*(dC2+dV2+dL2+dP2)))
print('planted',simplify(dC1+dV1+dL1+dP1+nu*(dC2+dV2+dL2+dP2+U/nu)-(k12-nu*u9*P2)))
P1s=solve(Eq(k12,U),P1)[0]; C1s=solve(dP1.subs(P1,P1s),C1)[0]
print('P1*',P1s,' C1*',simplify(C1s),' dC1/dC2',simplify(diff(C1s,C2)),' dC1/dkappa',simplify(diff(C1s,kap)))
P2s=k12/(nu*u9); C2s=solve(dP2.subs(P2,P2s),C2)[0]; print('C2*',simplify(C2s))
L2s=u1*C2/(u5+u6); V2s=solve(dC2.subs(L2,L2s),V2)[0]; print('V2*',simplify(V2s))
print('face dC2',dC2.subs({C2:0,L2:0,P2:0}))
