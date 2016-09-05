from django.db import models
from sendit_app.models.Repartidor import Repartidor


class Calificacion(models.Model):
    puntaje = models.IntegerField
    comentario = models.CharField(max_length=300, null=True)
    repartidor = models.ForeignKey(Repartidor)