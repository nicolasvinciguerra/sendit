from django.db import models
from django.utils import timezone
from sendit_app.models import Usuario
from sendit_app.models.Repartidor import Repartidor
from sendit_app.models.Plan import Plan
from sendit_app.models.Estado_Envio import Estado_Envio


class Envio(models.Model):
    fecha_hora_generado = models.DateTimeField(default=timezone.now)
    fecha_hora_entregado = models.DateTimeField(null=True)
    estado_choices = (
        (Estado_Envio.GENERADO, 'Generado'), (Estado_Envio.CANCELADO, 'Cancelado'),
        (Estado_Envio.EN_ESPERA, 'En espera'),
        (Estado_Envio.CONFIRMADO, 'Confirmado'), (Estado_Envio.EN_VIAJE, 'En viaje'),
        (Estado_Envio.ENTREGADO, 'Entregado'),
        (Estado_Envio.NO_ENTREGADO, 'No entregado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=Estado_Envio.GENERADO)
    repartidor = models.ForeignKey(Repartidor, related_name='envio_repartidor', null=True, unique=False)
    remitente = models.ForeignKey('Usuario', related_name='envio_remitente')
    categoria = models.CharField(max_length=10, choices=Repartidor.categoria_choices)
    codigo_recepcion = models.CharField(max_length=10, null=True)  # cuando haces un envio seguro, este codigo debe introducir el destinatario para confirmar recepcion
    nro_tracking = models.CharField(max_length=10)  # numero para poder rastrear el envio
    plan = models.ForeignKey(Plan, null=True)
