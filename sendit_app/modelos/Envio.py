from django.db import models
from sendit_app.modelos.Plan import Plan
from sendit_app.modelos.Categoria import Categoria
from sendit_app.modelos.Estado_Envio import Estado_Envio

class Envio(models.Model):
    fecha_hora_generado = models.DateTimeField(default= timezone.now)
    fecha_hora_entregado = models.DateTimeField(null=True)
    estado_choices = ((Estado_Envio.GENERADO, 'Generado'),(Estado_Envio.CANCELADO, 'Cancelado'), (Estado_Envio.EN_ESPERA, 'En espera'), (Estado_Envio.CONFIRMADO, 'Confirmado'), (Estado_Envio.EN_VIAJE, 'En viaje'), (Estado_Envio.ENTREGADO, 'Entregado'), (Estado_Envio.NO_ENTREGADO, 'No entregado') )
    estado = models.CharField(max_length=10, choices= estado_choices, default=Estado_Envio.GENERADO)
    repartidor = models.ForeignKey(Repartidor, related_name='repartidor_envio', null=True)
    remitente = models.ForeignKey(Usuario, related_name='remitente_envio', null= True)
    categoria = models.CharField(max_length=10, choices=Repartidor.categoria_choices)
    nro_tracking = models.CharField(max_length=10)
    plan = models.ForeignKey(Plan, null=True)
    envio = models.ManyToOneRel(Paquete)
    rastreo = models.ManyToOneRel(Rastreo)
    paquetes = models.ManyToOneRel(Paquete)