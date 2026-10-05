"""Cyclic words over {R, D, C}: rotation, reversal, exchange, class counting.

Conventions (used everywhere in the harness):
  rot(w, k)[i] = w[(i + k) % n]
  rev(w)[i]    = w[(-i) % n]
  swap_rd(w)   = w with R and D exchanged, C unchanged
"""

from itertools import product

ALPHABET = "RDC"


def rot(w, k):
    n = len(w)
    k %= n
    return w[k:] + w[:k]


def rev(w):
    n = len(w)
    return "".join(w[(-i) % n] for i in range(n))


def swap_rd(w):
    return w.translate(str.maketrans("RD", "DR"))


def rotations(w):
    return [rot(w, k) for k in range(len(w))]


def representative(w):
    """Representative of the rotation class: lexicographically least rotation."""
    return min(rotations(w))


def is_achiral(w):
    """True if w equals some rotation of its own reversal."""
    return rev(w) in rotations(w)


def all_words(n):
    return ("".join(t) for t in product(ALPHABET, repeat=n))


def rotation_classes(n):
    return sorted({representative(w) for w in all_words(n)})


def reversal_classes(n):
    """Classes under rotation and reversal (bracelets)."""
    return sorted({min(representative(w), representative(rev(w))) for w in all_words(n)})


def chiral_rotation_classes(n):
    return [c for c in rotation_classes(n) if not is_achiral(c)]


def achiral_words(n):
    """One representative per rotation class: achiral and containing R and D."""
    return [c for c in rotation_classes(n)
            if is_achiral(c) and "R" in c and "D" in c]


def validate_word_set(words):
    """Reject anything that is not a valid Stage word set.

    Raises ValueError on a chiral word, a word lacking R or D, a letter
    outside the alphabet, or two words from the same rotation class.
    """
    seen = set()
    for w in words:
        if not w or set(w) - set(ALPHABET):
            raise ValueError("bad letters in word %r" % (w,))
        if "R" not in w or "D" not in w:
            raise ValueError("word %r lacks R or D" % (w,))
        if not is_achiral(w):
            raise ValueError("chiral word %r in word set" % (w,))
        c = representative(w)
        if c in seen:
            raise ValueError("duplicate rotation class for %r" % (w,))
        seen.add(c)
    return True


ANCHORS = {
    "rotation_classes": {3: 11, 4: 24, 5: 51, 6: 130, 7: 315, 8: 834},
    "reversal_classes": {3: 10, 4: 21, 5: 39, 6: 92, 7: 198, 8: 498},
    "chiral_rotation_classes": {3: 2, 4: 6, 5: 24, 6: 76, 7: 234, 8: 672},
    "achiral_RD_words_3_to_5": 21,
    "achiral_RD_pairs_3_to_5": 94,
}


def anchor_counts():
    out = {
        "rotation_classes": {n: len(rotation_classes(n)) for n in range(3, 9)},
        "reversal_classes": {n: len(reversal_classes(n)) for n in range(3, 9)},
        "chiral_rotation_classes": {n: len(chiral_rotation_classes(n))
                                    for n in range(3, 9)},
        "achiral_RD_words_3_to_5": sum(len(achiral_words(n)) for n in (3, 4, 5)),
        "achiral_RD_pairs_3_to_5": sum(n * len(achiral_words(n)) for n in (3, 4, 5)),
    }
    return out


def check_anchors():
    """Raise AssertionError unless every validation anchor matches."""
    got = anchor_counts()
    if got != ANCHORS:
        raise AssertionError("anchor mismatch: got %r expected %r" % (got, ANCHORS))
    return got
