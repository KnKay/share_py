import pytest

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from share_app.models import Location
from conftest import Clients

class LocationTests(APITestCase, URLPatternsTestCase, Clients):
    urlpatterns = [
        path('', include('share.urls')),
    ]

    def setUp(self):
        # Set up data for the whole TestCase
        self.category =  Location.objects.create(city="Hamburg", post_code="22525")

    def test_anon_read(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('locations-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        url = reverse('locations-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["city"], "Hamburg")
