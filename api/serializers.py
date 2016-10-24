from django.contrib.auth import authenticate
from django.core.validators import validate_email
from rest_framework import exceptions
from rest_framework import serializers
from rest_framework.generics import get_object_or_404

from sendit_app.models.User import *
from sendit_app.models.Vehiculo import Vehiculo


class VehiculoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehiculo
        fields = '__all__'


class UserInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'es_repartidor', 'es_remitente', 'telefono',)


class UserOutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'es_repartidor', 'es_remitente', 'telefono',)


class PerfilRemitenteInputSerializer(serializers.ModelSerializer):
    user = UserInputSerializer(required=True)

    class Meta:
        model = PerfilRemitente
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(
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
        return remitente


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
