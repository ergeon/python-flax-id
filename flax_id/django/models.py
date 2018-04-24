from django.db import models

from .fields import FlaxId


class FlaxModel(models.Model):
    id = FlaxId()

    class Meta:
        abstract = True
