""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import time
import sys
import os
import scipy.sparse as sp
import numpy as np
sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc
from read_file.matrix_read import read_matrix_parallel


def inner_product(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1:
    :param matrix_size_col_1:
    :param density:
    :param file_id_1:
    :param matrix_size_row_2:
    :param matrix_size_col_2:
    :param file_id_2:
    ----------------------
    input must be vector nx1, vector nx1
    ----------------------
    Convert the A vector in csr format and B vector in csr format, ...
    ----------------------
    :return: a number
    """
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    BR, IB, JB = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    output = 0
    loop_bound = len(IA)    # len(IA) == len(IB)
    for row in range(1, loop_bound):
        ia_value = IA[row]
        a_nz = ia_value - IA[row - 1]
        if a_nz == 0:
            continue
        ib_value = IB[row]
        b_nz = ib_value - IB[row - 1]
        if b_nz == 0:
            continue
        output += AR[ia_value - 1] * BR[ib_value - 1]
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('inner product %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return output


def outer_product(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1:
    :param matrix_size_col_1:
    :param density:
    :param file_id_1:
    :param matrix_size_row_2:
    :param matrix_size_col_2:
    :param file_id_2:
    ----------------------
    input must be: vector 1xn, vector 1xn
    ----------------------
    Convert A matrix in csc format and B matrix in csr format, ...
    ----------------------
    :return: three list CR< IC, JC, is the result-matrix in csr format
    """
    '''1xn 1xn both'''
    AR, IA, JA = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    BR, IB, JB = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    CR, IC, JC = [], [0], []

    for a_value in AR:
        for b_value in BR:
            CR.append(a_value * b_value)
    IC = [ja_value * len(BR) for ja_value in JA]
    JC = JB * len(AR)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('outer product %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return CR, IC, JC


def multi_matrix_dense_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, file):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param file: string
    ----------------------
    input must be: matrix nxm, matrix mxn
    ----------------------
    Convert the one matrix in csr format and the other is stored as tuple, for the non zero values in each row
    (A matrix) multiply with the values in JA[index] position in all cols (B matrix) algorithm based on SpMV
    ----------------------
    :return: three lists CR, IC, JC, is the result of the multiplication saved in csr format
    """
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    B = read_matrix_parallel(file)
    CR, IC, JC = [], [0], []
    length_b = len(B[0])
    start_time = time.time()

    for index in range(len(IA) - 1):
        inner_index_a_1 = IA[index]
        inner_index_a_2 = IA[index + 1]

        if inner_index_a_1 == inner_index_a_2:
            continue

        for index_of_b in range(length_b):
            sum_of_each_row = 0

            for inner_index in range(inner_index_a_1, inner_index_a_2):
                if B[JA[inner_index]][index_of_b] == 0:
                    continue
                sum_of_each_row += AR[inner_index] * B[JA[inner_index]][index_of_b]

            if sum_of_each_row != 0:
                CR.append(sum_of_each_row)
                JC.append(index_of_b)
        IC.append(len(CR))
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('SpMM alg %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return CR, IC, JC


def multi_csr_matrix_dense_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, file):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param file: string
    ----------------------
    input must be: vector nx1, vector nx1
    ----------------------
    Convert the matrix in csr format, for the non zero values in each row(A matrix, use the IA) multiply with the
    values in JA[index] position in the sparse vector based on SpMV algorithm
    ----------------------
    :return: a list which represent a sparse vector
    """
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    x_vector = read_matrix_parallel(file)
    y_vector = []
    start_time = time.time()

    for index in range(len(IA) - 1):
        inner_index_1 = IA[index]
        inner_index_2 = IA[index + 1]
        y = 0

        for inner_index in range(inner_index_1, inner_index_2):
            x_list = list(list(x_vector[JA[inner_index]]))
            x = x_list[0]
            y = y + AR[inner_index] * x
        y_vector.append(y)

    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('SpMV alg csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return y_vector


def multi_csc_matrix_dense_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, file):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param file: string
    ----------------------
    input must be: vector nx1, vector nx1
    ----------------------
    Convert the matrix in csc format, for the non zero values in each col(A matrix, use the JA) multiply with the
    values in JA[index] position in the sparse vector based on SpMV algorithm
    ----------------------
    :return: a list which represent a sparse vector
    """
    AR, IA, JA = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    x_vector = read_matrix_parallel(file)
    y_vector = []
    start_time = time.time()

    for index in range(len(JA) - 1):
        y_vector.append(0)

    for index in range(len(JA)-1):
        inner_index_1 = JA[index]
        inner_index_2 = JA[index + 1]

        for inner_index in range(inner_index_1, inner_index_2):
            x_list = list(list(x_vector[index]))
            x = x_list[0]
            y_vector[IA[inner_index]] = y_vector[IA[inner_index]] + x * AR[inner_index]

    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('SpMV alg csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return y_vector


def multi_matrix_sparse_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param file_id_2: int
    ----------------------
    input must be: vector nx1, vector nx1
    ----------------------
    Convert the A matrix in csr format and the B matrix in csc format, usage of multiply_row_col function to multiply
    ----------------------
    :return: three lists CR, IC, JC, is the result in csc format stored
    """
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    XR, IX, JX = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    CR, IC, JC = [], [], [0]
    start_time = time.time()
    previous_ja_index = 0

    for index in range(1, len(IA)):
        nz_number = IA[index] - IA[index - 1]
        new_ja_index = previous_ja_index + nz_number
        result_of_rows_cols = multiply_row_col(JA[previous_ja_index:new_ja_index], AR[previous_ja_index:new_ja_index], IX, XR)
        previous_ja_index = new_ja_index
        if result_of_rows_cols:
            CR.append(result_of_rows_cols)
            IC.append(index-1)
    JC.append(len(CR))

    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('Matrix sparse-vector  %s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return CR, IC, JC


def multi_sparse_vector_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param file_id_2: int
    ----------------------
    input must be: vector nx1, vector nx1
    ----------------------
    Convert the A matrix in csc format and the B matrix in csr format, usage of multiply_row_col function to multiply
    ----------------------
    :return: three lists CR, IC, JC, is the result in csr format stored
    """
    AR, IA, JA = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    XR, IX, JX = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    CR, IC, JC = [], [0], []
    previous_ia_index = 0
    start = time.time()

    for index in range(1, len(JA)):
        nz_number = JA[index] - JA[index - 1]
        new_ia_index = previous_ia_index + nz_number
        result_of_rows_cols = multiply_row_col(IA[previous_ia_index:new_ia_index], AR[previous_ia_index:new_ia_index], JX, XR)
        previous_ia_index = new_ia_index
        if result_of_rows_cols:
            CR.append(result_of_rows_cols)
            JC.append(index - 1)
    IC.append(len(CR))
    print('time S_V_M', time.time() - start)

    return CR, IC, JC


def multiply_row_col(row_indexes, row_values, vector_nz_indexes, vector_nz_values):
    """
    :param row_indexes: list
    :param row_values: list
    :param vector_nz_indexes: list
    :param vector_nz_values: list
    ----------------------
    A loop in the max length of indexes lists multiply only when the elements in indexes lists is the same
    based in inner algorithm we found
    ----------------------
    :return: the result of a row/col multiply by a sparse vectors elements
    """
    result = 0
    length_row_index = len(row_indexes)
    length_vector_index = len(vector_nz_indexes)
    loop_upper_bound = max(length_row_index, length_vector_index)
    row_index = 0
    vector_index = 0
    for index in range(loop_upper_bound):
        if row_indexes[row_index] < vector_nz_indexes[vector_index]:
            row_index += 1
        elif row_indexes[row_index] > vector_nz_indexes[vector_index]:
            vector_index += 1
        else:
            result += row_values[row_index] * vector_nz_values[vector_index]
            row_index += 1
            vector_index += 1
        if row_index >= length_row_index or vector_index >= length_vector_index:
            break

    return result


def multi_matrix_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param file_id_2: int
    ----------------------
    Convert A matrix in csr format and B matrix in csc format, firstly with the usage of fetch_inner_for_loop_values
    function create the b_cols_list containing the number of non zero values in each cols in B matrix to use it
    in multiply_row_col_for_matrix_multi to multiply with the non zero values of A matrix
    ----------------------
    :return: three lists CR, IC, JC, is the result of the multiplication in csr format stored
    """
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    BR, IB, JB = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    CR, IC, JC = [], [0], []
    previous_index_a = 0
    counter_nz = 0

    start = time.time()
    b_cols_list = fetch_inner_for_loop_values(IB, BR, JB)
    length_jb = len(b_cols_list)
    length_ia = len(IA)

    for index in range(1, length_ia):
        nz_number_a = IA[index] - IA[index - 1]
        if nz_number_a == 0:
            continue
        new_index_a = previous_index_a + nz_number_a
        a_rows = JA[previous_index_a:new_index_a]
        a_values = AR[previous_index_a:new_index_a]
        previous_index_a = new_index_a

        for inner_index in range(length_jb):
            result = multiply_row_col_for_matrix_multi(a_rows, a_values, b_cols_list[inner_index])

            if result:
                CR.append(result)
                JC.append(inner_index - 1)
                counter_nz += 1
        IC.append(counter_nz)

    print(time.time() - start)
    print(length_ia)

    return CR, IC, JC


def multiply_row_col_for_matrix_multi(row_indexes, row_values, vector_nz):
    """
    :param row_indexes: list
    :param row_values: list
    :param vector_nz: list
    ----------------------

    ----------------------
    :return: the result of multiplication for a row and a col
    """
    result = 0
    for index, value in enumerate(row_indexes):
        if value in vector_nz:
            result += row_values[index] * vector_nz[value]

    return result


def fetch_inner_for_loop_values(ib, br, jb):
    """
    :param ib: list
    :param br: list
    :param jb: list
    ----------------------

    ----------------------
    :return: a list of non zero values per col
    """
    b_cols_list = []
    previous_index_b = 0
    for index in range(1, len(jb)):
        nz_number_b = jb[index] - jb[index - 1]
        new_index_b = previous_index_b + nz_number_b
        temp_dict = {}
        for inner_index in range(previous_index_b, new_index_b):
            temp_dict[ib[inner_index]] = br[inner_index]
        b_cols_list.append(temp_dict)
        previous_index_b = new_index_b

    return b_cols_list
