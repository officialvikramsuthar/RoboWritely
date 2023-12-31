# Generated by Django 4.2.4 on 2023-08-17 07:40

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Content",
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
                ("keywords", models.CharField(max_length=200)),
                ("heading", models.CharField(blank=True, max_length=200, null=True)),
                ("content", models.TextField()),
                ("slug", models.SlugField(unique=True)),
                ("timestamp", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
