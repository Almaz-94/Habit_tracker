from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, \
    UserListAPIView, \
    UserRetrieveAPIView, \
    MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='users_register'),
    path('list/', UserListAPIView.as_view(), name='users_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='users_profile'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]
