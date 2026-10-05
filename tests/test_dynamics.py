import unittest

import _path  # noqa: F401
from phys2_order.dynamics import ARM_BY_NAME, ARMS, MASK, NONE, PAUSE, SYNC, simulate
from phys2_order.stages import L, LR, O1, O2, compare, run_stage
from phys2_order.relabel import GROUPS, LABELED, POSITIONAL
from phys2_order.words import achiral_words, rot

MP = ARM_BY_NAME["(MASK,PAUSE)"]
PP = ARM_BY_NAME["(PAUSE,PAUSE)"]
MM = ARM_BY_NAME["(MASK,MASK)"]
CONTROL = ARM_BY_NAME["CONTROL"]


class HandTraces(unittest.TestCase):
    """Word DRR: D at phase 0, R at phases 1 and 2. Traces derived by hand."""

    def test_control_free_running(self):
        o = simulate("DRR", (0, 1), O1, CONTROL)
        # instant 0: A=0 (D), B=1 (R) -> A->B fires.
        # instant 2: A=2 (R), B=0 (D) -> B->A fires.
        self.assertEqual(o.fired, (True, True))
        self.assertEqual(o.fired_at, (0, 2))
        self.assertEqual(o.offsets, (1,))
        o = simulate("DRR", (0, 1), O2, CONTROL)
        self.assertEqual(o.fired_at, (2, 3))
        self.assertEqual(o.offsets, (1,))

    def test_mask_pause_O1(self):
        o = simulate("DRR", (0, 1), O1, MP)
        # instant 0: A->B fires. instant 1: A=1 masked, B=1 paused (both C).
        # instant 2: A=2, B=2; offset 0 for ever, B->A never fires.
        self.assertEqual(o.fired, (True, False))
        self.assertEqual(o.fired_at, (0, None))
        self.assertEqual(o.offsets, (0,))
        self.assertEqual(o.terminal, frozenset({(0, 0), (1, 1), (2, 2)}))
        self.assertEqual(o.cycle_length, 3)

    def test_mask_pause_O2(self):
        o = simulate("DRR", (0, 1), O2, MP)
        # instant 2: A=2 (R), B=0 (D): B->A fires. instant 3: A=2 held, B=1.
        # instant 4: A=0 (D), B=2 (R): A->B fires. instant 5: A=1, B=2 held.
        # instant 6: A=2, B=0: offset 1.
        self.assertEqual(o.fired_at, (2, 4))
        self.assertEqual(o.offsets, (1,))

    def test_pause_pause(self):
        o = simulate("DRR", (0, 1), O1, PP)
        # instant 0 fire; instant 1 both held at 0,1; instant 2: 1,2;
        # instant 3: A=2 (R), B=0 (D) -> B->A fires.
        self.assertEqual(o.fired_at, (0, 3))
        self.assertEqual(o.offsets, (1,))

    def test_mask_mask(self):
        o = simulate("DRR", (0, 1), O1, MM)
        # instant 2: A=2, B=0 but both were masked only at instant 1 -> fires.
        self.assertEqual(o.fired_at, (0, 2))
        self.assertEqual(o.offsets, (1,))

    def test_never_fires_is_a_cycle_verdict(self):
        o = simulate("DRR", (0, 0), O1, CONTROL)
        self.assertEqual(o.fired, (False, False))
        self.assertEqual(o.cycle_start, 0)
        self.assertEqual(o.cycle_length, 3)

    def test_sequential_trace(self):
        # Order (A, B), CONTROL, word DRR, phases (0, 0):
        # instants: (0,0) (1,0) (1,1) (2,1) (2,2) (0,2): at instant 5 A=0 D,
        # B=2 R -> A->B fires. Under SYNC the offset stays 0 and A, B always
        # show the same letter, so nothing ever fires.
        o = simulate("DRR", (0, 0), O1, CONTROL, schedule=(0, 1))
        self.assertEqual(o.fired_at[0], 5)
        self.assertEqual(simulate("DRR", (0, 0), O1, CONTROL).fired, (False, False))

    def test_sequential_pause_holds_own_advance(self):
        # Order (B, A), (MASK,PAUSE), DRR, phases (0, 1). Step boundaries are
        # the even instants.
        # instant 0: A=0 D, B=1 R -> A->B fires.
        # instant 1: B's own advance is the pause: B stays 1, shows C.
        # instant 2: A's own advance is the mask: A -> 1, shows C.
        # instant 3: B -> 2.  instant 4: A -> 2 (offset 0 at this boundary).
        # instant 5: B -> 0 (D) while A=2 (R) -> B->A fires.
        # instant 6: A paused at 2.  instant 7: B masked -> 1.
        # instant 8: A -> 0, B=1: offset 1 from here on.
        o = simulate("DRR", (0, 1), O1, MP, schedule=(1, 0))
        self.assertEqual(o.fired_at, (0, 5))
        self.assertEqual(o.offsets, (1,))


class PlantedInequivalence(unittest.TestCase):
    def test_hand_built_configuration_detected(self):
        # From the traces above: O1 fires one transaction, O2 fires two.
        _, _, ineq = compare("DRR", (0, 1), O1, O2, MP, SYNC)
        for g in GROUPS:
            for m in (LABELED, POSITIONAL):
                self.assertTrue(ineq[(g, m)], (g, m))

    def test_control_same_configuration_equivalent(self):
        _, _, ineq = compare("DRR", (0, 1), O1, O2, CONTROL, SYNC)
        self.assertFalse(any(ineq.values()))


def _buggy_treatment(arm, index, txn):
    # order-dependent fault: the first transaction of any protocol pauses its receiver
    return (NONE, PAUSE) if index == 0 else (NONE, NONE)


class PlantedControlBug(unittest.TestCase):
    def test_control_zero_stage1_small(self):
        rows = run_stage(1, cadences=(3, 4, 5), arms=(CONTROL,))
        self.assertEqual(len(rows), 94)
        self.assertFalse(any(any(r["ineq"].values()) for r in rows))

    def test_injected_bug_is_flagged(self):
        rows = run_stage(1, cadences=(3, 4, 5), arms=(CONTROL,),
                         treatment_fn=_buggy_treatment)
        self.assertGreater(sum(r["ineq"][("G1", LABELED)] for r in rows), 0)
        self.assertGreater(sum(r["ineq"][("G3", LABELED)] for r in rows), 0)


class Covariance(unittest.TestCase):
    def test_gauge_rotation_of_representative(self):
        """Choosing another rotation of the word as representative (with phases
        shifted to match) must not change any verdict."""
        for arm in ARMS:
            for n in (3, 4, 5):
                for w in achiral_words(n):
                    for d in range(n):
                        _, _, base = compare(w, (0, d), O1, O2, arm, SYNC)
                        for j in range(1, n):
                            w2 = rot(w, j)
                            ph = ((0 - j) % n, (d - j) % n)
                            _, _, other = compare(w2, ph, O1, O2, arm, SYNC)
                            self.assertEqual(base, other, (arm, w, d, j))

    def test_no_harness_error_stage2_small(self):
        rows = run_stage(2, cadences=(3, 4), schedules=(SYNC, (0, 1, 2), (2, 1, 0)))
        self.assertTrue(rows)

    def test_protocols(self):
        self.assertEqual(O1, ((0, 1), (1, 0)))
        self.assertEqual(O2, ((1, 0), (0, 1)))
        self.assertEqual(L, ((0, 1), (1, 2), (2, 0)))
        self.assertEqual(LR, ((0, 2), (2, 1), (1, 0)))


if __name__ == "__main__":
    unittest.main()
