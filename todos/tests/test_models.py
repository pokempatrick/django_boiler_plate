from rest_framework.test import APITestCase
from todos.models import Todos
from authentification.models import User


class TestModel(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

    def test_create_todos(self):
        todo = Todos.objects.create(
            title="my first test",
            description="I have to acheive what I've started",
            owner=self.user
        )
        self.assertIsInstance(todo, Todos)
        self.assertEqual(todo.title, 'my first test')
