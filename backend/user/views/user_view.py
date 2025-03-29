from django.db.models import QuerySet
from django.contrib.auth import get_user_model
from rest_framework import viewsets
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.permissions import BasePermission, IsAuthenticated, IsAdminUser
from user.serializers.user_detail_serializer import UserDetailSerializer
from user.serializers.user_list_serializer import UserListSerializer
from user.permissions import IsOwner

User = get_user_model()


class UserReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    lookup_field: str = 'id'

    throttle_classes: list[ScopedRateThrottle] = [ScopedRateThrottle]
    throttle_scope: str = None

    def get_serializer_class(self) -> type[UserListSerializer] | type[UserDetailSerializer]:
        if self.action == 'list':
            return UserListSerializer
        return UserDetailSerializer

    def get_queryset(self) -> QuerySet[User]:
        return User.objects.all()

    def get_permissions(self) -> list[BasePermission]:
        if self.action == 'retrieve':
            return [IsAuthenticated(), IsOwner()]
        return [IsAdminUser()]

    def set_throttle_scope(self) -> str:
        if self.action == 'retrieve':
            return 'user_read'
        return 'user_list'

    def get_throttles(self) -> list[ScopedRateThrottle]:
        self.throttle_scope = self.set_throttle_scope()
        return super().get_throttles()