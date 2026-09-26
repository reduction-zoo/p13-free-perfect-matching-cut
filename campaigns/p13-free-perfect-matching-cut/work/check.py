"""Independent decision oracles for Positive 1-in-3-SAT and P13-free cuts."""

import argparse
import json
import random
import subprocess
import sys
from itertools import product
from pathlib import Path

import z3


def legal_source(source):
    if not isinstance(source,dict):
        return False
    n,clauses = source.get("num_vars"),source.get("clauses")
    return (type(n) is int and n >= 0 and isinstance(clauses,list)
            and all(isinstance(clause,list) and len(clause) == 3
                    and all(type(v) is int and 0 <= v < n for v in clause)
                    and len(set(clause)) == 3 for clause in clauses))


def direct_one_in_three(source,assignment):
    return (isinstance(assignment,list) and len(assignment) == source["num_vars"]
            and all(type(value) is bool for value in assignment)
            and all(sum(assignment[v] for v in clause) == 1
                    for clause in source["clauses"]))


def solve_source(source):
    if not legal_source(source):
        raise ValueError("Illegal Positive 1-in-3-SAT formula")
    variables = [z3.Bool(f"x_{i}") for i in range(source["num_vars"])]
    solver = z3.Solver()
    for clause in source["clauses"]:
        solver.add(z3.Sum(*[z3.If(variables[v],1,0) for v in clause]) == 1)
    result = solver.check()
    if result not in (z3.sat,z3.unsat):
        raise RuntimeError(f"Inconclusive source solver: {result}")
    if result == z3.sat:
        model = solver.model()
        assignment = [z3.is_true(model.eval(v,model_completion=True)) for v in variables]
        if not direct_one_in_three(source,assignment):
            raise AssertionError("Z3 source answer violates direct predicate")
    return {"answer":result == z3.sat}


def valid_source(source,output):
    return (legal_source(source) and isinstance(output,dict)
            and set(output) == {"answer"} and type(output["answer"]) is bool
            and output == solve_source(source))


def adjacency(target):
    neighbors = [set() for _ in range(target["vertices"])]
    for u,v in target["edges"]:
        neighbors[u].add(v)
        neighbors[v].add(u)
    return neighbors


def induced_path_exists(neighbors,length):
    if len(neighbors) < length:
        return False

    def extend(path):
        if len(path) == length:
            return True
        for v in neighbors[path[-1]]:
            if v in path or any(v in neighbors[u] for u in path[:-1]):
                continue
            if extend(path+[v]):
                return True
        return False

    return any(extend([start]) for start in range(len(neighbors)))


def legal_target(target):
    if not isinstance(target,dict):
        return False
    n,edges = target.get("vertices"),target.get("edges")
    if type(n) is not int or n < 0 or not isinstance(edges,list):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    return not induced_path_exists(adjacency(target),13)


def direct_cut(target,side):
    n = target["vertices"]
    return (isinstance(side,list) and len(side) == n
            and all(type(value) is bool for value in side)
            and any(side) and not all(side)
            and all(sum(side[u] != side[v] for v in neighbors) == 1
                    for u,neighbors in enumerate(adjacency(target))))


def solve_target(target):
    if not legal_target(target):
        raise ValueError("Illegal P13-free graph")
    n = target["vertices"]
    side = [z3.Bool(f"side_{v}") for v in range(n)]
    solver = z3.Solver()
    solver.add(z3.Or(*side),z3.Or(*[z3.Not(value) for value in side]))
    for u,neighbors in enumerate(adjacency(target)):
        solver.add(z3.Sum(*[z3.If(side[u] != side[v],1,0) for v in neighbors]) == 1)
    result = solver.check()
    if result not in (z3.sat,z3.unsat):
        raise RuntimeError(f"Inconclusive target solver: {result}")
    if result == z3.sat:
        model = solver.model()
        bits = [z3.is_true(model.eval(value)) for value in side]
        if not direct_cut(target,bits):
            raise AssertionError("Z3 target decision lacks valid cut")
    return {"answer":result == z3.sat}


def valid_target(target,output):
    return (legal_target(target) and isinstance(output,dict)
            and set(output) == {"answer"} and type(output["answer"]) is bool
            and output == solve_target(target))


def exhaustive_target(target):
    return {"answer":any(direct_cut(target,list(bits))
                         for bits in product((False,True),repeat=target["vertices"]))}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert solve_source(source) == {"answer":expected}
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        exhaustive = any(direct_one_in_three(source,list(bits))
                         for bits in product((False,True),repeat=source["num_vars"]))
        assert current == case["expected"] == {"answer":exhaustive}
        assert valid_source(source,current)
    test_hand_cases()
    checked,seen = 0,set()
    for seed in range(200):
        rng = random.Random(seed)
        n = rng.randrange(9)
        edges = [[u,v] for u in range(n) for v in range(u+1,n) if rng.randrange(3) == 0]
        target = {"vertices":n,"edges":edges}
        key = json.dumps(target,sort_keys=True)
        if key not in seen and legal_target(target):
            seen.add(key)
            assert solve_target(target) == exhaustive_target(target)
            checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive target graphs")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal P13-free target: {target}")
        output = solve_target(target)
        payload = {"source":source,"target_solution":output}
        extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
        recovered_output = json.loads(extraction.stdout)
        if not valid_source(source,recovered_output):
            raise AssertionError(f"Invalid decision recovery from {output}: {recovered_output}")
        recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target decisions")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
