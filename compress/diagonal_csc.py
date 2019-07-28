"""To run: python3 diagonal_csc.py <size of rows> <size of cols> <density> <file_id>"""
import time
import sys
import os
import numpy as np
# from helpers.profile import profile
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel, read_matrix_sequentially


# @profile
def diagonal(matrix_size_row, matrix_size_col, density, file_id, parallel=True, write_time=False, file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param write_time: boolean
    :param file_path: string
    ----------------------

    ----------------------
    :return: two lists AD, LA, the first one contains the non zero values, the second one contains pointers for each
    diagonal about the range from the main diagonal
    """
    global A
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + str(density) + '_' + str(file_id) + '.txt'
    if parallel:
        A = np.array(read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True, 4, file_path))
    else:
        A = np.array(read_matrix_sequentially(file_name, matrix_size_row, matrix_size_col, density))

    LA, AD = [], [[]]
    a_length = len(A)
    start_time = time.time()

    # main diagonal
    main_diagonal = get_main_diagonal(a_length)

    # upper diagonal
    upper_diagonals = []
    for index in range(1, a_length):
        AD.append([])  # start initializing AD array
        upper_inner_diagonal = get_upper_inner_diagonal(index, a_length)
        if upper_inner_diagonal:
            LA.append(index)
            upper_diagonals.append(upper_inner_diagonal)

    # lower diagonal
    lower_diagonals = []
    for index in range(a_length - 1, 0, -1):
        lower_inner_diagonal = get_lower_inner_diagonal(index, a_length)
        if lower_inner_diagonal:
            LA.append(-1 * index)
            lower_diagonals.append(lower_inner_diagonal)

    # create AD array
    AD = tuple(AD)  # tuple or list or numpy
    if main_diagonal:
        create_ad_with_main_diagonal(AD, main_diagonal, upper_diagonals, lower_diagonals, a_length)
    else:
        create_ad_without_main_diagonal(AD, upper_diagonals, lower_diagonals, a_length)

    if write_time:
        total_time = time.time() - start_time
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('Diagonal %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
        print("total time : ", total_time)

    return AD, LA


def create_ad_with_main_diagonal(AD, main_diagonal, upper_diagonals, lower_diagonals, a_length):
    row = 0
    uppers_number = len(upper_diagonals)
    lowers_number = len(lower_diagonals)

    while row < a_length:
        AD[row].append(main_diagonal[row])
        for index in range(uppers_number):
            AD[row].append(upper_diagonals[index][row])

        for index in range(lowers_number):
            AD[row].append(lower_diagonals[index][row])

        row += 1


def create_ad_without_main_diagonal(AD, upper_diagonals, lower_diagonals, a_length):
    row = 0
    uppers_number = len(upper_diagonals)
    lowers_number = len(lower_diagonals)

    while row < a_length:
        for index in range(uppers_number):
            AD[row].append(upper_diagonals[index][row])

        for index in range(lowers_number):
            AD[row].append(lower_diagonals[index][row])
        row += 1


def get_upper_inner_diagonal(col, a_length):
    found_nv = False
    temp_diagonal = []
    mine_row_index = 0
    for index in range(col, a_length):  # 0,5 1,6
        value = A[mine_row_index][index]
        if value != 0:
            found_nv = True
        temp_diagonal.append(value)
        mine_row_index += 1
        if mine_row_index == a_length:
            break

    if found_nv:
        left_zeros = a_length - len(temp_diagonal)
        for index in range(left_zeros):
            temp_diagonal.append(0)
        return temp_diagonal
    else:
        return []


def get_lower_inner_diagonal(row, a_length):
    found_nv = False
    temp_diagonal = []
    mine_col_index = 0
    for index in range(row, a_length):  # 6,1 5,2
        value = A[index][mine_col_index]
        if value != 0:
            found_nv = True
        temp_diagonal.append(value)
        mine_col_index += 1
        if mine_col_index == a_length:
            break

    if found_nv:
        left_zeros = a_length - len(temp_diagonal)
        return ([0] * left_zeros) + temp_diagonal
    else:
        return []


def get_main_diagonal(a_length):
    main_diagonal = []
    found_nv = False
    for index in range(a_length):
        value = A[index][index]
        if value != 0:
            found_nv = True
        main_diagonal.append(value)
    if found_nv:
        return main_diagonal
    else:
        return []


def csc(matrix_size_row, matrix_size_col, density, file_id, parallel=True, write_time=False, file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param write_time: boolean
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to csc format write the execution time in a txt file, if parallel the initial matrix will
    be read parallel otherwise sequentially
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zero values, the second one the row-pointers for
    each non zero value, the third one contains the number of non zero values in a line (always the first element is 0
    and the last one the number of rows + 1)
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + str(file_id) + '.txt'
    if parallel:
        A = np.array(read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True, 4, file_path))
    else:
        A = np.array(read_matrix_sequentially(file_name, matrix_size_row, matrix_size_col, density))
    start_time = time.time()
    AR, IA, JA = [], [], [0]
    ne_counter = 0
    A = np.transpose(A)
    for col, line in enumerate(A):
        for row, value in enumerate(line):
            if value != 0:
                AR.append(value)
                ne_counter += 1
                IA.append(row)

                if len(JA) == 0:
                    JA.append(col)
        JA.append(ne_counter)
    total_time = time.time() - start_time

    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('CSC %s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))

    return AR, IA, JA


if __name__ == '__main__':
    if len(sys.argv) == 6:
        if sys.argv[1].lower() == 'csc':
            AR, IA, JA = csc(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], True, True)
        elif sys.argv[1].lower() == 'diagonal':
            diagonal(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], True, True)
    elif len(sys.argv) == 5:
        AR, IA, JA = csc(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        diagonal(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
    else:
        print('There is no main to run')
