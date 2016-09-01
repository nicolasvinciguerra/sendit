from django.db import models

class Usuario(models.Model):
    nombre_usuario = models.CharField(max_length=60, unique=True)
    mail = models.EmailField(unique=True, null=True)
    password = models.CharField(max_length=300)
    telefono = models.CharField(max_length=30, null=True)
    direccion = models.ForeignKey(Direccion, null=True)
