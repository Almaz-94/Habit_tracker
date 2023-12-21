from django.urls import path
from rest_framework.routers import DefaultRouter

from habits.apps import HabitsConfig
from habits.services import get_bot_link
from habits.views import HabitViewSet

app_name = HabitsConfig.name


router = DefaultRouter()
router.register(r'habits', HabitViewSet, basename='habits')
urlpatterns = [

] + router.urls
