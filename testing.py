import numpy as np
from numpy import testing
import NMath as nm
from NBody import NBody

# TESTING FOR NMATH

DP = 6

array_1d = np.array([2,-4,5.2])
array_2d = np.array([[21,1.8,1], [-2.2, -2.4, -2.2]])
array_2d_2 = np.array([[3.7,1.23,-8], [-1.2, -0.4, 2.2]])
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

def test_nmath_mat_cross():
    testing.assert_array_almost_equal(nm.mat_cross(array_2d, array_2d_2), np.array([[-15.63,171.7,19.17], [-6.16,7.48,-2]]), DP)
    rand_1 = np.random.rand(4,3)
    rand_2 = np.random.rand(4,3)
    testing.assert_equal(nm.mat_cross(rand_1, rand_2), np.cross(rand_1, rand_2))

# TESTING FOR NBODY

init_positions = np.array([[1,1,1],
                           [0,2,0],
                           [-1, 1, 2]])
init_velocities = np.array([[-1,1,1],
                            [1,1,0],
                            [-2, 0, 2]])
masses = np.array([1,2,3])

nbod = NBody(init_positions, init_velocities, masses)

def test_nbody_copy():
    nbod2 = nbod.copy()
    testing.assert_equal(nbod.com, nbod2.com)
    nbod2.com = np.array([2,3,4])
    testing.assert_raises(AssertionError, testing.assert_array_equal, nbod.com, nbod2.com)
    nbod2.angular_momentum = np.array([[2, 3, 4],
                                       [2, 3, 4],
                                       [2, 3, 4]])
    testing.assert_raises(AssertionError, testing.assert_array_equal, nbod.angular_momentum, nbod2.angular_momentum)

def test_nbody_check_update_input():
    # TEST: PYTHON ARRAY GIVEN -> CONVERTED TO NUMPY
    arr_positions = [[1,-1,1], [2,4,2], [3,2,1]]
    arr_velocities = [[1, -1, 1], [2, 4, 2], [3, 2, 1]]
    arr_masses = [3, 2, 1]
    nbod_test_init = NBody(arr_positions, arr_velocities, arr_masses)
    assert isinstance(nbod_test_init.positions, np.ndarray)
    testing.assert_equal(np.array(arr_positions) - nbod_test_init.com, nbod_test_init.positions)
    assert isinstance(nbod_test_init.velocities, np.ndarray)
    assert isinstance(nbod_test_init.masses, np.ndarray)

    # TEST: INPUT ARRAYS HAVE DIFFERENT SIZES/SHAPES -> ASSERTION ERROR RAISED
    testing.assert_raises(AssertionError, NBody, arr_positions, arr_velocities, arr_masses[:2])
    testing.assert_raises(AssertionError, NBody, [arr_positions[0]], arr_velocities, arr_masses)
    testing.assert_raises(AssertionError, NBody, [arr_positions[0]], arr_velocities[:2], arr_masses)


def test_nbody_init():
    # check masses
    testing.assert_equal(6, nbod.total_mass)
    testing.assert_equal(np.array([[1], [2], [3]]), nbod.stacked_masses)

    # check COM
    expected_com = np.array([-1/3, 4/3, 7/6])
    testing.assert_equal(expected_com, nbod.com)

    # check COM coordinates
    expected_positions = np.array([[4/3, -1/3, -1/6],
                                    [1/3, 2/3, -7/6],
                                    [-2/3, -1/3, 5/6]])
    testing.assert_array_almost_equal(expected_positions, nbod.positions, DP)

    expected_com_velocity = np.array([-5/6, 1/2, 7/6])
    expected_velocities = np.array([[-1/6, 1/2, -1/6],
                                    [11/6, 1/2, -7/6],
                                    [-7/6, -1/2, 5/6]])
    testing.assert_array_almost_equal(expected_velocities, nbod.velocities, DP)

    # check distances
    expected_distances = np.array([[[0,0,0], [-1,1,-1], [-2,0,1]],
                                   [[1,-1,1], [0,0,0], [-1,-1,2]],
                                   [[2,0,-1],[1,1,-2], [0,0,0]]])
    testing.assert_equal(expected_distances, nbod.distances)

    # check linear momentum
    expected_linear_momentum = np.array([[-1/6, 1/2, -1/6],
                                         [11/3, 1, -7/3],
                                         [-7/2, -3/2, 5/2]])
    testing.assert_array_almost_equal(expected_linear_momentum, nbod.linear_momentum, DP)

    expected_total_linear_momentum = np.array([0,0,0])
    testing.assert_array_almost_equal(expected_total_linear_momentum, nbod.total_linear_momentum, DP)

    # check angular momentum
    expected_angular_momentum = np.array([[5/36, 1/4, 11/18],
                                         [-7/18, -7/2, -19/9],
                                         [5/12, -5/4, -1/6]])
    testing.assert_array_almost_equal(expected_angular_momentum, nbod.angular_momentum, DP)

    expected_total_angular_momentum = np.array([1/6, -9/2, -5/3])
    testing.assert_array_almost_equal(expected_total_angular_momentum, nbod.total_angular_momentum, DP)

    # check energy
    expected_kinetic_energy = 11/72 + 179/36 + 83/24
    testing.assert_equal(expected_kinetic_energy, nbod.kinetic_energy)

    expected_gpe = -1*(2/np.sqrt(3) + 3/np.sqrt(5) + 6/np.sqrt(6))
    testing.assert_equal(expected_gpe, nbod.gpe)

    testing.assert_equal(expected_kinetic_energy + expected_gpe, nbod.energy)

def test_nbody_get_body_distances():
    pass

def test_nbody_get_acceleration():
    pass

def test_nbody_conserved_quantity():
    pass

def test_nbody_update():
    pass