import numpy as np

import NMath as nm
from NBody import NBody

# ------------------------------ EULER ------------------------------

def get_euler_nbod(r_1: np.array, masses, G = 1):
    """
    Produces an NBody instance with velocities satisfying the Euler 3-Body configuration
    :param r_1: the position of one of the non-central bodies in the configuration
    :param masses: the masses for each of the 3 bodies
    :param G: constant of gravitation
    :return: an NBody instance with velocities satisfying the Euler 3-Body configuration
    """

    # check: position is a vector in R^3 with the y component being non-zero
    assert r_1[1] != 0 and r_1.shape == (3,)
    assert r_1[2] == 0

    # calculate the velocity magnitude from the positions
    velocity_mag = np.sqrt((4*G*masses[0] + G*masses[1]) / (4 * nm.ten_norm(r_1, axis = 0, sqrt = True)))

    # initialise positions, with a body at the origin, and the other 2 bodies equally distanced and collinear
    init_positions = np.array([np.zeros(shape=(3,)), r_1, -r_1])

    # create the velocity array, by making the velocity vector perpendicular to the position
    init_velocity = velocity_mag * np.array([r_1[1], -r_1[0], 0]) / nm.ten_norm(r_1, axis=0, sqrt = True)

    # initialise velocities for simulation
    init_velocities = np.array([[0,0,0], init_velocity, -init_velocity])

    return NBody(init_positions, init_velocities, masses, escape_tolerance=-1)

# ------------------------------ LAGRANGE ------------------------------

def rot_mat(theta):
    """
    A rotation matrix, by angle theta (rad)
    """
    return np.array([[np.cos(theta), np.sin(theta), 0],[-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])

def get_lagrange_nbod(r_1: np.array, masses, G = 1):
    """
    Produces an NBody instance with velocities satisfying the Lagrange 3-Body configuration
    :param r_1: the position of any of the 3 bodies
    :param masses: the masses for each of the 3 bodies
    :param G: constant of gravitation
    :return: an NBody instance with velocities satisfying the Euler 3-Body configuration
    """

    assert r_1[2] == 0

    # initialise rotation matrix, and calculate position vector for the other 2 bodies
    R = rot_mat(2*np.pi/3)
    r_2 = R @ r_1
    r_3 = R @ r_2

    # calculate the gravitational force exerted on the body
    gravitational_force = G * ((masses[1]/nm.ten_norm(r_2 - r_1, axis = 0, sqrt = False)**(1.5))*(r_2 - r_1) +
                               (masses[2]/nm.ten_norm(r_3 - r_1, axis = 0, sqrt = False)**(1.5))*(r_3 - r_1))

    # pseudo-magnitude of centripetal force. Used to obtain the ratio (v/r)^2
    centripetal_mag = -1 * np.divide(gravitational_force, r_1, out=np.zeros_like(gravitational_force), where = r_1 != 0)

    # calculate the magnitude of the velocity vector
    velocity_mag = np.sqrt(centripetal_mag[np.nonzero(centripetal_mag)[0][0]] * nm.ten_norm(r_1, axis=0, sqrt=False))

    # calculate velocity, as a vector perpendicular to r_1
    v_1 = velocity_mag * np.array([r_1[1], -r_1[0], 0])/nm.ten_norm(r_1, axis = 0, sqrt=True)

    # initialise NBody
    init_positions = np.array([r_1, r_2, r_3])
    init_velocities = np.array([v_1, R @ v_1, R @ (R @ v_1)])

    return NBody(init_positions, init_velocities, masses, escape_tolerance=-1)

# ------------------------------ FIGURE 8 ------------------------------

# initial conditions taken from http://homepages.math.uic.edu/~jan/mcs320s07/Project_Two/sol_body.html
r_1 = np.array([0.97000436, -0.24308753, 0])
v_3 = np.array([-0.93240737,-0.86473146, 0])
v_2 = -v_3/2

figure_8 = NBody(np.array([r_1, -r_1, [0, 0, 0]]),
                 np.array([v_2, v_2, v_3]),
                 np.ones(shape = (3,)))