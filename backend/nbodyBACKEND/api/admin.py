from django.contrib import admin
from .models import NBody
from .models import Integrator

# Register your models here.
admin.site.register(NBody)
admin.site.register(Integrator)