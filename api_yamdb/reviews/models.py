import datetime

from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
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
            MinValueValidator(1988),
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
                fields=['title', 'genre'],
                name='unique_genre_title'
            )
        ]

"""
class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField()
    score = models.SmallIntegerField()
    created = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        unique = ('title')


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )
"""