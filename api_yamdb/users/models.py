from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    USER = 'us'
    MODERATOR = 'mo'
    ADMIN ='ad'
    ROLE_CHOICES = (
        ('us', 'user',),
        ('mo', 'moderator'),
        ('ad', 'admin')
    )
    role = models.CharField(
        max_length=2,
        choices=ROLE_CHOICES,
        default=USER,
    )
    bio = models.TextField(
        'Биография',
        blank=True,
    )
