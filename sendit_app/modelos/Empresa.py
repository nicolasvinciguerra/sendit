from django.db import models
from sendit_app.modelos.Usuario import Usuario

class Empresa(Usuario):
    razon_social = models.CharField(max_length=60)
    cuit = models.CharField(max_length=15)