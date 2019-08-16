"""
    To run test_coo only execute: pytest -k coo
"""
import sys
import pytest
sys.path.append('../')
from compress.csr_coo import coo


def test_coo_list_nxn_1():
    matrix = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = coo(matrix)
    assert ar == [2, 2, 44, 12, 21]
    assert ia == [0, 0, 1, 1, 3]
    assert ja == [0, 3, 1, 3, 0]


def test_coo_list_nxn_2():
    matrix = [[2, 0, 0, 2], (0, 44, 0, 12), [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = coo(matrix)
    assert ar == [2, 2, 44, 12, 21]
    assert ia == [0, 0, 1, 1, 3]
    assert ja == [0, 3, 1, 3, 0]


def test_coo_list_1xn():
    matrix = [[5, 3, 42, 0, 0, 0, 34]]
    ar, ia, ja = coo(matrix)
    assert ar == [5, 3, 42, 34]
    assert ia == [0, 0, 0, 0]
    assert ja == [0, 1, 2, 6]


def test_coo_list_nx1():
    matrix = [[34], [0], [32], [0]]
    ar, ia, ja = coo(matrix)
    assert ar == [34, 32]
    assert ia == [0, 2]
    assert ja == [0, 0]


def test_coo_zero_matrix():
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = coo(matrix)
    assert ar == []
    assert ia == []
    assert ja == []


def test_coo_zero_vector():
    matrix = [[0, 0, 0, 0]]
    ar, ia, ja = coo(matrix)
    assert ar == []
    assert ia == []
    assert ja == []


def test_coo_empty_list():
    matrix = []
    with pytest.raises(ValueError, match=r"Empty matrix"):
        coo(matrix)


def test_coo_wrong_matrix_format_1():
    matrix = [[12, 12], "21"]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        coo(matrix)


def test_coo_wrong_matrix_format_2():
    matrix = [[12, 12], ["21"]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        coo(matrix)


def test_coo_wrong_matrix_format_3():
    matrix = ""
    with pytest.raises(TypeError, match=r"Expected list or tuple. Got"):
        coo(matrix)