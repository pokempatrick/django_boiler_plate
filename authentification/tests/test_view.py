from django.test import TestCase, Client
from django.urls import reverse
import json
import jwt
from rest_framework import status
from authentification.models import User
from datetime import datetime, timedelta
from django.conf import settings


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.user_url = reverse('user')
        self.email_sign_url = reverse('email_sign')
        self.email_code_url = reverse('email_code')
        self.user_url = reverse('user')

        # creation d'un utilisateur
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

        # generate recover token
        self.recover_token = jwt.encode(
            {
                'username': self.user.username,
                'email': self.user.email,
                'user_id': self.user.id,
                'code': 1253,
                'exp': datetime.utcnow()+timedelta(hours=1)
            }, settings.SECRET_KEY2, algorithm='HS256')

    def test_registration(self):
        response = self.client.post(
            self.register_url,
            json.dumps({
                "username": "johndoes",
                "email": "jonhdoes@yahoo.fr",
                "password": "casho 15",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_good_credential(self):
        response = self.client.post(
            self.login_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
                "password": "1234password",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_login_bad_credential(self):
        response = self.client.post(
            self.login_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
                "password": "123password",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_password(self):
        pass

    def test_update_role(self):
        pass

    def test_sign_in_email_with_existing_email(self):
        response = self.client.post(
            self.email_sign_url,
            json.dumps({
                "email": "cyretruly@gmail.com",
            }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_sign_in_email_with_non_existing_email(self):
        response = self.client.post(
            self.email_sign_url,
            json.dumps({
                "email": "cyretruely@gmail.com",
            }),
            content_type="application/json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_code_email_with_bad_code(self):

        response = self.client.post(
            self.email_code_url,
            json.dumps({"code": 1243, }),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user(self):
        response = self.client.get(
            self.user_url,
            ** {'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
