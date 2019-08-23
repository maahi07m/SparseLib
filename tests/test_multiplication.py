"""
    To run test_multiplication only execute: pytest -k multiplication
"""
import sys

import pytest

sys.path.append('../')
from operations.multiplication import inner_product, outer_product, multiply_matrix_vector, multiply_vector_matrix, \
    matrix_matrix_multiplication


def test_inner_1():
    vector_1 = [[1], [0], [3]]
    vector_2 = [[0], [0], [5]]
    result = inner_product(vector_1, vector_2)
    assert result == 15


def test_inner_2():
    vector_1 = [[1], [0], [0]]
    vector_2 = [[0], [0], [5]]
    result = inner_product(vector_1, vector_2)
    assert result == 0


def test_inner_3():
    vector_1 = [[1], [0], [5]]
    vector_2 = [[0], [0], [5]]
    result = inner_product(vector_1, vector_2)
    assert result == 25


def test_inner_wrong_vector_format_1():
    vector_1 = [[1, 0, 3]]
    vector_2 = [[0, 0, 5]]
    with pytest.raises(ValueError, match=r"Both vectors must be nx1 size."):
        inner_product(vector_1, vector_2)


def test_inner_wrong_vector_format_2():
    vector_1 = [[1], [0], [0]]
    vector_2 = [[0, 0, 5]]
    with pytest.raises(ValueError, match=r"Both vectors must be nx1 size."):
        inner_product(vector_1, vector_2)


def test_inner_wrong_vector_format_3():
    vector_1 = [[]]
    vector_2 = [[]]
    with pytest.raises(ValueError, match=r"Both vectors must be nx1 size"):
        inner_product(vector_1, vector_2)


def test_inner_empty_vectors():
    vector_1 = []
    vector_2 = []
    with pytest.raises(ValueError, match=r"Empty vector_1 was given"):
        inner_product(vector_1, vector_2)


def test_inner_empty_vector_2():
    vector_1 = [[1], [0], [0]]
    vector_2 = []
    with pytest.raises(ValueError, match=r"Empty vector_2 was given"):
        inner_product(vector_1, vector_2)


def test_outer_1():
    vector_1 = [[1, 0, 3]]
    vector_2 = [[3, 0, 5]]
    ar, ia, ja = outer_product(vector_1, vector_2)
    assert ar == [3, 5, 9, 15]
    assert ia == [0, 2, 2, 4]
    assert ja == [0, 2, 0, 2]


def test_outer_2():
    vector_1 = [[1, 0, 0]]
    vector_2 = [[0, 0, 5]]
    ar, ia, ja = outer_product(vector_1, vector_2)
    assert ar == [5]
    assert ia == [0, 1, 1, 1]
    assert ja == [2]


def test_outer_3():
    vector_1 = [[3, 0, 5]]
    vector_2 = [[3, 0, 5]]
    ar, ia, ja = outer_product(vector_1, vector_2)
    assert ar == [9, 15, 15, 25]
    assert ia == [0, 2, 2, 4]
    assert ja == [0, 2, 0, 2]


def test_outer_wrong_vector_format_1():
    vector_1 = [[1], [0], [0]]
    vector_2 = [[0], [0], [5]]
    with pytest.raises(ValueError, match=r"Both vectors must be 1xn size."):
        outer_product(vector_1, vector_2)


def test_outer_wrong_vector_format_2():
    vector_1 = [[1], [0], [0]]
    vector_2 = [[0, 0, 5]]
    with pytest.raises(ValueError, match=r"Both vectors must be 1xn size."):
        outer_product(vector_1, vector_2)


def test_outer_wrong_vector_format_3():
    vector_1 = [[], []]
    vector_2 = [[], []]
    with pytest.raises(ValueError, match=r"Both vectors must be 1xn size."):
        outer_product(vector_1, vector_2)


def test_outer_empty_vector_1():
    vector_1 = []
    vector_2 = [[3, 0, 5]]
    with pytest.raises(ValueError, match=r"Empty vector_1 was given"):
        inner_product(vector_1, vector_2)


def test_outer_empty_vector_2():
    vector_1 = [[3, 0, 5]]
    vector_2 = []
    with pytest.raises(ValueError, match=r"Empty vector_2 was given"):
        inner_product(vector_1, vector_2)


