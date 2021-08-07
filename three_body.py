import numpy as np

import NMath as nm
from NBody import NBody

# if x position is not 0, then we lose the Euler property -  we need to have perpendicularity
def get_euler_nbod(position: np.array, masses, G = 1):
    """
    Produces an NBody instance with velocities satisfying the Euler 3-Body configuration
    :param position: the position of one of the non-central bodies in the configuration
    :param masses: the masses for each of the 3 bodies
    :param G: constant of gravitation
    :return: an NBody instance with velocities satisfying the Euler 3-Body configuration
    """

    print(position.shape)

    # check: position is a vector in R^3 with the y component being non-zero
    assert position[1] != 0 and position.shape == (3,)

    # calculate the velocity magnitude from the positions
    velocity = np.sqrt((4*G*masses[0] + G*masses[1])/(4*nm.ten_norm(position, axis = 0, sqrt = True)))

    # initialise positions, with a body at the origin, and the other 2 bodies equally distanced and collinear
    init_positions = np.array([np.zeros(shape=(3,)), position, -position])

    # create the velocity array, with velocity as the x component
    init_velocity = np.array([velocity, 0, 0])

    # initialise velocities for simulation
    init_velocities = np.array([[0,0,0], init_velocity, -init_velocity])

    return NBody(init_positions, init_velocities, masses, escape_tolerance=-1)

def rot_mat(theta):
    return np.array([[np.cos(theta), np.sin(theta), 0],[-np.sin(theta), np.cos(theta), 0], [0, 0, 1]])