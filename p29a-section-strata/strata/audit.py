"""Post-freeze constructions prompted by the proof audit of 27 Oct.

Both live in M = 3, with z = (z2, z3). They are corrections made after the
freeze and change no frozen claim's status.

* retraced_loop: P6(c). An A-B-A loop with exact retracing and T = 1/2, whose
  only identification is at B (R_pi rho_B = rho_B).
* free_passage_loop: P7. A family in psi in which the exit direction of z3 from
  the C2 arc is free, so a flip passage deforms into a non-flip one.
"""
import numpy as np

from .loops import TWO_PI, smooth
from .orientation import wrap
from .sections import rotate

RHO_A = np.array([0.30, 0.20j])          # g = 1
RHO_B = np.array([0.35, 0.0])            # in C2 (g = 2)
RHO_B_C3 = np.array([0.0, 0.35])         # control, in C3


def retraced_loop(rho_A=RHO_A, rho_B=RHO_B):
    """tau from rho_A to rho_B; R_(pi u) rho_B for u in [0, 1]; tau reversed exactly.

    Returns (gamma, joint_gap) with joint_gap = |R_pi rho_B - rho_B|, the jump
    where the rotated B section meets the start of the reversed path.
    """
    def gamma(t):
        x = 3 * (t % TWO_PI) / TWO_PI
        if x < 1:
            s = smooth(x)
            return (1 - s) * rho_A + s * rho_B
        if x < 2:
            return rotate(rho_B, np.pi * smooth(x - 1))
        s = smooth(x - 2)
        return s * rho_A + (1 - s) * rho_B
    return gamma, float(np.linalg.norm(rotate(rho_B, np.pi) - rho_B))


# --- P7 free-passage witness ------------------------------------------------------
#
# Quarters of the loop, x = 4 t / 2 pi:
#   [0, 1) entry: straight from rho_A to rho_B at beta = 0
#   [1, 2) B arc: R_(pi s) rho_B, held in C2 (z3 = 0)
#   [2, 3) exit: straight from rho_B to rho_A^psi = (0.30, e^(i psi) 0.20i)
#   [3, 4) A arc: z3 turned back by -psi, z2 fixed
# The window [0, 3) is written in the frame co-rotating with the B arc
# (beta = 0, pi s, pi), so that a resolution can replace its odd part.

def _beta(x):
    return 0.0 if x < 1 else (np.pi * smooth(x - 1) if x < 2 else np.pi)


def _even_body(x):
    if x < 1:
        s = smooth(x)
        return (1 - s) * RHO_A[0] + s * RHO_B[0]
    if x < 2:
        return RHO_B[0]
    s = smooth(x - 2)
    return (1 - s) * RHO_B[0] + s * RHO_A[0]


def _odd_body_raw(x, psi):
    if x < 1:
        return (1 - smooth(x)) * RHO_A[1]
    if x < 2:
        return 0j
    # lab z3 = s e^(i psi) 0.2i; the body frame is rotated by pi, which flips z3
    return -smooth(x - 2) * np.exp(1j * psi) * RHO_A[1]


def passage(psi):
    """Body-frame angle from the entry direction of z3 to its exit direction.

    Returns (delta, flip, detours): a flip is |delta| = pi exactly, and then
    both minimal detours (+pi, -pi) are taken; otherwise the one detour delta.
    """
    entry = np.angle(RHO_A[1])
    exit_ = np.angle(-np.exp(1j * psi) * RHO_A[1])
    delta = float(wrap(exit_ - entry))
    flip = abs(abs(delta) - np.pi) < 1e-12
    return delta, flip, ([np.pi, -np.pi] if flip else [delta])


def free_passage_loop(psi, detour=None, eps=0.3):
    """The psi-family loop; detour=None is the raw loop through the C2 arc.

    With detour = D, the odd part over the window is replaced by
    amp(w) 0.2 exp(i (pi/2 + D S(w))), w = x/3, amp = 1 - (1 - eps) sin^2(pi w),
    which joins the raw entry direction to the raw exit direction when
    D = psi + pi (mod 2 pi) and never vanishes.
    """
    a3 = abs(RHO_A[1])

    def gamma(t):
        x = 4 * (t % TWO_PI) / TWO_PI
        if x >= 3:
            s = smooth(x - 3)
            return np.array([RHO_A[0], np.exp(1j * psi * (1 - s)) * RHO_A[1]])
        if detour is None:
            odd = _odd_body_raw(x, psi)
        else:
            w = x / 3
            amp = 1 - (1 - eps) * np.sin(np.pi * w) ** 2
            odd = amp * a3 * np.exp(1j * (np.pi / 2 + detour * smooth(w)))
        return rotate(np.array([_even_body(x), odd]), _beta(x))
    return gamma


def on_b_arc(t):
    return 1 <= 4 * (t % TWO_PI) / TWO_PI <= 2
