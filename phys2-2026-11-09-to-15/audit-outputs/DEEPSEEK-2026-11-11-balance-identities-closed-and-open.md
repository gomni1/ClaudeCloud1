# DeepSeek verification — balance identities on closed and open levels

Received 11 Nov 2026 (relayed by Glenn). Answers the first verification handoff of NIGHT-REPORT-2026-11-11 (§8), on item N-2026-11-11-2 and the 10 Nov open-level result. Sections 1–3 below are DeepSeek's text as received, in its own LaTeX notation, unedited. Section 0 is Claude's note.

## 0. Claude's note (11 Nov 2026)

Verdict: confirmed. Claude worked through the algebra of all four parts and agrees with each step.

Independent numerical check (Claude, sympy, 40-digit arithmetic): 12 randomly drawn rate sets, seed 7, rates as random rationals, recruitment law rho(x) = k3·x^m/(h^m + x^m) with m in 2..6. At every balance found, 12 closed and 12 open, the relative difference between the two sides of each identity was below 3e-40. The law used is a smooth saturating one, not the binomial threshold law of the night run; the identities are stated for any differentiable rho, so this tests the claim, but it is not a re-run of the night's draws.

One slip in the received text, with no effect on the result: part 2 calls e_3 "the coefficient of lambda" in det(lambda·I − J). It is minus that coefficient; the same sign appears in det(lambda·I − J|_W), so e_3 = det(J|_W) stands.

Not covered by this file: the count of closed draws with no stable balance (5 in 20 000), and what those levels do. The second handoff of the same report (integrate the m = 19, kr = 3 draw) has not been returned.

## 1. Notation

For the closed system put

B=k_5+k_6,\quad A=k_1+k_2+k_7,\quad 
D=k_2+k_7+\frac{k_1k_5}{B},

a=\frac{k_1}{B},\quad b=\frac{k_7}{k_8},\quad c=1+a+b.

At a balance let

x=x_*,\quad R=k_{10}+\rho(x),\quad r=\rho'(x),\quad 
v=\frac VT=1-cx.

The closed balance condition gives

Rv=Dx. \tag{1}

Also

\frac{\partial \rho}{\partial(C,V,L,P)}
=\frac rT(1-x,-x,-x,-x)^T.

Since V/T=v, the term involving r becomes independent of T:

V\frac{\partial\rho}{\partial(C,V,L,P)}
=vr\,(1-x,-x,-x,-x).

---

## 2. DeepSeek's four parts

1. Closed system: proof of

e_3=k_8(k_5+k_6)H'(x_*)=k_8B\,H'(x_*).

Write the Jacobian as

J=J_0+\varepsilon\,u s^T,

where

\varepsilon=vr,\qquad u=(1,-1,0,0)^T,\qquad
s=(1-x,-x,-x,-x)^T,

and

J_0=
\begin{pmatrix}
-A&R&k_6&0\\
k_2&-R&k_5&k_8\\
k_1&0&-B&0\\
k_7&0&0&-k_8
\end{pmatrix}.

The matrix J_0 is the Jacobian obtained by ignoring the derivative of \rho; the derivative of \rho contributes the rank-one term \varepsilon us^T.

A direct computation of the four principal 3\times3 minors of J_0 gives

\begin{aligned}
M_{\hat C}&=-RBk_8,\\
M_{\hat V}&=-k_8(AB-k_1k_6)=-k_8BD,\\
M_{\hat L}&=-Rk_1k_8,\\
M_{\hat P}&=-RBk_7.
\end{aligned}

Hence

e_3(J_0)
=-RBk_8-k_8BD-Rk_1k_8-RBk_7
=-k_8B(cR+D). \tag{2}

Indeed,

k_8B c=k_8B+k_8k_1+Bk_7.

Now differentiate the four principal minors with respect to the rank-one parameter \varepsilon. One obtains

