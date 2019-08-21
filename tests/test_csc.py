"""
    To run test_csc only execute: pytest -k csc
"""
import sys

import pytest

sys.path.append('../')
from compress.diagonal_csc import csc


def test_csc_list_nxn_1():
    matrix = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = csc(matrix)
    assert ar == [2, 21, 44, 2, 12]
    assert ia == [0, 3, 1, 0, 1]
    assert ja == [0, 2, 3, 3, 5]


def test_csc_list_nxn_2():
    matrix = [[2, 0, 0, 2], (0, 44, 0, 12), [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = csc(matrix)
    assert ar == [2, 21, 44, 2, 12]
    assert ia == [0, 3, 1, 0, 1]
    assert ja == [0, 2, 3, 3, 5]


def test_csc_list_1xn():
    matrix = [[5, 3, 42, 0, 0, 0, 34]]
    ar, ia, ja = csc(matrix)
    assert ar == [5, 3, 42, 34]
    assert ia == [0, 0, 0, 0]
    assert ja == [0, 1, 2, 3, 3, 3, 3, 4]


def test_csc_list_nx1():
    matrix = [[34], [0], [32], [0]]
    ar, ia, ja = csc(matrix)
    assert ar == [34, 32]
    assert ja == [0, 2]
    assert ia == [0, 2]


def test_csc_zero_matrix():
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = csc(matrix)
    assert ar == []
    assert ja == [0, 0, 0, 0, 0]
    assert ia == []


def test_csc_zero_vector():
    matrix = [[0, 0, 0, 0]]
    ar, ia, ja = csc(matrix)
    assert ar == []
    assert ja == [0, 0, 0, 0, 0]
    assert ia == []


def test_csc_empty_list():
    matrix = []
    with pytest.raises(ValueError, match=r"Empty matrix"):
        csc(matrix)


def test_csc_wrong_matrix_format_1():
    matrix = [[12, 12], "21"]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csc(matrix)


def test_csc_wrong_matrix_format_2():
    matrix = [[12, 12], ["21"]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csc(matrix)


def test_csc_wrong_matrix_format_3():
    matrix = 0.05
    with pytest.raises(TypeError, match=r"Expected list or tuple. Got"):
        csc(matrix)


def test_csc_wrong_matrix_format_4():
    matrix = ""
    with pytest.raises(FileNotFoundError, match=r"File .* not found"):
        csc(matrix)
