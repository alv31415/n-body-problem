import numpy as np
import matplotlib.pyplot as plt

from three_body import *
from Leapfrog3 import Leapfrog3

def get_stability_matrix(perturb, limit, collision_tolerance, escape_tolerance):
    return np.random.rand(2*limit,2*limit)

def plot_stability_matrix(perturb, limit, collision_tolerance, escape_tolerance, tick_ratio = 10):

    stability_matrix = get_stability_matrix(perturb, limit, collision_tolerance, escape_tolerance)

    fig, ax = plt.subplots()
    cax = ax.imshow(stability_matrix, extent=(-limit, limit, -limit, limit))

    ax.set_xlabel(r"$\Delta v_x$")
    ax.set_ylabel(r"$\Delta v_y$")
    ax.set_title("Stability of Figure 8 Under Perturbations", pad = 20)

    ax.set_xticks(np.arange(-limit, limit+1, step = 2*limit/tick_ratio))
    ax.set_yticks(np.arange(-limit, limit+1, step = 2*limit/tick_ratio))

    cb = plt.colorbar(cax, ax = ax)
    cb.set_label("Colorbar Label", labelpad = 20)

    plt.tight_layout()
    plt.show()

plot_stability_matrix(perturb = 1, limit=10, collision_tolerance=10**-3, escape_tolerance=10**6)