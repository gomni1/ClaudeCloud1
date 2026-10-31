/* grammar-clock/csrc/ssa.c
 * Copied from PR 3: gomni1/ClaudeCloud1, branch grammar-exit-time, grammar-exit-time/csrc/ssa.c
 * (Gillespie direct method, xoshiro256** RNG).  Adapted for PHYS2 grammar-clock (SPEC K3):
 * the RNG and the direct-method selection loop are kept verbatim; the propensity table is replaced
 * by the four-role grammar closed level (threshold tables F_kr, F_kc passed in, x = n_C / N) and
 * the Brusselator (planted failure P2); new drivers run_clock and run_hist2 record ticks, samples,
 * visits to D and time-weighted histograms.  The original PR 3 drivers are removed. */
/* Exact stochastic simulation (Gillespie direct method) for the Contact/Void
 * grammar in Kurtz form and for the planted-failure models.  SPEC.md §2, §9. */
#include <stdint.h>
#include <math.h>
#include <string.h>
#include <time.h>

/* CPU deadline (process CPU seconds; <= 0 disables), checked every 2^20 events */
static double g_deadline = -1.0;
static int g_aborted = 0;
static inline double cpu_now(void) { return (double)clock() / CLOCKS_PER_SEC; }

/* ---------- RNG: xoshiro256** seeded through splitmix64 ---------- */
typedef struct { uint64_t s[4]; } rng_t;

static inline uint64_t rotl(const uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }

static inline uint64_t rng_next(rng_t *r) {
    const uint64_t result = rotl(r->s[1] * 5, 7) * 9;
    const uint64_t t = r->s[1] << 17;
    r->s[2] ^= r->s[0];
    r->s[3] ^= r->s[1];
    r->s[1] ^= r->s[2];
    r->s[0] ^= r->s[3];
    r->s[2] ^= t;
    r->s[3] = rotl(r->s[3], 45);
    return result;
}

