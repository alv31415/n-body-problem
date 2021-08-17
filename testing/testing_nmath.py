import numpy as np
from numpy import testing
import nmath as nm

DP = 13

array_1d = np.array([2,-4,5.2])
array_2d = np.array([[21,1.8,1], [-2.2, -2.4, -2.2]])
array_2d_2 = np.array([[3.7,1.23,-8], [-1.2, -0.4, 2.2]])
array_3d = np.array([[[1,1,1.4], [0.9, 0.8, 0.1]], [[-2.2, -2.4, -2.2], [0.9, 0.8, 0.1]]])

def test_ten_norm():
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

def test_vec_cross():
    vec1 = array_2d[0]
    vec2 = array_2d[1]

    testing.assert_equal(nm.vec_cross(vec1, vec2), np.cross(vec1, vec2))
    testing.assert_equal(nm.vec_cross(vec2, vec1), np.cross(vec2, vec1))
    testing.assert_array_almost_equal(nm.vec_cross(vec1, vec2), np.array([-1.56, 44, -46.44]))

def test_mat_cross():
    testing.assert_array_almost_equal(nm.mat_cross(array_2d, array_2d_2), np.array([[-15.63,171.7,19.17], [-6.16,7.48,-2]]), DP)
    rand_1 = np.random.rand(4,3)
    rand_2 = np.random.rand(4,3)
    testing.assert_equal(nm.mat_cross(rand_1, rand_2), np.cross(rand_1, rand_2))

def test_perc_change():
    testing.assert_array_almost_equal(nm.perc_change(5, np.array([5,-7,8,10.5])), np.array([0,2.4,0.6,1.1]), DP)
    testing.assert_almost_equal(nm.perc_change(5,5.832747327), 0.1665494654, DP)
    testing.assert_array_almost_equal(nm.perc_change(5, np.array([5, -7, 8, 10.5]), perc = True), np.array([0, 240, 60, 110]), DP)

def test_variable_delta():
    testing.assert_equal(nm.variable_delta(np.array([array_1d]), np.array([array_1d]), c = -1), -1)

    easy_positions = np.array([[1,1,1], [2,2,2]])
    easy_velocities = np.array([[1, 2, 1], [0, 2, -2.5]])
    testing.assert_almost_equal(nm.variable_delta(easy_positions, easy_velocities, c = 0.5), np.sqrt(3/53), DP)
    testing.assert_almost_equal(nm.variable_delta(easy_positions, easy_velocities, c = 0.5), 0.23791547571544322, DP)

def test_main():
    test_ten_norm()
    test_vec_cross()
    test_mat_cross()
    test_perc_change()
    test_variable_delta()