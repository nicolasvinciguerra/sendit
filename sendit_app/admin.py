from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models.Plan import Plan
from .models.Repartidor import Repartidor
from .models.Remitente import Remitente

admin.site.register(Plan)
admin.site.register(Remitente)
admin.site.register(Repartidor)


class RepartidorInline(admin.StackedInline):
    model = Repartidor
    can_delete = False
    verbose_name_plural = 'repartidor'


class RemitenteInline(admin.StackedInline):
    model = Remitente
    can_delete = False
    verbose_name_plural = 'remitente'


class UserAdmin(UserAdmin):
    inliness = (RepartidorInline, RemitenteInline, )


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
