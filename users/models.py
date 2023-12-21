from django.contrib.auth.models import AbstractUser
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class User(AbstractUser):
    """
    User model
    fields:
    username: username
    email: email
    chat_id: user's chat id in telegram
    telegram_username: telegram username
    """
    username = models.CharField(max_length=20, unique=True, verbose_name='Логин')
    email = models.EmailField(unique=True, verbose_name='почта', **NULLABLE)
    chat_id = models.IntegerField(unique=True, verbose_name='ид чата пользователя в ТГ', **NULLABLE)
    telegram_username = models.CharField(max_length=40, unique=True, verbose_name='Ник в телеграме', **NULLABLE)
