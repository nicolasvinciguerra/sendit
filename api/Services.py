from sendit_app.models import Envio, EstadoEnvio, PerfilRepartidor, EstadoRepartidor


class EnvioService:
    def buscar_notificar_repartidor(self, id_envio): #notificar al repartidor de un envio
        envio= Envio.objects.get(id=id_envio)
        if envio.estado == EstadoEnvio.GENERADO:
            repartidores = PerfilRepartidor.objects.filter(estado=EstadoRepartidor.ACTIVO, categoria=envio.categoria,)
            #NOTIFICAR A repartidores del envio
