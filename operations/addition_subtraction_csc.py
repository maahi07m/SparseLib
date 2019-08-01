"""This script calculate the addition and subtraction of two matrices and stored the results in csc format.
To run: python3 addition_subtraction_css.py <algorithm name> <size of rows> <size of cols> <density> <file_id_1> <file_id_2>
"""
import multiprocessing as mp
import os
import sys
import time

from numpy import array
from scipy.sparse import csc_matrix

sys.path.append('../')
from compress.diagonal_csc import csc
from read_file.matrix_read import read_matrix_parallel


def __prepare_matrix(line):
    data_to_write = ''
    for index, inner in enumerate(line):
        if index == line.shape[0] - 1:
            data_to_write += str(int(inner))
        else:
            data_to_write += ("%s\t" % str(int(inner)))
    data_to_write += "\n"
    return data_to_write


def write_np_table(matrix, file_name):
    number_process = mp.cpu_count()
    pool = mp.Pool(number_process)
    data_to_write = ''.join(pool.map(__prepare_matrix, matrix))
    pool.close()
    with open(os.path.join('../data_files', file_name), 'w') as f:
        f.write(data_to_write)


def validate_operation(cr, ic, jc, npr, inp, jnp, matrix_size_row, matrix_size_col, density, file_id_1, file_id_2,
                       operation_type):
    if cr == npr and ic == inp and jc == jnp:
        pass
    else:
        print("espase", matrix_size_row, matrix_size_col, file_id_1, file_id_2, density)
        with open(os.path.join('../operation_error', 'add_sub_operation_error_csc.txt'), 'a') as f:
            f.write(operation_type + '_csc\t%d\t%d\t%d\t%d\t%.5f\n' % (matrix_size_row, matrix_size_col, file_id_1,
                                                                       file_id_2, density))


def addition_matrices_numpy(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: result of the addition stored in numpy array format
    """
    file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_1) + '.txt'
    file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_2) + '.txt'
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = csc_matrix(array(a_matrix))
    b_matrix = csc_matrix(array(b_matrix))

    start_time = time.time()
    total = a_matrix + b_matrix
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
        f.write('addition_numpy_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    result_to_array = total.toarray()
    numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
                             + '20.txt'
    write_np_table(result_to_array, numpy_result_file_name)
    return csc(matrix_size_row, matrix_size_col, density, 20)


def subtraction_matrices_numpy(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
       :param matrix_size_row: int
       :param matrix_size_col: int
       :param density: float
       :param file_id_1: int
       :param file_id_2: int
       ----------------------
       :return: result of the subtraction stored in numpy array format
       """
    file_1 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_1) + '.txt'
    file_2 = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
             str(file_id_2) + '.txt'
    a_matrix = read_matrix_parallel(file_1)
    b_matrix = read_matrix_parallel(file_2)
    a_matrix = csc_matrix(array(a_matrix))
    b_matrix = csc_matrix(array(b_matrix))

    start_time = time.time()
    total = a_matrix - b_matrix
    total_time = time.time() - start_time

    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_numpy_time.txt'), 'a') as f:
        f.write('subtraction_numpy_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))

    result_to_array = total.toarray()
    numpy_result_file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' \
                             + '21.txt'
    write_np_table(result_to_array, numpy_result_file_name)
    return csc(matrix_size_row, matrix_size_col, density, 21)


def addition_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the addition of two matrices stored in csc format
    """
    ar, ia, ja = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csc(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [], [0]
    start_time = time.time()

    a_previous_col_index = 0
    b_previous_col_index = 0
    c_nz_counter = 0
    for col_index in range(1, len(ja)):  # len(ja) = len(jb)
        a_col_number = ja[col_index] - ja[col_index - 1]  # get A's row number
        b_col_number = jb[col_index] - jb[col_index - 1]  # get B's row number

        new_a_col_index = a_previous_col_index + a_col_number
        new_b_col_index = b_previous_col_index + b_col_number

        a_rows = ia[a_previous_col_index: new_a_col_index]
        b_rows = ib[b_previous_col_index: new_b_col_index]
        a_values = ar[a_previous_col_index: new_a_col_index]
        b_values = br[b_previous_col_index: new_b_col_index]

        a_value_index = 0
        b_value_index = 0
        common_rows = sorted(set(a_rows).intersection(b_rows))
        distinct_a = sorted(set(a_rows).difference(b_rows))
        distinct_b = sorted(set(b_rows).difference(a_rows))
        all_rows = sorted(set(a_rows).union(b_rows))
        for index in all_rows:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                ic.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(b_values[b_value_index])
                ic.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_rows:
                new_value = a_values[a_value_index] + b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    ic.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        jc.append(c_nz_counter)
        a_previous_col_index = new_a_col_index
        b_previous_col_index = new_b_col_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('addition_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return cr, ic, jc


def subtraction_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction of two matrices in csc format
    """
    ar, ia, ja = csc(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csc(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [], [0]
    start_time = time.time()

    a_previous_col_index = 0
    b_previous_col_index = 0
    c_nz_counter = 0
    for col_index in range(1, len(ja)):  # len(ja) = len(jb)
        a_col_number = ja[col_index] - ja[col_index - 1]
        b_col_number = jb[col_index] - jb[col_index - 1]

        new_a_col_index = a_previous_col_index + a_col_number
        new_b_col_index = b_previous_col_index + b_col_number

        a_rows = ia[a_previous_col_index: new_a_col_index]
        b_rows = ib[b_previous_col_index: new_b_col_index]
        a_values = ar[a_previous_col_index: new_a_col_index]
        b_values = br[b_previous_col_index: new_b_col_index]

        a_value_index = 0
        b_value_index = 0
        common_rows = sorted(set(a_rows).intersection(b_rows))
        distinct_a = sorted(set(a_rows).difference(b_rows))
        distinct_b = sorted(set(b_rows).difference(a_rows))
        all_rows = sorted(set(a_rows).union(b_rows))
        for index in all_rows:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                ic.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(-b_values[b_value_index])
                ic.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_rows:
                new_value = a_values[a_value_index] - b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    ic.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        jc.append(c_nz_counter)
        a_previous_col_index = new_a_col_index
        b_previous_col_index = new_b_col_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('subtraction_csc %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return cr, ic, jc


if __name__ == '__main__':
    if len(sys.argv) == 7:
        if sys.argv[1].lower() == 'addition':
            npr, inp, jnp = addition_matrices_numpy(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            AR1, IA1, JA1 = addition_matrices_nxn(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

            validate_operation(AR1, IA1, JA1, npr, inp, jnp, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], 'addition')
            
        elif sys.argv[1].lower() == 'subtraction':
            npr, inp, jnp = subtraction_matrices_numpy(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
            AR2, IA2, JA2 = subtraction_matrices_nxn(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])

            validate_operation(AR2, IA2, JA2, npr, inp, jnp, sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], 'subtraction')
    elif len(sys.argv) == 6:
        npr, inp, jnp = addition_matrices_numpy(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        AR1, IA1, JA1 = addition_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        validate_operation(AR1, IA1, JA1, npr, inp, jnp, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'addition')

        npr2, inp2, jnp2 = subtraction_matrices_numpy(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        AR2, IA2, JA2 = subtraction_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        validate_operation(AR2, IA2, JA2, npr2, inp2, jnp2, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'subtraction')
    else:
        print("There is no main to run")
