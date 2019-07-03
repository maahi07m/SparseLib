import time
import multiprocessing as mp

CPUS = mp.cpu_count()
# FILE = "output_10000_0.005_1.txt"
FILE = "output23000.txt"


def read_file():
    with open(FILE) as f:
        return f.read()


def process_func(line):
    return tuple([tuple(map(int, line.split('\t')))])[0]


def read_matrix_parallel_4():
    start_time = time.time()
    A = read_file().split('\n')
    A.pop()
    pool = mp.Pool(CPUS)
    result = tuple(pool.map(process_func, A))
    pool.close()
    stop_time = time.time()
    print('parallel: ', stop_time - start_time)
    return result


def read_matrix_sequentially():
    # file_name = 'output_' + sys.argv[1] + '_' + sys.argv[2] + '_' + sys.argv[3] + '.txt'
    file_name = FILE
    start = time.time()
    with open(file_name, 'r') as f:
        A = tuple([tuple(map(int, line.split())) for line in f])
    print(time.time()-start)
    return A


if __name__ == '__main__':
    # A_seq = read_matrix_sequentially()
    A_par4 = read_matrix_parallel_4()
    # print("A_par4 == A_seq ? ", A_par4 == A_seq)
