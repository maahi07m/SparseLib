import glob
import itertools as it
import os
import re


def read_file(file_name, return_list=False, file_path='../'):
    """
    :param return_list: boolean
    :param file_name: string
    :param file_path: string, where to search for file
    """
    number_of_header_lines = 4
    try:
        with open(os.path.join(file_path + 'data_files', file_name), 'r', encoding='utf-8') as f:
            head = __read_header(f, number_of_header_lines)
            number_of_pointers, number_of_row, numerical_values = int(head[1][1]), int(head[1][2]), int(head[1][3])
            m, n = int(head[2][1]), int(head[2][2])
            if int(head[1][4]) != 0:
                raise NotImplementedError("No supported format!")
            matrix_type = head[2][0]
            matrix = __choose_function(matrix_type, f, number_of_pointers, number_of_row, numerical_values, m, n)
            if return_list:
                return matrix
            else:
                __write_matrix_to_file(m, n, matrix, file_path)
    except EOFError:
        raise EOFError('EOFError')
    except FileNotFoundError:
        raise FileNotFoundError("File %s not found" % file_name)


def __read_header(f, number_of_header_lines):
    """
    :param f: file's pointer
    :param number_of_header_lines: int
    :return: header's data
    """
    # head contain the info of the matrix
    counter = 0
    head = []
    right_hand = True
    for line in f:
        item_in_line = line.split()
        head.append(item_in_line)
        if counter == 2:
            if int(head[1][4]) != 0 and right_hand:
                counter -= 1
                right_hand = False
        counter += 1
        if counter == number_of_header_lines:
            break
    return head


def __read_data(f, number_of_lines_to_read):
    """
    :param f: file's pointer
    :param number_of_lines_to_read: int
    :return: read values
    """
    return [item.split() for item in list(it.islice(f, number_of_lines_to_read))]


def __convert_strings_to_numbers(list_of_strings, convert_to_int=True):
    """
    :param list_of_strings: list with values that needed to be converted
    :param convert_to_int: boolean
    :return: converted list
    """
    if convert_to_int:
        return [item - 1 for item in list(map(int, list(it.chain(*list_of_strings))))]
    else:
        return list(map(float, list(it.chain(*list_of_strings))))


def __choose_function(matrix_type, f, number_of_pointers, number_of_row, numerical_values, m, n):
    """
    :param matrix_type: string
    :param f: file's pointer
    :param number_of_pointers: int
    :param number_of_row: int
    :param numerical_values: int
    :param m: int
    :param n: int
    :return: file's 2d matrix
    """
    matrix = []
    if 'RS' in matrix_type or 'CS' in matrix_type:
        list_numbers_per_cols = __convert_strings_to_numbers(
            __read_data(f, int(number_of_pointers)))  # csc format JA, number of values per line
        if len(list_numbers_per_cols) != int(n) + 1:  # len(JA) != number of columns +1
            raise TypeError('Wrong file format')
        else:
            list_indices_of_rows = __convert_strings_to_numbers(
                __read_data(f, int(number_of_row)))  # IA,  rows' indices for every column
            list_of_data = __read_ar_values(f, int(numerical_values))  # AR
            if len(list_of_data) != len(list_indices_of_rows):  # len(AR) != len(IA)
                raise TypeError('Wrong file format')
            else:
                matrix = __create_rs_cs(list_of_data, list_indices_of_rows, list_numbers_per_cols, m, n)

    elif 'RU' in matrix_type or 'CU' in matrix_type:
        list_numbers_per_cols = __convert_strings_to_numbers(
            __read_data(f, int(number_of_pointers)))  # csc format JA, number of values per line
        if len(list_numbers_per_cols) != int(n) + 1:  # len(JA) != number of columns + 1
            raise TypeError('Wrong file format')
        else:
            list_indices_of_rows = __convert_strings_to_numbers(
                __read_data(f, int(number_of_row)))  # IA, rows' indices for every column
            list_of_data = __read_ar_values(f, int(numerical_values))  # AR
            if len(list_of_data) != len(list_indices_of_rows):  # len(AR) != len(IA)
                raise TypeError('Wrong file format')
            else:
                matrix = __create_ru_cu(list_of_data, list_indices_of_rows, list_numbers_per_cols, m, n)
    else:
        raise NotImplementedError('No supported format!')
    return matrix


def __create_rs_cs(ar, ia, ja, m, n):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param m: int
    :param n: int
    :return: generates and returns the real or complex symmetric matrix
    """
    matrix = [[0 for _ in range(n)] for __ in range(m)]
    # print(len(ar), len(ia), len(ja))
    for index, value in enumerate(it.islice(ja, len(ja) - 1)):
        col_values = ar[value:ja[index + 1]]
        for inner_index, inner_value in enumerate(ia[value:ja[index + 1]]):
            if not col_values[inner_index]:
                continue
            matrix[inner_value][index] = col_values[inner_index]
            if inner_value != index:
                matrix[index][inner_value] = col_values[inner_index]
    return matrix


def __create_ru_cu(ar, ia, ja, m, n):
    """
    :param ar: list
    :param ia: list
    :param ja: list
    :param m: int
    :param n: int
    :return: generates and returns the real or complex non symmetric matrix
    """
    matrix = [[0 for _ in range(n)] for __ in range(m)]
    for index, value in enumerate(it.islice(ja, len(ja) - 1)):
        col_values = ar[value:ja[index + 1]]
        for inner_index, inner_value in enumerate(ia[value:ja[index + 1]]):
            matrix[inner_value][index] = col_values[inner_index]
    counter = 0
    for index in matrix:
        for inner_index in index:
            if not inner_index:
                counter += 1

    return matrix


def __read_ar_values(f, number_of_lines_to_read):
    """
    :param f: file's pointer
    :param number_of_lines_to_read: int
    :return: read values
    """
    values_per_line = [item for item in list(it.islice(f, number_of_lines_to_read))]
    p = re.compile('[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d{2} ) ?', re.VERBOSE)
    values_per_line = [float(re.sub('^-\.', '-0', item)) for line in values_per_line for item in p.findall(line)]
    return values_per_line


def __write_matrix_to_file(m, n, matrix, file_path):
    """
    :param m: int
    :param n: int
    :param matrix: list of lists
    :param file_path: string, where to store the file
    """
    file_id = __find_read_file_name(m, n)
    file_name = 'output_%d_%d_hb_%d.txt' % (m, n, file_id)
    data_to_write = ''
    for item in matrix:
        for index, inner in enumerate(item):
            if index == len(item) - 1:
                data_to_write += str(inner)
            else:
                data_to_write += ("%s\t" % str(inner))
        data_to_write += "\n"
    if not os.path.exists(file_path + 'data_files'):
        os.makedirs(file_path + 'data_files')
    with open(os.path.join(file_path + 'data_files', file_name), 'w') as f:
        f.write(data_to_write)


def __find_read_file_name(m, n):
    """
    :param m: int
    :param n: int
    :return file id
    Finds the last hb file's id with the same number of rows and columns. If there is no such file, return 1
    """
    # output_m_n_hb_id.txt
    file_name_to_search = 'output_%d_%d_hb' % (m, n)
    a = glob.glob('../data_files/' + file_name_to_search + '*.txt')
    if len(a):
        p = re.compile('.+_(.+?)\.txt', re.VERBOSE)
        try:
            ids = [int(p.search(item).group(1)) for item in a]
            id_to_use = max(ids)
        except AttributeError:
            id_to_use = 1
        return id_to_use
    return 1
