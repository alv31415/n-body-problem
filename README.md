# n-body-problem
Investigation of the N-Body problem via numerical methods

## How To Run a Simulation

Below is the recommended way of running a simulation, using some test data. 

```
import numpy as np

from NBody import NBody
from Leapfrog3 import Leapfrog3

STEPS = 10**3
DELTA = 10**-2
TOLERANCE = 10**-3
C = 0.01
ADAPTIVE = False

init_positions = np.array([[0,1,0], [0,-1,0]])
init_velocities = np.array([[0.4,0,0], [-0.4,0,0]])
masses = np.array([1,1])

nbod2 = NBody(init_positions, init_velocities, masses)
nbod2.G = 1

integ = Leapfrog3(nbod2, steps = STEPS, delta = DELTA, tolerance = TOLERANCE, adaptive = ADAPTIVE, c = C)

print(nbod2)
print("-"*20 + "\n")
integ.get_orbits()
print(nbod2)
integ.show_orbits(grid = True)
```
