from django.urls import path, include
from .views import RegisterUser, LoginUser

app_name = "account"

urlpatterns = [
    path("register", RegisterUser.as_view(), name="register"),
    path("login", LoginUser.as_view(), name="login"),
    path("api/v1/", include("account.api.v1.urls"), name="api"),
]
