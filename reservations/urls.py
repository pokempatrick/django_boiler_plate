from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter
router = DefaultRouter()

router.register('reservations', views.ReservationViewSet,
                basename='reservations')
# urlpatterns = [
#     path('picture', views.PictureView.as_view(), name='picture'),
# ]
urlpatterns = router.urls
