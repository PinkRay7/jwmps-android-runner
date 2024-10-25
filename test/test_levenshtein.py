import pytest
from zrTest.functions import levenshtein_distance, levenshtein_distance_memo

def test_levenshtein_same_string():
    s1 = "test"
    s2 = "test"
    m = len(s1)
    n = len(s2)
    expected = 0
    assert levenshtein_distance(s1, s2, m, n) == expected
    assert levenshtein_distance_memo(s1, s2, m, n) == expected

def test_levenshtein_empty_string():
    s1 = ""
    s2 = "test"
    m = len(s1)
    n = len(s2)
    expected = len(s2)
    assert levenshtein_distance(s1, s2, m, n) == expected
    assert levenshtein_distance_memo(s1, s2, m, n) == expected

def test_levenshtein_different_length_strings():
    s1 = "kitten"
    s2 = "sitting"
    m = len(s1)
    n = len(s2)
    expected = 3
    assert levenshtein_distance(s1, s2, m, n) == expected
    assert levenshtein_distance_memo(s1, s2, m, n) == expected

def test_levenshtein_one_char_difference():
    s1 = "flaw"
    s2 = "flaws"
    m = len(s1)
    n = len(s2)
    expected = 1
    assert levenshtein_distance(s1, s2, m, n) == expected
    assert levenshtein_distance_memo(s1, s2, m, n) == expected

def test_levenshtein_completely_different():
    s1 = "abc"
    s2 = "xyz"
    m = len(s1)
    n = len(s2)
    expected = 3
    assert levenshtein_distance(s1, s2, m, n) == expected
    assert levenshtein_distance_memo(s1, s2, m, n) == expected
