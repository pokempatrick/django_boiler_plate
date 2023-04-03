from rest_framework.test import APITestCase
from reservations.models import Reservations
from authentification.models import User
from datetime import datetime
from django.utils import timezone


class TestModel(APITestCase):

    def setUp(self):
        self.customer = User.objects.create_user(
            'customer', 'customer@gmail.com', '1234password')

    def test_create_reservation(self):
        reservation = Reservations.objects.create(
            date=datetime.now(tz=timezone.utc),
            statut="created",
            deposit=2000,
            table=5,
            customer=self.customer
        )
        self.assertIsInstance(reservation, Reservations)
        self.assertEqual(reservation.statut, 'created')
