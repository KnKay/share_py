import pytest
import random

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

    def test_annon_no_write(self):
        url = reverse('locations-list')
        data = {'city': 'Hamburg', 'post_code': 13371}
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), 1)


    def test_user_create(self):
        # Include an appropriate `Authorization:` header on all requests.
        rand = random.randrange(10000, 100000,)
        url = reverse('locations-list')
        data = {'city': 'Hamburg', "post_code":rand}
        response = self.user_client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert any(x["post_code"] == rand and x["city"] == "Hamburg" for x in response.data)
        # Creating the same should not create a new entry
        data = {'city': 'Hamburg', "post_code":rand}
        update = self.user_client.post(url,data, format='json')
        self.assertEqual(update.status_code, status.HTTP_202_ACCEPTED)
        response2 = self.client.get(url, format='json')
        assert response2.data == response.da