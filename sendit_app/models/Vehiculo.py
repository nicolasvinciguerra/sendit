from django.db import models


class Vehiculo(models.Model):
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    patente = models.CharField(max_length=60)
    seguro = models.CharField(max_length=60)
    tipo = models.CharField(max_length=60)
