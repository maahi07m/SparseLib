""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import os
import sys
import time

sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc


def inner_product(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2,
                  file_id_2):
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
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
        start_time = time.time()
        output = 0
        loop_bound = len(ia)  # len(ia) == len(ib)
        for row in range(1, loop_bound):
            ia_value = ia[row]
            a_nz = ia_value - ia[row - 1]
            if a_nz == 0:
                continue
            ib_value = ib[row]
            b_nz = ib_value - ib[row - 1]
            if b_nz == 0:
                continue
            output += ar[ia_value - 1] * br[ib_value - 1]
        total_time = time.time() - start_time
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
            f.write('inner product\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

        return output
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


def outer_product(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2, matrix_size_col_2,
                  file_id_2):
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
    :return: three list cr ic, jc, is the result-matrix in csr format
    """
    '''1xn 1xn both'''
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
        start_time = time.time()
        cr, ic, jc = [], [0], []

        for a_value in ar:
            for b_value in br:
                cr.append(a_value * b_value)
        ic = [ja_value * len(br) for ja_value in ja]
        jc = jb * len(ar)
        total_time = time.time() - start_time
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
            f.write('outer product\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

        return cr, ic, jc
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


def multiply_matrix_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                           matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param file_id_2: int
    ----------------------
    input must be: matrix mxn and vector nx1
    ----------------------
    Convert the A matrix in csr format and the B matrix in csc format, usage of multiply_row_col function to multiply
    ----------------------
    :return: three lists cr, ic, jc, is the result in csc format stored
    """
    if matrix_size_col_1 == matrix_size_row_2 and matrix_size_col_2 == 1:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        xr, ix, jx = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
        cr, ic, jc = [], [], [0]
        start_time = time.time()
        previous_ja_index = 0

        for index in range(1, len(ia)):
            nz_number = ia[index] - ia[index - 1]
            new_ja_index = previous_ja_index + nz_number
            result_of_rows_cols = multiply_row_col(ja[previous_ja_index:new_ja_index],
                                                   ar[previous_ja_index:new_ja_index], ix, xr)
            previous_ja_index = new_ja_index
            if result_of_rows_cols:
                cr.append(result_of_rows_cols)
                ic.append(index - 1)
        jc.append(len(cr))

        total_time = time.time() - start_time
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
            f.write('matrix-vector\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

        return cr, ic, jc
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


def multiply_vector_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                           matrix_size_col_2, file_id_2):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param density: float
    :param file_id_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param file_id_2: int
    ----------------------
    input must be: matrix nxm, vector 1xn
    ----------------------
    Convert the A matrix in csc format and the B matrix in csr format, usage of multiply_row_col function to multiply
    ----------------------
    :return: three lists cr, ic, jc, is the result in csr format stored
    """
    ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    xr, ix, jx = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    cr, ic, jc = [], [0], []
    previous_ia_index = 0
    start_time = time.time()

    for index in range(1, len(ja)):
        nz_number = ja[index] - ja[index - 1]
        if nz_number == 0:
            continue
        new_ia_index = previous_ia_index + nz_number
        result_of_rows_cols = multiply_row_col(ia[previous_ia_index:new_ia_index], ar[previous_ia_index:new_ia_index],
                                               jx, xr)
        previous_ia_index = new_ia_index
        if result_of_rows_cols:
            cr.append(result_of_rows_cols)
            jc.append(index - 1)

    ic.append(len(cr))
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
        f.write('vector-matrix\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, density, total_time))

    return cr, ic, jc


# TODO: tests , change dictionary to be passed from function caller, comments
# TODO: sparse matrix comments and write
# TODO: check again matrix vector multiplication
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
    row_nz_values = {}
    for index, value in enumerate(row_indexes):
        row_nz_values[value] = row_values[index]

    for index, value in enumerate(vector_nz_indexes):
        if value in row_nz_values:
            result += row_nz_values[value] * vector_nz_values[index]

    return result


# def multiply_row_col(row_indexes, row_values, vector_nz_indexes, vector_nz_values):
#     """
#     :param row_indexes: list
#     :param row_values: list
#     :param vector_nz_indexes: list
#     :param vector_nz_values: list
#     ----------------------
#     A loop in the max length of indexes lists multiply only when the elements in indexes lists is the same
#     based in inner algorithm we found
#     ----------------------
#     :return: the result of a row/col multiply by a sparse vectors elements
#     """
#     result = 0
#     length_row_index = len(row_indexes)
#     length_vector_index = len(vector_nz_indexes)
#     loop_upper_bound = max(length_row_index, length_vector_index)
#     row_index = 0
#     vector_index = 0
#     for index in range(loop_upper_bound):
#         if row_indexes[row_index] < vector_nz_indexes[vector_index]:
#             row_index += 1
#         elif row_indexes[row_index] > vector_nz_indexes[vector_index]:
#             vector_index += 1
#         else:
#             result += row_values[row_index] * vector_nz_values[vector_index]
#             row_index += 1
#             vector_index += 1
#         if row_index >= length_row_index or vector_index >= length_vector_index:
#             break
#
#     return result


def multiply_matrix_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                           matrix_size_col_2, file_id_2):
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
    :return: three lists cr, ic, jc, is the result of the multiplication in csr format stored
    """
    if matrix_size_col_1 == matrix_size_row_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
        cr, ic, jc = [], [0], []
        previous_index_a = 0
        counter_nz = 0

        start_time = time.time()
        b_cols_list = fetch_inner_for_loop_values(ib, br, jb)
        length_jb = len(b_cols_list)
        length_ia = len(ia)

        for index in range(1, length_ia):
            nz_number_a = ia[index] - ia[index - 1]
            if nz_number_a == 0:
                continue
            new_index_a = previous_index_a + nz_number_a
            a_rows = ja[previous_index_a:new_index_a]
            a_values = ar[previous_index_a:new_index_a]
            previous_index_a = new_index_a

            for inner_index in range(length_jb):
                result = multiply_row_col_for_matrix_matrix_multiplication(a_rows, a_values, b_cols_list[inner_index])

                if result:
                    cr.append(result)
                    jc.append(inner_index - 1)
                    counter_nz += 1
            ic.append(counter_nz)

        total_time = time.time() - start_time
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_time.txt'), 'a') as f:
            f.write(
                'matrix-matrix\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                           density, total_time))
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal')

    return cr, ic, jc


def multiply_row_col_for_matrix_matrix_multiplication(row_indexes, row_values, vector_nz):
    """
    :param row_indexes: list
    :param row_values: list
    :param vector_nz: list
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


if __name__ == '__main__':
    if sys.argv[1] == 'inner':
        result_inner = inner_product(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                                     int(sys.argv[6]),
                                     int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'outer':
        result_outer = outer_product(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                                     int(sys.argv[6]),
                                     int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'matrix_vector':
        multiply_matrix_vector(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                               int(sys.argv[6]),
                               int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'vector_matrix':
        multiply_vector_matrix(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                               int(sys.argv[6]),
                               int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'matrix_matrix':
        multiply_matrix_matrix(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                               int(sys.argv[6]),
                               int(sys.argv[7]), int(sys.argv[8]))
    else:
        print('You choose wrong algorithm.')
