from django.urls import include, path
from rest_framework import routers

from .views import CategoryViewSet, UserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'auth/signup', UserViewSet, basename='signup')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
]
