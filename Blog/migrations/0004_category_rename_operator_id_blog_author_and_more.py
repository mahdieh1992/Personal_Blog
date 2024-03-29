# Generated by Django 4.0.10 on 2024-02-25 19:26

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Blog", "0003_alter_blog_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("title", models.CharField(max_length=200)),
            ],
        ),
        migrations.RenameField(
            model_name="blog",
            old_name="operator_id",
            new_name="author",
        ),
        migrations.AlterField(
            model_name="blog",
            name="expire_date",
            field=models.DateField(default=datetime.date(2026, 2, 25)),
        ),
        migrations.AddField(
            model_name="blog",
            name="categories",
            field=models.ManyToManyField(
                related_name="blog", to="Blog.category"
            ),
        ),
    ]
