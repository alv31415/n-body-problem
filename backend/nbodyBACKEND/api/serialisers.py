from rest_framework import serializers
from .models import NBody, Integrator

class NBodySerialiser(serializers.ModelSerializer):
    class Meta:
        model = NBody
        fields = "__all__"

class IntegratorSerialiser(serializers.ModelSerializer):
    class Meta:
        model = Integrator
        fields = "__all__"