\begin{aligned}
\partial_\varepsilon M_{\hat C}&=xBk_8,\\
\partial_\varepsilon M_{\hat V}&=k_8B(1-cx),\\
\partial_\varepsilon M_{\hat L}&=xk_1k_8,\\
\partial_\varepsilon M_{\hat P}&=xBk_7.
\end{aligned}

Their sum is

xBk_8+k_8B(1-cx)+xk_1k_8+xBk_7
=k_8B.

Thus

e_3(J)=e_3(J_0)+\varepsilon k_8B
=k_8B\bigl[-(cR+D)+vr\bigr].

But

H(x)=R(x)(1-cx)-Dx,

so

H'(x)=r(1-cx)-cR-D=rv-cR-D.

Therefore

\boxed{e_3(J)=k_8B\,H'(x_*)=k_8(k_5+k_6)H'(x_*).}

The claim is true for every differentiable \rho\ge0, every positive balance, and every T>0.

---

2. e_3 as the product of the restricted eigenvalues

Let

W=\{(\delta C,\delta V,\delta L,\delta P):\delta C+\delta V+\delta L+\delta P=0\}.

Because the total T=C+V+L+P is conserved, the column sums of J are zero, hence

J(W)\subseteq W.

The right zero eigenvector produced by homogeneity is

y_*=\left(x,1-cx,\frac{k_1x}{B},\frac{k_7x}{k_8}\right)^T,

and its component sum is

x+(1-cx)+\frac{k_1x}{B}+\frac{k_7x}{k_8}=1.

Thus y_*\notin W. Therefore

\mathbb R^4=W\oplus \operatorname{span}(y_*),

and relative to this decomposition,

J=\begin{pmatrix}J|_W&0\\0&0\end{pmatrix}.

Consequently

\det(\lambda I-J)=\lambda\,\det(\lambda I-J|_W).

The coefficient e_3 is the coefficient of \lambda in the characteristic polynomial, so

\boxed{e_3=\det(J|_W)=\prod_{\text{three eigenvalues of }J|_W}\lambda_i.}

So part 2 is confirmed. If e_3\neq0, the restricted eigenvalues are exactly the three eigenvalues of J besides the zero eigenvalue coming from the conserved total. If e_3=0, there is an additional zero eigenvalue in W, but the determinant/product identity remains valid.

---

3. Three simple roots of H

Assume

0<x_a<x_b<x_c<1/c,\qquad H(x_i)=0,

with simple roots, and

H(0)=k_{10}+\rho(0)>0,\qquad
H(1/c)=-D/c<0.

Because the roots are simple, H changes sign at each root. Since H(0)>0, the signs alternate:

H'(x_a)<0,\qquad H'(x_b)>0,\qquad H'(x_c)<0.

By the identity of part 1,

e_3(x_a)<0,\qquad e_3(x_b)>0,\qquad e_3(x_c)<0.

At the middle balance x_b, the restricted 3\times3 matrix J|_W is real, so it has at least one real eigenvalue. Its eigenvalue product is e_3>0. Therefore either all three eigenvalues are real with product positive, or there is one real eigenvalue and a complex conjugate pair. In both cases there is at least one positive real eigenvalue in W. Thus the middle balance is unstable; in fact it always has a positive real eigenvalue within the conserved-total subspace.

At the outer roots, e_3<0. Since a real 3\times3 matrix has at least one real eigenvalue, the negative product implies that each outer balance has at least one negative real eigenvalue in W. This does not by itself imply stability: the other two eigenvalues could be positive real, or a complex pair with positive real part. So the only plain conclusion is:

· x_b: always has a positive real eigenvalue in W.
· x_a,x_c: each has at least one negative real eigenvalue in W; no general stability conclusion follows from the sign of e_3 alone.

---

4. Open-level counterpart

The open system is

