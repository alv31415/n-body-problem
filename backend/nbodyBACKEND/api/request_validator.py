import json
from copy import deepcopy

from rest_framework.exceptions import ParseError

def validate_nbody_array(data, key):
    if key in data:
        arrs = json.loads(data[key])

        print("Checking it is a list")
        if not isinstance(arrs, list):
            raise ParseError(f"'{key}' must have a value of type list")

        print("Checking it is a list of lists of length 3")
        for arr in arrs:
            if isinstance(arr, list):
                if not len(arr) == 3:
                    raise ParseError(f"Expected a 2D array for '{key}'', with internal arrays of length 3")
            else:
                raise ParseError(f"Element in '{key}'' is not an array")

        data[key] = arrs
    else:
        raise ParseError(f"Expected key '{key}' in request")

def validate_nbody_post(request):
    data = deepcopy(request.data)
    
    validate_nbody_array(data, "positions")
    validate_nbody_array(data, "velocities")

    if len(data["positions"]) != len(data["velocities"]):
        raise ParseError("Number of bodies is not the same for positions and velocities")

    if "masses" in data:
        masses = json.loads(data["masses"])

        if not isinstance(masses, list):
            raise ParseError("Masses must be given as a list")

        if len(masses) == len(data["positions"]):
            data["masses"] = masses
        else:
            raise ParseError(f"Number of masses ({len(masses)}) doesn't correspond with number of bodies")
    else:
        raise ParseError("Expect key 'masses' in request")

    return data

def validate_integrator_post(data_dict):
    data = deepcopy(data_dict)

    print("Data received")

    for k,v in data.items():
        if k != "name" and isinstance(v, str):
            try:
                v = float(v)
            except ValueError:
                pass

    print("Data Processed to include numbers")

    position_orbits = data["position_orbits"]

    for orbit in position_orbits:
        try:
            assert isinstance(orbit, list)
            assert len(orbit) == 3
        except AssertionError:
            raise ParseError(f"Position orbits incorrectly formatted")

    return data

                
