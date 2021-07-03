import numpy as np
from Integrator import Integrator

class Leapfrog(Integrator):
    """
    Class defining an integrator via the Euler-Cromer Method
    """

    def __init__(self, nbody, steps, delta, tolerance=1e-6, twostep = True):
        super().__init__(nbody, steps, delta, tolerance)

        # tensor of shape (n, steps, 3), containing orbits of length steps for all n bodies in the simulation
        # used to handle half integer velocity timesteps
        self.twostep = twostep
        self.previous_acceleration = self.nbody.get_acceleration()

        self.half_velocity_orbit = np.zeros((self.nbody.n, self.steps, 3))
        self.half_velocity_orbit[:, 0, :] = self.nbody.velocities + self.delta / 2 * self.nbody.get_acceleration()

    def integration_step(self, t):
        acc_t = self.nbody.get_acceleration()

        if self.twostep:
            new_half_velocities = self.half_velocity_orbit[:, t - 1, :] + self.delta * acc_t
            new_positions = self.position_orbit[:, t - 1, :] + self.delta * new_half_velocities
        else:
            new_half_velocities = self.velocity_orbit[:, t - 1, :] + self.delta/2 * acc_t
            new_positions = self.position_orbit[:, t - 1, :] + self.delta * new_half_velocities
            new_acc = self.nbody.get_acceleration(positions = new_positions)
            new_velocities = new_half_velocities + self.delta/2 * new_acc

        if self.twostep:
            self.half_velocity_orbit[:, t, :] = new_half_velocities
            self.nbody.update(new_positions, new_half_velocities, symplectic = True, tolerance=self.tolerance)
        else:
            self.velocity_orbit[:, t, :] = new_velocities
            self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)

        self.update_historic(t, self.nbody.energy, self.nbody.kinetic_energy, self.nbody.gpe,
                             self.nbody.total_angular_momentum)

        self.position_orbit[:, t, :] = new_positions


