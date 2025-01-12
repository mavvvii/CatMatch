from django.contrib.auth.models import AbstractUser
from django.db import models

import uuid

class User(AbstractUser):
    # User is a subclass of AbstractUser so it give filed of username, first_name, last_name, email, password, is_staff,
    # is_superuser, is_active,
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # Test case method
    def get_name(self):
        return f'{self.username}'