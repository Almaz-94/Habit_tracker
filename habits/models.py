from datetime import datetime

from django.conf import settings
from django.db import models
from django.utils import timezone

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """
    Model for Habit entity
    fields:
    creator : one-to-one relation to users.User model
    place: place where habit is performed
    time: at what time of the day to perform habit
    action: habit
    is_pleasant: bool for a pleasant habit. Cannot be combined with a 'reward' field
    reward: reward for habit execution
    duration_time: duration time of habit performance
    is_public: bool either or not habit can be seen by other users
    beginning_date: the day when habit will be practiced
    """
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                verbose_name="создатель",
                                **NULLABLE)
    place = models.CharField(max_length=150, verbose_name='место', **NULLABLE)
    time = models.TimeField(verbose_name='во сколько выполнять привычку')
    action = models.CharField(max_length=200, verbose_name='действие')
    is_pleasant = models.BooleanField(default=False, verbose_name='приятная')
    linked_habit = models.ForeignKey('self',
                                     on_delete=models.CASCADE,
                                     default=None,
                                     verbose_name='связанная привычка',
                                     **NULLABLE)
    period = models.PositiveSmallIntegerField(verbose_name='периодичность в днях', default=1)
    reward = models.CharField(max_length=200, default=None, verbose_name='награда', **NULLABLE)
    duration_time = models.PositiveSmallIntegerField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='публичная')
    beginning_date = models.DateTimeField(default=datetime.now, verbose_name='Дата начала привычки')

    def __str__(self):
        return f'Привычка "{self.action}" от {self.creator}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('id',)
