"""
    To run test_csr only execute: pytest -k csr
"""
import sys
import pytest
import os
import numpy as np
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from compress.csr_coo import csr


def test_csr_list_nxn_1():
    matrix = [[2, 0, 0, 2], [0, 44, 0, 12], [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = csr(matrix)
    assert ar == [2, 2, 44, 12, 21]
    assert ia == [0, 2, 4, 4, 5]
    assert ja == [0, 3, 1, 3, 0]


def test_csr_list_nxn_2():
    matrix = [[2, 0, 0, 2], (0, 44, 0, 12), [0, 0, 0, 0], [21, 0, 0, 0]]
    ar, ia, ja = csr(matrix)
    assert ar == [2, 2, 44, 12, 21]
    assert ia == [0, 2, 4, 4, 5]
    assert ja == [0, 3, 1, 3, 0]


def test_csr_list_1xn():
    matrix = [[5, 3, 42, 0, 0, 0, 34]]
    ar, ia, ja = csr(matrix)
    assert ar == [5, 3, 42, 34]
    assert ia == [0, 4]
    assert ja == [0, 1, 2, 6]


def test_csr_list_nx1():
    matrix = [[34], [0], [32], [0]]
    ar, ia, ja = csr(matrix)
    assert ar == [34, 32]
    assert ia == [0, 1, 1, 2, 2]
    assert ja == [0, 0]


def test_csr_zero_matrix():
    matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    ar, ia, ja = csr(matrix)
    assert ar == []
    assert ia == [0, 0, 0, 0]
    assert ja == []


def test_csr_zero_vector():
    matrix = [[0, 0, 0, 0]]
    ar, ia, ja = csr(matrix)
    assert ar == []
    assert ia == [0, 0]
    assert ja == []


def test_csr_empty_list():
    matrix = []
    with pytest.raises(ValueError, match=r"Empty matrix"):
        csr(matrix)


def test_csr_wrong_matrix_format_1():
    matrix = [[12, 12], "21"]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csr(matrix)


def test_csr_wrong_matrix_format_2():
    matrix = [[12, 12], ["21"]]
    with pytest.raises(ValueError, match=r"Every row in matrix must best list or tuple and have the same length"):
        csr(matrix)


"""
    Pytest does not support test for dispatched functions
"""
# def test_csr_file_nxn():
#     ar, ia, ja = csr('output_4_4_0.5_1.txt', file_path='')
#     assert ar == [2, 2, 44, 12, 21]
#     assert ia == [0, 2, 4, 4, 5]
#     assert ja == [0, 3, 1, 3, 0]
#
#
# def test_csr_file_parameters():
#     # give file dimension, density and it
#     ar, ia, ja = csr(4, 4, 0.5, 1, file_path='')
#     assert ar == [2, 2, 44, 12, 21]
#     assert ia == [0, 2, 4, 4, 5]
#     assert ja == [0, 3, 1, 3, 0]

