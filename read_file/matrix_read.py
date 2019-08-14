import multiprocessing as mp
import os
import sys


def __read_file(file_name, file_path):
    """
    :param file_name: string
    :param file_path: string
    :return: the file
    """
    try:
        with open(os.path.join(file_path + 'data_files', file_name), 'r') as f:
            return f.read()
    except FileNotFoundError:
        sys.exit("File %s not found" % file_name)


def __process_func(line):
    """
    :param line: a line from the file
    :return: the line split
    """
    return tuple([tuple(map(float, line.split()))])[0]


def read_matrix_parallel(file_name, processes_number=mp.cpu_count(), file_path='../'):
    """
    :param file_name: string
    :param processes_number: int
    :param file_path: string
    :return: file's matrix as list of lists
    """
    file_matrix = __read_file(file_name, file_path).split('\n')
    file_matrix.pop()
    pool = mp.Pool(processes_number)
    result = tuple(pool.map(__process_func, file_matrix))
    pool.close()

    return result
