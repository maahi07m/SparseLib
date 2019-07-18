import time
import sys
import numpy as np
sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc
from read_file.matrix_read import read_matrix_parallel
import scipy.sparse as sp
import multiprocessing as mp
from multiprocessing import Pool


file_1 = "output_5000_5000_0.005_2.txt"
file_2 = "output_5000_5000_0.005_1.txt"
matrix_size_row = 15000
matrix_size_col = 15000
matrix_size_row_1 = 5000
matrix_size_col_1 = 5000
matrix_size_row_2 = 5000
matrix_size_col_2 = 5000
density = 0.005
file_id_1 = 1
file_id_2 = 2


def matrix_matrix_multi():
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    B = read_matrix_parallel(file_1)
    CR, IC, JC = [], [0], []
    length_b = len(B)
    start = time.time()

    for index in range(len(IA) - 1):
        inner_index_a_1 = IA[index]
        inner_index_a_2 = IA[index + 1]

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
    print('time ---', time.time() - start)
    # print(CR, IC, JC)


def multi_csr_matrix_dense_vector():
    AR, IA, JA = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    x_vector = read_matrix_parallel(file_1)
    y_vector = []

    start = time.time()

    for index in range(len(IA) - 1):
        inner_index_1 = IA[index]
        inner_index_2 = IA[index + 1]
        y = 0

        for inner_index in range(inner_index_1, inner_index_2):
            x_list = list(list(x_vector[JA[inner_index]]))
            x = x_list[0]
            y = y + AR[inner_index] * x
        y_vector.append(y)

    print('time csr', time.time()-start)
    print(y_vector)

    return y_vector


def multi_csc_matrix_dense_vector():
    AR, IA, JA = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    x_vector = read_matrix_parallel(file_1)
    y_vector = []

    start = time.time()

    for index in range(len(JA) - 1):
        y_vector.append(0)

    for index in range(len(JA)-1):
        inner_index_1 = JA[index]
        inner_index_2 = JA[index + 1]

        for inner_index in range(inner_index_1, inner_index_2):
            x_list = list(list(x_vector[index]))
            x = x_list[0]
            y_vector[IA[inner_index]] = y_vector[IA[inner_index]] + x * AR[inner_index]

    print('time csc', time.time() - start)

    return y_vector


def multi_matrix_sparse_vector():
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    XR, IX, JX = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    CR, IC, JC = [], [], [0]
    start = time.time()
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
    print('time', time.time() - start)
    print(CR, IC, JC)

    return CR, IC, JC


def multi_sparse_vector_matrix():
    AR, IA, JA = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    XR, IX, JX = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    CR, IC, JC = [], [0], []
    previous_ia_index = 0

    for index in range(1, len(JA)):
        nz_number = JA[index] - JA[index - 1]
        new_ia_index = previous_ia_index + nz_number
        result_of_rows_cols = multiply_row_col(IA[previous_ia_index:new_ia_index], AR[previous_ia_index:new_ia_index], JX, XR)
        previous_ia_index = new_ia_index
        if result_of_rows_cols:
            CR.append(result_of_rows_cols)
            JC.append(index - 1)
    IC.append(len(CR))

    return CR, IC, JC


def multi_matrix_matrix():
    AR, IA, JA = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    BR, IB, JB = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    # print(AR, IA, JA )
    # print(BR, IB, JB)
    start = time.time()
    CR, IC, JC = [], [0], []
    previous_index_a = 0

    counter_nz = 0
    b_cols_list, b_values_list = fetch_inner_for_loop_values(IB, BR, JB)
    length_jb = len(JB)
    length_ia = len(IA)

    for index in range(1, length_ia):
        nz_number_a = IA[index] - IA[index - 1]
        new_index_a = previous_index_a + nz_number_a
        a_rows = JA[previous_index_a:new_index_a]
        a_values = AR[previous_index_a:new_index_a]
        previous_index_a = new_index_a

        for inner_index in range(1, length_jb):
            result = multiply_row_col(a_rows, a_values, b_cols_list[inner_index], b_values_list[inner_index])

            if result:
                CR.append(result)
                JC.append(inner_index - 1)
                counter_nz += 1
        IC.append(counter_nz)

    print(time.time() - start)
    print(length_ia)

    return CR, IC, JC


def multiply_row_col(row_indexes, row_values, vector_nz_indexes, vector_nz_values):
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


