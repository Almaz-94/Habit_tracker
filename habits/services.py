import os
from datetime import datetime, timedelta

import requests
from celery.schedules import crontab
from django.http import HttpResponse
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit
from users.models import User


bot_token = os.getenv('TELEGRAM_API_KEY')


for habit in Habit.objects.filter(is_pleasant=False):
    if habit.creator.telegram_username or habit.creator.chat_id:
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=habit.period,
            period=IntervalSchedule.SECONDS
        )
        PeriodicTask.objects.create(
            interval=schedule,
            name=f'reminder through telegram bot',
            task=f'habits.tasks.send_reminder',
            expires=datetime.utcnow() + timedelta(seconds=30)
        )



def get_bot_id():
    """ Получение данных чата """
    get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(get_id_url).json()
    return HttpResponse(response)
