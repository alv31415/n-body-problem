import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
import random
from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

class OrbitPlotter:
    def __init__(self, n, position_orbit, delta, steps, seed = 42, animation_steps = 1, twodims = True):
        self.n = n
        self.position_orbit = position_orbit
        self.delta = delta
        self.steps = steps
        self.seed = seed
        self.animation_steps = animation_steps
        self.twodims = twodims

        if twodims:
            self.fig, self.ax = plt.subplots()
        else:
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

    def animation_func_orbit_3D(self, frame):
        plt.cla()
        self.ax.annotate(f"t = {self.delta * frame * self.animation_steps}", xy=(0, 0))
        for i,orbit in enumerate(self.position_orbit[:,:frame*self.animation_steps,:]):
            if frame == self.n - 1:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.legend()
            else:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], c = self.colours[i])

            if (len(orbit) > 0):
                self.ax.scatter3D(orbit[-1, 0], orbit[-1, 1], orbit[-1,2], c = self.colours[i], s=10)

    def animation_func_orbit_2D(self, frame):
        plt.cla()
        self.ax.annotate(f"t = {frame * self.delta}", xy = (0,0))
        for i,orbit in enumerate(self.position_orbit[:,:frame*self.animation_steps,:]):
            if frame == self.n - 1:
                self.ax.plot(orbit[:,0], orbit[:,1], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.legend()
            else:
                self.ax.plot(orbit[:,0], orbit[:,1], c = self.colours[i])

            if (len(orbit) > 0):
                self.ax.scatter(orbit[-1, 0], orbit[-1, 1], c = self.colours[i], s=10)

    def plot_orbit(self, xlims = (-5,5), ylims = (-5,5)):

        if self.twodims:
            for i, orbit in enumerate(self.position_orbit):
                self.ax.plot(orbit[:, 0], orbit[:, 1], label=f"Orbit {i + 1}", c=self.colours[i])
                self.ax.scatter(orbit[0, 0], orbit[0, 1], c=self.colours[i], s=10, marker="^")
                self.ax.scatter(orbit[-1, 0], orbit[-1, 1], c=self.colours[i], s=10)
                self.ax.set_title(f"Trajectories for a {self.n}-body Problem")
        else:
            for i,orbit in enumerate(self.position_orbit):
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.scatter3D(orbit[0, 0], orbit[0, 1], orbit[0, 2], c = self.colours[i], s=10, marker = "^")
                self.ax.scatter3D(orbit[-1, 0], orbit[-1, 1], orbit[-1, 2], c = self.colours[i], s = 10)
                self.ax.set_title(f"Trajectories for a {self.n}-body Problem", pad=40)
                self.ax.set_zlabel("z")

        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        plt.show()

    def animate_orbit(self, xlims = (-5,5), ylims = (-5,5)):
        if self.twodims:
            animator = FuncAnimation(self.fig, self.animation_func_orbit_2D, frames = self.steps, repeat = False, interval = 100)
            self.ax.set_title(f"Trajectories for a {self.n}-body Problem")
        else:
            animator = FuncAnimation(self.fig, self.animation_func_orbit_3D, frames = self.steps, repeat = False, interval = 100)
            self.ax.set_title(f"Trajectories for a {self.n}-body Problem", pad=40)
            self.ax.set_zlabel("z")

        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

        plt.show()