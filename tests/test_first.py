import sys
sys.path.append('../')
try:
    from helpers.generator import generate_sparse_matrix
except:
    from helpers.generator import generate_sparse_matrix

def test_generator_call():
    matrix = generate_sparse_matrix(4, 4, 0.5,)
    assert type(matrix) == list

print('asd')