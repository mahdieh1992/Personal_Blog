# Generated by Django 4.0.10 on 2024-02-24 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Blog",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                ("shortdescription", models.CharField(max_length=250)),
                ("body", models.TextField()),
                (
                    "image",
                    models.ImageField(blank=True, upload_to="Image/blog"),
                ),
                ("is_deleted", models.BooleanField(default=False)),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                (
                    "expire_date",
                    models.DateField(default=datetime.date(2026, 2, 24)),
                ),
                ("modify_date", models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
