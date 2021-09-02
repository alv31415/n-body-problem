import numpy as np
from numpy import testing

import nmath as nm
from nbody import NBody
from leapfrog_3 import Leapfrog3

DP = 15

STEPS = 10
DELTA = 10**-2
TOLERANCE = 10**-3
C = 0.01
ADAPTIVE = False

init_positions = np.array([[0,1,0], [0,-1,0]])
init_velocities = np.array([[0.4,0,0], [-0.4,0,0]])
masses = np.array([1,1])

def test_leapfrog3_init():
    nbod = NBody(init_positions, init_velocities, masses)

    leapfrog = Leapfrog3(nbody = nbod, steps = STEPS, delta = DELTA, tolerance = TOLERANCE, adaptive = ADAPTIVE, adaptive_constant= C)

    assert not leapfrog.integrated

    assert leapfrog.position_orbit.shape == leapfrog.velocity_orbit.shape and leapfrog.position_orbit.shape == (2,10,3)

    # TEST: INITIAL VELOCITIES AND POSITIONS SET CORRECTLY
    testing.assert_array_almost_equal(leapfrog.position_orbit[:,0,:], init_positions, DP)
    testing.assert_array_almost_equal(leapfrog.velocity_orbit[:, 0, :], init_velocities, DP)

    # TEST: INITIAL ACCELERATION CALCULATED CORRECTLY
    init_acceleration = np.array([[0,-0.25, 0],
                                 [0,0.25, 0]])

    testing.assert_array_almost_equal(leapfrog.acc_t, init_acceleration, DP)

    # TEST: INITIAL ANGULAR MOMENTUM CALCULATED CORRECTLY
    init_total_amomentum = np.array([0,0,-0.8])

    testing.assert_array_almost_equal(leapfrog.nbody.total_angular_momentum, init_total_amomentum, DP)

    # TEST: INITIAL TOTAL ENERGY CALCULATED CORRECTLY
    init_kinetic_energy = 0.16
    init_gpe = -0.5

    init_total_energy = -0.34

    testing.assert_array_almost_equal(leapfrog.nbody.energy, init_total_energy, DP)

def test_leapfrog3_step():
    nbod = NBody(init_positions, init_velocities, masses)

    leapfrog = Leapfrog3(nbody=nbod, steps=STEPS, delta=DELTA, tolerance=TOLERANCE, adaptive=ADAPTIVE, adaptive_constant=C)

    leapfrog.integration_step(1)

    # TEST: POSITION CALCULATED CORRECTLY
    expected_new_positions = np.array([[0.4*DELTA, 1 - DELTA*DELTA*0.25*0.5, 0],
                                       [-0.4*DELTA, -1 + DELTA*DELTA*0.25*0.5, 0]])
    # [[0.004, 0.9999875, 0], [-0.004, -0.9999875, 0]]

    # TEST: ACCELERATION BASED ON NEW POSITIONS CALCULATED CORRECTLY
    testing.assert_array_almost_equal(leapfrog.position_orbit[:, 1, :], expected_new_positions, DP)

    position_vec = np.array([-0.8*DELTA, -2 + DELTA*DELTA*0.25, 0]) # [-0.008, -1.999975]
    position_vec_mag = np.sqrt(4 - 0.36*DELTA*DELTA + 0.0625*DELTA*DELTA*DELTA*DELTA) # 1.99999100013600061

    testing.assert_almost_equal(nm.ten_norm(position_vec, axis = 0, sqrt = True), position_vec_mag, DP)

    expected_new_acc_t = np.array([position_vec, -position_vec])/(position_vec_mag**3)
    # [[-0.004000017999809, -0.999991999896, 0], [0.004000017999809, 0.999991999896, 0]]

    testing.assert_almost_equal(leapfrog.acc_t, expected_new_acc_t, DP)

    # TEST: VELOCITIES BASED ON HALF-VELOCITY AND NEW ACCELERATION CALCULATED CORRECTLY
    expected_new_velocities = np.array([[0.4*(1 - (DELTA*DELTA)/(position_vec_mag**3)),
                                         0.25*DELTA*(-0.5 - 4/(position_vec_mag**3) + DELTA*DELTA*0.5/(position_vec_mag**3)),
                                         0],
                                        [-0.4*(1 - (DELTA*DELTA)/(position_vec_mag**3)),
                                         -0.25 * DELTA * (-0.5 - 4 / (position_vec_mag ** 3) + DELTA * DELTA * 0.5 / (position_vec_mag ** 3)),
                                         0]])
    #[[0.3999949999325, -0.0025000012496859, 0], [-0.3999949999325, 0.0025000012496859, 0]]

    testing.assert_array_almost_equal(leapfrog.velocity_orbit[:, 1, :], expected_new_velocities, DP)

    # TEST: Velocities CALCULATED CORRECTLY
    expected_kinetic_energy = 0.16 * (1 - (DELTA*DELTA)/(position_vec_mag**3))**2 \
                              + 0.25**2*DELTA**2*(-0.5 - 4/(position_vec_mag**3) + DELTA*DELTA*0.5/(position_vec_mag**3))**2 # 0.16000224997725
    expected_gpe = -1/position_vec_mag # -0.50000224997613

    expected_new_total_energy = expected_kinetic_energy + expected_gpe #-0.33999999999887

    testing.assert_almost_equal(leapfrog.nbody.kinetic_energy, expected_kinetic_energy, DP)
    testing.assert_almost_equal(leapfrog.nbody.gpe, expected_gpe, DP)
    testing.assert_almost_equal(leapfrog.nbody.energy, expected_new_total_energy, DP)

    # TEST: ANGULAR MOMENTUM CALCULATED CORRECTLY
    expected_new_angular_momentum = np.array([[0,0, -0.4],
                                              [0,0, -0.4]])

    testing.assert_array_almost_equal(leapfrog.nbody.angular_momentum, expected_new_angular_momentum, DP)

    expected_new_total_angular_momentum = np.array([0,0, 2*(-0.4)])

    testing.assert_array_almost_equal(leapfrog.nbody.total_angular_momentum, expected_new_total_angular_momentum, DP)

def test_main():
    test_leapfrog3_init()
    test_leapfrog3_step()