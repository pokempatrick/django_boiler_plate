from django.test import TestCase, Client
from django.urls import reverse
import json
from django.shortcuts import get_object_or_404
from reservations.models import Reservations
from authentification.models import User
from datetime import datetime
from django.utils import timezone


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.reservation_url = reverse('reservations-list')
        self.validation_reservation_url = reverse(
            'validation_reservation', args=["1"])

        # creation d'un utilisateur
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password', role_name="ROLE_ANONYME")

        # creation d'un autre utilisateur
        self.user2 = User.objects.create_user(
            'cyrus', 'cyrus@gmail.com', '1234152password')

        # creation d'un reservation
        self.reservation = Reservations.objects.create(
            date=datetime.now(tz=timezone.utc),
            statut="CREATE",
            deposit=2000,
            table=5,
            customer=self.user2
        )

        # creation d'un autre reservation
        self.reservation2 = Reservations.objects.create(
            date=datetime.now(tz=timezone.utc),
            statut="CREATE",
            deposit=2000,
            table=5,
            customer=self.user
        )

    def test_create_reservation(self):
        response = self.client.post(
            self.reservation_url,
            json.dumps({
                "statut": "CREATE",
                "date": "2023-12-23",
                "deposit": 2000,
                "table": 3,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['statut'], 'CREATE')

    def test_get_reservation(self):
        response = self.client.get(
            self.reservation_url+f'{self.reservation.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_reservation(self):
        response = self.client.get(
            self.reservation_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data['results'], list)
        self.assertIsInstance(response.data['count'], int)

    def test_search_reservation_by_customer_last_name(self):
        response = self.client.get(
            self.reservation_url+f'?search=cyrus',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )
        self.assertEqual(response.status_code, 200)

    def test_partial_update_reservation(self):
        response = self.client.patch(
            self.reservation_url+f'{self.reservation.id}/',
            json.dumps({
                "table": 10,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_validation_reservation(self):
        """ test de la validation de la reservation """
        response = self.client.post(
            self.validation_reservation_url,
            json.dumps({
                "statut": True,
                "description": "It's ok"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)

    def test_partial_update_reservation_with_bad_input(self):
        response = self.client.patch(
            self.reservation_url+f'{self.reservation.id}/',
            json.dumps({
                "statut": "DELETED",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_reservation_id(self):
        response = self.client.delete(
            self.reservation_url+f'{self.reservation.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 204)

    def test_create_reservation_with_bad_input(self):
        response = self.client.post(
            self.reservation_url,
            json.dumps({
                "title": "my first test",
                "description": "I have to acheive what I've started",
                "is_completed": "bonjour"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)
