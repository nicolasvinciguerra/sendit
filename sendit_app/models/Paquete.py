from django.db import models

from sendit_app.models import Usuario
from sendit_app.models.Direccion import Direccion
from sendit_app.models.Estado_Paquete import Estado_Paquete
from sendit_app.models.Envio import Envio


class Paquete(models.Model):
    fecha_hora_entrega = models.DateTimeField(null=True)
    destinatario = models.ForeignKey('Usuario', null=True)
    direccion = models.ForeignKey(Direccion)
    precio = models.FloatField(null=True)
    estado_choices = ((Estado_Paquete.GENERADO, 'Generado'), (Estado_Paquete.ENTREGADO, 'Entregado'),
                      (Estado_Paquete.EN_VIAJE, 'En viaje'), (Estado_Paquete.NO_ENTREGADO, 'No entregado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=Estado_Paquete.GENERADO)
    envio = models.ForeignKey(Envio)
