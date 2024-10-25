import pytest
from zrTest.functions import coin_change, coin_change_memo

def test_coin_change_basic():
    coins = [1, 2, 3]
    m = len(coins)
    n = 4
    expected = 4 
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected

def test_coin_change_zero_amount():
    coins = [1, 2, 3]
    m = len(coins)
    n = 0
    expected = 1
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected

def test_coin_change_no_coins():
    coins = []
    m = 0
    n = 5
    expected = 0
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected

def test_coin_change_impossible():
    coins = [2]
    m = 1
    n = 3
    expected = 0
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected

def test_coin_change_large_amount():
    coins = [1, 2, 5]
    m = len(coins)
    n = 11
    expected = 11
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected

def test_coin_change_single_coin():
    coins = [3]
    m = 1
    n = 9
    expected = 1
    assert coin_change(m, n, tuple(coins)) == expected
    assert coin_change_memo(m, n, tuple(coins)) == expected
