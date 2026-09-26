"""Fix seeded Positive 1-in-3-SAT decisions before construction."""

import json
import random
from itertools import combinations
from pathlib import Path


FOUR_TRIPLES = [list(values) for values in combinations(range(4),3)]


def formula(n,clauses):
    return {"num_vars":n,"clauses":clauses}


EDGE_CASES = [
    (formula(0,[]),True), (formula(1,[]),True), (formula(2,[]),True),
    (formula(3,[[0,1,2]]),True),
    (formula(3,[[0,1,2],[0,1,2]]),True),
    (formula(4,FOUR_TRIPLES),False),
    (formula(4,FOUR_TRIPLES[:3]),True),
    (formula(4,FOUR_TRIPLES+[FOUR_TRIPLES[0]]),False),
    (formula(5,FOUR_TRIPLES),False),
    (formula(5,[]),True),
    (formula(6,[[0,1,2],[3,4,5]]),True),
    (formula(5,[[0,1,2],[0,3,4]]),True),
    (formula(6,FOUR_TRIPLES+[[3,4,5]]),False),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(4,8)
    if seed % 2 == 0:
        hidden = [rng.randrange(2) == 1 for _ in range(n)]
        choices = [list(values) for values in combinations(range(n),3)
                   if sum(hidden[v] for v in values) == 1]
        if not choices:
            hidden = [i == 0 for i in range(n)]
            choices = [list(values) for values in combinations(range(n),3)
                       if sum(hidden[v] for v in values) == 1]
        rng.shuffle(choices)
        clauses = choices[:rng.randint(1,min(12,len(choices)))]
    else:
        clauses = list(FOUR_TRIPLES)
        choices = [list(values) for values in combinations(range(n),3)
                   if list(values) not in clauses]
        rng.shuffle(choices)
        clauses += choices[:rng.randint(0,min(8,len(choices)))]
    return formula(n,clauses)


def build_cases():
    from check import solve_source
    cases,seen = [],set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and answer["answer"] != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
