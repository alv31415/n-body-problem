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
        # timestep
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c = self.c)
            self.historic_delta = np.zeros(self.steps)
            self.historic_delta[0] = self.delta
        else:
            self.delta = delta
        # error allowed
        self.tolerance = tolerance
        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        self.position_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.position_orbit[:,0,:] = self.nbody.positions
        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        self.velocity_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.velocity_orbit[:, 0, :] = self.nbody.velocities

        # save constants across time
        self.historic_energy = np.zeros(self.steps)
        self.historic_energy[0] = self.nbody.energy
        self.historic_kinetic_energy = np.zeros(self.steps)
        self.historic_kinetic_energy[0] = self.nbody.kinetic_energy
        self.historic_gpe = np.zeros(self.steps)
        self.historic_gpe[0] = self.nbody.gpe
        self.historic_angular_momentum = np.zeros(shape = (self.steps, 3))
        self.historic_angular_momentum[0] = self.nbody.total_angular_momentum

    def integration_step(self, t):
        pass

    def update_historic(self, t, new_energy, new_kinetic_energy, new_gpe, new_angular_momentum):

        assert t != 0
        assert self.delta > 10e-7

        self.historic_energy[t] = new_energy
        self.historic_kinetic_energy[t] = new_kinetic_energy
        self.historic_gpe[t] = new_gpe
        self.historic_angular_momentum[t] = new_angular_momentum

        if self.adaptive:
            self.historic_delta[t] = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c = self.c)

    def get_orbits(self):
        for t in range(1, self.steps):
            #print(f"Time {t*self.delta}")
            self.integration_step(t)
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