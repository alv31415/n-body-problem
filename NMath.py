import numpy as np

# Helper file containing useful mathematical formulae

def ten_norm(ten, axis = 1, sqrt = True):
    """
    Calculates the norm of a tensor, as defined by the norm of each vector component
    :param ten: tensor to calculate norm
    :param axis: the "axis" over which the the norm is calculated. For an n-dimensional tensor, use norm n - 1
    :param sqrt: boolean to indicate whether we return the standard norm (with a square root) or not.
    Useful, since in many cases, the norm needs to be squared anyways
    :return: a lower dimensional (n-1) tensor with the norm calculated
    """

    if sqrt:
        return np.sqrt(np.sum(ten**2, axis = axis))
    else:
        return np.sum(ten**2, axis = axis)

def vec_cross(vec1, vec2):
    """
    Calculates cross product between 2 vectors
    """

    i = vec1[1]*vec2[2] - vec1[2]*vec2[1]
    j = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    k = vec1[0]*vec2[1] - vec1[1]*vec2[0]

    cross = np.array([i,j,k])

    return cross

def mat_cross(mat1, mat2):
    """
    Calculates the cross product between 2 (n x 3) matrices,
    defined as the pairwise cross product of the row vectors of the matrices
    :return: an (n x 3) matrix, with each row being the pairwise cross product of mat1 and mat2
    """
    n = len(mat1)
    mat_cross = np.zeros(shape = (n, 3))

    for i in range(n):
        mat_cross[i] = vec_cross(mat1[i], mat2[i])

    return mat_cross