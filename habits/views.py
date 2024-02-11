import os

import requests
from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsHabitCreator
from habits.serializers import HabitSerializer


bot_token = os.getenv('TELEGRAM_API_KEY')


class HabitViewSet(viewsets.ModelViewSet):

    """ViewSet for Habit model"""

    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    @action(methods=["get"], detail=False, url_path="bot", url_name="bot")
    def get_bot_link(self, *args):
        """Get tg bot link with /habits/bot/"""
        link = f'https://api.telegram.org/bot{bot_token}/getMe'
        name = requests.get(link).json()['result']['username']
        return Response(data={'Telegram bot': f'https://t.me/{name}'}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        """Set current user as a creator of the habit"""
        new_habit = serializer.save()
        new_habit.creator = self.request.user
        new_habit.save()

    def get_queryset(self):
        """Returns current user's habits alongside public ones"""
        user_or_public_habits = Habit.objects.filter(is_public=True)
        return user_or_public_habits

    def get_permissions(self):
        """
        Habits can be created only by authenticated users
        and updated/deleted only by their creators
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated(), ]
        elif self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsHabitCreator(), ]
        else:
            return [AllowAny(), ]
        return permission_classes
