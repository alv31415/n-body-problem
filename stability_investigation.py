import matplotlib.pyplot as plt
from matplotlib import colors
import time as t
import os

from three_body import *
from exceptions import *
from leapfrog_3 import Leapfrog3

def get_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1, delta_lim = 10**-5):
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
    exception_dict = {"SmallAdaptiveDeltaException" : 2,
                      "COMNotConservedException" : 3,
                      "LinearMomentumNotConservedException" : 4,
                      "BodyEscapeException" : 5,
                      "BodyCollisionException" : 6,
                      "AngularMomentumNotConservedException" : 7,
                      "Figure8InitException" : 8,
                      "EnergyNotConservedException" : 9}

    n = 2*n_trials + 1

    # initialise stability matrix
    stability_matrix = np.zeros(shape = (n,n))
    stability_matrix = np.floor(np.random.rand(n,n)*10)

    # the amount by which y component of velocity is changed
    dvy = perturb * n_trials

    t0 = t.time()
    for i in range(n):
        # the amount by which x component of velocity is changed
        dvx = -perturb * n_trials
        for j in range(n):
            print(f"{i},{j}")

            # initialise perturbed figure of 8
            try:
                # check for potential exceptions (either Figure of 8 or adaptive delta) during initialisation
                nbody = get_figure_8(-0.5*np.array([-0.93240737 + dvx, -0.86473146 + dvy, 0]), -0.24308753,
                                collision_tolerance=collision_tolerance, escape_tolerance=escape_tolerance)

                integrator = Leapfrog3(nbody, steps=steps, delta=delta, tolerance=tolerance, adaptive=True,
                                       c=adaptive_constant, store_properties=False, delta_lim = delta_lim)

                # integrate, and catch any exception in the process
                try:
                    integrator.get_orbits()

                    # if adaptive timestep took 10^5 steps (max allowed) set value
                    if integrator.full_run:
                        stability_matrix[i, j] = 1

                except(SmallAdaptiveDeltaException,
                       COMNotConservedException,
                       LinearMomentumNotConservedException,
                       BodyEscapeException,
                       BodyCollisionException,
                       AngularMomentumNotConservedException,
                       EnergyNotConservedException) as e:

                    # set matrix entry according to error
                    stability_matrix[i, j] = exception_dict[e.__class__.__name__]
            except (Figure8InitException,
                    SmallAdaptiveDeltaException) as e:

                # set matrix entry according to error
                stability_matrix[i, j] = exception_dict[e.__class__.__name__]

            dvx += perturb
        dvy -= perturb

    t1 = t.time()

    print(f"{n} x {n} Stability Matrix Calculated in {t1 - t0}s")
                
    return stability_matrix


def plot_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, n_ticks = 10, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1, delta_lim = 10**-5, **kwargs):
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
    stability_matrix = get_stability_matrix(perturb, n_trials, collision_tolerance, escape_tolerance, steps, delta, tolerance, adaptive_constant, delta_lim)

    n = n_trials*perturb

    # set up the figure and plot the matrix, with numbers giving pixel values
    fig, ax = plt.subplots()

    # since errors are discrete numbers, use this for the cmap
    cmap = plt.get_cmap("viridis")
    norm = colors.BoundaryNorm(np.arange(-0.5, 10, 1), cmap.N)

    cax = ax.imshow(stability_matrix, extent=(-n-perturb*0.5, n+perturb*0.5, -n-perturb*0.5, n+perturb*0.5),
                    norm = norm, cmap = cmap, vmin = 0, vmax = 9)

    # set plot properties
    ax.set_xlabel(r"$\Delta v_x$")
    ax.set_ylabel(r"$\Delta v_y$")
    ax.set_title("Stability of Figure 8 Under Perturbations", pad = 20)

    ax.set_xticks(np.arange(-n, n + perturb, step=2 * n / n_ticks))
    ax.set_yticks(np.arange(-n, n + perturb, step=2 * n / n_ticks))

    # show a colorbar
    cb = plt.colorbar(cax, ticks = np.arange(0,10))
    cb.set_label("Error Type", labelpad=20)

    plt.tight_layout()

    # save the plot
    if "save_fig" in kwargs:
        if kwargs["save_fig"] and "fig_name" in kwargs:
            if kwargs["fig_name"] is None:
                int_to_string = lambda x: str(x).replace(".", "_")
                save_string = f"../imgs/stability{2*n_trials + 1}-perturb{int_to_string(perturb)}-time{int(steps*delta)}-AC{int_to_string(adaptive_constant)}-DL{int_to_string(delta_lim)}"
            else:
                save_string = kwargs["fig_name"]

            idx = 2
            filename = save_string
            save_file = filename + ".png"
            # if we are to overwrite a file, check & modify the new file accordingly
            while os.path.exists(save_file):
                filename = save_string + f"({idx})"
                save_file = filename + ".png"
                idx +=1

            plt.savefig(save_file)

    plt.show()