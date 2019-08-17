import numpy as np


def csc_algorithm(matrix):
    """
    :param matrix: list
    :return: three vectors-lists AR, IA, JA.

    AR contains the non zero values, IA contains the corresponding row numbers of each non zero
    element in matrix and JA contains the relative starting position of each column
    of matrix in array AR.
    """
    ar, ia, ja = [], [], [0]
    ne_counter = 0
    file_matrix = np.transpose(matrix)
    for col, line in enumerate(file_matrix):
        for row, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ne_counter += 1
                ia.append(row)

                if len(ja) == 0:
                    ja.append(col)
        ja.append(ne_counter)

    return ar, ia, ja


def diagonal_algorithm(matrix):
    """
    :param matrix: list of lists
    :return: two vectors-lists AD, LA.

    Each diagonal of matrix that has at least one nonzero element is stored in a column of array AD.
    LA is a one-dimensional integer array of length nd, containing the diagonal numbers k
    for the diagonals stored in each corresponding column in array AD.
    """
    global A
    A = matrix
    la, ad = [], [[]]
    a_length = len(A)

    # main diagonal
    main_diagonal = __get_main_diagonal(a_length)
    if main_diagonal:
        la.append(0)

    # upper diagonal
    upper_diagonals = []
    for index in range(1, a_length):
        ad.append([])  # start initializing ad array
        upper_inner_diagonal = __get_upper_inner_diagonal(index, a_length)
        if upper_inner_diagonal:
            la.append(index)
            upper_diagonals.append(upper_inner_diagonal)

    # lower diagonal
    lower_diagonals = []
    # for index in range(a_length - 1, 0, -1):
    for index in range(1, a_length):
        lower_inner_diagonal = __get_lower_inner_diagonal(index, a_length)
        if lower_inner_diagonal:
            la.append(-1 * index)
            lower_diagonals.append(lower_inner_diagonal)

    # create ad array
    ad = tuple(ad)  # tuple or list or numpy
    if main_diagonal:
        __create_ad_with_main_diagonal(ad, main_diagonal, upper_diagonals, lower_diagonals, a_length)
    else:
        __create_ad_without_main_diagonal(ad, upper_diagonals, lower_diagonals, a_length)

    return ad, la


def __create_ad_with_main_diagonal(ad, main_diagonal, upper_diagonals, lower_diagonals, a_length):
    """
    :param ad: list
    :param main_diagonal: list
    :param upper_diagonals: list
    :param lower_diagonals: list
    :param a_length: int
    """
    row = 0
    uppers_number = len(upper_diagonals)
    lowers_number = len(lower_diagonals)
    while row < a_length:
        ad[row].append(main_diagonal[row])
        for index in range(uppers_number):
            ad[row].append(upper_diagonals[index][row])

        for index in range(lowers_number):
            ad[row].append(lower_diagonals[index][row])

        row += 1


def __create_ad_without_main_diagonal(ad, upper_diagonals, lower_diagonals, a_length):
    """
    :param ad: list
    :param upper_diagonals: list
    :param lower_diagonals: list
    :param a_length: int
    """
    row = 0
    uppers_number = len(upper_diagonals)
    lowers_number = len(lower_diagonals)

    while row < a_length:
        for index in range(uppers_number):
            ad[row].append(upper_diagonals[index][row])

        for index in range(lowers_number):
            ad[row].append(lower_diagonals[index][row])
        row += 1


def __get_upper_inner_diagonal(col, a_length):
    """
    :param col: list
    :param a_length: int
    :return: returns a list with non zero values if exists or an empty list
    """
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


def __get_lower_inner_diagonal(row, a_length):
    """
    :param row: list
    :param a_length: int
    :return: returns a list with non zero values if exists or an empty list
    """
    found_nv = False
    temp_diagonal = []
    mine_col_index = 0
    for index in range(row, a_length):
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


def __get_main_diagonal(a_length):
    """
    :param a_length: int
    :return: returns a list with non zero values if exists or an empty list
    """
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
