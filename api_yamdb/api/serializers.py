from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import Category, Genre, GenreTitle, Title, User


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.StringRelatedField(source='user', read_only=True)

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
