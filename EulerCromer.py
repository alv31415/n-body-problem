from Integrator import Integrator
import NMath as nm

class EulerCromer(Integrator):
    """
    Class defining an integrator via the Euler-Cromer Method
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        super().__init__(nbody, steps, delta, tolerance, adaptive, c)

    def integration_step(self, t):

        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t-1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:, t-1, :] + self.delta * new_velocities

        self.nbody.update(new_positions, new_velocities, symplectic = True, tolerance = self.tolerance)
        self.update_historic(t, self.nbody.energy, self.nbody.kinetic_energy, self.nbody.gpe,
                             self.nbody.total_angular_momentum)

        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities
