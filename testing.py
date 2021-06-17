import numpy as np
from numpy import testing
import NMath as nm

# TESTING FOR NMATH

DP = 6

array_1d = np.array([2,-4,5.2])
array_2d = np.array([[21,1.8,1], [-2.2, -2.4, -2.2]])
array_3d = np.array([[[1,1,1.4], [0.9, 0.8, 0.1]], [[-2.2, -2.4, -2.2], [0.9, 0.8, 0.1]]])

def test_nmath_ten_norm():
    # 1D
    testing.assert_equal(nm.ten_norm(array_1d, axis = 0, sqrt = True), np.linalg.norm(array_1d))
    testing.assert_almost_equal(nm.ten_norm(array_1d, axis=0, sqrt=False), 47.04, DP)
    # 2D
    testing.assert_equal(nm.ten_norm(array_2d, axis=1, sqrt=True), np.linalg.norm(array_2d, axis = 1))
    testing.assert_equal(nm.ten_norm(array_2d, axis=0, sqrt=True), np.linalg.norm(array_2d, axis=0))
    testing.assert_array_almost_equal(nm.ten_norm(array_2d, axis=1, sqrt=False), np.array([445.24, 15.44]), DP)
    # 3D
    testing.assert_equal(nm.ten_norm(array_3d, axis=2, sqrt=True), np.linalg.norm(array_3d, axis = 2))
    testing.assert_array_almost_equal(nm.ten_norm(array_3d, axis=2, sqrt=False),
                                      np.array([[3.96, 1.46], [15.44, 1.46]]), DP)

def test_nmath_vec_cross():
    vec1 = array_2d[0]
    vec2 = array_2d[1]

    testing.assert_equal(nm.vec_cross(vec1, vec2), np.cross(vec1, vec2))
    testing.assert_equal(nm.vec_cross(vec2, vec1), np.cross(vec2, vec1))
    testing.assert_array_almost_equal(nm.vec_cross(vec1, vec2), np.array([-1.56, 44, -46.44]))

def test_nmath_vec_cross():
    

# TESTING FOR NBODY