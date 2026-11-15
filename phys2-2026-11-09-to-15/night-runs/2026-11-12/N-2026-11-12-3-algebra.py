# N-2026-11-12-3: algebra for the minimal C_seed coupling (frozen in NIGHT-QUEUE-2026-11-12.md). Nothing is integrated.
import sympy as sp
k1,k2,k5,k6,k7,k8,k9,k10,k12,kap,sig,eps = sp.symbols('k1 k2 k5 k6 k7 k8 k9 k10 k12 kappa sigma epsilon', positive=True)
u1,u2,u5,u6,u7,u8,u9 = sp.symbols('u1 u2 u5 u6 u7 u8 u9', positive=True)
C1,V1,L1,P1,C2,V2,L2,P2 = sp.symbols('C1 V1 L1 P1 C2 V2 L2 P2', nonnegative=True)
r1,r2,x1 = sp.symbols('rho1 rho2 x1', nonnegative=True)   # recruitment rates and the lower Contact share, as symbols
def system(eps_on):
    passive = (eps*k9*P1) if eps_on else 0
    U = kap*P1*C2
    lower = [-(k1+k2+k7)*C1 + k6*L1 + (k10+r1)*V1, k2*C1 + k5*L1 + k8*P1 - (k10+r1)*V1 + k12, k1*C1 - (k5+k6)*L1, k7*C1 - (k8+k9)*P1 - U]
    s = sig*x1 + r2
    upper = [-(u1+u2+u7)*C2 + u6*L2 + s*V2, u2*C2 + u5*L2 + u8*P2 - s*V2 + U + passive, u1*C2 - (u5+u6)*L2, u7*C2 - (u8+u9)*P2]
    return lower, upper, U
lower, upper, U = system(False)
print('conservation: d(T1+T2)/dt - (k12 - k9 P1 - u9 P2) =', sp.simplify(sum(lower)+sum(upper) - (k12 - k9*P1 - u9*P2)))
print('planted failure (upper gains 2U): residual =', sp.simplify(sum(lower)+sum(upper)+U - (k12 - k9*P1 - u9*P2)))
# (a) invariance
z = {C2:0, V2:0, L2:0, P2:0}
print('(a) upper rates at the empty upper level:', [sp.simplify(e.subs(z)) for e in upper])
zc = {C2:0, L2:0, P2:0}
print('(a) upper rates with only Void present:', [sp.simplify(e.subs(zc)) for e in upper])
# (b) joint balances: pins
c = (u8+u9)/(u7*u9)
P1s = sp.solve(sp.Eq(k12, (k9 + kap*C2)*P1), P1)[0]            # lower total balance: k12 = k9 P1 + U
P2s = sp.solve(upper[3], P2)[0]
bal = sp.simplify((kap*P1*C2).subs(P1, P1s) - u9*P2s)            # upper total balance: U = u9 P2
print('(b) upper total balance factor:', sp.factor(bal))
print('(b) roots in C2:', sp.solve(sp.Eq(bal, 0), C2), ' ; 10 Nov form c*k12 - k9/kappa =', sp.simplify(c*k12 - k9/kap))
# at a balance with C2 = 0: P2 = L2 = 0, and dC2/dt = s V2 = 0 forces V2 = 0 when s > 0
print('(b) at C2 = 0: dC2/dt =', sp.simplify(upper[0].subs({C2:0, L2:0})), '-> V2 = 0 if sigma*x1 + rho2 > 0')
# (c) invasion matrix at the empty upper level, lower level at its own balance (P1 = k12/k9), seeding rate s frozen
s = sp.symbols('s', positive=True)
up_lin = [e.subs(sig*x1 + r2, s).subs(P1, k12/k9) for e in [-(u1+u2+u7)*C2 + u6*L2 + (sig*x1+r2)*V2, u2*C2 + u5*L2 + u8*P2 - (sig*x1+r2)*V2 + kap*P1*C2, u1*C2 - (u5+u6)*L2, u7*C2 - (u8+u9)*P2]]
A = sp.Matrix(up_lin).jacobian([C2, V2, L2, P2])
detA = sp.factor(A.det())
print('(c) A is Metzler (off-diagonals >= 0):', all((A[i,j] >= 0) == True or A[i,j] == 0 or A[i,j].is_nonnegative for i in range(4) for j in range(4) if i != j))
print('(c) det A =', detA)
print('(c) det A + [s (u5+u6) u7 u9 / k9]*(kappa*c*k12 - k9) =', sp.simplify(detA + (s*(u5+u6)*u7*u9/k9)*(kap*c*k12 - k9)), ' (0 means det A has the sign of k9 - kappa*c*k12 for every s > 0)')
# smallest further term that starts an empty upper level: a passive share eps of the lower exit k9 P1
lowerE, upperE, UE = system(True)
print('(a2) with passive share eps: upper rates at the empty upper level:', [sp.simplify(e.subs(z)) for e in upperE])
P1e = P1s                                   # the lower exit is still k9 P1 + kappa C2 P1 in total (the passive share is part of k9 P1)
balE = sp.together((eps*k9*P1 + kap*P1*C2).subs(P1, P1e) - u9*P2s)
num = sp.expand(sp.numer(balE)); print('(b2) balance numerator in C2:', sp.collect(num, C2))
q = sp.Poly(num, C2); print('(b2) coefficients:', q.all_coeffs())
print('(b2) product of roots =', sp.simplify(q.all_coeffs()[2]/q.all_coeffs()[0]), '(negative => exactly one positive root for every kappa >= 0)')
print('(b2) conservation with passive share: d(T1+T2)/dt - (k12 - (1-eps) k9 P1 - u9 P2) =', sp.simplify(sum(lowerE)+sum(upperE) - (k12 - k9*P1 - u9*P2) - eps*k9*P1), ' (the passive share eps*k9*P1 is part of the lower exit k9*P1, so each unit is still counted once)')
