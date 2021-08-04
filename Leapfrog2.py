from Integrator import Integrator
from EulerCromer import EulerCromer
import numpy as np
import NMath as nm

class Leapfrog2(Integrator):

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
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t - 1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:, t - 1, :] + self.delta * new_velocities

        self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)
        self.update_historic(t)

        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities
        self.int_step = t + 1