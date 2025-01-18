from django.db import models
import uuid


class Shelter(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    street = models.CharField(max_length=100, blank=False, null=False)
    postal_code = models.CharField(max_length=10, blank=False, null=False)
    city = models.CharField(max_length=100, blank=False, null=False)
    country = models.CharField(max_length=100, blank=False, null=False)
    phone_number = models.CharField(max_length=15, blank=False, null=False)
    email = models.EmailField(unique=True, blank=True, null=True)

    def __str__(self):
        return self.name