"""This script is a helper to validate the result of multiplication (usage numpy library)"""
import os
import sys
import time

import numpy as np
import scipy.sparse as sp

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


def inner_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_col_2, density, file_id_1, matrix_size_row_2,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    a_matrix = np.transpose(a_matrix)
    b_matrix = read_matrix_parallel(file_2)
    result = np.dot(a_matrix, b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('inner numpy \t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                          density, total_time))

    return result


def outer_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_col_2, density, file_id_1, matrix_size_row_2,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    result = np.outer(a_matrix, b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('outer numpy \t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                          density, total_time))

    return result


def numpy_matrix_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = np.array(a_matrix)
    b_matrix = np.array(b_matrix)
    start_time = time.time()
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'matrix vector numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density, total_time))
    return result


# TODO: density for second matrix-vector
def numpy_vector_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = np.array(a_matrix)
    b_matrix = np.array(b_matrix)
    start_time = time.time()
    result = b_matrix.dot(a_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'vector matrix numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density, total_time))
    # print(result)
    return result


def numpy_matrix_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = sp.csr_matrix(np.array(a_matrix))
    b_matrix = np.array(b_matrix)
    # a_matrix = scipy.sparse.csr_matrix(a_matrix)
    # b_matrix = scipy.sparse.csr_matrix(b_matrix)
    # result = sp.csr_matrix(a_matrix).multiply(sp.csr_matrix(b_matrix)).todense()
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'matrix matrix numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density, total_time))
    return result


if __name__ == '__main__':
    if sys.argv[1] == 'inner':
        result_inner = inner_product_numpy(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                                           int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'outer':
        result_outer = outer_product_numpy(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
                                           int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    elif sys.argv[1] == 'matrix_vector':
        result_matrix_vector = numpy_matrix_vector(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
                                                   int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]),
                                                   int(sys.argv[8]))
    else:
        result_matrix_matrix = numpy_matrix_matrix(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
                                                   int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]),
                                                   int(sys.argv[8]))
