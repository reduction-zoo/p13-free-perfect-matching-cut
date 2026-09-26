# Positive 1-in-3-SAT → P13-free Perfect Matching Cut

Independent research campaign for the [fixed question](campaigns/p13-free-perfect-matching-cut/question.md). [State](campaigns/p13-free-perfect-matching-cut/state.md) records the current evidence and next action.

The initial commit fixes the question and setup. [Prepare evidence](campaigns/p13-free-perfect-matching-cut/work/preparation.md), [contract](campaigns/p13-free-perfect-matching-cut/work/contract.md), and [fixed corpus](campaigns/p13-free-perfect-matching-cut/work/cases.json) are committed. The requested result is decision-only; no solution is claimed. Run the campaign from this repository and follow `AGENTS.md`.

Reproduce: `uv sync --locked`, then `uv run --locked python campaigns/p13-free-perfect-matching-cut/work/check.py --self-test`.
