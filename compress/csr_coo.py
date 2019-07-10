"""To run: python3 csr_coo.py <size> <density> <file_id>"""
import time
import sys
import os
sys.path.append('../')
from read_file.matrix_read import read_matrix_generator
from helpers import generator
import glob


def CSR(file_name, write_time=False, matrix_size='-', density='-', file_path='../'):
    start_time = time.time()
    AR, IA, JA = [], [], []
    IA.append(0)
    generator.get_user_input()
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


def COO(file_name, write_time=False, matrix_size='-', density='-', file_path='../'):
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
    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('COO %s\t%s\t%.5f\n' % (matrix_size, density, total_time))
    return AR, IA, JA


if __name__ == '__main__':
    if len(sys.argv) == 4:
        file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
        AR1, IA1, JA1 = CSR(file_name, True, sys.argv[1], sys.argv[2])
        print(AR1, IA1, JA1)
        AR2, IA2, JA2 = COO(file_name, True, sys.argv[1], sys.argv[2])
    # else:
    #     file_name = 'output_10_0.5_1.txt'
    #     AR1, IA1, JA1 = CSR(file_name, True, 10, 0.5)
    #     AR2, IA2, JA2 = COO(file_name, True, 10, 0.5)
