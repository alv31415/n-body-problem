import NMath as nm
from Integrator import Integrator

class Euler(Integrator):
    """
    Class defining an integrator via the Euler Method
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        super().__init__(nbody, steps, delta, tolerance, adaptive, c)

    def integration_step(self, t):

        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t-1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:,t-1,:] + self.delta * self.velocity_orbit[:,t-1,:]

        self.nbody.update(new_positions, new_velocities, symplectic = False, tolerance = self.tolerance)
        self.update_historic(t)

        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        self.velocity_orbit[:, t ,:] = new_velocities
        self.position_orbit[:,t, :] = new_positions


