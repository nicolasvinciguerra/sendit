from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser
from django.db import models

from sendit_app.models.Categoria import Categoria
from sendit_app.models.EstadoRepartidor import EstadoRepartidor
from sendit_app.models.Sexo import Sexo
from sendit_app.models.Vehiculo import Vehiculo


class User(AbstractUser):
    es_repartidor = models.BooleanField(default=False)
    es_remitente = models.BooleanField(default=False)
    fecha_alta_user = models.DateTimeField(auto_now_add=True)
    telefono = models.CharField(max_length=10, null=True)

    def get_perfil_remitente(self):
        remitente_profile = None
        if hasattr(self, 'remitenteprofile'):
            remitente_profile = self.remitenteprofile
        return remitente_profile

    def get_perfil_repartidor(self):
        repartidor_profile = None
        if hasattr(self, 'repartidorprofile'):
            repartidor_profile = self.repartidorprofile
        return repartidor_profile

    class Meta:
        db_table = 'auth_user'


class PerfilRemitente(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField(null=True)
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.CharField(max_length=1, choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15, null=True)
    empresa = models.BooleanField(default=False)
    cuit = models.CharField(max_length=10, null=True)
    razon_social = models.CharField(max_length=30, null=True)

    def es_empresa(self):
        return self.empresa

    def __str__(self):
        return self.user.username


class PerfilRepartidor(models.Model):
    user = models.OneToOneField(User, primary_key=True, on_delete=models.CASCADE)
    fecha_ultima_modificacion = models.DateTimeField(auto_now=True)
    fecha_nacimiento = models.DateField()
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.CharField(max_length=1, choices=sexo_choices)
    dni = models.CharField(max_length=10)
    vehiculo = models.ForeignKey(Vehiculo, null=True)
    categoria_choices = ((Categoria.DELIVERY_COMIDA, 'Delivery Comida'),
                         (Categoria.DELIVERY_CHICO, 'Delivery Paqueteria Pequeña y Documentos'),
                         (Categoria.DELIVERY_MEDIANO, 'Delivery Paqueteria Mediana'),
                         (Categoria.DELIVERY_GRANDE, 'Delivery Grandes Objetos'))
    categoria = models.CharField(max_length=10, choices=categoria_choices)
    estado_choices = ((EstadoRepartidor.INACTIVO, 'Inactivo'), (EstadoRepartidor.ACTIVO, 'Activo'),
                      (EstadoRepartidor.OCUPADO, 'Ocupado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=EstadoRepartidor.INACTIVO)
    puntaje_prom = models.FloatField(default=0)
    posicion_longitud = models.FloatField(null=True)
    posicion_latitud = models.FloatField(null=True)
    fecha_hora_ultima_pos = models.DateTimeField(null=True)

    def __str__(self):
        return self.user.username
