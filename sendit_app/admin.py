from django.contrib import admin

from sendit_app.models.User import User, PerfilRepartidor, PerfilRemitente
from sendit_app.models.Plan import Plan

admin.site.register(User)
admin.site.register(PerfilRepartidor)
admin.site.register(PerfilRemitente)
admin.site.register(Plan)
#Agregar las demas clases para manejar con el admin de django