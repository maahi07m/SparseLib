"""This script is a helper to validate the result of multiplication (usage numpy library)"""
import time
import sys
import os
import scipy.sparse as sp
import numpy as np
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


def inner_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_col_2, density, file_id_1, matrix_size_row_2,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    A = read_matrix_parallel(file_1)
    A = np.transpose(A)
    B = read_matrix_parallel(file_2)
    C = np.dot(A, B)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('inner numpy \t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                          density, total_time))

    return C


def outer_product_numpy(matrix_size_row_1, matrix_size_col_1, matrix_size_col_2, density, file_id_1, matrix_size_row_2,
                        file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    C = np.outer(A, B)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write('outer numpy \t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                          density, total_time))

    return C


def numpy_matrix_vector(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = np.array(A)
    B = np.array(B)
    start = time.time()
    C = A.dot(B)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'matrix vector numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density, total_time))
    return C

# TODO: density for second matrix-vector
def numpy_vector_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = sp.csr_matrix(np.array(A))
    B = np.array(B)
    start_time = time.time()
    result = B.dot(A)
    total_time = time.time() - start_time
    with open(os.path.join('../execution_results', 'multiplication_numpy_time.txt'), 'a') as f:
        f.write(
            'vector matrix numpy\t%s\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row_1, matrix_size_col_1, matrix_size_col_2,
                                                             density, total_time))

    return result


def numpy_matrix_matrix(matrix_size_row_1, matrix_size_col_1, density, file_id_1, matrix_size_row_2,
                        matrix_size_col_2, file_id_2):
    file_1 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
    file_2 = "output_{}_{}_{}_{}.txt".format(matrix_size_row_2, matrix_size_col_2, density, file_id_2)
    start_time = time.time()
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = sp.csr_matrix(np.array(A))
    B = np.array(B)
    # A = scipy.sparse.csr_matrix(A)
    # B = scipy.sparse.csr_matrix(B)
    # result = sp.csr_matrix(A).multiply(sp.csr_matrix(B)).todense()
    result = A.dot(B)
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
    #     result_outer = outer_product_numpy(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]),
    #                                        int(sys.argv[7]), int(sys.argv[8]))
    # elif sys.argv[1] == 'matrix_vector':
    #     result_matrix_vector = numpy_matrix_vector(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
    #                                                int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    # else:
    #     result_matrix_matrix = numpy_matrix_matrix(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]),
    #                                                int(sys.argv[6]), int(sys.argv[7]), int(sys.argv[8]))
    numpy_vector_matrix(4, 4, 0.5, 2, 1, 4,  2)