from django.db import models

class Pago_Repartidor(models.Model):
    fecha_hora = models.DateTimeField(default=timezone.now)
    monto = models.FloatField()
    repartidot = models.ForeignKey(Repartidor)