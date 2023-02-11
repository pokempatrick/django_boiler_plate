from django.urls import path
from . import views

urlpatterns = [
    path('register', views.ResgisterAPIView.as_view(), name='register'),
]
