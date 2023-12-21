import os
from datetime import datetime, timedelta
import requests
from celery import shared_task
from habits.models import Habit
from habits.services import create_message
from users.models import User

bot_token = os.getenv('TELEGRAM_API_KEY')


@shared_task
def send_reminder():

    """Sends reminders periodically through Telegram bot if chat_id is available"""

    send_message_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    for habit in Habit.objects.filter(is_pleasant=False):
        is_habit_practice_day = bool(habit.beginning_date == datetime.now().date())

        if not habit.creator.chat_id or not is_habit_practice_day:
            continue

        message = create_message(habit)

        if (datetime.now() + timedelta(minutes=30)).strftime("%H:%M") == habit.time.strftime("%H:%M"):
            details = {'chat_id': habit.creator.chat_id, 'text': message}
            requests.get(send_message_url, params=details).json()
        habit.beginning_date += timedelta(days=habit.period)
        habit.save()



@shared_task
def get_chat_id_from_update():

    """Checks Tg bot users for habit creators and updates User.chat_id field"""

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
