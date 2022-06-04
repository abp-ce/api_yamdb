from functools import partial
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

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


# class UserTokenSerializer(serializers.ModelSerializer):
#     confirmation_code = serializers.CharField()

#     class Meta:
#         model = User
#         fields = ('username', 'confirmation_code')


class UserTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()

    # class Meta:
    #     model = User
    #     fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'category', 'genre')

    def create(self, validated_data):
        category_data = validated_data.pop('category')
        genres_data = validated_data.pop('genre')
        category = Category.get_or_create(**category_data)
        title = Title.objects.create(**validated_data, category=category)
        for genre_data in genres_data:
            current_genre, status = Genre.objects.get_or_create(**genre_data)
            GenreTitle.objects.create(
                genre=current_genre, title=title
            )
        return title


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date')
