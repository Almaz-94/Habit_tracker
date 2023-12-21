import os
from datetime import datetime, timedelta

import requests
from celery import shared_task
from django_celery_beat.models import IntervalSchedule, PeriodicTask

from habits.models import Habit
from users.models import User

bot_token = os.getenv('TELEGRAM_API_KEY')


@shared_task
def send_reminder():
    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'

    for habit in Habit.objects.all():
        if not habit.creator.chat_id:
            continue

        message = f'Не забудь выполнить привычку "{habit.action}" в {habit.time}'
        if habit.linked_habit or habit.reward:
            message += f', а в качестве награды: {habit.linked_habit or habit.reward}'

        details = {'chat_id': habit.creator.chat_id, 'text': message}
        requests.get(send_message_url, params=details).json()
    return


# schedule_chat_id, created = IntervalSchedule.objects.get_or_create(
#                 every=12,
#                 period=IntervalSchedule.HOURS
#             )
# PeriodicTask.objects.create(
#     interval=schedule_chat_id,
#     name='Check for new ids in bot',
#     task='habits.tasks.get_chat_id_from_update',
#     expires=datetime.utcnow() + timedelta(seconds=30)
# )


@shared_task
def get_chat_id_from_update():

    get_id_url = f'https://api.telegram.org/bot{bot_token}/getUpdates'
    response = requests.get(get_id_url)

    if response.status_code == 200:
        for update in response.json()['result']:
            tg_username = update['message']['chat']['username']
            chat_id = update['message']['chat']['id']
            try:
                user = User.objects.get(telegram_username=tg_username)
            except User.DoesNotExist:
                continue
            if not user.chat_id:
                user.chat_id = chat_id
                user.save()