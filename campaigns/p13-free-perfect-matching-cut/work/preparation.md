# Preparation evidence

Prepared on 2026-09-26 before construction. The fixed corpus has 113
distinct legal Positive 1-in-3-SAT formulas: 13 hand-labelled edge cases
and 100 seeded random cases, with 63 YES and 50 NO decisions and zero to
eight variables. `generate_cases.py` retains seeds and generator;
`cases.json` stores independently checked decisions. Positive random
cases come from a hidden exact-one assignment. Negative cases contain
all four triples on four variables, which cannot all have sum one.
Z3 4.16.0 encodes each clause's sum of true variables as exactly one.
SAT models are checked by direct clause evaluation, UNSAT is conclusive,
and unknown is an error. Exhaustive assignments agreed with Z3 on all
113 source cases.

The target legal-instance check searches for an induced thirteen-vertex
path, extending only chordless simple paths; a thirteen-vertex path graph
is rejected by a hand fixture. Z3 encodes a nontrivial side assignment
with exactly one opposite neighbor per vertex. A SAT model is checked
against direct neighbor counts. Independent exhaustive side assignments
agreed with Z3 on 112 distinct target graphs with up to eight vertices.
Hand fixtures cover YES on an edge, NO on a triangle, invalid decisions,
and the P13 promise. All oracle outputs follow the question's decision-only
contract; no witness-extraction theorem is inferred.

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/p13-free-perfect-matching-cut/work/check.py --self-test
```

The self-test begins with the corpus gate, regenerates seeded formulas,
rechecks labels, and compares target decisions to exhaustive enumeration.
The candidate runner uses separate forward and recovery subprocesses.
An incorrect injected candidate was rejected after solving its target
and comparing its recovered decision. No actual reduction candidate
exists; finite checks do not establish hardness or a general reduction.
