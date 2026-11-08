"""Q3: pi -> l nu with the uniform count and one pairwise orientation weight on (l, nu)."""
import sympy as sp
from mpmath import mp, mpf, sqrt

mp.dps = 30
m_pi, m_mu, m_e = mpf("139.57039"), mpf("105.6583755"), mpf("0.51099895")


def kin(ml):
    p = (m_pi**2 - ml**2) / (2 * m_pi)
    E = (m_pi**2 + ml**2) / (2 * m_pi)
    return p, E, p / E


pe, Ee, be = kin(m_e)
pm, Em, bm = kin(m_mu)
# uniform count N = 4 pi p^2 / |d(E_l+E_nu)/dp| = 4 pi p^2 E_l / m_pi
Ne_over_Nmu = (pe**2 * Ee) / (pm**2 * Em)
print(f"beta_e = {float(be):.9f}   beta_mu = {float(bm):.9f}")
print(f"N_e/N_mu (uniform count) = {float(Ne_over_Nmu):.6f}")

# back to back, neutrino speed 1:  v_l . v_nu = -beta_l
W = {"ALIGNED": lambda b: (1 - b) / 2, "OPPOSED": lambda b: (1 + b) / 2}
R = {}
for k, w in W.items():
    R[k] = Ne_over_Nmu * w(be) / w(bm)
    print(f"{k:8s}: W_e = {float(w(be)):.6e}  W_mu = {float(w(bm)):.6e}  W_e/W_mu = {float(w(be)/w(bm)):.6e}  R = {float(R[k]):.6e}")

closed = (m_e / m_mu)**2 * ((m_pi**2 - m_e**2) / (m_pi**2 - m_mu**2))**2
print(f"closed form (m_e/m_mu)^2[(m_pi^2-m_e^2)/(m_pi^2-m_mu^2)]^2 = {float(closed):.10e}")
print(f"ALIGNED minus closed form (30-digit arithmetic) = {float(R['ALIGNED'] - closed):.3e}")

# symbolic identity
M, ml1, ml2 = sp.symbols("M m1 m2", positive=True)
def sym(ml):
    p = (M**2 - ml**2) / (2 * M); E = (M**2 + ml**2) / (2 * M)
    return p, E, (1 - p / E) / 2
p1, E1, w1 = sym(ml1); p2, E2, w2 = sym(ml2)
ratio = (p1**2 * E1 * w1) / (p2**2 * E2 * w2)
target = (ml1 / ml2)**2 * ((M**2 - ml1**2) / (M**2 - ml2**2))**2
print("sympy: ALIGNED ratio - closed form simplifies to", sp.simplify(ratio - target))
print("sympy: ALIGNED weight W_l =", sp.simplify(w1), "  OPPOSED weight =", sp.simplify(1 - w1))

# observation (PIENU 2015) and SM control (Cirigliano & Rosell 2007)
R_exp, s_stat, s_sys = 1.2344e-4, 0.0023e-4, 0.0019e-4
s_exp = (s_stat**2 + s_sys**2) ** 0.5
R_SM = 1.2352e-4
Ra = float(R["ALIGNED"]); Rb = float(R["OPPOSED"])
print(f"\nPIENU R = {R_exp:.4e} +/- {s_exp:.4e} (stat+syst in quadrature)")
print(f"ALIGNED/PIENU = {Ra / R_exp:.5f}   pull = {(Ra - R_exp) / s_exp:+.1f} sigma")
print(f"OPPOSED/PIENU = {Rb / R_exp:.4e}")
print(f"[control] SM R = {R_SM:.4e};  SM/tree = {R_SM / Ra:.5f}  -> radiative correction {100 * (R_SM / Ra - 1):+.3f} %")
print(f"[control] SM vs PIENU pull = {(R_SM - R_exp) / s_exp:+.2f} sigma")
