# N-2026-11-10-1: 50-digit re-verification of outer-unstable cases (as frozen).
import mpmath as mp, json, sys
mp.mp.dps=50
def verify(k,m,kr,V0):
    k=[mp.mpf(v) for v in k]; k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); D=k2+k7+k1*k5/(k5+k6)
    a=Cs; b=Cs+Ls+Ps
    F=lambda x: mp.betainc(kr,m-kr+1,0,x,regularized=True)
    Fp=lambda x: mp.factorial(m)/(mp.factorial(kr-1)*mp.factorial(m-kr))*x**(kr-1)*(1-x)**(m-kr)
    G=lambda x:(k10+k3*F(x))*(a-b*x)-D*Cs*x
    x=mp.findroot(G,a/(b+mp.mpf(V0)))
    V=a/x-b; C,L,P=Cs,Ls,Ps; T=C+V+L+P
    dx=[(T-C)/T**2,-C/T**2,-C/T**2,-C/T**2]
    rho=k3*F(x); drho=[k3*Fp(x)*d for d in dx]
    e=[0,1,0,0]
    JC=[[-(k1+k2+k7),0,k6,0][i]+(k10+rho)*e[i]+V*drho[i] for i in range(4)]
    JV=[[k2,0,k5,k8][i]-((k10+rho)*e[i]+V*drho[i]) for i in range(4)]
    J=mp.matrix([JC,JV,[k1,0,-(k5+k6),0],[k7,0,0,-(k8+k9)]])
    ev=mp.eig(J,left=False,right=False)
    # residual of the full RHS at the balance
    fC=-(k1+k2+k7)*C+k6*L+(k10+rho)*V; fV=k2*C+k5*L+k8*P-(k10+rho)*V+k12
    return dict(V=V,G=G(x),res=max(abs(fC),abs(fV)),eig=ev,maxre=max(mp.re(z) for z in ev),
                gp=k10+k3*F(x)+k3*V*Fp(x)*(-a/(b+V)**2),det=mp.det(J),K=k7*k9*(k5+k6))
if __name__=="__main__":
    d=json.load(open(sys.argv[1])); cases=d['outer_cases']; nmax=int(sys.argv[2]) if len(sys.argv)>2 else len(cases)
    ok=0; lines=[]
    for c in cases[:nmax]:
        r=verify(c['k'],c['m'],c['kr'],c['V'])
        good=r['maxre']>0 and r['res']<mp.mpf('1e-30')
        ok+=int(good)
        lines.append("draw %d m=%d kr=%d which=%s V*=%s maxRe=%s resid=%s g'=%s det/K/g'=%s eig=%s"%(c['i'],c['m'],c['kr'],'low-V' if c['which']==0 else 'high-V',mp.nstr(r['V'],12),mp.nstr(r['maxre'],12),mp.nstr(r['res'],3),mp.nstr(r['gp'],8),mp.nstr(r['det']/(r['K']*r['gp']),20),[mp.nstr(z,8) for z in r['eig']]))
    print("\n".join(lines)); print("verified unstable at 50 digits: %d of %d"%(ok,min(nmax,len(cases))))
