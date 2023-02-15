from rest_framework.test import APITestCase
from article.models import Articles
from authentification.models import User


class TestModel(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            'cyrce', 'cyretruly@gmail.com', '1234password')

    def test_create_article(self):
        article = Articles.objects.create(
            name="bill_management",
            description="I have to acheive what I've started",
            vendor="PLdev",
            added_by=self.user
        )
        self.assertIsInstance(article, Articles)
        self.assertEqual(article.name, 'bill_management')
