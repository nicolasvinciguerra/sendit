from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from sendit_app.models.User import User, PerfilRemitente, PerfilRepartidor
from api.serializers import PerfilRemitenteSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class RemitenteViewSet(viewsets.ModelViewSet):
    queryset = PerfilRemitente.objects.all()
    serializer_class = PerfilRemitenteSerializer

    # solo me va a devolver el usuario que tiene una sesion..REVISAR ESTO!
    def list(self, request, *args, **kwargs):
        queryset = PerfilRemitente.objects.all()
        user = get_object_or_404(queryset, user=request.user)
        serializer = RemitenteViewSet(user)
        return Response(serializer.data)


class RepartidorViewSet(viewsets.ModelViewSet):
    queryset = PerfilRepartidor.objects.all()
    serializer_class = PerfilRepartidor


'''
    def get_object(self):
        return self.request.user

    def list(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
'''

'''
@api_view(['GET'])
def current_user(request):
    if User.objects.get(request.user).es_remitente:
        serializer = PerfilRemitenteSerializer(request.user)
        return Response(serializer.data)
'''
