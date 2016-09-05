from django.db import models

class Direccion(models.Model):
    calle = models.CharField(max_length=60)
    numero = models.IntegerField
    piso_dpto = models.CharField(max_length=15, null=True)
    ciudad = models.CharField(max_length=30)
    observacion = models.CharField(max_length=60, null=True)
    pais = models.CharField(max_length=20, null=True, default='Argentina')

