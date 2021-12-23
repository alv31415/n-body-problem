# https://www.youtube.com/watch?v=TmsD8QExZ84

import numpy as np

from django.http.response import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from django.http import JsonResponse
from django.forms.models import model_to_dict
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from .serialisers import NBodySerialiser, IntegratorSerialiser
from .models import NBody, Integrator
from .request_validator import validate_nbody_post, validate_integrator_post
from sim import nbody as nb
from sim.leapfrog_3 import Leapfrog3
from sim.exceptions import *

# Create your views here.

@api_view(["GET"])
def apiOverview(request):

    api_urls = {
        "NBody List": "/nbody-list/",
        "NBody List IDs": "/nbody-list-ids/",
        "NBody Create": "/nbody-create/",
        "NBody View": "/nbody-view/<str:pk>",
        "NBody Update": "/nbody-update/<str:pk>",
        "NBody Delete": "/nbody-delete/<str:pk>",
        "NBody Delete All": "/nbody-delete-all/",
        "Integrator List": "/integrator-list/",
        "Integrator List IDs": "/integrator-list-ids/",
        "Integrator Create": "/integrator-create/",
        "Integrator View": "/integrator-view/<str:pk>",
        "Integrator Update": "/integrator-update/<str:pk>",
        "Integrator Delete": "/integrator-delete/<str:pk>",
        "Integrator Delete All": "/integrator-delete-all/"
    }

    return Response(api_urls)

# NBODY API

@api_view(["GET"])
def nbodyList(request):
    nbodies = NBody.objects.all()
    serialised_nbodies = NBodySerialiser(nbodies, many = True)
    return Response(serialised_nbodies.data)

@api_view(["GET"])
def nbodyListIDs(request):
    nbodies = NBody.objects.all()
    nbody_ids = nbodies.values_list("id", flat=True)
    return Response(list(nbody_ids))

@api_view(["POST"])
def nbodyCreate(request):
    try:
        serialised_nbody = NBodySerialiser(data = validate_nbody_post(request))

        if serialised_nbody.is_valid(raise_exception = True):
            serialised_nbody.save()

        return Response(serialised_nbody.data)
    except ParseError as e:
        return HttpResponse(status=418, reason = e)

@api_view(["GET"])
def nbodyView(request, pk):
    nbody = NBody.objects.get(id = pk)
    serialised_nbody = NBodySerialiser(nbody, many = False)
    return Response(serialised_nbody.data)

@api_view(["POST"])
def nbodyUpdate(request, pk):
    nbody = NBody.objects.get(id = pk)
    serialised_nbody = NBodySerialiser(instance = nbody, data = request.data)

    if serialised_nbody.is_valid():
        serialised_nbody.save()

    return Response(serialised_nbody.data)

@api_view(["DELETE"])
def nbodyDelete(request, pk):
    nbody = NBody.objects.get(id = pk)
    nbody.delete()
    return Response(f"NBody with id {pk} succesfully deleted!")

@api_view(["DELETE"])
def nbodyDeleteAll(request):

    nbodies = NBody.objects.all()
    nbody_ids = list(nbodies.values_list("id", flat=True))

    for pk in nbody_ids:
        nbody = NBody.objects.get(id = pk)
        nbody.delete()

    return Response(f"{len(nbody_ids)} NBodies succesfully deleted")

# INTEGRATOR API

@api_view(["GET"])
def integratorList(request):
    integrators = Integrator.objects.all()
    serialised_integrators = IntegratorSerialiser(integrators, many = True)
    return Response(serialised_integrators.data)

@api_view(["GET"])
def integratorListIDs(request):
    integrators = Integrator.objects.all()
    integrator_ids = integrators.values_list("id", flat=True)
    return Response(list(integrator_ids))

@api_view(["POST"])
def integratorCreate(request):
    data = request.data
    nbody = NBody.objects.get(id = data["nbody_id"])
    data["position_orbits"] = nbody.positions
    data["velocity_orbits"] = nbody.velocities

    try:
        data = validate_integrator_post(data)
        serialised_integrator = IntegratorSerialiser(data = data)

        if serialised_integrator.is_valid(raise_exception = True):
            serialised_integrator.save()

        return Response(serialised_integrator.data)
    except ParseError as e:
        return HttpResponse(status=418, reason = e)


@api_view(["GET"])
def integratorView(request, pk):
    integrator = Integrator.objects.get(id = pk)
    serialised_integrator = IntegratorSerialiser(integrator, many = False)
    return Response(serialised_integrator.data)

