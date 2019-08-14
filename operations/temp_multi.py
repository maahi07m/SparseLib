""" This script contains all the multiplies of matrices inner, outer, matrix-vector, vector-matrix, matrix-matrix """
import sys
from functools import singledispatch

sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel
from helpers.generator import generate_sparse_matrix
from read_file.read_hb_format import read_file

try:
    from multiplication_algorithm import *
    from temp_multi_numpy import *
except ImportError:
    from .multiplication_algorithm import *
    from .temp_multi_numpy import *


# TODO: correct warning messages


@singledispatch
def inner_product(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2) and all(len(value) == 1 for value in matrix_1) and \
            all(len(value) == 2 for value in matrix_2):
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csr(matrix_2)

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@inner_product.register
def _inner_product(file_name_1: str, file_name_2: str):
    ar, ia, ja = csr(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)

    if len(ia) == len(ib):
        if not all(value == 0 for value in ja):
            raise UserWarning(
                'Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')

        if not all(value == 0 for value in jb):
            raise UserWarning(
                'Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@inner_product.register
def _inner_product(matrix_size_row_1: int, matrix_size_col_1: int, density: float, file_id_1: int,
                   matrix_size_row_2: int, matrix_size_col_2: int, file_id_2: int):
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        if matrix_size_row_1 == matrix_size_row_2 and file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return inner_algorithm(ar, ia, br, ib)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@singledispatch
def outer_product(matrix_1: list, matrix_2: list):
    if len(matrix_1) == len(matrix_2) and len(matrix_1) == 1 and len(matrix_1[0]) == len(matrix_2[0]):
        ar, ia, ja = csc(matrix_1)
        if matrix_1 == matrix_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_2)

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@outer_product.register
def _outer_product(file_name_1: str, file_name_2: str):
    ar, ia, ja = csc(file_name_1)
    if file_name_2 == file_name_1:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(file_name_2)

    if len(ja) == len(jb):
        if not all(value == 0 for value in ia):
            raise UserWarning(
                'Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')

        if not all(value == 0 for value in ib):
            raise UserWarning(
                'Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@outer_product.register
def _outer_product(matrix_size_row_1: int, matrix_size_col_1: int, density: float, file_id_1: int,
                   matrix_size_row_2: int, matrix_size_col_2: int, file_id_2: int):
    if matrix_size_row_1 == matrix_size_row_2 and matrix_size_col_1 == matrix_size_col_2:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        if matrix_size_row_1 == matrix_size_row_2 and file_id_1 == file_id_2:
            br, ib, jb = ar, ia, ja
        else:
            br, ib, jb = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return outer_algorithm(ar, ja, br, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_row_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_1> and <matrix_size_col_2> to be equal too')


@singledispatch
def multiply_matrix_vector(matrix_1: list, matrix_2: list):
    matrix_1_col_size = len(matrix_1[0])
    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(len(row) == 1 for row in matrix_2) and \
            matrix_1_col_size == len(matrix_2):
        ar, ia, ja = csr(matrix_1)
        xr, ix, jx = csc(matrix_2)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_matrix_vector.register
def _multiply_matrix_vector(file_name_1: str, file_name_2: str):
    matrix_1 = read_matrix_parallel(file_name_1)
    matrix_2 = read_matrix_parallel(file_name_2)
    matrix_1_col_size = len(matrix_1[0])

    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(len(row) == 1 for row in matrix_2) and \
            matrix_1_col_size == len(matrix_2):
        ar, ia, ja = csr(matrix_1)
        xr, ix, jx = csc(matrix_2)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_matrix_vector.register
def _multiply_matrix_vector(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                            matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int):
    if matrix_size_col_1 == matrix_size_row_2 and matrix_size_col_2 == 1:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        xr, ix, jx = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return matrix_vector_algorithm(ar, ia, ja, xr, ix)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


# function for hb experiments
@multiply_matrix_vector.register
def _multiply_matrix_vector(is_hd: bool, matrix: list, file_name: str, density: float):
    # elegxoume oti oles oi grammes exoun to idio length
    matrix_col_size = len(matrix[0])
    if not all(len(row) == matrix_col_size for row in matrix):
        raise ReferenceError("den ine oles oi grammes ises se mikos")

    ar, ia, ja = csr(matrix)
    vector = generate_sparse_matrix(matrix_col_size, 1, density, return_list=True)
    xr, ix, jx = csc(vector)
    start_time = time.time()
    cr, ic, jc = matrix_vector_algorithm(ar, ia, ja, xr, ix)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
        f.write('matrix_vector\t%s\t%.5f\n' % (file_name, total_time))
    return cr, ic, jc, vector


@singledispatch
def multiply_vector_matrix(matrix_1: list, matrix_2: list):
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    if len(matrix_2) == 1 and len(matrix_1) == matrix_2_col_size and \
            all(len(row) == matrix_1_col_size for row in matrix_1):

        ar, ia, ja = csc(matrix_1)
        xr, ix, jx = csr(matrix_2)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_vector_matrix.register
def _multiply_vector_matrix(file_name_1: str, file_name_2: str):
    matrix_1 = read_matrix_parallel(file_name_1)
    matrix_2 = read_matrix_parallel(file_name_2)
    matrix_1_col_size = len(matrix_1[0])  # m
    matrix_2_col_size = len(matrix_2[0])  # n

    # if to x exi mia grammi kai oi grammes tou matrix_1 ine ises me tis stiles tou matrix_2 (n) kai oles oi grammes
    # tous matrix_1 ine mikous m
    if len(matrix_2) == 1 and len(matrix_1) == matrix_2_col_size and \
            all(len(row) == matrix_1_col_size for row in matrix_1):

        ar, ia, ja = csc(matrix_1)
        xr, ix, jx = csr(matrix_2)
        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@multiply_vector_matrix.register
def _multiply_vector_matrix(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                            matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int):
    if matrix_size_row_1 == matrix_size_col_2 and matrix_size_row_2 == 1:
        ar, ia, ja = csc(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        xr, ix, jx = csr(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return vector_matrix_algorithm(ar, ia, ja, xr, jx)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


# function for hb experiments
@multiply_vector_matrix.register
def _multiply_vector_matrix(is_hb: bool, matrix: list, file_name: str, density: float):
    matrix_col_size = len(matrix[0])
    if not all(len(row) == matrix_col_size for row in matrix):
        raise ReferenceError("den ine oles oi grammes ises se mikos")

    ar, ia, ja = csc(matrix)
    vector = generate_sparse_matrix(1, len(matrix), density, return_list=True)
    xr, ix, jx = csr(vector)
    start_time = time.time()
    cr, ic, jc = vector_matrix_algorithm(ar, ia, ja, xr, jx)
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
        f.write('vector_matrix\t%s\t%.5f\n' % (file_name, total_time))
    return cr, ic, jc, vector


@singledispatch
def matrix_matrix_multiplication(matrix_1: list, matrix_2: list):
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    matrix_2_row_size = len(matrix_2)

    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(
            len(row) == matrix_2_col_size for row in matrix_2) and matrix_1_col_size == matrix_2_row_size:
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)
        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@matrix_matrix_multiplication.register
def _matrix_matrix_multiplication(file_name_1: str, file_name_2: str):
    matrix_1 = read_matrix_parallel(file_name_1)
    matrix_2 = read_matrix_parallel(file_name_2)
    matrix_1_col_size = len(matrix_1[0])
    matrix_2_col_size = len(matrix_2[0])
    matrix_2_row_size = len(matrix_2)

    if all(len(row) == matrix_1_col_size for row in matrix_1) and all(
            len(row) == matrix_2_col_size for row in matrix_2) and matrix_1_col_size == matrix_2_row_size:
        ar, ia, ja = csr(matrix_1)
        br, ib, jb = csc(matrix_2)
        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


@matrix_matrix_multiplication.register
def _matrix_matrix_multiplication(matrix_size_row_1: int, matrix_size_col_1: int, matrix_size_row_2: int,
                                  matrix_size_col_2: int, density: float, file_id_1: int, file_id_2: int):
    if matrix_size_col_1 == matrix_size_row_2:
        ar, ia, ja = csr(matrix_size_row_1, matrix_size_col_1, density, file_id_1)
        br, ib, jb = csc(matrix_size_row_2, matrix_size_col_2, density, file_id_2)

        return matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
    else:
        raise UserWarning('Probably wrong input. Expected <matrix_size_col_1> and <matrix_size_row_2> to be equal and '
                          '<matrix_size_col_2> to be equal with 1')


# function for hb experiments
@matrix_matrix_multiplication.register
def _matrix_matrix_multiplication(is_hd: bool, matrix: list, file_name: str):
    matrix_col_size = len(matrix[0])
    if not all(len(row) == matrix_col_size for row in matrix):
        raise ReferenceError("den ine oles oi grammes ises se mikos")

    if matrix_col_size != len(matrix):
        return [], [], []
    else:
        ar, ia, ja = csr(matrix)
        br, ib, jb = csc(matrix)
        start_time = time.time()
        cr, ic, jc = matrix_matrix_algorithm(ar, ia, ja, br, ib, jb)
        total_time = time.time() - start_time
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
            f.write('matrix_matrix\t%s\t%.5f\n' % (file_name, total_time))
        return cr, ic, jc


def main():
    file_name = sys.argv[1]
    # file_name = "bcsstk08.rsa"
    # file_name = 'output_10_10_0.5_1.txt'
    try:
        matrix = read_file(file_name=file_name, return_list=True)
        # matrix = read_matrix_parallel(file_name=file_name)
        for _ in range(10):
            for density in [0.005, 0.01, 0.02]:

                ar, ia, ja, vector = multiply_matrix_vector(True, matrix, file_name, density)
                vector = [item for item in vector]
                npr, inp, jnp = numpy_matrix_vector(matrix, vector, file_name, density)
                validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'matrix_vector')

                ar, ia, ja, vector = multiply_vector_matrix(True, matrix, file_name, density)
                vector = [item for item in vector]
                npr, inp, jnp = numpy_vector_matrix(matrix, vector, file_name, density)
                validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'vector_matrix')

                ar, ia, ja = matrix_matrix_multiplication(True, matrix, file_name)
                if ar == [] and ia == [] and ja == []:
                    continue
                npr, inp, jnp = numpy_matrix_matrix(matrix, file_name, density)
                # print(ar)
                # print(ia)
                # print(ja)
                # print("-"*100)
                # print(npr)
                # print(inp)
                # print(jnp)
                validate_operation(ar, ia, ja, npr, inp, jnp, file_name, density, 'matrix_matrix')

    except TypeError as err:
        print("TypeError error: {0}".format(err))
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
            f.write('Wrong_file_format\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
            f.write('Wrong_file_format\t%s\n' % sys.argv[1])

    except NotImplementedError:
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
            f.write('No_supported_format!\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
            f.write('No_supported_format\t%s\n' % sys.argv[1])

    except ValueError as err:
        print("ValueError error: {0}".format(err))
        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_time.txt'), 'a') as f:
            f.write('ValueError_sto\t%s\n' % sys.argv[1])

        if not os.path.exists('../execution_results'):
            os.makedirs('../execution_results')
        with open(os.path.join('../execution_results', 'multiplication_hb_numpy_time.txt'), 'a') as f:
            f.write('ValueError_sto\t%s\n' % sys.argv[1])


if __name__ == '__main__':
    main()
