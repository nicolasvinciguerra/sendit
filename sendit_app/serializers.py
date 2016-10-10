from rest_framework import serializers
from sendit_app.models.Repartidor import Repartidor


class RepartidorSerializer(serializers.ModelSerializererializer):
    class Meta:
        model = Repartidor
