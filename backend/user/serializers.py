from rest_framework import serializers
from rest_framework.serializers import CharField, ValidationError
from user.models import User
import re
from typing import Dict, Any, Callable

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_username(self, username: str) -> str:
        if User.objects.filter(username = username).exists():
            raise serializers.ValidationError('Username already exists')
        return username

    def validate_password(self, password: str) -> str:
        demands_password: Dict[str, Callable[[str], bool]] = {
            "is_upper_case": lambda pwd: any(char.isupper() for char in pwd),
            "min_length": lambda pwd: len(pwd) >= 8,
            "contains_special_char": lambda pwd: re.search(r'[^a-zA-Z0-9]', pwd)
        }

        validation_results: Dict[str, bool] = {key: func(password) for key, func in demands_password.items()}

        errors: list[str] = []

        if not validation_results["is_upper_case"]:
            errors.append("Password must have one uppercase letter.")
        if not validation_results["min_length"]:
            errors.append("Password must contain at least 8 characters.")
        if not validation_results["contains_special_char"]:
            errors.append("Password must contain at least one special character.")

        if not errors:
            return password

        raise serializers.ValidationError(" ".join(errors))

    def create(self, validated_data: Dict[str, Any]) -> User:
        return User.objects.create_user(**validated_data)

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            raise ValidationError("Both 'username' and 'password' are required.")

        user = authenticate(username=username, password=password)
        if not user:
            raise ValidationError("Invalid credentials. Please try again.")

        data['user'] = user
        return data

class UserDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)  # Używamy set_password, aby zahaszować hasło
        return super().update(instance, validated_data)