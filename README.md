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
ADAPTIVE_CONSTANT = 0.1
ADAPTIVE = False

init_positions = np.array([[0,1,0], [0,-1,0]])
init_velocities = np.array([[0.4,0,0], [-0.4,0,0]])
masses = np.array([1,1])

nbod2 = NBody(init_positions, init_velocities, masses)
nbod2.G = 1

integ = Leapfrog3(nbod2, steps = STEPS, delta = DELTA, tolerance = TOLERANCE, adaptive = ADAPTIVE, c = ADAPTIVE_CONSTANT)

print(nbod2)
print("-"*20 + "\n")
integ.get_orbits()
print(nbod2)
integ.show_orbits(grid = True)
```

This should produce the following grid plot:

<p align = "center"><img src="https://github.com/alv31415/n-body-problem/blob/main/img/test_code_result.png" width = 720 height = 432></p>

and display the following in terminal: 

```
Bodies: 2
Total Mass: 2
Centre of Mass: [0. 0. 0.]
Linear Momentum:
 [[ 0.4  0.   0. ]
 [-0.4  0.   0. ]]
Total Linear Momentum: [0. 0. 0.]
Angular Momentum:
 [[ 0.   0.  -0.4]
 [-0.  -0.  -0.4]]
Total Angular Momentum: [ 0.   0.  -0.8]
Kinetic Energy: 0.16000000000000003
Gravitational Potential Energy: -0.5
Total Energy: -0.33999999999999997

--------------------

Bodies: 2
Total Mass: 2
Centre of Mass: [0. 0. 0.]
Linear Momentum:
 [[ 0.13593791 -0.51027534  0.        ]
 [-0.13593791  0.51027534  0.        ]]
Total Linear Momentum: [0. 0. 0.]
Angular Momentum:
 [[ 0.   0.  -0.4]
 [-0.   0.  -0.4]]
Total Angular Momentum: [ 0.   0.  -0.8]
Kinetic Energy: 0.27886003434284173
Gravitational Potential Energy: -0.6188600694601704
Total Energy: -0.3400000351173286


