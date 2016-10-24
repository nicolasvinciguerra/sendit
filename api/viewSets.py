from django.contrib.auth import get_user_model
from rest_framework import generics
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, list_route, detail_route
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from sendit_app.models.User import User, PerfilRemitente, PerfilRepartidor
from api.serializers import PerfilRemitenteInputSerializer, UserInputSerializer, PerfilRepartidorInputSerializer, \
    PerfilRemitenteOutputSerializer, UserOutputSerializer, PerfilRepartidorOutputSerializer


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    @list_route(methods=['get', 'put'], permission_classes=[IsAuthenticated], authentication_classes=(TokenAuthentication,))
    def me(self, request, *args, **kwargs):
        try:
            user = User.objects.get(username=request.user)
            if user.es_remitente:
                self.serializer_class = PerfilRemitenteOutputSerializer
                view = RemitenteViewSet.as_view({'get': 'retrieve', 'put': 'update'})
                return view(request, pk=user.id)
            if user.es_repartidor:
                self.serializer_class = PerfilRepartidorOutputSerializer
                view = RepartidorViewSet.as_view({'get': 'retrieve', 'put': 'update'})
                return view(request, pk=user.id)
        except:
            return Response(status=404, template_name=FileNotFoundError) #Revisar aca que devuevlo si no encuentro al usuario por alguna razon


class RemitenteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet,
                       mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = PerfilRemitente.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerfilRemitenteOutputSerializer
        if self.action == 'list':
            return PerfilRemitenteOutputSerializer
        if self.action == 'create':
            return PerfilRemitenteInputSerializer
        if self.action == 'update':
            return PerfilRemitenteInputSerializer



class RepartidorViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = PerfilRepartidor.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return PerfilRepartidorOutputSerializer
        if self.action == 'list':
            return PerfilRepartidorOutputSerializer
        if self.action == 'create':
            return PerfilRepartidorInputSerializer
        if self.action == 'update':
            return PerfilRepartidorInputSerializer
