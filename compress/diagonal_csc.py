"""To run: python3 diagonal_csc.py <size> <density> <file_id>"""
import time
import sys
import os
import numpy as np
# from helpers.profile import profile
sys.path.append('../')
from read_file.matrix_read import read_matrix_parallel


# @profile
def diagonal(write_time=False, matrix_size='-', density='-', file_path='../'):
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
            f.write('Diagonal %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
        print("total time : ", total_time)
    # return AD, LA
    # print(AD)
    # print(LA)


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


def CSC(file_name, write_time=False, matrix_size='-', density='-', file_path='../'):
    A = np.array(read_matrix_parallel(file_name, matrix_size, density))
    start_time = time.time()
    AR, IA, JA = [], [], []
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
    if write_time:
        total_time = time.time() - start_time
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('CSC %s\t%s\t%.5f\n' % (matrix_size, density, total_time))

    return AR, IA, JA


if __name__ == '__main__':
    global A
    if len(sys.argv) == 4:
        file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
        # A = read_matrix_parallel(file_name, sys.argv[1], sys.argv[2])
        # AR, IA, JA = CSC(np.array(A), True, sys.argv[1], sys.argv[2])
        # diagonal(True, sys.argv[1], sys.argv[2])
    else:
        file_name = 'output_10_0.5_1.txt'
        AR, IA, JA = CSC(np.array(A), True)
        # diagonal(True)
