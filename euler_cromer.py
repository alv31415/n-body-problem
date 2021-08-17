from integrator import Integrator
import nmath as nm

class EulerCromer(Integrator):
    """
    Class defining an integrator via the Euler-Cromer Method
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

        # execute initialisation from superclass
        super().__init__(nbody, steps, delta, tolerance, adaptive, c)

    def integration_step(self, t, delta):
        """
        Integration step for the Euler-Cromer method.
        v_t = v_{t-1} + a_{t-1}*Δt
        x_t = x_{t-1} + v_{t}*Δt
        :param t: the step at which the calculation is made
        """

        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t-1, :] + delta * acc_t
        new_positions = self.position_orbit[:, t-1, :] + delta * new_velocities

        return new_positions, new_velocities, None
