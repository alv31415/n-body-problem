import numpy as np
import warnings

# Helper file containing useful mathematical functions for calculations

def ten_norm(ten, axis = 1, sqrt = True):
    """
    Calculates the norm of a tensor, as defined by the norm of each vector component
    The norm being the square root of the sum of the squares of each component of the tensor
    :param ten: tensor to calculate norm
    :param axis: the "axis" over which the the norm is calculated. For an n-dimensional tensor, use norm n - 1
    :param sqrt: boolean to indicate whether we return the standard norm (with a square root) or not.
    :return: a lower dimensional (n-1) tensor with the norm calculated
    """

    if sqrt:
        return np.sqrt(np.sum(ten**2, axis = axis))
    else:
        return np.sum(ten**2, axis = axis)

def vec_cross(vec1, vec2):
    """
    Calculates cross product between 2 vectors
    """

    i = vec1[1]*vec2[2] - vec1[2]*vec2[1]
    j = vec1[2] * vec2[0] - vec1[0] * vec2[2]
    k = vec1[0]*vec2[1] - vec1[1]*vec2[0]

    cross = np.array([i,j,k])

    return cross

def mat_cross(mat1, mat2):
    """
    Calculates the cross product between 2 (n x 3) matrices,
    Defined as the pairwise cross product of the row vectors of the matrices
    :return: an (n x 3) matrix, with each row being the pairwise cross product of mat1 and mat2
    """

    n = len(mat1)
    mat_cross = np.zeros(shape = (n, 3))

    for i in range(n):
        mat_cross[i] = vec_cross(mat1[i], mat2[i])

    return mat_cross

def perc_change(initial, values, perc = False, init_val = 1):
    """
    Calculates absolute percentage/decimal change between the initial value and either a single value or a series of values
    :param initial: either a single value, or an array of values
    :param values: the values to be compared against initial to calculate percentage change
    :param perc: if True, the change is given as a percentage; otherwise as a decimal
    :param init_val: initial value when calculating percentages, should initial be 0/array of 0s
    :return: the percentage (as decimal or percentage) change between values and initial, in absolute terms
    """

    # check if initial is an array of values
    if isinstance(initial, np.ndarray) and (initial == 0).all():
        warnings.warn(f"The initial quantity was all 0, so percentage change is meaningless!. Comparing with baseline value: {init_val}",
                          category = RuntimeWarning)
        initial = np.ones_like(initial)*init_val
    elif (initial == 0):
        warnings.warn(f"The initial quantity was all 0, so percentage change is meaningless!. Comparing with baseline value: {init_val}",
                category=RuntimeWarning)
        initial = init_val

    change = np.abs((values - initial) / initial)

    # calculate percentage if required
    if perc:
        return change * 100

    return change

def variable_delta(positions, velocities, c, delta_lim = 10e-8):
    """
    Calculates variable delta for the system
    :param positions: positions of bodies in the system
    :param velocities: velocities of bodies in the system
    :param c: constant resizing factor for variable delta
    :param delta_lim: smallest value allowed for the variable delta
    :return: the calculated variable delta for the system
    """

    # check: positions and velocities are of the same size
    n = len(positions)

    assert n == len(velocities)

    # if only 1 body, then variable delta is the ratio of position magnitude to velocity magnitude, multiplied by c
    if n == 1:
        delta_x = ten_norm(positions[0], sqrt = True, axis = 0)
        delta_v = ten_norm(velocities[0], sqrt=True, axis=0)
        return c*delta_x/delta_v

    # create an (n x n) array to hold all calculated deltas for the system
    potential_deltas = np.ones(shape = (n, n))*np.inf

    # fill potential deltas with the ratio of position magnitude to velocity magnitude
    for i in range(n):
        for j in range(i):
                delta_x = ten_norm((positions[i] - positions[j]), sqrt = True, axis = 0)
                delta_v = ten_norm((velocities[i] - velocities[j]), sqrt = True, axis = 0)
                # entry (i,j) will be the same as (j,i) as we just consider magnitudes
                potential_deltas[i, j] = np.divide(delta_x, delta_v, where = delta_v != 0)
                potential_deltas[j, i] = potential_deltas[i, j]

    # variable delta will be the smallest delta within potential_deltas, multiplied by c
    variable_delta = c*np.amin(potential_deltas)

    # check; if delta is provided, ensure that the calculated variable delta does not become smaller than the minimum allowed
    if delta_lim is not None:
        assert variable_delta > 10e-8, f"Adaptive delta was made too small ({variable_delta}) - orbit unfeasible"

    return variable_delta

