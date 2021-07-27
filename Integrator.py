import numpy as np

import NMath as nm
from OrbitPlotter import OrbitPlotter

class Integrator:
    """
    Class defining a general integrator, acting as a "superclass" for Euler, Euler-Cromer and Leapfrog
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        # n-body simulation instance
        self.nbody = nbody

        # number of iterations to perform
        self.steps = int(steps)

        # flag to check if we use adaptive timestep
        self.adaptive = adaptive
        self.c = c

        # error allowed when updating the simulation
        self.tolerance = tolerance

        # delta
        self.delta = delta

        self.set_arrays()

    # overloaded method, dependent on the integration scheme utilised
    def integration_step(self, t):
        pass

    def update_historic(self, t):

        assert t != 0

        self.historic_energy[t] = self.nbody.energy#new_energy
        self.historic_kinetic_energy[t] = self.nbody.kinetic_energy#new_kinetic_energy
        self.historic_gpe[t] = self.nbody.gpe#new_gpe
        self.historic_angular_momentum[t,:] = self.nbody.total_angular_momentum

        if self.adaptive:
            self.historic_delta[t] = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c = self.c)

    def get_orbits(self):

        if self.integrated:
            self.set_arrays()
            self.get_orbits()
        else:
            for t in range(1, self.steps):
                    #print(f"Time {t*self.delta}")
                    self.integration_step(t)

            self.integrated = True

        #print(f"Total Energy: {self.nbody.energy}")
        #print(f"Total Linear Momentum: {self.nbody.total_linear_momentum}")
        #print(f"Total Angular Momentum: {self.nbody.total_angular_momentum}")

    def show_orbits(self, animate = False, seed = 42, animation_steps = 1, twodims = True, grid = False):

        plotter = OrbitPlotter(self, seed = seed, animation_steps = animation_steps, twodims = twodims, grid = grid)

        if grid:
            plotter.plot_grid()
        else:
            if animate:
                plotter.animate_orbit()
            else:
                plotter.plot_orbit()

    def set_arrays(self):
        # timestep
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)
            self.historic_delta = np.zeros(self.steps)
            self.historic_delta[0] = self.delta

        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        # keeps track of all positions of the bodies throughout the simulation
        self.position_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.position_orbit[:, 0, :] = self.nbody.positions

        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        # keeps track of all velocities of the bodies throughout the simulation
        self.velocity_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.velocity_orbit[:, 0, :] = self.nbody.velocities

        # save constants across time (for plotting purposes)
        self.historic_energy = np.zeros(self.steps)
        self.historic_energy[0] = self.nbody.energy
        self.historic_kinetic_energy = np.zeros(self.steps)
        self.historic_kinetic_energy[0] = self.nbody.kinetic_energy
        self.historic_gpe = np.zeros(self.steps)
        self.historic_gpe[0] = self.nbody.gpe
        self.historic_angular_momentum = np.zeros(shape=(self.steps, 3))
        self.historic_angular_momentum[0] = self.nbody.total_angular_momentum

        self.integrated = False
