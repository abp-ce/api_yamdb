import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from .user import User


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.slug})'


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        unique=True,
        db_index=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} ({self.slug})'


class Title(models.Model):
    name = models.TextField(
        db_index=True,
    )
    year = models.PositiveSmallIntegerField(
        validators=(
            MaxValueValidator(datetime.datetime.now().year),
        ),
        db_index=True,
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        null=True,
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle'
    )
    description = models.TextField(
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ('name',)


class GenreTitle(models.Model):
    genre = models.ForeignKey(
        Genre,
        on_delete=models.CASCADE,
    )
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
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
        related_name='reviews',
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    score = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        db_index=True
    )
    pub_date = models.DateTimeField(
        'Дата добавления',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('author', 'title'),
                name='unique_review_title'
            )
        ]
        ordering = ('pub_date', 'id',)


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
        db_index=True,
    )

    class Meta:
        ordering = ('pub_date', 'id',)
