import numpy as np

from Integrator import Integrator
import NMath as nm

class Leapfrog3(Integrator):
    """
    Class defining an integrator via the 3-Step Leapfrog 2-Step Method
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

        # save acceleration for next iteration.
        # Only require 1 expensive acceleration calculation per step
        self.acc_t = self.nbody.get_acceleration()

    def integration_step(self, t):
        """
        Integration step for the Integer 3-Step Leapfrog method.
        v_{t + 1/2} = v_t + 0.5*a_t*Δt
        x_{t + 1} = x_t + v_{t + 1/2}*Δt
        v_{t + 1} = v_{t + 1/2} + 0.5*a_{t + 1}*Δt
        :param t: the step at which the calculation is made
        """

        # check: step t is the same as the expected step int_step.
        # Ensures that when performing an integration_step, they happen at consecutive times
        # For example, integration_step(42) can only be performed if we have previously executed integration_step(41)
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        # perform 3-Step Leapfrog step
        new_half_velocities = self.velocity_orbit[:,t-1,:] + self.acc_t * self.delta * 0.5
        new_positions = self.position_orbit[:, t - 1, :] + new_half_velocities * self.delta
        acc_tt = self.nbody.get_acceleration(positions = new_positions)
        new_velocities = new_half_velocities + acc_tt * self.delta * 0.5

        # calculate adaptive delta by using a time-reversible delta
        if self.adaptive:

            # average of adaptive delta at time t and t+1
            reversible_delta = 0.5*(self.delta + nm.variable_delta(new_positions, new_velocities, c = self.c))

            # use reversible delta at time t again to calculate new positions and velocities
            # this ensures that when using adaptive delta, the integrator remains symplectic
            new_half_velocities = self.velocity_orbit[:, t - 1, :] + self.acc_t * reversible_delta * 0.5
            new_positions = self.position_orbit[:, t - 1, :] + new_half_velocities * reversible_delta
            acc_tt = self.nbody.get_acceleration(positions=new_positions)
            new_velocities = new_half_velocities + acc_tt * reversible_delta * 0.5

        # update the simulation with the calculated position and velocities
        self.nbody.update(new_positions, new_velocities, symplectic=True, tolerance=self.tolerance)
        
        # add the newly calculated energies and angular momentum (and adaptive delta) to the historic arrays
        self.update_historic(t)

        # if adaptive timestep is used, recalculate it
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        # set the newly calculated positions and velocities to the orbit arrays
        self.acc_t = acc_tt
        self.position_orbit[:, t, :] = new_positions
        self.velocity_orbit[:, t, :] = new_velocities

        # increment the int_step to ensure that integration_step is performed on continuous steps
        self.int_step = t + 1