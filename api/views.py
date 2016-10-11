from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from api.serializers import PerfilRemitenteSerializer, UserSerializer
from sendit_app.models import User


class UserViewSet(viewsets.ModelViewSet):
    model = User
    serializer_class = UserSerializer

    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


'''
@api_view(['GET'])
def current_user(request):
    if User.objects.get(request.user).es_remitente:
        serializer = PerfilRemitenteSerializer(request.user)
        return Response(serializer.data)
'''
