import numpy as np
from OrbitPlotter import OrbitPlotter

class Leapfrog():
    """
        Class defining an integrator via the Euler-Cromer Method
        """

    def __init__(self, nbody, steps, delta, tolerance=1e-6, twostep = True):
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
        self.position_orbit[:, 0, :] = self.nbody.positions
        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        # used to handle half integer velocity timesteps
        self.half_velocity_orbit = np.zeros((self.nbody.n, steps, 3))
        self.half_velocity_orbit[:, 0, :] = self.nbody.velocities + self.delta/2 * self.nbody.acceleration

        if twostep:
            self.full_velocity_orbit = np.zeros((self.nbody.n, steps, 3))
            self.full_velocity_orbit[:, 0, :] = self.nbody.velocities + self.delta / 2 * self.nbody.acceleration

    def integration_step(self, t):

        acc_t = self.nbody.acceleration
        new_velocities = self.velocity_orbit[:, t - 1, :] + self.delta * acc_t

        self.velocity_orbit[:, t, :] = new_velocities

        # add a check in case of collision between 2 bodies?

        new_positions = self.position_orbit[:, t - 1, :] + self.delta * self.velocity_orbit[:, t, :]

        self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)

        self.position_orbit[:, t, :] = new_positions

    def get_orbits(self):
        for t in range(1, self.steps):
            print(f"Time {t * self.delta}")
            self.integration_step(t)
            print(self.nbody.energy)
            print(self.nbody.total_linear_momentum)
            print(self.nbody.total_angular_momentum)

    def show_orbits(self, animate=False, seed=42, animation_steps=1):

        plotter = OrbitPlotter(self.nbody.n, self.position_orbit, seed=seed, animation_steps=animation_steps)

        if animate:
            plotter.animate_orbit()
        else:
            plotter.plot_orbit()
