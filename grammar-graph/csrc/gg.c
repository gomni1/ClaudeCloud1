/* grammar-graph/csrc/gg.c
 * Reused code: the xoshiro256** RNG (seeded through splitmix64) and the propensity conventions of
 * grammar-clock/csrc/ssa.c (PR 7: gomni1/ClaudeCloud1, branch grammar-clock; itself copied from PR 3,
 * grammar-exit-time/csrc/ssa.c): rate vector order (k1, k2, k3, k5, k6, k7, k8, k9, k10, k11, k12),
 * C->V = k2 + k11 F_kc, V->C = k10 + k3 F_kr with tabulated threshold values F_j(x) = Pr[Bin(m,x) >= j].
 * The RNG is copied verbatim. New here (SPEC.md section 1, 4): per-site exact Gillespie with a binary sum
 * tree over sites on a fixed graph, the lumped exact chain on K, exponentially filtered radius-2 ball
 * fields, phases/amplitudes, triangle windings and defect lists. */
#include <stdint.h>
#include <stdlib.h>
#include <math.h>
#include <string.h>
#include <time.h>

/* ---------- RNG (verbatim from grammar-clock/csrc/ssa.c) ---------- */
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

static inline double cpu_now(void) { return (double)clock() / CLOCKS_PER_SEC; }

/* roles */
enum { RC = 0, RV = 1, RL = 2, RP = 3 };

/* ---------- winding detector (shared by the simulator and the planted tests) ---------- */
static inline double wrapd(double d, int a, int b) {
    /* wrap into (-pi, pi]; exact tie at +-pi -> +pi if a < b else -pi (antisymmetric) */
    while (d > M_PI) d -= 2 * M_PI;
    while (d <= -M_PI) d += 2 * M_PI;
    if (d == M_PI) d = (a < b) ? M_PI : -M_PI;
    return d;
}
static inline int wind3(const double *phi, int a, int b, int c) {
    double s = wrapd(phi[b] - phi[a], a, b) + wrapd(phi[c] - phi[b], b, c) + wrapd(phi[a] - phi[c], c, a);
    return (int)lround(s / (2 * M_PI));
}
void gg_detect(int ntri, const int32_t *tri, const double *phi, int8_t *w) {
    for (int t = 0; t < ntri; t++) w[t] = (int8_t)wind3(phi, tri[3 * t], tri[3 * t + 1], tri[3 * t + 2]);
}

/* ---------- growable defect buffers ---------- */
static int32_t *g_dtri = NULL;
static int8_t *g_dsgn = NULL;
static int64_t g_nd = 0, g_cap = 0;
static void dpush(int32_t t, int8_t s) {
    if (g_nd == g_cap) {
        g_cap = g_cap ? 2 * g_cap : (1 << 20);
        g_dtri = (int32_t *)realloc(g_dtri, g_cap * sizeof(int32_t));
        g_dsgn = (int8_t *)realloc(g_dsgn, g_cap * sizeof(int8_t));
    }
    g_dtri[g_nd] = t;
    g_dsgn[g_nd] = s;
    g_nd++;
}
int64_t gg_ndef(void) { return g_nd; }
void gg_copy_defects(int32_t *tri, int8_t *sgn) {
    memcpy(tri, g_dtri, g_nd * sizeof(int32_t));
    memcpy(sgn, g_dsgn, g_nd * sizeof(int8_t));
}
void gg_free_defects(void) {
    free(g_dtri); free(g_dsgn);
    g_dtri = NULL; g_dsgn = NULL; g_nd = g_cap = 0;
}

/* ---------- graph simulator ---------- */
static inline double site_rate(int r, int i, const int32_t *nc, const int32_t *toff, const double *FR,
                               const double *FC, const double *k) {
    switch (r) {
        case RC: return k[0] + k[1] + k[5] + k[9] * FC[toff[i] + nc[i]];
        case RV: return k[8] + k[2] * FR[toff[i] + nc[i]];
        case RL: return k[3] + k[4];
        default: return k[6];
    }
}

/* fstat per frame: [R, sum_tri_amp_all, sum_tri_amp_def, total_winding, ndef]
 * stats: [events, frames_done, aborted, ndef_total, t_end] */
