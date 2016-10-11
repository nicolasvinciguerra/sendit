from rest_framework import serializers
from sendit_app.models.User import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'es_repartidor', 'es_remitente',)


class PerfilRemitenteSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = PerfilRemitente
        fields = '__all__'

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User(
            username=user_data['username'],
            email=user_data['email'],
        )
        user.set_password(user_data['password'])
        user.save()
        remitente = PerfilRemitente(
            user=user,
            fecha_nacimiento=validated_data['fecha_nacimiento'],
            sexo=validated_data['sexo'],
            dni=validated_data['dni'],
            empresa=validated_data['empresa'],
            cuit=validated_data['cuit'],
            razon_social=validated_data['razon_social']
        )
        return remitente


class PerfilRepartidorSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)

    class Meta:
        model = PerfilRepartidor
        fields = '__all__'
