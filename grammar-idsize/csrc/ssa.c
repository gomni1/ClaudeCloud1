/* Copied from grammar-exit-time/ (PR 3, gomni1/ClaudeCloud1#3) for task grammar-idsize; see grammar-idsize/README.md. */
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

/* ---------- models ---------- */
enum { M_MA = 0, M_TH = 1, M_MAC = 2, M_ID = 3, M_ND = 4 };
enum { T_D = 0, T_D0 = 1, T_VGE = 2, T_VLE = 3, T_X0 = 4, T_XOUT = 5, T_NONE = 6 };

#define NR 11
/* reaction order: r1 r2 r3 r5 r6 r7 r8 r9 r10 r11 r12; species (C, V, L, P) */
static const int NU[NR][4] = {
    {-1, 0, +1, 0},  /* 1  C -> L          */
    {-1, +1, 0, 0},  /* 2  C -> V          */
    {+1, -1, 0, 0},  /* 3  V + C -> 2C     */
    {0, +1, -1, 0},  /* 5  L -> V          */
    {+1, 0, -1, 0},  /* 6  L -> C          */
    {-1, 0, 0, +1},  /* 7  C -> P          */
    {0, +1, 0, -1},  /* 8  P -> V          */
    {0, 0, 0, -1},   /* 9  P -> 0          */
    {+1, -1, 0, 0},  /* 10 V -> C          */
    {-1, +1, 0, 0},  /* 11 2C -> V + C     */
    {0, +1, 0, 0},   /* 12 0 -> V          */
};

/* k = (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12) */
static inline int propensities(int model, double om, const double *k, const int64_t *n, double *a) {
    if (model == M_ID) {
        a[0] = om;
        a[1] = (double)n[0];
        return 2;
    }
    if (model == M_ND) {
        double r = (double)n[0] * (double)n[1] / om;
        a[0] = r; /* X + Y -> 2X */
        a[1] = r; /* X + Y -> 2Y */
        return 2;
    }
    const double C = (double)n[0], V = (double)n[1], L = (double)n[2], P = (double)n[3];
    a[0] = k[0] * C;
    a[1] = k[1] * C;
    a[3] = k[3] * L;
    a[4] = k[4] * L;
    a[5] = k[5] * C;
    a[6] = k[6] * P;
    a[7] = k[7] * P;
    a[8] = k[8] * V;
    a[10] = k[10] * om;
    if (model == M_TH) {
        double x = (C + V > 0.0) ? C / (C + V) : 0.0;
        double x2 = x * x;
        a[2] = k[2] * V * x2;
        a[9] = k[9] * C * x2;
    } else if (model == M_MA) {
        a[2] = k[2] * V * C / om;
        a[9] = k[9] * C * C / om;
    } else { /* M_MAC: combinatorial reaction 11 */
        a[2] = k[2] * V * C / om;
        a[9] = k[9] * C * (C - 1.0) / om;
    }
    return NR;
}

static inline void apply(int model, int r, int64_t *n) {
    if (model == M_ID) {
        n[0] += (r == 0) ? 1 : -1;
        return;
    }
    if (model == M_ND) {
        if (r == 0) { n[0] += 1; n[1] -= 1; } else { n[0] -= 1; n[1] += 1; }
        return;
    }
    n[0] += NU[r][0];
    n[1] += NU[r][1];
    n[2] += NU[r][2];
    n[3] += NU[r][3];
}

static inline int hit(int target, const int64_t *n, int64_t ta, int64_t tb) {
    switch (target) {
    case T_D: return n[0] == 0 && n[2] == 0;
    case T_D0: return n[0] == 0;
    case T_VGE: return n[1] >= ta;
    case T_VLE: return n[1] <= ta;
    case T_X0: return n[0] == 0;
    case T_XOUT: return n[0] <= ta || n[0] >= tb;
    default: return 0;
    }
}

