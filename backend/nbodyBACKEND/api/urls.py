from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.apiOverview, name = "api-overview"),

    path("nbody-list/", views.nbodyList, name = "api-nbody-list"),
    path("nbody-list-ids/", views.nbodyListIDs, name = "api-nbody-list-ids"),
    path("nbody-create/", views.nbodyCreate, name = "api-nbody-create"),
    path("nbody-view/<str:pk>", views.nbodyView, name = "api-nbody-view"),
    path("nbody-update/<str:pk>", views.nbodyUpdate, name = "api-nbody-update"),
    path("nbody-delete/<str:pk>", views.nbodyDelete, name = "api-nbody-delete"),
    path("nbody-delete-all/", views.nbodyDeleteAll, name = "api-nbody-delete-all"),
    
    path("integrator-list/", views.integratorList, name = "api-integrator-list"),
    path("integrator-list-ids/", views.integratorListIDs, name = "api-integrator-list-ids"),
    path("integrator-create/", views.integratorCreate, name = "api-integrator-create"),
    path("integrator-view/<str:pk>", views.integratorView, name = "api-integrator-view"),
    path("integrator-update/<str:pk>", views.integratorUpdate, name = "api-integrator-update"),
    path("integrator-reset/<str:pk>", views.integratorReset, name = "api-integrator-reset"),
    path("integrator-delete/<str:pk>", views.integratorDelete, name = "api-integrator-delete"),
    path("integrator-delete-all/", views.integratorDeleteAll, name = "api-integrator-delete-all")
]