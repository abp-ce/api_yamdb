from django.core.mail import send_mail
from rest_framework import filters
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from reviews.models import Category, Genre, GenreTitle, Title, User
from .permissions import IsAdminOrReadOnly
from .serializers import CategorySerializer, UserSerializer
from .viewsets import CreateListDestroyViewSet, CreateUpdateViewSet


class UserViewSet(CreateUpdateViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def send_password():
        password = 'asdftyui'
        send_mail(
            subject='Confirmation code',
            message=password,
            from_email='fake@yamdb.fake',
            recipient_list=['fake@yamdb.fake']
        )
        return 'asdftyui'

    def perform_create(self, serializer):
        serializer.save(password=self.send_password)

    def perform_update(self, serializer):
        serializer.save(password=self.send_password)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
