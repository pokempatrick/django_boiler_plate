from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('articles', views.ArticleViewSet, basename='articles')
urlpatterns = [
    # ...
]
urlpatterns += router.urls
