# Generated by Django 4.0.10 on 2024-02-24 13:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0007_alter_profile_user_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="expire_date",
            field=models.DateField(default=datetime.date(2026, 2, 24)),
        ),
    ]