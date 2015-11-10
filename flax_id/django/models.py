from django.db import models

from .fields import FlaxId


class FlaxModel(models.Model):
    id = FlaxId(primary_key=True)

    class Meta:
        abstract = True
        ordering = ('id',)
