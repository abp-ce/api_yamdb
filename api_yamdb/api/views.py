from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.core.validators import validate_email
from rest_framework import filters, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from reviews.models import Category, Genre, GenreTitle, Title, User, Review, Comment

from .permissions import IsAdminOrReadOnly
from .serializers import (CategorySerializer, UserSerializer,
                          UserSignupSerializer, YamdbTokenObtainPairSerializer)
from .viewsets import CreateListDestroyViewSet, CreateViewSet


def send_confirmation_code():
    confirmation_code = 'asdftyui'
    send_mail(
        subject='Confirmation code',
        message=confirmation_code,
        from_email='fake@yamdb.fake',
        recipient_list=['fake@yamdb.fake']
    )
    return confirmation_code


@api_view(['POST'])
@permission_classes((AllowAny, ))
def request_email(request):
    serializer = UserSignupSerializer(data=request.data)
    if 'username' not in serializer.initial_data:
        return Response('{ - username: [Отсутствует обязательное поле.] }',
                        status=status.HTTP_400_BAD_REQUEST)
    if 'email' not in serializer.initial_data:
        return Response('{ - email: [Отсутствует обязательное поле.] }',
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        validate_email(serializer.initial_data['email'])
    except ValidationError as error:
        return Response(error,
                        status=status.HTTP_400_BAD_REQUEST)
    if serializer.initial_data['username'] == 'me':
        return Response('Поле username не может быть me.',
                        status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(
        username=serializer.initial_data['username']
    ).exists():
        user = User.objects.get(username=serializer.initial_data['username'])
        user.set_password(send_confirmation_code())
    else:
        user = User(username=serializer.initial_data['username'],
                    email=serializer.initial_data['email'])
        user.set_password(send_confirmation_code())
    user.save()
    return Response(serializer.initial_data,
                    status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRoleOnly]
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class YamdbTokenObtainPairView(TokenObtainPairView):
    serializer_class = YamdbTokenObtainPairSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)


class ReviewViewSet(CreateListDestroyViewSet):
    queryset = Review.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination


class CommentViewSet(CreateListDestroyViewSet):
    queryset = Comment.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
