import os
from datetime import timedelta

import requests
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response

bot_token = os.getenv('TELEGRAM_API_KEY')


def create_message(habit):
    """Creates reminder message for habit creator"""
    next_day = habit.beginning_date + timedelta(days=habit.period)
    message = f'Не забудь выполнить привычку "{habit.action}" в {habit.time}, след раз {next_day}'
    if habit.linked_habit or habit.reward:
        message += f', а в качестве награды: {habit.linked_habit.action or habit.reward}'
    return message


def get_bot_link(*args):
    """Returns link to tg bot"""
    get_id_url = f'https://api.telegram.org/bot{bot_token}/getMe'
    name = requests.get(get_id_url).json()['result']['username']
    return Response(data={'Telegram bot': f'https://t.me/{name}'}, status=status.HTTP_200_OK)


