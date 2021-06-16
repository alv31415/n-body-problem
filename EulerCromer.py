from Integrator import Integrator

class EulerCromer(Integrator):
    """
    Class defining an integrator via the Euler-Cromer Method
    """
    def __init__(self, nbody, steps, delta, tolerance = 1e-6):
        super().__init__(nbody, steps, delta, tolerance)

    def integration_step(self, t):

        acc_t = self.nbody.acceleration
        new_velocities  = self.velocity_orbit[:,t-1,:] + self.delta * acc_t

        self.velocity_orbit[:, t, :] = new_velocities

        # add a check in case of collision between 2 bodies?

        new_positions = self.position_orbit[:,t-1,:] + self.delta * self.velocity_orbit[:,t,:]

        self.nbody.update(new_positions, new_velocities, symplectic = True, tolerance = self.tolerance)

        self.position_orbit[:,t,:] = new_positions