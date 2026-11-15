"""Q5: neutron decay, (e, nubar) weight mixing ALIGNED (share alpha) and OPPOSED (share 1-alpha)."""
import numpy as np
import sympy as sp
from scipy import integrate

# ---------- (a) a = 2 alpha - 1 (symbolic) ----------
al, c = sp.symbols("alpha c", real=True)          # c = v_e . v_nu = beta_e cos(theta)
W = al * (1 + c) / 2 + (1 - al) * (1 - c) / 2
print("(a) W =", sp.collect(sp.expand(W), c), " = (1/2)(1 + a c) with a =", sp.simplify(2 * sp.expand(W).coeff(c, 1)))

# ---------- (b) alpha from aSPECT ----------
for label, a, da in (("aSPECT 2020 (PRC 101, 055506)", -0.10430, 0.00084),
                     ("aSPECT reanalysis (arXiv:2308.16170)", -0.10402, 0.00082)):
    print(f"(b) {label}: a = {a} +/- {da}  ->  alpha = (1+a)/2 = {(1 + a) / 2:.5f} +/- {da / 2:.5f}")
alpha = (1 - 0.10430) / 2

# ---------- (c) <W> over the uniform count ----------
th = sp.symbols("theta")
print("(c) heavy recoil: angular measure dOmega_e dOmega_nu is isotropic; integral of cos(theta) over the relative angle =",
      sp.integrate(sp.cos(th) * sp.sin(th), (th, 0, sp.pi)), "-> <W> = 1/2 for every alpha")

m_n, m_p, m_e = 939.56542052, 938.27208816, 0.51099895
m_mu = 105.6583755
Delta = m_n - m_p
aem = 1 / 137.035999084


def N_exact(weight=lambda pe, Ee, Enu, cth: 1.0):
    """Uniform count with full proton recoil: int d3pe d3pnu delta(M - Ee - Enu - Ep)."""
    Eemax = (m_n**2 + m_e**2 - m_p**2) / (2 * m_n)
    pmax = np.sqrt(Eemax**2 - m_e**2)

    def inner(cth, pe):
        Ee = np.sqrt(pe**2 + m_e**2); A = m_n - Ee
        Enu = (A**2 - m_p**2 - pe**2) / (2 * (A + pe * cth))
        if Enu <= 0:
            return 0.0
        Ep = A - Enu
        jac = 1 + (Enu + pe * cth) / Ep
        return 8 * np.pi**2 * pe**2 * Enu**2 / jac * weight(pe, Ee, Enu, cth)

    val, err = integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)
    return val


N0 = N_exact()
Nbc = N_exact(lambda pe, Ee, Enu, cth: (pe / Ee) * cth)
mean_bc = Nbc / N0
print(f"(c) full recoil: <beta_e cos theta> over uniform count = {mean_bc:.3e}")
print(f"    -> <W> = 1/2 + (2 alpha - 1)<beta cos>/2 = {0.5 + (2 * alpha - 1) * mean_bc / 2:.8f}  (alpha = {alpha:.5f})")

# ---------- anchors: reproduce the stated 4.2211e8, 1.0557 and 1.0211 ----------
def N3(M, m1, m3, fermi=False):
    """Uniform count int d3p1 d3p2 d3p3 delta^4 with daughter 2 massless (full recoil)."""
    E1max = (M**2 + m1**2 - m3**2) / (2 * M); pmax = np.sqrt(E1max**2 - m1**2)

    def inner(cth, p):
        E1 = np.sqrt(p * p + m1 * m1); A = M - E1
        E2 = (A * A - m3 * m3 - p * p) / (2 * (A + p * cth))
        if E2 <= 0:
            return 0.0
        E3 = A - E2
        F = 1.0
        if fermi and p > 0:
            eta = aem * E1 / p
            F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
        return 8 * np.pi**2 * p * p * E2 * E2 / (1 + (E2 + p * cth) / E3) * F
    return integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)[0]


def N_heavy(E0, fermi=False):
    def f(Ee):
        pe = np.sqrt(Ee**2 - m_e**2)
        F = 1.0
        if fermi:
            eta = aem * Ee / pe
            F = 2 * np.pi * eta / (1 - np.exp(-2 * np.pi * eta))
        return 16 * np.pi**2 * pe * Ee * (E0 - Ee)**2 * F
    return integrate.quad(f, m_e, E0, epsabs=0, epsrel=1e-12)[0]


obs = 878.4 / 2.1969811e-6
N_mu = N3(m_mu, m_e, 0.0)                    # massive e, massless neutrinos
N_n, N_nF = N3(m_n, m_e, m_p), N3(m_n, m_e, m_p, fermi=True)
print(f"\nobserved Gamma_mu/Gamma_n = tau_n/tau_mu = {obs:.6e}")
print(f"   full kinematics: N_mu/N_n = {N_mu / N_n:.5e}  miss = {N_mu / N_n / obs:.5f};  with NR Fermi: miss = {N_mu / N_nF / obs:.5f}")
print(f"   (heavy-recoil variant for reference: miss = {7*np.pi**2*m_mu**5/240 / N_heavy(Delta) / obs:.5f}; "
      f"NR Fermi {7*np.pi**2*m_mu**5/240 / N_heavy(Delta, True) / obs:.5f})")
miss0 = N_mu / N_n / obs
missF = N_mu / N_nF / obs

