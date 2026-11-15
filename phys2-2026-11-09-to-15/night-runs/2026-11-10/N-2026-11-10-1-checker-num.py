import mpmath as mp, numpy as np
from scipy.special import betainc
mp.mp.dps=50
def run(m,kr,ks,label):
    kf=ks; K=[mp.mpf(x) for x in ks]
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=K
    Fx=lambda x: mp.betainc(kr,m-kr+1,0,x,regularized=True)
    Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); D=k2+k7+k1*k5/(k5+k6)
    g=lambda v:(k10+k3*Fx(Cs/(Cs+Ls+Ps+v)))*v - D*Cs
    # float scan
    c,l,p,d=map(float,(Cs,Ls,Ps,D))
    vs=np.logspace(-8,8,200001)
    gf=(kf[8]+kf[2]*betainc(kr,m-kr+1,c/(c+l+p+vs)))*vs-d*c
    idx=np.where(np.sign(gf[:-1])!=np.sign(gf[1:]))[0]
    roots=[mp.findroot(g,(mp.mpf(vs[i]),mp.mpf(vs[i+1])),solver='illinois') for i in idx]
    print(label,'C*,L*,P*,D=',[mp.nstr(z,12) for z in (Cs,Ls,Ps,D)],'nroots',len(roots))
    def fv(c,vv,l,p):
        T=c+vv+l+p; r=k3*Fx(c/T)
        return [-(k1+k2+k7)*c+k6*l+(k10+r)*vv, k2*c+k5*l+k8*p-(k10+r)*vv+k12, k1*c-(k5+k6)*l, k7*c-(k8+k9)*p]
    for v in roots:
        x0=[Cs,v,Ls,Ps]; h=mp.mpf(10)**-20; Jn=mp.matrix(4,4)
        for j in range(4):
            xp=list(x0); xm=list(x0); xp[j]+=h; xm[j]-=h
            A=fv(*xp); B=fv(*xm)
            for i in range(4): Jn[i,j]=(A[i]-B[i])/(2*h)
        res=max(abs(t) for t in fv(*x0)); gp=mp.diff(g,v)
        ev=sorted(mp.eig(Jn)[0],key=lambda z:(mp.re(z),mp.im(z)))
        M=mp.matrix([[Jn[i,j] for j in (0,2,3)] for i in (1,2,3)])
        print(' V*=',mp.nstr(v,14),'resid',mp.nstr(res,3),"g'=",mp.nstr(gp,8),'detJ=',mp.nstr(mp.det(Jn),8),"k7k9s*g'=",mp.nstr(k7*k9*(k5+k6)*gp,8))
        print('   eig',[mp.nstr(e,8) for e in ev])
        print('   cof(C,V)=',mp.nstr(-mp.det(M),8),' k7k9(k5+k6)=',mp.nstr(k7*k9*(k5+k6),8))
    return roots
run(27,7,[17.452344563736048,0.41372216747103946,44.67737830552512,8.05086975924266,0.06903256564057879,0.03229295995554182,0.083706798767576,0.010174673348427083,0.609928184398708,0.15342684932155354],'(c)')
run(10,6,[0.4885,0.1976,13.992,7.024,8.293,2.092,1.267,4.986,0.3117,16.654],'(d)')
