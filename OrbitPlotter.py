import numpy as np
import math
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.gridspec import GridSpec
from mpl_toolkits import mplot3d
import random

from matplotlib.axes._axes import _log as matplotlib_axes_logger
matplotlib_axes_logger.setLevel('ERROR')

class OrbitPlotter:
    def __init__(self, integrator, seed = 42, animation_steps = 1, twodims = True, grid = False):
        self.integrator = integrator
        self.n = integrator.nbody.n
        self.position_orbit = integrator.position_orbit
        self.delta = integrator.delta
        self.steps = integrator.steps
        self.seed = seed
        self.animation_steps = animation_steps
        self.twodims = twodims
        self.colours = self.generate_colour()
        self.times = np.arange(start=0, stop=self.steps * self.delta, step = self.delta)

        self.grid = grid

        if not grid:
            if twodims:
                self.fig, self.ax = plt.subplots()
            else:
                self.fig = plt.figure()
                self.ax = plt.axes(projection="3d")
            self.colours = self.generate_colour()
        else:
            self.fig = plt.figure(figsize = (11, 8))
            self.gs = GridSpec(nrows = 3, ncols = 4, figure = self.fig)

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
        for i,orbit in enumerate(self.position_orbit[:,:frame*self.animation_steps,:]):
            if frame == self.n - 1:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.legend()
            else:
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], c = self.colours[i])

            if (len(orbit) > 0):
                self.ax.scatter3D(orbit[-1, 0], orbit[-1, 1], orbit[-1,2], c = self.colours[i], s=10)

        self.ax.annotate(f"t = {round(frame * self.delta * self.animation_steps, 1)}", xy=self.integrator.nbody.com[:2])

    def animation_func_orbit_2D(self, frame):
        plt.cla()
        for i,orbit in enumerate(self.position_orbit[:,:np.int(np.floor(frame*self.animation_steps)),:]):
            if frame == self.n - 1:
                self.ax.plot(orbit[:,0], orbit[:,1], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.legend()
            else:
                self.ax.plot(orbit[:,0], orbit[:,1], c = self.colours[i])

            if (len(orbit) > 0):
                self.ax.scatter(orbit[-1, 0], orbit[-1, 1], c = self.colours[i], s=10)

        self.ax.set_title(f"Trajectories for a {self.n}-body Problem")

        self.ax.annotate(f"t = {round(frame * self.delta * self.animation_steps, 1)}", xy=self.integrator.nbody.com[:2])

    def animate_orbit(self, xlims = (-5,5), ylims = (-5,5)):

        assert (not self.grid)

        if self.twodims:
            animator = FuncAnimation(self.fig, self.animation_func_orbit_2D,
                                     frames = math.ceil(self.steps/self.animation_steps), repeat = False, interval = 100)
            plt.axis("equal")
        else:
            animator = FuncAnimation(self.fig, self.animation_func_orbit_3D,
                                     frames = math.ceil(self.steps/self.animation_steps), repeat = False, interval = 100)
            self.ax.set_zlabel("z")

        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        plt.show()

    def plot_orbit(self, xlims = (-5,5), ylims = (-5,5), size = 50):

        assert (not self.grid)

        if self.twodims:
            for i, orbit in enumerate(self.position_orbit):
                self.ax.plot(orbit[:, 0], orbit[:, 1], label=f"Orbit {i + 1}", c=self.colours[i])
                self.ax.scatter(orbit[0, 0], orbit[0, 1], c=self.colours[i], s = size, marker="^")
                self.ax.scatter(orbit[-1, 0], orbit[-1, 1], c=self.colours[i], s = size)
                self.ax.set_title(f"Trajectories for a {self.n}-body Problem")
        else:
            for i,orbit in enumerate(self.position_orbit):
                self.ax.plot3D(orbit[:,0], orbit[:,1], orbit[:,2], label = f"Orbit {i+1}", c = self.colours[i])
                self.ax.scatter3D(orbit[0, 0], orbit[0, 1], orbit[0, 2], c = self.colours[i], s = size, marker = "^")
                self.ax.scatter3D(orbit[-1, 0], orbit[-1, 1], orbit[-1, 2], c = self.colours[i], s = size)
                self.ax.set_title(f"Trajectories for a {self.n}-body Problem", pad=40)
                self.ax.set_zlabel("z")

        self.ax.set_xlim(xlims)
        self.ax.set_ylim(ylims)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")
        self.ax.legend()
        plt.show()

    def plot_energies(self, ax):

        ax.plot(self.times, self.integrator.historic_energy, label = "Total Energy", c = "k")
        ax.plot(self.times, self.integrator.historic_kinetic_energy, label="Kinetic Energy", c = "r")
        ax.plot(self.times, self.integrator.historic_gpe, label="Gravitational Potential Energy", c = "b")

        ax.set_title("Energy Change")
        ax.set_xlabel("Time")
        ax.set_ylabel("Energy")
        ax.legend()

    def plot_dim(self, data, dim, ax, title, legend = False):

        #assert (dim == 0) or (dim == 1)

        dim_data = data[:,:,dim]

        assert dim_data.shape == (self.n, self.steps)

        for i in range(len(dim_data)):
            ax.plot(self.times, dim_data[i], label = f"Orbit {i + 1}", c = self.colours[i])

        ax.set_title(f"{title} Change")
        ax.set_xlabel("Time")
        ax.set_ylabel(title)

        if legend:
            ax.legend(loc = "upper right")

    def plot_grid(self, xlims = (-5,5), ylims = (-5,5)):

        assert self.grid, "To display a grid with the orbit information, initialise OrbitPlotter with grid = True"

        ax_orbit = self.fig.add_subplot(self.gs[0:2, 0:2])
        ax_position_x = self.fig.add_subplot(self.gs[0,2])
        ax_position_y = self.fig.add_subplot(self.gs[1, 2])
        ax_position_z = self.fig.add_subplot(self.gs[2, 2])
        ax_velocity_x = self.fig.add_subplot(self.gs[0, 3])
        ax_velocity_y = self.fig.add_subplot(self.gs[1, 3])
        ax_velocity_z = self.fig.add_subplot(self.gs[2, 3])
        ax_energy = self.fig.add_subplot(self.gs[2, 0:2])

        for i, orbit in enumerate(self.position_orbit):
            ax_orbit.plot(orbit[:, 0], orbit[:, 1], label=f"Orbit {i + 1}", c = self.colours[i])
            ax_orbit.scatter(orbit[0, 0], orbit[0, 1], c = self.colours[i], s=10, marker="^")
            ax_orbit.scatter(orbit[-1, 0], orbit[-1, 1], c = self.colours[i], s=10)
        ax_orbit.set_title(f"Trajectories for a {self.n}-body Problem")
        ax_orbit.axis("equal")
        ax_orbit.legend()

        self.plot_energies(ax_energy)
        self.plot_dim(self.position_orbit, dim = 0, ax = ax_position_x, title = r"Position $x$")
        self.plot_dim(self.position_orbit, dim = 1, ax = ax_position_y, title=r"Position $y$")
        self.plot_dim(self.position_orbit, dim = 2, ax = ax_position_z, title = r"Position $z$")
        self.plot_dim(self.integrator.velocity_orbit, dim = 0, ax=ax_velocity_x, title = r"Velocity $x$")
        self.plot_dim(self.integrator.velocity_orbit, dim = 1, ax = ax_velocity_y, title = r"Velocity $y$")
        self.plot_dim(self.integrator.velocity_orbit, dim = 2, ax = ax_velocity_z, title = r"Velocity $z$")

        plt.tight_layout()
        plt.show()
