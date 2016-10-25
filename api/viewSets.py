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

from sendit_app.models import Envio
from sendit_app.models.User import User, PerfilRemitente, PerfilRepartidor
from api.serializers import PerfilRemitenteInputSerializer, UserInputSerializer, PerfilRepartidorInputSerializer, \
    PerfilRemitenteOutputSerializer, UserOutputSerializer, PerfilRepartidorOutputSerializer, EnvioSerializer


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


class RemitenteViewSet(viewsets.ModelViewSet):
    queryset = PerfilRemitente.objects.all()
    serializer_class = PerfilRemitenteInputSerializer

    @list_route(methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        model_serializer = PerfilRemitenteInputSerializer(data=request.data)
        model_serializer.is_valid(raise_exception=True)
        model_serializer.save()

        return Response(model_serializer.data)

    @list_route(methods=['get'], permission_classes=[IsAuthenticated],
                authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def me(self, request, *args, **kwargs):
        obj = get_object_or_404(RemitenteViewSet.queryset, user=request.user)
        serializer = PerfilRemitenteOutputSerializer(obj)
        return Response(serializer.data)

    def list(self, request):
        user = request.user
        if not user or not user.is_superuser:
            return HttpResponseForbidden()
        return super(RemitenteViewSet, self).list(request)

    def update(self, request, pk=None):
        user = User.objects.filter(id=pk).first()
        if not user or request.user != user:
            return HttpResponseForbidden()
        return super(RemitenteViewSet, self).update(request, pk=user.id)

    @detail_route(methods=['get'], permission_classes=[IsAuthenticated],
                  authentication_classes=(SessionAuthentication, TokenAuthentication,))
    def envios(self, request):
        serializer = EnvioSerializer(self.request.user.envio_remitente.all())
        return Response(serializer.data)



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


class EnviosUserViewSet(viewsets.ModelViewSet):
    serializer_class = EnvioSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (SessionAuthentication, TokenAuthentication,)
    queryset = Envio.objects.all()

    def list(self, request, *args, **kwargs):
        user = request.user
        if not user or not user.is_superuser:
            return HttpResponseForbidden()
        return super(EnviosUserViewSet, self).list(request)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)



