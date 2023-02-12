from django.db import models
from helpers.models import TrakingModel
from authentification.models import User
# Create your models here.


class Todos(TrakingModel):

    title = models.CharField(max_length=255)
    description = models.TextField()
    is_completed = models.BooleanField(default=False)
    owner = models.ForeignKey(
        User, related_name='todos', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.title} - {self.owner}'
