import matplotlib.pyplot as plt
import time as t

from three_body import *
from exceptions import *
from leapfrog_3 import Leapfrog3

def get_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1):
    """
    Perturbs Figure 8 orbit, producing a matrix outlining stability regions
    :param perturb: the amount by which velocity (in x and y directions) is perturbed at each iteration
    :param n_trials: the number of times that which we perturb the orbit to one side of 0.
                     Overall, will lead to a stability matrix of size (2*n_trials + 1 x 2*n_trials + 1)
    :param collision_tolerance: maximum distance between 2 bodies allowed before ending simulation
    :param escape_tolerance: maximum distance away from the centre of mass (COM) allowed before ending simulation
    :return: a (2*n_trials + 1 x 2*n_trials + 1), with numbers rnaging from 0 to 7, dependent on how the simulation ended.
             0 indicates that the simulation ran to completion without errors.
    """

    # encode errors as numbers
    exception_dict = {"SmallAdaptiveDeltaException" : 1,
                      "COMNotConservedException" : 2,
                      "LinearMomentumNotConservedException" : 3,
                      "BodyEscapeException" : 4,
                      "BodyCollisionException" : 5,
                      "AngularMomentumNotConservedException" : 6,
                      "EnergyNotConservedException" : 7}

    n = 2*n_trials + 1

    # initialise stability matrix
    stability_matrix = np.zeros(shape = (n,n))

    # the amount by which y component of velocity is changed
    dvy = perturb * n_trials

    t0 = t.time()
    for i in range(n):
        # the amount by which x component of velocity is changed
        dvx = -perturb * n_trials
        dvy -= perturb
        for j in range(n):
            print(f"{i},{j}")
            dvx += perturb

            # initialise perturbed figure of 8
            nbody = get_figure_8(-0.5*np.array([-0.93240737 + dvx, -0.86473146 + dvy, 0]), -0.24308753,
                                collision_tolerance=collision_tolerance, escape_tolerance=escape_tolerance)

            integrator = Leapfrog3(nbody, steps = steps, delta = delta, tolerance=tolerance, adaptive=True, c=adaptive_constant, store_properties=False)

            # integrate, and catch any exception in the process
            try:
                integrator.get_orbits()

                # if adaptive timestep took 10^5 steps (max allowed) set value
                if integrator.full_run:
                    stability_matrix[i, j] = 8
            except(SmallAdaptiveDeltaException,
                   COMNotConservedException,
                   LinearMomentumNotConservedException,
                   BodyEscapeException,
                   BodyCollisionException,
                   AngularMomentumNotConservedException,
                   EnergyNotConservedException) as e:

                # set matrix entry according to error
                stability_matrix[i,j] = exception_dict[e.__class__.__name__]

    t1 = t.time()

    print(f"{n} x {n} Stability Matrix Calculated in {t1 - t0}s")
                
    return stability_matrix


def plot_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, n_ticks = 10, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1):
    """
    Plots a stability matrix given the parameters
    :param perturb: the amount by which velocity (in x and y directions) is perturbed at each iteration
    :param n_trials: the number of times that which we perturb the orbit to one side of 0.
                     Overall, will lead to a stability matrix of size (2*n_trials + 1 x 2*n_trials + 1)
    :param collision_tolerance: maximum distance between 2 bodies allowed before ending simulation
    :param escape_tolerance: maximum distance away from the centre of mass (COM) allowed before ending simulation
    :param n_ticks: the number of ticks to use in the plot
    """

    # calculate stability matrix
    stability_matrix = get_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, steps, delta, tolerance, adaptive_constant)

    n = n_trials*perturb

    # set up the figure and plot the matrix, with numbers giving pixel values
    fig, ax = plt.subplots()
    cax = ax.imshow(stability_matrix, extent=(-n, n, -n, n))

    # set plot properties
    ax.set_xlabel(r"$\Delta v_x$")
    ax.set_ylabel(r"$\Delta v_y$")
    ax.set_title("Stability of Figure 8 Under Perturbations", pad = 20)

    ax.set_xticks(np.arange(-n, n + perturb, step=2 * n / n_ticks))
    ax.set_yticks(np.arange(-n, n + perturb, step=2 * n / n_ticks))

    cb = plt.colorbar(cax, ax = ax)
    cb.set_label("Colorbar Label", labelpad = 20)

    plt.tight_layout()
    plt.show()