from datetime import datetime

from rest_framework.exceptions import ValidationError


class HabitExclusionValidator:
    """Validates that field1 and field2 cant be picked simultaneously"""
    def __init__(self, field1, field2):
        self.field1 = field1
        self.field2 = field2

    def __call__(self, value):
        if dict(value).get(self.field1) and dict(value).get(self.field2):
            raise ValidationError(f'Поля {self.field1} и {self.field2} взаимоисключающие')


class HabitMaxDurationTimeValidator:
    """Validates that habit execution time cannot exceed 120 seconds"""
    def __init__(self, duration_time):
        self.duration_time = duration_time

    def __call__(self, value):
        dur_time = dict(value).get(self.duration_time)
        if not dur_time:
            return
        if dur_time > 120 or dur_time <= 0:
            raise ValidationError('Время на выполнение привычки должно быть положительным числом не превышающим 120')


class HabitMaxPeriodValidator:
    """Validates that habit is scheduled at least weekly"""
    def __init__(self, period):
        self.period = period

    def __call__(self, value):
        if not dict(value).get(self.period):
            return
        if dict(value).get(self.period) > 7:
            raise ValidationError('Периодичность привычки не должна превышать 7 дней')


class HabitLinkedValidator:
    """Validates that only pleasant habit can be a linked habit"""
    def __init__(self, linked_habit):
        self.linked_habit = linked_habit

    def __call__(self, value):
        l_habit = dict(value).get(self.linked_habit)
        if not l_habit:
            return
        if not l_habit.is_pleasant:
            raise ValidationError('Связанной может быть только приятная привычка')


class HabitPracticeDateValidator:
    """Validates that habit's next practice day is not in the past"""
    def __init__(self, beginning_date):
        self.beginning_date = beginning_date

    def __call__(self, value):
        beg_date = dict(value).get(self.beginning_date)
        if not beg_date:
            return
        if beg_date.date() < datetime.now().date():
            raise ValidationError(f'Дата начала привычки не может быть раньше {datetime.now().date()}')