import numpy as np
import NMath as nmath

class NBody:
    def __init__(self, init_positions, init_velocities, masses):

        self.n = len(init_positions)
        self.check_update_input(init_positions, init_velocities, masses)
        self.G = 6.67408e-11
        self.distances = np.zeros(shape = (self.n, self.n,3))
        self.get_body_distances()
        self.total_mass = np.sum(self.masses)
        self.stacked_masses = np.vstack(self.masses)
        self.com = self.get_com()
        self.linear_momentum = self.get_lmomentum()
        self.angular_momentum = self.get_amomentum()
        self.total_linear_momentum = np.sum(self.linear_momentum, axis = 0)
        self.total_angular_momentum = np.sum(self.angular_momentum, axis = 0)
        self.energy = self.get_energy()


    def check_update_input(self, init_positions, init_velocities, masses):

        assert (self.n == len(init_velocities) and self.n == len(masses)), \
            f"{n} positions given; {len(init_velocities)} velocities given; \
                        {len(masses)} masses given. These 3 quantities must be the same."

        assert (len(init_positions[0]) == 3 and len(init_velocities[0]) == 3)

        if (not isinstance(init_positions, np.ndarray)):
            self.positions = np.array(init_positions)
        else:
            self.positions = init_positions

        if (not isinstance(init_velocities, np.ndarray)):
            self.velocities = np.array(init_velocities)
        else:
            self.velocities = init_velocities

        if (not isinstance(masses, np.ndarray)):
            self.masses = np.array(masses)
        else:
            self.masses = masses

    def get_body_distances(self):
        for i in range(self.n):
            for j in range(i):
                if i != j:
                    self.distances[i,j] = self.positions[i] - self.positions[j]
                    self.distances[j,i] = -self.distances[i,j]
                else:
                    self.distances[i,j] = np.zeros(3)

    def get_com(self):
        com = np.sum(self.stacked_masses * self.positions, axis = 0)/self.total_mass

        return com

    def get_energy(self):
        kinetic_energy = np.sum(nmath.mat_norm(self.linear_momentum)**2 / self.masses)/2
        gpe = 0

        for i in range(self.n):
            for j in range(i):
                gpe += (self.masses[i]*self.masses[j])/nmath.vec_norm(self.distances[i,j])

        gpe *= (-self.G)

        return kinetic_energy + gpe

    def get_lmomentum(self):
        lmomentum = self.stacked_masses * self.velocities

        return lmomentum

    def get_amomentum(self):
        amomentum = nmath.mat_cross(self.positions, self.linear_momentum)

        return amomentum