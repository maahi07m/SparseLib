"""This script calculate the addition and subtraction of two matrices compressed in csr or csc format and return the
    results.
"""
import sys
from functools import singledispatch

sys.path.append('../')
from read_file.read_hb_format import read_file

try:
    from addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc
    from addition_subtraction_numpy import *
except ImportError:
    from .addition_subtraction_algorithm import addition_algorithm_csr, subtraction_algorithm_csr, \
        addition_algorithm_csc, subtraction_algorithm_csc
    from .addition_subtraction_numpy import *


@singledispatch
def csr_addition_matrices_hb(matrix_1: list, matrix_2: list):
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)
    cr, ic, jc = addition_algorithm_csr(ar, ia, ja, br, ib, jb)
    return cr, ic, jc


@csr_addition_matrices_hb.register
def _csr_addition_matrices_hb(file_name_1: str, file_name_2: str):
    matrix_1 = read_file(file_name=file_name_1, return_list=True)
    matrix_2 = read_file(file_name=file_name_2, return_list=True)
    ar, ia, ja = csr(matrix_1)
    if matrix_1 == matrix_2:
        br, ib, jb = ar, ia, ja
    else:
        br, ib, jb = csr(matrix_2)
    cr, ic, jc = addition_algorithm_csr(ar, ia, ja, br, ib, jb)
    return cr, ic, jc