def fetch_inner_for_loop_values(ib, br, jb):
    b_cols_list = ['_']
    b_values_list = ['_']
    previous_index_b = 0
    for index in range(1, len(jb)):
        nz_number_b = jb[index] - jb[index - 1]
        new_index_b = previous_index_b + nz_number_b
        b_cols_list.append(ib[previous_index_b:new_index_b])
        b_values_list.append(br[previous_index_b:new_index_b])
        previous_index_b = new_index_b

    return b_cols_list, b_values_list


# def multiply_row_col(row_indexes, row_values, vector_nz_indexes, vector_nz_values):
#     result = 0
#     indexes_union = sorted(set(row_indexes).union(vector_nz_indexes))
#     row_index = 0
#     vector_index = 0
#     for index in indexes_union:
#         if index not in row_indexes:
#             vector_index += 1
#         elif index not in vector_nz_indexes:
#             row_index += 1
#         else:
#             result += row_values[row_index] * vector_nz_values[vector_index]
#             row_index += 1
#             vector_index += 1
#
#     return result

# def multiply_row_col(row_indexes, row_values, vector_nz_indexes, vector_nz_values):
#     result = 0
#     loop_upper_bound = max(len(row_indexes), len(vector_nz_indexes))
#     loop_lower_bound = min(len(row_indexes), len(vector_nz_indexes)) - 1
#     for index in range(loop_upper_bound):
#         if index > loop_lower_bound:
#             break
#         if row_indexes[index] == vector_nz_indexes[index]:
#             result += row_values[index] * vector_nz_values[index]
#
#     return result

def inner_product_numpy():
    A = read_matrix_parallel(file_1)
    A = np.transpose(A)
    B = read_matrix_parallel(file_2)
    C = np.dot(A, B)
    print("numpy : ")
    print(C)


def inner_product():
    AR, IA, JA = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    BR, IB, JB = csr(matrix_size_row, matrix_size_col, density, file_id_2)

    index_a = 1
    index_b = 1
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
    print("our :", output)


def outer_product_numpy():
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    C = np.outer(A, B)
    print("numpy : ", C)


def outer_product():
    AR, IA, JA = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    BR, IB, JB = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    CR, IC, JC = [], [0], []

    values_per_row = IB[1]
    for _ in range(JA[0]):
        IC.append(0)

    ja_index = 1
    for a_value in AR:
        for b_value in BR:
            CR.append(a_value * b_value)
        JC += JB

        if ja_index < len(JA):
            number_of_empty_rows = JA[ja_index] - JA[ja_index - 1]
            ja_index +=1
            last_ic_value = IC[len(IC) - 1]
            if number_of_empty_rows == 1:
                IC.append(last_ic_value + values_per_row)
            else:
                for _ in range(number_of_empty_rows ):
                    IC.append(last_ic_value + values_per_row)
        else:
            IC.append(IC[len(IC) - 1] + values_per_row)
    # print(CR)
    # print(IC)
    # print(JC)

    return CR, IC, JC


def matrix_vector_numpy():
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    C = np.dot(A, B)
    print("numpy : ")
    print(C)


def matrix_vector():
    r, i , j = csc(matrix_size_row,  matrix_size_col, density, 3)
    AR, IA, JA = csr(matrix_size_row, matrix_size_col,  density, file_id_1)
    BR, IB, JB = csc(matrix_size_row, matrix_size_col,  density, file_id_2)
    CR, IC, JC = [], [0], []

    vector_size = len(IA)   # len(IA) == len(IB)
    for a_row_index in range(1, vector_size):
        row_nz_number = IA[a_row_index-1: a_row_index]


def numpy_matrix_matrix():
    A = read_matrix_parallel(file_2)
    B = read_matrix_parallel(file_1)

    A = sp.csr_matrix(np.array(A))
    B = np.array(B)
    # print('starting array')
    # A = scipy.sparse.csr_matrix(A)
    # B = scipy.sparse.csr_matrix(B)
    print('start time')
    start_time = time.time()
    # result = sp.csr_matrix(A).multiply(sp.csr_matrix(B)).todense()
    result = A.dot(B)
    # result = A*B

    print('time', time.time() -start_time)

    print(result)


if __name__ == '__main__':
    # c_vector = multi_csc_matrix_dense_vector()
    #c_vector = multi_csr_matrix_dense_vector()
    #CR, IC, JC = multi_matrix_sparse_vector()
    # CR, IC, JC = multi_sparse_vector_matrix()
    # CR, IC, JC = multi_matrix_matrix()
    # inner_product()
    #  outer_product()
    # inner_product_numpy()
    # outer_product_numpy()
    matrix_matrix_multi2()
    #numpy_matrix_matrix()