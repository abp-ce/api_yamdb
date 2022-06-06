from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilter
from .permissions import (AuthModeratorAdminOrReadOnly, IsAdminOrReadOnly,
                          IsAdminRoleOnly)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          TitleWriteSerializer, UserSerializer,
                          UserSignupSerializer, UserTokenSerializer)
from .viewsets import CreateListDestroyViewSet
from .utils import send_confirmation_code


@api_view(['POST'])
@permission_classes((AllowAny, ))
def request_email(request):
    serializer = UserSignupSerializer(data=request.data)
    if not serializer.is_valid():
        # Если, пользователь существует, всё равно отправляем
        # confirmation_code.
        if (
            'username' in serializer.errors
            and 'email' in serializer.errors
            and serializer.errors['username'][0].code == 'unique'
            and serializer.errors['email'][0].code == 'unique'
            and len(serializer.errors) == 2
        ):
            user = User.objects.get(
                username=serializer.initial_data['username']
            )
            send_confirmation_code(user)
        return Response(serializer.errors,
                        status=status.HTTP_400_BAD_REQUEST)
    user = User(
        username=serializer.validated_data['username'],
        email=serializer.validated_data['email']
    )
    user.save()
    send_confirmation_code(user)
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

    @action(methods=['get', 'patch'], detail=False,
            permission_classes=[IsAuthenticated])
    def me(self, request):
        serializer = self.get_serializer_class()
        if request.method == 'GET':
            data = serializer(request.user).data
            return Response(data, status=status.HTTP_200_OK)
        if request.method == 'PATCH':
            data = serializer(request.user, data=request.data, partial=True,
                              context={'request': request})
            if data.is_valid():
                data.save()
                user_data = UserSignupSerializer(request.user).data
                return Response({**user_data, **data.validated_data},
                                status=status.HTTP_200_OK)
            else:
                return Response(data.initial_data,
                                status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(CreateListDestroyViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class GenreViewSet(CreateListDestroyViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitleWriteSerializer
        return TitleSerializer

    def perform_create(self, serializer):
        category, status = Category.objects.get_or_create(
            slug=self.request.data.get('category')
        )
        if hasattr(self.request.data, 'getlist'):
            genre_slugs = self.request.data.getlist('genre')
        else:
            genre_slugs = self.request.data.get('genre')
        genres_list = []
        for genre_slug in genre_slugs:
            genre, status = Genre.objects.get_or_create(slug=genre_slug)
            genres_list.append(genre)
        serializer.save(category=category, genre=genres_list)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = (AuthModeratorAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (AuthModeratorAdminOrReadOnly,)
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
