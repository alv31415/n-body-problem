from math import sqrt
import numpy as np

def vec_norm(vec):
    assert len(vec) == 3, "Require a 3D vector"

    return sqrt(np.sum(vec**2))

def mat_norm(mat):
    n = len(mat)
    mat_norm = np.zeros(n)

    for i in range(n):
        mat_norm[i] = vec_norm(mat[i])

    return mat_norm

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