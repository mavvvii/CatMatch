from django.db import models
import uuid

from cats.models.shelter import Shelter


class Cat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, blank=False, null=False)
    age = models.IntegerField(blank=False, null=False)
    breed = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=False, null=False)
    color = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    shelter = models.ForeignKey(
        Shelter, on_delete=models.CASCADE, related_name="cat"
    )

    def __str__(self):
        return self.name