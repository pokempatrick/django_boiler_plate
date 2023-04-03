from django.db import models
from helpers.models import TrakingModel
from authentification.models import User
from django.core.validators import MinValueValidator
from .constant import STATUT

# Create your models here.


class Reservations(TrakingModel):

    statut = models.CharField(
        max_length=150, choices=STATUT, default="CREATED",
        blank=False,
        error_messages="The value is not supported")
    table = models.IntegerField(MinValueValidator(
        0, message="The value should be greater than 0"))
    deposit = models.IntegerField(MinValueValidator(
        0, message="The value should be greater than 0"))
    date = models.DateTimeField()
    customer = models.ForeignKey(
        User, related_name='customer', on_delete=models.CASCADE, blank=True, null=True)
    owner = models.ForeignKey(
        User, related_name='owner', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self) -> str:
        return f'{self.table} - {self.customer} - {self.statut}'


class Validations(TrakingModel):
    statut = models.BooleanField(default=True, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    reservation = models.ForeignKey(
        Reservations, related_name='validations', on_delete=models.CASCADE, blank=True, null=True)
    user = models.ForeignKey(
        User, related_name='validator', on_delete=models.CASCADE, blank=True, null=True)
