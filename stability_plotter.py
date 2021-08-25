import matplotlib.pyplot as plt
from matplotlib import colors
import time as t
import os

from three_body import *
from exceptions import *
from leapfrog_3 import Leapfrog3

class StabilityPlotter():
    def __init__(self, perturb, n_trials, collision_tolerance, escape_tolerance, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1, delta_lim = 10**-5):
        self.perturb = perturb
        self.n_trials = n_trials
        self.collision_tolerance = collision_tolerance
        self.escape_tolerance = escape_tolerance
        self.steps = steps
        self.delta = delta
        self.run_time = steps * delta
        self.tolerance = tolerance
        self.adaptive_constant = adaptive_constant
        self.delta_lim = delta_lim

        # encode errors as numbers
        self.exception_dict = {"SmallAdaptiveDeltaException": 2,
                              "COMNotConservedException": 3,
                              "BodyEscapeException": 4,
                              "BodyCollisionException": 5,
                              "Figure8InitException": 6,
                              "LinearMomentumNotConservedException": 7,
                              "AngularMomentumNotConservedException": 8,
                              "EnergyNotConservedException": 9}

    def get_error_score(self, exception, time_elapsed):

        addon = time_elapsed/self.run_time

        if addon == 1:
            addon -= 10**-4

        return self.exception_dict[exception.__class__.__name__] + addon

    def get_stability_matrix(self):
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

        n = 2 * self.n_trials + 1

        # initialise stability matrix
        stability_matrix = np.zeros(shape=(n, n))

        # the amount by which y component of velocity is changed
        dvy = self.perturb * self.n_trials

        t0 = t.time()
        for i in range(n):
            # the amount by which x component of velocity is changed
            dvx = -self.perturb * self.n_trials
            for j in range(n):
                print(f"{i},{j}")
                # initialise perturbed figure of 8
                try:
                    # check for potential exceptions (either Figure of 8 or adaptive delta) during initialisation
                    nbody = get_figure_8(-0.5 * np.array([-0.93240737 + dvx, -0.86473146 + dvy, 0]), -0.24308753,
                                         collision_tolerance=self.collision_tolerance, escape_tolerance=self.escape_tolerance)

                    integrator = Leapfrog3(nbody, steps=self.steps, delta=self.delta, tolerance=self.tolerance, adaptive=True,
                                           c=self.adaptive_constant, store_properties=False, delta_lim=self.delta_lim)

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
                        stability_matrix[i, j] = self.get_error_score(e, integrator.times[-1])
                except (Figure8InitException,
                        SmallAdaptiveDeltaException) as e:

                    # set matrix entry according to error
                    stability_matrix[i, j] = self.exception_dict[e.__class__.__name__]

                dvx += self.perturb
            dvy -= self.perturb

        t1 = t.time()

        print(f"{n} x {n} Stability Matrix Calculated in {t1 - t0}s")

        return stability_matrix

    def plot_stability_matrix(self, n_ticks = 10, grad = False, show = True, save_fig = False, **kwargs):
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
        stability_matrix = self.get_stability_matrix()

        n = self.n_trials*self.perturb

        # set up the figure and plot the matrix, with numbers giving pixel values
        fig, ax = plt.subplots()

        if grad:
            cmap = plt.get_cmap("nipy_spectral")
            cax = ax.imshow(stability_matrix,
                            extent=(-n - self.perturb * 0.5, n + self.perturb * 0.5, -n - self.perturb * 0.5, n + self.perturb * 0.5),
                            cmap=cmap, vmin=0, vmax=10)
        else:
            cmap = plt.get_cmap("viridis")
            # since errors are discrete numbers, use this for the cmap
            norm = colors.BoundaryNorm(np.arange(-0.5, 10, 1), cmap.N)

            cax = ax.imshow(stability_matrix,
                            extent=(-n - self.perturb * 0.5, n + self.perturb * 0.5, -n - self.perturb * 0.5, n + self.perturb * 0.5),
                            norm=norm, cmap=cmap, vmin=0, vmax=9)

        # set plot properties
        ax.set_xlabel(r"$\Delta v_x$")
        ax.set_ylabel(r"$\Delta v_y$")
        ax.set_title("Stability of Figure 8 Under Perturbations", pad=20)

        ax.set_xticks(np.arange(-n, n + self.perturb, step=2 * n / n_ticks))
        ax.set_yticks(np.arange(-n, n + self.perturb, step=2 * n / n_ticks))

        # show a colorbar
        cb = plt.colorbar(cax, ticks = range(0,10))
        cb.set_label("Error Type", labelpad=20)

        plt.tight_layout()

        # save the plot
        if save_fig and "fig_name" in kwargs:
            if kwargs["fig_name"] is None:
                int_to_string = lambda x: str(x).replace(".", "_")
                save_string = f"../imgs/stability{2*self.n_trials + 1}-perturb{int_to_string(self.perturb)}-time{int(self.steps*self.delta)}-AC{int_to_string(self.adaptive_constant)}-DL{int_to_string(self.delta_lim)}"
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

        if show:
            plt.show()