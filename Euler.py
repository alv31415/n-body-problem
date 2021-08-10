import NMath as nm
from Integrator import Integrator

class Euler(Integrator):
    """
    Class defining a non-symplectic integrator, via the Euler Method
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

    def integration_step(self, t):
        """
        Integration step for the Euler method.
        v_t = v_{t-1} + a_{t-1}*Δt
        x_t = x_{t-1} + v_{t-1}*Δt
        :param t: the step at which the calculation is made
        """

        # check: step t is the same as the expected step int_step.
        # Ensures that when performing an integration_step, they happen at consecutive times
        # For example, integration_step(42) can only be performed if we have previously executed integration_step(41)
        assert self.int_step == t, f"Attempted to integrate with a discontinuous time step. \n" \
                                   f"Step to Integrate: {t}\n" \
                                   f"Expected Step to Integrate: {self.int_step}\n"

        # perform Euler step
        acc_t = self.nbody.get_acceleration()

        new_velocities = self.velocity_orbit[:, t-1, :] + self.delta * acc_t
        new_positions = self.position_orbit[:,t-1,:] + self.delta * self.velocity_orbit[:,t-1,:]

        # update the simulation with the calculated position and velocities
        self.nbody.update(new_positions, new_velocities, symplectic = False, tolerance = self.tolerance)

        # add the newly calculated energies and angular momentum (and adaptive delta) to the historic arrays
        self.update_historic(t)

        # if adaptive timestep is used, recalculate it
        if self.adaptive:
            self.delta = nm.variable_delta(self.nbody.positions, self.nbody.velocities, c=self.c)

        # set the newly calculated positions and velocities to the orbit arrays
        self.velocity_orbit[:, t ,:] = new_velocities
        self.position_orbit[:,t, :] = new_positions

        # increment the int_step to ensure that integration_step is performed on continuous steps
        self.int_step = t + 1


