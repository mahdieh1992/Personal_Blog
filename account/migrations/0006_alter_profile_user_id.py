# Generated by Django 4.0.10 on 2024-02-23 12:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_customuser_expire_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="user_id",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
