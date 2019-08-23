"""
    To run test_addition only execute: pytest -k addition
"""
import sys

import pytest

sys.path.append('../')
from operations.addition_subtraction import csc_addition_matrices, csr_addition_matrices


def test_addition_csr_mxn():
    matrix_1 = [[1, 0, 3], [0, 0, 5]]
    matrix_2 = [[1, 0, 3], [0, 0, 5]]
    ar, ia, ja = csr_addition_matrices(matrix_1, matrix_2)
    assert ar == [2, 6, 10]
    assert ia == [0, 2, 3]
    assert ja == [0, 2, 2]


def test_addition_csr_mxn_2():
    matrix_1 = [[1, 0, 3], [0, 0, 5]]
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    ar, ia, ja = csr_addition_matrices(matrix_1, matrix_2)
    assert ar == [1, 2, 3, 1, 10]
    assert ia == [0, 3, 5]
    assert ja == [0, 1, 2, 1, 2]


def test_addition_csr_nxn():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2, 0], [0, 1, 5], [0, 2, 0]]
    ar, ia, ja = csr_addition_matrices(matrix_1, matrix_2)
    assert ar == [1, 2, 3, 1, 10, 1, 7]
    assert ia == [0, 3, 5, 7]
    assert ja == [0, 1, 2, 1, 2, 0, 1]


def test_addition_csr_zero_matrices():
    matrix_1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    matrix_2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = csr_addition_matrices(matrix_1, matrix_2)
    assert ar == []
    assert ia == [0, 0, 0, 0]
    assert ja == []


def test_addition_csr_different_matrices_rows():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    with pytest.raises(ValueError, match=r"Both matrices must have same number of rows."):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csr_different_matrices_columns():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2], [0, 1], [0, 2]]
    with pytest.raises(ValueError, match=r"Both matrices must have same number of columns"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csr_wrong_matrix_format_1():
    matrix_1 = [[12, 12], "21"]
    matrix_2 = [[0, 0], [0, 0]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csr_wrong_matrix_format_2():
    matrix_1 = [[0, 0], [0, 0]]
    matrix_2 = [[12, 12], {"21"}]
    with pytest.raises(ValueError, match=r"All matrix_2's rows must have equal length"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csr_wrong_matrix_format_3():
    matrix_1 = [[1, 0, 3], [0, 0], [1, 5, 0]]
    matrix_2 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    with pytest.raises(ValueError, match=r"All matrix_1's rows must have equal length"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csr_empty_matrix():
    matrix_1 = []
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    with pytest.raises(ValueError, match=r"First given matrix is empty"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_mxn():
    matrix_1 = [[1, 0, 3], [0, 0, 5]]
    matrix_2 = [[1, 0, 3], [0, 0, 5]]
    ar, ia, ja = csc_addition_matrices(matrix_1, matrix_2)
    assert ar == [2, 6, 10]
    assert ia == [0, 0, 1]
    assert ja == [0, 1, 1, 3]


def test_addition_csc_mxn_2():
    matrix_1 = [[1, 0, 3], [0, 0, 5]]
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    ar, ia, ja = csc_addition_matrices(matrix_1, matrix_2)
    assert ar == [1, 2, 1, 3, 10]
    assert ia == [0, 0, 1, 0, 1]
    assert ja == [0, 1, 3, 5]


def test_addition_csc_nxn():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2, 0], [0, 1, 5], [0, 2, 0]]
    ar, ia, ja = csc_addition_matrices(matrix_1, matrix_2)
    assert ar == [1, 1, 2, 1, 7, 3, 10]
    assert ia == [0, 2, 0, 1, 2, 0, 1]
    assert ja == [0, 2, 5, 7]


def test_addition_csc_zero_matrices():
    matrix_1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    matrix_2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = csc_addition_matrices(matrix_1, matrix_2)
    assert ar == []
    assert ia == []
    assert ja == [0, 0, 0, 0, 0]


def test_addition_csc_different_matrices_rows():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    with pytest.raises(ValueError, match=r"Both matrices must have same number of rows."):
        csc_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_different_matrices_columns():
    matrix_1 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    matrix_2 = [[0, 2], [0, 1], [0, 2]]
    with pytest.raises(ValueError, match=r"Both matrices must have same number of columns"):
        csr_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_wrong_matrix_format_1():
    matrix_1 = [[12, 12], "21"]
    matrix_2 = [[0, 0], [0, 0]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csc_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_wrong_matrix_format_2():
    matrix_1 = [[0, 0], [0, 0]]
    matrix_2 = [[12, 12], {"21"}]
    with pytest.raises(ValueError, match=r"All matrix_2's rows must have equal length"):
        csc_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_wrong_matrix_format_3():
    matrix_1 = [[1, 0, 3], [0, 0], [1, 5, 0]]
    matrix_2 = [[1, 0, 3], [0, 0, 5], [1, 5, 0]]
    with pytest.raises(ValueError, match=r"All matrix_1's rows must have equal length"):
        csc_addition_matrices(matrix_1, matrix_2)


def test_addition_csc_empty_matrix():
    matrix_1 = []
    matrix_2 = [[0, 2, 0], [0, 1, 5]]
    with pytest.raises(ValueError, match=r"First given matrix is empty"):
        csc_addition_matrices(matrix_1, matrix_2)
