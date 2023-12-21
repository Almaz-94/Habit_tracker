from django.conf import settings
from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
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
    period = models.PositiveSmallIntegerField(verbose_name='периодичность в днях', **NULLABLE)
    reward = models.CharField(max_length=200, default=None, verbose_name='награда', **NULLABLE)
    duration_time = models.PositiveSmallIntegerField(verbose_name='время на выполнение', **NULLABLE)
    is_public = models.BooleanField(default=False, verbose_name='публичная')
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'id {self.id} pleasant: {self.is_pleasant}  Привычка "{self.action}" от {self.creator}'

    class Meta:
        verbose_name = 'Привычка'
        verbose_name_plural = 'Привычки'
        ordering = ('id',)
