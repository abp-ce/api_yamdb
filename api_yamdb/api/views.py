from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from reviews.models import (Category, Genre, GenreTitle, Title, User,
                            Review, Comment)

from .permissions import IsAdminOrReadOnly, IsAdminRoleOnly
from .serializers import (CategorySerializer, UserSerializer,
                          UserSignupSerializer, UserTokenSerializer)
from .viewsets import CreateListDestroyViewSet, MeViewSet


def send_confirmation_code(user):
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Confirmation code',
        message=confirmation_code,
        from_email='fake@yamdb.fake',
        recipient_list=[user.email]
    )
    return confirmation_code


@api_view(['POST'])
@permission_classes((AllowAny, ))
def request_email(request):
    serializer = UserSignupSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    user = User(username=serializer.validated_data['username'],
                email=serializer.validated_data['email'])
    send_confirmation_code(user)
    user.save()
    return Response(serializer.validated_data,
                    status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def get_token(request):
    serializer = UserTokenSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    user = get_object_or_404(
        User, username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)},
            status=status.HTTP_200_OK
        )
    return Response(
        serializer.validated_data,
        status=status.HTTP_400_BAD_REQUEST
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminRoleOnly]
    lookup_field = 'username'
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)


class UserMeViewSet(MeViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return User.objects.all()

    @action(methods=['get', 'patch'], detail=False)
    def me(self, request):
        serializer = self.get_serializer_class()
        data = serializer(request.user).data
        return Response(data, status=status.HTTP_200_OK)


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
