from Integrator import Integrator
from EulerCromer import EulerCromer
import numpy as np
import NMath as nm

class Leapfrog2(Integrator):
    """
    Class defining an integrator via the 2-Step Leapfrog Method
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
        super().__init__(nbody, steps, delta, tolerance = tolerance, adaptive = adaptive, c = c)

        # execute mini Euler-Cromer to accurately calculate the velocity at half timestep
        half_steps = 10e2
        half_delta = self.delta/(2*half_steps) # will use half_steps steps, so calculate the delta accordingly

        half_integrator = EulerCromer(self.nbody, half_steps, half_delta, self.tolerance)

        half_integrator.get_orbits()

        # initialise half velocity orbit
        self.velocity_orbit[:,0,:] = self.nbody.velocities

    def integration_step(self, t):
        """
        Integration step for the 2-Step Leapfrog method.
        v_{1/2} = v_0 + a_0*Δt
        v_{t + 1/2} = v_{t - 1/2} + a_{t-1}*Δt
        x_t = x_{t-1} + v_{t + 1/2}*Δt
        :param t: the step at which the calculation is made
        """

        # check: step t is the same as the expected step int_step.
        # Ensures that when performing an integration_step, they happen at consecutive times
        # For example, integration_step(42) can only be performed if we have previously executed integration_step(41)
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        # perform 2-Step Leapfrog step
        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t - 1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:, t - 1, :] + self.delta * new_velocities

        # calculate adaptive delta by using a time-reversible delta
        if self.adaptive:
            # average of adaptive delta at time t and t+1
            reversible_delta = 0.5 * (self.delta + nm.variable_delta(new_positions, new_velocities, c=self.c))

            # use reversible delta at time t again to calculate new positions and velocities
            # this ensures that when using adaptive delta, the integrator remains symplectic
            new_velocities = self.velocity_orbit[:, t - 1, :] + reversible_delta * acc_t
            new_positions = self.position_orbit[:, t - 1, :] + reversible_delta * new_velocities

            # recalculate adaptive timestep
            self.delta = nm.variable_delta(new_positions, new_velocities, c=self.c)

        self.update_simulation(t, new_positions, new_velocities, symplectic=True)
