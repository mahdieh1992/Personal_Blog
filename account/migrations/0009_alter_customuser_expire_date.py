# Generated by Django 4.0.10 on 2024-02-25 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0008_alter_customuser_expire_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="expire_date",
            field=models.DateField(default=datetime.date(2026, 2, 25)),
        ),
    ]
