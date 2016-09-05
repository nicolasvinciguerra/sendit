from django.db import models

class Plan(models.Model):
    fecha_desde = models.DateField
    fecha_hasta = models.DateField
    limite_km = models.FloatField
    precio_km = models.FloatField