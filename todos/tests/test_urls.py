from django.test import SimpleTestCase
from django.urls import reverse, resolve

from todos.views import TodoAPIView


class TestUrls(SimpleTestCase):
    def test_todo_url_resolves(self):
        url = reverse('todo')
        url1 = reverse('todo', args=["15"])
        self.assertEquals(resolve(url).func.view_class, TodoAPIView)
        self.assertEquals(resolve(url1).func.view_class, TodoAPIView)
