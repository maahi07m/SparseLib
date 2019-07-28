"""To run: python3 csr_coo.py <algorithm name> <size of rows> <size of cols> <density> <file_id>"""
import os
import sys
import time

sys.path.append('../')
from read_file.matrix_read import read_matrix_generator, read_matrix_parallel


def csr(matrix_size_row, matrix_size_col, density, file_id, parallel=True, write_time=False, file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param write_time: boolean
    :param file_path: int
    ----------------------
    :return: due to boolean variable parallel the matrix will stored in csr format parallel or sequentially
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    if parallel:
        return csr_parallel(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path)
    else:
        return csr_sequential(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path)


def coo(matrix_size_row, matrix_size_col,  density, file_id, parallel=True, write_time=False, file_path='../'):
    """
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_id: int
    :param parallel: boolean
    :param write_time: boolean
    :param file_path: int
    ----------------------
    :return: due to boolean variable parallel the matrix will stored in coo format parallel or sequentially
    """
    file_name = 'output_' + str(matrix_size_row) + '_' + str(matrix_size_col) + '_' + str(density) + '_' + \
                str(file_id) + '.txt'
    if parallel:
        return coo_parallel(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path)
    else:
        return coo_sequential(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path)


def csr_parallel(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path):
    """
    :param file_name: string
    :param write_time: boolean
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to csr format parallel, write the execution time in a txt file
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains the number of non zero values in a line (always the first element is 0 and the last one
             the number of rows + 1), the third contains pointers of rows for the AR values
    """
    file_matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True, 4, file_path)
    start_time = time.time()
    ar, ia, ja = [], [], []
    ia.append(0)
    ne_counter = 0
    for row, line in enumerate(file_matrix):
        for col, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ne_counter += 1
                ja.append(col)
        ia.append(ne_counter)
    total_time = time.time() - start_time
    if write_time:
        with open(os.path.join(file_path + 'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('CSR\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return ar, ia, ja


def csr_sequential(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path):
    """
    :param file_name: string
    :param write_time: boolean
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to csr format sequentially write the execution time in a txt file
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains the number of non zero values in a line (always the first element is 0 and the last one
             the number of rows + 1), the third contains pointers of rows for the AR values
    """
    start_time = time.time()
    ar, ia, ja = [], [], []
    ia.append(0)
    ne_counter = 0
    try:
        with open(os.path.join(file_path + 'data_files', file_name), 'r') as f:
            for line in read_matrix_generator(f):
                for col, value in enumerate(line):
                    if value != 0:
                        ar.append(value)
                        ne_counter += 1
                        ja.append(col)
                ia.append(ne_counter)
        total_time = time.time() - start_time
        if write_time:
            with open(os.path.join(file_path + 'execution_results', 'execution_time.txt'), 'a') as f:
                f.write('CSR\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
        return ar, ia, ja
    except FileNotFoundError:
        sys.exit("File %s not found" % file_name)


def coo_parallel(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path):
    """
    :param file_name: string
    :param write_time: boolean
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to coo format parallel write the execution time in a txt file
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains the row-pointers and the third the col-pointers
    """
    file_matrix = read_matrix_parallel(file_name, matrix_size_row, matrix_size_col, density, True, 4, file_path)
    start_time = time.time()
    ar, ia, ja = [], [], []
    for row, line in enumerate(file_matrix):
        for col, value in enumerate(line):
            if value != 0:
                ar.append(value)
                ia.append(row)
                ja.append(col)
    total_time = time.time() - start_time
    if write_time:
        with open(os.path.join(file_path+'execution_results', 'execution_time.txt'), 'a') as f:
            f.write('COO\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
    return ar, ia, ja


def coo_sequential(file_name, write_time, matrix_size_row, matrix_size_col, density, file_path):
    """
    :param file_name: string
    :param write_time: boolean
    :param matrix_size_row: int
    :param matrix_size_col: int
    :param density: float
    :param file_path: string
    ----------------------
    Convert a matrix 1-d, 2-d to coo format sequentially write the execution time in a txt file
    ----------------------
    :return: three lists AR, IA, JA, the first one contains the non zeros values,
             the second contains the row-pointers and the third the col-pointers
    """
    start_time = time.time()
    ar, ia, ja = [], [], []
    try:
        with open(os.path.join(file_path + 'data_files', file_name), 'r') as f:
            for row, line in enumerate(read_matrix_generator(f)):
                for col, value in enumerate(line):
                    if value != 0:
                        ar.append(value)
                        ia.append(row)
                        ja.append(col)
        total_time = time.time() - start_time
        if write_time:
            with open(os.path.join(file_path + 'execution_results', 'execution_time.txt'), 'a') as f:
                f.write('COO\t%s\t%s\t%s\t%.5f\n' % (matrix_size_row, matrix_size_col, density, total_time))
        return ar, ia, ja
    except FileNotFoundError:
        sys.exit("File %s not found" % file_name)


if __name__ == '__main__':
    if len(sys.argv) == 6:
        if sys.argv[1].lower() == 'csr':
            AR1, IA1, JA1 = csr(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], True, True)
        elif sys.argv[1].lower() == 'coo':
            AR2, IA2, JA2 = coo(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], True, True)
    elif len(sys.argv) == 5:
        AR1, IA1, JA1 = csr(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
        AR2, IA2, JA2 = coo(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], True, True)
    else:
        raise UserWarning(
            'Probably wrong input. Expected <algorithm name> <size of rows> <size of cols> <density> <file_id>')
