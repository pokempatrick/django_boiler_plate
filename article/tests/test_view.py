from django.test import TestCase, Client
from django.urls import reverse
import json
from django.shortcuts import get_object_or_404
from article.models import Articles
from authentification.models import User


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.article_url = reverse('articles-list')

        # creation d'un utilisateur
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

        # creation d'un autre utilisateur
        self.user2 = User.objects.create_user(
            'cyrus', 'cyrus@gmail.com', '1234152password')

        # creation d'un article
        self.article = Articles.objects.create(
            added_by=self.user,
            name="Calculatrice",
            code="1515",
            vendor="casho 15",
            description="Calculatrice scientifique"
        )

        # creation d'un autre article
        self.article2 = Articles.objects.create(
            added_by=self.user,
            name="Calculatrice 2",
            code="1515",
            vendor="propos",
            description="Calculatrice scientifique"
        )

    def test_create_article(self):
        response = self.client.post(
            self.article_url,
            json.dumps({
                "name": "Calculatrice",
                "code": "1515",
                "vendor": "casho 15",
                "description": "Calculatrice scientifique"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_get_article(self):
        response = self.client.get(
            self.article_url+f'{self.article.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )
        self.assertEqual(response.status_code, 200)

    def test_get_all_article(self):
        response = self.client.get(
            self.article_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )

        self.assertEqual(response.status_code, 200)

    def test_update_article(self):
        response = self.client.put(
            self.article_url+f'{self.article.id}/',
            json.dumps({
                "name": "Calculatrice 15",
                "code": "1515",
                "vendor": "casho 15",
                "description": "Calculatrice scientifique",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_delete_article_id(self):
        response = self.client.delete(
            self.article_url+f'{self.article.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)

    def test_update_article_with_bad_input(self):
        response = self.client.put(
            self.article_url+f'{self.article.id}/',
            json.dumps({
                "title": "my first test 2",
                "description": "I have to acheive what I've started",
                "is_completed": "bonjour"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_create_article_with_bad_input(self):
        response = self.client.post(
            self.article_url,
            json.dumps({
                "title": "my first test",
                "description": "I have to acheive what I've started",
                "is_completed": "bonjour"
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 400)

    def test_delete_somebody_else_article(self):
        response = self.client.delete(
            self.article_url+f'{self.article.id}/',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user2.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 403)
