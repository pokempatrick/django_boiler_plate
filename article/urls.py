from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('articles', views.ArticleViewSet, basename='articles')
urlpatterns = [
    path('picture', views.PictureView.as_view(), name='picture'),
]
urlpatterns += router.urls
