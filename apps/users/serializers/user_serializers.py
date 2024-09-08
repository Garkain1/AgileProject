from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from ..models import User


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'position',
            'email',
            'phone',
            'last_login',
        )


class RegisterUserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(
        max_length=128,
        write_only=True,
    )

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'position',
            'password',
            're_password',
        )
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate(self, data):
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        if not username.isalnum() and '_' not in username:
            raise serializers.ValidationError(
                "Username must contain only letters, numbers, or _"
            )

        if not first_name.isalpha():
            raise serializers.ValidationError("First name must contain only letters")

        if not last_name.isalpha():
            raise serializers.ValidationError("Last name must contain only letters")

        password = data.get("password")
        re_password = data.get("re_password")

        if password != re_password:
            raise serializers.ValidationError({"password": "Passwords do not match"})

        validate_password(password)

        return data

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('re_password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
