"""To run: python3 csr_coo.py <size> <density> <file_id>"""
import time
import sys
import os
sys.path.append('../')
from read_file.matrix_read import read_matrix_generator, read_matrix_parallel


def csr(matrix_size, density, file_id, parallel=True, write_time=False, file_path='../'):
    file_name = 'output_' + str(matrix_size) + '_' + str(density) + '_' + str(file_id) + '.txt'
    if parallel:
        return csr_parallel(file_name, write_time, matrix_size, density, file_path)
    else:
        return csr_sequential(file_name, write_time, matrix_size, density, file_path)


def coo(matrix_size, density, file_id, parallel=True, write_time=False, file_path='../'):
    file_name = 'output_' + str(matrix_size) + '_' + str(density) + '_' + str(file_id) + '.txt'
    if parallel:
        return coo_parallel(file_name, write_time, matrix_size, density, file_path)
    else:
        return coo_sequential(file_name, write_time, matrix_size, density, file_path)


def csr_parallel(file_name, write_time, matrix_size, density, file_path):
    A = read_matrix_parallel(file_name, matrix_size, density, True, 4, file_path)
    start_time = time.time()
    AR, IA, JA = [], [], []
    IA.append(0)
    ne_counter = 0
    for row, line in enumerate(A):
        for col, value in enumerate(line):
            if value != 0:
                AR.append(value)
                ne_counter += 1
                JA.append(col)
        IA.append(ne_counter)

    # print("AR = ", AR)
    # print("IA = ", IA)
    # print("JA = ", JA)
    total_time = time.time() - start_time
    if write_time:
        with open(os.path.join(file_path + 'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('CSR %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
    return AR, IA, JA


def csr_sequential(file_name, write_time, matrix_size, density, file_path):
    start_time = time.time()
    AR, IA, JA = [], [], []
    IA.append(0)
    ne_counter = 0
    with open(os.path.join(file_path+'data_files', file_name), 'r') as f:
        for line in read_matrix_generator(f):
            for col, value in enumerate(line):
                if value != 0:
                    AR.append(value)
                    ne_counter += 1
                    JA.append(col)
            IA.append(ne_counter)

    # print("AR = ", AR)
    # print("IA = ", IA)
    # print("JA = ", JA)
    total_time = time.time() - start_time
    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('CSR %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
    return AR, IA, JA


def coo_parallel(file_name, write_time, matrix_size, density, file_path):
    A = read_matrix_parallel(file_name, matrix_size, density, True, 4, file_path)
    start_time = time.time()
    AR, IA, JA = [], [], []
    for row, line in enumerate(A):
        for col, value in enumerate(line):
            if value != 0:
                AR.append(value)
                IA.append(row)
                JA.append(col)
    total_time = time.time() - start_time
    print("AR = ", AR)
    print("IA = ", IA)
    print("JA = ", JA)
    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('COO %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
    return AR, IA, JA


def coo_sequential(file_name, write_time, matrix_size, density, file_path):
    start_time = time.time()
    AR, IA, JA = [], [], []
    with open(os.path.join(file_path+'data_files', file_name), 'r') as f:
        for row, line in enumerate(read_matrix_generator(f)):
            for col, value in enumerate(line):
                if value != 0:
                    AR.append(value)
                    IA.append(row)
                    JA.append(col)
    total_time = time.time() - start_time
    # print("AR = ", AR)
    # print("IA = ", IA)
    # print("JA = ", JA)
    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('COO %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
    return AR, IA, JA


if __name__ == '__main__':
    if len(sys.argv) == 5:
        if sys.argv[1].lower() == 'csr':
            AR1, IA1, JA1 = csr(sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        elif sys.argv[1].lower() == 'coo':
            AR2, IA2, JA2 = coo(sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        else:
            AR1, IA1, JA1 = csr(sys.argv[2], sys.argv[3], sys.argv[4], True, True)
            AR2, IA2, JA2 = coo(sys.argv[2], sys.argv[3], sys.argv[4], True, True)
    else:
        print("There is no main to run")
