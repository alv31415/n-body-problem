import numpy as np

from Integrator import Integrator
import NMath as nm

class Leapfrog3(Integrator):

    def __init__(self, nbody, steps, delta, tolerance = 1e-6, adaptive = False, c = 1):
        super().__init__(nbody, steps, delta, tolerance = tolerance, adaptive = adaptive, c = c)

        # save acceleration for next iteration (only 1 acceleration calculation per step)
        self.acc_t = self.nbody.get_acceleration()

        # initialise half-velocity tensor
        # keeps track of half velocity across the simulation
        self.half_velocity_orbit = np.zeros(shape = (self.nbody.n, self.steps, 3))
        self.half_velocity_orbit[:,0,:] = self.velocity_orbit[:,0,:] +  self.acc_t * self.delta * 0.5

    def integration_step(self, t):

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
        self.half_velocity_orbit[:, t, :] = new_half_velocities
        self.velocity_orbit[:, t, :] = new_velocities