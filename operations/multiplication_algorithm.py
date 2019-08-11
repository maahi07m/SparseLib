def inner_algorithm(ar, ia,  br, ib):
    output = 0
    loop_bound = len(ia)  # len(ia) == len(ib)
    for row in range(1, loop_bound):
        ia_value = ia[row]
        a_nz = ia_value - ia[row - 1]
        if a_nz == 0:
            continue
        ib_value = ib[row]
        b_nz = ib_value - ib[row - 1]
        if b_nz == 0:
            continue
        output += ar[ia_value - 1] * br[ib_value - 1]

    return output


def outer_algorithm(ar, ja, br, jb):
    cr, ic, jc = [], [0], []

    for a_value in ar:
        for b_value in br:
            cr.append(a_value * b_value)
    ic = [ja_value * len(br) for ja_value in ja]
    jc = jb * len(ar)

    return cr, ic, jc


def multiply_matrix_vector_algorithm(ar, ia, ja, xr, ix):
    cr, ic, jc = [], [], [0]

    previous_ja_index = 0
    vector_nz_values_dict = fetch_vector_values(ix, xr)
    for index in range(1, len(ia)):
        nz_number = ia[index] - ia[index - 1]
        new_ja_index = previous_ja_index + nz_number
        result_of_rows_cols = multiply_row_col(ja[previous_ja_index:new_ja_index],
                                               ar[previous_ja_index:new_ja_index], vector_nz_values_dict)
        previous_ja_index = new_ja_index
        if result_of_rows_cols:
            cr.append(result_of_rows_cols)
            ic.append(index - 1)
    jc.append(len(cr))

    return cr, ic, jc


def multiply_vector_matrix_algorithm(ar, ia, ja, xr, jx):
    cr, ic, jc = [], [0], []
    previous_ia_index = 0
    vector_nz_values_dict = fetch_vector_values(jx, xr)
    for index in range(1, len(ja)):
        nz_number = ja[index] - ja[index - 1]
        if nz_number == 0:
            continue
        new_ia_index = previous_ia_index + nz_number
        result_of_rows_cols = multiply_row_col(ia[previous_ia_index:new_ia_index], ar[previous_ia_index:new_ia_index],
                                               vector_nz_values_dict)
        previous_ia_index = new_ia_index
        if result_of_rows_cols:
            cr.append(result_of_rows_cols)
            jc.append(index - 1)

    ic.append(len(cr))

    return cr, ic, jc


def multiply_row_col(row_indexes, row_values, vector_nz_values):
    """
    :param row_indexes: list
    :param row_values: list
    :param vector_nz_values: list
    ----------------------
    A loop in the max length of indexes lists multiply only when the elements in indexes lists is the same
    based in inner algorithm we found
    ----------------------
    :return: the result of a row/col multiply by a sparse vectors elements
    """
    result = 0
    for index, value in enumerate(row_indexes):
        if value in vector_nz_values:
            result += vector_nz_values[value] * row_values[index]
    return result


def fetch_vector_values(vector_nz_indexes, vector_nz_values):
    vector_nz_values_dict = {}
    for index, value in enumerate(vector_nz_indexes):
        vector_nz_values_dict[value] = vector_nz_values[index]
    return vector_nz_values_dict