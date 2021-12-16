from django.db import models

# Create your models here.

class NBody(models.Model):
    positions = models.JSONField()
    velocities = models.JSONField()
    masses = models.JSONField()
    collision_tolerance = models.FloatField()
    escape_tolerance = models.FloatField()

    def __str__(self) -> str:
        return super().__str__()

class Integrator(models.Model):
    name = models.TextField()
    steps = models.FloatField()
    delta = models.FloatField()
    tolerance = models.FloatField()
    adaptive = models.BooleanField()
    adaptive_constant = models.FloatField()
    delta_lim = models.FloatField()
    nbody_id = models.ForeignKey(NBody, on_delete = models.CASCADE, db_column = "nbody_id")
    position_orbits = models.JSONField()
    velocity_orbits = models.JSONField()

    def __str__(self) -> str:
        return self.name





