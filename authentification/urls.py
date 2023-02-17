from django.urls import path
from . import views

urlpatterns = [
    path('register', views.ResgisterAPIView.as_view(), name='register'),
    path('login', views.LoginAPIView.as_view(), name='login'),
    path('user', views.AuthUserAPIView.as_view(), name='user'),
    path('email_sign', views.EmailSign.as_view(), name='email_sign'),
    path('email_code', views.CodeVerification.as_view(), name='email_code'),
]
