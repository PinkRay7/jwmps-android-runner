from zrTest.functions import matrix_chain_order, matrix_chain_order_memo

def test_matrix_chain_single_matrix():
    dimensions = (10, 20)
    i = 1
    j = 1
    expected = 0
    assert matrix_chain_order(i, j, dimensions) == expected
    assert matrix_chain_order_memo(i, j, dimensions) == expected

def test_matrix_chain_two_matrices():
    dimensions = (10, 20, 30)
    i = 1
    j = 2
    expected = 6000
    assert matrix_chain_order(i, j, dimensions) == expected
    assert matrix_chain_order_memo(i, j, dimensions) == expected

def test_matrix_chain_three_matrices():
    dimensions = (10, 20, 30, 40)
    i = 1
    j = 3
    expected = 18000
    assert matrix_chain_order(i, j, dimensions) == expected
    assert matrix_chain_order_memo(i, j, dimensions) == expected

def test_matrix_chain_larger():
    dimensions = (10, 20, 30, 40, 50)
    i = 1
    j = 4
    expected = 38000
    assert matrix_chain_order(i, j, dimensions) == expected
    assert matrix_chain_order_memo(i, j, dimensions) == expected