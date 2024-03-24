import pytest

from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken



@pytest.fixture(autouse=True)
def admin_client(db):
    admin = User.objects.get_or_create(username = 'admin', is_staff=True)[0]
    client = APIClient()
    refresh = RefreshToken.for_user(admin)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

@pytest.fixture(autouse=True)
@pytest.mark.django_db
def user_client():
    user = User.objects.get_or_create(username='user')[0]
    client = APIClient()
    refresh = RefreshToken.for_user(user)
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    return client

class Clients():
    # toDo: this seems to be wrong...
    @pytest.fixture(autouse=True)
    def _request_clients(self, admin_client, user_client):
        self.admin_client = admin_client
        self.user_client = user_client
