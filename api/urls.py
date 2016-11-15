from api.viewSets import UserViewSet, RepartidorViewSet, RemitenteViewSet, EnviosViewSet,TestUpdateVehiculo, \
    EnviosRepartidorView
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from api import views

router = DefaultRouter()
router.register(r'users/remitente', RemitenteViewSet)
router.register(r'users/repartidor', RepartidorViewSet)
router.register(r'users', UserViewSet)
router.register(r'envios', EnviosViewSet)
router.register(r'test', TestUpdateVehiculo)


urlpatterns = [
    url(r'^token-login/', views.obtain_auth_token),
    url(r'^envios-repartidor/', EnviosRepartidorView.as_view())
]

urlpatterns += router.urls
