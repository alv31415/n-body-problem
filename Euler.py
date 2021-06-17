from Integrator import Integrator

class Euler(Integrator):
    """
    Class defining an integrator via the Euler Method
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6):
        super().__init__(nbody, steps, delta, tolerance)

    def integration_step(self, t):

        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t-1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:,t-1,:] + self.delta * self.velocity_orbit[:,t-1,:]

        self.nbody.update(new_positions, new_velocities, symplectic = False, tolerance = self.tolerance)
        self.update_historic(t, self.nbody.energy, self.nbody.kinetic_energy, self.nbody.gpe,
                             self.nbody.total_angular_momentum)

        self.velocity_orbit[:, t ,:] = new_velocities
        self.position_orbit[:,t, :] = new_positions