def test_matrix_vector_1():
    matrix = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0], [4]]
    ar, ia, ja = multiply_matrix_vector(matrix, vector)
    assert ar == [12, 48, 42]
    assert ia == [0, 1, 3]
    assert ja == [0, 3]


def test_matrix_vector_2():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0], [4]]
    ar, ia, ja = multiply_matrix_vector(matrix, vector)
    assert ar == [48, 42]
    assert ia == [0, 2]
    assert ja == [0, 2]


def test_matrix_vector_3():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[0], [0], [0], [0]]
    ar, ia, ja = multiply_matrix_vector(matrix, vector)
    assert ar == []
    assert ia == []
    assert ja == [0, 0]


def test_matrix_vector_wrong_format_1():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0]]
    with pytest.raises(ValueError, match=r"Wrong inputs. Matrix must be mxn or nxn and vector nx1."):
        multiply_matrix_vector(matrix, vector)


def test_matrix_vector_wrong_format_2():
    matrix = [[0, 44, 0, 12], [0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0]]
    with pytest.raises(ValueError, match=r"Wrong inputs. Matrix must be mxn or nxn and vector nx1."):
        multiply_matrix_vector(matrix, vector)


def test_matrix_vector_wrong_format_3():
    matrix = [[0, 44, 0, 12], [0, 0, 0], [21, 0, 0, 0]]
    vector = [[0], [0], [0], [0]]
    with pytest.raises(ValueError, match=r"All matrix's rows must have equal length"):
        multiply_matrix_vector(matrix, vector)


def test_matrix_vector_wrong_format_4():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[0], [0], [0], [0, 1]]
    with pytest.raises(ValueError, match=r"All vectors's rows must contain only one element"):
        multiply_matrix_vector(matrix, vector)


def test_matrix_vector_empty_vector():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = []
    with pytest.raises(ValueError, match=r"Empty vector was given"):
        multiply_matrix_vector(matrix, vector)


def test_matrix_vector_empty_matrix():
    matrix = []
    vector = [[2], [0], [0]]
    with pytest.raises(ValueError, match=r"Empty matrix was given"):
        multiply_matrix_vector(matrix, vector)


def test_vector_matrix_1():
    matrix = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2, 0, 0, 4]]
    ar, ia, ja = multiply_vector_matrix(matrix, vector)
    assert ar == [88, 4]
    assert ia == [0, 2]
    assert ja == [0, 3]


def test_vector_matrix_2():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2, 0, 4]]
    ar, ia, ja = multiply_vector_matrix(matrix, vector)
    assert ar == [84, 88, 24]
    assert ia == [0, 3]
    assert ja == [0, 1, 3]


def test_vector_matrix_3():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[0, 0, 0]]
    ar, ia, ja = multiply_vector_matrix(matrix, vector)
    assert ar == []
    assert ia == [0, 0]
    assert ja == []


def test_vector_matrix_wrong_format_1():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0]]
    with pytest.raises(ValueError, match=r"Wrong inputs. Matrix must be mxn or nxn and vector 1xn."):
        multiply_vector_matrix(matrix, vector)


def test_vector_matrix_wrong_format_2():
    matrix = [[0, 44, 0, 12], [0, 0], [21, 0, 0, 0]]
    vector = [[2], [0], [0]]
    with pytest.raises(ValueError, match=r"Wrong inputs. Matrix must be mxn or nxn and vector 1xn."):
        multiply_vector_matrix(matrix, vector)


def test_vector_matrix_wrong_format_3():
    matrix = [[0, 44, 0, 12], [0, 0, 0], [21, 0, 0, 0]]
    vector = [[2, 0, 4]]
    with pytest.raises(ValueError, match=r"All matrix's rows must have equal length"):
        multiply_vector_matrix(matrix, vector)


