"""
 To run: python3 generator.py <number of rows> <number of columns>
            <density> <file_id> <return_list> <lower_bound> <upper_bound>
 It creates a sparse matrix with <number of rows> of rows and <number of columns> columns. If <return_list> is false,
 then the generated matrix will be written to a file in format
 output_<number of rows>_<number of columns>_<density>_<file_id>.txt
"""
import sys

try:
    from generator_helpers import __generate_matrix, __write_matrix_to_file
except ImportError:
    from .generator_helpers import __generate_matrix, __write_matrix_to_file


def generate_sparse_matrix(first_dimension, second_dimension, density, file_id=1, return_list=True, lower_bound=-1000,
                           upper_bound=100, file_path='../'):
    """
    :param first_dimension: int
    :param second_dimension: int
    :param density: float
    :param file_id: int
    :param lower_bound: int
    :param upper_bound: int
    :param return_list: boolean
    :param file_path: string
    :return: a list

    Helper function that generate a sparse matrix and return it as a list of list or write it to a file
    """
    generated_matrix = __generate_matrix(lower_bound, upper_bound, first_dimension, second_dimension, density)
    if return_list:
        return generated_matrix.toarray()
    else:
        __write_matrix_to_file(str(first_dimension), str(second_dimension), str(density), str(file_id),
                               generated_matrix, file_path=file_path)


if __name__ == '__main__':
    if len(sys.argv) == 8:
        return_list = sys.argv[5].lower() == 'true'
        # in case bounds and boolean variable which return or write the matrix in txt file are given
        generate_sparse_matrix(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
                               return_list, int(sys.argv[6]), int(sys.argv[7]))
    elif len(sys.argv) == 6:
        return_list = sys.argv[5].lower() == 'true'
        # in case bounds are NOT given but boolean variable which return or write the matrix in txt file is given
        generate_sparse_matrix(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]),
                               return_list)
        # generate(11, 12, 0.5, 1)
    else:
        # in case only dimensions, density and file_id are given
        generate_sparse_matrix(int(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), int(sys.argv[4]))
