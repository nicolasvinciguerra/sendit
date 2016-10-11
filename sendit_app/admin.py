from django.contrib import admin

from sendit_app.models.User import User, PerfilRepartidor, PerfilRemitente

admin.site.register(User)
admin.site.register(PerfilRepartidor)
admin.site.register(PerfilRemitente)
#Agregar las demas clases para manejar con el admin de django