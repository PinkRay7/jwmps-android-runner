import pytest
from zrTest.functions import knapsack, knapsack_memo

def test_knapsack_basic():
    W = 10
    weights = (1, 3, 4, 5)
    values = (150, 200, 300, 350)
    n = len(values)
    expected = 800 
    
    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected

def test_knapsack_basic_2():
    W = 10
    weights = (2, 1, 5, 3)
    values = (300, 200, 400, 500)
    n = len(values)
    expected = 1200

    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected

def test_knapsack_no_items():
    W = 10
    weights = ()
    values = ()
    n = len(values)
    expected = 0
    
    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected

def test_knapsack_no_capacity():
    W = 0
    weights = (1, 2, 3)
    values = (0, 20, 30)
    n = len(values)
    expected = 0
    
    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected

def test_knapsack_exact_capacity():
    W = 3
    weights = (1, 3, 4)
    values = (10, 20, 30)
    n = len(values)
    expected = 20
    
    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected

def test_knapsack_large_values():
    W = 50
    weights = (10, 20, 30)
    values = (60, 100, 120)
    n = len(values)
    expected = 220
    
    assert knapsack(W, n, weights, values) == expected
    assert knapsack_memo(W, n, weights, values) == expected