from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from reviews.models import User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')


class YamdbTokenObtainPairSerializer(TokenObtainPairSerializer):
    confirmation_code = serializers.CharField(max_length=8)

    def to_internal_value(self, data):
        resource_data = data
        resource_data['password'] = data['confirmation_code']
        return super().to_internal_value(resource_data)

    class Meta:
        fields = ('username', 'confirmation_code')
