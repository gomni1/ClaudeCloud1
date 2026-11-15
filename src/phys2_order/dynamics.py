"""Deterministic succession with conservative handoffs and refractory arms.

State at an instant: per-entity phase (mod n) and refractory mode, the
protocol pointer, and (sequential schedule only) the sub-step index.

Instants:
  * SYNC: one instant per step; every entity advances between instants.
  * Sequential order (i0, i1, ...): one instant before any advance and one
    after each single advance; entity order[sub] advances next.

At each instant only the next protocol transaction is checked. X->Y fires
iff X shows D and Y shows R. At most one transaction fires per instant.

Refractory, applied to each end of a fired transaction at that end's next
own advance:
  MASK : the advance moves the phase on as usual; the entity shows C until
         its following advance.
  PAUSE: the advance does not move the phase; the entity shows C until its
         following advance.
  NONE : nothing.
Until that next own advance the end keeps showing its letter.

Termination: the pre-check state is a complete description, so the run is
eventually periodic. The run stops at the first repeated pre-check state;
the verdict "never fires" comes from that cycle, never from a step cutoff.
"""

from collections import namedtuple

NONE, MASK, PAUSE = "NONE", "MASK", "PAUSE"

Arm = namedtuple("Arm", "name donor receiver")

ARMS = (
    Arm("(MASK,PAUSE)", MASK, PAUSE),
    Arm("(PAUSE,PAUSE)", PAUSE, PAUSE),
    Arm("(MASK,MASK)", MASK, MASK),
    Arm("(PAUSE,MASK)", PAUSE, MASK),
    Arm("CONTROL", NONE, NONE),
)
ARM_BY_NAME = {a.name: a for a in ARMS}

SYNC = "SYNC"

# per-entity refractory modes
_NORMAL, _PEND_MASK, _PEND_PAUSE, _SHOW_C = 0, 1, 2, 3
_PENDING = {NONE: _NORMAL, MASK: _PEND_MASK, PAUSE: _PEND_PAUSE}

Outcome = namedtuple(
    "Outcome",
    "fired fired_at terminal offsets cycle_start cycle_length",
)
# fired      : tuple of bool, one per protocol position
# fired_at   : tuple of instant index or None
# terminal   : frozenset of phase tuples at step boundaries in the terminal cycle
# offsets    : tuple (p_i - p_0) mod n for i >= 1 in the terminal cycle
# cycle_start, cycle_length : instants


class HarnessError(RuntimeError):
    pass


def _treatments(arm, index, txn, treatment_fn):
    if treatment_fn is not None:
        return treatment_fn(arm, index, txn)
    return arm.donor, arm.receiver


def simulate(word, phases0, protocol, arm, schedule=SYNC, treatment_fn=None):
    """Run one protocol from one starting configuration.

    word      : str over {R, D, C}, shared by all entities
    phases0   : tuple of starting phases, one per entity
    protocol  : tuple of (donor_index, receiver_index)
    arm       : Arm
    schedule  : SYNC, or a tuple giving a fixed sequential update order
    treatment_fn : optional (arm, protocol_index, txn) -> (donor_t, receiver_t);
                   used only by tests to inject faults.
    """
    n = len(word)
    k = len(phases0)
    if schedule != SYNC:
        if sorted(schedule) != list(range(k)):
            raise ValueError("sequential order must be a permutation of entities")
    phases = [p % n for p in phases0]
    modes = [_NORMAL] * k
    ptr = 0
    sub = 0
    fired_at = [None] * len(protocol)
    seen = {}
    history = []
    t = 0

    def shows(i):
        return "C" if modes[i] == _SHOW_C else word[phases[i]]

    def head_holds():
        if ptr >= len(protocol):
            return False
        x, y = protocol[ptr]
        return shows(x) == "D" and shows(y) == "R"

    def advance(i):
        m = modes[i]
        if m == _PEND_MASK:
            phases[i] = (phases[i] + 1) % n
            modes[i] = _SHOW_C
        elif m == _PEND_PAUSE:
            modes[i] = _SHOW_C
        elif m == _SHOW_C:
            phases[i] = (phases[i] + 1) % n
            modes[i] = _NORMAL
        else:
            phases[i] = (phases[i] + 1) % n

    while True:
        state = (tuple(phases), tuple(modes), ptr, sub)
        if state in seen:
            start = seen[state]
            break
        seen[state] = t
        history.append(state)

        if head_holds():
            x, y = protocol[ptr]
            td, tr = _treatments(arm, ptr, (x, y), treatment_fn)
            for i, tt in ((x, td), (y, tr)):
                if modes[i] != _NORMAL:
                    raise HarnessError("entity %d fired again before advancing" % i)
                modes[i] = _PENDING[tt]
            fired_at[ptr] = t
            ptr += 1
            if head_holds():
                # Every protocol in this study has consecutive transactions
                # sharing an entity in opposite roles, so this cannot happen;
                # the one-firing-per-instant convention is therefore immaterial.
                raise HarnessError("two transactions could fire at one instant")

        if schedule == SYNC:
            for i in range(k):
                advance(i)
        else:
            advance(schedule[sub])
            sub = (sub + 1) % k
        t += 1

    cycle = history[start:]
    if len({s[2] for s in cycle}) != 1:
        raise HarnessError("protocol pointer moved inside terminal cycle")
    if any(m != _NORMAL for s in cycle for m in s[1]):
        raise HarnessError("refractory mode inside terminal cycle")
    terminal = frozenset(s[0] for s in cycle if s[3] == 0)
    offs = {tuple((p[i] - p[0]) % n for i in range(1, k)) for p in terminal}
    if len(offs) != 1:
        raise HarnessError("terminal cycle is not free-running at fixed offsets")
    return Outcome(
        fired=tuple(f is not None for f in fired_at),
        fired_at=tuple(fired_at),
        terminal=terminal,
        offsets=offs.pop(),
        cycle_start=start,
        cycle_length=len(cycle),
    )