def test_vector_matrix_empty_vector():
    matrix = [[0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    vector = []
    with pytest.raises(ValueError, match=r"Empty vector was given"):
        multiply_vector_matrix(matrix, vector)


def test_vector_matrix_empty_matrix():
    matrix = []
    vector = [[2, 0, 4]]
    with pytest.raises(ValueError, match=r"Empty matrix was given"):
        multiply_matrix_vector(matrix, vector)


def test_matrix_matrix_nxn_1():
    matrix_1 = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = matrix_matrix_multiplication(matrix_1, matrix_2)
    assert ar == [46, 4, 252, 1936, 528, 42, 42]
    assert ia == [0, 2, 5, 5, 7]
    assert ja == [0, 3, 0, 1, 3, 0, 3]


def test_matrix_matrix_nxn_2():
    matrix_1 = [[2, 0, 0, 2], [0, 44, 0, 12], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[2, 0, 0, 2], [0, 0, 0, 12], [0, 2, 0, 10], [21, 0, 0, 0]]
    ar, ia, ja = matrix_matrix_multiplication(matrix_1, matrix_2)
    assert ar == [46, 4, 252, 528, 14, 14, 42, 42]
    assert ia == [0, 2, 4, 6, 8]
    assert ja == [0, 3, 0, 3, 0, 3, 0, 3]


def test_matrix_matrix_nxn_3():
    matrix_1 = [[2, 0, 0, 2], [0, 44, 0, 12], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = matrix_matrix_multiplication(matrix_1, matrix_2)
    assert ar == []
    assert ia == [0, 0, 0, 0, 0]
    assert ja == []


def test_matrix_matrix_mxn():
    matrix_1 = [[2, 0, 0, 2], [0, 44, 0, 12], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[2, 0, 0], [0, 0, 12], [0, 2, 10], [1, 6, 0]]
    ar, ia, ja = matrix_matrix_multiplication(matrix_1, matrix_2)
    assert ar == [6, 12, 12, 72, 528, 14, 42]
    assert ia == [0, 2, 5, 6, 7]
    assert ja == [0, 1, 0, 1, 2, 0, 0]


def test_matrix_matrix_mxn_1():
    matrix_1 = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    matrix_2 = [[2, 0, 0], [0, 0, 12], [0, 2, 10], [1, 6, 0]]
    ar, ia, ja = matrix_matrix_multiplication(matrix_1, matrix_2)
    assert ar == []
    assert ia == [0, 0, 0, 0, 0]
    assert ja == []


def test_matrix_matrix_empty_matrix_1():
    matrix_1 = []
    matrix_2 = [[2, 0, 0], [0, 0, 12], [0, 2, 10], [1, 6, 0]]
    with pytest.raises(ValueError, match=r"First given matrix is empty"):
        matrix_matrix_multiplication(matrix_1, matrix_2)


def test_matrix_matrix_empty_matrix_2():
    matrix_1 = [[2, 0, 0], [0, 0, 12], [0, 2, 10], [1, 6, 0]]
    matrix_2 = []
    with pytest.raises(ValueError, match=r"Second given matrix is empty"):
        matrix_matrix_multiplication(matrix_1, matrix_2)


def test_matrix_matrix_wrong_format_1():
    matrix_1 = [[2, 0, 0, 2], [0, 2], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[2, 0, 0, 2], [0, 0, 0, 12], [0, 2, 0, 10], [21, 0, 0, 0]]
    with pytest.raises(ValueError, match=r"All matrix_1's rows must have equal length"):
        matrix_matrix_multiplication(matrix_1, matrix_2)


def test_matrix_matrix_wrong_format_2():
    matrix_1 = [[2, 0, 0, 2], [0, 2, 2, 0], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[2, 0, 0, 2], [0, 0, 0, 12], [10], [21, 0, 0, 0]]
    with pytest.raises(ValueError, match=r"All matrix_2's rows must have equal length"):
        matrix_matrix_multiplication(matrix_1, matrix_2)


def test_matrix_matrix_wrong_format_3():
    matrix_1 = [[2, 0, 0, 2], [0, 2, 2, 0], [7, 0, 0, 0], [21, 0, 0, 0]]
    matrix_2 = [[0, 0, 0, 12], [10, 0, 2, 2], [21, 0, 0, 0]]
    with pytest.raises(ValueError, match=r"Wrong inputs. Matrix_1 must be mxn and matrix_2 nxk."):
        matrix_matrix_multiplication(matrix_1, matrix_2)
