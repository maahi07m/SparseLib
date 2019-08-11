"""To run: python3 diagonal_csc.py <size of rows> <size of cols> <density> <file_id>"""
import multiprocessing as mp
import sys
from functools import singledispatch

import numpy as np

try:
    from diagonal_csc_algorithms import csc_algorithm, diagonal_algorithm
except ImportError:
    from .diagonal_csc_algorithms import csc_algorithm, diagonal_algorithm

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel, read_matrix_sequentially


@singledispatch
def diagonal(matrix: list):
    """
    :param matrix: list of lists
    ----------------------
    the user gives a list of lists
    ----------------------
    :return: two vectors, more specifically is the matrix stored in diagonal format
    """
    return diagonal_algorithm(np.array(matrix))


@diagonal.register
def _diagonal(file_name: str, parallel=True, number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param parallel: boolean
    :param number_process: int
    :param file_path: string
    ----------------------
    he user gives a string-file_name of the matrix
    ----------------------
    :return: two vectors, more specifically vectors represent the matrix stored in diagonal format
    """
    if parallel:
        matrix = np.array(read_matrix_parallel(file_name, number_process=number_process, file_path=file_path))
        return diagonal_algorithm(matrix)
    else:
        matrix = np.array(read_matrix_sequentially(file_name, file_path=file_path))
        return diagonal_algorithm(matrix)


@diagonal.register
def _diagonal(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int, parallel=True,
              number_process=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param file_path: string
    ----------------------
    Read and store files' non zeros diagonals
    ----------------------
    :return: two lists ad, la, the first one contains the non zero values, the second one contains pointers for each
    diagonal about the range from the main diagonal
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    if parallel:
        matrix = np.array(read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True,
                                               number_process=number_process, file_path=file_path))
        return diagonal_algorithm(matrix)
    else:
        matrix = np.array(read_matrix_sequentially(file_name, matrix_size_row, matrix_size_col, density, file_path))
        return diagonal_algorithm(matrix)


@singledispatch
def csc(matrix: list):
    """
    :param matrix: list of lists
    ---------------------
    the user gives a list of lists
    ---------------------
    :return: three vectors, the first contains the nz values, the second the number of nz values in each col and the
    third the pointers of row for every nz value
    """
    return csc_algorithm(np.array(matrix))


@csc.register
def _csc(file_name: str, parallel=True, number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param parallel: boolean
    :param number_process: int
    :param file_path: string
    ---------------------
    the user gives a string-file_name of the matrix
    ---------------------
    :return: three vectors, the first contains the nz values, the second the number of nz values in each col and the
    third the pointers of row for every nz value
    """
    if parallel:
        matrix = np.array(read_matrix_parallel(file_name, number_process=number_process, file_path=file_path))
        return csc_algorithm(matrix)
    else:
        matrix = np.array(read_matrix_sequentially(file_name, file_path=file_path))
        return csc_algorithm(matrix)


@csc.register
def _csc(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int, parallel=True, file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param file_path: string
    ----------------------
    the user gives dimensions, density and file_id of the txt file - matrix
    ----------------------
    :return: three lists ar, ia, ja, the first one contains the non zero values, the second one the row-pointers for
    each non zero value, the third one contains the number of non zero values in a line (always the first element is 0
    and the last one the number of rows + 1)
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    if parallel:
        file_matrix = np.array(read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True, 4,
                                                    file_path))
        return csc_algorithm(file_matrix)
    else:
        file_matrix = np.array(read_matrix_sequentially(file_name, matrix_size_row, matrix_size_col, density,
                                                        file_path))
        return csc_algorithm(file_matrix)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        if sys.argv[1].lower() == 'csc':
            AR, IA, JA = csc(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), True)
            AR1, IA1, JA1 = csc('output_10_10_0.05_1.txt')
            AR2, IA2, JA2 = csc(read_matrix_parallel('output_10_10_0.05_1.txt'))
        elif sys.argv[1].lower() == 'diagonal':
            AR, IA = diagonal(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]), True)
            AR1, IA1 = diagonal('output_10_10_0.05_1.txt')
            AR2, IA2 = diagonal(read_matrix_parallel('output_10_10_0.05_1.txt'))
            if AR==AR1 and AR1==AR2:
                print('ok')
            if IA==IA1 and IA1==IA2:
                print('ok')
    elif len(sys.argv) == 5:
        AR, IA, JA = csc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        diagonal(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
    else:
        raise UserWarning('Probably wrong input. Expected <size of rows> <size of cols> <density> <file_id>')
