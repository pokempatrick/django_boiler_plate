from django.test import TestCase, Client
from django.urls import reverse
import json
from django.shortcuts import get_object_or_404
from todos.models import Todos
from authentification.models import User


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.todo_url = reverse('todo')

        # creation d'un utilisateur
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

        # creation d'un todo
        self.todo = Todos.objects.create(
            title="my first test",
            description="I have to acheive what I've started",
            owner=self.user
        )

    def test_create_todo(self):

        response = self.client.post(
            self.todo_url,
            json.dumps({
                "title": "my first test",
                "description": "I have to acheive what I've started",
                "owner": 1,
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 201)

    def test_get_todo(self):
        response = self.client.get(
            self.todo_url+f'{self.todo.id}',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )

        self.assertEqual(response.status_code, 200)

    def test_get_all_todo(self):
        response = self.client.get(
            self.todo_url,
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
        )

        self.assertEqual(response.status_code, 200)

    def test_get_update_todo(self):
        response = self.client.put(
            self.todo_url+f'{self.todo.id}',
            json.dumps({
                "title": "my first test 2",
                "description": "I have to acheive what I've started",
            }),
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 200)

    def test_get_delete_todo_id_1(self):
        response = self.client.delete(
            self.todo_url+f'{self.todo.id}',
            **{'HTTP_AUTHORIZATION': f'Bearer {self.user.token}'},
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)
