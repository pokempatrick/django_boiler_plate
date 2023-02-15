from django.db import models
from helpers.models import TrakingModel
from authentification.models import User
# Create your models here.


class Articles(TrakingModel):

    name = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    vendor = models.CharField(max_length=255)
    description = models.TextField()
    added_by = models.ForeignKey(
        User, related_name='articles', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.code} - {self.added_by}'
