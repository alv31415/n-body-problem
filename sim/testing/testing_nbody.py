import numpy as np
from numpy import testing

from nbody import NBody

DP = 13

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
    test_positions = np.array([[1,1,1],
                              [-1,2,3],
                              [-2,-1,-0.6]])
    # TEST: DISTANCE CALCULATION WITH EXTERIOR ARRAY OF POSITIONS
    expected_distances = np.array([[[0,0,0], [-2,1,2], [-3,-2,-1.6]],
                                   [[2,-1,-2], [0,0,0], [-1,-3, -3.6]],
                                   [[3,2,1.6], [1,3,3.6], [0,0,0]]])

    testing.assert_equal(expected_distances, nbod.get_body_distances(positions = test_positions))
    testing.assert_raises(AssertionError, testing.assert_equal, expected_distances, nbod.distances)

    # TEST: DISTANCE CALCULATION WITH COLLISION
    collision_positions = np.array([[1,1,1], [1.1, 1.1, 1.1]])
    nbod.collision_tolerance = 1
    testing.assert_raises(AssertionError, nbod.get_body_distances, collision_positions)
    nbod.collision_tolerance = 10e-10
    nbod.get_body_distances(positions = collision_positions)

def test_nbody_get_acceleration():
    test_positions = np.array([[1, 1, 1],
                               [-1, 2, 3],
                               [-2, -1, -0.6]])

    # TEST: ACCELERATION WITHIN SIMULATION
    expected_acceleration = np.array([[-2*(3**(-3/2)) - 6*(5**(-3/2)), 2*(3**(-3/2)), -2*(3**(-3/2)) + 3*(5**(-3/2))],
                                      [1*(3**(-3/2)) - 3*(6**(-3/2)), -1*(3**(-3/2)) - 3*(6**(-3/2)), 1*(3**(-3/2)) + 6*(6**(-3/2))],
                                      [2*(5**(-3/2)) + 2*(6**(-3/2)), 2*(6**(-3/2)), -1*(5**(-3/2)) - 4*(6**(-3/2))]])
    testing.assert_array_almost_equal(expected_acceleration, nbod.get_acceleration(), DP)

    # TEST: ACCELERATION OUTSIDE SIMULATION
    test_expected_acceleration = np.array([[-4*9**(-3/2) - 9*15.56**(-3/2), 2*9**(-3/2) - 6*15.56**(-3/2), 4*9**(-3/2) - 4.8*15.56**(-3/2)],
                                           [2*9**(-3/2) - 3*22.96**(-3/2), -1*9**(-3/2) - 9*22.96**(-3/2), -2*9**(-3/2) - 10.8*22.96**(-3/2)],
                                           [3*15.56**(-3/2) + 2*22.96**(-3/2), 2*15.56**(-3/2) + 6*22.96**(-3/2), 1.6*15.56**(-3/2) + 7.2*22.96**(-3/2)]])
    testing.assert_array_almost_equal(test_expected_acceleration, nbod.get_acceleration(positions = test_positions), DP)

def test_nbody_conserved_quantity():
    # TEST: CONSERVE SCALAR
    assert nbod.conserved_quantity(23,23.0001,10e-3)
    assert not nbod.conserved_quantity(23, 23.01, 10e-3)

    # TEST: CONSERVE VECTOR
    assert nbod.conserved_quantity(np.array([12.65, 13.8, 12.00002]), np.array([12.65, 13.8, 11.999999]), 10e-4)
    assert not nbod.conserved_quantity(np.array([12.65, 13.8, 12.00002]), np.array([12.65, 13.8, 11.999999]), 10e-8)

def test_nbody_update_symp():
    energy = nbod.energy
    kinetic_energy = nbod.kinetic_energy
    gpe = nbod.gpe
    linear_momentum = nbod.linear_momentum
    total_linear_momentum = nbod.total_linear_momentum
    angular_momentum = nbod.angular_momentum
    total_angular_momentum = nbod.total_angular_momentum

    positions = nbod.positions
    velocities = nbod.velocities
    accelerations = nbod.get_acceleration()

    nbod.update(new_positions = positions, new_velocities = velocities, symplectic = True, tolerance = 10e-3)

    testing.assert_equal(energy, nbod.energy)
    testing.assert_equal(kinetic_energy, nbod.kinetic_energy)
    testing.assert_equal(gpe, nbod.gpe)
    testing.assert_equal(linear_momentum, nbod.linear_momentum)
    testing.assert_equal(total_linear_momentum, nbod.total_linear_momentum)
    testing.assert_equal(angular_momentum, nbod.angular_momentum)
    testing.assert_equal(total_angular_momentum, nbod.total_angular_momentum)
    testing.assert_equal(np.abs(accelerations), np.abs(nbod.get_acceleration()))

def test_nbody_update_errors():

    # TEST: ESCAPE TOLERANCE CONDITION FAILS

    nbod_escape = NBody(init_positions = init_positions, init_velocities = init_velocities, masses = masses, escape_tolerance = 1)

    # check that first 2 update conditions are satisfied

    assert (3 == len(init_positions) and 3 == len(init_velocities))

    assert (len(init_positions[0]) == 3 and len(init_velocities[0]) == 3)

    testing.assert_raises(AssertionError, nbod_escape.update, init_positions, init_velocities)

def test_main():
    test_nbody_copy()
    test_nbody_check_update_input()
    test_nbody_init()
    test_nbody_get_body_distances()
    test_nbody_get_acceleration()
    test_nbody_conserved_quantity()
    test_nbody_update_symp()
    test_nbody_update_errors()






