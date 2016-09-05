from django.db import models
from sendit_app.modelos.Usuario import Usuario
from sendit_app.modelos.Sexo import Sexo

class Persona(Usuario):
    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    fecha_Nacimiento = models.DateTimeField(null=True)
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'),(Sexo.MUJER, 'Mujer'))
    sexo = models.BinaryField(choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15, null=True)