/* Advance from time t (state n) until the target is hit or time reaches t_end.
 * Returns 1 on hit (t set to hit time), 0 if t_end reached (t = t_end).
 * events and dsec (time spent in D, optional) are accumulated. */
static inline int advance(int model, double om, const double *k, int64_t *n, double *t, double t_end,
                          int target, int64_t ta, int64_t tb, rng_t *rng, uint64_t *events,
                          int sec_target, int64_t sa, int *sec_hit) {
    double a[NR];
    for (;;) {
        int m = propensities(model, om, k, n, a);
        double a0 = 0.0;
        for (int i = 0; i < m; i++) a0 += a[i];
        if (a0 <= 0.0) { *t = t_end; return 0; }
        double dt = -log(unif(rng)) / a0;
        if (*t + dt >= t_end) { *t = t_end; return 0; }
        *t += dt;
        double u = unif(rng) * a0, acc = 0.0;
        int r = m - 1;
        for (int i = 0; i < m; i++) {
            acc += a[i];
            if (u <= acc) { r = i; break; }
        }
        apply(model, r, n);
        (*events)++;
        if (sec_hit && !*sec_hit && hit(sec_target, n, sa, 0)) *sec_hit = 1;
        if (hit(target, n, ta, tb)) return 1;
        if (g_deadline > 0.0 && ((*events) & 0xFFFFF) == 0 && cpu_now() > g_deadline) {
            g_aborted = 1;
            return 2;
        }
    }
}

/* Run up to nruns recorded runs (exit or censored).
 * Burn-in of length t_burn with restarts on hits; exit time measured from t_burn,
 * censored at cap.  max_attempts (<= 0: unlimited) bounds total burn-in attempts;
 * max_cpu (<= 0: unlimited) bounds the CPU seconds of the call (the run in
 * progress is then discarded).  Outputs per run: time, censored flag, restarts,
 * events, passed-through-D flag.  Totals: attempts, events in failed burn-in
 * attempts, all events, aborted flag (1 = attempts, 2 = cpu).
 * Returns the number of runs completed. */
int run_exits(int model, double om, const double *k, const int64_t *n0, int target, int64_t ta, int64_t tb,
              double t_burn, double cap, int nruns, uint64_t seed, int64_t max_attempts, double max_cpu,
              double *out_time, int32_t *out_cens, int64_t *out_restarts, double *out_events,
              int32_t *out_secD, int64_t *tot_attempts, double *tot_failed_events, double *tot_events,
              int32_t *aborted) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t attempts = 0;
    double failed_ev = 0.0, all_ev = 0.0;
    int done = 0;
    *aborted = 0;
    g_aborted = 0;
    g_deadline = (max_cpu > 0.0) ? cpu_now() + max_cpu : -1.0;
    for (int i = 0; i < nruns; i++) {
        int64_t restarts = 0;
        uint64_t ev = 0;
        int64_t n[4];
        double t = 0.0;
        int ok = 0;
        while (!ok) {
            if (max_attempts > 0 && attempts >= max_attempts) { *aborted = 1; goto finish; }
            attempts++;
            memcpy(n, n0, sizeof(n));
            t = 0.0;
            if (hit(target, n, ta, tb)) { ok = 1; break; } /* start in target: zero time */
            if (t_burn > 0.0) {
                uint64_t ev_b = 0;
                int h = advance(model, om, k, n, &t, t_burn, target, ta, tb, &rng, &ev_b, 0, 0, 0);
                all_ev += (double)ev_b;
                if (h == 2) { *aborted = 2; goto finish; }
                if (h == 1) {
                    restarts++;
                    failed_ev += (double)ev_b;
                    continue;
                }
                ev += ev_b;
            }
            ok = 1;
        }
        double tt = 0.0;
        int secD = 0;
        int want_sec = (target == T_VGE || target == T_VLE);
        int h = 1;
        if (!hit(target, n, ta, tb)) {
            uint64_t ev_r = 0;
            h = advance(model, om, k, n, &tt, cap, target, ta, tb, &rng, &ev_r, T_D, 0, want_sec ? &secD : 0);
            ev += ev_r;
            all_ev += (double)ev_r;
            if (h == 2) { *aborted = 2; goto finish; }
        }
        out_time[i] = h ? tt : cap;
        out_cens[i] = h ? 0 : 1;
        out_restarts[i] = restarts;
        out_events[i] = (double)ev;
        out_secD[i] = secD;
        done++;
    }
