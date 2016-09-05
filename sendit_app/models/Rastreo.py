from django.db import models

class Rastreo(models.Model):
    fecha_hora = models.DateTimeField(default= timezone.now)
    latitud = models.FloatField
    longitud = models.FloatField