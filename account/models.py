from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .manager import CustomUserManager
from django.utils import timezone
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.html import format_html
from rest_framework.authtoken.models import Token

# Create your models here.

date_now = date.today()
year_add = date_now.year + 2
date_now = date_now.replace(year=year_add)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Use this option if i want to start from scratch by creating my own,completely new user model.

    """

    email = models.EmailField(_("email address"), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    is_confirm = models.BooleanField(default=False)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    expire_date = models.DateField(default=date_now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    """
    model profile for register user extra info
    """

    user_id = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    image = models.ImageField(null=True, upload_to="Image/acount", blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    national_code = models.CharField(max_length=10, null=False, blank=True)

    def __str__(self) -> str:
        return f"{self.user_id}"

    def show_image(self):
        """
        show image in list_display admin
        """
        if self.image:
            return format_html(
                f"<img src='{self.image.url}', width='70', height='70'>"
            )
        else:
            return format_html(f"<h1>Not exists image</h1>")


@receiver(post_save, sender=CustomUser)
def register_profile(sender, instance, created, **kwargs):
    """
    register created user_id in profile when user created
    """
    if created:
        Profile.objects.create(user_id=instance)
        Token.objects.create(user=instance)

