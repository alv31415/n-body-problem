import numpy as np
from numpy import testing

from NBody import NBody
from Leapfrog3 import Leapfrog3

DP = 12
DP_ANGULAR = 15

STEPS = 10
DELTA = 10e-3
TOLERANCE = 10e-3
C = 0.01
ADAPTIVE = False

init_positions = np.array([[1,2,1],
                           [0,0,0],
                           [-1, -2, -1]])
init_velocities = np.array([[-1,1,1],
                            [1,1,0],
                            [-2, 0, 2]])
masses = np.array([1,3,1])

adjusted_velocities = np.array([[-1, 0.2, 0.4],[1,0.2,-0.6],[-2,-0.8,1.4]])

def test_leapfrog3_step():
    nbod = NBody(init_positions, init_velocities, masses)

    leapfrog = Leapfrog3(nbody = nbod, steps = STEPS, delta = DELTA, tolerance = TOLERANCE, adaptive = ADAPTIVE, c = C)

    assert not leapfrog.integrated

    assert leapfrog.position_orbit.shape == leapfrog.velocity_orbit.shape and leapfrog.position_orbit.shape == (3,10,3)

    testing.assert_array_almost_equal(init_positions, leapfrog.position_orbit[:,0,:], DP)
    testing.assert_array_almost_equal(adjusted_velocities, leapfrog.velocity_orbit[:, 0, :], DP)

    """
    init_acceleration = np.array([[-2/(48*np.sqrt(6)) - 3/(6*np.sqrt(6)), -4/(48*np.sqrt(6)) - 6/(6*np.sqrt(6)), -2/(48*np.sqrt(6)) - 3/(6*np.sqrt(6))],
                                  [0,0,0],
                                  [2/(48*np.sqrt(6)) + 3/(6*np.sqrt(6)), 4/(48*np.sqrt(6)) + 6/(6*np.sqrt(6)), 2/(48*np.sqrt(6)) + 3/(6*np.sqrt(6))]])
    """

    init_acceleration = 13/(24*np.sqrt(6)) * np.array([[-1,-2,-1],
                                  [0, 0, 0],
                                  [1,2,1]])

    testing.assert_array_almost_equal(init_acceleration, leapfrog.acc_t, DP)

    expected_half_velocity_init = np.array([[-1 - DELTA*13/(48 * np.sqrt(6)),
                                             0.2 - DELTA*13/(24 * np.sqrt(6)),
                                             0.4 - DELTA*13/(48 * np.sqrt(6))],
                                            [1,0.2,-0.6],
                                            [-2 + DELTA*13 / (48 * np.sqrt(6)),
                                             -0.8 + DELTA*13 / (24 * np.sqrt(6)),
                                             1.4 + DELTA*13 / (48 * np.sqrt(6))]])

    testing.assert_array_almost_equal(expected_half_velocity_init, leapfrog.half_velocity_orbit[:,0,:], DP)

    leapfrog.integration_step(1)

    """
    expected_new_positions = np.array([[1 + DELTA*(-1 - DELTA*13/(48 * np.sqrt(6))),
                                             2 + DELTA*(0.2 - DELTA*13/(24 * np.sqrt(6))),
                                             1 + DELTA*(0.4 - DELTA*13/(48 * np.sqrt(6)))],
                                            [DELTA*1,DELTA*0.2,DELTA*-0.6],
                                            [-1 + DELTA*(-2 + DELTA*13 / (48 * np.sqrt(6))),
                                             -2 + DELTA*(-0.8 + DELTA*13 / (24 * np.sqrt(6))),
                                             -1 + DELTA*(1.4 + DELTA*13 / (48 * np.sqrt(6)))]])
    """

    expected_new_positions = init_positions + DELTA*expected_half_velocity_init

    testing.assert_array_almost_equal(expected_new_positions, leapfrog.position_orbit[:, 1, :], DP)

    expected_new_acc_t = 0

    expected_new_velocities = expected_half_velocity_init + DELTA*expected_new_acc_t*0.5

    testing.assert_array_almost_equal(expected_new_velocities, leapfrog.velocity_orbit[:, 1, :], DP)

    expected_new_total_energy = 0
    expected_new_angular_momentum = 0
    expected_new_total_angular_momentum = 0