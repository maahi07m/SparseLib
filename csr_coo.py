# To run: python3 csr_coo.py <number>


import time
import sys


def read_matrix(file):
    # line = ([tuple(map(int, data.split())) for data in file])
    while True:
        data = file.readline()
        if not data:
            break
        line = tuple(map(int, data.split()))
        yield line


def CSR():
    AR, IA, JA = [], [], []
    IA.append(0)
    ne_counter = 0
    file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
    # file_name = 'output.txt'
    with open(file_name, 'r') as f:
        for line in read_matrix(f):
            for col, value in enumerate(line):
                if value != 0:
                    AR.append(value)
                    ne_counter += 1
                    JA.append(col)
            IA.append(ne_counter)

    # print("AR = ", AR)
    # print("IA = ", IA)
    # print("JA = ", JA)
    return AR, IA, JA


def COO():
    AR, IA, JA = [], [], []
    file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
    # file_name = 'output.txt'
    with open(file_name, 'r') as f:
        for row,line in enumerate(read_matrix(f)):
            for col, value in enumerate(line):
                if value != 0:
                    AR.append(value)
                    IA.append(row)
                    JA.append(col)
    return AR, IA, JA


if __name__ == '__main__':
    start_time = time.time()
    AR1, IA1, JA1 = CSR()
    total_time = time.time() - start_time
    with open('execution_time.txt', 'a') as f:
        f.write('CSR %s\t%s\t%.5f\n' % (sys.argv[1], sys.argv[2], total_time))

    start_time = time.time()
    AR2, IA2, JA2 = COO()
    total_time = time.time() - start_time
    with open('execution_time.txt', 'a') as f:
        f.write('COO %s\t%s\t%.5f\n' % (sys.argv[1], sys.argv[2], total_time))
