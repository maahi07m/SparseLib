def csr_algorithm(file_matrix):
    """
    :param file_matrix: list of lists
    ----------------------
    :return: three vectors, the first contains the nz values, the second contains the number of nz values in each row
    and the third contains the pointer of cols in which a nz value exists
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
    ----------------------
    :return: three vectors, the first is the nz values, the second and the third the pointers of rows and cols
    respectively in which a nz value exists
    """
    ar, ia, ja = [], [], []
    for row, line in enumerate(file_matrix):
        for col, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ia.append(row)
                ja.append(col)

    return ar, ia, ja