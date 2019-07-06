import time
from numpy import array
from scipy.sparse import csc_matrix
import sys
sys.path.append('../')
from compress.diagonal_csc import CSC
from read_file.matrix_read import read_matrix_parallel

file_1 = "output_1000_0.005_1.txt"
file_2 = "output_1000_0.005_2.txt"
# file_1 = "output_6_0.5_1.txt"
# file_2 = "output_6_0.5_2.txt"


def addition_matrices_numpy():
    A = read_matrix_parallel(file_1, '')
    B = read_matrix_parallel(file_2, '')
    A = csc_matrix(array(A))
    B = csc_matrix(array(B))

    start = time.time()
    total = A + B
    stop = time.time()

    print("numpy time : ", stop-start)
    x = total.toarray()
    with open("../data_files/temp.txt", 'w') as f:
        for item in x:
            for index,inner in enumerate(item):
                if index == item.shape[0] - 1:
                    f.write("%s" % str(int(inner)), )
                else:
                    f.write("%s\t" % str(int(inner)), )
            f.write("\n")

    return CSC('temp.txt')
    # return total


def subtration_matrices_numpy():
    A = read_matrix_parallel(file_1, '')
    B = read_matrix_parallel(file_2, '')
    A = csc_matrix(array(A))
    B = csc_matrix(array(B))

    start = time.time()
    total = A - B
    stop = time.time()

    print("numpy time : ", stop-start)
    x = total.toarray()
    with open("../data_files/temp.txt", 'w') as f:
        for item in x:
            for index,inner in enumerate(item):
                if index == item.shape[0] - 1:
                    f.write("%s" % str(int(inner)), )
                else:
                    f.write("%s\t" % str(int(inner)), )
            f.write("\n")

    return CSC('temp.txt')
    # return total


def addition_matrices_nxn():
    AR, IA, JA = CSC(file_name=file_1)
    # print(AR)
    # print(IA)
    # print(JA)
    print("-" * 100)
    BR, IB, JB = CSC(file_name=file_2)
    # print(BR)
    # print(IB)
    # print(JB)
    CR, IC, JC = [], [], [0]
    print("-" * 100)
    start = time.time()

    a_previous_col_index = 0
    b_previous_col_index = 0
    c_nz_counter = 0
    for col_index in range(1, len(JA)):     # len(JA) = len(JB)
        a_col_number = JA[col_index] - JA[col_index-1]  # get A's row number
        b_col_number = JB[col_index] - JB[col_index-1]  # get B's row number

        new_a_col_index = a_previous_col_index + a_col_number
        new_b_col_index = b_previous_col_index + b_col_number

        a_rows = IA[a_previous_col_index: new_a_col_index]
        b_rows = IB[b_previous_col_index: new_b_col_index]
        a_values = AR[a_previous_col_index: new_a_col_index]
        b_values = BR[b_previous_col_index: new_b_col_index]

        a_value_index = 0
        b_value_index = 0
        common_rows = sorted(set(a_rows).intersection(b_rows))
        distinct_a = sorted(set(a_rows).difference(b_rows))
        distinct_b = sorted(set(b_rows).difference(a_rows))
        all_rows = sorted(set(a_rows).union(b_rows))
        for index in all_rows:
            if index in distinct_a:
                CR.append(a_values[a_value_index])
                IC.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                CR.append(b_values[b_value_index])
                IC.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_rows:
                new_value = a_values[a_value_index] + b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    CR.append(new_value)
                    IC.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        JC.append(c_nz_counter)
        a_previous_col_index = new_a_col_index
        b_previous_col_index = new_b_col_index
    print(time.time() - start)
    return CR, IC, JC


def subtration_matrices_nxn():
    AR, IA, JA = CSC(file_name=file_1)
    # print(AR)
    # print(IA)
    # print(JA)
    print("-" * 100)
    BR, IB, JB = CSC(file_name=file_2)
    # print(BR)
    # print(IB)
    # print(JB)
    CR, IC, JC = [], [], [0]
    print("-" * 100)
    start = time.time()

    a_previous_col_index = 0
    b_previous_col_index = 0
    c_nz_counter = 0
    for col_index in range(1, len(JA)):     # len(JA) = len(JB)
        a_col_number = JA[col_index] - JA[col_index-1]  # get A's row number
        b_col_number = JB[col_index] - JB[col_index-1]  # get B's row number

        new_a_col_index = a_previous_col_index + a_col_number
        new_b_col_index = b_previous_col_index + b_col_number

        a_rows = IA[a_previous_col_index: new_a_col_index]
        b_rows = IB[b_previous_col_index: new_b_col_index]
        a_values = AR[a_previous_col_index: new_a_col_index]
        b_values = BR[b_previous_col_index: new_b_col_index]

        a_value_index = 0
        b_value_index = 0
        common_rows = sorted(set(a_rows).intersection(b_rows))
        distinct_a = sorted(set(a_rows).difference(b_rows))
        distinct_b = sorted(set(b_rows).difference(a_rows))
        all_rows = sorted(set(a_rows).union(b_rows))
        for index in all_rows:
            if index in distinct_a:
                CR.append(a_values[a_value_index])
                IC.append(index)
                a_value_index += 1
                c_nz_counter += 1
            elif index in distinct_b:
                CR.append(-b_values[b_value_index])
                IC.append(index)
                b_value_index += 1
                c_nz_counter += 1
            elif index in common_rows:
                new_value = a_values[a_value_index] - b_values[b_value_index]
                if new_value == 0:
                    a_value_index += 1
                    b_value_index += 1
                    continue
                else:
                    CR.append(new_value)
                    IC.append(index)
                    a_value_index += 1
                    b_value_index += 1
                    c_nz_counter += 1
        JC.append(c_nz_counter)
        a_previous_col_index = new_a_col_index
        b_previous_col_index = new_b_col_index
    print(time.time() - start)
    return CR, IC, JC


if __name__ == '__main__':
    npR, Inp, Jnp = addition_matrices_numpy()
    C, IC, JC = addition_matrices_nxn()

    for x in range(len(C)):
        if C[x] != npR[x]:
            print(x, C[x], npR[x])
    print('----')
    for i in range(len(IC)):
        if IC[i] != Inp[i]:
            print(i, IC[i], Inp[i])
    print('----')

    for  z in range(len(JC)):
        if JC[z] != Jnp[z]:
            print(z, JC[z], Jnp[z])