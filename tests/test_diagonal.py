"""
    To run test_diagonal only execute: pytest -k diagonal
"""
import sys
import pytest
sys.path.append('../')
from compress.diagonal_csc import diagonal


def test_diagonal_list_nxn_1():
    matrix = [
        [11, 0, 13, 0, 0, 0],
        [21, 22, 0, 24, 0, 0],
        [0, 32, 33, 0, 35, 0],
        [0, 0, 43, 44, 0, 46],
        [51, 0, 0, 54, 55, 0],
        [61, 62, 0, 0, 65, 66]
    ]
    ad, la = diagonal(matrix)
    assert ad == (
        [11, 13, 0, 0, 0],
        [22, 24, 21, 0, 0],
        [33, 35, 32, 0, 0],
        [44, 46, 43, 0, 0],
        [55, 0, 54, 51, 0],
        [66, 0, 65, 62, 61]
    )
    assert la == [0, 2, -1, -4, -5]


def test_diagonal_list_nxn_2():
    matrix = [
        [2, 0, 0, 2],
        [0, 44, 0, 12],
        [0, 0, 0, 0],
        [21, 0, 0, 0]
    ]
    ad, la = diagonal(matrix)
    assert ad == (
        [2, 0, 2, 0],
        [44, 12, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 21]
    )
    assert la == [0, 2, 3, -3]


def test_diagonal_list_nxn_3():
    matrix = [
        [2, 0, 0, 0],
        [0, 44, 0, 12],
        [0, 0, 0, 0],
        [21, 0, 0, 55]
    ]
    ad, la = diagonal(matrix)
    assert ad == (
        [2, 0, 0],
        [44, 12, 0],
        [0, 0, 0],
        [55, 0, 21]
    )
    assert la == [0, 2, -3]


def test_diagonal_zero_main_diagonal():
    matrix = [
        [0, 0, 2, 2],
        [2, 0, 0, 12],
        [6, 0, 0, 0],
        [5, 32, 0, 0]
    ]
    ad, la = diagonal(matrix)
    print(ad)
    print(la)
    assert ad == (
        [2, 2, 0, 0, 0],
        [12, 0, 2, 0, 0],
        [0, 0, 0, 6, 0],
        [0, 0, 0, 32, 5]
    )
    assert la == [2, 3, -1, -2, -3]


def test_diagonal_upper_triangular_matrix():
    matrix = [
        [2, 22, 0, 5, 5],
        [0, 0, 2, 0, 0],
        [0, 0, 3, 6, 0],
        [0, 0, 0, 0, 5],
        [0, 0, 0, 0, 2]
    ]
    ad, la = diagonal(matrix)
    assert ad == (
        [2, 22, 5, 5],
        [0, 2, 0, 0],
        [3, 6, 0, 0],
        [0, 5, 0, 0],
        [2, 0, 0, 0]
    )
    assert la == [0, 1, 3, 4]


def test_diagonal_lower_triangular_matrix():
    matrix = [
        [0, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 2, 0, 0],
        [3, 6, 8, 0]
    ]
    ad, la = diagonal(matrix)
    assert ad == (
        [0, 0, 0],
        [1, 0, 0],
        [2, 0, 0],
        [8, 6, 3],
    )
    assert la == [-1, -2, -3]


def test_diagonal_list_nx1():
    matrix = [[34], [0], [32], [0]]
    with pytest.raises(ValueError, match=r"Matrix must be nxn"):
        diagonal(matrix)


def test_diagonal_zero_matrix():
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ad, la = diagonal(matrix)
    assert ad == ([], [], [], [])
    assert la == []


def test_diagonal_empty_list():
    matrix = []
    with pytest.raises(ValueError, match=r"Empty matrix"):
        diagonal(matrix)


def test_diagonal_wrong_matrix_format_1():
    matrix = [[12, 12], "21"]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        diagonal(matrix)


def test_diagonal_wrong_matrix_format_2():
    matrix = [[12, 12], ["21"]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        diagonal(matrix)


def test_diagonal_wrong_matrix_format_3():
    matrix = ""
    with pytest.raises(TypeError, match=r"Expected list or tuple. Got"):
        diagonal(matrix)
