from django.db import models


class Plan(models.Model):
    fecha_desde = models.DateField(null=True)
    fecha_hasta = models.DateField(null=True)
    limite_km = models.FloatField(default=0)
    precio_km = models.FloatField(default=0)
