from django.db import models
from django.utils import timezone
from sendit_app.models.Envio import Envio




class Rastreo(models.Model):
    fecha_hora = models.DateTimeField(default= timezone.now)
    latitud = models.FloatField
    longitud = models.FloatField
    velocidad = models.FloatField
    Envio = models.ForeignKey(Envio)