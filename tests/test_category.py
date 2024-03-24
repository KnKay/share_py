import pytest

from django.urls import include, path, reverse
from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from share_app.models import Category
from conftest import Clients

class CategoryTests(APITestCase, URLPatternsTestCase, Clients):
    urlpatterns = [
        path('', include('share.urls')),
    ]

    def setUp(self):
        # Set up data for the whole TestCase
        self.category =  Category.objects.create(name="Test")

    def test_anon_read(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('categories-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        url = reverse('categories-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test")

    def test_anon_create(self):
        url = reverse('categories-list')
        data = {'name': 'posted'}
        response = self.client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(len(response.data), 1)

    def test_admin_read(self):
        """
        Ensure we can create a new account object.
        """
        url = reverse('categories-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        url = reverse('categories-detail', args=[1])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Test")

    def test_admin_create(self):
        # Include an appropriate `Authorization:` header on all requests.
        url = reverse('categories-list')
        data = {'name': 'posted', "description":"Need to be set"}
        response = self.admin_client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


    def test_user_create(self):
        # Include an appropriate `Authorization:` header on all requests.
        url = reverse('categories-list')
        data = {'name': 'posted', "description":"Need to be set"}
        response = self.user_client.post(url,data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
