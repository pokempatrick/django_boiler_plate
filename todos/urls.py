from django.urls import path, re_path
from . import views

urlpatterns = [
    path('<str:id>', views.TodoAPIView.as_view(), name='todo'),
    path('', views.TodoAPIView.as_view(), name='todo'),
]
