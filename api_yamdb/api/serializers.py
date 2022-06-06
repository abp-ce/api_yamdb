from statistics import mean

from django.shortcuts import get_object_or_404
from rest_framework import serializers

from reviews.models import (Category, Comment, Genre, GenreTitle, Review,
                            Title, User)


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Username me is not allowed.")
        return value


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
            and self.context.get('request').user.role == 'user'
            and value != 'user'
        ):
            value = 'user'
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
        reviews = obj.reviews.all()
        if reviews:
            list = []
            for review in reviews:
                value = review.score
                list.append(value)
            return int(mean(list))
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
    author = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date',)


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
        read_only_fields = ('author',)
