from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Genre, GenreTitle, Title, User, Review, Comment


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'bio', 'role')


class YamdbTokenObtainPairSerializer(TokenObtainPairSerializer):
    confirmation_code = serializers.CharField(max_length=8)

    def to_internal_value(self, data):
        resource_data = data
        resource_data['password'] = data['confirmation_code']
        return super().to_internal_value(resource_data)

    class Meta:
        fields = ('username', 'confirmation_code')


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class ReviewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = ('text', 'author', 'score', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = ('text', 'author', 'pub_date')
