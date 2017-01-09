from django.db import models


class TipoVehiculo:
    MOTO_COMIDA = 'moto_com'
    MOTO_PAQUETERIA = 'moto_paq'
    AUTO = 'auto'
    CAMIONETA = 'camioneta'
    CAMION = 'camion'
    BICICLETA = 'bici'


class Vehiculo(models.Model):
    marca = models.CharField(max_length=60)
    modelo = models.CharField(max_length=60)
    patente = models.CharField(max_length=60)
    seguro = models.CharField(max_length=60)
    tipo_choices = ((TipoVehiculo.AUTO, 'Automovil'),
                    (TipoVehiculo.BICICLETA, 'Bicicleta'),
                    (TipoVehiculo.CAMION, 'Camión'),
                    (TipoVehiculo.CAMIONETA, 'Camioneta'),
                    (TipoVehiculo.MOTO_COMIDA, 'Moto con caja térmica'),
                    (TipoVehiculo.MOTO_PAQUETERIA, 'Moto con caja para paqueteria'))
    tipo = models.CharField(max_length=10, choices=tipo_choices)
