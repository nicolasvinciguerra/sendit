from django.db import models
class Direccion(models.Model):
    calle = models.CharField(max_length=60)
    numero = models.IntegerField
    ciudad = models.CharField(max_length=60)

