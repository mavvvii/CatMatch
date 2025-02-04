from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import viewsets, status
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAdminUser
from rest_framework.decorators import action


from user.serializers import UserSerializer, UserLoginSerializer, UserDetailSerializer, UserUpdateSerializer
from rest_framework.response import Response
from user.models import User
from django.contrib.auth import get_user_model

import logging

from typing import List, Type
logger = logging.getLogger(__name__)

User = get_user_model()


class UserViewSet(viewsets.GenericViewSet, viewsets.mixins.ListModelMixin):
    permission_classes = [AllowAny]
    lookup_field: str = 'id'
    lookup_url_kwarg: str = 'id'

    def get_serializer_class(self) -> [UserSerializer | UserLoginSerializer]:
        if self.action == 'list':
            return UserSerializer
        return UserDetailSerializer

    def get_queryset(self):
        return User.objects.all()

    def list(self, request):
        queryset: QuerySet[User] = self.get_queryset()
        serializer: UserDetailSerializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        user_id: UUID = kwargs.get(self.lookup_url_kwarg)
        queryset: QuerySet[User] = self.get_queryset()

        try:
            user: User = queryset.get(id = user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer: UserDetailSerializer = self.get_serializer(user)

        return Response(serializer.data)


class UserRegistrationView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def get_queryset(self):
        return User.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  # Zapisujemy użytkownika

            # Dodajemy użytkownika do grupy "user"
            user_group, _ = Group.objects.get_or_create(name="user")
            user.groups.add(user_group)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    permission_classes = [AllowAny]
    serializer_class = UserLoginSerializer

    def create(self, request):
        from django.contrib.auth import authenticate


        username = request.data.get('username')
        password = request.data.get('password')

        user_auth = authenticate(username=username, password=password)

        if user_auth is not None:
            refresh = RefreshToken.for_user(user_auth)
            return Response({
                'token': str(refresh),
                'access': str(refresh.access_token),
                'user_id': str(user_auth.id)
            })
        return Response({'detail': "Invalid credentailas"}, status=status.HTTP_401_UNAUTHORIZED)

class UserUpdateView(viewsets.GenericViewSet, viewsets.mixins.UpdateModelMixin):
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()

    def partial_update(self, request, *args, **kwargs):
        user = request.user  # The user is automatically set by the JWTAuthentication
        if user is None:
            raise AuthenticationFailed('Invalid token or user not authenticated.')

        user_id = kwargs.get('id')
        if str(user.id) != str(user_id):
            return Response({'detail': "You cannot update another user's profile."}, status=status.HTTP_403_FORBIDDEN)

        # Logowanie oryginalnych danych
        logger.debug(f"Received data for update: {request.data}")

        # Handle password hashing if password is provided
        password = request.data.get('password', None)
        if password:
            logger.debug(f"Before hashing: {password}")  # Logujemy oryginalne hasło
            # Haszowanie hasła przed zapisaniem
            request.data['password'] = make_password(password)
            logger.debug(f"After hashing: {request.data['password']}")  # Logujemy zahaszowane hasło

        # Serializer setup with partial=True for partial update
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            # Save only the fields that are passed
            serializer.save()

            # Refresh token for the updated user
            refresh = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh),
                'access': str(refresh.access_token),
                'user_id': str(user.id)
            })

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddToShelterStaffView(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = None  # Nie potrzebujemy serializera
    permission_classes = [IsAdminUser]  # Możesz zmienić na IsAuthenticated jeśli ma być dostęp dla zalogowanych

    def get_serializer_class(self):
        return None  # DRF nie będzie wymagał serializera

    def partial_update(self, request, id=None):
        """
        PATCH endpoint do dodawania użytkownika do grupy 'shelterstaff' na podstawie ID.
        """
        try:
            user = self.get_queryset().get(id=id)  # Pobranie użytkownika na podstawie ID
            group, _ = Group.objects.get_or_create(name="shelterstaff")  # Pobranie lub utworzenie grupy

            if group in user.groups.all():
                return Response({"message": f"User {user.username} is already in shelterstaff group."},
                                status=status.HTTP_200_OK)

            user.groups.add(group)  # Dodanie użytkownika do grupy
            return Response({"message": f"User {user.username} added to shelterstaff group."},
                            status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)