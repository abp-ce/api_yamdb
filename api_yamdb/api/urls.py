from django.urls import include, path
from rest_framework import routers
# from rest_framework_simplejwt.views import TokenObtainPairView

from .views import CategoryViewSet, UserViewSet, YamdbTokenObtainPairView, request_email

app_name = 'api'

router = routers.DefaultRouter()
# router.register(r'auth/signup', UserViewSet, basename='signup')
# router.register(r'auth/token', YamdbTokenObtainPairView.as_view(),
#                 basename='token')
router.register(r'categories', CategoryViewSet, basename='categories')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/token/', YamdbTokenObtainPairView.as_view(), name='token'),
    path('v1/auth/signup/', request_email, name='signup')
]
