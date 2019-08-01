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


def write_outer(matrix, operation_type):
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    with open(os.path.join('../numpy_results', operation_type + '_numpy.txt'), 'w') as f:
        f.write(data_to_write)


def inner_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density, file_id_1,
                        file_id_2):
    """
    :param matrix_size_row_1: number
    :param matrix_size_col_1: number
    :param matrix_size_row_2: number
    :param matrix_size_col_2: number
    :param density: number
    :param file_id_1: string
    :param file_id_2: string
    ----------------------
    input must be vector nx1 and vector nx1
    ----------------------
    :return: a number
    """
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    a_matrix = np.transpose(a_matrix)
    b_matrix = read_matrix_parallel(file_2)
    result = np.dot(a_matrix, b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('inner numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                         density, total_time))
    with open(os.path.join('../numpy_results', 'inner_numpy.txt'), 'w') as f:
        f.write('%d\n' % result)
    return result


def outer_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density, file_id_1,
                        file_id_2):
    """
    :param matrix_size_row_1: number
    :param matrix_size_col_1: number
    :param matrix_size_row_2: number
    :param matrix_size_col_2: number
    :param density: number
    :param file_id_1: string
    :param file_id_2: string
    ----------------------
    input must be vector mx1 and vector nx1
    ----------------------
    :return: a matrix mxn
    """
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    result = np.outer(a_matrix, b_matrix)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('outer numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                         density, total_time))
    write_outer(result, 'outer')

    return result


def numpy_matrix_vector(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density, file_id_1,
                        file_id_2):
    """
    :param matrix_size_row_1: number
    :param matrix_size_col_1: number
    :param matrix_size_row_2: number
    :param matrix_size_col_2: number
    :param density: number
    :param file_id_1: string
    :param file_id_2: string
    ----------------------
    input must be matrix mxn and vector nx1
    ----------------------
    :return: a vector mx1
    """
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
    write_outer(result, 'matrix_vector')
    return result


# TODO: density for second matrix-vector
def numpy_vector_matrix(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density, file_id_1,
                        file_id_2):
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


def numpy_matrix_matrix(matrix_size_row_1, matrix_size_col_1, matrix_size_row_2, matrix_size_col_2, density, file_id_1,
                        file_id_2):
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
    # if sys.argv[1] == 'inner':
    #     result_inner = inner_product_numpy(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
    #                                        int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    # elif sys.argv[1] == 'outer':
    #     result_outer = outer_product_numpy(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
    #                                        int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    # elif sys.argv[1] == 'matrix_vector':
    #     result_matrix_vector = numpy_matrix_vector(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
    #                                                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]),
    #                                                int(sys.argv[8]))
    # elif sys.argv[1] == 'matrix_matrix':
    #     result_matrix_matrix = numpy_matrix_matrix(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]),
    #                                                int(sys.argv[5]), int(sys.argv[6]), int(sys.argv[7]),
    #                                                int(sys.argv[8]))
    # else:
    #     print('You choose wrong algorithm.')
    numpy_matrix_vector(4, 4, 4, 1, 0.5, 1, 2)
