"""Stage runners. Each returns one row per (schedule, arm, word, configuration)."""

from itertools import permutations

from .dynamics import ARMS, SYNC, simulate
from .relabel import GROUPS, LABELED, POSITIONAL, apply, equivalent, make_record
from .words import achiral_words, validate_word_set

A, B, C = 0, 1, 2
O1 = ((A, B), (B, A))
O2 = ((B, A), (A, B))
L = ((A, B), (B, C), (C, A))
LR = ((A, C), (C, B), (B, A))

MODES = (LABELED, POSITIONAL)

STAGE1_CADENCES = tuple(range(3, 9))
STAGE2_CADENCES = tuple(range(3, 7))


def stage1_configs(n):
    words = achiral_words(n)
    validate_word_set(words)
    for w in words:
        for d in range(n):
            yield w, (0, d)


def stage2_configs(n):
    words = achiral_words(n)
    validate_word_set(words)
    for w in words:
        for d1 in range(n):
            for d2 in range(n):
                yield w, (0, d1, d2)


def compare(word, phases, p1, p2, arm, schedule, apply_fn=apply,
            treatment_fn=None, groups=GROUPS, modes=MODES):
    """Run both protocols from one configuration and test equivalence."""
    k = len(phases)
    o1 = simulate(word, phases, p1, arm, schedule, treatment_fn)
    o2 = simulate(word, phases, p2, arm, schedule, treatment_fn)
    ineq = {}
    for mode in modes:
        r1 = make_record(word, p1, o1, mode)
        r2 = make_record(word, p2, o2, mode)
        for g in groups:
            ineq[(g, mode)] = not equivalent(r1, r2, g, k, apply_fn)
    return o1, o2, ineq


def run_stage(stage, cadences=None, arms=ARMS, schedules=None, apply_fn=apply,
              treatment_fn=None, groups=GROUPS, modes=MODES):
    if stage == 1:
        configs, p1, p2, k = stage1_configs, O1, O2, 2
        cadences = cadences or STAGE1_CADENCES
    elif stage == 2:
        configs, p1, p2, k = stage2_configs, L, LR, 3
        cadences = cadences or STAGE2_CADENCES
    else:
        raise ValueError(stage)
    if schedules is None:
        schedules = (SYNC,)
    rows = []
    for sched in schedules:
        for arm in arms:
            for n in cadences:
                for word, phases in configs(n):
                    o1, o2, ineq = compare(word, phases, p1, p2, arm, sched,
                                           apply_fn, treatment_fn, groups, modes)
                    rows.append({
                        "stage": stage, "schedule": sched, "arm": arm.name,
                        "n": n, "word": word, "phases": phases,
                        "out1": o1, "out2": o2, "ineq": ineq,
                    })
    return rows


def sequential_orders(k):
    return tuple(permutations(range(k)))


def count(rows, arm, n, group, mode=LABELED, schedule=SYNC):
    sel = [r for r in rows if r["arm"] == arm and r["n"] == n
           and r["schedule"] == schedule]
    return sum(r["ineq"][(group, mode)] for r in sel), len(sel)
