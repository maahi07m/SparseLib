import itertools as it
import os
import re
import glob
import sys


def read_file(file_name):
    number_of_header_lines = 4
    matrix = []
    try:
        with open("../data_files/" + file_name, 'r', encoding='utf-8') as f:
            head, flag = __read_header(f, number_of_header_lines)
            number_of_pointers, number_of_row, numerical_values = int(head[1][1]), int(head[1][2]), int(head[1][3])
            m, n = int(head[2][1]), int(head[2][2])
            if int(head[1][4]) != 0:
                raise NotImplementedError("No supported format!")

            matrix_type = head[2][0]
            matrix = __choose_function(matrix_type, f, number_of_pointers, number_of_row, numerical_values, m, n)
            __write_matrix_to_file(m, n, matrix)
            return matrix
    except EOFError:
        print('EOFError')
        sys.exit(1)


def __read_header(f, N):
    # head contain the info of the matrix
    counter = 0
    head = []
    flag = True
    for line in f:
        item_in_line = line.split()
        head.append(item_in_line)
        if counter == 2:
            if int(head[1][4]) != 0 and flag:
                counter -= 1
                flag = False
        counter += 1
        if counter == N:
            break
    return head, flag


def __read_data(f, N):
    return [item.split() for item in list(it.islice(f, N))]


def __convert_strings_to_numbers(list_of_strings, convert_to_int=True):
    if convert_to_int:
        return [item - 1 for item in list(map(int, list(it.chain(*list_of_strings))))]
    else:
        return list(map(float, list(it.chain(*list_of_strings))))


def __choose_function(matrix_type, f, number_of_pointers, number_of_row, numerical_values, m, n):
    matrix = []
    if 'RS' in matrix_type or 'CS' in matrix_type:
        list_numbers_per_cols = __convert_strings_to_numbers(
            __read_data(f, int(number_of_pointers)))  # csc format JA plithos timon ana grammi
        if len(list_numbers_per_cols) != int(n) + 1:    # len(JA) != number of columns +1
            print('Wrong file format')
        else:
            list_indices_of_rows = __convert_strings_to_numbers(
                __read_data(f, int(number_of_row)))  # IA oi deiktes ton rows gia kathe stili
            list_of_data = __convert_strings_to_numbers(__read_data(f, int(numerical_values)), convert_to_int=False)  # AR
            if len(list_of_data) != len(list_indices_of_rows):  # len(AR) != len(IA)
                print('Wrong file format')
            else:
                matrix = __create_rs_cs(list_of_data, list_indices_of_rows, list_numbers_per_cols, m, n)

    elif 'RU' in matrix_type or 'CU' in matrix_type:
        list_numbers_per_cols = __convert_strings_to_numbers(
            __read_data(f, int(number_of_pointers)))  # csc format JA plithos timon ana grammi
        if len(list_numbers_per_cols) != int(n) + 1:    # len(JA) != number of columns + 1
            print('Wrong file format')
        else:
            list_indices_of_rows = __convert_strings_to_numbers(
                __read_data(f, int(number_of_row)))  # IA oi deiktes ton rows gia kathe stili
            list_of_data = __read_ru_values(f, int(numerical_values))  # AR
            if len(list_of_data) != len(list_indices_of_rows):  # len(AR) != len(IA)
                print('Wrong file format')
            else:
                matrix = __create_ru_cu(list_of_data, list_indices_of_rows, list_numbers_per_cols, m, n)
    else:
        raise NotImplementedError('No supported format!')
    return matrix


def __create_rs_cs(AR, IA, JA, m, n):
    matrix = [[0 for _ in range(n)] for __ in range(m)]
    print(len(AR), len(IA), len(JA))
    for index, value in enumerate(it.islice(JA, len(JA) - 1)):
        col_values = AR[value:JA[index + 1]]
        for inner_index, inner_value in enumerate(IA[value:JA[index + 1]]):
            if not col_values[inner_index]:
                continue
            matrix[inner_value][index] = col_values[inner_index]
            if inner_value != index:
                matrix[index][inner_value] = col_values[inner_index]
    return matrix


def __create_ru_cu(AR, IA, JA, m, n):
    matrix = [[0 for value in range(n)] for i in range(m)]
    for index, value in enumerate(it.islice(JA, len(JA) - 1)):
        col_values = AR[value:JA[index + 1]]
        for inner_index, inner_value in enumerate(IA[value:JA[index + 1]]):
            matrix[inner_value][index] = col_values[inner_index]
    counter = 0
    for index in matrix:
        for inner_index in index:
            if not inner_index:
                counter += 1

    return matrix


def __read_ru_values(f, N):
    values_per_line = [item for item in list(it.islice(f, N))]
    p = re.compile('[-+]? (?: (?: \d* \. \d+ ) | (?: \d+ \.? ) )(?: [Ee] [+-]? \d{2} ) ?', re.VERBOSE)
    values_per_line = [float(re.sub('^-\.', '-0', item)) for line in values_per_line for item in p.findall(line)]
    return values_per_line


def __write_matrix_to_file(m, n, matrix, file_path='../'):
    id = __find_read_file_name(m, n)
    file_name = 'output_%d_%d_hb_%d.txt' % (m, n, id)
    data_to_write = ''
    for item in matrix:
        for index, inner in enumerate(item):
            if index == len(item) - 1:
                data_to_write += str(inner)
            else:
                data_to_write += ("%s\t" % str(inner))
        data_to_write += "\n"
    with open(os.path.join(file_path+'data_files', file_name), 'w') as f:
        f.write(data_to_write)


def __find_read_file_name(m, n):
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


if __name__ == '__main__':
    try:
        final_matrix = read_file(file_name=sys.argv[1])
    except FileNotFoundError:
        print("File not found")
        sys.exit(1)
    # print(final_matrix)
