from rest_framework import viewsets
from django.contrib.auth import get_user_model

from user.serializers.user_login_serializer import UserLoginSerializer
from user.serializers.user_update_serializer import UserUpdateSerializer


import logging

User = get_user_model()
logger = logging.getLogger(__name__)


class UserRegistrationView(viewsets.GenericViewSet, viewsets.mixins.CreateModelMixin):
    serializer_class = User
    permission_classes = (permissions.AllowAny,)

    def get_queryset(self):
        return User.objects.all()

class UserLoginView(viewsets.GenericViewSet, viewsets.mixins.RetrieveModelMixin):
    pass

class UserUpdateView(viewsets.GenericViewSet, viewsets.mixins.UpdateModelMixin):
    pass
    # serializer_class = UserUpdateSerializer
    # queryset = User.objects.all()
    #
    # def partial_update(self, request, *args, **kwargs):
    #     user = request.user  # The user is automatically set by the JWTAuthentication
    #     if user is None:
    #         raise AuthenticationFailed('Invalid token or user not authenticated.')
    #
    #     user_id = kwargs.get('id')
    #     if str(user.id) != str(user_id):
    #         return Response({'detail': "You cannot update another user's profile."}, status=status.HTTP_403_FORBIDDEN)
    #
    #     # Logowanie oryginalnych danych
    #     logger.debug(f"Received data for update: {request.data}")
    #
    #     # Handle password hashing if password is provided
    #     password = request.data.get('password', None)
    #     if password:
    #         logger.debug(f"Before hashing: {password}")  # Logujemy oryginalne hasło
    #         # Haszowanie hasła przed zapisaniem
    #         request.data['password'] = make_password(password)
    #         logger.debug(f"After hashing: {request.data['password']}")  # Logujemy zahaszowane hasło
    #
    #     # Serializer setup with partial=True for partial update
    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #
    #     if serializer.is_valid():
    #         # Save only the fields that are passed
    #         serializer.save()
    #
    #         # Refresh token for the updated user
    #         refresh = RefreshToken.for_user(user)
    #         return Response({
    #             'token': str(refresh),
    #             'access': str(refresh.access_token),
    #             'user_id': str(user.id)
    #         })
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


