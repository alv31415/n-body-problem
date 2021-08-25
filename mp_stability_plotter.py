import matplotlib.pyplot as plt
from matplotlib import colors
import time as t
import os
from multiprocessing import Pool
import tqdm

from three_body import *
from exceptions import *
from leapfrog_3 import Leapfrog3
from stability_plotter import StabilityPlotter

class MPStabilityPlotter(StabilityPlotter):
    def __init__(self, perturb, n_trials, collision_tolerance, escape_tolerance, steps = 10**4, delta = 10**-2, tolerance = 10**-2, adaptive_constant = 0.1, delta_lim = 10**-5):
        super().__init__(perturb, n_trials, collision_tolerance, escape_tolerance, steps, delta, tolerance, adaptive_constant, delta_lim)

    def get_stability_cell(self, coords):

        row, col = coords

        n = self.perturb * self.n_trials

        # the amount by which y component of velocity is changed
        dvy = n - row * self.perturb

        # the amount by which x component of velocity is changed
        dvx = -n + col * self.perturb

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
                    return 1
                else:
                    return 0

            except(SmallAdaptiveDeltaException,
                   COMNotConservedException,
                   LinearMomentumNotConservedException,
                   BodyEscapeException,
                   BodyCollisionException,
                   AngularMomentumNotConservedException,
                   EnergyNotConservedException) as e:

                # set matrix entry according to error
                return self.get_error_score(e, integrator.times[-1])
        except (Figure8InitException,
                SmallAdaptiveDeltaException) as e:

            # set matrix entry according to error
            return self.exception_dict[e.__class__.__name__]

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
        args = []

        n = 2 * self.n_trials + 1

        for i in range(n):
            for j in range(n):
                args.append((i, j))

        t0 = t.time()

        n_cpus = os.cpu_count()

        with Pool(n_cpus) as pool:
            results = list(tqdm.tqdm(pool.imap(func = self.get_stability_cell, iterable = args), total = n*n))

        stability_matrix = np.array(results).reshape((n,n))

        t1 = t.time()

        print(f"{n} x {n} Stability Matrix Calculated in {t1 - t0}s")

        return stability_matrix