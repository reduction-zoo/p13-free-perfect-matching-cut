# Research instructions

Read the [fixed question](campaigns/p13-free-perfect-matching-cut/question.md), [prior state](campaigns/p13-free-perfect-matching-cut/state.md) and [preparation notes](campaigns/p13-free-perfect-matching-cut/work/preparation.md). The fixed [test corpus](campaigns/p13-free-perfect-matching-cut/work/cases.json) and [verifier](campaigns/p13-free-perfect-matching-cut/work/check.py) are the starting evidence; the preparation notes state their coverage and any pending checks.

Run `uv sync --locked`, then `uv run --locked python campaigns/p13-free-perfect-matching-cut/work/check.py --self-test` before relying on that evidence. Follow the current user's AutoResearch pipeline. Preserve prior evidence, commit new work incrementally and make only evidence-backed claims.
