# To run: python3 generator.py <number of rows> <number of cols> <density>
# It creates a sparse matrix with <number> of rows and columns
import time
import sys
import os
import numpy as np
from scipy.sparse import random


def get_user_input():
    will_bounds = input('Do you want to give the bounds for the matrix? Y/n \n')
    if will_bounds.lower() == 'y':
        while True:
            lb = input('Give the lower bounds\n')
            ub = input('Give the upper bounds\n')
            if not lb.isnumeric() or not ub.isnumeric():
                print("Wrong input. Bounds must be numeric. Please try again")
                continue
            if int(lb) > int(ub):
                print("The given lower bound is higher that the upper bound. Please try again")
                continue
            else:
                lb = int(lb)
                ub = int(ub)
                break
    else:
        lb = -1000
        ub = 1000

    will_size = input('Do you want to give matrix\'s number of rows and columns? Y/n \n')
    if will_size.lower() == 'y':
        while True:
            m = input('Give the number of rows\n')
            n = input('Give the number of columns\n')
            if not m.isnumeric() or not n.isnumeric():
                print("Wrong input. Rows and columns must be numeric. Please try again")
                continue
            else:
                m = int(m)
                n = int(n)
                break
    else:
        m = 100
        n = 100

    will_density = input('Do you want to give matrix\'s density? Y/n \n')
    if will_density.lower() == 'y':
        while True:
            dens = input('Give the density\n')
            try:
                dens = float(dens)
                break
            except ValueError:
                print("Wrong input. Density must be numeric. Please try again")
                continue
    else:
        dens = 0.1

    return lb, ub, m, n, dens


def generate_sparse_matrix(lb, ub, m, n, dens):
    # np.random.seed(2)
    np.random.seed(int(time.time()))
    temp_matrix = random(m, n, format='csr', density=dens)
    generated_matrix = np.round((ub-lb + 1)*temp_matrix + lb*temp_matrix.ceil())
    return generated_matrix


def write_matrix_to_file(lower_bound, upper_bound, first_dimension, second_dimension, density, id, matrix, file_path):
    # file_name = 'output' + str(lb) + "_" + str(ub) + "_" + str(m) + "_" + str(n) + ".txt"
    file_name = 'output_' + first_dimension + '_' + second_dimension + '_' + density + '_' + id + '.txt'
    matrix = matrix.toarray()
    with open(os.path.join(file_path+'data_files', file_name), 'w') as f:
        for item in matrix:
            for index,inner in enumerate(item):
                if index == item.shape[0] - 1:
                    f.write("%s" % str(int(inner)), )
                else:
                    f.write("%s\t" % str(int(inner)), )
            f.write("\n")


def generate(first_dimension, second_dimension, density, file_id, lower_bound=-1000, upper_bound=100, file_path='../'):
    # lb, ub, m, n, dens = get_user_input()
    # generated_matrix = generate_sparse_matrix(lb, ub, m, n, dens)
    # lb, ub, m, n, dens = -1000, 1000,100,100
    generated_matrix = generate_sparse_matrix(lower_bound, upper_bound, first_dimension, second_dimension, density)
    write_matrix_to_file(lower_bound, upper_bound, str(first_dimension), str(second_dimension), str(density),
                         str(file_id), generated_matrix, file_path=file_path)
    # print(generated_matrix.A)


if __name__ == '__main__':
    if len(sys.argv) == 7:
        generate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6]))
    else:
        generate(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