finish:
    g_deadline = -1.0;
    *tot_attempts = attempts;
    *tot_failed_events = failed_ev;
    *tot_events = all_ev;
    return done;
}

/* Time-weighted histogram of nV (index 0..nmax; larger values go to nmax) over
 * [t_burn, t_burn + t_total], split into nblocks equal time blocks:
 * hist has shape (nblocks, nmax + 1).  Also counts completed switches between
 * nV <= lo and nV >= hi.  Returns events. */
double run_hist(int model, double om, const double *k, const int64_t *n0, double t_burn, double t_total,
                uint64_t seed, int64_t nmax, int nblocks, double *hist, int64_t lo, int64_t hi,
                int64_t *n_switch) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4];
    memcpy(n, n0, sizeof(n));
    double a[NR];
    double t = 0.0;
    uint64_t ev = 0;
    if (t_burn > 0.0) advance(model, om, k, n, &t, t_burn, T_NONE, 0, 0, &rng, &ev, 0, 0, 0);
    double t0 = t, t_end = t_burn + t_total, blk = t_total / nblocks;
    int side = (n[1] <= lo) ? -1 : ((n[1] >= hi) ? 1 : 0);
    int64_t sw = 0;
    t = t0;
    for (;;) {
        int m = propensities(model, om, k, n, a);
        double a0 = 0.0;
        for (int i = 0; i < m; i++) a0 += a[i];
        double dt = (a0 > 0.0) ? -log(unif(&rng)) / a0 : t_end - t;
        double t_next = t + dt;
        if (t_next > t_end) t_next = t_end;
        /* deposit [t, t_next) into blocks */
        int64_t v = n[1] < nmax ? n[1] : nmax;
        double s = t;
        while (s < t_next) {
            int b = (int)((s - t0) / blk);
            if (b >= nblocks) b = nblocks - 1;
            double b_end = t0 + (b + 1) * blk;
            double e = t_next < b_end ? t_next : b_end;
            if (b == nblocks - 1) e = t_next;
            hist[(int64_t)b * (nmax + 1) + v] += e - s;
            s = e;
        }
        if (t_next >= t_end) break;
        t = t_next;
        double u = unif(&rng) * a0, acc = 0.0;
        int r = m - 1;
        for (int i = 0; i < m; i++) {
            acc += a[i];
            if (u <= acc) { r = i; break; }
        }
        apply(model, r, n);
        ev++;
        if (n[1] <= lo && side == 1) { side = -1; sw++; }
        else if (n[1] >= hi && side == -1) { side = 1; sw++; }
        else if (side == 0) side = (n[1] <= lo) ? -1 : ((n[1] >= hi) ? 1 : 0);
    }
    *n_switch = sw;
    return (double)ev;
}

/* Record the state at the given increasing times (no target). */
double run_traj(int model, double om, const double *k, const int64_t *n0, int ntimes, const double *times,
                uint64_t seed, int64_t *out) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4];
    memcpy(n, n0, sizeof(n));
    double t = 0.0;
    uint64_t ev = 0;
    for (int j = 0; j < ntimes; j++) {
        advance(model, om, k, n, &t, times[j], T_NONE, 0, 0, &rng, &ev, 0, 0, 0);
        memcpy(out + 4 * j, n, sizeof(n));
    }
    return (double)ev;
}

/* Expose propensities for the drift check (M0). */
int propensity_vec(int model, double om, const double *k, const int64_t *n, double *a) {
    return propensities(model, om, k, n, a);
}
