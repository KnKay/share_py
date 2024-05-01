import pytest
import random

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from share_app.models import Item, Category, Location
from conftest import Clients

class ItemTests(APITestCase, URLPatternsTestCase, Clients):
    urlpatterns = [
        path('', include('share.urls')),
    ]

    def setUp(self):
        # Set up data for the whole TestCase
        self.location = Location.objects.create(city="Hamburg", post_code="22525")
        self.category =  Category.objects.create(name="Test2")
        self.item = Item.objects.create(
            description="An awesome thing to share",
            header="This is short",
            category = self.category,
            location = self.location
        )

    def test_anon_read(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('items-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        url = reverse('items-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["header"], "This is short")

    def test_annon_no_write(self):
        pass


    def test_user_create(self):
        # Include an appropriate `Authorization:` header on all requests.
        pass
