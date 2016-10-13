from api.views import UserViewSet, RemitenteViewSet, RepartidorViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'users/remitente', RemitenteViewSet)
router.register(r'users/repartidor', RepartidorViewSet)
router.register(r'users', UserViewSet)

urlpatterns = router.urls
