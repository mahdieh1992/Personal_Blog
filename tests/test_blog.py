import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker
from django.urls import reverse
from Blog.models import Category

user = get_user_model()

data = {"email": "samples@gmail.com", "password": "1234!@#$"}

fake = Faker()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def create_user():
    common_user = user.objects.create_user(**data)
    common_user.is_confirm = True
    common_user.save()
    return common_user


@pytest.fixture
def create_superuser():
    super_user = user.objects.create_superuser(**data)
    super_user.is_confirm = True
    super_user.save()
    return super_user


@pytest.mark.django_db
class Test_Blog:

    def test_category_create(self, api_client, create_superuser):
        """
        test create category user must be logged in and is admin
        """
        url_login = reverse("account:AccountApi:login")
        url = reverse("Blog:BlogApi:category")
        data_category = {"title": "test"}
        response_login = api_client.post(url_login, data)
        response = api_client.post(url, data_category)
        assert response_login.status_code == 200
        assert response.status_code == 201

    def test_category_list(self, api_client, create_superuser):
        """
        show list created
        """
        url_login = reverse("account:AccountApi:login")
        url = reverse("Blog:BlogApi:category")
        response_login = api_client.post(url_login, data)
        response = api_client.get(url)
        assert response.status_code == 200
        assert response_login.status_code == 200

    def test_blog_create_with_admin(self, api_client, create_superuser):
        create_superuser = create_superuser
        """
        create blog if user is super_user and authorized8
        """
        cat = Category.objects.create(title="test")
        url = reverse("Blog:BlogApi:create_blog")
        for _ in range(10):
            data_blog = {
                "author": create_superuser.email,
                "categories": [cat.id],
                "title": fake.name(),
                "shortdescription": fake.name(),
                "body": fake.text(),
                "expire_date": "2024-08-09",
                "modify_date": "2024-08-09",
            }
            print(data_blog)
            url_login = reverse("account:AccountApi:login")
            response_login = api_client.post(url_login, data)
            response = api_client.post(url, data_blog)
            assert response.status_code == 201

    def test_blog_create_with_common_user(self, api_client, create_user):
        """
        create blog if user is not super_user and authorized
        """

        create_user = create_user
        url = reverse("Blog:BlogApi:create_blog")
        data_blog = {
            "author": create_user,
            "title": fake.name(),
            "shortdescription": fake.text(),
            "body": fake.text(),
        }

        url_login = reverse("account:AccountApi:login")
        response_login = api_client.post(url_login, data)
        response = api_client.post(url, data_blog)
        assert response_login.status_code == 200
        assert response.status_code == 403

    def test_blog_create_with_superuser_unauthorized(
        self, api_client, create_superuser
    ):
        """
        create blog if user is super_user and unathorized
        """

        create_user = create_superuser
        url = reverse("Blog:BlogApi:create_blog")
        data_blog = {
            "author": create_user,
            "title": fake.name(),
            "shortdescription": fake.text(),
            "body": fake.text(),
        }

        response = api_client.post(url, data_blog)
        assert response.status_code == 401

    def test_blog_list(self, api_client):
        url = reverse("Blog:BlogApi:blog-list")
        response = api_client.get(url)
        assert response.status_code == 200
