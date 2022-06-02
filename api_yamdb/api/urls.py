from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, GenreViewSet, TitleViewSet, UserViewSet,
                    YamdbTokenObtainPairView, request_email)

# from rest_framework_simplejwt.views import TokenObtainPairView


app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'auth/signup', UserViewSet, basename='signup')
# router.register(r'auth/token', YamdbTokenObtainPairView.as_view(),
#                 basename='token')
router.register(r'users', UserViewSet, basename='userss')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', YamdbTokenObtainPairView.as_view(), name='token'),
    path('v1/auth/signup/', request_email, name='signup')
]
