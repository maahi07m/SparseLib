def addition_algorithm_csr(ar, ia, ja, br, ib, jb):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param br: list
    :param ib: list
    :param jb: list
    ----------------------
    :return: three vectors, the result of addition stored in csr format
    """
    cr, ic, jc = [], [0], []

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
    return cr, ic, jc


def subtraction_algorithm_csr(ar, ia, ja, br, ib, jb):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param br: list
    :param ib: list
    :param jb: list
    ----------------------
    :return: three vectors, the result of subtraction stored in csr format
    """
    cr, ic, jc = [], [0], []

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

    return cr, ic, jc


def addition_algorithm_csc(ar, ia, ja, br, ib, jb):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param br: list
    :param ib: list
    :param jb: list
    ----------------------
    :return: three vectors, the result of addition stored in csc format
    """
    cr, ic, jc = [], [], [0]

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

    return cr, ic, jc


def subtraction_algorithm_csc(ar, ia, ja, br, ib, jb):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param br: list
    :param ib: list
    :param jb: list
    ----------------------
    :return: three vectors, the result of ths subtraction stored in csc format
    """
    cr, ic, jc = [], [], [0]

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

    return cr, ic, jc
