import numpy as np

from Integrator import Integrator
import NMath as nm

# no need for half_velocity_orbit - only for testing purposes

class Leapfrog3(Integrator):

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

        # save acceleration for next iteration.
        # Only require 1 expensive acceleration calculation per step
        self.acc_t = self.nbody.get_acceleration()

    def integration_step(self, t):
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        # calculate next half velocity
        new_half_velocities = self.velocity_orbit[:,t-1,:] + self.acc_t * self.delta * 0.5

        # calculate next position based on half velocity
        new_positions = self.position_orbit[:, t - 1, :] + new_half_velocities * self.delta

        # calculate accelerations based on the new positions
        acc_tt = self.nbody.get_acceleration(positions = new_positions)

        # calculate next velocity
        new_velocities = new_half_velocities + acc_tt * self.delta * 0.5

        # update the simulation with the new positions and velocities
        self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)
        
        # update constants of simulation (energy, angular momentum)
        self.update_historic(t)

        # calculate adaptable delta if necessary
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        # save calculated values for position, half velocity and velocity
        self.acc_t = acc_tt
        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities
        self.int_step = t + 1