# ---------- (d) muon weight = Michel-matching case (<W_mu> = 5/7), neutron <W_n> = 1/2 ----------
Wmu, Wn = 5 / 7, 1 / 2
print(f"\n(d) <W_mu>/<W_n> = {Wmu / Wn:.6f}")
print(f"    new miss (no Coulomb)     = {miss0:.5f} x {Wmu / Wn:.5f} = {miss0 * Wmu / Wn:.5f}")
print(f"    new miss (NR Fermi, Z=1)  = {missF:.5f} x {Wmu / Wn:.5f} = {missF * Wmu / Wn:.5f}")
print(f"    required neutron parent-side factor F_n = {miss0 * Wmu / Wn:.4f} (no Coulomb) / {missF * Wmu / Wn:.4f} (NR Fermi)")
print(f"    equivalently <W_n> would have to be {Wn * miss0 * Wmu / Wn:.4f} / {Wn * missF * Wmu / Wn:.4f} instead of 0.5")

# ---------- [control] Standard Model factor on the same basis ----------
hbar = 6.582119569e-22        # MeV s
GF = 1.1663788e-11            # MeV^-2 (PDG)
Vud, lam = 0.97373, 1.2754    # PDG 2024 (Vud from superallowed; lambda average)
f_full, one_RC = 1.6887, 1.03886   # Czarnecki-Marciano-Sirlin 2018 (f incl. Coulomb, size, recoil)
f0 = N_n / (16 * np.pi**2 * m_e**5)           # PHYS2 neutron count in f units (anchor basis)
fNR = N_nF / (16 * np.pi**2 * m_e**5)
Gmu0 = GF**2 * m_mu**5 / (192 * np.pi**3)
one_dmu = (hbar / 2.1969811e-6) / Gmu0       # muon corrections absorbed when GF is defined
core = Vud**2 * (1 + 3 * lam**2) / 4
F_SM0 = core * f_full * one_RC / f0 / one_dmu
F_SMF = core * f_full * one_RC / fNR / one_dmu
print(f"\n[control] PHYS2 count in f units: no Coulomb = {f0:.5f}, f with NR Fermi = {fNR:.5f}, full SM f = {f_full}")
print(f"[control] muon side 1+delta_mu = {one_dmu:.5f}")
print(f"[control] V_ud^2 = {Vud**2:.5f}, 1+3 lambda^2 = {1 + 3 * lam**2:.5f}, (2/8) V^2(1+3l^2) = {core:.5f}, (1+3l^2)/4 = {(1 + 3 * lam**2) / 4:.5f}")
print(f"[control] SM factor, no-Coulomb basis = {F_SM0:.4f}  (required {miss0 * Wmu / Wn:.4f}; ratio {F_SM0 / (miss0 * Wmu / Wn):.5f})")
print(f"[control] SM factor, NR-Fermi basis   = {F_SMF:.4f}  (required {missF * Wmu / Wn:.4f}; ratio {F_SMF / (missF * Wmu / Wn):.5f})")
print(f"[control] SM tau_n = 4908.6 s / (V^2(1+3l^2)) = {4908.6 / (Vud**2 * (1 + 3 * lam**2)):.2f} s  vs 878.4 s")
# SM link between alpha and lambda: alpha = (1+l^2)/(1+3l^2)
lam_from_alpha = np.sqrt((1 - alpha) / (3 * alpha - 1))
print(f"[control] SM link alpha = (1+l^2)/(1+3l^2): alpha(l=1.2754) = {(1 + lam**2) / (1 + 3 * lam**2):.5f}; "
      f"|l| from aSPECT alpha = {lam_from_alpha:.4f}")

# ---------- electron-mass check on <W_mu> (Q4 used massless daughters) ----------
def N3w(M, m1, m3, w):
    E1max = (M**2 + m1**2 - m3**2) / (2 * M); pmax = np.sqrt(E1max**2 - m1**2)

    def inner(cth, p):
        E1 = np.sqrt(p * p + m1 * m1); A = M - E1
        E2 = (A * A - m3 * m3 - p * p) / (2 * (A + p * cth))
        if E2 <= 0:
            return 0.0
        E3 = A - E2
        return 8 * np.pi**2 * p * p * E2 * E2 / (1 + (E2 + p * cth) / E3) * w(p / E1, cth)
    return integrate.dblquad(inner, 0, pmax, -1, 1, epsabs=0, epsrel=1e-11)[0]


Wmu_me = N3w(m_mu, m_e, 0.0, lambda be, cth: (1 - be * cth) / 2) / N_mu
print(f"\n<W_mu> for OPPOSED(e, nu) with massive electron (Q2: W = (1 - v_e.n_nu)/2) = {Wmu_me:.6f}  (massless 5/7 = {5/7:.6f})")
print(f"   -> new miss with this <W_mu> and <W_n> = 0.5: {miss0 * Wmu_me / 0.5:.5f} (no Coulomb), {missF * Wmu_me / 0.5:.5f} (NR Fermi)")
print(f"[control] consistency of SM constants: 2 pi^3 hbar / (G_F^2 m_e^5 f (1+RC)) = "
      f"{2 * np.pi**3 * hbar / (GF**2 * m_e**5 * f_full * one_RC):.1f} s (CMS 2018 quote: 4908.6 s)")
print(f"[control] SM pieces: f/fNR = {f_full / fNR:.5f}, 1/(1+delta_mu) = {1 / one_dmu:.5f}, "
      f"f(1+RC)/fNR/(1+delta_mu) = {f_full * one_RC / fNR / one_dmu:.5f}")
print(f"[control] old common-W near-agreement in SM terms: 8<W_mu> = {8 * 5 / 7:.4f} vs V^2(1+3l^2) = {Vud**2 * (1 + 3 * lam**2):.4f}")
