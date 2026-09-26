# Prepared decision contract

The Positive 1-in-3-SAT source input is `{"num_vars": n, "clauses":
[[v1,v2,v3], ...]}` with `n >= 0` and each clause containing three
distinct unnegated variable indices in `0..n-1`. Repeated clauses are
allowed. Its output is `{"answer": true}` exactly when an assignment
gives exactly one true variable to every clause, and `{"answer": false}`
otherwise. The archived question requests a decision result, so an
assignment is an internal oracle certificate, not a required output.

The target input is `{"vertices": n, "edges": [[u,v], ...]}` with a
simple undirected graph containing no induced path on thirteen vertices.
Disconnected and empty graphs are allowed. Its output is `{"answer":
true}` exactly when there is a nontrivial two-side partition in which
every vertex has exactly one opposite-side neighbor; otherwise it is
`{"answer": false}`. A cut witness is an internal certificate, not part
of this fixed theorem's output contract.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": {"answer": bool}}` and writes
the correct source decision. The commands share no memory, exit nonzero
on errors, and send diagnostics to stderr. They must be deterministic and
polynomial time. Both target decisions must be mapped correctly.

`check.py --candidate PATH` independently decides every constructed target
on the fixed source corpus and checks the recovered source decision.
