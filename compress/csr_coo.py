"""To run: python3 csr_coo.py <algorithm name> <size of rows> <size of cols> <density> <file_id>"""
import sys
import multiprocessing as mp
from functools import singledispatch
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
try:
    from csr_coo_algorithm import csr_algorithm, coo_algorithm
except ImportError:
    from .csr_coo_algorithm import csr_algorithm, coo_algorithm


@singledispatch
def csr(matrix: list):
    """
    :param matrix: list of lists
    ----------------------
    Convert a matrix 1-d, 2-d to csr format parallel
    ----------------------
    :return: three vectors, the user gives a list of lists and take back the matrix stored in csr format
    """
    return csr_algorithm(matrix)


@csr.register
def _csr(file_name: str, number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param number_process: int
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to csr format parallel
    ----------------------
    :return: three vectors, the user gives a string-file_name and take back the matrix stored in csr format
    """
    matrix = read_matrix_parallel(file_name, number_process=number_process, file_path=file_path)
    return csr_algorithm(matrix)


@csr.register
def _csr(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int,
         number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_id: int
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to csr format parallel
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains the number of non zero values in a line (always the first element is 0 and the last one
             the number of rows + 1), the third contains pointers of rows for the AR values, the user gives the
             dimensions, density and file_id of the matrix
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    file_matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density,
                                       number_process=number_process, file_path=file_path)
    return csr_algorithm(file_matrix)


@singledispatch
def coo(matrix: list):
    """
    :param matrix: list of lists
    ----------------------
    Convert a matrix 1-d, 2-d to coo format parallel
    ----------------------
    :return: three vectors, the user gives a list of lists and take back the matrix stored in coo format
    """
    return coo_algorithm(matrix)


@coo.register
def _coo(file_name: str, number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param number_process: int
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to coo format parallel
    ----------------------
    :return: three vectors, the user gives a string-file_name and take back the matrix stored in coo format
    """
    matrix = read_matrix_parallel(file_name, number_process=number_process, file_path=file_path)
    return coo_algorithm(matrix)


@coo.register
def _coo(matrix_size_row: int, matrix_size_col: int, density: float, file_id: int,
         number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_id: int
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to coo format parallel
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains pointers of rows for the AR values, the third contains pointers of cols for the AR
             values, the user gives the dimensions, density and file_id of the matrix
    """

    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    file_matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density,
                                       number_process=number_process, file_path=file_path)
    return coo_algorithm(file_matrix)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        if sys.argv[1].lower() == 'csr':
            AR1, IA1, JA1 = csr(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]))
            AR2, IA2, JA2 = csr('output_10_10_0.05_1.txt')
            AR3, IA3, JA3 = csr(read_matrix_parallel('output_10_10_0.05_1.txt'))
            if AR3==AR1 and AR1==AR2:
                print('ok')
            if IA3==IA1 and IA1==IA2:
                print('ok')
            if JA1==JA2 and JA3==JA2:
                print('ok')
        elif sys.argv[1].lower() == 'coo':
            AR1, IA1, JA1 = coo(int(sys.argv[2]), int(sys.argv[3]), float(sys.argv[4]), int(sys.argv[5]))
            AR2, IA2, JA2 = coo('output_10_10_0.05_1.txt')
            AR3, IA3, JA3 = coo(read_matrix_parallel('output_10_10_0.05_1.txt'))
            if AR3 == AR1 and AR1 == AR2:
                print('ok')
            if IA3 == IA1 and IA1 == IA2:
                print('ok')
            if JA1 == JA2 and JA3 == JA2:
                print('ok')
    elif len(sys.argv) == 5:
        AR1, IA1, JA1 = csr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        AR2, IA2, JA2 = coo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
    else:
        raise UserWarning(
            'Probably wrong input. Expected <algorithm name> <size of rows> <size of cols> <density> <file_id>')
