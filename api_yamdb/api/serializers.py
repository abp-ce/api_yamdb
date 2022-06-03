from rest_framework import serializers

from reviews.models import Category, Genre, GenreTitle, Title, User, Review, Comment


class UserSignupSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError("Username me is not allowed.")
        return value


class UserTokenSerializer(serializers.ModelSerializer):
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')


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
