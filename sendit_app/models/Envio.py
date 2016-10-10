from django.db import models
from django.utils import timezone
from sendit_app.models import Remitente
from sendit_app.models.Repartidor import Repartidor
from sendit_app.models.Plan import Plan
from sendit_app.models.EstadoEnvio import EstadoEnvio


class Envio(models.Model):
    fecha_hora_generado = models.DateTimeField(default=timezone.now)
    fecha_hora_entregado = models.DateTimeField(null=True)
    estado_choices = (
        (EstadoEnvio.GENERADO, 'Generado'), (EstadoEnvio.CANCELADO, 'Cancelado'),
        (EstadoEnvio.EN_ESPERA, 'En espera'),
        (EstadoEnvio.CONFIRMADO, 'Confirmado'), (EstadoEnvio.EN_VIAJE, 'En viaje'),
        (EstadoEnvio.ENTREGADO, 'Entregado'),
        (EstadoEnvio.NO_ENTREGADO, 'No entregado'))
    estado = models.CharField(max_length=10, choices=estado_choices, default=EstadoEnvio.GENERADO)
    repartidor = models.ForeignKey(Repartidor, related_name='envio_repartidor', null=True, unique=False)
    remitente = models.ForeignKey(Remitente)
    categoria = models.CharField(max_length=10, choices=Repartidor.categoria_choices)
    codigo_recepcion = models.CharField(max_length=10, null=True)  # cuando haces un envio seguro, este codigo debe introducir el destinatario para confirmar recepcion
    nro_tracking = models.CharField(max_length=10)  # numero para poder rastrear el envio
    plan = models.ForeignKey(Plan, null=True)
