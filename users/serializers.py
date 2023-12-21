from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = self.Meta.model(**validated_data)
        # instance = User(**validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

    # def save(self):
    #     new_user = User(username=self.validated_data['username'])
    #     password = self.validated_data['password']
    #     new_user.set_password(password)
    #     new_user.save()
    #     return new_user

    class Meta:
        model = User
        fields = '__all__'


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        return token
