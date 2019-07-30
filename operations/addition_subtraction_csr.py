"""This script calculate the addition and subtraction of two matrices and stored the results in csr format.
To run: python3 addition_subtraction_csr.py <algorithm name> <size of rows> <size of cols> <density> <file_id_1> <file_id_2>
"""
import os
import sys
import time

from numpy import array
from scipy.sparse import csr_matrix

sys.path.append('../')
from compress.csr_coo import csr
from read_file.matrix_read import read_matrix_parallel


def addition_matrices_numpy(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: result of the addition stored in numpy array format
    """
    file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_1) + '.txt'
    file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_2) + '.txt'
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = csr_matrix(array(a_matrix))
    b_matrix = csr_matrix(array(b_matrix))

    start_time = time.time()
    total = a_matrix + b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
        f.write('addition_numpy_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    # x = total.toarray()
    # with open("../data_files/output_10_0.5_3.txt", 'w') as f:
    #     for item in x:
    #         for index,inner in enumerate(item):
    #             if index == item.shape[0] - 1:
    #                 f.write("%s" % str(int(inner)), )
    #             else:
    #                 f.write("%s\t" % str(int(inner)), )
    #         f.write("\n")
    #
    # return csr(matrix_size, density, file_id_1+2)
    return total.toarray()


def addition_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the addition of two matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [0], []
    start_time = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(ia)):  # len(ia) = len(ib)
        a_row_number = ia[row_index] - ia[row_index - 1]  # get A's row number
        b_row_number = ib[row_index] - ib[row_index - 1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = ja[a_previous_row_index: new_a_row_index]
        b_columns = jb[b_previous_row_index: new_b_row_index]
        a_values = ar[a_previous_row_index: new_a_row_index]
        b_values = br[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns + b_columns))
        for index in all_columns:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                jc.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(b_values[b_value_index])
                jc.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] + b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    jc.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        ic.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('addition_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    # return cr, ic, jc
    return [], [], []


def subtraction_matrices_numpy(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction stored in numpy array
    """
    file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_1) + '.txt'
    file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_2) + '.txt'
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = csr_matrix(array(a_matrix))
    b_matrix = csr_matrix(array(b_matrix))

    start_time = time.time()
    total = a_matrix - b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
        f.write('subtraction_numpy_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    # x = total.toarray()
    # with open("../data_files/temp.txt", 'w') as f:
    #     for item in x:
    #         for index,inner in enumerate(item):
    #             if index == item.shape[0] - 1:
    #                 f.write("%s" % str(int(inner)), )
    #             else:
    #                 f.write("%s\t" % str(int(inner)), )
    #         f.write("\n")
    # return csr(matrix_size, density, file_id_1+2)
    return total.toarray()


def subtraction_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction of two matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [0], []
    start_time = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(ia)):  # len(ia) = len(ib)
        a_row_number = ia[row_index] - ia[row_index - 1]  # get A's row number
        b_row_number = ib[row_index] - ib[row_index - 1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = ja[a_previous_row_index: new_a_row_index]
        b_columns = jb[b_previous_row_index: new_b_row_index]
        a_values = ar[a_previous_row_index: new_a_row_index]
        b_values = br[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns).union(b_columns))
        for index in all_columns:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                jc.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(-b_values[b_value_index])
                jc.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] - b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    jc.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        ic.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('subtraction_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    # return cr, ic, jc
    return [], [], []


if __name__ == '__main__':
    if len(sys.argv) == 7:
        if sys.argv[1].lower() == 'addition':
            AR1, IA1, JA1 = addition_matrices_nxn(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
        elif sys.argv[1].lower() == 'subtraction':
            AR2, IA2, JA2 = subtraction_matrices_nxn(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif len(sys.argv) == 6:
        AR1, IA1, JA1 = addition_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        AR2, IA2, JA2 = subtraction_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
    else:
        print("There is no main to run")
    # npR, Inp, Jnp = addition_matrices_numpy()
    # numpy_result = addition_matrices_numpy()
    #
    # C, IC, JC = addition_matrices_nxn()

    # for x in range(len(C)):
    #     if C[x] != npR[x]:
    #         print(x, C[x], npR[x])
    # print('----')
    # for i in range(len(IC)):
    #     if IC[i] != Inp[i]:
    #         print(i, IC[i], Inp[i])
    # print('----')
    #
    # for  z in range(len(JC)):
    #     if JC[z] != Jnp[z]:
    #         print(z, JC[z], Jnp[z])
