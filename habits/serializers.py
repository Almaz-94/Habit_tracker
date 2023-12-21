from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitExclusionValidator, HabitMaxDurationTimeValidator, HabitMaxPeriodValidator, \
    HabitLinkedValidator


class HabitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Habit
        fields = '__all__'
        validators = [HabitExclusionValidator('is_pleasant', 'linked_habit'),
                      HabitExclusionValidator('is_pleasant', 'reward'),
                      HabitMaxDurationTimeValidator('duration_time'),
                      HabitMaxPeriodValidator('period'),
                      HabitLinkedValidator('linked_habit')
                      ]

