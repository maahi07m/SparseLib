"""
    This script was created only for the execution of our experiments on Harwell-Boeing formatted files
"""
import os
import sys
import time

import numpy as np
import scipy.sparse as sp

sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc


def validate_operation(cr, ic, jc, npr, inp, jnp, file_name, density, operation_type):
    if all(np.isclose(cr, npr)) and all(np.isclose(ic, inp)) and all(np.isclose(jc, jnp)):
        pass
    else:
        with open(os.path.join('../operation_error', 'multiplication_hb_numpy_error.txt'), 'a') as f:
            f.write(operation_type + '_\t%s\t%.5f\n' % (file_name, density))


def numpy_matrix_vector(matrix, vector, file_name, density):
    a_matrix = np.array(matrix)
    b_matrix = np.array(vector)
    start_time = time.time()
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
        f.write('matrix_vector_numpy\t%s\t%.5f\t%.5f\n' % (file_name, density, total_time))

    return csc(result)


def numpy_vector_matrix(matrix, vector, file_name, density):
    a_matrix = np.array(matrix)
    b_matrix = np.array(vector)
    start_time = time.time()
    result = b_matrix.dot(a_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
        f.write('vector_matrix_numpy\t%s\t%.5f\t%.5f\n' % (file_name, density, total_time))

    return csr(result)


def numpy_matrix_matrix(matrix, file_name, density):
    start_time = time.time()
    a_matrix = sp.csr_matrix(np.array(matrix))
    b_matrix = np.array(matrix)
    result = a_matrix.dot(b_matrix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
        f.write('matrix_matrix_numpy\t%s\t%.5f\t%.5f\n' % (file_name, density, total_time))

    return csr(result)
