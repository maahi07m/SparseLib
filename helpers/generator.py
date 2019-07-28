"""
 To run: python3 generator.py <number of rows> <number of cols> <density> <file_id>
 It creates a sparse matrix with <number of rows> of rows and <number of cols> columns
"""
import multiprocessing as mp
import os
import sys
import time

import numpy as np
from scipy.sparse import random


def generate_sparse_matrix(lb, ub, m, n, dens):
    """
    :param lb: int
    :param ub: int
    :param m: int
    :param n: int
    :param dens: float
    ----------------------
    Generate a sparse matrix mxn
    ----------------------
    :return: sparse matrix
    """
    np.random.seed(int(time.time()))
    temp_matrix = random(m, n, format='csr', density=dens)
    generated_matrix = np.round((ub-lb + 1)*temp_matrix + lb*temp_matrix.ceil())
    return generated_matrix


def write_matrix_to_file(first_dimension, second_dimension, density, file_id, matrix, file_path):
    """
    :param first_dimension: int
    :param second_dimension: int
    :param density: float
    :param file_id: int
    :param matrix: list
    :param file_path: string
    ----------------------
    Store in data files a txt file containing the generated matrix mxn with name e.g. "output_1000_1000_0.005_1.txt"
    ----------------------
    :return: -
    """
    file_name = 'output_' + first_dimension + '_' + second_dimension + '_' + density + '_' + file_id + '.txt'
    matrix = matrix.toarray()
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    start_time = time.time()
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    with open(os.path.join(file_path+'data_files', file_name), 'w') as f:
        f.write(data_to_write)
    print(time.time() - start_time)


def __prepare_matrix(line):
    data_to_write = ''
    for index, inner in enumerate(line):
        if index == line.shape[0] - 1:
            data_to_write += str(int(inner))
        else:
            data_to_write += ("%s\t" % str(int(inner)))
    data_to_write += "\n"
    return data_to_write


def generate(first_dimension, second_dimension, density, file_id=1, lower_bound=-1000, upper_bound=100,
             file_path='../'):
    """
    :param first_dimension: int
    :param second_dimension: int
    :param density: float
    :param file_id: int
    :param lower_bound: int
    :param upper_bound: int
    :param file_path: string
    ----------------------
    Helper function to call generated_matrix to create the sparse matrix and write_matrix_to_file to save the matrix in
    a txt file
    ----------------------
    :return: -
    """
    generated_matrix = generate_sparse_matrix(lower_bound, upper_bound, first_dimension, second_dimension, density)
    write_matrix_to_file(str(first_dimension), str(second_dimension), str(density), str(file_id), generated_matrix,
                         file_path=file_path)
    # print(generated_matrix.A)


if __name__ == '__main__':
    if len(sys.argv) == 7:
        generate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]),
                 int(sys.argv[6]))
    else:
        generate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
        # generate(11, 12, 0.5, 1)
