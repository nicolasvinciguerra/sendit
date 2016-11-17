from api.utils import id_generator
from sendit_app.models import Envio, EstadoEnvio, PerfilRepartidor, EstadoRepartidor
from sendit_app.models import PerfilRemitente
from sendit_app.models import Plan
from sendit_app.models import RastreoEnvio


class EnvioService:
    def buscar_notificar_repartidor(self, envio_id): #notificar al repartidor de un envio
        envio= Envio.objects.get(id=envio_id)
        if envio.estado == EstadoEnvio.GENERADO:
            repartidores = PerfilRepartidor.objects.filter(estado=EstadoRepartidor.ACTIVO, categoria=envio.categoria,)
            #NOTIFICAR A repartidores del envio


    def crear_envio(self, datos, user, plan_id):
        envio = Envio(
            estado=EstadoEnvio.GENERADO,
            remitente=PerfilRemitente.objects.get(user=user),
            # destinatario=PerfilRemitente.objects.get(user=User.objects.get(username=validated_data['destinatario'])),
            email_destinatario=datos['email_destinatario'],
            telefono_destinatario=datos['telefono_destinatario'],
            categoria=datos['categoria'],
            requiere_confirmacion=datos['requiere_confirmacion'],
            direccion_destino=datos['direccion_destino'],
            direccion_origen=datos['direccion_origen'],
            plan=Plan.objects.get(id=plan_id),
            precio=53.5
        )
        envio.nro_tracking = envio.id
        if envio.requiere_confirmacion:
            envio.codigo_recepcion = id_generator()
        envio.save()
        return envio.id

    def cancelar_envio(self,envio_id):
            envio = Envio.objects.get(id=envio_id)
            envio.estado = EstadoEnvio.CANCELADO
            envio.save()

    def repartidor_envio(self,envio_id):
        envio = Envio.objects.get(id=envio_id)
        if envio.repartidor:
            repartidor = PerfilRepartidor.objects.get(user=envio.repartidor)
            return {'status':'repartidor asiganado', 'repartidor_name':repartidor.user.first_name, 'repartidor_last_name': repartidor.user.last_name}
        return {'status':'repartidor no asignado'}

    def rastrear_envio(self,envio_id):
        return RastreoEnvio.objects.filter(envio_id=envio_id).last('fecha_hora')


