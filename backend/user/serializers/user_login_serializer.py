from rest_framework import serializers
from user.models import User


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