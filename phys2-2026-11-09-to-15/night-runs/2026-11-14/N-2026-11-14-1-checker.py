import numpy as np, itertools, time
t0=time.time()
D1,D2=10000.0,2000.0
om=np.pi/5
X=np.arange(-500,501).astype(float)
centres=[-100,0,100]
Y=np.array([c+d for c in centres for d in range(-2,3)],float)   # 15 histories per x
slit=np.repeat([0,1,2],5)
L=np.sqrt(D1**2+Y[:,None]**2)+np.sqrt(D2**2+(X[None,:]-Y[:,None])**2)  # (15,1001)
configs=[c for r in range(4) for c in itertools.combinations(range(3),r)]
def slitR(theta,k):
    # per-slit resultants, shape (3,nx,2) or with leading draw axis
    u=np.stack([np.cos(k*theta),np.sin(k*theta)],-1)
    return np.stack([u[...,slit==i,:,:].sum(-3) for i in range(3)],0)
def Pall(Rs,readout,s=None):
    P={}
    for c in configs:
        if len(c)==0: P[c]=np.zeros(Rs.shape[1:-1]); continue
        R=sum(Rs[i] for i in c); m=(R**2).sum(-1)
        if readout=='R2': P[c]=m
        elif readout=='R4': P[c]=m**2
        elif readout=='RS': P[c]=1-np.exp(-m/s)
    return P
def measures(P):
    A,B,C=(0,),(1,),(2,)
    I2={p:P[p]-P[(p[0],)]-P[(p[1],)]+P[()] for p in [(0,1),(0,2),(1,2)]}
    I3=P[(0,1,2)]-P[(0,1)]-P[(0,2)]-P[(1,2)]+P[A]+P[B]+P[C]-P[()]
    s2=sum(np.abs(v).sum(-1) for v in I2.values())
    k2=s2/P[(0,1,2)].sum(-1)
    with np.errstate(invalid='ignore',divide='ignore'):
        k3=np.abs(I3).sum(-1)/s2
    return k2,k3,I2,I3
def maxima(p):
    i=np.arange(1,len(p)-1)
    m=(p[i]>p[i-1])&(p[i]>p[i+1])&(p[i]>=0.1*p.max())
    xs=X[i[m]]
    return len(xs),(np.diff(xs).mean() if len(xs)>1 else np.nan)
print("== 1. no noise ==")
th=om*L
Rs2=slitR(th,2); Rs1=slitR(th,1)
s=np.median((Rs2.sum(0)**2).sum(-1)); print("s (median |R_ABC|^2) =",s)
for name,Rs,ro in [('R2',Rs2,'R2'),('R4',Rs2,'R4'),('RS',Rs2,'RS'),('C-arrow',Rs1,'R2')]:
    P=Pall(Rs,ro,s); k2,k3,I2,I3=measures(P)
    print(f"{name:8s} kappa2={k2:.6f} kappa3={k3:.3e}  max|I3|={np.abs(I3).max():.3e}")
    if name=='R2': PR2=P
    if name=='C-arrow': PAr=P
    if name=='R4': PR4=P; I3R4=I3
    if name=='RS': PRS=P
# C+
Pc={c:np.full(len(X),5.0*len(c)) for c in configs}
k2,k3,I2,I3=measures(Pc)
print("C+ kappa2=",k2," max|I2|=",max(np.abs(v).max() for v in I2.values())," max|I3|=",np.abs(I3).max()," kappa3=",k3)
print("== 2. fringes ==")
for nm,P in [('R2',PR2),('C-arrow',PAr)]:
    print(nm,"ABC",maxima(P[(0,1,2)]),"AB",maxima(P[(0,1)]),"AC",maxima(P[(0,2)]))
print("ratio arrow/R2 (AB) =",maxima(PAr[(0,1)])[1]/maxima(PR2[(0,1)])[1])
# small-angle prediction of spacing: period of doubled angle 2*om*dL = 2pi -> dL = 5 ; arrow dL=10
print("far-field prediction spacing AB: R2",5*D2/100," arrow",10*D2/100, "(paraxial, d=100)")
print("== 3. closed forms ==")
sI=(Rs2**2).sum(-1); p=lambda i,j:2*(Rs2[i]*Rs2[j]).sum(-1)
cf=2*(sI[0]*p(1,2)+sI[1]*p(0,2)+sI[2]*p(0,1)+p(0,1)*p(0,2)+p(0,1)*p(1,2)+p(0,2)*p(1,2))
print("R4 I3 closed form max abs diff:",np.abs(cf-I3R4).max()," scale",np.abs(I3R4).max())
r2=1.7; f4=lambda n:(n*n*r2)**2
print("R4 equal in-phase: I3/r^4=",(f4(3)-3*f4(2)+3*f4(1))/r2**2," I2/r^4=",(f4(2)-2*f4(1))/r2**2)
u=0.37; g=lambda n:1-np.exp(-n*n*u)
print("RS equal in-phase: I3 direct",g(3)-3*g(2)+3*g(1)," claimed",1-np.exp(-9*u)+3*np.exp(-4*u)-3*np.exp(-u),
      "| I2 direct",g(2)-2*g(1)," claimed",2*np.exp(-u)-np.exp(-4*u)-1)
