import numpy as np
import NMath as nmath
from copy import deepcopy

class NBody:
    """
    Class used to simulate the n-body problem.
    """
    def __init__(self, init_positions, init_velocities, masses):

        self.n = len(init_positions)
        self.check_update_input(init_positions, init_velocities, masses)
        self.G = 1#6.67408e-11

        # tensor of distances between any 2 objects
        self.distances = np.zeros(shape = (self.n, self.n,3))
        self.get_body_distances()

        self.total_mass = np.sum(self.masses)
        # stacked_masses is a convenient way of storing masses for certain computations
        self.stacked_masses = np.vstack(self.masses)

        # calculate simulation properties
        self.com = self.get_com()
        self.linear_momentum = self.get_lmomentum()
        self.angular_momentum = self.get_amomentum()
        self.total_linear_momentum = np.sum(self.linear_momentum, axis = 0)
        self.total_angular_momentum = np.sum(self.angular_momentum, axis = 0)
        self.energy = self.get_energy()
        self.acceleration = self.get_acceleration()

    def check_update_input(self, init_positions, init_velocities, masses):
        """
        Checks that class initialisation has been done with correct parameters
        Ensures that positions, velocities and masses all have the same number of elements
        Ensure that positions and velocities are matrices of shape (n x 3)
        Lastly, ensures that position, velocity and mass tensors are numpy arrays
        """

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
        """
        Calculates the direction vector from all bodies in the n-body system
        Composed of tensor of dimensions (n,n,3),
        where entry (i,j) contains the direction vector from object i to object j
        For optimisation reasons, since the direction vector (i,j) is the negative of the direction (j,i),
        we just need to calculate the upper triangular part of the matrix
        """
        # could be vectorised by doing a transpose - do speed tests
        for i in range(self.n):
            for j in range(i):
                if i != j:
                    self.distances[i,j] = self.positions[j] - self.positions[i]
                    self.distances[j,i] = -self.distances[i,j]
                else:
                    self.distances[i,j] = np.zeros(3)

    def get_com(self):
        """
        Calculates the centre of mass of the system
        :return: a position vector in 3D for the COM of the system
        """
        com = np.sum(self.stacked_masses * self.positions, axis = 0)/self.total_mass

        return com

    def get_lmomentum(self):
        """
        Calculates the linear momentum of each element of the system
        :return: an (n x 3) matrix, with each entry i corresponding to the momentum of o body i
        """
        lmomentum = self.stacked_masses * self.velocities

        return lmomentum

    def get_amomentum(self):
        """
        Calculates the angular momentum of each element of the system
        :return: an (n x 3) matrix, with each entry i corresponding to the angular momentum of o body i
        """
        amomentum = nmath.mat_cross(self.positions, self.linear_momentum)

        return amomentum

    def get_energy(self):
        """
        Calculates the total energy of the system, mainly to ensure that the symplectic integrator functions correctly
        :return: the total energy of the system, given as the sum of kinetic and gravitational potential energy
        """
        kinetic_energy = np.sum(nmath.ten_norm(self.linear_momentum, axis = 1, sqrt = False) / self.masses)/2
        gpe = 0

        for i in range(self.n):
            for j in range(i):
                gpe += (self.masses[i]*self.masses[j])/nmath.ten_norm(self.distances[i,j], axis = 0)

        gpe *= (-self.G)

        return kinetic_energy + gpe

    def get_acceleration(self):
        """
        Calculates the acceleration of every particle of the system - solely depends on their position
        :return: an (n x 3) matrix, with each entry i corresponding to the acceleration of o body i
        """
        # calculate the magnitude of the distances between bodies
        inv_dist_mag3 = nmath.ten_norm(self.distances, axis = 2, sqrt = False)
        # if any distance is 0, set it to infinity -> this indicates that the body is in the same position,
        # so to avoid division by 0 error, and to avoid unnecessary computational costs, set to infinity
        # as the force felt is expected to be 0 anyways
        inv_dist_mag3[inv_dist_mag3 == 0] = np.inf
        # exponentiate; calculates 1/(magnitude of distance)^3
        inv_dist_mag3 = inv_dist_mag3**(-1.5)

        # tensor, with entry (i,j) giving a unit vector for the direction of the force felt by i due to j
        acc_direction = inv_dist_mag3[:,:,np.newaxis] * self.distances

        self.acc_direction = acc_direction

        # use slicing to obtain (n x n) matrices for the direction values (x y z) of the acceleration
        # by using a matrix product, we perform the necessary sum
        # since the direction for the force between an object and itself is the 0 vector,
        # this doesn't contribute to the sum
        acc_x = acc_direction[:, :, 0] @ self.masses
        acc_y = acc_direction[:, :, 1] @ self.masses
        acc_z = acc_direction[:, :, 2] @ self.masses

        # combine all of the acceleration directions into an acceleration vector
        acceleration = self.G * np.vstack((acc_x, acc_y, acc_z)).T

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
        """
        Checks that a quantity is conserved across iterations of the simulation (within a given tolerance)
        """
        return (np.abs(new_value - old_value) < tolerance).all()

    def update(self, new_positions, new_velocities, symplectic = True, tolerance = 1e-6):
        """
        Updates the simulation, given newly calculated positions and distances.
        :param symplectic: if symplectic, will check that conserved quantities are conserved
        :param tolerance: tolerance for conservation
        """
        assert (self.n == len(new_positions) and self.n == len(new_velocities)), \
            f"{len(new_positions)} positions given; {len(new_velocities)} velocities given; \
                                    These 2 quantities must be the same."

        assert (len(new_positions[0]) == 3 and len(new_velocities[0]) == 3)

        # if positions and velocities have the correct format, update positions and velocities
        self.positions = new_positions
        self.velocities = new_velocities
        self.get_body_distances()

        # calculate the values for the new system
        new_linear_momentum = self.get_lmomentum()

        new_total_linear_momentum = np.sum(new_linear_momentum, axis = 0)

        new_angular_momentum = self.get_amomentum()

        new_total_angular_momentum = np.sum(new_angular_momentum, axis=0)

        new_energy = self.get_energy()

        # how exactly to check for conserved COM
        # adapt coordinates so that COM is the centre?

        # check if quantities are conserved
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

            # set the properties of the system
            self.linear_momentum = new_linear_momentum
            self.total_linear_momentum = new_total_linear_momentum

            self.angular_momentum = new_angular_momentum
            self.total_angular_momentum = new_total_angular_momentum

            self.energy = new_energy

            self.acceleration = self.get_acceleration()

    def copy(self):
        return deepcopy(self)


