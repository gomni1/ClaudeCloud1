# N-2026-11-10-1 numerical harness, as frozen in NIGHT-QUEUE-2026-11-10.md (item 1).
# No ODE integration: balances and Jacobians only. Per-draw summaries only are kept.
import numpy as np, json, sys, time, math
from scipy.optimize import brentq
from scipy.special import betainc, gammaln
RNG_SEED=20261110
def F(x,m,kr): return betainc(kr, m-kr+1, x)          # Pr[Bin(m,x)>=kr]
def Fp(x,m,kr):                                         # beta density
    return math.exp(gammaln(m+1)-gammaln(kr)-gammaln(m-kr+1)+(kr-1)*math.log(x)+(m-kr)*math.log1p(-x))
def pins(k):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    Ps=k12/k9; Cs=(k8+k9)*k12/(k7*k9); Ls=k1*Cs/(k5+k6); D=k2+k7+k1*k5/(k5+k6)
    return Cs,Ls,Ps,D
def balances(k,m,kr,ngrid=4000):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    Cs,Ls,Ps,D=pins(k); a=Cs; b=Cs+Ls+Ps; g=D*Cs
    G=lambda x:(k10+k3*F(x,m,kr))*(a-b*x)-g*x
    xe=a/b
    xs=np.linspace(0,xe,ngrid+1)[1:-1]
    vals=np.array([G(t) for t in xs])
    s=np.concatenate(([1.0],np.sign(vals),[-1.0]))     # exact end signs: G(0)=k10*a>0, G(xe)=-g*a/b<0
    pts=np.concatenate(([0.0],xs,[xe]))
    roots=[]
    for i in range(len(s)-1):
        if s[i]!=s[i+1]:
            lo,hi=pts[i],pts[i+1]
            if s[i]==0: roots.append(lo); continue
            if s[i+1]==0: continue
            roots.append(brentq(G,lo,hi,xtol=1e-15,rtol=1e-15,maxiter=200))
    return roots,(Cs,Ls,Ps,D,a,b)
def jac(k,m,kr,C,V,L,P):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    T=C+V+L+P; x=C/T
    dx=np.array([(T-C)/T**2,-C/T**2,-C/T**2,-C/T**2])
    rho=k3*F(x,m,kr); drho=k3*Fp(x,m,kr)*dx
    e=np.zeros(4); e[1]=1.0
    JC=np.array([-(k1+k2+k7),0,k6,0])+(k10+rho)*e+V*drho
    JV=np.array([k2,0,k5,k8])-((k10+rho)*e+V*drho)
    JL=np.array([k1,0,-(k5+k6),0]); JP=np.array([k7,0,0,-(k8+k9)])
    return np.array([JC,JV,JL,JP])
def gprime(k,m,kr,V,a,b):
    k1,k2,k3,k5,k6,k7,k8,k9,k10,k12=k
    x=a/(b+V)
    return k10+k3*F(x,m,kr)+k3*V*Fp(x,m,kr)*(-a/(b+V)**2)
def analyse(k,m,kr):
    roots,(Cs,Ls,Ps,D,a,b)=balances(k,m,kr)
    out=[]
    for x in roots:
        V=a/x-b
        J=jac(k,m,kr,Cs,V,Ls,Ps)
        lam=np.linalg.eigvals(J)
        gp=gprime(k,m,kr,V,a,b)
        K=k[5]*k[7]*(k[3]+k[4])
        dJ=np.linalg.det(J)
        rel=abs(dJ-K*gp)/(abs(dJ)+K*abs(gp)+1e-300)
        out.append(dict(V=V,x=x,maxre=float(lam.real.max()),maxabs=float(abs(lam).max()),gp=gp,det=dJ,rel=rel,J=J,K=K))
    return out
def draw(rng):
    k=tuple(10**rng.uniform(-2,2,10))
    m=int(rng.integers(2,31)); kr=int(rng.integers(2,m+1))
    return k,m,kr
if __name__=="__main__":
    mode=sys.argv[1]
    if mode=="repro":
        k=(0.4885,0.1976,13.992,7.024,8.293,2.092,1.267,4.986,0.3117,16.654)
        res=analyse(k,10,6)
        for r in sorted(res,key=lambda r:r['V']):
            print("V*=%.3f"%r['V'], "eig=",np.round(np.sort_complex(np.linalg.eigvals(r['J'])),3), "g'=%.4g det=%.4g rel=%.2e"%(r['gp'],r['det'],r['rel']))
        sys.exit()
    rng=np.random.default_rng(RNG_SEED)
    maxdraws=int(sys.argv[2]); wall=float(sys.argv[3]); target=int(sys.argv[4])
    t0=time.time(); n=0; three=0; summ=[]; counts={}; flags=dict(identity=0,middle_stable=0,outer_unstable=0,gp_sign_mismatch=0)
    plantP1=dict(run=0,tripped=0,minrel=1e9); plantP2=dict(run=0,tripped=0); outer_cases=[]
    while n<maxdraws and time.time()-t0<wall and three<target:
        k,m,kr=draw(rng); n+=1
        try: res=analyse(k,m,kr)
        except Exception as ex:
            counts['error']=counts.get('error',0)+1; continue
        counts[len(res)]=counts.get(len(res),0)+1
        if len(res)!=3: continue
        three+=1
        res=sorted(res,key=lambda r:r['V'])
        rec=dict(i=n,m=m,kr=kr,V=[r['V'] for r in res],maxre=[r['maxre'] for r in res],rel=[r['rel'] for r in res],gp=[r['gp'] for r in res])
        for r in res:
            if r['rel']>1e-6: flags['identity']+=1
        if res[1]['maxre']<=0: flags['middle_stable']+=1
        if not (res[0]['gp']>0 and res[1]['gp']<0 and res[2]['gp']>0): flags['gp_sign_mismatch']+=1
        for j in (0,2):
            if res[j]['maxre']>1e-9*res[j]['maxabs']:
                flags['outer_unstable']+=1; outer_cases.append(dict(i=n,k=k,m=m,kr=kr,which=j,V=res[j]['V'],maxre=res[j]['maxre']))
        if plantP1['run']<200:
            # P1: shift (C,V) entry by delta, compare det to identity with UNSHIFTED g' (as frozen)
            for r in res[:1]:
                d=0.5*abs(r['gp'])+1; Js=r['J'].copy(); Js[0,1]+=d
                dJs=np.linalg.det(Js); rel=abs(dJs-r['K']*r['gp'])/(abs(dJs)+r['K']*abs(r['gp'])+1e-300)
                plantP1['run']+=1; plantP1['tripped']+=int(rel>1e-6); plantP1['minrel']=min(plantP1['minrel'],rel)
            # P2: J+sI at the most stable balance
            js=min(range(3),key=lambda j:res[j]['maxre']); J=res[js]['J']
            s=1-res[js]['maxre']; lam=np.linalg.eigvals(J+s*np.eye(4)); mr=lam.real.max()
            plantP2['run']+=1; plantP2['tripped']+=int(mr>1e-9*abs(lam).max())
        summ.append(rec)
    el=time.time()-t0
    out=dict(draws=n,three_balance=three,elapsed_s=el,root_counts=counts,flags=flags,plantP1=plantP1,plantP2=plantP2,outer_cases=outer_cases[:200])
    json.dump(out,open(sys.argv[5],'w'),indent=1,default=float)
    json.dump(summ,open(sys.argv[5].replace('.json','-perdraw.json'),'w'),default=float)
    print(json.dumps({k:v for k,v in out.items() if k!='outer_cases'},default=float)); print("outer cases:",len(outer_cases))
