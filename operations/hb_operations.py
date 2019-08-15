"""This script calculate the addition and subtraction of two matrices compressed in csr or csc format and return the
    results.
"""
import sys

sys.path.append('../')
from read_file.read_hb_format import read_file
from compress.csr_coo import csr
from compress.diagonal_csc import csc

try:
    from addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc
except ImportError:
    from .addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc

try:
    from multiplication_algorithm import matrix_vector_algorithm, vector_matrix_algorithm, matrix_matrix_algorithm

except ImportError:
    from .multiplication_algorithm import matrix_vector_algorithm, vector_matrix_algorithm, matrix_matrix_algorithm


def csr_addition_matrices_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)

    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


def csr_subtraction_matrices_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)

    return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


def csc_addition_matrices_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    ar, ia, ja = csc(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(matrix_2)

    return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


def csc_subtraction_matrices_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    ar, ia, ja = csc(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(matrix_2)

    return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


def multiply_matrix_vector_hb(file_name_1: str, file_name_2: str):
    matrix = read_file(file_name=file_name_1, return_list=True)
    vector = read_file(file_name=file_name_2, return_list=True)
    matrix_1_col_size = len(matrix[0])
    if all(len(row) == matrix_1_col_size for row in matrix) and all(len(row) == 1 for row in vector) and \
       matrix_1_col_size == len(vector):

        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs dimensions. Matrix must be mxn or nxn and vector nx1.')


def multiply_vector_matrix_hb(file_name_1: str, file_name_2: str):
    matrix = read_file(file_name=file_name_1, return_list=True)
    vector = read_file(file_name=file_name_2, return_list=True)
    matrix_col_size = len(matrix[0])  # m
    vector_col_size = len(vector[0])  # n

    if len(vector) == 1 and len(matrix) == vector_col_size and \
            all(len(row) == matrix_col_size for row in matrix):

        ar, ia, ja = csc(matrix)
        xr, ix, jx = csr(vector)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


def matrix_matrix_multiplication_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_row_size = len(matrix_2)

    if matrix_1_col_size == matrix_2_row_size:
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)

        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxm.')


if __name__ == '__main__':
    cr, ic, jc = matrix_matrix_multiplication_hb('bcsstk01.rsa', 'bcsstk01.rsa')
    print(len(cr))
    print(len(ic))
    print(len(jc))
