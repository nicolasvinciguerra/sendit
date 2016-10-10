from django.contrib.auth.models import User
from django.db import models
from sendit_app.models.Sexo import Sexo
from django.db.models.signals import post_save
from django.dispatch import receiver


class Remitente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fecha_alta_user = models.DateTimeField(auto_now_add=True)
    fecha_nacimiento = models.DateField(null=True)
    sexo_choices = ((Sexo.HOMBRE, 'Hombre'), (Sexo.MUJER, 'Mujer'))
    sexo = models.BinaryField(choices=sexo_choices, null=True)
    dni = models.CharField(max_length=15, null=True)
    empresa = models.BinaryField(default=0)
    cuit = models.CharField(max_length=10, null=True)
    razon_social = models.CharField(max_length=30, null=True)

    def es_empresa(self):
        if self.Empresa == 1:
            return True
        return False


@receiver(post_save, sender=User)
def create_user_remitente(sender, instance, created, **kwargs):
    if created:
        Remitente.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_remitente(sender, instance, **kwargs):
    instance.remitente.save()
