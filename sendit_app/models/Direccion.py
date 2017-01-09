from django.db import models


class Direccion(models.Model):
    calle = models.CharField(max_length=50)
    numero = models.IntegerField(null=True)
    piso = models.CharField(max_length=2, null=True)
    dpto = models.CharField(max_length=2, null=True)
    ciudad = models.CharField(max_length=30)
    pais = models.CharField(max_length=20, default='Argentina')
    observacion = models.CharField(max_length=60, null=True)
