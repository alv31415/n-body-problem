from Integrator import Integrator
import NMath as nm

class Leapfrog2Int(Integrator):

    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        """
        :param nbody: NBody instance which we integrate
        :param steps: the number of steps to integrate for
        :param delta: timestep to use for the integrator. Smaller timesteps lead to more accurate orbits.
        :param tolerance: allowed absolute error for determining conservation of calculated quantities
        :param adaptive: if True, the Integrator will use an adaptive timestep (instead of a fixed one)
        :param c: constant used when calculating adaptive timestep. Smaller c leads to more accurate orbits.
        """

        # execute initialisation from superclass
        super().__init__(nbody, steps, delta, tolerance = tolerance, adaptive = adaptive, c = c)

    def integration_step(self, t):
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        acc_t = self.nbody.get_acceleration()

        new_positions = self.position_orbit[:, t - 1, :] \
                        + self.delta * self.velocity_orbit[:, t - 1, :] \
                        + 0.5 * acc_t * self.delta**2

        acc_tt = self.nbody.get_acceleration(positions = new_positions)

        new_velocities = self.velocity_orbit[:, t - 1, :] \
                         + 0.5 * (acc_t + acc_tt) * self.delta

        self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)
        self.update_historic(t)

        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities
        self.int_step = t + 1