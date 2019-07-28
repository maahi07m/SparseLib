import time
import sys
import scipy.sparse as sp
import numpy as np
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


def outer_product_numpy(file_1, file_2):
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    C = np.outer(A, B)
    print("numpy : ", C)


def numpy_matrix_matrix(file_1, file_2):
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
    print('time', time.time() - start_time)

    print(result)


def numpy_matrix_vector(file_1, file_2):
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = np.array(A)
    B = np.array(B)
    start = time.time()
    C = A.dot(B)
    print('time numpy', time.time() - start)

    return C


def inner_product_numpy(file_1, file_2):
    A = read_matrix_parallel(file_1)
    A = np.transpose(A)
    B = read_matrix_parallel(file_2)
    start = time.time()
    C = np.dot(A, B)
    print("numpy : ", time.time()- start)


if __name__ == '__main__':
    inner_product_numpy()
    outer_product_numpy()
    numpy_matrix_matrix()
    numpy_matrix_vector()

