import unittest
from math import factorial

import _path  # noqa: F401
from phys2_order.dynamics import ARM_BY_NAME, SYNC, simulate
from phys2_order.relabel import (
    GROUPS, LABELED, POSITIONAL, apply, apply_buggy_reversal,
    apply_to_configuration, apply_to_configuration_buggy_reversal,
    apply_to_protocol, equivalent, group_elements, make_record,
)
from phys2_order.stages import L, LR, O1, O2
from phys2_order.words import achiral_words, all_words, rev, rot


def _records(n, k, protocol):
    out = []
    for w in achiral_words(n)[:3]:
        for d in range(n):
            ph = (0, d) if k == 2 else (0, d, (2 * d + 1) % n)
            for arm in ("(MASK,PAUSE)", "CONTROL"):
                o = simulate(w, ph, protocol, ARM_BY_NAME[arm])
                for mode in (LABELED, POSITIONAL):
                    out.append(make_record(w, protocol, o, mode))
    return out


class GroupStructure(unittest.TestCase):
    def test_sizes(self):
        for n in (3, 5):
            for k in (2, 3):
                base = factorial(k) * n
                self.assertEqual(len(list(group_elements("G1", n, k))), base)
                self.assertEqual(len(list(group_elements("G2", n, k))), 2 * base)
                self.assertEqual(len(list(group_elements("G3", n, k))), 4 * base)

    def test_closure_on_records(self):
        """Orbits computed by brute force are closed under a second application."""
        for k, proto in ((2, O1), (3, L)):
            for rec in _records(4, k, proto)[:12]:
                for G in GROUPS:
                    els = list(group_elements(G, 4, k))
                    orbit = {apply(g, rec) for g in els}
                    for r in list(orbit)[:6]:
                        self.assertTrue({apply(g, r) for g in els} <= orbit)

    def test_letter_shown_is_preserved_by_rot_and_rev(self):
        n = 5
        w = "RDCCD"
        for p in range(n):
            for k in range(n):
                w2, ph = apply_to_configuration(((0,), k, False, False), w, (p,))
                self.assertEqual(w2[ph[0]], w[p])
                w2, ph = apply_to_configuration(((0,), k, True, False), w, (p,))
                self.assertEqual(w2[ph[0]], w[p])

    def test_exchange_maps_O1_to_O2_and_L_to_reversed_list(self):
        x = ((0, 1), 0, False, True)
        self.assertEqual(apply_to_protocol(x, O1), O2)
        x3 = ((0, 1, 2), 0, False, True)
        self.assertEqual(apply_to_protocol(x3, L), ((1, 0), (2, 1), (0, 2)))
        swap_bc = ((0, 2, 1), 0, False, False)
        self.assertEqual(apply_to_protocol(swap_bc, L), LR)

    def test_symmetry_of_equivalence(self):
        recs = _records(4, 2, O1) + _records(4, 2, O2)
        for G in GROUPS:
            for r1 in recs[:20]:
                for r2 in recs[:20]:
                    if r1[0] != r2[0]:
                        continue
                    self.assertEqual(equivalent(r1, r2, G, 2),
                                     equivalent(r2, r1, G, 2))


def _orbit_count(configs, group, n, k, act):
    configs = set(configs)
    els = list(group_elements(group, n, k))
    seen, orbits = set(), 0
    for c in sorted(configs):
        if c in seen:
            continue
        orbits += 1
        stack = [c]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            for g in els:
                y = act(g, *x)
                if y in configs and y not in seen:
                    stack.append(y)
    return orbits


class PlantedRelabelBug(unittest.TestCase):
    def test_buggy_reversal_changes_configuration_counts(self):
        n, k = 7, 3
        w = next(w for w in achiral_words(n) if len(set(rot(w, j) for j in range(n))) == n)
        # full configuration space of one achiral word: every rotation, all phases
        configs = {(rot(w, j), (p0, p1, p2)) for j in range(n)
                   for p0 in range(n) for p1 in range(n) for p2 in range(n)}
        good = _orbit_count(configs, "G2", n, k, apply_to_configuration)
        bad = _orbit_count(configs, "G2", n, k, apply_to_configuration_buggy_reversal)
        self.assertNotEqual(good, bad)

    def test_buggy_reversal_changes_two_entity_word_counts(self):
        n = 5
        configs = {(w, (0, d)) for w in all_words(n) if "R" in w and "D" in w
                   for d in range(n)}
        configs = {(rot(w, j), ((0 - j) % n, (d - j) % n))
                   for (w, (_, d)) in configs for j in range(n)}
        good = _orbit_count(configs, "G2", n, 2, apply_to_configuration)
        bad = _orbit_count(configs, "G2", n, 2, apply_to_configuration_buggy_reversal)
        self.assertNotEqual(good, bad)

    def test_buggy_reversal_changes_a_verdict(self):
        n = 7
        w = achiral_words(n)[0]
        o = simulate(w, (0, 1, 3), L, ARM_BY_NAME["CONTROL"])
        rec1 = make_record(w, L, o, LABELED)
        # image of rec1 under reversal followed by the rotation that restores w
        k = next(k for k in range(n) if rot(rev(w), k) == w)
        rec2 = apply(((0, 1, 2), k, True, False), rec1)
        self.assertEqual(rec2[1], w)
        self.assertTrue(equivalent(rec1, rec2, "G2", 3))
        self.assertFalse(equivalent(rec1, rec2, "G2", 3, apply_buggy_reversal))
        self.assertFalse(equivalent(rec1, rec2, "G1", 3))


if __name__ == "__main__":
    unittest.main()
