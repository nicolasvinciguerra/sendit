from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from api import views

from rest_framework import routers
from api.views import UserViewSet

router = routers.SimpleRouter()
router.register(r'users', UserViewSet)

urlpatterns = router.urls
