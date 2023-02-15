from django.test import SimpleTestCase
from django.urls import reverse, resolve

from article.views import ArticleViewSet


class TestUrls(SimpleTestCase):
    def test_article_url_resolves(self):
        url_detail = reverse('articles-detail', args=["15"])
        url_list = reverse('articles-list')

        self.assertEquals(resolve(url_detail).func.cls, ArticleViewSet)
        self.assertEquals(resolve(url_list).func.cls, ArticleViewSet)
