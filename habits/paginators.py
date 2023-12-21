from rest_framework.pagination import PageNumberPagination


class HabitPaginator(PageNumberPagination):
    """Paginator class for Habit viewset"""
    page_size = 5
