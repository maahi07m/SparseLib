def csr_algorithm(file_matrix):
    """
    :param file_matrix: list of lists
    :return: three vectors-lists AR, IA, JA.

    Compress a matrix 1-d or 2-d to csr format using the function csr_algorithm.
    AR contains the non zero values, IA contains the relative starting position of each row
    of matrix in array AR and JA contains the corresponding column numbers of each non zero
    element in matrix.
    """
    ar, ia, ja = [], [], []
    ia.append(0)
    ne_counter = 0
    for row, line in enumerate(file_matrix):
        for col, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ne_counter += 1
                ja.append(col)
        ia.append(ne_counter)

    return ar, ia, ja


def coo_algorithm(file_matrix):
    """
    :param file_matrix: list
    :return: three vectors-lists AR, IA, JA.

    AR contains the non zero values, IA contains the corresponding row number of each non
    zero element in matrix and JA contains the corresponding column number of each non
    zero element in matrix.
    """
    ar, ia, ja = [], [], []
    for row, line in enumerate(file_matrix):
        for col, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ia.append(row)
                ja.append(col)

    return ar, ia, ja
