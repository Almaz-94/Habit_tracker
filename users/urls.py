from django.urls import path

from users.apps import UsersConfig
from users.views import UserCreateAPIView, \
    UserListAPIView, \
    UserUpdateAPIView, \
    UserRetrieveAPIView, \
    MyTokenObtainPairView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='users'),
    path('list/', UserListAPIView.as_view(), name='users_list'),
    path('<int:pk>/', UserRetrieveAPIView.as_view(), name='users_profile'),
    # path('profile_update/', UserUpdateAPIView.as_view(), name='users_update'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
]