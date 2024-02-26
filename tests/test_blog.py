import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from faker import Faker
from django.urls import reverse

user=get_user_model()

data={
    'email':'samples@gmail.com',
    'password':'1234!@#$'
}

fake=Faker() 



@pytest.fixture
def api_client():
    client=APIClient()
    return client


@pytest.fixture
def create_user():
    common_user=user.objects.create_user(**data)
    common_user.is_confirm=True
    common_user.save()
    return common_user

@pytest.fixture
def create_superuser():
    super_user=user.objects.create_superuser(**data)
    super_user.is_confirm=True
    super_user.save()
    return super_user
  


@pytest.mark.django_db
class Test_Blog:
   
    def test_blog_create_with_admin(self,api_client,create_superuser):
        """
            create blog if user is super_user and authorized 
        """
        create_user=create_superuser
        url=reverse("Blog:BlogApi:create_blog")
        for _ in range(10):
            data_blog={
                "operator_id":create_user,
                "title":fake.name(),
                "shortdescription":fake.text(),
                "body":fake.text()
            }
         
            url_login=reverse("account:AccountApi:login")  
            response_login=api_client.post(url_login,data)
            print(response_login)
            response=api_client.post(url,data_blog)
            assert response_login.status_code==200
            assert response.status_code==201

    def test_blog_create_with_common_user(self,api_client,create_user):
        """
            create blog if user is not super_user and authorized 
         """

        create_user=create_user
        url=reverse("Blog:BlogApi:create_blog")
        data_blog={
                "operator_id":create_user,
                "title":fake.name(),
                "shortdescription":fake.text(),
                "body":fake.text()
            }
         
        url_login=reverse("account:AccountApi:login")  
        response_login=api_client.post(url_login,data)
        response=api_client.post(url,data_blog)
        assert response_login.status_code==200
        assert response.status_code==403

    def test_blog_create_with_superuser_unauthorized(self,api_client,create_superuser):
        """
            create blog if user is super_user and unathorized 
         """

        create_user=create_superuser
        url=reverse("Blog:BlogApi:create_blog")
        data_blog={
                "operator_id":create_user,
                "title":fake.name(),
                "shortdescription":fake.text(),
                "body":fake.text()
            }
         
        response=api_client.post(url,data_blog)
        assert response.status_code==401

    

