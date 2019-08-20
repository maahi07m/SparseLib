import multiprocessing as mp
import os
import time

import numpy as np
from scipy.sparse import random


def __generate_matrix(lb, ub, m, n, dens):
    """
    :param lb: int
    :param ub: int
    :param m: int
    :param n: int
    :param dens: float
    :return: sparse matrix

    Generate a sparse matrix mxn with lower bound (lb) and upper bound (ub)
    """
    np.random.seed(int(time.time()))
    temp_matrix = random(m, n, format='csr', density=dens)
    generated_matrix = np.round((ub - lb + 1) * temp_matrix + lb * temp_matrix.ceil())
    return generated_matrix


def __write_matrix_to_file(first_dimension, second_dimension, density, file_id, matrix, file_path):
    """
    :param first_dimension: int
    :param second_dimension: int
    :param density: float
    :param file_id: int
    :param matrix: list
    :param file_path: string
    :return: -

    Store in data files a txt file containing the generated matrix mxn with name e.g. "output_1000_1000_0.005_1.txt"
    """
    file_name = 'output_' + first_dimension + '_' + second_dimension + '_' + density + '_' + file_id + '.txt'
    matrix = matrix.toarray()
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    if not os.path.exists(file_path + 'data_files'):
        os.makedirs(file_path + 'data_files')
    with open(os.path.join(file_path + 'data_files', file_name), 'w') as f:
        f.write(data_to_write)


def __prepare_matrix(line):
    """
    :param line: list
    :return: a string containing matrix's entries
    """
    data_to_write = ''
    for index, inner in enumerate(line):
        if index == line.shape[0] - 1:
            data_to_write += str(int(inner))
        else:
            data_to_write += ("%s\t" % str(int(inner)))
    data_to_write += "\n"
    return data_to_write
