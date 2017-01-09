from django.utils import timezone
from django.db import models
from sendit_app.models.User import User


class PagoRepartidor(models.Model):
    fecha_hora = models.DateTimeField(default=timezone.now)
    monto = models.FloatField()
    repartidor = models.ForeignKey(User)
    fecha_hora_Pagado = models.DateTimeField(null=True)