# Generated by Django 4.0.10 on 2024-02-27 14:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0004_category_rename_operator_id_blog_author_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="blog",
            name="expire_date",
            field=models.DateField(default=datetime.date(2026, 2, 27)),
        ),
    ]
