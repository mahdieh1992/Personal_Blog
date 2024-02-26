from django.urls import path
from .views import (
    RegisterUserView,
    SendEmail,
    VerifyRegisterEmailView,
    ResendVerifyEmailRegister,
    LoginUserView,
    LogoutUserView,
    ProfileUser
    
)

app_name = "AccountApi"
urlpatterns = [
    path("register/", RegisterUserView.as_view(), name="register"),
    path(
        "register/verify_register/<str:token>",
        VerifyRegisterEmailView.as_view(),
        name="verify_register",
    ),
    path(
        "register/Resend_token/",
        ResendVerifyEmailRegister.as_view(),
        name="testSendEmail",
    ),
    path("testSendEmail/", SendEmail.as_view(), name="testSendEmail"),
    path("login/",LoginUserView.as_view(),name="login"),
    path("logout/",LogoutUserView.as_view(),name="logout"),
    path("profile/",ProfileUser.as_view(),name="profile")
]
