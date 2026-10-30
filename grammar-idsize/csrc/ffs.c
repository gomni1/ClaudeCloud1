/* Forward flux sampling kernels for grammar-idsize (SPEC §3).
 * The propensities, stoichiometry and RNG are copied from grammar-exit-time/csrc/ssa.c (PR 3). */
#include <stdint.h>
#include <math.h>
#include <string.h>

typedef struct { uint64_t s[4]; } rng_t;
static inline uint64_t rotl(const uint64_t x, int k) { return (x << k) | (x >> (64 - k)); }
static inline uint64_t rng_next(rng_t *r) {
    const uint64_t result = rotl(r->s[1] * 5, 7) * 9;
    const uint64_t t = r->s[1] << 17;
    r->s[2] ^= r->s[0]; r->s[3] ^= r->s[1]; r->s[1] ^= r->s[2]; r->s[0] ^= r->s[3];
    r->s[2] ^= t; r->s[3] = rotl(r->s[3], 45);
    return result;
}
static inline uint64_t splitmix64(uint64_t *x) {
    uint64_t z = (*x += 0x9e3779b97f4a7c15ULL);
    z = (z ^ (z >> 30)) * 0xbf58476d1ce4e5b9ULL;
    z = (z ^ (z >> 27)) * 0x94d049bb133111ebULL;
    return z ^ (z >> 31);
}
static void rng_seed(rng_t *r, uint64_t seed) { uint64_t x = seed; for (int i = 0; i < 4; i++) r->s[i] = splitmix64(&x); }
static inline double unif(rng_t *r) { return ((rng_next(r) >> 11) + 1) * 0x1.0p-53; }

enum { M_MA = 0, M_TH = 1, M_ID = 3 };
#define NR 11
static const int NU[NR][4] = {
    {-1, 0, +1, 0}, {-1, +1, 0, 0}, {+1, -1, 0, 0}, {0, +1, -1, 0}, {+1, 0, -1, 0}, {-1, 0, 0, +1},
    {0, +1, 0, -1}, {0, 0, 0, -1}, {+1, -1, 0, 0}, {-1, +1, 0, 0}, {0, +1, 0, 0},
};

static inline int props(int model, double om, const double *k, const int64_t *n, double *a) {
    if (model == M_ID) { a[0] = om; a[1] = (double)n[0]; return 2; }
    const double C = (double)n[0], V = (double)n[1], L = (double)n[2], P = (double)n[3];
    a[0] = k[0] * C; a[1] = k[1] * C; a[3] = k[3] * L; a[4] = k[4] * L; a[5] = k[5] * C;
    a[6] = k[6] * P; a[7] = k[7] * P; a[8] = k[8] * V; a[10] = k[10] * om;
    if (model == M_TH) {
        double x = (C + V > 0.0) ? C / (C + V) : 0.0, x2 = x * x;
        a[2] = k[2] * V * x2; a[9] = k[9] * C * x2;
    } else {
        a[2] = k[2] * V * C / om; a[9] = k[9] * C * C / om;
    }
    return NR;
}
static inline void apply(int model, int r, int64_t *n) {
    if (model == M_ID) { n[0] += (r == 0) ? 1 : -1; return; }
    n[0] += NU[r][0]; n[1] += NU[r][1]; n[2] += NU[r][2]; n[3] += NU[r][3];
}
/* order parameter: nC + nL for the grammar, nX for immigration-death */
static inline int64_t ordp(int model, const int64_t *n) { return model == M_ID ? n[0] : n[0] + n[2]; }

/* one Gillespie step; returns dt (inf if no reaction) */
static inline double step(int model, double om, const double *k, int64_t *n, rng_t *rng) {
    double a[NR], a0 = 0.0;
    int m = props(model, om, k, n, a);
    for (int i = 0; i < m; i++) a0 += a[i];
    if (a0 <= 0.0) return INFINITY;
    double dt = -log(unif(rng)) / a0, u = unif(rng) * a0, acc = 0.0;
    int r = m - 1;
    for (int i = 0; i < m; i++) { acc += a[i]; if (u <= acc) { r = i; break; } }
    apply(model, r, n);
    return dt;
}

/* Burn-in of length t_burn from n0, restarting on a hit of the target (order parameter == 0). */
static void burn(int model, double om, const double *k, const int64_t *n0, double t_burn, int64_t *n, rng_t *rng,
                 int64_t *restarts, double *events) {
    for (;;) {
        memcpy(n, n0, 4 * sizeof(int64_t));
        double t = 0.0;
        int hit = 0;
        while (1) {
            double a[NR], a0 = 0.0;
            int m = props(model, om, k, n, a);
            for (int i = 0; i < m; i++) a0 += a[i];
            double dt = -log(unif(rng)) / a0;
            if (t + dt >= t_burn) break;
            t += dt;
            double u = unif(rng) * a0, acc = 0.0;
            int r = m - 1;
            for (int i = 0; i < m; i++) { acc += a[i]; if (u <= acc) { r = i; break; } }
            apply(model, r, n);
            (*events) += 1;
            if (ordp(model, n) == 0) { hit = 1; break; }
        }
        if (!hit) return;
        (*restarts)++;
    }
}

