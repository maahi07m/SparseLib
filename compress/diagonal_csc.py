"""To run: python3 diagonal_csc.py <size of rows> <size of cols> <density> <file_id>"""
import sys
import numpy as np
import multiprocessing as mp
from functools import singledispatch
try:
    from diagonal_csc_algorithms import csc_algorithm, diagonal_algorithm
except ImportError:
    from .diagonal_csc_algorithms import csc_algorithm, diagonal_algorithm

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


@singledispatch
def diagonal(matrix: list):
    """
    :param matrix: list
    :return: two vectors-lists AD, LA.

    Compress a squared matrix 2-d to diagonal format using the function diagonal_algorithm.
    Each diagonal of matrix that has at least one nonzero element is stored in a column of array AD.
    LA is a one-dimensional integer array of length nd, containing the diagonal numbers k
    for the diagonals stored in each corresponding column in array AD.
    """
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        if len(matrix) != matrix_col_size:
            raise ValueError('Matrix must be nxn')
        return diagonal_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')


@diagonal.register
def _diagonal(file_name: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param processes_number: int
    :param file_path: string
    :return two vectors-lists AD, LA.

    Compress a squared matrix 2-d to diagonal format using the function diagonal_algorithm.
    Each diagonal of matrix that has at least one nonzero element is stored in a column of array AD.
    LA is a one-dimensional integer array of length nd, containing the diagonal numbers k
    for the diagonals stored in each corresponding column in array AD.
    """
    matrix = read_matrix_parallel(file_name, processes_number=processes_number, file_path=file_path)
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        if len(matrix) != matrix_col_size:
            raise ValueError('Matrix must be nxn')
        return diagonal_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')


@diagonal.register
def _diagonal(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int,
              processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param processes_number int
    :param file_path: string
    :return two vectors-lists AD, LA.

    Compress a squared matrix 2-d to diagonal format using the function diagonal_algorithm.
    Each diagonal of matrix that has at least one nonzero element is stored in a column of array AD.
    LA is a one-dimensional integer array of length nd, containing the diagonal numbers k
    for the diagonals stored in each corresponding column in array AD.
    """
    file_name = 'output_%d_%d_%s_%d.txt' % (matrix_size_row, matrix_size_col, str(density), file_id)
    matrix = read_matrix_parallel(file_name, processes_number=processes_number, file_path=file_path)
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        if len(matrix) != matrix_col_size:
            raise ValueError('Matrix must be nxn')
        return diagonal_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')


@singledispatch
def csc(matrix: list):
    """
    :param matrix: list of lists
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to csc format using the function csc_algorithm.
    AR contains the non zero values, IA contains the corresponding row numbers of each non zero
    element in matrix and JA contains the relative starting position of each column
    of matrix in array AR.
    """
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        return csc_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')


@csc.register
def _csc(file_name: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param processes_number: int
    :param file_path: string
    :return: three vectors-lists AR, IA, JA

    Compress a matrix 1-d or 2-d to csc format using the function csc_algorithm.
    AR contains the non zero values, IA contains the corresponding row numbers of each non zero
    element in matrix and JA contains the relative starting position of each column
    of matrix in array AR.
    """
    matrix = read_matrix_parallel(file_name, processes_number=processes_number, file_path=file_path)
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        return csc_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')


@csc.register
def _csc(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int, processes_number=mp.cpu_count(),
         file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param processes_number: int
    :param file_path: string
    :return: three vectors-lists AR, IA, JA

    Compress a matrix 1-d or 2-d to csc format using the function csc_algorithm.
    AR contains the non zero values, IA contains the corresponding row numbers of each non zero
    element in matrix and JA contains the relative starting position of each column
    of matrix in array AR.
    """
    file_name = 'output_%d_%d_%s_%d.txt' % (matrix_size_row, matrix_size_col, str(density), file_id)
    matrix = read_matrix_parallel(file_name, processes_number=processes_number, file_path=file_path)
    if type(matrix) != list and type(matrix) != tuple:
        raise TypeError("Expected list or tuple. Got %s", type(matrix))
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all((type(row) == list or type(row) == tuple) and len(row) == matrix_col_size for row in matrix):
            raise ValueError("Every row in matrix must best list or tuple and have the same length")
        return csc_algorithm(np.array(matrix))
    else:
        raise ValueError('Empty matrix')
