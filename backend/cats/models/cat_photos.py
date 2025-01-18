from django.db import models
import uuid

from cats.models.cat import Cat

class CatPhotos(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    photo = models.ImageField(upload_to="cats_photos/", null=True, blank=True)
    cat = models.ForeignKey(Cat, on_delete=models.CASCADE)

    def __str__(self):
        return self.name