/* Flux stage: count first crossings to order parameter <= M0 after a visit to A (>= MA).
 * Stores crossing configurations.  Returns the number stored; *tot_time is the flux time. */
int ffs_flux(int model, double om, const double *k, const int64_t *n0, double t_burn, int64_t MA, int64_t M0,
             int ncross, uint64_t seed, double max_events, int64_t *out_states, double *tot_time,
             int64_t *restarts, double *events, int64_t *n_hitD) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4];
    *restarts = 0; *events = 0.0; *n_hitD = 0; *tot_time = 0.0;
    burn(model, om, k, n0, t_burn, n, &rng, restarts, events);
    int lastA = ordp(model, n) >= MA;
    double t_seg = 0.0, t_lastA = 0.0;
    int got = 0;
    while (got < ncross) {
        if (*events > max_events) break;
        double dt = step(model, om, k, n, &rng);
        if (!isfinite(dt)) break;
        t_seg += dt;
        (*events) += 1;
        int64_t M = ordp(model, n);
        if (M >= MA) { lastA = 1; t_lastA = t_seg; }
        else if (lastA && M <= M0) {
            memcpy(out_states + 4 * got, n, 4 * sizeof(int64_t));
            got++;
            lastA = 0;
        }
        if (M == 0) { /* reached the target during the flux stage: exclude time since the last A visit */
            (*n_hitD)++;
            *tot_time += t_lastA;
            burn(model, om, k, n0, t_burn, n, &rng, restarts, events);
            lastA = ordp(model, n) >= MA;
            t_seg = 0.0; t_lastA = 0.0;
        }
    }
    *tot_time += t_seg;
    return got;
}

/* squared distance from point x (4) to polyline path (np x 4) */
static double dist_path(const double *x, const double *path, int np) {
    double best = INFINITY;
    for (int i = 0; i + 1 < np; i++) {
        const double *a = path + 4 * i, *b = path + 4 * (i + 1);
        double ab[4], ax[4], l2 = 0.0, dot = 0.0;
        for (int j = 0; j < 4; j++) { ab[j] = b[j] - a[j]; ax[j] = x[j] - a[j]; l2 += ab[j] * ab[j]; dot += ab[j] * ax[j]; }
        double t = l2 > 0 ? dot / l2 : 0.0;
        if (t < 0) t = 0; if (t > 1) t = 1;
        double d2 = 0.0;
        for (int j = 0; j < 4; j++) { double e = ax[j] - t * ab[j]; d2 += e * e; }
        if (d2 < best) best = d2;
    }
    return sqrt(best);
}

/* Interface trials: from configurations `starts` (nstart x 4), run until order parameter <= Mnext (success)
 * or >= MA (failure).  Per trial outputs: success, end state, parent index, max nV/om, distance sum/count. */
int ffs_trials(int model, double om, const double *k, const int64_t *starts, int nstart, int ntrials, int64_t Mnext,
               int64_t MA, uint64_t seed, int sample_every, const double *path, int npath, int32_t *out_ok,
               int64_t *out_state, int32_t *out_parent, double *out_maxv, double *out_dsum, int32_t *out_dcnt,
               double *events) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4];
    *events = 0.0;
    int nok = 0;
    for (int tr = 0; tr < ntrials; tr++) {
        int p = (int)(unif(&rng) * nstart);
        if (p >= nstart) p = nstart - 1;
        memcpy(n, starts + 4 * p, 4 * sizeof(int64_t));
        double maxv = (double)n[1] / om, dsum = 0.0;
        int dcnt = 0, ok = 0;
        uint64_t ev = 0;
        for (;;) {
            double dt = step(model, om, k, n, &rng);
            if (!isfinite(dt)) break;
            ev++;
            double v = (double)n[1] / om;
            if (v > maxv) maxv = v;
            if (npath > 1 && sample_every > 0 && ev % sample_every == 0) {
                double x[4] = {n[0] / om, n[1] / om, n[2] / om, n[3] / om};
                dsum += dist_path(x, path, npath);
                dcnt++;
            }
            int64_t M = ordp(model, n);
            if (M <= Mnext) { ok = 1; break; }
            if (M >= MA) break;
        }
        *events += (double)ev;
        out_ok[tr] = ok;
        memcpy(out_state + 4 * tr, n, 4 * sizeof(int64_t));
        out_parent[tr] = p;
        out_maxv[tr] = maxv;
        out_dsum[tr] = dsum;
        out_dcnt[tr] = dcnt;
        nok += ok;
    }
    return nok;
}
