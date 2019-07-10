import time
from numpy import array
from scipy.sparse import csr_matrix
import sys
sys.path.append('../')
from compress.csr_coo import csr
from read_file.matrix_read import read_matrix_parallel

file_1 = "output_10_0.5_1.txt"
file_2 = "output_10_0.5_3.txt"
matrix_size = 10
density = 0.5
file_id_1 = 1
file_id_2 = 3


def addition_matrices_numpy():
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = csr_matrix(array(A))
    B = csr_matrix(array(B))

    start = time.time()
    total = A + B
    stop = time.time()

    print("numpy time : ", stop-start)
    x = total.toarray()
    # with open("../data_files/output_10_0.5_3.txt", 'w') as f:
    #     for item in x:
    #         for index,inner in enumerate(item):
    #             if index == item.shape[0] - 1:
    #                 f.write("%s" % str(int(inner)), )
    #             else:
    #                 f.write("%s\t" % str(int(inner)), )
    #         f.write("\n")
    #
    # return csr(matrix_size, density, file_id_1+2)
    return total.toarray()


def addition_matrices_nxn():
    AR, IA, JA = csr(matrix_size, density, file_id_1)
    # print(AR)
    # print(IA)
    # print(JA)
    print("-" * 100)
    BR, IB, JB = csr(matrix_size, density, file_id_2)
    # print(BR)
    # print(IB)
    # print(JB)
    CR, IC, JC = [], [0], []
    print("-" * 100)
    start = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(IA)):     # len(IA) = len(IB)
        a_row_number = IA[row_index] - IA[row_index-1]  # get A's row number
        b_row_number = IB[row_index] - IB[row_index-1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = JA[a_previous_row_index: new_a_row_index]
        b_columns = JB[b_previous_row_index: new_b_row_index]
        a_values = AR[a_previous_row_index: new_a_row_index]
        b_values = BR[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns + b_columns))
        for index in all_columns:
            if index in distinct_a:
                CR.append(a_values[a_value_index])
                JC.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                CR.append(b_values[b_value_index])
                JC.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] + b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    CR.append(new_value)
                    JC.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        IC.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    print(time.time()-start)
    return CR, IC, JC


def subtration_matrices_numpy():
    A = read_matrix_parallel(file_1)
    B = read_matrix_parallel(file_2)
    A = csr_matrix(array(A))
    B = csr_matrix(array(B))

    start = time.time()
    total = A - B
    stop = time.time()

    print("numpy time : ", stop-start)
    # x = total.toarray()
    # with open("../data_files/temp.txt", 'w') as f:
    #     for item in x:
    #         for index,inner in enumerate(item):
    #             if index == item.shape[0] - 1:
    #                 f.write("%s" % str(int(inner)), )
    #             else:
    #                 f.write("%s\t" % str(int(inner)), )
    #         f.write("\n")
    # return csr(matrix_size, density, file_id_1+2)
    return total.toarray()


def subtration_matrices_nxn():
    AR, IA, JA = csr(matrix_size, density, file_id_1)
    # print(AR)
    # print(IA)
    # print(JA)
    print("-" * 100)
    BR, IB, JB = csr(matrix_size, density, file_id_2)
    # print(BR)
    # print(IB)
    # print(JB)
    CR, IC, JC = [], [0], []
    print("-" * 100)
    start = time.time()

    a_previous_row_index = 0
    b_previous_row_index = 0
    c_nz_counter = 0
    for row_index in range(1, len(IA)):     # len(IA) = len(IB)
        a_row_number = IA[row_index] - IA[row_index-1]  # get A's row number
        b_row_number = IB[row_index] - IB[row_index-1]  # get B's row number

        new_a_row_index = a_previous_row_index + a_row_number
        new_b_row_index = b_previous_row_index + b_row_number

        a_columns = JA[a_previous_row_index: new_a_row_index]
        b_columns = JB[b_previous_row_index: new_b_row_index]
        a_values = AR[a_previous_row_index: new_a_row_index]
        b_values = BR[b_previous_row_index: new_b_row_index]

        a_value_index = 0
        b_value_index = 0
        common_col = sorted(set(a_columns).intersection(b_columns))
        distinct_a = sorted(set(a_columns).difference(b_columns))
        distinct_b = sorted(set(b_columns).difference(a_columns))
        all_columns = sorted(set(a_columns).union(b_columns))
        for index in all_columns:
            if index in distinct_a:
                CR.append(a_values[a_value_index])
                JC.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                CR.append(-b_values[b_value_index])
                JC.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_col:
                new_value = a_values[a_value_index] - b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    CR.append(new_value)
                    JC.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        IC.append(c_nz_counter)
        a_previous_row_index = new_a_row_index
        b_previous_row_index = new_b_row_index
    print(time.time()-start)
    return CR, IC, JC


if __name__ == '__main__':
    # npR, Inp, Jnp = addition_matrices_numpy()
    numpy_result = addition_matrices_numpy()

    C, IC, JC = addition_matrices_nxn()

    # for x in range(len(C)):
    #     if C[x] != npR[x]:
    #         print(x, C[x], npR[x])
    # print('----')
    # for i in range(len(IC)):
    #     if IC[i] != Inp[i]:
    #         print(i, IC[i], Inp[i])
    # print('----')
    #
    # for  z in range(len(JC)):
    #     if JC[z] != Jnp[z]:
    #         print(z, JC[z], Jnp[z])
