from django.urls import include, path
from rest_framework import routers

<<<<<<< HEAD
from .views import (CategoryViewSet, CommentViewSet, ReviewViewSet,
                    UserViewSet, YamdbTokenObtainPairView, request_email)

# from rest_framework_simplejwt.views import TokenObtainPairView

=======
from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserMeViewSet, UserViewSet,
                    get_token, request_email)
>>>>>>> master

app_name = 'api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='users')
router.register(r'categories', CategoryViewSet, basename='categories')
router.register(r'genres', GenreViewSet, basename='genres')
router.register(r'titles', TitleViewSet, basename='titles')
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

urlpatterns = [
    path('v1/users/me/', UserMeViewSet.as_view({'get': 'me', 'patch': 'me'}), name="me"),
    path('v1/', include(router.urls)),
    path('v1/auth/token/', get_token, name='token'),
    path('v1/auth/signup/', request_email, name='signup'),
]
