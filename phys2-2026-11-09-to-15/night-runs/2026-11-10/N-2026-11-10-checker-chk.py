import sympy as sp, mpmath as mp
C,V,L,P=sp.symbols('C V L P',positive=True)
k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=sp.symbols('k1 k2 k3 k5 k6 k7 k8 k9 k10 k12',positive=True)
F=sp.Function('F'); T=C+V+L+P; rho=k3*F(C/T)
f=sp.Matrix([-(k1+k2+k7)*C+k6*L+(k10+rho)*V, k2*C+k5*L+k8*P-(k10+rho)*V+k12, k1*C-(k5+k6)*L, k7*C-(k8+k9)*P])
X=sp.Matrix([C,V,L,P]); J=f.jacobian(X)
print('row sum', sp.simplify(sp.ones(1,4)*J))
print('(a) diff', sp.simplify(J.det()-k7*k9*(k5+k6)*J[0,1]))
cof=J.cofactor(0,1); print('true cofactor (C,V):', sp.simplify(cof))
d=sp.symbols('d'); Jp=J.copy(); Jp[0,1]+=d
print('det shift - d*cof', sp.simplify(Jp.det()-J.det()-d*cof))
# numerics
mp.mp.dps=50
def run(m,kr,ks,label):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=[mp.mpf(x) for x in ks]
    Fx=lambda x: mp.betainc(kr,m-kr+1,0,x,regularized=True)
    Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); D=k2+k7+k1*k5/(k5+k6)
    g=lambda v:(k10+k3*Fx(Cs/(Cs+Ls+Ps+v)))*v - D*Cs
    # scan for roots on log grid
    vs=[mp.mpf(10)**(mp.mpf(i)/400) for i in range(-2400,4000)]
    roots=[]; prev=g(vs[0])
    for a,b in zip(vs,vs[1:]):
        gb=g(b)
        if prev*gb<0: roots.append(mp.findroot(g,(a,b),solver='anderson'))
        prev=gb
    print(label,'Cs,Ls,Ps',mp.nstr(Cs,12),mp.nstr(Ls,12),mp.nstr(Ps,12),'nroots',len(roots))
    for v in roots:
        def fv(c,vv,l,p):
            T=c+vv+l+p; r=k3*Fx(c/T)
            return [-(k1+k2+k7)*c+k6*l+(k10+r)*vv, k2*c+k5*l+k8*p-(k10+r)*vv+k12, k1*c-(k5+k6)*l, k7*c-(k8+k9)*p]
        x0=[Cs,v,Ls,Ps]; h=mp.mpf(10)**-20
        Jn=mp.matrix(4,4)
        for j in range(4):
            xp=list(x0); xm=list(x0); xp[j]+=h; xm[j]-=h
            a=fv(*xp); b=fv(*xm)
            for i in range(4): Jn[i,j]=(a[i]-b[i])/(2*h)
        res=max(abs(t) for t in fv(*x0))
        gp=mp.diff(lambda u:g(u),v)
        ev=mp.eig(Jn)[0]
        print(' V*=',mp.nstr(v,14),'resid',mp.nstr(res,3),"g'=",mp.nstr(gp,8),'detJ=',mp.nstr(mp.det(Jn),8),'k7k9s g\'=',mp.nstr(k7*k9*(k5+k6)*gp,8))
        print('   eig',[mp.nstr(e,8) for e in sorted(ev,key=lambda z:mp.re(z))])
        # true cofactor
        M=mp.matrix([[Jn[i,j] for j in (0,2,3)] for i in (1,2,3)])
        print('   cof(C,V)=',mp.nstr(-mp.det(M),8),' vs k7k9(k5+k6)=',mp.nstr(k7*k9*(k5+k6),8))
    return roots
run(27,7,[17.452344563736048,0.41372216747103946,44.67737830552512,8.05086975924266,0.06903256564057879,0.03229295995554182,0.083706798767576,0.010174673348427083,0.609928184398708,0.15342684932155354],'(c)')
run(10,6,[0.4885,0.1976,13.992,7.024,8.293,2.092,1.267,4.986,0.3117,16.654],'(d)')
