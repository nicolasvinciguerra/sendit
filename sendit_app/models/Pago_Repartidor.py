from django.utils import timezone
from django.db import models
from sendit_app.models import Repartidor


class Pago_Repartidor(models.Model):
    fecha_hora = models.DateTimeField(default=timezone.now)
    monto = models.FloatField()
    repartidor = models.ForeignKey(Repartidor)
    fecha_hora_Pagado = models.DateTimeField(null=True)