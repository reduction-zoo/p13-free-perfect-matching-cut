from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    one = {"num_vars":3,"clauses":[[0,1,2]]}
    assert solve_source(one) == {"answer":True}
    assert valid_source(one,{"answer":True})
    complete4 = {"num_vars":4,"clauses":[[a,b,c] for a in range(4) for b in range(a+1,4) for c in range(b+1,4)]}
    assert solve_source(complete4) == {"answer":False}
    assert not valid_source(complete4,{"answer":True})
    assert not legal_source({"num_vars":3,"clauses":[[0,0,1]]})
    assert solve_target({"vertices":2,"edges":[[0,1]]}) == {"answer":True}
    assert solve_target({"vertices":3,"edges":[[0,1],[1,2],[0,2]]}) == {"answer":False}
    assert not valid_target({"vertices":2,"edges":[[0,1]]},{"answer":False})
    path13 = {"vertices":13,"edges":[[i,i+1] for i in range(12)]}
    assert not legal_target(path13)


if __name__ == "__main__":
    test_hand_cases()