\begin{aligned}
\dot C&=-(k_1+k_2+k_7)C+k_6L+(k_{10}+\rho(x))V,\\
\dot V&=k_2C+k_5L+k_8P-(k_{10}+\rho(x))V+k_{12},\\
\dot L&=k_1C-(k_5+k_6)L,\\
\dot P&=k_7C-(k_8+k_9)P.
\end{aligned}

Put

K=k_8+k_9,\qquad R=k_{10}+\rho(x_*),\qquad r=\rho'(x_*),

and

x=\frac{C_*}{T_*},\qquad v=\frac{V_*}{T_*},\qquad T_*=C_*+V_*+L_*+P_*.

At the open balance,

L_*=\frac{k_1}{B}C_*,\qquad
P_*=\frac{k_7}{K}C_*,\qquad
RV_*=DC_*,

and

C_*=\frac{Kk_{12}}{k_7k_9}.

The Jacobian again has the form

J=J_0+\varepsilon us^T,\qquad \varepsilon=vr,

with u=(1,-1,0,0)^T, s=(1-x,-x,-x,-x)^T, and

J_0=
\begin{pmatrix}
-A&R&k_6&0\\
k_2&-R&k_5&k_8\\
k_1&0&-B&0\\
k_7&0&0&-K
\end{pmatrix}.

A direct determinant computation gives

\det J_0=k_7k_9BR.

Also J_0 z=u has solution

z=(0,1/R,0,0)^T,

so

s^Tz=-\frac{x}{R}.

By the matrix determinant lemma,

\begin{aligned}
\det J
&=\det J_0\bigl(1+\varepsilon s^TJ_0^{-1}u\bigr)\\
&=k_7k_9BR\left(1-\varepsilon\frac{x}{R}\right)\\
&=k_7k_9B(R-vrx).
\end{aligned}

Now

g(V)=\left(k_{10}+\rho\left(\frac{C_*}{C_*+L_*+P_*+V}\right)\right)V.

At V=V_*,

\frac{d}{dV}\frac{C_*}{C_*+L_*+P_*+V}
=-\frac{x}{T_*},

so

g'(V_*)=R+V_*r\left(-\frac{x}{T_*}\right)
=R-vrx.

Therefore

\boxed{\det J=k_7k_9B\,g'(V_*)
=k_7k_9(k_5+k_6)g'(V_*).}

So the open-level identity is also true.

Relation between the two identities

They share the same underlying mechanism: the dependence of \rho on x=C/T enters the Jacobian as a rank-one perturbation

vr\,u s^T,

and the balance equations make the relevant adjugate response simple. In the closed case the conserved total produces a zero eigenvalue, so the natural quantity is the coefficient e_3, equivalently the determinant on the invariant subspace W. In the open case there is no conserved total, so the natural quantity is the full 4\times4 determinant. Thus the two are not literally the same identity, but they are two coefficient-level consequences of the same rank-one chain-rule structure.

---

## 3. DeepSeek's final verdict and confidence

1. Closed identity
   e_3=k_8(k_5+k_6)H'(x_*)
   is true. Proof above.
2. e_3=\det(J|_W)= product of the three restricted eigenvalues is true, because J(W)\subset W and the homogeneity zero eigenvector y_* lies outside W.
3. With three simple roots, the signs are
   H'(x_a)<0,\qquad H'(x_b)>0,\qquad H'(x_c)<0.
   The middle balance always has a positive real eigenvalue in W. Each outer balance has at least one negative real eigenvalue in W, but no general stability conclusion follows.
4. The open-level determinant identity is true:
   \det J=k_7k_9(k_5+k_6)g'(V_*).
   It shares the rank-one \rho(x) mechanism with the closed result, but is a separate determinant-level identity rather than a specialization of the closed e_3 identity.

Confidence: high for all algebraic parts and sign conclusions. The main hidden assumptions are positivity of the rates, T>0, differentiability of \rho, and, in part 3, simplicity of the three roots and absence of additional roots in the stated interval.
