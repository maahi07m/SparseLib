import time
from numpy import array
from scipy.sparse import csr_matrix
import sys
sys.path.append('../')
from compress.csr_coo import CSR
from read_file.matrix_read import read_matrix_parallel

file_1 = "output_10_0.5_1.txt"
file_2 = "output_10_0.5_2.txt"
size = 10

def sum_1xN():
    AR1, IA1, JA1, size = CSR(file_1)
    print("-" * 100)
    AR2, IA2, JA2, _ = CSR(file_2)

    start = time.time()

    # clean memory from useless variables
    del IA1, IA2

    total = []
    count_1 = count_2 = 0
    for index in range(size):
        if index in JA1 and index in JA2:
            total.append(AR1[count_1] + AR2[count_2])
            count_1 += 1
            count_2 += 1
        elif index in JA1 and index not in JA2:
            total.append(AR1[count_1])
            count_1 += 1
        elif index not in JA1 and index in JA2:
            total.append(AR2[count_2])
            count_2 += 1
        else:
            total.append(0)

    stop = time.time()
    print("-" * 100)
    print("time : ", stop - start)
    print("-" * 100)
    print(total)


def sum_Nx1():
    AR1, IA1, JA1, size = CSR(file_1)
    print("-" * 100)
    AR2, IA2, JA2, _ = CSR(file_2)

    start = time.time()
    # clean memory from useless variables
    del JA1, JA2

    total = []
    ar1_index = 0
    ar2_index = 0
    row_number = len(IA1)

    for index in range(1, row_number):   # start from their second element
        # if has_value_1 == 0 then line has value, otherwise not
        # same for has_value_2
        has_value_1 = (IA1[index] - IA1[index-1])
        has_value_2 = (IA2[index] - IA2[index-1])

        if has_value_1 == 0 and has_value_2 == 0:
            total.append(0)
        elif has_value_1 == 1 and has_value_2 == 0:
            total.append(AR1[ar1_index])
            ar1_index += 1
        elif has_value_1 == 0 and has_value_2 == 1:
            total.append(AR2[ar2_index])
            ar2_index += 1
        else:
            total.append(AR1[ar1_index] + AR2[ar2_index])
            ar1_index += 1
            ar2_index += 1

    stop = time.time()
    print("-" * 100)
    print("time : ", stop - start)
    print("-" * 100)
    for line in total:
        print(line)


def sum_matrices_nxn():
    AR1, IA1, JA1 = CSR(file_1)
    print("-"*100)
    AR2, IA2, JA2 = CSR(file_2)

    start = time.time()
    total = []
    nz_count_1 = 0
    nz_count_2 = 0
    row_index_1 = 1
    row_index_2 = 1
    col_index_1 = 0
    col_index_2 = 0
    while row_index_1 <= size and row_index_2 <= size:
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
        for index in range(size):
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
    # for line in total:
    #     print(line)
    return total


def subtraction_1xN():
    # AR1 - AR2
    AR1, IA1, JA1 = CSR(file_1)
    print("-" * 100)
    AR2, IA2, JA2 = CSR(file_2)

    start = time.time()

    # clean memory from useless variables
    del IA1, IA2

    total = []
    count_1 = count_2 = 0
    for index in range(size):
        if index in JA1 and index in JA2:
            total.append(AR1[count_1] - AR2[count_2])
            count_1 += 1
            count_2 += 1
        elif index in JA1 and index not in JA2:
            total.append(AR1[count_1])
            count_1 += 1
        elif index not in JA1 and index in JA2:
            total.append(-AR2[count_2])
            count_2 += 1
        else:
            total.append(0)

    stop = time.time()
    print("-" * 100)
    print("time : ", stop - start)
    print("-" * 100)
    return total


def subtraction_Nx1():
    # AR1 - AR2
    AR1, IA1, JA1, size = CSR(file_1)
    print("-" * 100)
    AR2, IA2, JA2, _ = CSR(file_2)

    start = time.time()
    # clean memory from useless variables
    del JA1, JA2

    total = []
    ar1_index = 0
    ar2_index = 0
    row_number = len(IA1)

    for index in range(1, row_number):   # start from their second element
        # if has_value_1 == 0 then line has value, otherwise not
        # same for has_value_2
        has_value_1 = (IA1[index] - IA1[index-1])
        has_value_2 = (IA2[index] - IA2[index-1])

        if has_value_1 == 0 and has_value_2 == 0:
            total.append(0)
        elif has_value_1 == 1 and has_value_2 == 0:
            total.append(AR1[ar1_index])
            ar1_index += 1
        elif has_value_1 == 0 and has_value_2 == 1:
            total.append(-AR2[ar2_index])
            ar2_index += 1
        else:
            total.append(AR1[ar1_index] - AR2[ar2_index])
            ar1_index += 1
            ar2_index += 1

    stop = time.time()
    print("-" * 100)
    print("time : ", stop - start)
    print("-" * 100)
    for line in total:
        print(line)


def subtraction_matrices_nxn():
    # AR1 - AR2
    AR1, IA1, JA1, size = CSR(file_1)
    print("-"*100)
    AR2, IA2, JA2, _ = CSR(file_2)

    start = time.time()
    total = []
    nz_count_1 = 0
    nz_count_2 = 0
    row_index_1 = 1
    row_index_2 = 1
    col_index_1 = 0
    col_index_2 = 0
    while row_index_1 <= size and row_index_2 <= size:
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
        for index in range(size):
            if index not in columns_1 and index in columns_2:
                temp_list.append(-values_2[col_to_values_2])
                col_to_values_2 += 1
            elif index in columns_1 and index not in columns_2:
                temp_list.append(values_1[col_to_values_1])
                col_to_values_1 += 1
            elif index in columns_1 and index in columns_2:
                temp_list.append(values_1[col_to_values_1] - values_2[col_to_values_2])
                col_to_values_1 += 1
                col_to_values_2 += 1
            else:
                temp_list.append(0)

        total.append(temp_list)
        row_index_1 += 1
        row_index_2 += 1
    stop = time.time()
    print("-" * 100)
    print("our time : ", stop-start)
    print("-" * 100)
    for line in total:
        print(line)
    # return total


def sum_matrices_numpy():
    A = read_matrix_parallel(file_1, '')

    B = read_matrix_parallel(file_2, '')

    start = time.time()
    A = csr_matrix(array(A))
    B = csr_matrix(array(B))
    total = A + B

    stop = time.time()
    print("numpy time : ", stop-start)
    return total.toarray()


def subtraction_matrices_numpy():
    A = read_matrix_parallel(file_1)

    B = read_matrix_parallel(file_2)

    start = time.time()
    A = csr_matrix(array(A))
    B = csr_matrix(array(B))
    total = A - B

    stop = time.time()
    print("numpy time : ", stop-start)
    return total.toarray()


if __name__ == '__main__':
    total = sum_matrices_nxn()
    # sum_1xN()
    # sum_Nx1()
    # subtraction_matrices()
    # total = subtraction_1xN()
    # subtraction_Nx1()

    total_np = sum_matrices_numpy()
    # total_np = subtraction_matrices_numpy()
    print(total_np)
    print(total == total_np)

