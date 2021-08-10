import numpy as np

import NMath as nm
from OrbitPlotter import OrbitPlotter

class Integrator:
    """
    Class defining a general integrator, acting as a "superclass" for Euler, Euler-Cromer and all Leapfrog methods
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        """
        :param nbody: NBody instance which we integrate
        :param steps: the number of steps to integrate for
        :param delta: timestep to use for the integrator. Smaller timesteps lead to more accurate orbits.
        :param tolerance: allowed absolute error for determining conservation of calculated quantities
        :param adaptive: if True, the Integrator will use an adaptive timestep (instead of a fixed one)
        :param c: constant used when calculating adaptive timestep. Smaller c leads to more accurate orbits.
        """
        self.nbody = nbody

        self.steps = int(steps)

        self.adaptive = adaptive
        self.c = c

        self.tolerance = tolerance

        self.delta = delta

        # creates all arrays used by integrator
        # these hold the positions and velocities of the calculated orbits,
        # alongside the change of quantities which should be conserved if the integrator is symplectic (i.e energy)
        self.set_arrays()

        # the number of steps that the integrator has been run for
        self.int_step = 1

    def integration_step(self, t):
        """
        Overloaded method, dependent on the integration scheme utilised
        """
        pass

    def update_historic(self, t):
        """
        Updates the historic arrays of quantities which should be conserved (i.e energy)
        :param t: the step for which the historic quantites are calculated
        """

        assert t != 0

        self.historic_energy[t] = self.nbody.energy
        self.historic_kinetic_energy[t] = self.nbody.kinetic_energy
        self.historic_gpe[t] = self.nbody.gpe
        self.historic_angular_momentum[t,:] = self.nbody.total_angular_momentum

        if self.adaptive:
            self.historic_delta[t] = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c = self.c)

    def get_orbits(self):
        """
        Performs the integration, by applying the integration step as many times as specified by the initialisation
        If get_orbits has already been executed once, will remove all the previously calculated steps, and calculate new orbits
        """
        # check to see if integration has already been performed
        if self.integrated:
            self.set_arrays()
            self.get_orbits()
        else:
            # integration step until we have done the required steps
            while self.int_step < self.steps:
                self.integration_step(self.int_step)

                # if adaptive timestep is used, recalculate it
                if self.adaptive:
                    self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

            # update flag
            self.integrated = True

    def show_orbits(self, animate = False, seed = 42, animation_steps = 1, twodims = True, grid = False):
        """
        Used to visualise the orbits calculated by the integrator
        :param animate: if True, will produce an animated plot of the orbits
        :param seed: used as seed to generate the colours of the plot
        :param animation_steps: number of steps to consider per frame of animation
        :param twodims: if True, will plot the orbit using 2 dimensions (x and y)
        :param grid: if True, will plot in 2 dimensions,
                     whilst displaying information, such as energy, angular momentum, position and velocity change across time
        """

        assert self.integrated, "No orbits were calculated. Run get_orbits() first!"

        plotter = OrbitPlotter(self, seed = seed, animation_steps = animation_steps, twodims = twodims, grid = grid)

        if grid:
            plotter.plot_grid()
        else:
            if animate:
                plotter.animate_orbit()
            else:
                plotter.plot_orbit()

    def set_arrays(self):
        """
        Used to initialise all the arrays used by Integrators.
        Generates and initialises arrays for positions, velocities, energies, and angular momentum.
        These arrays contain not only the calculated orbits, butadditional information used for plotting or debugging.
        """

        # if adaptive timestep is used, create an array for it
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)
            self.historic_delta = np.zeros(self.steps)
            self.historic_delta[0] = self.delta

        # tensor of shape (n x steps x 3), containing the positions of the n bodies throughout the calculated orbit
        self.position_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.position_orbit[:, 0, :] = self.nbody.positions

        # tensor of shape (n x steps x 3), containing the velocities of the n bodies throughout the calculated orbit
        self.velocity_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.velocity_orbit[:, 0, :] = self.nbody.velocities

        # save constants (energies, angular momentum) across time (for plotting purposes)
        self.historic_energy = np.zeros(self.steps)
        self.historic_energy[0] = self.nbody.energy
        self.historic_kinetic_energy = np.zeros(self.steps)
        self.historic_kinetic_energy[0] = self.nbody.kinetic_energy
        self.historic_gpe = np.zeros(self.steps)
        self.historic_gpe[0] = self.nbody.gpe
        self.historic_angular_momentum = np.zeros(shape=(self.steps, 3))
        self.historic_angular_momentum[0] = self.nbody.total_angular_momentum

        # reset flag (this method is used when the integrator is going to be run)
        self.integrated = False
