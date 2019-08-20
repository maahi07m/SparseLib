"""This script is a helper to validate the result of multiplication (usage numpy library)"""
import multiprocessing as mp
import os
import sys
import time

import numpy as np
import scipy.sparse as sp

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


def __prepare_matrix(line):
    data_to_write = ''
    for index, inner in enumerate(line):
        if index == line.shape[0] - 1:
            data_to_write += str(int(inner))
        else:
            data_to_write += ("%s\t" % str(int(inner)))
    data_to_write += "\n"
    return data_to_write


def write_(matrix, matrix_size_row, matrix_size_col, density_1, density_2, operation_type):
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    if operation_type == 'outer':
        file_id = 31
    elif operation_type == 'matrix_vector':
        file_id = 32
    elif operation_type == 'vector_matrix':
        file_id = 33
    else:
        file_id = 34
    with open(os.path.join('../data_files', 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' +
                                            str(density_1) + str(density_2) + '_' + str(file_id) + '.txt'), 'w') as f:
        f.write(data_to_write)


def inner_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density_1,
                        density_2, file_id_1, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density_1, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density_2, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    a_matrix = np.transpose(a_matrix)
    b_matrix = read_matrix_parallel(file_2)
    result = np.dot(a_matrix, b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('inner numpy\t%s\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density_1, density_2, total_time))
    if not os.path.exists('../numpy_results'):
        os.makedirs('../numpy_results')
    with open(os.path.join('../numpy_results', 'inner_numpy.txt'), 'w') as f:
        f.write('%d\n' % result)
    return result


def outer_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density_1,
                        density_2, file_id_1,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density_1, density_2, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density_1, density_2, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    result = np.outer(a_matrix, b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('outer numpy\t%s\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density_1, density_2, total_time))

    write_(result, matrix_size_col_1, matrix_size_col_2, density_1, density_2, 'outer')

    return result


def numpy_matrix_vector(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density_1,
                        density_2, file_id_1,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density_1, density_2, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density_1, density_2, file_id_2)
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = np.array(a_matrix)
    b_matrix = np.array(b_matrix)
    start_time = time.time()
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('matrix vector numpy\t%s\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1,
                                                                     matrix_size_col_2, density_1, density_2,
                                                                     total_time))
    write_(result, matrix_size_row_2, matrix_size_col_2, density_1, density_2, 'matrix_vector')
    return result


def numpy_vector_matrix(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density_1,
                        density_2, file_id_1,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density_1, density_2, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density_1, density_2, file_id_2)
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = np.array(a_matrix)
    b_matrix = np.array(b_matrix)
    start_time = time.time()
    result = b_matrix.dot(a_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'vector matrix numpy\t%s\t%s\t%s\t%s\t%s\t%.5f\n' % (
            matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
            density_1, density_2, total_time))
    write_(result, matrix_size_col_1, matrix_size_col_1, density_1, density_2, 'vector_matrix')
    return result


def numpy_matrix_matrix(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density_1,
                        density_2, file_id_1,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density_1, density_2, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density_1, density_2, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = sp.csr_matrix(np.array(a_matrix))
    b_matrix = np.array(b_matrix)
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'matrix matrix numpy\t%s\t%s\t%s\t%s\t%s\t%.5f\n' % (
            matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
            density_1, density_2, total_time))
    write_(result, matrix_size_col_1, matrix_size_row_2, density_1, density_2, 'matrix_matrix')
    return result
