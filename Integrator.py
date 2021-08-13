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

    def integration_step(self, t, delta):
        """
        Overloaded method, dependent on the integration scheme utilised.
        At a given step t, uses delta to calculates positions, velocities and acceleration (in some cases)
        :param t: the step at which the calculation is made
        :param delta: the timestep to use at the integration step
        :return: newly calculated positions, velocities (for step t), and in some cases acceleration (for time t+1)
                 Acceleration is returned for Leapfrog2Int and Leapfrog3
        """

        return None, None, None

    def simulation_step(self, t):
        """
        For a given step, calculates the new positions and velocities via the integration step.
        Then, updates the simulation with these values.
        :param t: the step at which the calculation is made
        """

        # check: step t is the same as the expected step int_step.
        # Ensures that when performing an integration_step, they happen at consecutive times
        # For example, integration_step(42) can only be performed if we have previously executed integration_step(41)
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        new_positions, new_velocities, acc_tt = self.integration_step(t, self.delta)

        # calculate adaptive delta by using a time-reversible delta
        if self.adaptive:
            # average of adaptive delta at time t and t+1
            reversible_delta = 0.5 * (self.delta + nm.variable_delta(new_positions, new_velocities, c=self.c))

            # use reversible delta at time t again to calculate new positions and velocities
            # this ensures that when using adaptive delta, the integrator remains symplectic
            new_positions, new_velocities, acc_tt = self.integration_step(t, delta=reversible_delta)

            # recalculate adaptive timestep
            self.delta = nm.variable_delta(new_positions, new_velocities, c=self.c)

        self.update_simulation(t, new_positions, new_velocities, symplectic=True)

        # set the calculated acceleration for the next iteration
        if acc_tt is not None:
            self.acc_t = acc_tt


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
            self.historic_delta[t] = self.delta

    def update_simulation(self, t, new_positions, new_velocities, symplectic):
        """
        Given newly calculated positions and velocities, updates NBody, alongside historic arrays
        :param t: step at which positions and velocities were calculated
        :param new_positions: newly calculated positions by integrator
        :param new_velocities: newly calculated velocities by integrator
        :param symplectic: True for symplectic integrator,
                           checks that energy,angular momentum.etc... are conserved after the update
        """

        # update the simulation with the calculated position and velocities
        self.nbody.update(new_positions, new_velocities, symplectic=symplectic, tolerance=self.tolerance)

        # add the newly calculated energies and angular momentum (and adaptive delta) to the historic arrays
        self.update_historic(t)

        # set the newly calculated positions and velocities to the orbit arrays
        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities

        # increment the int_step to ensure that integration_step is performed on continuous steps
        self.int_step = t + 1

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
            # integration step until we have done the required steps/time (if adaptive)
            while self.int_step < self.steps:
                self.simulation_step(self.int_step)

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
        These arrays contain not only the calculated orbits, but additional information used for plotting or debugging.
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
