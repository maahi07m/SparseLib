"""This script calculate the addition and subtraction of two matrices compressed in csr or csc format and return the
    results.
"""
import sys
from functools import singledispatch
sys.path.append('../')
from read_file.read_hb_format import read_file
try:
    from addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr,\
        addition_algorithm_csc, subtraction_algorithm_csc
    from addition_subtraction_numpy import *
except ImportError:
    from .addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr,\
        addition_algorithm_csc, subtraction_algorithm_csc
    from .addition_subtraction_numpy import *


@singledispatch
def csr_addition_matrices(matrix_1: list, matrix_2: list):
    """
    :param matrix_1: list of lists
    :param matrix_2: list of lists
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices.register
def _csr_addition_matrices(file_name_1: str, file_name_2: str, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name_1: string
    :param file_name_2: string
    :param processes_number: int
    :param file_path: string
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(file_name_1, processes_number, file_path)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2, processes_number, file_path)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@csr_addition_matrices.register
def _csr_addition_matrices(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                           matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int,
                           processes_number=mp.cpu_count(), file_path='../'):
    """
    :param matrix_size_row_1: int
    :param matrix_size_col_1: int
    :param matrix_size_row_2: int
    :param matrix_size_col_2: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    :param processes_number: int
    :param file_path: string
    :return: the result of the addition of tow matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1, processes_number, file_path)
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2 and file_id_1 == file_id_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2, processes_number, file_path)
    return addition_algorithm_csr(ar, ia, ja, br, ib, jb)


@singledispatch
def csr_subtraction_matrices(matrix_1: list, matrix_2: list):
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


@csr_subtraction_matrices.register
def _csr_subtraction_matrices(file_name_1: str, file_name_2: str):
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


@csr_subtraction_matrices.register
def _csr_subtraction_matrices(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
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
@csr_subtraction_matrices.register
def _csr_subtraction_matrices(is_hb: bool, matrix: list, file_name: str):
    ar, ia, ja = csr(matrix)
    br, ib, jb = ar, ia, ja
    start_time = time.time()
    cr, ic, jc = subtraction_algorithm_csr(ar, ia, ja, br, ib, jb)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
        f.write('subtraction_csr\t%s\t%.5f\n' % (file_name, total_time))
    return cr, ic, jc


@singledispatch
def csc_addition_matrices(matrix_1: list, matrix_2: list):
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


@csc_addition_matrices.register
def _csc_addition_matrices(file_name_1: str, file_name_2: str):
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


@csc_addition_matrices.register
def _csc_addition_matrices(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
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
@csc_addition_matrices.register
def _csc_addition_matrices(is_hb: bool, matrix: list, file_name: str):
    ar, ia, ja = csc(matrix)
    br, ib, jb = ar, ia, ja
    start_time = time.time()
    cr, ic, jc = addition_algorithm_csc(ar, ia, ja, br, ib, jb)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
        f.write('addition_csc\t%s\t%.5f\n' % (file_name, total_time))
    return cr, ic, jc


@singledispatch
def csc_subtraction_matrices(matrix_1: list, matrix_2: list):
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


@csc_subtraction_matrices.register
def _csc_subtraction_matrices(file_name_1: str, file_name_2: str):
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


@csc_subtraction_matrices.register
def _csc_subtraction_matrices(matrix_size_row: int, matrix_size_col: int, density: float, file_id_1: int,
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
@csc_subtraction_matrices.register
def _csc_subtraction_matrices(is_hb: bool, matrix: list, file_name: str):
    ar, ia, ja = csc(matrix)
    br, ib, jb = ar, ia, ja
    start_time = time.time()
    cr, ic, jc = subtraction_algorithm_csc(ar, ia, ja, br, ib, jb)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
        f.write('subtraction_csc\t%s\t%.5f\n' % (file_name, total_time))
    return cr, ic, jc


def main():
    try:
        matrix = read_file(file_name=sys.argv[1], return_list=True)
        # matrix = read_matrix_parallel(file_name=sys.argv[1])

        for _ in range(10):
            ar, ia, ja = csr_addition_matrices(True, matrix, sys.argv[1])
            npr, inp, jnp = addition_matrices_numpy_csr(matrix, sys.argv[1])
            validate_operation(ar, ia, ja, npr, inp, jnp, sys.argv[1], 'addition_csr')

            ar, ia, ja = csr_subtraction_matrices(True, matrix, sys.argv[1])
            npr, inp, jnp = subtraction_matrices_numpy_csr(matrix, sys.argv[1])
            validate_operation(ar, ia, ja, npr, inp, jnp, sys.argv[1], 'subtraction_csr')

            ar, ia, ja = csc_addition_matrices(True, matrix, sys.argv[1])
            npr, inp, jnp = addition_matrices_numpy_csc(matrix, sys.argv[1])
            validate_operation(ar, ia, ja, npr, inp, jnp, sys.argv[1], 'addition_csc')

            ar, ia, ja = csc_subtraction_matrices(True, matrix, sys.argv[1])
            npr, inp, jnp = subtraction_matrices_numpy_csc(matrix, sys.argv[1])
            validate_operation(ar, ia, ja, npr, inp, jnp, sys.argv[1], 'subtraction_csc')
    except TypeError:
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
            f.write('Wrong_file_format\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
            f.write('Wrong_file_format\t%s\n' % sys.argv[1])

    except NotImplementedError:
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
            f.write('No_supported_format!\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
            f.write('No_supported_format\t%s\n' % sys.argv[1])

    except ValueError:
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_time.txt'), 'a') as f:
            f.write('ValueError_sto\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'add_sub_hb_numpy_time.txt'), 'a') as f:
            f.write('ValueError_sto\t%s\n' % sys.argv[1])


if __name__ == '__main__':
    main()
