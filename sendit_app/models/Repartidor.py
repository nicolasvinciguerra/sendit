from django.db import models
from django.contrib.auth.models import User
from sendit_app.models.Categoria import Categoria
from sendit_app.models.Sexo import Sexo
from sendit_app.models.Vehiculo import Vehiculo
from sendit_app.models.EstadoRepartidor import EstadoRepartidor
from django.db.models.signals import post_save
from django.dispatch import receiver


class Repartidor(models.Model):
    user = models.OneToOneField(User)
    fecha_alta_user = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.BinaryField(choices=sexo_choices)
    dni = models.CharField(max_length=10)
    telefono = models.CharField(max_length=10)
    vehiculo = models.ForeignKey(Vehiculo)
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


@receiver(post_save, sender=User)
def create_user_repartidor(sender, instance, created, **kwargs):
    if created:
        Repartidor.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_repartidor(sender, instance, **kwargs):
    instance.repartidor.save()
