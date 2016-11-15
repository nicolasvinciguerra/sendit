from django.contrib.auth import authenticate
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from sendit_app.models import Direccion
from sendit_app.models import Envio
from sendit_app.models import EstadoEnvio
from sendit_app.models import Plan
from sendit_app.models.User import *
from sendit_app.models.Vehiculo import Vehiculo
from api.utils import id_generator


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'
        partial = True


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'first_name', 'last_name', 'es_repartidor', 'telefono',)


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'es_repartidor', 'telefono',)


class PerfilRemitenteInputSerializer(serializers.ModelSerializer):
    user = UserInputSerializer(required=True, partial=True)

    class Meta:
        model = PerfilRemitente
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            username=user_data['username'],
            email=user_data['email'],
            telefono=user_data['telefono'],
            es_remitente=True
        )
        user.set_password(user_data['password'])
        user.save()
        remitente = PerfilRemitente(
            user=user,
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            # deberia controlar que si no es empresa debe tener este campo y ser mayor de edad..
            sexo=validated_data['sexo'],
            dni=validated_data['dni'],
            empresa=validated_data['empresa'],
            cuit=validated_data['cuit'],
            razon_social=validated_data['razon_social']
        )
        remitente.save()
        return remitente.id


class PerfilRemitenteOutputSerializer(serializers.ModelSerializer):
    user = UserOutputSerializer(required=True)

    class Meta:
        model = PerfilRemitente
        read_only_fields = ('user',)
        fields = '__all__'


class PerfilRepartidorInputSerializer(serializers.HyperlinkedModelSerializer):  # VER EL TEMA DEL serializers.HyperlinkedModelSerializer
    user = UserInputSerializer(required=True)
    vehiculo = VehiculoSerializer(required=True)

    class Meta:
        model = PerfilRepartidor
        fields = '__all__'
        # depth = 1 #me devuelve los objetos completos adentros de este objeto (ej. vehiculo)

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        vehiculo_data = validated_data.pop('vehiculo')
        user = User(
            username=user_data['username'],
            email=user_data['email'],
            es_repartidor=True
        )
        user.set_password(user_data['password'])
        user.save()
        # si no carga el vehiculo ahora, deberia controlar si vehiculo tiene datos para guardarlo
        vehiculo = Vehiculo(
            marca=vehiculo_data['marca'],
            modelo=vehiculo_data['modelo'],
            patente=vehiculo_data['patente'],
            seguro=vehiculo_data['seguro'],
            tipo=vehiculo_data['tipo']
        )
        vehiculo.save()
        repartidor = PerfilRepartidor(
            user=user,
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            sexo=validated_data['sexo'],
            dni=validated_data['dni'],
            vehiculo=vehiculo,
            categoria=validated_data['categoria']
        )
        repartidor.save()
        return repartidor


class PerfilRepartidorOutputSerializer(serializers.HyperlinkedModelSerializer):
    user = UserOutputSerializer(required=True)
    vehiculo = VehiculoSerializer(required=True)

    class Meta:
        model = PerfilRepartidor
        fields = '__all__'


class AuthCustomTokenSerializer(serializers.Serializer):
    username = serializers.CharField(label=("Username"))
    password = serializers.CharField(label=("Password"), style={'input_type': 'password'})
    user_id = UserOutputSerializer(required=False)

    class Meta:
        model = Token
        fields = '__all__'


    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user:
                if not user.is_active:
                    msg = ('User account is disabled.')
                    raise serializers.ValidationError(msg)
            else:
                msg = ('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg)
        else:
            msg = ('Must include "username" and "password".')
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class DireccionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Direccion
        fields = '__all__'


class EnvioSerializer(serializers.ModelSerializer):
    direccion_origen = DireccionSerializer(required=True)
    direccion_destino = DireccionSerializer(required=True)

    class Meta:
        model = Envio
        fields = 'destinatario', 'telefono_destinatario', 'email_destinatario','categoria', 'requiere_confirmacion', 'direccion_origen', 'direccion_destino'

    def create(self, validated_data, user, current_plan):
        dir_origen_data = validated_data.pop('direccion_origen')
        dir_destino_data = validated_data.pop('direccion_destino')
        dir_origen = DireccionSerializer(dir_destino_data).save()
        dir_destino = DireccionSerializer(dir_origen_data).save()

        envio = Envio(
            estado=EstadoEnvio.GENERADO,
            remitente= PerfilRemitente.objects.get(user=user),
            destinatario=PerfilRemitente.objects.get(user__username=validated_data['destinatario']),
            email_destinatario=validated_data['email_destinatario'],
            telefono_destinatario=validated_data['telefono_destinatario'],
            categoria=validated_data['categoria'],
            requiere_confirmacion=validated_data['requiere_confirmacion'],
            direccion_destino_id=dir_destino.id,
            direccion_origen_id=dir_origen.id,
            plan=Plan.objects.get(id=current_plan),
            precio=53.5
        )
        envio.nro_tracking=envio.id
        if envio.requiere_confirmacion:
            envio.codigo_recepcion = id_generator()
        envio.save()
        return envio.id


