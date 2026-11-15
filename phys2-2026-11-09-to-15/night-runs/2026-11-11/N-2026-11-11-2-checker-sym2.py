import sympy as sp
C,V,L,P=sp.symbols('C V L P',positive=True)
k1,k2,k5,k6,k7,k8,k10,T,x=sp.symbols('k1 k2 k5 k6 k7 k8 k10 T x',positive=True)
rho=sp.Function('rho')
Tt=C+V+L+P; X=C/Tt
f=sp.Matrix([-(k1+k2+k7)*C+k6*L+(k10+rho(X))*V,
 k2*C+k5*L+k8*P-(k10+rho(X))*V,
 k1*C-(k5+k6)*L, k7*C-k8*P])
J=f.jacobian([C,V,L,P])
c=1+k1/(k5+k6)+k7/k8; D=k2+k7+k1*k5/(k5+k6)
r,rp=sp.symbols('r rp')
sub={C:x*T,L:k1*x*T/(k5+k6),P:k7*x*T/k8,V:T*(1-c*x)}
Js=J.subs(sub).doit()
Js=Js.replace(lambda e: isinstance(e,sp.Subs) or isinstance(e,sp.Derivative), lambda e: rp)
Js=Js.subs(rho(x),r)
# replace rho(anything simplifying to x)
Js=Js.applyfunc(lambda e: e.replace(rho, lambda a: r))
Js=sp.simplify(Js)
print(Js.free_symbols)
# check column sums zero
print([sp.simplify(sum(Js[:,j])) for j in range(4)])

import itertools
e3=sum(Js.extract(list(i),list(i)).det() for i in itertools.combinations(range(4),3))
R=sp.Function('R')
H=(k10+R(x))*(1-c*x)-D*x
Hp=sp.diff(H,x).subs(sp.Derivative(R(x),x),rp).subs(R(x),r)
print('e4',sp.cancel(Js.det()))
print('ratio',sp.cancel(sp.together(e3/(k8*(k5+k6)*Hp))))
print('planted',sp.cancel(sp.together(e3/(k8*(k5+k6)*(Hp+c*(k10+r))))))
B=sp.Matrix([[1,0,0],[-1,1,1],[0,-1,0],[0,0,-1]])
Bp=(B.T*B).inv()*B.T
print('restr',sp.cancel(sp.together((Bp*Js*B).det()/(k8*(k5+k6)*Hp))))
print(Js)
