"""This script calculates the addition and subtraction of two matrices compressed in csr or csc format and returns the
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
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the addition of two Harwell-Boeing matrices in csr format

    It takes as input two files in Harwell-Boeing format and returns the result of their addition in csr format
    """
    matrix_1 = read_file(file_name=file_name_1)
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
        matrix_2 = read_file(file_name=file_name_2)

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


def csr_subtraction_matrices_hb(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the subtraction of two Harwell-Boeing matrices in csr format

    It takes as input two files in Harwell-Boeing format and returns the result of their subtraction in csr format
    """
    matrix_1 = read_file(file_name=file_name_1)
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
        matrix_2 = read_file(file_name=file_name_2)

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


def csc_addition_matrices_hb(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the addition of two Harwell-Boeing matrices in csc format

    It takes as input two files in Harwell-Boeing format and returns the result of their addition in csc format
    """
    matrix_1 = read_file(file_name=file_name_2)
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
        matrix_2 = read_file(file_name=file_name_2)

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


def csc_subtraction_matrices_hb(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the subtraction of two Harwell-Boeing matrices in csc format

    It takes as input two files in Harwell-Boeing format and returns the result of their subtraction in csc format
    """
    matrix_1 = read_file(file_name=file_name_1)
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
        matrix_2 = read_file(file_name=file_name_2)

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


def multiply_matrix_vector_hb(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the multiplication of a Harwell-Boeing matrix and a Harwell-Boeing vector in csc format

    It takes as input two files in Harwell-Boeing format and returns the result of their multiplication in csc format.
    Matrix must be either mxn or nxn and vector must be nx1
    """
    matrix = read_file(file_name=file_name_1)
    vector = read_file(file_name=file_name_2)
    matrix_col_size = len(matrix[0])

    if len(matrix) == 0:
        raise ValueError("Empty matrix was given")

    if len(vector) == 0:
        raise ValueError("Empty vector was given")

    if matrix_col_size == len(vector):
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All matrix's rows must have equal length")

        if not all(len(row) == 1 for row in vector):
            raise ValueError("All vectors's rows must contain only one element")

        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


def multiply_vector_matrix_hb(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the multiplication of a Harwell-Boeing vector and a Harwell-Boeing matrix in csr format

    It takes as input two files in Harwell-Boeing format and returns the result of their multiplication in csr format.
    Vector must be nx1 and matrix must be either nxm or nxn
    """
    matrix = read_file(file_name=file_name_1)
    vector = read_file(file_name=file_name_2)
    matrix_col_size = len(matrix[0])  # m
    vector_col_size = len(vector[0])  # n

    if len(matrix) == 0:
        raise ValueError("Empty matrix was given")

    if len(vector) == 0:
        raise ValueError("Empty vector was given")

    # if x has only one line and matrix's rows are equal to vector's columns and all lines of matrix are equal to
    # m length
    if len(vector) == 1 and len(matrix) == vector_col_size:
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All matrix's rows must have equal length")

        ar, ia, ja = csc(matrix)
        xr, ix, jx = csr(vector)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


def matrix_matrix_multiplication_hb(file_name_1: str, file_name_2: str):
    """D
    :param file_name_1: string
    :param file_name_2: string
    :return: the result of the multiplication of a Harwell-Boeing matrices in csr format

    It takes as input two files in Harwell-Boeing format and returns the result of their multiplication in csr format.
    The first matrix must be mxn or nxn and the second one must nxk
    """
    matrix_1 = read_file(file_name=file_name_1)
    matrix_2 = read_file(file_name=file_name_2)
    if len(matrix_1) == 0:
        raise ValueError("First given matrix is empty")

    if len(matrix_2) == 0:
        raise ValueError("Second given matrix is empty")

    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    matrix_2_row_size = len(matrix_2)

    if matrix_1_col_size == matrix_2_row_size:
        if not all(len(row) == matrix_1_col_size for row in matrix_1):
            raise ValueError("All matrix_1's rows must have equal length")

        if not all(len(row) == matrix_2_col_size for row in matrix_2):
            raise ValueError("All matrix_2's rows must have equal length")

        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)
        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxk.')
