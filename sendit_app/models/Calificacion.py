from django.db import models
from sendit_app.models.User import User


class Calificacion(models.Model):
    puntaje = models.IntegerField
    comentario = models.CharField(max_length=300, null=True)
    repartidor = models.ForeignKey(User)
