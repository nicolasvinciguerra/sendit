from django.db import models

class Calificacion(models.Model):
    puntaje = models.IntegerField
    comentario = models.CharField(max_length=300, null=True)