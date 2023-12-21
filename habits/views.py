from itertools import chain

from django.db.models import Q
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsHabitCreator
from habits.serializers import HabitSerializer


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    pagination_class = HabitPaginator

    def perform_create(self, serializer):
        new_habit = serializer.save()
        new_habit.creator = self.request.user
        new_habit.save()

    def get_queryset(self):
        user_or_public_habits = Habit.objects.filter(Q(creator=self.request.user) | Q(is_public=True))
        return user_or_public_habits

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [IsAuthenticated(), ]
        elif self.action in ['update', 'destroy', 'partial_update']:
            permission_classes = [IsHabitCreator(), ]
        else:
            return [AllowAny()]
        return permission_classes

    # def create(self, request, *args, **kwargs):
    #     action = request.data.get('action')
    #     duration_time = request.data.get('duration_time')
    #     time = request.data.get('time')
    #     serializer = self.get_serializer(data={'creator': request.user.pk,
    #                                            'action': action,
    #                                            "duration_time": duration_time,
    #                                            'time':time})
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     return Response({'Привычка создана'}, status=status.HTTP_201_CREATED)
