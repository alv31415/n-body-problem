import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
import random

class OrbitPlotter:
    def __init__(self, n, position_orbit, seed = 42, animation_steps = 1):
        self.n = n
        self.position_orbit = position_orbit
        self.seed = seed
        self.animation_steps = animation_steps
        self.fig = plt.figure()
        self.ax = plt.axes(projection="3d")
        self.colours = self.generate_colour()

    def generate_colour(self):
        random.seed(self.seed)
        colours = []
        for i in range(self.n):
            r = random.random()
            g = random.random()
            b = random.random()
            colours.append((r, g, b))

        return colours

    def animation_func_orbit(self, frame):
        for i,orbit in enumerate(self.position_orbit[:,:frame*self.animation_steps,:]):
            if frame == self.n - 1:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.legend()
            else:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], c = self.colours[i])

    def plot_orbit(self):

        for i,orbit in enumerate(self.position_orbit):
            self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
            self.ax.scatter3D(orbit[0, 0], orbit[0, 1], orbit[0, 2], c = self.colours[i], s=10, marker = "^")
            self.ax.scatter3D(orbit[-1, 0], orbit[-1, 1], orbit[-1, 2], c = self.colours[i], s = 10)

        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_title(f"Trajectories for a {self.n}-body Problem", pad = 40)
        self.ax.legend()
        plt.show()

    def animate_orbit(self):
        animator = FuncAnimation(self.fig, self.animation_func_orbit, interval = 100)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.set_zlabel("z")
        self.ax.set_title(f"Trajectories for a {self.n}-body Problem", pad=40)
        plt.show()