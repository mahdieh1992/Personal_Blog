import pytest
from django.contrib.auth import get_user_model
from faker import Faker
from rest_framework.test import APIClient
from django.urls import reverse
from rest_framework.authtoken.models import Token

fake = Faker()
global user
user = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


data = {"email": "example@gmail.com", "password": "1234!@#$"}


@pytest.fixture
def create_user():
    getuser = user.objects.create_user(
        email=data["email"], password=data["password"], is_confirm=True
    )
    return getuser.id


@pytest.mark.django_db
class TestAccount:
    url = reverse("account:AccountApi:register")

    def test_register_get_url(self, api_client):
        """
        checking url is  correct
        """
        url = self.url
        response = api_client.get(url)
        assert response.status_code == 405

    def test_register_user_post(self, api_client):
        """
        checking create user succesfuly
        """
        data = {
            "email": "test@gmail.com",
            "password": "1234!@#$",
            "ConfirmPassword": "1234!@#$",
        }
        url = self.url
        response = api_client.post(url, data)
        assert response.status_code == 201
        assert user.objects.filter(email=data["email"])

    def test_create_user_exists(self, api_client, create_user):
        """
        checking user exists during create
        """
        url = self.url
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_create_user_simple_password(self, api_client):
        """
        If the password is not complex
        """
        data = {
            "email": "test1@gmail.com",
            "password": "123",
            "ConfirmPassword": "123",
        }
        url = self.url
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_create_user_password_not_match(self, api_client):
        url = self.url
        data = {
            "email": "example@gmail.com",
            "password": "1234!@#$",
            "ConfirmPassword": "1234^&*$",
        }
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_login_user_invalid(self, api_client):
        """
        if email or password invalid
        """
        url = reverse("account:AccountApi:login")
        user1 = {"email": "sample@gmail.com", "password": "1234!@#$"}
        response = api_client.post(url, user1)
        assert response.status_code == 400
        assert b"email or password invalid" in response.content

    def test_Edit_profile_Unauthorized(self, api_client):
        """
        test for edit user information if user Unauthorized it returns code 401
        """
        url = reverse("account:AccountApi:profile")
        response = api_client.get(url)
        assert response.status_code == 401

    def test_login_user_not_exists(self, api_client):
        """
        login if user is not exists
        """
        url = reverse("account:AccountApi:login")
        response = api_client.post(url, data)
        assert response.status_code == 400

    def test_login_user_exists_gettoken(self, api_client, create_user):
        object_user = create_user
        """
           test login user with assert token for user
        """
        url = reverse("account:AccountApi:login")
        response = api_client.post(url, data)
        token = Token.objects.get(user=object_user)
        assert response.status_code == 200
        assert token is not None
