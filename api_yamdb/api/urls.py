from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'auth/signup', UserViewSet, basename='signup')

urlpatterns = [
    path('v1/', include(router.urls)),
]
