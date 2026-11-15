import numpy as np
rng=np.random.default_rng(1)
def I3(P,a,b,c,ext=None):
    return P(a+b+c)-P(a+b)-P(a+c)-P(b+c)+P(a)+P(b)+P(c)
n2=lambda R:(R**2).sum(-1)
N=10000
a,b,c=[rng.uniform(-3,3,(N,2)) for _ in range(3)]
e=np.array([1.,0.])
fs={'|R|^2':n2,'aniso':lambda R:R[...,0]**2+3*R[...,1]**2+R[...,0]*R[...,1],'|R|^2+e.R':lambda R:n2(R)+R@e,
 '1-exp':lambda R:1-np.exp(-n2(R))}
for p in [1,1.5,2.5,3,4]: fs['|R|^%g'%p]=(lambda p:lambda R:n2(R)**(p/2))(p)
print("1. claimed numerics: max|I3|/max|P|")
for k,P in fs.items():
    allP=np.concatenate([P(x) for x in (a+b+c,a+b,a+c,b+c,a,b,c)])
    print('  %-10s %.3g   minP=%.3g'%(k,np.abs(I3(P,a,b,c)).max()/np.abs(allP).max(),allP.min()))
# 2. base point: Delta^3 P(x) = I3(a,b,c+x)-I3(a,b,x) for arbitrary P
P=lambda R:np.sin(R[...,0])*np.exp(R[...,1])+n2(R)**1.3
x=rng.uniform(-3,3,(N,2))
d3=P(x+a+b+c)-P(x+a+b)-P(x+a+c)-P(x+b+c)+P(x+a)+P(x+b)+P(x+c)-P(x)
print("2. base-point identity residual:",np.abs(d3-(I3(P,a,b,c+x)-I3(P,a,b,x))).max())
# 3. saturation: kappa = I3/(|I12|+|I13|+|I23|) for 1-exp(-|R|^2/s), |R_i|~1
a1,b1,c1=[rng.uniform(-1,1,(N,2)) for _ in range(3)]
print("3. saturation P=1-exp(-|R|^2/s): median |I3|/sum|I2|, times s")
for s in [10,100,1000,1e4]:
    P=lambda R:-np.expm1(-n2(R)/s)
    I2=lambda u,v:P(u+v)-P(u)-P(v)
    k=np.abs(I3(P,a1,b1,c1))/(np.abs(I2(a1,b1))+np.abs(I2(a1,c1))+np.abs(I2(b1,c1)))
    print('  s=%-7g median=%.3g  median*s=%.3g  max*s=%.3g'%(s,np.median(k),np.median(k)*s,k.max()*s))
# 4. sensitivity to exponent: P=|R|^(2+eps)
print("4. P=|R|^(2+eps): median and max kappa / eps")
for eps in [1e-1,1e-2,1e-3]:
    P=lambda R:n2(R)**(1+eps/2)
    I2=lambda u,v:P(u+v)-P(u)-P(v)
    k=np.abs(I3(P,a1,b1,c1))/(np.abs(I2(a1,b1))+np.abs(I2(a1,c1))+np.abs(I2(b1,c1)))
    print('  eps=%g  median/eps=%.3g  max/eps=%.3g'%(eps,np.median(k)/eps,k.max()/eps))
# 5. history-count escape: state (R,n) additive. P = beta|R|^2+alpha n+gamma n^2 ; and n^2-|R|^2 (|R_i|<=n_i)
print("5. P=g(|R|^2,n), n additive")
ns=[rng.integers(1,6,N).astype(float) for _ in range(3)]
def unit(N):
    v=rng.normal(size=(N,2));r=rng.uniform(0,1,N)**.5
    return v/np.linalg.norm(v,axis=1)[:,None]*r[:,None]
Rs=[unit(N)*n[:,None] for n in ns]
def I3g(g):
    (A,B,C),(na,nb,nc)=Rs,ns
    return g(A+B+C,na+nb+nc)-g(A+B,na+nb)-g(A+C,na+nc)-g(B+C,nb+nc)+g(A,na)+g(B,nb)+g(C,nc)
for name,g in [('|R|^2+0.7n',lambda R,n:n2(R)+.7*n),('n^2-|R|^2',lambda R,n:n*n-n2(R)),('|R|^2+n+0.3n^2',lambda R,n:n2(R)+n+.3*n*n),
               ('|R|^2/n (non-quadratic)',lambda R,n:n2(R)/n),('|R|^2*n',lambda R,n:n2(R)*n),('sqrt(n)|R|',lambda R,n:np.sqrt(n*n2(R)**.5))]:
    print('  %-26s max|I3|=%.3g'%(name,np.abs(I3g(g)).max()))
# 6. restricted domain: all |R_i|=1 (phase-only). polynomial ansatz f(s)=sum c_k s^k, k=1..8, s=|R|^2. null space of I3 constraints
th=rng.uniform(0,2*np.pi,(400,3))
u=[np.stack([np.cos(th[:,i]),np.sin(th[:,i])],1) for i in range(3)]
K=range(0,9)
M=np.stack([I3(lambda R:n2(R)**k,*u) for k in K],1)
sv=np.linalg.svd(M,compute_uv=False)
print("6. unit-phasor-only domain, f(|R|^2) polynomial deg<=8 incl. constant: singular values\n  ",np.array2string(sv/sv[0],precision=2))
# 7. Hamel-type pathology on a Q-subspace: f additive over Q-span{1,sqrt2}: f(p+q sqrt2)=p-q ; P=f(x)^2 (1-D illustration)
p,q=[rng.integers(-50,50,(N,3)) for _ in range(2)]
f=lambda p,q:(p-q)**2
i3=f(p.sum(1),q.sum(1))-sum(f(p[:,i]+p[:,j],q[:,i]+q[:,j]) for i,j in [(0,1),(0,2),(1,2)])+sum(f(p[:,i],q[:,i]) for i in range(3))
xs=p[:,0]+q[:,0]*2**.5; sel=np.abs(xs)<0.05
print("7. P(p+q*sqrt2)=(p-q)^2: max|I3|=%d ; on |x|<0.05: max P=%d (true quadratic would give <=%.3g*const)"%(np.abs(i3).max(),f(p[:,0],q[:,0])[sel].max(),0.05**2))
