import time
import multiprocessing as mp
import os


def __read_file(file_name):
    with open(os.path.join('../data_files', file_name), 'r') as f:
        return f.read()


def __process_func(line):
    return tuple([tuple(map(int, line.split('\t')))])[0]


def read_matrix_parallel(file_name, matrix_length='-', density='-', write_time=False,
                         number_process=mp.cpu_count(), file_path='../'):
    start_time = time.time()
    A = __read_file(file_name).split('\n')
    A.pop()
    pool = mp.Pool(number_process)
    result = tuple(pool.map(__process_func, A))
    pool.close()
    if write_time:
        total_time = time.time() - start_time
        print('parallel: ', total_time)
        with open(os.path.join(file_path + 'execution_results', 'read_time.txt'), 'a') as f:
            f.write('parallel\t%s\t%s\t%.5f\n' % (matrix_length, density, total_time))
    return result


def read_matrix_sequentially(file_name, write_time=False, matrix_length='-', density='-'):
    start_time = time.time()
    with open(os.path.join('..data_files', file_name), 'r') as f:
        matrix_result = tuple([tuple(map(int, line.split())) for line in f])
    if write_time:
        total_time = time.time() - start_time
        print('sequential: ', total_time)
        with open(os.path.join('..execution_results', 'read_time.txt'), 'a') as f:
            f.write('sequential\t%s\t%s\t%.5f\n' % (matrix_length, density, total_time))
    return matrix_result


def read_matrix_generator(file):
    while True:
        data = file.readline()
        if not data:
            break
        line = tuple(map(int, data.split()))
        yield line
