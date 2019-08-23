""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import multiprocessing as mp
import sys
from functools import singledispatch

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from compress.csr_coo import csr
from compress.diagonal_csc import csc

try:
    from multiplication_algorithm import *
except ImportError:
    from .multiplication_algorithm import *


@singledispatch
def inner_product(vector_1: list, vector_2: list):
    """
    :param vector_1: list
    :param vector_2: list
    :return: the result of inner product of two vectors-lists

    Input must be vector nx1, vector nx1.
    """
    if len(vector_1) == 0:
        raise ValueError("Empty vector_1 was given")

    if vector_1 == vector_2 and all(len(value) == 1 for value in vector_1):
        ar, ia, ja = csr(vector_1)
        br, ib, jb = ar, ia, ja
        return inner_algorithm(ar, ia, br, ib)
    else:
        if len(vector_2) == 0:
            raise ValueError("Empty vector_2 was given")

        if len(vector_1) == len(vector_2) and all(len(value) == 1 for value in vector_1) and \
                all(len(value) == 1 for value in vector_2):
            ar, ia, ja = csr(vector_1)
            br, ib, jb = csr(vector_2)

            return inner_algorithm(ar, ia, br, ib)
        else:
            raise ValueError('Both vectors must be nx1 size.')


@inner_product.register
def __inner_product(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of inner product of two vectors-lists

    Input must be vector nx1, vector nx1.
    """
    vector_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(vector_1) == 0:
        raise ValueError("Empty vector_1 was given")

    if file_name_2 == file_name_1:
        if all(len(value) == 1 for value in vector_1):
            ar, ia, ja = csr(file_name_1, processes_number, file_path)
            br, ib, jb = ar, ia, ja
            return inner_algorithm(ar, ia, br, ib)
        else:
            raise ValueError('Both vectors must be nx1 size.')
    else:
        vector_2 = read_matrix_parallel(file_name_2, processes_number, file_path)
        if len(vector_2) == 0:
            raise ValueError("Empty vector_2 was given")

        if len(vector_1) == len(vector_2) and all(len(value) == 1 for value in vector_1) and \
                all(len(value) == 1 for value in vector_2):
            ar, ia, ja = csr(vector_1)
            br, ib, jb = csr(vector_2)

            return inner_algorithm(ar, ia, br, ib)
        else:
            raise ValueError('Both vectors must be nx1 size.')


@inner_product.register
def __inner_product(vector_size_row_1: int, vector_size_col_1: int, vector_size_row_2: int,
                    vector_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                    processes_number=mp.cpu_count(), file_path='../'):
    """
    :param vector_size_row_1: int
    :param vector_size_col_1: int
    :param vector_size_row_2: int
    :param vector_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: the result of inner product of two vectors-lists

     Input must be vector nx1, vector nx1.
    """
    if vector_size_row_1 == 0:
        raise ValueError("Vector_size_row_1 cannot be zero")

    if vector_size_col_1 == 0:
        raise ValueError("Vector_size_col_1 cannot be zero")

    if vector_size_row_1 == vector_size_row_2 and vector_size_col_1 == vector_size_col_2 and file_id_1 == file_id_2:
        if vector_size_col_1 != 1:
            raise ValueError("Vector_size_col_1 and vector_size_col_2 must be equal to 1")

        ar, ia, ja = csr(vector_size_row_1, vector_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = ar, ia, ja
        return inner_algorithm(ar, ia, br, ib)
    elif vector_size_row_1 == vector_size_row_2:
        if vector_size_col_1 != 1:
            raise ValueError("Vector_size_col_1 must be equal to 1")
        if vector_size_col_2 != 1:
            raise ValueError("Vector_size_col_2 must be equal to 1")

        ar, ia, ja = csr(vector_size_row_1, vector_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csr(vector_size_row_2, vector_size_col_2, density, file_id_2, processes_number, file_path)
        return inner_algorithm(ar, ia, br, ib)
    else:
        raise ValueError('Both vectors must be nx1 size.')


@singledispatch
def outer_product(vector_1: list, vector_2: list):
    """
    :param vector_1: list
    :param vector_2: list
    :return: three list cr ic, jc. It is the result-matrix in csr format

    Input must be: vector 1xn, vector 1xn
    """
    if len(vector_1) == 0:
        raise ValueError("Empty vector_1 was given")

    if vector_1 == vector_2 and len(vector_1) == 1:
        ar, ia, ja = csc(vector_1)
        br, ib, jb = csr(vector_2)
        return outer_algorithm(ar, ja, br, jb)
    elif vector_1 != vector_2 and len(vector_1) == 1 and len(vector_2) == 1 and len(vector_1[0]) == len(vector_2[0]):
        ar, ia, ja = csc(vector_1)
        br, ib, jb = csr(vector_2)
        return outer_algorithm(ar, ja, br, jb)
    else:
        raise ValueError('Both vectors must be 1xn size.')


@outer_product.register
def __outer_product(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: three list cr ic, jc. It is the result-matrix in csr format

    Input must be: vector 1xn, vector 1xn
    """
    vector_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    if len(vector_1) == 0:
        raise ValueError("Empty vector_1 was given")

    if file_name_2 == file_name_1:
        if len(vector_1) != 1:
            raise ValueError('Both vectors must be 1xn size.')

        ar, ia, ja = csc(vector_1)
        br, ib, jb = csr(vector_1)
        return outer_algorithm(ar, ja, br, jb)

    else:
        vector_2 = read_matrix_parallel(file_name_2, processes_number, file_path)
        if len(vector_1) == 1 and len(vector_2) == 1 and len(vector_1[0]) == len(vector_2[0]):
            ar, ia, ja = csc(vector_1)
            br, ib, jb = csr(vector_2)
            return outer_algorithm(ar, ja, br, jb)
        else:
            raise ValueError('Both vectors must be 1xn size.')


@outer_product.register
def __outer_product(vector_size_row_1: int, vector_size_col_1: int, vector_size_row_2: int,
                    vector_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                    processes_number=mp.cpu_count(), file_path='../'):
    """
    :param vector_size_row_1: int
    :param vector_size_col_1: int
    :param vector_size_row_2: int
    :param vector_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: three list cr ic, jc. It is the result-matrix in csr format

    Input must be: vector 1xn, vector 1xn
    """
    if vector_size_row_1 == 0:
        raise ValueError("Vector_size_row_1 cannot be zero")

    if vector_size_col_1 == 0:
        raise ValueError("Vector_size_col_1 cannot be zero")

    if vector_size_row_1 != 1:
        raise ValueError("Vector_size_row_1 must be equal to 1")

    if vector_size_row_2 != 1:
        raise ValueError("Vector_size_row_2 must be equal to 1")

    if vector_size_col_1 == vector_size_col_2:
        ar, ia, ja = csc(vector_size_row_1, vector_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csr(vector_size_row_2, vector_size_col_2, density, file_id_2, processes_number, file_path)
        return outer_algorithm(ar, ja, br, jb)
    else:
        raise ValueError('Both vectors must be 1xn size.')


@singledispatch
def multiply_matrix_vector(matrix: list, vector: list):
    """
    :param matrix: list
    :param vector: list
    :return: three lists cr, ic, jc, It is the result in csc format stored

    Input must be: matrix mxn or nxn and vector nx1
    """
    if len(matrix) == 0:
        raise ValueError("Empty matrix was given")

    if len(vector) == 0:
        raise ValueError("Empty vector was given")

    matrix_1_col_size = len(matrix[0])
    if matrix_1_col_size == len(vector):
        if not all(len(row) == matrix_1_col_size for row in matrix):
            raise ValueError("All matrix's rows must have equal length")

        if not all(len(row) == 1 for row in vector):
            raise ValueError("All vectors's rows must contain only one element")

        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


@multiply_matrix_vector.register
def __multiply_matrix_vector(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number:  int
    :param file_path: string
    :return: three lists cr, ic, jc, It is the result in csc format stored

    Input must be: matrix mxn or nxn and vector nx1
    """
    matrix = read_matrix_parallel(file_name_1, processes_number, file_path)
    vector = read_matrix_parallel(file_name_2, processes_number, file_path)
    matrix_1_col_size = len(matrix[0])

    if len(matrix) == 0:
        raise ValueError("Empty matrix was given")

    if len(vector) == 0:
        raise ValueError("Empty vector was given")

    if matrix_1_col_size == len(vector):
        if not all(len(row) == matrix_1_col_size for row in matrix):
            raise ValueError("All matrix's rows must have equal length")

        if not all(len(row) == 1 for row in vector):
            raise ValueError("All vectors's rows must contain only one element")

        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


@multiply_matrix_vector.register
def __multiply_matrix_vector(matrix_size_row: int, matrix_size_col: int, vector_size_row: int,
                             vector_size_col: int, density: float, file_id_1: int, file_id_2: int,
                             processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param vector_size_row: int
    :param vector_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: three lists cr, ic, jc, It is the result in csc format stored

    Input must be: matrix mxn or nxn and vector nx1
    """
    if matrix_size_row == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if vector_size_row == 0:
        raise ValueError("Matrix_size_row_2 cannot be zero")

    if matrix_size_col == 0:
        raise ValueError("matrix_size_col_1 cannot be zero")

    if vector_size_col == 0:
        raise ValueError("matrix_size_col_2 cannot be zero")

    if matrix_size_col == vector_size_row and vector_size_col == 1:
        ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1, processes_number, file_path)
        xr, ix, jx = csc(vector_size_row, vector_size_col, density, file_id_2, processes_number, file_path)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


@singledispatch
def multiply_vector_matrix(matrix: list, vector: list):
    """
    :param matrix: list
    :param vector: list
    :return: three lists cr, ic, jc. It is the result in csr format stored

    Input must be: matrix nxm or nxn and vector 1xn
    """
    if len(matrix) == 0:
        raise ValueError("Empty matrix was given")

    if len(vector) == 0:
        raise ValueError("Empty vector was given")

    matrix_col_size = len(matrix[0])
    vector_col_size = len(vector[0])
    if len(vector) == 1 and len(matrix) == vector_col_size:
        if not all(len(row) == matrix_col_size for row in matrix):
            raise ValueError("All matrix's rows must have equal length")

        ar, ia, ja = csc(matrix)
        xr, ix, jx = csr(vector)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


@multiply_vector_matrix.register
def __multiply_vector_matrix(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :return: three lists cr, ic, jc. It is the result in csr format stored

    Input must be: matrix nxm or nxn and vector 1xn
    """
    matrix = read_matrix_parallel(file_name_1, processes_number, file_path)
    vector = read_matrix_parallel(file_name_2, processes_number, file_path)
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


@multiply_vector_matrix.register
def __multiply_vector_matrix(matrix_size_row: int, matrix_size_col: int, vector_size_row: int,
                             vector_size_col: int, density: float, file_id_1: int, file_id_2: int,
                             processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param vector_size_row: int
    :param vector_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :return: three lists cr, ic, jc. It is the result in csr format stored

    Input must be: matrix nxm or nxn and vector 1xn
    """
    if matrix_size_row == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if vector_size_row == 0:
        raise ValueError("Matrix_size_row_2 cannot be zero")

    if matrix_size_col == 0:
        raise ValueError("matrix_size_col_1 cannot be zero")

    if vector_size_col == 0:
        raise ValueError("matrix_size_col_2 cannot be zero")

    if matrix_size_row == vector_size_col and vector_size_row == 1:
        ar, ia, ja = csc(matrix_size_row, matrix_size_col, density, file_id_1, processes_number, file_path)
        xr, ix, jx = csr(vector_size_row, vector_size_col, density, file_id_2, processes_number, file_path)

        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


@singledispatch
def matrix_matrix_multiplication(matrix_1: list, matrix_2: list):
    """
    :param matrix_1: list
    :param matrix_2: list
    :return: three lists cr, ic, jc. It is the result of the multiplication in csr format stored

    Input must be: matrix_1 mxn and matrix_2 nxk.
    """
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


@matrix_matrix_multiplication.register
def __matrix_matrix_multiplication(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(),
                                   file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: three lists cr, ic, jc. It is the result of the multiplication in csr format stored

     Input must be: matrix_1 mxn and matrix_2 nxk.
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)
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


@matrix_matrix_multiplication.register
def __matrix_matrix_multiplication(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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
    :return: three lists cr, ic, jc. It is the result of the multiplication in csr format stored

    Input must be: matrix_1 mxn and matrix_2 nxk.
    """
    if matrix_size_row_1 == 0:
        raise ValueError("Matrix_size_row_1 cannot be zero")

    if matrix_size_col_1 == 0:
        raise ValueError("Matrix_size_col_1 cannot be zero")

    if matrix_size_row_2 == 0:
        raise ValueError("Matrix_size_row_2 cannot be zero")

    if matrix_size_col_2 == 0:
        raise ValueError("Matrix_size_col_2 cannot be zero")

    if matrix_size_col_1 == matrix_size_row_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxk.')
