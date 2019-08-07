"""This script calculate the addition and subtraction of two matrices compressed in csr or csc format and stored the
    results in a file.
    To run: python3 addition_subtraction.py <operation_type> <algorithm name> <size of rows> <size of cols> <density>
    <file_id_1> <file_id_2>
    or
    To run: python3 addition_subtraction.py <size of rows> <size of cols> <density> <file_id_1> <file_id_2>
"""
import os
import sys
import time

try:
    from addition_subtraction_numpy import addition_matrices_numpy_csr, subtraction_matrices_numpy_csc, \
        addition_matrices_numpy_csc, subtraction_matrices_numpy_csr, validate_operation

except ImportError:
    from .addition_subtraction_numpy import addition_matrices_numpy_csr, subtraction_matrices_numpy_csc, \
        addition_matrices_numpy_csc, subtraction_matrices_numpy_csr, validate_operation
sys.path.append('../')
from compress.csr_coo import csr
from compress.diagonal_csc import csc


def csr_addition_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the addition of two matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [0], []
    start_time = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(ia)):  # len(ia) = len(ib)
        a_row_number = ia[row_index] - ia[row_index - 1]  # get A's row number
        b_row_number = ib[row_index] - ib[row_index - 1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = ja[a_previous_row_index: new_a_row_index]
        b_columns = jb[b_previous_row_index: new_b_row_index]
        a_values = ar[a_previous_row_index: new_a_row_index]
        b_values = br[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns + b_columns))
        for index in all_columns:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                jc.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(b_values[b_value_index])
                jc.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] + b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    jc.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        ic.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('addition_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return cr, ic, jc


def csr_subtraction_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id_1: int
    :param file_id_2: int
    ----------------------
    :return: the result of the subtraction of two matrices stored in csr format
    """
    ar, ia, ja = csr(matrix_size_row, matrix_size_col, density, file_id_1)
    br, ib, jb = csr(matrix_size_row, matrix_size_col, density, file_id_2)
    cr, ic, jc = [], [0], []
    start_time = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(ia)):  # len(ia) = len(ib)
        a_row_number = ia[row_index] - ia[row_index - 1]  # get A's row number
        b_row_number = ib[row_index] - ib[row_index - 1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = ja[a_previous_row_index: new_a_row_index]
        b_columns = jb[b_previous_row_index: new_b_row_index]
        a_values = ar[a_previous_row_index: new_a_row_index]
        b_values = br[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns).union(b_columns))
        for index in all_columns:
            if index in distinct_a:
                cr.append(a_values[a_value_index])
                jc.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                cr.append(-b_values[b_value_index])
                jc.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] - b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    cr.append(new_value)
                    jc.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        ic.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    total_time = time.time() - start_time
    if not os.path.exists('../execution_results'):
        os.makedirs('../execution_results')
    with open(os.path.join('../execution_results', 'add_sub_time.txt'), 'a') as f:
        f.write('subtraction_csr %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return cr, ic, jc
    # return [], [], []


def csc_addition_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
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


def csc_subtraction_matrices_nxn(matrix_size_row, matrix_size_col, density, file_id_1, file_id_2):
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


def main():
    if len(sys.argv) == 7:
        if sys.argv[1].lower() == 'addition' and sys.argv[2] == 'csr':
            npr, inp, jnp = addition_matrices_numpy_csr(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
            csr_ar, csr_ia, csr_ja = csr_addition_matrices_nxn(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                               sys.argv[7])
            validate_operation(csr_ar, csr_ia, csr_ja, npr, inp, jnp, sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], sys.argv[7], 'addition')

        elif sys.argv[1].lower() == 'addition' and sys.argv[2] == 'csc':
            npr, inp, jnp = addition_matrices_numpy_csc(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
            csc_ar, csc_ia, csc_ja = csc_addition_matrices_nxn(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                               sys.argv[7])
            validate_operation(csc_ar, csc_ia, csc_ja, npr, inp, jnp, sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], sys.argv[7], 'addition')

        elif sys.argv[1].lower() == 'subtraction' and sys.argv[2] == 'csr':
            npr, inp, jnp = subtraction_matrices_numpy_csr(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                           sys.argv[7])
            csr_ar, csr_ia, csr_ja = csr_subtraction_matrices_nxn(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                                  sys.argv[7])
            validate_operation(csr_ar, csr_ia, csr_ja, npr, inp, jnp, sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], sys.argv[7], 'addition')

        elif sys.argv[1].lower() == 'subtraction' and sys.argv[2] == 'csc':
            npr, inp, jnp = subtraction_matrices_numpy_csc(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                           sys.argv[7])
            csc_ar, csc_ia, csc_ja = csc_subtraction_matrices_nxn(sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6],
                                                                  sys.argv[7])
            validate_operation(csc_ar, csc_ia, csc_ja, npr, inp, jnp, sys.argv[3], sys.argv[4], sys.argv[5],
                               sys.argv[6], sys.argv[7], 'addition')

    elif len(sys.argv) == 6:
        npr, inp, jnp = addition_matrices_numpy_csr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        csr_ar, csr_ia, csr_ja = csr_addition_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                           sys.argv[5])
        validate_operation(csr_ar, csr_ia, csr_ja, npr, inp, jnp, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'addition')

        npr, inp, jnp = subtraction_matrices_numpy_csr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        csr_ar, csr_ia, csr_ja = csr_subtraction_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                              sys.argv[5])
        validate_operation(csr_ar, csr_ia, csr_ja, npr, inp, jnp, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'subtraction')

        npr, inp, jnp = addition_matrices_numpy_csc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        csc_ar, csc_ia, csc_ja = csc_addition_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                           sys.argv[5])
        validate_operation(csc_ar, csc_ia, csc_ja, npr, inp, jnp, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'addition')

        npr, inp, jnp = subtraction_matrices_numpy_csc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
        csr_ar, csr_ia, csr_ja = csc_subtraction_matrices_nxn(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                                                              sys.argv[5])
        validate_operation(csr_ar, csr_ia, csr_ja, npr, inp, jnp, sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4],
                           sys.argv[5], 'subtraction')
    else:
        print("There is no main to run")


if __name__ == '__main__':
    main()
