import os
import requests
from datetime import datetime, timedelta

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from rest_framework_simplejwt.tokens import AccessToken

from habits.models import Habit
from users.models import User
from habits.services import create_message


class HabitTestCase(APITestCase):
    def setUp(self):
        """ Creates and authenticates test user """
        user_data = {
            'username': 'Test',
            'password': '123456'
        }
        self.user = User.objects.create(**user_data)
        self.user.set_password(user_data.get('password'))
        self.user.save()

        self.client = APIClient()
        access_token = AccessToken.for_user(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_habit_creation(self):
        """ Tests habit creation """
        response = self.client.post(
            '/habits/',
            data={
                'time': '14:00',
                'action': 'test code',
                'period': 1,
                'duration_time': 100,
            }
        )
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        self.assertEqual(response.json().get('beginning_date')[:10],
                         str(datetime.today().date()))
        response.json().pop('beginning_date')

        self.assertEqual(response.json(),
                         {
                             'id': 1,
                             'place': None,
                             'time': '14:00:00',
                             'action': 'test code',
                             'is_pleasant': False,
                             'period': 1,
                             'reward': None,
                             'duration_time': 100,
                             'is_public': False,
                             'linked_habit': None
                         }
                         )

        self.assertTrue(Habit.objects.all().exists())

    def test_habit_list(self):
        """ Tests get habit list request"""
        habit1 = Habit.objects.create(time='00:00', action='tst', period=1, duration_time=50,
                                      creator=self.user, beginning_date='3000-01-01')
        response = self.client.get('/habits/')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        self.assertEqual(response.json(),
                         {
                             "count": 1,
                             "next": None,
                             "previous": None,
                             "results":
                                 [
                                     {
                                         "id": habit1.id,
                                         "place": None,
                                         "time": "00:00:00",
                                         "action": habit1.action,
                                         "is_pleasant": False,
                                         "period": habit1.period,
                                         "reward": None,
                                         "duration_time": habit1.duration_time,
                                         "is_public": False,
                                         "beginning_date": '3000-01-01T00:00:00Z',
                                         "linked_habit": None
                                     }
                                 ]
                         }
                         )

    def test_habit_validators(self):
        habit = Habit.objects.create(time='00:00', action='tst', period=1, duration_time=50, is_pleasant=False)
        response = self.client.post(
            '/habits/',
            data={
                'time': '14:00',
                'action': 'test code',
                'period': 8,
                'duration_time': 130,
                'is_pleasant': True,
                'linked_habit': habit.pk,
                'reward': 'pospat',
            }
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {
                             "non_field_errors": [
                                 "Поля is_pleasant и linked_habit взаимоисключающие",
                                 "Поля is_pleasant и reward взаимоисключающие",
                                 "Время на выполнение привычки должно быть положительным числом не превышающим 120",
                                 "Периодичность привычки не должна превышать 7 дней",
                                 "Связанной может быть только приятная привычка"
                             ]
                         }
                         )

    def test_habit_period_validators(self):
        response = self.client.post(
            '/habits/',
            data={
                'time': '14:00',
                'action': 'test code2',
                'period': 0,
                'is_pleasant': False,
                'reward': 'pospat',
            }
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": ['Периодичность привычки не может быть меньше 1']})

    def test_habit_beginning_date(self):
        response = self.client.post(
            '/habits/',
            data={
                'time': '14:00',
                'action': 'test code2',
                'period': 1,
                'is_pleasant': False,
                'reward': 'pospat',
                'beginning_date': datetime.today().date() - timedelta(days=1)
            }
        )
        self.assertEqual(response.status_code,
                         status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(),
                         {"non_field_errors": [f'Дата начала привычки не может быть раньше {datetime.now().date()}']})


class TgBotTestCase(APITestCase):
    def setUp(self) -> None:
        self.bot_token = os.getenv('TELEGRAM_API_KEY')

    def test_getting_bot_link(self):
        response = self.client.get('/habits/bot/')
        self.assertEqual(response.status_code,
                         status.HTTP_200_OK)
        link = f'https://api.telegram.org/bot{self.bot_token}/getMe'
        name = requests.get(link).json()['result']['username']

        self.assertEqual(response.json(),
                         {"Telegram bot": f"https://t.me/{name}"}
                         )


class ServicesTestCase(APITestCase):
    def setUp(self) -> None:
        """Creates test user and test habits"""
        user_data = {
            'username': 'Test',
            'password': '123456'
        }
        self.user = User.objects.create(**user_data)
        self.user.save()

        self.habit_1 = Habit.objects.create(time='01:11', action='test1', period=1, duration_time=50, creator=self.user,
                                            beginning_date='3000-01-01')
        self.habit_2 = Habit.objects.create(time='03:33', action='test3', period=7, duration_time=10, creator=self.user,
                                            beginning_date='3000-01-01', is_pleasant=True)
        self.habit_3 = Habit.objects.create(time='02:22', action='test2', period=7, duration_time=10, creator=self.user,
                                            beginning_date='3000-01-01', linked_habit=self.habit_2)

    def test_create_message(self):
        """Tests message creation for tg reminder"""
        message_1 = create_message(self.habit_1)

        self.assertEqual(message_1,
                         f'Не забудь выполнить привычку "{self.habit_1.action}" в {self.habit_1.time}'
                         )

        message_3 = create_message(self.habit_3)
        self.assertEqual(message_3,
                         f'Не забудь выполнить привычку "{self.habit_3.action}" в {self.habit_3.time}'
                         f', а в качестве награды: {self.habit_3.linked_habit.action or self.habit_3.reward}'
                         )
