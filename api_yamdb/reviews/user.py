from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'
    ROLE_CHOICES = (
        (USER, 'user',),
        (MODERATOR, 'moderator'),
        (ADMIN, 'admin')
    )
    email = models.EmailField('Email', unique=True)
    role = models.CharField(
        'Роль',
        max_length=30,
        choices=ROLE_CHOICES,
        default=USER,
        db_index=True,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )

    class Meta:
        ordering = ('username',)
        constraints = [
            models.UniqueConstraint(
                fields=('username', 'email'),
                name='unique_username_email'
            )
        ]

    def __str__(self):
        return self.username