int gg_run_graph(int N, const int32_t *off, const int32_t *nbr, const int32_t *toff, const double *FR,
                 const double *FC, const double *k, int8_t *role, double t_max, double dt_frame, double tau,
                 uint64_t seed, const int32_t *boff, const int32_t *bidx, int ntri, const int32_t *tri,
                 double cs, double vs, double sc, double sv, int nframes, int32_t *gcount, double *fstat,
                 uint8_t *chg, int nsnap, const int32_t *snapf, uint8_t *snap, double max_cpu, double *stats,
                 int nbatch, double *twacc) {
    rng_t rng;
    rng_seed(&rng, seed);
    double cpu0 = cpu_now();
    int P = 1;
    while (P < N) P <<= 1;
    double *tree = (double *)calloc(2 * P, sizeof(double));
    int32_t *nc = (int32_t *)calloc(N, sizeof(int32_t));
    double *yC = (double *)malloc(N * sizeof(double)), *yV = (double *)malloc(N * sizeof(double));
    double *tl = (double *)calloc(N, sizeof(double));
    double *fC = (double *)malloc(N * sizeof(double)), *fV = (double *)malloc(N * sizeof(double));
    double *phi = (double *)malloc(N * sizeof(double)), *amp = (double *)malloc(N * sizeof(double));
    int64_t cnt[4] = {0, 0, 0, 0};
    int nb = (N + 7) / 8;
    gg_free_defects();
    for (int i = 0; i < N; i++) {
        cnt[role[i]]++;
        yC[i] = role[i] == RC;
        yV[i] = role[i] == RV;
    }
    for (int i = 0; i < N; i++)
        for (int e = off[i]; e < off[i + 1]; e++) nc[i] += role[nbr[e]] == RC;
    for (int i = 0; i < N; i++) tree[P + i] = site_rate(role[i], i, nc, toff, FR, FC, k);
    for (int u = P - 1; u >= 1; u--) tree[u] = tree[2 * u] + tree[2 * u + 1];
#define TSET(i, val) do { int _u = P + (i); tree[_u] = (val); _u >>= 1; \
        while (_u >= 1) { tree[_u] = tree[2 * _u] + tree[2 * _u + 1]; _u >>= 1; } } while (0)
    double t = 0.0;
    int64_t ev = 0;
    int f = 0, aborted = 0, isnap = 0;
    double tf = dt_frame;
    for (;;) {
        double a0 = tree[1];
        double tn = t + (-log(unif(&rng)) / a0);
        /* frames in (t, tn] */
        while (f < nframes && tf <= tn && tf <= t_max + 1e-12) {
            double sx = 0, sy = 0;
            for (int j = 0; j < N; j++) {
                double ex = exp(-(tf - tl[j]) / tau);
                double xc = role[j] == RC, xv = role[j] == RV;
                fC[j] = xc + (yC[j] - xc) * ex;
                fV[j] = xv + (yV[j] - xv) * ex;
            }
            for (int i = 0; i < N; i++) {
                double c = 0, v = 0;
                for (int e = boff[i]; e < boff[i + 1]; e++) { c += fC[bidx[e]]; v += fV[bidx[e]]; }
                int nbi = boff[i + 1] - boff[i];
                double X = (c / nbi - cs) / sc, Y = (v / nbi - vs) / sv;
                phi[i] = atan2(Y, X);
                amp[i] = sqrt(X * X + Y * Y);
                sx += cos(phi[i]);
                sy += sin(phi[i]);
            }
            for (int r = 0; r < 4; r++) gcount[4 * f + r] = (int32_t)cnt[r];
            double sa = 0, sd = 0;
            int64_t tw = 0, nd0 = g_nd;
            for (int q = 0; q < ntri; q++) {
                int a = tri[3 * q], b = tri[3 * q + 1], c = tri[3 * q + 2];
                double ta = (amp[a] + amp[b] + amp[c]) / 3.0;
                sa += ta;
                int w = wind3(phi, a, b, c);
                if (w) { dpush(q, (int8_t)w); sd += ta; tw += w; }
            }
            if (fstat) {
                fstat[5 * f + 0] = sqrt(sx * sx + sy * sy) / N;
                fstat[5 * f + 1] = sa;
                fstat[5 * f + 2] = sd;
                fstat[5 * f + 3] = (double)tw;
                fstat[5 * f + 4] = (double)(g_nd - nd0);
            }
            if (isnap < nsnap && snapf[isnap] == f) {
                for (int i = 0; i < N; i++) {
                    double u = (phi[i] + M_PI) / (2 * M_PI) * 256.0;
                    int qv = (int)u;
                    snap[(int64_t)isnap * N + i] = (uint8_t)(qv & 255);
                }
                isnap++;
            }
            f++;
            tf = (f + 1) * dt_frame;
        }
        if (twacc) { /* time-weighted moments of the role fractions over [t, min(tn, t_max)) (H3) */
            double te = tn < t_max ? tn : t_max, ta = t, Tb = t_max / nbatch;
            while (ta < te) {
                int b = (int)(ta / Tb);
                if (b >= nbatch) b = nbatch - 1;
                double be = (b + 1) * Tb, seg = (te < be ? te : be) - ta;
                if (b == nbatch - 1) seg = te - ta;
                double *A = twacc + 6 * b, xc = cnt[0] / (double)N;
                A[0] += seg;
                for (int r = 0; r < 4; r++) A[1 + r] += seg * cnt[r] / (double)N;
                A[5] += seg * xc * xc;
                ta += seg;
                if (seg <= 0) break;
            }
        }
        if (tn > t_max || f >= nframes) break;
        t = tn;
        /* choose site */
        double u = unif(&rng) * a0;
        int node = 1;
        while (node < P) {
            int l = 2 * node;
            if (u < tree[l]) node = l; else { u -= tree[l]; node = l + 1; }
        }
        int i = node - P;
        if (i >= N || tree[node] <= 0.0) continue; /* rounding guard: redraw (no time advance lost: t set) */
        int r = role[i], rn;
        double ri = tree[node], u2 = unif(&rng) * ri;
        if (r == RC) rn = (u2 < k[0]) ? RL : (u2 < k[0] + k[5]) ? RP : RV;
        else if (r == RV) rn = RC;
        else if (r == RL) rn = (u2 < k[3]) ? RV : RC;
        else rn = RV;
        /* filter of site i advanced to t with old indicator */
        {
            double ex = exp(-(t - tl[i]) / tau);
            double xc = r == RC, xv = r == RV;
            yC[i] = xc + (yC[i] - xc) * ex;
            yV[i] = xv + (yV[i] - xv) * ex;
            tl[i] = t;
        }
        role[i] = (int8_t)rn;
        cnt[r]--; cnt[rn]++;
        if (chg && f < nframes) chg[(int64_t)f * nb + (i >> 3)] |= (uint8_t)(1u << (i & 7));
        if (r == RC || rn == RC) {
            int d = (rn == RC) ? 1 : -1;
            for (int e = off[i]; e < off[i + 1]; e++) {
                int j = nbr[e];
                nc[j] += d;
                if (role[j] == RC || role[j] == RV) TSET(j, site_rate(role[j], j, nc, toff, FR, FC, k));
            }
        }
        TSET(i, site_rate(rn, i, nc, toff, FR, FC, k));
        ev++;
        if ((ev & 0xFFFF) == 0 && max_cpu > 0 && cpu_now() - cpu0 > max_cpu) { aborted = 1; break; }
    }
    stats[0] = (double)ev; stats[1] = f; stats[2] = aborted; stats[3] = (double)g_nd; stats[4] = t;
    free(tree); free(nc); free(yC); free(yV); free(tl); free(fC); free(fV); free(phi); free(amp);
    return aborted;
}

