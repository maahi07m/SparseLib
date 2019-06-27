import math
import time
import sys
import math


def read_matrix(file):
    # line = ([tuple(map(int, data.split())) for data in file])
    while True:
        data = file.readline()
        if not data:
            break
        line = tuple(map(int, data.split()))
        yield line


def CSR(file_name):
    AR, IA, JA = [], [], []
    IA.append(0)
    ne_counter = 0
    # file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
    with open(file_name, 'r') as f:
        for line in read_matrix(f):
            for col, value in enumerate(line):
                if value != 0:
                    AR.append(value)
                    ne_counter += 1
                    JA.append(col)
            IA.append(ne_counter)

    print("AR = ", AR)
    print("IA = ", IA)
    print("JA = ", JA)
    return AR, IA, JA, 5


def sum_matrices():
    AR1, IA1, JA1, size1 = CSR("output_15000_0.005_1.txt")
    print("-"*100)
    AR2, IA2, JA2, size2 = CSR("output_15000_0.005_2.txt")

    start = time.time()
    total = []
    nz_count_1 = 0
    nz_count_2 = 0
    row_index_1 = 1
    row_index_2 = 1
    col_index_1 = 0
    col_index_2 = 0
    while row_index_1 <= size1 and row_index_2 <= size2:
        temp_list = []
        nz_count_1 = IA1[row_index_1] - IA1[row_index_1 - 1]
        columns_1 = JA1[col_index_1: col_index_1 + nz_count_1]
        values_1 = AR1[col_index_1: col_index_1 + nz_count_1]
        col_index_1 += nz_count_1

        nz_count_2 = IA2[row_index_2] - IA2[row_index_2 - 1]
        columns_2 = JA2[col_index_2: col_index_2 + nz_count_2]
        values_2 = AR2[col_index_2: col_index_2 + nz_count_2]
        col_index_2 += nz_count_2

        col_to_values_1 = 0
        col_to_values_2 = 0
        for index in range(size1):
            if index not in columns_1 and index in columns_2:
                temp_list.append(values_2[col_to_values_2])
                col_to_values_2 += 1
            elif index in columns_1 and index not in columns_2:
                temp_list.append(values_1[col_to_values_1])
                col_to_values_1 += 1
            elif index in columns_1 and index in columns_2:
                temp_list.append(values_1[col_to_values_1] + values_2[col_to_values_2])
                col_to_values_1 += 1
                col_to_values_2 += 1
            else:
                temp_list.append(0)

        total.append(temp_list)
        row_index_1 += 1
        row_index_2 += 1
    stop = time.time()
    print("-" * 100)
    print("time : ", stop-start)
    print("-" * 100)
    for line in total:
        print(line)


if __name__ == '__main__':
    sum_matrices()

