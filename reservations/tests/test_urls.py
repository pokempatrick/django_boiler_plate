from django.test import SimpleTestCase
from django.urls import reverse, resolve

from reservations.views import ReservationViewSet, ValidationAPIView


class TestUrls(SimpleTestCase):
    def test_reservation_url_resolves(self):
        url_detail = reverse('reservations-detail', args=["15"])
        url_list = reverse('reservations-list')
        validation_url = reverse('validation_reservation', args=["12"])

        self.assertEquals(resolve(url_detail).func.cls, ReservationViewSet)
        self.assertEquals(resolve(url_list).func.cls, ReservationViewSet)
        self.assertEquals(
            resolve(validation_url).func.view_class, ValidationAPIView)