@api_view(["POST"])
def integratorUpdate(request, pk):

    # need to read request body to avoid Heroku H18 error
    # https://stackoverflow.com/questions/12704777/how-should-i-interpret-heroku-h18-errors/26783847
    unnecessary = request.data

    # get integrator from database
    integrator = Integrator.objects.get(id = pk)

    # get corresponding nbody from database
    nbody = NBody.objects.get(id = integrator.nbody_id.id)

    # if request was already made, we can return same data as already calculated
    # otherwise repeated calls will keep updating the integrator, which is rather inefficient
    if (len(np.array(integrator.position_orbits).shape) == 3):

        integrator_data = model_to_dict(integrator)

        serialised_integrator = IntegratorSerialiser(instance = integrator, data = integrator_data, many = False)

        if serialised_integrator.is_valid(raise_exception = True):
            serialised_integrator.save()

        # respond with the old positions of the nbody
        
        return Response(serialised_integrator.data)

    # instantiate nbody and integrator, and calculate orbits
    try:
        nbod = nb.NBody(np.array(nbody.positions), np.array(nbody.velocities), np.array(nbody.masses),
                    collision_tolerance = nbody.collision_tolerance,
                    escape_tolerance = nbody.escape_tolerance)

        integ = Leapfrog3(nbody = nbod,
                        steps = integrator.steps,
                        delta = integrator.delta,
                        tolerance = integrator.tolerance,
                        adaptive = integrator.adaptive,
                        adaptive_constant = integrator.adaptive_constant,
                        delta_lim = integrator.delta_lim,
                        store_properties = False)

        # integrate, and catch any exception in the process
        try:
            integ.get_orbits()

            old_positions = np.array(integrator.position_orbits)

            if len(old_positions.shape) == 2:
                old_positions = old_positions[:,np.newaxis,:]

            calculated_positions = integ.position_orbit[:,1:,:]

            n_old = old_positions.shape[1]
            n_calc = calculated_positions.shape[1]

            new_positions = np.zeros(shape = (nbod.n, n_old + n_calc, 3))
            new_positions[:,0:n_old,:] = old_positions
            new_positions[:,n_old:,:] = calculated_positions

            old_velocities = np.array(integrator.velocity_orbits)

            if len(old_velocities.shape) == 2:
                old_velocities = old_velocities[:,np.newaxis,:]

            calculated_velocities = integ.velocity_orbit[:,1:,:]

            assert (n_old == old_velocities.shape[1])
            assert (n_calc == calculated_velocities.shape[1])

            new_velocities = np.zeros(shape = (nbod.n, n_old + n_calc, 3))
            new_velocities[:,0:n_old,:] = old_velocities
            new_velocities[:,n_old:,:] = calculated_velocities

        except(SmallAdaptiveDeltaException,
                COMNotConservedException,
                LinearMomentumNotConservedException,
                BodyEscapeException,
                BodyCollisionException,
                AngularMomentumNotConservedException,
                EnergyNotConservedException) as e:

                return HttpResponse(status=418, reason = f"Error during integration: {e}")

    except (Figure8InitException,
            SmallAdaptiveDeltaException) as e:

            return HttpResponse(status=418, reason = f"Error during initialisation: {e}")

    integrator_data = model_to_dict(integrator)
    integrator_data["position_orbits"] = new_positions.tolist()
    integrator_data["velocity_orbits"] = new_velocities.tolist()

    serialised_integrator = IntegratorSerialiser(instance = integrator, data = integrator_data, many = False)

    if serialised_integrator.is_valid(raise_exception = True):
        serialised_integrator.save()

    # respond with the new positions of the nbody
    
    return Response(serialised_integrator.data)

@api_view(["POST"])
def integratorReset(request, pk):
    integrator = Integrator.objects.get(id = pk)
    integrator_data = model_to_dict(integrator)
    og_positions = np.array(integrator_data["position_orbits"])[:,0,:].tolist()
    og_velocities = np.array(integrator_data["velocity_orbits"])[:,0,:].tolist()
    integrator_data["position_orbits"] = og_positions
    integrator_data["velocity_orbits"] = og_velocities

    nbody = NBody.objects.get(id = integrator.nbody_id.id)
    nbody_data = model_to_dict(nbody)
    nbody_data["positions"] = og_positions
    nbody_data["velocities"] = og_velocities

    serialised_integrator = IntegratorSerialiser(instance = integrator, data = integrator_data, many = False)

    if serialised_integrator.is_valid(raise_exception = True):
        serialised_integrator.save()

    serialised_nbody = NBodySerialiser(instance = nbody, data = nbody_data, many = False)

    if serialised_nbody.is_valid(raise_exception = True):
        serialised_nbody.save()

    return Response(serialised_integrator.data)



@api_view(["DELETE"])
def integratorDelete(request, pk):
    integrator = Integrator.objects.get(id = pk)
    integrator.delete()
    return Response(f"Integrator with id {pk} succesfully deleted!")

@api_view(["DELETE"])
def integratorDeleteAll(request):

    integrators = Integrator.objects.all()
    integrator_ids = list(integrators.values_list("id", flat=True))

    for pk in integrator_ids:
        integrator = Integrator.objects.get(id = pk)
        integrator.delete()

    return Response(f"{len(integrator_ids)} Integrators succesfully deleted")