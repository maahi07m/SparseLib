import multiprocessing as mp
import os
import sys
import time

from numpy import array
from scipy.sparse import csr_matrix, csc_matrix

sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc


def __prepare_matrix(line):
    data_to_write = ''
    for index, inner in enumerate(line):
        if index == line.shape[0] - 1:
            data_to_write += str(int(inner))
        else:
            data_to_write += ("%s\t" % str(int(inner)))
    data_to_write += "\n"
    return data_to_write


def __write_np_table(matrix, file_name):
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    with open(os.path.join('../data_files', file_name), 'w') as f:
        f.write(data_to_write)


def validate_operation(cr, ic, jc, npr, inp, jnp, file_name, operation_type):
    if cr == npr and ic == inp and jc == jnp:
        pass
    else:
        print("espase sto %s gia to %s" % (operation_type, file_name))
        with open(os.path.join('../operation_error', 'add_sub__hb_operation_error.txt'), 'a') as f:
            f.write(operation_type + '_\t%s\n' % file_name)


# def addition_matrices_numpy_csr(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
#     """
#     :param matrix_size_row: int
#     :param matrix_size_col: int
#     :param density: float
#     :param file_id_1: int
#     :param file_id_2: int
#     ----------------------
#     :return: result of the addition stored in numpy array format
#     """
#     file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_1) + '.txt'
#     file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_2) + '.txt'
#     a_matrix = read_matrix_parallel(file_1)
#     b_matrix = read_matrix_parallel(file_2)
#     a_matrix = csr_matrix(array(a_matrix))
#     b_matrix = csr_matrix(array(b_matrix))
#
#     start_time = time.time()
#     total = a_matrix + b_matrix
#     total_time = time.time() - start_time
#
#     if not os.path.exists('../execution_results'):
#         os.makedirs('../execution_results')
#     with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
#         f.write('addition_numpy_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
#     result_to_array = total.toarray()
#     numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
#                              + '22.txt'
#     __write_np_table(result_to_array, numpy_result_file_name)
#     return csr(matrix_size_row, matrix_size_col, density, 22)
#
#
# def subtraction_matrices_numpy_csr(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
#     """
#     :param matrix_size_row: int
#     :param matrix_size_col: int
#     :param density: float
#     :param file_id_1: int
#     :param file_id_2: int
#     ----------------------
#     :return: the result of the subtraction stored in numpy array
#     """
#     file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_1) + '.txt'
#     file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_2) + '.txt'
#     a_matrix = read_matrix_parallel(file_1)
#     b_matrix = read_matrix_parallel(file_2)
#     a_matrix = csr_matrix(array(a_matrix))
#     b_matrix = csr_matrix(array(b_matrix))
#
#     start_time = time.time()
#     total = a_matrix - b_matrix
#     total_time = time.time() - start_time
#
#     if not os.path.exists('../execution_results'):
#         os.makedirs('../execution_results')
#     with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
#         f.write('subtraction_numpy_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
#     result_to_array = total.toarray()
#     numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
#                              + '23.txt'
#     __write_np_table(result_to_array, numpy_result_file_name)
#     return csr(matrix_size_row, matrix_size_col, density, 23)
#
#
# def addition_matrices_numpy_csc(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
#     """
#     :param matrix_size_row: int
#     :param matrix_size_col: int
#     :param density: float
#     :param file_id_1: int
#     :param file_id_2: int
#     ----------------------
#     :return: result of the addition stored in numpy array format
#     """
#     file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_1) + '.txt'
#     file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_2) + '.txt'
#     a_matrix = read_matrix_parallel(file_1)
#     b_matrix = read_matrix_parallel(file_2)
#     a_matrix = csc_matrix(array(a_matrix))
#     b_matrix = csc_matrix(array(b_matrix))
#
#     start_time = time.time()
#     total = a_matrix + b_matrix
#     total_time = time.time() - start_time
#     if not os.path.exists('../execution_results'):
#         os.makedirs('../execution_results')
#     with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
#         f.write('addition_numpy_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
#     result_to_array = total.toarray()
#     numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
#                              + '20.txt'
#     __write_np_table(result_to_array, numpy_result_file_name)
#     return csc(matrix_size_row, matrix_size_col, density, 20)
#
#
# def subtraction_matrices_numpy_csc(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
#     """
#        :param matrix_size_row: int
#        :param matrix_size_col: int
#        :param density: float
#        :param file_id_1: int
#        :param file_id_2: int
#        ----------------------
#        :return: result of the subtraction stored in numpy array format
#        """
#     file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_1) + '.txt'
#     file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
#              str(file_id_2) + '.txt'
#     a_matrix = read_matrix_parallel(file_1)
#     b_matrix = read_matrix_parallel(file_2)
#     a_matrix = csc_matrix(array(a_matrix))
#     b_matrix = csc_matrix(array(b_matrix))
#
#     start_time = time.time()
#     total = a_matrix - b_matrix
#     total_time = time.time() - start_time
#
#     if not os.path.exists('../execution_results'):
#         os.makedirs('../execution_results')
#     with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
#         f.write('subtraction_numpy_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
#
#     result_to_array = total.toarray()
#     numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
#                              + '21.txt'
#     __write_np_table(result_to_array, numpy_result_file_name)
#     return csc(matrix_size_row, matrix_size_col, density, 21)


def addition_matrices_numpy_csr(matrix, file_name):
    a_matrix = csr_matrix(array(matrix))
    b_matrix = a_matrix

    start_time = time.time()
    total = a_matrix + b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
        f.write('addition_numpy_csr\t%s\t%.5f\n' % (file_name, total_time))

    result_to_array = [list(item) for item in total.toarray()]
    return csr(result_to_array)


def subtraction_matrices_numpy_csr(matrix, file_name):
    a_matrix = csr_matrix(array(matrix))
    b_matrix = a_matrix

    start_time = time.time()
    total = a_matrix - b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
        f.write('subtraction_numpy_csr\t%s\t%.5f\n' % (file_name, total_time))

    result_to_array = [list(item) for item in total.toarray()]
    return csr(result_to_array)


def addition_matrices_numpy_csc(matrix, file_name):
    a_matrix = csc_matrix(array(matrix))
    b_matrix = a_matrix

    start_time = time.time()
    total = a_matrix + b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
        f.write('addition_numpy_csc\t%s\t%.5f\n' % (file_name, total_time))

    result_to_array = [list(item) for item in total.toarray()]
    return csc(result_to_array)


def subtraction_matrices_numpy_csc(matrix, file_name):
    a_matrix = csc_matrix(array(matrix))
    b_matrix = a_matrix

    start_time = time.time()
    total = a_matrix - b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
        f.write('subtraction_numpy_csc\t%s\t%.5f\n' % (file_name, total_time))

    result_to_array = [list(item) for item in total.toarray()]
    return csc(result_to_array)
