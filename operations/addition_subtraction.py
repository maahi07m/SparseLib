"""This script calculate the addition and subtraction of two matrices compressed in csr or csc format and return the
    results.
"""
import multiprocessing as mp
import sys
from functools import singledispatch

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from compress.csr_coo import csr
from compress.diagonal_csc import csc
try:
    from addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc
except ImportError:
    from .addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc


@singledispatch
def csr_addition_matrices(matrix_1: list, matrix_2: list):
    """
    :param matrix_1: list of lists
    :param matrix_2: list of lists
    :return: the result of the addition of two matrices stored in csr format
    """
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if matrix_1 == matrix_2:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices.register
def _csr_addition_matrices(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of the addition of two matrices stored in csr format
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if file_name_2 == file_name_1:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)

        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices.register
def _csr_addition_matrices(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                           matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                           processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: the result of the addition of two matrices stored in csr format
    """
    if matrix_size_row_1 == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if matrix_size_col_1 == 0:
        raise ValueError("Matrix_size_col_1 cannot be zero")

    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and file_id_1 == file_id_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        if matrix_size_row_2 == 0:
            raise ValueError("Matrix_size_row_2 cannot be zero")

        if matrix_size_col_2 == 0:
            raise ValueError("Matrix_size_col_2 cannot be zero")

        if matrix_size_row_1 == matrix_size_row_2:
            raise ValueError('Both matrices must have same number of rows.')

        if matrix_size_col_1 == matrix_size_col_2:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)
        return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@singledispatch
def csr_subtraction_matrices(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   :return: the result of the subtraction of two matrices stored in csr format
   """
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if matrix_1 == matrix_2:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_subtraction_matrices.register
def _csr_subtraction_matrices(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the subtraction of two matrices stored in csr format
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if file_name_2 == file_name_1:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)

        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_subtraction_matrices.register
def _csr_subtraction_matrices(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                              matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                              processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: the result of the subtraction of two matrices stored in csr format
    """
    if matrix_size_row_1 == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if matrix_size_col_1 == 0:
        raise ValueError("Matrix_size_col_1 cannot be zero")

    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and file_id_1 == file_id_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)
    else:
        if matrix_size_row_2 == 0:
            raise ValueError("Matrix_size_row_2 cannot be zero")

        if matrix_size_col_2 == 0:
            raise ValueError("matrix_size_col_2 cannot be zero")

        if matrix_size_row_1 == matrix_size_row_2:
            raise ValueError('Both matrices must have same number of rows.')

        if matrix_size_col_1 == matrix_size_col_2:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)
        return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@singledispatch
def csc_addition_matrices(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   :return: the result of the addition of two matrices stored in csc format
   """
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if matrix_1 == matrix_2:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")
        ar, ia, ja = csc(matrix_1)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = csc(matrix_2)
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_addition_matrices.register
def _csc_addition_matrices(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of the addition of two matrices stored in csc format
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if file_name_2 == file_name_1:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)

        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = csc(matrix_2)
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_addition_matrices.register
def _csc_addition_matrices(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                           matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                           processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :return: the result of the addition of two matrices stored in csc format
    """
    if matrix_size_row_1 == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if matrix_size_col_1 == 0:
        raise ValueError("Matrix_size_col_1 cannot be zero")

    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and file_id_1 == file_id_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = ar, ia, ja
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        if matrix_size_row_2 == 0:
            raise ValueError("Matrix_size_row_2 cannot be zero")

        if matrix_size_col_2 == 0:
            raise ValueError("Matrix_size_col_2 cannot be zero")

        if matrix_size_row_1 == matrix_size_row_2:
            raise ValueError('Both matrices must have same number of rows.')

        if matrix_size_col_1 == matrix_size_col_2:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)
        return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@singledispatch
def csc_subtraction_matrices(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   :return: the result of the subtraction of tow matrices stored in csc format
   """
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if matrix_1 == matrix_2:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = csc(matrix_2)
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_subtraction_matrices.register
def _csc_subtraction_matrices(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of the subtraction of tow matrices stored in csc format
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if file_name_2 == file_name_1:
        matrix_1_col_size = len(matrix_1[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrices' rows must have equal length")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)

        if len(matrix_2) == 0:
            raise ValueError("Second given matrix is empty")

        if len(matrix_1) != len(matrix_2):
            raise ValueError('Both matrices must have same number of rows.')

        matrix_1_col_size = len(matrix_1[0])
        matrix_2_col_size = len(matrix_2[0])
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        if matrix_1_col_size != matrix_2_col_size:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_1)
        br, ib, jb = csc(matrix_2)
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_subtraction_matrices.register
def _csc_subtraction_matrices(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                              matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                              processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :return: the result of the subtraction of tow matrices stored in csc format
    """
    if matrix_size_row_1 == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if matrix_size_col_1 == 0:
        raise ValueError("Matrix_size_col_1 cannot be zero")

    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and file_id_1 == file_id_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = ar, ia, ja
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)
    else:
        if matrix_size_row_2 == 0:
            raise ValueError("Matrix_size_row_2 cannot be zero")

        if matrix_size_col_2 == 0:
            raise ValueError("Matrix_size_col_2 cannot be zero")

        if matrix_size_row_1 == matrix_size_row_2:
            raise ValueError('Both matrices must have same number of rows.')

        if matrix_size_col_1 == matrix_size_col_2:
            raise ValueError("Both matrices must have same number of columns")

        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)
        return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)
