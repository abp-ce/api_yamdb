from django.db.models import Avg
from django.db.utils import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .utils import send_confirmation_code
from reviews.models import Category, Comment, Genre, Review, Title
from reviews.user import User


class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField()
    email = serializers.EmailField()

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Username me is not allowed.")
        return value

    def create(self, validated_data):
        try:
            instance, _ = User.objects.get_or_create(**validated_data)
        except IntegrityError:
            raise serializers.ValidationError("Email is already exists.")
        send_confirmation_code(instance)
        return instance


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

    def validate_role(self, value):
        if (
            'request' in self.context
            and self.context.get('request').user.role == User.USER
            and value != User.USER
        ):
            value = User.USER
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')
        lookup_field = 'slug'


class TitleSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'rating',
                  'description', 'category', 'genre')

    def get_rating(self, obj):
        score = obj.reviews.all().aggregate(Avg('score')).get('score__avg')
        if score:
            return int(score)
        return None


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault(),
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, attrs):
        request = self.context['request']
        if request.method == 'POST':
            view = self.context.get('view')
            title_id = view.kwargs['title_id']
            title = get_object_or_404(Title, pk=title_id)
            review = title.reviews.filter(
                author=self.context['request'].user
            )
            if review.exists():
                raise serializers.ValidationError(
                    'Title-author pair is already exists.'
                )
        return super().validate(attrs)


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
