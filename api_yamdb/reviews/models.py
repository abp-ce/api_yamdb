import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
from django.db import models


class User(AbstractUser):
    USER = 'us'
    MODERATOR = 'mo'
    ADMIN = 'ad'
    ROLE_CHOICES = (
        (USER, 'user',),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            )
        ]


class Category(models.Model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )


class Title(models.Model):
    name = models.TextField()
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(datetime.datetime.now().year),
        )
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    description = models.TextField(
        blank=True,
        null=True,
    )


class GenreTitle(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genre',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
        related_name='title',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('title', 'genre'),
                name='unique_genre_title'
            )
        ]


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='review',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    score = models.SmallIntegerField()
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review_title'
            )
        ]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
    )
