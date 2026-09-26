# Positive 1-in-3-SAT → P13-free Perfect Matching Cut

Category: Complexity open

## Source

The source is Positive 1-in-3-SAT with explicit clauses of three unnegated variables. Its valid output is the correct YES/NO answer.

## Target

The target is a graph with no induced path on thirteen vertices and asks for a nontrivial cut having exactly one opposite neighbor at every vertex. The archived fixed theorem requests decision outputs; it does not establish witness extraction. Its valid output for this fixed theorem is the correct YES/NO answer.

## Required result

Construct a polynomial-time instance map preserving the correct decision answer. Recovery maps the target YES/NO answer to the source answer. The archived theorem is decision-only; no witness recovery theorem is claimed. The requested complexity conclusion is NP-hardness for the stated target problem.

## Acceptance

Give explicit construction and recovery algorithms, a general proof for every legal input and every valid target output, and polynomial runtime and encoding-size bounds. Specify finite output encodings and handle NO-SOLUTION outputs when applicable. Tests compare recovered source outputs with independent source solutions.

## Why it matters

The question addresses a forbidden-path boundary for perfect matching cuts.

## Difficulty

Variable and clause gadgets must compose without creating long induced paths. A decision reduction should not be presented as an established search reduction.

## Literature context

The cited structural classification leaves the P13-free perfect matching cut question separate from hardness on larger induced-path classes.

Literature checked 2026-09-14. This summarizes the archived literature search on the date above. Unpublished, unindexed and overlooked work remains outside coverage; no new novelty assessment was performed.

## References

- [Complexity and algorithms for matching cut problems in graphs without long induced paths and cycles](https://arxiv.org/html/2307.05402v3): - R1: Complexity and algorithms for matching cut problems in graphs without long induced paths and cycles, v3, October 8, 2025, Theorems 3–4, Table 1, Section 3.1, Observation 1, footnote 1, Section 5; JCSS 156 (2026), 103723.
- [JCSS 156 (2026), 103723](https://doi.org/10.1016/j.jcss.2025.103723): - R1: Complexity and algorithms for matching cut problems in graphs without long induced paths and cycles, v3, October 8, 2025, Theorems 3–4, Table 1, Section 3.1, Observation 1, footnote 1, Section 5; JCSS 156 (2026), 103723.

Fixed from board record `website/questions/p13-free-perfect-matching-cut.json` in board checkout at 6c7d3bd9c0a8f595279969a9c0a4d1853a3f5c17; the record was copied from the current working tree.
