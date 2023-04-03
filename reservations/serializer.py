from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from reservations.models import Reservations
from reservations.models import Validations


class ValidationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Validations
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    customer = RegisterSerilizer(
        read_only=True, default=None)

    owner = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Reservations
        fields = '__all__'
