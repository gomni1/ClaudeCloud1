# N-2026-11-11-2 symbolic part: closed level, restricted determinant vs slope of H at a balance.
import sympy as sp
k1,k2,k5,k6,k7,k8,k10 = sp.symbols('k1 k2 k5 k6 k7 k8 k10', positive=True)
C,V,L,P = sp.symbols('C V L P', positive=True)
rho = sp.Function('rho')
T = C+V+L+P; x = C/T
f = sp.Matrix([-(k1+k2+k7)*C + k6*L + (k10+rho(x))*V,
               k2*C + k5*L + k8*P - (k10+rho(x))*V,
               k1*C - (k5+k6)*L,
               k7*C - k8*P])
y = sp.Matrix([C,V,L,P])
J = f.jacobian(y)
print('column sums zero:', [sp.simplify(sum(J[:,j])) for j in range(4)])
# e3 = sum of principal 3x3 minors
e3 = 0
for drop in range(4):
    idx = [i for i in range(4) if i != drop]
    e3 += J.extract(idx, idx).det()
B = sp.Matrix([[1,0,0],[-1,-1,-1],[0,1,0],[0,0,1]])  # columns eC-eV, eL-eV, eP-eV (order C,V,L,P)
M = (B.T*B).inv()*B.T*J*B
# balance substitution
xs, Ts, r0, r1 = sp.symbols('xs Ts r0 r1', positive=True)
D = k2 + k7 + k1*k5/(k5+k6)
c = 1 + k1/(k5+k6) + k7/k8
sub_state = {C: xs*Ts, L: k1*xs*Ts/(k5+k6), P: k7*xs*Ts/k8, V: Ts*(1-c*xs)}
def at_bal(e):
    # replace rho(x) and rho'(x) wherever they appear
    e = e.replace(lambda a: isinstance(a, sp.Subs), lambda a: sp.Symbol('RP'))
    e = e.replace(lambda a: isinstance(a, sp.Derivative), lambda a: sp.Symbol('RP'))
    e = e.replace(lambda a: a.func == rho, lambda a: sp.Symbol('R0'))
    e = e.subs(sub_state)
    r0val = D*xs/(1-c*xs) - k10
    return sp.simplify(e.subs({sp.Symbol('R0'): r0val, sp.Symbol('RP'): r1}))
e3b = at_bal(e3); detMb = at_bal(M.det())
print('e3 - det M at balance:', sp.simplify(e3b - detMb))
r0val = D*xs/(1-c*xs) - k10
Hp = r1*(1-c*xs) - c*(k10+r0val) - D
q = sp.simplify(e3b/Hp)
print('q =', sp.factor(q))
print('dq/dr1 =', sp.simplify(sp.diff(q, r1)))
# sign test: write in u = 1 - c*x with x eliminated? Use direct factor and positivity check
num, den = sp.fraction(sp.factor(q))
print('numerator:', sp.factor(num)); print('denominator:', sp.factor(den))
# planted P1: H' wrong
Hw = Hp + c*(k10+r0val)
qw = sp.simplify(e3b/Hw)
print('P1 dqw/dr1 is zero?', sp.simplify(sp.diff(qw, r1)) == 0)
