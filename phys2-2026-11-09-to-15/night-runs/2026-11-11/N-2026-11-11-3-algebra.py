# N-2026-11-11-3: consistency algebra for the revised two-level coupling (specification only; no dynamics run).
import sympy as sp
k1,k2,k3,k5,k6,k7,k8,k9,k10,k12 = sp.symbols('k1 k2 k3 k5 k6 k7 k8 k9 k10 k12', positive=True)
u1,u2,u3,u5,u6,u7,u8,u9 = sp.symbols('u1 u2 u3 u5 u6 u7 u8 u9', positive=True)
kap, nu, sig = sp.symbols('kappa nu sigma', positive=True)
C1,V1,L1,P1,C2,V2,L2,P2 = sp.symbols('C1 V1 L1 P1 C2 V2 L2 P2', nonnegative=True)
r1, r2 = sp.symbols('rho1 rho2', nonnegative=True)   # each level's own recruitment per unit Void (any law)
T1 = C1+V1+L1+P1
x1 = C1/T1
U = (k9 + kap*C2)*P1           # all lower output goes up: passive breach k9*P1 plus active uptake kappa*P1*C2
s2 = sig*x1                     # upper seeding templated from below (replaces the upper level's own u10)
f1 = sp.Matrix([-(k1+k2+k7)*C1 + k6*L1 + (k10+r1)*V1,
                k2*C1 + k5*L1 + k8*P1 - (k10+r1)*V1 + k12,
                k1*C1 - (k5+k6)*L1,
                k7*C1 - k8*P1 - U])
f2 = sp.Matrix([-(u1+u2+u7)*C2 + u6*L2 + (s2+r2)*V2,
                u2*C2 + u5*L2 + u8*P2 - (s2+r2)*V2 + U/nu,
                u1*C2 - (u5+u6)*L2,
                u7*C2 - (u8+u9)*P2])
ledger = sp.simplify(sum(f1) + nu*sum(f2) - (k12 - nu*u9*P2))
print('d(T1 + nu*T2)/dt - (k12 - nu*u9*P2) =', ledger)
# planted failure for the later test: upper gains 2U/nu
f2w = f2.copy(); f2w[1] = f2[1] + U/nu
print('planted: residual =', sp.factor(sp.simplify(sum(f1) + nu*sum(f2w) - (k12 - nu*u9*P2))))
# lower pins at balance given C2
P1s = sp.solve(sp.Eq(sum(f1), 0).subs({}), P1)  # sum f1 = k12 - U
print('sum f1 =', sp.simplify(sum(f1)))
P1b = k12/(k9+kap*C2)
C1b = sp.simplify((k8*P1b + U.subs(P1, P1b))/k7)
print('P1* =', P1b, '; C1* =', sp.simplify(C1b), '; dC1*/dC2 =', sp.simplify(sp.diff(C1b, C2)))
# upper level at balance: supply U*/nu = k12/nu whatever kappa
print('U at lower balance =', sp.simplify(U.subs(P1, P1b)))
C2b = (u8+u9)*(k12/nu)/(u7*u9)
print('C2* (upper pin) =', C2b)
# seeding: on the face C2 = L2 = P2 = 0 with V2 > 0, dC2/dt = sigma*x1*V2 > 0 if C1 > 0
print('dC2/dt on face C2=L2=P2=0:', sp.simplify(f2[0].subs({C2:0, L2:0, P2:0})))
print('dV2/dt on face C2=L2=P2=V2=0:', sp.simplify(f2[1].subs({C2:0, L2:0, P2:0, V2:0})))
