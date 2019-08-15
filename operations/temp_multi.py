""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import sys
import multiprocessing as mp
from functools import singledispatch

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from compress.csr_coo import csr
from compress.diagonal_csc import csc

try:
    from multiplication_algorithm import *
except ImportError:
    from .multiplication_algorithm import *


# TODO: correct warning messages
# TODO: test whole the project
# TODO: import as library in another project (module package set up)
# TODO: tests, find an easier project to check as example not numpy
# TODO: correct any warnings and wrongs by accident that may exists


@singledispatch
def inner_product(vector_1: list, vector_2: list):
    """
    :param vector_1: list
    :param vector_2: list
    :return: the result of inner product of two vectors-lists

    Input must be vector nx1, vector nx1.
    """
    if len(vector_1) == len(vector_2) and all(len(value) == 1 for value in vector_1) and \
            all(len(value) == 1 for value in vector_2):
        ar, ia, ja = csr(vector_1)
        br, ib, jb = csr(vector_2)

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise ValueError('Both vectors must be nx1 size.')


@inner_product.register
def _inner_product(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of inner product of two vectors-lists

    Input must be vector nx1, vector nx1.
    """
    ar, ia, ja = csr(file_name_1, processes_number, file_path)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2, processes_number, file_path)

    if len(ia) == len(ib) and all(value == 0 for value in ja) and all(value == 0 for value in jb):
        return inner_algorithm(ar, ia, br, ib)
    else:
        raise ValueError('Both vectors must be nx1 size.')


@inner_product.register
def _inner_product(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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
    :return: the result of inner product of two vectors-lists

     Input must be vector nx1, vector nx1.
    """
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and matrix_size_col_1 == 1:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        if file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

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
    if len(vector_1) == len(vector_2) and len(vector_1) == 1 and len(vector_1[0]) == len(vector_2[0]):
        ar, ia, ja = csc(vector_1)
        if vector_1 == vector_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(vector_2)

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise ValueError('Both vectors must be 1xn size.')


@outer_product.register
def _outer_product(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: three list cr ic, jc. It is the result-matrix in csr format

    Input must be: vector 1xn, vector 1xn
    """
    ar, ia, ja = csc(file_name_1, processes_number, file_path)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2, processes_number, file_path)

    if len(ja) == len(jb) and all(value == 0 for value in ia) and all(value == 0 for value in ib):
        return outer_algorithm(ar, ja, br, jb)
    else:
        raise ValueError('Both vectors must be 1xn size.')


@outer_product.register
def _outer_product(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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
    :return: three list cr ic, jc. It is the result-matrix in csr format

    Input must be: vector 1xn, vector 1xn
    """
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_row_1 == 1 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        if file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

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
    matrix_1_col_size = len(matrix[0])
    if all(len(row) == matrix_1_col_size for row in matrix) and all(len(row) == 1 for row in vector) and \
            matrix_1_col_size == len(vector):
        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


@multiply_matrix_vector.register
def _multiply_matrix_vector(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
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

    if all(len(row) == matrix_1_col_size for row in matrix) and all(len(row) == 1 for row in vector) and \
            matrix_1_col_size == len(vector):
        ar, ia, ja = csr(matrix)
        xr, ix, jx = csc(vector)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector nx1.')


@multiply_matrix_vector.register
def _multiply_matrix_vector(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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
    :return: three lists cr, ic, jc, It is the result in csc format stored

    Input must be: matrix mxn or nxn and vector nx1
    """
    if matrix_size_col_1 == matrix_size_row_2 and matrix_size_col_2 == 1:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        xr, ix, jx = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

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
    matrix_1_col_size = len(matrix[0])
    matrix_2_col_size = len(vector[0])
    if len(vector) == 1 and len(matrix) == matrix_2_col_size and \
            all(len(row) == matrix_1_col_size for row in matrix):

        ar, ia, ja = csc(matrix)
        xr, ix, jx = csr(vector)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


@multiply_vector_matrix.register
def _multiply_vector_matrix(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
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

    # if x has only one line and matrix's rows are equal to vector's columns and all lines of matrix are equal to
    # m length
    if len(vector) == 1 and len(matrix) == vector_col_size and \
            all(len(row) == matrix_col_size for row in matrix):

        ar, ia, ja = csc(matrix)
        xr, ix, jx = csr(vector)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


@multiply_vector_matrix.register
def _multiply_vector_matrix(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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
    :return: three lists cr, ic, jc. It is the result in csr format stored

    Input must be: matrix nxm or nxn and vector 1xn
    """
    if matrix_size_row_1 == matrix_size_col_2 and matrix_size_row_2 == 1:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        xr, ix, jx = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise ValueError('Wrong inputs. Matrix must be mxn or nxn and vector 1xn.')


@singledispatch
def matrix_matrix_multiplication(matrix_1: list, matrix_2: list):
    """
    :param matrix_1: list
    :param matrix_2: list
    :return: three lists cr, ic, jc. It is the result of the multiplication in csr format stored

    Input must be: matrix_1 mxn and matrix_2 nxm.
    """
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    matrix_2_row_size = len(matrix_2)

    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(
            len(row) == matrix_2_col_size for row in matrix_2) and matrix_1_col_size == matrix_2_row_size:
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)
        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxm.')


@matrix_matrix_multiplication.register
def _matrix_matrix_multiplication(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: three lists cr, ic, jc. It is the result of the multiplication in csr format stored

     Input must be: matrix_1 mxn and matrix_2 nxm.
    """
    matrix_1 = read_matrix_parallel(file_name_1, processes_number, file_path)
    matrix_2 = read_matrix_parallel(file_name_2, processes_number, file_path)
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    matrix_2_row_size = len(matrix_2)

    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(
            len(row) == matrix_2_col_size for row in matrix_2) and matrix_1_col_size == matrix_2_row_size:
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)
        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxm.')


@matrix_matrix_multiplication.register
def _matrix_matrix_multiplication(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
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

    Input must be: matrix_1 mxn and matrix_2 nxm.
    """
    if matrix_size_col_1 == matrix_size_row_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)

        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise ValueError('Wrong inputs. Matrix_1 must be mxn and matrix_2 nxm.')


# def main():
#     file_name = sys.argv[1]
#     # file_name = "bcsstk08.rsa"
#     # file_name = 'output_10_10_0.5_1.txt'
#     try:
#         matrix = read_file(file_name=file_name, return_list=True)
#         # matrix = read_matrix_parallel(file_name=file_name)
#         for _ in range(10):
#             for density in [0.005, 0.01, 0.02]:
#
#                 ar, ia, ja, vector = multiply_matrix_vector(True, matrix, file_name, density)
#                 vector = [item for item in vector]
#                 npr, inp, jnp = numpy_matrix_vector(matrix, vector, file_name, density)
#                 validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'matrix_vector')
#
#                 ar, ia, ja, vector = multiply_vector_matrix(True, matrix, file_name, density)
#                 vector = [item for item in vector]
#                 npr, inp, jnp = numpy_vector_matrix(matrix, vector, file_name, density)
#                 validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'vector_matrix')
#
#                 ar, ia, ja = matrix_matrix_multiplication(True, matrix, file_name)
#                 if ar == [] and ia == [] and ja == []:
#                     continue
#                 npr, inp, jnp = numpy_matrix_matrix(matrix, file_name, density)
#                 # print(ar)
#                 # print(ia)
#                 # print(ja)
#                 # print("-"*100)
#                 # print(npr)
#                 # print(inp)
#                 # print(jnp)
#                 validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'matrix_matrix')
#
#     except TypeError as err:
#         print("TypeError error: {0}".format(err))
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
#             f.write('Wrong_file_format\t%s\n' % sys.argv[1])
#
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
#             f.write('Wrong_file_format\t%s\n' % sys.argv[1])
#
#     except NotImplementedError:
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
#             f.write('No_supported_format!\t%s\n' % sys.argv[1])
#
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
#             f.write('No_supported_format\t%s\n' % sys.argv[1])
#
#     except ValueError as err:
#         print("ValueError error: {0}".format(err))
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
#             f.write('ValueError_sto\t%s\n' % sys.argv[1])
#
#         if not os.path.exists('../execution_results'):
#             os.makedirs('../execution_results')
#         with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
#             f.write('ValueError_sto\t%s\n' % sys.argv[1])
#

# if __name__ == '__main__':
#     main()
