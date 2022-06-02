from django.core.mail import send_mail

from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, GenreTitle, Title, User
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, UserSerializer, YamdbTokenObtainPairSerializer
from .viewsets import CreateListDestroyViewSet, CreateViewSet


class UserViewSet(CreateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def send_confirmation_code(self):
        confirmation_code = 'asdftyui'
        send_mail(
            subject='Confirmation code',
            message=confirmation_code,
            from_email='fake@yamdb.fake',
            recipient_list=['fake@yamdb.fake']
        )
        return confirmation_code

    def perform_create(self, serializer):
        user = User(username=self.request.data['username'],
                    email=self.request.data['email'])
        user.set_password(self.send_confirmation_code())
        user.save()


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)

