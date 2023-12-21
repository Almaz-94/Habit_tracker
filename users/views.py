from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsOwner
from users.serializers import UserSerializer, MyTokenObtainPairSerializer


class UserCreateAPIView(CreateAPIView):
    """View for creating instance of User model"""
    serializer_class = UserSerializer


class UserUpdateAPIView(UpdateAPIView):
    """View for updating instance of User model"""
    serializer_class = UserSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]


class UserRetrieveAPIView(RetrieveAPIView):
    """View for retrieving instance of User model"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class UserListAPIView(ListAPIView):
    """View for retrieving all instances of User model"""
    serializer_class = UserSerializer
    queryset = User.objects.all()


class MyTokenObtainPairView(TokenObtainPairView):
    """View for obtaining authorization token"""
    serializer_class = MyTokenObtainPairSerializer
