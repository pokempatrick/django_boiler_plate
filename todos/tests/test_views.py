from django.test import TestCase, Client
from django.urls import reverse
from todos.models import Todos
from authentification.models import User
import json
from django.shortcuts import get_object_or_404


class TestViews(TestCase):
    @classmethod
    def setUp(self):

        self.client = Client()
        self.login_url = reverse('login')
        self.register_url = reverse('register')
        self.todo_url = reverse('todo')
        self.todo_url_id1 = reverse('todo', args=[1])

        # self.client.post(self.register_url, json.dumps({
        #     "email": "johndoes@gmail.com",
        #     "password": "123456",
        #     "username": 'john'
        # }))

        # self.token = self.client.get(self.login_url, json.dumps({
        #     "email": "johndoes@gmail.com",
        #     "password": "123456"
        # }))["token"]

        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

    def test_create_todo(self):
        response = self.client.post(
            self.todo_url,
            json.dumps({
                "title": "my first test",
                "description": "I have to acheive what I've started",
                "owner": 1,
            }),
            # Authorization=f'Bearer {self.user.token}',
            content_type="application/json"
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)

    # def test_get_todo(self):
    #     response = self.client.get(
    #         self.todo_url_id1,
    #         # Authorization=f'Bearer {self.user.token}',
    #         # content_type="application/json"
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_all_todo(self):
    #     response = self.client.get(
    #         self.todo_url,
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_update_todo_id_1(self):
    #     response = self.client.put(
    #         self.todo_url_id1,
    #         json.dumps({
    #             "title": "my first test 2",
    #             "description": "I have to acheive what I've started",
    #             "owner": 1,
    #         }),
    #         # Authorization=f'Bearer {self.user.token}',
    #         content_type="application/json"
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)

    # def test_get_delete_todo_id_1(self):
    #     response = self.client.delete(
    #         self.todo_url_id1,
    #         # Authorization=f'Bearer {self.user.token}',
    #         content_type="application/json"
    #     )
    #     print(response.data)
    #     self.assertEqual(response.status_code, 200)
