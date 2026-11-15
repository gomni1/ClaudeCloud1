import sympy as sp, numpy as np
k1,k2,k5,k6,k7,k8,k9,k10,k12,u1,u2,u5,u6,u7,u8,u9,kap,sig,s,eps=sp.symbols('k1 k2 k5 k6 k7 k8 k9 k10 k12 u1 u2 u5 u6 u7 u8 u9 kappa sigma s epsilon',positive=True)
C1,V1,L1,P1,C2,V2,L2,P2,r1,r2=sp.symbols('C1 V1 L1 P1 C2 V2 L2 P2 rho1 rho2',nonnegative=True)
def sys(mult=1,e=0):
    U=kap*P1*C2; x1=C1/(C1+V1+L1+P1); se=sig*x1+r2
    lo=[-(k1+k2+k7)*C1+k6*L1+(k10+r1)*V1, k2*C1+k5*L1+k8*P1-(k10+r1)*V1+k12, k1*C1-(k5+k6)*L1, k7*C1-(k8+k9)*P1-U]
    up=[-(u1+u2+u7)*C2+u6*L2+se*V2, u2*C2+u5*L2+u8*P2-se*V2+mult*U+e*k9*P1, u1*C2-(u5+u6)*L2, u7*C2-(u8+u9)*P2]
    return lo,up
lo,up=sys()
print('(1)',sp.simplify(sum(lo)+sum(up)-(k12-k9*P1-u9*P2)))
lo2,up2=sys(2); print('(1) 2U err',sp.simplify(sum(lo2)+sum(up2)-(k12-k9*P1-u9*P2)))
print('(2) empty',[sp.simplify(e.subs({C2:0,V2:0,L2:0,P2:0})) for e in up])
print('(2) void only dC2',up[0].subs({C2:0,L2:0,P2:0}))
# (3)
sol=sp.solve([sum(lo),sum(up),up[2],up[3]],[P1,P2,L2,C2],dict=True); print('(3)',[ (sp.simplify(d[C2]),sp.simplify(d[P1])) for d in sol])
c=(u8+u9)/(u7*u9)
# (4)
A=sp.Matrix([[-(u1+u2+u7),s,u6,0],[u2+kap*k12/k9,-s,u5,u8],[u1,0,-(u5+u6),0],[u7,0,0,-(u8+u9)]])
print('(4) det diff',sp.simplify(A.det()-s*(u5+u6)*(k9*u7*u9-kap*k12*(u8+u9))/k9))
rng=np.random.default_rng(0); bad=0; lyap_bad=0
syms=[u1,u2,u5,u6,u7,u8,u9,k9,k12,kap,s]
f=sp.lambdify(syms,A,'numpy')
for i in range(20000):
    v=np.exp(rng.uniform(-4,4,len(syms)))
    M=np.array(f(*v),float); ab=np.linalg.eigvals(M).real.max()
    thr=v[9]*(v[5]+v[6])/(v[4]*v[6])*v[8]-v[7]   # kappa*c*k12-k9
    if abs(thr)<1e-6*v[7]: continue
    if (ab>0)!=(thr>0): bad+=1
print('(4) sign mismatches in 20000 random draws:',bad)
# s->0 growth rate
v=dict(zip(syms,[1,1,1,1,1,1,1,1,1,5,1]))
for sv in [1,1e-2,1e-4]:
    v[s]=sv; print('  s=',sv,'abscissa',np.linalg.eigvals(np.array(A.subs(v),float)).real.max())
# common copositive linear Lyapunov vector (independent of s): w^T A <0 below threshold
d,eta=sp.symbols('delta eta',positive=True)
w=sp.Matrix([[1,1+d,1+d,u8/(u8+u9)*(1+d)+eta]])
wa=(w*A).applyfunc(sp.simplify); print('(4) w^T A =',list(wa))
print('   col C at delta=eta=0:',sp.simplify(wa[0].subs({d:0,eta:0})),' vs kappa*k12/k9-1/c:',sp.simplify(wa[0].subs({d:0,eta:0})-(kap*k12/k9-1/c)))
# (5)
lo5,up5=sys(1,eps)
print('(5) cons',sp.simplify(sum(lo5)+sum(up5)-(k12-(1-eps)*k9*P1-u9*P2)))
P1b=k12/(k9+kap*C2); P2b=u7*C2/(u8+u9)
q=sp.numer(sp.together((eps*k9+kap*C2)*P1b-u9*P2b))
claim=kap*u7*u9*C2**2+(k9*u7*u9-kap*k12*(u8+u9))*C2-eps*k12*k9*(u8+u9)
print('(5) quad ratio',sp.simplify(q/claim))
print('(5) kappa=0 root',sp.solve(claim.subs(kap,0),C2), ' at threshold:',sp.solve(claim.subs(kap,k9/(c*k12)),C2))
r=sp.solve(claim,C2)[1]; print('(5) small-eps series below thr:',sp.simplify(sp.series(r,eps,0,2).removeO().subs({u7:1,u8:1,u9:1,k9:1,k12:1,kap:sp.Rational(1,4)})), [sp.simplify(x.subs({u7:1,u8:1,u9:1,k9:1,k12:1,kap:sp.Rational(1,4)})) for x in sp.solve(claim,C2)])
# counter-construction: thresholded passive feed eps*k9*max(P1-Pc,0)
Pc=sp.symbols('P_c',positive=True)
qq=sp.numer(sp.together(eps*k9*(P1b-Pc)+kap*C2*P1b-C2/c))
print('counter: balance poly at C2=0 ->',sp.factor(qq.subs(C2,0)),' (zero iff k12=k9*Pc)')
vals={u7:1,u8:1,u9:1,k9:1,kap:1,eps:sp.Rational(1,10),Pc:sp.Rational(1,4)}  # c=2, old thr k12=0.5, new thr k12=0.25
for kk in [0.2,0.25,0.26,0.3,0.5,1]:
    print('  k12',kk,[float(x) for x in sp.Poly(qq.subs(vals).subs(k12,sp.nsimplify(kk)),C2).nroots() if abs(sp.im(x))<1e-12])
