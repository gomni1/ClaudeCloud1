"""Lawful relabellings and brute-force outcome equivalence.

An outcome RECORD is (mode, word, fired, terminal):
  word     : the concrete word string the run used
  fired    : labeled mode    -> frozenset of ((donor, receiver), fired_bool),
                                one per intended transaction (order dropped)
             positional mode -> tuple of fired_bool by protocol position
  terminal : frozenset of phase tuples (one entry per entity) visited at
             step boundaries in the terminal cycle

A group element is g = (perm, k, rev, xch) and acts as
  g = P_perm . Rot_k . Rev^rev . X^xch     (X applied first)
with
  X     : word -> swap_rd(word); each (x, y) -> (y, x); phases unchanged
  Rev   : word -> rev(word);     each phase p -> (-p) mod n
  Rot_k : word -> rot(word, k);  each phase p -> (p - k) mod n
  P     : entity i -> perm[i];   (x, y) -> (perm[x], perm[y]);
          new_phases[perm[i]] = old_phases[i]
In positional mode X and P leave the fired tuple unchanged (they map a
protocol position to the same position).

Groups (entity permutations are always included):
  G1 = {P, Rot}
  G2 = G1 + Rev
  G3 = G2 + X
Every element of each group has exactly one normal form above, so iterating
over all (perm, k, rev, xch) enumerates the whole group.

Two records are equivalent under G iff some g in G maps the first exactly
onto the second (concrete word, fired data and terminal set all equal).
"""

from itertools import permutations

from .words import rot, rev, swap_rd

GROUPS = ("G1", "G2", "G3")
LABELED, POSITIONAL = "labeled", "positional"


def make_record(word, protocol, outcome, mode=LABELED):
    if mode == LABELED:
        fired = frozenset(zip(protocol, outcome.fired))
    elif mode == POSITIONAL:
        fired = tuple(outcome.fired)
    else:
        raise ValueError(mode)
    return (mode, word, fired, outcome.terminal)


def group_elements(group, n, k_entities):
    revs = (False, True) if group in ("G2", "G3") else (False,)
    xchs = (False, True) if group == "G3" else (False,)
    if group not in GROUPS:
        raise ValueError(group)
    for perm in permutations(range(k_entities)):
        for k in range(n):
            for r in revs:
                for x in xchs:
                    yield (perm, k, r, x)


def _phases_map(terminal, f):
    return frozenset(tuple(f(p) for p in ph) for ph in terminal)


def apply(g, record):
    """Correct action of g on a record."""
    perm, k, r, x = g
    mode, word, fired, terminal = record
    n = len(word)
    if x:
        word = swap_rd(word)
        if mode == LABELED:
            fired = frozenset(((b, a), f) for (a, b), f in fired)
    if r:
        word = rev(word)
        terminal = _phases_map(terminal, lambda p: (-p) % n)
    if k:
        word = rot(word, k)
        terminal = _phases_map(terminal, lambda p: (p - k) % n)
    if mode == LABELED:
        fired = frozenset(((perm[a], perm[b]), f) for (a, b), f in fired)
    terminal = frozenset(_permute(ph, perm) for ph in terminal)
    return (mode, word, fired, terminal)


def _permute(ph, perm):
    out = [None] * len(ph)
    for i, p in enumerate(ph):
        out[perm[i]] = p
    return tuple(out)


def apply_buggy_reversal(g, record):
    """Planted fault: reversal flips the word but does not remap the phases."""
    perm, k, r, x = g
    if not r:
        return apply(g, record)
    mode, word, fired, terminal = record
    record = (mode, rev(word), fired, terminal)
    return apply((perm, k, False, x), record)


def equivalent(rec1, rec2, group, k_entities, apply_fn=apply):
    n = len(rec1[1])
    for g in group_elements(group, n, k_entities):
        if apply_fn(g, rec1) == rec2:
            return True
    return False


def apply_to_configuration(g, word, phases):
    """Action of g on a starting configuration (word, phase tuple)."""
    perm, k, r, x = g
    n = len(word)
    if x:
        word = swap_rd(word)
    if r:
        word = rev(word)
        phases = tuple((-p) % n for p in phases)
    if k:
        word = rot(word, k)
        phases = tuple((p - k) % n for p in phases)
    return word, _permute(phases, perm)


def apply_to_configuration_buggy_reversal(g, word, phases):
    perm, k, r, x = g
    if r:
        word = rev(word)
    return apply_to_configuration((perm, k, False, x), word, phases)


def apply_to_protocol(g, protocol):
    """Action of g on an ordered protocol (Rot and Rev leave it unchanged)."""
    perm, k, r, x = g
    out = []
    for a, b in protocol:
        if x:
            a, b = b, a
        out.append((perm[a], perm[b]))
    return tuple(out)
