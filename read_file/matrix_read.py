import multiprocessing as mp
import os
import sys
import time


def __read_file(file_name, file_path):
    """
    :param file_name: string
    :param file_path: string
    ----------------------
    :return: whole file read
    """
    try:
        with open(os.path.join(file_path + 'data_files', file_name), 'r') as f:
            return f.read()
    except FileNotFoundError:
        sys.exit("File %s not found" % file_name)


def __process_func(line):
    """
    :param line: line of the txt file string
     ----------------------
    :return: the line split by tabs
    """
    return tuple([tuple(map(int, line.split('\t')))])[0]


def read_matrix_parallel(file_name, matrix_length_row='-', matrix_length_col='-', density='-', write_time=False,
                         number_process=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param matrix_length_row: int
    :param matrix_length_col: int
    :param density: float
    :param write_time: boolean
    :param number_process: int
    :param file_path: string
    ----------------------
    :return: file's matrix as list of lists
    """
    start_time = time.time()
    file_matrix = __read_file(file_name, file_path).split('\n')
    file_matrix.pop()
    pool = mp.Pool(number_process)
    result = tuple(pool.map(__process_func, file_matrix))
    pool.close()
    if write_time:
        total_time = time.time() - start_time
        if not os.path.exists(file_path + 'execution_results'):
            os.makedirs(file_path + 'execution_results')
        with open(os.path.join(file_path + 'execution_results', 'read_time.txt'), 'a') as f:
            f.write('parallel\t%s\t%s\t%s\t%.5f\n' % (matrix_length_row, matrix_length_col, density, total_time))
    return result


def read_matrix_sequentially(file_name, write_time=False, matrix_length_row='-', matrix_length_col='-', density='-',
                             file_path='../'):
    """
    :param file_name: string
    :param write_time: boolean
    :param matrix_length_row: int
    :param matrix_length_col: int
    :param density: float]
    :param file_path: string
    ----------------------
    :return: file's matrix as list of lists
    """
    start_time = time.time()
    try:
        with open(os.path.join('..data_files', file_name), 'r') as f:
            matrix_result = tuple([tuple(map(int, line.split())) for line in f])
    except FileNotFoundError:
        sys.exit("File %s not found" % file_name)

    if write_time:
        total_time = time.time() - start_time
        if not os.path.exists(file_path + 'execution_results'):
            os.makedirs(file_path + 'execution_results')
        with open(os.path.join(file_path + 'execution_results', 'read_time.txt'), 'a') as f:
            f.write('sequential\t%s\t%s\t%s\t%.5f\n' % (matrix_length_row, matrix_length_col, density, total_time))
    return matrix_result


def read_matrix_generator(file):
    """
    :param file: a file pointer
    ----------------------
    :return: file's line as tuple with integers
    """
    while True:
        data = file.readline()
        if not data:
            break
        line = tuple(map(int, data.split()))
        yield line
