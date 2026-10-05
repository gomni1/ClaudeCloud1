import unittest

import _path  # noqa: F401
from phys2_order.words import (
    ANCHORS, achiral_words, anchor_counts, representative, check_anchors,
    is_achiral, rev, rot, swap_rd, validate_word_set,
)


class Conventions(unittest.TestCase):
    def test_rot(self):
        w = "RDCC"
        for k in range(4):
            for i in range(4):
                self.assertEqual(rot(w, k)[i], w[(i + k) % 4])

    def test_rev(self):
        w = "RDCCD"
        for i in range(5):
            self.assertEqual(rev(w)[i], w[(-i) % 5])

    def test_swap(self):
        self.assertEqual(swap_rd("RDCR"), "DRCD")


class Anchors(unittest.TestCase):
    def test_all_anchors(self):
        self.assertEqual(anchor_counts(), ANCHORS)
        check_anchors()

    def test_explicit_values(self):
        got = anchor_counts()
        self.assertEqual([got["rotation_classes"][n] for n in range(3, 9)],
                         [11, 24, 51, 130, 315, 834])
        self.assertEqual([got["reversal_classes"][n] for n in range(3, 9)],
                         [10, 21, 39, 92, 198, 498])
        self.assertEqual([got["chiral_rotation_classes"][n] for n in range(3, 9)],
                         [2, 6, 24, 76, 234, 672])
        self.assertEqual(got["achiral_RD_words_3_to_5"], 21)
        self.assertEqual(got["achiral_RD_pairs_3_to_5"], 94)


class WordSet(unittest.TestCase):
    def test_word_sets_valid(self):
        for n in range(3, 9):
            ws = achiral_words(n)
            self.assertTrue(validate_word_set(ws))
            for w in ws:
                self.assertEqual(w, representative(w))
                self.assertTrue(is_achiral(w))

    def test_planted_chiral_word_rejected(self):
        self.assertFalse(is_achiral("RDC"))
        ws = achiral_words(3) + ["RDC"]
        with self.assertRaises(ValueError):
            validate_word_set(ws)

    def test_other_bad_words_rejected(self):
        for bad in (["RRC"], ["DDC"], ["CCC"], ["DRR", "RDR"], ["RXD"]):
            with self.assertRaises(ValueError):
                validate_word_set(bad)


if __name__ == "__main__":
    unittest.main()
