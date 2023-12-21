from rest_framework import serializers

from habits.models import Habit
from habits.validators import HabitExclusionValidator, HabitMaxDurationTimeValidator, HabitMaxPeriodValidator, \
    HabitLinkedValidator, HabitPracticeDateValidator


class HabitSerializer(serializers.ModelSerializer):
    """Serializer for Habit model"""
    class Meta:
        model = Habit
        # fields = '__all__'
        exclude = ('creator',)
        validators = [HabitExclusionValidator('is_pleasant', 'linked_habit'),
                      HabitExclusionValidator('is_pleasant', 'reward'),
                      HabitMaxDurationTimeValidator('duration_time'),
                      HabitMaxPeriodValidator('period'),
                      HabitLinkedValidator('linked_habit'),
                      HabitPracticeDateValidator('beginning_date')
                      ]

