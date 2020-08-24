from django.contrib.auth.models import User, Group
from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import Profile


# 시리얼라이저는 응답으로 보낼 데이터의 형태를 정해주는 하나의 틀과 같음.


# 회원가입
class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", "password")
        extra_kwargs = {"password" : {"write_only" : True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data["username"], None, validated_data["password"]
        )

        return user

# 접속 유저중인지 확인
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username")

# 로그인
class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Unable to log in with provided credentials.")

# Profile
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ("email", "nickname", "point", "like", "phone",)
        