from api.viewSets import UserViewSet, RepartidorViewSet, RemitenteViewSet
from rest_framework.routers import DefaultRouter
from django.conf.urls import url

from api import views

router = DefaultRouter()
router.register(r'users/remitente', RemitenteViewSet)
router.register(r'users/repartidor', RepartidorViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    url(r'^api-token/', views.obtain_auth_token)
]

urlpatterns += router.urls