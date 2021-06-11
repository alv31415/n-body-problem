from math import sqrt
import numpy as np

def ten_norm(ten, axis = 1, sqrt = True):

    if sqrt:
        return np.sqrt(np.sum(ten**2, axis = axis))
    else:
        return np.sum(ten**2, axis = axis)

def vec_cross(vec1, vec2):

    i = vec1[1]*vec2[2] - vec1[2]*vec2[1]
    j = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    k = vec1[0]*vec2[1] - vec1[1]*vec2[0]

    cross = np.array([i,j,k])

    return cross

def mat_cross(mat1, mat2):
    n = len(mat1)
    mat_cross = np.zeros(shape = (n, 3))

    for i in range(n):
        mat_cross[i] = vec_cross(mat1[i], mat2[i])

    return mat_cross