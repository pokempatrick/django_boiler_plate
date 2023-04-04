from rest_framework import serializers
from authentification.serializer import RegisterSerilizer
from reservations.models import Reservations
from reservations.models import Validations


class ValidationPureSerializer(serializers.ModelSerializer):
    user = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Validations
        fields = '__all__'


class ReservationPureSerializer(serializers.ModelSerializer):
    customer = RegisterSerilizer(
        read_only=True, default=None)

    owner = RegisterSerilizer(
        read_only=True, default=None)

    class Meta:
        model = Reservations
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    customer = RegisterSerilizer(
        read_only=True, default=None)

    owner = RegisterSerilizer(
        read_only=True, default=None)

    validations = ValidationPureSerializer(
        read_only=True, default=None, many=True)

    class Meta:
        model = Reservations
        fields = '__all__'


class ValidationSerializer(serializers.ModelSerializer):
    user = RegisterSerilizer(
        read_only=True, default=None)

    reservation = ReservationPureSerializer(
        read_only=True, default=None)

    class Meta:
        model = Validations
        fields = '__all__'
