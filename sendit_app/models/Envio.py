from django.db import models
from django.utils import timezone

from sendit_app.models import Direccion
from sendit_app.models.Categoria import Categoria
from sendit_app.models.EstadoEnvio import EstadoEnvio
from sendit_app.models.Plan import Plan
from sendit_app.models.User import PerfilRepartidor, PerfilRemitente


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
    repartidor = models.ForeignKey(PerfilRepartidor, related_name='envio_repartidor', null=True, unique=False)
    destinatario = models.ForeignKey(PerfilRemitente, related_name='envio_destinatario', null=True, unique=False)
    telefono_destinatario = models.CharField(max_length=15, null=True)
    email_destinatario = models.CharField(max_length=30, null=True)
    remitente = models.ForeignKey(PerfilRemitente, related_name='envio_remitente', unique=False)
    categoria_choices = ((Categoria.DELIVERY_COMIDA, 'Delivery Comida'),
                         (Categoria.DELIVERY_CHICO, 'Delivery Paqueteria Pequeña y Documentos'),
                         (Categoria.DELIVERY_MEDIANO, 'Delivery Paqueteria Mediana'),
                         (Categoria.DELIVERY_GRANDE, 'Delivery Grandes Objetos'))
    categoria = models.CharField(max_length=10, choices=categoria_choices, default=Categoria.DELIVERY_CHICO)
    requiere_confirmacion = models.BooleanField()
    codigo_recepcion = models.CharField(max_length=10, null=True)  # cuando haces un envio seguro, este codigo debe introducir el destinatario para confirmar recepcion
    nro_tracking = models.CharField(max_length=10, null=True)  # numero para poder rastrear el envio
    plan = models.ForeignKey(Plan, null=True)
    direccion_origen = models.ForeignKey(Direccion, related_name='direccion_origen')
    direccion_destino = models.ForeignKey(Direccion, related_name='direccion_destino')
    precio = models.FloatField()
    pagado = models.BooleanField(default=False)
