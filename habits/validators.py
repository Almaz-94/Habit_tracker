from rest_framework.exceptions import ValidationError

from habits.models import Habit


class HabitExclusionValidator:
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        if dict(value).get(self.field1) and dict(value).get(self.field2):
            raise ValidationError(f'Поля {self.field1} и {self.field2} взаимоисключающие')


class HabitMaxDurationTimeValidator:
    def __init__(self, duration_time):
        self.duration_time = duration_time

    def __call__(self, value):
        if not dict(value).get(self.duration_time):
            return
        if dict(value).get(self.duration_time) > 120:
            raise ValidationError('Время на выполнение привычки должно быть не больше 120 секунд')


class HabitMaxPeriodValidator:
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        if not dict(value).get(self.period):
            return
        if dict(value).get(self.period) > 7:
            raise ValidationError('Периодичность привычки не должна превышать 7 дней')


class HabitLinkedValidator:
    def __init__(self, linked_habit):
        self.linked_habit = linked_habit

    def __call__(self, value):
        l_habit = dict(value).get(self.linked_habit)
        if not l_habit:
            return
        if not l_habit.is_pleasant:
            raise ValidationError('Связанной может быть только приятная привычка')