from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.decorators import api_view, list_route, detail_route
from rest_framework.generics import get_object_or_404, CreateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from sendit_app.models import Envio, Vehiculo, EstadoEnvio
from sendit_app.models.User import User, PerfilRemitente, PerfilRepartidor
from api.serializers import PerfilRemitenteInputSerializer, UserInputSerializer, PerfilRepartidorInputSerializer, \
    PerfilRemitenteOutputSerializer, UserOutputSerializer, PerfilRepartidorOutputSerializer, EnvioSerializer, VehiculoSerializer
from api.Services import EnvioService


class UserViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()

    @list_route(methods=['get', 'put'], permission_classes=[IsAuthenticated], authentication_classes=(SessionAuthentication, TokenAuthentication,))
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

    @detail_route(methods=['post'], permission_classes=[IsAuthenticated], authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def set_password(self, request, pk=None):
        user = self.get_object()
        serializer = PasswordSerializer(data=request.data)
        if serializer.is_valid():
            user.set_password(serializer.data['password'])
            user.save()
            return Response({'status': 'password set'})
        else:
            return Response(serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class RemitenteViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet,
                        mixins.UpdateModelMixin, mixins.RetrieveModelMixin):
    queryset = PerfilRemitente.objects.all()
    serializer_class = PerfilRemitenteInputSerializer

    '''@list_route(methods=['post'], permission_classes=[AllowAny]) #NO FUNCIONANDO, PARA REGISTRO /users/reartidor metodo:post
    def register(self, request):
        return Response({'id_user': RemitenteViewSet.create(self, request)})
    '''

    @list_route(methods=['get', 'put'], permission_classes=[IsAuthenticated],
                authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def me(self, request, *args, **kwargs):
        self.serializer_class = PerfilRemitenteOutputSerializer
        view = RemitenteViewSet.as_view({'get': 'retrieve', 'put': 'update'})
        return view(request, pk=request.user.id)


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

    @detail_route(methods=['put'], permission_classes=[IsAuthenticated], authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def actualizar_ubicacion(self, request, pk):
        repartidor_serializer = PerfilRepartidorInputSerializer(
            instance=PerfilRepartidor.objects.get(user=request.user),
            data=self.request.data,
            partial=True
        )
        if repartidor_serializer.is_valid():
            repartidor_serializer.save()
        return Response({'status':'actualizado'})

    @list_route(methods=['get', 'put'], permission_classes=[IsAuthenticated],
                authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def me(self, request, *args, **kwargs):
        self.serializer_class = PerfilRepartidorOutputSerializer
        view = RepartidorViewSet.as_view({'get': 'retrieve', 'put': 'update'})
        return view(request, pk=request.user.id)



class TestUpdateVehiculo(viewsets.ModelViewSet):
    queryset = Vehiculo.objects.all()
    serializer_class = VehiculoSerializer

    def update(self, request, *args, **kwargs):
        vehiculo_serializer = VehiculoSerializer(
            instance=self.get_object(),
            data=self.request.data,
            partial=True
        )
        if vehiculo_serializer.is_valid():
            vehiculo_serializer.save()
        return Response(vehiculo_serializer.data)


class EnviosViewSet(viewsets.ModelViewSet):
    authentication_classes = (SessionAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)

    queryset = Envio.objects.all()
    serializer_class = EnvioSerializer

    def create(self, request, *args, **kwargs):
        return Response({'envio_id': EnvioService.crear_envio(self, datos=request.data, user=request.user, plan_id=1)})

    @detail_route(methods=['get'])
    def reintentar_busqueda(self, request, pk):
        EnvioService.buscar_notificar_repartidor(pk)
        return Response({'status': 'buscando y notificando repartidores'})

    @detail_route(methods=['get'])
    def cancelar_busqueda(self, request, pk):
        EnvioService.cancelar_envio(pk)
        return  Response({'status':'envio cancelado'})

    @detail_route(methods=['get'])
    def get_repartidor(self, request, pk):
        return EnvioService.repartidor_envio(pk)


    @detail_route(methods=['get'])
    def tracking_envio(self, request, pk):
        tracking = EnvioService.rastrear_envio(pk)
        return {'lat':tracking.latitud, 'lon':tracking.longitud}

    def get_queryset(self):
        """
        This view should return a list of all the envios
        for the currently authenticated user.
        """
        if self.request.user.es_remitente:
            remitente = PerfilRemitente.objects.get(user=self.request.user)
            return Envio.objects.filter(remitente=remitente)
        else:
            repartidor = PerfilRepartidor.objects.get(user=self.request.user)
            return Envio.objects.filter(estado=EstadoEnvio.GENERADO, categoria=repartidor.categoria)