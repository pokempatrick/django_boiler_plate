from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('reservations', views.ReservationViewSet,
                basename='reservations')
urlpatterns = [
    path('validation/reservations/<str:pk>/', views.ValidationAPIView.as_view(),
         name='validation_reservation'),
]
urlpatterns += router.urls
