from django.db import models

from sendit_app.models import Remitente
from sendit_app.models.Direccion import Direccion
from sendit_app.models.EstadoPaquete import EstadoPaquete
from sendit_app.models.Envio import Envio


class Paquete(models.Model):
    fecha_hora_entrega = models.DateTimeField(null=True)
    destinatario = models.ForeignKey(Remitente, null=True)
    direccion = models.ForeignKey(Direccion)
    precio = models.FloatField(null=True)
    estado_choices = ((EstadoPaquete.GENERADO, 'Generado'), (EstadoPaquete.ENTREGADO, 'Entregado'),
                      (EstadoPaquete.EN_VIAJE, 'En viaje'), (EstadoPaquete.NO_ENTREGADO, 'No entregado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=EstadoPaquete.GENERADO)
    envio = models.ForeignKey(Envio)
