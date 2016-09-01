from django.db import models
from django.utils import timezone
from sendit_app.modelos.Calificacion import Calificacion
from sendit_app.modelos.Empresa import Empresa
from sendit_app.modelos.Envio import Envio
from sendit_app.modelos.Pago_Repartidor import Pago_Repartidor
from sendit_app.modelos.Paquete import Paquete
from sendit_app.modelos.Persona import Persona
from sendit_app.modelos.Rastreo import Rastreo
from sendit_app.modelos.Repartidor import Repartidor
from sendit_app.modelos.Direccion import Direccion


class Vehiculo(models.Model):
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    patente = models.CharField(max_length=60)
    seguro = models.CharField(max_length=60)
    tipo = models.CharField(max_length=60)


class Plan(models.Model):
    fecha_desde = models.DateField
    fecha_hasta = models.DateField
    limite_km = models.FloatField
    precio_km = models.FloatField


class Categoria():
    DELIVERY_COMIDA = 'COMIDA'
    DELIVERY_CHICO = 'CHICO'
    DELIVERY_MEDIANO = 'MEDIANO'
    DELIVERY_GRANDE = 'GRANDE'

class Sexo():
    HOMBRE = 0
    MUJER = 1

class Estado_Repartidor():
    INACTIVO = 'INACTIVO'
    ACTIVO = 'ACTIVO'
    OCUPADO = 'OCUPADO'

class Estado_Envio ():
    GENERADO = 'GENERADO'
    CANCELADO = 'CANCELADO'
    EN_ESPERA = 'ESPERA'
    CONFIRMADO = 'CONFIRMADO'
    EN_VIAJE = 'VIAJE'
    NO_ENTREGADO = 'NO_ENTREGADO'
    ENTREGADO = 'ENTREGADO'


class Estado_Paquete ():
    GENERADO = 'GENERADO'
    EN_VIAJE = 'VIAJE'
    NO_ENTREGADO = 'NO_ENTREGADO'
    ENTREGADO = 'ENTREGADO'



























