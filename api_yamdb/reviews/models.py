
from django.db import models


class Titles(models.Model):
    pass


class Review(models.Model):
    title = models.ForeignKey(
        Titles, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField()
    score = models.SmallIntegerField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created = models.DateTimeField(
        'Дата добавления', auto_now_add=True, db_index=True)
