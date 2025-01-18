from django.db import models
import uuid

from cats.models.cat import Cat
from user.models import User

class CatAdopted(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    adoption_date = models.DateField(blank=False, null=False)
    cat = models.ForeignKey(
        Cat, on_delete=models.CASCADE, blank=False, null=False
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False
    )