import sys
import multiprocessing as mp
from functools import singledispatch
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
try:
    from csr_coo_algorithm import csr_algorithm, coo_algorithm
except ImportError:
    from .csr_coo_algorithm import csr_algorithm, coo_algorithm


@singledispatch
def csr(matrix: list):
    """
    :param matrix: list of lists
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to csr format using the function csr_algorithm.
    AR contains the non zero values, IA contains the relative starting position of each row
    of matrix in array AR and JA contains the corresponding column numbers of each non zero
    element in matrix.
    """
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All the lines have not the same number of elements")
        return csr_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')


@csr.register
def _csr(file_name: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param processes_number: int
    :param file_path: string
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to csr format using the function csr_algorithm.
    AR contains the non zero values, IA contains the relative starting position of each row
    of matrix in array AR and JA contains the corresponding column numbers of each non zero
    element in matrix.
    """
    matrix = read_matrix_parallel(file_name, number_process=processes_number, file_path=file_path)
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All the lines have not the same number of elements")
        return csr_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')


@csr.register
def _csr(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int,
         number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_id: int
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to csr format using the function csr_algorithm.
    AR contains the non zero values, IA contains the relative starting position of each row
    of matrix in array AR and JA contains the corresponding column numbers of each non zero
    element in matrix.
    """
    file_name = 'output_%d_%d_%s_%d.txt' % (matrix_size_row, matrix_size_col, str(density), file_id)
    matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density,
                                  number_process=number_process, file_path=file_path)
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All the lines have not the same number of elements")
        return csr_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')


@singledispatch
def coo(matrix: list):
    """
    :param matrix: list of lists
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to coo format using the function coo_algorithm.
    AR contains the non zero values, IA contains the corresponding row number of each non
    zero element in matrix and JA contains the corresponding column number of each non
    zero element in matrix.
    """
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ReferenceError("All the lines have not the same number of elements")
        return coo_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')


@coo.register
def _coo(file_name: str, number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param number_process: int
    :param file_path: string
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to coo format using the function coo_algorithm.
    AR contains the non zero values, IA contains the corresponding row number of each non
    zero element in matrix and JA contains the corresponding column number of each non
    zero element in matrix.
    """
    matrix = read_matrix_parallel(file_name, number_process=number_process, file_path=file_path)
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ReferenceError("All the lines have not the same number of elements")
        return coo_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')


@coo.register
def _coo(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int,
         number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_id: int
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to coo format using the function coo_algorithm.
    AR contains the non zero values, IA contains the corresponding row number of each non
    zero element in matrix and JA contains the corresponding column number of each non
    zero element in matrix.
    """
    file_name = 'output_%d_%d_%s_%d.txt' % (matrix_size_row, matrix_size_col, str(density), file_id)
    matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density,
                                  number_process=number_process, file_path=file_path)
    if len(matrix) != 0:
        matrix_col_size = len(matrix[0])
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ReferenceError("All the lines have not the same number of elements")
        return coo_algorithm(matrix)
    else:
        raise ValueError('Empty matrix')