static inline uint64_t splitmix64(uint64_t *x) {
    uint64_t z = (*x += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}

static void rng_seed(rng_t *r, uint64_t seed) {
    uint64_t x = seed;
    for (int i = 0; i < 4; i++) r->s[i] = splitmix64(&x);
}

/* uniform on (0, 1] */
static inline double unif(rng_t *r) { return ((rng_next(r) >> 11) + 1) * 0x1.0p-53; }

/* ---------- models (grammar-clock) ---------- */
enum { M_G = 0, M_BR = 1 };
#define NRG 9
/* grammar closed level, species (C, V, L, P); reactions 1 2 3 5 6 7 8 10 11 */
static const int NUG[NRG][4] = {
    {-1, 0, +1, 0},  /* 1  C -> L          */
    {-1, +1, 0, 0},  /* 2  C -> V          */
    {+1, -1, 0, 0},  /* 3  V + C -> 2C     */
    {0, +1, -1, 0},  /* 5  L -> V          */
    {+1, 0, -1, 0},  /* 6  L -> C          */
    {-1, 0, 0, +1},  /* 7  C -> P          */
    {0, +1, 0, -1},  /* 8  P -> V          */
    {+1, -1, 0, 0},  /* 10 V -> C          */
    {-1, +1, 0, 0},  /* 11 2C -> V + C     */
};
static const int NUB[4][2] = {{+1, 0}, {-1, +1}, {+1, -1}, {-1, 0}};

/* k = (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12) for M_G; (a, b) for M_BR.
 * FR[nC] = F_kr(nC/N), FC[nC] = F_kc(nC/N) (Kurtz form: Omega*k3*(V/Omega)*F = k3*V*F). */
static inline int propensities(int model, double om, const double *k, const double *FR, const double *FC,
                               const int64_t *n, double *a) {
    if (model == M_BR) {
        const double X = (double)n[0], Y = (double)n[1];
        a[0] = k[0] * om;
        a[1] = k[1] * X;
        a[2] = X * X * Y / (om * om);
        a[3] = X;
        return 4;
    }
    const double C = (double)n[0], V = (double)n[1], L = (double)n[2], P = (double)n[3];
    a[0] = k[0] * C;
    a[1] = k[1] * C;
    a[2] = k[2] * V * FR[n[0]];
    a[3] = k[3] * L;
    a[4] = k[4] * L;
    a[5] = k[5] * C;
    a[6] = k[6] * P;
    a[7] = k[8] * V;
    a[8] = k[9] * C * FC[n[0]];
    return NRG;
}

static inline void apply(int model, int r, int64_t *n) {
    if (model == M_BR) {
        n[0] += NUB[r][0];
        n[1] += NUB[r][1];
        return;
    }
    n[0] += NUG[r][0];
    n[1] += NUG[r][1];
    n[2] += NUG[r][2];
    n[3] += NUG[r][3];
}

/* one direct-method step; returns 0 if a0 == 0 */
static inline int step(int model, double om, const double *k, const double *FR, const double *FC, int64_t *n,
                       double *t, double *dt_out, rng_t *rng) {
    double a[NRG];
    int m = propensities(model, om, k, FR, FC, n, a);
    double a0 = 0.0;
    for (int i = 0; i < m; i++) a0 += a[i];
    if (a0 <= 0.0) return 0;
    double dt = -log(unif(rng)) / a0;
    *dt_out = dt;
    *t += dt;
    double u = unif(rng) * a0, acc = 0.0;
    int r = m - 1;
    for (int i = 0; i < m; i++) {
        acc += a[i];
        if (u <= acc) { r = i; break; }
    }
    apply(model, r, n);
    return 1;
}

/* Clock run.  Ticks: upward crossing of c0 = n[0]/om >= cmid after c0 < cdrop (armed).
 * Samples: species 0..nsp-1 (as concentrations) at t = j*dt_s (piecewise-constant path, value just
 * before the grid time), j < max_samp.  Stops at max_ticks ticks, t_max, max_events or the CPU
 * deadline.  stats: [0] events, [1] D visits (entries into n_C = n_L = 0), [2] ticks, [3] final t,
 * [4] aborted (1 = cpu), [5] samples written.  Final state returned in n0 (in/out). */
int run_clock(int model, double om, const double *k, const double *FR, const double *FC, int64_t *n0,
              double t_max, int64_t max_ticks, int64_t max_events, double cmid, double cdrop, double dt_s,
              int nsp, int64_t max_samp, float *samp, double *ticks, uint64_t seed, double max_cpu,
              double *stats) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4] = {n0[0], n0[1], n0[2], n0[3]};
    double t = 0.0, dt = 0.0;
    int64_t nt = 0, js = 0;
    uint64_t ev = 0, dvis = 0;
    int armed = ((double)n[0] / om < cdrop), inD = (model == M_G && n[0] == 0 && n[2] == 0);
    double deadline = max_cpu > 0 ? cpu_now() + max_cpu : -1.0;
    int aborted = 0;
    double tnext = 0.0;
    for (;;) {
        double tprev = t;
        int64_t nprev[4] = {n[0], n[1], n[2], n[3]};
        if (!step(model, om, k, FR, FC, n, &t, &dt, &rng)) { t = t_max; }
        if (t > t_max) t = t_max;
        /* samples on the grid in [tprev, t): state before this event */
        while (tnext < t && js < max_samp) {
            for (int s = 0; s < nsp; s++) samp[js * nsp + s] = (float)((double)nprev[s] / om);
            js++;
            tnext = js * dt_s;
        }
        if (t >= t_max) break;
        ev++;
        double c = (double)n[0] / om;
        if (c < cdrop) armed = 1;
        else if (armed && c >= cmid) { ticks[nt++] = t; armed = 0; }
        if (model == M_G) {
            int d = (n[0] == 0 && n[2] == 0);
            if (d && !inD) dvis++;
            inD = d;
        }
        if (nt >= max_ticks || (max_events > 0 && (int64_t)ev >= max_events)) break;
        if (deadline > 0.0 && (ev & 0xFFFFF) == 0 && cpu_now() > deadline) { aborted = 1; break; }
    }
    for (int s = 0; s < 4; s++) n0[s] = n[s];
    stats[0] = (double)ev; stats[1] = (double)dvis; stats[2] = (double)nt; stats[3] = t;
    stats[4] = (double)aborted; stats[5] = (double)js;
    return (int)nt;
}

/* Time-weighted histogram of n[0] over n_events events after n_burn events (grammar model). */
double run_hist2(int model, double om, const double *k, const double *FR, const double *FC, const int64_t *n0,
                 int64_t n_burn, int64_t n_events, uint64_t seed, int64_t hlen, double *hist) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4] = {n0[0], n0[1], n0[2], n0[3]};
    double t = 0.0, dt = 0.0;
    for (int64_t e = 0; e < n_burn; e++)
        if (!step(model, om, k, FR, FC, n, &t, &dt, &rng)) return -1.0;
    double T = 0.0;
    for (int64_t e = 0; e < n_events; e++) {
        int64_t c = n[0];
        if (!step(model, om, k, FR, FC, n, &t, &dt, &rng)) return -1.0;
        if (c < hlen) hist[c] += dt;
        T += dt;
    }
    return T;
}