/* ---------- lumped exact chain on K ---------- */
/* FRt[m] = F_kr(m/(N-1)), FCt[m] = F_kc(m/(N-1)), m = 0..N-1. out: nsamp x 4 counts at t = (s+1) dt_s */
int gg_run_lumped(int N, const double *FRt, const double *FCt, const double *k, const int64_t *n0, double t_max,
                  double dt_s, int nsamp, uint64_t seed, int32_t *out, double *stats) {
    rng_t rng;
    rng_seed(&rng, seed);
    int64_t n[4] = {n0[0], n0[1], n0[2], n0[3]};
    double t = 0.0, a[8];
    int s = 0;
    int64_t ev = 0;
    double ts = dt_s;
    for (;;) {
        int64_t C = n[0];
        double fcC = C > 0 ? FCt[C - 1] : 0.0; /* C site sees C-1 C neighbours */
        a[0] = n[0] * k[0];                     /* C->L */
        a[1] = n[0] * k[5];                     /* C->P */
        a[2] = n[0] * (k[1] + k[9] * fcC);      /* C->V */
        a[3] = n[1] * (k[8] + k[2] * FRt[C]);   /* V->C */
        a[4] = n[2] * k[3];                     /* L->V */
        a[5] = n[2] * k[4];                     /* L->C */
        a[6] = n[3] * k[6];                     /* P->V */
        double a0 = 0;
        for (int q = 0; q < 7; q++) a0 += a[q];
        double tn = t + (-log(unif(&rng)) / a0);
        while (s < nsamp && ts <= tn && ts <= t_max + 1e-12) {
            for (int r = 0; r < 4; r++) out[4 * s + r] = (int32_t)n[r];
            s++;
            ts = (s + 1) * dt_s;
        }
        if (tn > t_max || s >= nsamp) break;
        t = tn;
        double u = unif(&rng) * a0, acc = 0;
        int q = 6;
        for (int j = 0; j < 7; j++) { acc += a[j]; if (u < acc) { q = j; break; } }
        switch (q) {
            case 0: n[0]--; n[2]++; break;
            case 1: n[0]--; n[3]++; break;
            case 2: n[0]--; n[1]++; break;
            case 3: n[1]--; n[0]++; break;
            case 4: n[2]--; n[1]++; break;
            case 5: n[2]--; n[0]++; break;
            default: n[3]--; n[1]++; break;
        }
        ev++;
    }
    stats[0] = (double)ev; stats[1] = s; stats[2] = t;
    return 0;
}

