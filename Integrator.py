import numpy as np
from OrbitPlotter import OrbitPlotter

class Integrator:
    """
    Class defining a general integrator, acting as a "superclass" for Euler, Euler-Cromer and Leapfrog
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6):
        # n-body simulation instance
        self.nbody = nbody
        # number of iterations to perform
        self.steps = steps
        # timestep
        self.delta = delta
        # error allowed
        self.tolerance = tolerance
        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        self.position_orbit = np.zeros((self.nbody.n, steps, 3))
        self.position_orbit[:,0,:] = self.nbody.positions
        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        self.velocity_orbit = np.zeros((self.nbody.n, steps, 3))
        self.velocity_orbit[:, 0, :] = self.nbody.velocities

        # save constants across time
        self.historic_energy = np.zeros(steps)
        self.historic_energy[0] = self.nbody.energy
        self.historic_kinetic_energy = np.zeros(steps)
        self.historic_kinetic_energy[0] = self.nbody.kinetic_energy
        self.historic_gpe = np.zeros(steps)
        self.historic_gpe[0] = self.nbody.gpe
        #self.historic_angular_momentum = np.zeros(steps)
        #self.historic_angular_momentum[0] = self.nbody.total_angular_momentum

    def integration_step(self, t):
        pass

    def update_historic(self, t, new_energy, new_kinetic_energy, new_gpe, new_angular_momentum):

        assert t != 0

        self.historic_energy[t] = new_energy
        self.historic_kinetic_energy[t] = new_kinetic_energy
        self.historic_gpe[t] = new_gpe
        #self.historic_angular_momentum = new_angular_momentum

    def get_orbits(self):
        for t in range(1, self.steps):
            print(f"Time {t*self.delta}")
            self.integration_step(t)
        print(f"Total Energy: {self.nbody.energy}")
        print(f"Total Linear Momentum: {self.nbody.total_linear_momentum}")
        print(f"Total Angular Momentum: {self.nbody.total_angular_momentum}")

    def show_orbits(self, animate = False, seed = 42, animation_steps = 1, twodims = True, grid = False):

        plotter = OrbitPlotter(self, seed = seed, animation_steps = animation_steps, twodims = twodims, grid = grid)

        if grid:
            plotter.plot_grid()
        else:
            if animate:
                plotter.animate_orbit()
            else:
                plotter.plot_orbit()