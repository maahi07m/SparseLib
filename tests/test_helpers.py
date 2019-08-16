import sys
import os
import numpy as np
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from helpers.generator import generate_sparse_matrix


def test_generator_call():
    matrix = generate_sparse_matrix(4, 4, 0.5,)
    assert type(matrix) == np.ndarray


def test_generator_nxn():
    matrix = generate_sparse_matrix(4, 4, 0.5)
    matrix_col_size = len(matrix[0])
    assert type(matrix) == np.ndarray
    assert all(type(row) == type(matrix) == np.ndarray for row in matrix)
    assert all(len(row) == matrix_col_size for row in matrix)


def test_generator_1xn():
    matrix = generate_sparse_matrix(1, 4, 0.5)
    assert type(matrix) == np.ndarray
    assert len(matrix) == 1
    assert type(matrix[0]) == np.ndarray
    assert len(matrix[0]) == 4


def test_generator_write_file():
    generate_sparse_matrix(1, 5, 0.5, 1, return_list=False, file_path='')
    assert os.path.exists('data_files/output_1_5_0.5_1.txt') == 1


def test_generator_file_content():
    generate_sparse_matrix(1, 5, 0.5, 1, return_list=False, file_path='')
    matrix = read_matrix_parallel('output_1_5_0.5_1.txt', file_path='')
    assert type(matrix) == tuple
    assert len(matrix) == 1
    assert type(matrix[0]) == tuple
    assert len(matrix[0]) == 5
