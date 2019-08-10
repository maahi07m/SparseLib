import sys
from functools import singledispatch
sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc
from read_file.matrix_read import read_matrix_parallel
from read_file.read_hb_format import read_file
try:
    from addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr,\
        addition_algorithm_csc, subtraction_algorithm_csc
except ImportError:
    from .addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr,\
        addition_algorithm_csc, subtraction_algorithm_csc


@singledispatch
def csr_addition_matrices_nxn(matrix_1: list, matrix_2: list):
    """
    :param matrix_1: list of lists
    :param matrix_2: list of lists
    ----------------------
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices_nxn.register
def _csr_addition_matrices_nxn(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    ----------------------
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices_nxn.register
def _csr_addition_matrices_nxn(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
                               file_id_2: int):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)

# function for hb experiments
@csr_addition_matrices_nxn.register
def _csr_addition_matrices_nxn(is_hb: bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csr(matrix)
    br, ib, jb = ar, ia, ja
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@singledispatch
def csr_subtraction_matrices_nxn(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   ----------------------
   :return: the result of the subtraction of tow matrices stored in csr format
   """
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)
    return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_subtraction_matrices_nxn.register
def _csr_subtraction_matrices_nxn(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    ----------------------
    :return: the result of the subtraction of tow matrices stored in csr format
    """
    ar, ia, ja = csr(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)
    return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_subtraction_matrices_nxn.register
def _csr_subtraction_matrices_nxn(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
                                  file_id_2: int):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction of tow matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)

# function for hb experiments
@csr_subtraction_matrices_nxn.register
def _csr_subtraction_matrices_nxn(is_hb: bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csr(matrix)
    br, ib, jb = ar, ia, ja
    return subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)


@singledispatch
def csc_addition_matrices_nxn(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   ----------------------
   :return: the result of the addition of tow matrices stored in csc format
   """
    ar, ia, ja = csc(matrix_1)
    if matrix_2 == matrix_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(matrix_2)
    return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_addition_matrices_nxn.register
def _csc_addition_matrices_nxn(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    ----------------------
    :return: the result of the addition of tow matrices stored in csc format
    """
    ar, ia, ja = csc(file_name_1)
    if file_name_1 == file_name_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(file_name_2)
    return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_addition_matrices_nxn.register
def _csc_addition_matrices_nxn(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
                               file_id_2: int):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the addition of tow matrices stored in csc format
    """
    ar, ia, ja = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csc(matrix_size_row, matrix_size_col, density, file_id_2)
    return addition_algorithm_csc(ar, ia, ja, br, ib, jb)

# function for hb experiments
@csc_addition_matrices_nxn.register
def _csc_addition_matrices_nxn(is_hb: bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csc(matrix)
    br, ib, jb = ar, ia, ja
    return addition_algorithm_csc(ar, ia, ja, br, ib, jb)


@singledispatch
def csc_subtraction_matrices_nxn(matrix_1: list, matrix_2: list):
    """
   :param matrix_1: list of lists
   :param matrix_2: list of lists
   ----------------------
   :return: the result of the subtraction of tow matrices stored in csc format
   """
    ar, ia, ja = csc(matrix_1)
    if matrix_2 == matrix_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(matrix_2)
    return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_subtraction_matrices_nxn.register
def _csc_subtraction_matrices_nxn(file_name_1: str, file_name_2: str):
    """
    :param file_name_1: string
    :param file_name_2: string
    ----------------------
    :return: the result of the subtraction of tow matrices stored in csc format
    """
    ar, ia, ja = csc(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csc(file_name_2)
    return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


@csc_subtraction_matrices_nxn.register
def _csc_subtraction_matrices_nxn(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
                                  file_id_2: int):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction of tow matrices stored in csc format
    """
    ar, ia, ja = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csc(matrix_size_row, matrix_size_col, density, file_id_2)
    return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)

# function for hb experiments
@csc_subtraction_matrices_nxn.register
def _csc_subtraction_matrices_nxn(is_hb: bool, file_name: str):
    matrix = read_file(file_name=file_name, return_list=True)
    ar, ia, ja = csc(matrix)
    br, ib, jb = ar, ia, ja
    return subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)


if __name__ == '__main__':
    AR1, IA1, JA1 = csr_addition_matrices_nxn(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
                                                 int(sys.argv[5]))
    AR2, IA2, JA2 = csr_addition_matrices_nxn('output_10_10_0.05_1.txt', 'output_10_10_0.05_1.txt')
    AR3, IA3, JA3 = csr_addition_matrices_nxn(read_matrix_parallel('output_10_10_0.05_1.txt'),
                                                 read_matrix_parallel('output_10_10_0.05_1.txt'))
    # if AR3 == AR1 and AR1 == AR2:
    #     print('ok')
    # if IA3 == IA1 and IA1 == IA2:
    #     print('ok')
    # if JA1 == JA2 and JA3 == JA2:
    #     print('ok')
    ar, ia, ja = csr_addition_matrices_nxn(True, 'bcsstk01.rsa')