"""Section fields over the base circle: builders and loop-level instruments.

A loop is a function gamma(t) -> section vector, periodic on [0, 2 pi).
"""
import numpy as np

from .sections import modes, rotate, stratum_distance, symmetry_order

TWO_PI = 2 * np.pi
GOLD = (np.sqrt(5) - 1) / 2


def smooth(x):
    """C2 smoothstep on [0, 1] (zero first and second derivative at the ends)."""
    x = min(max(x, 0.0), 1.0)
    return x ** 3 * (10 - 15 * x + 6 * x * x)


# --- instruments --------------------------------------------------------------

def connection_rotation(gamma, weights, n=4000):
    """A_w = closed integral of <xi g, dg>_w / <xi g, xi g>_w (SPEC 1.9).

    Midpoint rule at n and 2n with Richardson extrapolation.
    """
    def estimate(n):
        ts = TWO_PI * np.arange(n + 1) / n
        pts = np.array([gamma(t) for t in ts])
        m = modes(pts[0])
        mid = 0.5 * (pts[1:] + pts[:-1])
        dg = pts[1:] - pts[:-1]
        xi = 1j * m * mid
        num = np.real(np.sum(weights * np.conj(xi) * dg, axis=1))
        den = np.sum(weights * np.abs(xi) ** 2, axis=1)
        return float(np.sum(num / den))
    a1, a2 = estimate(n), estimate(2 * n)
    return (4 * a2 - a1) / 3


def unit_weights(M):
    return np.ones(M - 1)


def square_weights(M):
    return np.arange(2, M + 1, dtype=float) ** 2


def find_passages(gamma, k, n=256, tol=1e-9):
    """Locate passages of the loop through the closed stratum C_k.

    Every cyclic local minimum of d_k on the grid is refined by golden-section
    search; returns (passages, grid_minimum) with passages = [(t, d_k), ...].
    """
    ts = TWO_PI * np.arange(n) / n
    d = np.array([stratum_distance(gamma(t), k) for t in ts])
    found = []
    for i in range(n):
        if d[i] <= d[i - 1] and d[i] <= d[(i + 1) % n]:
            a, b = ts[i] - TWO_PI / n, ts[i] + TWO_PI / n
            f = lambda t: stratum_distance(gamma(t % TWO_PI), k)
            c, e = b - GOLD * (b - a), a + GOLD * (b - a)
            for _ in range(200):
                if b - a < 1e-14:
                    break
                if f(c) < f(e):
                    b, e = e, c
                    c = b - GOLD * (b - a)
                else:
                    a, c = c, e
                    e = a + GOLD * (b - a)
            t_min = (0.5 * (a + b)) % TWO_PI
            if f(t_min) < tol:
                found.append((t_min, f(t_min)))
    return found, float(d.min())


def stratum_audit(gamma, n=2000):
    """Minimum over samples of the distance to each C_k (k >= 2) and to the circle."""
    ts = TWO_PI * np.arange(n) / n
    pts = [gamma(t) for t in ts]
    M = len(pts[0]) + 1
    out = {f"C{k}": min(stratum_distance(z, k) for z in pts) for k in range(2, M + 1)}
    out["circle"] = min(float(np.linalg.norm(z)) for z in pts)
    return out


def max_step(gamma, n=2000):
    """Largest sup-norm change of r(phi) between consecutive samples (continuity)."""
    ts = TWO_PI * np.arange(n + 1) / n
    pts = np.array([gamma(t) for t in ts])
    # sup_phi |r1 - r2| <= sum_m |z1_m - z2_m|, an upper bound used as the check
    return float(np.max(np.sum(np.abs(np.diff(pts, axis=0)), axis=1)))


# --- H1b: explicit homotopies -------------------------------------------------

def h1b_homotopy_M5(s, a=(0.15, 0.1, 0.04, 0.05), c=(0.1, 0.1, 0.06, 0.025),
                    phases=(0.3, 1.1, 2.0, 0.7)):
    """Orbit loop of a free section (s = 0) to a constant loop (s = 2), inside V_free.

    Stage 1 (0 <= s <= 1) contracts (z3, z5) along straight lines; they vanish at
    different s (|a3|/(|a3|+|c3|) = 0.5 and |a5|/(|a5|+|c5|) = 2/3), so never
    together. Stage 2 (1 <= s <= 2) contracts (z2, z4) while z3 = c3, z5 = c5 != 0.
    """
    a2, a3, a4, a5 = (amp * np.exp(1j * ph) for amp, ph in zip(a, phases))
    c2, c3, c4, c5 = c

    def gamma(t):
        e = lambda m, amp: amp * np.exp(1j * m * t)
        if s <= 1:
            return np.array([e(2, a2), (1 - s) * e(3, a3) + s * c3,
                             e(4, a4), (1 - s) * e(5, a5) + s * c5])
        u = s - 1
        return np.array([(1 - u) * e(2, a2) + u * c2, c3,
                         (1 - u) * e(4, a4) + u * c4, c5])
    return gamma


# --- H3: rigid-sector loops ---------------------------------------------------

HALF_WIDTH = 0.6


