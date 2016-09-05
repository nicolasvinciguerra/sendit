from django.db import models
from sendit_app.models.Usuario import Usuario
from sendit_app.models.Sexo import Sexo


class Persona(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_nacimiento = models.DateTimeField(null=True)
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.BinaryField(choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15, null=True)