print("== 5c. conservation ==")
tot={c:PR2[c].sum() for c in configs}
print("screen totals R2:",{''.join('ABC'[i] for i in c):round(v,1) for c,v in tot.items()})
print("sum singles=",tot[(0,)]+tot[(1,)]+tot[(2,)]," ABC=",tot[(0,1,2)]," mean P_ABC=",PR2[(0,1,2)].mean())
print("|R_slit|^2 range over screen:",sI.min(),sI.max(),"  per slit means",sI.mean(-1))
print("incoherent floor mean P_ABC = 15 ; ratio",PR2[(0,1,2)].mean()/15)
# wider screen check of the 'forward lobe' explanation
Xw=np.arange(-20000,20001,7).astype(float)
Lw=np.sqrt(D1**2+Y[:,None]**2)+np.sqrt(D2**2+(Xw[None,:]-Y[:,None])**2)
Rw=slitR(om*Lw,2); print("wide screen (|x|<=20000, step 7): mean |R_A|^2 =",(Rw[0]**2).sum(-1).mean(),
      " mean P_ABC =",((Rw.sum(0))**2).sum(-1).mean()," (15 = conserved-on-average value)")
print("== 4. noise ==")
rng=np.random.default_rng(987654321)
sig=[0,0.001,0.002,0.003,0.005,0.007,0.01,0.015,0.02,0.03,0.05,0.1,0.2,0.5,1.0,np.pi/2]
ND=2000; CH=100
# analytic prediction for reading A (infinite draws): E|R|^2 = n + sum_{h!=h'} cos(2om(L-L')) exp(-2 sig^2 (L+L'))
def predA(sg):
    P={}
    c2=np.cos(2*th); s2=np.sin(2*th)
    for c in configs:
        if not c: P[c]=np.zeros(len(X)); continue
        idx=np.where(np.isin(slit,c))[0]
        d=np.exp(-2*sg**2*L[idx])           # per-history amplitude decay
        Rx=(d*c2[idx]).sum(0); Ry=(d*s2[idx]).sum(0)
        P[c]=Rx**2+Ry**2+(1-d**2).sum(0)
    return measures(P)[:2]
print(" sigma    A:k2(2000) A:k3      A:k2(200)  A:k3(200) | predA k2  exp(-4s^2L) | B:k2 mean  sd     B:k3 max  | meanP_ABC")
for sg in sig:
    acc={c:np.zeros(len(X)) for c in configs}; acc200=None
    k2B=[];k3B=[]
    for ch in range(ND//CH):
        xi=rng.standard_normal((CH,15,len(X)))
        thn=th[None]+sg*np.sqrt(L)[None]*xi
        Rs=slitR(thn,2)       # (3,CH,nx,2)
        P=Pall(Rs,'R2')
        k2,k3,_,_=measures(P); k2B+=list(k2); k3B+=list(k3)
        for c in configs: acc[c]+=P[c].sum(0)
        if ch==1: acc200={c:acc[c]/200 for c in configs}
    PA={c:acc[c]/ND for c in configs}
    a2,a3,_,_=measures(PA); b2,b3,_,_=measures(acc200)
    p2,p3=predA(sg)
    print(f"{sg:7.4f}  {a2:8.4f}  {a3:.1e}  {b2:8.4f}  {b3:.1e} | {p2:8.4f}  {np.exp(-4*sg**2*L.mean()):.4f}     | {np.mean(k2B):.4f}  {np.std(k2B):.4f}  {np.max(k3B):.1e} | {PA[(0,1,2)].mean():.2f}")
# correlated-jitter variant (outside the rule; caveat f): histories through the same slit grain share the source->slit leg jitter
print("== 5f. variant NOT in the rule: shared first-leg jitter per slit grain is identical to rule (one history per (y,x)); ")
print("   but a common jitter across all 15 histories (fully shared route) leaves kappa2 unchanged:")
xi=rng.standard_normal((200,1,len(X)))*np.ones((1,15,1))
P=Pall(slitR(th[None]+0.05*np.sqrt(L)[None]*xi,2),'R2'); PA={c:P[c].mean(0) for c in configs}
print("   sigma=0.05 common-mode jitter: reading A kappa2=",measures(PA)[0])
# sensitivity to omega (fringe count / lobes)
print("== sensitivity: omega variants (R2 kappa2, ABC maxima) ==")
for o in [np.pi/5,np.pi/4,np.pi/7,1.0,np.pi]:
    P=Pall(slitR(o*L,2),'R2'); print(f"   omega={o:.4f} kappa2={measures(P)[0]:.4f} kappa3={measures(P)[1]:.1e} maxima ABC={maxima(P[(0,1,2)])} meanP={P[(0,1,2)].mean():.1f}")
print("runtime",time.time()-t0)