def sector_loop(classes, shapes, c, j):
    """Rigid-sector loop (SPEC 1.10).

    classes: three labels for the sectors centred at 0, 2pi/3, 4pi/3.
    shapes:  label -> reference shape s_X.
    c:       sector rotations in turns.  j: relabel index per sector (mod k_X).
    The parameter u = t + HALF_WIDTH starts at the beginning of sector 0.
    Returns (gamma, info) with info = {T, residual, k}.
    """
    k = {X: symmetry_order(shapes[X]) for X in set(classes)}
    segments = []                       # (u0, u1, kind, data)
    beta, a = 0.0, 0.0
    width = 2 * HALF_WIDTH
    for i, X in enumerate(classes):
        u0 = i * TWO_PI / 3
        segments.append((u0, u0 + width, "sector", (X, beta, TWO_PI * c[i], a)))
        beta += TWO_PI * c[i]
        a += TWO_PI * j[i] / k[X]
        Y = classes[(i + 1) % 3]
        g0, g1 = u0 + width, (i + 1) * TWO_PI / 3
        if X == Y:
            segments.append((g0, g1, "hold", (X, beta, a)))
        else:
            segments.append((g0, g1, "transition", (X, Y, beta, a)))

    def gamma(t):
        u = (t + HALF_WIDTH) % TWO_PI
        for u0, u1, kind, data in segments:
            if u0 <= u <= u1 + 1e-15:
                lam = (u - u0) / (u1 - u0)
                if kind == "sector":
                    X, b0, db, rep = data
                    return rotate(shapes[X], b0 + db * smooth(lam) + rep)
                if kind == "hold":
                    X, b, rep = data
                    return rotate(shapes[X], b + rep)
                X, Y, b, rep = data
                body = (1 - smooth(lam)) * shapes[X] + smooth(lam) * shapes[Y]
                return rotate(body, b + rep)
        raise ValueError(u)

    X0 = classes[0]
    end = rotate(shapes[X0], beta + a)
    residual = float(np.linalg.norm(end - shapes[X0]))
    # residual = 0 lets the closing point use the symmetry of s_X0 implicitly;
    # rep_residual = 0 asks every identification to be one of the listed relabels
    rep_residual = abs(float((beta + a + np.pi) % TWO_PI - np.pi))
    return gamma, {"T": float(sum(c)), "residual": residual,
                   "rep_residual": rep_residual, "k": k}


# --- H4a: loops through C2 arcs and their resolutions -----------------------

def passage_loop(s_B, u, windows, beta_turns, deform=0.0, path=None, eps=0.3):
    """gamma(t) = R_beta(t) (s_B(t) + O(t)), with O odd, s_B in C2.

    windows: list of (t1, t2, t3, t4) = entry transition [t1,t2], C2 arc [t2,t3],
             exit transition [t3,t4]; the odd part flips sign across each window.
    beta_turns: rotation (turns) applied smoothly across each C2 arc.
    deform: amplitude of a non-rigid deformation that keeps the arcs in C2 and
            the rest asymmetric.
    path: None for the loop itself (O passes through 0 on the arc); otherwise a
          function P(lam, u) giving a path from u to -u with |P| = |u|, which
          resolves every window (the resolved loop avoids C2).
    """
    def beta(t):
        b = 0.0
        for (t1, t2, t3, t4), turns in zip(windows, beta_turns):
            b += TWO_PI * turns * smooth((t - t2) / (t3 - t2))
        return b + deform * 0.2 * np.sin(3 * t)

    def odd(t, uu):
        sign = 1.0
        for (t1, t2, t3, t4) in windows:
            if t < t1:
                break
            if t >= t4:
                sign = -sign
                continue
            lam = (t - t1) / (t4 - t1)
            if path is None:
                if t <= t2:
                    return sign * (1 - smooth((t - t1) / (t2 - t1))) * uu
                if t <= t3:
                    return 0 * uu
                return -sign * smooth((t - t3) / (t4 - t3)) * uu
            amp = 1 - (1 - eps) * np.sin(np.pi * lam) ** 2
            return sign * amp * path(lam, uu)
        return sign * uu

    def gamma(t):
        t = t % TWO_PI
        sB = s_B * (1 + deform * 0.3 * np.sin(t))
        uu = u * (1 + deform * 0.4 * np.cos(2 * t)) * np.exp(1j * deform * np.sin(t))
        return rotate(sB + odd(t, uu), beta(t))
    return gamma


def path_up(lam, u):
    return np.exp(1j * np.pi * lam) * u


def path_down(lam, u):
    return np.exp(-1j * np.pi * lam) * u


def path_family(mu):
    """Paths from u to -u on the sphere |P| = |u| (needs two odd modes).

    P = cos(pi lam) u + sin(pi lam) w_mu, with w_mu real-orthogonal to u and
    |w_mu| = |u|; mu = 0 gives path_up, mu = 1 gives path_down.
    """
    def path(lam, u):
        odd = u[[1, 3]]                       # (z3, z5)
        v = np.array([-np.conj(odd[1]), np.conj(odd[0])])
        w = np.cos(np.pi * mu) * 1j * odd + np.sin(np.pi * mu) * v
        out = np.zeros_like(u)
        out[[1, 3]] = np.cos(np.pi * lam) * odd + np.sin(np.pi * lam) * w
        return out
    return path
