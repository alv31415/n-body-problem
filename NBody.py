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
        self.acceleration = self.get_acceleration()

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
        # could be vectorised by doing a transpose - do speed tests
        for i in range(self.n):
            for j in range(i):
                if i != j:
                    self.distances[i,j] = self.positions[j] - self.positions[i]
                    self.distances[j,i] = -self.distances[i,j]
                else:
                    self.distances[i,j] = np.zeros(3)

    def get_com(self):
        com = np.sum(self.stacked_masses * self.positions, axis = 0)/self.total_mass

        return com

    def get_lmomentum(self):
        lmomentum = self.stacked_masses * self.velocities

        return lmomentum

    def get_amomentum(self):
        amomentum = nmath.mat_cross(self.positions, self.linear_momentum)

        return amomentum

    def get_energy(self):
        kinetic_energy = np.sum(nmath.ten_norm(self.linear_momentum, axis = 1, sqrt = False) / self.masses)/2
        gpe = 0

        for i in range(self.n):
            for j in range(i):
                gpe += (self.masses[i]*self.masses[j])/nmath.ten_norm(self.distances[i,j], axis = 0)

        gpe *= (-self.G)

        return kinetic_energy + gpe

    def get_acceleration(self):
        inv_dist_mag3 = nmath.ten_norm(self.distances, axis = 2, sqrt = False)
        inv_dist_mag3[inv_dist_mag3 == 0] = np.inf
        inv_dist_mag3 = inv_dist_mag3**(-1.5)

        acc_direction = inv_dist_mag3[:,:,np.newaxis] * self.distances

        self.acc_direction = acc_direction

        acc_x = acc_direction[:, :, 0] @ self.masses
        acc_y = acc_direction[:, :, 1] @ self.masses
        acc_z = acc_direction[:, :, 0] @ self.masses
        acceleration = np.vstack((acc_x, acc_y, acc_z)).T

        return acceleration

    def __str__(self):
        return f"Bodies: {self.n}\n" + \
               f"Total Mass: {self.total_mass}\n" + \
               f"Centre of Mass: {self.com}\n" + \
               f"Linear Momentum:\n {self.linear_momentum}\n" + \
               f"Total Linear Momentum: {self.total_linear_momentum}\n" + \
               f"Angular Momentum:\n {self.angular_momentum}\n" + \
               f"Total Angular Momentum: {self.total_angular_momentum}\n" + \
               f"Total Energy: {self.energy}\n"

    def conserved_quantity(self, new_value, old_value, tolerance):
        return (np.abs(new_value - old_value) < tolerance).all()

    def update(self, new_positions, new_velocities, symplectic = True, tolerance = 1e-6):
        assert (self.n == len(new_positions) and self.n == len(new_velocities)), \
            f"{len(new_positions)} positions given; {len(new_velocities)} velocities given; \
                                    These 2 quantities must be the same."

        assert (len(new_positions[0]) == 3 and len(new_velocities[0]) == 3)

        self.positions = new_positions
        self.velocities = new_velocities
        self.get_body_distances()

        new_linear_momentum = self.get_lmomentum()

        new_total_linear_momentum = np.sum(new_linear_momentum, axis = 0)

        new_angular_momentum = self.get_amomentum()

        new_total_angular_momentum = np.sum(new_angular_momentum, axis=0)

        new_energy = self.get_energy()

        # how exactly to check for conserved COM
        # adapt coordinates so that COM is the centre?

        if (symplectic):
            assert (self.conserved_quantity(new_total_linear_momentum, self.total_linear_momentum, tolerance = tolerance)), \
                    f"Total Linear Momentum was NOT conserved after the update.\
                    \nCurrent Total Linear Momentum: {self.total_linear_momentum}\n" \
                    f"Calculated Total Linear Momentum: {new_total_linear_momentum}\n"

            assert (self.conserved_quantity(new_total_angular_momentum, self.total_angular_momentum, tolerance = tolerance)), \
                    f"Total Angular Momentum was NOT conserved after the update.\
                    \nCurrent Total Angular Momentum: {self.total_angular_momentum}\n" \
                    f"Calculated Total Angular Momentum: {new_total_angular_momentum}\n"

            assert (self.conserved_quantity(new_energy, self.energy, tolerance = tolerance)), \
                    f"Total Energy was NOT conserved after the update.\
                    \nCurrent Total Energy: {self.energy}\n" \
                    f"Calculated Total Energy: {new_energy}\n"

            self.linear_momentum = new_linear_momentum
            self.total_linear_momentum = new_total_linear_momentum

            self.angular_momentum = new_angular_momentum
            self.total_angular_momentum = new_total_angular_momentum

            self.energy = new_energy

            self.acceleration = self.get_acceleration()


