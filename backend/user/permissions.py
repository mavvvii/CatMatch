from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import View
from django.contrib.auth import get_user_model

User = get_user_model()


class IsOwner(BasePermission):
    def has_object_permission(self, request: Request, view: View, obj: User) -> bool:
        return request.user == obj.owner