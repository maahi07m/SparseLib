""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import os
import sys
import time
from functools import singledispatch

sys.path.append('../')
from compress.csr_coo import csr
from read_file.matrix_read import read_matrix_parallel
from helpers.generator import generate_sparse_matrix
from compress.diagonal_csc import csc
from read_file.read_hb_format import read_file
try:
    from operations.multiplication_algorithm import inner_algorithm, outer_algorithm, multiply_matrix_vector_algorithm,\
        multiply_vector_matrix_algorithm
except ImportError:
    from operations.multiplication_algorithm import inner_algorithm, outer_algorithm, multiply_matrix_vector_algorithm, \
        multiply_vector_matrix_algorithm

@singledispatch
def inner_product(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2):
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@inner_product.register
def _inner_product(file_name_1: str, file_name_2: str):
    ar, ia, ja = csr(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)

    return inner_algorithm(ar, ia, br, ib)


@inner_product.register
def _inner_product(matrix_size_row_1: int, matrix_size_col_1: int, density: float, file_id_1: int,
                   matrix_size_row_2: int, matrix_size_col_2: int,file_id_2: int):
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        if matrix_size_row_1 == matrix_size_row_2 and file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@singledispatch
def outer_product(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2):
        ar, ia, ja = csc(matrix_1)
        if matrix_1 == matrix_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_2)

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@outer_product.register
def _outer_product(file_name_1: str, file_name_2: str):
    ar, ia, ja = csc(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)

    return outer_algorithm(ar, ja, br, jb)


@outer_product.register
def _outer_product(matrix_size_row_1: int, matrix_size_col_1: int, density: float, file_id_1: int,
                   matrix_size_row_2: int, matrix_size_col_2: int,file_id_2: int):
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        if matrix_size_row_1 == matrix_size_row_2 and file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@singledispatch
def multiply_matrix_vector(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2):
        ar, ia, ja = csr(matrix_1)
        xr, ix, jx = csc(matrix_2)

        return multiply_matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_matrix_vector.register
def _multiply_matrix_vector(file_name_1: str, file_name_2: str):
    ar, ia, ja = csr(file_name_1)
    xr, ix, jx = csc(file_name_2)

    return multiply_matrix_vector_algorithm(ar, ia, ja, xr, ix)


@multiply_matrix_vector.register
def _multiply_matrix_vector(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                            matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int):
    if matrix_size_col_1 == matrix_size_row_2 and matrix_size_col_2 == 1:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        xr, ix, jx = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return multiply_matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_matrix_vector.register
def _multiply_matrix_vector(is_hd: bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csr(matrix)
    # xr, ix, jx = !!!!!!!!!!!!!!!!! ATTENTION!!!!!!


@singledispatch
def multiply_vector_matrix(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2[0]):
        ar, ia, ja = csc(matrix_1)
        xr, ix, jx = csr(matrix_2)

        return multiply_vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_vector_matrix.register
def _multiply_vector_matrix(file_name_1: str, file_name_2: str):
    ar, ia, ja = csc(file_name_1)
    xr, ix, jx = csr(file_name_2)

    return multiply_vector_matrix_algorithm(ar, ia, ja, xr, jx)


@multiply_vector_matrix.register
def _multiply_vector_matrix(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                            matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int):
    if matrix_size_row_1 == matrix_size_col_2 and matrix_size_row_2 == 1:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        xr, ix, jx = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return multiply_vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_vector_matrix.register
def _multiply_vector_matrix(is_hb:bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csc(matrix)
    # xr, ix, jx = !!!!!!!!!!!!!!!!! ATTENTION!!!!!!


if __name__ == '__main__':
    # out2= inner_product('output_5_1_0.5_1.txt', 'output_5_1_0.5_1.txt')

    # out1= inner_product(read_matrix_parallel('output_5_1_0.5_1.txt'),
    #                               read_matrix_parallel('output_5_1_0.5_1.txt'))
    # out3 = inner_product(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
    #                      int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
    #
    # if out1==out2==out3:
    #     print('ok')

    # cr, ic, jc = outer_product(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
    #                              int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
    # cr1, ic1, jc1 = outer_product('output_1_4_0.5_2.txt', 'output_1_4_0.5_2.txt')
    # cr2, ic2, jc2 = outer_product(read_matrix_parallel('output_1_4_0.5_2.txt'),
    #                               read_matrix_parallel('output_1_4_0.5_2.txt'))
    #
    # print(cr, ic, jc)
    # print(cr1, ic1, jc1)
    # print(cr2, ic2, jc2)
    # if cr == cr1 == cr2:
    #     print('ok')
    # if ic == ic1 == ic2:
    #     print('ok'
    # if jc == jc1 == jc2:
    #     print('ok')

    # cr, ic, jc = multiply_vector_matrix(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]),
    #                                     float(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]))
    #
    # cr1, ic1, jc1 = multiply_vector_matrix('output_4_4_0.5_2.txt', 'output_1_4_0.5_2.txt')
    #
    # cr2, ic2, jc2 = multiply_vector_matrix(read_matrix_parallel('output_4_4_0.5_2.txt'),
    #                                        read_matrix_parallel('output_1_4_0.5_2.txt'))
    #
    # if cr == cr1 == cr2:
    #     print('ok')
    # if ic == ic1 == ic2:
    #     print('ok')
    # if jc == jc1 == jc2:
    #     print('ok')
