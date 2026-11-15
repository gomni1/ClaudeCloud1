# N-2026-11-10-2: consistency algebra for the specified two-way coupling (no dynamics run).
import sympy as sp
k1,k2,k5,k6,k7,k8,k9,k10,k12,kap=sp.symbols('k1 k2 k5 k6 k7 k8 k9 k10 k12 kappa',positive=True)
u1,u2,u5,u6,u7,u8,u9,u10=sp.symbols('u1 u2 u5 u6 u7 u8 u9 u10',positive=True)
C1,V1,L1,P1,C2,V2,L2,P2,r1,r2=sp.symbols('C1 V1 L1 P1 C2 V2 L2 P2 rho1 rho2',nonnegative=True)
U=kap*P1*C2                       # uptake: encounter of lower breach-ready units with upper Contact
fC1=-(k1+k2+k7)*C1+k6*L1+(k10+r1)*V1
fV1=k2*C1+k5*L1+k8*P1-(k10+r1)*V1+k12
fL1=k1*C1-(k5+k6)*L1
fP1=k7*C1-(k8+k9)*P1-U
fC2=-(u1+u2+u7)*C2+u6*L2+(u10+r2)*V2
fV2=u2*C2+u5*L2+u8*P2-(u10+r2)*V2+U      # supply to the upper arrives as Void, and only as U
fL2=u1*C2-(u5+u6)*L2
fP2=u7*C2-(u8+u9)*P2
tot=sp.simplify(fC1+fV1+fL1+fP1+fC2+fV2+fL2+fP2)
print("d(T1+T2)/dt =",tot,"  (U cancels: each unit counted once)")
# lower balance pins given C2 (any recruitment law)
P1s=sp.solve(sp.Eq(k12,k9*P1+U),P1)[0]
C1s=sp.solve(sp.Eq(fP1.subs(P1,P1s),0),C1)[0]
print("P1* =",sp.simplify(P1s)); print("C1* =",sp.simplify(C1s))
print("dC1*/dC2 =",sp.factor(sp.diff(C1s,C2)))
print("uptake at balance U* =",sp.simplify(U.subs(P1,P1s)),"; limit C2->oo:",sp.limit(U.subs(P1,P1s),C2,sp.oo))
print("C1* limits: C2=0:",sp.simplify(C1s.subs(C2,0)),"  C2->oo:",sp.limit(C1s,C2,sp.oo))
# planted double-count: upper receives 2U
tot_bad=sp.simplify(tot+U)
print("planted double count adds exactly:",tot_bad-tot)
# joint balance: the upper's own throughput pin (S2 applied to the upper with supply U): C2* = c*U*, c=(u8+u9)/(u7*u9)
c=(u8+u9)/(u7*u9)
sol=sp.solve(sp.Eq(C2,c*U.subs(P1,P1s)),C2)
print("joint balance C2* solutions:",[sp.simplify(s) for s in sol])
C2s=c*k12-k9/kap
print("upper exists (C2*>0) iff kappa*c*k12 > k9; then C1* =",sp.simplify(C1s.subs(C2,C2s)))
